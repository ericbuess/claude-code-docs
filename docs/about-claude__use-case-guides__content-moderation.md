---
title: Content moderation
url: https://platform.claude.com/docs/en/about-claude/use-case-guides/content-moderation
description: Content moderation is a critical aspect of maintaining a safe, respectful, and productive environment in digital applications. This guide discusses how Claude can be used to moderate content within your digital application.
---

> Visit the [content moderation cookbook](https://platform.claude.com/cookbook/misc-building-moderation-filter) to see an example content moderation implementation using Claude.

<Tip>
  This guide is focused on moderating user-generated content within your application. If you're looking for guidance on moderating interactions with Claude, refer to 

  [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

  .
</Tip>

## Before building with Claude

### Decide whether to use Claude for content moderation

Here are some key indicators that you should use an LLM like Claude instead of a traditional ML or rules-based approach for content moderation:

<AccordionGroup>
  <Accordion title="You want a cost-effective and rapid implementation">
    Traditional ML methods require significant engineering resources, ML expertise, and infrastructure costs. Human moderation systems incur even higher costs. With Claude, you can have a sophisticated moderation system operational in significantly less time and at a much lower cost.
  </Accordion>

  <Accordion title="You want both semantic understanding and quick decisions">
    Traditional ML approaches, such as bag-of-words models or simple pattern matching, often struggle to understand the tone, intent, and context of the content. While human moderation systems excel at understanding semantic meaning, they require time for content to be reviewed. Claude addresses both needs by combining semantic understanding with the ability to deliver moderation decisions quickly.
  </Accordion>

  <Accordion title="You need consistent policy decisions">
    By leveraging its advanced reasoning capabilities, Claude can interpret and apply complex moderation guidelines uniformly. This consistency helps ensure fair treatment of all content, reducing the risk of inconsistent or biased moderation decisions that can undermine user trust.
  </Accordion>

  <Accordion title="Your moderation policies are likely to change or evolve over time">
    Once a traditional ML approach has been established, changing it is a laborious and data-intensive undertaking. On the other hand, as your product or customer needs evolve, Claude can easily adapt to changes or additions to moderation policies without extensive relabeling of training data.
  </Accordion>

  <Accordion title="You require interpretable reasoning for your moderation decisions">
    If you want to provide users or regulators with clear explanations behind moderation decisions, Claude can generate detailed and coherent justifications. This transparency is important for building trust and ensuring accountability in content moderation practices.
  </Accordion>

  <Accordion title="You need multilingual support without maintaining separate models">
    Traditional ML approaches typically require separate models or extensive translation processes for each supported language. Human moderation requires hiring a workforce fluent in each supported language. Claude’s multilingual capabilities allow it to classify tickets in various languages without the need for separate models or extensive translation processes, streamlining moderation for global customer bases.
  </Accordion>

  <Accordion title="You require multimodal support">
    Claude's multimodal capabilities allow it to analyze and interpret content across both text and images. This makes it a versatile tool for comprehensive content moderation in environments where different media types need to be evaluated together.
  </Accordion>
</AccordionGroup>

<Note>
  All Claude models are trained with built-in safety behaviors. This may result in Claude moderating content deemed particularly dangerous (in line with the 

  [Acceptable Use Policy](https://www.anthropic.com/legal/aup)

  ), regardless of the prompt used. For example, an adult website that wants to allow users to post explicit sexual content may find that Claude still flags explicit content as requiring moderation, even if they specify in their prompt not to moderate explicit sexual content. Consider reviewing the AUP in advance of building a moderation solution.
</Note>

### Generate examples of content to moderate

Before developing a content moderation solution, first create examples of content that should be flagged and content that should not be flagged. Ensure that you include edge cases and challenging scenarios that may be difficult for a content moderation system to handle effectively. Afterward, review your examples to create a well-defined list of moderation categories. For instance, the examples generated by a social media platform might include the following:

<CodeGroup exclude="shell">
  ```python Python
  client = anthropic.Anthropic()

  allowed_user_comments = [
      "This movie was great, I really enjoyed it. The main actor really killed it!",
      "I hate Mondays.",
      "It is a great time to invest in gold!",
  ]

  disallowed_user_comments = [
      "Delete this post now or you better hide. I am coming after you and your family.",
      "Stay away from the 5G cellphones!! They are using 5G to control you.",
      "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
  ]

  # Sample user comments to test the content moderation
  user_comments = allowed_user_comments + disallowed_user_comments

  # Categories considered unsafe for content moderation
  unsafe_categories = [
      "Child Exploitation",
      "Conspiracy Theories",
      "Hate",
      "Indiscriminate Weapons",
      "Intellectual Property",
      "Non-Violent Crimes",
      "Privacy",
      "Self-Harm",
      "Sex Crimes",
      "Sexual Content",
      "Specialized Advice",
      "Violent Crimes",
  ]
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const allowedUserComments = [
    "This movie was great, I really enjoyed it. The main actor really killed it!",
    "I hate Mondays.",
    "It is a great time to invest in gold!"
  ];

  const disallowedUserComments = [
    "Delete this post now or you better hide. I am coming after you and your family.",
    "Stay away from the 5G cellphones!! They are using 5G to control you.",
    "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!"
  ];

  // Sample user comments to test the content moderation
  const userComments = [...allowedUserComments, ...disallowedUserComments];

  // Categories considered unsafe for content moderation
  const unsafeCategories = [
    "Child Exploitation",
    "Conspiracy Theories",
    "Hate",
    "Indiscriminate Weapons",
    "Intellectual Property",
    "Non-Violent Crimes",
    "Privacy",
    "Self-Harm",
    "Sex Crimes",
    "Sexual Content",
    "Specialized Advice",
    "Violent Crimes"
  ];
  ```

  ```csharp C#
  var client = new AnthropicClient();

  string[] allowedUserComments =
  [
      "This movie was great, I really enjoyed it. The main actor really killed it!",
      "I hate Mondays.",
      "It is a great time to invest in gold!",
  ];

  string[] disallowedUserComments =
  [
      "Delete this post now or you better hide. I am coming after you and your family.",
      "Stay away from the 5G cellphones!! They are using 5G to control you.",
      "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
  ];

  // Sample user comments to test the content moderation
  string[] userComments = [.. allowedUserComments, .. disallowedUserComments];

  // Categories considered unsafe for content moderation
  string[] unsafeCategories =
  [
      "Child Exploitation",
      "Conspiracy Theories",
      "Hate",
      "Indiscriminate Weapons",
      "Intellectual Property",
      "Non-Violent Crimes",
      "Privacy",
      "Self-Harm",
      "Sex Crimes",
      "Sexual Content",
      "Specialized Advice",
      "Violent Crimes",
  ];
  ```

  ```go Go
  var client = anthropic.NewClient()

  var allowedUserComments = []string{
  	"This movie was great, I really enjoyed it. The main actor really killed it!",
  	"I hate Mondays.",
  	"It is a great time to invest in gold!",
  }

  var disallowedUserComments = []string{
  	"Delete this post now or you better hide. I am coming after you and your family.",
  	"Stay away from the 5G cellphones!! They are using 5G to control you.",
  	"Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
  }

  // Sample user comments to test the content moderation
  var userComments = slices.Concat(allowedUserComments, disallowedUserComments)

  // Categories considered unsafe for content moderation
  var unsafeCategories = []string{
  	"Child Exploitation",
  	"Conspiracy Theories",
  	"Hate",
  	"Indiscriminate Weapons",
  	"Intellectual Property",
  	"Non-Violent Crimes",
  	"Privacy",
  	"Self-Harm",
  	"Sex Crimes",
  	"Sexual Content",
  	"Specialized Advice",
  	"Violent Crimes",
  }

  ```

  ```java Java
  final AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  final List<String> allowedUserComments = List.of(
          "This movie was great, I really enjoyed it. The main actor really killed it!",
          "I hate Mondays.",
          "It is a great time to invest in gold!");

  final List<String> disallowedUserComments = List.of(
          "Delete this post now or you better hide. I am coming after you and your family.",
          "Stay away from the 5G cellphones!! They are using 5G to control you.",
          "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!");

  // Sample user comments to test the content moderation
  final List<String> userComments =
          Stream.concat(allowedUserComments.stream(), disallowedUserComments.stream()).toList();

  // Categories considered unsafe for content moderation
  final List<String> unsafeCategories = List.of(
          "Child Exploitation",
          "Conspiracy Theories",
          "Hate",
          "Indiscriminate Weapons",
          "Intellectual Property",
          "Non-Violent Crimes",
          "Privacy",
          "Self-Harm",
          "Sex Crimes",
          "Sexual Content",
          "Specialized Advice",
          "Violent Crimes");
  ```

  ```php PHP
  $client = new Client();

  $allowedUserComments = [
      'This movie was great, I really enjoyed it. The main actor really killed it!',
      'I hate Mondays.',
      'It is a great time to invest in gold!',
  ];

  $disallowedUserComments = [
      'Delete this post now or you better hide. I am coming after you and your family.',
      'Stay away from the 5G cellphones!! They are using 5G to control you.',
      'Congratulations! You have won a $1,000 gift card. Click here to claim your prize!',
  ];

  // Sample user comments to test the content moderation
  $userComments = [...$allowedUserComments, ...$disallowedUserComments];

  // Categories considered unsafe for content moderation
  $unsafeCategories = [
      'Child Exploitation',
      'Conspiracy Theories',
      'Hate',
      'Indiscriminate Weapons',
      'Intellectual Property',
      'Non-Violent Crimes',
      'Privacy',
      'Self-Harm',
      'Sex Crimes',
      'Sexual Content',
      'Specialized Advice',
      'Violent Crimes',
  ];
  ```

  ```ruby Ruby
  CLIENT = Anthropic::Client.new

  ALLOWED_USER_COMMENTS = [
    "This movie was great, I really enjoyed it. The main actor really killed it!",
    "I hate Mondays.",
    "It is a great time to invest in gold!"
  ]

  DISALLOWED_USER_COMMENTS = [
    "Delete this post now or you better hide. I am coming after you and your family.",
    "Stay away from the 5G cellphones!! They are using 5G to control you.",
    "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!"
  ]

  # Sample user comments to test the content moderation
  USER_COMMENTS = ALLOWED_USER_COMMENTS + DISALLOWED_USER_COMMENTS

  # Categories considered unsafe for content moderation
  UNSAFE_CATEGORIES = [
    "Child Exploitation",
    "Conspiracy Theories",
    "Hate",
    "Indiscriminate Weapons",
    "Intellectual Property",
    "Non-Violent Crimes",
    "Privacy",
    "Self-Harm",
    "Sex Crimes",
    "Sexual Content",
    "Specialized Advice",
    "Violent Crimes"
  ]
  ```
</CodeGroup>

Effectively moderating these examples requires a nuanced understanding of language. In the comment, `This movie was great, I really enjoyed it. The main actor really killed it!`, the content moderation system needs to recognize that "killed it" is a metaphor, not an indication of actual violence. Conversely, despite the lack of explicit mentions of violence, the comment `Delete this post now or you better hide. I am coming after you and your family.` should be flagged by the content moderation system.

The unsafe categories can be customized to fit your specific needs. For example, if you want to prevent minors from creating content on your website, you could add "Underage Posting" to the categories.

***

## How to moderate content using Claude

### Select the right Claude model

When selecting a model, it’s important to consider the size of your data. If costs are a concern, a smaller model such as Claude Haiku 4.5 is an excellent choice because of its cost-effectiveness. The following is an estimate of the cost to moderate text for a social media platform that receives one billion posts per month:

* **Content size**

  * Posts per month: 1B
  * Characters per post: 100
  * Total characters: 100B

* **Estimated tokens**

  * Input tokens: 28.6B (assuming 1 token per 3.5 characters)
  * Percentage of messages flagged: 3%
  * Output tokens per flagged message: 50
  * Total output tokens: 1.5B

* **Claude Haiku 4.5 estimated cost**

  * Input token cost: 28,600 MTok \* $1.00/MTok = $28,600 USD
  * Output token cost: 1,500 MTok \* $5.00/MTok = $7,500 USD
  * Monthly cost: $28,600 + $7,500 = $36,100 USD

* **Claude Opus 5 estimated cost**

  * Input token cost: 28,600 MTok \* $5.00/MTok = $143,000 USD
  * Output token cost: 1,500 MTok \* $25.00/MTok = $37,500 USD
  * Monthly cost: $143,000 + $37,500 = $180,500 USD

* **Claude Opus 4.8 estimated cost**

  * Input token cost: 28,600 MTok \* $5.00/MTok = $143,000 USD
  * Output token cost: 1,500 MTok \* $25.00/MTok = $37,500 USD
  * Monthly cost: $143,000 + $37,500 = $180,500 USD

<Tip>
  Actual costs may differ from these estimates. These estimates are based on the prompt highlighted in the section on 

  [batch processing](https://platform.claude.com/docs/en/about-claude/use-case-guides/content-moderation#consider-batch-processing)

  . Output tokens can be reduced even further by removing the 

  `explanation`

   field from the response.
</Tip>

### Build a strong prompt

To use Claude for content moderation, Claude must understand the moderation requirements of your application. Start by writing a prompt that allows you to define your moderation needs:

<CodeGroup exclude="shell">
  ```python Python
  def moderate_message(message, unsafe_categories):
      # Convert the unsafe categories into a string, with each category on a new line
      unsafe_category_str = "\n".join(unsafe_categories)

      # Construct the prompt for Claude, including the message and unsafe categories
      assessment_prompt = f"""
      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>{message}</message>

      Unsafe Categories:
      <categories>
      {unsafe_category_str}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {{
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }}
  Do not include markdown formatting or code fences in your response."""

      # Send the request to Claude for content moderation
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=200,
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse the JSON response from Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)

      # Extract the violation status from the assessment
      contains_violation = assessment["violation"]

      # If there's a violation, get the categories and explanation; otherwise, use empty defaults
      violated_categories = assessment.get("categories", []) if contains_violation else []
      explanation = assessment.get("explanation") if contains_violation else None

      return contains_violation, violated_categories, explanation


  # Process each comment and print the results
  for comment in user_comments:
      print(f"\nComment: {comment}")
      violation, violated_categories, explanation = moderate_message(
          comment, unsafe_categories
      )

      if violation:
          print(f"Violated Categories: {', '.join(violated_categories)}")
          print(f"Explanation: {explanation}")
      else:
          print("No issues detected.")
  ```

  ```typescript TypeScript
  // Shape of the JSON assessment Claude returns
  interface ModerationAssessment {
    violation: boolean;
    categories?: string[];
    explanation?: string;
  }

  async function moderateMessage(
    message: string,
    unsafeCategories: string[]
  ): Promise<{ violation: boolean; violatedCategories: string[]; explanation?: string }> {
    // Convert the unsafe categories into a string, with each category on a new line
    const unsafeCategoryStr = unsafeCategories.join("\n");

    // Construct the prompt for Claude, including the message and unsafe categories
    const assessmentPrompt = `
      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>${message}</message>

      Unsafe Categories:
      <categories>
      ${unsafeCategoryStr}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }
  Do not include markdown formatting or code fences in your response.`;

    // Send the request to Claude for content moderation
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse the JSON response from Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: ModerationAssessment = JSON.parse(textBlock.text);

    // Extract the violation status from the assessment
    const containsViolation = assessment.violation;

    // If there's a violation, get the categories and explanation; otherwise, use empty defaults
    const violatedCategories = containsViolation ? assessment.categories ?? [] : [];
    const explanation = containsViolation ? assessment.explanation : undefined;

    return { violation: containsViolation, violatedCategories, explanation };
  }

  // Process each comment and print the results
  for (const comment of userComments) {
    console.log(`\nComment: ${comment}`);
    const { violation, violatedCategories, explanation } = await moderateMessage(
      comment,
      unsafeCategories
    );

    if (violation) {
      console.log(`Violated Categories: ${violatedCategories.join(", ")}`);
      console.log(`Explanation: ${explanation}`);
    } else {
      console.log("No issues detected.");
    }
  }
  ```

  ```csharp C#
  async Task<(bool ContainsViolation, List<string> ViolatedCategories, string? Explanation)> ModerateMessage(
      string message,
      IReadOnlyList<string> categories
  )
  {
      // Convert the unsafe categories into a string, with each category on a new line
      var unsafeCategoryText = string.Join("\n", categories);

      // Construct the prompt for Claude, including the message and unsafe categories
      var assessmentPrompt = $$"""

      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>{{message}}</message>

      Unsafe Categories:
      <categories>
      {{unsafeCategoryText}}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }
  Do not include markdown formatting or code fences in your response.
  """;

      // Send the request to Claude for content moderation
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 200,
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Narrow the first content block to a text block, then parse Claude's JSON response
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      var assessment = JsonNode.Parse(textBlock.Text)!;

      // Extract the violation status from the assessment
      var containsViolation = assessment["violation"]!.GetValue<bool>();

      // If there's a violation, get the categories and explanation; otherwise, use empty defaults
      List<string> violatedCategories = containsViolation
          ? assessment["categories"]?.AsArray().Select(category => category!.GetValue<string>()).ToList() ?? []
          : [];
      var explanation = containsViolation ? assessment["explanation"]?.GetValue<string>() : null;

      return (containsViolation, violatedCategories, explanation);
  }

  // Process each comment and print the results
  foreach (var comment in userComments)
  {
      Console.WriteLine($"\nComment: {comment}");
      var (violation, violatedCategories, explanation) = await ModerateMessage(comment, unsafeCategories);

      if (violation)
      {
          Console.WriteLine($"Violated Categories: {string.Join(", ", violatedCategories)}");
          Console.WriteLine($"Explanation: {explanation}");
      }
      else
      {
          Console.WriteLine("No issues detected.");
      }
  }
  ```

  ```go Go
  func moderateMessage(message string, unsafeCategories []string) (bool, []string, string) {
  	// Convert the unsafe categories into a string, with each category on a new line
  	unsafeCategoryStr := strings.Join(unsafeCategories, "\n")

  	// Construct the prompt for Claude, including the message and unsafe categories
  	assessmentPrompt := fmt.Sprintf(`
      Determine whether the following message warrants moderation,
      based on the unsafe categories outlined below.

      Message:
      <message>%s</message>

      Unsafe Categories:
      <categories>
      %s
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
      "violation": <Boolean field denoting whether the message should be moderated>,
      "categories": [Comma-separated list of violated categories],
      "explanation": [Optional. Only include if there is a violation.]
      }
  Do not include markdown formatting or code fences in your response.`, message, unsafeCategoryStr)

  	// Send the request to Claude for content moderation
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 200,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Narrow the first content block to a text block before reading its text
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Parse the JSON response from Claude
  	var assessment struct {
  		Violation   bool     `json:"violation"`
  		Categories  []string `json:"categories"`
  		Explanation string   `json:"explanation"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}

  	// If there's a violation, return the categories and explanation; otherwise, use empty defaults
  	if !assessment.Violation {
  		return false, nil, ""
  	}
  	return true, assessment.Categories, assessment.Explanation
  }

  // moderateAllComments processes each comment and prints the results.
  func moderateAllComments() {
  	for _, comment := range userComments {
  		fmt.Printf("\nComment: %s\n", comment)
  		violation, violatedCategories, explanation := moderateMessage(comment, unsafeCategories)

  		if violation {
  			fmt.Printf("Violated Categories: %s\n", strings.Join(violatedCategories, ", "))
  			fmt.Printf("Explanation: %s\n", explanation)
  		} else {
  			fmt.Println("No issues detected.")
  		}
  	}
  }

  ```

  ```java Java
  record ModerationResult(boolean violation, List<String> violatedCategories, String explanation) {}

  ModerationResult moderateMessage(String message, List<String> unsafeCategories)
          throws JsonProcessingException {
      // Convert the unsafe categories into a string, with each category on a new line
      String unsafeCategoryStr = String.join("\n", unsafeCategories);

      // Construct the prompt for Claude, including the message and unsafe categories
      String assessmentPrompt = """

              Determine whether the following message warrants moderation,
              based on the unsafe categories outlined below.

              Message:
              <message>%s</message>

              Unsafe Categories:
              <categories>
              %s
              </categories>

              Respond with ONLY a JSON object, using the format below:
              {
              "violation": <Boolean field denoting whether the message should be moderated>,
              "categories": [Comma-separated list of violated categories],
              "explanation": [Optional. Only include if there is a violation.]
              }
          Do not include markdown formatting or code fences in your response."""
              .formatted(message, unsafeCategoryStr);

      // Send the request to Claude for content moderation
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(200)
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse the JSON response from Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      ObjectMapper mapper = new ObjectMapper();
      JsonNode assessment = mapper.readTree(assessmentJson);

      // Extract the violation status from the assessment
      boolean containsViolation = assessment.required("violation").asBoolean();

      // If there's a violation, get the categories and explanation; otherwise, use empty defaults
      List<String> violatedCategories = containsViolation && assessment.has("categories")
              ? mapper.convertValue(assessment.get("categories"), new TypeReference<List<String>>() {})
              : List.of();
      String explanation = containsViolation && assessment.hasNonNull("explanation")
              ? assessment.get("explanation").asText()
              : null;

      return new ModerationResult(containsViolation, violatedCategories, explanation);
  }

  // Process each comment and print the results
  void printModerationResults() throws JsonProcessingException {
      for (String comment : userComments) {
          IO.println("\nComment: " + comment);
          ModerationResult result = moderateMessage(comment, unsafeCategories);

          if (result.violation()) {
              IO.println("Violated Categories: " + String.join(", ", result.violatedCategories()));
              IO.println("Explanation: " + result.explanation());
          } else {
              IO.println("No issues detected.");
          }
      }
  }
  ```

  ```php PHP
  $moderateMessage = function (string $message, array $unsafeCategories) use ($client): array {
      // Convert the unsafe categories into a string, with each category on a new line
      $unsafeCategoryStr = implode("\n", $unsafeCategories);

      // Construct the prompt for Claude, including the message and unsafe categories
      $assessmentPrompt = <<<PROMPT

          Determine whether the following message warrants moderation,
          based on the unsafe categories outlined below.

          Message:
          <message>{$message}</message>

          Unsafe Categories:
          <categories>
          {$unsafeCategoryStr}
          </categories>

          Respond with ONLY a JSON object, using the format below:
          {
          "violation": <Boolean field denoting whether the message should be moderated>,
          "categories": [Comma-separated list of violated categories],
          "explanation": [Optional. Only include if there is a violation.]
          }
      Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Send the request to Claude for content moderation
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 200,
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse the JSON response from Claude. The SDK decodes each content block
      // into its concrete class, so find the TextBlock before reading the text.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');
      $assessment = json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);

      // Extract the violation status from the assessment
      $containsViolation = $assessment['violation'];

      // If there's a violation, get the categories and explanation; otherwise, use empty defaults
      $violatedCategories = $containsViolation ? ($assessment['categories'] ?? []) : [];
      $explanation = $containsViolation ? ($assessment['explanation'] ?? null) : null;

      return [$containsViolation, $violatedCategories, $explanation];
  };

  // Process each comment and print the results
  foreach ($userComments as $comment) {
      echo "\nComment: {$comment}\n";
      [$violation, $violatedCategories, $explanation] = $moderateMessage($comment, $unsafeCategories);

      if ($violation) {
          echo 'Violated Categories: ' . implode(', ', $violatedCategories) . "\n";
          echo "Explanation: {$explanation}\n";
      } else {
          echo "No issues detected.\n";
      }
  }
  ```

  ```ruby Ruby
  def moderate_message(message, unsafe_categories)
    # Convert the unsafe categories into a string, with each category on a new line
    unsafe_category_str = unsafe_categories.join("\n")

    # Construct the prompt for Claude, including the message and unsafe categories
    assessment_prompt = <<~PROMPT.chomp

          Determine whether the following message warrants moderation,
          based on the unsafe categories outlined below.

          Message:
          <message>#{message}</message>

          Unsafe Categories:
          <categories>
          #{unsafe_category_str}
          </categories>

          Respond with ONLY a JSON object, using the format below:
          {
          "violation": <Boolean field denoting whether the message should be moderated>,
          "categories": [Comma-separated list of violated categories],
          "explanation": [Optional. Only include if there is a violation.]
          }
      Do not include markdown formatting or code fences in your response.
    PROMPT

    # Send the request to Claude for content moderation
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse the JSON response from Claude
    text_block = response.content.find { it.type == :text }
    assessment = JSON.parse(text_block.text)

    # Extract the violation status from the assessment
    contains_violation = assessment["violation"]

    # If there's a violation, get the categories and explanation; otherwise, use empty defaults
    violated_categories = contains_violation ? assessment.fetch("categories", []) : []
    explanation = contains_violation ? assessment["explanation"] : nil

    [contains_violation, violated_categories, explanation]
  end


  # Process each comment and print the results
  USER_COMMENTS.each do |comment|
    puts "\nComment: #{comment}"
    violation, violated_categories, explanation = moderate_message(comment, UNSAFE_CATEGORIES)

    if violation
      puts "Violated Categories: #{violated_categories.join(", ")}"
      puts "Explanation: #{explanation}"
    else
      puts "No issues detected."
    end
  end
  ```
</CodeGroup>

In this example, the `moderate_message` function contains an assessment prompt that includes the unsafe content categories and the message to evaluate. The prompt asks Claude to assess whether the message should be moderated, based on the unsafe categories you defined earlier.

The model's assessment is then parsed to determine if there is a violation. If there is a violation, Claude also returns a list of violated categories and an explanation as to why the message is unsafe.

### Evaluate your prompt

Content moderation is a classification problem. Thus, you can use the same techniques outlined in the [classification cookbook](https://platform.claude.com/cookbook/capabilities-classification-guide) to determine the accuracy of your content moderation system.

One additional consideration is that instead of treating content moderation as a binary classification problem, you may instead create multiple categories to represent various risk levels. Creating multiple risk levels allows you to adjust the aggressiveness of your moderation. For example, you might want to automatically block user queries that are deemed high risk, while users with many medium risk queries are flagged for human review.

<CodeGroup exclude="shell">
  ```python Python
  def assess_risk_level(message, unsafe_categories):
      # Convert the unsafe categories into a string, with each category on a new line
      unsafe_category_str = "\n".join(unsafe_categories)

      # Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
      assessment_prompt = f"""
      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>{message}</message>

  Unsafe Categories:
  <categories>
  {unsafe_category_str}
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {{
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }}
  Do not include markdown formatting or code fences in your response."""

      # Send the request to Claude for risk assessment
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=200,
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse the JSON response from Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)

      # Extract the risk level, violated categories, and explanation from the assessment
      risk_level = assessment["risk_level"]
      violated_categories = assessment["categories"]
      explanation = assessment.get("explanation")

      return risk_level, violated_categories, explanation


  # Process each comment and print the results
  for comment in user_comments:
      print(f"\nComment: {comment}")
      risk_level, violated_categories, explanation = assess_risk_level(
          comment, unsafe_categories
      )

      print(f"Risk Level: {risk_level}")
      if violated_categories:
          print(f"Violated Categories: {', '.join(violated_categories)}")
      if explanation:
          print(f"Explanation: {explanation}")
  ```

  ```typescript TypeScript
  // Shape of the JSON risk assessment Claude returns
  interface RiskAssessment {
    risk_level: number;
    categories: string[];
    explanation?: string;
  }

  async function assessRiskLevel(
    message: string,
    unsafeCategories: string[]
  ): Promise<{ riskLevel: number; violatedCategories: string[]; explanation?: string }> {
    // Convert the unsafe categories into a string, with each category on a new line
    const unsafeCategoryStr = unsafeCategories.join("\n");

    // Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
    const assessmentPrompt = `
      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>${message}</message>

  Unsafe Categories:
  <categories>
  ${unsafeCategoryStr}
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }
  Do not include markdown formatting or code fences in your response.`;

    // Send the request to Claude for risk assessment
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse the JSON response from Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: RiskAssessment = JSON.parse(textBlock.text);

    // Extract the risk level, violated categories, and explanation from the assessment
    const { risk_level: riskLevel, categories: violatedCategories, explanation } = assessment;

    return { riskLevel, violatedCategories, explanation };
  }

  // Process each comment and print the results
  for (const comment of userComments) {
    console.log(`\nComment: ${comment}`);
    const { riskLevel, violatedCategories, explanation } = await assessRiskLevel(
      comment,
      unsafeCategories
    );

    console.log(`Risk Level: ${riskLevel}`);
    if (violatedCategories.length > 0) {
      console.log(`Violated Categories: ${violatedCategories.join(", ")}`);
    }
    if (explanation) {
      console.log(`Explanation: ${explanation}`);
    }
  }
  ```

  ```csharp C#
  async Task<(int RiskLevel, List<string> ViolatedCategories, string? Explanation)> AssessRiskLevel(
      string message,
      IReadOnlyList<string> categories
  )
  {
      // Convert the unsafe categories into a string, with each category on a new line
      var unsafeCategoryText = string.Join("\n", categories);

      // Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
      var assessmentPrompt = $$"""

      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>{{message}}</message>

  Unsafe Categories:
  <categories>
  {{unsafeCategoryText}}
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }
  Do not include markdown formatting or code fences in your response.
  """;

      // Send the request to Claude for risk assessment
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 200,
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Narrow the first content block to a text block, then parse Claude's JSON response
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      var assessment = JsonNode.Parse(textBlock.Text)!;

      // Extract the risk level, violated categories, and explanation from the assessment
      var riskLevel = assessment["risk_level"]!.GetValue<int>();
      var violatedCategories = assessment["categories"]!
          .AsArray()
          .Select(category => category!.GetValue<string>())
          .ToList();
      var explanation = assessment["explanation"]?.GetValue<string>();

      return (riskLevel, violatedCategories, explanation);
  }

  // Process each comment and print the results
  foreach (var comment in userComments)
  {
      Console.WriteLine($"\nComment: {comment}");
      var (riskLevel, violatedCategories, explanation) = await AssessRiskLevel(comment, unsafeCategories);

      Console.WriteLine($"Risk Level: {riskLevel}");
      if (violatedCategories.Count > 0)
      {
          Console.WriteLine($"Violated Categories: {string.Join(", ", violatedCategories)}");
      }
      if (!string.IsNullOrEmpty(explanation))
      {
          Console.WriteLine($"Explanation: {explanation}");
      }
  }
  ```

  ```go Go
  func assessRiskLevel(message string, unsafeCategories []string) (int, []string, string) {
  	// Convert the unsafe categories into a string, with each category on a new line
  	unsafeCategoryStr := strings.Join(unsafeCategories, "\n")

  	// Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
  	assessmentPrompt := fmt.Sprintf(`
      Assess the risk level of the following message,
      based on the unsafe categories listed below.

  Message:
  <message>%s</message>

  Unsafe Categories:
  <categories>
  %s
  </categories>

  Assign a risk level based on your confidence that the user's message should be moderated
  based on the defined unsafe categories:

  0 - No risk
  1 - Low risk
  2 - Medium risk
  3 - High risk

  Respond with ONLY a JSON object, using the format below:
  {
    "risk_level": <Numerical field denoting the risk level>,
    "categories": [Comma-separated list of violated categories],
    "explanation": <Optional. Only include if risk level is greater than 0>
  }
  Do not include markdown formatting or code fences in your response.`, message, unsafeCategoryStr)

  	// Send the request to Claude for risk assessment
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 200,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Narrow the first content block to a text block before reading its text
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Parse the JSON response from Claude
  	var assessment struct {
  		RiskLevel   int      `json:"risk_level"`
  		Categories  []string `json:"categories"`
  		Explanation string   `json:"explanation"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}

  	// Return the risk level, violated categories, and explanation from the assessment
  	return assessment.RiskLevel, assessment.Categories, assessment.Explanation
  }

  // assessAllRiskLevels processes each comment and prints the results.
  func assessAllRiskLevels() {
  	for _, comment := range userComments {
  		fmt.Printf("\nComment: %s\n", comment)
  		riskLevel, violatedCategories, explanation := assessRiskLevel(comment, unsafeCategories)

  		fmt.Printf("Risk Level: %d\n", riskLevel)
  		if len(violatedCategories) > 0 {
  			fmt.Printf("Violated Categories: %s\n", strings.Join(violatedCategories, ", "))
  		}
  		if explanation != "" {
  			fmt.Printf("Explanation: %s\n", explanation)
  		}
  	}
  }

  ```

  ```java Java
  record RiskAssessment(int riskLevel, List<String> violatedCategories, String explanation) {}

  RiskAssessment assessRiskLevel(String message, List<String> unsafeCategories)
          throws JsonProcessingException {
      // Convert the unsafe categories into a string, with each category on a new line
      String unsafeCategoryStr = String.join("\n", unsafeCategories);

      // Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
      String assessmentPrompt = """

              Assess the risk level of the following message,
              based on the unsafe categories listed below.

          Message:
          <message>%s</message>

          Unsafe Categories:
          <categories>
          %s
          </categories>

          Assign a risk level based on your confidence that the user's message should be moderated
          based on the defined unsafe categories:

          0 - No risk
          1 - Low risk
          2 - Medium risk
          3 - High risk

          Respond with ONLY a JSON object, using the format below:
          {
            "risk_level": <Numerical field denoting the risk level>,
            "categories": [Comma-separated list of violated categories],
            "explanation": <Optional. Only include if risk level is greater than 0>
          }
          Do not include markdown formatting or code fences in your response."""
              .formatted(message, unsafeCategoryStr);

      // Send the request to Claude for risk assessment
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(200)
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse the JSON response from Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      ObjectMapper mapper = new ObjectMapper();
      JsonNode assessment = mapper.readTree(assessmentJson);

      // Extract the risk level, violated categories, and explanation from the assessment
      int riskLevel = assessment.required("risk_level").asInt();
      JsonNode categoriesNode = assessment.required("categories");
      List<String> violatedCategories = categoriesNode.isNull()
              ? List.of()
              : mapper.convertValue(categoriesNode, new TypeReference<List<String>>() {});
      String explanation = assessment.hasNonNull("explanation")
              ? assessment.get("explanation").asText()
              : null;

      return new RiskAssessment(riskLevel, violatedCategories, explanation);
  }

  // Process each comment and print the results
  void printRiskLevels() throws JsonProcessingException {
      for (String comment : userComments) {
          IO.println("\nComment: " + comment);
          RiskAssessment assessment = assessRiskLevel(comment, unsafeCategories);

          IO.println("Risk Level: " + assessment.riskLevel());
          if (!assessment.violatedCategories().isEmpty()) {
              IO.println("Violated Categories: " + String.join(", ", assessment.violatedCategories()));
          }
          if (assessment.explanation() != null && !assessment.explanation().isEmpty()) {
              IO.println("Explanation: " + assessment.explanation());
          }
      }
  }
  ```

  ```php PHP
  $assessRiskLevel = function (string $message, array $unsafeCategories) use ($client): array {
      // Convert the unsafe categories into a string, with each category on a new line
      $unsafeCategoryStr = implode("\n", $unsafeCategories);

      // Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
      $assessmentPrompt = <<<PROMPT

          Assess the risk level of the following message,
          based on the unsafe categories listed below.

      Message:
      <message>{$message}</message>

      Unsafe Categories:
      <categories>
      {$unsafeCategoryStr}
      </categories>

      Assign a risk level based on your confidence that the user's message should be moderated
      based on the defined unsafe categories:

      0 - No risk
      1 - Low risk
      2 - Medium risk
      3 - High risk

      Respond with ONLY a JSON object, using the format below:
      {
        "risk_level": <Numerical field denoting the risk level>,
        "categories": [Comma-separated list of violated categories],
        "explanation": <Optional. Only include if risk level is greater than 0>
      }
      Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Send the request to Claude for risk assessment
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 200,
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse the JSON response from Claude. The SDK decodes each content block
      // into its concrete class, so find the TextBlock before reading the text.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');
      $assessment = json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);

      // Extract the risk level, violated categories, and explanation from the assessment
      $riskLevel = $assessment['risk_level'];
      $violatedCategories = $assessment['categories'];
      $explanation = $assessment['explanation'] ?? null;

      return [$riskLevel, $violatedCategories, $explanation];
  };

  // Process each comment and print the results
  foreach ($userComments as $comment) {
      echo "\nComment: {$comment}\n";
      [$riskLevel, $violatedCategories, $explanation] = $assessRiskLevel($comment, $unsafeCategories);

      echo "Risk Level: {$riskLevel}\n";
      if ($violatedCategories) {
          echo 'Violated Categories: ' . implode(', ', $violatedCategories) . "\n";
      }
      if ($explanation) {
          echo "Explanation: {$explanation}\n";
      }
  }
  ```

  ```ruby Ruby
  def assess_risk_level(message, unsafe_categories)
    # Convert the unsafe categories into a string, with each category on a new line
    unsafe_category_str = unsafe_categories.join("\n")

    # Construct the prompt for Claude, including the message, unsafe categories, and risk level definitions
    assessment_prompt = <<~PROMPT.chomp

          Assess the risk level of the following message,
          based on the unsafe categories listed below.

      Message:
      <message>#{message}</message>

      Unsafe Categories:
      <categories>
      #{unsafe_category_str}
      </categories>

      Assign a risk level based on your confidence that the user's message should be moderated
      based on the defined unsafe categories:

      0 - No risk
      1 - Low risk
      2 - Medium risk
      3 - High risk

      Respond with ONLY a JSON object, using the format below:
      {
        "risk_level": <Numerical field denoting the risk level>,
        "categories": [Comma-separated list of violated categories],
        "explanation": <Optional. Only include if risk level is greater than 0>
      }
      Do not include markdown formatting or code fences in your response.
    PROMPT

    # Send the request to Claude for risk assessment
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse the JSON response from Claude
    text_block = response.content.find { it.type == :text }
    assessment = JSON.parse(text_block.text)

    # Extract the risk level, violated categories, and explanation from the assessment
    risk_level = assessment["risk_level"]
    violated_categories = assessment["categories"]
    explanation = assessment["explanation"]

    [risk_level, violated_categories, explanation]
  end


  # Process each comment and print the results
  USER_COMMENTS.each do |comment|
    puts "\nComment: #{comment}"
    risk_level, violated_categories, explanation = assess_risk_level(comment, UNSAFE_CATEGORIES)

    puts "Risk Level: #{risk_level}"
    puts "Violated Categories: #{violated_categories.join(", ")}" if violated_categories&.any?
    puts "Explanation: #{explanation}" if explanation
  end
  ```
</CodeGroup>

This code implements an `assess_risk_level` function that uses Claude to evaluate the risk level of a message. The function accepts a message and the unsafe categories as inputs.

Within the function, a prompt is generated for Claude, including the message to be assessed, the unsafe categories, and specific instructions for evaluating the risk level. The prompt instructs Claude to respond with a JSON object that includes the risk level, the violated categories, and an optional explanation.

This approach enables flexible content moderation by assigning risk levels. It can be seamlessly integrated into a larger system to automate content filtering or flag comments for human review based on their assessed risk level. For instance, when running this code, the comment `Delete this post now or you better hide. I am coming after you and your family.` is identified as high risk because of its dangerous threat. Conversely, the comment `Stay away from the 5G cellphones!! They are using 5G to control you.` is categorized as medium risk.

### Deploy your prompt

Once you are confident in the quality of your solution, it's time to deploy it to production. Here are some best practices to follow when using content moderation in production:

1. **Provide clear feedback to users:** When user input is blocked or a response is flagged because of content moderation, provide informative and constructive feedback to help users understand why their message was flagged and how they can rephrase it appropriately. In the earlier coding examples, this is done through the `explanation` field in the Claude response.

2. **Analyze moderated content:** Keep track of the types of content being flagged by your moderation system to identify trends and potential areas for improvement.

3. **Continuously evaluate and improve:** Regularly assess the performance of your content moderation system using metrics such as precision and recall tracking. Use this data to iteratively refine your moderation prompts, keywords, and assessment criteria.

***

## Improve performance

In complex scenarios, it may be helpful to consider additional strategies to improve performance beyond standard [prompt engineering techniques](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview). Here are some advanced strategies:

### Define topics and provide examples

In addition to listing the unsafe categories in the prompt, further improvements can be made by providing definitions and phrases related to each category.

<CodeGroup exclude="shell">
  ```python Python
  # Categories considered unsafe for content moderation, with their definitions
  unsafe_category_definitions = {
      "Child Exploitation": "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
      "Conspiracy Theories": """Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.""",
      "Hate": """Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.""",
      "Indiscriminate Weapons": "Content that enables the creation of weapons of mass destruction.",
      "Intellectual Property": "Content that violates the intellectual property rights of third parties.",
      "Non-Violent Crimes": "Content that enables, encourages, or excuses the commission of non-violent crimes.",
      "Privacy": "Content that contains sensitive, personal information about private individuals.",
      "Self-Harm": "Content that enables, encourages, or excuses acts of intentional self-harm.",
      "Sex Crimes": "Content that enables, encourages, or excuses the commission of sex crimes.",
      "Sexual Content": "Content that contains erotic descriptions or explicit depictions of sex acts.",
      "Specialized Advice": """Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.""",
      "Violent Crimes": "Content that enables, encourages, or excuses the commission of violent crimes.",
  }


  def moderate_message_with_definitions(message, unsafe_category_definitions):
      # Format unsafe categories string, with each category and its definition on a new line
      unsafe_category_str = "\n".join(
          f"{category}: {definition}"
          for category, definition in unsafe_category_definitions.items()
      )

      # Construct the prompt for Claude, including the message and unsafe categories
      assessment_prompt = f"""Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>{message}</message>

  Unsafe Categories and Their Definitions:
  <categories>
  {unsafe_category_str}
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {{
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }}
  Do not include markdown formatting or code fences in your response."""

      # Send the request to Claude for content moderation
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=200,
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse the JSON response from Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)

      # Extract the violation status from the assessment
      contains_violation = assessment["violation"]

      # If there's a violation, get the categories and explanation; otherwise, use empty defaults
      violated_categories = assessment.get("categories", []) if contains_violation else []
      explanation = assessment.get("explanation") if contains_violation else None

      return contains_violation, violated_categories, explanation


  # Process each comment and print the results
  for comment in user_comments:
      print(f"\nComment: {comment}")
      violation, violated_categories, explanation = moderate_message_with_definitions(
          comment, unsafe_category_definitions
      )

      if violation:
          print(f"Violated Categories: {', '.join(violated_categories)}")
          print(f"Explanation: {explanation}")
      else:
          print("No issues detected.")
  ```

  ```typescript TypeScript
  // Shape of the JSON assessment Claude returns
  interface DefinitionBasedAssessment {
    violation: boolean;
    categories?: string[];
    explanation?: string;
  }

  // Categories considered unsafe for content moderation, with their definitions
  // (object keys preserve insertion order, so categories render in this order)
  const unsafeCategoryDefinitions: Record<string, string> = {
    "Child Exploitation":
      "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
    "Conspiracy Theories": `Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.`,
    "Hate": `Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.`,
    "Indiscriminate Weapons":
      "Content that enables the creation of weapons of mass destruction.",
    "Intellectual Property":
      "Content that violates the intellectual property rights of third parties.",
    "Non-Violent Crimes":
      "Content that enables, encourages, or excuses the commission of non-violent crimes.",
    "Privacy":
      "Content that contains sensitive, personal information about private individuals.",
    "Self-Harm": "Content that enables, encourages, or excuses acts of intentional self-harm.",
    "Sex Crimes": "Content that enables, encourages, or excuses the commission of sex crimes.",
    "Sexual Content":
      "Content that contains erotic descriptions or explicit depictions of sex acts.",
    "Specialized Advice": `Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.`,
    "Violent Crimes":
      "Content that enables, encourages, or excuses the commission of violent crimes."
  };

  async function moderateMessageWithDefinitions(
    message: string,
    unsafeCategoryDefinitions: Record<string, string>
  ): Promise<{ violation: boolean; violatedCategories: string[]; explanation?: string }> {
    // Format the unsafe categories string, with each category and its definition on a new line
    const unsafeCategoryStr = Object.entries(unsafeCategoryDefinitions)
      .map(([category, definition]) => `${category}: ${definition}`)
      .join("\n");

    // Construct the prompt for Claude, including the message and unsafe categories
    const assessmentPrompt = `Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>${message}</message>

  Unsafe Categories and Their Definitions:
  <categories>
  ${unsafeCategoryStr}
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }
  Do not include markdown formatting or code fences in your response.`;

    // Send the request to Claude for content moderation
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse the JSON response from Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: DefinitionBasedAssessment = JSON.parse(textBlock.text);

    // Extract the violation status from the assessment
    const containsViolation = assessment.violation;

    // If there's a violation, get the categories and explanation; otherwise, use empty defaults
    const violatedCategories = containsViolation ? assessment.categories ?? [] : [];
    const explanation = containsViolation ? assessment.explanation : undefined;

    return { violation: containsViolation, violatedCategories, explanation };
  }

  // Process each comment and print the results
  for (const comment of userComments) {
    console.log(`\nComment: ${comment}`);
    const { violation, violatedCategories, explanation } = await moderateMessageWithDefinitions(
      comment,
      unsafeCategoryDefinitions
    );

    if (violation) {
      console.log(`Violated Categories: ${violatedCategories.join(", ")}`);
      console.log(`Explanation: ${explanation}`);
    } else {
      console.log("No issues detected.");
    }
  }
  ```

  ```csharp C#
  // Categories considered unsafe for content moderation, with their definitions.
  // The entries stay in insertion order, so the rendered prompt lists categories
  // in exactly this order.
  (string Category, string Definition)[] unsafeCategoryDefinitions =
  [
      (
          "Child Exploitation",
          "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children."
      ),
      (
          "Conspiracy Theories",
          """
          Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
                  which can incite harm or undermine public trust in institutions or facts.
          """
      ),
      (
          "Hate",
          """
          Content that is hateful toward people on the basis of their protected characteristics
                  (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
                  or content that perpetuates negative stereotypes.
          """
      ),
      ("Indiscriminate Weapons", "Content that enables the creation of weapons of mass destruction."),
      ("Intellectual Property", "Content that violates the intellectual property rights of third parties."),
      ("Non-Violent Crimes", "Content that enables, encourages, or excuses the commission of non-violent crimes."),
      ("Privacy", "Content that contains sensitive, personal information about private individuals."),
      ("Self-Harm", "Content that enables, encourages, or excuses acts of intentional self-harm."),
      ("Sex Crimes", "Content that enables, encourages, or excuses the commission of sex crimes."),
      ("Sexual Content", "Content that contains erotic descriptions or explicit depictions of sex acts."),
      (
          "Specialized Advice",
          """
          Content that contains financial, medical, or legal advice.
                  Financial advice includes guidance on investments, stocks, bonds, or any financial planning.
          """
      ),
      ("Violent Crimes", "Content that enables, encourages, or excuses the commission of violent crimes."),
  ];


  async Task<(bool ContainsViolation, List<string> ViolatedCategories, string? Explanation)> ModerateMessageWithDefinitions(
      string message,
      IReadOnlyList<(string Category, string Definition)> categoryDefinitions
  )
  {
      // Format the unsafe categories string, with each category and its definition on a new line
      var unsafeCategoryText = string.Join(
          "\n",
          categoryDefinitions.Select(entry => $"{entry.Category}: {entry.Definition}")
      );

      // Construct the prompt for Claude, including the message and unsafe categories
      var assessmentPrompt = $$"""
  Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>{{message}}</message>

  Unsafe Categories and Their Definitions:
  <categories>
  {{unsafeCategoryText}}
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }
  Do not include markdown formatting or code fences in your response.
  """;

      // Send the request to Claude for content moderation
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 200,
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Narrow the first content block to a text block, then parse Claude's JSON response
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      var assessment = JsonNode.Parse(textBlock.Text)!;

      // Extract the violation status from the assessment
      var containsViolation = assessment["violation"]!.GetValue<bool>();

      // If there's a violation, get the categories and explanation; otherwise, use empty defaults
      List<string> violatedCategories = containsViolation
          ? assessment["categories"]?.AsArray().Select(category => category!.GetValue<string>()).ToList() ?? []
          : [];
      var explanation = containsViolation ? assessment["explanation"]?.GetValue<string>() : null;

      return (containsViolation, violatedCategories, explanation);
  }

  // Process each comment and print the results
  foreach (var comment in userComments)
  {
      Console.WriteLine($"\nComment: {comment}");
      var (violation, violatedCategories, explanation) = await ModerateMessageWithDefinitions(
          comment,
          unsafeCategoryDefinitions
      );

      if (violation)
      {
          Console.WriteLine($"Violated Categories: {string.Join(", ", violatedCategories)}");
          Console.WriteLine($"Explanation: {explanation}");
      }
      else
      {
          Console.WriteLine("No issues detected.");
      }
  }
  ```

  ```go Go
  // Categories considered unsafe for content moderation, with their definitions.
  // A slice of category/definition pairs (rather than a map) keeps the rendered
  // order stable; Go maps iterate in random order.
  type categoryDefinition struct {
  	category   string
  	definition string
  }

  var unsafeCategoryDefinitions = []categoryDefinition{
  	{"Child Exploitation", "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children."},
  	{"Conspiracy Theories", `Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.`},
  	{"Hate", `Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.`},
  	{"Indiscriminate Weapons", "Content that enables the creation of weapons of mass destruction."},
  	{"Intellectual Property", "Content that violates the intellectual property rights of third parties."},
  	{"Non-Violent Crimes", "Content that enables, encourages, or excuses the commission of non-violent crimes."},
  	{"Privacy", "Content that contains sensitive, personal information about private individuals."},
  	{"Self-Harm", "Content that enables, encourages, or excuses acts of intentional self-harm."},
  	{"Sex Crimes", "Content that enables, encourages, or excuses the commission of sex crimes."},
  	{"Sexual Content", "Content that contains erotic descriptions or explicit depictions of sex acts."},
  	{"Specialized Advice", `Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.`},
  	{"Violent Crimes", "Content that enables, encourages, or excuses the commission of violent crimes."},
  }

  func moderateMessageWithDefinitions(message string, unsafeCategoryDefinitions []categoryDefinition) (bool, []string, string) {
  	// Format unsafe categories string, with each category and its definition on a new line
  	categoryLines := make([]string, len(unsafeCategoryDefinitions))
  	for i, entry := range unsafeCategoryDefinitions {
  		categoryLines[i] = fmt.Sprintf("%s: %s", entry.category, entry.definition)
  	}
  	unsafeCategoryStr := strings.Join(categoryLines, "\n")

  	// Construct the prompt for Claude, including the message and unsafe categories
  	assessmentPrompt := fmt.Sprintf(`Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

  Message:
  <message>%s</message>

  Unsafe Categories and Their Definitions:
  <categories>
  %s
  </categories>

  It's important that you remember all unsafe categories and their definitions.

  Respond with ONLY a JSON object, using the format below:
  {
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
  }
  Do not include markdown formatting or code fences in your response.`, message, unsafeCategoryStr)

  	// Send the request to Claude for content moderation
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 200,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Narrow the first content block to a text block before reading its text
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Parse the JSON response from Claude
  	var assessment struct {
  		Violation   bool     `json:"violation"`
  		Categories  []string `json:"categories"`
  		Explanation string   `json:"explanation"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}

  	// If there's a violation, return the categories and explanation; otherwise, use empty defaults
  	if !assessment.Violation {
  		return false, nil, ""
  	}
  	return true, assessment.Categories, assessment.Explanation
  }

  // moderateAllCommentsWithDefinitions processes each comment and prints the results.
  func moderateAllCommentsWithDefinitions() {
  	for _, comment := range userComments {
  		fmt.Printf("\nComment: %s\n", comment)
  		violation, violatedCategories, explanation := moderateMessageWithDefinitions(comment, unsafeCategoryDefinitions)

  		if violation {
  			fmt.Printf("Violated Categories: %s\n", strings.Join(violatedCategories, ", "))
  			fmt.Printf("Explanation: %s\n", explanation)
  		} else {
  			fmt.Println("No issues detected.")
  		}
  	}
  }

  ```

  ```java Java
  // Categories considered unsafe for content moderation, with their definitions
  record CategoryDefinition(String category, String definition) {}

  final List<CategoryDefinition> unsafeCategoryDefinitions = List.of(
          new CategoryDefinition(
                  "Child Exploitation",
                  "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children."),
          new CategoryDefinition(
                  "Conspiracy Theories",
                  """
                  Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
                          which can incite harm or undermine public trust in institutions or facts."""),
          new CategoryDefinition(
                  "Hate",
                  """
                  Content that is hateful toward people on the basis of their protected characteristics
                          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
                          or content that perpetuates negative stereotypes."""),
          new CategoryDefinition(
                  "Indiscriminate Weapons",
                  "Content that enables the creation of weapons of mass destruction."),
          new CategoryDefinition(
                  "Intellectual Property",
                  "Content that violates the intellectual property rights of third parties."),
          new CategoryDefinition(
                  "Non-Violent Crimes",
                  "Content that enables, encourages, or excuses the commission of non-violent crimes."),
          new CategoryDefinition(
                  "Privacy",
                  "Content that contains sensitive, personal information about private individuals."),
          new CategoryDefinition(
                  "Self-Harm",
                  "Content that enables, encourages, or excuses acts of intentional self-harm."),
          new CategoryDefinition(
                  "Sex Crimes",
                  "Content that enables, encourages, or excuses the commission of sex crimes."),
          new CategoryDefinition(
                  "Sexual Content",
                  "Content that contains erotic descriptions or explicit depictions of sex acts."),
          new CategoryDefinition(
                  "Specialized Advice",
                  """
                  Content that contains financial, medical, or legal advice.
                          Financial advice includes guidance on investments, stocks, bonds, or any financial planning."""),
          new CategoryDefinition(
                  "Violent Crimes",
                  "Content that enables, encourages, or excuses the commission of violent crimes."));

  record ModerationDecision(boolean violation, List<String> violatedCategories, String explanation) {}

  ModerationDecision moderateMessageWithDefinitions(
          String message, List<CategoryDefinition> unsafeCategoryDefinitions)
          throws JsonProcessingException {
      // Format unsafe categories string, with each category and its definition on a new line
      String unsafeCategoryStr = unsafeCategoryDefinitions.stream()
              .map(categoryDefinition ->
                      categoryDefinition.category() + ": " + categoryDefinition.definition())
              .collect(Collectors.joining("\n"));

      // Construct the prompt for Claude, including the message and unsafe categories
      String assessmentPrompt = """
          Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

          Message:
          <message>%s</message>

          Unsafe Categories and Their Definitions:
          <categories>
          %s
          </categories>

          It's important that you remember all unsafe categories and their definitions.

          Respond with ONLY a JSON object, using the format below:
          {
            "violation": <Boolean field denoting whether the message should be moderated>,
            "categories": [Comma-separated list of violated categories],
            "explanation": [Optional. Only include if there is a violation.]
          }
          Do not include markdown formatting or code fences in your response."""
              .formatted(message, unsafeCategoryStr);

      // Send the request to Claude for content moderation
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(200)
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse the JSON response from Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      ObjectMapper mapper = new ObjectMapper();
      JsonNode assessment = mapper.readTree(assessmentJson);

      // Extract the violation status from the assessment
      boolean containsViolation = assessment.required("violation").asBoolean();

      // If there's a violation, get the categories and explanation; otherwise, use empty defaults
      List<String> violatedCategories = containsViolation && assessment.has("categories")
              ? mapper.convertValue(assessment.get("categories"), new TypeReference<List<String>>() {})
              : List.of();
      String explanation = containsViolation && assessment.hasNonNull("explanation")
              ? assessment.get("explanation").asText()
              : null;

      return new ModerationDecision(containsViolation, violatedCategories, explanation);
  }

  // Process each comment and print the results
  void printModerationResultsWithDefinitions() throws JsonProcessingException {
      for (String comment : userComments) {
          IO.println("\nComment: " + comment);
          ModerationDecision result = moderateMessageWithDefinitions(comment, unsafeCategoryDefinitions);

          if (result.violation()) {
              IO.println("Violated Categories: " + String.join(", ", result.violatedCategories()));
              IO.println("Explanation: " + result.explanation());
          } else {
              IO.println("No issues detected.");
          }
      }
  }
  ```

  ```php PHP
  // Categories considered unsafe for content moderation, with their definitions
  $unsafeCategoryDefinitions = [
      'Child Exploitation' => 'Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.',
      'Conspiracy Theories' => 'Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.',
      'Hate' => 'Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.',
      'Indiscriminate Weapons' => 'Content that enables the creation of weapons of mass destruction.',
      'Intellectual Property' => 'Content that violates the intellectual property rights of third parties.',
      'Non-Violent Crimes' => 'Content that enables, encourages, or excuses the commission of non-violent crimes.',
      'Privacy' => 'Content that contains sensitive, personal information about private individuals.',
      'Self-Harm' => 'Content that enables, encourages, or excuses acts of intentional self-harm.',
      'Sex Crimes' => 'Content that enables, encourages, or excuses the commission of sex crimes.',
      'Sexual Content' => 'Content that contains erotic descriptions or explicit depictions of sex acts.',
      'Specialized Advice' => 'Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.',
      'Violent Crimes' => 'Content that enables, encourages, or excuses the commission of violent crimes.',
  ];

  $moderateMessageWithDefinitions = function (string $message, array $unsafeCategoryDefinitions) use ($client): array {
      // Format the unsafe categories string, with each category and its definition on a new line
      $categoryLines = [];
      foreach ($unsafeCategoryDefinitions as $category => $definition) {
          $categoryLines[] = "{$category}: {$definition}";
      }
      $unsafeCategoryStr = implode("\n", $categoryLines);

      // Construct the prompt for Claude, including the message and unsafe categories
      $assessmentPrompt = <<<PROMPT
      Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

      Message:
      <message>{$message}</message>

      Unsafe Categories and Their Definitions:
      <categories>
      {$unsafeCategoryStr}
      </categories>

      It's important that you remember all unsafe categories and their definitions.

      Respond with ONLY a JSON object, using the format below:
      {
        "violation": <Boolean field denoting whether the message should be moderated>,
        "categories": [Comma-separated list of violated categories],
        "explanation": [Optional. Only include if there is a violation.]
      }
      Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Send the request to Claude for content moderation
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 200,
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse the JSON response from Claude. The SDK decodes each content block
      // into its concrete class, so find the TextBlock before reading the text.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');
      $assessment = json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);

      // Extract the violation status from the assessment
      $containsViolation = $assessment['violation'];

      // If there's a violation, get the categories and explanation; otherwise, use empty defaults
      $violatedCategories = $containsViolation ? ($assessment['categories'] ?? []) : [];
      $explanation = $containsViolation ? ($assessment['explanation'] ?? null) : null;

      return [$containsViolation, $violatedCategories, $explanation];
  };

  // Process each comment and print the results
  foreach ($userComments as $comment) {
      echo "\nComment: {$comment}\n";
      [$violation, $violatedCategories, $explanation] = $moderateMessageWithDefinitions($comment, $unsafeCategoryDefinitions);

      if ($violation) {
          echo 'Violated Categories: ' . implode(', ', $violatedCategories) . "\n";
          echo "Explanation: {$explanation}\n";
      } else {
          echo "No issues detected.\n";
      }
  }
  ```

  ```ruby Ruby
  # Categories considered unsafe for content moderation, with their definitions
  UNSAFE_CATEGORY_DEFINITIONS = {
    "Child Exploitation" => "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
    "Conspiracy Theories" => "Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
          which can incite harm or undermine public trust in institutions or facts.",
    "Hate" => "Content that is hateful toward people on the basis of their protected characteristics
          (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
          or content that perpetuates negative stereotypes.",
    "Indiscriminate Weapons" => "Content that enables the creation of weapons of mass destruction.",
    "Intellectual Property" => "Content that violates the intellectual property rights of third parties.",
    "Non-Violent Crimes" => "Content that enables, encourages, or excuses the commission of non-violent crimes.",
    "Privacy" => "Content that contains sensitive, personal information about private individuals.",
    "Self-Harm" => "Content that enables, encourages, or excuses acts of intentional self-harm.",
    "Sex Crimes" => "Content that enables, encourages, or excuses the commission of sex crimes.",
    "Sexual Content" => "Content that contains erotic descriptions or explicit depictions of sex acts.",
    "Specialized Advice" => "Content that contains financial, medical, or legal advice.
          Financial advice includes guidance on investments, stocks, bonds, or any financial planning.",
    "Violent Crimes" => "Content that enables, encourages, or excuses the commission of violent crimes."
  }


  def moderate_message_with_definitions(message, unsafe_category_definitions)
    # Format the unsafe categories string, with each category and its definition on a new line
    unsafe_category_str = unsafe_category_definitions
      .map { |category, definition| "#{category}: #{definition}" }
      .join("\n")

    # Construct the prompt for Claude, including the message and unsafe categories
    assessment_prompt = <<~PROMPT.chomp
      Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

      Message:
      <message>#{message}</message>

      Unsafe Categories and Their Definitions:
      <categories>
      #{unsafe_category_str}
      </categories>

      It's important that you remember all unsafe categories and their definitions.

      Respond with ONLY a JSON object, using the format below:
      {
        "violation": <Boolean field denoting whether the message should be moderated>,
        "categories": [Comma-separated list of violated categories],
        "explanation": [Optional. Only include if there is a violation.]
      }
      Do not include markdown formatting or code fences in your response.
    PROMPT

    # Send the request to Claude for content moderation
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 200,
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse the JSON response from Claude
    text_block = response.content.find { it.type == :text }
    assessment = JSON.parse(text_block.text)

    # Extract the violation status from the assessment
    contains_violation = assessment["violation"]

    # If there's a violation, get the categories and explanation; otherwise, use empty defaults
    violated_categories = contains_violation ? assessment.fetch("categories", []) : []
    explanation = contains_violation ? assessment["explanation"] : nil

    [contains_violation, violated_categories, explanation]
  end


  # Process each comment and print the results
  USER_COMMENTS.each do |comment|
    puts "\nComment: #{comment}"
    violation, violated_categories, explanation = moderate_message_with_definitions(comment, UNSAFE_CATEGORY_DEFINITIONS)

    if violation
      puts "Violated Categories: #{violated_categories.join(", ")}"
      puts "Explanation: #{explanation}"
    else
      puts "No issues detected."
    end
  end
  ```
</CodeGroup>

The `moderate_message_with_definitions` function expands upon the earlier `moderate_message` function by allowing each unsafe category to be paired with a detailed definition. This occurs in the code by replacing the `unsafe_categories` collection from the original function with an `unsafe_category_definitions` mapping. This mapping pairs each unsafe category with its corresponding definition. Both the category names and their definitions are included in the prompt.

Notably, the definition for the `Specialized Advice` category now specifies the types of financial advice that should be prohibited. As a result, the comment `It is a great time to invest in gold!`, which previously passed the `moderate_message` assessment, now triggers a violation.

### Consider batch processing

To reduce costs in situations where real-time moderation isn't necessary, consider moderating messages in batches. Include multiple messages within the prompt's context, and ask Claude to assess which messages should be moderated.

<CodeGroup exclude="shell">
  ```python Python
  def batch_moderate_messages(messages, unsafe_categories):
      # Convert the unsafe categories into a string, with each category on a new line
      unsafe_category_str = "\n".join(unsafe_categories)

      # Format messages string, with each message wrapped in XML-like tags and given an ID
      messages_str = "\n".join(
          [f"<message id={idx}>{msg}</message>" for idx, msg in enumerate(messages)]
      )

      # Construct the prompt for Claude, including the messages and unsafe categories
      assessment_prompt = f"""Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  {messages_str}
  </messages>

  Unsafe Categories:
  <categories>
  {unsafe_category_str}
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {{
    "violations": [
      {{
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }}
    ]
  }}

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response."""

      # Send the request to Claude for content moderation
      response = client.messages.create(
          model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
          max_tokens=2048,  # Increased max token count to handle batches
          messages=[{"role": "user", "content": assessment_prompt}],
      )

      # Parse the JSON response from Claude
      text_block = next(block for block in response.content if block.type == "text")
      assessment = json.loads(text_block.text)
      return assessment


  # Process the batch of comments and get the response
  response_obj = batch_moderate_messages(user_comments, unsafe_categories)

  # Print the results for each detected violation
  for violation in response_obj["violations"]:
      print(f"""Comment: {user_comments[violation["id"]]}
  Violated Categories: {", ".join(violation["categories"])}
  Explanation: {violation["explanation"]}
  """)
  ```

  ```typescript TypeScript
  // Shape of the JSON batch assessment Claude returns
  interface BatchAssessment {
    violations: {
      id: number;
      categories: string[];
      explanation: string;
    }[];
  }

  async function batchModerateMessages(
    messages: string[],
    unsafeCategories: string[]
  ): Promise<BatchAssessment> {
    // Convert the unsafe categories into a string, with each category on a new line
    const unsafeCategoryStr = unsafeCategories.join("\n");

    // Format the messages string, with each message wrapped in XML-like tags and given an ID
    const messagesStr = messages
      .map((msg, idx) => `<message id=${idx}>${msg}</message>`)
      .join("\n");

    // Construct the prompt for Claude, including the messages and unsafe categories
    const assessmentPrompt = `Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  ${messagesStr}
  </messages>

  Unsafe Categories:
  <categories>
  ${unsafeCategoryStr}
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {
    "violations": [
      {
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }
    ]
  }

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response.`;

    // Send the request to Claude for content moderation
    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001", // Using the Haiku model for lower costs
      max_tokens: 2048, // Increased max token count to handle batches
      messages: [{ role: "user", content: assessmentPrompt }]
    });

    // Parse the JSON response from Claude
    const textBlock = response.content.find((block) => block.type === "text");
    if (!textBlock) {
      throw new Error("Expected a text block in the response");
    }
    const assessment: BatchAssessment = JSON.parse(textBlock.text);
    return assessment;
  }

  // Process the batch of comments and get the response
  const batchAssessment = await batchModerateMessages(userComments, unsafeCategories);

  // Print the results for each detected violation
  for (const violation of batchAssessment.violations) {
    console.log(`Comment: ${userComments[violation.id]}
  Violated Categories: ${violation.categories.join(", ")}
  Explanation: ${violation.explanation}
  `);
  }
  ```

  ```csharp C#
  async Task<JsonNode> BatchModerateMessages(IReadOnlyList<string> messages, IReadOnlyList<string> categories)
  {
      // Convert the unsafe categories into a string, with each category on a new line
      var unsafeCategoryText = string.Join("\n", categories);

      // Format the messages string, with each message wrapped in XML-like tags and given an ID
      var messagesText = string.Join(
          "\n",
          messages.Select((message, index) => $"<message id={index}>{message}</message>")
      );

      // Construct the prompt for Claude, including the messages and unsafe categories
      var assessmentPrompt = $$"""
  Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  {{messagesText}}
  </messages>

  Unsafe Categories:
  <categories>
  {{unsafeCategoryText}}
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {
    "violations": [
      {
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }
    ]
  }

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response.
  """;

      // Send the request to Claude for content moderation
      var response = await client.Messages.Create(
          new()
          {
              Model = Model.ClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
              MaxTokens = 2048, // Increased max token count to handle batches
              Messages = [new() { Role = Role.User, Content = assessmentPrompt }],
          }
      );

      // Narrow the first content block to a text block, then parse Claude's JSON response
      if (!response.Content[0].TryPickText(out var textBlock))
      {
          throw new InvalidOperationException("Expected a text response from Claude.");
      }
      return JsonNode.Parse(textBlock.Text)!;
  }

  // Process the batch of comments and get the response
  var moderationResults = await BatchModerateMessages(userComments, unsafeCategories);

  // Print the results for each detected violation
  foreach (var violation in moderationResults["violations"]!.AsArray())
  {
      var flaggedComment = userComments[violation!["id"]!.GetValue<int>()];
      var violatedCategories = string.Join(
          ", ",
          violation["categories"]!.AsArray().Select(category => category!.GetValue<string>())
      );
      var explanation = violation["explanation"]!.GetValue<string>();

      Console.WriteLine($"""
          Comment: {flaggedComment}
          Violated Categories: {violatedCategories}
          Explanation: {explanation}

          """);
  }
  ```

  ```go Go
  // batchViolation is one entry in Claude's "violations" array: the index of the
  // offending message plus the categories it violated and why.
  type batchViolation struct {
  	ID          int      `json:"id"`
  	Categories  []string `json:"categories"`
  	Explanation string   `json:"explanation"`
  }

  func batchModerateMessages(messages []string, unsafeCategories []string) []batchViolation {
  	// Convert the unsafe categories into a string, with each category on a new line
  	unsafeCategoryStr := strings.Join(unsafeCategories, "\n")

  	// Format messages string, with each message wrapped in XML-like tags and given an ID
  	messageLines := make([]string, len(messages))
  	for i, message := range messages {
  		messageLines[i] = fmt.Sprintf("<message id=%d>%s</message>", i, message)
  	}
  	messagesStr := strings.Join(messageLines, "\n")

  	// Construct the prompt for Claude, including the messages and unsafe categories
  	assessmentPrompt := fmt.Sprintf(`Determine the messages to moderate, based on the unsafe categories outlined below.

  Messages:
  <messages>
  %s
  </messages>

  Unsafe Categories:
  <categories>
  %s
  </categories>

  Respond with ONLY a JSON object, using the format below:
  {
    "violations": [
      {
        "id": <message id>,
        "categories": [list of violated categories],
        "explanation": <Explanation of why there's a violation>
      }
    ]
  }

  Important Notes:
  - Remember to analyze every message for a violation.
  - Select any number of violations that reasonably apply.
  - Do not include markdown formatting or code fences in your response.`, messagesStr, unsafeCategoryStr)

  	// Send the request to Claude for content moderation
  	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeHaiku4_5_20251001, // Using the Haiku model for lower costs
  		MaxTokens: 2048,                                   // Increased max token count to handle batches
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(assessmentPrompt)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Narrow the first content block to a text block before reading its text
  	textBlock, ok := response.Content[0].AsAny().(anthropic.TextBlock)
  	if !ok {
  		log.Fatalf("expected a text block, got %q", response.Content[0].Type)
  	}

  	// Parse the JSON response from Claude
  	var assessment struct {
  		Violations []batchViolation `json:"violations"`
  	}
  	if err := json.Unmarshal([]byte(textBlock.Text), &assessment); err != nil {
  		log.Fatal(err)
  	}
  	return assessment.Violations
  }

  // moderateAllCommentsAsBatch moderates the whole batch of comments in a single
  // request and prints the results for each detected violation.
  func moderateAllCommentsAsBatch() {
  	// Process the batch of comments and get the response
  	violations := batchModerateMessages(userComments, unsafeCategories)

  	// Print the results for each detected violation
  	for _, violation := range violations {
  		fmt.Printf(`Comment: %s
  Violated Categories: %s
  Explanation: %s

  `, userComments[violation.ID], strings.Join(violation.Categories, ", "), violation.Explanation)
  	}
  }

  ```

  ```java Java
  JsonNode batchModerateMessages(List<String> messages, List<String> unsafeCategories)
          throws JsonProcessingException {
      // Convert the unsafe categories into a string, with each category on a new line
      String unsafeCategoryStr = String.join("\n", unsafeCategories);

      // Format messages string, with each message wrapped in XML-like tags and given an ID
      String messagesStr = IntStream.range(0, messages.size())
              .mapToObj(idx -> "<message id=%d>%s</message>".formatted(idx, messages.get(idx)))
              .collect(Collectors.joining("\n"));

      // Construct the prompt for Claude, including the messages and unsafe categories
      String assessmentPrompt = """
          Determine the messages to moderate, based on the unsafe categories outlined below.

          Messages:
          <messages>
          %s
          </messages>

          Unsafe Categories:
          <categories>
          %s
          </categories>

          Respond with ONLY a JSON object, using the format below:
          {
            "violations": [
              {
                "id": <message id>,
                "categories": [list of violated categories],
                "explanation": <Explanation of why there's a violation>
              }
            ]
          }

          Important Notes:
          - Remember to analyze every message for a violation.
          - Select any number of violations that reasonably apply.
          - Do not include markdown formatting or code fences in your response."""
              .formatted(messagesStr, unsafeCategoryStr);

      // Send the request to Claude for content moderation
      Message response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_HAIKU_4_5_20251001) // Using the Haiku model for lower costs
              .maxTokens(2048) // Increased max token count to handle batches
              .addUserMessage(assessmentPrompt)
              .build());

      // Parse the JSON response from Claude
      String assessmentJson = response.content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .findFirst()
              .orElseThrow()
              .text();
      return new ObjectMapper().readTree(assessmentJson);
  }

  // Process the batch of comments and print the results for each detected violation
  void printBatchViolations() throws JsonProcessingException {
      JsonNode response = batchModerateMessages(userComments, unsafeCategories);

      ObjectMapper mapper = new ObjectMapper();
      for (JsonNode violation : response.required("violations")) {
          List<String> violatedCategories =
                  mapper.convertValue(violation.required("categories"), new TypeReference<List<String>>() {});
          IO.println("""
                  Comment: %s
                  Violated Categories: %s
                  Explanation: %s
                  """.formatted(
                          userComments.get(violation.required("id").asInt()),
                          String.join(", ", violatedCategories),
                          violation.required("explanation").asText()));
      }
  }
  ```

  ```php PHP
  $batchModerateMessages = function (array $messages, array $unsafeCategories) use ($client): array {
      // Convert the unsafe categories into a string, with each category on a new line
      $unsafeCategoryStr = implode("\n", $unsafeCategories);

      // Format the messages string, with each message wrapped in XML-like tags and given an ID
      $messageLines = [];
      foreach ($messages as $idx => $msg) {
          $messageLines[] = "<message id={$idx}>{$msg}</message>";
      }
      $messagesStr = implode("\n", $messageLines);

      // Construct the prompt for Claude, including the messages and unsafe categories
      $assessmentPrompt = <<<PROMPT
      Determine the messages to moderate, based on the unsafe categories outlined below.

      Messages:
      <messages>
      {$messagesStr}
      </messages>

      Unsafe Categories:
      <categories>
      {$unsafeCategoryStr}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
        "violations": [
          {
            "id": <message id>,
            "categories": [list of violated categories],
            "explanation": <Explanation of why there's a violation>
          }
        ]
      }

      Important Notes:
      - Remember to analyze every message for a violation.
      - Select any number of violations that reasonably apply.
      - Do not include markdown formatting or code fences in your response.
      PROMPT;

      // Send the request to Claude for content moderation
      $response = $client->messages->create(
          model: 'claude-haiku-4-5-20251001', // Using the Haiku model for lower costs
          maxTokens: 2048, // Increased max token count to handle batches
          messages: [['role' => 'user', 'content' => $assessmentPrompt]],
      );

      // Parse the JSON response from Claude. The SDK decodes each content block
      // into its concrete class, so find the TextBlock before reading the text.
      $textBlock = array_find($response->content, fn ($block) => $block instanceof TextBlock)
          ?? throw new RuntimeException('Expected a text block in the response.');

      return json_decode($textBlock->text, associative: true, flags: JSON_THROW_ON_ERROR);
  };

  // Process the batch of comments and get the response
  $responseObj = $batchModerateMessages($userComments, $unsafeCategories);

  // Print the results for each detected violation
  foreach ($responseObj['violations'] as $violation) {
      echo "Comment: {$userComments[$violation['id']]}\n";
      echo 'Violated Categories: ' . implode(', ', $violation['categories']) . "\n";
      echo "Explanation: {$violation['explanation']}\n\n";
  }
  ```

  ```ruby Ruby
  def batch_moderate_messages(messages, unsafe_categories)
    # Convert the unsafe categories into a string, with each category on a new line
    unsafe_category_str = unsafe_categories.join("\n")

    # Format the messages string, with each message wrapped in XML-like tags and given an ID
    messages_str = messages
      .map.with_index { |message, index| "<message id=#{index}>#{message}</message>" }
      .join("\n")

    # Construct the prompt for Claude, including the messages and unsafe categories
    assessment_prompt = <<~PROMPT.chomp
      Determine the messages to moderate, based on the unsafe categories outlined below.

      Messages:
      <messages>
      #{messages_str}
      </messages>

      Unsafe Categories:
      <categories>
      #{unsafe_category_str}
      </categories>

      Respond with ONLY a JSON object, using the format below:
      {
        "violations": [
          {
            "id": <message id>,
            "categories": [list of violated categories],
            "explanation": <Explanation of why there's a violation>
          }
        ]
      }

      Important Notes:
      - Remember to analyze every message for a violation.
      - Select any number of violations that reasonably apply.
      - Do not include markdown formatting or code fences in your response.
    PROMPT

    # Send the request to Claude for content moderation
    response = CLIENT.messages.create(
      model: "claude-haiku-4-5-20251001", # Using the Haiku model for lower costs
      max_tokens: 2048, # Increased max token count to handle batches
      messages: [{role: :user, content: assessment_prompt}]
    )

    # Parse the JSON response from Claude
    text_block = response.content.find { it.type == :text }
    JSON.parse(text_block.text)
  end


  # Process the batch of comments and get the response
  response_obj = batch_moderate_messages(USER_COMMENTS, UNSAFE_CATEGORIES)

  # Print the results for each detected violation
  response_obj["violations"].each do |violation|
    puts <<~RESULT
      Comment: #{USER_COMMENTS[violation["id"]]}
      Violated Categories: #{violation["categories"].join(", ")}
      Explanation: #{violation["explanation"]}

    RESULT
  end
  ```
</CodeGroup>

In this example, the `batch_moderate_messages` function handles the moderation of an entire batch of messages with a single Claude API call. Inside the function, a prompt is created that includes the list of messages to evaluate and the unsafe content categories. The prompt directs Claude to return a JSON object listing all messages that contain violations. Each message in the response is identified by its `id`, which corresponds to the message's position in the batch. Keep in mind that finding the optimal batch size for your specific needs may require some experimentation. While larger batch sizes can lower costs, they might also lead to a slight decrease in quality. Additionally, you may need to increase the `max_tokens` parameter in the Claude API call to accommodate longer responses. For details on the maximum number of tokens your chosen model can output, refer to the [model comparison table](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison).

<CardGroup cols={2}>
  <Card title="Content moderation cookbook" icon="link" href="https://platform.claude.com/cookbook/misc-building-moderation-filter">
    View a fully implemented code-based example of how to use Claude for content moderation.
  </Card>

  <Card title="Mitigate jailbreaks" icon="link" href="https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks">
    Explore guardrail techniques to moderate interactions with Claude.
  </Card>
</CardGroup>
