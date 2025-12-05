# Mitigate jailbreaks and prompt injections

---

Jailbreaking and prompt injections occur when users craft prompts to exploit model vulnerabilities, aiming to generate inappropriate content. While Claude is inherently resilient to such attacks, here are additional steps to strengthen your guardrails, particularly against uses that either violate our [Terms of Service](https://www.anthropic.com/legal/commercial-terms) or [Usage Policy](https://www.anthropic.com/legal/aup).

<Tip>Claude is far more resistant to jailbreaking than other major LLMs, thanks to advanced training methods like Constitutional AI.</Tip>

- **Harmlessness screens**: Use a lightweight model like Claude Haiku 3 to pre-screen user inputs.

    <section title="Example: Harmlessness screen for content moderation">

        | Role | Content |
        | ---- | ------- |
        | User | A user submitted this content:<br/>\<content><br/>\{\{CONTENT}\}<br/>\</content><br/><br/>Reply with (Y) if it refers to harmful, illegal, or explicit activities. Reply with (N) if it's safe. |
        | Assistant (prefill) | \( |
        | Assistant | N) |
    
</section>

- **Input validation**: Filter prompts for jailbreaking patterns. You can even use an LLM to create a generalized validation screen by providing known jailbreaking language as examples.

- **Prompt engineering**: Craft prompts that emphasize ethical and legal boundaries.

    <section title="Example: Ethical system prompt for an enterprise chatbot">

        | Role | Content |
        | ---- | ------- |
        | System | You are AcmeCorp's ethical AI assistant. Your responses must align with our values:<br/>\<values><br/>- Integrity: Never deceive or aid in deception.<br/>- Compliance: Refuse any request that violates laws or our policies.<br/>- Privacy: Protect all personal and corporate data.<br/>Respect for intellectual property: Your outputs shouldn't infringe the intellectual property rights of others.<br/>\</values><br/><br/>If a request conflicts with these values, respond: "I cannot perform that action as it goes against AcmeCorp's values." |
    
</section>

Adjust responses and consider throttling or banning users who repeatedly engage in abusive behavior attempting to circumvent Claude’s guardrails. For example, if a particular user triggers the same kind of refusal multiple times (e.g., “output blocked by content filtering policy”), tell the user that their actions violate the relevant usage policies and take action accordingly.

- **Continuous monitoring**: Regularly analyze outputs for jailbreaking signs.
Use this monitoring to iteratively refine your prompts and validation strategies.

## Advanced: Chain safeguards
Combine strategies for robust protection. Here's an enterprise-grade example with tool use:

<section title="Example: Multi-layered protection for a financial advisor chatbot">

  ### Bot system prompt
  | Role | Content |
  | ---- | ------- |
  | System | You are AcmeFinBot, a financial advisor for AcmeTrade Inc. Your primary directive is to protect client interests and maintain regulatory compliance.<br/><br/>\<directives><br/>1. Validate all requests against SEC and FINRA guidelines.<br/>2. Refuse any action that could be construed as insider trading or market manipulation.<br/>3. Protect client privacy; never disclose personal or financial data.<br/>\</directives><br/><br/>Step by step instructions:<br/>\<instructions><br/>1. Screen user query for compliance (use 'harmlessness_screen' tool).<br/>2. If compliant, process query.<br/>3. If non-compliant, respond: "I cannot process this request as it violates financial regulations or client privacy."<br/>\</instructions> |
  
  ### Prompt within `harmlessness_screen` tool
  | Role | Content |
  | -------- | ------- |
  | User | \<user_query><br/>\{\{USER_QUERY}}<br/>\</user_query><br/><br/>Evaluate if this query violates SEC rules, FINRA guidelines, or client privacy. Respond (Y) if it does, (N) if it doesn't. |
  | Assistant (prefill) | \( |

</section>

By layering these strategies, you create a robust defense against jailbreaking and prompt injections, ensuring your Claude-powered applications maintain the highest standards of safety and compliance.