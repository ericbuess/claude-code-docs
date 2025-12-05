# LaTeX legend

Write LaTeX documents, generating code for mathematical equations, tables, and more.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively. |
| User   | I need to create a simple table with three columns and two rows. The header row should contain the titles "Name," "Age," and "City." The data row should have the values "John," "25," and "New York."                                                                                                                                                                                               |

## Example Output

Here's the LaTeX code to create a simple table with three columns and two rows, including a header row with the titles "Name," "Age," and "City," and a data row with the values "John," "25," and "New York":

```latex
\begin{table}[h]
\centering
\begin{tabular}{|c|c|c|}
\hline
Name & Age & City \\
\hline
John & 25 & New York \\
\hline
\end{tabular}
\caption{Sample Table}
\label{tab:sample}
\end{table}

```

Explanation:

- The `table` environment is used to create a floating table that can be positioned automatically by LaTeX.
- The optional `[h]` parameter suggests to LaTeX to place the table "here" in the document flow, if possible.
- The `\centering` command centers the table horizontally on the page.
- The `tabular` environment is used to create the actual table structure.
- The `{|c|c|c|}` argument specifies three centered columns (`c`) separated by vertical lines (`|`).
- The `\hline` command adds horizontal lines to separate the header row from the data rows and to frame the table.
- The `&` character separates the cells within a row, and `\\` marks the end of a row.
- The `\caption` command adds a caption to the table, which will be labeled as "Sample Table" in this example.
- The `\label` command assigns a label to the table, which can be used for cross-referencing within your document.

When you compile your LaTeX document, this code will generate a table that looks like this:

```
+------+-----+----------+
| Name | Age |   City   |
+------+-----+----------+
| John |  25 | New York |
+------+-----+----------+

```

---

## API Request

<Tabs>
<Tab title="Python">
```python
import anthropic

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2000,
    temperature=0,
    system="You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": 'I need to create a simple table with three columns and two rows. The header row should contain the titles "Name," "Age," and "City." The data row should have the values "John," "25," and "New York."',
                }
            ],
        }
    ],
)
print(message.content)


````
</Tab>
<Tab title="TypeScript">
```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 2000,
  temperature: 0,
  system: "You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
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
max_tokens=2000,
temperature=0,
system="You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
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
  max_tokens: 2000,
  temperature: 0,
  system: "You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
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
max_tokens=2000,
temperature=0,
system="You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
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
  max_tokens: 2000,
  temperature: 0,
  system: "You are an AI assistant with expertise in LaTeX, a document preparation system widely used for academic and technical writing. Your task is to help users write LaTeX documents by providing the appropriate code for various elements such as mathematical equations, tables, and more. Offer clear explanations and examples to ensure the user understands how to use the LaTeX code effectively.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I need to create a simple table with three columns and two rows. The header row should contain the titles \"Name,\" \"Age,\" and \"City.\" The data row should have the values \"John,\" \"25,\" and \"New York.\""
        }
      ]
    }
  ]
});
console.log(msg);

````

</Tab>
</Tabs>