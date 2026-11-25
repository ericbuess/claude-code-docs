> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Share a cloud or Remote Control session

> Check what recipients of a shared Claude Code session can read, choose who can open the link, and stop sharing.

You can share a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md) or a [Remote Control](https://code.claude.com/docs/en/remote-control.md) session with a link so that other people can read the conversation.

> [!NOTE]
>
> To share a claude.ai chat, see [Share and unshare chats](https://support.claude.com/en/articles/10593882-share-and-unshare-chats).

## What recipients see

When you share a cloud or Remote Control session, recipients see the conversation so far, with Claude's tool calls and their results, including content such as:

* **Messages**: your prompts, images you added, the names of files you attached, and Claude's replies and thinking
* **Code and commands**: file contents that Claude read, wrote, or edited, and commands that you or Claude ran, with their output
* **Credentials**: keys or tokens that appear in a message, a file, or command output
* **Other repositories**: results of Claude's GitHub searches, which can include private repositories that recipients can't open
* **Connector results**: what a [connector](https://code.claude.com/docs/en/mcp.md#use-mcp-servers-from-claude-ai) returned, such as emails, documents, and Slack messages
* **Web content**: pages that Claude read and screenshots it took
* **Your setup**: names of connectors Claude used, and names and descriptions of any connectors, [skills](https://code.claude.com/docs/en/skills.md), and [plugins](https://code.claude.com/docs/en/plugins/overview.md) it looked up

Your display name appears on the shared session. On a Max, Ultra, or Pro plan, you can [hide it](#share-from-a-max-or-pro-account).

A recipient's view doesn't update in real time. When they reload the page or open the link again, they see messages added to the session after you shared, until you [stop sharing](#stop-sharing-a-session).

### What recipients see in a Remote Control session

When you share a Remote Control session, recipients can also see:

* The contents of files Claude read on your computer during the session, including files outside the folder you started the session in
* Text and screenshots of pages Claude opened during the session through the [Claude in Chrome extension](https://code.claude.com/docs/en/chrome.md), including sites where you're signed in

## Share a session

[Check the session](#check-a-session-before-you-share) first. Then select **Share** at the top of the session, choose **Team** or **Public**, whichever your plan offers, select **Copy link**, and send the link.

### Check a session before you share

Read the conversation, expand the tool calls, and look for the content listed in [What recipients see](#what-recipients-see). If the conversation holds something recipients shouldn't see, keep the session **Private**.

The server [blocks sharing in some cases](#unshareable-sessions), but a session it lets you share can hold sensitive content.

### Share from an Enterprise or Team account

On Enterprise and Team plans, other members of your claude.ai organization may be able to open a session you share:

* **Visibility options**: **Private** and **Team**
* **Repository access**: to open a cloud session you shared, recipients need access to each of its private repositories through their [connected GitHub account](https://code.claude.com/docs/en/web-quickstart.md#connect-github). Members without repository access may be able to open a Remote Control session's link.

### Share from a Max, Ultra, or Pro account

On Max, Ultra, and Pro plans, anyone who has the link and is signed in to claude.ai may be able to open a session you share:

* **Visibility options**: **Private** and **Public**
* **Repository access**: **Require repository access** is off by default. Turn it on to limit the cloud sessions you share to recipients with access to each session's private repositories. People without repository access may be able to open a Remote Control session's link.

To turn on **Require repository access** or turn off **Show your name**, go to [**Settings > Privacy**](https://claude.ai/settings/data-privacy-controls) on claude.ai and click **Manage** next to **Shared Code sessions**.

## Stop sharing a session

To stop sharing a session you shared, set its visibility back to **Private**. Do this before you move on from a session or an organization, because the link keeps working after you:

* Archive the session
* Turn off Remote Control or close your terminal
* Leave or are removed from the organization, for a link you shared as **Team**

For what ends a link without you setting it to **Private**, see [Links that stop opening](#links-that-stop-opening).

## Troubleshoot sharing

You can't share a session when your organization has turned sharing off or the server refuses that session. A link can also stop opening after you share it.

### Sharing is turned off for your organization

If **Share** is dimmed with "Sharing is disabled by your organization.", ask an [Owner](https://code.claude.com/docs/en/server-managed-settings.md#access-control) to turn on **Share cloud sessions** in [**Organization settings > Data and privacy**](https://claude.ai/admin-settings/data-privacy-controls). You need this setting on to share Remote Control sessions too.

Under some compliance configurations, you can't share sessions even with the setting on.

### Sessions you can't share

You can't share some sessions because they may hold content that recipients shouldn't see. If sharing fails with a message such as "This session can't be shared.", trying again doesn't help.

For example, on Enterprise and Team plans, you can't share a cloud session that uses [uploaded code](https://code.claude.com/docs/en/claude-code-on-the-web.md#send-local-repositories-without-github), because there's no way to check who's allowed to see that code. To share work on that code, start a new session whose repository is on github.com and wasn't uploaded.

### Links that stop opening

If recipients can't open a link, check for these causes:

* **Visibility**: the session is **Private**, or the recipient isn't signed in to claude.ai or is outside your organization on a **Team** link. Check [who can open the link](#share-a-session).
* **Repository access**: the link [requires repository access](#share-a-session), and the recipient's GitHub account can't read the repository. Ask them to [connect an account](https://code.claude.com/docs/en/web-quickstart.md#connect-github) that can.
* **Uploaded or non-GitHub code**: the link requires repository access, and the code was [uploaded](https://code.claude.com/docs/en/claude-code-on-the-web.md#send-local-repositories-without-github) or is on a Git host such as GitLab or Bitbucket. Share from a session whose repository is on github.com and wasn't uploaded.
* **Invalid link**: the share link may not match the address in your browser, and a **Public** link changes when you stop sharing and share again. Copy the current link from **Share** and send it.
* **Organization setting**: [**Share cloud sessions** is off](#sharing-is-turned-off-for-your-organization) for the organization. Ask an Owner to turn it back on.
* **Upgraded plan**: you shared a **Public** link, then upgraded your plan to Team or Enterprise. The link follows the rules for [Enterprise and Team accounts](#share-from-an-enterprise-or-team-account).
* **Downgraded plan**: you shared a **Public** link, then moved to the Free plan. [Upgrade](https://claude.ai/upgrade) to a Max, Ultra, or Pro plan, and the same link opens with no further step.

You can't restore the link in these cases:

* The session was deleted
* The session became [one you can't share](#unshareable-sessions)
* You shared a **Public** link, then [moved your personal account](https://support.claude.com/en/articles/9267400-move-your-personal-claude-account-to-a-team-or-enterprise-organization) into an existing organization
* Anthropic turned off the link, for example after an abuse or copyright review. The session shows as **Private**, and sharing it again fails with "Couldn't share this session. Try again."

## Related resources

* [Use Claude Code in the cloud](https://code.claude.com/docs/en/claude-code-on-the-web.md): archive, delete, and move cloud sessions
* [Remote Control](https://code.claude.com/docs/en/remote-control.md): continue a local session from another device
