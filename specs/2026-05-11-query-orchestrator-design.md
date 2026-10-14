# Query Orchestrator Design

**Date:** 2026-05-11
**Status:** Approved (brainstorming phase)
**Target branch:** `feature/query-orchestrator`
**Target upstream:** PR to `ericbuess/claude-code-docs`

## 1. Goal

Add a `/query` slash command to the `claude-code-docs` mirror that handles multi-part research questions against the local docs. The command:

1. Parses a user query into N independent sub-questions.
2. Generates a unique task folder per query.
3. Dispatches a specialized subagent per sub-question, in **batches of 3 parallel calls**.
4. Each subagent reads a generated docs map to identify relevant files, reads them, writes a structured answer file.
5. The orchestrator assembles all answer files into a single `query.md` per task.
6. The user sees a short chat summary + a path to the assembled file.

The existing `/docs` command is **untouched**. The new feature is additive.

## 2. Non-Goals

- Renaming the repo. Original name `claude-code-docs` is preserved.
- Converting the repo into a Claude Code plugin (no `plugin.json` at root). Existing `install.sh` pattern is followed.
- LLM-based map generation. Map generation is deterministic Python only.
- Multi-language templates. Templates and skill outputs are English.

## 3. Architecture

### High-level flow

```
/query "Hooks ve MCP nedir, nasıl entegre edilir?"
    │
    ▼
~/.claude/commands/query.md (slash command)
    │  $ARGUMENTS → "Hooks ve MCP nedir, nasıl entegre edilir?"
    ▼
Skill: query-orchestrator (~/.claude/skills/query-orchestrator/SKILL.md)
    │
    ├── Step 1: Parse → 3 sub-questions
    ├── Step 2: Generate task ID = QUERY-TASK-hooks-1715432100123
    ├── Step 3: mkdir ~/.claude-code-docs/query/<TASK_ID>/
    ├── Step 4: Write query.md (template-filled with pending placeholders)
    ├── Step 5: Dispatch subagents in batches of 3
    │      ┌──────────────┬──────────────┬──────────────┐
    │      │ Task(Q1)     │ Task(Q2)     │ Task(Q3)     │  (parallel, single message)
    │      └──────┬───────┴──────┬───────┴──────┬───────┘
    │             ▼              ▼              ▼
    │      query-researcher (×3, each writes one QUERY-N.md)
    │             │              │              │
    │             ▼              ▼              ▼
    │      QUERY-1.md      QUERY-2.md      QUERY-3.md
    │
    ├── Step 6: Read all QUERY-N.md in parallel, assemble into query.md
    │       (single Write overwrites query.md with all answers embedded)
    └── Step 7: Chat summary + path
```

### Storage layout

**Repo-side (committed):**
- `docs/DOCS_MAP.md` — auto-generated map, committed by workflow
- `scripts/build_docs_map.py` — deterministic map generator (stdlib only)
- `claude-files/commands/query.md` — slash command source
- `claude-files/agents/query-researcher.md` — subagent source
- `claude-files/skills/query-orchestrator/SKILL.md` — orchestrator skill source
- `.github/workflows/build-docs-map.yml` — workflow that regenerates the map

**User-side (after install.sh):**
- `~/.claude/commands/query.md` — copied from repo
- `~/.claude/agents/query-researcher.md` — copied from repo
- `~/.claude/skills/query-orchestrator/SKILL.md` — copied from repo
- `~/.claude-code-docs/query/` — user query workspace (gitignored, user data)
- `~/.claude-code-docs/docs/DOCS_MAP.md` — pulled from the cloned repo

## 4. Repo Structure (after change)

