---
title: Customer support agent
url: https://platform.claude.com/docs/en/about-claude/use-case-guides/customer-support-chat
description: Build a customer support chatbot with Claude that answers product questions, stays on topic, and generates quotes through tool use.
---

## Prerequisites

To follow this guide, you need:

* A Claude API key (set as the `ANTHROPIC_API_KEY` environment variable)
* Python 3.9 or later

Install the required packages:

```bash
pip install anthropic streamlit python-dotenv
```

## Before building with Claude

### Decide whether to use Claude for support chat

Here are some key indicators that you should employ an LLM like Claude to automate portions of your customer support process:

<AccordionGroup>
  <Accordion title="High volume of repetitive queries">
    Claude excels at handling a large number of similar questions efficiently, freeing up human agents for more complex issues.
  </Accordion>

  <Accordion title="Need for quick information synthesis">
    Claude can quickly retrieve, process, and combine information from vast knowledge bases, while human agents may need time to research or consult multiple sources.
  </Accordion>

  <Accordion title="24/7 availability requirement">
    Claude can provide round-the-clock support without fatigue, whereas staffing human agents for continuous coverage can be costly and challenging.
  </Accordion>

  <Accordion title="Rapid scaling during peak periods">
    Claude can handle sudden increases in query volume without the need for hiring and training additional staff.
  </Accordion>

  <Accordion title="Consistent brand voice">
    You can instruct Claude to consistently represent your brand's tone and values, whereas human agents may vary in their communication styles.
  </Accordion>
</AccordionGroup>

Some considerations for choosing Claude over other LLMs:

* You prioritize natural, nuanced conversation: Claude's sophisticated language understanding allows for more natural, context-aware conversations that feel more human-like than chats with other LLMs.
* You often receive complex and open-ended queries: Claude can handle a wide range of topics and inquiries without generating canned responses or requiring extensive programming of permutations of user utterances.
* You need scalable multilingual support: Claude's multilingual capabilities allow it to engage in conversations in over 200 languages without the need for separate chatbots or extensive translation processes for each supported language.

### Define your ideal chat interaction

Outline an ideal customer interaction to define how and when you expect the customer to interact with Claude. This outline will help to determine the technical requirements of your solution.

Here is an example chat interaction for car insurance customer support:

* **Customer:** Initiates support chat experience
  * **Claude:** Warmly greets customer and initiates conversation

* **Customer:** Asks about insurance for their new electric car
  * **Claude:** Provides relevant information about electric vehicle coverage

* **Customer:** Asks questions related to unique needs for electric vehicle insurances
  * **Claude:** Responds with accurate and informative answers and provides links to the sources

* **Customer:** Asks off-topic questions unrelated to insurance or cars
  * **Claude:** Clarifies it does not discuss unrelated topics and steers the user back to car insurance

* **Customer:** Expresses interest in an insurance quote

  * **Claude:** Ask a set of questions to determine the appropriate quote, adapting to their responses
  * **Claude:** Sends a request to use the quote generation API tool along with necessary information collected from the user
  * **Claude:** Receives the response information from the API tool use, synthesizes the information into a natural response, and presents the provided quote to the user

* **Customer:** Asks follow up questions

  * **Claude:** Answers follow up questions as needed
  * **Claude:** Guides the customer to the next steps in the insurance process and closes out the conversation

<Tip>
  In the real example that you write for your own use case, you might find it useful to write out the actual words in this interaction so that you can also get a sense of the ideal tone, response length, and level of detail you want Claude to have.
</Tip>

### Break the interaction into unique tasks

Customer support chat is a collection of multiple different tasks, from question answering to information retrieval to taking action on requests, wrapped up in a single customer interaction. Before you start building, break down your ideal customer interaction into every task you want Claude to be able to perform. This ensures you can prompt and evaluate Claude for every task, and gives you a good sense of the range of interactions you need to account for when writing test cases.

<Tip>
  Customers sometimes find it helpful to visualize this as an interaction flowchart of possible conversation inflection points depending on user requests.
</Tip>

Here are the key tasks associated with the example insurance interaction:

1. Greeting and general guidance

   * Warmly greet the customer and initiate conversation
   * Provide general information about the company and interaction

2. Product information

   * Provide information about electric vehicle coverage
     <Note>
       This will require that Claude have the necessary information in its context, and might imply that a 

       [RAG integration](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide)

        is necessary.
     </Note>
   * Answer questions related to unique electric vehicle insurance needs
   * Answer follow-up questions about the quote or insurance details
   * Offer links to sources when appropriate

3. Conversation management

   * Stay on topic (car insurance)
   * Redirect off-topic questions back to relevant subjects

4. Quote generation

   * Ask appropriate questions to determine quote eligibility
   * Adapt questions based on customer responses
   * Submit collected information to quote generation API
   * Present the provided quote to the customer

### Establish success criteria

Work with your support team to [define success criteria and write detailed evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) with measurable benchmarks and goals.

Here are criteria and benchmarks that can be used to evaluate how successfully Claude performs the defined tasks:

<AccordionGroup>
  <Accordion title="Query comprehension accuracy">
    This metric evaluates how accurately Claude understands customer inquiries across various topics. Measure this by reviewing a sample of conversations and assessing whether Claude has the correct interpretation of customer intent, critical next steps, what successful resolution looks like, and more. Aim for a comprehension accuracy of 95% or higher.
  </Accordion>

  <Accordion title="Response relevance">
    This assesses how well Claude's response addresses the customer's specific question or issue. Evaluate a set of conversations and rate the relevance of each response (using LLM-based grading for scale). Target a relevance score of 90% or above.
  </Accordion>

  <Accordion title="Response accuracy">
    Assess the correctness of general company and product information provided to the user, based on the information provided to Claude in context. Target 100% accuracy in this introductory information.
  </Accordion>

  <Accordion title="Citation provision relevance">
    Track the frequency and relevance of links or sources offered. Target providing relevant sources in 80% of interactions where additional information could be beneficial.
  </Accordion>

  <Accordion title="Topic adherence">
    Measure how well Claude stays on topic, such as the topic of car insurance in the example implementation. Aim for 95% of responses to be directly related to car insurance or the customer's specific query.
  </Accordion>

  <Accordion title="Content generation effectiveness">
    Measure how successful Claude is at determining when to generate informational content and how relevant that content is. For example, in this implementation, you would be determining how well Claude understands when to generate a quote and how accurate that quote is. Target 100% accuracy, as this is vital information for a successful customer interaction.
  </Accordion>

  <Accordion title="Escalation efficiency">
    This measures Claude's ability to recognize when a query needs human intervention and escalate appropriately. Track the percentage of correctly escalated conversations versus those that should have been escalated but weren't. Aim for an escalation accuracy of 95% or higher.
  </Accordion>
</AccordionGroup>

Here are criteria and benchmarks that can be used to evaluate the business impact of employing Claude for support:

<AccordionGroup>
  <Accordion title="Sentiment maintenance">
    This assesses Claude's ability to maintain or improve customer sentiment throughout the conversation. Use sentiment analysis tools to measure sentiment at the beginning and end of each conversation. Aim for maintained or improved sentiment in 90% of interactions.
  </Accordion>

  <Accordion title="Deflection rate">
    The percentage of customer inquiries successfully handled by the chatbot without human intervention. Typically aim for 70-80% deflection rate, depending on the complexity of inquiries.
  </Accordion>

  <Accordion title="Customer satisfaction score">
    A measure of how satisfied customers are with their chatbot interaction. Usually done through post-interaction surveys. Aim for a CSAT score of 4 out of 5 or higher.
  </Accordion>

  <Accordion title="Average handle time">
    The average time it takes for the chatbot to resolve an inquiry. This varies widely based on the complexity of issues, but generally, aim for a lower AHT compared to human agents.
  </Accordion>
</AccordionGroup>

## How to implement Claude as a customer service agent

### Choose the right Claude model

The choice of model depends on the trade-offs between cost, accuracy, and response time.

For customer support chat, Claude Opus 5 is well suited to balance intelligence, latency, and cost, including the most complex support scenarios that require deep reasoning across long, multi-step conversations. However, for instances where you have conversation flow with multiple prompts including RAG, tool use, or long-context prompts, Claude Haiku 4.5 may be more suitable to optimize for latency.

### Build a strong prompt

Using Claude for customer support requires Claude having enough direction and context to respond appropriately, while having enough flexibility to handle a wide range of customer inquiries.

Start by writing the elements of a strong prompt, beginning with a system prompt. Create a file called `config.py` and add each of the following blocks to it:

```python
IDENTITY = """You are Eva, a friendly and knowledgeable AI assistant for Acme Insurance
Company. Your role is to warmly welcome customers and provide information on
Acme's insurance offerings, which include car insurance and electric car
insurance. You can also help customers get quotes for their insurance needs."""
```

<Tip>
  While you may be tempted to put all your information inside a system prompt as a way to separate instructions from the user conversation, Claude actually works best with the bulk of its prompt content written inside the first 

  `User`

   turn (with the only exception being role prompting). Read more at 

  [Giving Claude a role with a system prompt](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role)

  .
</Tip>

It's best to break down complex prompts into subsections and write one part at a time. For each task, you might find greater success by following a step-by-step process to define the parts of the prompt Claude would need to do the task well. For this car insurance customer support example, you'll be writing piecemeal all the parts for a prompt starting with the "Greeting and general guidance" task. This also makes debugging your prompt easier as you can more quickly adjust individual parts of the overall prompt.

```python
STATIC_GREETINGS_AND_GENERAL = """
<static_context>
Acme Auto Insurance: Your Trusted Companion on the Road

About:
At Acme Insurance, we understand that your vehicle is more than just a mode of transportation—it's your ticket to life's adventures.
Since 1985, we've been crafting auto insurance policies that give drivers the confidence to explore, commute, and travel with peace of mind.
Whether you're navigating city streets or embarking on cross-country road trips, Acme is there to protect you and your vehicle.
Our innovative auto insurance policies are designed to adapt to your unique needs, covering everything from fender benders to major collisions.
With Acme's award-winning customer service and swift claim resolution, you can focus on the joy of driving while we handle the rest.
We're not just an insurance provider—we're your co-pilot in life's journeys.
Choose Acme Auto Insurance and experience the assurance that comes with superior coverage and genuine care. Because at Acme, we don't just
insure your car—we fuel your adventures on the open road.

Note: We also offer specialized coverage for electric vehicles, ensuring that drivers of all car types can benefit from our protection.

Acme Insurance offers the following products:
- Car insurance
- Electric car insurance
- Two-wheeler insurance

Business hours: Monday-Friday, 9 AM - 5 PM EST
Customer service number: 1-800-123-4567
</static_context>
"""
```

Then do the same for your car insurance and electric car insurance information.

