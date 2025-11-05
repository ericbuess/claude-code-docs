# Ticket routing

> This guide walks through how to harness Claude's advanced natural language understanding capabilities to classify customer support tickets at scale based on customer intent, urgency, prioritization, customer profile, and more.

## Define whether to use Claude for ticket routing

Here are some key indicators that you should use an LLM like Claude  instead of traditional ML approaches for your classification task:

<AccordionGroup>
  <Accordion title="You have limited labeled training data available">
    Traditional ML processes require massive labeled datasets. Claude's pre-trained model can effectively classify tickets with just a few dozen labeled examples, significantly reducing data preparation time and costs.
  </Accordion>

  <Accordion title="Your classification categories are likely to change or evolve over time">
    Once a traditional ML approach has been established, changing it is a laborious and data-intensive undertaking. On the other hand, as your product or customer needs evolve, Claude can easily adapt to changes in class definitions or new classes without extensive relabeling of training data.
  </Accordion>

  <Accordion title="You need to handle complex, unstructured text inputs">
    Traditional ML models often struggle with unstructured data and require extensive feature engineering. Claude's advanced language understanding allows for accurate classification based on content and context, rather than relying on strict ontological structures.
  </Accordion>

  <Accordion title="Your classification rules are based on semantic understanding">
    Traditional ML approaches often rely on bag-of-words models or simple pattern matching. Claude excels at understanding and applying underlying rules when classes are defined by conditions rather than examples.
  </Accordion>

  <Accordion title="You require interpretable reasoning for classification decisions">
    Many traditional ML models provide little insight into their decision-making process. Claude can provide human-readable explanations for its classification decisions, building trust in the automation system and facilitating easy adaptation if needed.
  </Accordion>

  <Accordion title="You want to handle edge cases and ambiguous tickets more effectively">
    Traditional ML systems often struggle with outliers and ambiguous inputs, frequently misclassifying them or defaulting to a catch-all category. Claude's natural language processing capabilities allow it to better interpret context and nuance in support tickets, potentially reducing the number of misrouted or unclassified tickets that require manual intervention.
  </Accordion>

  <Accordion title="You need multilingual support without maintaining separate models">
    Traditional ML approaches typically require separate models or extensive translation processes for each supported language. Claude's multilingual capabilities allow it to classify tickets in various languages without the need for separate models or extensive translation processes, streamlining support for global customer bases.
  </Accordion>
</AccordionGroup>

***

## Build and deploy your LLM support workflow

### Understand your current support approach

Before diving into automation, it's crucial to understand your existing ticketing system. Start by investigating how your support team currently handles ticket routing.

Consider questions like:

* What criteria are used to determine what SLA/service offering is applied?
* Is ticket routing used to determine which tier of support or product specialist a ticket goes to?
* Are there any automated rules or workflows already in place? In what cases do they fail?
* How are edge cases or ambiguous tickets handled?
* How does the team prioritize tickets?

The more you know about how humans handle certain cases, the better you will be able to work with Claude to do the task.

### Define user intent categories

A well-defined list of user intent categories is crucial for accurate support ticket classification with Claude. Claude’s ability to route tickets effectively within your system is directly proportional to how well-defined your system’s categories are.

Here are some example user intent categories and subcategories.

