# Using the Evaluation Tool

The [Claude Console](/dashboard) features an **Evaluation tool** that allows you to test your prompts under various scenarios.

---

## Accessing the Evaluate Feature

To get started with the Evaluation tool:

1. Open the Claude Console and navigate to the prompt editor.
2. After composing your prompt, look for the 'Evaluate' tab at the top of the screen.

![Accessing Evaluate Feature](/docs/images/access_evaluate.png)

<Tip>
Ensure your prompt includes at least 1-2 dynamic variables using the double brace syntax: \{\{variable\}\}. This is required for creating eval test sets.
</Tip>

## Generating Prompts

The Console offers a built-in [prompt generator](/docs/en/build-with-claude/prompt-engineering/prompt-generator) powered by Claude Opus 4.1:

<Steps>
  <Step title="Click 'Generate Prompt'">
    Clicking the 'Generate Prompt' helper tool will open a modal that allows you to enter your task information.
  </Step>
  <Step title="Describe your task">
    Describe your desired task (e.g., "Triage inbound customer support requests") with as much or as little detail as you desire. The more context you include, the more Claude can tailor its generated prompt to your specific needs.
  </Step>
  <Step title="Generate your prompt">
    Clicking the orange 'Generate Prompt' button at the bottom will have Claude generate a high quality prompt for you. You can then further improve those prompts using the Evaluation screen in the Console.
  </Step>
</Steps>

This feature makes it easier to create prompts with the appropriate variable syntax for evaluation.

![Prompt Generator](/docs/images/promptgenerator.png)

## Creating Test Cases

When you access the Evaluation screen, you have several options to create test cases:

1. Click the '+ Add Row' button at the bottom left to manually add a case.
2. Use the 'Generate Test Case' feature to have Claude automatically generate test cases for you.
3. Import test cases from a CSV file.

To use the 'Generate Test Case' feature:

<Steps>
  <Step title="Click on 'Generate Test Case'">
    Claude will generate test cases for you, one row at a time for each time you click the button.
  </Step>
  <Step title="Edit generation logic (optional)">
    You can also edit the test case generation logic by clicking on the arrow dropdown to the right of the 'Generate Test Case' button, then on 'Show generation logic' at the top of the Variables window that pops up. You may have to click `Generate' on the top right of this window to populate initial generation logic.
    
    Editing this allows you to customize and fine tune the test cases that Claude generates to greater precision and specificity.
  </Step>
</Steps>

Here's an example of a populated Evaluation screen with several test cases:

![Populated Evaluation Screen](/docs/images/eval_populated.png)

<Note>
If you update your original prompt text, you can re-run the entire eval suite against the new prompt to see how changes affect performance across all test cases.
</Note>

## Tips for Effective Evaluation

<section title="Prompt Structure for Evaluation">

To make the most of the Evaluation tool, structure your prompts with clear input and output formats. For example:

```
In this task, you will generate a cute one sentence story that incorporates two elements: a color and a sound.
The color to include in the story is:
<color>
{{COLOR}}
</color>
The sound to include in the story is:
<sound>
{{SOUND}}
</sound>
Here are the steps to generate the story:
1. Think of an object, animal, or scene that is commonly associated with the color provided. For example, if the color is "blue", you might think of the sky, the ocean, or a bluebird.
2. Imagine a simple action, event or scene involving the colored object/animal/scene you identified and the sound provided. For instance, if the color is "blue" and the sound is "whistle", you might imagine a bluebird whistling a tune.
3. Describe the action, event or scene you imagined in a single, concise sentence. Focus on making the sentence cute, evocative and imaginative. For example: "A cheerful bluebird whistled a merry melody as it soared through the azure sky."
Please keep your story to one sentence only. Aim to make that sentence as charming and engaging as possible while naturally incorporating the given color and sound.
Write your completed one sentence story inside <story> tags.

```

This structure makes it easy to vary inputs (\{\{COLOR\}\} and \{\{SOUND\}\}) and evaluate outputs consistently.

</section>

<Tip>
Use the 'Generate a prompt' helper tool in the Console to quickly create prompts with the appropriate variable syntax for evaluation.
</Tip>

## Understanding and comparing results

The Evaluation tool offers several features to help you refine your prompts:

1. **Side-by-side comparison**: Compare the outputs of two or more prompts to quickly see the impact of your changes.
2. **Quality grading**: Grade response quality on a 5-point scale to track improvements in response quality per prompt.
3. **Prompt versioning**: Create new versions of your prompt and re-run the test suite to quickly iterate and improve results.

By reviewing results across test cases and comparing different prompt versions, you can spot patterns and make informed adjustments to your prompt more efficiently.

Start evaluating your prompts today to build more robust AI applications with Claude!