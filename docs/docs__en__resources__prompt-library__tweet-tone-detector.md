# Tweet tone detector

Detect the tone and sentiment behind tweets.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| System | Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision. |
| User   | Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail                                                                                                                                                                                                                                                                                                                                                              |

### Example output

> Tone: Sarcastic
> Sentiment: Negative

### API request

<CodeGroup>
    ```python Python
    import anthropic
    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        temperature=0,
        system="Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript TypeScript
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic({
      apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
    });
    
    const msg = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python AWS Bedrock Python
    from anthropic import AnthropicBedrock
    
    # See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    # for authentication options
    client = AnthropicBedrock()
    
    message = client.messages.create(
        model="anthropic.claude-sonnet-4-5-20250929-v1:0",
        max_tokens=1000,
        temperature=0,
        system="Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript AWS Bedrock TypeScript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";
    
    // See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    // for authentication options
    const client = new AnthropicBedrock();
    
    const msg = await client.messages.create({
      model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python Vertex AI Python
    from anthropic import AnthropicVertex
    
    client = AnthropicVertex()
    
    message = client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=1000,
        temperature=0,
        system="Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript Vertex AI TypeScript
    import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';
    
    // Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
    // Additionally goes through the standard `google-auth-library` flow.
    const client = new AnthropicVertex();
    
    const msg = await client.messages.create({
      model: "claude-sonnet-4@20250514",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Wow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>