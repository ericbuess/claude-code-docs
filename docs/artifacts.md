> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Share session output as artifacts

> Artifacts turn Claude Code's work into live, interactive pages on claude.ai that you can keep private, share with your organization, or publish to a public link.

<Note>
  Artifacts are available on Pro, Max, Team, and Enterprise plans and require a session signed in with [`/login`](/docs/en/setup#authenticate). See [Availability](#availability) for the full set of requirements.
</Note>

An artifact is a live, interactive web page that Claude Code publishes from your session to a private URL on claude.ai. You open it in a browser, and it updates in place as the session continues. Share it from the page header when you want someone else to see it too.

<Frame>
  <img src="https://mintcdn.com/claude-code/kaHIYYMIYMYPxQg9/images/artifacts-viewer.png?fit=max&auto=format&n=kaHIYYMIYMYPxQg9&q=85&s=dbfd671cdb0d15f49f808b9e89778fe1" alt="An artifact open in a browser at claude.ai/code/artifact. The viewer header shows the artifact title acme-funnel-fix, a Share button, and the author avatar. The Share menu is open with the Always share latest version toggle, a version picker reading Sharing version 2, an Everyone at Acme audience selector, and a Copy link button. Below the header, the artifact page shows two mobile mockups side by side, a funnel chart, and a row of metric cards." width="2511" height="1890" data-path="images/artifacts-viewer.png" />
</Frame>

## When to use an artifact

Use an artifact when terminal text is the wrong medium for what Claude produced: output that is easier to look at and interact with than to read line by line. Claude builds the page from anything your session can reach, including your codebase and data it pulls through your [connected tools](/docs/en/mcp), so the page can show things that would take paragraphs to describe. For example, ask Claude to:

* Walk a reviewer through a pull request with annotated diffs
* Render a dashboard from data the session already pulled
* Lay out several design or implementation options side by side
* Keep an investigation timeline that fills in while a long task runs
* Send a teammate a link instead of pasting output into Slack
* Publish a status board that [pulls fresh data through MCP connectors](#pull-live-data-with-mcp-connectors) each time someone opens it

See [What you can build](#what-you-can-build) for prompts that match these, and [Pull live data with MCP connectors](#pull-live-data-with-mcp-connectors) for the connector-backed board's prompt.

### What an artifact is not

An artifact is a capture of work: one self-contained page with no backend, so it can't store form input or serve multiple routes, and its only path to outside data when someone views it is [calling MCP connectors](#pull-live-data-with-mcp-connectors). For a hosted internal tool with a backend, deploy it on your own infrastructure instead. See [Page constraints](#page-constraints) for the full set of limits.

## Create an artifact

Claude may publish an artifact on its own when the output suits a page, or you can ask for one directly. To ask, name the feature or describe the visual output you want in plain language. A good candidate is anything easier to see than to read as text, such as an annotated diff, a chart, or a set of options to compare. The prompts below are two examples; see [What you can build](#what-you-can-build) for more patterns.

```text wrap theme={null}
Make an artifact that walks through this PR with the diff annotated inline.
```

```text wrap theme={null}
Build a dashboard artifact of last week's deploy failures by service and keep it updated as you investigate.
```

Unless you name a location, Claude writes the page to an HTML or Markdown file in a temporary directory outside your project, then publishes it. Publishing a new artifact goes through your session's [permission mode](/docs/en/permission-modes):

* **Auto mode**: the classifier reviews the publish instead of prompting you, so Claude can publish a page without you seeing a prompt. Which mode your sessions start in depends on your plan; see [the starting permission mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode).
* **Manual and Accept edits modes**: Claude Code asks for permission; it might say something like `Claude wants to publish deploy-failures.html, uploading it to claude.ai (Anthropic's servers) to host as the page "Deploy failures by service", private to you until you share it`. Select **Yes** to publish.

After you approve an artifact once, Claude Code republishes it without asking, and asks again in some cases, including when:

* Claude declares a runtime capability for the page, such as [connector calls](#pull-live-data-with-mcp-connectors)
* You have since [shared it publicly](#share-an-artifact)
* You have since shared it with specific people or your organization with the latest version chosen as the version viewers see

After the first publish, Claude prints the URL, and your browser opens to the new page. Press `Ctrl+]` at any time to reopen the most recent artifact from the terminal.

Claude picks the artifact's title and an emoji for its browser-tab icon. Both appear in your [gallery of artifacts](#share-an-artifact) on claude.ai and in shared links, so ask Claude to use a specific title or icon if you want one.

To stop the browser from opening automatically when a new artifact is published, set `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` in your environment.

If Claude responds that it cannot publish, or writes a local HTML file without a link, the tool is not enabled for your session. Check the [Availability](#availability) requirements.

## Update an artifact

Ask Claude to revise the page, or let a long-running task republish as it makes progress. Claude edits the underlying file and publishes again to the same URL.

```text wrap theme={null}
Add a per-region breakdown below the summary chart and republish.
```

Anyone with the page open sees the update in place. Each publish becomes a version, and from the **Share** control in the page header you can choose which version viewers see.

To update an artifact from a different session, give Claude its URL, or attach it with [`/artifacts`](#find-an-artifact-again). Without either, a new session creates a new artifact instead of updating one.

```text wrap theme={null}
Update https://claude.ai/code/artifact/5fbea6f3-... with today's numbers.
```

## Find an artifact again

Run `/artifacts` in Claude Code to list every artifact you own and every artifact shared with you. Select one and press `o` to open it in your browser or `c` to copy its link. Press `Enter` to attach it to the current session; before v2.1.216, `Enter` opened it in your browser. Claude Code reads the list from your claude.ai account, so it works in a new session and after `/clear`, when the link has scrolled out of the terminal. Requires Claude Code v2.1.208 or later.

## Share an artifact

A new artifact is visible only to you. To share it, open the artifact in your browser and use the **Share** control in the page header. The header also links to your gallery at [claude.ai/code/artifacts](https://claude.ai/code/artifacts), which lists every artifact you have created.

Viewers in your organization can see who published the page: on an artifact shared within your organization, your name is in the title menu, and on a public artifact it's in the page header for signed-in viewers in your organization. A viewer who opens a public link without signing in, or from outside your organization, sees the label `Content is user-generated and unverified.` instead of your name.

Who you can share with depends on your plan:

* **Within your organization**: on Team and Enterprise plans, grant access to specific people in your organization, or to everyone in it. Viewers sign in to claude.ai as members of your organization to see the page.
* **Publicly**: share a link that anyone on the internet can open, with no claude.ai sign-in required. On Pro and Max plans, a public link is the only way to share an artifact. On Team and Enterprise plans, public sharing is off until an Owner [enables it for the organization](#control-public-sharing).

### Let someone edit with you

People you share with are viewers by default: they see each version you publish but can't change the page. On Team and Enterprise plans, you can also make someone an editor. In the share dialog, add a person and switch their role from **viewer** to **editor**.

An editor publishes new versions the same way you [update the artifact from another session](#update-an-artifact): they give Claude the artifact's URL, or attach it from [`/artifacts`](#find-an-artifact-again), and Claude pulls the current content and republishes with their changes. Everyone with the page open sees each update live.

## Collect comments on an artifact

When you share an artifact within your organization, the people you share it with can leave comments on the page, and you can have Claude read those comments and reply to them. You need Claude Code v2.1.221 or later and a Team or Enterprise plan, because only an artifact you [share within your organization](#share-an-artifact) takes comments. Claude reads the comments in two cases:

* **You ask Claude to read them**: give Claude the artifact's URL and ask for the comments. Claude lists each thread and marks the comments someone who can edit the artifact sent to it.
* **Someone who can edit the artifact sends a comment to Claude**: in a thread on the page, they send a comment with **Send to Claude**, or mention `@claude` in one. Either way, they activate the thread.

Claude can reply to or resolve only an activated thread. Other threads stay open until a person resolves them on the page. Viewers see each reply attributed to Claude, via you.

If you share an artifact publicly, viewers can't comment on it: the page says `Comments aren't available while this Artifact is shared publicly.` To switch an artifact that already has comment threads to a public link, delete the threads first.

To ask for the comments yourself, give Claude the URL:

```text wrap theme={null}
Read the comments on https://claude.ai/code/artifact/5fbea6f3-... and make the changes the commenters ask for.
```

If Claude tells you it can't read comments, check three things:

* You're running Claude Code v2.1.221 or later.
* You're not in your first session since you installed Claude Code or upgraded from a version before v2.1.221. In that [first session after an install or upgrade](/docs/en/env-vars#first-session-after-an-install-or-upgrade), Claude might not be able to read comments yet; start a new session and ask again.
* You haven't turned feature-flag fetching off.

### Let Claude reply to comments on its own

After your session publishes an artifact, Claude Code watches that artifact for comments for as long as the session runs. When someone who can edit the artifact sends a comment to Claude, it reaches your session right away, and Claude can read the thread and reply without you asking.

You need Claude Code v2.1.228 or later. If you turned [feature-flag fetching](/docs/en/env-vars#features-that-need-feature-flag-fetching) off, Claude Code doesn't watch for comments.

Your [permission mode](/docs/en/permission-modes) decides what Claude does when a sent comment arrives:

* **Claude replies on its own**: when your permission mode lets Claude post the reply without asking you, Claude reads the thread and replies, and edits the artifact when the comment asks for a change. You see `Auto-replied to comment thread on Artifact: <name>` or `Auto-edited Artifact: <name> in response to a comment thread`.
* **Claude waits for you**: outside plan mode, when posting the reply would need your approval, you see `Comments are waiting on Artifact: <name>`. Claude then asks you for approval to read the thread, and again to post the reply.
* **Claude pauses in plan mode**: you see `Comments are waiting on Artifact: <name>`, and Claude doesn't reply until you leave plan mode and ask it to read and reply.

Claude also stops replying on its own to an artifact after it handles 60 sent comments or thread activations on that artifact within an hour. You see `Comments are waiting on Artifact: <name>` once, and Claude picks up again as that hour's comments age out.

Run `/tasks` to see each artifact your session is watching, listed as a live-updates task. You can stop Claude from replying on its own in any of these ways:

* **Press Ctrl+C once at an idle prompt**: Claude pauses replying on every artifact your session is watching. Replies start again after you send your next message.
* **Stop the task in `/tasks`**: Claude stops replying on that artifact until you ask it to resume replies there. Publishing the artifact again doesn't start replies again, and the stop still applies when you resume the session later.
* **Press `Ctrl+X Ctrl+K` twice within 3 seconds**: the chord that [stops every running background subagent](/docs/en/interactive-mode#general-controls) also stops Claude from replying on every artifact for the rest of the session. Asking Claude to resume replies doesn't undo this stop.

If the service that delivers comments becomes unavailable or stops answering, Claude Code keeps trying to reconnect for a while, then stops watching each artifact your session was watching.

## Pull live data with MCP connectors

An artifact can call [MCP connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) each time someone views it, so the page shows current data rather than a snapshot from the session that built it. Connector calls from artifacts are available on Pro, Max, Team, and Enterprise plans and require Claude Code v2.1.209 or later. On earlier versions, Claude publishes the page with whatever data the session gathered while building it.

To create a connector-backed page, name the connector and the data you want in your prompt:

```text wrap theme={null}
Build a dashboard artifact of our open pull requests that pulls the live list through my GitHub connector when the page loads.
```

Claude declares which connectors the page may call as part of publishing, and the page can't call connectors outside that declaration. Only connectors from your claude.ai account qualify: Claude names them in the declaration, and when someone views the page, each call [runs through the viewing account's own connection](#how-connector-calls-work-for-viewers) to that connector. Local MCP servers you configure in Claude Code, such as servers from `.mcp.json`, can supply data while Claude builds the page, but the published page can't call them.

The page fetches data when it loads and can refresh on an interval or when a viewer uses a refresh control on the page. Responses are cached in the viewer's browser, so a reopened page renders from the cached responses immediately, then updates with fresh results.

### How connector calls work for viewers

When a published page calls a connector, the call uses the account of the person viewing the page, not the account of the person who published it:

* **Each viewer uses their own connectors**: calls go through the viewing account's connected tools, so two people opening the same dashboard can see different data depending on what their accounts can access. The page never sees anyone's credentials; claude.ai makes the calls on the page's behalf.
* **Viewers approve access first**: claude.ai asks each viewer for permission before the page's first connector call. A viewer who declines, or who hasn't connected a connector the page uses, still sees the page without its live sections.
* **Actions use the viewer's account too**: a page can offer controls that invoke connector tools with side effects, such as posting a message or updating an issue. The action goes through the account of whoever selects the control.

When you plan to share a connector-backed page, ask Claude to include a fallback message in each live section that names the connector it needs. A viewer who's missing the connection then sees what to connect instead of an empty section.

An artifact that calls connectors can't be shared to a public link on any plan. On Team and Enterprise plans, you can keep it private or [share it within your organization](#share-an-artifact). On Pro and Max plans, where a public link is the only way to share, a connector-backed artifact stays private to you.

### The page shows no live data for a viewer

When a connector-backed page renders but its live sections stay empty for someone you shared it with, work through these causes:

* **The viewer hasn't connected the connector**: connectors are per-account, so each viewer needs their own connection to every connector the page calls. They can add one under **Settings > Connectors** on claude.ai, then reload the page.
* **The viewer declined the permission ask**: a denial lasts for the rest of that page load. Reloading the page brings the permission ask back.
* **Connector calls are turned off for the organization**: an Owner controls the [**Enable artifact connectors** toggle](#control-connector-calls-from-artifacts) in admin settings.

## What you can build

An artifact is a single HTML page, so anything you can express in HTML, CSS, and inline JavaScript is in scope. The patterns below come up most often.

### Walk through a change

Ask for a page that renders a diff or a design change with annotations beside the relevant lines, so reviewers can read your reasoning next to the code instead of reconstructing it from a description.

```text wrap theme={null}
Make an artifact that walks through this PR. Render the diff with margin annotations and color-code findings by severity.
```

### Compare alternatives

Ask for several variants on one page so you can evaluate them against each other. This works for layouts, copy, API shapes, or implementation plans.

```text wrap theme={null}
Make an artifact with four distinctly different layouts for the settings panel. Vary density and grouping, and lay them out as a grid with a one-line tradeoff under each.
```

### Tune with interactive controls

Ask for sliders, toggles, or input fields bound to whatever you are adjusting, so you can explore values directly instead of describing them.

```text wrap theme={null}
Build an artifact with sliders for the easing curve, duration, and delay so I can try values on this transition. Show the animation live as I move them.
```

### Bring the result back to your session

An artifact can act as a lightweight editor for a decision you then hand back to Claude. Ask for an export control that produces text you can paste into the terminal, so the result of interacting with the page flows back into the session instead of staying on the page.

```text wrap theme={null}
Make a triage board artifact with each open issue as a draggable card across Now, Next, Later, and Cut columns. Add a "Copy as prompt" button that gives me the final ordering to paste back here.
```

### Track work in progress

Ask Claude to keep an artifact current while a long task runs, so anyone with the link can follow along without reading the terminal.

```text wrap theme={null}
Turn this migration plan into a checklist artifact. Check items off as you complete them and add a note for anything you skip.
```

## Improve the visual design

Claude applies a built-in design skill when it builds an artifact, so pages get a deliberate palette, typography, and layout without extra prompting. Requires Claude Code v2.1.182 or later. That skill also looks for an existing design system in your project before choosing its own. Design tokens are the named color, typography, and spacing values your design system reuses. To keep artifacts consistent with your product's branding, record them where Claude can find them, such as the project's [CLAUDE.md](/docs/en/memory) or a theme file in your repository:

```markdown theme={null}
## Design system

- Colors: primary #1a4d8f, accent #f59e0b, surface #f8fafc
- Typography: Inter for body, JetBrains Mono for code
- Spacing: 8px scale, 6px border radius
```

Claude treats your design system as higher precedence than its own choices, and your prompt as higher precedence than both. The heading and format above are an example; any clear list of colors, fonts, and spacing works.

For typography, Claude can load a typeface from Google Fonts, the one external font source an artifact page can load from. Claude inlines any other typeface as a `@font-face` data URI and gives every typeface a fallback stack, so the page still renders if a font doesn't load. To use a specific typeface, name it in your prompt or your design system.

## Draft a design canvas

To mock up a UI, a screen flow, a landing page, or a poster rather than build a page, run `/design` with a brief. Claude drafts the design as artboards on one canvas and publishes the canvas as an artifact that runs a research preview of Claude Design's editor. The brief names what you want drawn:

```text wrap theme={null}
/design a settings screen for a mobile banking app
```

Open the published artifact to review the artboards. Where saving is enabled for your account, select an element on an artboard, change it, and save to publish a new version; otherwise you view the draft and export it as PNG or PDF.

`/design` requires a session where [artifacts are available](#availability) and Claude Code v2.1.234 or later.

## Page constraints

Each artifact is one self-contained page. Claude Code wraps the file you publish in an HTML document shell and serves it under a strict Content Security Policy (CSP), which shapes what the page can do.

| Constraint        | Effect                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| External requests | The page can load typefaces from Google Fonts, and scripts from [four public CDN hosts](#allowlist-the-viewer-domain): cdnjs, the Tailwind and jQuery CDNs, and selected paths on jsDelivr such as `/npm/`. The CSP blocks every external image and all other external scripts, stylesheets, and fonts, and lets `fetch`, XHR, and WebSocket calls reach only the page's own origin and the Google Fonts hosts. Claude therefore loads any library the page needs from one of those CDNs, inlines all other CSS and JavaScript, and embeds images as data URIs. [Connector calls](#pull-live-data-with-mcp-connectors) go through claude.ai, which makes the network call itself. |
| No backend        | An artifact is a static page. It can't store data submitted through a form or authenticate viewers itself. Its only way to fetch data when someone views it is [calling MCP connectors](#pull-live-data-with-mcp-connectors), not an API of its own.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Single page       | Relative links do not resolve, because nothing is deployed alongside the page. For multi-section content, Claude uses in-page anchors rather than separate files.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Source file types | The published file must be `.html`, `.htm`, or `.md`. Markdown files render as styled HTML.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Rendered size     | The rendered page must be 16 MiB or smaller. Large embedded images are the usual cause when a publish fails for size.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

Generating an artifact uses output tokens like any other response, and a styled page is more token-intensive than the same content as terminal text. Inline CSS, JavaScript for interactive controls, and especially images embedded as data URIs are the main contributors. To reduce an artifact's token cost:

* Prefer SVG, or HTML and CSS, for diagrams over embedded raster images
* Omit interactivity you do not need
* Have the page summarize large datasets rather than inline them in full

## Availability

Artifacts require every condition below. When one is not met, Claude writes a local HTML file or says it cannot publish instead.

| Requirement         | Available when                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plan                | Pro, Max, Team, or Enterprise. On Pro and Max plans, artifacts are private to you until you share them, and no admin management applies. On Team plans, artifacts are on by default. On Enterprise plans, an Owner [enables them](#manage-artifacts-for-your-organization) in claude.ai admin settings.                                                                                                                                       |
| Authentication      | The session is backed by a claude.ai account: sign in with `/login` in the CLI or desktop app. Claude Tag sessions are signed in through the agent's identity, so no step is needed there. Sessions using an API key, [gateway token](/docs/en/llm-gateway), or cloud-provider credential cannot publish.                                                                                                                                          |
| Model provider      | Anthropic API. Not available on [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), or [Microsoft Foundry](/docs/en/microsoft-foundry).                                                                                                                                                                                                                                                                   |
| Organization policy | Customer-managed encryption keys (CMEK), HIPAA, and [Zero Data Retention](/docs/en/zero-data-retention) are not enabled for the organization.                                                                                                                                                                                                                                                                                                      |
| Surface             | Claude Code CLI version 2.1.183 or later, or the Claude desktop app version 1.13576.0 or later. [Claude Tag](https://claude.com/docs/claude-tag/overview) sessions can also publish artifacts when both Claude Tag and artifacts are enabled for the organization. Off by default in [Agent SDK](/docs/en/agent-sdk/overview), GitHub Action, and MCP-server contexts, and when [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/en/env-vars) is set. |

## Disable artifacts

To turn artifacts off for your own sessions regardless of your organization's setting, use any of:

| Where                                | What to do                                                                                                                            |
| :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| [`/config`](/docs/en/commands)            | Turn the **Artifacts** row off, which writes [`"enableArtifact": false`](/docs/en/settings-reference#enableartifact) to your user settings |
| [Settings file](/docs/en/settings)        | Set `"enableArtifact": false`. The deprecated `"disableArtifact": true` also turns artifacts off                                      |
| [Environment variable](/docs/en/env-vars) | Set `CLAUDE_CODE_DISABLE_ARTIFACT=1`                                                                                                  |
| [Permission rule](/docs/en/permissions)   | Add `Artifact` to `permissions.deny`                                                                                                  |

Once you turn artifacts off in a [`--settings`](/docs/en/cli-reference#cli-flags) file or with `CLAUDE_CODE_DISABLE_ARTIFACT`, or your administrator turns them off in [managed settings](/docs/en/server-managed-settings), no settings file turns them back on. Before v2.1.242, a file higher in the [precedence stack](/docs/en/settings#settings-precedence) could turn artifacts back on even when a lower-precedence file set `"enableArtifact": false`.

You can also set `"enableArtifact": false` in a project's `.claude/settings.json` or `.claude/settings.local.json` to turn artifacts off for sessions in that project. An `"enableArtifact": true` in either file doesn't turn them back on. Honoring the key in project and local settings requires Claude Code v2.1.242 or later.

## Manage artifacts for your organization

Owners on Team and Enterprise plans control artifacts from [claude.ai admin settings](https://claude.ai/admin-settings/claude-code). Artifact content is stored on Anthropic-operated infrastructure and is visible only to authenticated members of the publishing organization, unless the artifact is [shared publicly](#control-public-sharing).

### Enable or disable artifacts

To enable or disable artifacts for the whole organization, go to [**Settings > Claude Code > Capabilities**](https://claude.ai/admin-settings/claude-code) and use the **Artifacts** toggle. On Enterprise plans with role-based access control, you can additionally scope artifacts to specific roles: go to [**Settings > Roles**](https://claude.ai/admin-settings/roles), edit a role, and set the **Artifacts** permission under the **Claude Code** group.

### Control connector calls from artifacts

[Connector calls from artifacts](#pull-live-data-with-mcp-connectors) have their own toggle, separate from the **Artifacts** toggle that turns artifacts on or off. Go to [**Settings > Capabilities**](https://claude.ai/admin-settings/capabilities) and use the **Enable artifact connectors** toggle. The same toggle governs connector calls from artifacts created in claude.ai conversations, which is why it sits under **Settings > Capabilities** rather than **Settings > Claude Code**.

### Control public sharing

Public sharing is off by default on Team and Enterprise plans, so members can share artifacts only within the organization until an Owner turns it on. To let members publish artifacts to public links that anyone can view without signing in, go to **Settings > Claude Code > Capabilities** and turn on **External sharing** under the **Artifacts** toggle. Turning it back off blocks access through existing public links without changing each artifact's audience; access resumes if you re-enable it.

### Set a retention policy

To set how long artifacts are kept before automatic deletion, go to [**Settings > Data & privacy controls**](https://claude.ai/admin-settings/data-privacy-controls). You can set separate retention periods for artifacts that are still private to their author and artifacts that have been shared.

### Review the audit log

Publishing, sharing, and deleting an artifact each appear in your organization's audit log under the `claude_artifact_*` event types, the same family used for artifacts created in claude.ai conversations.

### Allowlist the viewer domain

The viewer on claude.ai loads each artifact from a sandboxed `*.claudeusercontent.com` origin. If your organization restricts outbound network access, add that domain to your allowlist alongside `claude.ai`. See [Network access requirements](/docs/en/network-config#network-access-requirements) for the full list.

An artifact that loads a typeface from [Google Fonts](#improve-the-visual-design) also requests `fonts.googleapis.com` and `fonts.gstatic.com`. Both hosts are optional. If you block them, artifacts render in fallback typefaces. Block with a fast rejection rather than a silent drop so the font request fails immediately instead of delaying the page's first render.

Artifacts can also load JavaScript libraries, such as React or a charting package, from `cdnjs.cloudflare.com`, `cdn.jsdelivr.net`, `cdn.tailwindcss.com`, and `code.jquery.com`, and from no other external host. If you block those hosts, the parts of an artifact that depend on a library don't work, and unlike a blocked font, a blocked library has no fallback. Block with a fast rejection here too, so a blocked library request fails at once rather than hanging until it times out.

### List and delete artifacts with the Compliance API

The [Compliance API](https://docs.claude.com/en/api/compliance) provides endpoints to list an organization's artifacts, retrieve a specific version's content, and delete an artifact:

| Method   | Endpoint                                                            |
| :------- | :------------------------------------------------------------------ |
| `GET`    | `/v1/compliance/code/artifacts`                                     |
| `GET`    | `/v1/compliance/code/artifacts/{artifact_id}/versions/{version_id}` |
| `DELETE` | `/v1/compliance/code/artifacts/{artifact_id}`                       |

For the request and response schemas, see the [Compliance API reference](https://docs.claude.com/en/api/compliance/code/artifacts).

## Related resources

* Browse [prompting patterns and workflows](/docs/en/prompt-library) that pair with artifacts
* Turn an artifact prompt you reuse into a [skill](/docs/en/skills) so you can invoke it as a command
* [Connect MCP servers](/docs/en/mcp) so Claude can pull data into an artifact while it builds the page
