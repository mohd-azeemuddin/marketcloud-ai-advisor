import json, re, time, hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

BASE = "https://marketcloud.co.uk/"
OUT = Path("data/raw"); OUT.mkdir(parents=True, exist_ok=True)
MAX_PAGES = 70
HEADERS = {"User-Agent": "MarketCloudAdvisorBot/0.1 (internship demo)"}
norm = lambda h: h.replace("www.", "")

def clean(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "form"]):
        t.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    lines = [re.sub(r"\s+", " ", l).strip() for l in soup.get_text("\n").split("\n")]
    return title, "\n".join(l for l in lines if len(l) > 2)

def crawl():
    host = norm(urlparse(BASE).netloc)
    queue, seen = [BASE], set()
    while queue and len(seen) < MAX_PAGES:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
        except Exception as e:
            print("skip", url, e); continue
        if r.status_code != 200 or "text/html" not in r.headers.get("content-type", ""):
            continue
        for a in BeautifulSoup(r.text, "html.parser").find_all("a", href=True):
            link = urldefrag(urljoin(url, a["href"]))[0]
            if (norm(urlparse(link).netloc) == host and link not in seen
                    and not re.search(r"\.(pdf|jpg|png|zip)$", link, re.I)):
                queue.append(link)
        title, text = clean(r.text)
        if len(text) > 200:
            name = hashlib.md5(url.encode()).hexdigest()[:10]
            (OUT / f"{name}.json").write_text(
                json.dumps({"url": url, "title": title, "text": text}, ensure_ascii=False, indent=1),
                encoding="utf-8")
            print("saved", url, len(text))
        time.sleep(1)

if __name__ == "__main__":
    crawl()