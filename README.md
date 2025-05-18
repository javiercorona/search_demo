# 📑  User-Command Quick Reference

| # | Command (PowerShell) | What it does / When to use it |
|---|----------------------|------------------------------|
| **0** | `Set-Location D:\search_demo` | Jump to the project root. Do this first in every new terminal. |
| **1** | `.\python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir="D:\Python312" Include_test=0` | **Silent install** Python 3.12 under `D:\Python312` and put it on `PATH`. Run once on a fresh machine. |
| **1.1** | `python --version` | Confirm the new Python version is active. |
| **1.2** | `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1` | Optional: create & activate a project-local virtual-env. |
| **1.3** | `pip install streamlit beautifulsoup4 requests tqdm` | Install minimal package set. |
| **2** | `python generate_queries.py --topics-file topics.txt --verbs "how to" "guide to" "tutorial on" --out extra_queries.txt` | Explode a *topics* list into 10⁴-style query phrases. |
| **2.1** | `Get-Content queries.txt,extra_queries.txt | Set-Content all_queries.txt` | Merge the canonical and generated query files. |
| **3-DRY** | `python train_search_updated.py -i items.json -q all_queries.txt --dry-run` | **Dry-run** trainer – tells you how many new items would be added, but **doesn’t touch** `items.json`. |
| **3-LIVE** | `python train_search_updated.py -i items.json -q all_queries.txt --progress-interval 5000` | Real training pass: backs up the file, appends/enriches new stubs, prints progress every 5 000 queries. |
| **3-TINY** | `"foo","bar" | Set-Content small.txt`<br>`python train_search_updated.py -i items.json -q small.txt` | Micro test (two queries) – handy to verify the pipeline quickly. |
| **4** | `streamlit run app.py` | Launch the GUI (<http://localhost:8501>). |
| **5** | `Get-ChildItem -File | ? Length -eq 0 | Remove-Item` | Remove zero-byte junk files that sometimes appear. |
| **6** | `Remove-Item -Recurse __pycache__ -Force -EA 0` | Clear Python byte-code caches. |
| **7** | `setx /M PATH ("D:\Python312;D:\Python312\Scripts;" + $env:Path)` | (Admin) Make the 3.12 install permanently first on system PATH. |
| **8** | `where python` | Show every python.exe on the current PATH (debugging). |
| **9** | `pip freeze > requirements.txt` | Snapshot exact package versions for reproducible installs. |

---

### Common Errors & Quick Fixes

| Error message | Likely cause | One-liner fix |
|---------------|-------------|---------------|
| `python is not recognized` | Path not set / wrong terminal | `Set-Location D:\Python312; ./python.exe --version` or see command **7** |
| `KeyError: 'title'` in **search_with_download.py** | Old `items.json` record missing fields | Re-run trainer (**3-LIVE**) to auto-fill |
| `File does not exist: app.py` from Streamlit | Running from wrong folder | `Set-Location D:\search_demo` first, or `streamlit run D:\search_demo\app.py` |
| Still shows Python 3.11 after install | Old version precedes 3.12 on PATH | Re-open terminal or run command **7** |

---

*Keep this list close — it’s 99 % of everything you’ll type while iterating on the project.*  
Happy hacking! 🎉


python train_search.py --items items.json --queries queries.txt

cd C:\Users\Projects\search_demo
python train_search.py --items items.json --queries queries.txt
streamlit run app.py
python generate_queries.py
