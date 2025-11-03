# Claude Code Documentation Mirror - Project Instructions

> This file provides guidance to Claude Code when working in this repository.
>
> **Project Goal**: Build a production-ready Claude documentation mirror (550+ pages) with automated updates, enhanced features, and comprehensive testing.

## Quick Context

@README.md - Project overview and status
@REPOSITORY_STRUCTURE.md - Repository organization
@specs/IMPLEMENTATION_PLAN.md - Complete 7-phase roadmap
@specs/IMPLEMENTATIONMONITOR.md - Progress tracking

**Current Status**: Phase 1 complete. Repository restructured with upstream integration. Ready for Phase 2.

**Current Branch**: `development` (push here)
**Upstream Reference**: `./upstream/` (costiash/claude-code-docs clone - reference only, gitignored)

## Project Structure

* **`docs/`** - 47 mirrored Claude Code documentation files (from upstream)
* **`scripts/`** - Python utilities
  * `fetch_claude_docs.py` - Upstream's production fetcher (reference)
  * `main.py` - Our enhanced fetcher (to be developed)
  * `extract_paths.py` - Path extraction and cleaning tool
* **`specs/`** - Implementation planning documents (7-phase plan)
* **`analysis/`** - Phase 1 analysis of upstream implementation
* **`upstream/`** - Reference clone of costiash/claude-code-docs (gitignored)
* **`.github/workflows/`** - GitHub Actions for automation

## Code Style & Standards

* Use Python 3.12+ features and type hints on all functions
* Follow PEP 8 style guide
* Write clear docstrings for all public functions
* Test coverage target: **85% minimum** (enforced in CI/CD)
* Use descriptive variable names over abbreviations

## Working with This Project

### Git Workflow

* **Development branch**: All work happens here (current)
* **Main branch**: Production-ready code only
* Always commit with descriptive messages
* Reference file:line numbers when discussing code (e.g., `scripts/main.py:42`)

### Before Making Changes

1. Read relevant specs in `@specs/IMPLEMENTATION_PLAN.md`
2. Check `@specs/IMPLEMENTATIONMONITOR.md` for current progress
3. Review `@analysis/` documents for upstream implementation patterns

### After Completing Work

1. Update `@specs/IMPLEMENTATIONMONITOR.md` checkboxes
2. Run tests before committing
3. Update documentation if adding features

## Phase Execution Guidelines

### How to Execute Phases

* **Use Task tool with general-purpose agent** for all phase execution (see `@specs/execution_template.md`)
* Each phase has a ready-to-use prompt template
* ALWAYS update `@specs/IMPLEMENTATIONMONITOR.md` after completing tasks
* Phases must be executed sequentially (1→2→3→4→5→6→7)

### Current Phase: Phase 2 - Path Extraction & Cleaning

Next steps:
1. Enhance `scripts/extract_paths.py` with categorization logic
2. Clean 631 raw paths → 550 unique paths
3. Generate `paths_manifest.json` with categories
4. Create statistics report

Estimated time: 20 minutes

### Phase Completion Checklist

Before marking any phase complete:
* ✅ All deliverables created
* ✅ IMPLEMENTATIONMONITOR.md updated
* ✅ Tests pass (if applicable)
* ✅ Changes committed to `development` branch

### 7-Phase Implementation Plan

1. **Phase 1** ✅ COMPLETE - Repository Setup & Analysis (30min)
2. **Phase 2** ⏳ NEXT - Path Extraction & Cleaning (20min)
3. **Phase 3** - Script Development (2hrs)
4. **Phase 4** - Integration & Adaptation (1.5hrs)
5. **Phase 5** - Comprehensive Testing (2.5hrs)
6. **Phase 6** - Documentation (45min)
7. **Phase 7** - Validation & QA (1hr)

**Total**: 8-9 hours | **Progress**: 14% (4/28 tasks complete)

## Technical Specifications

### Path Categorization

Use these rules when working with paths:
* `/en/docs/` (excluding claude-code) → `core_documentation`
* `/en/api/` → `api_reference`
* `/en/docs/claude-code/` → `claude_code`
* `/en/prompt-library/` → `prompt_library`

Target: ~550 unique paths (cleaned from 631 raw)

### Fetching Implementation

**Key Discovery from Phase 1**:
* No HTML parsing needed! Docs site serves markdown directly at `.md` URLs
* Only need `requests==2.32.4` - no beautifulsoup4 or markdownify
* Use upstream's proven patterns: retry logic, rate limiting, SHA256 change detection

### Testing Requirements

* **Minimum coverage**: 85% (enforced in CI/CD)
* **Required suites**: Unit, Integration, Validation
* **Before marking phase complete**: All tests must pass

## Common Commands

### Current (Development Phase)

```bash
# Check project status
git status

# Run Phase 2 path extraction
python scripts/extract_paths.py --source temp.html --output paths_manifest.json

# Commit changes
git add . && git commit -m "Phase 2: Path extraction complete"
git push origin development
```

### Future (Post-Implementation)

```bash
# Run tests
pytest

# Check coverage (85% minimum)
pytest --cov=scripts --cov-report=term

# Update documentation
python scripts/main.py --update-all

# Search paths
python scripts/lookup_paths.py "hooks"
```

## Important Rules

### Phase Execution

* Use Task tool with general-purpose agent (see `@specs/execution_template.md`)
* Execute phases in order: 1→2→3→4→5→6→7
* ALWAYS update `@specs/IMPLEMENTATIONMONITOR.md` after completing work
* Don't skip phases - each builds on the previous

### Testing

* All new code needs unit tests minimum
* 85%+ coverage is mandatory
* Tests must pass before marking phase complete

### Upstream Reference

When implementing features, reference:
* `@upstream/scripts/fetch_claude_docs.py` - Production fetcher (646 lines)
* `@analysis/fetch_mechanism.md` - Implementation analysis
* `@analysis/path_mapping.md` - Path mapping rules

## Success Criteria

When all 7 phases are complete:
* ✅ 550+ documentation pages mirrored locally
* ✅ Auto-updates every 3 hours via GitHub Actions
* ✅ 85%+ test coverage achieved
* ✅ All tests passing
* ✅ Path validation working
* ✅ Complete documentation written

Performance targets:
* Fetch time: < 2 minutes per 100 pages
* Memory usage: < 500 MB during processing
* Path reachability: > 99%

## Dependencies

**Current**:
* Python 3.12+
* requests==2.32.4

**Future (Phase 3+)**:
* pytest + pytest-cov (testing only)
* No HTML parsing libraries needed (markdown served directly!)

## Quick Start for Contributors

1. Clone and setup: `git clone <repo> && cd claude-code-docs`
2. Check current phase: See "Current Phase" section above
3. Read phase template: `@specs/execution_template.md`
4. Execute with Task tool
5. Update progress: `@specs/IMPLEMENTATIONMONITOR.md`

## Useful File References

* `@README.md` - Project overview
* `@REPOSITORY_STRUCTURE.md` - Repository organization
* `@specs/IMPLEMENTATION_PLAN.md` - Complete 7-phase plan with rationale
* `@specs/IMPLEMENTATIONMONITOR.md` - Progress tracking
* `@analysis/fetch_mechanism.md` - Upstream implementation analysis

---

**Remember**: Use @ to reference files, update IMPLEMENTATIONMONITOR.md after completing work, and always test before committing!
