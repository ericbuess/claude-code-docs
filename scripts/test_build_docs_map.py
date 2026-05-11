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


from build_docs_map import tokenize, compute_tfidf, top_keywords


def test_tokenize_removes_stopwords():
    tokens = tokenize("The quick brown fox jumps over the lazy dog.")
    assert "quick" in tokens
    assert "brown" in tokens
    assert "the" not in tokens
    assert "over" not in tokens


def test_tokenize_strips_markdown():
    tokens = tokenize("`code` is **important** for [docs](url).")
    assert "code" not in tokens  # in backticks -> stripped
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
