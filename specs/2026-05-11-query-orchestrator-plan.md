# Query Orchestrator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `/query` slash command to claude-code-docs that batches multi-question research across the local docs mirror via specialized subagents.

**Architecture:** A deterministic Python script generates `docs/DOCS_MAP.md` (title + summary + TF-IDF keywords per file). A GitHub workflow regenerates the map after every docs update. `install.sh` is extended to deploy a slash command, a query-orchestrator skill, and a query-researcher subagent into `~/.claude/`. The skill parses user input into N sub-questions, dispatches subagents in batches of 3 parallel, and assembles answers into a per-task `query.md` under `~/.claude-code-docs/query/`.

**Tech Stack:** Python 3.11 stdlib (re, math, pathlib, collections), pytest, GitHub Actions, bash, Claude Code skill/agent/command markdown format.

**Spec:** [`specs/2026-05-11-query-orchestrator-design.md`](2026-05-11-query-orchestrator-design.md)

**Branch:** `feature/query-orchestrator` (already created)

---

## File Structure

**Create:**
- `scripts/build_docs_map.py` — map generator
- `scripts/test_build_docs_map.py` — pytest tests
- `scripts/test_fixtures/doc_a.md` — fixture: doc with H1 + frontmatter
- `scripts/test_fixtures/doc_b.md` — fixture: doc with code block before paragraph
- `scripts/test_fixtures/doc_c.md` — fixture: doc without H1
- `docs/DOCS_MAP.md` — generated map (committed)
- `claude-files/commands/query.md` — slash command (deployed by install.sh)
- `claude-files/agents/query-researcher.md` — subagent (deployed by install.sh)
- `claude-files/skills/query-orchestrator/SKILL.md` — skill (deployed by install.sh)
- `.github/workflows/build-docs-map.yml` — workflow

**Modify:**
- `install.sh` — append `/query` install block after `/docs` setup
- `uninstall.sh` — append `/query` removal block
- `README.md` — add `/query` usage section
- `CLAUDE.md` — add `/query` section + extend ultrathink list

**Responsibility separation:**
- `scripts/` holds Python and shell — no markdown content
- `claude-files/` mirrors `~/.claude/` install target — only markdown content
- `docs/` is the docs mirror — only `DOCS_MAP.md` is added; no internal design docs leak in
- `specs/` is internal — spec + plan only

---

## Task 1: Set up test fixtures for build_docs_map.py

**Files:**
- Create: `scripts/test_fixtures/doc_a.md`
- Create: `scripts/test_fixtures/doc_b.md`
- Create: `scripts/test_fixtures/doc_c.md`

- [ ] **Step 1: Create fixture `doc_a.md` — normal doc with H1, frontmatter, paragraph**

File `scripts/test_fixtures/doc_a.md`:

```markdown
---
title: Hooks Reference
description: A reference for hooks in Claude Code
---

# Hooks

Hooks let you configure event-driven automation in Claude Code by intercepting tool calls before, after, or during execution. Hooks fire on events like PreToolUse, PostToolUse, and Stop.

## Hook events

The supported events are:

- PreToolUse
- PostToolUse
- Stop
```

- [ ] **Step 2: Create fixture `doc_b.md` — doc with code block before first paragraph**

File `scripts/test_fixtures/doc_b.md`:

```markdown
# MCP Servers

```bash
claude mcp add my-server
```

The Model Context Protocol allows you to integrate external tools and resources into Claude Code through stdio, SSE, or HTTP transports.

## Configuration
```

- [ ] **Step 3: Create fixture `doc_c.md` — no H1, fallback to filename**

File `scripts/test_fixtures/doc_c.md`:

```markdown
This file has no H1 heading. It begins with prose explaining the topic.

## Subheading
```

- [ ] **Step 4: Commit fixtures**

```bash
git add scripts/test_fixtures/
git commit -m "test: add fixtures for build_docs_map.py"
```

---

## Task 2: Implement build_docs_map.py with TDD

**Files:**
- Create: `scripts/build_docs_map.py`
- Create: `scripts/test_build_docs_map.py`

- [ ] **Step 1: Create empty script with shebang and docstring**

File `scripts/build_docs_map.py`:

```python
#!/usr/bin/env python3
"""
Build a navigation map of all docs in docs/ folder.
Outputs docs/DOCS_MAP.md — used by the /query skill to identify relevant files.
"""
```