```python
STATIC_CAR_INSURANCE = """
<static_context>
Car Insurance Coverage:
Acme's car insurance policies typically cover:
1. Liability coverage: Pays for bodily injury and property damage you cause to others.
2. Collision coverage: Pays for damage to your car in an accident.
3. Comprehensive coverage: Pays for damage to your car from non-collision incidents.
4. Medical payments coverage: Pays for medical expenses after an accident.
5. Uninsured/underinsured motorist coverage: Protects you if you're hit by a driver with insufficient insurance.

Optional coverages include:
- Rental car reimbursement
- Roadside assistance
- New car replacement
</static_context>
"""

STATIC_ELECTRIC_CAR_INSURANCE = """
<static_context>
Electric Car Insurance:
Our specialized electric car insurance goes beyond traditional auto coverage,
offering tailored protection for your high-tech investment. In addition to standard coverages, we offer:
- Safeguarding expensive battery systems
- Covering home charging equipment
- Adapting to the rapidly evolving world of electric vehicles

Whether you're driving a Rivian, Nissan Leaf, Chevrolet Bolt,
or any other electric vehicle, our knowledgeable agents are ready to craft a policy
that gives you the confidence to enjoy every electron-powered mile.
</static_context>
"""
```

Now that you have your static content, add at least 4-5 sample "good" interactions to guide Claude's responses. These examples should be representative of your ideal customer interaction and can include elements such as guardrails and tool calls.

```python
EXAMPLES = """
Here are a few examples of how you can interact with customers:

<example 1>
H: Hi, do you offer commercial insurance for small businesses?

A: Ah! Unfortunately, we don't offer commercial insurance at this time.
However, we do provide a range of personal insurance products including car insurance and electric car insurance.
Would you like to know more about these offerings?
</example 1>

<example 2>
H: Hi, what are your business hours?

A: Our business hours are Monday to Friday, 9 AM to 5 PM EST.
If you have any questions or need assistance, feel free to reach out during those times.
How else can I assist you today?
</example 2>

<example 3>
H: I'm shopping for car insurance. What does Acme offer?

A: Great choice! Acme's car insurance policies typically include:
- Liability coverage: Protects you if you're at fault in an accident
- Collision coverage: Pays for damage to your car in an accident
- Comprehensive coverage: Covers non-collision incidents like theft or vandalism
- Medical payments coverage: Pays for medical expenses after an accident
- Uninsured/underinsured motorist coverage: Protects you from drivers with insufficient insurance

We also offer optional coverages like rental car reimbursement, roadside assistance, and new car replacement.
Would you like more details on any of these coverages, or do you have specific questions about insuring your vehicle?
</example 3>

<example 4>
H: I'd like to hear about your electric car insurance.

A: Certainly! Our electric car insurance is specially designed to meet the unique needs of electric vehicle owners.
In addition to all the standard coverages we offer for regular cars, our electric car policies include:

- Battery coverage: Protection against damage or degradation of your vehicle's expensive battery system
- Tech package: Covers repairs or replacement of advanced electronics and onboard computer systems
- Charging station coverage: Protects both home and portable charging equipment
- Cybersecurity protection: Coverage against hacking or digital threats
- Specialized roadside assistance: Includes flatbed towing to protect the vehicle's undercarriage

We cover a wide range of electric vehicles, including popular models from Tesla, Rivian, Nissan, Chevrolet, and more.
Is there a specific electric vehicle you're looking to insure, or would you like more details on any of these coverages?
</example 4>

<example 5>
H: I'd like to get a quote for my car insurance.

A: Certainly! I'd be happy to help you get a quote for your car insurance.
To provide you with an accurate quote, I'll need to collect some information about your vehicle and the primary driver.
Let's start with the basics:

1. What is the make and model of your vehicle?
2. What year was it manufactured?
3. Approximately how many miles have you driven?
4. What is the age of the primary driver?

Once you provide this information, I'll use our quoting tool to generate a personalized insurance quote for you.
</example 5>
"""
```

You will also want to include any important instructions outlining dos and don'ts for how Claude should interact with the customer. This may draw from brand guardrails or support policies.

```python
ADDITIONAL_GUARDRAILS = """Please adhere to the following guardrails:
1. Only provide information about insurance types listed in our offerings.
2. If asked about an insurance type we don't offer, politely state
that we don't provide that service.
3. Do not speculate about future product offerings or company plans.
4. Don't make promises or enter into agreements it's not authorized to make.
You only provide information and guidance.
5. Do not mention any competitor's products or services.
"""
```

Now combine all these sections into a single string to use as your prompt.

```python
TASK_SPECIFIC_INSTRUCTIONS = " ".join(
    [
        STATIC_GREETINGS_AND_GENERAL,
        STATIC_CAR_INSURANCE,
        STATIC_ELECTRIC_CAR_INSURANCE,
        EXAMPLES,
        ADDITIONAL_GUARDRAILS,
    ]
)
```

### Add dynamic and agentic capabilities with tool use

Claude is capable of taking actions and retrieving information dynamically using client-side tool use functionality. Start by listing any external tools or APIs the prompt should use.

For this example, start with one tool for calculating the quote.

<Tip>
  As a reminder, this tool will not perform the actual calculation, it will just signal to the application that a tool should be used with whatever arguments specified.
</Tip>

Add the model name, the tool definition, and a stub implementation to `config.py`:

