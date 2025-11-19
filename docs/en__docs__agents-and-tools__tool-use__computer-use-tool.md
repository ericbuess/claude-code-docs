# Computer use tool

---

Claude can interact with computer environments through the computer use tool, which provides screenshot capabilities and mouse/keyboard control for autonomous desktop interaction.

<Note>
Computer use is currently in beta and requires a [beta header](/docs/en/api/beta-headers):
- `"computer-use-2025-01-24"` (Claude 4 models and Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)))
</Note>

## Overview

Computer use is a beta feature that enables Claude to interact with desktop environments. This tool provides:

- **Screenshot capture**: See what's currently displayed on screen
- **Mouse control**: Click, drag, and move the cursor
- **Keyboard input**: Type text and use keyboard shortcuts
- **Desktop automation**: Interact with any application or interface

While computer use can be augmented with other tools like bash and text editor for more comprehensive automation workflows, computer use specifically refers to the computer use tool's capability to see and control desktop environments.

## Model compatibility

Computer use is available for the following Claude models:

| Model | Tool Version | Beta Flag |
|-------|--------------|-----------|
| Claude 4 models | `computer_20250124` | `computer-use-2025-01-24` |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | `computer_20250124`| `computer-use-2025-01-24` |

<Note>
Claude 4 models use updated tool versions optimized for the new architecture. Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) introduces additional capabilities including the thinking feature for more insight into the model's reasoning process.
</Note>

<Warning>
Older tool versions are not guaranteed to be backwards-compatible with newer models. Always use the tool version that corresponds to your model version.
</Warning>

## Security considerations

<Warning>
Computer use is a beta feature with unique risks distinct from standard API features. These risks are heightened when interacting with the internet. To minimize risks, consider taking precautions such as:

1. Use a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents.
2. Avoid giving the model access to sensitive data, such as account login information, to prevent information theft.
3. Limit internet access to an allowlist of domains to reduce exposure to malicious content.
4. Ask a human to confirm decisions that may result in meaningful real-world consequences as well as any tasks requiring affirmative consent, such as accepting cookies, executing financial transactions, or agreeing to terms of service.

In some circumstances, Claude will follow commands found in content even if it conflicts with the user's instructions. For example, Claude instructions on webpages or contained in images may override instructions or cause Claude to make mistakes. We suggest taking precautions to isolate Claude from sensitive data and actions to avoid risks related to prompt injection.

We've trained the model to resist these prompt injections and have added an extra layer of defense. If you use our computer use tools, we'll automatically run classifiers on your prompts to flag potential instances of prompt injections. When these classifiers identify potential prompt injections in screenshots, they will automatically steer the model to ask for user confirmation before proceeding with the next action. We recognize that this extra protection won't be ideal for every use case (for example, use cases without a human in the loop), so if you'd like to opt out and turn it off, please [contact us](https://support.claude.com/en/).

We still suggest taking precautions to isolate Claude from sensitive data and actions to avoid risks related to prompt injection.

Finally, please inform end users of relevant risks and obtain their consent prior to enabling computer use in your own products.

</Warning>

<Card
  title="Computer use reference implementation"
  icon="computer"
  href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
>

Get started quickly with our computer use reference implementation that includes a web interface, Docker container, example tool implementations, and an agent loop.

**Note:** The implementation has been updated to include new tools for both Claude 4 models and Claude Sonnet 3.7. Be sure to pull the latest version of the repo to access these new features.

</Card>

<Tip>
  Please use [this form](https://forms.gle/BT1hpBrqDPDUrCqo7) to provide
  feedback on the quality of the model responses, the API itself, or the quality
  of the documentation - we cannot wait to hear from you!
</Tip>

## Quick start

Here's how to get started with computer use:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-5",  # or another compatible model
    max_tokens=1024,
    tools=[
        {
          "type": "computer_20250124",
          "name": "computer",
          "display_width_px": 1024,
          "display_height_px": 768,
          "display_number": 1,
        },
        {
          "type": "text_editor_20250124",
          "name": "str_replace_editor"
        },
        {
          "type": "bash_20250124",
          "name": "bash"
        }
    ],
    messages=[{"role": "user", "content": "Save a picture of a cat to my desktop."}],
    betas=["computer-use-2025-01-24"]
)
print(response)
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: computer-use-2025-01-24" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "tools": [
      {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1
      },
      {
        "type": "text_editor_20250124",
        "name": "str_replace_editor"
      },
      {
        "type": "bash_20250124",
        "name": "bash"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Save a picture of a cat to my desktop."
      }
    ]
  }'
