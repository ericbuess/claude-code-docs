# Tongue twister

Create challenging tongue twisters.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

| Role | Content                                                                                                                                                                                                                                                                                               |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User | Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters. |

## Example Output

Tongue Twister 1:  
 The shrewd shrew chewed through the shiny, shimmering shoe.

Tongue Twister 2:  
 Brisk breezes blew by the blue-blooded, blabbering, babbling baboon.

Tongue Twister 3:  
 The perplexed piper picked a peck of pickled peppers while practicing his piping.

Tongue Twister 4:  
 Six sleek, slick, slender sleds slid swiftly down the steep, snowy slope.

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
  temperature=1,
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters."
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
  temperature: 1,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters."
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
    temperature=1,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters."
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
  temperature: 1,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters."
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
    max_tokens=1000,
    temperature=1,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters."
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
  max_tokens: 1000,
  temperature: 1,
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate complex and creative tongue twisters. Aim to create tongue twisters that are not only challenging to say but also engaging, entertaining, and potentially humorous. Consider incorporating wordplay, rhyme, and alliteration to enhance the difficulty and enjoyment of the tongue twisters."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>