```python
import time

MODEL = "claude-opus-5"

TOOLS = [
    {
        "name": "get_quote",
        "description": "Calculate the insurance quote based on user input. Returned value is per month premium.",
        "input_schema": {
            "type": "object",
            "properties": {
                "make": {"type": "string", "description": "The make of the vehicle."},
                "model": {"type": "string", "description": "The model of the vehicle."},
                "year": {
                    "type": "integer",
                    "description": "The year the vehicle was manufactured.",
                },
                "mileage": {
                    "type": "integer",
                    "description": "The mileage on the vehicle.",
                },
                "driver_age": {
                    "type": "integer",
                    "description": "The age of the primary driver.",
                },
            },
            "required": ["make", "model", "year", "mileage", "driver_age"],
        },
    }
]


def get_quote(make, model, year, mileage, driver_age):
    """Returns the premium per month in USD"""
    # You can call an http endpoint or a database to get the quote.
    # Here, we simulate a delay of 1 seconds and return a fixed quote of 100.
    time.sleep(1)
    return 100
```

### Deploy your prompts

It's hard to know how well your prompt works without deploying it in a test production setting and [running evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests). Build a small application using the prompt, the Anthropic SDK, and Streamlit for a user interface.

In a file called `chatbot.py` (or the equivalent module in your language), set up the ChatBot class, which will encapsulate the interactions with the Anthropic SDK.

The class should have two main methods: one that calls the API to generate a message, and one that processes each incoming user input.

