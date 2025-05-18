#!/usr/bin/env python3
import os, re, sys, json, argparse, subprocess, requests
from datetime import datetime
from collections import defaultdict
from googlesearch import search as google_search

# ──────────────────────────────────────────────────────────────────────────────
# Config
ARCHIVE_EXTS = (".zip", ".tar.gz", ".tar", ".tgz", ".tar.bz2")
IMAGE_EXTS   = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg")
# ──────────────────────────────────────────────────────────────────────────────

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_archive(url): return url.lower().endswith(ARCHIVE_EXTS)
def is_image(url):   return url.lower().endswith(IMAGE_EXTS)
def is_py(url):      return url.lower().endswith(".py")

def download(url, dst):
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        total = int(r.headers.get("Content-Length","0") or 0)
        done = 0
        with open(dst, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk); done += len(chunk)
        print(f"[{timestamp()}] Downloaded {done}/{total} → {dst}")
    except Exception as e:
        print(f"[{timestamp()}] ❌ {e}")

def google_fallback(q,n): return list(google_search(q, num_results=n))

class SearchEngine:
    def __init__(self, items):
        self.items = items
        self.title_index = {item["title"].lower(): item for item in items}

    def search(self, query, top_n=5):
        q = query.lower().strip()
        # 1) Exact title match
        if q in self.title_index:
            return [self.title_index[q]]
        # 2) Keyword match: any item whose title contains all words
        toks = [w for w in re.split(r"\W+", q) if w]
        res = []
        for item in self.items:
            t = item["title"].lower()
            if all(tok in t for tok in toks):
                res.append(item)
                if len(res) >= top_n:
                    break
        return res

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-i","--items",      default="items.json")
    p.add_argument("-d","--download-dir", default=os.path.expanduser("~/Downloads"))
    p.add_argument("-n","--top-n",      type=int, default=5)
    p.add_argument("-T","--test-file",  default=None)
    args = p.parse_args()

    # Load items.json
    try:
        items = json.load(open(args.items, encoding="utf-8"))
    except:
        print(f"[{timestamp()}] ⚠️ could not load {args.items}")
        items = []

    engine = SearchEngine(items)
    os.makedirs(args.download_dir, exist_ok=True)

    # Batch test mode
    if args.test_file:
        qs = [l.strip() for l in open(args.test_file, encoding="utf-8") if l.strip()]
        print(f"[{timestamp()}] Running {len(qs)} test queries...")
        for q in qs:
            res = engine.search(q, top_n=args.top_n)
            status = "Local" if res else "Fallback"
            top = res[0]["title"] if res else "<none>"
            print(f"[{timestamp()}] {status:8} | {q:<60} → {top}")
        return

    # Interactive
    print(f"[{timestamp()}] Enter search (empty to exit)")
    while True:
        q = input("Search> ").strip()
        if not q:
            print(f"[{timestamp()}] Bye!"); break

        print(f"[{timestamp()}] Searching → {q}")
        res = engine.search(q, top_n=args.top_n)
        if res:
            print(f"[{timestamp()}] {len(res)} local result(s):")
            for i,item in enumerate(res,1):
                print(f"  {i}. {item['title']} price:{item.get('price',0)}")
                if item.get("price",0)==0 and item.get("download_url"):
                    dst = os.path.join(args.download_dir, os.path.basename(item["download_url"]))
                    print(f"[{timestamp()}] ↓ fetching → {dst}")
                    download(item["download_url"], dst)
        else:
            print(f"[{timestamp()}] No local hits → Google")
            for url in google_fallback(q, args.top_n):
                print(f"[{timestamp()}] → {url}")

if __name__=="__main__":
    main()
