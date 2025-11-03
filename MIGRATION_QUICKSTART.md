# Migration Quick Start Guide

**This is your step-by-step execution guide. Follow in order.**

---

## Pre-Flight Check (5 minutes)

```bash
# 1. You're in the right directory
pwd
# Should show: /home/rudycosta3/claude-code-docs

# 2. Review what you're about to do
cat MIGRATION_SUMMARY.md  # 2-minute read

# 3. Create safety backup
git branch pre-migration-backup
git push origin pre-migration-backup

# 4. Clean working directory
git status
# If dirty, commit or stash changes

# 5. Note current state
git log -1 --oneline > pre-migration-state.txt
pytest --co -q | wc -l >> pre-migration-state.txt  # Test count
```

---

## Phase 1: Installation System (2 hours)

### Step 1.1: Enhance install.sh

**Location**: Lines 497-540 of `install.sh`

**Add after success message:**

```bash
# Open install.sh
nano install.sh  # or vim, code, etc.

# Go to line 497 (after echo "⚠️  Note: Restart Claude Code...")
# Add the enhanced installation code from MIGRATION_PLAN.md Phase 1.1
```

**Quick copy-paste** (from MIGRATION_PLAN.md):
```bash
# Extract the code block from MIGRATION_PLAN.md
sed -n '/# ========================================/,/^echo ""$/p' MIGRATION_PLAN.md > /tmp/enhanced_install.sh

# Review it
cat /tmp/enhanced_install.sh

# Append to install.sh
cat /tmp/enhanced_install.sh >> install.sh
```

**Validate**:
```bash
# Check syntax
bash -n install.sh

# Should show no errors
```

### Step 1.2: Create Enhanced Helper

```bash
# Copy template
cp scripts/claude-docs-helper.sh.template scripts/claude-docs-helper.sh

# Make executable
chmod +x scripts/claude-docs-helper.sh

# Edit to add enhanced features
# (See MIGRATION_PLAN.md Phase 1, Step 2 for full code)
nano scripts/claude-docs-helper.sh
```

**Or create from scratch:**
```bash
# Full script in MIGRATION_PLAN.md Phase 1.2
# Copy the entire enhanced helper script
```

### Step 1.3: Test Installation

**Test Standard Mode:**
```bash
# Run installer (answer N)
./install.sh <<< "N"

# Verify
~/.claude-code-docs/claude-docs-helper.sh -t
~/.claude-code-docs/claude-docs-helper.sh hooks

# Should work without Python
```

**Test Enhanced Mode:**
```bash
# Remove previous install
rm -rf ~/.claude-code-docs
rm ~/.claude/commands/docs.md

# Run installer (answer Y)
./install.sh <<< "Y"

# Verify enhanced features
~/.claude-code-docs/claude-docs-helper.sh --search "test"
~/.claude-code-docs/claude-docs-helper.sh --help

# Should show enhanced commands
```

### Step 1.4: Commit Phase 1

```bash
git add install.sh scripts/claude-docs-helper.sh
git commit -m "Phase 1: Enhanced installation system

- Add optional enhanced mode to install.sh
- Create enhanced helper script with Python features
- Maintain backward compatibility with standard mode
- Tested on macOS and Linux"

git push origin development
```

**Time Check**: Should take ~2 hours
**Validate**: Both modes work, tests pass

---

## Phase 2: Directory Restructuring (1 hour)

### Step 2.1: Create New Structure

```bash
# Create docs-dev directory
mkdir -p docs-dev/analysis

# Move files
mv DEVELOPMENT.md docs-dev/
mv docs/CAPABILITIES.md docs-dev/ 2>/dev/null || true
mv docs/EXAMPLES.md docs-dev/ 2>/dev/null || true
mv analysis/* docs-dev/analysis/
rmdir analysis
mv specs docs-dev/specs

# Verify
tree -L 2 -I '.git|.venv|__pycache__'
```

### Step 2.2: Create ENHANCEMENTS.md

```bash
# Full content in MIGRATION_PLAN.md Phase 2, Step 4
# Or use this shortcut:
cat > ENHANCEMENTS.md << 'EOF'
# Enhanced Features

[Copy from MIGRATION_PLAN.md]
EOF
```

### Step 2.3: Update .gitignore

```bash
# Ensure these are ignored
cat >> .gitignore << 'EOF'
# Reports and temporary files
reports/
temp/
*.tmp
*.log

# Keep docs-dev
!docs-dev/
EOF
```

### Step 2.4: Commit Phase 2

```bash
git add -A
git commit -m "Phase 2: Clean directory structure

- Move developer docs to docs-dev/
- Move analysis to docs-dev/analysis/
- Create ENHANCEMENTS.md documenting additions
- Update .gitignore for cleaner structure
- Align with upstream conventions"

git push origin development
```

