import requests, re, os
from datetime import datetime

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "result/iptv.m3u"
CATEGORIES = ["CCTV", "卫视", "地方", "体育", "电影", "少儿"]

def fetch_sources():
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def download_content(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

def parse_streams(s):
    return re.findall(r'#EXTINF:-1.*?,(.*?)\n(https?://[^\s]+)', s, re.IGNORECASE)

def categorize(name):
    return next((cat for cat in CATEGORIES if cat in name), "其它")

def process_and_save(streams):
    seen = set()
    groups = {}
    for name, url in streams:
        if url in seen: continue
        seen.add(url)
        cat = categorize(name)
        groups.setdefault(cat, []).append((name, url))

    os.makedirs("result", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in sorted(groups):
            f.write(f"\n# ------ {cat} ------\n")
            for name, url in groups[cat]:
                f.write(f"#EXTINF:-1,{name}\n{url}\n")
    print(f"Saved {len(seen)} unique streams.")

def main():
    print(f"UTC start: {datetime.utcnow()}")
    urls = fetch_sources()
    streams = []
    for u in urls:
        content = download_content(u)
        if content:
            streams += parse_streams(content)
    process_and_save(streams)

if __name__ == "__main__":
    main()
