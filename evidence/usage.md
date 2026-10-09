# Claude Code usage

How much Claude Code was used on this project, measured from Claude Code's own session logs on my computer.

## How it was measured {#method}

Claude Code writes a log file for every session, and each model response in it records its token counts. The script
[`measure_usage.py`](measure_usage.py) reads every session log of this project (including the logs of sub-agents),
counts each response once, and adds up the token counts. It was run on 7 October 2026, while this site was being built,
so the last day is partial. Its complete output is [`usage_output.txt`](usage_output.txt).

The script is adapted from the project's earlier measuring script. Two changes: the log folder is now a command-line
argument, so no local path is published, and the dollar estimate at API list prices was removed, because the prices
in it had not been re-checked.

## Result {#result}

- Model responses: 27,081
- Active days (UTC): 23, from 15 September to 7 October 2026
- Output tokens: 30,348,293
- Input tokens read from cache: 5,797,772,883
- Input tokens written to cache: 366,312,225
- Uncached input tokens: 105,855

## What it does not cover {#limits}

- It covers the whole project, including problems that went nowhere and results that are not public yet; it cannot be
  split cleanly by problem, because many sessions ran in parallel.
- It counts Claude Code only. ChatGPT and other models were used through their own apps and are not counted.
- Most of the tokens are cache reads: the model re-reading its own context in long sessions.

## How many agents at once {#concurrency}

The script [`measure_concurrency.py`](measure_concurrency.py) reads the same session logs. For every minute since
15 September 2026 it counts how many separate logs recorded a model response in that minute; each main session and each
sub-agent has its own log. This measures response activity per minute, not open sessions, and minutes with no responses
are left out. It was run on 8 October 2026. Its complete output is [`concurrency_output.txt`](concurrency_output.txt).

- All agents (main sessions and sub-agents) responding in the same minute: median 2; 8 or fewer in 96% of minutes;
  12 or fewer in 99% of minutes; at most 20 (during an overnight run on 28 September).
- Main Claude Code sessions responding in the same minute: at most 4.

So the system usually ran fewer than ten agents at a time. It counts Claude Code only; ChatGPT and other models are not
included.
