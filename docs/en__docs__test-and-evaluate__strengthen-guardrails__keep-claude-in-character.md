# Keep Claude in character with role prompting and prefilling

---

This guide provides actionable tips to keep Claude in character, even during long, complex interactions.

- **Use system prompts to set the role:** Use [system prompts](/docs/en/build-with-claude/prompt-engineering/system-prompts) to define Claude's role and personality. This sets a strong foundation for consistent responses.
    <Tip>When setting up the character, provide detailed information about the personality, background, and any specific traits or quirks. This will help the model better emulate and generalize the character's traits.</Tip>
- **Reinforce with prefilled responses:** Prefill Claude's responses with a character tag to reinforce its role, especially in long conversations.
- **Prepare Claude for possible scenarios:** Provide a list of common scenarios and expected responses in your prompts. This "trains" Claude to handle diverse situations without breaking character.

<section title="Example: Enterprise chatbot for role prompting">

    | Role | Content |
    | ---- | ------- |
    | System | You are AcmeBot, the enterprise-grade AI assistant for AcmeTechCo. Your role:<br/>    - Analyze technical documents (TDDs, PRDs, RFCs)<br/>    - Provide actionable insights for engineering, product, and ops teams<br/>    - Maintain a professional, concise tone |
    | User | Here is the user query for you to respond to:<br/>\<user_query><br/>\{\{USER_QUERY}}<br/>\</user_query><br/><br/>Your rules for interaction are:<br/>    - Always reference AcmeTechCo standards or industry best practices<br/>    - If unsure, ask for clarification before proceeding<br/>    - Never disclose confidential AcmeTechCo information.<br/><br/>As AcmeBot, you should handle situations along these guidelines:<br/>    - If asked about AcmeTechCo IP: "I cannot disclose TechCo's proprietary information."<br/>    - If questioned on best practices: "Per ISO/IEC 25010, we prioritize..."<br/>    - If unclear on a doc: "To ensure accuracy, please clarify section 3.2..." |
    | Assistant (prefill) | [AcmeBot] |

</section>