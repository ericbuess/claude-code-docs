> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Test plugins with evals

> Write eval cases for your Claude Code plugin, run them with claude plugin eval, grade the results, compare against a no-plugin baseline, and gate CI on the score.

`claude plugin eval` runs your [plugin](/docs/en/plugins) against a suite of test cases and scores the results. Each case is a realistic prompt plus one or more graders. A grader is a pass/fail check on what Claude produced, such as a regex over the reply, whether a particular tool was called, or a rubric that a second model judges the reply against.

You don't have to write the suite by hand; `claude plugin eval init` asks you about your plugin, proposes the cases and graders, tries them, and writes the files, and you can ask Claude to do the same from a session you already have open.

Use evals to measure how reliably your plugin steers Claude to the right outcome, to catch regressions when you change the plugin or a new model ships, and to see what the plugin contributes compared with no plugin at all.

This page is for plugin and skill authors who have a working plugin and want to test its behavior, and for teams that gate plugin changes in CI. Its case format is separate from the `evals/evals.json` file the [skill-creator plugin](/docs/en/skills#run-evals-with-skill-creator) uses. To create a plugin, see [Create plugins](/docs/en/plugins); to check a plugin's files for syntax and schema errors rather than its behavior, use [`claude plugin validate`](/docs/en/plugins-reference#plugin-validate).

<Note>
  Every eval run and every judge grader is a real model call on your account, counted against your plan's usage or your API bill, so check the [requirements](#requirements) first. Then [create your first eval suite](#create-your-first-eval-suite), or go to [Run evals in CI](#run-evals-in-ci) if you already have one.
</Note>

## Requirements

To run plugin evals you need:

* Claude Code v2.1.269 or later. Run `claude --version` to check and `claude update` to upgrade.
* A plugin directory with a `plugin.json` or `.claude-plugin/plugin.json` manifest, or a [skills-directory plugin](/docs/en/plugins-reference#skills-directory-plugins).
* The same authentication and model provider your normal Claude Code sessions use. Eval runs, judge-scored graders, and `claude plugin eval init` call the model with your credentials, so they count against your plan's usage limits or your API bill. When the command reports a cost, the figure is a [list-price estimate](/docs/en/costs) of those calls.

## How an eval run works

An eval suite lives in a directory called `evals/` inside your plugin, laid out as [Write and refine cases](#write-and-refine-cases) shows. Each case is its own subdirectory with a [prompt](#set-run-limits-and-tools-in-prompt-md) and one or more [graders](#grade-the-result). The prompt is something a person using your plugin might type, such as a request one of its skills should handle.

### What happens in a run

For each run of a case, Claude Code starts a fresh, [isolated](#how-runs-are-isolated) [non-interactive session](/docs/en/headless) with only your plugin loaded, sends the prompt, and lets Claude work until it finishes or hits the case's turn or time limit. Each grader then checks the final reply, the full transcript, or a file Claude created, and passes or fails.

### How a case is scored

One run of a non-deterministic agent tells you little, so each case runs three times by default. A run's score is the fraction of its graders that passed, weighted if you set weights, and the case's score is the mean across its runs. A case passes when its score meets the [`--threshold`](#command-options), `1.0` by default.

### The no-plugin baseline

A high score on its own doesn't tell you the plugin helped, because Claude might do as well without it. To separate the two, each case's runs are repeated with no plugin loaded by default, and you get two scores, `WITH` and `W/OUT`. Their difference, `Δ`, is what the plugin contributed. If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass. The two sets of runs are called the with-arm and the without-arm; [Compare against a no-plugin baseline](#compare-against-a-no-plugin-baseline) covers how graders are scored across them and how to turn the baseline off.

A suite makes roughly cases × runs × arms agent runs plus three short judge calls per `llm` or `baseline` grader per run, and results vary between runs.

## Create your first eval suite

This walkthrough writes one case for your own plugin, runs it, and reads the result. Before you start, make sure you have:

* Claude Code v2.1.269 or later and the other [requirements](#requirements)
* A terminal open at your plugin's root directory, the one containing `plugin.json` or `.claude-plugin/plugin.json`
* One skill in the plugin you want to test, and a request a user would type that should trigger it

<Steps>
  <Step title="Create the cases">
    From the plugin root, run:

    ```bash theme={null}
    claude plugin eval init
    ```

    If Claude Code doesn't already trust this directory it first asks `Trust this plugin directory?`; answer `y`. An interactive Claude Code session then opens. Claude reads your plugin and asks you what a good result looks like, proposes prompts that should and shouldn't trigger the plugin, designs graders for each, pilots them once to check they behave, and writes one case directory per prompt under `evals/`, each named after its prompt. When Claude tells you the suite is ready, exit that session with `/exit` or Ctrl+D to return to your shell.

    If you already have a Claude Code session open at the plugin root, you can instead ask Claude there to run `claude plugin eval init`. Claude runs the command and then asks you the same questions in that conversation.

    If you'd rather write a case yourself to see exactly what the files contain, follow [Write a case by hand](#write-a-case-by-hand) and come back here to run it.
  </Step>

  <Step title="Run the suite">
    Back at your shell in the plugin root, run every case under `evals/`:

    ```bash theme={null}
    claude plugin eval .
    ```

    You already trusted this directory during step 1, so the run starts immediately. If you wrote the case by hand instead, the run first asks `Trust this plugin directory? [y/N]`; answer `y`. [What a run can access](#security) explains what you're agreeing to.

    Each case runs three times with your plugin and three times without it, so one case is six runs. A progress line prints as each run finishes, with that run's score and each grader's verdict.
  </Step>

  <Step title="Read the summary">
    When the suite finishes you see a summary table, followed by where the report went:

    ```text theme={null}
    CASE        WITH  W/OUT Δ      RUNS COST    NOTES
    first-case  1.00  0.33  +0.67  6    $0.41

    1 case(s) · mean Δ +0.67 · 74s · $0.41
    Report: /Users/you/my-plugin/evals/results/2026-09-10T17-02-11-482Z/report.html
    Published: https://claude.ai/... · keep local next time with --no-publish
    ```

    `WITH` is the case's score with your plugin loaded, `W/OUT` is the score without it, and a positive `Δ` means the plugin raised the score. `COST` is a list-price estimate of the model calls, and `NOTES` shows the highest-weight failing grader's explanation, or the run's error, from the with-arm.
  </Step>

  <Step title="Open the report and iterate">
    Open the `Published:` URL, or the `Report:` path when no `Published:` line appears, to see each grader's verdict and explanation for every run, and for `llm` graders the judge's votes and the excerpt it judged. The `Published:` line appears only when your account can [publish reports](#html-report).

    The most common first finding is a `Δ` near zero with the case's `tool_used: Skill` grader failing, which means Claude isn't choosing your skill on natural phrasing. Adjust the skill's [`description`](/docs/en/skills#frontmatter-reference), run `claude plugin eval .` again, and compare.

    To iterate on one case cheaply, run a single arm once. A single run is noisy, so confirm any change at the default three runs before you trust it. With one arm the table shows `SCORE` and `PASS%` columns instead of `WITH`, `W/OUT`, and `Δ`:

    ```bash theme={null}
    claude plugin eval . --case <case-name> --runs 1 --ablation none
    ```

    Replace `<case-name>` with one of the directory names under `evals/`.
  </Step>
</Steps>

<h2 id="write-and-refine-cases">
  Write and refine cases
</h2>

The cases `claude plugin eval init` writes are plain files you can open, change, and add to. A case is a directory under the plugin's eval directory that contains a `prompt.md`, a `case.yaml`, or both. To group cases, nest them under a directory that isn't itself a case; anything inside a case directory, such as `graders/` and fixture files, belongs to that case.

This is the layout `claude plugin eval init` writes and the one to use for new suites. The [eval suite reference](#eval-suite-reference) has the complete tree, including mocks and results:

```text theme={null}
my-plugin/
├── .claude-plugin/plugin.json
├── skills/...
└── evals/
    ├── first-case/
    │   ├── prompt.md          # frontmatter: case fields; body: the prompt
    │   ├── graders/
    │   │   ├── criteria.md    # frontmatter: type + options; body: rubric or pattern
    │   │   └── skill-fired.md
    │   └── case.yaml          # optional: only for context.* fields
    ├── ignores-unrelated-request/
    │   └── ...
    └── results/               # written by each run; add to .gitignore
```

### Write a case by hand

Having Claude write the cases with `claude plugin eval init` is the recommended path. To write one yourself instead, start from a blank template. The following command writes a case named `first-case` with a placeholder `prompt.md` and one placeholder grader, and runs nothing:

```bash theme={null}
claude plugin eval init --bare first-case
```

```text theme={null}
evals/first-case/
├── prompt.md            # the prompt sent to Claude, plus run limits
└── graders/
    └── criteria.md      # one grader: how to score the result
```

In `prompt.md` you write the message Claude receives in each run, and set the run's limits and the tools the case may use in its frontmatter. Open `evals/first-case/prompt.md` and replace the placeholder body with your request, phrased the way a user would type it rather than naming the skill:

```markdown theme={null}
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

<a request a user would type that your skill should handle>
```

For a skill that drafts commit messages, the body might be `Write me a commit message for this change: I renamed getUser to fetchUser and updated the three call sites.` Each run starts in an empty working directory, so put whatever the task needs in the prompt itself, or [set up the workspace](#add-setup-or-history-with-case-yaml) first. The [full list of frontmatter fields](#prompt-md-fields) covers the model, timeout, tags, and environment variables.

Each file under `graders/` is one check applied after the run. Open `evals/first-case/graders/criteria.md` and replace the placeholder with a rubric for the judge model, written as concrete PASS and FAIL conditions:

```markdown theme={null}
---
type: llm
---

PASS if <what a correct response contains>.
FAIL if <what a wrong or missing response looks like>.
```

Then add a second grader that checks whether your skill is what produced the answer. Create `evals/first-case/graders/skill-fired.md`, replacing `your-skill-name` with the `name` from your skill's `SKILL.md`:

```markdown theme={null}
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?your-skill-name"'
---
```

This passes when Claude invoked that skill at least once during the run, including by its namespaced `plugin-name:skill-name` form. [Grader types](#grader-types) lists the other checks available, such as matching a regex or confirming a file was created.

With both files saved, run the case the way the [quickstart](#create-your-first-eval-suite) does, with `claude plugin eval .` from the plugin root.

<h3 id="set-run-limits-and-tools-in-prompt-md">
  Set run limits and tools in prompt.md
</h3>

Set a case's `max_turns`, `timeout_seconds`, `model`, `tags`, and the `allowed_tools` it may use in `prompt.md` frontmatter; the [prompt.md frontmatter](#prompt-md-fields) reference lists every field and its default. Claude receives the body exactly as you wrote it. `@path` mentions in it aren't expanded into file attachments, so if Claude needs to read a file, grant a tool for it in `allowed_tools`.

<h3 id="grade-the-result">
  Choose and weight graders
</h3>

A grader's frontmatter sets its `type`, and optionally a `weight` that makes it count for more of the run's score and an [`arm`](#compare-against-a-no-plugin-baseline) that controls how it's scored against the baseline. Of the six types, `regex`, `tool_used`, `tool_order`, and `file_exists` are computed from the transcript and files and cost nothing, while `llm` and `baseline` call a judge model and add to the run's cost.

There are no custom-code graders. [Grader types](#grader-types) lists each type's options and pass condition, and [what a grader can look at](#what-a-grader-can-look-at) lists the values `target` and `focus` accept.

The judge for `llm` and `baseline` graders is a small fast model by default. Pass `--judge-model sonnet` or a full model ID to use a stronger one for nuanced rubrics.

#### Choose graders that give a stable signal

An `llm` grader asks a model for a verdict, so its answer can differ between runs, and it differs more the longer the text it has to read. These habits keep a suite's scores steady enough to trust:

* For long output such as a generated file, grade it with a `regex` grader over the file's contents, which checks the whole file the same way every time. Keep `llm` graders for short outputs, with rubrics written as concrete PASS and FAIL conditions.
* Give each case one grader on the result, such as the final message or a produced file, and one on how Claude got there, such as `tool_used` or `tool_order`. Together they tell you both whether the answer was right and whether your plugin produced it.
* If a case's `tool_used: Skill` grader passes but `Δ` is negative, suspect the judge before the plugin. A small judge model can mark a correct answer wrong because it's formatted differently from what the rubric describes. Re-run with `--judge-model sonnet`, and tighten the rubric so formatting doesn't decide the verdict.
* To check that a build or test passed inside the run, have the prompt ask Claude to run it and write the outcome to a file, grade that file, and assert the command ran with a `tool_used` grader whose `input_match` names the command.

<h3 id="compare-against-a-no-plugin-baseline">
  Score against the no-plugin baseline
</h3>

When a plugin is under test, each case runs in two arms by default. The with-arm is its runs with the plugin loaded, and the without-arm is the same number of runs with no plugin at all. The summary and report show both scores and `Δ`, the with-arm score minus the without-arm score. Pass `--ablation none` to run only the with-arm, which halves the cost when you don't need the comparison, such as while iterating on graders.

In a two-arm run, some graders are reported with `scored: false`. A check like "the skill was invoked" can never pass without the plugin, so counting it would push the without-arm toward zero and inflate `Δ`. To keep the two arms comparable, Claude Code excludes such graders from the score in both arms and reports them in the with-arm as pass/fail indicators only. That includes:

* Every `tool_used` grader whose `tool` is `Skill`
* Any grader you mark `arm: with-only`

If every grader in a case is one of these, they're scored normally instead, since there would be nothing left to score. Set `arm: both` on a grader to score it in both arms regardless, which is what you want for a "must not invoke the skill" check with `min: 0` and `max: 0`. Under `--ablation none` nothing is excluded, so the same suite can produce a different absolute score in the two modes.

### Use a different eval directory

If `evals/` is already taken by another tool, keep the suite in a different directory. You can record that directory in the plugin's `plugin.json` so every run and every collaborator uses it, or pass it on the command line for a single run:

* **In `plugin.json`**: add `"experimental": { "evals": "quality/evals" }`.
* **On the command line**: pass `--eval-dir quality/evals` to both `claude plugin eval` and `claude plugin eval init`.

If you set both, the flag's directory is used. Give a relative path of plain directory names such as `qa` or `quality/evals`; an absolute path or one containing `..` is rejected. Cases, results, and `init` output all move to that directory.

## Set up fixtures and mocks

A case can need more than a prompt: files or a git repository in the workspace, an earlier conversation to continue, or answers from the MCP servers your plugin talks to. Each of those is set up beside the case so runs stay repeatable.

<h3 id="add-setup-or-history-with-case-yaml">
  Seed the workspace or conversation
</h3>

Each run starts in an empty workspace. When a case needs more than the prompt, add a `case.yaml` beside `prompt.md` with a `context` block.

To create fixture files or a git repository first, write a Bash script in the case directory and name it in `context.scaffold_script`. The script runs as you, outside the agent's sandbox, and only when you pass `--scaffold`, so pass that flag only for suites you or your organization wrote. To continue an earlier conversation, save the transcript as a `.jsonl` file and name it in `context.history_file`, and the case's prompt becomes the next user turn. To let Claude read fixture directories in the case during the run, list them in `context.add_dirs`.

A `case.yaml` also needs `schema_version: "1.1"` and `name`; the [case.yaml fields](#case-yaml-fields) reference has the full list.

This `case.yaml` seeds a workspace from a script and lets Claude read fixtures from a `resources/` directory:

```yaml theme={null}
schema_version: "1.1"
name: changelog-from-diff
tags: [smoke]
context:
  scaffold_script: fixture.sh
  add_dirs: [resources]
```

<h3 id="mock-mcp-servers">
  Mock MCP servers
</h3>

You can evaluate a plugin whose skills call MCP tools without the real service behind them. Put one Markdown file per tool under `evals/mocks/<server>/<tool>.md` for the whole suite, or under a case's own `mocks/` directory for one case, where `<server>` is the server's name in your plugin's [MCP configuration](/docs/en/plugins-reference#mcp-servers).

A run never starts your plugin's real MCP servers unless you ask. Claude Code registers a stand-in under each server's own name. Tools with a mock file answer from it and are allowed without an `--allow-tools` grant, and a tool with no mock file isn't available to Claude. A server with no mocks at all appears in the case's `mocked:` progress line as `plugin_<plugin>_<server>[not started: no mock]`.

The file's body is what the tool returns to Claude. This mock stands in for a `create_issue` tool on a server named `tracker`, checks the input Claude sends, and echoes the title back. Save it as `evals/mocks/tracker/create_issue.md`:

```markdown theme={null}
---
expect:
  title: string
  priority: [low, medium, high]
---

Created issue #4821: {{input.title}}
```

Insert fields from the call's input with `{{input.<field>}}`, and the contents of a fixture file beside the mock with `{{file:fixtures/{input.<field>}.json}}`. The `expect:` block guards the input. If a call violates it, the run aborts with score 0 and records why, so a case can assert what your plugin asked the server to do. Set `error: true` to return the body as a tool error instead, or `type: agent` to have a small model answer as the server from instructions in the body. The [mock file reference](#mock-files) lists every key and the `_server.md` and `_tools.json` files.

To grade the calls themselves, point a grader at `target: mock_calls`.

To run against the plugin's real MCP servers instead, pass one of these flags. Either way those processes run as you, outside the run's sandbox, and their tools need an [`--allow-tools` grant](#grant-tools):

* **`--allow-real-servers`**: start the real process for each server you haven't mocked, and keep answering mocked tools from their files
* **`--mocks off`**: ignore `mocks/` entirely and start every server the plugin declares

#### Replay agent mock answers

A `type: agent` mock answers with a model call, so its output varies between runs. When a run completes without an error or abort, Claude Code saves each answer an agent mock gave under the results directory in `mock-recordings/`.

Open `ADOPT.txt` there to see each recording and the `.replay/<server>/` directory to copy it into, beside the mock that produced it. After you copy a recording there, later runs answer the identical call from it with no model call. Commit `.replay/` alongside `mocks/` so CI runs are repeatable.

## Run evals

Once a suite exists, `claude plugin eval` runs it. You choose which plugin and cases run with the target argument, grant any tools the cases need beyond the read-only set with `--allow-tools`, and control run count, models, cost, and output with the other options.

### Choose what to evaluate

Most of the time you run `claude plugin eval .` from the plugin root, which runs every case in the suite with the plugin you're standing in loaded. To run a single case file, or to evaluate a plugin you installed rather than one you're developing, pass a different target:

| Target                                                    | What runs                                                                                                                                                                                         |
| :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A plugin's root directory, such as `.`                    | Every case under its eval directory, with that plugin loaded                                                                                                                                      |
| A single `prompt.md` or `case.yaml` file                  | That case, with its enclosing plugin loaded                                                                                                                                                       |
| An installed plugin by name, `name` or `name@marketplace` | The cases in the installed copy's eval directory, with the installed copy loaded. Results are written under `./evals/results/` in your current directory, or `./<dir>/results/` with `--eval-dir` |
| `name@skills-dir`                                         | The same, for a [skills-directory plugin](/docs/en/plugins-reference#skills-directory-plugins)                                                                                                         |
| Omitted                                                   | The current directory as a path                                                                                                                                                                   |

Add `--case <glob>` to filter by case name and `--tag <tag>` to keep cases with any of the given tags. Put the target before `--tag`, `--allow-tools`, and `--json`. The first two take a list and `--json` takes an optional path, so each of them reads a target that follows as its own value.

### Grant tools

Runs never stop to ask for permission. Built-in tools that need a grant you didn't give, such as `Bash`, `Write`, `Edit`, `WebFetch`, and `WebSearch`, are removed from the session, so Claude can't call them at all. The allowlist is the read-only tools the case lists in `allowed_tools`, from `Read`, `Glob`, `Grep`, `NotebookRead`, `Skill`, `Agent`, `TodoWrite`, and the task tools `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, `TaskStop`, and `TaskOutput`, plus whatever you grant with `--allow-tools`, which applies to every case in the run. To let cases use `Bash`, `Write`, `Edit`, `WebFetch`, or `WebSearch`, grant them yourself:

```bash theme={null}
claude plugin eval . --allow-tools Write Edit "Bash(npm test *)"
```

When a case asked for a tool you didn't grant, the run lists it on stderr as `not granted`. Tools on a [mocked](#mock-mcp-servers) MCP server need no grant. Tools on a real plugin MCP server need both the server started, with `--allow-real-servers` or `--mocks off`, and a grant by name, such as `--allow-tools "mcp__plugin_my-plugin_github__*"`; a plugin's MCP tools are named `mcp__plugin_<plugin>_<server>__<tool>`.

When you grant `Bash` in any form, every command runs under Claude Code's [OS-level sandbox](/docs/en/sandboxing). Writes are confined to the run's workspace, your home directory and Claude Code configuration are unreadable, and network access is limited to domains you grant with `--allow-tools "WebFetch(domain:example.com)"`. If you grant Bash or PowerShell on a machine with no sandbox backend, Claude Code refuses each run rather than running it unconfined, and the case shows a run error and usually scores 0. Native Windows has no backend, so run shell-granting suites under WSL2; on Linux, install `bubblewrap` and `socat` first. See the [sandboxing prerequisites](/docs/en/sandboxing).

### Command options

This table covers the options for run count, models, scoring, cost, tool grants, mocks, and output. Run `claude plugin eval --help` for the complete list, which also includes `--case`, `--tag`, `--eval-dir`, `--no-scaffold`, `--report`, and `--verbose`.

| Option                     | Default                                                                        | Effect                                                                                                                                                                                                                                                                                     |
| :------------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--runs <n>`               | Each case's `runs`, else 3                                                     | Runs per case per arm                                                                                                                                                                                                                                                                      |
| `-j`, `--concurrency <n>`  | `1`                                                                            | Run up to this many agent runs at once, from 1 to 8. They share your account's rate limit, so this shortens wall-clock time rather than raising throughput past that limit. Results keep case order                                                                                        |
| `--model <model>`          | Each case's `model`, else `ANTHROPIC_MODEL` if set, else Claude Code's default | Model for the agent under test. Pin it in CI so a model rollout isn't mistaken for a plugin regression                                                                                                                                                                                     |
| `--judge-model <model>`    | A small fast model                                                             | Model for `llm` and `baseline` graders                                                                                                                                                                                                                                                     |
| `--ablation <mode>`        | `with-without` when a plugin resolves, else `none`                             | Whether to also run each case without the plugin to measure what it adds. `none` runs one arm; `with-without` adds the no-plugin baseline                                                                                                                                                  |
| `--threshold <0..1>`       | `1.0`                                                                          | A case passes when its with-arm score is at least this. Any case below it makes the command exit 1                                                                                                                                                                                         |
| `--max-cost-usd <usd>`     | No ceiling                                                                     | A ceiling on the run's list-price cost estimate, not on plan usage. Checked before each run starts. Once spent, nothing further starts; runs already in flight finish, so spend can pass the ceiling by those runs. If any run is left unstarted, the command exits 2 with partial results |
| `--allow-tools <tools...>` | None                                                                           | Grant tools beyond the read-only set. See [Grant tools](#grant-tools)                                                                                                                                                                                                                      |
| `--scaffold`               | Off                                                                            | Run each case's [`scaffold_script`](#add-setup-or-history-with-case-yaml)                                                                                                                                                                                                                  |
| `--trust-plugin`           | Off                                                                            | Skip the first-run trust prompt for a plugin whose code and suite you'd run yourself. Pass it in CI so the job is never refused by or left waiting at the prompt. See [What a run can access](#security)                                                                                   |
| `--mocks <mode>`           | `record`                                                                       | `record` answers MCP tool calls from [mocks](#mock-mcp-servers), doesn't start the plugin's real servers, and saves agent-mock answers for replay. `off` ignores mocks and starts the plugin's real MCP servers                                                                            |
| `--allow-real-servers`     | Off                                                                            | With `--mocks record`, also start the plugin's real MCP servers for servers that have no mock                                                                                                                                                                                              |
| `--json [path]`            | Off                                                                            | Print the [result document](#json-result) to stdout, or write it to a path ending in `.json`. The run is quiet: no progress lines or summary table                                                                                                                                         |
| `--output-dir <dir>`       | `<eval dir>/results/<timestamp>/`                                              | Where `aggregate-result.json` and `report.html` go                                                                                                                                                                                                                                         |
| `--no-publish`             |                                                                                | Keep the HTML report local. See [HTML report](#html-report)                                                                                                                                                                                                                                |
| `--publish-report`         |                                                                                | Publish the report even where it would stay local by default, such as a run a Claude Code session started                                                                                                                                                                                  |
| `--keep-temp`              | Off                                                                            | Keep every run's sandbox directory and print its path, for debugging what Claude produced                                                                                                                                                                                                  |

<h3 id="run-evals-in-ci">
  Run evals in CI
</h3>

In your CI job, run the suite with `--json` to write the result for archiving, and fail the build on the exit code. Pass `--trust-plugin` so the job never waits at the [first-run trust prompt](#security), pin both models so scores are comparable over time, keep the report local, and set a cost ceiling as an upper limit:

```bash theme={null}
claude plugin eval . \
  --trust-plugin \
  --json results.json \
  --threshold 0.8 \
  --model claude-sonnet-5 \
  --judge-model claude-haiku-4-5 \
  --no-publish \
  --max-cost-usd 20
```

The job's exit code tells you what happened:

| Exit code | Meaning                                                                                                                                                                                                        |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0         | Every case scored at or above `--threshold` and every case file loaded                                                                                                                                         |
| 1         | A case scored below the threshold, a case file failed to load, no cases were found, a run couldn't be started, the plugin directory isn't trusted and `--trust-plugin` wasn't passed, or an option was invalid |
| 2         | Partial run: the `--max-cost-usd` ceiling was hit, or your credential was rejected before or at the first run. `results.json` is still written with `partial: true` and the reason                             |
| 130       | Interrupted. Partial results are written                                                                                                                                                                       |
| 143       | Terminated, such as by a CI timeout                                                                                                                                                                            |

Problems writing or publishing the HTML report never change the exit code. With `--json` the run prints no progress or per-case diagnostics, so to see why a case scored low, run it locally without `--json`.

A CI runner needs a Claude Code install and [credentials in the environment](/docs/en/authentication) such as `ANTHROPIC_API_KEY`. Without `--trust-plugin`, a job whose checkout directory Claude Code doesn't already trust is refused with exit 1 when it has no terminal, or waits at the prompt when the runner allocates one. `claude plugin eval init` needs a terminal to ask you its questions; in CI, run `claude plugin eval init --bare <name>` to get the blank template.

To keep costs predictable, give quick every-change suites only graders that don't call a judge, use `--ablation none` where you don't need `Δ`, and leave `partial: true` documents and runs with `skippedPaidGraders` out of any trend you chart.

## Read the results

Every run with at least one case writes a `results/<timestamp>/` directory inside the eval directory, containing `aggregate-result.json` and `report.html`. For a path target that's under the plugin; for a plugin you named, it's under your current directory, as the [target table](#choose-what-to-evaluate) shows. The summary table, the JSON, and the report all render the same result data.

### HTML report

`report.html` shows the suite's scores and `Δ`, then each case with its prompt, its graders, and every run's verdicts and explanations. It's a single self-contained file that makes no external requests, so you can attach it to a CI job or open it from disk.

If you're signed in with a claude.ai subscription and [artifacts](/docs/en/artifacts) are available for your account, Claude Code also publishes the report as a private artifact and prints `Published: <url>`. Pass `--no-publish` to keep it local. If no `Published:` line appears, such as with API-key authentication, the local file is the report.

A run that a Claude Code session started, such as when you ask Claude to run the suite for you, also stays local, and its `Report:` line says `kept local`. Add `--publish-report` to that command to publish it.

### JSON result

`aggregate-result.json`, and `--json` output, is a versioned document with `schemaVersion: 1` for CI scripts to parse. Field names are camelCase and new fields are added without renaming existing ones, so write your script to ignore fields it doesn't recognize.

These are the fields a gating script usually reads. The document also carries the suite configuration, every grader definition, and per-run grader results with explanations and evidence:

| Field                                             | Meaning                                                                                                                                                                                  |
| :------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `partial`, `partialReason`                        | `true` with `cost_ceiling`, `interrupted`, or `auth_failed` when the suite didn't finish. Leave partial results out of trend charts                                                      |
| `aggregates.overallScore`                         | Mean case score across the suite                                                                                                                                                         |
| `aggregates.casesPassed`, `aggregates.casesTotal` | Cases at or above `--threshold`, and the total                                                                                                                                           |
| `aggregates.meanDelta`                            | Mean `Δ` across cases, under the two-arm mode                                                                                                                                            |
| `cases[].name`                                    | Case name                                                                                                                                                                                |
| `cases[].aggregates.score`                        | Mean with-arm run score for the case                                                                                                                                                     |
| `cases[].aggregates.delta`                        | With-arm score minus without-arm score. Omitted when the arms aren't comparable                                                                                                          |
| `cases[].arms.with[].error`                       | `null`, or why a run ended abnormally, such as `timed out after 300s`. A run that started but ended badly is still graded on what it produced, so a non-null error doesn't imply score 0 |
| `cases[].arms.with[].aborted`                     | Present when a [mock](#mock-mcp-servers)'s `expect:` or `abort_when` stopped the run, with `server`, `tool`, and `reason`. The run scores 0 and `error` stays `null`                     |
| `cases[].arms.with[].skippedPaidGraders`          | `true` when the cost ceiling skipped this run's judge graders, so its score isn't comparable                                                                                             |
| `costUsd`, `durationSeconds`, `claudeVersion`     | Estimated cost at list price including judge calls, wall-clock seconds, and the Claude Code version that ran the suite                                                                   |

<h2 id="security">
  What a run can access
</h2>

`claude plugin eval` loads the target plugin's skills and hooks and runs its eval suite on your machine, as you. Pointing it at a plugin is the same trust decision as `claude --plugin-dir`, so only evaluate plugins you trust. The isolation described in this section limits what the agent under test can reach; it isn't a boundary against the plugin's own code, and a suite that passes says nothing about whether the plugin is safe.

### Trust the plugin directory

The first time you run `claude plugin eval` against a directory, Claude Code asks `Trust this plugin directory?` before it loads anything from it, unless you already accepted the trust prompt there in an interactive `claude` session. Inside a git repository, answering yes trusts the whole repository, for interactive sessions too. When stdin or stdout isn't a terminal, or under `--json`, the run can't ask and is refused with exit 1; pass `--trust-plugin` to assert the trust yourself, only for a plugin you'd run on your own machine. A target you name rather than give as a path, meaning an installed plugin or a skills-directory plugin, skips the prompt.

Some parts of the plugin and suite run only when you pass their flag for that run: a case's [`scaffold_script`](#add-setup-or-history-with-case-yaml) with `--scaffold`, [tools beyond the read-only set](#grant-tools) with `--allow-tools`, and the plugin's [real MCP servers](#mock-mcp-servers) with `--allow-real-servers` or `--mocks off`. A case's `allowed_tools` and a skill's own `allowed-tools` frontmatter can't widen any of them. When the plugin ships hooks you didn't write, or you start its real MCP servers, treat its scores as advisory unless you ran it in an isolated environment such as a container or CI runner, since hooks and servers run outside the agent's sandbox and could touch the files the graders read.

<h3 id="how-runs-are-isolated">
  How runs are isolated
</h3>

Each run gets a throwaway home directory, working directory, and Claude Code configuration, and the agent under test runs there as a `claude -p` child process with only your plugin loaded. Keep these consequences in mind when you write cases:

* **Nothing personal or project-level loads.** Your user settings, hooks, `CLAUDE.md` files, MCP servers, other installed plugins, memory, and skills are absent, and no project-scoped `.claude/` or `.mcp.json` above the sandbox is read. Most of your shell environment is withheld too; only an [allowlist](#prompt-md-fields) and `EVAL_*` variables reach the run. If the plugin needs setup, ship it in the plugin, create it in a `scaffold_script`, or pass `EVAL_*` variables.
* **Managed policy can still restrict a run.** Restrictions in [managed settings](/docs/en/managed-settings) an administrator deployed to the machine apply inside a run, so results on a managed machine can differ from an unmanaged one by that policy.
* **The Artifact tool is off.** A skill that publishes an [artifact](/docs/en/artifacts) can be graded only on what it produces before that step.
* **The case definitions are hidden from the agent.** A run can't read the eval directory, so Claude can't see the case's prompt, its graders, or sibling cases.
* **No network sandbox outside shell commands.** Shell commands you grant run under the sandbox's network rules. A `WebFetch(domain:…)` grant reaches that domain directly, and the plugin's own hooks and any real MCP servers you start can reach any host.

## Eval suite reference

Everything an eval suite can contain lives under the plugin's eval directory, `evals/` unless you [configured another](#use-a-different-eval-directory). This tree shows every file `claude plugin eval` reads or writes there; only `prompt.md` or `case.yaml` is required for a case to exist:

```text theme={null}
evals/
├── <case>/                        # one directory per case; nest under a non-case directory to group
│   ├── prompt.md                  # frontmatter: case and run fields; body: the prompt
│   ├── case.yaml                  # optional: context.* fields, or the whole case in one file
│   ├── graders/
│   │   └── <name>.md              # one grader per file; frontmatter: type and options; body: rubric
│   ├── mocks/                     # optional: mocks for this case only, same layout as below
│   └── <fixtures, scripts, transcripts referenced by case.yaml>
├── mocks/                         # optional: suite-wide MCP mocks
│   ├── <server>/
│   │   ├── <tool>.md              # one mocked tool; body: the tool result
│   │   ├── _server.md             # optional: one agent that answers several tools
│   │   ├── _tools.json            # optional: saved tools/list response for real descriptions and schemas
│   │   └── fixtures/              # files inserted with {{file:fixtures/...}}
│   └── .replay/<server>/          # adopted agent-mock recordings, answered without a model call
└── results/<timestamp>/           # written by each run; add results/ to .gitignore
    ├── aggregate-result.json
    ├── report.html
    └── mock-recordings/           # agent-mock answers from clean runs, with ADOPT.txt
```

<h3 id="prompt-md-fields">
  prompt.md frontmatter
</h3>

`prompt.md` frontmatter accepts these fields. An unknown key is an error:

| Field                  | Default                      | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :--------------------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                 | The directory name           | Case name. `--case` globs match it and the report keys on it                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `description`          |                              | For humans. Not used at run time                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `tags`                 | `[]`                         | Labels for `--tag` filtering. A case runs if any of its tags matches                                                                                                                                                                                                                                                                                                                                                                                                          |
| `plugins`              | The nearest enclosing plugin | Plugin directories under test, relative to the case directory. Set `plugins: ["../.."]` when auto-detection doesn't find your plugin; see [the plugin didn't load](#the-baseline-arm-shows-no-plugin-or-delta-is-zero)                                                                                                                                                                                                                                                        |
| `runs`                 | `3`                          | Runs per arm, 1 to 50. `--runs` overrides it                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `expected_outcome`     |                              | For humans. Not used at run time                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `model`                | The child session's default  | Model for the agent under test. `--model` overrides it                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `max_turns`            | `10`                         | Turn cap, up to 200. Hitting it is recorded as a run error and usually lowers the score, so set it generously                                                                                                                                                                                                                                                                                                                                                                 |
| `timeout_seconds`      | `300`                        | Wall-clock cap per run, up to 3600                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `allowed_tools`        | `[]`                         | Tools the case wants, such as `[Read, Glob, Grep, Skill]`. Read-only tools are granted when listed here; for anything else, see [Grant tools](#grant-tools)                                                                                                                                                                                                                                                                                                                   |
| `append_system_prompt` |                              | Text appended to the child session's system prompt                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `env`                  | `{}`                         | Extra environment variables for the child session. Keys must match `EVAL_[A-Z0-9_]*`; any other key fails the run. The run inherits only an allowlist from your shell: basics such as `PATH` and locale, proxy and certificate settings, the variables that select and authenticate your model provider, most `ANTHROPIC_*` and `CLAUDE_CODE_*` configuration, and `EVAL_*`. To hand the plugin anything else, such as a toolchain setting, export it as an `EVAL_*` variable |

<h3 id="case-yaml-fields">
  case.yaml fields
</h3>

`case.yaml` describes the same case in YAML and adds the fields that point at other files. It requires `schema_version: "1.1"` and `name`. The `prompt.md` fields `description`, `tags`, `plugins`, `runs`, and `expected_outcome` go at the top level; `model`, `max_turns`, `timeout_seconds`, `allowed_tools`, `append_system_prompt`, and `env` go under `execution:`. When both files exist, `prompt.md` frontmatter overrides the matching `case.yaml` fields, the `prompt.md` body is the prompt, and `graders/*.md` are added after any graders listed in `case.yaml`.

These fields exist only in `case.yaml`:

| Field                     | Purpose                                                                                                                                                                                                                 |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context.scaffold_script` | A Bash script in the case directory that runs in the empty workspace before Claude starts, to create fixture files or a git repository. It runs only when you pass [`--scaffold`](#add-setup-or-history-with-case-yaml) |
| `context.history_file`    | A `.jsonl` transcript in the case directory to resume. The case's prompt becomes the next user turn                                                                                                                     |
| `context.add_dirs`        | Directories inside the case directory that Claude may read during the run, granted read-only                                                                                                                            |
| `execution.prompt`        | The prompt, when you keep the whole case in `case.yaml` and omit `prompt.md`                                                                                                                                            |
| `graders`                 | A list of graders, each with a `name` plus the same keys a `graders/*.md` file takes in frontmatter. For `llm` graders, put the rubric in `criteria`                                                                    |

### Grader frontmatter

Every grader file under `graders/` takes these keys in frontmatter, plus the options for its type. The grader's name is the filename without `.md`:

| Key      | Default  | Purpose                                                                                                                                                                     |
| :------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`   | required | One of the [grader types](#grader-types)                                                                                                                                    |
| `weight` | `1`      | Relative weight in the run's score. Any positive number                                                                                                                     |
| `arm`    | unset    | `with-only` excludes the grader from scoring in a [two-arm run](#compare-against-a-no-plugin-baseline); `both` forces a `tool_used: Skill` grader to be scored in both arms |

#### What a grader can look at

`regex` graders take a `target` and `llm` graders take a `focus`. Both accept the same values:

| Value                            | What the grader sees                                                                                                                                                                                                                                                                                           |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `last_message`                   | Claude's final response text. This is the default                                                                                                                                                                                                                                                              |
| `trace`                          | The whole session as JSON, one message per line. Quotes and newlines inside it are JSON-escaped, so a regex matches `\"` rather than `"`.                                                                                                                                                                      |
| `files`                          | The list of paths Claude created during the run, one per line. Not their contents, and not files that a scaffold created or that Claude only modified                                                                                                                                                          |
| `{ source: file, path: <path> }` | The contents of one file in the workspace after the run. Use this to grade what the plugin produced. A PNG, JPEG, GIF, or WebP file is shown to an `llm` judge as an image. An `llm` judge refuses other binary files such as `.pptx` or PDF; render them to an image or write them out as text and grade that |
| `mock_calls`                     | Each call Claude made to a [mocked MCP tool](#mock-mcp-servers), with its input and the mock's answer                                                                                                                                                                                                          |

#### Grader types

Each grader type below lists its options and when it passes:

| Type          | Options                               | Passes when                                                                                                                                                                                                                  |
| :------------ | :------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `regex`       | `pattern`, `flags`, `match`, `target` | The JavaScript regex `pattern` is found in the target. Set `match: not_contains` to require absence or `match: "count:N"` to require exactly N matches. Put case-insensitivity in `flags: i`; inline `(?i)` isn't supported  |
| `tool_used`   | `tool`, `input_match`, `min`, `max`   | The number of calls to `tool` whose JSON-encoded input matches the optional `input_match` regex is between `min`, default 1, and `max`, default unlimited. To assert a tool was never called, set both `min: 0` and `max: 0` |
| `tool_order`  | `before`, `after`                     | Both tools were called and the first matching `before` call precedes the first matching `after` call. Each is a tool name or `{ tool, input_match }`                                                                         |
| `file_exists` | `path`, `exists`                      | A file Claude created matches the `path` glob, or none does with `exists: false`. Only files created during the run count                                                                                                    |
| `llm`         | `criteria`, `focus`                   | A judge model votes PASS on the rubric in at least two of three votes. In the `.md` layout the file body is the criteria                                                                                                     |
| `baseline`    | `baseline_file`, `criteria`           | A judge finds the run satisfies the criteria at least as well as the reference transcript at `baseline_file`, a `.jsonl` in the case directory                                                                               |

<h3 id="mock-files">
  Mock files
</h3>

A `<tool>.md` file under `mocks/<server>/` answers one tool. Its body is the tool result, with `{{input.<field>}}` and `{{file:fixtures/<name>}}` substitutions. Its frontmatter accepts these keys:

| Key          | Default | Purpose                                                                                                                                                                                                                                                                             |
| :----------- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | `fixed` | `fixed` returns the body as written. `agent` treats the body as instructions for a small model that plays the server for the run and sees earlier calls as history                                                                                                                  |
| `expect`     | unset   | A map from dotted input paths to a type name such as `string`, `number`, `boolean`, `array`, or `object`, a `/regex/`, a literal, or a list of allowed literals. A call that violates it aborts the run with score 0 and is reported as `aborted` with the server, tool, and reason |
| `error`      | `false` | `fixed` only. Return the body as a tool error                                                                                                                                                                                                                                       |
| `abort_when` | unset   | `agent` only. Prose listing the only conditions under which the agent may abort the run                                                                                                                                                                                             |

Two optional files sit beside the tool files in a server's directory:

* **`_server.md`**: a single `type: agent` mock that answers several tools, listed in its `tools:` frontmatter key. A `<tool>.md` for the same tool takes precedence. Put an `expect:` guard on the individual `<tool>.md`, not here
* **`_tools.json`**: a saved `tools/list` response from the real server, so mocked tools carry their real descriptions and input schemas instead of a permissive placeholder

A case's own `mocks/` directory uses the same layout and overrides the suite's mocks file by file.

## Troubleshooting

These are the problems authors hit most often, keyed on what you see.

### "plugin eval is currently in early access"

Your build predates general availability of the command. Run `claude update`, then run the command again in a fresh session.

### "plugin eval is currently unavailable"

Anthropic has switched the command off server-side. Nothing on your machine turns it back on; run `claude update` and try again in a fresh session later.

### "is not a trusted plugin directory, and this run cannot stop to ask you about it"

This is the first run against a directory Claude Code doesn't trust yet, and it can't ask you because stdin or stdout isn't a terminal or you passed `--json`. Run `claude plugin eval <dir>` once in a terminal and answer the prompt, or pass `--trust-plugin` if you trust the plugin's code and suite. See [What a run can access](#security).

### "No eval cases found"

No `<case>/prompt.md` or `<case>/case.yaml` exists beneath the eval directory in effect, or your `--case` and `--tag` filters matched no case. Run from the plugin root, or run `claude plugin eval init` to create a suite.

### The baseline arm shows no plugin, or delta is zero

If the summary has no `W/OUT` column, or the case fails with "ablation requested but no plugin resolved", no plugin was found for the case. Add `plugins: ["../.."]` to the case, giving the path from the case directory to the plugin directory.

If the plugin did load and `Δ` is still near zero with your `tool_used: Skill` grader failing, that's usually a real finding, meaning the skill's `description` doesn't trigger on the prompt's phrasing. Adjust the description and re-run the same suite.

### Everything scores zero although the right files were produced

Your graders target `files`, the list of created paths, when you meant the file's contents. Use `{ source: file, path: <path> }` as the `target` or `focus`. Separately, `file_exists` counts only files created during the run, so a file the scaffold created or that Claude only edited is invisible to it; grade its contents, or use `tool_used` on `Edit`.

### A regex over the trace doesn't match text I can see

The default `target` is `last_message`, not the trace. When you do target `trace`, it's JSON per line, so quotes appear as `\"`. Regexes use JavaScript syntax, so put `i` in `flags` rather than writing `(?i)`.

### Tools are denied, MCP tools are missing, or Bash won't run

Anything beyond the read-only set needs your grant, such as `--allow-tools Bash Write`. Your personal MCP servers never load in a run. The plugin's own servers don't start unless you [opt in](#mock-mcp-servers), and their tools then also need an `--allow-tools "mcp__plugin_<plugin>_<server>__*"` grant; a mocked tool needs neither.

### The run exits 1 but the results look fine

The default `--threshold` is 1.0, so the command exits 1 when any case scores below perfect. Set a threshold that matches your bar. Exit 1 also covers a case file that failed to load, which is reported on stderr above the table.

### "--json output path must end in .json"

You put the target after `--json`, so it was read as the output path. Put the target first, as in `claude plugin eval . --json`, or give `--json` an explicit `.json` path.

### A grader shows passed: false under a run that scored 1.0

That grader is excluded from the score by design in a two-arm run, and its `scored` field is `false`. See [Compare against a no-plugin baseline](#compare-against-a-no-plugin-baseline).

### Runs fail with a usage-limit or rate-limit error partway through

If your account reaches its plan's usage limit or an API rate limit while a suite is running, each later run ends with that error, is graded on what it produced, and usually scores 0. The suite still finishes and isn't marked `partial`, so the result can look like a regression. Check the `NOTES` column or `cases[].arms.with[].error` in the JSON for the limit message before trusting the scores, then re-run after the limit resets, with `--runs 1` or a `--case` filter if you need to stay under it.

### Runs time out or hit the turn cap

The defaults are 10 turns and 300 seconds. Raise `max_turns` and `timeout_seconds` in the case for tasks that need more, and use `--max-cost-usd` as the cost ceiling rather than tight per-run limits.

## See also

* [Create plugins](/docs/en/plugins): build the plugin you're testing, and load it with `--plugin-dir` during development
* [Plugins reference](/docs/en/plugins-reference#plugin-eval): the `plugin eval` and `plugin eval init` command entries and the manifest's `experimental.evals` key
* [Skills](/docs/en/skills): how a skill's description decides when Claude invokes it, which is what a case that checks whether the skill triggers is measuring
* [Sandboxing](/docs/en/sandboxing): the OS-level sandbox that applies when you grant Bash to a run
* [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces): publish the plugin once its suite passes
