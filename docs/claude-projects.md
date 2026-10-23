> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Let Claude coordinate ongoing work with Projects

> Hand Claude a stream of related tasks in one conversation and let it run them as parallel cloud sessions that share repositories, instructions, and memory.

> [!NOTE]
>
> Projects are in public beta on Pro and Max plans and rolling out gradually. The rollout started with accounts that have used [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md) and don't have existing projects in claude.ai chat or Cowork. Projects aren't offered on Team or Enterprise plans yet.
>
> If you don't see **Projects** in the sidebar at [claude.ai/code](https://claude.ai/code) or in the Code tab of the [desktop app](https://code.claude.com/docs/en/desktop.md), check under **More** there. If it's missing there too, the rollout hasn't reached your account yet. You can [join the waitlist](https://claude.com/form/projects), and see [Run agents in parallel](https://code.claude.com/docs/en/agents.md) for what you can use in the meantime.

A project is one ongoing conversation where Claude coordinates a stream of related work for you. You tell it what needs doing and it starts a thread for each task.

Each thread is usually a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md): Claude Code running in the cloud rather than on your machine. When a task needs something only your computer has, you can ask Claude to [run that thread on your computer](#run-a-thread-on-your-own-computer) instead of in the cloud, through [Remote Control](https://code.claude.com/docs/en/remote-control.md). Threads run in parallel, and you can check on them and steer them from your phone. Cloud threads keep going after you close your laptop, while a thread on your computer runs only while that computer is awake.

Without a project, running several sessions means doing the coordinating yourself: you decide what each one works on, repeat the same background at the start of each, and check back to see which finished or needs an answer. With a project, you instead:

* **Send work to one place**: paste a bug report, a stack trace, or a list of tasks into the conversation whenever one comes up. Claude starts a thread for each piece of work or passes it to the thread already working in that area, and answers quick questions in place.
* **Set context once**: every new thread starts with the project's instructions, so a rule you state once, such as which branch to target, reaches all of them.
* **Walk away and come back to finished work**: when you come back an hour later or the next morning, the **Overview** pane shows which threads finished, which pull requests are ready for review, and which thread is waiting for your answer.

If you already know the work you want a project to run, go straight to [Create a project](#create-a-project).

## When to use a project

A project is worth creating when the work has a goal that outlasts one session and keeps producing tasks. These kinds of work suit a project well:

* **One goal across many repositories**: "Bring every service up to the new lint config." Claude can run a thread per repository, each with its own pull request, and the [**Overview** pane](#see-what-needs-you-in-overview) shows which ones are ready for review.
* **An area you keep feeding**: the bugs, stack traces, and review requests for one service, pasted into the conversation as they reach you. A pitfall you tell Claude to remember after one fix is in [project memory](#give-a-project-standing-context) for the next.
* **A build or migration bigger than a session**: "Build what `docs/spec.md` describes" or "Move the app off the deprecated ORM." The work splits into threads that each take a part, decisions you ask Claude to remember early on reach the later cloud threads, and the spec changes and bugs you find during the build go into the same conversation.
* **Work that isn't code**: a folder of contracts or a support-ticket export you keep coming back to with new questions, such as "find the ten most common integration mistakes in these tickets." Upload the documents instead of adding a repository, and threads deliver each write-up as a file on the project's [**Library** tab](#see-what-needs-you-in-overview).

In any of them you can send a batch of tasks, tell Claude to start without asking you to confirm, and walk away. When you're back, you can find the threads that need you under [**Waiting on you**](#see-what-needs-you-in-overview). You can also ask Claude to put part of the work on a schedule as a [cloud scheduled task](https://code.claude.com/docs/en/routines.md). If one of these is your situation, [create a project](#create-a-project).

### When something else fits better

A project still fits when only some tasks need your machine. Cloud threads work on GitHub repositories and on the files, folders, and Google Drive folders you upload to the project, and for the occasional task that needs a local database or a tool on your computer, you can ask Claude to [run that task's thread on your computer](#run-a-thread-on-your-own-computer). Something other than a project fits better in these cases:

* **One task that fits in a session**: "Fix the flaky login test." Start a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md) yourself.
* **Work where every task needs your machine**: a local database, a device emulator, or an API behind your VPN. Use a local session, or [agent view](https://code.claude.com/docs/en/agent-view.md) to run several at once. If the work only needs local files, upload them to the project instead.
* **One task that repeats on a schedule with no conversation around it**: "Post a dependency report every Monday." Create a [cloud scheduled task](https://code.claude.com/docs/en/routines.md) on its own.
* **Several people giving Claude work and steering it together in a Slack channel**: see [Claude Tag](https://claude.com/docs/claude-tag/overview).

A project draws on the same plan limits as your other Claude Code sessions and uses them faster. [Usage and cost](#usage-and-cost) covers what draws on your plan and how to keep it down.

## How a project is organized

A project is one coordinating conversation with Claude plus the threads it starts to do the work. These are its parts:

* **The project conversation**: one long-running session where Claude acts as coordinator. It takes what you send, decides what becomes a thread, and keeps track of every thread it started. It sees what threads report back, not every step they take.
* **Threads**: the workers. Each is a separate session with its own context window that does one piece of work and reports back to the conversation when it finishes. A cloud thread works on its own branch and opens a pull request when the work calls for one.
* **What every cloud thread starts with**:
  * The project's repositories and files, plus its [instructions and memory](#give-a-project-standing-context)
  * The `CLAUDE.md` in [each of the project's repositories](#what-threads-pick-up-from-your-repositories), but not the repositories' skills, `.claude/settings.json`, or `.mcp.json`
  * The [connectors](#get-skills-plugins-connectors-and-tools-into-threads) on your claude.ai account
  * A [cloud environment](#choose-an-environment-for-threads) that sets its network access, environment variables, network secrets, and installed tools
* **The Overview pane**: where you [see all the threads at once](#see-what-needs-you-in-overview) and which of them need you. Its other tabs are **Library** for the files you added and the files threads produced, **Pull requests** for the ones threads opened, and **Scheduled tasks** for scheduled work in the project.

Cloud threads don't pick up anything from the Claude Code setup on your own machine. [Get skills, plugins, connectors, and tools into threads](#get-skills-plugins-connectors-and-tools-into-threads) covers how to give them what they'd otherwise be missing.

Here is how those parts connect, from you through the conversation to the threads doing the work, with **Overview** tracking their state:

![Diagram of a project. You write in the project conversation, where Claude answers or starts a thread. Each cloud thread works on its own branch and pull request. The Overview pane lists threads by state, such as ready for review, waiting on you, and working.](https://mintcdn.com/claude-code/e8CLbxM17eD7cAiv/images/claude-projects-overview.svg?fit=max\&auto=format\&n=e8CLbxM17eD7cAiv\&q=85\&s=dbf446f69f0bbdb9961d21af207cb93b)

## Create a project

You create and use projects at [claude.ai/code](https://claude.ai/code), in the Code tab of the desktop app, or in the Claude mobile app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude). In the browser and the desktop app there are two ways to start a project:

* **From scratch**, when you know the stream of work you want Claude to run: open the **New project** dialog and name it. [Start a new project from scratch](#start-a-new-project-from-scratch) walks through the dialog.
* **From a cloud session that's already doing the work**: in that session's sidebar menu, choose **Move to project**, then **Continue as new project**. Claude proposes the project's setup from what the session was doing. See [Start from an existing cloud session](#start-from-an-existing-cloud-session).

Either way, [check the prerequisites](#check-the-prerequisites) first.

### Check the prerequisites

Before you create a project, check your plan, your GitHub setup, and what the work needs to reach:

* **Plan**: you're on Pro or Max, and **Projects** shows in your sidebar, directly or under **More**. Select **Projects** and check that it offers **New project** or **Get started**.
* **GitHub, if the project will work on code**: your code is on github.com rather than GitHub Enterprise Server, GitLab, or Bitbucket, your connected GitHub account has push access to it, and the Claude GitHub App is installed on it. If you connected GitHub with [`/web-setup`](https://code.claude.com/docs/en/web-quickstart#connect-from-your-terminal), that token lets your other cloud sessions reach a repository but isn't enough for a project's cloud threads, which need the Claude GitHub App. [Set up GitHub access](#set-up-github-access) has the steps.
* **Network access, secrets, and tools**: for cloud threads, these come from the project's [cloud environment](#choose-an-environment-for-threads). The default environment already reaches [common package registries](https://code.claude.com/docs/en/cloud-environments.md#default-allowed-domains), so check this only if the work needs other domains, a secret, or a tool that isn't preinstalled. If the work needs an MCP server, check that it shows as connected in your [claude.ai connectors](https://claude.ai/customize/connectors).

### Start a new project from scratch

Starting a project from scratch means opening the **New project** dialog, naming the stream of work, and optionally giving it a goal and the repositories and files it works on. Only the name is required, so you can create the project first and fill in the rest as the work takes shape.

**1. Open Projects**

At [claude.ai/code](https://claude.ai/code) or in the Code tab of the desktop app, select **Projects** in the left sidebar, or under **More** there. In a browser you can also go straight to [claude.ai/code/projects/browse](https://claude.ai/code/projects/browse). Then select **New project**. If the button reads **Get started** instead, select it and first upgrade or archive the existing claude.ai projects it lists.

**2. Fill in the New project dialog**

Scope the project to one stream of work you'll keep adding to, such as everything it takes to keep one API under its latency target. [When to use a project](#when-to-use-a-project) has more examples. Then fill in the dialog's fields:

* **Name**: how the project appears in the **Projects** list.
* **Goal** (optional): one line of what you're trying to get done, such as "Hold p95 API latency under 200 ms". Claude in the conversation works toward it. Without a goal, Claude works from the tasks you send, and you can add a goal later in **Project settings > General**.
* **Context** (optional): the GitHub repositories this project works on, plus any files, folders, or Google Drive folders threads should read. Click **Add** for each. Add the repositories most tasks need rather than every one the work might touch; [Decide which repositories to add](#decide-which-repositories-to-add) covers the choice, and you can add more later in **Project settings > Environment**.

Standing rules for how threads should work go in [project instructions](#give-a-project-standing-context), which you set after the project exists.

**3. Create the project**

Click **Create project**. The project's conversation opens with a message box at the bottom, where you describe work for Claude.

On your first project, Claude takes a turn of its own as soon as the project is created, unless you send a message first. That turn uses your plan. In it, Claude may:

* Start one thread that explores the repository without changing anything and proposes next steps, if the project has a repository it can read.
* Post **Setup recommendations** drawn from your recent cloud sessions: repositories to add, scheduled tasks to create, and threads it could start. Every recommended repository and scheduled task starts switched on. Switch off the ones you don't want, then click **Update setup** to add the rest, or ignore the recommendations and describe work yourself.

The project is now listed under **Projects** in the sidebar, and its conversation is open. [Your first batch](#your-first-batch) covers what to set up before you send it work.

### Start from an existing cloud session

If a cloud session you started yourself is doing work that belongs in a project, open its sidebar menu and choose **Move to project**, then pick from the submenu:

* Choose **Continue as new project** to create a new project from the session. The project opens, and Claude reads the session and posts **Setup recommendations** in the project conversation for you to confirm. The original session stays in your session list. If it was in the middle of a turn it keeps running, so stop it yourself if you don't want both working at once.
* Choose one of your existing projects to bring the session's work into that project. That project opens, and a message sent on your behalf asks Claude to read the session and pick up where it left off. The original session stays in your session list, unchanged.

A **Set up project** banner can also appear above a cloud session's message box. If you use it instead of **Continue as new project**, the result is the same, except that the session's running turn stops once the project opens.

A local session doesn't have these options. To continue its work in a project, describe the work in the project conversation, or push its branch, add that repository to the project, and name the branch in the task.

### Set up GitHub access

Most GitHub setup happens once, not per project. You connect your GitHub account to Claude once, and the Claude GitHub App is installed once per repository, or once for a whole GitHub organization if you give it all repositories. You come back to these steps when you add a repository the Claude GitHub App doesn't cover yet or one in a GitHub organization that enforces SSO.

**1. Connect your GitHub account**

If you haven't used claude.ai/code before, your first visit walks you through connecting GitHub; see [Connect GitHub](https://code.claude.com/docs/en/web-quickstart.md#connect-github). Otherwise use one of the [GitHub authentication options](https://code.claude.com/docs/en/claude-code-on-the-web.md#github-authentication-options).

**2. Install the Claude GitHub App on the project's repositories**

Install the [Claude GitHub App](https://github.com/apps/claude) and grant it the repositories the project will use. On a repository owned by a GitHub organization, only an organization owner can complete the install; if you aren't one, GitHub sends the owner an install request and the project can't use the repository until they approve it.

**3. Authorize SSO for organizations that enforce it**

If a GitHub organization enforces SAML SSO, reconnect GitHub and authorize the Claude app for that organization. Until you do, that organization's private repositories don't appear in the **New project** dialog or **Project settings > Environment**.

When one of these steps is incomplete, the **New project** dialog and the project page name the missing step and link to where you finish it. Finish the step there, then click **Check again** if the dialog offers it. If a repository is still missing from the list afterward, open the Claude GitHub App's installation on GitHub, at [github.com/settings/installations](https://github.com/settings/installations) for a personal account, and confirm the repository is listed under **Repository access**. For the error messages a thread or the project reports when access is still wrong, see [Repository access errors](#repository-access-errors).

## Work in a project

Give Claude work through the project conversation: tasks one at a time or several at once, plus updates and loose thoughts as they come up. Claude routes each message, and threads do the work and report back.

### Your first batch

Before you send a new project a batch of work, set it up so the first threads come back the way you want:

1. [Write project instructions](#write-project-instructions): the brief every thread starts from, such as which branch to target, how a thread checks its work, and what needs your go-ahead.
2. Send one small piece of the real work, or start one of the threads Claude suggested if it offered any, and open the thread when it finishes to see how it reports back and what it did on its branch. If it assumed something wrong or couldn't reach what it needed, [Threads guessed or stalled instead of asking](#threads-guessed-or-stalled-instead-of-asking) covers where to fix that.
3. Check **Thread model** and **Thread effort** in **Project settings > General**. A new project runs every thread on Opus at high effort, which draws on your plan fastest; [Choose models and let Claude manage context](#choose-models-and-let-claude-manage-context) covers the alternatives.
4. Ask Claude to [propose threads before starting them and to run a few at a time](#tune-how-claude-runs-a-project), and drop those limits once a few threads come back the way you want.

### Send work and read results

Claude decides where each message you send in the conversation goes:

* A quick question usually gets an answer in the conversation.
* New work goes to a new thread or to a thread already working in that area, and Claude tells you which. Each new thread shows up under your message as a card: a box with the thread's title and status, which you click to open the thread.
* Several unrelated tasks in one message become separate threads.

If Claude routes something differently than you wanted, say so. [Tune how Claude runs a project](#tune-how-claude-runs-a-project) lists things you can tell it, such as reusing an existing thread for follow-ups or answering in place instead of starting a thread.

A thread's full results stay in the thread, and you open its card in the conversation to read them. Files a thread produced are also on the **Library** tab in **Overview**.

Sometimes Claude proposes threads instead of starting them, in a **Suggested threads** list. Click the arrow on a suggestion to start that thread. When several are listed, a button under the list starts all of them.

### Review a thread's pull request

When a cloud thread changes code, this is what it does unless you tell it otherwise:

* **Branch**: works on a new branch, started from the repository's default branch.
* **Pull request**: opens one when you ask, and can open one on its own for a bug fix or another concrete change.
* **After it opens**: watches the pull request with [auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests) turned on, whether or not auto-fix is on for your other cloud sessions. It pushes fixes when CI fails, addresses review comments, and replies in the thread when checks pass and the pull request is ready for you.

When a thread has pushed a branch or opened a pull request, its card in the conversation can show a button for the next step:

* **Resolve conflicts**, **Fix CI**, **Address comments**, and **Merge it** send that instruction to the thread as a message from you, so you can prompt the thread yourself instead of waiting for it to react to the pull request.
* **Review PR** opens the pull request on GitHub.
* **Create PR** appears when an idle thread has pushed a branch but hasn't opened a pull request. Clicking it creates the pull request from that branch directly rather than sending the thread an instruction to open one.

To change when threads open pull requests, for example only when you ask, or which branch they start from, say so in the task or in [project instructions](#write-project-instructions).

### See what needs you in Overview

The **Overview** pane beside the conversation tracks the project's threads. It's already open the first time you open a new project. The **Overview** button in the project header closes and reopens it, and shows a dot when a thread is waiting on you.

In the desktop app, you also get a desktop notification when Claude posts in the conversation, a thread hits an error, or a thread needs your input, so you don't have to keep the project open to find out. To also get one each time a thread finishes a turn, or to turn them off for a project, choose **Notifications** in the project's sidebar menu. These notifications are desktop-only: in a browser, check the dot on the **Overview** button.

The pane's **Threads** tab groups threads by state:

| Group | What's in it |
| :- | :- |
| **Ready for review** | Threads whose pull request is open and awaiting review |
| **Waiting on you** | Threads that need your reply or approval, or that failed |
| **Working** | Threads still running |
| **Landing** | Threads whose pull request is approved or queued to merge |
| **Idle** | Threads that finished and aren't waiting on anything |
| **Resolved** | Threads marked done: by you from the thread's menu, by Claude once you've taken the last step, such as merging its pull request, or automatically after a week with no activity. You can reopen one from the same menu |

The pane's other tabs are:

* **Library**: the files and folders you added and the files threads produced
* **Pull requests**: shown once threads have opened any
* **Scheduled tasks**: the [cloud scheduled tasks](https://code.claude.com/docs/en/routines.md) Claude set up from this project

### Open a thread when you need control

Click a thread's card in the conversation or its row in **Overview** to open its transcript in the Overview pane. From there you can:

* Read what Claude did, step by step.
* Steer the task by writing in the thread's own message box. A message there goes straight to that thread, while a follow-up in the project conversation reaches it only when Claude matches the follow-up to that thread.
* Answer a permission prompt the thread is waiting on.
* Interrupt the thread with **Stop**, which replaces the send button while the thread is working, or by pressing Esc.

### Choose models and let Claude manage context

Set models and effort in **Project settings > General**. A new project runs Opus everywhere, with high [effort](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) for threads and low effort for the conversation:

* **Thread model** and **Thread effort** apply to threads. To use a different model for one task, ask for it in the task; for a thread already running, use that thread's model picker.
* **Coordinator model** and **Coordinator effort** apply to Claude in the project conversation.

You don't manage context windows in a project. Threads compact automatically, and the conversation works from recent messages, recent threads, and project memory rather than its full history, so it keeps going for as long as the project runs. Put anything that must never be dropped in [project memory](#give-a-project-standing-context). If one thread outgrows its context, it shows [Claude ran out of context on this turn](#context-limit).

### Tune how Claude runs a project

Tell Claude in the conversation how many threads to run at once, when to post updates, and when to open pull requests. If Claude is coordinating in a way you don't want, say so. For example, you can say:

* "Propose threads and wait for my go-ahead before starting them" or "Start these now without asking me to confirm"
* "Run at most two threads at a time" or "Reuse an existing thread for follow-ups in the same area"
* "Post shorter updates" or "Only post when something finishes or is blocked"
* "Give me a status update on every thread"
* "Do this task with a smaller model"
* "Don't open a pull request until I've seen the plan"
* "Tell me what's wrong in these repositories and don't fix anything yet", when you want to go through the findings before any of them becomes a thread
* "Answer that here instead of starting a thread", when Claude starts a thread for something you meant as a quick question

Claude saves preferences like these to [project memory](#give-a-project-standing-context) on its own and follows them in later cloud threads. They're instructions Claude keeps to, not enforced settings, so a thread limit you give this way isn't a hard cap. Add one to project instructions when you want it worded exactly and applied to every thread from the start.

### Unblock a thread waiting on approval

Threads run in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) when the thread's model supports it, so most tool calls run without asking you. When a thread needs your approval, the prompt is inside that thread and the thread waits until you answer it there. Telling Claude in the project conversation to go ahead doesn't reach it.

Each approval covers that prompt, or the rest of that thread if you choose the broader option. Cloud threads don't read [permission rules](https://code.claude.com/docs/en/permissions.md) from a repository's `.claude/settings.json`, so you rely on auto mode and on the approvals you give inside each thread.

### Run a thread on your own computer

When a task needs something only your computer has, such as a local database, a device emulator, or an API behind your VPN, ask Claude to run the thread for that task on your computer instead of in the cloud. When you ask in the project conversation, the thread is a Claude Code session in a folder on your machine, connected through [Remote Control](https://code.claude.com/docs/en/remote-control.md). The project's other threads keep running in the cloud. Compared with a cloud thread, a thread on your computer:

* Works with the files, tools, MCP servers, and Claude Code settings on that machine, including its hooks and permission rules, instead of the project's cloud environment
* Starts with the project's instructions, but not with its memory files loaded
* Runs only while that computer is awake with Remote Control turned on

**1. Connect the folder**

On the computer that has the folder the task needs, make it available through Remote Control in one of two ways. Both need Claude Code v2.1.280 or later on that computer.

* **In the Claude desktop app**: open **Settings > Claude Code**, turn on **Use this computer from your phone and claude.ai**, and add the folder to the list under that switch. Threads can run on this computer while the app is open.
* **In a terminal**: run `claude remote-control` in the folder and leave it running. In a git repository, add `--spawn worktree` to give each thread there its own [worktree](https://code.claude.com/docs/en/worktrees.md) instead of the folder itself.

**2. Ask for the task with Work locally**

In the project conversation, choose **Work locally** from the **+** menu beside the message box, which tags your message **Local**, and write what you want done. Saying in the message that the task should run on your computer works too.

**3. Allow it on the card**

Claude answers with an **Allow Claude to work in a folder on your device** card. Pick the folder if you connected several. Two threads working in one folder at the same time can overwrite each other's changes, so if the folder is a git repository, you can turn on **Worktree** in the folder's options to give this thread its own worktree instead. Then click **Allow once**.

The thread runs in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), so Claude runs commands and edits files in that folder without asking you each time. If auto mode is unavailable or turned off in that computer's Claude Code, the thread runs without it, and any permission prompt it raises waits for your answer in the thread, as [Unblock a thread waiting on approval](#unblock-a-thread-waiting-on-approval) describes.

While the thread runs, a laptop icon in its header shows whether your computer is connected. Click it to see which folder the thread is using or to turn the connection off. The thread pauses while that computer is asleep, and stops if the desktop app or `claude remote-control` quits. [Lost contact with your folder](#lost-contact-with-your-folder) covers getting it going again. In the desktop app, turn on **Keep this computer awake for Remote Control** under **Settings > Claude Code** to stop the computer from sleeping on its own.

A project can't run a thread on your computer while [**Require trusted devices**](https://code.claude.com/docs/en/remote-control.md#trusted-devices) is on for your account.

## Give a project standing context

Project memory, project instructions, and the project's repositories, files, and environment carry context across threads. You set each one once.

| Context | What it carries | How you set it |
| :- | :- | :- |
| Project memory | Notes Claude keeps about the project, such as requirements, decisions, and pitfalls, stored as files. Every cloud thread reads the index file `MEMORY.md` when it starts and opens the other files when it needs them | Ask Claude in the project conversation or any cloud thread to remember a requirement, a decision, or a pitfall, or to forget one. Read, edit, and delete the files in **Project settings > Memory** |
| Project instructions | Text sent to each new thread and to Claude in the project conversation, up to 16,000 characters. [Write project instructions](#write-project-instructions) covers what to put in it | **Project settings > Memory > Project instructions**, or ask Claude to change the instructions |
| Repositories, files, and environment | The repositories every cloud thread clones, the folders and files it can read under `/mnt/project-files`, and the cloud environment it runs in | Repositories and environment in **Project settings > Environment**, or ask Claude in the conversation to add a repository to the project. [Files and folders](#add-files-and-folders) from **Add** on the **Library** tab in **Overview** |

**Project settings > Memory** lists these files under **Auto memory**, because Claude writes them itself as it works in the project. They're separate from the [auto memory](https://code.claude.com/docs/en/memory.md) Claude Code keeps on your machine, even though both use a `MEMORY.md` index. Project memory is also separate from the `CLAUDE.md` files in the project's repositories. Each cloud thread still reads those `CLAUDE.md` files from its clone when it starts, so put instructions about a repository in its `CLAUDE.md` and notes about the project in project memory.

### Write project instructions

Project instructions are the brief every new thread starts from. Click the gear icon in the project header to open **Project settings**, then go to **Memory > Project instructions**. A useful brief covers:

* What the project is for
* Where the work happens: which repositories, which branch to start from, how to name pull requests
* How a thread checks its own work before calling it done
* What to do when something it needs is missing
* What needs your go-ahead first

For example:

```text theme={null}
This project holds p95 latency for the payments API under 200 ms: profiling, query and caching fixes, and the dependency upgrades that come with them, in the payments-api repository.

- Branch from main and open one draft pull request per thread.
- Before you call work done, run `make test` and `make lint` and paste the summary lines in your final message.
- If you can't reach something you need, such as a repository, a secret, an API, or a connector, say exactly what's missing in your first message and stop. Don't substitute, mock, or guess.
- Don't merge, force-push, or change CI configuration without asking me in the thread.
```

Rules about one repository, such as its build commands, belong in that repository's `CLAUDE.md`, which every cloud thread reads when the repository is part of the project. Once work is underway, when you correct a thread, also tell Claude to remember the correction: it goes into [project memory](#give-a-project-standing-context) and later cloud threads start with it.

### Decide which repositories to add

The repositories you add to a project come with their code and `CLAUDE.md` in every cloud thread, but [not their skills, `.claude/settings.json`, or `.mcp.json`](#what-threads-pick-up-from-your-repositories). Repositories you don't add are still within reach: a cloud thread can add one to itself when its task needs it. Most projects use both:

* **Add it to the project**, in the **New project** dialog, in **Project settings > Environment**, or by asking Claude in the conversation to add it to the project. Every cloud thread from then on clones it and starts with its `CLAUDE.md` loaded, whether or not the task touches it.
* **Leave it off and let threads add it when needed.** A cloud thread whose task needs a repository the project doesn't have can add it to itself, and a note in the thread says it was added to this thread only. The clone happens partway through the task, so that repository's `CLAUDE.md` wasn't there when the thread started. The next thread starts without it. A repository added this way needs the same [prerequisites](#check-the-prerequisites) as a project repository: the Claude GitHub App installed on it and push access from your GitHub account.

A project doesn't need a repository at all. Its cloud threads can still research, write documents, and write and run code in their own sandbox, and they deliver files to the **Library** tab. Any of its cloud threads can still add a repository to itself when a task calls for one.

Once the project has repositories, Claude can only add repositories from a GitHub owner the project already uses, whether it adds one to the project or a thread adds one to itself. To bring in a repository from a different owner, add it to the project yourself in **Project settings > Environment**.

For a project that spans many repositories, such as one feature with server, web, mobile, and desktop code, add the one or two repositories nearly every task touches and name the others in [project instructions](#write-project-instructions) so Claude knows where the rest of the code lives. Cloud threads then start small and pull in the other repositories only for the tasks that need them.

### Add files and folders

Add the files and folders you want threads to read in the **New project** dialog's **Context** field, or afterward with **Add** on the **Library** tab in **Overview**. These limits apply to what you add:

* **Library tab**: up to 100 files and 2 GB in one pick, with a single file up to 480 MB.
* **New project dialog**: files over 30 MB are skipped, so add larger files from the **Library** tab after you create the project.
* **Folders**: when you add a folder from either place, the project receives a copy of its first 100 files up to 200 MB, without any files over 30 MB, hidden files, or `node_modules`. A project holds up to 10 folders and Google Drive folders combined, and single files don't count toward that limit.
* **Changes after upload**: uploads are copies, so a change you make on your computer afterward doesn't reach the project until you upload the file again and choose **Replace** when asked about the existing name.

### What threads pick up from your repositories

Cloud threads load each repository's `CLAUDE.md` instructions but not its skills, `.mcp.json` servers, or `.claude/settings.json`, whether the project has one repository or several.

| In each repository | In a cloud thread |
| :- | :- |
| `CLAUDE.md`, `.claude/CLAUDE.md`, and `.claude/rules/` at the repository root | Loaded from every repository when the thread starts. `CLAUDE.md` files in subdirectories and [path-specific rules](https://code.claude.com/docs/en/memory.md#path-specific-rules) aren't loaded |
| Skills under `.claude/skills/` | Not loaded. Enable the skill for your claude.ai account instead, as [Get skills, plugins, connectors, and tools into threads](#get-skills-plugins-connectors-and-tools-into-threads) describes |
| Agents and commands under `.claude/` | Not loaded. To use them, [run the thread on your own computer](#run-a-thread-on-your-own-computer) |
| MCP servers in `.mcp.json` | Not loaded. Use the connectors on your claude.ai account instead, as [Get skills, plugins, connectors, and tools into threads](#get-skills-plugins-connectors-and-tools-into-threads) describes |
| Plugins enabled in `.claude/settings.json` | Not loaded. Add the plugin in **Project settings > Plugins** instead |
| Permission rules in `.claude/settings.json` | Not applied. Approve tool calls inside the thread, as [Unblock a thread waiting on approval](#unblock-a-thread-waiting-on-approval) describes, or [run the thread on your own computer](#run-a-thread-on-your-own-computer) |
| Hooks in `.claude/settings.json` | Not run. To use your hooks, [run the thread on your own computer](#run-a-thread-on-your-own-computer) |
| `env` in `.claude/settings.json` | Not applied. Set environment variables in the [cloud environment](#choose-an-environment-for-threads) |

### Choose an environment for threads

Every new cloud thread starts in the project's [cloud environment](https://code.claude.com/docs/en/cloud-environments.md). The environment sets which domains threads can reach, which environment variables they have, which network secrets are added to their requests, and what the setup script installs before Claude starts. Cloud threads use a default Anthropic-hosted environment until you pick one in **Project settings > Environment**.

If cloud threads need to reach an internal API or a private package registry, or need a token your machine normally holds, change the environment rather than the project: see [Network access](https://code.claude.com/docs/en/cloud-environments.md#network-access), [Add network secrets](https://code.claude.com/docs/en/cloud-environments.md#add-network-secrets), and [Setup scripts](https://code.claude.com/docs/en/cloud-environments.md#setup-scripts).

### Get skills, plugins, connectors, and tools into threads

Cloud threads don't have the skills, MCP servers, plugins, and tools installed only on your machine. A thread that Claude runs on your machine through [Remote Control](https://code.claude.com/docs/en/remote-control.md) uses what's installed there. To make each of these available to cloud threads:

* Skills: enable them for your claude.ai account, and cloud threads load the [skills you enable there](https://code.claude.com/docs/en/skills.md#skills-in-cowork-and-cloud-sessions), apart from [some threads in a self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments-configuration.md#how-each-session’s-config-is-assembled). Skills committed to a repository's `.claude/skills/` don't load in cloud threads.
* Plugins: add them in **Project settings > Plugins**; they load into each new cloud thread. Plugins that a repository declares in its `.claude/settings.json` [don't load in cloud threads](https://code.claude.com/docs/en/cloud-environments.md#what-carries-over-from-your-setup).
* MCP servers: cloud threads get their MCP tools from the connectors on your claude.ai account, which are MCP servers you connect once at [claude.ai/customize/connectors](https://claude.ai/customize/connectors). Every cloud thread can use all of them with no per-project setup. The project conversation itself has no connectors, so send work that needs one as a task for a cloud thread. [How connectors reach Claude Code](https://code.claude.com/docs/en/mcp.md#how-connectors-reach-claude-code) lists the rules for cloud sessions and the settings that turn connectors off.
* Command-line tools and packages: install them in the environment's [setup script](https://code.claude.com/docs/en/cloud-environments.md#setup-scripts).

To see which connectors a running cloud thread has at claude.ai/code, open the thread and select **Connectors** from the **+** menu beside its message box. Turning a connector off there removes it from that thread and saves that as your account default, so new threads and claude.ai chats start without it until you turn it back on. A cloud thread picks up a connector you add or reconnect after the next message you send it.

## Project settings reference

You change project settings at claude.ai/code or in the desktop app, not in `settings.json`. Open **Project settings** from **Settings** in the project's sidebar menu or from the gear icon in the project header.

Settings save as you change them; a text field you're editing, such as the goal or instructions, shows **Save changes** and **Discard** until you leave it. Changes to instructions, repositories, plugins, and environment in **Project settings** reach new threads, not threads already running.

| Setting | Section | What it controls |
| :- | :- | :- |
| Name, icon, and goal | General | The project's name and icon in the sidebar, and its one-line goal |
| Coordinator model and effort | General | The model and [effort level](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) for Claude in the project conversation |
| Thread model and effort | General | The model and effort level for threads |
| Project instructions | Memory | [Standing rules](#give-a-project-standing-context) every new thread receives |
| Project repositories | Environment | The repositories new cloud threads clone |
| Cloud environment | Environment | The [cloud environment](#choose-an-environment-for-threads) new cloud threads run in |
| Plugins | Plugins | The plugins that load into each new cloud thread |
| Usage | Usage | [Token use](#usage-and-cost) by thread and by model |
| Memory | Memory | The project's [memory files](#give-a-project-standing-context) |
| Restart Claude | General | Restarts the project conversation when [Claude stops responding there](#claude-hasnt-responded) |
| Pause, Archive, Delete | General | Stops, hides, or removes the project; see [Pause, archive, or delete a project](#pause-archive-or-delete-a-project) |

### Pause, archive, or delete a project

All three controls are at the bottom of **Project settings > General**:

* **Pause**: stops everything at once. Every running thread and the conversation are interrupted, no new threads start, scheduled tasks don't run, and the project doesn't accept messages until you resume it. Click **Resume** in the same place or on the banner above the project's message box; a paused thread continues when you send it a message after that.
* **Archive**: hides the project from the sidebar and archives its threads, which stops any thread that was running or watching a pull request. Scheduled tasks in the project don't run while it's archived. To bring the project back, open it from the Projects page and click **Unarchive**. Its threads stay archived until you unarchive them individually from the session list.
* **Delete**: permanently removes the project along with its threads, its memory, and its files, and turns off the project's scheduled tasks. This can't be undone. Branches and pull requests the threads pushed to GitHub aren't affected.

## Usage and cost

Project usage counts against the same [plan limits](https://code.claude.com/docs/en/errors.md#youve-hit-your-session-limit) as your other Claude Code sessions, and a project can't spend past those limits on its own.

A thread that reaches your plan's limit waits and continues on its own when the limit resets, so work you left running starts using your next usage window without a message from you. [A thread hit the usage limit](#usage-limit-reached) covers what you see, how to stop it, and the one case that doesn't wait.

Work goes past your plan's limits only if you have turned on [usage credits](https://code.claude.com/docs/en/costs.md#add-usage-credits-to-your-subscription) for your account. A thread can't turn them on for you.

### What draws on your plan

A project uses your limits faster than a single session does, and on a Pro plan in particular you should expect to reach your limit sooner on days you run one. These are the parts of a project that use your plan:

* **Running threads**: each is a full session, and several can run at once. There's no fixed number; Claude starts as many as the work calls for, and a limit you [ask for](#tune-how-claude-runs-a-project) is a preference rather than a cap. The enforced limit is 200 new threads per day across your projects.
* **The conversation**: Claude uses tokens of its own reading what threads report and deciding what to do next.
* **Threads watching a pull request**: an idle thread wakes up and uses your plan again when CI fails or a review comment arrives on its pull request. To stop that, ask in the thread for it to stop watching the pull request.

A project with no running threads, no watched pull requests, and no new messages doesn't use your plan while it sits idle, and neither does an archived project.

### See and reduce a project's usage

Open **Usage** in **Project settings** to see token use by thread and by model, and how much went to the project conversation. To bring it down:

* A follow-up routed to a thread that has been idle longer than the [cache lifetime](https://code.claude.com/docs/en/prompt-caching.md#cache-lifetime), an hour on Pro and Max within your plan's limits, re-reads that thread's whole conversation before doing anything. For new work, asking Claude to start a fresh thread can use less than reviving a large old one.
* For work that doesn't need the largest model, [choose a smaller model or a lower effort level](#choose-models-and-let-claude-manage-context) for threads, the conversation, or both.
* Ask Claude in the project conversation to run fewer threads at a time, or to answer small questions itself instead of starting a thread.

## How projects relate to other Claude Code features

Several Claude Code features let more than one session work at the same time, so running work in parallel is not by itself what a project is for. In a project, Claude starts and tracks the sessions instead of you, and each one starts from the same instructions. This is how each neighboring feature connects to a project:

* **Claude Tag**: [Claude Tag](https://claude.com/docs/claude-tag/overview) is Claude in your team's Slack channels, on Team and Enterprise plans. Anyone in a channel can give it work, everyone in the channel sees and steers it, and it uses connections an admin set up for that channel. A project is yours alone: you're the only one who sends it work or sees its threads, it uses your own GitHub access and connectors, and it's on Pro and Max. [How Claude Tag differs from Cowork and Claude Code](https://claude.com/docs/claude-tag/concepts/how-it-works#how-claude-tag-differs-from-cowork-and-claude-code) has the side-by-side.
* **Cloud sessions**: every thread is a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md) unless you ask Claude to run it on your machine. Either way, Claude starts and tracks it instead of you. You can also bring the work of a cloud session you started yourself into a project: choose [**Move to project**](#start-from-an-existing-cloud-session) in that session's sidebar menu.
* **Scheduled tasks**: when you ask for scheduled work in a project, Claude creates a [cloud scheduled task](https://code.claude.com/docs/en/routines.md) that runs as threads in that project and appears on its **Scheduled tasks** tab. Scheduled tasks you create outside a project keep working on their own.
* **Remote Control**: [Remote Control](https://code.claude.com/docs/en/remote-control.md) connects claude.ai to a Claude Code session running on your machine. When you ask Claude in a project to run a thread on your computer, the project [uses Remote Control to do it](#run-a-thread-on-your-own-computer).
* **Local sessions and agent view**: a session you start yourself in your terminal, IDE, or the desktop app's local environment can't be added to a project. [Agent view](https://code.claude.com/docs/en/agent-view.md) is a screen for tracking several local sessions side by side, and you still start each one and give it its task yourself.
* **Worktrees**: a [worktree](https://code.claude.com/docs/en/worktrees.md) gives each local session its own working copy of a repository. Cloud threads don't need them: each clones its repositories into its own cloud sandbox and works on its own branch.
* **Agent teams**: an [agent team](https://code.claude.com/docs/en/agent-teams.md) is one session that starts teammate sessions for a single task, on your machine or inside a cloud session, and ends with that task.
* **Subagents**: a [subagent](https://code.claude.com/docs/en/sub-agents.md) runs inside one session, does a side task in its own context window, and returns a summary to that session. A project's threads are whole sessions that Claude starts and that report back to the project conversation, and a thread can still use subagents for its own side tasks.
* **Projects in claude.ai chat and Cowork**: the [earlier Projects experience](https://support.claude.com/en/articles/9517075-what-are-projects), which groups conversations and reference files without threads or a coordinator. Those projects keep working as they do today until the redesigned experience reaches them.

[Run agents in parallel](https://code.claude.com/docs/en/agents.md) compares these options side by side.

## Limitations

* Projects are available at claude.ai/code, in the desktop app, and in the Claude mobile app, not in the terminal CLI, the VS Code extension, or the JetBrains plugin, and not through Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry.
* Project threads are [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md), or sessions on your own machine through [Remote Control](https://code.claude.com/docs/en/remote-control.md), with Anthropic as the model provider in both cases. [Security](https://code.claude.com/docs/en/security.md) and [Data usage](https://code.claude.com/docs/en/data-usage.md) cover how cloud sessions are isolated and what's retained, and [Connection and security](https://code.claude.com/docs/en/remote-control.md#connection-and-security) covers how a thread on your machine connects and what's stored.
* You can't add a session you started yourself on your machine to a project. A project reaches your machine only by [running a thread there through Remote Control](#run-a-thread-on-your-own-computer), and that section lists what it needs.
* A cloud thread's sandbox pauses between turns and resumes when the thread continues. If the sandbox can't be resumed, the thread continues from a fresh clone, so uncommitted changes can be lost. On long tasks, ask Claude to commit and push work in progress.
* A project belongs to one user. You can't share a project or its threads with another user, and thread transcripts don't have the share option other cloud sessions have. There are no organization-level controls for projects during the beta.
* A thread belongs to the one project that started it. You can't move or copy a thread to another project, or move it out to stand alone. [**Move to project**](#start-from-an-existing-cloud-session) goes the other way only: it brings a cloud session's work into a project. You can't merge two projects into one.

## Troubleshooting

For the GitHub setup prompts in the **New project** dialog, see [Set up GitHub access](#set-up-github-access).

### A thread looks stuck

Claude doesn't post each step a thread takes, so a thread that shows as running with no new messages in the project conversation is usually still working. A new cloud thread also provisions its [cloud environment](https://code.claude.com/docs/en/cloud-environments.md) before Claude begins, so its first update takes a moment. Open the thread to read its transcript. If the thread is waiting on a permission prompt, answer it there.

### Threads guessed or stalled instead of asking

When several threads come back having assumed something wrong, worked around missing access, or stopped with "blocked", the cause is usually the same gap in the project's setup rather than a problem with each task. Sort out which threads are sound before you fix anything:

1. Ask Claude in the conversation: "For every open thread, list what you asked it to do, what it assumed or couldn't reach, and what it's waiting on." Claude reads each thread and answers in the conversation.
2. For threads that started from a wrong assumption, open the thread from **Overview** and mark it resolved from its menu, or tell it what to do instead in its message box. Its branch and any pull request stay on GitHub until you delete them.
3. Fix the gap once, in [project instructions](#give-a-project-standing-context) or the [environment](#choose-an-environment-for-threads), then send one thread before sending the rest of the work again as new threads.

### Claude hasn't responded

The project conversation shows a "Claude hasn't responded" banner when Claude is running but its replies aren't reaching the project. Click **Restart Claude** on the banner, or go to **Project settings > General** and click **Restart** in the **Restart Claude** row. Claude reconnects to the conversation; any reply it was in the middle of writing is lost, and threads aren't affected.

### Repository access errors

Three messages mean a thread or the project can't reach one of its repositories. A project's cloud threads need the [GitHub prerequisites](#check-the-prerequisites) even when your other cloud sessions clone the same repository without trouble.

* **"Couldn't start the session — Claude doesn't have GitHub access to this project's repository"**, reported before the thread starts, when the Claude GitHub App isn't installed on that repository, is suspended, or isn't linked to the GitHub account you connected.
* **"Unable to access your repository"**, reported by a thread when its clone fails: GitHub rejected the clone, the repository wasn't found under the name the project has, or the branch the thread was asked to start from doesn't exist.
* **"Claude can't access" a repository**, shown when you save repositories in the **New project** dialog or **Project settings**. The message continues with an install link and a reconnect link. Use the install link if the Claude GitHub App isn't on that repository, and the reconnect link if it is, since the GitHub App can be installed on GitHub without being linked to the account you connected to Claude. If the message says the GitHub App is suspended or doesn't include this repository, follow its link to GitHub to fix that.

To fix any of them, click the button the message offers, such as **Install GitHub App** or **Select repositories on GitHub**, then **Check again**. When the block is on the GitHub organization's side, such as an owner who hasn't approved the app or an IP allow list that excludes Claude, the message shows a **See how to fix** link instead. If there's no button, follow [Set up GitHub access](#set-up-github-access), then send another message to retry.

### A thread hit the usage limit

When a thread or the project conversation reaches your plan's five-hour or weekly limit, it keeps retrying on its own and continues when the limit resets. A thread that a scheduled task started doesn't wait: its turn stops with a limit error, and you send it a message after the limit resets.

While a thread waits, it shows **Service is busy** with "Claude is still retrying and will continue automatically." You don't need to do anything for the work to continue. If you'd rather it not use your next usage window, click **Stop** in the thread, or [pause the project](#pause-archive-or-delete-a-project) to hold every thread. [Usage limit errors](https://code.claude.com/docs/en/errors.md#youve-hit-your-session-limit) explain the limits and when they reset.

### Additional usage credits are required

A thread or the project conversation made a request your plan covers only with usage credits, such as one to a model or context size your plan doesn't include, and usage credits aren't turned on for your account. [Add usage credits to your subscription](https://code.claude.com/docs/en/costs.md#add-usage-credits-to-your-subscription) covers who can turn them on or buy them on each plan. Once credits are available, send another message to retry.

### Lost contact with your folder

A thread running on your computer shows this when the Claude Code session there stopped responding, usually because the computer went to sleep or the desktop app or `claude remote-control` quit. Wake the computer, and if the desktop app or `claude remote-control` is no longer running there, start it again: reopen the app and confirm **Use this computer from your phone and claude.ai** is still on under **Settings > Claude Code**, or run `claude remote-control` again in the same folder.

### Other messages

These messages name their own cause. The table gives the next step for each.

| Message | What to do |
| :- | :- |
| "Unable to connect to repository" with "Claude couldn't reach GitHub to fetch your repository" | Wait a moment, then send another message to retry |
| "Unable to connect to repository" with "Claude couldn't access your repository or environment" | Your GitHub account needs push access to the repository, and the environment must still exist. Check both in **Project settings > Environment**, then retry |
| "Couldn't show the setup proposal" | The app you have open is older than the **Setup recommendations** Claude sent. Refresh the page or restart the desktop app, or ask Claude to propose the setup again |
| "The project's environment was removed" | Choose a different environment in **Project settings > Environment**; the change applies to new threads |
| "Setup script failed" | Click **Edit setup script** on the error, fix the script in the environment, then send another message. [Setup script failed](https://code.claude.com/docs/en/web-quickstart.md#setup-script-failed) lists common causes |
| "Claude ran out of context on this turn" | The thread filled its context window. If the message says the thread continues in a fresh session, it carries on by itself; otherwise ask Claude in the project conversation to start a new thread for the remaining work |
| "Couldn't start in" followed by your folder's name | You allowed a thread to run on your computer, but the session couldn't start there. When a line under the message gives the reason, fix that, then ask Claude to run the task again |
| "Claude is out of date on your device" | The computer you picked to run a thread has a Claude Code version older than v2.1.280. Update Claude Code there, or update the desktop app if that's what connects the folder, then ask Claude to run the task again |
| "Reached the turn limit" | The thread reached the cap on agentic turns that [`CLAUDE_CODE_MAX_TURNS`](https://code.claude.com/docs/en/env-vars) sets. Send another message to continue, or raise or remove that variable where it's set |

## Related resources

* [Use Claude Code in the cloud](https://code.claude.com/docs/en/claude-code-on-the-web.md): how the cloud sessions behind each cloud thread work, including GitHub access options and auto-fix on pull requests
* [Configure cloud environments](https://code.claude.com/docs/en/cloud-environments.md): change what cloud threads can reach on the network, give them environment variables and network secrets, and install tools with a setup script
* [Automate work with scheduled tasks](https://code.claude.com/docs/en/routines.md): schedules, triggers, and management for scheduled tasks, including the ones Claude creates from a project
* [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view.md): run and track several sessions on your own machine when the work needs tools or services only your machine can reach
* [Projects redesigned: from folder to conversation](https://claude.com/blog/projects-redesigned): the launch announcement, with the thinking behind making a project a conversation with Claude
