# Portmanteau poet

Blend two words together to create a new, meaningful portmanteau.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                            |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible. |
| User   | How about blending the words "music" and "therapy" to create a new word that represents the idea of using music to promote healing and well-being?                                                                                                 |

## Example output

Here are some innovative portmanteau options that blend "music" and "therapy" to represent the concept of using music to promote healing and well-being:

1.  Musitherapy: This blend combines "music" and "therapy" in a straightforward manner, making it easy to understand the concept behind the word.
2.  Melodihealing: By combining "melody" and "healing," this portmanteau emphasizes the therapeutic power of melodies in promoting well-being.
3.  Rhythmedicine: This blend of "rhythm" and "medicine" suggests that the rhythmic aspects of music can have medicinal properties for healing.
4.  Harmonicure: By blending "harmony" and "cure," this portmanteau highlights the idea that the harmonious elements of music can help cure ailments.
5.  Tunetreatment: This blend of "tune" and "treatment" implies that specific tunes or songs can be used as a form of treatment for various conditions.
6.  Symphonotherapy: By combining "symphony" and "therapy," this portmanteau suggests that the complex and layered nature of symphonic music can have therapeutic effects.
7.  Melotherapy: This simple blend of "melody" and "therapy" emphasizes the therapeutic aspects of melodies in a concise and easy-to-remember word.
8.  Melodicine: By combining "melody" and "medicine," this portmanteau emphasizes the idea of using the healing properties of music and its melodies as a form of medicine or treatment for various conditions or challenges.

Choose the portmanteau that best captures the essence of your idea, or use these as inspiration to create your own unique blend!

---

## API request

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
  system="You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "How about blending the words \"music\" and \"therapy\" to create a new word that represents the idea of using music to promote healing and well-being?"
        }
      ]
    }
  ]
)
print(message.content)

```

</Tab>
<Tab title="TypeScript">

```

import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
model: "claude-sonnet-4-5",
max_tokens: 1000,
temperature: 1,
system: "You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "How about blending the words \"music\" and \"therapy\" to create a new word that represents the idea of using music to promote healing and well-being?"
}
]
}
]
});
console.log(msg);

```
</Tab>
<Tab title="AWS Bedrock Python">

```

from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock

# for authentication options

client = AnthropicBedrock()

message = client.messages.create(
model="anthropic.claude-sonnet-4-5-20250929-v1:0",
max_tokens=1000,
temperature=1,
system="You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "How about blending the words \"music\" and \"therapy\" to create a new word that represents the idea of using music to promote healing and well-being?"
}
]
}
]
)
print(message.content)

```
</Tab>
<Tab title="AWS Bedrock TypeScript">

```

import AnthropicBedrock from '@anthropic-ai/bedrock-sdk';

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
max_tokens: 1000,
temperature: 1,
system: "You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "How about blending the words \"music\" and \"therapy\" to create a new word that represents the idea of using music to promote healing and well-being?"
}
]
}
]
});
console.log(msg);

```
</Tab>
<Tab title="Vertex AI Python">

```

from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
model="claude-sonnet-4@20250514",
max_tokens=1000,
temperature=1,
system="You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible.",
messages=[
{
"role": "user",
"content": [
{
"type": "text",
"text": "How about blending the words \"music\" and \"therapy\" to create a new word that represents the idea of using music to promote healing and well-being?"
}
]
}
]
)
print(message.content)

```
</Tab>
<Tab title="Vertex AI TypeScript">

```

import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
model: "claude-sonnet-4@20250514",
max_tokens: 1000,
temperature: 1,
system: "You are an AI assistant with a knack for creating innovative portmanteaus. Your task is to help users blend two words together to form a new, meaningful word that captures the essence of both original words. Offer several options if possible.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "How about blending the words \"music\" and \"therapy\" to create a new word that represents the idea of using music to promote healing and well-being?"
}
]
}
]
});
console.log(msg);

```
</Tab>
</Tabs>

```