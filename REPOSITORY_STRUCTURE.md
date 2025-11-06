# Repository Structure Design
## Merged claude-code-docs Structure

This document defines the final repository structure that merges:
- **Upstream**: costiash/claude-code-docs proven implementation
- **Our Additions**: Enhanced features, specifications, and analysis

---

## Final Directory Tree

```
claude-code-docs/
├── .github/
│   └── workflows/                    # ✅ GitHub Actions (COPIED from upstream)
│       ├── claude-code-review.yml    #    Auto PR reviews with Claude
│       ├── claude.yml                #    Respond to @claude mentions
│       └── update-docs.yml           #    Auto-fetch docs every 3 hours
│
├── docs/                             # 📚 Documentation mirror (TO COPY from upstream)
│   ├── *.md                          #    47 Claude Code doc files
│   └── docs_manifest.json            #    Documentation manifest
│
├── scripts/                          # 🛠️ Utilities (MERGE upstream + ours)
│   ├── fetch_claude_docs.py          #    FROM upstream - production fetcher
│   ├── claude-docs-helper.sh.template #   FROM upstream - helper script
│   ├── requirements.txt              #    FROM upstream - dependencies
│   ├── main.py                       #    OUR enhanced fetcher (MOVE from root)
│   ├── extract_paths.py              #    OUR path extraction tool (MOVE from root)
│   ├── lookup_paths.py               #    TO CREATE Phase 3 - path search
│   └── update_sitemap.py             #    TO CREATE Phase 3 - sitemap mgmt
│
├── specs/                            # 📋 OUR implementation plans (KEEP)
│   ├── IMPLEMENTATION_PLAN.md        #    7-phase implementation roadmap
│   ├── IMPLEMENTATIONMONITOR.md      #    Progress tracking with checkboxes
│   └── execution_template.md         #    Phase execution templates
│
├── analysis/                         # 🔍 OUR Phase 1 analysis (KEEP)
│   ├── repo_structure.md             #    Upstream repo analysis
│   ├── fetch_mechanism.md            #    Fetching implementation details
│   └── path_mapping.md               #    Path-to-file mapping rules
│
├── tests/                            # 🧪 Test suite (TO CREATE Phase 5)
│   ├── unit/                         #    Unit tests (85%+ coverage target)
│   ├── integration/                  #    Integration tests
│   └── validation/                   #    Path validation tests
│
├── upstream/                         # 🔄 Reference clone (KEEP for comparison)
│   └── [costiash/claude-code-docs]   #    Original repo for diffing & updates
│
├── .gitignore                        # Git ignore patterns (ENHANCE)
├── .python-version                   # Python version specification (KEEP)
├── pyproject.toml                    # Python project config (UPDATE)
├── uv.lock                           # UV dependency lock (KEEP)
│
├── temp.html                         # Raw sitemap HTML (KEEP - useful reference)
├── extracted_paths.txt               # Raw path extraction (KEEP - useful reference)
│
├── install.sh                        # Installation script (COPY from upstream, MAY ADAPT)
├── uninstall.sh                      # Uninstallation script (COPY from upstream)
├── LICENSE                           # License file (COPY from upstream)
├── UNINSTALL.md                      # Uninstall documentation (COPY from upstream)
│
├── CLAUDE.md                         # ⭐ OUR project instructions (KEEP & UPDATE)
├── README.md                         # ⭐ OUR project documentation (KEEP & UPDATE)
└── REPOSITORY_STRUCTURE.md           # This file (CREATED)
```

---

## Implementation Steps

### Step 1: Copy Core Directories ✅ (workflows done)
```bash
# Already done:
# ✅ .github/workflows/ copied

# To do:
cp -r upstream/docs/ docs/
cp -r upstream/scripts/ scripts/
```

### Step 2: Move Our Files to Proper Locations
```bash
# Move our scripts to scripts/ directory
mv main.py scripts/main.py
mv extract_paths.py scripts/extract_paths.py

# Keep these at root for reference
# - temp.html
# - extracted_paths.txt
```

### Step 3: Copy Additional Files
```bash
# Copy installation and documentation files
cp upstream/install.sh install.sh
cp upstream/uninstall.sh uninstall.sh
cp upstream/LICENSE LICENSE
cp upstream/UNINSTALL.md UNINSTALL.md
```

### Step 4: Update Configuration Files
```bash
# Update .gitignore to exclude:
# - upstream/ (keep as reference, don't commit)
# - temp files
# - Python cache

# Update pyproject.toml to include:
# - upstream dependencies (requests)
# - our additional dependencies (pytest, etc.)
```

---

## Rationale for Key Decisions

### 1. Keep `upstream/` Directory
**Decision**: Keep the cloned upstream repo at `./upstream/`

