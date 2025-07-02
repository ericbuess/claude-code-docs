# Auto-Sync for Claude Code Documentation

This directory contains scripts to automatically sync Claude Code documentation updates to your local repository.

## 🚀 Quick Start

### 1. Test the sync manually
```bash
cd /path/to/claude-code-docs
./auto-sync/auto-sync.sh
```

### 2. Set up automatic syncing
```bash
# Open your crontab
crontab -e

# Add this line (replace path with your actual repository path)
30 */6 * * * cd /path/to/claude-code-docs && ./auto-sync/auto-sync.sh --quiet
```

That's it! Your documentation will automatically update 30 minutes after each GitHub Action run.

## 📋 What's Included

### Scripts

1. **`auto-sync.sh`** - Main sync script
   - Safely pulls latest documentation updates
   - Checks for conflicts before pulling
   - Logs all operations to `sync.log`
   - Usage: `./auto-sync.sh [--quiet]`

2. **`check-updates.sh`** - Check for available updates
   - Returns exit code 0 if updates available
   - Returns exit code 1 if already up to date
   - Usage: `./check-updates.sh [--verbose]`

### Installation Examples

- **`install/cron-example`** - Example crontab configurations

## 🔧 Setup Instructions

### Prerequisites

- Git must be installed
- Repository must be cloned locally
- Git credentials configured (if using HTTPS)

### macOS Specific Notes

1. **Cron Permission**: On macOS, you may need to grant cron "Full Disk Access":
   - System Settings → Privacy & Security → Full Disk Access
   - Add `/usr/sbin/cron`

2. **Alternative for macOS**: Consider using `launchd` instead of cron for better integration

### Basic Setup

1. Clone the repository if you haven't already:
   ```bash
   git clone https://github.com/ericbuess/claude-code-docs.git
   cd claude-code-docs
   ```

2. Test the sync script:
   ```bash
   ./auto-sync/auto-sync.sh
   ```

3. Add to crontab to sync automatically:
   ```bash
   crontab -e
   ```
   
   Add this line:
   ```bash
   # Sync 30 minutes after each GitHub Action run
   30 */6 * * * cd /full/path/to/claude-code-docs && ./auto-sync/auto-sync.sh --quiet
   ```
   
   This runs at 00:30, 06:30, 12:30, and 18:30 UTC - giving the GitHub Action time to complete.

## 📊 Monitoring

### View Logs
```bash
# Watch live updates
tail -f auto-sync/sync.log

# View recent syncs
tail -20 auto-sync/sync.log

# Check for errors
grep ERROR auto-sync/sync.log
```

### Check Sync Status
```bash
# Check if updates are available
./auto-sync/check-updates.sh --verbose

# View last sync time
grep "completed successfully" auto-sync/sync.log | tail -1
```

## 🛡️ Safety Features

The auto-sync script includes several safety measures:

1. **Conflict Detection**: Won't pull if you have local changes
2. **Error Handling**: Logs errors and exits safely
3. **Atomic Updates**: Uses git's built-in safety features
4. **Detailed Logging**: Everything is logged to `sync.log`

## ⚠️ Important Notes

1. **No Local Changes**: The auto-sync will fail if you have uncommitted local changes
2. **Network Required**: Needs internet connection to check/pull updates
3. **Git Credentials**: Make sure git can access the repository without prompting
4. **Path Requirements**: Use absolute paths in crontab

## 🔍 Troubleshooting

### Cron not working?
```bash
# Check if cron is running
pgrep cron

# Check cron logs (macOS)
log show --predicate 'process == "cron"' --last 1h

# Test with a simple cron job first
* * * * * echo "test" >> /tmp/crontest.log
```

### Permission Issues?
```bash
# Make sure scripts are executable
chmod +x auto-sync/*.sh

# Check repository permissions
ls -la .git/
```

### Git Authentication?
```bash
# Test git access
git fetch origin

# For HTTPS, cache credentials
git config credential.helper cache
```

## 📝 Advanced Usage

### Only Sync When Updates Available

If you want to check more frequently but only pull when needed:
```bash
# Check every hour, only sync if updates exist
0 * * * * cd /path/to/claude-code-docs && ./auto-sync/check-updates.sh && ./auto-sync/auto-sync.sh --quiet
```

### Log Rotation

Add to your crontab to prevent logs from growing too large:
```bash
# Weekly log rotation
0 0 * * 0 cd /path/to/claude-code-docs && mv auto-sync/sync.log auto-sync/sync.log.old && touch auto-sync/sync.log
```

## 🤝 Contributing

If you have improvements for the auto-sync functionality, please submit a pull request!

## 📄 License

Same as the parent repository.