- [ ] **Step 2: Write failing test for `extract_title`**

File `scripts/test_build_docs_map.py`:

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from build_docs_map import extract_title

FIXTURES = Path(__file__).parent / "test_fixtures"


def test_extract_title_from_h1():
    content = (FIXTURES / "doc_a.md").read_text()
    assert extract_title(content, "doc_a.md") == "Hooks"


def test_extract_title_fallback_to_filename():
    content = (FIXTURES / "doc_c.md").read_text()
    assert extract_title(content, "doc_c.md") == "Doc C"


def test_extract_title_handles_double_underscore():
    content = ""
    assert extract_title(content, "agent-sdk__hooks.md") == "Agent Sdk / Hooks"
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd scripts && python -m pytest test_build_docs_map.py::test_extract_title_from_h1 -v`
Expected: FAIL with `ImportError: cannot import name 'extract_title'`

- [ ] **Step 4: Implement `extract_title`**

Append to `scripts/build_docs_map.py`:

```python
import re


def extract_title(content: str, filename: str) -> str:
    """Extract title from first H1, fallback to filename slug."""
    m = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    base = filename.replace('.md', '').replace('__', ' / ').replace('-', ' ').replace('_', ' ')
    return base.title()
```

- [ ] **Step 5: Run tests to verify all 3 pass**

Run: `cd scripts && python -m pytest test_build_docs_map.py -v`
Expected: 3 passed

- [ ] **Step 6: Write failing tests for `extract_summary`**

Append to `scripts/test_build_docs_map.py`:

```python
from build_docs_map import extract_summary


def test_extract_summary_first_paragraph():
    content = (FIXTURES / "doc_a.md").read_text()
    summary = extract_summary(content)
    assert "Hooks let you configure event-driven automation" in summary
    assert "frontmatter" not in summary.lower()


def test_extract_summary_skips_code_blocks():
    content = (FIXTURES / "doc_b.md").read_text()
    summary = extract_summary(content)
    assert "Model Context Protocol" in summary
    assert "claude mcp add" not in summary


def test_extract_summary_truncates_at_200_chars():
    long_para = " ".join(["word"] * 100)
    content = f"# Title\n\n{long_para}"
    summary = extract_summary(content)
    assert len(summary) <= 203  # 200 + "..."


def test_extract_summary_empty_doc():
    summary = extract_summary("")
    assert summary == "(no summary available)"
```

- [ ] **Step 7: Run tests to verify they fail**

Run: `cd scripts && python -m pytest test_build_docs_map.py -v -k summary`
Expected: 4 failed with `ImportError` or `AttributeError`

- [ ] **Step 8: Implement `extract_summary` and `strip_markdown` helper**

Append to `scripts/build_docs_map.py`:

```python
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
```

- [ ] **Step 9: Run tests to verify all summary tests pass**

Run: `cd scripts && python -m pytest test_build_docs_map.py -v`
Expected: 7 passed

- [ ] **Step 10: Write failing tests for `tokenize` and `compute_tfidf`**

Append to `scripts/test_build_docs_map.py`:

```python
from build_docs_map import tokenize, compute_tfidf, top_keywords


def test_tokenize_removes_stopwords():
    tokens = tokenize("The quick brown fox jumps over the lazy dog.")
    assert "quick" in tokens
    assert "brown" in tokens
    assert "the" not in tokens
    assert "over" not in tokens


def test_tokenize_strips_markdown():
    tokens = tokenize("`code` is **important** for [docs](url).")
    assert "code" not in tokens  # in backticks → stripped
    assert "important" in tokens
    assert "docs" not in tokens  # in stopword list


def test_compute_tfidf_distinguishes_docs():
    docs = {
        "a.md": "hooks hooks hooks event event tool",
        "b.md": "mcp mcp mcp server transport",
        "c.md": "the quick brown fox jumps"
    }
    tfidf = compute_tfidf(docs)
    a_keywords = top_keywords(tfidf["a.md"], n=3)
    b_keywords = top_keywords(tfidf["b.md"], n=3)
    assert "hooks" in a_keywords
    assert "mcp" in b_keywords
    assert "hooks" not in b_keywords
