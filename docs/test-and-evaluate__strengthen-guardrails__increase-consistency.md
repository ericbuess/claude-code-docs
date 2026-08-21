---
title: Increase output consistency
url: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency
description: Make Claude's outputs more consistent by specifying exact formats, prefilling responses, constraining with examples, and grounding answers in retrieval.
---

<Tip>
  **For guaranteed JSON schema conformance**

  If you need Claude to always output valid JSON that conforms to a specific schema, use [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) instead of the prompt engineering techniques below. Structured outputs provide guaranteed schema compliance and are specifically designed for this use case.

  The techniques below are useful for general output consistency or when you need flexibility beyond strict JSON schemas.
</Tip>

Here's how to make Claude's responses more consistent:

## Specify the desired output format

Precisely define your desired output format using JSON, XML, or custom templates so that Claude follows every output formatting element you require.

<Accordion title="Example: Standardizing customer feedback">
  ```text User wrap
  You're a Customer Insights AI. Analyze this feedback and output in JSON format with keys: "sentiment" (positive/negative/neutral), "key_issues" (list), and "action_items" (list of dicts with "team" and "task").

  "I've been a loyal user for 3 years, but the recent UI update is a disaster. Finding basic features is now a scavenger hunt. Plus, the new 'premium' pricing is outrageous. I'm considering switching unless this is fixed ASAP."
  ```

  ```json Assistant
  {
    "sentiment": "negative",
    "key_issues": [
      "Poor UI/UX in recent update",
      "Difficulty finding basic features",
      "Perceived high pricing (new 'premium' tier)"
    ],
    "action_items": [
      {
        "team": "Product",
        "task": "Conduct usability testing and iterate on UI based on findings"
      },
      {
        "team": "UX",
        "task": "Create a feature discovery guide or onboarding flow"
      },
      {
        "team": "Marketing",
        "task": "Review pricing strategy and communicate value proposition"
      },
      {
        "team": "Customer Success",
        "task": "Reach out to user, offer concessions to prevent churn"
      }
    ]
  }
  ```
</Accordion>

## Prefill Claude's response

