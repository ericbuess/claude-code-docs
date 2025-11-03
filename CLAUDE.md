# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code Documentation Mirror** project designed to create a local mirror of Anthropic's Claude documentation (550+ pages) with automated updates and fast offline access. The project is currently in the **planning/specification phase** with a 7-phase implementation plan ready for execution.

**Status**: Phase 0 complete (specifications created). Implementation awaits execution starting with Phase 1.

**Key Goal**: Build production-ready documentation fetching, mirroring, and validation system integrated with costiash/claude-code-docs approach.

## Architecture Overview

### Three-Document Planning System

The project uses a structured approach with three critical specification documents in `specs/`:

1. **IMPLEMENTATION_PLAN.md** - Complete 7-phase roadmap (8-9 hours of work)
   - Detailed tasks, deliverables, and success criteria for each phase
   - Technical decisions and rationale
   - Timeline and validation requirements

2. **IMPLEMENTATIONMONITOR.md** - Progress tracking with checkboxes
   - 28 tasks across 7 phases
   - Phase completion tracking and sign-off sections
   - Overall project status dashboard

3. **execution_template.md** - Ready-to-use prompts for Task tool
   - Complete template prompts for each phase
   - Designed for autonomous execution via Task tool with general-purpose agent
   - **Critical**: Each phase template includes mandatory instructions to update IMPLEMENTATIONMONITOR.md

### Planned Final Architecture (Post-Implementation)

```
claude-code-docs/
├── docs/              # Mirrored documentation (550+ pages)
│   └── en/
│       ├── docs/      # Core documentation (~280 paths)
│       ├── api/       # API reference (~95 paths)
│       ├── prompt-library/  # Prompt library (~105 paths)
│       └── resources/
├── scripts/           # Python utilities (to be created)
│   ├── main.py           # Documentation fetcher
│   ├── extract_paths.py  # Path extraction & cleaning
│   ├── lookup_paths.py   # Search & validation
│   └── update_sitemap.py # Sitemap management
├── tests/             # Test suite (85%+ coverage target)
│   ├── unit/
│   ├── integration/
│   └── validation/
├── .github/workflows/ # CI/CD automation
│   ├── update-docs.yml   # Auto-update every 3 hours
│   ├── test.yml          # Test suite
│   └── validate.yml      # Daily validation
├── .claude/           # Claude Code integration
│   └── commands/
│       ├── docs.md         # Natural language doc search
│       ├── update-docs.md  # Trigger updates
│       └── search-docs.md  # Path search
├── specs/             # Implementation specifications
├── upstream/          # Reference: costiash/claude-code-docs clone
└── analysis/          # Analysis documents (created in Phase 1)
```

## Current State

### Existing Files

- **temp.html** (3.8MB) - Complete sitemap of Claude documentation
- **extracted_paths.txt** (631 paths) - Raw extraction (needs cleaning)
- **extract_paths.py** - Basic path extraction (needs enhancement)
- **main.py** - Placeholder (needs full implementation)
- **pyproject.toml** - Project config (Python 3.12+, requests library)

### Specifications Created

- `specs/IMPLEMENTATION_PLAN.md` - Comprehensive 7-phase plan
- `specs/IMPLEMENTATIONMONITOR.md` - Detailed progress tracker
- `specs/execution_template.md` - Phase execution templates

## Executing the Implementation

### Phase Execution Workflow

**CRITICAL**: Use the Task tool with general-purpose agent for each phase:

1. **Read the phase template** from `specs/execution_template.md`
2. **Copy the complete prompt** for the desired phase
3. **Invoke Task tool**:
   ```
   Task(
     subagent_type="general-purpose",
     description="Phase X: [Phase Name]",
     prompt="[Complete phase template from execution_template.md]"
   )
   ```
4. **Agent autonomously executes** all tasks in the phase
5. **Agent MUST update** `specs/IMPLEMENTATIONMONITOR.md` checkboxes
6. **Verify completion** before proceeding to next phase

### Phase Sequence (Must Execute in Order)

1. **Phase 1** (30min): Repository Setup & Analysis
   - Clone costiash/claude-code-docs to `./upstream/`
   - Analyze their structure and fetching mechanism
   - Create analysis documents in `./analysis/`

2. **Phase 2** (20min): Path Extraction & Cleaning
   - Enhance `extract_paths.py` with categorization
   - Clean 631 paths → 550 unique paths
   - Generate `paths_manifest.json` with categories
   - Create statistics report

3. **Phase 3** (2hrs): Script Development
   - Implement `main.py` as production fetcher (500+ lines)
   - Create `update_sitemap.py` for sitemap management
   - Create `lookup_paths.py` for search/validation
   - Add CLI interfaces to all scripts

4. **Phase 4** (1.5hrs): Integration & Adaptation
   - Reorganize to match costiash directory structure
   - Configure `.claude/commands/` integration
   - Setup GitHub Actions workflows
   - Configure version control

5. **Phase 5** (2.5hrs): Comprehensive Testing Suite
   - Create 20+ unit tests
   - Create 10+ integration tests
   - Create 15+ validation tests
   - Setup CI/CD pipelines
   - Target: 85%+ code coverage

6. **Phase 6** (45min): Documentation & Guidelines
   - Update README.md with complete docs
   - Create DEVELOPMENT.md contributor guide
   - Create docs/CAPABILITIES.md feature docs
   - Create docs/EXAMPLES.md with examples

7. **Phase 7** (1hr): Validation & Quality Assurance
   - Run full test suite
   - Manual validation (20 random paths)
   - Performance testing
   - Security review
   - Final integration test