<AccordionGroup>
  <Accordion title="Technical issue">
    * Hardware problem
    * Software bug
    * Compatibility issue
    * Performance problem
  </Accordion>

  <Accordion title="Account management">
    * Password reset
    * Account access issues
    * Billing inquiries
    * Subscription changes
  </Accordion>

  <Accordion title="Product information">
    * Feature inquiries
    * Product compatibility questions
    * Pricing information
    * Availability inquiries
  </Accordion>

  <Accordion title="User guidance">
    * How-to questions
    * Feature usage assistance
    * Best practices advice
    * Troubleshooting guidance
  </Accordion>

  <Accordion title="Feedback">
    * Bug reports
    * Feature requests
    * General feedback or suggestions
    * Complaints
  </Accordion>

  <Accordion title="Order-related">
    * Order status inquiries
    * Shipping information
    * Returns and exchanges
    * Order modifications
  </Accordion>

  <Accordion title="Service request">
    * Installation assistance
    * Upgrade requests
    * Maintenance scheduling
    * Service cancellation
  </Accordion>

  <Accordion title="Security concerns">
    * Data privacy inquiries
    * Suspicious activity reports
    * Security feature assistance
  </Accordion>

  <Accordion title="Compliance and legal">
    * Regulatory compliance questions
    * Terms of service inquiries
    * Legal documentation requests
  </Accordion>

  <Accordion title="Emergency support">
    * Critical system failures
    * Urgent security issues
    * Time-sensitive problems
  </Accordion>

  <Accordion title="Training and education">
    * Product training requests
    * Documentation inquiries
    * Webinar or workshop information
  </Accordion>

  <Accordion title="Integration and API">
    * Integration assistance
    * API usage questions
    * Third-party compatibility inquiries
  </Accordion>
</AccordionGroup>

In addition to intent, ticket routing and prioritization may also be influenced by other factors such as urgency, customer type, SLAs, or language. Be sure to consider other routing criteria when building your automated routing system.

### Establish success criteria

Work with your support team to [define clear success criteria](/en/docs/build-with-claude/define-success) with measurable benchmarks, thresholds, and goals.

Here are some standard criteria and benchmarks when using LLMs for support ticket routing:

<AccordionGroup>
  <Accordion title="Classification consistency">
    This metric assesses how consistently Claude classifies similar tickets over time. It's crucial for maintaining routing reliability. Measure this by periodically testing the model with a set of standardized inputs and aiming for a consistency rate of 95% or higher.
  </Accordion>

  <Accordion title="Adaptation speed">
    This measures how quickly Claude can adapt to new categories or changing ticket patterns. Test this by introducing new ticket types and measuring the time it takes for the model to achieve satisfactory accuracy (e.g., >90%) on these new categories. Aim for adaptation within 50-100 sample tickets.
  </Accordion>

  <Accordion title="Multilingual handling">
    This assesses Claude's ability to accurately route tickets in multiple languages. Measure the routing accuracy across different languages, aiming for no more than a 5-10% drop in accuracy for non-primary languages.
  </Accordion>

  <Accordion title="Edge case handling">
    This evaluates Claude's performance on unusual or complex tickets. Create a test set of edge cases and measure the routing accuracy, aiming for at least 80% accuracy on these challenging inputs.
  </Accordion>

  <Accordion title="Bias mitigation">
    This measures Claude's fairness in routing across different customer demographics. Regularly audit routing decisions for potential biases, aiming for consistent routing accuracy (within 2-3%) across all customer groups.
  </Accordion>

  <Accordion title="Prompt efficiency">
    In situations where minimizing token count is crucial, this criteria assesses how well Claude performs with minimal context. Measure routing accuracy with varying amounts of context provided, aiming for 90%+ accuracy with just the ticket title and a brief description.
  </Accordion>

  <Accordion title="Explainability score">
    This evaluates the quality and relevance of Claude's explanations for its routing decisions. Human raters can score explanations on a scale (e.g., 1-5), with the goal of achieving an average score of 4 or higher.
  </Accordion>
</AccordionGroup>

Here are some common success criteria that may be useful regardless of whether an LLM is used:

