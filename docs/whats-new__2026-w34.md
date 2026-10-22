> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 34 · August 17–21, 2026

> Draft editable UI artboards with the /design skill, set the Concise output style, and start a Claude Code session on your machine from your phone.

Releases [v2.1.234 → v2.1.239](/docs/en/changelog.md#2-1-234)
3 features · August 17–21

/design
research preview

The `/design` skill brings Claude Design's artboard workflow into the CLI and Claude Code Desktop, built on artifacts. Run it with a brief and Claude publishes a canvas of editable artboards for your UI. Pick one, tweak it, then have Claude implement it. Available on Pro, Max, Team, and Enterprise. Requires v2.1.234 or later.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/design-skill.mp4?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=0b376a94227c14a4204af89c4c9fd7ac" />

Describe what you want designed and let Claude draft the options:

```text Claude Code theme={null}
> /design redesign the composer based on what people actually use it for
```

Claude prints a link to the published canvas. Open it, pick an artboard, and tell Claude which option to implement.

[Where artifacts are available](/docs/en/artifacts.md#availability)

Concise output style
v2.1.237

Concise is a new built-in output style. Claude leads with the result and skips preamble and narration, while doing the work as thoroughly as in the Default style. When you ask for an explanation or more detail, Claude answers in full. Error reports, security warnings, and confirmations for destructive actions keep their complete content.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/concise-output-style.mp4?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=dfb40ec8921ed1bc82eb629042a8ec17" />

Turn it on under **Output style** in `/config`, or set it in your settings file:

```json ~/.claude/settings.json {2} theme={null}
{
  "outputStyle": "Concise"
}
```

Run `/clear` or start a new session, and Claude's replies lead with the result.

[Built-in output styles](/docs/en/output-styles.md#built-in-output-styles)

Start a session on your machine from your phone
mobile

Any machine running `claude remote-control` now shows up as a device card at the top of the Code tab in the Claude app. Remote Control is also out of research preview.

![The Code tab in the Claude mobile app with a Devices section showing a connected MacBook as a device card above the sessions list](https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/remote-control-phone-start.jpg?fit=max\&auto=format\&n=2SnAdpL4dJ18nKb3\&q=85\&s=9f0ebedab23aa0e1732cc37782573907)

Start Remote Control on the machine you want to reach, then open the Code tab on your phone:

```bash terminal theme={null}
claude remote-control
```

Your machine appears as a device card at the top of the Code tab. Tap it to pick a directory and start a session there.

[Start a Remote Control session](/docs/en/remote-control.md#start-a-remote-control-session)

Other wins

Claude Code now continues your session automatically when a claude.ai usage limit resets; turn it off from the **Continue automatically at usage limit** row in `/config`The optional [`spellcheck` setting](/docs/en/interactive-mode#check-spelling-as-you-type) underlines misspelled words in the prompt input as you type, using your installed `aspell`, `hunspell`, or `ispell`On a branch with an open GitLab merge request, with the `glab` CLI authenticated through `glab auth login`, the footer shows an [`MR !N` badge](/docs/en/interactive-mode#gitlab-merge-requests) colored by whether the merge request is a draft, open, or mergeableChange the effort level from your phone or claude.ai/code and it [applies to the session on your machine](/docs/en/remote-control.md#what-connected-devices-see); Remote Control sessions hosted by Desktop or VS Code also show connected devices the session's current permission modeYou can open [`/permissions`](/docs/en/permissions#manage-permissions) or run `/add-dir <path>` while Claude is working; permission rule changes apply to the rest of the current turnWhen background tasks keep a [`/goal`](/docs/en/goal#background-work-defers-evaluation) waiting, Claude checks in on them after 30 minutes instead of waiting indefinitely and keeps checking in, at longer intervals while the session sits idle; set `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0` to opt outYour own prompts now render markdown in the transcript, with highlighted code blocks, inline code, and lists, the same way replies doThe new [`ANTHROPIC_DEFAULT_MODEL`](/docs/en/model-config#set-a-default-model-for-new-sessions) environment variable sets the model new sessions start on; a `/model` pick still overrides it and persists across restartsWith the `notify_when_idle` input on `SendMessage`, Claude can ask another Claude Code session on the same machine to [send one notice when it next goes idle](/docs/en/cross-session-messaging.md#get-a-notice-when-another-session-goes-idle)Set [`keybindingFlavor`](/docs/en/interactive-mode#make-ctrl-w-delete-back-to-whitespace) to `"readline"` to make `Ctrl+W` in the prompt delete back to the previous whitespace, as Bash does, instead of stopping at punctuation such as `/`On native Windows, your Claude Code sessions can now [message each other](/docs/en/cross-session-messaging.md#availability) with `SendMessage` and find each other with `ListAgents`, as on macOS and LinuxSelf-hosted runners accept `--defer-shutdown-max-min`, which [keeps serving attached sessions](/docs/en/self-hosted-environments-deploy.md#defer-the-drain-past-the-first-signal) for a set number of minutes after SIGTERMSelf-hosted runners accept `--proxy-authorization-command` or `--proxy-authorization-file` to supply a fresh `Proxy-Authorization` header for [egress proxies that require one](/docs/en/self-hosted-environments-deploy.md#authenticate-to-an-egress-proxy)

[Full changelog for v2.1.234–v2.1.239 →](/docs/en/changelog.md#2-1-234)
