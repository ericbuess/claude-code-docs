#!/usr/bin/env python3
"""
Build a navigation map of all docs in docs/ folder.
Outputs docs/DOCS_MAP.md — used by the /query skill to identify relevant files.
"""

import re


def extract_title(content: str, filename: str) -> str:
    """Extract title from first H1, fallback to filename slug."""
    m = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    base = filename.replace('.md', '').replace('__', ' / ').replace('-', ' ').replace('_', ' ')
    return base.title()


def strip_markdown(text: str) -> str:
    """Remove markdown syntax for clean text extraction."""
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[*_]+', '', text)
    return text


def extract_summary(content: str, max_chars: int = 200) -> str:
    """Extract first paragraph after H1; skip code blocks, lists, blockquotes, frontmatter."""
    content = re.sub(r'^---[\s\S]+?---\n', '', content, count=1)

    lines = content.split('\n')
    in_code = False
    para_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith('#'):
            if para_lines:
                break
            continue
        if not stripped:
            if para_lines:
                break
            continue
        if stripped.startswith(('|', '- ', '* ', '> ')):
            if para_lines:
                break
            continue
        para_lines.append(stripped)

    summary = ' '.join(para_lines)
    summary = strip_markdown(summary)
    summary = re.sub(r'\s+', ' ', summary).strip()

    if not summary:
        return "(no summary available)"

    if len(summary) > max_chars:
        truncated = summary[:max_chars]
        last_period = truncated.rfind('.')
        if last_period > max_chars * 0.6:
            summary = truncated[:last_period + 1]
        else:
            summary = truncated + '...'

    return summary


import math
from collections import Counter

STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
    'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'can', 'this', 'that', 'these', 'those', 'you', 'they',
    'what', 'which', 'who', 'when', 'where', 'how', 'why', 'all', 'each', 'every',
    'some', 'any', 'not', 'only', 'so', 'if', 'then', 'than', 'about', 'into',
    'through', 'between', 'use', 'using', 'used', 'one', 'two', 'three', 'first',
    'second', 'over', 'under', 'also', 'just', 'such', 'them', 'their', 'there',
    'here', 'its', 'his', 'her', 'our', 'your', 'see', 'make', 'made',
    'claude', 'code', 'anthropic', 'docs', 'documentation',
    'http', 'https', 'www', 'com', 'org', 'example',
}


def tokenize(text: str) -> list[str]:
    """Tokenize text to words for keyword extraction."""
    text = strip_markdown(text).lower()
    words = re.findall(r'\b[a-z][a-z0-9_-]{2,}\b', text)
    return [w for w in words if w not in STOPWORDS]


def compute_tfidf(documents: dict) -> dict:
    """Compute TF-IDF scores for all documents."""
    tfs = {name: Counter(tokenize(content)) for name, content in documents.items()}
    df = Counter()
    for name, tf in tfs.items():
        for term in tf:
            df[term] += 1
    n_docs = len(documents) or 1
    tfidf = {}
    for name, tf in tfs.items():
        total_terms = sum(tf.values()) or 1
        scores = {}
        for term, freq in tf.items():
            tf_norm = freq / total_terms
            idf = math.log(n_docs / df[term]) if df[term] else 0
            scores[term] = tf_norm * idf
        tfidf[name] = scores
    return tfidf


def top_keywords(tfidf_scores: dict, n: int = 8) -> list[str]:
    """Return top N keywords by TF-IDF score."""
    sorted_terms = sorted(tfidf_scores.items(), key=lambda x: -x[1])
    return [term for term, score in sorted_terms[:n]]


from datetime import datetime, timezone
from pathlib import Path

DOCS_DIR_DEFAULT = Path(__file__).resolve().parent.parent / "docs"


def categorize(filename: str) -> str:
    if filename.startswith("agent-sdk__"):
        return "Agent SDK"
    if filename.startswith("whats-new__"):
        return "Weekly Updates"
    return "General"


def build_map(docs_dir: Path = None, output_file: Path = None) -> None:
    docs_dir = docs_dir or DOCS_DIR_DEFAULT
    output_file = output_file or (docs_dir / "DOCS_MAP.md")

    docs = {}
    for md_file in sorted(docs_dir.glob("*.md")):
        if md_file.name == "DOCS_MAP.md":
            continue
        docs[md_file.name] = md_file.read_text(encoding="utf-8")

    if not docs:
        print(f"No docs found in {docs_dir}")
        return

    print(f"Indexing {len(docs)} documents...")

    tfidf = compute_tfidf(docs)

    grouped = {"Agent SDK": [], "Weekly Updates": [], "General": []}
    for name in sorted(docs.keys()):
        grouped[categorize(name)].append(name)

    lines = []
    lines.append("# Docs Map")
    lines.append("")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"> Auto-generated by `scripts/build_docs_map.py` on {now}")
    lines.append(f"> {len(docs)} files indexed.")
    lines.append("")
    lines.append("Used by the `/query` skill to identify relevant docs for a given question.")
    lines.append("Each entry shows the file, its title, a short summary, and discriminative keywords (TF-IDF).")
    lines.append("")
    lines.append("---")
    lines.append("")

    for group_name in ("Agent SDK", "Weekly Updates", "General"):
        files = grouped[group_name]
        if not files:
            continue
        lines.append(f"## {group_name}")
        lines.append("")
        for name in files:
            content = docs[name]
            title = extract_title(content, name)
            summary = extract_summary(content)
            keywords = top_keywords(tfidf[name])
            lines.append(f"### `{name}`")
            lines.append(f"**Title:** {title}")
            lines.append(f"**Summary:** {summary}")
            lines.append(f"**Keywords:** {', '.join(keywords)}")
            lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ Wrote {output_file} ({len(docs)} entries)")


if __name__ == "__main__":
    build_map()
