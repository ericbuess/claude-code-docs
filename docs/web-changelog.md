> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on the web changelog

> Release notes for Claude Code on the web, Remote Control, and Claude Tag in Slack, listing new features, improvements, and bug fixes by date.

This page lists changes by date for [Claude Code on the web](/docs/en/claude-code-on-the-web), [Remote Control](/docs/en/remote-control), and [Claude Tag](/docs/en/claude-tag), which brings Claude into your Slack channels. For changes that ship in a Claude Code CLI release, see the [Claude Code changelog](/docs/en/changelog).

<Update label="September 8, 2026">
  **Claude Code on the web**

  * Fixed GitHub Enterprise Server sessions reporting your GitHub account as not connected after its token expired. Pull request and issue lookups, merges, and reviews now refresh the token automatically.
  * Fixed `gh` and GitHub API calls from cloud sessions failing in organizations that haven't installed the Claude GitHub App. These calls now use your connected GitHub account, and the error message tells you when no account is connected.

  **Claude Tag**

  * Fixed Claude replying "The API rejected the request as invalid" when your organization has run out of usage credits. The reply now begins "This organization is out of usage credits for Claude Tag" and says how to add credits and retry.
  * Fixed requests in a thread to edit or delete a message that Claude posted at the channel's top level. The request now reaches the channel's own session, which posted the message, instead of Claude posting a correction in the thread.
  * Fixed **Connect** on **Tool access for Claude Tag** requests under **Admin settings > Review requests** failing with "Authorization failed" or showing the requested [access bundle](https://claude.com/docs/claude-tag/concepts/glossary#access-bundle) as deleted.
  * Added a **Use a custom connector** link to the preset connection forms in Claude Tag admin settings, so you can switch to a custom connection without starting over.
</Update>
