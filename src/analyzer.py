"""
AI Business Opportunity Analyzer - FREE version using Groq API
"""
import os
from groq import Groq
from typing import List, Dict
from datetime import datetime
from affiliate_links import AFFILIATE_LINKS, has_affiliate_link


class OpportunityAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    SYSTEM_PROMPT = """You are an elite AI Business Intelligence Analyst specializing in money-making opportunities.

Create a high-value "AI Opportunities Briefing" with these EXACT sections:

1. EXECUTIVE SUMMARY
- 3-4 bullets of the highest-value opportunities today

2. TODAY'S HOT AI TOOL LAUNCHES
For each tool: name, description, business opportunity, Opportunity Score 1-10, action step

3. TRENDING AI OPPORTUNITIES
- 2-3 emerging patterns and how to profit from them

4. VIETNAM MARKET SPOTLIGHT
- Key Vietnam tech/business developments

5. FUNDING & ACQUISITION ALERTS
- Recent funding rounds and what they signal

6. COMMUNITY BUZZ
- What builders and founders are discussing

7. AFFILIATE PICKS: TOOLS WITH REVENUE POTENTIAL
- Highlight 2-3 tools with specific money-making use cases

8. ACTION ITEMS
- 3 concrete things to do TODAY

RULES:
- Be SPECIFIC. Name exact tools, prices, dollar amounts.
- Explain WHO each tool is for and HOW they make money.
- Use bold for tool names and dollar amounts.
- Tone: Sharp, energetic, business-focused.
- Length: 1000-1500 words."""

    def _build_affiliate_context(self) -> str:
        tools = sorted([t for t in AFFILIATE_LINKS.keys() if "YOUR-ID" not in AFFILIATE_LINKS[t]])
        if not tools:
            tools = sorted(AFFILIATE_LINKS.keys())
        return "AFFILIATE PROGRAMS AVAILABLE:\n" + ", ".join(tools[:50])

    def analyze(self, articles: List[Dict]) -> str:
        input_text = self._format_articles(articles)
        affiliate_context = self._build_affiliate_context()

        print("Sending to Groq (FREE) for business analysis...")

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT + "\n\n" + affiliate_context},
                {"role": "user", "content": f"Create the AI Opportunities Briefing:\n\n{input_text}"}
            ],
            temperature=0.6,
            max_tokens=2500
        )

        briefing = response.choices[0].message.content
        print("Analysis complete!")
        return briefing

    def _format_articles(self, articles: List[Dict]) -> str:
        lines = [f"DAILY INTELLIGENCE - {datetime.now().strftime('%Y-%m-%d %H:%M')}", "=" * 50]

        by_category = {}
        for a in articles:
            cat = a.get("category", "general")
            by_category.setdefault(cat, []).append(a)

        cat_names = {
            "ai_tools": "AI TOOL LAUNCHES",
            "community": "COMMUNITY DISCUSSIONS",
            "technology": "TECHNOLOGY NEWS",
            "vietnam": "VIETNAM MARKET",
            "ai_landscape": "AI INDUSTRY",
            "funding": "FUNDING & INVESTMENT",
            "research": "RESEARCH",
            "business": "BUSINESS NEWS",
        }

        for category, items in sorted(by_category.items(), key=lambda x: -len(x[1])):
            name = cat_names.get(category, category.upper())
            lines.extend([f"\n{'='*40}", f"{name} ({len(items)} items)", f"{'='*40}"])

            for item in items[:10]:
                lines.append(f"\nTitle: {item['title']}")
                lines.append(f"Source: {item['source']}")
                if item.get("summary"):
                    lines.append(f"Summary: {item['summary'][:200]}")
                if item.get("stars"):
                    lines.append(f"Stars: {item['stars']}")
                for tool in AFFILIATE_LINKS:
                    if tool.lower() in item['title'].lower():
                        lines.append(f"[AFFILIATE: {tool}]")
                        break

        lines.extend([
            "\n\nAFFILIATE REFERENCE:",
            "HIGH COMMISSION (30-50%): Copy.ai (45%), Jasper (50%), Writesonic (30%), Notion (50%)",
            "MEDIUM (15-25%): SurferSEO (25%), Murf AI (20%), ElevenLabs (22%)",
            "ONE-TIME: Semrush ($200/sale), Grammarly ($20/signup)",
        ])

        return "\n".join(lines)

    def add_disclaimer(self, briefing: str) -> str:
        disclaimer = (
            "\n\n---\n"
            "*Some links are affiliate links. I earn commission at no cost to you."
            " I only recommend tools with genuine business value.*"
        )
        return briefing + disclaimer


if __name__ == "__main__":
    from collector import OpportunityCollector
    collector = OpportunityCollector()
    articles = collector.collect_all()
    analyzer = OpportunityAnalyzer()
    briefing = analyzer.analyze(articles)
    briefing = analyzer.add_disclaimer(briefing)
    print(briefing[:1000])