<CodeGroup exclude="shell">
  ```python Python
  # In your chatbot.py, import these from the config.py you wrote above:
  # from config import IDENTITY, TOOLS, MODEL, get_quote
  from anthropic import Anthropic
  from dotenv import load_dotenv

  load_dotenv()


  class ChatBot:
      def __init__(self, session_state):
          self.anthropic = Anthropic()
          self.session_state = session_state

      def generate_message(
          self,
          messages,
          max_tokens,
      ):
          try:
              response = self.anthropic.messages.create(
                  model=MODEL,
                  system=IDENTITY,
                  max_tokens=max_tokens,
                  messages=messages,
                  tools=TOOLS,
              )
              return response
          except Exception as e:
              return {"error": str(e)}

      def process_user_input(self, user_input):
          self.session_state.messages.append({"role": "user", "content": user_input})

          response_message = self.generate_message(
              messages=self.session_state.messages,
              max_tokens=2048,
          )

          if "error" in response_message:
              return f"An error occurred: {response_message['error']}"

          if response_message.content[-1].type == "tool_use":
              tool_use = response_message.content[-1]
              func_name = tool_use.name
              func_params = tool_use.input
              tool_use_id = tool_use.id

              result = self.handle_tool_use(func_name, func_params)
              self.session_state.messages.append(
                  {"role": "assistant", "content": response_message.content}
              )
              self.session_state.messages.append(
                  {
                      "role": "user",
                      "content": [
                          {
                              "type": "tool_result",
                              "tool_use_id": tool_use_id,
                              "content": f"{result}",
                          }
                      ],
                  }
              )

              follow_up_response = self.generate_message(
                  messages=self.session_state.messages,
                  max_tokens=2048,
              )

              if "error" in follow_up_response:
                  return f"An error occurred: {follow_up_response['error']}"

              response_text = next(
                  (block.text for block in follow_up_response.content if block.type == "text"),
                  None,
              )
              if response_text is None:
                  raise Exception("An error occurred: Unexpected response type")
              self.session_state.messages.append(
                  {"role": "assistant", "content": response_text}
              )
              return response_text

          text_block = next(
              (block for block in response_message.content if block.type == "text"), None
          )
          if text_block is not None:
              response_text = text_block.text
              self.session_state.messages.append(
                  {"role": "assistant", "content": response_text}
              )
              return response_text

          raise Exception("An error occurred: Unexpected response type")

      def handle_tool_use(self, func_name, func_params):
          if func_name == "get_quote":
              premium = get_quote(**func_params)
              return f"Quote generated: ${premium:.2f} per month"

          raise Exception("An unexpected tool was used")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  class ChatBot {
    // IDENTITY, MODEL, TOOLS, and getQuote mirror the config.py values defined
    // earlier in this guide (shown in Python).
    readonly anthropic = new Anthropic();
    readonly messages: Anthropic.MessageParam[] = [];

    async generateMessage(
      messages: Anthropic.MessageParam[],
      maxTokens: number
    ): Promise<Anthropic.Message> {
      return this.anthropic.messages.create({
        model: MODEL,
        system: IDENTITY,
        max_tokens: maxTokens,
        messages,
        tools: TOOLS
      });
    }

    async processUserInput(userInput: string): Promise<string> {
      this.messages.push({ role: "user", content: userInput });

      const responseMessage = await this.generateMessage(this.messages, 2048);

      const lastBlock = responseMessage.content.at(-1);
      if (lastBlock?.type === "tool_use") {
        const toolResult = this.handleToolUse(lastBlock.name, lastBlock.input);

        this.messages.push({ role: "assistant", content: responseMessage.content });
        this.messages.push({
          role: "user",
          content: [{ type: "tool_result", tool_use_id: lastBlock.id, content: toolResult }]
        });

        const followUpResponse = await this.generateMessage(this.messages, 2048);

        const followUpBlock = followUpResponse.content.find(
          (block): block is Anthropic.TextBlock => block.type === "text"
        );
        if (!followUpBlock) {
          throw new Error("An error occurred: Unexpected response type");
        }
        this.messages.push({ role: "assistant", content: followUpBlock.text });
        return followUpBlock.text;
      }

      const firstBlock = responseMessage.content.find(
        (block): block is Anthropic.TextBlock => block.type === "text"
      );
      if (firstBlock) {
        this.messages.push({ role: "assistant", content: firstBlock.text });
        return firstBlock.text;
      }

      throw new Error("An error occurred: Unexpected response type");
    }

    handleToolUse(toolName: string, toolInput: unknown): string {
      if (toolName === "get_quote") {
        // The SDK types tool_use.input as unknown; narrow it to the get_quote schema.
        if (
          toolInput === null ||
          typeof toolInput !== "object" ||
          !("make" in toolInput) || typeof toolInput.make !== "string" ||
          !("model" in toolInput) || typeof toolInput.model !== "string" ||
          !("year" in toolInput) || typeof toolInput.year !== "number" ||
          !("mileage" in toolInput) || typeof toolInput.mileage !== "number" ||
          !("driver_age" in toolInput) || typeof toolInput.driver_age !== "number"
        ) {
          throw new Error("An error occurred: Unexpected tool input");
        }
        const { make, model: vehicleModel, year, mileage, driver_age: driverAge } = toolInput;

        const premium = getQuote(make, vehicleModel, year, mileage, driverAge);
        return `Quote generated: $${premium.toFixed(2)} per month`;
      }

      throw new Error("An unexpected tool was used");
    }
  }
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  // Config.Model, Config.Identity, Config.Tools, and Config.GetQuote mirror
  // the config.py values defined earlier in this guide (shown in Python).
  public class ChatBot
  {
      private readonly AnthropicClient _anthropic = new();

      public List<MessageParam> Messages { get; } = [];

      public async Task<Message> GenerateMessage(List<MessageParam> messages, long maxTokens) =>
          await _anthropic.Messages.Create(
              new MessageCreateParams
              {
                  Model = Config.Model,
                  System = Config.Identity,
                  MaxTokens = maxTokens,
                  Messages = messages,
                  Tools = Config.Tools,
              }
          );

      public async Task<string> ProcessUserInput(string userInput)
      {
          Messages.Add(new() { Role = Role.User, Content = userInput });

          var responseMessage = await GenerateMessage(Messages, maxTokens: 2048);

          if (responseMessage.Content[^1].TryPickToolUse(out var toolUse))
          {
              var toolResult = HandleToolUse(toolUse.Name, toolUse.Input);

              Messages.Add(new()
              {
                  Role = Role.Assistant,
                  Content = responseMessage.Content
                      .Select(contentBlock => new ContentBlockParam(contentBlock.Json))
                      .ToList(),
              });
              Messages.Add(new()
              {
                  Role = Role.User,
                  Content = new List<ContentBlockParam>
                  {
                      new ToolResultBlockParam { ToolUseID = toolUse.ID, Content = toolResult },
                  },
              });

              var followUpResponse = await GenerateMessage(Messages, maxTokens: 2048);

              foreach (var block in followUpResponse.Content)
              {
                  if (block.TryPickText(out var followUpText))
                  {
                      Messages.Add(new() { Role = Role.Assistant, Content = followUpText.Text });
                      return followUpText.Text;
                  }
              }

              throw new InvalidOperationException("An error occurred: Unexpected response type");
          }

          foreach (var block in responseMessage.Content)
          {
              if (block.TryPickText(out var textBlock))
              {
                  Messages.Add(new() { Role = Role.Assistant, Content = textBlock.Text });
                  return textBlock.Text;
              }
          }

          throw new InvalidOperationException("An error occurred: Unexpected response type");
      }

      public string HandleToolUse(string funcName, IReadOnlyDictionary<string, JsonElement> funcParams)
      {
          if (funcName == "get_quote")
          {
              var premium = Config.GetQuote(
                  funcParams["make"].GetString()!,
                  funcParams["model"].GetString()!,
                  funcParams["year"].GetInt64(),
                  funcParams["mileage"].GetInt64(),
                  funcParams["driver_age"].GetInt64()
              );
              return $"Quote generated: ${premium:F2} per month";
          }

          throw new ArgumentException("An unexpected tool was used");
      }
  }
  ```

  ```go Go
  import (
  	"context"
  	"encoding/json"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  // ChatBot wraps the Anthropic client and the conversation history. The
  // identity, model, tools, and getQuote values it uses mirror the config.py
  // definitions earlier in this guide (shown in Python).
  type ChatBot struct {
  	client   anthropic.Client
  	messages []anthropic.MessageParam
  }

  func NewChatBot() *ChatBot {
  	return &ChatBot{client: anthropic.NewClient()}
  }

  func (bot *ChatBot) GenerateMessage(ctx context.Context, messages []anthropic.MessageParam, maxTokens int64) (*anthropic.Message, error) {
  	return bot.client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     model,
  		System:    []anthropic.TextBlockParam{{Text: identity}},
  		MaxTokens: maxTokens,
  		Messages:  messages,
  		Tools:     tools,
  	})
  }

  func (bot *ChatBot) ProcessUserInput(ctx context.Context, userInput string) (string, error) {
  	bot.messages = append(bot.messages, anthropic.NewUserMessage(anthropic.NewTextBlock(userInput)))

  	response, err := bot.GenerateMessage(ctx, bot.messages, 2048)
  	if err != nil {
  		return "", err
  	}

  	lastBlock := response.Content[len(response.Content)-1]
  	if toolUse, ok := lastBlock.AsAny().(anthropic.ToolUseBlock); ok {
  		result, err := bot.HandleToolUse(toolUse.Name, toolUse.Input)
  		if err != nil {
  			return "", err
  		}

  		bot.messages = append(bot.messages,
  			response.ToParam(),
  			anthropic.NewUserMessage(anthropic.NewToolResultBlock(toolUse.ID, result, false)),
  		)

  		followUp, err := bot.GenerateMessage(ctx, bot.messages, 2048)
  		if err != nil {
  			return "", err
  		}

  		for _, block := range followUp.Content {
  			if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  				bot.messages = append(bot.messages, anthropic.NewAssistantMessage(anthropic.NewTextBlock(textBlock.Text)))
  				return textBlock.Text, nil
  			}
  		}
  		return "", fmt.Errorf("an error occurred: unexpected response type")
  	}

  	for _, block := range response.Content {
  		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  			bot.messages = append(bot.messages, anthropic.NewAssistantMessage(anthropic.NewTextBlock(textBlock.Text)))
  			return textBlock.Text, nil
  		}
  	}

  	return "", fmt.Errorf("an error occurred: unexpected response type")
  }

  func (bot *ChatBot) HandleToolUse(toolName string, toolInput json.RawMessage) (string, error) {
  	if toolName != "get_quote" {
  		return "", fmt.Errorf("an unexpected tool was used: %s", toolName)
  	}

  	var input struct {
  		Make      string `json:"make"`
  		Model     string `json:"model"`
  		Year      int    `json:"year"`
  		Mileage   int    `json:"mileage"`
  		DriverAge int    `json:"driver_age"`
  	}
  	if err := json.Unmarshal(toolInput, &input); err != nil {
  		return "", err
  	}
  	premium := getQuote(input.Make, input.Model, input.Year, input.Mileage, input.DriverAge)
  	return fmt.Sprintf("Quote generated: $%.2f per month", premium), nil
  }

  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;

  // IDENTITY, MODEL, TOOLS, and getQuote mirror the config.py values defined
  // earlier in this guide (shown in Python).
  class ChatBot {
      final AnthropicClient anthropic;
      final List<MessageParam> messages;

      ChatBot() {
          // Reads the API key from the ANTHROPIC_API_KEY environment variable
          this.anthropic = AnthropicOkHttpClient.fromEnv();
          this.messages = new ArrayList<>();
      }

      Message generateMessage(List<MessageParam> messages, long maxTokens) {
          return anthropic.messages().create(MessageCreateParams.builder()
                  .model(MODEL)
                  .system(IDENTITY)
                  .maxTokens(maxTokens)
                  .messages(messages)
                  .tools(TOOLS)
                  .build());
      }

      String processUserInput(String userInput) {
          messages.add(MessageParam.builder()
                  .role(MessageParam.Role.USER)
                  .content(userInput)
                  .build());

          Message responseMessage = generateMessage(messages, 2048);

          List<ContentBlock> content = responseMessage.content();
          ContentBlock lastBlock = content.getLast();
          if (lastBlock.isToolUse()) {
              ToolUseBlock toolUse = lastBlock.asToolUse();
              Map<String, JsonValue> toolInput =
                      (Map<String, JsonValue>) toolUse._input().asObject().orElseThrow();
              String result = handleToolUse(toolUse.name(), toolInput);

              messages.add(MessageParam.builder()
                      .role(MessageParam.Role.ASSISTANT)
                      .contentOfBlockParams(content.stream().map(ContentBlock::toParam).toList())
                      .build());
              messages.add(MessageParam.builder()
                      .role(MessageParam.Role.USER)
                      .contentOfBlockParams(List.of(ContentBlockParam.ofToolResult(
                              ToolResultBlockParam.builder()
                                      .toolUseId(toolUse.id())
                                      .content(result)
                                      .build())))
                      .build());

              Message followUpResponse = generateMessage(messages, 2048);

              ContentBlock followUpBlock = followUpResponse.content().stream()
                      .filter(ContentBlock::isText)
                      .findFirst()
                      .orElseThrow(() -> new IllegalStateException("An error occurred: Unexpected response type"));
              String responseText = followUpBlock.asText().text();
              messages.add(MessageParam.builder()
                      .role(MessageParam.Role.ASSISTANT)
                      .content(responseText)
                      .build());
              return responseText;
          } else {
              ContentBlock textBlock = content.stream()
                      .filter(ContentBlock::isText)
                      .findFirst()
                      .orElseThrow(() -> new IllegalStateException("An error occurred: Unexpected response type"));
              String responseText = textBlock.asText().text();
              messages.add(MessageParam.builder()
                      .role(MessageParam.Role.ASSISTANT)
                      .content(responseText)
                      .build());
              return responseText;
          }
      }

      String handleToolUse(String funcName, Map<String, JsonValue> funcParams) {
          return switch (funcName) {
              case "get_quote" -> {
                  double premium = getQuote(
                          funcParams.get("make").asStringOrThrow(),
                          funcParams.get("model").asStringOrThrow(),
                          ((Number) funcParams.get("year").asNumber().orElseThrow()).longValue(),
                          ((Number) funcParams.get("mileage").asNumber().orElseThrow()).longValue(),
                          ((Number) funcParams.get("driver_age").asNumber().orElseThrow()).longValue());
                  yield "Quote generated: $%.2f per month".formatted(premium);
              }
              default -> throw new IllegalArgumentException("An unexpected tool was used");
          };
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Messages\Message;
  use Anthropic\Messages\MessageParam;
  use Anthropic\Messages\TextBlock;
  use Anthropic\Messages\ToolResultBlockParam;
  use Anthropic\Messages\ToolUseBlock;

  class ChatBot
  {
      // MODEL, IDENTITY, TOOLS, and get_quote() mirror the config.py values
      // defined earlier in this guide (shown in Python).

      /** @var list<MessageParam> */
      public private(set) array $messages = [];

      public function __construct(
          private readonly Client $anthropic = new Client(),
      ) {}

      /**
       * @param list<MessageParam> $messages
       */
      public function generateMessage(array $messages, int $maxTokens): Message
      {
          return $this->anthropic->messages->create(
              model: MODEL,
              system: IDENTITY,
              maxTokens: $maxTokens,
              messages: $messages,
              tools: TOOLS,
          );
      }

      public function processUserInput(string $userInput): string
      {
          $this->messages[] = MessageParam::with(role: 'user', content: $userInput);

          $responseMessage = $this->generateMessage($this->messages, maxTokens: 2048);

          $content = $responseMessage->content;
          $lastBlock = array_last($content);

          if ($lastBlock instanceof ToolUseBlock) {
              $toolResult = $this->handleToolUse($lastBlock->name, $lastBlock->input);

              $this->messages[] = MessageParam::with(role: 'assistant', content: $content);
              $this->messages[] = MessageParam::with(
                  role: 'user',
                  content: [
                      ToolResultBlockParam::with(toolUseID: $lastBlock->id, content: $toolResult),
                  ],
              );

              $followUpResponse = $this->generateMessage($this->messages, maxTokens: 2048);

              $firstBlock = array_find(
                  $followUpResponse->content,
                  static fn ($block): bool => $block instanceof TextBlock,
              );
              if (!$firstBlock instanceof TextBlock) {
                  throw new RuntimeException('An error occurred: Unexpected response type');
              }

              $this->messages[] = MessageParam::with(role: 'assistant', content: $firstBlock->text);

              return $firstBlock->text;
          }

          $firstBlock = array_find($content, static fn ($block): bool => $block instanceof TextBlock);
          if ($firstBlock instanceof TextBlock) {
              $this->messages[] = MessageParam::with(role: 'assistant', content: $firstBlock->text);

              return $firstBlock->text;
          }

          throw new RuntimeException('An error occurred: Unexpected response type');
      }

      /**
       * @param array<string, mixed> $funcParams
       */
      private function handleToolUse(string $funcName, array $funcParams): string
      {
          if ($funcName === 'get_quote') {
              $premium = get_quote(...$funcParams);

              return sprintf('Quote generated: $%.2f per month', $premium);
          }

          throw new RuntimeException('An unexpected tool was used');
      }
  }
  ```

  ```ruby Ruby
  # IDENTITY, MODEL, TOOLS, and get_quote mirror the config.py values defined
  # earlier in this guide (shown in Python).
  require "anthropic"

  class ChatBot
    attr_reader :messages

    def initialize
      @anthropic = Anthropic::Client.new
      @messages = []
    end

    def generate_message(messages, max_tokens)
      @anthropic.messages.create(
        model: MODEL,
        system_: IDENTITY,
        max_tokens:,
        messages:,
        tools: TOOLS
      )
    end

    def process_user_input(user_input)
      @messages << {role: "user", content: user_input}

      response_message = generate_message(@messages, 2048)

      case response_message.content
      in [*, Anthropic::ToolUseBlock => tool_use]
        result = handle_tool_use(tool_use.name, tool_use.input)
        @messages << {role: "assistant", content: response_message.content}
        @messages << {
          role: "user",
          content: [{type: "tool_result", tool_use_id: tool_use.id, content: result}]
        }

        follow_up_response = generate_message(@messages, 2048)

        case follow_up_response.content
        in [*, Anthropic::TextBlock => text_block, *]
          @messages << {role: "assistant", content: text_block.text}
          text_block.text
        else
          raise "An error occurred: Unexpected response type"
        end
      in [*, Anthropic::TextBlock => text_block, *]
        @messages << {role: "assistant", content: text_block.text}
        text_block.text
      else
        raise "An error occurred: Unexpected response type"
      end
    end

    def handle_tool_use(tool_name, tool_input)
      raise "An unexpected tool was used" unless tool_name == "get_quote"

      premium = get_quote(**tool_input)
      format("Quote generated: $%.2f per month", premium)
    end
  end
  ```
