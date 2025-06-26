import requests
import re
import os
from datetime import datetime

# 文件路径
SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "result/iptv.m3u"
CATEGORIES = ["CCTV", "卫视", "地方", "体育", "电影", "少儿"]

def fetch_sources():
    urls = []
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def download_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"下载失败: {url} | 错误: {e}")
        return ""

def parse_streams(content):
    pattern = re.compile(r'#EXTINF:-1.*?,(.*?)\n(https?:\/\/[^\s]+)', re.IGNORECASE)
    return pattern.findall(content)

def categorize(name):
    for cat in CATEGORIES:
        if cat in name:
            return cat
    return "其它"

def process_and_save(all_streams):
    seen_urls = set()
    categorized = {}

    for name, url in all_streams:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        cat = categorize(name)
        categorized.setdefault(cat, []).append((name, url))

    os.makedirs("result", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in sorted(categorized.keys()):
            f.write(f"\n# ------ {cat} ------\n")
            for name, url in categorized[cat]:
                f.write(f"#EXTINF:-1,{name}\n{url}\n")

    print(f"共保存频道: {len(seen_urls)}")

def main():
    print(f"开始时间: {datetime.utcnow()} UTC")
    urls = fetch_sources()
    all_streams = []
    for url in urls:
        content = download_content(url)
        if content:
            all_streams.extend(parse_streams(content))
    process_and_save(all_streams)

if __name__ == "__main__":
    main()
