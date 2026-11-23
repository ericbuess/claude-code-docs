> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Approvals classifiers

> Let a Claude Approvals rule depend on Code Review's answer or on a question you define. Add a classifier, read its answer, and limit what a run costs.

In [Claude Approvals](https://code.claude.com/docs/en/approvals.md), the rules in your [policy file](https://code.claude.com/docs/en/approvals-policy.md) decide who has to approve a pull request. A classifier lets a rule depend on a judgment about the change, such as whether Code Review passed or how risky the change is. For example, a rule can ask for two people, and for only one when a classifier rates the change as low risk.

A rule can decide from paths, facts, and classifiers:

* **Paths**: which files the pull request changes
* **[Facts](https://code.claude.com/docs/en/approvals-policy.md#if)**: details of the pull request itself, such as how many lines changed or who opened it
* **Classifiers**: the answer to a question about the change. Use one for what paths and facts can't express

Claude Approvals is in [public beta](https://code.claude.com/docs/en/approvals.md#availability) for organizations on Team and Enterprise plans.

## How a classifier works

A classifier has a name, a question, and the answers that it can give. Its answer reaches a rule in these steps:

1. **Choose or define a classifier**: `claude/code_review` and `claude/diff` [come with Claude Approvals](#classifiers-anthropic-provides). A custom classifier is a folder in your repository, `.claude/classifiers/<name>/`, on the default branch
2. **Name it in a rule**: write the classifier's name in a rule's condition in your policy file, `.claude/approvals.yml`. For a custom classifier in the folder `change_risk`, the name is `repo/change_risk`, as in `"repo/change_risk = low"`
3. **Approvals runs it on a pull request**: for example, when a pull request opens ready for review and changes a file that the rule matches. See [When a classifier runs](#when-a-classifier-runs). Each run that calls a model is [billed](#what-a-classifier-run-costs) to your organization's usage credits
4. **The rule uses the answer**: the answer helps decide who has to approve. It shows under **Classifier results** in Claude's comment on the pull request, unless a [`reuse`](https://code.claude.com/docs/en/approvals-policy#reuse) condition reads it

## Example classifier definition

You define a custom classifier in a file named `def.yml`. The file holds the question for the model, in `prompt`, and the answers that the model can pick, in `outputs`.

This example defines a classifier named `change_risk`. Its `prompt` asks the model to rate how risky a change is, and its `outputs` lets the model answer `low`, `medium`, or `high`:

```yaml theme={null}
# .claude/classifiers/change_risk/def.yml
version: 1
description: "How risky is this change to ship?"
model: opus
prompt: |
  Rate how risky this change is to ship.
  high: it touches sign-in, billing or a data migration.
  medium: it changes behavior a user can see.
  low: anything else.
  When two ratings fit, pick the higher.
outputs:
  risk: { type: ordinal, values: [low, medium, high] }
```

Each key in the example does one job:

| Key | In this example |
| :- | :- |
| `version` | The format's version, `1` |
| `description` | One line that says what the classifier asks |
| `model` | The Claude model that answers, here the newest Opus model |
| `prompt` | The question. It says what each rating means, and which one to pick when two fit |
| `outputs` | The answers that the model picks from. This classifier has one output, `risk`, and its `values` run from least to most |

A definition can also set `inputs`, `tools`, and `budget`. See [Classifier definition file keys](#classifier-definition-file-keys).

### Use the example's rating in a rule

A classifier takes its name from its folder. The example is saved at `.claude/classifiers/change_risk/def.yml`, so you write `repo/change_risk` in your policy file's rules.

To use the rating, compare it with a value in a rule's condition. For example, `if: "repo/change_risk = low"` is true when the model answered `low`. For a rule that asks for fewer people under that condition, see [Read a classifier's answer from a rule](#read-a-classifier’s-answer-from-a-rule).

## Classifiers Anthropic provides

Claude Approvals comes with prebuilt classifiers, `claude/code_review` and `claude/diff`. To use one, write its name in a condition in one of your rules.

### `claude/code_review`

`claude/code_review` tells a rule whether [Code Review](https://code.claude.com/docs/en/code-review.md) passed. For example, `if: "claude/code_review = pass"` is true while its answer is `pass`.

`claude/code_review` gives one of these answers:

| Answer | When |
| :- | :- |
| `pass` | A review finished with no [Important finding](https://code.claude.com/docs/en/code-review-pull-requests.md#severity-levels) open |
| `fail` | A review finished with an Important finding open |

You can read it in any condition, or list it under [`advisory`](https://code.claude.com/docs/en/approvals-policy#advisory).

* **To read the severity of its open findings**: write `claude/code_review.severity`, which is `none`, `minimal`, or `high`
* **To let people turn `fail` into `pass`**: name them in your policy's [`findings`](https://code.claude.com/docs/en/approvals-policy#findings) lists. They do it by closing the Important findings

### `claude/diff`

`claude/diff` tells a rule how much a pull request changed since an approval or an earlier answer. It answers `trivial`, `same_intent`, or `different`.

Read it in a condition under [`reuse`](https://code.claude.com/docs/en/approvals-policy#reuse), which says what continues to count after a push.

## Add a custom classifier

With a custom classifier, you write a question about a pull request, and a Claude model answers it. You define the classifier in a file in your repository, then name it in a rule:

1. **Define the classifier**: create a folder under `.claude/classifiers/`, named in lower-case letters, digits, and `_`. In it, save a [`def.yml`](#classifier-definition-file-keys) that holds the question and the answers to pick from. In a rule, you write the folder `change_risk` as `repo/change_risk`.
2. **Name it under `advisory`**: in the root `.claude/approvals.yml`, pick a rule that has a `verdict` and whose `paths` match the files that you want judged, and list the classifier under that rule's [`advisory`](https://code.claude.com/docs/en/approvals-policy#advisory). Under `advisory`, the classifier runs and [is billed](#what-a-classifier-run-costs), and decides nothing.
3. **Merge both files**: open one pull request with both, and Claude comments on the pull request. If the rule that you edited is enforced, expect a warning that says "rules still hold on these files", which doesn't block the merge. Merge the pull request once the **Policy files in this change** section of that comment reports no refusal.
4. **Read its answers**: open a pull request that changes those files, and [look for the answer](#when-a-classifier’s-answer-appears) in Claude's comment.
5. **Let a rule depend on it**: once you trust the answers, [read them from a rule](#read-a-classifier’s-answer-from-a-rule).

### When a classifier's answer appears

After you merge a classifier's definition and the rule that names it, wait five minutes. Then open a pull request that isn't a draft and that changes a file that rule's `paths` match. Look for the classifier's line in one of these places:

* **Claude's comment**: under **Classifier results**
* **The Claude Approvals check's summary**: under **Advisory classifiers (not counted toward this verdict)**

At first, the line reads "no result recorded yet". A run can take up to 10 minutes, or longer where the classifier's `def.yml` sets a longer [time limit](#budget). Under an enforced rule, the line stays as it is when the run ends.

The answer shows the next time Approvals evaluates the pull request, for example when someone approves it or requests changes. The line then reads, for example, "`repo/change_risk`: reported `low` (advisory)".

* **The line still shows no result**: wait until the run's time limit is up, then have someone approve the pull request or request changes
* **Your classifier has no line**: check that the rule that names the classifier has a `verdict`, and that its `paths` match the file you changed

## Read a classifier's answer from a rule

To make a rule depend on a classifier's answer, write the classifier's name in a condition: the rule's own `if`, or the `if` of an [`override`](https://code.claude.com/docs/en/approvals-policy#override). Once `repo/change_risk` answers well under `advisory`, move its name into an override's `if`.

Keep the strict verdict on the rule itself, because the rule's verdict applies [when a run gives no answer](#what-a-rule-sees-when-a-classifier-run-gives-no-answer).

This rule asks for two people, and for one while `repo/change_risk` answers `low`:

```yaml theme={null}
# .claude/approvals.yml
version: 1
rules:
  - purpose: "Two people. One is enough when the risk is low."
    paths: ["**"]
    verdict: { claude: comments, seats: 2 }
    override:
      - { if: "repo/change_risk = low", verdict: { claude: comments, seats: 1 } }
```

### Ways to read a classifier in a condition

A condition can read a classifier in these forms:

| Form | Example | Reads |
| :- | :- | :- |
| Name alone | `"repo/change_risk <= medium"` | The only output |
| `.output` | `"repo/api_review.breaking = yes"` | One output by name. Required when the classifier's definition has several |
| `.severity` | `"repo/api_review.severity >= high"` | The worst open finding, from `none`, `minimal`, `low`, `medium`, `high`, or `critical`. Needs `findings` in `tools` |
| `(input=value)` | `"claude/code_review(level=deep) = pass"` | A run with that input. Code Review's `level` is `quick`, `standard`, or `deep` |
| `= error`, `= incomplete` | `"repo/change_risk = error"` | How a run ended with no answer |

## Classifier definition file keys

Write a classifier's definition in `def.yml`, which can be up to 64 KiB. For a whole file, see [Example classifier definition](#example-classifier-definition).

You can write these keys in `def.yml`:

| Key | Required | Values |
| :- | :- | :- |
| `version` | Yes | `1`, as a bare number |
| `description` | Yes | One line, up to 1,000 characters |
| `model` | Yes | A model family in lower case, such as `opus` or `sonnet`, or the exact Claude API ID of a generally available model from the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview). The model has to [support auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) |
| `prompt` | This or `prompt.md` | The question. For a long one, save `prompt.md` beside `def.yml`, up to 512 KiB |
| [`outputs`](#outputs) | No | A map of output names to their types and values |
| [`inputs`](#inputs) | No | A map of input names that a rule can set |
| [`tools`](#tools) | No | A list |
| [`budget`](#budget) | No | `{ time, cost }` |

If you name a model family, the classifier uses that family's newest model, so cost and answers can change with no pull request. If you name an exact ID, the classifier stops loading when that model is retired. Your organization's list of allowed models applies to these runs.

### `outputs`

Give each output a `type`, and write names and values in lower-case letters, digits, and `_`. Don't name an output `severity`, and don't use `true`, `false`, `error`, `incomplete`, or `complete` as a value. Put quotes around `"yes"` and `"no"`.

| `type` | Also needs | [Operators](https://code.claude.com/docs/en/approvals-policy.md#if) in a condition |
| :- | :- | :- |
| `criteria` | `values`, a list of words | `=`, `!=` |
| `ordinal` | `values`, least first | All six |
| `numeric` | `min` and `max`, whole numbers | All six |

### `inputs`

An input is a value that a rule can set for a run. Define each input under `inputs` in `def.yml`, then set it from a rule in parentheses after the classifier's name, as in `repo/change_risk(rigor=thorough)`. Give each input a `default`, and either `values` or `min` and `max`, as in `rigor: { values: [quick, thorough], merge: right, default: quick }`. Say in your prompt what each value changes.

An input's `merge` says what happens when rules ask for different values on one pull request:

| `merge` | What runs |
| :- | :- |
| `left`, `right` | One run, with the word that stands earlier or later in `values` |
| `min`, `max` | One run, with the smaller or larger number |
| `list` | One run, with every word asked for |
| Omitted | A separate billed run for each value |

### `tools`

List an entry under `tools` to let a run do more:

| Entry | Lets a run | Limit |
| :- | :- | :- |
| `findings` | Read parts of the pull request's review threads, report findings as new ones, and resolve or reopen its own | 16 open threads |
| `comment` | Post one comment | 5,000 characters |
| `code` | Read files beyond the diff | Read-only |
| `labels` | Add labels that the repository already has, and remove the ones it added | 8 labels. None whose name starts with `approvals:` or `claude-` |
| `reviewers` | Add reviewers, and remove the ones it added | 8 reviewers |

Approvals holds back some of a run's `tools` in observe mode and on some pull requests:

* **In observe mode**: a run keeps only `findings` and `code` from its `tools`. Approvals can list the findings in its own comment, and opens no new review threads. That holds while your policy file, or every rule that names the classifier and matches a changed file, says [`mode: observe`](https://code.claude.com/docs/en/approvals-policy#rule-keys).
* **On some pull requests**: a run adds no comment, label, review thread, or GitHub review request. Examples are a pull request from a fork, and one where an author lacks write access

#### `labels`

Don't grant `labels` where a label gates a merge, a deploy, or a workflow. A label that a run adds is a real label on the pull request, and anything that reads labels can act on it.

#### `reviewers`

Say in your prompt whom to add, by login. Where a rule that [applies](https://code.claude.com/docs/en/approvals-policy.md#how-rules-combine-into-one-verdict) [reads the classifier's answer](#read-a-classifier’s-answer-from-a-rule), the **Claude Approvals** check can wait for their approval, on top of [`seats`](https://code.claude.com/docs/en/approvals-policy#verdict). Name people who have write access. With a policy file in a subdirectory, [list the classifier only under `advisory`](https://code.claude.com/docs/en/approvals-policy#policy-files-in-subdirectories).

To drop a reviewer who can't approve, first merge a change to the prompt if it names that person, and allow five minutes. Then comment [`@claude approvals rerun`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals) on the pull request.

### `budget`

Set `time`, `cost`, or both under `budget`, as in `budget: { time: 300, cost: 5 }`. A run that reaches either limit stops, and a condition then reads `incomplete`. If you ask for more than the maximum, the run gets the maximum and Approvals warns you.

| Key | Unit | Default | Maximum |
| :- | :- | :- | :- |
| `time` | Whole seconds | `600` | `3600` |
| `cost` | Whole US dollars | `10` | `10` |

Approvals stops a run when its estimated spend reaches `cost`, and the bill can be higher. Under \$5, a run on a large pull request can stop before it answers.

## How a classifier run behaves

A rule's result can turn on when its classifier runs, what the run can read, and what happens when it gives no answer.

### When a classifier runs

A `repo/` classifier runs on a pull request only if you name it in a matching rule: in an `if`, an override's `if`, a `reuse` condition, or `advisory`. On a [pull request from a fork](https://code.claude.com/docs/en/approvals-pull-requests.md#pull-requests-from-forks-and-outside-contributors), `repo/` classifiers don't start before a maintainer vouches for the commit. For `claude/code_review`, see [when Approvals starts a review](https://code.claude.com/docs/en/approvals-setup.md#what-approvals-costs).

* **What can start a run**: a pull request opens ready for review, is marked ready, or is reopened. A push that changes the diff, a change of base branch, and a [rerun of the Claude Approvals check](https://code.claude.com/docs/en/approvals-pull-requests.md#comment-commands-for-approvals) can also start one. After [your policy stops observing](https://code.claude.com/docs/en/approvals-setup.md#enforce-your-policy-and-require-claude-approvals), Approvals evaluates some open pull requests by itself, which can start a run.
* **Which definition runs**: the default branch's copy of the definition and prompt. A pull request's own copy doesn't run. The folder's files are [protected files](https://code.claude.com/docs/en/approvals-policy.md#protected-files).
* **A changed definition ends earlier answers**: an edit to `def.yml` or `prompt.md` counts once it's on the default branch. An open pull request keeps its check until its next evaluation, such as a push or a rerun. That evaluation drops the earlier answer, and the classifier can run again.
* **After a push that changes the diff**: an earlier answer can count where [`reuse`](https://code.claude.com/docs/en/approvals-policy#reuse) keeps it, or where the push changes only covered files whose rules don't name the classifier
* **Order**: with `run: sequential`, the default, an override's classifiers normally wait for the overrides above it. With `run: parallel`, they can all start at once, which can bill runs that no verdict needed.

### What a classifier run can read and change

A `repo/` classifier's run is a Claude Code cloud session on Anthropic's infrastructure. If your organization requires self-hosted compute, a condition reads `error` in place of that run's answer.

Check what the session can read and what it can change:

* **What it can read**: the pull request's title, description, labels, author, changed files, diff, approvals, and required reviewers, the classifier's earlier runs, your policy files, and the files under `.claude/classifiers/`. With `findings` in `tools`, it reads parts of the review threads
* **What `code` adds**: read-only copies of files at the pull request's head and on the default branch, without some files, such as `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.mcp.json`, and files whose names end in `.pdf`
* **What it can change**: the session's GitHub access is read-only. Where [`tools`](#tools) lists an entry that writes, the run records what it asks for, and Approvals can carry it out after the run.

A run reads text that the pull request's author wrote, and that text can try to steer the classifier's answer. On paths that matter, [ask for a person](https://code.claude.com/docs/en/approvals-github-rules.md#ask-for-a-person-who-isn’t-an-author) in a rule that reads no classifier.

### What a rule sees when a classifier run gives no answer

When a run ends with no answer, a condition normally reads one of these values:

| A condition reads | When |
| :- | :- |
| `incomplete` | The run began and ended with no answer |
| `error` | The run couldn't start, was broken off, or outlasted the check's wait |

In both cases, an override that needs the answer leaves the rule's own `verdict` in place. A rule's own `if` that needs the answer fails the **Claude Approvals** check, with the title **A classifier had no result**.

To choose another verdict, put [an override](https://code.claude.com/docs/en/approvals-policy.md#override) on `= error` or `= incomplete` above the overrides that read the answer. An override can't choose another verdict for a missing answer in a rule's own `if`. Move the comparison that reads the classifier from the rule's `if` into an override.

## What a classifier run costs

A run that calls a model is billed to your organization's usage credits, by tokens:

| Classifier | What's billed |
| :- | :- |
| A custom classifier, `repo/<name>` | Each run. That includes runs in observe mode, runs under `advisory`, and runs that end with no answer. After an error, Approvals can start the run again by itself, more than once, and each of those runs is billed |
| `claude/diff` | Each answer that calls a model |
| `claude/code_review` | Billed as [Code Review](https://code.claude.com/docs/en/code-review-costs.md) |

### Limit what a custom classifier costs

You can cap one run, cap the month, pick a lower-cost model, or start fewer runs:

* **Cap one run**: in the classifier's `def.yml`, add `budget: { cost: 5 }`. Approvals stops a run when its estimated spend reaches that many US dollars, and the bill can be higher. With no [`budget`](#budget), the cap is \$10
* **Cap the month**: set a [spend limit for classifier runs](https://code.claude.com/docs/en/approvals-setup.md#limit-what-a-policy-costs) at [**Organization settings > Usage**](https://claude.ai/admin-settings/usage), which takes an Owner role
* **Pick a lower-cost model**: in `def.yml`, change `model`, for example from `opus` to `sonnet`
* **Start fewer runs**: make your edits to `def.yml` and `prompt.md` in one pull request. After each merged edit, the classifier runs again at each open pull request's next evaluation

## Related resources

* [Claude Approvals policy file reference](https://code.claude.com/docs/en/approvals-policy.md): conditions, overrides, `reuse`, and `findings`
* [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md): observe mode, enforcement, and spend limits
* [Troubleshoot Claude Approvals](https://code.claude.com/docs/en/approvals-troubleshooting.md): when a classifier gives no answer
* [Data usage](https://code.claude.com/docs/en/data-usage.md): how Anthropic handles data from Claude Code