```
</CodeGroup>

<Note>
A beta header is only required for the computer use tool.

The example above shows all three tools being used together, which requires the beta header because it includes the computer use tool.
</Note>

---

## How computer use works

<Steps>
  <Step
    title="1. Provide Claude with the computer use tool and a user prompt"
    icon="tool"
  >
    - Add the computer use tool (and optionally other tools) to your API request.
    - Include a user prompt that requires desktop interaction, e.g., "Save a picture of a cat to my desktop."
  </Step>
  <Step title="2. Claude decides to use the computer use tool" icon="wrench">
    - Claude assesses if the computer use tool can help with the user's query.
    - If yes, Claude constructs a properly formatted tool use request.
    - The API response has a `stop_reason` of `tool_use`, signaling Claude's intent.
  </Step>
  <Step
    title="3. Extract tool input, evaluate the tool on a computer, and return results"
    icon="computer"
  >
    - On your end, extract the tool name and input from Claude's request.
    - Use the tool on a container or Virtual Machine.
    - Continue the conversation with a new `user` message containing a `tool_result` content block.
  </Step>
  <Step
    title="4. Claude continues calling computer use tools until it's completed the task"
    icon="arrows-clockwise"
  >
    - Claude analyzes the tool results to determine if more tool use is needed or the task has been completed.
    - If Claude decides it needs another tool, it responds with another `tool_use` `stop_reason` and you should return to step 3.
    - Otherwise, it crafts a text response to the user.
  </Step>
</Steps>

We refer to the repetition of steps 3 and 4 without user input as the "agent loop" - i.e., Claude responding with a tool use request and your application responding to Claude with the results of evaluating that request.

### The computing environment

Computer use requires a sandboxed computing environment where Claude can safely interact with applications and the web. This environment includes:

1. **Virtual display**: A virtual X11 display server (using Xvfb) that renders the desktop interface Claude will see through screenshots and control with mouse/keyboard actions.

2. **Desktop environment**: A lightweight UI with window manager (Mutter) and panel (Tint2) running on Linux, which provides a consistent graphical interface for Claude to interact with.

3. **Applications**: Pre-installed Linux applications like Firefox, LibreOffice, text editors, and file managers that Claude can use to complete tasks.

4. **Tool implementations**: Integration code that translates Claude's abstract tool requests (like "move mouse" or "take screenshot") into actual operations in the virtual environment.

5. **Agent loop**: A program that handles communication between Claude and the environment, sending Claude's actions to the environment and returning the results (screenshots, command outputs) back to Claude.

When you use computer use, Claude doesn't directly connect to this environment. Instead, your application:

1. Receives Claude's tool use requests
2. Translates them into actions in your computing environment
3. Captures the results (screenshots, command outputs, etc.)
4. Returns these results to Claude

For security and isolation, the reference implementation runs all of this inside a Docker container with appropriate port mappings for viewing and interacting with the environment.

---

## How to implement computer use

### Start with our reference implementation

We have built a [reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) that includes everything you need to get started quickly with computer use:

- A [containerized environment](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/Dockerfile) suitable for computer use with Claude
- Implementations of [the computer use tools](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools)
- An [agent loop](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/computer_use_demo/loop.py) that interacts with the Claude API and executes the computer use tools
- A web interface to interact with the container, agent loop, and tools.

### Understanding the multi-agent loop

The core of computer use is the "agent loop" - a cycle where Claude requests tool actions, your application executes them, and returns results to Claude. Here's a simplified example:

```python
async def sampling_loop(
    *,
    model: str,
    messages: list[dict],
    api_key: str,
    max_tokens: int = 4096,
    tool_version: str,
    thinking_budget: int | None = None,
    max_iterations: int = 10,  # Add iteration limit to prevent infinite loops
):
    """
    A simple agent loop for Claude computer use interactions.

    This function handles the back-and-forth between:
    1. Sending user messages to Claude
    2. Claude requesting to use tools
    3. Your app executing those tools
    4. Sending tool results back to Claude
    """
    # Set up tools and API parameters
    client = Anthropic(api_key=api_key)
    beta_flag = "computer-use-2025-01-24" if "20250124" in tool_version else "computer-use-2024-10-22"

    # Configure tools - you should already have these initialized elsewhere
    tools = [
        {"type": f"computer_{tool_version}", "name": "computer", "display_width_px": 1024, "display_height_px": 768},
        {"type": f"text_editor_{tool_version}", "name": "str_replace_editor"},
        {"type": f"bash_{tool_version}", "name": "bash"}
    ]

    # Main agent loop (with iteration limit to prevent runaway API costs)
    iterations = 0
    while True and iterations < max_iterations:
        iterations += 1
        # Set up optional thinking parameter (for Claude Sonnet 3.7)
        thinking = None
        if thinking_budget:
            thinking = {"type": "enabled", "budget_tokens": thinking_budget}

        # Call the Claude API
        response = client.beta.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            tools=tools,
            betas=[beta_flag],
            thinking=thinking
        )

        # Add Claude's response to the conversation history
        response_content = response.content
        messages.append({"role": "assistant", "content": response_content})

        # Check if Claude used any tools
        tool_results = []
        for block in response_content:
            if block.type == "tool_use":
                # In a real app, you would execute the tool here
                # For example: result = run_tool(block.name, block.input)
                result = {"result": "Tool executed successfully"}

                # Format the result for Claude
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # If no tools were used, Claude is done - return the final messages
        if not tool_results:
            return messages

        # Add tool results to messages for the next iteration with Claude
        messages.append({"role": "user", "content": tool_results})