</CodeGroup>

### Build your user interface

Test deploying this code with Streamlit using a main method. This `main()` function sets up a Streamlit-based chat interface. Streamlit is a Python framework, so this part of the walkthrough is shown in Python only; the ChatBot class above is the piece you can port to any language.

Do this in a file called `app.py`

```python
import streamlit as st
from chatbot import ChatBot
from config import TASK_SPECIFIC_INSTRUCTIONS


def main():
    st.title("Chat with Eva, Acme Insurance Company's Assistant🤖")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "content": TASK_SPECIFIC_INSTRUCTIONS},
            {"role": "assistant", "content": "Understood"},
        ]

    chatbot = ChatBot(st.session_state)

    # Display user and assistant messages skipping the first two
    for message in st.session_state.messages[2:]:
        # ignore tool use blocks
        if isinstance(message["content"], str):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_msg := st.chat_input("Type your message here..."):
        st.chat_message("user").markdown(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Eva is thinking..."):
                response_placeholder = st.empty()
                full_response = chatbot.process_user_input(user_msg)
                response_placeholder.markdown(full_response)


if __name__ == "__main__":
    main()
```

Run the program with:

```bash
streamlit run app.py
```

### Evaluate your prompts

Prompting often requires testing and optimization for it to be production ready. To determine the readiness of your solution, evaluate the chatbot performance using a systematic process combining quantitative and qualitative methods. Creating a [strong empirical evaluation](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests#build-evaluations) based on your defined success criteria will allow you to optimize your prompts.

### Improve performance

In complex scenarios, it may be helpful to consider additional strategies to improve performance beyond standard [prompt engineering techniques](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) & [guardrail implementation strategies](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations). Here are some common scenarios:

#### Reduce long context latency with RAG

When dealing with large amounts of static and dynamic context, including all information in the prompt can lead to high costs, slower response times, and reaching context window limits. In this scenario, implementing Retrieval Augmented Generation (RAG) techniques can improve performance and efficiency.

By using [embedding models like Voyage](https://platform.claude.com/docs/en/build-with-claude/embeddings) to convert information into vector representations, you can create a more scalable and responsive system. This approach allows for dynamic retrieval of relevant information based on the current query, rather than including all possible context in every prompt.

Implementing RAG for support use cases has been shown to increase accuracy, reduce response times, and reduce API costs in systems with extensive context requirements. See the [RAG recipe](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide) for a worked example.

#### Integrate real-time data with tool use

When dealing with queries that require real-time information, such as account balances or policy details, embedding-based RAG approaches are not sufficient. Instead, tool use can enhance your chatbot's ability to provide accurate, real-time responses. For example, you can use tool use to look up customer information, retrieve order details, and cancel orders on behalf of the customer.

This approach, [outlined in the tool use: customer service agent recipe](https://platform.claude.com/cookbook/tool-use-customer-service-agent), lets you integrate live data into Claude's responses and provide a more personalized and efficient customer experience.

#### Strengthen input and output guardrails

When deploying a chatbot, especially in customer service scenarios, it's important to prevent risks associated with misuse, out-of-scope queries, and inappropriate responses. While Claude is inherently resilient to such scenarios, here are additional steps to strengthen your chatbot guardrails:

* [Reduce hallucination](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations): Implement fact-checking mechanisms and [citations](https://platform.claude.com/cookbook/misc-using-citations) to ground responses in provided information.
* Cross-check information: Verify that the agent's responses align with your company's policies and known facts.
* Avoid contractual commitments: Ensure the agent doesn't make promises or enter into agreements it's not authorized to make.
* [Mitigate jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks): Use methods like harmlessness screens and input validation to prevent users from exploiting model vulnerabilities, aiming to generate inappropriate content.
* Avoid mentioning competitors: Implement a competitor mention filter to maintain brand focus and not mention any competitor's products or services.
* [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency): Prevent Claude from changing style or going out of character, even during long, complex interactions.
* Remove Personally Identifiable Information (PII): Unless explicitly required and authorized, strip out any PII from responses.

#### Reduce perceived response time with streaming

When dealing with potentially lengthy responses, implementing streaming can improve user engagement and satisfaction. In this scenario, users receive the answer progressively instead of waiting for the entire response to be generated.

Here is how to implement streaming:

1. Use the [Anthropic Streaming API](https://platform.claude.com/docs/en/build-with-claude/streaming) to support streaming responses.
2. Set up your frontend to handle incoming chunks of text.
3. Display each chunk as it arrives, simulating real-time typing.
4. Implement a mechanism to save the full response, allowing users to view it if they navigate away and return.

In some cases, streaming enables the use of more advanced models with higher base latencies, as the progressive display mitigates the impact of longer processing times.

#### Scale your chatbot

As the complexity of your chatbot grows, your application architecture can evolve to match. Before you add further layers to your architecture, consider the following less exhaustive options:

* Ensure that you are making the most out of your prompts and optimizing through prompt engineering. Use the [prompt engineering guides](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) to write the most effective prompts.
* Add additional [tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) to the prompt (which can include [prompt chains](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#chain-complex-prompts)) and see if you can achieve the functionality required.

If your chatbot handles incredibly varied tasks, you may want to consider adding a [separate intent classifier](https://platform.claude.com/cookbook/capabilities-classification-guide) to route the initial customer query. For the existing application, this would involve creating a decision tree that would route customer queries through the classifier and then to specialized conversations (with their own set of tools and system prompts). Note, this method requires an additional call to Claude that can increase latency.

### Integrate Claude into your support workflow

While these examples have focused on Python functions callable within a Streamlit environment, deploying Claude for real-time support chatbot requires an API service.

Here's how you can approach this:

1. Create an API wrapper: Develop a simple API wrapper around your classification function. For example, you can use Flask API or Fast API to wrap your code into a HTTP Service. Your HTTP service could accept the user input and return the Assistant response in its entirety. Thus, your service could have the following characteristics:

   * Server-Sent Events (SSE): SSE allows for real-time streaming of responses from the server to the client. This provides a smooth, interactive experience when working with LLMs.
   * Caching: Implementing caching can improve response times and reduce unnecessary API calls.
   * Context retention: Maintaining context when a user navigates away and returns is important for continuity in conversations.

2. Build a web interface: Implement a user-friendly web UI for interacting with the Claude-powered agent.

## Next steps

<CardGroup cols={2}>
  <Card title="Tool use" icon="wrench" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview">
    Give Claude access to your APIs so it can take action on behalf of customers.
  </Card>

  <Card title="Develop tests" icon="check" href="https://platform.claude.com/docs/en/test-and-evaluate/develop-tests">
    Build evaluations to measure your support agent against the success criteria you defined.
  </Card>

  <Card title="Streaming" icon="bolt" href="https://platform.claude.com/docs/en/build-with-claude/streaming">
    Stream responses so customers see answers as they generate.
  </Card>

  <Card title="Prompt engineering" icon="lightbulb" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview">
    Refine your system prompt and examples for better task performance.
  </Card>
</CardGroup>