<AccordionGroup>
  <Accordion title="Routing accuracy">
    Routing accuracy measures how often tickets are correctly assigned to the appropriate team or individual on the first try. This is typically measured as a percentage of correctly routed tickets out of total tickets. Industry benchmarks often aim for 90-95% accuracy, though this can vary based on the complexity of the support structure.
  </Accordion>

  <Accordion title="Time-to-assignment">
    This metric tracks how quickly tickets are assigned after being submitted. Faster assignment times generally lead to quicker resolutions and improved customer satisfaction. Best-in-class systems often achieve average assignment times of under 5 minutes, with many aiming for near-instantaneous routing (which is possible with LLM implementations).
  </Accordion>

  <Accordion title="Rerouting rate">
    The rerouting rate indicates how often tickets need to be reassigned after initial routing. A lower rate suggests more accurate initial routing. Aim for a rerouting rate below 10%, with top-performing systems achieving rates as low as 5% or less.
  </Accordion>

  <Accordion title="First-contact resolution rate">
    This measures the percentage of tickets resolved during the first interaction with the customer. Higher rates indicate efficient routing and well-prepared support teams. Industry benchmarks typically range from 70-75%, with top performers achieving rates of 80% or higher.
  </Accordion>

  <Accordion title="Average handling time">
    Average handling time measures how long it takes to resolve a ticket from start to finish. Efficient routing can significantly reduce this time. Benchmarks vary widely by industry and complexity, but many organizations aim to keep average handling time under 24 hours for non-critical issues.
  </Accordion>

  <Accordion title="Customer satisfaction scores">
    Often measured through post-interaction surveys, these scores reflect overall customer happiness with the support process. Effective routing contributes to higher satisfaction. Aim for CSAT scores of 90% or higher, with top performers often achieving 95%+ satisfaction rates.
  </Accordion>

  <Accordion title="Escalation rate">
    This measures how often tickets need to be escalated to higher tiers of support. Lower escalation rates often indicate more accurate initial routing. Strive for an escalation rate below 20%, with best-in-class systems achieving rates of 10% or less.
  </Accordion>

  <Accordion title="Agent productivity">
    This metric looks at how many tickets agents can handle effectively after implementing the routing solution. Improved routing should increase productivity. Measure this by tracking tickets resolved per agent per day or hour, aiming for a 10-20% improvement after implementing a new routing system.
  </Accordion>

  <Accordion title="Self-service deflection rate">
    This measures the percentage of potential tickets resolved through self-service options before entering the routing system. Higher rates indicate effective pre-routing triage. Aim for a deflection rate of 20-30%, with top performers achieving rates of 40% or higher.
  </Accordion>

  <Accordion title="Cost per ticket">
    This metric calculates the average cost to resolve each support ticket. Efficient routing should help reduce this cost over time. While benchmarks vary widely, many organizations aim to reduce cost per ticket by 10-15% after implementing an improved routing system.
  </Accordion>
</AccordionGroup>

### Choose the right Claude model

The choice of model depends on the trade-offs between cost, accuracy, and response time.

Many customers have found `claude-3-5-haiku-20241022` an ideal model for ticket routing, as it is the fastest and most cost-effective model in the Claude 3 family while still delivering excellent results. If your classification problem requires deep subject matter expertise or a large volume of intent categories complex reasoning, you may opt for the [larger Sonnet model](/en/docs/about-claude/models).

### Build a strong prompt

Ticket routing is a type of classification task. Claude analyzes the content of a support ticket and classifies it into predefined categories based on the issue type, urgency, required expertise, or other relevant factors.

Let’s write a ticket classification prompt. Our initial prompt should contain the contents of the user request and return both the reasoning and the intent.