```

The loop continues until either Claude responds without requesting any tools (task completion) or the maximum iteration limit is reached. This safeguard prevents potential infinite loops that could result in unexpected API costs.

<Warning>
  When using the computer use tool, you must include the appropriate beta flag for your model version:
  
    <section title="Claude 4 models">

      When using `computer_20250124`, include this beta flag: 
      ```
      "betas": ["computer-use-2025-01-24"]
      ```
    
</section>
    <section title="Claude Sonnet 3.7">

      When using `computer_20250124`, include this beta flag: 
      ```
      "betas": ["computer-use-2025-01-24"]
      ```
    
</section>
  
</Warning>

We recommend trying the reference implementation out before reading the rest of this documentation.

### Optimize model performance with prompting

Here are some tips on how to get the best quality outputs:

1. Specify simple, well-defined tasks and provide explicit instructions for each step.
2. Claude sometimes assumes outcomes of its actions without explicitly checking their results. To prevent this you can prompt Claude with `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Some UI elements (like dropdowns and scrollbars) might be tricky for Claude to manipulate using mouse movements. If you experience this, try prompting the model to use keyboard shortcuts.
4. For repeatable tasks or UI interactions, include example screenshots and tool calls of successful outcomes in your prompt.
5. If you need the model to log in, provide it with the username and password in your prompt inside xml tags like `<robot_credentials>`. Using computer use within applications that require login increases the risk of bad outcomes as a result of prompt injection. Please review our [guide on mitigating prompt injections](/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) before providing the model with login credentials.

