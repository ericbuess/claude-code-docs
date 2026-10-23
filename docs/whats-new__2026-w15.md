> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 15 · April 6–10, 2026

> Ultraplan cloud planning, the Monitor tool with self-pacing /loop, /team-onboarding for packaging your setup, and /autofix-pr from your terminal.

Releases [v2.1.92 → v2.1.101](https://code.claude.com/docs/en/changelog.md#2-1-92)
4 features · April 6–10

Ultraplan
research preview

Kick off plan mode in the cloud from your terminal, then review the result in your browser. Claude drafts the plan in a Claude Code on the web session while your terminal stays free; when it's ready you comment on individual sections, ask for revisions, and choose to execute remotely or send it back to your CLI. As of v2.1.101 the first run auto-creates a default cloud environment, so there's no web setup step before you can try it.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/aFXPQxiBOW99MHS3/images/whats-new/ultraplan.mp4?fit=max&auto=format&n=aFXPQxiBOW99MHS3&q=85&s=e8f2f23730c6a5c289dbf3e7b13eadf6" />

Run the command, or just include the keyword in any prompt:

```text title="Claude Code" wrap theme={null}
/ultraplan migrate the auth service from sessions to JWTs
```

[Ultraplan guide](https://code.claude.com/docs/en/ultraplan)

Monitor tool
v2.1.98

A new built-in tool that spawns a background watcher and streams its events into the conversation: each event lands as a new transcript message that Claude reacts to immediately. Tail a training run, babysit a PR's CI, or auto-fix a dev server crash the moment it happens, all without a Bash sleep loop holding the turn open.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/aFXPQxiBOW99MHS3/images/whats-new/monitor-tool.mp4?fit=max&auto=format&n=aFXPQxiBOW99MHS3&q=85&s=f4156c15a0999de5c5157f54a3117c89" />

Ask Claude to watch something while you keep working:

```text title="Claude Code" wrap theme={null}
Tail server.log in the background and tell me the moment a 5xx shows up
```

This pairs with `/loop`, which now self-paces: omit the interval and Claude schedules the next tick based on the task, or reaches for the Monitor tool to skip polling altogether.

```text title="Claude Code" wrap theme={null}
/loop check CI on my PR
```

[Monitor tool reference](https://code.claude.com/docs/en/tools-reference.md#monitor-tool)

/autofix-pr
CLI

PR auto-fix landed on the web in Week 13. Now you can turn it on without leaving your terminal: `/autofix-pr` infers the open PR for your current branch and enables auto-fix for it on Claude Code on the web in one step. Push your branch, run the command, walk away; Claude watches CI and review comments and pushes fixes until it's green.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/aFXPQxiBOW99MHS3/images/whats-new/autofix-pr.mp4?fit=max&auto=format&n=aFXPQxiBOW99MHS3&q=85&s=95f191eb4711130a128aec3f6b720527" />

Run it from the PR's branch:

```text title="Claude Code" wrap theme={null}
/autofix-pr
```

[Auto-fix pull requests](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests)

/team-onboarding
v2.1.101

Generates a teammate ramp-up guide from your local Claude Code usage. Run it in a project you know well and hand the output to a new teammate so they can replay your setup instead of starting from defaults.

Run it from a project you've spent real time in:

```text title="Claude Code" wrap theme={null}
/team-onboarding
```

[Commands reference](https://code.claude.com/docs/en/commands.md)

Other wins

Focus view: press `Ctrl+O` in flicker-free mode to collapse the view to your last prompt, a one-line tool summary with diffstats, and Claude's final responseGuided [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md) and [Google Cloud's Agent Platform](https://code.claude.com/docs/en/google-vertex-ai.md) setup wizards on the login screen: pick "3rd-party platform" for step-by-step auth, region, credential check, and model pinning`/agents` gets a tabbed layout: a Running tab shows live subagents with a `● N running` count, plus Run agent and View running instance actions in the Library tabDefault effort level is now `high` for API-key, Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, Team, and Enterprise users (control with `/effort`)`/cost` shows a per-model and cache-hit breakdown for subscription users`/release-notes` is now an interactive version pickerStatus line: new `refreshInterval` setting re-runs the command every N seconds, and `workspace.git_worktree` in the JSON input`CLAUDE_CODE_PERFORCE_MODE`: Edit/Write fail on read-only files with a `p4 edit` hint instead of silently overwritingOS CA certificate store is now trusted by default, so enterprise TLS proxies work without extra setup (`CLAUDE_CODE_CERT_STORE=bundled` to opt out)Amazon Bedrock powered by Mantle: set `CLAUDE_CODE_USE_MANTLE=1`Hardened Bash tool permissions: backslash-escaped flags, env-var prefixes, `/dev/tcp` redirects, and compound commands now prompt correctly`UserPromptSubmit` hooks can set the session title via `hookSpecificOutput.sessionTitle`

[Full changelog for v2.1.92–v2.1.101 →](https://code.claude.com/docs/en/changelog.md#2-1-92)
