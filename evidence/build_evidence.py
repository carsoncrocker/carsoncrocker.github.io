# Renders the plain evidence files (*.md in this folder) as styled HTML pages with linkable anchors.
# The .md files are the source; run "python build_evidence.py" here after editing one of them.
# Supports only what these files use: headings with {#id}, paragraphs, "> " quotes, "- " lists,
# ``` code fences, `code`, **bold** and [text](url).
import html, re, os

PAGES = {
    "ledger_extract.md": "Ledger extract",
    "log_quotes.md": "Log quotes",
    "withdrawn.md": "Withdrawn",
    "usage.md": "Claude Code usage",
}
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Carson Crocker</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="../">Carson Crocker</a>
  <nav class="nav" aria-label="Site"><a href="../">Home</a><a href="../results/">Results</a><a href="../case-study.html">Case study</a><a href="../log.html">Log</a></nav>
</div></header>
<main class="wrap evidence">
<p class="small"><a href="./">Evidence</a> / {title} · plain text: <a href="{src}">{src}</a></p>
"""
FOOT = """</main>
<footer><div class="wrap">
  <p>Generated from <a href="{src}">{src}</a> by build_evidence.py. Excerpts are verbatim except where marked [redacted: ...].</p>
</div></footer>
</body>
</html>
"""


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def quote_inline(t):  # verbatim excerpts: escape, keep only bold
    t = html.escape(t, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def render(md):
    out, para, quote, items, code = [], [], [], [], None

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()
        if quote:
            out.append("<blockquote class=\"verbatim\">" + "<br>".join(quote_inline(q) for q in quote) + "</blockquote>")
            quote.clear()
        if items:
            out.append("<ul>" + "".join("<li>" + inline(i) + "</li>" for i in items) + "</ul>")
            items.clear()

    for line in md.split("\n"):
        if code is not None:
            if line.startswith("```"):
                out.append("<pre>" + html.escape("\n".join(code)) + "</pre>")
                code = None
            else:
                code.append(line)
            continue
        if line.startswith("```"):
            flush(); code = []
            continue
        if line.startswith("> ") or line == ">":
            if para or items:
                flush()
            quote.append(line[2:])
            continue
        m = re.match(r"(#{1,3}) (.*?)(?: \{#([\w-]+)\})?$", line)
        if m:
            flush()
            n = len(m.group(1))
            ident = f' id="{m.group(3)}"' if m.group(3) else ""
            out.append(f"<h{n}{ident}>{inline(m.group(2))}</h{n}>")
            continue
        if line.startswith("- "):
            if para or quote:
                flush()
            items.append(line[2:])
            continue
        if line.startswith("  ") and items:
            items[-1] += " " + line.strip()
            continue
        if not line.strip():
            flush()
            continue
        if quote:
            flush()
        para.append(line.strip())
    flush()
    return "\n".join(out)


here = os.path.dirname(os.path.abspath(__file__))
for src, title in PAGES.items():
    md = open(os.path.join(here, src), encoding="utf-8").read()
    body = render(md)
    page = HEAD.format(title=title, src=src) + body + "\n" + FOOT.format(src=src)
    open(os.path.join(here, src[:-3] + ".html"), "w", encoding="utf-8", newline="\n").write(page)
    print("wrote", src[:-3] + ".html")