<Tip>
  If you repeatedly encounter a clear set of issues or know in advance the tasks
  Claude will need to complete, use the system prompt to provide Claude with
  explicit tips or instructions on how to do the tasks successfully.
</Tip>

### System prompts

When one of the Anthropic-defined tools is requested via the Claude API, a computer use-specific system prompt is generated. It's similar to the [tool use system prompt](/docs/en/agents-and-tools/tool-use/implement-tool-use#tool-use-system-prompt) but starts with:

> You have access to a set of functions you can use to answer the user's question. This includes access to a sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

As with regular tool use, the user-provided `system_prompt` field is still respected and used in the construction of the combined system prompt.

### Available actions

The computer use tool supports these actions:

**Basic actions (all versions)**
- **screenshot** - Capture the current display
- **left_click** - Click at coordinates `[x, y]`
- **type** - Type text string
- **key** - Press key or key combination (e.g., "ctrl+s")
- **mouse_move** - Move cursor to coordinates

**Enhanced actions (`computer_20250124`)**
Available in Claude 4 models and Claude Sonnet 3.7:
- **scroll** - Scroll in any direction with amount control
- **left_click_drag** - Click and drag between coordinates
- **right_click**, **middle_click** - Additional mouse buttons
- **double_click**, **triple_click** - Multiple clicks
- **left_mouse_down**, **left_mouse_up** - Fine-grained click control
- **hold_key** - Hold a key while performing other actions
- **wait** - Pause between actions

<section title="Example actions">

```json
// Take a screenshot
{
  "action": "screenshot"
}

// Click at position
{
  "action": "left_click",
  "coordinate": [500, 300]
}

// Type text
{
  "action": "type",
  "text": "Hello, world!"
}

// Scroll down (Claude 4/3.7)
{
  "action": "scroll",
  "coordinate": [500, 400],
  "scroll_direction": "down",
  "scroll_amount": 3
}
```

</section>

### Tool parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes | Tool version (`computer_20250124` or `computer_20241022`) |
| `name` | Yes | Must be "computer" |
| `display_width_px` | Yes | Display width in pixels |
| `display_height_px` | Yes | Display height in pixels |
| `display_number` | No | Display number for X11 environments |

