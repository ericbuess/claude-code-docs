> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Best practices for Claude Code

> Get more out of Claude Code: tell Claude what it can't see, give it a check to run, and enforce the rules that can't have exceptions.

Claude Code is built in a way that, in most cases, your first plain prompt in a fresh session already does the right thing, without any setup on your part.

For example:

* To let commands run safely without you approving each one, new terminal and VS Code sessions start in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), where a classifier reviews anything risky before it runs.
* To keep your main conversation focused while independent work happens in parallel, Claude delegates to subagents and checks in only when it has to.
* To keep a long session going without you managing it, your conversation is compacted automatically before the context window fills.

This page covers what to do when the defaults aren't enough. That usually happens when your project has knowledge, rules, or constraints that Claude can't see from the code alone:

* A deploy process that lives in someone's head
* A file that must never be read
* A check that has to pass before anything counts as done
* A budget you need to stay under

No default can know those things about your project, so this is where a small amount of setup on your side pays off.

When a session doesn't go the way you expected, it's almost always one of these:

* Claude built something different from what you had in mind, or it has to rediscover the same fact at the start of every session. It's missing information it can't get from reading the repo. See [Tell Claude what it can't see](#tell-claude-what-it-cant-see).
* Claude said it was done and it wasn't quite, usually because it had no way to check its own work. See [Give Claude a check to run](#give-claude-a-check-to-run).
* Claude did something that must never happen in this repo, or skipped a step that must always happen. A prompt alone can't guarantee either of those. See [Enforce the rules that can't have exceptions](#enforce-the-rules-that-cant-have-exceptions).
* Claude got it right, but it took more time, tokens, or permission prompts than the task was worth. See [Change a default](#change-a-default).

[Let Claude run without you](#let-claude-run-without-you) applies the same four points to unattended runs, and [What you can stop doing](#what-you-can-stop-doing) lists the advice that current models have made unnecessary.

> [!NOTE]
>
> Setup for a whole team is on a separate page: [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup.md).

## Deterministic and non-deterministic instructions

Every instruction you give Claude Code is one of these:

1. Non-deterministic: you write the instruction, and Claude (the model) reads it. This can be your prompt, `CLAUDE.md`, or a skill. The model then decides what to do with this information. It usually follows your commands, and current models are good at understanding your intent without much context, but there's no *guarantee* that it'll follow your instructions. It can still decide not to do things, or do other things.
2. Deterministic: you configure the instruction, and Claude Code (the harness) *has* to execute this. This can be a hook, a deny rule, or a managed setting. Claude Code applies this every time, no matter what the model decided to do.

Most things in Claude Code come in both forms:

| | Non-deterministic (Claude decides) | Deterministic (Claude Code enforces) |
| :- | :- | :- |
| What to do | Your prompt, `CLAUDE.md`, skills Claude picks up itself | Hooks, and which skills only you can start |
| What it can touch | Auto mode's classifier | Deny rules, the sandbox in [strict mode](https://code.claude.com/docs/en/sandboxing.md#turn-off-the-retry-with-strict-sandbox-mode), managed settings |
| When it's done | A request for evidence, `/goal`, `/code-review` | Tests, typecheck, a `Stop` hook, CI |
| How much it spends | Effort level, Claude's own pace | `--max-turns` or [`--max-budget-usd`](https://code.claude.com/docs/en/cli-reference) with `-p`, a [spend limit](https://code.claude.com/docs/en/costs.md) you've set |
| Who has the last word | Claude's summary of what it did | Branch protection, a person who approves the merge |

Most of the time, you want Claude to decide. Almost every guideline has exceptions, and current models are good at reading the code in front of them and judging whether a guideline fits the situation. With the actual code in front of it, Claude is usually better placed to make that call than a rule you wrote in advance.

The deterministic kind is for when you want to make sure certain things *always* happen (or never happen), no matter what the model decides. This doesn't have to be anything dramatic. Auto mode already [blocks the dramatic things](https://code.claude.com/docs/en/permission-modes.md#what-the-classifier-blocks-by-default), like a production deploy or a force push over someone's work. It's usually something specific to *your* project, and it can be as niche as you want it to be:

* Never edit the generated client in `src/gen/`
* Always run the license-header script after creating a file

You could've written either of these as a line in `CLAUDE.md` or in your prompt, and Claude would follow it nearly every time. But no matter how strongly you word it, whether Claude follows that line on a given turn is still Claude's call.

> [!TIP]
>
> If you keep adding emphasis to a `CLAUDE.md` line and Claude still misses it, that's a sign the line belongs in a hook. The reverse holds too: if you have hooks for things that are only preferences, delete them and let Claude decide.

## Tell Claude what it can't see

> [!TIP]
>
> Only write down what Claude can't find by reading the repo, or what it would otherwise spend time rediscovering every session.

Claude starts every task by reading your code, and current models are *very* good at this. They'll find your file layout, your conventions, your test framework, and how existing components are built, usually faster than you could explain them. That means Claude already knows most of what you might be tempted to write down for it.

What it can't find is the information that was never in the repo:

* A decision your team made in a meeting
* A deploy process that lives in one person's head
* The environment variable your integration tests need

There's also information that *is* in the repo but takes a few minutes of digging to find, and Claude has to redo that digging at the start of every session.

A good test before you write anything down for Claude:

1. Could it find this by reading the code?
2. Would it actually go and look?

If both are yes, leave it out.

### Write a specific prompt

A specific prompt helps for the same reason, because it gives Claude information it doesn't already have. If you name the file, describe the symptom, and say what "fixed" looks like up front, you usually save yourself a round of corrections later.

The same goes for a preference between two reasonable approaches: Claude can't read that from the code, so if you care which one it picks, say so up front.

| Instead of | Try |
| :- | :- |
| *"fix the login bug"* | *"users report login fails after the session times out. look at token refresh in src/auth/, write a failing test that reproduces it, then fix it"* |
| *"add a calendar widget"* | *"follow the pattern in HotDogWidget.php and build a calendar widget that lets you pick a month and page between years. no new libraries"* |

If you already have the thing Claude needs, hand it over instead of describing it:

* A file: type `@` and the path to [include the file contents](https://code.claude.com/docs/en/common-workflows.md#reference-files-and-directories) in your message.
* An image: paste the screenshot of the design or the error into the prompt.
* Command output: pipe it in from your shell with `cat error.log | claude -p "what's going on here"`.

Phrases like `think step by step` or `be thorough` are ordinary prompt text rather than keywords. The main control for how hard Claude thinks is the [effort level](https://code.claude.com/docs/en/model-config.md#adjust-effort-level), which [Change the model and effort](#change-the-model-and-effort) covers. Wording like that can still nudge Claude within its effort setting, but it won't lift it past it.

One phrase that does still help is `be ambitious`. Claude tends to read a request conservatively and build the smallest thing that satisfies it, since it can't see how much you were hoping for. When you want the fuller version, with the edge cases handled and the natural follow-on included, say so:

```text theme={null}
build the settings page from the mockup. be ambitious: empty and error states, the save flow wired up, keyboard navigation, not just the layout
```

That's telling Claude about scope, which only you know, rather than how hard to think.

And when you're exploring rather than fixing something specific, a vague prompt like `what would you improve in this file?` is completely fine. You'll correct a bit more as you go, and that's the trade-off.

### Brainstorm with Claude first

When you don't know exactly what you want yet, you don't have to work it all out before you prompt. Ask Claude to interview you instead:

```text theme={null}
I want to add rate limiting to the public API but haven't thought it through yet. Interview me until you could write the spec, then write it to SPEC.md.
```

Claude comes back with multiple-choice questions about the parts you haven't pinned down: per-user versus per-key limits, what happens to requests over the limit, what's out of scope. It keeps asking until the answers add up to a spec.

Once `SPEC.md` exists, start a fresh session to build from it, so the build begins with a clean context and a written definition of done. It's also the file you'll point the reviewer at later, in [Give Claude a check to run](#give-claude-a-check-to-run).

### Keep CLAUDE.md short

Claude Code loads [`CLAUDE.md`](https://code.claude.com/docs/en/memory) into every session, which means every line in it takes a little of Claude's attention on *every* task, whether it's relevant or not. That's why the file works best when it only holds what Claude couldn't work out from the code itself:

* How to confirm work in this repo: the exact test, typecheck, and lint commands, and how to run a single test file
* Places where the code is misleading: an old pattern that's everywhere but that new code must not copy, or a directory that looks unused but isn't
* Decisions that aren't in the repo: which error helper the team settled on, how deploys work, what needs a migration review
* Anything you've had to correct twice already

A `CLAUDE.md` that passes that test stays short:

```markdown CLAUDE.md theme={null}
# Commands
- Install: pnpm install
- Run one test file: pnpm vitest run path/to/file.test.ts
- Typecheck: pnpm tsc --noEmit

# Conventions
- Use the error helpers in src/lib/errors.ts, never throw raw strings
- src/legacy/ is still live but don't copy its patterns into new code

# Gotchas
- Integration tests need DATABASE_URL set, see .env.example
```

In a session, run `/context` to confirm that Claude loaded the file.

Notice that the typecheck line is only the command. Claude needs to know the command so it can check its own work as it goes. If you also want Claude Code to *enforce* a passing typecheck before Claude finishes, that's a job for a [`Stop` hook](#enforce-the-check-with-a-stop-hook). A line like `Always typecheck before you finish` in this file works most of the time, not every time.

You don't have to write the file from scratch:

* `/init` generates a starting version from your codebase. From there the work is mostly removing lines. The [memory guide](https://code.claude.com/docs/en/memory.md#write-effective-instructions) recommends staying under 200.
* `/doctor` suggests cuts for anything Claude can [already work out from the code](https://code.claude.com/docs/en/memory.md#my-claude-md-is-too-large).
* `/doctor prompt-audit` flags instructions that were written for older models, point at files that no longer exist, or [contradict each other](https://code.claude.com/docs/en/memory.md#audit-your-instruction-files).

Your personal preferences go in `CLAUDE.local.md` instead of `CLAUDE.md`, and you add that file to `.gitignore` so it stays out of the repo.

> [!NOTE]
>
> If Claude keeps ignoring a line that *is* in `CLAUDE.md`, adding IMPORTANT probably won't fix it. Either the file has grown long enough that the line gets lost, or the line is a rule that can't have exceptions, in which case it belongs in a [hook](#enforce-the-rules-that-cant-have-exceptions).

### Scope rules to one part of the codebase

If a rule only matters in one part of the codebase, put it in [`.claude/rules/`](https://code.claude.com/docs/en/memory#path-specific-rules) with a `paths:` filter so it only loads when Claude is actually working there. For example, this `.claude/rules/api.md` loads for TypeScript files under `src/api/`:

```markdown .claude/rules/api.md theme={null}
---
paths:
  - "src/api/**/*.ts"
---
- Validate request bodies with the zod schemas in src/api/schemas/, don't hand-roll checks
- Every new endpoint needs an entry in openapi.yaml, CI fails without it
```

### Put team procedures in skills

A more capable model knows more about engineering, but not how *your* team does a release, what your incident runbook says, or how you want API docs written. That kind of knowledge goes in a [skill](https://code.claude.com/docs/en/skills.md): a procedure or a piece of team knowledge saved at `.claude/skills/<name>/SKILL.md`.

Skills are also lighter on context than `CLAUDE.md` for this kind of thing. For a skill Claude can start on its own, it sees the name and description in every session, but only [reads the full file](https://code.claude.com/docs/en/skills.md#skill-content-lifecycle) when the task calls for it. A long release procedure sitting in a skill doesn't weigh on your unrelated bug fix the way it would in `CLAUDE.md`.

> [!NOTE]
>
> The `CLAUDE.md` rule applies to skills too: only write down what Claude can't find on its own.

For a workflow with side effects, like actually cutting that release, add `disable-model-invocation: true`. Claude then [can't start the skill on its own](https://code.claude.com/docs/en/skills.md#control-who-invokes-a-skill), and it only runs when you type `/release` yourself. Saved as `.claude/skills/release/SKILL.md`, it could look like this:

```markdown .claude/skills/release/SKILL.md theme={null}
---
name: release
description: Cut a new release. Bumps the version, writes the changelog entry, tags it and pushes the tag so CI can publish.
disable-model-invocation: true
---
1. Make sure you're on main with a clean tree. If not, stop and ask.
2. Run `pnpm changeset version` and commit the result.
3. Summarize the PRs merged since the last tag into CHANGELOG.md, one line each, user-facing changes only.
4. Tag `v<new version>` and push the tag. CI publishes from there, never publish from your machine.
```

### Connect the tools Claude needs

Some of what Claude can't see lives in another system entirely, like your issue tracker or your error dashboard. If that system has a CLI, that's usually the easiest way in. With `gh` installed and signed in, for example, Claude will open pull requests and read review comments without any explanation from you. For a CLI it hasn't seen before, pointing it at `--help` is enough.

For systems without a CLI, there's [MCP](https://code.claude.com/docs/en/mcp.md). You add a server from your shell:

```bash theme={null}
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

The server then shows up under `/mcp` inside a session. Connected servers add their tool names and instructions to the context even when you're not using them, so it's worth [turning off the ones you don't need](https://code.claude.com/docs/en/mcp.md#disable-a-server-without-removing-it) there.

And if you work in a typed language, a [code intelligence plugin](https://code.claude.com/docs/en/plugins/code-intelligence.md) lets Claude jump straight to a definition instead of reading through many files to find it.

## Give Claude a check to run

Claude stops when the work looks done. If it has nothing to run that tells it whether the work actually *is* done, "looks done" is all it has to go on. In practice that makes you the test suite, and every mistake sits there until you happen to notice it.

If you give it something that comes back pass or fail, Claude can close that loop itself. It makes the change, runs the check, and if something broke it reads the output and fixes it before running the check again.

> [!TIP]
>
> Give Claude something it can run that comes back pass or fail. Once it has that, it can keep going on its own and you don't have to watch.

The check can be almost anything, as long as Claude can read the result:

* A test file
* A build's exit code
* A linter
* A script that diffs output against a fixture
* A [browser screenshot](https://code.claude.com/docs/en/chrome.md) next to the mockup

If your repo already has one of these, the single most useful line in your `CLAUDE.md` is the command that runs it.

How strict you make the check is up to you. The options go from Claude deciding for itself all the way to Claude Code enforcing it:

* In the prompt: `run the auth tests after, and keep going until they pass`. Claude decides for itself when it's satisfied. This works for any task, today, with no setup.
* As a goal: [`/goal all tests in tests/auth pass and lint is clean`](https://code.claude.com/docs/en/goal) sets a condition that a separate model checks against the conversation after every turn, and Claude keeps going until it's met. You rarely need this in the session yourself. It matters for long background runs, where Claude sometimes ends a turn with a progress summary while items are still open, and the goal sends it back.
* As a Stop hook: a [`Stop` hook](https://code.claude.com/docs/en/hooks#stop) runs your script whenever Claude tries to end its turn, and sends Claude back to work if the script exits with code 2. This one is enforced by Claude Code (the harness), so the turn doesn't end until the typecheck passes or the [block limit](https://code.claude.com/docs/en/hooks.md#stop-input) is reached. There's an [example further down](#enforce-the-check-with-a-stop-hook).
* By someone who didn't write the code: in the terminal, [`/code-review`](https://code.claude.com/docs/en/code-review-local) reviews the diff in a fresh subagent that never saw your conversation. It isn't swayed by the reasoning that produced the code.

Whichever option you use, ask Claude for *evidence*: the command it ran and its output, or the screenshot. "All tests pass" on its own tells you very little, and reading the output is faster than rerunning the check yourself. For a session you weren't watching, it's also the only evidence you have.

> [!TIP]
>
> Once Claude says it's done, you can also run [`/verify`](https://code.claude.com/docs/en/skills#run-and-verify-your-app) in the session, which has Claude build and run the app and look at the result. That catches the kind of problem that tests and typechecks miss.

### Review against your spec

If you'd rather have the review check the work against your plan than hunt for bugs in general, write the review prompt yourself:

```text theme={null}
use a subagent to review the rate limiter diff against SPEC.md, check every requirement is implemented and the listed edge cases have tests, report gaps that affect correctness and skip style
```

> [!NOTE]
>
> Don't drop the `skip style` part of that prompt. A reviewer that's asked to find problems will always find *something*. If you fix every finding, you end up with extra abstraction layers and tests for cases that can't happen.

### Enforce the check with a Stop hook

The `Stop` hook version of the typecheck rule is a few lines in `.claude/settings.json`. Exit code 2 is what blocks the stop. Whatever the command prints to stderr goes back to Claude as the reason it can't finish yet, which is why the compiler output is redirected there:

```json .claude/settings.json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "pnpm tsc --noEmit 1>&2 || exit 2" }
        ]
      }
    ]
  }
}
```

To see it work, ask Claude for a change that breaks a type: instead of finishing, it gets the compiler errors back and keeps going until `tsc` passes. If the hook blocks [eight stops in a row](https://code.claude.com/docs/en/hooks.md#stop-input) with no tool call between them, Claude Code overrides the next block and ends the turn. To raise the cap, set [`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`](https://code.claude.com/docs/en/env-vars).

## Enforce the rules that can't have exceptions

> [!TIP]
>
> If something has to happen every time, make it a hook, a deny rule, or a managed setting. `CLAUDE.md` is for guidelines, and Claude is allowed to decide a guideline doesn't apply.

Take three rules you might have in `CLAUDE.md` today: `Never read .env`, `Always run the formatter after editing`, `Don't touch the migrations folder`. Claude will follow these almost every time. For the few where "almost" isn't good enough, move them out of `CLAUDE.md` and into configuration that Claude Code (the harness) applies itself. From then on, the outcome doesn't depend on what the model remembers or decides.

### Enforce steps with hooks

[Hooks](https://code.claude.com/docs/en/hooks-guide.md) run something of yours at fixed points in Claude's loop: before or after a tool call, when Claude tries to stop, when a session starts, and so on. That something can be:

* A shell command (the usual case)
* A POST to an HTTP endpoint
* A tool call on one of your MCP servers
* A [`prompt` or `agent` hook](https://code.claude.com/docs/en/hooks#hook-handler-fields), which lets a model decide

A `prompt` or `agent` hook asks *another model* to decide, so it isn't deterministic either. For real enforcement, use a `command` or `http` hook, and add [`onFailure: "block"`](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails) if the action should also be stopped when the hook itself crashes or times out. For a hook that scans commits for secrets, say, you'd rather block the commit than let it through unscanned while the scanner is down.

Here's the formatter rule as a `PostToolUse` hook. It runs after every `Edit` or `Write`, and whether Claude remembers the rule no longer matters, because Claude isn't the one running it:

```json .claude/settings.json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "npx prettier --write --ignore-unknown \"$(jq -r '.tool_input.file_path')\"" }
        ]
      }
    ]
  }
}
```

To check the hook, ask Claude to add a badly indented line to a file Prettier formats. The saved file comes back with the indentation fixed.

The migrations rule becomes a [`PreToolUse` hook](https://code.claude.com/docs/en/hooks-guide#block-edits-to-protected-files) that exits with code 2 for any path under `migrations/`. You don't have to write it yourself: `write a hook that blocks edits to the migrations folder` works as a prompt, and `/hooks` shows the result. Don't overdo it, though: a hook is for a rule with *zero* exceptions, and `Prefer named exports` has plenty, so that one stays in `CLAUDE.md`.

### Limit access with permission rules and the sandbox

[Permission rules](https://code.claude.com/docs/en/permissions.md) decide what Claude is allowed to run, read, and fetch. `deny` rules hold in every permission mode, including auto and `bypassPermissions`, which is exactly why the `.env` rule belongs there:

```json .claude/settings.json theme={null}
{
  "permissions": {
    "allow": ["Bash(pnpm tsc --noEmit)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)", "Read(./.env.local)", "Read(./secrets/**)"]
  }
}
```

With this saved, asking Claude what's in `.env` fails, through the `Read` tool and through `cat .env` alike.

Rules match tool calls, not intent, so it's worth knowing where the edges are:

* The `Read` rule *does* catch `cat .env`, because Claude Code recognizes the [common file-reading commands](https://code.claude.com/docs/en/permissions.md#read-and-edit).
* It won't catch a script that opens the file.
* A `WebFetch` deny rule for a domain does nothing about `curl` to that same domain, unless the sandbox is on.

For an OS-level limit on filesystem or network access, turn on the [sandbox](https://code.claude.com/docs/en/sandboxing.md) with `/sandbox` in a session. It confines Claude's shell commands on macOS, Linux, and WSL2 and [picks up your `Read` deny rules and `WebFetch(domain:...)` rules](https://code.claude.com/docs/en/sandboxing#permission-rules) too, so for anything security-related you want both.

By default Claude can still ask to retry a blocked command outside the sandbox, and that request goes through the normal permission flow. [Strict sandbox mode](https://code.claude.com/docs/en/sandboxing.md#turn-off-the-retry-with-strict-sandbox-mode), in the `/sandbox` **Overrides** tab, turns that retry off.

> [!WARNING]
>
> Auto mode is a classifier model judging each action rather than a hard rule. It's good at that, but like any judgment call it can be wrong. You can also tune what it treats as risky, and your org can turn it off entirely, so your "never" rules belong in deny rules or hooks.

### Choose who a rule applies to

Where a rule lives decides who it applies to:

* `.claude/settings.local.json` and `~/.claude/settings.json` are yours alone. When you select **Yes, and don't ask again** for a command, Claude Code saves that rule to the local file.
* `.claude/settings.json` and the hooks in it belong to the repo. Once you commit them, they apply to everyone who works in the repo. Its deny rules apply right away. Its `allow` rules wait until each person accepts the [trust dialog](https://code.claude.com/docs/en/permissions.md#what-runs-before-you-trust-a-folder) for that folder, and [workspace trust](https://code.claude.com/docs/en/hooks.md#workspace-trust) also decides when its hooks start running on their machine.
* [Managed settings](https://code.claude.com/docs/en/managed-settings.md) belong to the organization. They come from the admin console, MDM, or a `managed-settings.json` file, and no personal settings file can override them, which makes them the only place for a security team's policy. If you are the person who sets them, see [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup.md).

Whatever the scope, keep the enforced set small. Every hook and deny rule will occasionally fire when it shouldn't, and someone has to maintain each one. If you ever find yourself at forty of them, most are probably preferences that Claude could have weighed on its own.

## Change a default

> [!TIP]
>
> The defaults are good enough to leave alone until a task costs more time, tokens, or interruptions than it should. When that happens, run `/usage` in the session to see where it went.

A new session already makes a handful of decisions for you:

* Interactive terminal and VS Code sessions start in auto mode.
* It runs [Claude Opus 5.5 at medium effort](https://code.claude.com/docs/en/model-config.md#default-model-setting) on most plans and providers.
* It delegates work to subagents when it sees a reason to.
* It compacts the conversation as it grows.

Most of the time you never think about these. When a task does cost more than it should, one of these four is usually why.

### Change the permission mode

Both ends of the permission range have a cost:

* **Manual mode**: you approve every edit and every command that isn't read-only yourself. Safe, but after the tenth prompt you start approving without reading, and nothing moves while you're away from the keyboard.
* **`bypassPermissions`**: approves everything your deny and ask rules don't cover, which only makes sense in a disposable container.

[Auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) sits between the two, and it's what interactive terminal and VS Code sessions [start in](https://code.claude.com/docs/en/permission-modes.md#which-mode-a-session-starts-in). Claude works without stopping for routine approvals, and a separate classifier model checks actions in [a fixed order](https://code.claude.com/docs/en/permission-modes.md#how-the-classifier-evaluates-actions) before they run. It concentrates on [the things you'd want a person to stop](https://code.claude.com/docs/en/permission-modes.md#what-the-classifier-blocks-by-default):

* `curl | bash`
* Production deploys and migrations
* Force pushes over other people's work
* Sensitive data sent to external endpoints
* Actions that look driven by content Claude read rather than by you

When it does block something, you get a notification and the action shows up under **Recently denied** in `/permissions`, where you can retry it with a manual approval. After [three blocks in a row](https://code.claude.com/docs/en/permission-modes.md#when-auto-mode-falls-back) (or twenty in total), auto mode pauses and goes back to asking you.

None of this replaces your deterministic controls, because it runs *after* them. Deny and ask rules and `PreToolUse` hooks apply before the classifier sees anything, so a deny rule blocks in auto mode exactly like it does everywhere else. The sandbox still confines the [shell commands it wraps](https://code.claude.com/docs/en/sandboxing.md#what-runs-outside-the-sandbox).

> [!NOTE]
>
> You can also say `don't push until I've reviewed` in the conversation, and the classifier [treats that as a block signal](https://code.claude.com/docs/en/permission-modes.md#boundaries-you-state-in-conversation). It's still a model reading the transcript, and the sentence can get lost when the conversation compacts, so anything that matters belongs in a deny rule.

The opposite problem is the classifier repeatedly stopping something that's routine in your setup. Rather than approving it manually every time, add it to `autoMode.allow` or describe your trusted infrastructure in the [auto mode configuration](https://code.claude.com/docs/en/auto-mode-config.md). It's plain English rather than patterns, and [`/auto-mode-setup`](https://code.claude.com/docs/en/auto-mode-config#generate-environment-entries) can draft the `environment` part for you from your project and recent sessions:

```json ~/.claude/settings.json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Source control: github.com/example-org and every repo under it",
      "Trusted internal domains: *.internal.example.com"
    ],
    "allow": [
      "$defaults",
      "Deploying to the staging namespace is fine, it's isolated from production and resets nightly"
    ]
  }
}
```

> [!WARNING]
>
> Keep `"$defaults"` in every list you set, because without it your entries *replace* that list's built-in rules instead of adding to them. For `environment` and `allow` you'd lose the built-in context and exceptions, and a `soft_deny` list without it drops the built-in blocks on force pushes and production deploys.
>
> The `autoMode` block also has to live in `~/.claude/settings.json` rather than the project, because the classifier ignores `autoMode` in project settings.

If you'd rather see every edit and command before it happens, `Shift+Tab` in the session cycles through the permission modes, Manual included, or start with `claude --permission-mode manual` from your shell. And if Manual then asks too often, `/fewer-permission-prompts` scans your recent transcripts for common read-only Bash and MCP calls and adds them to an allowlist in `.claude/settings.json`.

### Change the model and effort

[Effort](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) is the main control for how long Claude thinks, and it replaces most of what people used to do with prompt wording. Claude Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`, which is plenty for everyday feature work with a clear scope. The times you'd move it, with `/effort` in the session:

* Raise it with `/effort high` or `/effort xhigh` when getting it right depends on cases that are quick to overlook. Think of a bug in code you didn't write, a flaky test, or a schema change where Claude has to find every reader of the old shape. Claude then checks more edge cases and verifies more of its work before answering, which is where the extra time and tokens go.
* Lower it with `/effort low` when you're going back and forth quickly and reviewing each result anyway: brainstorming, a first sketch, a rename across a few files. Claude gets you a starting point sooner, and since you're steering every step, the extra deliberation wouldn't have changed much besides the wait.
* Save `max` for a hard problem you want Claude to work through without you, like hunting for a security vulnerability. On ordinary tasks it tends to overthink, so you pay more for an answer that may be no better than `high` would have given you.
* When only the next message needs it, like one tricky question in the middle of otherwise routine work, put [`ultrathink`](https://code.claude.com/docs/en/model-config#use-ultrathink-for-one-off-deep-reasoning) in that prompt instead of changing the setting.

For the model itself, the default Opus 5.5 handles most coding well and Sonnet costs less on routine work. [Claude Fable 5.1](https://code.claude.com/docs/en/model-config.md#work-with-fable) is there when you select it explicitly with `/model fable`, and Haiku is a good fit for subagents doing simple jobs. [Model configuration](https://code.claude.com/docs/en/model-config.md) has the full list per plan and provider.

### Know what subagents cost

Claude delegates to [subagents](https://code.claude.com/docs/en/sub-agents.md) on its own:

* Broad codebase searches go to the built-in Explore agent.
* Side tasks get [forked](https://code.claude.com/docs/en/sub-agents.md#fork-the-current-conversation) while fork mode is on (the default).
* The subagents it starts run in the background by default, so your main conversation keeps moving.

You rarely need to ask for any of this, but it helps to know what you're getting and what it costs.

Subagents pay off in these situations:

* Running independent pieces of work at the same time, so the whole task finishes sooner
* Keeping long output, like a full test run or a wide search, out of your main conversation, where it would otherwise ride along for the rest of the session
* Getting a reviewer that hasn't seen how the code was written
* Giving a task fewer tools than the main session has, like a reviewer that can read but not edit

What they cost you is mostly tokens, since every subagent sends its own requests and they count against the same usage as your main conversation. Sometimes it's time as well: a fresh subagent first has to gather context your conversation already had, so it can end up *slower* than doing the task where you are.

And by default it's the same model (or a smaller one) on the same task. You get parallelism or a fresh pair of eyes out of it, but not a smarter answer.

To spend less on them:

* Set [`model: haiku`](https://code.claude.com/docs/en/sub-agents#choose-a-model) in a subagent's definition if its work is simple, like collecting the files that import a module or checking links in the docs. That kind of job doesn't need the bigger model, and Haiku costs a lot less per request.
* Ask for short summaries back, so twenty results don't fill your context anyway.
* Check `/usage` to see what share of your usage each subagent type takes, so you can tell which ones are earning their cost.
* Give a custom subagent in `.claude/agents/` only `tools: Read, Grep, Glob`. Now it's a reviewer that can't edit anything, and that limit is enforced by Claude Code rather than requested in a prompt.

That reviewer is one short file, `.claude/agents/reviewer.md`:

```markdown .claude/agents/reviewer.md theme={null}
---
name: reviewer
description: Reviews changed files against the spec they were built from. Use after implementing a feature, before opening the PR.
tools: Read, Grep, Glob
---
You're reviewing code you didn't write. Compare the changed files against the spec you're given,
check that every requirement is implemented and the listed edge cases have tests,
and report only the gaps that affect correctness. Skip style.
```

Ask Claude to `have the reviewer compare the rate limiter against SPEC.md` and the gaps come back into your session, where Claude can fix them.

### Keep cost and context down

With a 1M-token window on most current models and compaction near the top of it, you'll rarely run out of context. You can still *pay* for context you don't need, though. Every request sends the whole conversation, so a session that's collected three unrelated tasks re-reads all three on every turn of the fourth. That's [discounted while the cache is warm](https://code.claude.com/docs/en/costs.md#why-usage-climbs-in-a-long-session) and full price once it expires.

[`/usage`](https://code.claude.com/docs/en/costs) is the first place to look. On Pro, Max, Team, and Enterprise it breaks your usage down by skill, subagent, plugin, and MCP server. It also flags patterns like long context or frequent cache misses once one of them passes 10% of your usage. From there, the usual fixes:

* `/clear` between unrelated tasks. It costs nothing, and it means the next task doesn't keep paying for the previous one's history. `/clear oauth-migration` names the session you're leaving, so you can come back to it later.
* `/compact` with a focus, like `/compact keep the API changes and the test commands`. On a long session `/compact` is itself a big request, since it reads the whole conversation to summarize it, and even more so once the cache has expired.
* Keep an eye on background work: a `/loop`, a goal's check after every turn, and Claude's own subagents all keep sending requests while you aren't typing.

> [!NOTE]
>
> The [prompt cache](https://code.claude.com/docs/en/prompt-caching.md) lasts about an hour on a subscription and five minutes on an API key, cloud provider, or usage credits. Subagents get five minutes unless you change it.
>
> On the one-hour cache, a session past about 200K tokens that sits idle is compacted shortly before the cache expires, so after lunch you continue from a summary. If you don't need the history at all, a fresh session still costs less.

## Steer the session

> [!TIP]
>
> Watch the first minute, press `Esc` the moment Claude drifts, and after two failed corrections run `/clear` and write a better prompt instead of a third.

No amount of configuration replaces watching the first minute and stepping in when Claude heads somewhere you didn't intend. There are only a few controls for that, and they're worth knowing by heart:

* `Esc` stops Claude mid-action and keeps everything up to that point, so you can redirect without losing work.
* `/rewind`, or `Esc` twice on an empty prompt, opens the [rewind menu](https://code.claude.com/docs/en/checkpointing.md#rewind-and-summarize), where you roll the code, the conversation, or both back to an earlier prompt. That makes it low-risk to try the bolder approach first and rewind if it doesn't work out. The same menu can also summarize part of the conversation when it has gone stale.
* `/clear` starts over. If you've corrected the same thing twice and it's still wrong, a third correction mostly adds to a conversation that already contains two failed attempts for Claude to keep re-reading. `/clear` plus one new prompt that folds in what you learned works better almost every time.

> [!WARNING]
>
> Checkpoints cover the files Claude edited with its own file tools in your main conversation, so a file that only a Bash command touched [isn't restored](https://code.claude.com/docs/en/checkpointing.md#bash-command-changes-not-tracked). They work alongside git rather than replacing it.

Two smaller ones: [`/btw`](https://code.claude.com/docs/en/interactive-mode#side-questions-with-%2Fbtw) answers a quick question without adding anything to the history. And for work that spans several days, `/rename oauth-migration` in the session names it, so that [`claude --resume oauth-migration`](https://code.claude.com/docs/en/sessions#resume-by-session-id-or-name) from your shell picks it back up later, checkpoints included. `claude --continue` resumes the most recent one.

## Let Claude run without you

> [!TIP]
>
> Before a run goes unattended, make sure it knows what done looks like, can check its own work, and can only touch what it should. Give it a cap on turns or spend, and have a person approve the result at the end.

Everything on this page matters a little more once you're not around to catch mistakes. While you're watching, Claude missing some piece of context isn't a big deal: you notice within a message or two and tell it. In a run you started before going to bed, nobody tells it, and you find out the next morning that it spent the whole night building on the wrong assumption.

Before you leave a task running on its own, it's worth going through these five questions with that specific task in mind:

1. Does it know what done looks like? A goal condition, a spec file, or a failing test it has to turn green.
2. Can it check its own work? The test suite, a `Stop` hook, some kind of review step.
3. What's it allowed to touch? Permission rules, `dontAsk`, the sandbox, a worktree, the one branch it may push to.
4. What stops it? `--max-turns`, `--max-budget-usd`, a spend limit.
5. Where does the result go, and who signs off? A PR, a comment, or a summary, and then a person approving the merge, the deploy, or anything else you can't take back.

Once it's going, Claude will carry a long task through on its own. The parts that stay with you are starting it, deciding what "done" means this time, and approving the merge at the end.

### Run Claude from a script

[`claude -p "prompt"`](https://code.claude.com/docs/en/headless) runs once and exits, which is how Claude Code ends up in CI jobs, git hooks, and shell loops.

In a script you'll almost always want a few more flags:

* [`--bare`](https://code.claude.com/docs/en/headless#start-faster-with-bare-mode) skips hooks, skills, plugins, MCP servers, and `CLAUDE.md` files, the repo's as well as the machine's, so the run does the same thing wherever it runs. It also never touches your claude.ai login: auth comes from `ANTHROPIC_API_KEY`, an `apiKeyHelper` in the file you pass with `--settings`, or your cloud provider's credentials.
* `--append-system-prompt`, `--mcp-config`, and `--settings` pass in whatever the run *does* need, explicitly.
* `--allowedTools` pre-approves its tools, and [`--permission-mode dontAsk`](https://code.claude.com/docs/en/permission-modes#allow-only-pre-approved-tools-with-dontask-mode) refuses anything else that would have prompted.
* `--output-format json` gives you a single result object to parse, and `stream-json` with `--verbose` streams events as they happen.

Put together, that looks like this:

```bash theme={null}
for file in $(cat files.txt); do
  claude --bare -p "Migrate $file to the new logger API and commit. Reply OK or FAIL." \
    --allowedTools "Read,Edit,Bash(git add *),Bash(git commit *)" \
    --permission-mode dontAsk \
    --max-turns 20
done
```

When a run finishes, Claude replies `OK` or `FAIL`, and a run that hits the turn limit exits with an error instead. Try it on three files first, see what goes wrong, fix the prompt, then run the rest.

Auto mode works with `-p` too if you pass `--permission-mode auto`. In a non-interactive run, a classifier block denies that one action and Claude carries on, and repeated blocks don't pause the run the way they do in a terminal. Read [how the thresholds apply there](https://code.claude.com/docs/en/permission-modes.md#repeated-block-thresholds) before you rely on it.

### Start runs on a schedule or an event

Once a run is going, Claude can handle the rest by itself. The one thing it can't do is decide to *start*, so something has to: you, a timer, or an event like a failed CI check or a new PR.

Inside an open session that's [`/loop`](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop), which repeats a prompt on an interval:

```text theme={null}
/loop 15m check CI on this branch, and if it's red pull the failing job's log, fix it and push
```

Each run is another turn in the same session, so don't leave one going in a long conversation. For anything that should happen while your laptop is closed, [`/schedule`](https://code.claude.com/docs/en/routines#create-from-the-cli) sets up a [cloud scheduled task](https://code.claude.com/docs/en/routines.md) that runs on a timer. It needs a claude.ai login rather than an API key. You can add a GitHub-event trigger by asking Claude, or an API trigger at [claude.ai/code/routines](https://claude.ai/code/routines).

> [!WARNING]
>
> Before you leave a cloud scheduled task running, protect `main` with a [GitHub branch rule the task can't bypass](https://code.claude.com/docs/en/routines.md#repositories-and-branch-permissions). And watch the first few runs of anything new before trusting it unattended.

### Run sessions in parallel

When you have separate pieces of work going at once, give each its own checkout so the edits can't collide. [`claude -w feature-auth`](https://code.claude.com/docs/en/worktrees#start-claude-in-a-worktree) starts a session in a new worktree, the [desktop app](https://code.claude.com/docs/en/desktop.md#work-in-parallel-with-sessions) runs several of these side by side, and [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md) run them in the cloud instead of on your machine.

A worktree is a fresh checkout, which means gitignored files like `.env` aren't there and dependencies aren't installed. For the first, list the gitignored files you need in a [`.worktreeinclude`](https://code.claude.com/docs/en/worktrees#copy-gitignored-files-into-worktrees) at the repo root (same syntax as `.gitignore`) and Claude Code copies them into every worktree it creates:

```text .worktreeinclude theme={null}
.env
.env.local
config/dev-credentials.json
```

Keep it to small files: it copies rather than links, so `node_modules` in there would mean a full copy per worktree. For large directories there's the [`worktree.symlinkDirectories`](https://code.claude.com/docs/en/settings-reference#worktree-symlinkdirectories) setting, or keep the install command in `CLAUDE.md` so Claude runs it whenever it starts in a new checkout.

You rarely have to clean any of this up yourself:

* When you exit an unnamed worktree session, Claude Code [removes the worktree](https://code.claude.com/docs/en/worktrees.md#clean-up-worktrees) if there's nothing in it. For a named session, or one with changes, it asks what to do.
* Subagent worktrees disappear when the subagent finishes without changes.
* Subagent and background-session worktrees that do get left behind are swept once they're older than `cleanupPeriodDays` and hold no work.

> [!NOTE]
>
> A `claude -p --worktree` run is one you clean up yourself, since it exits without asking. Remove those with `git worktree remove <path>`, and if git refuses because the worktree is locked, `git worktree unlock <path>` first.

For one big mechanical change across many files, [`/batch migrate every handler to the v2 response helpers`](https://code.claude.com/docs/en/commands) splits the work into 5 to 30 units and shows you the plan. Then it runs each unit in its own worktree and opens a PR for it. From your shell, [`claude agents`](https://code.claude.com/docs/en/agent-view) (still a research preview) gives you one screen for everything running in the background on your machine.

A second session is also the easiest independent reviewer you can get. One session writes the rate limiter, another reviews `@src/middleware/rateLimiter.ts` without having watched it being written, and you paste the findings back into the first. Same idea as `/code-review`, with you carrying the messages.

## What you can stop doing

Every one of these was good advice when it was written. Most were workarounds for something the model couldn't reliably do yet, and the models have since caught up. If a few are still habits, here's why it's safe to drop them.

| The old advice | Why it's gone |
| :- | :- |
| The context window is your main constraint, manage it aggressively | Most current models have a 1M-token window and compaction happens on its own, so running out is rare. `/clear` between tasks is still worth doing, because a focused context gets you better answers and costs less. |
| Add IMPORTANT or ALL CAPS to instructions Claude keeps missing | Older models sometimes needed the emphasis. Current ones follow a plainly worded line, and piling on emphasis mostly makes Claude over-apply the rule. If it's a rule that can't bend, turn it into a hook or a deny rule. If the line is getting lost in a long file, the file needs to be shorter. |
| Use subagents to protect your context window | Running out of context is rarely the problem anymore. Subagents are still great for parallel work, keeping noisy output out of your way, and independent review, but each of those costs extra tokens. |
| Delegate to a subagent for a better answer | Handing the same task to a subagent doesn't make the answer any better. A fresh reviewer does help, because it hasn't seen your reasoning, which is a different thing from delegating. |
| `think hard`, `think harder`, `be thorough` in the prompt | Effort is the control for that. Those phrases are ordinary prompt text that nudges Claude within its effort setting rather than keywords that raise it. `ultrathink` still works: it asks for deeper reasoning on that single turn without touching your effort setting. |
| Tell Claude to keep going, loop until done, don't be lazy | Current models usually carry on through an agreed task without being told, and lines like that are more likely to cause over-work than fix a stall. Giving Claude a check to pass is different, and still worth doing. If a run does stop short, say `continue`, and for runs nobody's watching, `/goal` or a `Stop` hook enforces it. |
| Describe your architecture and file layout in `CLAUDE.md` | Claude reads the repo itself. Only write down what isn't in there. |

If any other advice on this page ever starts to feel like busywork, that's probably a sign it belongs in this table too.

## Related resources

* [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works.md): the loop, the tools, and what loads at startup
* [Explore the context window](https://code.claude.com/docs/en/context-window.md): what uses space in a session and when it loads
* [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md): the choice between skills, hooks, MCP, subagents, and plugins
* [Choose a permission mode](https://code.claude.com/docs/en/permission-modes.md) and [Configure permissions](https://code.claude.com/docs/en/permissions.md)
* [Manage costs effectively](https://code.claude.com/docs/en/costs.md)
* [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md) and [Automate work with cloud scheduled tasks](https://code.claude.com/docs/en/routines.md)
* For team leads and admins: [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup.md)
