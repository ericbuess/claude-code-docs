# Enhancements Directory

This directory contains comprehensive documentation for the enhanced features of claude-code-docs.

## Overview

The enhanced edition extends [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) with optional Python-based capabilities while maintaining full backward compatibility. This directory documents those enhancements.

## What's Inside

### Core Documentation

- **[FEATURES.md](FEATURES.md)** - Complete feature list and technical details
  - Documentation coverage (573 active paths tracked)
  - Full-text search capabilities
  - Path validation tools
  - Advanced search and filtering
  - Comprehensive testing (620 tests)
  - Performance benchmarks

- **[CAPABILITIES.md](CAPABILITIES.md)** - Detailed capability documentation
  - Documentation coverage breakdown (6 categories)
  - Search capabilities (path + content search)
  - Validation features (HTTP reachability testing)
  - Advanced features (change detection, batch operations)
  - Technical implementation details
  - Performance characteristics

- **[EXAMPLES.md](EXAMPLES.md)** - Practical usage examples
  - Using enhancements in Claude Code
  - The `/docs` command with examples
  - Command-line usage patterns
  - Common workflows
  - Tips and tricks

## Quick Start

### For Users

If you've installed the enhanced edition, you can:

1. **Search documentation**: `/docs <topic>`
2. **Browse categories**: `/docs --list-categories`
3. **Validate paths**: `/docs --validate`
4. **Content search**: `/docs --search-content <query>`

See [EXAMPLES.md](EXAMPLES.md) for detailed usage.

### For Developers

If you're working on the codebase:

1. **Understand capabilities**: Read [CAPABILITIES.md](CAPABILITIES.md)
2. **See technical details**: Read [FEATURES.md](FEATURES.md)
3. **Learn patterns**: Review [EXAMPLES.md](EXAMPLES.md)
4. **Check tests**: See `tests/` directory

## Architecture

### Single Installation with Graceful Degradation

The enhanced edition uses a single installation approach:

**Always Installed**:
- 573 documentation paths tracked in manifest
- 571 files downloaded
- Python scripts for enhanced features

**Runtime Behavior** (automatic feature detection):
- **Without Python 3.9+**: Basic documentation reading via `/docs` command
- **With Python 3.9+**: Full-text search, validation, fuzzy matching, auto-regeneration

No separate "modes" - features activate automatically based on Python availability.

### Key Components

**Documentation Coverage**:
- 6 categories of documentation
- 573 total paths
- All available English documentation

**Search System**:
- Path-based search (fuzzy matching)
- Content-based search (full-text)
- Category filtering
- Relevance ranking

**Validation System**:
- HTTP reachability testing
- Parallel validation (ThreadPoolExecutor)
- Detailed reporting
- Broken link detection

**Update System**:
- SHA256-based change detection
- Selective fetching (only changed docs)
- Batch operations
- Rate limiting and retry logic

## Category Breakdown

The 573 documentation paths are organized into:

1. **API Reference** (377 paths - 65.8%)
   - Complete API docs, Admin API, Agent SDK, multi-language SDK docs (Python, TypeScript, Go, Java, Kotlin, Ruby)

2. **Core Documentation** (82 paths - 14.3%)
   - About Claude, Build with Claude, Test and Evaluate, Guides

3. **Prompt Library** (65 paths - 11.3%)
   - 65 unique prompt templates

4. **Claude Code** (46 paths - 8.0%)
   - CLI-specific docs, hooks, skills, MCP, IDE integrations

5. **Release Notes** (2 paths - 0.3%)
   - Overview and system prompts updates

6. **Resources** (1 path - 0.2%)
   - Resources overview

## Performance

Key performance metrics:

- **Search**: <100ms per query
- **Fetch**: ~32s per 100 paths
- **Validation**: ~60s for all 573 paths
- **Memory**: ~35 MB typical usage
- **Index size**: ~45KB

## Files in This Directory

```
enhancements/
├── README.md          # This file - directory overview
├── FEATURES.md        # Complete feature list and specs
├── CAPABILITIES.md    # Detailed capability documentation
└── EXAMPLES.md        # Usage examples and patterns
```

## Related Documentation

### In Repository Root

- **README.md** - Main repository documentation
- **CONTRIBUTING.md** - Contribution guidelines
- **CLAUDE.md** - Project architecture and instructions
- **CHANGELOG.md** - Version history

### For Developers

- **docs-dev/** - Developer documentation (if exists)
- **tests/** - Test suite (294 tests)
- **scripts/** - Python implementation scripts

## Use Cases

### Individual Users

- Quick access to Anthropic documentation
- Offline documentation browsing
- Fast search across all docs
- Topic discovery

### Development Teams

- CI/CD integration testing
- Documentation validation
- Custom tooling development
- Content analysis

### Contributors

- Path discovery and coverage
- Quality assurance
- Update automation
- Feature development

## Getting Started

1. **Installation**: Follow installation guide in root README.md
2. **Basic usage**: See [EXAMPLES.md](EXAMPLES.md) Quick Start
3. **Advanced features**: Read [CAPABILITIES.md](CAPABILITIES.md)
4. **Development**: See [FEATURES.md](FEATURES.md) technical details

## Contributing to Enhancements

Interested in contributing? See:

1. Root **CONTRIBUTING.md** for general guidelines
2. **CLAUDE.md** for project architecture
3. **FEATURES.md** for technical implementation
4. **tests/** directory for test patterns

## Upstream Compatibility

All enhancements are designed to be:

- **Optional**: Standard mode works without Python
- **Backward compatible**: Doesn't break upstream functionality
- **Well tested**: 294 tests with 99.3% pass rate (294 passing, 2 skipped)
- **Documented**: Comprehensive documentation
- **Modular**: Can adopt features independently

## Potential Upstream Contribution

These enhancements are designed for potential contribution back to upstream:

**Proposed PRs**:
1. Optional enhanced mode installation
2. Extended path coverage (573 paths)
3. Full-text search capability
4. Testing framework
5. Enhanced documentation

See [FEATURES.md](FEATURES.md) for details on upstream contribution strategy.

## Support

### Questions?

- **Feature questions**: See [CAPABILITIES.md](CAPABILITIES.md)
- **Usage help**: See [EXAMPLES.md](EXAMPLES.md)
- **Installation**: See root README.md
- **Contributing**: See CONTRIBUTING.md

### Issues?

If you encounter issues with enhanced features:

1. Check [EXAMPLES.md](EXAMPLES.md) for correct usage
2. Verify Python 3.9+ is installed
3. Check paths_manifest.json exists
4. Run validation: `/docs --validate`
5. Review test output: `pytest tests/ -v`

## Version Information

Current enhanced edition version: See CHANGELOG.md in repository root

Last documentation update: 2025-11-06

## License

Enhancements provided under same license as upstream. See LICENSE file in repository root.

## Acknowledgments

Built on the excellent foundation of [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs).

Enhanced features developed to provide comprehensive coverage of Anthropic's documentation ecosystem while maintaining full compatibility with upstream.
