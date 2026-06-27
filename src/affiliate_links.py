"""
Affiliate Link Manager - Replace YOUR-ID with your actual affiliate IDs
"""
import re

AFFILIATE_LINKS = {
    # === AI Writing ===
    "copy.ai": "https://www.copy.ai/?via=YOUR-ID",
    "jasper": "https://www.jasper.ai/?utm_source=YOUR-ID",
    "writesonic": "https://writesonic.com?via=YOUR-ID",
    "grammarly": "https://grammarly.go2cloud.org/aff_c?offer_id=YOUR-ID",
    "quillbot": "https://quillbot.com?ref=YOUR-ID",
    "frase": "https://www.frase.io/?via=YOUR-ID",

    # === AI Video ===
    "synthesia": "https://www.synthesia.io/?via=YOUR-ID",
    "invideo": "https://invideo.io?ref=YOUR-ID",
    "pictory": "https://pictory.ai?ref=YOUR-ID",
    "descript": "https://www.descript.com/?utm_source=YOUR-ID",
    "heygen": "https://www.heygen.com/?via=YOUR-ID",
    "runway": "https://runwayml.com/?ref=YOUR-ID",

    # === AI Voice ===
    "elevenlabs": "https://elevenlabs.io/?ref=YOUR-ID",
    "eleven labs": "https://elevenlabs.io/?ref=YOUR-ID",
    "murf": "https://murf.ai?ref=YOUR-ID",
    "murf ai": "https://murf.ai?ref=YOUR-ID",
    "otter.ai": "https://otter.ai/referral/YOUR-ID",
    "otter": "https://otter.ai/referral/YOUR-ID",

    # === AI Design ===
    "midjourney": "https://www.midjourney.com?ref=YOUR-ID",
    "canva": "https://www.canva.com/affiliate/YOUR-ID",
    "adcreative": "https://www.adcreative.ai/?ref=YOUR-ID",
    "adcreative.ai": "https://www.adcreative.ai/?ref=YOUR-ID",

    # === AI Marketing / SEO ===
    "semrush": "https://www.semrush.com/sem/?ref=YOUR-ID",
    "surfer seo": "https://surferseo.com?ref=YOUR-ID",
    "surferseo": "https://surferseo.com?ref=YOUR-ID",
    "ahrefs": "https://ahrefs.com?ref=YOUR-ID",

    # === AI Productivity ===
    "notion": "https://www.notion.so/product/affiliate?ref=YOUR-ID",
    "notion ai": "https://www.notion.so/product/affiliate?ref=YOUR-ID",
    "taskade": "https://www.taskade.com/?ref=YOUR-ID",

    # === AI Coding ===
    "github copilot": "https://github.com/features/copilot?ref=YOUR-ID",
    "tabnine": "https://www.tabnine.com/?ref=YOUR-ID",
    "replit": "https://replit.com/?ref=YOUR-ID",
    "cursor": "https://cursor.sh/?ref=YOUR-ID",

    # === AI Assistants ===
    "chatgpt": "https://chat.openai.com/invite/YOUR-ID",
    "claude": "https://claude.ai?ref=YOUR-ID",
    "perplexity": "https://www.perplexity.ai?ref=YOUR-ID",
    "poe": "https://poe.com?ref=YOUR-ID",
}


def get_affiliate_link(tool_name: str) -> str:
    return AFFILIATE_LINKS.get(tool_name.lower().strip(), "")


def has_affiliate_link(tool_name: str) -> bool:
    return tool_name.lower().strip() in AFFILIATE_LINKS


def inject_affiliate_links(text: str) -> str:
    modified = text
    for tool_name, url in AFFILIATE_LINKS.items():
        if "YOUR-ID" in url:
            continue
        pattern = re.compile(r'\b' + re.escape(tool_name) + r'\b', re.IGNORECASE)
        if pattern.search(modified) and url not in modified:
            modified += f"\n\n_[{tool_name}]({url})_"
    return modified


if __name__ == "__main__":
    print(f"Total tools in database: {len(AFFILIATE_LINKS)}")
    print("ACTION: Replace 'YOUR-ID' with your actual affiliate IDs!")
