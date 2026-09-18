> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Let Claude coordinate ongoing work with Projects

> Give Claude a body of related work in one conversation and let it coordinate parallel cloud sessions that share repositories, instructions, and memory.

<Note>
  Projects are in public beta on Pro and Max plans and rolling out gradually, starting with accounts that have used [cloud sessions](/docs/en/claude-code-on-the-web) and don't have existing projects in claude.ai chat or Cowork. They aren't available on Team or Enterprise plans yet. If **Projects** doesn't appear in the sidebar at [claude.ai/code](https://claude.ai/code) or in the Code tab of the [desktop app](/docs/en/desktop), the rollout hasn't reached your account, and you can [join the waitlist](https://claude.com/form/projects). [Run agents in parallel](/docs/en/agents) lists what you can use in the meantime.
</Note>

A project is one ongoing conversation where Claude coordinates a stream of related work for you. You tell it what needs doing and it starts a thread for each task. Each thread is a [cloud session](/docs/en/claude-code-on-the-web): Claude Code running in the cloud rather than on your machine. Threads run in parallel and keep going after you close the laptop, and you can check on them and steer them from your phone.

Without a project, running several sessions means doing the coordinating yourself: you decide what each one works on, repeat the same background at the start of each, and check back to see which finished or needs an answer. With a project, you instead:

* **Send work to one place**: paste a bug report, a stack trace, or a list of tasks into the conversation whenever one comes up. Claude starts a thread for each piece of work or passes it to the thread already working in that area, and answers quick questions in place.
* **Set context once**: every new thread starts with the project's repositories, instructions, and memory, so a rule you state once, such as which branch to target, reaches all of them.
* **Walk away and come back to finished work**: when you come back an hour later or the next morning, the **Overview** pane shows which threads finished, which pull requests are ready for review, and which thread is waiting for your answer.

If you already know the work you want a project to run, go straight to [Create a project](#create-a-project).

## When to use a project

A project is worth creating when the work has a goal that outlasts one session and keeps producing tasks. These kinds of work suit a project well:

* **One goal across many repositories**: "Bring every service up to the new lint config." Claude can run a thread per repository, each with its own pull request, and the [**Overview** pane](#see-what-needs-you-in-overview) shows which ones are ready for review.
* **An area you keep feeding**: the bugs, stack traces, and review requests for one service, pasted into the conversation as they reach you. A pitfall you tell Claude to remember after one fix is in [project memory](#give-a-project-standing-context) for the next.
* **A build or migration bigger than a session**: "Build what `docs/spec.md` describes" or "Move the app off the deprecated ORM." The work splits into threads that each take a part, decisions you ask Claude to remember early on reach the later threads, and the spec changes and bugs you find during the build go into the same conversation.
* **Work that isn't code**: a folder of contracts or a support-ticket export you keep coming back to with new questions, such as "find the ten most common integration mistakes in these tickets." Upload the documents instead of adding a repository, and threads deliver each write-up as a file on the project's [**Library** tab](#see-what-needs-you-in-overview).

In any of them you can send a batch of tasks, tell Claude to start without asking you to confirm, walk away, and find the threads that need you under [**Waiting on you**](#see-what-needs-you-in-overview) when you're back, or ask Claude to put part of the work on a schedule as a [routine](/docs/en/routines). If one of these is your situation, [create a project](#create-a-project).

### When something else fits better

Threads work on GitHub repositories and on the files, folders, and Google Drive folders you upload to the project, not on files or tools that exist only on your machine. Something else fits better in these cases:

* **One task that fits in a session**: "Fix the flaky login test." Start a [cloud session](/docs/en/claude-code-on-the-web) yourself.
* **Work that needs tools or services only your machine can reach**: a local database, a device emulator, an API behind your VPN. Use a local session, or [agent view](/docs/en/agent-view) to run several at once. If the work only needs local files, upload them to the project instead.
* **One task that repeats on a schedule with no conversation around it**: "Post a dependency report every Monday." Create a [routine](/docs/en/routines) on its own.
* **Several people giving Claude work and steering it together in a Slack channel**: see [Claude Tag](https://claude.com/docs/claude-tag/overview).

A project draws on the same plan limits as your other Claude Code sessions and uses them faster. [Usage and cost](#usage-and-cost) covers what draws on your plan and how to keep it down.

## How a project is organized

A project is one coordinating conversation with Claude plus the threads it starts to do the work. These are its parts:

* **The project conversation**: one long-running session where Claude acts as coordinator. It takes what you send, decides what becomes a thread, and keeps track of every thread it started. It sees what threads report back, not every step they take.
* **Threads**: the workers. Each is a separate [cloud session](/docs/en/claude-code-on-the-web) with its own context window that does one piece of work on its own branch, opens a pull request when the work calls for one, and reports back to the conversation when it finishes.
* **What every thread starts with**:
  * The project's repositories and files, plus its [instructions and memory](#give-a-project-standing-context)
  * The `CLAUDE.md`, skills, and plugins in [each of the project's repositories](#what-threads-pick-up-from-your-repositories), and in a project with one repository, that repository's permission rules and hooks too
  * The [connectors](#get-skills-plugins-connectors-and-tools-into-threads) on your claude.ai account
  * A [cloud environment](#choose-an-environment-for-threads) that sets its network access, environment variables, API credentials, and installed tools
* **The Overview pane**: where you [see all the threads at once](#see-what-needs-you-in-overview) and which of them need you. Its other tabs are **Library** for the files you added and the files threads produced, **Pull requests** for the ones threads opened, and **Routines** for scheduled work in the project.

Threads don't pick up anything from the Claude Code setup on your own machine. [Get skills, plugins, connectors, and tools into threads](#get-skills-plugins-connectors-and-tools-into-threads) covers how to give them what they'd otherwise be missing.

Here is how those parts connect, from you through the conversation to the threads doing the work, with **Overview** tracking their state:

<Frame>
  <img src="https://mintcdn.com/claude-code/e8CLbxM17eD7cAiv/images/claude-projects-overview.svg?fit=max&auto=format&n=e8CLbxM17eD7cAiv&q=85&s=dbf446f69f0bbdb9961d21af207cb93b" className="dark:hidden" alt="Diagram of a project. You write in the project conversation, where Claude answers or starts a thread. Each thread is a cloud session working on its own branch and pull request. The Overview pane lists threads by state, such as ready for review, waiting on you, and working." width="600" height="250" data-path="images/claude-projects-overview.svg" />

  <img src="https://mintcdn.com/claude-code/e8CLbxM17eD7cAiv/images/claude-projects-overview-dark.svg?fit=max&auto=format&n=e8CLbxM17eD7cAiv&q=85&s=549a5ba9fea8433729babc37a1f6e9c8" className="hidden dark:block" alt="Diagram of a project. You write in the project conversation, where Claude answers or starts a thread. Each thread is a cloud session working on its own branch and pull request. The Overview pane lists threads by state, such as ready for review, waiting on you, and working." width="600" height="250" data-path="images/claude-projects-overview-dark.svg" />
</Frame>

## Create a project

You create and use projects at [claude.ai/code](https://claude.ai/code), in the Code tab of the desktop app, or in the Claude mobile app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude). In the browser and the desktop app there are two ways to start a project:

* **From scratch**, when you know the stream of work you want Claude to run: open the **New project** dialog and name it. [Start a new project from scratch](#start-a-new-project-from-scratch) walks through the dialog.
* **From a cloud session that's already doing the work**: choose **Continue as a project** from that session's menu, and Claude proposes the project's setup from what the session was doing. See [Start from an existing cloud session](#start-from-an-existing-cloud-session).

Either way, [check the prerequisites](#check-the-prerequisites) first.

### Check the prerequisites

Before you create a project, check your plan, your GitHub setup, and what the work needs to reach:

* **Plan**: you're on Pro or Max and **Projects** shows in your sidebar.
* **GitHub, if the project will work on code**: your code is on github.com rather than GitHub Enterprise Server, GitLab, or Bitbucket, your connected GitHub account has push access to it, and the Claude GitHub App is installed on it. If you connected GitHub with [`/web-setup`](/docs/en/web-quickstart#connect-from-your-terminal), that token lets your other cloud sessions reach a repository but isn't enough for project threads, which need the Claude GitHub App. [Set up GitHub access](#set-up-github-access) has the steps.
* **Network, credentials, and tools**: these come from the project's [cloud environment](#choose-an-environment-for-threads). The default environment already reaches [common package registries](/docs/en/cloud-environments#default-allowed-domains), so check this only if the work needs other domains, a secret, or a tool that isn't preinstalled. If the work needs an MCP server, check that it shows as connected in your [claude.ai connectors](https://claude.ai/customize/connectors).

### Start a new project from scratch

Starting a project from scratch means opening the **New project** dialog, naming the stream of work, and optionally giving it a goal and the repositories and files it works on. Only the name is required, so you can create the project first and fill in the rest as the work takes shape.

<Steps>
  <Step title="Open Projects">
    At [claude.ai/code](https://claude.ai/code) or in the Code tab of the desktop app, select **Projects** in the left sidebar, then select **New project**. In a browser you can also go straight to [claude.ai/code/projects/browse](https://claude.ai/code/projects/browse).
  </Step>

  <Step title="Fill in the New project dialog">
    Scope the project to one stream of work you'll keep adding to, such as everything it takes to keep one API under its latency target. [When to use a project](#when-to-use-a-project) has more examples. Then fill in the dialog's fields:

    * **Name**: how the project appears in the **Projects** list.
    * **Goal** (optional): one line of what you're trying to get done, such as "Hold p95 API latency under 200 ms". Claude in the conversation works toward it. Without a goal, Claude works from the tasks you send, and you can add a goal later in **Project settings > General**.
    * **Context** (optional): the GitHub repositories this project works on, plus any files, folders, or Google Drive folders threads should read. Click **Add** for each. Add the repositories most tasks need rather than every one the work might touch; [Decide which repositories to add](#decide-which-repositories-to-add) covers the choice, and you can add more later in **Project settings > Environment**.

    Standing rules for how threads should work go in [project instructions](#give-a-project-standing-context), which you set after the project exists.
  </Step>

  <Step title="Create the project">
    Click **Create project**. The project's conversation opens with a message box at the bottom, where you describe work for Claude.

    On your first project, Claude takes a turn of its own as soon as the project is created, unless you send a message first. That turn uses your plan. In it, Claude may:

    * Start one thread that explores the repository without changing anything and proposes next steps, if the project has a repository it can read.
    * Post **Setup recommendations** drawn from your recent cloud sessions: repositories to add, routines to create, and threads it could start. Every recommended repository and routine starts switched on. Switch off the ones you don't want, then click **Update setup** to add the rest, or ignore the recommendations and describe work yourself.
  </Step>
</Steps>

The project is now listed under **Projects** in the sidebar, and its conversation is open. [Your first batch](#your-first-batch) covers what to set up before you send it work.

### Start from an existing cloud session

If you already have a cloud session doing work that belongs in a project, open the session's menu in the sidebar and choose **Continue as a project** or **Move to project**:

* **Continue as a project** creates a new project named after the session and opens it. Claude reads the session and posts **Setup recommendations** in the conversation for you to confirm. The original session stays in your session list, and if it was in the middle of a turn it keeps running, so stop it yourself if you don't want both working at once. If you use the **Set up project** banner that can appear above a cloud session's message box instead, the result is the same, except that the session's running turn stops once the project opens.
* **Move to project** brings the session's work into an existing project. It posts a message in that project's conversation asking Claude to read the session and pick up where it left off, and new work continues in the project's own threads. The original session stays in your session list, unchanged.

### Set up GitHub access

Most GitHub setup happens once, not per project. You connect your GitHub account to Claude once, and the Claude GitHub App is installed once per repository, or once for a whole GitHub organization if you give it all repositories. You come back to these steps when you add a repository the Claude GitHub App doesn't cover yet or one in a GitHub organization that enforces SSO.

<Steps>
  <Step title="Connect your GitHub account">
    If you haven't used claude.ai/code before, your first visit walks you through connecting GitHub; see [Connect GitHub](/docs/en/web-quickstart#connect-github). Otherwise use one of the [GitHub authentication options](/docs/en/claude-code-on-the-web#github-authentication-options).
  </Step>

  <Step title="Install the Claude GitHub App on the project's repositories">
    Install the [Claude GitHub App](https://github.com/apps/claude) and grant it the repositories the project will use. On a repository owned by a GitHub organization, only an organization owner can complete the install; if you aren't one, GitHub sends the owner an install request and the project can't use the repository until they approve it.
  </Step>

  <Step title="Authorize SSO for organizations that enforce it">
    If a GitHub organization enforces SAML SSO, reconnect GitHub and authorize the Claude app for that organization. Until you do, that organization's private repositories don't appear in the **New project** dialog or **Project settings > Environment**.
  </Step>
</Steps>

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

When a thread changes code, this is what it does unless you tell it otherwise:

* **Branch**: works on a new branch, started from the repository's default branch.
* **Pull request**: opens one when you ask, and can open one on its own for a bug fix or another concrete change.
* **After it opens**: watches the pull request with [auto-fix](/docs/en/claude-code-on-the-web#auto-fix-pull-requests) turned on, whether or not auto-fix is on for your other cloud sessions. It pushes fixes when CI fails, addresses review comments, and replies in the thread when checks pass and the pull request is ready for you.

When a thread has pushed a branch or opened a pull request, its card in the conversation can show a button for the next step:

* **Resolve conflicts**, **Fix CI**, **Address comments**, and **Merge it** send that instruction to the thread as a message from you, so you can prompt the thread yourself instead of waiting for it to react to the pull request.
* **Review PR** opens the pull request on GitHub.
* **Create PR** appears when an idle thread has pushed a branch but hasn't opened a pull request. Clicking it creates the pull request from that branch directly rather than sending the thread an instruction to open one.

To change when threads open pull requests, for example only when you ask, or which branch they start from, say so in the task or in [project instructions](#write-project-instructions).

### See what needs you in Overview

The **Overview** pane beside the conversation tracks the project's threads. It's already open the first time you open a new project. The **Overview** button in the project header closes and reopens it, and shows a dot when a thread is waiting on you.

In the desktop app, you also get a desktop notification when Claude posts in the conversation, a thread hits an error, or a thread needs your input, so you don't have to keep the project open to find out. To also get one each time a thread finishes a turn, or to turn them off for a project, choose **Notifications** in the project's sidebar menu. These notifications are desktop-only: in a browser, check the dot on the **Overview** button.

The pane's **Threads** tab groups threads by state:

| Group                | What's in it                                                                                                                                                                                                           |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ready for review** | Threads whose pull request is open and awaiting review                                                                                                                                                                 |
| **Waiting on you**   | Threads that need your reply or approval, or that failed                                                                                                                                                               |
| **Working**          | Threads still running                                                                                                                                                                                                  |
| **Landing**          | Threads whose pull request is approved or queued to merge                                                                                                                                                              |
| **Idle**             | Threads that finished and aren't waiting on anything                                                                                                                                                                   |
| **Resolved**         | Threads marked done: by you from the thread's menu, by Claude once you've taken the last step, such as merging its pull request, or automatically after a week with no activity. You can reopen one from the same menu |

The pane's other tabs are **Library** for the files and folders you added and the files threads produced, **Pull requests** once threads have opened any, and **Routines** for the [routines](/docs/en/routines) Claude set up from this project.

### Open a thread when you need control

Click a thread's card in the conversation or its row in **Overview** to open its transcript in the Overview pane. From there you can:

* Read what Claude did, step by step.
* Steer the task by writing in the thread's own message box. A message there goes straight to that thread, while a follow-up in the project conversation reaches it only when Claude matches the follow-up to that thread.
* Answer a permission prompt the thread is waiting on.
* Interrupt the thread with **Stop**, which replaces the send button while the thread is working, or by pressing Esc.

### Choose models and let Claude manage context

Set models and effort in **Project settings > General**. A new project runs Opus everywhere, with high [effort](/docs/en/model-config#adjust-effort-level) for threads and low effort for the conversation:

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

Claude saves preferences like these to [project memory](#give-a-project-standing-context) on its own and follows them in later threads. They're instructions Claude keeps to, not enforced settings, so a thread limit you give this way isn't a hard cap. Add one to project instructions when you want it worded exactly and applied to every thread from the start.

### Unblock a thread waiting on approval

Threads run in [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) when the thread's model supports it, so most tool calls run without asking you. When a thread needs your approval, the prompt is inside that thread and the thread waits until you answer it there. Telling Claude in the project conversation to go ahead doesn't reach it.

Each approval covers that prompt, or the rest of that thread if you choose the broader option. To let every thread run certain commands without asking, or to block some, add [permission rules](/docs/en/permissions) to the repository's `.claude/settings.json`. Threads apply them only in a project with one repository; see [What threads pick up from your repositories](#what-threads-pick-up-from-your-repositories).

## Give a project standing context

Project memory, project instructions, and the project's repositories, files, and environment carry context across threads. You set each one once and it applies to every new thread.

| Context                              | What it carries                                                                                                                                                                                                 | How you set it                                                                                                                                                                                                  |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project memory                       | Notes Claude keeps about the project, such as requirements, decisions, and pitfalls, stored as files. Every thread reads the index file `MEMORY.md` when it starts and opens the other files when it needs them | Ask Claude in the project conversation or any thread to remember a requirement, a decision, or a pitfall, or to forget one. Read, edit, and delete the files in **Project settings > Memory**                   |
| Project instructions                 | Text sent to each new thread and to Claude in the project conversation, up to 16,000 characters. [Write project instructions](#write-project-instructions) covers what to put in it                             | **Project settings > Memory > Project instructions**, or ask Claude to change the instructions                                                                                                                  |
| Repositories, files, and environment | The repositories every thread clones, the folders and files every thread can read under `/mnt/project-files`, and the cloud environment threads run in                                                          | Repositories and environment in **Project settings > Environment**, or ask Claude in the conversation to add a repository to the project. Files and folders from **Add** on the **Library** tab in **Overview** |

**Project settings > Memory** lists these files under **Auto memory**, because Claude writes them itself as it works in the project. They're separate from the [auto memory](/docs/en/memory) Claude Code keeps on your machine, even though both use a `MEMORY.md` index. Project memory is also separate from the `CLAUDE.md` files in the project's repositories. Each thread still reads those `CLAUDE.md` files from its clone when it starts, so put instructions about a repository in its `CLAUDE.md` and notes about the project in project memory.

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

Rules about one repository, such as its build commands, belong in that repository's `CLAUDE.md`, which every thread reads when the repository is part of the project. Once work is underway, when you correct a thread, also tell Claude to remember the correction: it goes into [project memory](#give-a-project-standing-context) and later threads start with it.

### Decide which repositories to add

The repositories you add to a project come with everything in them, their code, `CLAUDE.md`, and skills, in every thread. Repositories you don't add are still within reach: a thread can add one to itself when its task needs it. Most projects use both:

* **Add it to the project**, in the **New project** dialog, in **Project settings > Environment**, or by asking Claude in the conversation to add it to the project. Every thread from then on clones it and starts with its `CLAUDE.md` and skills loaded, whether or not the task touches it. Going from one repository to several also changes what threads take from each repository's `.claude/settings.json`; see [What threads pick up from your repositories](#what-threads-pick-up-from-your-repositories).
* **Leave it off and let threads add it when needed.** A thread whose task needs a repository the project doesn't have can add it to itself, and a note in the thread says it was added to this thread only. The clone happens partway through the task, so that repository's `CLAUDE.md` and skills weren't there when the thread started. The next thread starts without it again. A repository a thread adds needs the same [prerequisites](#check-the-prerequisites) as a project repository: the Claude GitHub App installed on it and push access from your GitHub account.

A project doesn't need a repository at all. Its threads can still research, write documents, and write and run code in their own sandbox, and they deliver files to the **Library** tab. A thread there can also add a repository to itself when a task calls for one.

Once the project has repositories, Claude can only add repositories from a GitHub owner the project already uses, whether it adds one to the project or a thread adds one to itself. To bring in a repository from a different owner, add it to the project yourself in **Project settings > Environment**.

For a project that spans many repositories, such as one feature with server, web, mobile, and desktop code, add the one or two repositories nearly every task touches and name the others in [project instructions](#write-project-instructions) so Claude knows where the rest of the code lives. Threads then start small and pull in the other repositories only for the tasks that need them.

### What threads pick up from your repositories

Each thread clones every repository in the project and loads `CLAUDE.md`, skills, and plugins from all of them. Permission rules, hooks, and `env` come only from the `.claude/settings.json` in the directory the thread starts in: inside the repository when the project has one, and above the clones when it has several, where no repository's file is read for them.

| In each repository                                                    | One repository                                                                                                                      | Several repositories                                                                                                                        |
| :-------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `CLAUDE.md`                                                           | Loaded when the thread starts                                                                                                       | Loaded from every repository when the thread starts                                                                                         |
| Skills, agents, and commands under `.claude/`                         | Loaded                                                                                                                              | Loaded from every repository                                                                                                                |
| Plugins enabled in `.claude/settings.json`                            | Loaded                                                                                                                              | Loaded from every repository. If two repositories disagree about a plugin, set it in **Project settings > Plugins**, which takes precedence |
| Permission rules, hooks, and `env` defined in `.claude/settings.json` | Apply to the thread, except the `env` keys that [no cloud session honors](/docs/en/cloud-environments#what-carries-over-from-your-setup) | Don't apply                                                                                                                                 |

In a project with several repositories, each clone is attached to the thread as an [additional directory](/docs/en/memory#load-from-additional-directories) with `CLAUDE.md` loading turned on, which is why every repository's `CLAUDE.md` and skills load at start even though the thread starts above them. In either case, hooks that an enabled plugin provides still run, since plugins load from every repository. In a project with several repositories, put standing rules in project instructions and give threads environment variables through the [cloud environment](#choose-an-environment-for-threads).

### Choose an environment for threads

Every new thread starts in the project's [cloud environment](/docs/en/cloud-environments). The environment sets which domains threads can reach, which environment variables they have, which API credentials are added to their requests, and what the setup script installs before Claude starts. Threads use a default Anthropic-hosted environment until you pick one in **Project settings > Environment**.

If threads need to reach an internal API or a private package registry, or need a token your machine normally holds, change the environment rather than the project: see [Network access](/docs/en/cloud-environments#network-access), [Add API credentials](/docs/en/cloud-environments#add-api-credentials), and [Setup scripts](/docs/en/cloud-environments#setup-scripts).

### Get skills, plugins, connectors, and tools into threads

Threads are cloud sessions, so they don't have the skills, MCP servers, plugins, and tools installed only on your machine. To make each of these available to threads:

* Skills, subagents, and commands: commit them to a repository you added to the project, for example a skill at `.claude/skills/<skill-name>/SKILL.md`. Each thread clones every repository in the project and loads `.claude/skills/`, `.claude/agents/`, and `.claude/commands/` from each of them, so a skill committed to one repository is available in every new thread. Threads also load the skills you enable for your claude.ai account.
* Plugins: add them in **Project settings > Plugins**; they load into each new thread. Plugins that a repository declares in its `.claude/settings.json` load too; see [What carries over from your setup](/docs/en/cloud-environments#what-carries-over-from-your-setup).
* MCP servers: threads get their MCP tools from the connectors on your claude.ai account, which are MCP servers you connect once at [claude.ai/customize/connectors](https://claude.ai/customize/connectors) or through the **Manage connectors** link in **Project settings > Environment**. Every thread can use all of them with no per-project setup. The project conversation itself has no connectors, so send work that needs one as a task for a thread. In a project with one repository, threads also load MCP servers from that repository's [`.mcp.json`](/docs/en/cloud-environments#what-carries-over-from-your-setup). [How connectors reach Claude Code](/docs/en/mcp#how-connectors-reach-claude-code) lists the rules for cloud sessions and the settings that turn connectors off.
* Command-line tools and packages: install them in the environment's [setup script](/docs/en/cloud-environments#setup-scripts).

To see which connectors a running thread has at claude.ai/code, open the thread and select **Connectors** from the **+** menu beside its message box. Turning a connector off there removes it from that thread and saves that as your account default, so new threads and claude.ai chats start without it until you turn it back on. A thread picks up a connector you add or reconnect after the next message you send it.

## Project settings reference

You change project settings at claude.ai/code or in the desktop app, not in `settings.json`. Open **Project settings** from **Settings** in the project's sidebar menu or from the gear icon in the project header.

Settings save as you change them; a text field you're editing, such as the goal or instructions, shows **Save changes** and **Discard** until you leave it. Changes to instructions, repositories, plugins, and environment in **Project settings** reach new threads, not threads already running.

| Setting                      | Section     | What it controls                                                                                                    |
| :--------------------------- | :---------- | :------------------------------------------------------------------------------------------------------------------ |
| Name, icon, and goal         | General     | The project's name and icon in the sidebar, and its one-line goal                                                   |
| Coordinator model and effort | General     | The model and [effort level](/docs/en/model-config#adjust-effort-level) for Claude in the project conversation           |
| Thread model and effort      | General     | The model and effort level for threads                                                                              |
| Project instructions         | Memory      | [Standing rules](#give-a-project-standing-context) every new thread receives                                        |
| Project repositories         | Environment | The repositories new threads clone                                                                                  |
| Cloud environment            | Environment | The [cloud environment](#choose-an-environment-for-threads) new threads run in                                      |
| Connectors                   | Environment | A link to manage the claude.ai connectors threads get                                                               |
| Plugins                      | Plugins     | The plugins that load into each new thread                                                                          |
| Usage                        | Usage       | [Token use](#usage-and-cost) by thread and by model                                                                 |
| Memory                       | Memory      | The project's [memory files](#give-a-project-standing-context)                                                      |
| Restart Claude               | General     | Restarts the project conversation when [Claude stops responding there](#claude-hasnt-responded)                     |
| Pause, Archive, Delete       | General     | Stops, hides, or removes the project; see [Pause, archive, or delete a project](#pause-archive-or-delete-a-project) |

### Pause, archive, or delete a project

All three controls are at the bottom of **Project settings > General**:

* **Pause**: stops everything at once. Every running thread and the conversation are interrupted, no new threads start, routines don't run, and the project doesn't accept messages until you resume it. Click **Resume** in the same place or on the banner above the project's message box; a paused thread continues when you send it a message after that.
* **Archive**: hides the project from the sidebar and archives its threads, which stops any thread that was running or watching a pull request. Routines in the project don't run while it's archived. To bring the project back, open it from the Projects page and click **Unarchive**. Its threads stay archived until you unarchive them individually from the session list.
* **Delete**: permanently removes the project along with its threads, its memory, and its files, and turns off the project's routines. This can't be undone. Branches and pull requests the threads pushed to GitHub aren't affected.

## Usage and cost

Project usage counts against the same [plan limits](/docs/en/errors#youve-hit-your-session-limit) as your other Claude Code sessions, and a project can't spend past those limits on its own.

A thread that reaches your plan's limit waits and continues on its own when the limit resets, so work you left running starts using your next usage window without a message from you. [A thread hit the usage limit](#usage-limit-reached) covers what you see, how to stop it, and the one case that doesn't wait.

Work goes past your plan's limits only if you have turned on [usage credits](/docs/en/costs#add-usage-credits-to-your-subscription) for your account. A thread can't turn them on for you.

### What draws on your plan

A project uses your limits faster than a single session does, and on a Pro plan in particular you should expect to reach your limit sooner on days you run one. These are the parts of a project that use your plan:

* **Running threads**: each is a full session, and several can run at once. There's no fixed number; Claude starts as many as the work calls for, and a limit you [ask for](#tune-how-claude-runs-a-project) is a preference rather than a cap. The enforced limit is 200 new threads per day across your projects.
* **The conversation**: Claude uses tokens of its own reading what threads report and deciding what to do next.
* **Threads watching a pull request**: an idle thread wakes up and uses your plan again when CI fails or a review comment arrives on its pull request. To stop that, ask in the thread for it to stop watching the pull request.

A project with no running threads, no watched pull requests, and no new messages doesn't use your plan while it sits idle, and neither does an archived project.

### See and reduce a project's usage

Open **Usage** in **Project settings** to see token use by thread and by model, and how much went to the project conversation. To bring it down:

* A follow-up routed to a thread that has been idle longer than the [cache lifetime](/docs/en/prompt-caching#cache-lifetime), an hour on Pro and Max within your plan's limits, re-reads that thread's whole conversation before doing anything. For new work, asking Claude to start a fresh thread can use less than reviving a large old one.
* For work that doesn't need the largest model, [choose a smaller model or a lower effort level](#choose-models-and-let-claude-manage-context) for threads, the conversation, or both.
* Ask Claude in the project conversation to run fewer threads at a time, or to answer small questions itself instead of starting a thread.

## How projects relate to other Claude Code features

Several Claude Code features let more than one session work at the same time, so running work in parallel is not by itself what a project is for. In a project, Claude starts and tracks the sessions instead of you, each one starts from the same repositories, instructions, and memory, and the work lives in the cloud for as long as it lasts. This is how each neighboring feature connects to a project:

* **Claude Tag**: [Claude Tag](https://claude.com/docs/claude-tag/overview) is Claude in your team's Slack channels, on Team and Enterprise plans. Anyone in a channel can give it work, everyone in the channel sees and steers it, and it uses connections an admin set up for that channel. A project is yours alone: you're the only one who sends it work or sees its threads, it uses your own GitHub access and connectors, and it's on Pro and Max. [How Claude Tag differs from Cowork and Claude Code](https://claude.com/docs/claude-tag/concepts/how-it-works#how-claude-tag-differs-from-cowork-and-claude-code) has the side-by-side.
* **Cloud sessions**: every thread is a [cloud session](/docs/en/claude-code-on-the-web), started and tracked by Claude instead of by you. A cloud session you started yourself can become a project or feed one through [**Continue as a project** or **Move to project**](#start-from-an-existing-cloud-session).
* **Routines**: when you ask for scheduled work in a project, Claude creates a [routine](/docs/en/routines) that runs as threads in that project and appears on its **Routines** tab. Routines you create outside a project keep working on their own.
* **Local sessions and agent view**: sessions in your terminal, IDE, or the desktop app's local environment run on your machine and can't be part of a project. [Agent view](/docs/en/agent-view) is a screen for tracking several of those local sessions; it has no coordinator.
* **Worktrees**: a [worktree](/docs/en/worktrees) gives each local session its own working copy of a repository so parallel sessions on your machine don't overwrite each other. Threads don't need them: each thread clones its repositories into its own cloud sandbox and works on its own branch.
* **Agent teams**: an [agent team](/docs/en/agent-teams) is one session that starts teammate sessions for a single task, on your machine or inside a cloud session, and ends with that task.
* **Projects in claude.ai chat and Cowork**: the [earlier Projects experience](https://support.claude.com/en/articles/9517075-what-are-projects), which groups conversations and reference files without threads or a coordinator. Those projects keep working as they do today until the redesigned experience reaches them.

[Run agents in parallel](/docs/en/agents) compares these options side by side.

## Limitations

* Projects are available at claude.ai/code, in the desktop app, and in the Claude mobile app, not in the terminal CLI or through Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. The CLI's [`claude project`](/docs/en/cli-reference) command, which manages local Claude Code state for a directory, is unrelated.
* Project threads are [cloud sessions](/docs/en/claude-code-on-the-web) with Anthropic as the model provider. [Security](/docs/en/security) and [Data usage](/docs/en/data-usage) cover how cloud sessions are isolated and what's retained.
* A local session can't be part of a project.
* A thread's sandbox pauses between turns and resumes when the thread continues. If the sandbox can't be resumed, the thread continues from a fresh clone, so uncommitted changes can be lost. On long tasks, ask Claude to commit and push work in progress.
* A project belongs to one user. You can't share a project or its threads with another user, and thread transcripts don't have the share option other cloud sessions have. There are no organization-level controls for projects during the beta.
* A thread belongs to the one project that started it. You can't move or copy a thread to another project, or move it out to stand alone. [**Move to project**](#start-from-an-existing-cloud-session) goes the other way only: it brings a cloud session's work into a project.

## Troubleshooting

For the GitHub setup prompts in the **New project** dialog, see [Set up GitHub access](#set-up-github-access).

### A thread looks stuck

Claude doesn't post each step a thread takes, so a thread that shows as running with no new messages in the project conversation is usually still working. A new thread also provisions its [cloud environment](/docs/en/cloud-environments) before Claude begins, so its first update takes a moment. Open the thread to read its transcript. If the thread is waiting on a permission prompt, answer it there.

### Threads guessed or stalled instead of asking

When several threads come back having assumed something wrong, worked around missing access, or stopped with "blocked", the cause is usually the same gap in the project's setup rather than a problem with each task. Sort out which threads are sound before you fix anything:

1. Ask Claude in the conversation: "For every open thread, list what you asked it to do, what it assumed or couldn't reach, and what it's waiting on." Claude reads each thread and answers in the conversation.
2. For threads that started from a wrong assumption, open the thread from **Overview** and mark it resolved from its menu, or tell it what to do instead in its message box. Its branch and any pull request stay on GitHub until you delete them.
3. Fix the gap once, in [project instructions](#give-a-project-standing-context) or the [environment](#choose-an-environment-for-threads), then send one thread before sending the rest of the work again as new threads.

<h3 id="claude-hasnt-responded">
  Claude hasn't responded
</h3>

The project conversation shows a "Claude hasn't responded" banner when Claude is running but its replies aren't reaching the project. Click **Restart Claude** on the banner, or go to **Project settings > General** and click **Restart** in the **Restart Claude** row. Claude reconnects to the conversation; any reply it was in the middle of writing is lost, and threads aren't affected.

<h3 id="repository-access-errors">
  Repository access errors
</h3>

Three messages mean a thread or the project can't reach one of its repositories. A project thread needs the [GitHub prerequisites](#check-the-prerequisites) even when your other cloud sessions clone the same repository without trouble.

* **"Couldn't start the session — Claude doesn't have GitHub access to this project's repository"**, reported before the thread starts, when the Claude GitHub App isn't installed on that repository, is suspended, or isn't linked to the GitHub account you connected.
* **"Unable to access your repository"**, reported by a thread when its clone fails: GitHub rejected the clone, the repository wasn't found under the name the project has, or the branch the thread was asked to start from doesn't exist.
* **"Claude can't access" a repository**, shown when you save repositories in the **New project** dialog or **Project settings**. The message continues with an install link and a reconnect link. Use the install link if the Claude GitHub App isn't on that repository, and the reconnect link if it is, since the GitHub App can be installed on GitHub without being linked to the account you connected to Claude. If the message says the GitHub App is suspended or doesn't include this repository, follow its link to GitHub to fix that.

To fix any of them, click the button the message offers, such as **Install GitHub App** or **Select repositories on GitHub**, then **Check again**. When the block is on the GitHub organization's side, such as an owner who hasn't approved the app or an IP allow list that excludes Claude, the message shows a **See how to fix** link instead. If there's no button, follow [Set up GitHub access](#set-up-github-access), then send another message to retry.

<h3 id="usage-limit-reached">
  A thread hit the usage limit
</h3>

When a thread or the project conversation reaches your plan's five-hour or weekly limit, it keeps retrying on its own and continues when the limit resets. While it waits, the thread shows **Service is busy** with "Claude is still retrying and will continue automatically." You don't need to do anything for the work to continue. If you'd rather it not use your next usage window, click **Stop** in the thread, or [pause the project](#pause-archive-or-delete-a-project) to hold every thread. A thread that a routine started doesn't wait: its turn stops with a limit error, and you send it a message after the limit resets.

[Usage limit errors](/docs/en/errors#youve-hit-your-session-limit) explain the limits and when they reset.

<h3 id="additional-usage-credits-are-required">
  Additional usage credits are required
</h3>

A thread or the project conversation made a request your plan covers only with usage credits, such as one to a model or context size your plan doesn't include, and usage credits aren't turned on for your account. [Add usage credits to your subscription](/docs/en/costs#add-usage-credits-to-your-subscription) covers who can turn them on or buy them on each plan. Once credits are available, send another message to retry.

<h3 id="context-limit">
  Other messages
</h3>

These messages name their own cause. The table gives the next step for each.

| Message                                                                                        | What to do                                                                                                                                                                                                                |
| :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "Unable to connect to repository" with "Claude couldn't reach GitHub to fetch your repository" | Wait a moment, then send another message to retry                                                                                                                                                                         |
| "Unable to connect to repository" with "Claude couldn't access your repository or environment" | Your GitHub account needs push access to the repository, and the environment must still exist. Check both in **Project settings > Environment**, then retry                                                               |
| "Couldn't show the setup proposal"                                                             | The app you have open is older than the **Setup recommendations** Claude sent. Refresh the page or restart the desktop app, or ask Claude to propose the setup again                                                      |
| "The project's environment was removed"                                                        | Choose a different environment in **Project settings > Environment**; the change applies to new threads                                                                                                                   |
| "Setup script failed"                                                                          | Click **Edit setup script** on the error, fix the script in the environment, then send another message. [Setup script failed](/docs/en/web-quickstart#setup-script-failed) lists common causes                                 |
| "Claude ran out of context on this turn"                                                       | The thread filled its context window. If the message says the thread continues in a fresh session, it carries on by itself; otherwise ask Claude in the project conversation to start a new thread for the remaining work |
| "Reached the turn limit"                                                                       | The thread reached the cap on agentic turns that [`CLAUDE_CODE_MAX_TURNS`](/docs/en/env-vars) sets. Send another message to continue, or raise or remove that variable where it's set                                          |

## Related resources

* [Use Claude Code in the cloud](/docs/en/claude-code-on-the-web): how the cloud sessions behind each thread work, including GitHub access options and auto-fix on pull requests
* [Configure cloud environments](/docs/en/cloud-environments): change what threads can reach on the network, give them environment variables and API credentials, and install tools with a setup script
* [Automate work with routines](/docs/en/routines): schedules, triggers, and management for routines, including the ones Claude creates from a project
* [Manage multiple agents with agent view](/docs/en/agent-view): run and track several sessions on your own machine when the work needs tools or services only your machine can reach
* [Projects redesigned: from folder to conversation](https://claude.com/blog/projects-redesigned): the launch announcement, with the thinking behind making a project a conversation with Claude
