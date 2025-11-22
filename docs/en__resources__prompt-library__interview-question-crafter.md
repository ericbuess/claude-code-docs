# Interview question crafter

Generate questions for interviews.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes. |
| User   | You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies.                                                             |

## Example Output

1.  Can you walk me through a successful multi-channel marketing campaign you developed and executed in your previous role? What were the challenges you faced, and how did you overcome them?
2.  How do you measure the success of your marketing campaigns, and what metrics do you focus on? Can you provide an example of how you used data and analytics to optimize a campaign's performance?
3.  In your experience, what are the key elements of a successful e-commerce marketing strategy? How do you ensure that your strategies align with the company's overall business objectives?
4.  Can you share an example of a time when you had to collaborate with a cross-functional team (e.g., product, sales, or customer service) to achieve a marketing goal? What challenges did you encounter, and how did you foster effective collaboration?
5.  How do you stay informed about the latest marketing trends and technologies, and how have you applied this knowledge to improve your marketing strategies or campaigns?
6.  Can you describe a time when a marketing campaign you were involved in didn't perform as expected? What did you learn from the experience, and how did you apply those lessons to future campaigns?
7.  Our company values innovation and continuous improvement. Can you share an example of a time when you introduced a new marketing approach, tool, or technology that significantly impacted your team's performance or results?

---

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
  temperature=0.5,
  system="Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
  temperature: 0.5,
  system: "Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
    temperature=0.5,
    system="Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
                }
            ]
        }
    ]
)
print(message.content)

```

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
temperature: 0.5,
system: "Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
    temperature=0.5,
    system="Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
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
  temperature: 0.5,
  system: "Your task is to generate a series of thoughtful, open-ended questions for an interview based on the given context. The questions should be designed to elicit insightful and detailed responses from the interviewee, allowing them to showcase their knowledge, experience, and critical thinking skills. Avoid yes/no questions or those with obvious answers. Instead, focus on questions that encourage reflection, self-assessment, and the sharing of specific examples or anecdotes.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are interviewing a candidate for a marketing manager position at a well-established e-commerce company. The ideal candidate should have experience developing and executing multi-channel marketing campaigns, strong analytical skills, and the ability to collaborate effectively with cross-functional teams. They should also be passionate about staying up-to-date with the latest marketing trends and technologies."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>