<Tip>
  Try the [prompt generator](/en/docs/prompt-generator) on the [Claude Console](https://console.anthropic.com/login) to have Claude write a first draft for you.
</Tip>

Here's an example ticket routing classification prompt:

```python  theme={null}
def classify_support_request(ticket_contents):
    # Define the prompt for the classification task
    classification_prompt = f"""You will be acting as a customer support ticket classification system. Your task is to analyze customer support requests and output the appropriate classification intent for each request, along with your reasoning. 

        Here is the customer support request you need to classify:

        <request>{ticket_contents}</request>

        Please carefully analyze the above request to determine the customer's core intent and needs. Consider what the customer is asking for has concerns about.

        First, write out your reasoning and analysis of how to classify this request inside <reasoning> tags.

        Then, output the appropriate classification label for the request inside a <intent> tag. The valid intents are:
        <intents>
        <intent>Support, Feedback, Complaint</intent>
        <intent>Order Tracking</intent>
        <intent>Refund/Exchange</intent>
        </intents>

        A request may have ONLY ONE applicable intent. Only include the intent that is most applicable to the request.

        As an example, consider the following request:
        <request>Hello! I had high-speed fiber internet installed on Saturday and my installer, Kevin, was absolutely fantastic! Where can I send my positive review? Thanks for your help!</request>

        Here is an example of how your output should be formatted (for the above example request):
        <reasoning>The user seeks information in order to leave positive feedback.</reasoning>
        <intent>Support, Feedback, Complaint</intent>

        Here are a few more examples:
        <examples>
        <example 2>
        Example 2 Input:
        <request>I wanted to write and personally thank you for the compassion you showed towards my family during my father's funeral this past weekend. Your staff was so considerate and helpful throughout this whole process; it really took a load off our shoulders. The visitation brochures were beautiful. We'll never forget the kindness you showed us and we are so appreciative of how smoothly the proceedings went. Thank you, again, Amarantha Hill on behalf of the Hill Family.</request>

        Example 2 Output:
        <reasoning>User leaves a positive review of their experience.</reasoning>
        <intent>Support, Feedback, Complaint</intent>
        </example 2>
        <example 3>

        ...

        </example 8>
        <example 9>
        Example 9 Input:
        <request>Your website keeps sending ad-popups that block the entire screen. It took me twenty minutes just to finally find the phone number to call and complain. How can I possibly access my account information with all of these popups? Can you access my account for me, since your website is broken? I need to know what the address is on file.</request>

        Example 9 Output:
        <reasoning>The user requests help accessing their web account information.</reasoning>
        <intent>Support, Feedback, Complaint</intent>
        </example 9>

        Remember to always include your classification reasoning before your actual intent output. The reasoning should be enclosed in <reasoning> tags and the intent in <intent> tags. Return only the reasoning and the intent.
        """
```

Let's break down the key components of this prompt:

* We use Python f-strings to create the prompt template, allowing the `ticket_contents` to be inserted into the `<request>` tags.
* We give  Claude a clearly defined role as a classification system that carefully analyzes the ticket content to determine the customer's core intent and needs.
* We instruct Claude on proper output formatting, in this case to provide its reasoning and analysis inside `<reasoning>` tags, followed by the appropriate classification label inside `<intent>` tags.
* We specify the valid intent categories: "Support, Feedback, Complaint", "Order Tracking", and "Refund/Exchange".
* We include a few examples (a.k.a. few-shot prompting) to illustrate how the output should be formatted, which improves accuracy and consistency.

The reason we want to have Claude split its response into various XML tag sections is so that we can use regular expressions to separately extract the reasoning and intent from the output. This allows us to create targeted next steps in the ticket routing workflow, such as using only the intent to decide which person to route the ticket to.

### Deploy your prompt

It’s hard to know how well your prompt works without deploying it in a test production setting and [running evaluations](/en/docs/build-with-claude/develop-tests).

Let’s build the deployment structure. Start by defining the method signature for wrapping our call to Claude. We'll take the method we’ve already begun to write, which has `ticket_contents` as input, and now return a tuple of `reasoning` and `intent` as output. If you have an existing automation using traditional ML, you'll want to follow that method signature instead.

```python  theme={null}
import anthropic
import re

# Create an instance of the Claude API client
client = anthropic.Anthropic()

# Set the default model
DEFAULT_MODEL="claude-3-5-haiku-20241022"

def classify_support_request(ticket_contents):
    # Define the prompt for the classification task
    classification_prompt = f"""You will be acting as a customer support ticket classification system. 
        ...
        ... The reasoning should be enclosed in <reasoning> tags and the intent in <intent> tags. Return only the reasoning and the intent.
        """
    # Send the prompt to the API to classify the support request.
    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": classification_prompt}],
        stream=False,
    )
    reasoning_and_intent = message.content[0].text

    # Use Python's regular expressions library to extract `reasoning`.
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", reasoning_and_intent, re.DOTALL
    )
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

    # Similarly, also extract the `intent`.
    intent_match = re.search(r"<intent>(.*?)</intent>", reasoning_and_intent, re.DOTALL)
    intent = intent_match.group(1).strip() if intent_match else ""

    return reasoning, intent
```

This code:

* Imports the Anthropic library and creates a client instance using your API key.
* Defines a `classify_support_request` function that takes a `ticket_contents` string.
* Sends the `ticket_contents` to Claude for classification using the `classification_prompt`
* Returns the model's `reasoning` and `intent` extracted from the response.

Since we need to wait for the entire reasoning and intent text to be generated before parsing, we set `stream=False` (the default).

***

## Evaluate your prompt

Prompting often requires testing and optimization for it to be production ready. To determine the readiness of your solution, evaluate performance based on the success criteria and thresholds you established earlier.

To run your evaluation, you will need test cases to run it on. The rest of this guide assumes you have already [developed your test cases](/en/docs/build-with-claude/develop-tests).

### Build an evaluation function

Our example evaluation for this guide measures Claude’s performance along three key metrics:

* Accuracy
* Cost per classification

You may need to assess Claude on other axes depending on what factors that are important to you.

To assess this, we first have to modify the script we wrote and add a function to compare the predicted intent with the actual intent and calculate the percentage of correct predictions. We also have to add in cost calculation and time measurement functionality.

```python  theme={null}
import anthropic
import re

# Create an instance of the Claude API client
client = anthropic.Anthropic()

# Set the default model
DEFAULT_MODEL="claude-3-5-haiku-20241022"

def classify_support_request(request, actual_intent):
    # Define the prompt for the classification task
    classification_prompt = f"""You will be acting as a customer support ticket classification system. 
        ...
        ...The reasoning should be enclosed in <reasoning> tags and the intent in <intent> tags. Return only the reasoning and the intent.
        """

    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": classification_prompt}],
    )
    usage = message.usage  # Get the usage statistics for the API call for how many input and output tokens were used.
    reasoning_and_intent = message.content[0].text

    # Use Python's regular expressions library to extract `reasoning`.
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", reasoning_and_intent, re.DOTALL
    )
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

    # Similarly, also extract the `intent`.
    intent_match = re.search(r"<intent>(.*?)</intent>", reasoning_and_intent, re.DOTALL)
    intent = intent_match.group(1).strip() if intent_match else ""

      # Check if the model's prediction is correct.
    correct = actual_intent.strip() == intent.strip()

    # Return the reasoning, intent, correct, and usage.
    return reasoning, intent, correct, usage
```

Let’s break down the edits we’ve made:

* We added the `actual_intent` from our test cases into the `classify_support_request` method and set up a comparison to assess whether Claude’s intent classification matches our golden intent classification.
* We extracted usage statistics for the API call to calculate cost based on input and output tokens used

### Run your evaluation

A proper evaluation requires clear thresholds and benchmarks to determine what is a good result. The script above will give us the runtime values for accuracy, response time, and cost per classification, but we still would need clearly established thresholds. For example:

* **Accuracy:** 95% (out of 100 tests)
* **Cost per classification:** 50% reduction on average (across 100 tests) from current routing method

Having these thresholds allows you to quickly and easily tell at scale, and with impartial empiricism, what method is best for you and what changes might need to be made to better fit your requirements.

***

## Improve performance

In complex scenarios, it may be helpful to consider additional strategies to improve performance beyond standard [prompt engineering techniques](/en/docs/build-with-claude/prompt-engineering/overview) & [guardrail implementation strategies](/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations). Here are some common scenarios:

### Use a taxonomic hierarchy for cases with 20+ intent categories

As the number of classes grows, the number of examples required also expands, potentially making the prompt unwieldy. As an alternative, you can consider implementing a hierarchical classification system using a mixture of classifiers.

1. Organize your intents in a taxonomic tree structure.
2. Create a series of classifiers at every level of the tree, enabling a cascading routing approach.

For example, you might have a top-level classifier that broadly categorizes tickets into "Technical Issues," "Billing Questions," and "General Inquiries." Each of these categories can then have its own sub-classifier to further refine the classification.

<img src="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=5289a8c92716a132311081bc9efed4fc" alt="" data-og-width="2998" width="2998" data-og-height="430" height="430" data-path="images/ticket-hierarchy.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?w=280&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=6e2d5e710d722b23f00f43e14a9aa94c 280w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?w=560&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=a6184c7df444a8c4bfbdbd7f5b46bb3e 560w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?w=840&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=31536d5d35e186e5cadf58d5b3657ce8 840w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?w=1100&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=efc29d26d9808a8003c0bc66e7ac9ddb 1100w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?w=1650&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=4694bf9a36805541f14c2d33221a82ad 1650w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/ticket-hierarchy.png?w=2500&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=2ac2109b054a21342ae533e6098789d0 2500w" />

* **Pros - greater nuance and accuracy:** You can create different prompts for each parent path, allowing for more targeted and context-specific classification. This can lead to improved accuracy and more nuanced handling of customer requests.

* **Cons - increased latency:** Be advised that multiple classifiers can lead to increased latency, and we recommend implementing this approach with our fastest model, Haiku.

### Use vector databases and similarity search retrieval to handle highly variable tickets

Despite providing examples being the most effective way to improve performance, if support requests are highly variable, it can be hard to include enough examples in a single prompt.

In this scenario, you could employ a vector database to do similarity searches from a dataset of examples and retrieve the most relevant examples for a given query.

This approach, outlined in detail in our [classification recipe](https://github.com/anthropics/anthropic-cookbook/blob/82675c124e1344639b2a875aa9d3ae854709cd83/skills/classification/guide.ipynb), has been shown to improve performance from 71% accuracy to 93% accuracy.

### Account specifically for expected edge cases

Here are some scenarios where Claude may misclassify tickets (there may be others that are unique to your situation). In these scenarios,consider providing explicit instructions or examples in the prompt of how Claude should handle the edge case:

<AccordionGroup>
  <Accordion title="Customers make implicit requests">
    Customers often express needs indirectly. For example, "I've been waiting for my package for over two weeks now" may be an indirect request for order status.

    * **Solution:** Provide Claude with some real customer examples of these kinds of requests, along with what the underlying intent is. You can get even better results if you include a classification rationale for particularly nuanced ticket intents, so that Claude can better generalize the logic to other tickets.
  </Accordion>

  <Accordion title="Claude prioritizes emotion over intent">
    When customers express dissatisfaction, Claude may prioritize addressing the emotion over solving the underlying problem.

    * **Solution:** Provide Claude with directions on when to prioritize customer sentiment or not. It can be something as simple as “Ignore all customer emotions. Focus only on analyzing the intent of the customer’s request and what information the customer might be asking for.”
  </Accordion>

  <Accordion title="Multiple issues cause issue prioritization confusion">
    When customers present multiple issues in a single interaction, Claude may have difficulty identifying the primary concern.

    * **Solution:** Clarify the prioritization of intents so thatClaude can better rank the extracted intents and identify the primary concern.
  </Accordion>
</AccordionGroup>

***

## Integrate Claude into your greater support workflow

Proper integration requires that you make some decisions regarding how your Claude-based ticket routing script fits into the architecture of your greater ticket routing system.There are two ways you could do this:

* **Push-based:** The support ticket system you’re using (e.g. Zendesk) triggers your code by sending a webhook event to your routing service, which then classifies the intent and routes it.
  * This approach is more web-scalable, but needs you to expose a public endpoint.
* **Pull-Based:** Your code pulls for the latest tickets based on a given schedule and routes them at pull time.
  * This approach is easier to implement but might make unnecessary calls to the support ticket system when the pull frequency is too high or might be overly slow when the pull frequency is too low.

For either of these approaches, you will need to wrap your script in a service. The choice of approach depends on what APIs your support ticketing system provides.

***

<CardGroup cols={2}>
  <Card title="Classification cookbook" icon="link" href="https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/classification">
    Visit our classification cookbook for more example code and detailed eval guidance.
  </Card>

  <Card title="Claude Console" icon="link" href="https://console.anthropic.com/dashboard">
    Begin building and evaluating your workflow on the Claude Console.
  </Card>
</CardGroup>