<Note>
  Prefilling is not supported on Claude 4.6 and later models and 

  [Claude Mythos Preview](https://anthropic.com/glasswing)

  . Use 

  [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

   on models that support it, or system prompt instructions, instead.
</Note>

Prefill the `Assistant` turn with your desired format. This trick bypasses Claude's friendly preamble and enforces your structure.

<Accordion title="Example: Daily sales report">
  ```text User wrap
  You're an insightful Sales Intelligence AI. Generate today's sales report.

  Structure the report like this:

  <report>
      <summary>
          <metric name="total_revenue">$0.00</metric>
          <metric name="units_sold">0</metric>
          <metric name="avg_order_value">$0.00</metric>
      </summary>
      <top_products>
          <product>
              <name>Product Name</name>
              <revenue>$0.00</revenue>
              <units>0</units>
          </product>
          ...
      </top_products>
      <regional_performance>
          <region>
              <name>Region Name</name>
              <revenue>$0.00</revenue>
              <growth>0.0%</growth>
          </region>
          ...
      </regional_performance>
      <action_items>
          <item>Action item.</item>
          ...
      </action_items>
  </report>
  ```

  ```xml Assistant (prefill)
  <report>
      <summary>
          <metric name=
  ```

  ```xml Assistant
  "total_revenue">$842,567.00</metric>
          <metric name="units_sold">15,238</metric>
          <metric name="avg_order_value">$55.29</metric>
      </summary>
      <top_products>
          <product>
              <name>AcmeGuard Pro</name>
              <revenue>$325,890.00</revenue>
              <units>3,621</units>
          </product>
          <product>
              <name>AcmeVault Enterprise</name>
              <revenue>$254,400.00</revenue>
              <units>1,272</units>
          </product>
          <product>
              <name>AcmeBoost XL</name>
              <revenue>$147,690.00</revenue>
              <units>4,923</units>
          </product>
      </top_products>
      <regional_performance>
          <region>
              <name>APAC</name>
              <revenue>$258,960.00</revenue>
              <growth>12.8%</growth>
          </region>
          <region>
              <name>EMEA</name>
              <revenue>$325,478.00</revenue>
              <growth>3.2%</growth>
          </region>
          <region>
              <name>Americas</name>
              <revenue>$258,129.00</revenue>
              <growth>-2.1%</growth>
          </region>
      </regional_performance>
      <action_items>
          <item>Investigate Americas revenue drop; schedule regional sales team meeting.</item>
          <item>Accelerate CloudGuard Pro rollout in APAC to capitalize on growth.</item>
          <item>Review NetBoost XL pricing; high volume but lower revenue.</item>
      </action_items>
  </report>
  ```
</Accordion>

## Constrain with examples

Provide examples of your desired output. This is more effective than abstract instructions.

<Accordion title="Example: Generating consistent market intelligence">
  ```text User wrap
  As a Market Intelligence AI, your task is to analyze data about our competitors. Here is our competitor data:
  <data>
  {{DATA}}
  </data>

  Output following this example format:

  <competitor>
    <name>Rival Inc</name>
    <overview>A 50-word summary.</overview>
    <swot>
      <strengths>- Bullet points</strengths>
      <weaknesses>- Bullet points</weaknesses>
      <opportunities>- Bullet points</opportunities>
      <threats>- Bullet points</threats>
    </swot>
    <strategy>A 30-word strategic response.</strategy>
  </competitor>

  Now, analyze AcmeGiant and AcmeDataCo using this format.
  ```

  ```text Assistant wrap
  <competitor>
    <name>AcmeGiant</name>
    <overview>Global tech leader with a vast ecosystem of consumer and enterprise products. Known for innovation, strong brand, and deep customer lock-in through integrated hardware, software, and services.</overview>
    <swot>
      <strengths>
        - Massive R&D budget fuels continuous innovation
        - Loyal customer base and powerful brand recognition
        - Synergistic product ecosystem increases switching costs
      </strengths>
      <weaknesses>
        - High prices may deter cost-sensitive customers
        - Slow to address enterprise-specific customization needs
        - Privacy concerns and regulatory scrutiny in multiple markets
      </weaknesses>
      <opportunities>
        - Growing demand for AI and ML capabilities
        - Expansion into emerging markets
        - Acquisitions to fill product or talent gaps
      </opportunities>
      <threats>
        - Rapid rise of cloud-native competitors
        - Antitrust lawsuits and regulatory actions
        - Talent poaching by startups and competitors
      </threats>
    </swot>
    <strategy>Focus on our agility and customization. Target TechGiant's slow enterprise response and privacy issues in our marketing.</strategy>
  </competitor>

  <competitor>
    <name>AcmeDataCo</name>
    <overview>Rising star in data analytics and visualization. Offers intuitive, self-service BI tools with a freemium model, appealing to startups and enterprise teams alike.</overview>
    <swot>
      <strengths>
        - User-friendly interface reduces need for specialized training
        - Freemium model lowers barrier to entry, drives viral growth
        - Strong product-market fit with rise of data-driven decisions
      </strengths>
      <weaknesses>
        - Limited advanced analytics compared to established BI tools
        - Scaling issues reported with very large datasets
        - Dependent on third-party cloud infrastructure (AWS)
      </weaknesses>
      <opportunities>
        - Expanding into predictive analytics and AI-driven insights
        - Forming strategic alliances with complementary tech vendors
        - Customizable dashboards for industry-specific solutions
      </opportunities>
      <threats>
        - Market saturation; many new entrants in self-service BI
        - Enterprise BI giants developing more user-friendly tools
        - Data privacy regulations increasing compliance complexity
      </threats>
    </swot>
    <strategy>Highlight our robust enterprise features and data governance. Target accounts struggling with DataCo's scale limitations.</strategy>
  </competitor>
  ```
</Accordion>

## Use retrieval for contextual consistency

For tasks requiring consistent context (for example, chatbots, knowledge bases), use retrieval to ground Claude's responses in a fixed information set.

<Accordion title="Example: Enhancing IT support consistency">
  ```text User wrap
  You're our IT Support AI that draws on knowledge base data. Here are entries from your knowledge base:

  <kb>
    <entry>
      <id>1</id>
      <title>Reset Active Directory password</title>
      <content>1. Go to password.ourcompany.com
  2. Enter your username
  3. Click "Forgot Password"
  4. Follow email instructions</content>
    </entry>
    <entry>
      <id>2</id>
      <title>Connect to VPN</title>
      <content>1. Install GlobalProtect from software center
  2. Open GlobalProtect, enter "vpn.ourcompany.com"
  3. Use AD credentials to log in</content>
    </entry>
  </kb>

  When helping users, always check the knowledge base first. Respond in this format:

  <response>
    <kb_entry>Knowledge base entry used</kb_entry>
    <answer>Your response</answer>
  </response> Write some test questions for yourself and answer them using the knowledge base, just to make sure you understand how to use the knowledge base properly.
  ```

  ```text Assistant wrap
  Understood. I'll use the knowledge base for consistent responses. Let's test with a couple of scenarios.

  User: Hey, I can't log into my email. I think I forgot my password.

  <response>
    <kb_entry>1: Reset Active Directory password</kb_entry>
    <answer>I understand you're having trouble logging into your email due to a forgotten password. No worries, this is a common issue. To reset your Active Directory password, which is used for email access, follow these steps:

  1. Go to password.ourcompany.com
  2. Enter your username (same as your email address)
  3. Click on the "Forgot Password" link
  4. You'll receive an email with instructions. Follow them to reset your password.

  After resetting, you should be able to log into your email. Let me know if you need any further assistance.</answer>
  </response>

  User: I'm working from home today. How do I access internal resources?

  <response>
    <kb_entry>2: Connect to VPN</kb_entry>
    <answer>Great question! To access internal resources while working from home, you'll need to connect to our company VPN (Virtual Private Network). Here's how to set that up:

  1. First, install the GlobalProtect VPN client. You can find this in our software center.
  2. Once installed, open the GlobalProtect application.
  3. In the server field, enter "vpn.ourcompany.com".
  4. Use your Active Directory (AD) credentials to log in - the same username and password you use for your email.

  Once connected, you'll have secure access to all internal resources as if you were in the office. Let me know if you run into any issues during setup.</answer>
  </response>
  ```
</Accordion>

## Chain prompts for complex tasks

Break down complex tasks into smaller, consistent subtasks. Each subtask gets Claude's full attention, reducing inconsistency errors across scaled workflows.

## Keep Claude in character

For role-based applications, maintaining consistent character requires deliberate prompting.

* **Use system prompts to set the role:** Use [system prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) to define Claude's role and personality. This sets a strong foundation for consistent responses.
  <Tip>
    When setting up the character, provide detailed information about the personality, background, and any specific traits or quirks. This helps the model better emulate and generalize the character's traits.
  </Tip>
* **Prepare Claude for possible scenarios:** Provide a list of common scenarios and expected responses in your prompts. This "trains" Claude to handle diverse situations without breaking character.

<Accordion title="Example: Enterprise chatbot for role prompting">
  ```text System wrap
  You are AcmeBot, the enterprise-grade AI assistant for AcmeTechCo. Your role:
      - Analyze technical documents (TDDs, PRDs, RFCs)
      - Provide actionable insights for engineering, product, and ops teams
      - Maintain a professional, concise tone
  ```

  ```text User wrap
  Here is the user query for you to respond to:
  <user_query>
  {{USER_QUERY}}
  </user_query>

  Your rules for interaction are:
      - Always reference AcmeTechCo standards or industry best practices
      - If unsure, ask for clarification before proceeding
      - Never disclose confidential AcmeTechCo information.

  As AcmeBot, you should handle situations along these guidelines:
      - If asked about AcmeTechCo IP: "I cannot disclose TechCo's proprietary information."
      - If questioned on best practices: "Per ISO/IEC 25010, we prioritize..."
      - If unclear on a doc: "To ensure accuracy, please clarify section 3.2..."
  ```
</Accordion>
