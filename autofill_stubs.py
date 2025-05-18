#!/usr/bin/env python3
import os, json

BASE = os.path.dirname(__file__)
ITEMS = os.path.join(BASE, "items.json")

with open(ITEMS, "r", encoding="utf-8") as f:
    items = json.load(f)

changed = 0
for item in items:
    if not item.get("content", "").strip():
        title = item["title"]
        # Fill a minimal description
        item["content"] = f"A stub entry for the query: '{title}'. Please replace with real details."
        # If download_url empty, give a placeholder
        if not item.get("download_url"):
            item["download_url"] = "https://example.com/PLACEHOLDER"
        changed += 1

if changed:
    with open(ITEMS, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    print(f"Filled {changed} stub entries in items.json")
else:
    print("No empty stubs found—nothing to fill.")