```
claude-code-docs/
├── docs/                                       (existing, +1 generated file)
│   ├── ... 127 existing docs ...
│   └── DOCS_MAP.md                             ← NEW (auto-generated, committed)
│
├── scripts/                                    (existing, +1 file)
│   ├── claude-docs-helper.sh.template          (unchanged)
│   ├── fetch_claude_docs.py                    (unchanged)
│   ├── requirements.txt                        (unchanged)
│   └── build_docs_map.py                       ← NEW (Python stdlib only)
│
├── claude-files/                               ← NEW folder
│   ├── commands/
│   │   └── query.md
│   ├── agents/
│   │   └── query-researcher.md
│   └── skills/
│       └── query-orchestrator/
│           └── SKILL.md
│
├── .github/workflows/                          (existing, +1 file)
│   ├── update-docs.yml                         (unchanged)
│   ├── release.yml                             (unchanged)
│   └── build-docs-map.yml                      ← NEW
│
├── install.sh                                  ← MODIFIED (~30 lines appended)
├── uninstall.sh                                ← MODIFIED (~15 lines appended)
├── README.md                                   ← MODIFIED (+1 section)
├── CLAUDE.md                                   ← MODIFIED (+1 section)
└── specs/
    └── 2026-05-11-query-orchestrator-design.md ← This document
```

Rationale: `scripts/` stays code-only (Unix convention). `claude-files/` mirrors the install target (`~/.claude/`) so the install.sh copy logic is a parallel directory walk.

## 5. Map Generation

### Script: `scripts/build_docs_map.py`

**Inputs:** `docs/*.md` (top-level, non-recursive, excluding `DOCS_MAP.md`)
**Output:** `docs/DOCS_MAP.md`
**Dependencies:** Python 3.11+ stdlib only (no pip installs)

**Algorithm per file:**

1. **Title:** First `# H1` in content. Fallback: filename slug → title case (e.g., `agent-sdk__hooks.md` → "Agent Sdk / Hooks").
2. **Summary:** After stripping YAML frontmatter, find the first non-heading non-empty paragraph that is not a code block, list, or blockquote. Strip markdown syntax. Cap at 200 chars: prefer breaking at the last sentence end within the cap; if no sentence end falls past 60% of the cap, hard-truncate with `...`.
3. **Keywords:** TF-IDF across all docs. Top 8 terms by score. Stopword filter includes English common words + Claude Code-specific high-frequency terms (`claude`, `code`, `anthropic`, `docs`).

**Categorization:** Filename prefix groups files in the output map:
- `agent-sdk__*` → **Agent SDK** section
- `whats-new__*` → **Weekly Updates** section
- Everything else → **General** section

**Token budget:** ~150 tokens per entry × 127 entries ≈ 19K tokens. Acceptable for skill load.

### Output format

```markdown
# Docs Map

> Auto-generated by `scripts/build_docs_map.py` on 2026-05-11 12:00 UTC
> 127 files indexed.

Used by the `/query` skill to identify relevant docs for a given question.
Each entry shows the file, its title, a short summary, and discriminative keywords (TF-IDF).

---

## Agent SDK

### `agent-sdk__hooks.md`
**Title:** Hooks
**Summary:** Configure event-driven automation in the Agent SDK with PreToolUse, PostToolUse, Stop, and other hook events to validate, modify, or block tool execution.
**Keywords:** hooks, pretooluse, posttoouse, stop, event, hook_event_name, exitcode, blocking

(... more entries ...)

## Weekly Updates

### `whats-new__2026-w19.md`
**Title:** What's new — Week 19 2026
**Summary:** Release notes for the week of May 4-10, 2026...
**Keywords:** ...

## General

### `hooks.md`
**Title:** Hooks
**Summary:** ...
**Keywords:** ...
```

## 6. Slash Command

### `claude-files/commands/query.md`

```markdown
---
description: Research Claude Code documentation by batching multi-question queries to specialized subagents
argument-hint: <your question(s) — single or multi-part>
---

The user has invoked /query with the following input:

$ARGUMENTS

Use the Skill tool to invoke the `query-orchestrator` skill. Pass the user query above as the skill's argument. Follow the skill's instructions exactly.
```

The command is a thin trigger — all logic is in the skill.

## 7. Skill: query-orchestrator

### `claude-files/skills/query-orchestrator/SKILL.md`

**Frontmatter:**
```yaml
---
name: query-orchestrator
description: Use when handling /query slash command — parses multi-part questions, dispatches batched subagents to research docs, and assembles final answer
---
```

**Procedure (7 steps):**