<Warning>
Keep display resolution at or below 1280x800 (WXGA) for best performance. Higher resolutions may cause accuracy issues due to [image resizing](/docs/en/build-with-claude/vision#evaluate-image-size).
</Warning>

<Note>
**Important**: The computer use tool must be explicitly executed by your application - Claude cannot execute it directly. You are responsible for implementing the screenshot capture, mouse movements, keyboard inputs, and other actions based on Claude's requests.
</Note>

### Enable thinking capability in Claude 4 models and Claude Sonnet 3.7

Claude Sonnet 3.7 introduced a new "thinking" capability that allows you to see the model's reasoning process as it works through complex tasks. This feature helps you understand how Claude is approaching a problem and can be particularly valuable for debugging or educational purposes.

To enable thinking, add a `thinking` parameter to your API request:

```json
"thinking": {
  "type": "enabled",
  "budget_tokens": 1024
}
```

The `budget_tokens` parameter specifies how many tokens Claude can use for thinking. This is subtracted from your overall `max_tokens` budget.

When thinking is enabled, Claude will return its reasoning process as part of the response, which can help you:

1. Understand the model's decision-making process
2. Identify potential issues or misconceptions
3. Learn from Claude's approach to problem-solving
4. Get more visibility into complex multi-step operations

Here's an example of what thinking output might look like:

```
[Thinking]
I need to save a picture of a cat to the desktop. Let me break this down into steps:

1. First, I'll take a screenshot to see what's on the desktop
2. Then I'll look for a web browser to search for cat images
3. After finding a suitable image, I'll need to save it to the desktop

Let me start by taking a screenshot to see what's available...
```

### Augmenting computer use with other tools

The computer use tool can be combined with other tools to create more powerful automation workflows. This is particularly useful when you need to:
- Execute system commands ([bash tool](/docs/en/agents-and-tools/tool-use/bash-tool))
- Edit configuration files or scripts ([text editor tool](/docs/en/agents-and-tools/tool-use/text-editor-tool))
- Integrate with custom APIs or services (custom tools)

<CodeGroup>
  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: computer-use-2025-01-24" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 2000,
      "tools": [
        {
          "type": "computer_20250124",
          "name": "computer",
          "display_width_px": 1024,
          "display_height_px": 768,
          "display_number": 1
        },
        {
          "type": "text_editor_20250124",
          "name": "str_replace_editor"
        },
        {
          "type": "bash_20250124",
          "name": "bash"
        },
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              },
              "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Find flights from San Francisco to a place with warmer weather."
        }
      ],
      "thinking": {
        "type": "enabled",
        "budget_tokens": 1024
      }
    }'
  ```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[
        {
          "type": "computer_20250124",
          "name": "computer",
          "display_width_px": 1024,
          "display_height_px": 768,
          "display_number": 1,
        },
        {
          "type": "text_editor_20250124",
          "name": "str_replace_editor"
        },
        {
          "type": "bash_20250124",
          "name": "bash"
        },
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              },
              "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
              }
            },
            "required": ["location"]
          }
        },
    ],
    messages=[{"role": "user", "content": "Find flights from San Francisco to a place with warmer weather."}],
    betas=["computer-use-2025-01-24"],
    thinking={"type": "enabled", "budget_tokens": 1024},
)
print(response)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

const message = await anthropic.beta.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  tools: [
      {
        type: "computer_20250124",
        name: "computer",
        display_width_px: 1024,
        display_height_px: 768,
        display_number: 1,
      },
      {
        type: "text_editor_20250124",
        name: "str_replace_editor"
      },
      {
        type: "bash_20250124",
        name: "bash"
      },
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              description: "The unit of temperature, either 'celsius' or 'fahrenheit'"
            }
          },
          required: ["location"]
        }
      },
  ],
  messages: [{ role: "user", content: "Find flights from San Francisco to a place with warmer weather." }],
  betas: ["computer-use-2025-01-24"],
  thinking: { type: "enabled", budget_tokens: 1024 },
});
console.log(message);
```
```java Java
import java.util.List;
import java.util.Map;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaToolBash20250124;
import com.anthropic.models.beta.messages.BetaToolComputerUse20250124;
import com.anthropic.models.beta.messages.BetaToolTextEditor20250124;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaThinkingConfigParam;
import com.anthropic.models.beta.messages.BetaTool;

public class MultipleToolsExample {

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
                .model("claude-sonnet-4-5")
                .maxTokens(1024)
                .addTool(BetaToolComputerUse20250124.builder()
                        .displayWidthPx(1024)
                        .displayHeightPx(768)
                        .displayNumber(1)
                        .build())
                .addTool(BetaToolTextEditor20250124.builder()
                        .build())
                .addTool(BetaToolBash20250124.builder()
                        .build())
                .addTool(BetaTool.builder()
                        .name("get_weather")
                        .description("Get the current weather in a given location")
                        .inputSchema(BetaTool.InputSchema.builder()
                                .properties(
                                        JsonValue.from(
                                                Map.of(
                                                        "location", Map.of(
                                                                "type", "string",
                                                                "description", "The city and state, e.g. San Francisco, CA"
                                                        ),
                                                        "unit", Map.of(
                                                                "type", "string",
                                                                "enum", List.of("celsius", "fahrenheit"),
                                                                "description", "The unit of temperature, either 'celsius' or 'fahrenheit'"
                                                        )
                                                )
                                        ))
                                .build()
                        )
                        .build())
                .thinking(BetaThinkingConfigParam.ofEnabled(
                        BetaThinkingConfigEnabled.builder()
                                .budgetTokens(1024)
                                .build()
                ))
                .addUserMessage("Find flights from San Francisco to a place with warmer weather.")
                .addBeta("computer-use-2025-01-24")
                .build();

        BetaMessage message = client.beta().messages().create(params);
        System.out.println(message);
    }
}
```
</CodeGroup>

