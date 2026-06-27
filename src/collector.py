"""
AI Business Opportunity Collector
Fetches: AI tool launches, trending repos, tech news, business opportunities
Sources: Product Hunt, GitHub Trending, Reddit AI, Tech news, Vietnam news
"""
import feedparser
import requests
import re
from datetime import datetime, timedelta
from typing import List, Dict


class OpportunityCollector:
    def __init__(self):
        self.articles = []
        self.cutoff_date = datetime.now() - timedelta(hours=48)

    PRODUCT_HUNT_RSS = [
        {"name": "Product Hunt (AI)", "url": "https://www.producthunt.com/topics/artificial-intelligence/feed"},
        {"name": "Product Hunt (Productivity)", "url": "https://www.producthunt.com/topics/productivity/feed"},
        {"name": "Product Hunt (Developer Tools)", "url": "https://www.producthunt.com/topics/developer-tools/feed"},
        {"name": "Product Hunt (Marketing)", "url": "https://www.producthunt.com/topics/marketing/feed"},
        {"name": "Product Hunt (All)", "url": "https://www.producthunt.com/feed"},
    ]

    REDDIT_RSS = [
        {"name": "Reddit r/artificial", "url": "https://www.reddit.com/r/artificial/.rss"},
        {"name": "Reddit r/SideProject", "url": "https://www.reddit.com/r/SideProject/.rss"},
        {"name": "Reddit r/startups", "url": "https://www.reddit.com/r/startups/.rss"},
    ]

    TECH_RSS = [
        {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
        {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
        {"name": "Wired", "url": "https://www.wired.com/feed/rss"},
        {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
        {"name": "Ars Technica", "url": "https://arstechnica.com/feed/"},
    ]

    VIETNAM_RSS = [
        {"name": "VnExpress (Tech)", "url": "https://vnexpress.net/rss/so-hoa.rss"},
        {"name": "VnExpress (Business)", "url": "https://vnexpress.net/rss/kinh-doanh.rss"},
        {"name": "Tuoi Tre (Tech)", "url": "https://tuoitre.vn/rss/cong-nghe.rss"},
        {"name": "Thanh Nien (Tech)", "url": "https://thanhnien.vn/rss/cong-nghe.rss"},
        {"name": "VietnamNet (Business)", "url": "https://vietnamnet.vn/rss/kinh-doanh.rss"},
    ]

    BUSINESS_RSS = [
        {"name": "Crunchbase Daily", "url": "https://news.crunchbase.com/feed/"},
    ]

    def fetch_rss(self, source: Dict) -> List[Dict]:
        articles = []
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:10]:
                published = self._parse_date(entry)
                if published and published < self.cutoff_date:
                    continue
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": self._clean_html(entry.get("summary", entry.get("description", "")))[:400],
                    "source": source["name"],
                    "published": published or datetime.now(),
                    "category": self._categorize(source["name"]),
                    "type": "article",
                })
        except Exception as e:
            print(f"  RSS Error {source['name']}: {e}")
        return articles

    def fetch_hacker_news(self) -> List[Dict]:
        articles = []
        try:
            resp = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
            story_ids = resp.json()[:15]
            for sid in story_ids:
                story_resp = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
                story = story_resp.json()
                if story and story.get("title"):
                    articles.append({
                        "title": story["title"],
                        "link": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                        "summary": "",
                        "source": "Hacker News",
                        "published": datetime.now(),
                        "category": "technology",
                        "type": "article",
                    })
        except Exception as e:
            print(f"  HN Error: {e}")
        return articles

    def fetch_github_trending(self) -> List[Dict]:
        articles = []
        headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        try:
            query = "stars:>100 pushed:>2024-01-01 language:python OR language:typescript"
            resp = requests.get(
                f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=15",
                headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for repo in data.get("items", [])[:15]:
                    desc = repo.get("description", "") or ""
                    articles.append({
                        "title": f"GitHub: {repo['full_name']} - {desc[:100]}",
                        "link": repo["html_url"],
                        "summary": f"Stars: {repo.get('stargazers_count', 0)} | {desc[:200]}",
                        "source": "GitHub Trending",
                        "published": datetime.now(),
                        "category": "ai_tools",
                        "type": "github_repo",
                        "stars": repo.get("stargazers_count", 0),
                    })
        except Exception as e:
            print(f"  GitHub Error: {e}")
        return articles

    def _parse_date(self, entry):
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
        except:
            pass
        return datetime.now()

    def _clean_html(self, raw: str) -> str:
        clean = re.sub(r'<[^>]+>', '', raw)
        return clean.strip()

    def _categorize(self, source_name: str) -> str:
        name = source_name.lower()
        if "product hunt" in name:
            return "ai_tools"
        if "reddit" in name:
            return "community"
        if "github" in name:
            return "ai_tools"
        if any(x in name for x in ["vnexpress", "tuoi tre", "thanh nien", "vietnamnet"]):
            return "vietnam"
        if any(x in name for x in ["techcrunch", "verge", "wired", "ars", "hacker"]):
            return "technology"
        if "venturebeat" in name:
            return "ai_landscape"
        if "crunchbase" in name:
            return "funding"
        if "mit" in name:
            return "research"
        return "business"

    def collect_all(self) -> List[Dict]:
        all_articles = []

        print("[1/6] Fetching AI tool launches from Product Hunt...")
        for source in self.PRODUCT_HUNT_RSS:
            articles = self.fetch_rss(source)
            all_articles.extend(articles)
            print(f"  {source['name']}: {len(articles)} launches")

        print("[2/6] Fetching community discussions from Reddit...")
        for source in self.REDDIT_RSS:
            articles = self.fetch_rss(source)
            all_articles.extend(articles)
            print(f"  {source['name']}: {len(articles)} posts")

        print("[3/6] Fetching trending GitHub repositories...")
        articles = self.fetch_github_trending()
        all_articles.extend(articles)
        print(f"  GitHub Trending: {len(articles)} repos")

        print("[4/6] Fetching tech news...")
        for source in self.TECH_RSS:
            articles = self.fetch_rss(source)
            all_articles.extend(articles)
            print(f"  {source['name']}: {len(articles)} articles")

        print("[5/6] Fetching Vietnam news...")
        for source in self.VIETNAM_RSS:
            articles = self.fetch_rss(source)
            all_articles.extend(articles)
            print(f"  {source['name']}: {len(articles)} articles")

        print("[6/6] Fetching Hacker News...")
        articles = self.fetch_hacker_news()
        all_articles.extend(articles)
        print(f"  Hacker News: {len(articles)} stories")

        all_articles.sort(key=lambda x: x["published"], reverse=True)

        by_category = {}
        for a in all_articles:
            cat = a["category"]
            by_category[cat] = by_category.get(cat, 0) + 1

        print(f"\n{'='*50}")
        print(f"TOTAL OPPORTUNITIES: {len(all_articles)}")
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")
        print(f"{'='*50}\n")

        return all_articles


if __name__ == "__main__":
    collector = OpportunityCollector()
    articles = collector.collect_all()
    print(f"\nFirst 5 articles:")
    for a in articles[:5]:
        print(f"- [{a['category']}] {a['title'][:90]}...")

