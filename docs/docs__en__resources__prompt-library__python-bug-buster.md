# Python bug buster

Detect and fix bugs in Python code.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming. |
| User   | def calculate_average(nums): <br/> sum = 0 <br/> for num in nums: <br/> sum += num <br/> average = sum / len(nums) <br/> return average <br/><br/> numbers = [10, 20, 30, 40, 50] <br/> result = calculate_average(numbers) <br/> print("The average is:", results)                                                                                                 |

## Example Output

Corrected Python code:

```python Python
def calculate_average(nums):
    total = 0
    for num in nums:
        total += num
    average = total / len(nums)
    return average

numbers = [10, 20, 30, 40, 50]
result = calculate_average(numbers)
print("The average is:", result)
```

Explanation:

    1. Changed the variable name "sum" to "total" to avoid using the built-in Python function "sum()".
    2. Fixed the typo in the print statement, changing "results" to "result" to correctly reference the variable.

## API Request

<Tabs>
<Tab title="Python">

```python
import anthropic

client = anthropic.Anthropic(
  # defaults to os.environ.get("ANTHROPIC_API_KEY")
  api_key="my_api_key",
)
message = client.messages.create(
  model="claude-sonnet-4-5",
  max_tokens=1000,
  temperature=0,
  system="Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
  messages=[
    {
    "role": "user",
    "content": [
        {
          "type": "text",
          "text": "def calculate_average(nums):\n sum = 0\n for num in nums:\n sum += num\n average = sum / len(nums)\n return average\n\nnumbers = [10, 20, 30, 40, 50]\nresult = calculate_average(numbers)\nprint(\"The average is:\", results)"
        }
      ]
    }
  ]
)
print(message.content)

```

</Tab>
<Tab title="TypeScript">

```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1000,
  temperature: 0,
  system: "Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "def calculate_average(nums):\n   sum = 0\n   for num in nums:\n      sum += num\n   average = sum / len(nums)\n   return average\n\nnumbers = [10, 20, 30, 40, 50]\nresult = calculate_average(numbers)\nprint(\"The average is:\", results)"
        }
      ]
    }
  ]
});
console.log(msg);
````

  </Tab>
  <Tab title="AWS Bedrock Python">
```python
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock

# for authentication options

client = AnthropicBedrock()

message = client.messages.create(
model="anthropic.claude-sonnet-4-5-20250929-v1:0",
max_tokens=1000,
temperature=0,
system="Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "def calculate_average(nums):\n sum = 0\n for num in nums:\n sum += num\n average = sum / len(nums)\n return average\n\nnumbers = [10, 20, 30, 40, 50]\nresult = calculate_average(numbers)\nprint(\"The average is:\", results)"
}
]
}
]
)
print(message.content)

````
  </Tab>
    <Tab title="AWS Bedrock TypeScript">
```typescript
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
  max_tokens: 1000,
  temperature: 0,
  system: "Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "def calculate_average(nums):\n   sum = 0\n   for num in nums:\n      sum += num\n   average = sum / len(nums)\n   return average\n\nnumbers = [10, 20, 30, 40, 50]\nresult = calculate_average(numbers)\nprint(\"The average is:\", results)"
        }
      ]
    }
  ]
});
console.log(msg);
````

  </Tab>
    <Tab title="Vertex AI Python">
```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
model="claude-sonnet-4@20250514",
max_tokens=1000,
temperature=0,
system="Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "def calculate_average(nums):\n sum = 0\n for num in nums:\n sum += num\n average = sum / len(nums)\n return average\n\nnumbers = [10, 20, 30, 40, 50]\nresult = calculate_average(numbers)\nprint(\"The average is:\", results)"
}
]
}
]
)
print(message.content)

````
  </Tab>
    <Tab title="Vertex AI TypeScript">
```typescript
import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
  model: "claude-sonnet-4@20250514",
  max_tokens: 1000,
  temperature: 0,
  system: "Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "def calculate_average(nums):\n   sum = 0\n   for num in nums:\n      sum += num\n   average = sum / len(nums)\n   return average\n\nnumbers = [10, 20, 30, 40, 50]\nresult = calculate_average(numbers)\nprint(\"The average is:\", results)"
        }
      ]
    }
  ]
});
console.log(msg);
````

  </Tab>
</Tabs>