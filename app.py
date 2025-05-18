import os
import json
import streamlit as st

from search_with_download import SearchEngine

# ─── Config ────────────────────────────────────────────────────────────────
BASE_DIR = "D:/search_demo"        # single source of truth for paths
ITEMS_FILE = os.path.join(BASE_DIR, "items.json")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ─── Load catalogue ────────────────────────────────────────────────────────
try:
    with open(ITEMS_FILE, encoding="utf-8") as f:
        items = json.load(f)
except Exception as e:
    st.error(f"Could not load {ITEMS_FILE}: {e}")
    st.stop()

# older items (or hand-edited ones) may be missing the 'title' key
for it in items:
    if "title" not in it:
        it["title"] = it.get("query", "<no-title>")
    it.setdefault("price", 0)
    it.setdefault("download_url", "")

engine = SearchEngine(items)

# ─── UI Layout ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Search Demo", page_icon="🔍")
st.title("🔍  Local-first Search Demo")

query = st.text_input("Search for…", placeholder="e.g. bootstrap plumber")

if st.button("Search") and query.strip():
    q = query.strip()
    st.info(f"**Query:** {q}")

    results = engine.search(q, top_n=10)

    if results:
        st.success(f"{len(results)} local result(s) found")
        for item in results:
            st.markdown(f"### {item['title']}")
            st.write(item.get("content", ""))
            price = item.get("price", 0)

            if price == 0 and item.get("download_url"):
                fname = os.path.basename(item["download_url"])
                dest = os.path.join(DOWNLOAD_DIR, fname)
                if st.button(f"⬇️  Download {fname}", key=fname):
                    try:
                        import requests

                        r = requests.get(item["download_url"], timeout=10)
                        r.raise_for_status()
                        with open(dest, "wb") as fp:
                            fp.write(r.content)
                        st.success(f"Saved → {dest}")
                    except Exception as exc:
                        st.error(f"Download failed: {exc}")
            else:
                st.write(f"Price: {price}")
            st.divider()
    else:
        st.warning("No local matches – showing Google links instead:")
        try:
            from googlesearch import search as gsearch

            for url in gsearch(q, num_results=5):
                st.markdown(f"- <{url}>")
        except Exception as exc:
            st.error(f"Could not fetch Google results: {exc}")