## Key Technical Decisions

### Documentation Scope
- **Categories**: Core Docs + API Reference + Claude Code + Prompt Library
- **Total paths**: ~550 (cleaned from 631 raw)
- **Excludes**: Deprecated/legacy content

### Integration Strategy
- **Approach**: Clone and adapt locally from costiash/claude-code-docs
- **Rationale**: Learn from proven implementation

### Content Fetching
- **Method**: Match costiash approach exactly
- **Source**: https://docs.anthropic.com
- **Format**: HTML → Markdown conversion

### Testing Requirements
- **Coverage**: 85%+ required
- **Suites**: Unit + Integration + Validation
- **CI/CD**: GitHub Actions with automated testing

### Update Automation
- **Frequency**: Every 3 hours via GitHub Actions
- **Change detection**: Content hash comparison
- **Changelog**: Automatic generation

## Development Commands (Post-Implementation)

### Path Management
```bash
# Extract and clean paths from sitemap
python scripts/extract_paths.py --source temp.html --output paths_manifest.json

# Show statistics
python scripts/extract_paths.py --stats

# Validate paths
python scripts/extract_paths.py --validate
```

### Documentation Fetching
```bash
# Update all documentation
python scripts/main.py --update-all

# Update specific category
python scripts/main.py --update-category core
python scripts/main.py --update-category api_reference
python scripts/main.py --update-category claude_code
python scripts/main.py --update-category prompt_library

# Force re-fetch (ignore cache)
python scripts/main.py --force
```

### Path Search & Validation
```bash
# Search for paths
python scripts/lookup_paths.py "prompt engineering"
python scripts/lookup_paths.py "mcp"

# Validate specific path
python scripts/lookup_paths.py --check /en/docs/build-with-claude

# Validate all 550+ paths
python scripts/lookup_paths.py --validate-all
```

### Testing
```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/validation/ -v

# Run with coverage
pytest --cov=scripts --cov-report=html --cov-report=term

# Check coverage threshold (85%)
coverage report --fail-under=85
```

### Claude Code Integration
```bash
# Natural language documentation search
/docs how to use tool use with python

# Update documentation
/update-docs

# Search paths
/search-docs mcp integration

# Validate documentation
/validate-docs
```

## Critical Implementation Notes

### ALWAYS Use Task Tool for Phase Execution

**Do NOT execute phases directly**. Each phase template in `execution_template.md` is designed for autonomous execution via the Task tool with the general-purpose agent. This ensures:

- Complete context is provided
- All tasks are executed systematically
- IMPLEMENTATIONMONITOR.md is updated properly
- Deliverables are validated before phase completion

### Progress Tracking is Mandatory

After completing any phase or task:
1. ✅ Mark checkboxes in `specs/IMPLEMENTATIONMONITOR.md`
2. ✅ Fill in completion dates and durations
3. ✅ Document any issues encountered
4. ✅ Update overall project statistics

### Sequential Phase Execution

Phases MUST be executed in order (1→2→3→4→5→6→7). Each phase builds on deliverables from previous phases. Do not skip ahead.

### Testing Requirements

- All new code requires tests (unit tests minimum)
- 85%+ coverage is mandatory (checked in CI/CD)
- All tests must pass before marking phase complete
- Integration test required before production

### Path Categorization Logic

When working with paths, use these category assignments:
- `/en/docs/` (excluding claude-code) → `core_documentation`
- `/en/api/` → `api_reference`
- `/en/docs/claude-code/` → `claude_code`
- `/en/prompt-library/` → `prompt_library`

### Upstream Reference

The costiash/claude-code-docs repository (cloned to `./upstream/` in Phase 1) is the reference implementation. Match their:
- Directory structure
- Fetching mechanism
- File naming conventions
- Documentation format

## Project Goals & Success Metrics

### Final Deliverables (All Phases Complete)

- [ ] 550+ documentation pages mirrored locally
- [ ] Automatic updates every 3 hours
- [ ] 85%+ test coverage
- [ ] Natural language search via `/docs` command
- [ ] Path validation and broken link detection
- [ ] Complete documentation (README, DEVELOPMENT, examples)
- [ ] GitHub Actions CI/CD pipeline
- [ ] Clean environment integration test passing

### Performance Targets

- Fetch time: < 2 minutes per 100 pages
- Memory usage: < 500 MB during processing
- Search performance: < 1 second per query
- Path reachability: > 99%

### Quality Standards

- All tests passing (100%)
- No critical security vulnerabilities
- Documentation clear and comprehensive
- Code follows PEP 8 style guide
- Type hints on all functions

## Dependencies

### Current
- Python 3.12+
- requests==2.32.4

### Planned (Phase 3+)
- beautifulsoup4 (HTML parsing)
- markdownify (HTML to Markdown)
- pytest + pytest-cov (testing)
- pytest-asyncio (async testing)

## Version Control

- Repository initialized (no commits yet)
- No remote configured (to be added in Phase 1)
- `.gitignore` configured for Python projects

## Next Steps

**Current Status**: Ready to begin Phase 1

**To Start Implementation**:
1. Read `specs/execution_template.md`
2. Copy Phase 1 template prompt
3. Invoke Task tool with general-purpose agent
4. Monitor progress in `specs/IMPLEMENTATIONMONITOR.md`

**Do NOT**:
- Execute phases manually without Task tool
- Skip progress tracking in IMPLEMENTATIONMONITOR.md
- Proceed to next phase without completing current phase
- Ignore testing requirements (85%+ coverage mandatory)