```

- [ ] **Step 11: Run tests to verify they fail**

Run: `cd scripts && python -m pytest test_build_docs_map.py -v -k "tokenize or tfidf"`
Expected: 3 failed with ImportError

- [ ] **Step 12: Implement tokenize, compute_tfidf, top_keywords**

Append to `scripts/build_docs_map.py`:

```python
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
```

- [ ] **Step 13: Run tests to verify all pass**

Run: `cd scripts && python -m pytest test_build_docs_map.py -v`
Expected: 10 passed

- [ ] **Step 14: Write failing test for `build_map` output structure**

Append to `scripts/test_build_docs_map.py`:

```python
import tempfile
from build_docs_map import build_map


def test_build_map_writes_grouped_output(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "hooks.md").write_text("# Hooks\n\nHook event documentation.")
    (docs_dir / "agent-sdk__overview.md").write_text("# Agent SDK\n\nSDK overview content.")
    (docs_dir / "whats-new__2026-w19.md").write_text("# Week 19\n\nWeekly release notes.")

    output = docs_dir / "DOCS_MAP.md"
    build_map(docs_dir=docs_dir, output_file=output)

    content = output.read_text()
    assert "# Docs Map" in content
    assert "## Agent SDK" in content
    assert "## Weekly Updates" in content
    assert "## General" in content
    assert "### `hooks.md`" in content
    assert "**Title:** Hooks" in content
    assert "**Summary:**" in content
    assert "**Keywords:**" in content
    assert "DOCS_MAP.md" not in [line.strip() for line in content.split("###")[1:]]
```

- [ ] **Step 15: Run test to verify it fails**

Run: `cd scripts && python -m pytest test_build_docs_map.py::test_build_map_writes_grouped_output -v`
Expected: FAIL with ImportError or "build_map() takes ..."

- [ ] **Step 16: Implement `build_map`**

Append to `scripts/build_docs_map.py`:

```python
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
```

- [ ] **Step 17: Run all tests, verify all pass**

Run: `cd scripts && python -m pytest test_build_docs_map.py -v`
Expected: 11 passed

- [ ] **Step 18: Commit**

```bash
git add scripts/build_docs_map.py scripts/test_build_docs_map.py
git commit -m "feat: add build_docs_map.py with TF-IDF keyword extraction"
```

---

## Task 3: Generate initial DOCS_MAP.md from real docs

**Files:**
- Create: `docs/DOCS_MAP.md`

- [ ] **Step 1: Run the script against the real docs folder**

Run from repo root:
```bash
python scripts/build_docs_map.py
```
Expected output: `Indexing 127 documents...` and `✓ Wrote .../docs/DOCS_MAP.md (127 entries)`

- [ ] **Step 2: Spot-check the output**

Run: `head -50 docs/DOCS_MAP.md`
Expected: H1 "Docs Map", generation timestamp, "127 files indexed", section headers (## Agent SDK, ## Weekly Updates, ## General), entries with title/summary/keywords.

Run: `wc -l docs/DOCS_MAP.md`
Expected: ~640 lines (127 entries × 5 lines + headers).

- [ ] **Step 3: Verify DOCS_MAP.md is not self-referencing**

Run: `grep "^### .DOCS_MAP.md" docs/DOCS_MAP.md || echo "OK - not self-referencing"`
Expected: `OK - not self-referencing`

- [ ] **Step 4: Commit**

```bash
git add docs/DOCS_MAP.md
git commit -m "feat: add initial DOCS_MAP.md (127 entries)"
```

---

## Task 4: Add GitHub workflow for map auto-regeneration

**Files:**
- Create: `.github/workflows/build-docs-map.yml`

- [ ] **Step 1: Write the workflow file**

File `.github/workflows/build-docs-map.yml`:

```yaml
name: Build Docs Map

on:
  workflow_run:
    workflows: ["Update Claude Code Documentation"]
    types: [completed]
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - 'scripts/build_docs_map.py'
      - 'docs/**/*.md'

permissions:
  contents: write

jobs:
  build-map:
    if: github.event.workflow_run.conclusion == 'success' || github.event_name != 'workflow_run'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          ref: main

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build docs map
        run: python scripts/build_docs_map.py

      - name: Commit if changed
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          if [[ -n "$(git status --porcelain docs/DOCS_MAP.md)" ]]; then
            git add docs/DOCS_MAP.md
            git commit -m "Update DOCS_MAP.md - $(date +'%Y-%m-%d')"
            git push
          else
            echo "No changes to DOCS_MAP.md"
          fi