### Build a custom computer use environment

The [reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) is meant to help you get started with computer use. It includes all of the components needed have Claude use a computer. However, you can build your own environment for computer use to suit your needs. You'll need:

- A virtualized or containerized environment suitable for computer use with Claude
- An implementation of at least one of the Anthropic-defined computer use tools
- An agent loop that interacts with the Claude API and executes the `tool_use` results using your tool implementations
- An API or UI that allows user input to start the agent loop

#### Implement the computer use tool

The computer use tool is implemented as a schema-less tool. When using this tool, you don't need to provide an input schema as with other tools; the schema is built into Claude's model and can't be modified.

<Steps>
  <Step title="Set up your computing environment">
    Create a virtual display or connect to an existing display that Claude will interact with. This typically involves setting up Xvfb (X Virtual Framebuffer) or similar technology.
  </Step>
  <Step title="Implement action handlers">
    Create functions to handle each action type that Claude might request:
    ```python
    def handle_computer_action(action_type, params):
        if action_type == "screenshot":
            return capture_screenshot()
        elif action_type == "left_click":
            x, y = params["coordinate"]
            return click_at(x, y)
        elif action_type == "type":
            return type_text(params["text"])
        # ... handle other actions
    ```
  </Step>
  <Step title="Process Claude's tool calls">
    Extract and execute tool calls from Claude's responses:
    ```python
    for content in response.content:
        if content.type == "tool_use":
            action = content.input["action"]
            result = handle_computer_action(action, content.input)
            
            # Return result to Claude
            tool_result = {
                "type": "tool_result",
                "tool_use_id": content.id,
                "content": result
            }
    ```
  </Step>
  <Step title="Implement the agent loop">
    Create a loop that continues until Claude completes the task:
    ```python
    while True:
        response = client.beta.messages.create(...)
        
        # Check if Claude used any tools
        tool_results = process_tool_calls(response)
        
        if not tool_results:
            # No more tool use, task complete
            break
            
        # Continue conversation with tool results
        messages.append({"role": "user", "content": tool_results})
    ```
  </Step>
</Steps>

#### Handle errors

When implementing the computer use tool, various errors may occur. Here's how to handle them:

<section title="Screenshot capture failure">

If screenshot capture fails, return an appropriate error message:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Failed to capture screenshot. Display may be locked or unavailable.",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Invalid coordinates">

If Claude provides coordinates outside the display bounds:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Coordinates (1200, 900) are outside display bounds (1024x768).",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Action execution failure">

If an action fails to execute:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Failed to perform click action. The application may be unresponsive.",
      "is_error": true
    }
  ]
}
```

</section>

#### Follow implementation best practices

<section title="Use appropriate display resolution">

Set display dimensions that match your use case while staying within recommended limits:
- For general desktop tasks: 1024x768 or 1280x720
- For web applications: 1280x800 or 1366x768
- Avoid resolutions above 1920x1080 to prevent performance issues

</section>

<section title="Implement proper screenshot handling">

When returning screenshots to Claude:
- Encode screenshots as base64 PNG or JPEG
- Consider compressing large screenshots to improve performance
- Include relevant metadata like timestamp or display state

</section>

<section title="Add action delays">

Some applications need time to respond to actions:
```python
def click_and_wait(x, y, wait_time=0.5):
    click_at(x, y)
    time.sleep(wait_time)  # Allow UI to update
```

</section>

<section title="Validate actions before execution">

Check that requested actions are safe and valid:
```python
def validate_action(action_type, params):
    if action_type == "left_click":
        x, y = params.get("coordinate", (0, 0))
        if not (0 <= x < display_width and 0 <= y < display_height):
            return False, "Coordinates out of bounds"
    return True, None
