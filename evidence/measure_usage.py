# Counts Claude Code usage for this project from Claude Code's local session logs (*.jsonl).
# Adapted from the project's earlier measuring script: the log folder is now a command-line argument
# (so no local path is published) and the API-price estimate was removed (prices were not re-checked).
# Run: python measure_usage.py <folder with the project's Claude Code session logs>
import json, glob, os, sys
ROOT = sys.argv[1]
K = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
rec = {}
for f in glob.glob(os.path.join(ROOT, "**", "*.jsonl"), recursive=True):
    for line in open(f, encoding="utf-8", errors="ignore"):
        if '"usage"' not in line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        m = d.get("message") or {}
        u = m.get("usage")
        if not u or m.get("model") in (None, "<synthetic>"):
            continue
        r = rec.setdefault((m.get("id"), d.get("requestId")),
                           {"day": (d.get("timestamp") or "")[:10], **{k: 0 for k in K}})
        for k in K:  # streamed entries repeat; keep the largest count per message
            r[k] = max(r[k], u.get(k) or 0)
days = sorted({r["day"] for r in rec.values() if r["day"]})
print(f"model responses: {len(rec):,}")
print(f"active days (UTC): {len(days)}, from {days[0]} to {days[-1]}")
for k in K:
    print(f"{k}: {sum(r[k] for r in rec.values()):,}")
