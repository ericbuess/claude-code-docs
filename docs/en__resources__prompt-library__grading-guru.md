# Grading guru

Compare and evaluate the quality of written texts based on user-defined criteria and standards.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

| Role | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User | Evaluate the following two texts based on the given criteria: <br/> <br/> Text 1: <br/> The sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment. <br/><br/> Text 2: <br/> The sunset was pretty. The birds were singing and the wind was blowing. It made me happy. <br/><br/> Criteria: <br/> 1. Descriptive language and imagery <br/> 2. Sentence structure and variety <br/> 3. Emotional impact and engagement <br/> 4. Grammar and punctuation |

## Example Output

Based on the provided criteria, here is my evaluation of the two texts:

Text 1:

1.  Descriptive language and imagery: The text uses vivid and evocative language to paint a picture of the setting. Phrases like "warm golden glow," "birds chirped their evening songs," and "gentle breeze rustled through the leaves" create a strong visual and auditory imagery, immersing the reader in the scene.
2.  Sentence structure and variety: The text demonstrates a good mix of sentence structures, with both simple and compound sentences. This variety helps to maintain a smooth flow and keeps the reader engaged.
3.  Emotional impact and engagement: The text effectively conveys a sense of peace, joy, and contentment, inviting the reader to share in the emotional experience of the moment. The description of the setting and the use of positive language create a strong emotional connection.
4.  Grammar and punctuation: The text appears to be grammatically correct and well-punctuated, with no obvious errors or issues.

Text 2:

1.  Descriptive language and imagery: The text lacks detailed descriptive language and imagery. While it mentions the sunset, birds, and wind, it does not provide any vivid or evocative details to help the reader visualize the scene.
2.  Sentence structure and variety: The text consists of short, simple sentences with little variation in structure. This lack of variety can make the writing feel monotonous and less engaging.
3.  Emotional impact and engagement: The text conveys a positive emotion by stating "It made me happy," but it does not provide a strong emotional connection or engagement due to the lack of descriptive language and imagery.
4.  Grammar and punctuation: The text appears to be grammatically correct and well-punctuated, with no obvious errors or issues.

Comparative Analysis:  
 Based on the evaluation, Text 1 performs significantly better than Text 2 in terms of descriptive language, imagery, sentence structure, variety, and emotional impact. Text 1 creates a vivid and immersive experience for the reader and demonstrates a higher quality of writing based on the given criteria, with its strong descriptive language, varied sentence structures, and effective emotional engagement. Text 2, while grammatically correct, lacks the descriptive richness and emotional impact present in Text 1.

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
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Evaluate the following two texts based on the given criteria: \n \nText 1: \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment. \n \nText 2: \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy. \n \nCriteria: \n1. Descriptive language and imagery \n2. Sentence structure and variety \n3. Emotional impact and engagement \n4. Grammar and punctuation",
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
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
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
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
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
  max_tokens: 2000,
  temperature: 0,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="Vertex AI Python">

```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=2000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
                }
            ]
        }
    ]
)
print(message.content)

```

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
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Evaluate the following two texts based on the given criteria:  \n  \nText 1:  \nThe sun was setting behind the mountains, casting a warm golden glow across the valley. The birds chirped their evening songs as the gentle breeze rustled through the leaves. It was a peaceful and serene moment, one that filled the heart with joy and contentment.  \n  \nText 2:  \nThe sunset was pretty. The birds were singing and the wind was blowing. It made me happy.  \n  \nCriteria:  \n1. Descriptive language and imagery  \n2. Sentence structure and variety  \n3. Emotional impact and engagement  \n4. Grammar and punctuation"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>