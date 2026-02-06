> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Customize your status line

> Configure a custom status bar to monitor context window usage, costs, and git status in Claude Code

The status line is a customizable bar at the bottom of Claude Code that runs any shell script you configure. It receives JSON session data on stdin and displays whatever your script prints, giving you a persistent, at-a-glance view of context usage, costs, git status, or anything else you want to track.

Status lines are useful when you:

* Want to monitor context window usage as you work
* Need to track session costs
* Work across multiple sessions and need to distinguish them
* Want git branch and status always visible

Here's an example of a [multi-line status line](#display-multiple-lines) that displays git info on the first line and a color-coded context bar on the second.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87" alt="A multi-line status line showing model name, directory, git branch on the first line, and a context usage progress bar with cost and duration on the second line" data-og-width="776" width="776" data-og-height="212" height="212" data-path="images/statusline-multiline.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=2e448b44c332620e6c9c2be4ded992e5 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=f796af2db9c68ab2ddbc5136840b9551 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d29c13d6164773198a0b2c47b31f6c09 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d7720e5f51310185c0c02152f6c10d8b 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=b4e008cde27990a8d5783e41e5b93246 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=40ab24813303dc2e4c09f2675f3faf6e 2500w" />
</Frame>

This page walks through [setting up a basic status line](#set-up-a-status-line), explains [how the data flows](#how-status-lines-work) from Claude Code to your script, lists [all the fields you can display](#available-data), and provides [ready-to-use examples](#examples) for common patterns like git status, cost tracking, and progress bars.

## Set up a status line

Use the [`/statusline` command](#use-the-statusline-command) to have Claude Code generate a script for you, or [manually create a script](#manually-configure-a-status-line) and add it to your settings.

### Use the /statusline command

The `/statusline` command accepts natural language instructions describing what you want displayed. Claude Code generates a script file in `~/.claude/` and updates your settings automatically:

```
/statusline show model name and context percentage with a progress bar
```

### Manually configure a status line

Add a `statusLine` field to your user settings (`~/.claude/settings.json`, where `~` is your home directory) or [project settings](/en/settings#settings-files). Set `type` to `"command"` and point `command` to a script path or an inline shell command. For a full walkthrough of creating a script, see [Build a status line step by step](#build-a-status-line-step-by-step).

```json  theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2
  }
}
```

The `command` field runs in a shell, so you can also use inline commands instead of a script file. This example uses `jq` to parse the JSON input and display the model name and context percentage:

```json  theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'"
  }
}
```

The optional `padding` field adds extra horizontal spacing (in characters) to the status line content. Defaults to `0`. This padding is in addition to the interface's built-in spacing, so it controls relative indentation rather than absolute distance from the terminal edge.

### Disable the status line

Run `/statusline` and ask it to remove or clear your status line (e.g., `/statusline delete`, `/statusline clear`, `/statusline remove it`). You can also manually delete the `statusLine` field from your settings.json.

## Build a status line step by step

This walkthrough shows what's happening under the hood by manually creating a status line that displays the current model, working directory, and context window usage percentage.

<Note>Running [`/statusline`](#use-the-statusline-command) with a description of what you want configures all of this for you automatically.</Note>

These examples use Bash scripts, which work on macOS and Linux. On Windows, you can run Bash scripts through [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) or rewrite them in PowerShell.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=696445e59ca0059213250651ad23db6b" alt="A status line showing model name, directory, and context percentage" data-og-width="726" width="726" data-og-height="164" height="164" data-path="images/statusline-quickstart.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=728c4bd06c8559cb46ddffffad983373 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=f9d28e0f8f48f695167dd1d632a6cf4f 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=57a2803a18cafe8cf1aa05619444f20c 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=52cdd52865842f0cda24489dd5310d3b 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=f8876ea1f72bf40bd0aeec483ee20164 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=6b1524305c7c71122cde65d0c3822374 2500w" />
</Frame>

<Steps>
  <Step title="Create a script that reads JSON and prints output">
    Claude Code sends JSON data to your script via stdin. This script uses [`jq`](https://jqlang.github.io/jq/), a command-line JSON parser you may need to install, to extract the model name, directory, and context percentage, then prints a formatted line.

    Save this to `~/.claude/statusline.sh` (where `~` is your home directory, such as `/Users/username` on macOS or `/home/username` on Linux):

    ```bash  theme={null}
    #!/bin/bash
    # Read JSON data that Claude Code sends to stdin
    input=$(cat)

    # Extract fields using jq
    MODEL=$(echo "$input" | jq -r '.model.display_name')
    DIR=$(echo "$input" | jq -r '.workspace.current_dir')
    # The "// 0" provides a fallback if the field is null
    PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

    # Output the status line - ${DIR##*/} extracts just the folder name
    echo "[$MODEL] 📁 ${DIR##*/} | ${PCT}% context"
    ```
  </Step>

  <Step title="Make it executable">
    Mark the script as executable so your shell can run it:

    ```bash  theme={null}
    chmod +x ~/.claude/statusline.sh
    ```
  </Step>

  <Step title="Add to settings">
    Tell Claude Code to run your script as the status line. Add this configuration to `~/.claude/settings.json`, which sets `type` to `"command"` (meaning "run this shell command") and points `command` to your script:

    ```json  theme={null}
    {
      "statusLine": {
        "type": "command",
        "command": "~/.claude/statusline.sh"
      }
    }
    ```

    Your status line appears at the bottom of the interface. Settings reload automatically, but changes won't appear until your next interaction with Claude Code.
  </Step>
</Steps>

## How status lines work

Claude Code runs your script and pipes [JSON session data](#available-data) to it via stdin. Your script reads the JSON, extracts what it needs, and prints text to stdout. Claude Code displays whatever your script prints.

**When it updates**

Your script runs after each new assistant message, when the permission mode changes, or when vim mode toggles. Updates are debounced at 300ms, meaning rapid changes batch together and your script runs once things settle. If a new update triggers while your script is still running, the in-flight execution is cancelled. If you edit your script, the changes won't appear until your next interaction with Claude Code triggers an update.

**What your script can output**

* **Multiple lines**: each `echo` or `print` statement displays as a separate row. See the [multi-line example](#display-multiple-lines).
* **Colors**: use [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) like `\033[32m` for green (terminal must support them). See the [git status example](#git-status-with-colors).
* **Links**: use [OSC 8 escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#OSC) to make text clickable (Cmd+click on macOS, Ctrl+click on Windows/Linux). Requires a terminal that supports hyperlinks like iTerm2, Kitty, or WezTerm. See the [clickable links example](#clickable-links).

<Note>The status line runs locally and does not consume API tokens. It temporarily hides during certain UI interactions, including autocomplete suggestions, the help menu, and permission prompts.</Note>

## Available data

Claude Code sends the following JSON fields to your script via stdin:

| Field                                                                     | Description                                                                                                                                                                                  |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model.id`, `model.display_name`                                          | Current model identifier and display name                                                                                                                                                    |
| `cwd`, `workspace.current_dir`                                            | Current working directory. Both fields contain the same value; `workspace.current_dir` is preferred for consistency with `workspace.project_dir`.                                            |
| `workspace.project_dir`                                                   | Directory where Claude Code was launched, which may differ from `cwd` if the working directory changes during a session                                                                      |
| `cost.total_cost_usd`                                                     | Total session cost in USD                                                                                                                                                                    |
| `cost.total_duration_ms`                                                  | Total wall-clock time since the session started, in milliseconds                                                                                                                             |
| `cost.total_api_duration_ms`                                              | Total time spent waiting for API responses in milliseconds                                                                                                                                   |
| `cost.total_lines_added`, `cost.total_lines_removed`                      | Lines of code changed                                                                                                                                                                        |
| `context_window.total_input_tokens`, `context_window.total_output_tokens` | Cumulative token counts across the session                                                                                                                                                   |
| `context_window.context_window_size`                                      | Maximum context window size in tokens. 200000 by default, or 1000000 for models with extended context.                                                                                       |
| `context_window.used_percentage`                                          | Pre-calculated percentage of context window used                                                                                                                                             |
| `context_window.remaining_percentage`                                     | Pre-calculated percentage of context window remaining                                                                                                                                        |
| `context_window.current_usage`                                            | Token counts from the last API call, described in [context window fields](#context-window-fields)                                                                                            |
| `exceeds_200k_tokens`                                                     | Whether the total token count (input, cache, and output tokens combined) from the most recent API response exceeds 200k. This is a fixed threshold regardless of actual context window size. |
| `session_id`                                                              | Unique session identifier                                                                                                                                                                    |
| `transcript_path`                                                         | Path to conversation transcript file                                                                                                                                                         |
| `version`                                                                 | Claude Code version                                                                                                                                                                          |
| `output_style.name`                                                       | Name of the current output style                                                                                                                                                             |
| `vim.mode`                                                                | Current vim mode (`NORMAL` or `INSERT`) when [vim mode](/en/interactive-mode#vim-editor-mode) is enabled                                                                                     |
| `agent.name`                                                              | Agent name when running with the `--agent` flag or agent settings configured                                                                                                                 |

<Accordion title="Full JSON schema">
  Your status line command receives this JSON structure via stdin:

  ```json  theme={null}
  {
    "cwd": "/current/working/directory",
    "session_id": "abc123...",
    "transcript_path": "/path/to/transcript.jsonl",
    "model": {
      "id": "claude-opus-4-6",
      "display_name": "Opus"
    },
    "workspace": {
      "current_dir": "/current/working/directory",
      "project_dir": "/original/project/directory"
    },
    "version": "1.0.80",
    "output_style": {
      "name": "default"
    },
    "cost": {
      "total_cost_usd": 0.01234,
      "total_duration_ms": 45000,
      "total_api_duration_ms": 2300,
      "total_lines_added": 156,
      "total_lines_removed": 23
    },
    "context_window": {
      "total_input_tokens": 15234,
      "total_output_tokens": 4521,
      "context_window_size": 200000,
      "used_percentage": 8,
      "remaining_percentage": 92,
      "current_usage": {
        "input_tokens": 8500,
        "output_tokens": 1200,
        "cache_creation_input_tokens": 5000,
        "cache_read_input_tokens": 2000
      }
    },
    "exceeds_200k_tokens": false,
    "vim": {
      "mode": "NORMAL"
    },
    "agent": {
      "name": "security-reviewer"
    }
  }
  ```

  **Fields that may be absent** (not present in JSON):

  * `vim`: appears only when vim mode is enabled
  * `agent`: appears only when running with the `--agent` flag or agent settings configured

  **Fields that may be `null`**:

  * `context_window.current_usage`: `null` before the first API call in a session
  * `context_window.used_percentage`, `context_window.remaining_percentage`: may be `null` early in the session

  Handle missing fields with conditional access and null values with fallback defaults in your scripts.
</Accordion>

### Context window fields

The `context_window` object provides two ways to track context usage:

* **Cumulative totals** (`total_input_tokens`, `total_output_tokens`): sum of all tokens across the entire session, useful for tracking total consumption
* **Current usage** (`current_usage`): token counts from the most recent API call, use this for accurate context percentage since it reflects the actual context state

The `current_usage` object contains:

* `input_tokens`: input tokens in current context
* `output_tokens`: output tokens generated
* `cache_creation_input_tokens`: tokens written to cache
* `cache_read_input_tokens`: tokens read from cache

The `used_percentage` field is calculated from input tokens only: `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. It does not include `output_tokens`.

If you calculate context percentage manually from `current_usage`, use the same input-only formula to match `used_percentage`.

The `current_usage` object is `null` before the first API call in a session.

## Examples

These examples show common status line patterns. To use any example:

1. Save the script to a file like `~/.claude/statusline.sh` (or `.py`/`.js`)
2. Make it executable: `chmod +x ~/.claude/statusline.sh`
3. Add the path to your [settings](#manually-configure-a-status-line)

The Bash examples use [`jq`](https://jqlang.github.io/jq/) to parse JSON. Python and Node.js have built-in JSON parsing.

### Context window usage

Display the current model and context window usage with a visual progress bar. Each script reads JSON from stdin, extracts the `used_percentage` field, and builds a 10-character bar where filled blocks (▓) represent usage:

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=15b58ab3602f036939145dde3165c6f7" alt="A status line showing model name and a progress bar with percentage" data-og-width="448" width="448" data-og-height="152" height="152" data-path="images/statusline-context-window-usage.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=a18fecd31f06b16e984b1ab3310acbc0 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=2f4b3caff156efede2ded995dbaf167f 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=8f6b8c7e7d3a999c570e96ad2ea13d5a 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d9334e6a08e6f11a253733c8592774a9 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e79490da8f62952e4d92837c408e63dc 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=6f7c9ef8e629a794969c54b24163f92d 2500w" />
</Frame>

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  # Read all of stdin into a variable
  input=$(cat)

  # Extract fields with jq, "// 0" provides fallback for null
  MODEL=$(echo "$input" | jq -r '.model.display_name')
  PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

  # Build progress bar: printf creates spaces, tr replaces with blocks
  BAR_WIDTH=10
  FILLED=$((PCT * BAR_WIDTH / 100))
  EMPTY=$((BAR_WIDTH - FILLED))
  BAR=""
  [ "$FILLED" -gt 0 ] && BAR=$(printf "%${FILLED}s" | tr ' ' '▓')
  [ "$EMPTY" -gt 0 ] && BAR="${BAR}$(printf "%${EMPTY}s" | tr ' ' '░')"

  echo "[$MODEL] $BAR $PCT%"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys

  # json.load reads and parses stdin in one step
  data = json.load(sys.stdin)
  model = data['model']['display_name']
  # "or 0" handles null values
  pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)

  # String multiplication builds the bar
  filled = pct * 10 // 100
  bar = '▓' * filled + '░' * (10 - filled)

  print(f"[{model}] {bar} {pct}%")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  // Node.js reads stdin asynchronously with events
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      // Optional chaining (?.) safely handles null fields
      const pct = Math.floor(data.context_window?.used_percentage || 0);

      // String.repeat() builds the bar
      const filled = Math.floor(pct * 10 / 100);
      const bar = '▓'.repeat(filled) + '░'.repeat(10 - filled);

      console.log(`[${model}] ${bar} ${pct}%`);
  });
  ```
</CodeGroup>

### Git status with colors

Show git branch with color-coded indicators for staged and modified files. This script uses [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) for terminal colors: `\033[32m` is green, `\033[33m` is yellow, and `\033[0m` resets to default.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e656f34f90d1d9a1d0e220988914345f" alt="A status line showing model, directory, git branch, and colored indicators for staged and modified files" data-og-width="742" width="742" data-og-height="178" height="178" data-path="images/statusline-git-context.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=c1bced5f46afdc9aae549702591f8457 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=debe46a7a888234ec692751243bba492 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=3a069d5c8b0395908e42f0e295fd4854 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=26aff0978865756d5ea299a22e5e9afd 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d5ac1d59881e6f2032af053557dc4590 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=46febbf34b0ee646502d095433132709 2500w" />
</Frame>

Each script checks if the current directory is a git repository, counts staged and modified files, and displays color-coded indicators:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')

  GREEN='\033[32m'
  YELLOW='\033[33m'
  RESET='\033[0m'

  if git rev-parse --git-dir > /dev/null 2>&1; then
      BRANCH=$(git branch --show-current 2>/dev/null)
      STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
      MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

      GIT_STATUS=""
      [ "$STAGED" -gt 0 ] && GIT_STATUS="${GREEN}+${STAGED}${RESET}"
      [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${YELLOW}~${MODIFIED}${RESET}"

      echo -e "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH $GIT_STATUS"
  else
      echo "[$MODEL] 📁 ${DIR##*/}"
  fi
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])

  GREEN, YELLOW, RESET = '\033[32m', '\033[33m', '\033[0m'

  try:
      subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
      branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
      staged_output = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
      modified_output = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
      staged = len(staged_output.split('\n')) if staged_output else 0
      modified = len(modified_output.split('\n')) if modified_output else 0

      git_status = f"{GREEN}+{staged}{RESET}" if staged else ""
      git_status += f"{YELLOW}~{modified}{RESET}" if modified else ""

      print(f"[{model}] 📁 {directory} | 🌿 {branch} {git_status}")
  except:
      print(f"[{model}] 📁 {directory}")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);

      const GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RESET = '\x1b[0m';

      try {
          execSync('git rev-parse --git-dir', { stdio: 'ignore' });
          const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
          const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
          const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;

          let gitStatus = staged ? `${GREEN}+${staged}${RESET}` : '';
          gitStatus += modified ? `${YELLOW}~${modified}${RESET}` : '';

          console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} ${gitStatus}`);
      } catch {
          console.log(`[${model}] 📁 ${dir}`);
      }
  });
  ```
</CodeGroup>

### Cost and duration tracking

Track your session's API costs and elapsed time. The `cost.total_cost_usd` field accumulates the cost of all API calls in the current session. The `cost.total_duration_ms` field measures total elapsed time since the session started, while `cost.total_api_duration_ms` tracks only the time spent waiting for API responses.

Each script formats cost as currency and converts milliseconds to minutes and seconds:

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e3444a51fe6f3440c134bd5f1f08ad29" alt="A status line showing model name, session cost, and duration" data-og-width="588" width="588" data-og-height="180" height="180" data-path="images/statusline-cost-tracking.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=b1d35fa8acd792f559b6b1662ed10204 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=a3ed4330c3645fc28b87a6cab55be0b7 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=386ee2ed68a7d520eba20eac54f7fe52 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=479c2515e53f46d5d1da3b87a6dd993a 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=1340c7589a4cb89ec071234aba3571d1 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=69056cf4fe3271770cac4dc1704bcd0a 2500w" />
</Frame>

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

  COST_FMT=$(printf '$%.2f' "$COST")
  DURATION_SEC=$((DURATION_MS / 1000))
  MINS=$((DURATION_SEC / 60))
  SECS=$((DURATION_SEC % 60))

  echo "[$MODEL] 💰 $COST_FMT | ⏱️ ${MINS}m ${SECS}s"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
  duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

  duration_sec = duration_ms // 1000
  mins, secs = duration_sec // 60, duration_sec % 60

  print(f"[{model}] 💰 ${cost:.2f} | ⏱️ {mins}m {secs}s")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const cost = data.cost?.total_cost_usd || 0;
      const durationMs = data.cost?.total_duration_ms || 0;

      const durationSec = Math.floor(durationMs / 1000);
      const mins = Math.floor(durationSec / 60);
      const secs = durationSec % 60;

      console.log(`[${model}] 💰 $${cost.toFixed(2)} | ⏱️ ${mins}m ${secs}s`);
  });
  ```
</CodeGroup>

### Display multiple lines

Your script can output multiple lines to create a richer display. Each `echo` statement produces a separate row in the status area.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87" alt="A multi-line status line showing model name, directory, git branch on the first line, and a context usage progress bar with cost and duration on the second line" data-og-width="776" width="776" data-og-height="212" height="212" data-path="images/statusline-multiline.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=2e448b44c332620e6c9c2be4ded992e5 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=f796af2db9c68ab2ddbc5136840b9551 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d29c13d6164773198a0b2c47b31f6c09 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d7720e5f51310185c0c02152f6c10d8b 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=b4e008cde27990a8d5783e41e5b93246 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=40ab24813303dc2e4c09f2675f3faf6e 2500w" />
</Frame>

This example combines several techniques: threshold-based colors (green under 70%, yellow 70-89%, red 90%+), a progress bar, and git branch info. Each `print` or `echo` statement creates a separate row:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')
  COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
  DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

  CYAN='\033[36m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; RESET='\033[0m'

  # Pick bar color based on context usage
  if [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"
  elif [ "$PCT" -ge 70 ]; then BAR_COLOR="$YELLOW"
  else BAR_COLOR="$GREEN"; fi

  FILLED=$((PCT / 10)); EMPTY=$((10 - FILLED))
  BAR=$(printf "%${FILLED}s" | tr ' ' '█')$(printf "%${EMPTY}s" | tr ' ' '░')

  MINS=$((DURATION_MS / 60000)); SECS=$(((DURATION_MS % 60000) / 1000))

  BRANCH=""
  git rev-parse --git-dir > /dev/null 2>&1 && BRANCH=" | 🌿 $(git branch --show-current 2>/dev/null)"

  echo -e "${CYAN}[$MODEL]${RESET} 📁 ${DIR##*/}$BRANCH"
  COST_FMT=$(printf '$%.2f' "$COST")
  echo -e "${BAR_COLOR}${BAR}${RESET} ${PCT}% | ${YELLOW}${COST_FMT}${RESET} | ⏱️ ${MINS}m ${SECS}s"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])
  cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
  pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
  duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

  CYAN, GREEN, YELLOW, RED, RESET = '\033[36m', '\033[32m', '\033[33m', '\033[31m', '\033[0m'

  bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
  filled = pct // 10
  bar = '█' * filled + '░' * (10 - filled)

  mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

  try:
      branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True, stderr=subprocess.DEVNULL).strip()
      branch = f" | 🌿 {branch}" if branch else ""
  except:
      branch = ""

  print(f"{CYAN}[{model}]{RESET} 📁 {directory}{branch}")
  print(f"{bar_color}{bar}{RESET} {pct}% | {YELLOW}${cost:.2f}{RESET} | ⏱️ {mins}m {secs}s")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);
      const cost = data.cost?.total_cost_usd || 0;
      const pct = Math.floor(data.context_window?.used_percentage || 0);
      const durationMs = data.cost?.total_duration_ms || 0;

      const CYAN = '\x1b[36m', GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RED = '\x1b[31m', RESET = '\x1b[0m';

      const barColor = pct >= 90 ? RED : pct >= 70 ? YELLOW : GREEN;
      const filled = Math.floor(pct / 10);
      const bar = '█'.repeat(filled) + '░'.repeat(10 - filled);

      const mins = Math.floor(durationMs / 60000);
      const secs = Math.floor((durationMs % 60000) / 1000);

      let branch = '';
      try {
          branch = execSync('git branch --show-current', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
          branch = branch ? ` | 🌿 ${branch}` : '';
      } catch {}

      console.log(`${CYAN}[${model}]${RESET} 📁 ${dir}${branch}`);
      console.log(`${barColor}${bar}${RESET} ${pct}% | ${YELLOW}$${cost.toFixed(2)}${RESET} | ⏱️ ${mins}m ${secs}s`);
  });
  ```
</CodeGroup>

### Clickable links

This example creates a clickable link to your GitHub repository. It reads the git remote URL, converts SSH format to HTTPS with `sed`, and wraps the repo name in OSC 8 escape codes. Hold Cmd (macOS) or Ctrl (Windows/Linux) and click to open the link in your browser.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=4bcc6e7deb7cf52f41ab85a219b52661" alt="A status line showing a clickable link to a GitHub repository" data-og-width="726" width="726" data-og-height="198" height="198" data-path="images/statusline-links.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?w=280&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=9386f78056f7be99599bcefe9e838180 280w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?w=560&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=d748012a0866c37dddc6babd4b7a88c4 560w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?w=840&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=bade8fbfcde957c1033c376c58b89131 840w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?w=1100&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=9f7e0c729ea093c3b39682619fd3f201 1100w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?w=1650&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=ccec17e90a89d82381888a4a9a8fa40e 1650w, https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?w=2500&fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=4d2e34a4d2f24e174cae1256c84f9a52 2500w" />
</Frame>

Each script gets the git remote URL, converts SSH format to HTTPS, and wraps the repo name in OSC 8 escape codes. The Bash version uses `printf '%b'` which interprets backslash escapes more reliably than `echo -e` across different shells:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')

  # Convert git SSH URL to HTTPS
  REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

  if [ -n "$REMOTE" ]; then
      REPO_NAME=$(basename "$REMOTE")
      # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
      # printf %b interprets escape sequences reliably across shells
      printf '%b' "[$MODEL] 🔗 \e]8;;${REMOTE}\a${REPO_NAME}\e]8;;\a\n"
  else
      echo "[$MODEL]"
  fi
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, re, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']

  # Get git remote URL
  try:
      remote = subprocess.check_output(
          ['git', 'remote', 'get-url', 'origin'],
          stderr=subprocess.DEVNULL, text=True
      ).strip()
      # Convert SSH to HTTPS format
      remote = re.sub(r'^git@github\.com:', 'https://github.com/', remote)
      remote = re.sub(r'\.git$', '', remote)
      repo_name = os.path.basename(remote)
      # OSC 8 escape sequences
      link = f"\033]8;;{remote}\a{repo_name}\033]8;;\a"
      print(f"[{model}] 🔗 {link}")
  except:
      print(f"[{model}]")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;

      try {
          let remote = execSync('git remote get-url origin', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
          // Convert SSH to HTTPS format
          remote = remote.replace(/^git@github\.com:/, 'https://github.com/').replace(/\.git$/, '');
          const repoName = path.basename(remote);
          // OSC 8 escape sequences
          const link = `\x1b]8;;${remote}\x07${repoName}\x1b]8;;\x07`;
          console.log(`[${model}] 🔗 ${link}`);
      } catch {
          console.log(`[${model}]`);
      }
  });
  ```
</CodeGroup>

### Cache expensive operations

Your status line script runs frequently during active sessions. Commands like `git status` or `git diff` can be slow, especially in large repositories. This example caches git information to a temp file and only refreshes it every 5 seconds.

Use a stable, fixed filename for the cache file like `/tmp/statusline-git-cache`. Each status line invocation runs as a new process, so process-based identifiers like `$$`, `os.getpid()`, or `process.pid` produce a different value every time and the cache is never reused.

Each script checks if the cache file is missing or older than 5 seconds before running git commands:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')

  CACHE_FILE="/tmp/statusline-git-cache"
  CACHE_MAX_AGE=5  # seconds

  cache_is_stale() {
      [ ! -f "$CACHE_FILE" ] || \
      # stat -f %m is macOS, stat -c %Y is Linux
      [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
  }

  if cache_is_stale; then
      if git rev-parse --git-dir > /dev/null 2>&1; then
          BRANCH=$(git branch --show-current 2>/dev/null)
          STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
          MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
          echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
      else
          echo "||" > "$CACHE_FILE"
      fi
  fi

  IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

  if [ -n "$BRANCH" ]; then
      echo "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH +$STAGED ~$MODIFIED"
  else
      echo "[$MODEL] 📁 ${DIR##*/}"
  fi
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, os, time

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])

  CACHE_FILE = "/tmp/statusline-git-cache"
  CACHE_MAX_AGE = 5  # seconds

  def cache_is_stale():
      if not os.path.exists(CACHE_FILE):
          return True
      return time.time() - os.path.getmtime(CACHE_FILE) > CACHE_MAX_AGE

  if cache_is_stale():
      try:
          subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
          branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
          staged = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
          modified = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
          staged_count = len(staged.split('\n')) if staged else 0
          modified_count = len(modified.split('\n')) if modified else 0
          with open(CACHE_FILE, 'w') as f:
              f.write(f"{branch}|{staged_count}|{modified_count}")
      except:
          with open(CACHE_FILE, 'w') as f:
              f.write("||")

  with open(CACHE_FILE) as f:
      branch, staged, modified = f.read().strip().split('|')

  if branch:
      print(f"[{model}] 📁 {directory} | 🌿 {branch} +{staged} ~{modified}")
  else:
      print(f"[{model}] 📁 {directory}")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const fs = require('fs');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);

      const CACHE_FILE = '/tmp/statusline-git-cache';
      const CACHE_MAX_AGE = 5; // seconds

      const cacheIsStale = () => {
          if (!fs.existsSync(CACHE_FILE)) return true;
          return (Date.now() / 1000) - fs.statSync(CACHE_FILE).mtimeMs / 1000 > CACHE_MAX_AGE;
      };

      if (cacheIsStale()) {
          try {
              execSync('git rev-parse --git-dir', { stdio: 'ignore' });
              const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
              const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
              const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
              fs.writeFileSync(CACHE_FILE, `${branch}|${staged}|${modified}`);
          } catch {
              fs.writeFileSync(CACHE_FILE, '||');
          }
      }

      const [branch, staged, modified] = fs.readFileSync(CACHE_FILE, 'utf8').trim().split('|');

      if (branch) {
          console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} +${staged} ~${modified}`);
      } else {
          console.log(`[${model}] 📁 ${dir}`);
      }
  });
  ```
