---
title: Prompt engineering overview
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
description: Learn when prompt engineering is the right solution, and find Claude prompting techniques and interactive tutorials.
---

## Before prompt engineering

This guide assumes that you have:

1. A clear definition of the success criteria for your use case
2. Some ways to empirically test against those criteria
3. A first draft prompt you want to improve

If not, spend time establishing that first. Check out [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) for tips and guidance.

<CardGroup cols={2}>
  <Card title="Prompt generator notebook" icon="link" href="https://colab.research.google.com/github/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb">
    Don't have a first draft prompt? Generate one with the metaprompt recipe from the Claude Cookbook.
  </Card>

  <Card title="Prompting best practices" icon="link" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    For model-specific tuning guidance for Claude's latest models, start here.
  </Card>
</CardGroup>

***

## When to prompt engineer

This guide focuses on success criteria that are controllable through prompt engineering. Not every success criteria or failing eval is best solved by prompt engineering. For example, you can sometimes improve latency and cost more easily by selecting a different model.

***

## How to prompt engineer

All prompting techniques (from clarity and examples to XML structuring, role prompting, thinking, and prompt chaining) are covered in [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). That's the living reference; start there.

For general prompt engineering craft beyond Claude-specific techniques, see the blog post on [best practices for prompt engineering](https://claude.com/blog/best-practices-for-prompt-engineering).

***

## Prompt engineering tutorial

If you're an interactive learner, you can start with the interactive tutorials instead!

<CardGroup cols={2}>
  <Card title="GitHub prompting tutorial" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    An example-filled tutorial that covers the prompt engineering concepts found in the docs.
  </Card>

  <Card title="Google Sheets prompting tutorial" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    A lighter-weight version of the prompt engineering tutorial, as an interactive spreadsheet.
  </Card>
</CardGroup>