**Step 1 — Parse user query into sub-questions**

Rules:
- One cohesive question → N=1
- Explicit numbering (1./2./3. or bulleted) → follow numbering
- Independent parts joined by `and`/`ve` → split
- Each sub-question must be answerable independently from docs

**Step 2 — Generate task ID**

- Extract first sub-question's most discriminative content word (skip stopwords like `the`, `a`, `what`, `how`, `is`, `does`).
- Slugify: lowercase, ASCII, hyphens.
- If no content word can be identified (e.g., "How does it work?"), fall back to the literal keyword `query`.
- Append epoch milliseconds via Bash: `date +%s%3N`.
- Format: `QUERY-TASK-<keyword>-<epoch_ms>`.
- Example: `QUERY-TASK-hooks-1715432100123`.
- Fallback example: `QUERY-TASK-query-1715432100123`.

**Step 3 — Create task folder**

```bash
mkdir -p ~/.claude-code-docs/query/<TASK_ID>
```

**Step 4 — Write initial query.md from template**

Template (inline in SKILL.md):

```markdown
# Query Task: {TASK_ID}

**Original user query:**
> {ORIGINAL_USER_INPUT}

**Created at:** {ISO_TIMESTAMP}
**Number of sub-questions:** {N}
**Status:** in-progress

---

## [QUERY-1] — {SHORT_TITLE_1}

**Question:** {SUB_QUESTION_1}

**Answer:**
<!-- ANSWER-1-START -->
_pending — researcher dispatched_
<!-- ANSWER-1-END -->

---

## [QUERY-2] — {SHORT_TITLE_2}

(... repeat for N ...)
```

`SHORT_TITLE_n` is a 3-5 word descriptor derived from each sub-question.

**Step 5 — Dispatch subagents in batches of 3**

CRITICAL: All Task tool calls in one batch MUST be sent in a SINGLE message to execute in parallel.

| N  | Batches |
|----|---------|
| 1  | [1]     |
| 2  | [2]     |
| 3  | [3]     |
| 4  | [3, 1]  |
| 5  | [3, 2]  |
| 7  | [3, 3, 1] |
| 15 | [3, 3, 3, 3, 3] |

Each Task call:
```
subagent_type: query-researcher
description: "Research [QUERY-N]"
prompt: |
  Task: <TASK_ID>
  Query ID: [QUERY-N]
  Question: <sub-question text>
  Output file: ~/.claude-code-docs/query/<TASK_ID>/QUERY-<N>.md
  Docs map: ~/.claude-code-docs/docs/DOCS_MAP.md
  Docs folder: ~/.claude-code-docs/docs/
```

Wait for ALL calls in a batch to return before issuing the next batch.

**Step 6 — Assemble answers into query.md**

After all batches:
1. Issue parallel Read calls for every `QUERY-N.md` (single message, N Read calls).
2. For each file, extract content below the H1 header.
3. Build the complete final `query.md` in memory:
   - Header (task id, original query, timestamp, N, **Status: complete**)
   - For each [QUERY-N]: question + the extracted body (replacing the `_pending_` placeholder)
4. Single Write call overwrites `query.md`.

Missing file handling: if a `QUERY-N.md` does not exist, insert:
> ⚠️ Researcher did not complete this query. Re-run `/query` for just this question.

**Step 7 — Chat summary**

```
✓ Query complete: <TASK_ID> (<N> questions)

• [QUERY-1] <one-line synthesis>
• [QUERY-2] <one-line synthesis>
• ...

Full details: ~/.claude-code-docs/query/<TASK_ID>/query.md
```

### Failure modes

| Failure | Handling |
|---------|----------|
| `mkdir` fails | Abort with error message |
| DOCS_MAP.md missing | Tell user to re-run install.sh |
| Subagent returns no file | Insert warning placeholder, continue with others |
| Parsing yields N=0 | Ask user to rephrase |
| Template inline placeholder unmatched | Fail loudly |

## 8. Subagent: query-researcher

### `claude-files/agents/query-researcher.md`

