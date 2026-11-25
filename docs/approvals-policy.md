> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Approvals policy file reference

> Reference for the Claude Approvals policy file, `.claude/approvals.yml`: its keys, how rules combine, how approvals count, and an example policy.

A policy file, `.claude/approvals.yml`, tells [Claude Approvals](https://code.claude.com/docs/en/approvals.md) who has to approve a pull request and when Claude may approve it. Look up its keys here, how its rules combine, and how approvals are counted.

> [!TIP]
>
> To set up Approvals and require the **Claude Approvals** check, see [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md). To find out what a check's title means, see [Work with Claude Approvals on a pull request](https://code.claude.com/docs/en/approvals-pull-requests.md). For a file that the check refuses, see [Fix a policy file that Approvals refuses](https://code.claude.com/docs/en/approvals-troubleshooting.md#fix-a-policy-file-that-approvals-refuses). To define a `repo/<name>` classifier, see [Claude Approvals classifiers](https://code.claude.com/docs/en/approvals-classifiers.md).

## How a policy file works

A policy file is a list of rules. Each rule names the files that it's about, in `paths`, and says what a pull request that changes them needs:

* **`seats`**: how many people have to approve
* **`claude`**: whether Claude `approves`, `comments`, or `blocks`
* **`override`**: another verdict, which replaces the rule's own while its `if` is true

This policy file is the one that [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md#let-claude-approve-when-code-review-passes) starts from. It asks for two people to approve a change, or one person when Claude's review passes. In both cases, the pull request's author can count as one person:

```yaml theme={null}
# .claude/approvals.yml
version: 1
mode: observe
rules:
  - purpose: "A change takes two people. When Claude's review passes, one is enough and Claude approves."
    paths: ["**"]
    verdict: { claude: comments, seats: 2 }
    override:
      - { if: "claude/code_review = pass", verdict: { claude: approves, seats: 1 } }
  - purpose: "A change to the review rules takes two people."
    paths: ["**/.claude/**"]
    nested: inherit
    verdict: { claude: comments, seats: 2 }
```

Each line of that file does one job:

| Line | What it does |
| :- | :- |
| [`mode: observe`](#top-level-keys) | The **Claude Approvals** check shows what the rules would decide. Delete the line to enforce them |
| `purpose` | Says why the rule exists |
| [`paths: ["**"]`](#paths) | The first rule matches every file |
| [`verdict`](#verdict) | Two people have to approve, and [the author can count as one](#whether-a-pull-request’s-author-counts). Claude comments and doesn't approve |
| [`override`](#override) | While [`claude/code_review`](https://code.claude.com/docs/en/approvals-classifiers#classifiers-anthropic-provides) reads `pass`, one person, who can be the author, is enough and Claude can approve |
| `paths: ["**/.claude/**"]` | The second rule matches the files under any `.claude/` directory, which include the policy file |
| [`nested: inherit`](#policy-files-in-subdirectories) | Once you enforce the policy, keeps the second rule in force in subdirectories that have their own policy file |

A file under `.claude/` matches both rules. Approvals [takes the strictest of the verdicts that apply](#how-rules-combine-into-one-verdict), so once you enforce the policy, a change to that file needs two people, because the second rule has no `override`.

## Where to put a policy file

Save the policy file as `.claude/approvals.yml` in your repository's root, and merge it into the default branch. Approvals reads policy files from the default branch, so the file's rules apply once it's merged.

You can also name the file `.claude/approvals.yaml`, which Approvals reads where the `.yml` file is absent. To give a directory rules of its own, add [a policy file there](#policy-files-in-subdirectories).

### When a change to a policy file takes effect

While a change to a policy file is in an open pull request, Approvals can check the changed file for errors, and applies none of its rules. The rules on the default branch decide for that pull request.

Once the change merges, new pull requests get the new rules, and open ones get them from their next evaluation. Approvals can read the earlier copy for a few minutes more. To evaluate an open pull request now, comment [`@claude approvals rerun`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals).

### Policy files in subdirectories

To give a directory its own rules beside the root policy file, add a `.claude/approvals.yml` inside it, such as `services/billing/.claude/approvals.yml`.

For each changed file, Approvals walks up from that file's directory. The first enforcing policy file that covers the changed file, and in which a rule with a `verdict` [applies](#how-rules-combine-into-one-verdict), decides for it. A `nested: inherit` rule in a policy file higher up counts as one of the deciding policy file's rules.

* **The nearest policy file decides**: it can ask for less than the root policy file. Above it, only rules marked `nested: inherit` still count.
* **`paths` start at the directory**: in `services/billing/.claude/approvals.yml`, write `api/**` to match the files under `services/billing/api/`
* **`locals` reach down**: in a policy file, you can use the locals of the policy files above it
* **Each policy file has its own `mode`**: while the root policy file observes, none of its rules count under a directory's enforcing policy file, the `nested: inherit` rules included
* **Some custom classifiers go only under `advisory`**: that's a classifier whose [`tools`](https://code.claude.com/docs/en/approvals-classifiers#tools) list `reviewers` or `labels`, or that has an [input](https://code.claude.com/docs/en/approvals-classifiers.md#inputs) with no `merge`. List it in an enforced rule with no `if`. If a rule reads its result, the check on pull requests under a directory's policy file can read **Cannot evaluate: classifier outside advisory**

## Rules for the whole file

Follow these rules in every part of the file:

* **Keys and fixed values**: write keys, and fixed values such as `observe` and `approves`, in lower case. Approvals refuses a file that has an unknown key
* **Purposes, patterns, and conditions**: put double quotes around every purpose, `paths` pattern, and condition
* **`!` items**: put double quotes around each `"!"` item outside a condition. Inside a condition, a `!` item takes single quotes. Approvals refuses a file that has an unquoted `!` item
* **YAML**: keep the file to one YAML document, or Approvals refuses the file. Indent with spaces. Anchors, aliases, and `!!` tags draw at least a warning

## Top-level keys

Write these keys at the top level of the file:

| Key | Required | Values | Default | Description |
| :- | :- | :- | :- | :- |
| `version` | Yes | `1` | | The schema version, as a bare number |
| `rules` | Yes | List of [rules](#rule-keys) | | Rule order doesn't matter |
| `mode` | No | `enforce`, `observe` | `enforce` | `observe` shows what the rules would decide and holds for every rule in the file. For the checks that still aren't neutral, and for pull requests into other branches, see [Approvals in observe mode](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-in-observe-mode) |
| `nested` | No | `overwrite`, `inherit` | `overwrite` | The default for this file's rules. See [Policy files in subdirectories](#policy-files-in-subdirectories) |
| `run` | No | `sequential`, `parallel` | `sequential` | The default for this file's rules. See [When a classifier runs](https://code.claude.com/docs/en/approvals-classifiers.md#when-a-classifier-runs) |
| `locals` | No | Map of names to values | | Values to reuse. See [`locals` and `use`](#locals-and-use) |

## Rule keys

Give each rule a `purpose`, `paths`, and at least one of `verdict`, `advisory`, `findings`, and `reuse`. If `reuse` is the only one of the four that a rule has, the value of `reuse` has to be `false` or name a classifier. A rule with no `verdict` asks nobody and [covers](#how-rules-combine-into-one-verdict) no file.

You can write these keys on a rule:

| Key | Type | Default | Description |
| :- | :- | :- | :- |
| `purpose` | One line of text | Required | Why the rule exists |
| [`paths`](#paths) | List of patterns | Required | The changed files that the rule matches |
| [`verdict`](#verdict) | Map | | What Claude does and who has to approve |
| [`if`](#if) | Condition | `true` | The rule applies only while the condition is true |
| [`override`](#override) | List | | Other verdicts, each under a condition |
| [`advisory`](#advisory) | List of classifiers | | Classifiers that run and decide nothing |
| [`reuse`](#reuse) | Condition or map | Keep nothing | What still counts after a push that changes the diff |
| [`findings`](#findings) | Map | No list | Who may close a classifier's finding |
| [`use`](#locals-and-use) | List of `"@name"` | | Locals whose keys are copied into the rule |
| `mode` | `enforce`, `observe` | The file's | A rule that observes neither [applies nor covers](#how-rules-combine-into-one-verdict) a file |
| `nested` | `overwrite`, `inherit` | The file's | `inherit` keeps the rule in force under the policy files below |
| `run` | `sequential`, `parallel` | The file's | Whether the rule's own classifiers start in turn or together |

### `paths`

Write each pattern as a path from the directory that holds the `.claude` folder. A moved file counts at its old path and its new one.

| Pattern | Matches |
| :- | :- |
| `*` | Any characters within one folder |
| `**` | Any number of folders, dot folders too. It has to be a whole segment, as in `**/*.go` |
| `{a,b}`, `[ab]`, `?` | Alternatives, one character of a set, and any one character |
| `infra/**` | Every file in the folder. A bare `infra` matches no file in it, and `infra/` is refused |
| `*.md` | Markdown files beside the policy file's `.claude` folder. For any depth, write `**/*.md` |
| `"!docs/**"` | Takes the files out of this rule only. A rule needs at least one pattern with no `!` |

### `if`

Write a condition as `true`, `false`, or one double-quoted string with a fact's or a classifier's name on the left, such as `"pr/files_changed > 50"`. When you give a rule an `if`, keep another rule with no `if` on the same paths. While the `if` is false, the rule that has it doesn't apply. Where rules cover a file and none applies, [the Claude Approvals check fails](#how-rules-combine-into-one-verdict).

* **Operators**: `=`, `!=`, `<`, `<=`, `>`, `>=`
* **Joining**: `AND` and `OR` in capitals. Use parentheses to mix the two.
* **Lists**: write `ANY` or `ALL` before `pr/authors` and `pr/approved_by`. Where the condition leads to a lighter verdict, use `ALL`: with `ANY`, one listed author relaxes the rule for everyone else's commits. Where it leads to a stricter one, use `ANY`: with `ALL`, one unlisted author switches it off. To test for an empty list, write neither, as in `"pr/approved_by = empty"`.
* **Quotes**: single quotes around a login, a branch pattern, or a whole `!` item in a [list of people](#people-lists), as in `"ANY pr/authors = [humans, '!acme/interns']"`. No quotes around a team, a `bot:` name, or a fact without a `!`, as in `"ALL pr/authors = ['ana-acme', acme/payments]"`
* **Classifiers**: `claude/code_review = pass`, `repo/change_risk <= medium`, and the other forms under [Read a classifier's answer from a rule](https://code.claude.com/docs/en/approvals-classifiers.md#read-a-classifier’s-answer-from-a-rule)

A fact comes from the pull request itself:

| Fact | Example | Holds |
| :- | :- | :- |
| `pr/files_changed`, `pr/files_added`, `pr/files_removed` | `"pr/files_changed > 50"` | Counts over the whole pull request |
| `pr/diff_lines` | `"pr/diff_lines <= 20"` | Changed lines in the whole pull request |
| `rule/files_changed`, `rule/files_added`, `rule/files_removed` | `"rule/files_changed = pr/files_changed"` | Counts among the files that this rule's `paths` match |
| `pr/authors` | `"ALL pr/authors = bot:dependabot"` | Accounts that wrote or pushed a commit, and the account that opened the pull request |
| `pr/opened_by` | `"pr/opened_by = acme/release"` | The account that opened the pull request. After someone else pushes to a bot's pull request, an override on `pr/opened_by = bot:dependabot` stops lowering what the rule asks for |
| `pr/approved_by` | `"ANY pr/approved_by = acme/security"` | People with write access who approved the current diff. Authors and bots aren't among them. Also takes `= empty` and `!= empty`, with no `ANY` or `ALL` |
| `pr/base` | `"pr/base = 'release/**'"` | The branch that the pull request targets |

### `verdict`

A `verdict` says what Claude does and who has to approve. In a rule's `verdict`, write `claude`, and write `seats` unless `claude` is `blocks`.

| Field | Values | Description |
| :- | :- | :- |
| `claude` | `approves`, `comments`, `blocks` | `approves`: Claude can post an approving review once the **Claude Approvals** check passes, if [every rule that applies says so and every changed file is covered](#how-rules-combine-into-one-verdict). The field starts no review, so where the rule reads no classifier, Claude can approve a change that no review has read. `comments`: Claude doesn't approve. `blocks`: the check fails, whoever approves |
| `seats` | `0` to `16`, or a list of up to eight sets | How many [people](#how-people’s-approvals-are-counted) have to approve. A number `N` is short for `[{ count: N, from: humans }]`. Refused beside `blocks` |
| `max_age` | A whole number and `s`, `m`, `h`, or `d`, from `1m` to `83d` | How long an evaluation's results count. After that, the check fails with the title **Results are older than the policy allows** |

Give each set in `seats` a `count`, from `1` to `16`, and a `from`, which is a [people list](#people-lists). Every set has to be filled, and one person can fill a seat in several sets.

### People lists

A people list names accounts. Write one as a set's `from` under [`seats`](#verdict), or under [`findings`](#findings), as one item or as a list in brackets. Only accounts with write access to the repository count.

| Item | Means |
| :- | :- |
| `humans` | Every person, authors included. A machine user, which is a user account that a script or an agent drives, counts as a person. The `claude` user account, which Claude's cloud sessions commit as, doesn't |
| `bots` | Every bot and GitHub App, Claude's apps and `github-actions` included |
| `everyone` | `humans` and `bots` together. Write it alone, with no brackets |
| `nobody` | Nobody. Write it alone, under `findings` only |
| `ana-acme` | One login. In a condition, put it in single quotes |
| `acme/payments` | A team of the repository's GitHub organization |
| `bot:dependabot` | One bot, with no `[bot]` suffix. `bot:claude` means Claude's apps |
| `pr/authors`, `pr/opened_by` | The accounts that the fact holds |
| `"!pr/authors"` | Takes accounts away. Quote it, with single quotes in a condition, and put it beside an item with no `!` |

If a set's `from` admits Claude, for example through `bots`, `everyone`, or `bot:claude`, and every rule that applies says `approves`, Approvals counts a seat in that set as filled before Claude approves. The **Claude Approvals** check can then pass with no person's approval.

### `override`

An override changes its rule's verdict while the override's own `if` is true. Approvals reads the `override` list from the top, and the first true override applies.

| Key | Required | Description |
| :- | :- | :- |
| `if` | Yes | A [condition](#if) |
| `verdict` | At least one of these three | Each field that it writes replaces the rule's. `seats` is replaced as a whole |
| `reuse`, `findings` | At least one of these three | Replaces the rule's whole value |
| `purpose`, `use` | No | As on a rule. Here `use` can copy `verdict` and `findings` |

When an override's `if` reads a classifier, the **Claude Approvals** check waits for the classifier's run:

* **The run is still going**: the check stays in progress. It can finish early when the approvals already meet every verdict that the rule could still pick, unless the classifier's `tools` list [`reviewers`](https://code.claude.com/docs/en/approvals-classifiers#reviewers). With a policy file in a subdirectory, [list such a classifier only under `advisory`](#policy-files-in-subdirectories)
* **The run ended with no answer**: reading stops at that override, and the rule's own `verdict` applies. Put the strict verdict on the rule for this reason.
* **You want to catch a missing answer**: put an override on `= error` or `= incomplete` above the ones that read the answer

In a rule's own `if`, a comparison with no answer fails the check, whoever approves, unless another part of the condition settles it.

### `advisory`

Under `advisory`, list classifier names or calls, such as `[claude/code_review, repo/change_risk]`. A `repo/` classifier listed here [can run](https://code.claude.com/docs/en/approvals-classifiers.md#when-a-classifier-runs), and each run is billed. List it in a rule that has a `verdict`.

To keep Code Review's automatic reviews, list `claude/code_review` here, or read it in an `if`, in a rule that has a `verdict` and matches the files you want reviewed.

### `reuse`

`reuse` says which earlier approvals and classifier answers continue to count after a push that changes the diff, under a condition that usually reads [`claude/diff`](https://code.claude.com/docs/en/approvals-classifiers#classifiers-anthropic-provides).

When `claude/diff`'s answer is at most `same_intent` and Claude's review of the new commit passes, this example can keep people's approvals:

```yaml theme={null}
# in .claude/approvals.yml, on a rule
    reuse:
      seats: "claude/diff <= same_intent AND claude/code_review = pass"
```

Write `reuse` in one of these forms:

| Form | Can keep |
| :- | :- |
| `seats: <condition>` | People's approvals |
| `<classifier>: <condition>` | That classifier's earlier answer |
| `reuse: <condition>` | Both: the seats and the classifiers that the rule reads |
| `false` | Nothing. `unset`, in an override, removes the rule's value |

Before you rely on `reuse`, check these cases:

* **Every rule that matches the files**: write `reuse` on each of them
* **When `claude/diff` gives no answer**: a condition that reads it keeps nothing
* **After a dismissal or a force-push**: the example keeps no approval that GitHub dismissed, and normally none given before a force-push. `reuse` can keep them under a `seats` condition that reads `claude/diff` and no other classifier, such as `"claude/diff <= same_intent"`.
* **Earlier authors count too**: where `reuse` keeps `seats`, people who held the [author's seat](#whether-a-pull-request’s-author-counts) at an earlier commit can continue to count. Two of them can fill `seats: 2` with nobody approving. To prevent that, exclude authors from the set with `"!pr/authors"`.
* **Files that a push left alone**: in a policy file that writes `reuse`, an approval can outlast a push to other files only. Those can be files that no rule covers, or whose rules couldn't count that person. An approval that GitHub dismissed normally doesn't

### `findings`

A classifier can report findings as review threads, and a condition can read their severity as `.severity`. Use `findings` to say who may close a finding, by resolving its thread or with [`@claude approvals resolve`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals).

Until a rule's `findings` lists who may close findings, a person's resolve alone doesn't lower `.severity`. A classifier needs no list to close its own finding, as Code Review can when a later review finds it fixed.

This example lets the `acme/leads` team, less the pull request's authors, close Code Review's findings:

```yaml theme={null}
# in .claude/approvals.yml, on a rule with no if, beside verdict
    findings:
      resolution:
        claude/code_review: [acme/leads, "!pr/authors"]
```

Under `findings`, write `resolution` with one of these values:

| Value | Meaning |
| :- | :- |
| A [people list](#people-lists) | One list for every classifier's findings. `resolution: humans` lets people with write access close them, the author included |
| A map of classifier names to lists | A list for each classifier |
| A list of sets, each `{ if, from }` | Each `if` can read `finding/severity`, as in `{ if: "finding/severity >= high", from: acme/leads }`. Where each `if` reads `finding/severity` alone, the first set whose `if` is true decides. End with a set that has no `if` |
| `nobody` | No person's resolve alone closes a finding. A classifier can close its own findings |

To let people close findings, put a list on a rule that has no `if` and covers the finding's file. Put that rule in the [policy file that decides](#policy-files-in-subdirectories) for the file. For a resolve alone to count, every list that applies to that file has to admit the person who resolves.

A failed `claude/code_review` is one answer for the whole pull request. Check every changed file under a rule that compares that answer, as in `claude/code_review = pass`:

* **Every file's lists admit the person who resolves**: once every Important finding of the review is closed, it can read `pass`, with no new review
* **One file's lists don't admit the person who resolves, or that file has `nobody` or no list**: that person's resolve leaves the review `fail`. Write a list for that file that admits the person.

Closing a finding changes no code, so people can lower `.severity` and pass a failed review with nothing fixed. Keep the lists short.

### `locals` and `use`

To reuse a value, name it under `locals` at the top of the policy file. Then write `"@name"` where the value belongs, or copy a whole map into a rule with `use`.

In this example, `payments_owner` names one set of people, and `strict` names a whole verdict that the first rule copies with `use`:

```yaml theme={null}
# .claude/approvals.yml
version: 1
locals:
  payments_owner: { count: 1, from: [acme/payments, "!pr/authors"] }
  strict:
    verdict: { claude: comments, seats: [{ count: 2, from: humans }, "@payments_owner"] }
rules:
  - purpose: "The payments API takes two people, one of them a payments owner."
    paths: ["services/payments/api/**"]
    use: ["@strict"]
  - purpose: "Everything else takes two people."
    paths: ["**"]
    verdict: { claude: comments, seats: 2 }
```

Check what a local can hold and where you can use it:

* **What a local holds**: text, a number, `true` or `false`, a list, or one map
* **Where `"@name"` can stand**: for the whole of `paths`, a people list, `seats`, `verdict`, or `override`, and for one item of `paths`, a people list, or `seats`. Inside a condition it takes no quotes of its own, as in `"pr/files_changed > @many"`.
* **What `use` copies**: `verdict`, `override`, `if`, `paths`, `reuse`, `advisory`, and `findings`. What the rule writes itself wins: key by key inside `verdict`, `findings`, and a `reuse` map, and whole for any other key.

## How rules combine into one verdict

Approvals takes the strictest of the verdicts that apply: `blocks` outranks `comments`, which outranks `approves`, and every rule's seats have to be filled. Which verdicts apply turns on whether a rule matches, applies to, or covers a changed file:

* **Matches**: a rule matches a changed file when its `paths` include the file and no `"!"` item takes it out
* **Applies**: a rule applies to a changed file when it matches, its [`mode`](#rule-keys) is `enforce`, and its `if` is true or absent
* **Covers**: a rule covers a changed file when it matches, its `mode` is `enforce`, and it has a `verdict`, whatever its `if` says

Approvals picks a policy file, then rules, then verdicts:

1. **The policy file**: for each changed file, the [nearest enforcing one](#policy-files-in-subdirectories) that covers it and in which a rule with a `verdict` applies. `nested: inherit` rules in policy files higher up count as its rules.
2. **The rules**: the ones that apply to each changed file.
3. **Each rule's verdict**: its own, or its first true [`override`](#override).
4. **One verdict for the pull request**: the strictest across all changed files. One person can fill a seat in several rules, and the shortest `max_age` applies.

Under an enforced policy, these cases end another way:

| Case | What happens |
| :- | :- |
| No rule covers a changed file | Nobody is asked to review that file. A [protected file](#protected-files) can still need a person. Claude doesn't approve the pull request |
| No rule covers any changed file | Normally no check appears. Where GitHub requires the check on the default branch, it normally ends neutral, with the title **Nothing ran, not blocking: no file is covered**. GitHub counts that as passing. With no root policy file, a pull request that changes no file under a directory's policy file can get no check, so a required check waits |
| Rules cover a changed file, and none applies | The check fails, with a title that starts **No rule applies to** |
| A file moves between a path that rules cover and one that they don't | No check appears, and Claude comments that Approvals did not run. Where GitHub requires the check, the pull request waits |

To avoid these, cover every path with root rules that have no `if`, as the first rule of the [starter policy](#how-a-policy-file-works) does.

## How people's approvals are counted

An approval can count when an account with write access gives it in a GitHub review or an [`@claude approve`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals) comment. It has to be on the latest commit, or on an earlier one that [still counts](#earlier-approvals-after-a-new-push).

While a person with write access requests changes on a pull request that has a covered file, the **Claude Approvals** check normally reads **Changes requested** once nothing else holds it.

### Whether a pull request's author counts

On a pull request that a person with write access opened, the author can fill one seat without approving, in a set that admits them. Except on [a fork's or an outside contributor's pull request](https://code.claude.com/docs/en/approvals-pull-requests.md#pull-requests-from-forks-and-outside-contributors), the author alone can meet `seats: 1`. `seats: 2` can be the author and one more person.

* **Who holds the author's seat**: at the commit that the pull request was opened with, the person who opened it. After a later push, normally the person who both wrote and pushed the latest commit.
* **When nobody holds it**: for example, after a push of a commit that one person wrote and another pushed. The **Claude Approvals** check's summary gives the reason, and if you opened the pull request, you can then comment [`@claude approve`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals).
* **To exclude authors**: write `seats: [{ count: 1, from: [humans, "!pr/authors"] }]`. In a set of named people, name at least one more than `count`, or an author's own pull request can wait. On a [fork's pull request](https://code.claude.com/docs/en/approvals-pull-requests.md#pull-requests-from-forks-and-outside-contributors), no approval counts toward a set that excludes `pr/authors`.
* **What `"!pr/authors"` goes by**: the accounts that GitHub names as having written or pushed a commit or opened the pull request. It doesn't read `Co-authored-by` lines, and an agent's commits under another account don't make a person an author.
* **Bots**: a bot fills the seat only in a set that admits it, on a pull request that it opened and whose latest commit it pushed
* **Machine users**: an agent that works under a user account other than `claude` holds the seat as a person does, and can be the one person that a [protected file](#protected-files) needs. To keep it out, take its login out of the rule's set with `"!"`, as in `[humans, "!acme-ci"]`. For protected files, put that set in a rule whose `paths` name them, marked `nested: inherit`.

### Earlier approvals after a new push

After a push, an earlier approval counts or stops counting by what the push changed:

* **The diff's text stays identical**: an earlier approval that GitHub hasn't dismissed can count.
* **The diff's text changes**: earlier approvals normally stop counting. Where the policy writes [`reuse`](#reuse), some can continue to count

Approvals normally [asks GitHub to dismiss](https://code.claude.com/docs/en/approvals-github-rules.md#required-reviews-and-codeowners) Claude's own approval when it evaluates the push, and Claude approves the new commit only if the **Claude Approvals** check passes again.

## Protected files

A protected file is Approvals' term for a file that controls how pull requests are reviewed, such as the policy file itself. An edit to one can weaken the review of later pull requests. For example, an edit to the policy file can lower the number of people that they need.

Where a rule covers a changed file, Approvals normally [asks for a person](#who-has-to-approve-a-change-to-a-protected-file) on a change to a protected file. The list of protected files is built in:

* **Policy and classifier files**: every policy file, and everything under `.claude/classifiers/`
* **Review instructions**: `REVIEW.md` at the repository's root
* **Git files**: `.gitmodules`, `.gitattributes`, symlinks, and submodule pointers
* **Code owners**: any file named `CODEOWNERS`

Don't rely on other files being protected. Write a rule for the ones that matter to you, such as the `.github` folder, `CLAUDE.md`, `AGENTS.md`, `.mcp.json`, and the rest of the `.claude` folder.

### Who has to approve a change to a protected file

The person that Approvals asks for can be the pull request's author:

| Pull request | Who has to approve |
| :- | :- |
| A rule covers a changed file | Normally at least one person with write access. That person can be the pull request's author, and isn't a bot |
| No rule covers any changed file | Can need one person, who can be the author, or nobody |
| It changes a policy or classifier file in [observe mode](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-in-observe-mode) | Can need one person, who can be the author |

### When Claude approves a change to a protected file

Claude approves a pull request that changes a protected file only if a rule applies to that file and every rule that applies says `approves`. A rule on `"**"` can count. Claude doesn't approve a pull request that changes a `.gitattributes` file, a symlink, or a submodule pointer, whatever the rules say.

## Policy file size and count limits

Keep each file within these limits, or Approvals refuses it:

| What | Limit |
| :- | :- |
| One policy file | 448 KiB |
| Policy files in a repository | 1,024 files, 8 MiB together. Past either, Approvals reads none of them |
| Rules in a file | 512 |
| Locals in a file | 512 |
| Patterns in a rule, not counting `"!"` items | 256 |
| Overrides | 16 in a rule, 128 in a file |
| Entries in any list | 1,024 |
| `purpose` | 1,000 characters |
| A condition | 4,096 characters, eight levels of parentheses |
| `seats` as a number, or a set's `count` | 16 |
| Sets in one `seats` | 8 |
| Sets under `resolution` | 16 |
| Teams in one list, or in all the sets of one `seats` | 10 |
| Names under one `use` | 8 |
| Custom classifiers that a file names | 16 |
| Different classifier runs that a file asks for | 32 |

A pull request has limits too. Past them, GitHub lists the **Claude Approvals** check as **Action required**:

* **Changed files**: 2,000 or more. The check's title reads **Change too large to evaluate**. Split the pull request.
* **Commits**: more than 250, where a set excludes authors with `"!pr/authors"`. The title reads **Too many commits to tell who wrote it**. Have an author squash it to 250 commits or fewer and force-push.

## Related resources

* [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md): turn on observe mode, enforce the policy, and require the **Claude Approvals** check
* [Troubleshoot Claude Approvals](https://code.claude.com/docs/en/approvals-troubleshooting.md): fix a policy file that the check refuses
* [Claude Approvals classifiers](https://code.claude.com/docs/en/approvals-classifiers.md): the classifiers that a condition can read, and how to define your own
