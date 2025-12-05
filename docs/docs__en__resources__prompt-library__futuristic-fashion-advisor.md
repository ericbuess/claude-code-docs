# Futuristic fashion advisor

Suggest avant-garde fashion trends and styles for the user's specific preferences.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks. |
| User   | Personal style: Edgy, minimal, with a touch of androgyny Favorite colors: Black, white, and deep red Preferred materials: Leather, denim, and high-quality cotton Body type: Tall and lean Fashion goals: To create a striking, fearless look for an art gallery opening                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

### Example output

> Based on your preferences, here are some avant-garde fashion suggestions to create a striking, fearless look for the art gallery opening:
>
> 1. Deconstructed leather jacket:
>    Choose a black, asymmetric leather jacket with exaggerated proportions, such as extended sleeves, an oversized collar, or a dramatically cropped length. Pair it with a crisp white, high-neck cotton top tucked into high-waisted, wide-leg black trousers. Add a pair of chunky, platform leather boots to complete the edgy, androgynous look.
>
> 2. Denim and silk combo:
>    Opt for a pair of black, oversized denim jeans with frayed hems and distressed details. Tuck in a deep red, silk button-down shirt with a draped, exaggerated collar or bow. Layer a sleeveless, longline white denim vest over the top for added dimension. Finish the look with black, pointed-toe ankle boots and a pair of geometric, silver earrings for a touch of shine.
>
> 3. Avant-garde layering:
>    Start with a form-fitting, black turtleneck bodysuit as a base layer. Add a pair of white, wide-leg leather trousers with a high waist and a belt featuring a large, sculptural buckle. Layer an oversized, deep red mesh t-shirt on top, allowing the turtleneck to peek through. Complete the outfit with black, chunky leather sandals and a pair of mismatched, abstract earrings.
>
> Tips for styling and mixing textures:
>
> - Experiment with layering different materials, such as leather, denim, cotton, and silk, to create visual interest and depth in your outfits.
> - Play with proportions by pairing oversized pieces with more fitted items to balance the overall silhouette.
> - Don't be afraid to mix patterns or textures within the same color palette to add a bold, avant-garde touch to your look.
> - Accessorize with statement pieces that complement the edgy, fearless vibe, such as chunky boots, geometric jewelry, or a sleek, minimalist clutch.
>   Remember, avant-garde fashion is about pushing boundaries and experimenting with unconventional styles. Embrace your unique taste and have fun creating striking, memorable looks that showcase your personal style.

### API Request

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
        temperature=1,
        system="Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Personal style: Edgy, minimal, with a touch of androgyny  \nFavorite colors: Black, white, and deep red  \nPreferred materials: Leather, denim, and high-quality cotton  \nBody type: Tall and lean  \nFashion goals: To create a striking, fearless look for an art gallery opening"
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
      temperature: 1,
      system: "Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Personal style: Edgy, minimal, with a touch of androgyny  \nFavorite colors: Black, white, and deep red  \nPreferred materials: Leather, denim, and high-quality cotton  \nBody type: Tall and lean  \nFashion goals: To create a striking, fearless look for an art gallery opening"
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
        temperature=1,
        system="Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Personal style: Edgy, minimal, with a touch of androgyny  \nFavorite colors: Black, white, and deep red  \nPreferred materials: Leather, denim, and high-quality cotton  \nBody type: Tall and lean  \nFashion goals: To create a striking, fearless look for an art gallery opening"
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
      temperature: 1,
      system: "Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Personal style: Edgy, minimal, with a touch of androgyny  \nFavorite colors: Black, white, and deep red  \nPreferred materials: Leather, denim, and high-quality cotton  \nBody type: Tall and lean  \nFashion goals: To create a striking, fearless look for an art gallery opening"
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
        temperature=1,
        system="Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Personal style: Edgy, minimal, with a touch of androgyny  \nFavorite colors: Black, white, and deep red  \nPreferred materials: Leather, denim, and high-quality cotton  \nBody type: Tall and lean  \nFashion goals: To create a striking, fearless look for an art gallery opening"
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
      temperature: 1,
      system: "Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. If the user doesn't provide this information, ask the user about their personal style, favorite colors, preferred materials, body type, and any specific fashion goals or occasions they have in mind. Use this information to generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style while still considering the user's individual taste and needs. For each suggestion, provide a detailed description of the outfit or style, including key pieces, color combinations, materials, and accessories. Explain how the suggested avant-garde fashion choices can be incorporated into the user's wardrobe and offer tips on styling, layering, and mixing patterns or textures to create unique, eye-catching looks.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Personal style: Edgy, minimal, with a touch of androgyny  \nFavorite colors: Black, white, and deep red  \nPreferred materials: Leather, denim, and high-quality cotton  \nBody type: Tall and lean  \nFashion goals: To create a striking, fearless look for an art gallery opening"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>