**Rationale**:
- Easy comparison: `diff scripts/fetch_claude_docs.py upstream/scripts/fetch_claude_docs.py`
- Track upstream updates: `cd upstream && git pull`
- Learn from reference implementation during development
- Can be excluded from our commits via .gitignore

### 2. Merge `scripts/` Directory
**Decision**: Combine upstream scripts + our enhanced scripts in single `scripts/` directory

**Rationale**:
- Maintains consistency with upstream structure
- Our scripts extend (not replace) upstream functionality
- Users can choose between upstream's fetcher or our enhanced version
- Clean organization: all utilities in one place

### 3. Keep Our Additions at Root
**Decision**: Keep `specs/`, `analysis/`, `CLAUDE.md`, `README.md` at root level

**Rationale**:
- `specs/` and `analysis/` are implementation-specific, not part of doc mirror
- Our `CLAUDE.md` explains our enhanced version vs upstream
- Our `README.md` documents our additional features
- Clear separation: upstream mirror vs our enhancements

### 4. Adopt Upstream's Installation Scripts
**Decision**: Copy `install.sh` and `uninstall.sh` from upstream

**Rationale**:
- Proven installation mechanism (538 lines, battle-tested)
- Handles edge cases we haven't considered
- May need minor adaptations for our features in Phase 4
- Starting point is better than writing from scratch

### 5. Future `tests/` Directory
**Decision**: Create comprehensive test suite in Phase 5

**Rationale**:
- 85%+ coverage requirement (per implementation plan)
- Separate unit/integration/validation concerns
- Clean structure for CI/CD integration
- Not present in upstream (opportunity for contribution)

---

## File Categories

### From Upstream (Copy As-Is)
- `docs/` - 47 markdown files + manifest
- `scripts/fetch_claude_docs.py` - Production fetcher (646 lines)
- `scripts/claude-docs-helper.sh.template` - Helper script
- `scripts/requirements.txt` - Dependencies
- `install.sh` - Installation script (538 lines)
- `uninstall.sh` - Uninstallation script
- `LICENSE` - License file
- `UNINSTALL.md` - Uninstall documentation

### Our Additions (Keep & Enhance)
- `specs/` - Complete implementation planning
- `analysis/` - Phase 1 analysis documents
- `scripts/main.py` - Our enhanced fetcher
- `scripts/extract_paths.py` - Path extraction tool
- `CLAUDE.md` - Our project instructions
- `README.md` - Our project documentation
- `REPOSITORY_STRUCTURE.md` - This file

### To Be Created (Future Phases)
- `scripts/lookup_paths.py` - Phase 3
- `scripts/update_sitemap.py` - Phase 3
- `tests/` - Phase 5 (unit, integration, validation)

### Reference/Temporary (Keep but Don't Deploy)
- `upstream/` - Cloned reference repo (excluded from commits)
- `temp.html` - Raw sitemap for development
- `extracted_paths.txt` - Raw path list for reference

---

## Git Strategy

### Branch Structure
```
upstream/main (remote: costiash/claude-code-docs)
├── main (our production branch - matches upstream structure)
└── development (our work branch - adds enhancements)
```

### Development Workflow
1. **Development Branch**: All our work happens here
   - Keep specs/, analysis/, enhanced scripts
   - Test and validate implementations
   - Update documentation

2. **Main Branch**: Clean, deployable version
   - Merge from development when phases complete
   - Maintain compatibility with upstream
   - Production-ready code only

3. **Upstream Tracking**: Stay synchronized
   - Fetch upstream changes: `git fetch upstream`
   - Review upstream updates: `git log upstream/main`
   - Merge upstream improvements when beneficial

---

## Next Steps

### Immediate (Current Task)
1. ✅ Copy workflows to `.github/workflows/` (DONE)
2. ⏳ Copy `docs/` from upstream to root
3. ⏳ Copy `scripts/` from upstream to root
4. ⏳ Move our files to proper locations
5. ⏳ Copy additional files (install.sh, etc.)
6. ⏳ Update .gitignore
7. ⏳ Set up Git branching strategy

### Phase 2 Onward
- Phase 2: Enhance extract_paths.py in scripts/
- Phase 3: Create lookup_paths.py and update_sitemap.py
- Phase 4: Integrate and configure
- Phase 5: Create comprehensive tests/
- Phase 6: Documentation
- Phase 7: Validation

---

## Success Metrics

Final structure provides:
- ✅ Compatibility with upstream update mechanisms
- ✅ Clean separation of concerns (mirror vs enhancements)
- ✅ Easy comparison with upstream reference
- ✅ Comprehensive testing infrastructure (Phase 5)
- ✅ Production-ready installation scripts
- ✅ Clear documentation for users and contributors

---

**Status**: Design Complete ✅
**Next**: Implement restructuring
**Target**: Match upstream structure + our enhancements
