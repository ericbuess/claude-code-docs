> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Message your other Claude Code sessions

> Let Claude list and message your other Claude Code sessions on this machine, and reach your sessions on other machines or on the web.

<Note>
  Cross-session messaging requires Claude Code v2.1.224 or later and runs on macOS and Linux. When a session meets the requirements, messaging is on with nothing to enable. See [Availability](#availability) for provider requirements and how to confirm a session has it.
</Note>

Cross-session messaging lets Claude deliver a message from one of your Claude Code sessions to another. When a change in one session breaks what another is building on, Claude can warn that session before you notice. When one session settles a question another is blocked on, Claude can send the answer across.

A message is a piece of text one Claude writes to another, never conversation history or files. To move a whole conversation or its context, [resume the session](/docs/en/sessions#resume-a-session) instead.

Claude uses two tools for this: `ListAgents` to discover which agents it can reach, and `SendMessage` to deliver a message to one of them by name. With the same `SendMessage` tool, Claude can also message [subagents](/docs/en/sub-agents#resume-subagents) and [agent team](/docs/en/agent-teams) teammates within a single session or team. This page covers messages between your independent sessions.

## When to use cross-session messaging

Use messaging when one of your sessions has something another session needs mid-task. Claude can send a message on its own when it sees the need, for example after making a change that affects work another session is doing, or you can ask it to send one. The common cases:

* **Hand over a finding**: when one session discovers a breaking change or makes a decision, Claude summarizes it for the session working on the affected area, instead of you re-explaining it there.
* **Coordinate parallel worktrees**: when sessions work the same repository in separate [worktrees](/docs/en/worktrees), Claude can tell the other sessions what landed.
* **Get status from long-running work**: have a migration or test run report back to the session you're watching, or ask it yourself from there.
* **Message across machines**: reach one of your sessions on another machine or on the web.

Use messaging between independent sessions that you start and steer yourself. Claude Code has a dedicated feature for each of the other ways to run or reach multiple sessions, so use the one built for what you're doing instead:

* To continue one conversation in another terminal, or share its context with a new session, [resume the session](/docs/en/sessions#resume-a-session)
* For a coordinated team of sessions Claude spawns and supervises, use [agent teams](/docs/en/agent-teams)
* To watch and steer many sessions from one place, use [agent view](/docs/en/agent-view)
* To steer a session yourself from your phone or another device, rather than have sessions message each other, use [Remote Control](/docs/en/remote-control)
* To push external events, such as CI results or chat messages, into a session, use [channels](/docs/en/channels)

## Message another session

When one of your sessions learns something another session needs, such as a finding, a status, or a decision, Claude passes it along instead of you copy-pasting between terminals. Claude discovers the target with `ListAgents` and sends with `SendMessage`, so you never call either tool yourself. Claude can decide to send a message without being asked, and you can also prompt for one.

To prompt one yourself, tell Claude what you want the other session to know or do. This example is a prompt you type, not a message Claude sends:

```text wrap theme={null}
Ask the session running in my other terminal whether the migration finished
```

Claude writes the actual message itself, so your prompt can leave the content to Claude. This prompt asks for a summary without dictating its wording, and what Claude sends varies:

```text wrap theme={null}
Explain what we just did to the session working on the payments API
```

To name the target yourself, mention the session in your prompt: type `@` followed by the first letters of the session's name and pick the session from the typeahead, the same way you [@-mention a subagent](/docs/en/sub-agents#invoke-subagents-explicitly). Requires Claude Code v2.1.232 or later. Claude Code inserts the mention, such as `@api-worker`, and tells Claude which session it names, so Claude can message that session without listing your sessions first. This prompt names the target with a mention:

```text wrap theme={null}
Let @api-worker know the schema migration finished
```

Once you type at least one letter after the `@`, Claude Code suggests your other live sessions on this machine; after a bare `@`, session rows don't appear. A cloud or Remote Control session appears in the suggestions only after Claude has already listed or messaged your sessions beyond this machine. You can also type the mention without the picker. When more than one live session answers to the mentioned name, Claude asks you which one you mean before sending.

For what the message Claude writes looks like when it arrives, including an example of one, see [what a message looks like](#what-a-message-looks-like).

### Message delivery

The receiving Claude reads the message between tool calls during an active turn, so a running tool is never interrupted. When the receiving session is idle, Claude Code starts a new turn with the message.

Between two ordinary interactive sessions with default settings, Claude Code delivers the message. Delivery isn't guaranteed in every configuration, though. The receiving session checks each arriving message against its own [inbound controls](#control-inbound-messages), and the check ends in one of three outcomes:

* **Delivered**: Claude Code passes the message to the receiving Claude.
* **Held**: Claude Code sets the message aside undelivered. A held message reaches Claude only when you approve it or a later mode or settings change allows it.
* **Refused**: Claude Code drops the message without delivering it.

Once delivered, the message counts toward [usage](/docs/en/costs) like a prompt you type, and the receiving Claude can reply to the sender the same way, except in the [one-way cross-machine case](#message-sessions-on-other-machines).

Permission boundaries stay per-session. Claude is instructed never to ask another session for an action that was denied or blocked in its own session, or that its own permission settings would block, and to route that work back to you instead. On the receiving side, the [receiving session's own permission prompts and rules still apply](#how-a-session-treats-an-incoming-message) to anything the message asks for.

### See which sessions Claude can reach

Claude finds a message's target on its own, so you don't need to run anything before asking it to send. To see for yourself which sessions Claude can reach, run the `/list-agents` command. It lists each session with the name it answers to, and that name is where Claude addresses a message. The listing covers:

* **Subagents**: agents running inside the current session. [Agent team](/docs/en/agent-teams) teammates aren't listed; Claude messages them through the team's own roster.
* **Your other local sessions**: Claude Code sessions running on the same machine, including [background sessions](/docs/en/agent-view). A session appears only when it binds an [inbox socket](#the-sessions-inbox-socket).
* **Your cloud sessions**: your [Claude Code on the web](/docs/en/claude-code-on-the-web) sessions, shown while this session is connected to [Remote Control](/docs/en/remote-control). Claude Code labels them `cloud` in the listing.
* **Your Remote Control sessions on other machines**: shown while this session is connected to [Remote Control](/docs/en/remote-control), and labeled `Remote Control`. Claude Code shows `offline` as the status of a session whose Remote Control connection has dropped.

Claude addresses a session beyond this machine by name, the same as a local session. See [Message sessions on other machines](#message-sessions-on-other-machines) for how those messages travel.

A session answers to the name you set with the [`/rename`](/docs/en/commands) command or the [`--name`](/docs/en/cli-reference#cli-flags) flag. When you don't set one, Claude Code names the session itself. For an interactive session, Claude Code derives the name from the working directory's folder name, such as `my-app-3f` in a `my-app` directory.

When you rename a session, or start or resume an interactive one, with a name another live session on this machine already uses, Claude Code leaves the name with the session that already has it and [renames yours to a variant](/docs/en/sessions#name-your-sessions). Sessions can still share a name, for example when one of them runs an earlier version of Claude Code or the shared name is one Claude Code generated. Claude Code shows each local session's working directory in the `/list-agents` output, so you can tell same-named sessions apart when they run in different directories. Claude addresses the message in one of two ways, depending on how many live sessions answer to the name:

* **One session answers to the name**: Claude Code delivers the message on the name alone.
* **Several sessions share the name, or Claude Code couldn't check everywhere your sessions run**: Claude adds a short identifier to each row of its listing and uses the identifier in the address.

### Message sessions on other machines

How a message travels, and whether it passes through Anthropic servers, depends on where the target session runs:

| Where the other session runs                            | How the message travels                                                                                 |
| :------------------------------------------------------ | :------------------------------------------------------------------------------------------------------ |
| On this machine                                         | Over a per-session socket, never through Anthropic servers                                              |
| On another of your machines                             | Through Anthropic servers, arriving over that machine's [Remote Control](/docs/en/remote-control) connection |
| On [Claude Code on the web](/docs/en/claude-code-on-the-web) | Through Anthropic servers, straight to the cloud session                                                |

Starting a conversation with a session on another of your machines requires Claude Code v2.1.225 or later and a target that [appears in the listing](#see-which-sessions-claude-can-reach). Before v2.1.225, Claude could only reply to a message that arrived from one.

Same-machine delivery works wherever the feature is enabled. Each session registers itself in files on disk and binds its inbox socket there. When Claude lists or messages your local sessions, Claude Code reads those files to find them, so two sessions can reach each other only when they can see the same files. A container has its own filesystem, so a session inside it and a session on the host can't reach each other. Two sessions inside the same container can still message each other, including on a [self-hosted runner](/docs/en/self-hosted-environments).

While this session is connected to Remote Control, when you message a session on another of your machines, Claude Code shows the message in that session's conversation under this session's Remote Control name. The Claude on that machine can reply to that name. For example, when this session is connected to Remote Control as `laptop-graceful-unicorn` and you message your desktop, you see the message in the desktop session under `laptop-graceful-unicorn`.

If this session isn't connected to Remote Control when Claude sends to a session beyond this machine, the message still goes through, but without a [reply address](#what-a-message-looks-like), so the receiving Claude can't answer it. Claude is told as much when it sends.

To require your approval before any message goes beyond this machine, set [`isolatePeerMachines`](#require-approval-for-cross-machine-messages).

## How a session treats an incoming message

When session A messages session B, Claude Code tells B's Claude that the message came from another session, not from you, and limits what the message can do:

* **It can't approve anything**: a message from another session never counts as your consent, so it can't answer a pending permission prompt on your behalf.
* **It can't change configuration**: Claude Code instructs the receiving Claude never to change permission settings, `CLAUDE.md`, or other configuration because another session asked.
* **Commands don't run**: a command in the message's text, such as `/compact`, arrives as plain text. Claude Code never executes it.
* **Permission prompts still fire**: if acting on the message requires a permission the receiving session doesn't have, you see the same prompt you'd see for any other work.

<h3 id="what-a-message-looks-like">
  What a message looks like
</h3>

When the message arrives, it appears in the conversation under the sender's session name and stays there. Claude Code queues it while Claude is mid-turn, or starts a new turn with it right away when the session is idle.

A message is a piece of text one Claude writes to another. Claude receives it with the sender's name and a reply address, except for a [one-way cross-machine message](#message-sessions-on-other-machines), which carries no reply address. You see the name and the text, and the receiving session gets only that text, never the sender's conversation history or files.

This example is a message one Claude wrote to another, as the receiving session sees it:

```text wrap theme={null}
Schema migration finished: the new column is tenant_id, and rebasing on main is safe now.
```

### Control inbound messages

Set [`crossSessionInbound`](/docs/en/settings#available-settings) to choose what a session does with messages arriving from your other sessions:

| Value    | Behavior                                                                                                                                                                                              |
| :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `accept` | Claude Code delivers each message to Claude                                                                                                                                                           |
| `hold`   | Claude Code shows a notice for each message and doesn't deliver it. If an `accept` later applies, per the [precedence rules](/docs/en/settings#available-settings), Claude Code releases the held messages |
| `refuse` | Claude Code drops each message without delivering it                                                                                                                                                  |

Beyond editing a settings file, you can select the value in the `/config` row **Messages from your other sessions**. Claude Code writes the value you select to your user settings. The row requires Claude Code v2.1.232 or later and doesn't appear while managed settings or the `--settings` flag sets the key, since a user-settings value wouldn't apply then. Claude Code rejects the `/config crossSessionInbound=value` shorthand for this key.

To see which value applies, follow the `crossSessionInbound` precedence rules in the [settings reference](/docs/en/settings#available-settings). When no value applies, Claude Code decides per message from the two sessions' permission modes. It groups sessions that [bypass permission prompts](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) into one class, and every other session into the other. Plan mode counts as bypassing in sessions with bypass permissions available, and [auto](/docs/en/permission-modes#eliminate-prompts-with-auto-mode), `acceptEdits`, and `dontAsk` count as prompting:

* **The receiving session prompts for permissions**: Claude Code delivers each message. It holds one for your approval only when the sending session identifies itself as bypassing permission prompts.
* **The receiving session bypasses permission prompts**: Claude Code holds each message for your approval. It delivers one only when the sending session identifies itself as also bypassing.

When the default holds a message, Claude Code opens an approval dialog in the receiving session. The dialog shows the sender and a preview:

* **Approve** delivers that one message to Claude.
* **Deny**, or dismissing the dialog, drops it.
* When the dialog stays unanswered past the [`dialogExpiry`](/docs/en/settings#available-settings) deadline, Claude Code closes it and drops the message. The deadline defaults to five minutes. While no terminal is attached to a [background session](/docs/en/agent-view), Claude Code leaves the dialog open past the deadline. After you attach, Claude Code closes the dialog and drops the message only if it stays unanswered for a full deadline period.
* If this session's permission-mode class changes while messages are held, Claude Code re-applies the inbound rules, delivers the messages they now accept, and shows a notice.
* If a change makes `refuse` apply while messages are held, Claude Code drops every held message and reports a denial to each sender it can reach.

When the sender runs on the same machine, Claude Code tells the sending session what happened. A notice appears there when the message is held, and a follow-up reports the outcome when the receiver later delivers, denies, or expires it. A message refused on arrival produces no sender-side notice.

Claude Code holds at most 100 messages, separately from the delivery queue, and past that drops the oldest.

### Non-interactive sessions

Claude Code binds an inbox socket for a [`claude -p`](/docs/en/headless) session like an interactive one, so a long-running `-p` worker can receive messages and appears in the listing. When you start a session in [bare mode](/docs/en/headless#start-faster-with-bare-mode), Claude Code doesn't bind the socket, so that session can't receive messages and doesn't appear in the agent list.

A `-p` session can't show the approval dialog. When the [inbound default](#control-inbound-messages) holds a message there, Claude Code keeps it for the same [`dialogExpiry`](/docs/en/settings#available-settings) deadline the dialog uses, five minutes by default:

* **Before the deadline**: if a mode or settings change allows the message, Claude Code delivers it.
* **Past the deadline**: Claude Code drops the message and reports it as expired to a sender it can reach.

Set `dialogExpiry` to `"never"` to keep default-held messages until the session ends. A message held by an explicit `hold` setting doesn't expire; Claude Code delivers it only when an `accept` later applies.

When the session ends with messages still held, Claude Code reports them as expired to each sender it can reach. Before v2.1.225, no deadline applied in a `-p` session: a held message stayed held unless a permission-mode change during the run delivered it, and a session that ended with held messages reported nothing to their senders.

To let a `-p` worker take messages unattended, start it with `crossSessionInbound` set to `accept` in its `--settings` value. An `accept` in your user settings also works but applies to every session you run.

<h3 id="the-sessions-inbox-socket">
  The session's inbox socket
</h3>

Read this section when a session you expect isn't in the agent list, when you want a script or hook to post into a session, or when a sandboxed command can't reach the socket.

Claude Code binds an inbox socket for each session with cross-session messaging enabled, where other sessions on the machine deliver messages. It restricts the socket to your operating-system user, so on a shared machine another user's sessions can't reach it. For which session kinds bind one, see [Non-interactive sessions](#non-interactive-sessions).

You can find the path in two places:

* `/status` shows it in the `Peer address` row. The path is prefixed with `uds:`.
* Claude Code exports it to [hooks](/docs/en/hooks) and Bash commands as the [`CLAUDE_CODE_MESSAGING_SOCKET`](/docs/en/env-vars#variables) environment variable:
  * In a session that starts with messaging on, Claude Code exports the variable before any hook runs, including `SessionStart`.
  * When a session starts before Claude Code has fetched the feature flag that turns messaging on, such as the first session after you install Claude Code or upgrade from a version without messaging, Claude Code binds the inbox and exports the variable as soon as the fetch completes. Hooks and processes that started before that point keep the variable unset, while later hooks and Bash commands see it.
  * Each session exports its own socket, never one inherited from a parent session.

Alongside the path, Claude Code exports a per-session token as [`CLAUDE_CODE_MESSAGING_TOKEN`](/docs/en/env-vars#variables). A script posting to its own session's socket can send `{"type":"auth","token":"<token>"}` as the first line of its connection. The [own-child rules](#own-child-messages) below say when Claude Code consults the token and how it treats a message it can't verify.

<span id="own-child-messages" />Claude Code runs messages arriving on the socket through the same [inbound controls](#control-inbound-messages) as any other peer message, with one exception and one prerequisite:

* **Own-child messages**: when no `crossSessionInbound` value applies, Claude Code delivers a message it verifies came from the session's own child processes, such as a hook or Bash command posting back to its own session's socket.
  * On Linux, including inside WSL 2, Claude Code can verify by process evidence even for a child that has already exited. On macOS it can verify that way only while the posting process is still running, and in a container where Claude Code runs as process ID 1 it has no process evidence at all.
  * Where that process evidence is missing, on macOS after the posting process has exited and in containers where Claude Code runs as process ID 1, Claude Code verifies a child that sent the session's exported [`CLAUDE_CODE_MESSAGING_TOKEN`](/docs/en/env-vars#variables) as its first-line auth frame.
  * When Claude Code can verify neither way, it treats the message like any other that asserts no permission class, so a session that bypasses permission prompts holds it for your approval.
* **Sandboxed sessions**: control whether a Bash command can reach the socket from inside the [sandbox](/docs/en/sandboxing) with the sandbox's Unix-socket settings, [`sandbox.network.allowAllUnixSockets` and `sandbox.network.allowUnixSockets`](/docs/en/settings#sandbox-settings).

## Restrict cross-session messaging

Beyond the per-message defaults, you can narrow messaging in two ways. Require your approval before any message leaves the machine, or turn messaging off for a session or an organization.

### Require approval for cross-machine messages

Set [`isolatePeerMachines`](/docs/en/settings#available-settings) to `true` to require your explicit approval before any `SendMessage` reaches a session beyond this machine:

```json theme={null}
{
  "isolatePeerMachines": true
}
```

With this set, Claude Code asks for your approval before Claude's message to a session beyond this machine leaves, even in `bypassPermissions` mode, which skips ordinary permission prompts. A `true` from any settings scope applies, so a checked-in project file can turn the requirement on but not off. Claude Code doesn't prompt for messages between sessions on the same machine.

### Turn off cross-session messaging

Receiving and sending are separate controls, so turn off whichever direction you need, or both. Use `crossSessionInbound` for messages that arrive, and permission rules for what Claude here can send or list:

* **Stop receiving**: set `crossSessionInbound` to `refuse`, and Claude Code drops inbound peer messages without delivering them. From project or local settings, `refuse` applies over every other source, and from your user settings it applies unless managed settings or the `--settings` flag set a value.
* **Stop sending and listing**: add [permission deny rules](/docs/en/permissions#tool-specific-permission-rules) naming `SendMessage` and `ListAgents`. Both take the bare tool name with no specifier.

Administrators can turn both sides off for an organization in [managed settings](/docs/en/permissions#managed-settings), combining the deny rules with the `refuse`:

```json theme={null}
{
  "permissions": {
    "deny": ["SendMessage", "ListAgents"]
  },
  "crossSessionInbound": "refuse"
}
```

With this in place, Claude Code still binds each session's inbox socket, but drops every message that arrives on it without delivering anything to Claude. Denying `SendMessage` also removes messaging to subagents and agent-team teammates, since the same tool serves both. A refusing session shows no visible change, in its own `/status` or in other sessions' listings, so confirm the setting from the session's configuration.

## Availability

Cross-session messaging requires Claude Code v2.1.224 or later. Availability also depends on your platform, provider, and configuration:

* **Operating system**: available on macOS and Linux, including Linux inside WSL 2. Claude Code doesn't offer cross-session messaging on native Windows.
* **Provider**: not available on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry.
* **Feature-flag evaluation**: when any of [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, or `DISABLE_GROWTHBOOK`](/docs/en/env-vars#variables) turns off the feature-flag evaluation the feature depends on, cross-session messaging stays off. Each variable's row says which values do that. Unset whichever applies. These variables can come from your shell, from a settings file's `env` map, or from managed settings.

To check a session, type `/list-agents`, also available as `/peers`. The result separates a session that doesn't have the feature from a session where something narrower blocked a message, such as a missing `SendMessage` tool or a refused send:

* **`/list-agents` isn't recognized**: the session doesn't have cross-session messaging. Work through the requirements above, starting with `claude --version` for the version requirement.
* **`/list-agents` works but a send didn't arrive**: messaging is on, and something narrower applies:
  * **Deny rules**: a [permission deny rule](#turn-off-cross-session-messaging) removes the `SendMessage` and `ListAgents` tools.
  * **Inbound controls**: the [receiving session's inbound controls](#control-inbound-messages) can hold or drop what you send it.
  * **Cloud session missing**: a cloud session appears only while this session is connected to [Remote Control](/docs/en/remote-control).
  * **Other-machine session missing**: a session on another of your machines appears only when it runs with [Remote Control](/docs/en/remote-control) and this session is connected as well.
  * **Starting a conversation**: [Message sessions on other machines](#message-sessions-on-other-machines) covers starting a conversation with a session beyond this machine.

In a session with messaging, `/status` also shows a `Peer address` row with the session's own inbox address.

## Limitations

The limits here are properties of the messaging channel itself and apply wherever the feature runs. For platform and provider gaps, see [Availability](#availability) instead.

* **Plain text only**: Claude sends only plain text across sessions. Structured [agent team](/docs/en/agent-teams) protocol messages stay within a team.
* **Message loops are throttled**: Claude Code rate-limits repeated messages per sender, drops identical repeats arriving within a short window, and caps accepted messages waiting for Claude to read them at 50 per session. A message loop between two sessions therefore stops on its own.

## Related resources

* [Subagents](/docs/en/sub-agents#resume-subagents) and [agent teams](/docs/en/agent-teams#messages-between-agents): messaging within a single session or team
* [Background agents](/docs/en/agent-view): dispatch and monitor the parallel sessions you might message
* [Remote Control](/docs/en/remote-control): connect this session to reach your sessions on other machines
* [Settings](/docs/en/settings#available-settings): `crossSessionInbound`, `isolatePeerMachines`, and `dialogExpiry`
* [Permission modes](/docs/en/permission-modes): the modes behind the inbound default's two classes
* [Tools reference](/docs/en/tools-reference): the `ListAgents` and `SendMessage` rows in the tools table
* [Run agents in parallel](/docs/en/agents): compare the ways Claude Code runs multiple agents
