# Culinary creator

Suggest recipe ideas based on the user's available ingredients and dietary preferences.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment. |
| User   | Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey <br/> Dietary preferences: gluten free                                                                                                                                                                                                                                                                                                                                                                                                             |

## Example Output

Suggested recipes:

Honey Garlic Chicken Stir-Fry

Description: A quick and flavorful stir-fry featuring tender chicken breast, crisp vegetables, and a sweet and savory honey garlic sauce.  
 Ingredients:

- 2 chicken breasts, cut into bite-sized pieces
- 2 cups broccoli florets
- 1 cup sliced carrots
- 1 onion, diced
- 3 cloves garlic, minced
- 2 tbsp olive oil
- 1/4 cup soy sauce (gluten-free)
- 2 tbsp honey

Instructions:

1.  In a large skillet or wok, heat olive oil over medium-high heat.
2.  Add diced onion and minced garlic, and sauté until fragrant, about 2 minutes.
3.  Add chicken pieces and cook until no longer pink, about 5-7 minutes.
4.  Add broccoli and carrots, and stir-fry until vegetables are tender-crisp, about 5 minutes.
5.  In a small bowl, whisk together soy sauce and honey.
6.  Pour the sauce over the chicken and vegetables, and stir to coat evenly.
7.  Cook for an additional 2-3 minutes, or until the sauce has thickened slightly.
8.  Serve hot with steamed rice.

Chicken and Veggie Rice Bowls

Description: A hearty and nutritious rice bowl topped with seasoned chicken, roasted vegetables, and a drizzle of soy sauce.

Ingredients:

- 2 chicken breasts, cut into bite-sized pieces
- 2 cups broccoli florets
- 1 cup sliced carrots
- 1 onion, diced
- 2 cloves garlic, minced
- 2 tbsp olive oil
- 1/4 cup soy sauce (gluten-free)
- 2 cups cooked rice

Instructions:

1.  Preheat the oven to 400°F (200°C).
2.  In a large bowl, combine chicken pieces, broccoli, carrots, onion, and garlic.
3.  Drizzle with olive oil and half of the soy sauce, and toss to coat evenly.
4.  Spread the chicken and vegetables on a baking sheet and roast in the preheated oven for 20-25 minutes, or until the chicken is cooked through and the vegetables are tender.
5.  Divide cooked rice among serving bowls.
6.  Top each bowl with the roasted chicken and vegetables.
7.  Drizzle the remaining soy sauce over the top of each bowl.
8.  Serve hot and enjoy!

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
  max_tokens=2000,
  temperature=0.5,
  system="Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages=[
    {
    "role": "user",
    "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey \nDietary preferences: gluten free"
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
  max_tokens: 2000,
  temperature: 0.5,
  system: "Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
        }
      ]
    }
  ]
});
console.log(msg);

````

</Tab>
<Tab title="AWS Bedrock Python">

```
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
# for authentication options
client = AnthropicBedrock()

message = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens=2000,
    temperature=0.5,
    system="Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
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
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
  max_tokens: 2000,
  temperature: 0.5,
  system: "Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
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
    max_tokens=2000,
    temperature=0.5,
    system="Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
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
  max_tokens: 2000,
  temperature: 0.5,
  system: "Your task is to generate personalized recipe ideas based on the user's input of available ingredients and dietary preferences. Use this information to suggest a variety of creative and delicious recipes that can be made using the given ingredients while accommodating the user's dietary needs, if any are mentioned. For each recipe, provide a brief description, a list of required ingredients, and a simple set of instructions. Ensure that the recipes are easy to follow, nutritious, and can be prepared with minimal additional ingredients or equipment.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Available ingredients: chicken breast, broccoli, carrots, onion, garlic, olive oil, rice, gluten free soy sauce, honey  \nDietary preferences: gluten free"
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>