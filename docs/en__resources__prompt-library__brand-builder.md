# Brand builder

Craft a design brief for a holistic brand identity.

---

> Copy this prompt into our developer [Console](/login?selectAccount=true&returnTo=%2Fdashboard%3F) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| System | Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.                                                                                              |
| User   | Brand specs: This is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods The brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility. The brand identity should achieve the following goals: 1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship. 2. Appeal to the target audience by conveying a sense of style, quality, and trendiness. 3. Differentiate the brand from competitors in the sustainable fashion market. 4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices. |

### Example output

> Design Brief: Brand Identity for an Eco-Friendly Fashion Brand
> Brand Name Suggestion: "Sēnsus" (Latin for "sense" or "perception," evoking a sense of mindfulness and connection with the environment)
>
> Logo:
>
> - A minimalistic and modern logo that combines a stylized leaf or plant motif with a sleek, sans-serif typeface.
> - The leaf or plant element symbolizes the brand's commitment to sustainability and environmental stewardship, while the clean typography conveys a sense of sophistication and style.
> - The logo should be versatile and work well across various applications, including clothing tags, packaging, and digital platforms.
>   Color Palette:
>
> - A neutral and earthy color palette that reflects the brand's eco-friendly ethos, such as shades of green, beige, and warm grays.
> - Accent colors like deep teal or mustard yellow can be used sparingly to add vibrancy and depth.
> - The color palette should evoke a sense of natural harmony and balance, while still being fashion-forward and appealing to the target audience.
>   Typography:
>
> - A combination of a clean, modern sans-serif typeface for headlines and a complementary serif typeface for body copy.
> - The typography should be legible and visually appealing, conveying a sense of quality and sophistication.
> - Consistent use of typographic hierarchy and spacing will create a cohesive and organized brand identity.
>   Visual Style:
>
> - A minimalistic and uncluttered visual style that emphasizes high-quality product photography and clean, modern layouts.
> - Incorporate natural elements, such as plant motifs or textures, to reinforce the brand's eco-friendly values and connection with nature.
> - Use negative space effectively to create a sense of openness and breathability, reflecting the brand's commitment to sustainability.
>   Tone of Voice:
>
> - The brand's tone of voice should be approachable, knowledgeable, and authentic.
> - Use language that educates and inspires consumers about the benefits of sustainable fashion and ethical production methods.
> - Incorporate a touch of sophistication and style to appeal to the target audience's fashion-conscious sensibilities.
>   Brand Personality:
>
> - Eco-conscious and environmentally aware, yet stylish and fashion-forward.
> - Confident and passionate about promoting sustainable practices and ethical choices.
> - Inclusive and welcoming, inviting consumers to join a like-minded community committed to making positive changes.
>   Overall, the brand identity for "Sēnsus" should strike a balance between eco-friendly values and fashion-forward aesthetics, appealing to consumers who want to look stylish while making environmentally responsible choices. The cohesive visual and verbal elements should create a strong emotional connection with the target audience and inspire them to embrace a more sustainable lifestyle.

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
        max_tokens=2000,
        temperature=1,
        system="Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
        max_tokens=2000,
        temperature=1,
        system="Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
        max_tokens=2000,
        temperature=1,
        system="Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
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
      max_tokens: 2000,
      temperature: 1,
      system: "Your task is to create a comprehensive design brief for a holistic brand identity based on the given specifications. The brand identity should encompass various elements such as suggestions for the brand name, logo, color palette, typography, visual style, tone of voice, and overall brand personality. Ensure that all elements work together harmoniously to create a cohesive and memorable brand experience that effectively communicates the brand's values, mission, and unique selling proposition to its target audience. Be detailed and comprehensive and provide enough specific details for someone to create a truly unique brand identity.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Brand specs:\nThis is a brand that focuses on creating high-quality, stylish clothing and accessories using eco-friendly materials and ethical production methods\nThe brand targets environmentally conscious consumers aged 25-40 who value fashion, sustainability, and social responsibility.\nThe brand identity should achieve the following goals:\n1. Reflect the brand's commitment to sustainability, ethical practices, and environmental stewardship.\n2. Appeal to the target audience by conveying a sense of style, quality, and trendiness.\n3. Differentiate the brand from competitors in the sustainable fashion market.\n4. Create a strong emotional connection with consumers and inspire them to make more environmentally friendly choices."
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>