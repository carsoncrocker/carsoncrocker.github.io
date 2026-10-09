"""How many Claude Code agents worked at the same time.

Usage: python measure_concurrency.py <claude-projects-folder-of-this-project> [<more folders> ...]

Reads every Claude Code session log (*.jsonl, including sub-agent logs) under the given folders.
For each minute (UTC) since 15 September 2026, it counts how many separate logs recorded a model
response in that minute. This measures response activity per minute, not open sessions; minutes with
no responses are left out. A log is one main session or one sub-agent. It prints the distribution
of that count, and the same for main sessions only (logs not under a 'subagents' folder).
"""
import collections, datetime, glob, json, os, statistics, sys

START = datetime.datetime(2026, 9, 15, tzinfo=datetime.timezone.utc)

def main(folders):
    files = []
    for d in folders:
        files += glob.glob(os.path.join(d, '**', '*.jsonl'), recursive=True)
    files = sorted({os.path.realpath(f) for f in files})   # no path counted twice
    every = collections.defaultdict(set)   # minute -> logs active
    mains = collections.defaultdict(set)
    for f in files:
        sub = 'subagents' in f.replace('\\', '/').split('/')
        with open(f, encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if rec.get('type') != 'assistant' or not rec.get('timestamp'):
                    continue
                t = datetime.datetime.fromisoformat(rec['timestamp'].replace('Z', '+00:00'))
                if t < START:
                    continue
                minute = int(t.timestamp()) // 60
                every[minute].add(f)
                if not sub:
                    mains[minute].add(f)

    def summary(name, d):
        c = sorted(len(v) for v in d.values())
        share = lambda k: sum(x <= k for x in c) / len(c)
        q = lambda p: next(k for k in range(c[-1] + 1) if share(k) >= p)   # smallest k with >= p of minutes at or below k
        busiest = min(d, key=lambda m: (-len(d[m]), m))   # earliest minute with the maximum
        when = datetime.datetime.fromtimestamp(busiest * 60, datetime.timezone.utc)
        print(f'{name}: minutes with activity {len(c)}; median {statistics.median(c)}; '
              f'at or below {q(0.95)} in {share(q(0.95)):.1%} of minutes; at or below {q(0.99)} in {share(q(0.99)):.1%}; '
              f'max {c[-1]} (earliest {when:%Y-%m-%d %H:%M} UTC)')

    print(f'log files read: {len(files)}')
    summary('All agents (main sessions and sub-agents)', every)
    summary('Main sessions only', mains)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
