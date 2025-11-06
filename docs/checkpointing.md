# Checkpointing

> Automatically track and rewind Claude's edits to quickly recover from unwanted changes.

Claude Code automatically tracks Claude's file edits as you work, allowing you to quickly undo changes and rewind to previous states if anything gets off track.

## How checkpoints work

As you work with Claude, checkpointing automatically captures the state of your code before each edit. This safety net lets you pursue ambitious, wide-scale tasks knowing you can always return to a prior code state.

### Automatic tracking

Claude Code tracks all changes made by its file editing tools:

* Every user prompt creates a new checkpoint
* Checkpoints persist across sessions, so you can access them in resumed conversations
* Automatically cleaned up along with sessions after 30 days (configurable)

### Rewinding changes

Press `Esc` twice (`Esc` + `Esc`) or use the `/rewind` command to open up the rewind menu. You can choose to restore:

* **Conversation only**: Rewind to a user message while keeping code changes
* **Code only**: Revert file changes while keeping the conversation
* **Both code and conversation**: Restore both to a prior point in the session

## Common use cases

Checkpoints are particularly useful when:

* **Exploring alternatives**: Try different implementation approaches without losing your starting point
* **Recovering from mistakes**: Quickly undo changes that introduced bugs or broke functionality
* **Iterating on features**: Experiment with variations knowing you can revert to working states

## Limitations

### Bash command changes not tracked

Checkpointing does not track files modified by bash commands. For example, if Claude Code runs:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

These file modifications cannot be undone through rewind. Only direct file edits made through Claude's file editing tools are tracked.

### External changes not tracked

Checkpointing only tracks files that have been edited within the current session. Manual changes you make to files outside of Claude Code and edits from other concurrent sessions are normally not captured, unless they happen to modify the same files as the current session.

### Not a replacement for version control

Checkpoints are designed for quick, session-level recovery. For permanent version history and collaboration:

* Continue using version control (ex. Git) for commits, branches, and long-term history
* Checkpoints complement but don't replace proper version control
* Think of checkpoints as "local undo" and Git as "permanent history"

## See also

* [Interactive mode](/en/docs/claude-code/interactive-mode) - Keyboard shortcuts and session controls
* [Slash commands](/en/docs/claude-code/slash-commands) - Accessing checkpoints using `/rewind`
* [CLI reference](/en/docs/claude-code/cli-reference) - Command-line options