```

</section>

<section title="Log actions for debugging">

Keep a log of all actions for troubleshooting:
```python
import logging

def log_action(action_type, params, result):
    logging.info(f"Action: {action_type}, Params: {params}, Result: {result}")
```

</section>

---

## Understand computer use limitations

The computer use functionality is in beta. While Claude's capabilities are cutting edge, developers should be aware of its limitations:

1. **Latency**: the current computer use latency for human-AI interactions may be too slow compared to regular human-directed computer actions. We recommend focusing on use cases where speed isn't critical (e.g., background information gathering, automated software testing) in trusted environments.
2. **Computer vision accuracy and reliability**: Claude may make mistakes or hallucinate when outputting specific coordinates while generating actions. Claude Sonnet 3.7 introduces the thinking capability that can help you understand the model's reasoning and identify potential issues.
3. **Tool selection accuracy and reliability**: Claude may make mistakes or hallucinate when selecting tools while generating actions or take unexpected actions to solve problems. Additionally, reliability may be lower when interacting with niche applications or multiple applications at once. We recommend that users prompt the model carefully when requesting complex tasks.
4. **Scrolling reliability**: Claude Sonnet 3.7 introduced dedicated scroll actions with direction control that improves reliability. The model can now explicitly scroll in any direction (up/down/left/right) by a specified amount.
5. **Spreadsheet interaction**: Mouse clicks for spreadsheet interaction have improved in Claude Sonnet 3.7 with the addition of more precise mouse control actions like `left_mouse_down`, `left_mouse_up`, and new modifier key support. Cell selection can be more reliable by using these fine-grained controls and combining modifier keys with clicks.
6. **Account creation and content generation on social and communications platforms**: While Claude will visit websites, we are limiting its ability to create accounts or generate and share content or otherwise engage in human impersonation across social media websites and platforms. We may update this capability in the future.
7. **Vulnerabilities**: Vulnerabilities like jailbreaking or prompt injection may persist across frontier AI systems, including the beta computer use API. In some circumstances, Claude will follow commands found in content, sometimes even in conflict with the user's instructions. For example, Claude instructions on webpages or contained in images may override instructions or cause Claude to make mistakes. We recommend:
   a. Limiting computer use to trusted environments such as virtual machines or containers with minimal privileges
   b. Avoiding giving computer use access to sensitive accounts or data without strict oversight
   c. Informing end users of relevant risks and obtaining their consent before enabling or requesting permissions necessary for computer use features in your applications
8. **Inappropriate or illegal actions**: Per Anthropic's terms of service, you must not employ computer use to violate any laws or our Acceptable Use Policy.

Always carefully review and verify Claude's computer use actions and logs. Do not use Claude for tasks requiring perfect precision or sensitive user information without human oversight.

---

## Pricing

Computer use follows the standard [tool use pricing](/docs/en/agents-and-tools/tool-use/overview#pricing). When using the computer use tool:

**System prompt overhead**: The computer use beta adds 466-499 tokens to the system prompt

**Computer use tool token usage**:
| Model | Input tokens per tool definition |
| ----- | -------------------------------- |
| Claude 4.x models | 735 tokens |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | 735 tokens |

**Additional token consumption**:
- Screenshot images (see [Vision pricing](/docs/en/build-with-claude/vision))
- Tool execution results returned to Claude

<Note>
If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages.
</Note>

## Next steps

<CardGroup cols={2}>
  <Card
    title="Reference implementation"
    icon="github-logo"
    href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
  >
    Get started quickly with our complete Docker-based implementation
  </Card>
  <Card
    title="Tool documentation"
    icon="tool"
    href="/docs/en/agents-and-tools/tool-use/overview"
  >
    Learn more about tool use and creating custom tools
  </Card>
</CardGroup>