**Frontmatter:**
```yaml
---
name: query-researcher
description: Research a single sub-question by reading Claude Code documentation and producing a structured answer file
tools: Read, Grep, Glob, Write, Bash
---
```

**Tools rationale:**
- `Read`, `Grep`, `Glob`, `Bash`: read and search docs
- `Write`: produce the single output file
- NO `Edit` (only writes new file)
- NO `Task` (no recursion)
- NO `WebFetch` (local docs only)

**Procedure (4 steps):**

1. **Pick relevant docs (max 5):** Read DOCS_MAP.md, match question against title/summary/keywords. Prefer specific docs over `overview.md`. May use `grep -l "term" ~/.claude-code-docs/docs/*.md | head -5` for term-specific searches.

2. **Read selected docs.** Hard cap 5. If a referenced doc is clearly more relevant, swap rather than add.

3. **Synthesize answer** — 200-500 words typical, with citations.

4. **Write output file** in exact structure:

```markdown
# Answer to [QUERY-N]

**Question:** <restated>
**Task:** <TASK_ID>

## Researched files

- `docs/file1.md` — why relevant
- `docs/file2.md` — why relevant

## Answer

<synthesized answer with markdown formatting>

## Source excerpts

> Short relevant quote from file1.md

> Short relevant quote from file2.md

## Notes

<gaps, ambiguities, or "none">
```

When the orchestrator assembles, everything below the H1 (`# Answer to [QUERY-N]`) becomes the answer body that replaces the `_pending_` placeholder in `query.md`. So the user sees question + researched files + answer + sources + notes in the final document.

## 9. GitHub Workflow

### `.github/workflows/build-docs-map.yml`

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
      - run: python scripts/build_docs_map.py
      - name: Commit if changed
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          if [[ -n "$(git status --porcelain docs/DOCS_MAP.md)" ]]; then
            git add docs/DOCS_MAP.md
            git commit -m "Update DOCS_MAP.md - $(date +'%Y-%m-%d')"
            git push
          fi
```

**Trigger rationale:**
- `workflow_run` after `Update Claude Code Documentation` completes successfully → fresh map after every docs sync (required because `GITHUB_TOKEN` pushes do not fire `push` triggers).
- `push` on `scripts/build_docs_map.py` → regenerate when the script itself changes (uses default `GITHUB_TOKEN` push from contributors, which DOES fire on PR merges).
- `workflow_dispatch` → manual.

## 10. install.sh / uninstall.sh changes

### install.sh — append a new block after `/docs` setup

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

- Existing `/docs` setup is untouched
- Idempotent (overwrites on re-run, providing upgrade path)
- Graceful degradation if `claude-files/` is missing (older repo checkouts)

### uninstall.sh — append a new block

```bash
# Remove /query feature files
echo ""
echo "Removing /query feature..."

[[ -f ~/.claude/commands/query.md ]] && rm -f ~/.claude/commands/query.md && echo "✓ Removed /query command"
[[ -f ~/.claude/agents/query-researcher.md ]] && rm -f ~/.claude/agents/query-researcher.md && echo "✓ Removed query-researcher agent"
[[ -d ~/.claude/skills/query-orchestrator ]] && rm -rf ~/.claude/skills/query-orchestrator && echo "✓ Removed query-orchestrator skill"

# Ask before removing query outputs (user data!)
if [[ -d "$HOME/.claude-code-docs/query" ]] && [[ -n "$(ls -A "$HOME/.claude-code-docs/query" 2>/dev/null)" ]]; then
    echo ""
    echo "⚠️  Found query outputs at $HOME/.claude-code-docs/query/"
    read -p "Delete query history? (y/N): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] && rm -rf "$HOME/.claude-code-docs/query" && echo "✓ Removed query history"
fi
```

User query data is treated as protected — only removed on explicit confirmation.

## 11. README.md / CLAUDE.md updates

**README.md** — add a `/query` subsection under "Usage":

```markdown
### Multi-question research with /query

`/query` parses your input into sub-questions, dispatches research subagents in batches of 3 in parallel, and assembles a structured answer file.

```bash
/query What is a hook?                          # single question
/query Explain hooks and MCP, then compare them # multi-part
/query 1. ... 2. ... 3. ...                     # explicit numbering
```