**Time Check**: Should take ~1 hour
**Validate**: `tree` output looks clean, no broken imports

---

## Phase 3: Command Integration (15 minutes)

### Step 3.1: Remove Old Commands

```bash
# Delete old commands
rm .claude/commands/search-docs.md
rm .claude/commands/update-docs.md
rm .claude/commands/validate-docs.md

# Keep only:
ls .claude/commands/
# Should show: docs.md, prime.md
```

### Step 3.2: Update Documentation

```bash
# Update references in docs-dev/
grep -r "search-docs\|update-docs\|validate-docs" docs-dev/
# Replace with /docs --search, /docs --update-all, etc.

# Example:
sed -i 's/\/search-docs/\/docs --search/g' docs-dev/*.md
sed -i 's/\/update-docs/\/docs --update-all/g' docs-dev/*.md
sed -i 's/\/validate-docs/\/docs --validate/g' docs-dev/*.md
```

### Step 3.3: Commit Phase 3

```bash
git add .claude/commands/ docs-dev/
git commit -m "Phase 3: Unified /docs command

- Remove separate search-docs, update-docs, validate-docs
- Consolidate into single /docs command with flags
- Update documentation references
- Align with upstream command pattern"

git push origin development
```

**Time Check**: ~15 minutes
**Validate**: `/docs` command works for all modes

---

## Phase 4: Hook System (30 minutes)

### Step 4.1: Verify Hook Configuration

```bash
# Check if installer set up hook
cat ~/.claude/settings.json | jq '.hooks.PreToolUse'

# Should show hook command
```

### Step 4.2: Test Hook

```bash
# Trigger hook by reading a doc
cat ~/.claude-code-docs/docs/hooks.md

# Should auto-update if behind
```

### Step 4.3: Commit Phase 4

```bash
git add .
git commit -m "Phase 4: Hook system active

- Verify PreToolUse hook configured by installer
- Test auto-update on doc read
- Document hook behavior"

git push origin development
```

**Time Check**: ~30 minutes
**Validate**: Hook triggers, auto-updates work

---

## Phase 5: Documentation (1 hour)

### Step 5.1: Update README.md

```bash
# Backup current
cp README.md README.md.backup

# Edit with new structure (from MIGRATION_PLAN.md Phase 5.1)
nano README.md

# Key sections:
# - Installation (standard and enhanced)
# - Usage (both modes)
# - Features (comparison table)
```

### Step 5.2: Update CLAUDE.md

```bash
# Use content from MIGRATION_PLAN.md Phase 5.2
nano CLAUDE.md
```

### Step 5.3: Create CONTRIBUTING.md

```bash
# Full content in MIGRATION_PLAN.md Phase 5.3
nano CONTRIBUTING.md
```

### Step 5.4: Commit Phase 5

```bash
git add README.md CLAUDE.md CONTRIBUTING.md
git commit -m "Phase 5: Documentation alignment

- Update README for dual-mode installation
- Enhance CLAUDE.md for project guidance
- Create CONTRIBUTING.md for contributors
- Document all features clearly"

git push origin development
```

**Time Check**: ~1 hour
**Validate**: All docs accurate, links work

---

## Phase 6: Testing (1.5 hours)

### Step 6.1: Fix Failing Tests

```bash
# Run tests to see failures
pytest tests/ -v | tee test-results.txt

# Fix function signature mismatches
# (See MIGRATION_PLAN.md Phase 6.1 for details)

# Common fixes:
# - fetch_page(url, session) not fetch_page(url)
# - content_has_changed(path, content) signature
```

### Step 6.2: Add Installation Tests

```bash
# Create tests/integration/test_installation.py
nano tests/integration/test_installation.py
# (Content from MIGRATION_PLAN.md Phase 6.2)
```

### Step 6.3: Update CI/CD

```bash
# Edit .github/workflows/test.yml
nano .github/workflows/test.yml
# Add installation testing jobs
```

### Step 6.4: Commit Phase 6

```bash
git add tests/ .github/workflows/
git commit -m "Phase 6: All tests passing

- Fix function signature mismatches (24 → 0 failures)
- Add installation tests for both modes
- Update CI/CD to test standard and enhanced
- 174 tests, 100% passing"

git push origin development
```

**Time Check**: ~1.5 hours
**Validate**: `pytest` shows all green

---

## Phase 7: PR Preparation (1 hour)

### Step 7.1: Create Feature Branches

```bash
# For each proposed PR
git checkout -b feature/enhanced-installation
git checkout development

git checkout -b feature/extended-paths
git checkout development

git checkout -b feature/full-text-search
git checkout development

# etc. for all 6 PRs
```

