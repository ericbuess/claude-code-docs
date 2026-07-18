> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code with Chrome

> Connect Claude Code to your Chrome browser to test web apps, debug with console logs, automate form filling, and extract data from web pages.

Claude Code integrates with the [Claude in Chrome browser extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) to give you browser automation capabilities from the CLI or the [VS Code extension](/en/vs-code#automate-browser-tasks-with-chrome). Build your code, then test and debug in the browser without switching contexts.

Claude opens new tabs for browser tasks and shares your browser's login state, so it can access any site you're already signed into. Browser actions run in a visible Chrome window in real time. When Claude encounters a login page or CAPTCHA, it pauses and asks you to handle it manually.

<Note>
  Chrome integration works with Google Chrome and Microsoft Edge. Claude Code also detects the extension and sets up the connection in other Chromium-based browsers, including Brave, Arc, Vivaldi, and Opera. Chrome integration isn't supported in Windows Subsystem for Linux (WSL).
</Note>

## Capabilities

With Chrome connected, you can chain browser actions with coding tasks in a single workflow:

* **Live debugging**: read console errors and DOM state directly, then fix the code that caused them
* **Design verification**: build a UI from a Figma mock, then open it in the browser to verify it matches
* **Web app testing**: test form validation, check for visual regressions, or verify user flows
* **Authenticated web apps**: interact with Google Docs, Gmail, Notion, or any app you're logged into without API connectors
* **Data extraction**: pull structured information from web pages and save it locally
* **Task automation**: automate repetitive browser tasks like data entry, form filling, or multi-site workflows
* **File uploads**: attach files from your machine to upload fields on web pages
* **Session recording**: record browser interactions as GIFs to document or share what happened

## Prerequisites

Before using Claude Code with Chrome, you need:

* [Google Chrome](https://www.google.com/chrome/), [Microsoft Edge](https://www.microsoft.com/edge), or another Chromium-based browser such as Brave, Arc, Vivaldi, or Opera
* [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) version 1.0.36 or higher, available in the Chrome Web Store
* [Claude Code](/en/quickstart#step-1-install-claude-code)
* A direct Anthropic plan (Pro, Max, Team, or Enterprise)

<Note>
  Chrome integration is not available through third-party providers like Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. If you access Claude exclusively through a third-party provider, you need a separate claude.ai account to use this feature.
</Note>

## Get started in the CLI

<Steps>
  <Step title="Launch Claude Code with Chrome">
    Start Claude Code with the `--chrome` flag:

    ```bash theme={null}
    claude --chrome
    ```

    The first time you launch with Chrome, Claude Code shows a one-time dialog that introduces the integration and explains how site permissions work. Press Enter to continue.

    To enable Chrome for future sessions without the flag, see [Enable Chrome by default](#enable-chrome-by-default).
  </Step>

  <Step title="Ask Claude to use the browser">
    This example navigates to a page, interacts with it, and reports what it finds, all from your terminal or editor:

    ```text theme={null}
    Go to code.claude.com/docs, click on the search box,
    type "hooks", and tell me what results appear
    ```

    The first browser action asks for permission to use the `claude-in-chrome` skill. Approve it and Claude opens a new tab and starts the task.
  </Step>
</Steps>

Run `/chrome` at any time to check the connection status, manage permissions, reconnect the extension, or choose which connected browser to use. The integration is working when the status panel shows "Status: Enabled" and "Extension: Installed". If more than one browser is connected when a browser action starts, Claude prompts you to pick one.

For VS Code, see [browser automation in VS Code](/en/vs-code#automate-browser-tasks-with-chrome).

### Enable Chrome by default

To avoid passing `--chrome` each session, run `/chrome` and select "Enabled by default".

Claude Code starts normally when Chrome isn't running. Before v2.1.211, startup could hang when Chrome integration was enabled but Chrome wasn't running.

In the [VS Code extension](/en/vs-code#automate-browser-tasks-with-chrome), Chrome is available whenever the Chrome extension is installed. No additional flag is needed.

<Note>
  Enabling Chrome by default in the CLI increases context usage since browser tools are always loaded. If you notice increased context consumption, disable this setting and use `--chrome` only when needed.
</Note>

### Manage site permissions

Site-level permissions are inherited from the Chrome extension. Manage permissions in the Chrome extension settings to control which sites Claude can browse, click, and type on.

### Browser tools in plan mode

In [plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode), browser tool calls that only read the page or browser state run without a permission prompt, and calls that change state prompt for approval.

* **Read-only calls**: `read_page`, `get_page_text`, `find`, reading console messages or network requests, and taking a screenshot
* **State-changing calls**: clicks, typing, navigation, tab and window management, and recording a GIF

As of v2.1.199, an otherwise read-only call that sets a state-changing input flag, such as `createIfEmpty` on `tabs_context_mcp`, `clear` on the console and network readers, or `save_to_disk` on a screenshot, also prompts for approval. A `browser_batch` call runs without a prompt only when every action inside it is read-only.

## Example workflows

These examples show common ways to combine browser actions with coding tasks. Run `/mcp`, select `claude-in-chrome`, then select **View tools** to see the full list of available browser tools.

### Test a local web application

When developing a web app, ask Claude to verify your changes work correctly:

```text theme={null}
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude navigates to your local server, interacts with the form, and reports what it observes.

### Debug with console logs

Claude can read console output to help diagnose problems. Tell Claude what patterns to look for rather than asking for all console output, since logs can be verbose:

```text theme={null}
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude reads the console messages and can filter for specific patterns or error types.

### Automate form filling

Speed up repetitive data entry tasks:

```text theme={null}
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude reads your local file, navigates the web interface, and enters the data for each record.

### Upload files to web pages

Claude can attach files from your machine to upload fields on a page. Claude Code reads the file and sends its contents to the browser, so uploads work in both local and remote sessions. Requires Claude Code v2.1.211 or later.

This example attaches a log file to a form:

```text theme={null}
Open the bug tracker at bugs.example.com, create a new issue,
and attach logs/session.log to it
```

Three restrictions apply to uploads:

* **Permissions**: Claude can upload a file only when the session is allowed to read it, so [permission rules](/en/settings#permission-settings) that deny `Read` access to a file also block uploading it.
* **Size**: a single upload can include up to 10 MB of files in total.
* **Hard links**: Claude refuses files that have multiple hard links, which is common inside package-manager stores like `node_modules`. Copy the file and upload the copy.

### Draft content in Google Docs

Use Claude to write directly in your documents without API setup:

```text theme={null}
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude opens the document, clicks into the editor, and types the content. This works with any web app you're logged into: Gmail, Notion, Sheets, and more.

### Extract data from web pages

Pull structured information from websites:

```text theme={null}
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude navigates to the page, reads the content, and compiles the data into a structured format.

### Run multi-site workflows

Coordinate tasks across multiple websites:

```text theme={null}
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude works across tabs to gather information and complete the workflow.

### Record a demo GIF

Create shareable recordings of browser interactions:

```text theme={null}
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude records the interaction sequence and saves it as a GIF file. The recording captures everything visible in the browser, including account details on logged-in pages, so review it before sharing it outside your team.

### Save screenshots to disk

Ask Claude to keep a screenshot as a file:

```text theme={null}
Take a screenshot of the checkout page and save it to disk
```

Claude saves the image to disk and reports the file path. Before v2.1.211, the screenshot tool's `save_to_disk` option didn't write a file.

## Troubleshooting

### Extension not detected

If Claude Code can't detect the Chrome extension:

1. Verify the Chrome extension is installed and enabled in `chrome://extensions`
2. Verify Claude Code is up to date by running `claude --version`
3. Check that Chrome is running
4. Run `/chrome` and select "Reconnect extension" to re-establish the connection
5. If the issue persists, restart both Claude Code and Chrome

The first time you enable Chrome integration, Claude Code installs a native messaging host configuration file. Chrome reads this file on startup, so if the extension isn't detected on your first attempt, restart Chrome to pick up the new configuration.

As of v2.1.199, Claude Code opens a browser tab prompting you to connect the extension only on that first install. Later sessions that rewrite the configuration file, for example after switching Claude Code builds or config directories, don't reopen it.

If the connection still fails, verify the host configuration file exists at:

For Chrome:

* **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**: `~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**: check `HKCU\Software\Google\Chrome\NativeMessagingHosts\` in the Windows Registry

For Edge:

* **macOS**: `~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**: `~/.config/microsoft-edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**: check `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\` in the Windows Registry

Other Chromium-based browsers read the same file from their own configuration directory, named after the browser. For example, Brave on macOS uses `~/Library/Application Support/BraveSoftware/Brave-Browser/NativeMessagingHosts/`, and on Windows each browser has its own registry key, such as `HKCU\Software\BraveSoftware\Brave-Browser\NativeMessagingHosts\`.

### Browser not responding

If Claude's browser commands stop working:

1. Check if a modal dialog (alert, confirm, prompt) is blocking the page. JavaScript dialogs block browser events and prevent Claude from receiving commands. Dismiss the dialog manually, then tell Claude to continue.
2. Ask Claude to create a new tab and try again
3. Restart the Chrome extension by disabling and re-enabling it in `chrome://extensions`

### Connection drops during long sessions

The Chrome extension's service worker can go idle during extended sessions, which breaks the connection. If browser tools stop working after a period of inactivity, run `/chrome` and select "Reconnect extension".

### Windows-specific issues

On Windows, you may encounter:

* **Named pipe conflicts (EADDRINUSE)**: if another process is using the same named pipe, restart Claude Code. Close any other Claude Code sessions that might be using Chrome.
* **Native messaging host errors**: if the native messaging host crashes on startup, try reinstalling Claude Code to regenerate the host configuration.
* **Setup pages fail to open**: {/* min-version: 2.1.211 */}update Claude Code. Before v2.1.211, the browser tab prompting you to connect the extension could fail to open on Windows.

### Common error messages

These are the most frequently encountered errors and how to resolve them:

| Error                                       | Cause                                            | Fix                                                             |
| ------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------- |
| "Browser extension is not connected"        | Native messaging host cannot reach the extension | Restart Chrome and Claude Code, then run `/chrome` to reconnect |
| Extension shows "Not detected" in `/chrome` | Chrome extension is not installed or is disabled | Install or enable the extension in `chrome://extensions`        |
| "No tab available"                          | Claude tried to act before a tab was ready       | Ask Claude to create a new tab and retry                        |
| "Receiving end does not exist"              | Extension service worker went idle               | Run `/chrome` and select "Reconnect extension"                  |

## See also

* [Computer use](/en/computer-use): control native macOS apps when a task can't be done in a browser
* [Use Claude Code in VS Code](/en/vs-code#automate-browser-tasks-with-chrome): browser automation in the VS Code extension
* [CLI reference](/en/cli-reference): command-line flags including `--chrome`
* [Common workflows](/en/common-workflows): more ways to use Claude Code
* [Data and privacy](/en/data-usage): how Claude Code handles your data
* [Getting started with Claude in Chrome](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome): full documentation for the Chrome extension, including shortcuts, scheduling, and permissions
