# Quickstart

> Welcome to Claude Code!

This quickstart guide will have you using AI-powered coding assistance in just a few minutes. By the end, you'll understand how to use Claude Code for common development tasks.

## Before you begin

Make sure you have:

* A terminal or command prompt open
* A code project to work with
* A [Claude.ai](https://claude.ai) (recommended) or [Claude Console](https://console.anthropic.com/) account

## Step 1: Install Claude Code

### NPM Install

If you have [Node.js 18 or newer installed](https://nodejs.org/en/download/):

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

### Native Install

<Tip>
  Alternatively, try our new native install, now in beta.
</Tip>

**Homebrew (macOS, Linux):**

```sh  theme={null}
brew install --cask claude-code
```

**macOS, Linux, WSL:**

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell  theme={null}
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**

```batch  theme={null}
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

## Step 2: Log in to your account

Claude Code requires an account to use. When you start an interactive session with the `claude` command, you'll need to log in:

```bash  theme={null}
claude
# You'll be prompted to log in on first use
```

```bash  theme={null}
/login
# Follow the prompts to log in with your account
```

You can log in using either account type:

* [Claude.ai](https://claude.ai) (subscription plans - recommended)
* [Claude Console](https://console.anthropic.com/) (API access with pre-paid credits)

Once logged in, your credentials are stored and you won't need to log in again.

<Note>
  When you first authenticate Claude Code with your Claude Console account, a workspace called "Claude Code" is automatically created for you. This workspace provides centralized cost tracking and management for all Claude Code usage in your organization.
</Note>

<Note>
  You can have both account types under the same email address. If you need to log in again or switch accounts, use the `/login` command within Claude Code.
</Note>

## Step 3: Start your first session

Open your terminal in any project directory and start Claude Code:

```bash  theme={null}
cd /path/to/your/project
claude
```

You'll see the Claude Code welcome screen with your session information, recent conversations, and latest updates. Type `/help` for available commands or `/resume` to continue a previous conversation.

<Tip>
  After logging in (Step 2), your credentials are stored on your system. Learn more in [Credential Management](/en/docs/claude-code/iam#credential-management).
</Tip>

## Step 4: Ask your first question

Let's start with understanding your codebase. Try one of these commands:

```
> what does this project do?
```

Claude will analyze your files and provide a summary. You can also ask more specific questions:

```
> what technologies does this project use?
```

```
> where is the main entry point?
```

```
> explain the folder structure
```

You can also ask Claude about its own capabilities:

```
> what can Claude Code do?
```

```
> how do I use slash commands in Claude Code?
```

```
> can Claude Code work with Docker?
```

<Note>
  Claude Code reads your files as needed - you don't have to manually add context. Claude also has access to its own documentation and can answer questions about its features and capabilities.
</Note>

## Step 5: Make your first code change

Now let's make Claude Code do some actual coding. Try a simple task:

```
> add a hello world function to the main file
```

Claude Code will:

1. Find the appropriate file
2. Show you the proposed changes
3. Ask for your approval
4. Make the edit

<Note>
  Claude Code always asks for permission before modifying files. You can approve individual changes or enable "Accept all" mode for a session.
</Note>

## Step 6: Use Git with Claude Code

Claude Code makes Git operations conversational:

```
> what files have I changed?
```

```
> commit my changes with a descriptive message
```

You can also prompt for more complex Git operations:

```
> create a new branch called feature/quickstart
```

```
> show me the last 5 commits
```

```
> help me resolve merge conflicts
```

## Step 7: Fix a bug or add a feature

Claude is proficient at debugging and feature implementation.

Describe what you want in natural language:

```
> add input validation to the user registration form
```

Or fix existing issues:

```
> there's a bug where users can submit empty forms - fix it
```

Claude Code will:

* Locate the relevant code
* Understand the context
* Implement a solution
* Run tests if available

## Step 8: Test out other common workflows

There are a number of ways to work with Claude:

**Refactor code**

```
> refactor the authentication module to use async/await instead of callbacks
```

**Write tests**

```
> write unit tests for the calculator functions
```

**Update documentation**

```
> update the README with installation instructions
```

**Code review**

```
> review my changes and suggest improvements
```

<Tip>
  **Remember**: Claude Code is your AI pair programmer. Talk to it like you would a helpful colleague - describe what you want to achieve, and it will help you get there.
</Tip>

## Essential commands

Here are the most important commands for daily use:

| Command             | What it does                      | Example                             |
| ------------------- | --------------------------------- | ----------------------------------- |
| `claude`            | Start interactive mode            | `claude`                            |
| `claude "task"`     | Run a one-time task               | `claude "fix the build error"`      |
| `claude -p "query"` | Run one-off query, then exit      | `claude -p "explain this function"` |
| `claude -c`         | Continue most recent conversation | `claude -c`                         |
| `claude -r`         | Resume a previous conversation    | `claude -r`                         |
| `claude commit`     | Create a Git commit               | `claude commit`                     |
| `/clear`            | Clear conversation history        | `> /clear`                          |
| `/help`             | Show available commands           | `> /help`                           |
| `exit` or Ctrl+C    | Exit Claude Code                  | `> exit`                            |

See the [CLI reference](/en/docs/claude-code/cli-reference) for a complete list of commands.

## Pro tips for beginners

<AccordionGroup>
  <Accordion title="Be specific with your requests">
    Instead of: "fix the bug"

    Try: "fix the login bug where users see a blank screen after entering wrong credentials"
  </Accordion>

  <Accordion title="Use step-by-step instructions">
    Break complex tasks into steps:

    ```
    > 1. create a new database table for user profiles
    ```

    ```
    > 2. create an API endpoint to get and update user profiles
    ```

    ```
    > 3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="Let Claude explore first">
    Before making changes, let Claude understand your code:

    ```
    > analyze the database schema
    ```

    ```
    > build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="Save time with shortcuts">
    * Press `?` to see all available keyboard shortcuts
    * Use Tab for command completion
    * Press ↑ for command history
    * Type `/` to see all slash commands
  </Accordion>
</AccordionGroup>

## What's next?

Now that you've learned the basics, explore more advanced features:

<CardGroup cols={3}>
  <Card title="Common workflows" icon="graduation-cap" href="/en/docs/claude-code/common-workflows">
    Step-by-step guides for common tasks
  </Card>

  <Card title="CLI reference" icon="terminal" href="/en/docs/claude-code/cli-reference">
    Master all commands and options
  </Card>

  <Card title="Configuration" icon="gear" href="/en/docs/claude-code/settings">
    Customize Claude Code for your workflow
  </Card>

  <Card title="Claude Code on the web" icon="cloud" href="/en/docs/claude-code/claude-code-on-the-web">
    Run tasks asynchronously in the cloud
  </Card>
</CardGroup>

## Getting help

* **In Claude Code**: Type `/help` or ask "how do I..."
* **Documentation**: You're here! Browse other guides
* **Community**: Join our [Discord](https://www.anthropic.com/discord) for tips and support