### Step 7.2: Write PR Descriptions

```bash
# Use templates from MIGRATION_PLAN.md Phase 7.3
# Create PR-descriptions/ directory
mkdir PR-descriptions

# One file per PR
nano PR-descriptions/01-enhanced-installation.md
nano PR-descriptions/02-extended-paths.md
# etc.
```

### Step 7.3: Create GitHub Issues

```bash
# If planning to contribute upstream
# Create issues on GitHub for tracking
```

### Step 7.4: Commit Phase 7

```bash
git add PR-descriptions/
git commit -m "Phase 7: PR preparation complete

- Create feature branches for 6 PRs
- Write PR descriptions and justifications
- Prepare for upstream contribution
- Document enhancement strategy"

git push origin development
```

**Time Check**: ~1 hour
**Validate**: All branches created, PRs documented

---

## Post-Migration Validation (30 minutes)

### Final Checklist

```bash
# 1. All tests pass
pytest
# ✅ 174/174 passing

# 2. Standard install works
rm -rf ~/.claude-code-docs
./install.sh <<< "N"
~/.claude-code-docs/claude-docs-helper.sh hooks
# ✅ Works without Python

# 3. Enhanced install works
rm -rf ~/.claude-code-docs
./install.sh <<< "Y"
~/.claude-code-docs/claude-docs-helper.sh --search "test"
# ✅ Works with Python

# 4. /docs command functional
/docs hooks
/docs --search "mcp"
/docs --validate
# ✅ All modes work

# 5. CI/CD passing
git push origin development
# Check GitHub Actions
# ✅ All workflows green

# 6. Documentation accurate
cat README.md
cat ENHANCEMENTS.md
# ✅ All info correct

# 7. Can sync with upstream
git remote -v
git fetch upstream
git merge upstream/main --no-commit --no-ff
# ✅ No major conflicts
git merge --abort  # Don't actually merge yet
```

### Create Release Tag

```bash
# Tag the migration completion
git tag -a v1.0.0-enhanced -m "Migration complete: Upstream-compatible enhanced edition"
git push origin v1.0.0-enhanced
```

---

## Success!

You've successfully migrated to an upstream-compatible structure while preserving all enhancements!

### What You've Achieved

✅ **Upstream Compatible**
- Single-command installation
- Standard `/docs` command
- PreToolUse hook system
- Clean directory structure

✅ **All Enhancements Preserved**
- 459 documentation paths
- Full-text search capability
- Path validation tools
- 174 comprehensive tests

✅ **Dual Mode Support**
- Standard mode (47 docs, no Python)
- Enhanced mode (459 paths, all features)
- Graceful degradation

✅ **PR Ready**
- 6 feature branches prepared
- PR descriptions written
- Can contribute back to upstream

### Next Steps

1. **Choose Your Path**:
   - **Option A**: Submit PRs to upstream (see PR-descriptions/)
   - **Option B**: Maintain as "Enhanced Edition" fork

2. **Regular Maintenance**:
   ```bash
   # Monthly sync with upstream
   git fetch upstream
   git merge upstream/main
   ```

3. **Keep Tests Passing**:
   ```bash
   # Before each push
   pytest
   ```

4. **Document Changes**:
   ```bash
   # Update CHANGELOG.md
   nano CHANGELOG.md
   ```

---

## Troubleshooting

### Installation Fails

```bash
# Check dependencies
which git jq curl python3

# Check Python version
python3 --version  # Should be 3.12+

# Run with debug
bash -x install.sh
```

### Tests Failing

```bash
# Show failing tests
pytest -v --tb=short

# Run specific test
pytest tests/unit/test_specific.py -v

# Check coverage
pytest --cov=scripts
```

### /docs Command Not Working

```bash
# Verify installation
ls -la ~/.claude-code-docs/claude-docs-helper.sh

# Check permissions
chmod +x ~/.claude-code-docs/claude-docs-helper.sh

# Test directly
~/.claude-code-docs/claude-docs-helper.sh hooks
```

### Sync Issues with Upstream

```bash
# Check remote
git remote -v

# Fetch latest
git fetch upstream

# Show what changed
git log HEAD..upstream/main --oneline

# Merge carefully
git merge upstream/main
```

---

## Questions?

- **Full Details**: See MIGRATION_PLAN.md
- **Summary**: See MIGRATION_SUMMARY.md
- **Visual Guide**: See MIGRATION_ROADMAP.md
- **This Guide**: MIGRATION_QUICKSTART.md (you are here)

---

**Total Time**: 6-8 hours
**Complexity**: Medium
**Risk**: Low (can rollback)
**Value**: High (upstream compatible + all enhancements)

**Ready? Let's go! Start with Phase 1.**
