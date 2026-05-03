import time
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

CATEGORY_RSS = {
    "it": "https://news.naver.com/section/rss?sid=105",
    "economy": "https://news.naver.com/section/rss?sid=101",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def _get_article_content(url: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for selector in ["#dic_area", "#articleBodyContents", ".newsct_article"]:
            tag = soup.select_one(selector)
            if tag:
                for unwanted in tag.select("script, style, .u_likeit_layer"):
                    unwanted.decompose()
                text = tag.get_text(separator="\n", strip=True)
                return text[:3000]
    except Exception:
        pass
    return ""


def _parse_rss(url: str) -> list[dict]:
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"dc": "http://purl.org/dc/elements/1.1/"}
    items = root.findall(".//item")
    results = []
    for item in items:
        results.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "summary": (item.findtext("description") or "").strip(),
            "published": (item.findtext("pubDate") or "").strip(),
        })
    return results


def crawl_naver_news(category: str = "it", max_articles: int = 3) -> list[dict]:
    url = CATEGORY_RSS.get(category, CATEGORY_RSS["it"])
    entries = _parse_rss(url)

    articles = []
    for entry in entries[:max_articles]:
        content = _get_article_content(entry["link"])
        articles.append(
            {
                "title": entry["title"],
                "link": entry["link"],
                "summary": entry["summary"],
                "content": content or entry["summary"],
                "published": entry["published"],
                "category": category,
            }
        )
        time.sleep(0.5)

    return articles
