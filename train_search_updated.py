#!/usr/bin/env python3
import argparse
import json
import sys

def enrich_stub(query):
    """
    Your actual enrichment logic goes here.
    For now this just creates a minimal stub.
    """
    return {
        "query": query,
        # you can add other default fields here...
    }

def train_on_queries(items_path, queries_path, output_path, progress_interval, dry_run):
    # Load existing items
    with open(items_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    # Load queries
    with open(queries_path, 'r', encoding='utf-8') as f:
        queries = [line.strip() for line in f if line.strip()]

    total = len(queries)
    added = 0

    for idx, q in enumerate(queries, start=1):
        stub = enrich_stub(q)
        items.append(stub)
        added += 1

        if progress_interval and idx % progress_interval == 0:
            print(f"[{idx}/{total}] processed", file=sys.stderr)

    print(f"✅ Prepared {added} new stubs{' (dry run)' if dry_run else ''}.")

    if not dry_run:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✓ Written out to {output_path}")

def main():
    p = argparse.ArgumentParser(description="Train/enrich search stubs from query list")
    p.add_argument('-i','--items',     required=True, help="Path to your items.json")
    p.add_argument('-q','--queries',   required=True, help="Path to .txt file of queries")
    p.add_argument('-o','--output',    help="Where to write updated JSON (defaults to items file)")
    p.add_argument('--progress-interval', type=int, default=0,
                   help="Print progress every N queries (0 to disable)")
    p.add_argument('--dry-run', action='store_true',
                   help="Run through but don’t actually save changes")
    args = p.parse_args()

    output_path = args.output or args.items

    train_on_queries(
        items_path=args.items,
        queries_path=args.queries,
        output_path=output_path,
        progress_interval=args.progress_interval,
        dry_run=args.dry_run
    )

if __name__ == '__main__':
    main()