</CodeGroup>

## Tips

* **Test with mock input**: `echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":25}}' | ./statusline.sh`
* **Keep output short**: the status bar has limited width, so long output may get truncated or wrap awkwardly
* **Cache slow operations**: your script runs frequently during active sessions, so commands like `git status` can cause lag. See the [caching example](#cache-expensive-operations) for how to handle this.

Community projects like [ccstatusline](https://github.com/sirmalloc/ccstatusline) and [starship-claude](https://github.com/martinemde/starship-claude) provide pre-built configurations with themes and additional features.

## Troubleshooting

**Status line not appearing**

* Verify your script is executable: `chmod +x ~/.claude/statusline.sh`
* Check that your script outputs to stdout, not stderr
* Run your script manually to verify it produces output
* If `disableAllHooks` is set to `true` in your settings, the status line is also disabled. Remove this setting or set it to `false` to re-enable.

**Status line shows `--` or empty values**

* Fields may be `null` before the first API response completes
* Handle null values in your script with fallbacks such as `// 0` in jq
* Restart Claude Code if values remain empty after multiple messages

**Context percentage shows unexpected values**

* Use `used_percentage` for accurate context state rather than cumulative totals
* The `total_input_tokens` and `total_output_tokens` are cumulative across the session and may exceed the context window size
* Context percentage may differ from `/context` output due to when each is calculated

**OSC 8 links not clickable**

* Verify your terminal supports OSC 8 hyperlinks (iTerm2, Kitty, WezTerm)
* Terminal.app does not support clickable links
* SSH and tmux sessions may strip OSC sequences depending on configuration
* If escape sequences appear as literal text like `\e]8;;`, use `printf '%b'` instead of `echo -e` for more reliable escape handling

**Display glitches with escape sequences**

* Complex escape sequences (ANSI colors, OSC 8 links) can occasionally cause garbled output if they overlap with other UI updates
* If you see corrupted text, try simplifying your script to plain text output
* Multi-line status lines with escape codes are more prone to rendering issues than single-line plain text

**Script errors or hangs**

* Scripts that exit with non-zero codes or produce no output cause the status line to go blank
* Slow scripts block the status line from updating until they complete. Keep scripts fast to avoid stale output.
* If a new update triggers while a slow script is running, the in-flight script is cancelled
* Test your script independently with mock input before configuring it

**Notifications share the status line row**

* System notifications like MCP server errors, auto-updates, and token warnings display on the right side of the same row as your status line
* Enabling verbose mode adds a token counter to this area
* On narrow terminals, these notifications may truncate your status line output