```

- [ ] **Step 2: Lint the YAML (visual inspection)**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/build-docs-map.yml'))"`
Expected: no output (parses successfully).

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/build-docs-map.yml
git commit -m "ci: add build-docs-map workflow"
```

---

## Task 5: Add slash command file

**Files:**
- Create: `claude-files/commands/query.md`

- [ ] **Step 1: Write the slash command file**

File `claude-files/commands/query.md`:

```markdown
---
description: Research Claude Code documentation by batching multi-question queries to specialized subagents
argument-hint: <your question(s) — single or multi-part>
---

The user has invoked /query with the following input:

$ARGUMENTS

Use the Skill tool to invoke the `query-orchestrator` skill. Pass the user query above as the skill's argument. Follow the skill's instructions exactly.
```

- [ ] **Step 2: Commit**

```bash
git add claude-files/commands/query.md
git commit -m "feat: add /query slash command"
```

---

## Task 6: Add query-researcher subagent file

**Files:**
- Create: `claude-files/agents/query-researcher.md`

- [ ] **Step 1: Write the agent file**

File `claude-files/agents/query-researcher.md`:

````markdown
---
name: query-researcher
description: Research a single sub-question by reading Claude Code documentation files and producing a structured answer file
tools: Read, Grep, Glob, Write, Bash
---

# Query Researcher

You research ONE sub-question. You read the docs map, pick 2-5 relevant files, read them, then write a structured answer to a specific file path.

## Input (provided in your prompt)

The orchestrator gives you these fields:

- `Task: <TASK_ID>` — the parent task identifier
- `Query ID: [QUERY-N]` — your specific query slot
- `Question:` — the actual question text
- `Output file:` — exact path where you write the answer
- `Docs map:` — path to DOCS_MAP.md
- `Docs folder:` — path to the docs directory

## Procedure

### Step 1 — Pick relevant docs (max 5)

Read the docs map with the Read tool. Match the question against entries via:

- Title overlap
- Summary overlap
- Keyword overlap (each entry lists TF-IDF keywords)

Prefer specific files over general ones (e.g., `hooks.md` over `overview.md` for a hooks question). If the question is broad with no specific match, pick 1 general + 2 specific.

You may use Grep to find term-specific matches:

```bash
grep -l "specific-term" ~/.claude-code-docs/docs/*.md | head -5
```

### Step 2 — Read selected docs

Use the Read tool on each selected file. **Hard cap: 5 files.** If a file you're reading references another that's clearly more relevant, swap rather than add.

### Step 3 — Synthesize an answer

Build an answer that:

- Directly answers the question
- Cites which docs you used
- Quotes short relevant excerpts
- Is 200-500 words typical (longer only if necessary)
- Notes gaps or ambiguities when docs don't fully cover the question

### Step 4 — Write the output file

Use the Write tool to create the output file at the path provided in your input. Use this EXACT structure:

```markdown
# Answer to [QUERY-N]

**Question:** <restate the question>
**Task:** <TASK_ID>

## Researched files

- `docs/file1.md` — why relevant
- `docs/file2.md` — why relevant

## Answer

<synthesized answer with markdown formatting>

## Source excerpts

> Short relevant quote from `file1.md`

> Short relevant quote from `file2.md`

## Notes

<gaps, ambiguities, or "none">
```

## Constraints

- Read AT MOST 5 docs
- Write EXACTLY ONE output file (path given in input)
- Do NOT call other subagents (no Task tool)
- Do NOT fetch from the web (use only the local docs folder)
- If no docs match the question, write the output file with `## Answer\n_No matching documentation found for this question. Suggested related topics: ..._`
````

- [ ] **Step 2: Commit**

```bash
git add claude-files/agents/query-researcher.md
git commit -m "feat: add query-researcher subagent"
```

---

## Task 7: Add query-orchestrator skill

**Files:**
- Create: `claude-files/skills/query-orchestrator/SKILL.md`

- [ ] **Step 1: Write the skill file**

File `claude-files/skills/query-orchestrator/SKILL.md`:

````markdown
---
name: query-orchestrator
description: Use when handling /query slash command — parses multi-part questions, dispatches batched subagents to research docs, and assembles final answer
---

# Query Orchestrator

You orchestrate research on Claude Code documentation when the user invokes `/query`. You decompose the user's input into sub-questions, dispatch a `query-researcher` subagent for each in batches of 3 parallel, and assemble all answers into a single output file.

## Inputs

The slash command passes the user's raw query as your argument. Examples:

- "What are hooks?" (single question, N=1)
- "Explain hooks and MCP, and how to integrate them" (3 sub-questions)
- "1. ... 2. ... 3. ..." (explicit numbering)

## Step-by-step procedure

### Step 1 — Parse into sub-questions

Identify each independent factual sub-question in the user's input. A sub-question is something a researcher could answer alone by reading docs.

Rules:

- One cohesive question → N = 1
- Explicit numbering (1./2./3. or bullets) → follow numbering
- Independent parts joined by `and`/`ve` → split (only if each part is independently answerable)
- Trim and normalize each sub-question to a clear standalone form

Output internally:

```
SUB_QUESTIONS = [
  "What are hooks?",
  "What is MCP?",
  "How to integrate hooks with MCP?"
]
N = 3
```

### Step 2 — Generate task ID

- Take the first sub-question's most discriminative content word, skipping stopwords (`the`, `a`, `what`, `how`, `is`, `does`).
- Lowercase, ASCII-normalize, slugify.
- If no content word can be identified (e.g., "How does it work?"), use the literal keyword `query`.
- Append current epoch milliseconds via Bash: `date +%s%3N`.
- Format: `QUERY-TASK-<keyword>-<epoch_ms>`.
- Example: `QUERY-TASK-hooks-1715432100123`.

### Step 3 — Create task folder

Use the Bash tool:

```bash
mkdir -p ~/.claude-code-docs/query/<TASK_ID>
```

### Step 4 — Write initial query.md

Use the Write tool to create `~/.claude-code-docs/query/<TASK_ID>/query.md` from this template (substitute placeholders):

```markdown
# Query Task: <TASK_ID>

**Original user query:**
> <ORIGINAL_USER_INPUT>

**Created at:** <ISO_TIMESTAMP>
**Number of sub-questions:** <N>
**Status:** in-progress

---

## [QUERY-1] — <SHORT_TITLE_1>

**Question:** <SUB_QUESTION_1>

**Answer:**
<!-- ANSWER-1-START -->
_pending — researcher dispatched_
<!-- ANSWER-1-END -->

---

## [QUERY-2] — <SHORT_TITLE_2>

**Question:** <SUB_QUESTION_2>

**Answer:**
<!-- ANSWER-2-START -->
_pending — researcher dispatched_
<!-- ANSWER-2-END -->

---

<!-- repeat the [QUERY-N] block for every sub-question -->
```

`SHORT_TITLE_n` is a 3-5 word descriptor you derive from the sub-question (e.g., "What are hooks?" → "Hooks definition").

### Step 5 — Dispatch subagents in batches of 3

**CRITICAL:** All Task tool calls in one batch MUST be sent in a SINGLE message to execute in parallel. If you send them in separate messages they will execute sequentially.

Batching table:

| N  | Batches      |
|----|--------------|
| 1  | [1]          |
| 2  | [2]          |
| 3  | [3]          |
| 4  | [3, 1]       |
| 5  | [3, 2]       |
| 7  | [3, 3, 1]    |
| 15 | [3, 3, 3, 3, 3] |

For each batch of up to 3 consecutive sub-questions:

1. In a SINGLE message, issue up to 3 parallel Task tool calls.
2. Each Task call uses `subagent_type: query-researcher`.
3. Wait for ALL calls in the batch to return before starting the next batch.

Each Task call prompt MUST contain these exact fields:

```
Task: <TASK_ID>
Query ID: [QUERY-N]
Question: <sub-question text>
Output file: ~/.claude-code-docs/query/<TASK_ID>/QUERY-<N>.md
Docs map: ~/.claude-code-docs/docs/DOCS_MAP.md
Docs folder: ~/.claude-code-docs/docs/
```

### Step 6 — Assemble answers into final query.md

After ALL batches complete:

1. Issue parallel Read calls for every `QUERY-N.md` (single message, N Read tool calls).
2. For each file, extract everything below the H1 header (`# Answer to [QUERY-N]`) — this is the answer body.
3. Build the complete final `query.md` in memory: header (TASK_ID, original query, timestamp, N, `Status: complete`), then for each [QUERY-N] the question text plus the extracted body (replacing the `_pending_` placeholder).
4. Single Write call overwrites `query.md` with the complete assembled content.

If a `QUERY-N.md` is missing (subagent failed):

- Insert: `_⚠️ Researcher did not complete this query. Re-run `/query` for just this question._` in place of the answer body.

### Step 7 — Chat summary

Output to chat:

```
✓ Query complete: <TASK_ID> (<N> questions)

• [QUERY-1] <one-line synthesis of answer 1>
• [QUERY-2] <one-line synthesis of answer 2>
• ...

Full details: ~/.claude-code-docs/query/<TASK_ID>/query.md
```

Keep each bullet to one line. Do not paste the full answers in chat.

## Failure handling

| Failure | Handling |
|---------|----------|
| `mkdir` fails | Abort with error message; do not dispatch subagents |
| DOCS_MAP.md missing | Tell user to re-run `~/.claude-code-docs/install.sh` |
| Subagent returns no file | Insert warning placeholder for that query; continue with others |
| Parsing yields N=0 | Ask user to rephrase the query |
````

- [ ] **Step 2: Commit**

```bash
git add claude-files/skills/query-orchestrator/SKILL.md
git commit -m "feat: add query-orchestrator skill"
```

---

## Task 8: Extend install.sh with /query setup

**Files:**
- Modify: `install.sh`

- [ ] **Step 1: Read current end of install.sh to find insertion point**

Run: `grep -n "Available topics" install.sh`
Expected: returns a line number (the success message). Insert BEFORE this line.

- [ ] **Step 2: Add the /query install block**

Find this section in `install.sh`:

```bash
# Clean up old installations now that v0.3 is set up
cleanup_old_installations

# Success message
echo ""
echo "✅ Claude Code Docs v0.3.3 installed successfully!"
```

Insert the following block BETWEEN `cleanup_old_installations` and `# Success message`:

```bash
# Setup /query feature (skill + agent + command)
echo ""
echo "Installing /query feature..."

mkdir -p ~/.claude/commands
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/skills/query-orchestrator

if [[ -d "$INSTALL_DIR/claude-files" ]]; then
    cp "$INSTALL_DIR/claude-files/commands/query.md" \
       ~/.claude/commands/query.md
    cp "$INSTALL_DIR/claude-files/agents/query-researcher.md" \
       ~/.claude/agents/query-researcher.md
    cp "$INSTALL_DIR/claude-files/skills/query-orchestrator/SKILL.md" \
       ~/.claude/skills/query-orchestrator/SKILL.md
    echo "✓ Installed /query command, query-researcher agent, query-orchestrator skill"
else
    echo "⚠️  claude-files/ missing — /query feature will not be available"
fi

mkdir -p "$INSTALL_DIR/query"
echo "✓ Query workspace ready at $INSTALL_DIR/query"
```

- [ ] **Step 3: Validate the script syntax**

Run: `bash -n install.sh`
Expected: no output (syntax valid).

- [ ] **Step 4: Smoke-test against the local checkout**

Run from the repo root:
```bash
INSTALL_DIR="$(pwd)" bash -c '
mkdir -p ~/.claude/commands ~/.claude/agents ~/.claude/skills/query-orchestrator
cp "$INSTALL_DIR/claude-files/commands/query.md" ~/.claude/commands/query.md
cp "$INSTALL_DIR/claude-files/agents/query-researcher.md" ~/.claude/agents/query-researcher.md
cp "$INSTALL_DIR/claude-files/skills/query-orchestrator/SKILL.md" ~/.claude/skills/query-orchestrator/SKILL.md
ls -l ~/.claude/commands/query.md ~/.claude/agents/query-researcher.md ~/.claude/skills/query-orchestrator/SKILL.md
'
```
Expected: 3 files listed with their sizes.

- [ ] **Step 5: Commit**

```bash
git add install.sh
git commit -m "feat: extend install.sh to deploy /query files"
```

---

## Task 9: Extend uninstall.sh with /query removal

**Files:**
- Modify: `uninstall.sh`

- [ ] **Step 1: Find insertion point**

Run: `grep -n "Remove directories" uninstall.sh`
Expected: returns a line number. Insert the new block BEFORE this section.

- [ ] **Step 2: Add the /query removal block**

In `uninstall.sh`, find this section:

```bash
echo "✓ Removed hooks (backup: ~/.claude/settings.json.backup)"
```

Insert the following block AFTER it (before `# Remove directories`):

```bash
# Remove /query feature files
echo ""
echo "Removing /query feature..."

[[ -f ~/.claude/commands/query.md ]] && rm -f ~/.claude/commands/query.md && echo "✓ Removed /query command"
[[ -f ~/.claude/agents/query-researcher.md ]] && rm -f ~/.claude/agents/query-researcher.md && echo "✓ Removed query-researcher agent"
[[ -d ~/.claude/skills/query-orchestrator ]] && rm -rf ~/.claude/skills/query-orchestrator && echo "✓ Removed query-orchestrator skill"

if [[ -d "$HOME/.claude-code-docs/query" ]] && [[ -n "$(ls -A "$HOME/.claude-code-docs/query" 2>/dev/null)" ]]; then
    echo ""
    echo "⚠️  Found query outputs at $HOME/.claude-code-docs/query/"
    read -p "Delete query history? (y/N): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] && rm -rf "$HOME/.claude-code-docs/query" && echo "✓ Removed query history"
fi
```

- [ ] **Step 3: Validate the script syntax**

Run: `bash -n uninstall.sh`
Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add uninstall.sh
git commit -m "feat: extend uninstall.sh to remove /query files"
```

---

## Task 10: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add the /query section**

In `README.md`, find this line:

```markdown
### Customize command name
```

Insert the following section ABOVE it (between the existing `### Read Claude Code changelog` section and `### Customize command name`):

````markdown
### Multi-question research with /query

`/query` parses your input into sub-questions, dispatches research subagents in batches of 3 in parallel, and assembles a structured answer file.

```bash
/query What is a hook?                          # single question
/query Explain hooks and MCP, then compare them # multi-part
/query 1. ... 2. ... 3. ...                     # explicit numbering
```

Each query produces a folder under `~/.claude-code-docs/query/QUERY-TASK-<keyword>-<id>/`
containing the full structured answer with citations. Useful for non-trivial questions that span multiple docs.

````

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: document /query feature in README"
```

---

## Task 11: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add /query section**

In `CLAUDE.md`, find this section:

```markdown
## For /docs Command

When responding to /docs commands:
1. Follow the instructions in the docs.md command file
2. Read documentation files from the docs/ directory only
3. Use the manifest to know available topics
```

Insert the following block AFTER it (before `## Files to ultrathink about`):

```markdown
## For /query Command

When responding to /query commands:
1. Invoke the `query-orchestrator` skill via the Skill tool
2. Follow the skill's 7-step procedure (parse → task ID → folder → template → batch dispatch → assemble → summary)
3. Subagents read from docs/ folder via DOCS_MAP.md
4. Outputs accumulate in ~/.claude-code-docs/query/
```

- [ ] **Step 2: Extend ultrathink list**

In `CLAUDE.md`, find:

```markdown
## Files to ultrathink about

@install.sh
@README.md
@uninstall.sh
@UNINSTALL.md
@claude-docs-helper.md
@scripts/
@.github/workflows/
```

Replace with:

```markdown
## Files to ultrathink about

@install.sh
@README.md
@uninstall.sh
@UNINSTALL.md
@claude-docs-helper.md
@scripts/
@.github/workflows/
@docs/DOCS_MAP.md
@claude-files/
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: document /query in CLAUDE.md and extend ultrathink list"
```

---

## Task 12: End-to-end manual validation

**Files:** none (manual testing)

- [ ] **Step 1: Reinstall locally to deploy the new files**

Run from repo root:
```bash
# Simulate a fresh install pointing at the local checkout
INSTALL_DIR="$(pwd)" bash -x install.sh 2>&1 | tail -30
```

Note: this assumes `install.sh` has been adapted to use `INSTALL_DIR` (it does — already defined at the top). If the existing install.sh resists running from a non-default location, instead simulate the relevant steps:

```bash
mkdir -p ~/.claude/commands ~/.claude/agents ~/.claude/skills/query-orchestrator
cp claude-files/commands/query.md ~/.claude/commands/query.md
cp claude-files/agents/query-researcher.md ~/.claude/agents/query-researcher.md
cp claude-files/skills/query-orchestrator/SKILL.md ~/.claude/skills/query-orchestrator/SKILL.md
mkdir -p "$HOME/.claude-code-docs/query"
```

Verify:
```bash
ls -l ~/.claude/commands/query.md ~/.claude/agents/query-researcher.md ~/.claude/skills/query-orchestrator/SKILL.md
```
Expected: 3 files exist.

- [ ] **Step 2: Restart Claude Code, then test N=1**

In Claude Code: `/query What is a hook?`

Expected:
- Task folder created at `~/.claude-code-docs/query/QUERY-TASK-<word>-<ms>/`
- `query.md` exists with `Status: complete`
- One answer assembled from at least one doc file

Verify:
```bash
ls ~/.claude-code-docs/query/
cat ~/.claude-code-docs/query/QUERY-TASK-*/query.md
```

- [ ] **Step 3: Test N=3 (single batch of 3 parallel)**

In Claude Code: `/query Explain hooks, MCP, and how to integrate them`

Expected:
- New task folder
- 3 `QUERY-N.md` files exist
- `query.md` shows all 3 answers assembled

Verify:
```bash
ls ~/.claude-code-docs/query/QUERY-TASK-* | tail -1 | xargs ls
```
Expected: `query.md`, `QUERY-1.md`, `QUERY-2.md`, `QUERY-3.md`.

- [ ] **Step 4: Test N=5 (batches of [3, 2])**

In Claude Code: `/query 1. What are hooks? 2. What is MCP? 3. What are skills? 4. How do plugins work? 5. What is the Agent SDK?`

Expected:
- 5 `QUERY-N.md` files
- `query.md` assembled with all 5 answers

- [ ] **Step 5: Test edge case — DOCS_MAP.md missing**

```bash
mv ~/.claude-code-docs/docs/DOCS_MAP.md /tmp/DOCS_MAP.md.bak
```

In Claude Code: `/query What is a hook?`

Expected: skill produces a clear error message instructing the user to re-run install.sh or rebuild the map.

Restore:
```bash
mv /tmp/DOCS_MAP.md.bak ~/.claude-code-docs/docs/DOCS_MAP.md
```

- [ ] **Step 6: Test uninstall**

Run: `bash uninstall.sh`
Expected:
- Files removed: `~/.claude/commands/query.md`, `~/.claude/agents/query-researcher.md`, `~/.claude/skills/query-orchestrator/`
- Prompted to delete `~/.claude-code-docs/query/` (answer N to keep history)

- [ ] **Step 7: Reinstall to leave system in working state**

Run the simulated install commands from Step 1 again. Verify `/query` works again with a single-question test.

---

## Task 13: Final repo review and push

**Files:** none (review + push)

- [ ] **Step 1: Run the full test suite**

```bash
cd scripts && python -m pytest test_build_docs_map.py -v
```
Expected: all tests pass.

- [ ] **Step 2: Check git log shows clean commits**

Run: `git log --oneline main..HEAD`
Expected: 12 commits (one per task), with conventional commit messages.

- [ ] **Step 3: Squash if requested or push as-is**

Push the branch:
```bash
git push -u origin feature/query-orchestrator
```

- [ ] **Step 4: Open a draft PR for early maintainer feedback**

(User action) Open a draft PR on GitHub with body:
- Link to spec doc in branch
- Summary of new features
- Note: existing `/docs` is unchanged
- Test results

---

## Self-Review

**Spec coverage check (every section of the spec mapped to a task):**

| Spec § | Task |
|--------|------|
| §5 Map generation | Task 1 (fixtures), Task 2 (script+tests), Task 3 (initial map) |
| §6 Slash command | Task 5 |
| §7 Skill | Task 7 |
| §8 Subagent | Task 6 |
| §9 GitHub workflow | Task 4 |
| §10 install.sh | Task 8 |
| §10 uninstall.sh | Task 9 |
| §11 README.md | Task 10 |
| §11 CLAUDE.md | Task 11 |
| §12 Test plan | Task 2 (unit), Task 12 (manual) |
| §14 Acceptance criteria | Task 12 (end-to-end) + Task 13 (review) |

All spec sections covered.

**Type/signature consistency:**

- `extract_title(content, filename)` — used consistently in tests and implementation ✓
- `extract_summary(content, max_chars=200)` — consistent ✓
- `tokenize(text) -> list[str]` — consistent ✓
- `compute_tfidf(documents: dict) -> dict` — consistent ✓
- `build_map(docs_dir=None, output_file=None)` — accepts overrides for testing ✓

**Placeholder check:** No "TBD", "TODO", "implement later", or vague guidance. Every code step shows complete code.

---

## Execution Handoff

Plan complete and saved to `specs/2026-05-11-query-orchestrator-plan.md`. Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
