#!/usr/bin/env python3
import os, json, re, requests

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE  = os.path.join(BASE_DIR, "items.json")
QUERIES_FILE= os.path.join(BASE_DIR, "queries.txt")

def enrich_stub(title):
    proj = title.replace(" ", "-").lower()
    # 1) Try PyPI
    try:
        r = requests.get(f"https://pypi.org/pypi/{proj}/json", timeout=5)
        if r.ok:
            info = r.json().get("info",{})
            summary = info.get("summary","").strip()
            urls    = info.get("project_urls") or {}
            url     = urls.get("Source") or urls.get("Homepage") or info.get("home_page","")
            return summary, url
    except:
        pass
    # 2) Fallback to GitHub search
    try:
        q  = "+".join(title.split())
        gh = requests.get(f"https://api.github.com/search/repositories?q={q}+in:name,description", timeout=5)
        if gh.ok and gh.json().get("items"):
            repo = gh.json()["items"][0]
            return repo.get("description","").strip(), repo.get("html_url","")
    except:
        pass
    return "", ""

def main():
    # load or init
    try:
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except:
        items = []

    existing = {item['title'] for item in items}

    # ensure every query is stubbed
    with open(QUERIES_FILE, 'r', encoding='utf-8') as f:
        queries = [q.strip() for q in f if q.strip()]

    added = []
    for q in queries:
        if q not in existing:
            items.append({
                "title": q,
                "content": "",
                "tags": [w for w in re.split(r"\W+", q.lower()) if w],
                "language": None,
                "price": 0,
                "download_url": ""
            })
            existing.add(q)
            added.append(q)

    # now enrich any item missing content or URL
    enriched = []
    for item in items:
        if not item.get("content") or not item.get("download_url"):
            summary, url = enrich_stub(item["title"])
            if summary and not item.get("content"):
                item["content"] = summary
            if url and not item.get("download_url"):
                item["download_url"] = url
            if summary or url:
                enriched.append(item["title"])

    # save back
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)

    if added:
        print(f"✅ Added {len(added)} new stubs:")
        for q in added:
            print("  •", q)
    if enriched:
        print(f"✅ Enriched {len(enriched)} entries:")
        for t in enriched:
            print("  •", t)
    if not added and not enriched:
        print("ℹ️  No changes—everything up to date.")

if __name__=="__main__":
    main()