Each query produces a folder under `~/.claude-code-docs/query/QUERY-TASK-<keyword>-<id>/`
containing the full structured answer with citations. Useful for non-trivial questions that span multiple docs.
```

**CLAUDE.md** — add a `/query` section and extend the ultrathink list:

```markdown
## For /query Command

When responding to /query commands:
1. Invoke the query-orchestrator skill via the Skill tool
2. Follow the skill's 7-step procedure (parse → task ID → folder → template → batch dispatch → assemble → summary)
3. Subagents read from docs/ folder via DOCS_MAP.md
4. Outputs accumulate in ~/.claude-code-docs/query/
```

Add to "Files to ultrathink about":
- `@docs/DOCS_MAP.md`
- `@scripts/build_docs_map.py`
- `@claude-files/`

## 12. Test Plan

### Unit (automated)

Add `scripts/test_build_docs_map.py` with fixtures covering:
- Title extraction (with H1, without H1, with frontmatter)
- Summary extraction (skipping code blocks, lists, blockquotes)
- TF-IDF keyword selection across 3 sample docs
- Stopword filtering

### Manual (release gate)

1. Clean macOS / Linux system → `bash install.sh`
2. Verify file presence:
   - `~/.claude/commands/query.md`
   - `~/.claude/agents/query-researcher.md`
   - `~/.claude/skills/query-orchestrator/SKILL.md`
   - `~/.claude-code-docs/query/` exists, empty
3. Restart Claude Code → `/query What is a hook?` (N=1)
4. `/query Explain hooks and MCP and how to integrate them` (N=3, single batch of 3 parallel)
5. `/query 1. ... 2. ... 3. ... 4. ... 5. ...` (N=5, batches [3,2])
6. `/query` with 15 explicit questions (5 batches of 3)
7. Edge case: temporarily delete DOCS_MAP.md → skill produces a clear error
8. Edge case: kill one subagent mid-flight → orchestrator inserts warning placeholder for that QUERY-N
9. `bash uninstall.sh` → verify removal + query history prompt

### Workflow

- Manually trigger `build-docs-map.yml` via `workflow_dispatch` → DOCS_MAP.md correctly produced
- Run `update-docs.yml` manually → confirm `build-docs-map.yml` fires via `workflow_run` after success

## 13. Open Risks

1. **Subagent parallelism inconsistency.** Claude may sometimes serialize Task calls. The skill must explicitly state "MUST issue all calls in ONE message" with strong wording.
2. **Map token growth.** ~19K today, ~30K at 200 docs. Subagents read the whole map. Future iteration: pre-filter by category before dispatching to the subagent.
3. **PR size.** Large additive change. Break into 4 commits for easier review:
   - Commit 1: `scripts/build_docs_map.py` + initial DOCS_MAP.md
   - Commit 2: `.github/workflows/build-docs-map.yml`
   - Commit 3: `claude-files/` (command, agent, skill)
   - Commit 4: `install.sh` / `uninstall.sh` / README / CLAUDE.md updates
4. **Maintainer acceptance.** Feature is opinionated. Worth opening a discussion issue before the PR to gauge interest.

## 14. Acceptance Criteria

- [ ] `bash install.sh` on a clean machine installs all `/query` artifacts without errors
- [ ] `/query "What is a hook?"` produces a `query.md` with an assembled answer citing at least one doc file
- [ ] `/query` with 5 sub-questions produces exactly 5 `QUERY-N.md` files dispatched in 2 batches (parallel within each batch)
- [ ] `/query` with 15 sub-questions runs 5 batches; final `query.md` contains all 15 answers
- [ ] If a subagent fails, the assembled `query.md` shows a warning placeholder for that query, not a crash
- [ ] `bash uninstall.sh` removes all `/query` files; asks before deleting query history
- [ ] `scripts/build_docs_map.py` runs locally with no external dependencies and produces `docs/DOCS_MAP.md`
- [ ] `build-docs-map.yml` fires after `update-docs.yml` completes successfully
- [ ] Existing `/docs` command continues to work unchanged
