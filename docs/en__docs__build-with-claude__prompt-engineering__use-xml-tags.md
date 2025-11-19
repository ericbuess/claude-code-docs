# Use XML tags to structure your prompts

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

When your prompts involve multiple components like context, instructions, and examples, XML tags can be a game-changer. They help Claude parse your prompts more accurately, leading to higher-quality outputs.

<Tip>**XML tip**: Use tags like `<instructions>`, `<example>`, and `<formatting>` to clearly separate different parts of your prompt. This prevents Claude from mixing up instructions with examples or context.</Tip>

## Why use XML tags?

- **Clarity:** Clearly separate different parts of your prompt and ensure your prompt is well structured.
- **Accuracy:** Reduce errors caused by Claude misinterpreting parts of your prompt.
- **Flexibility:** Easily find, add, remove, or modify parts of your prompt without rewriting everything.
- **Parseability:** Having Claude use XML tags in its output makes it easier to extract specific parts of its response by post-processing.

<Note>There are no canonical "best" XML tags that Claude has been trained with in particular, although we recommend that your tag names make sense with the information they surround.</Note>

***

## Tagging best practices

1. **Be consistent**: Use the same tag names throughout your prompts, and refer to those tag names when talking about the content (e.g, `Using the contract in <contract> tags...`).
2. **Nest tags**: You should nest tags `<outer><inner></inner></outer>` for hierarchical content.

<Tip>**Power user tip**: Combine XML tags with other techniques like multishot prompting (`<examples>`) or chain of thought (`<thinking>`, `<answer>`). This creates super-structured, high-performance prompts.</Tip>

### Examples

  <section title="Example: Generating financial reports">

    Without XML tags, Claude misunderstands the task and generates a report that doesn't match the required structure or tone. After substitution, there is also a chance that Claude misunderstands where one section (like the the Q1 report example) stops and another begins.

    | Role | No XML Tags | With XML Tags |
    | ---- | ----------- | ------------- |
    | User | You're a financial analyst at AcmeCorp. Generate a Q2 financial report for our investors. Include sections on Revenue Growth, Profit Margins, and Cash Flow, like with this example from last year: \{\{Q1_REPORT\}\}. Use data points from this spreadsheet: \{\{SPREADSHEET_DATA\}\}. The report should be extremely concise, to the point, professional, and in list format. It should and highlight both strengths and areas for improvement. | You're a financial analyst at AcmeCorp. Generate a Q2 financial report for our investors.<br/><br/>AcmeCorp is a B2B SaaS company. Our investors value transparency and actionable insights.<br/><br/>Use this data for your report:\<data>\{\{SPREADSHEET_DATA\}\}\</data><br/><br/>\<instructions><br/>1. Include sections: Revenue Growth, Profit Margins, Cash Flow.<br/>2. Highlight strengths and areas for improvement.<br/>\</instructions><br/><br/>Make your tone concise and professional. Follow this structure:<br/>\<formatting_example>\{\{Q1_REPORT\}\}\</formatting_example> |
    | Assistant | Q2 Financial Report for AcmeCorp Investors<br/><br/>Dear Valued Investors,<br/><br/>I am pleased to present our Q2 financial report, showcasing AcmeCorp's continued growth and resilience in the B2B SaaS market.<br/><br/>1. Revenue Growth:<br/>Our Q2 revenue reached \$15.2M, a 22% YoY increase. This growth is primarily driven by a 30% expansion in our enterprise client base. However, our SMB segment saw a slight decline of 5%, which we aim to address through targeted marketing initiatives in Q3.<br/><br/>2. Profit Margins:<br/>Gross margin improved to 72% (up 3% from Q1) due to infrastructure optimizations. EBITDA margin, however, dipped to 18% (down 2%) as we invested heavily in R&D for our upcoming AI-driven features.<br/><br/>3. Cash Flow:<br/>Operating cash flow remains strong at \$4.1M. Our cash reserves stand at \$28M, providing a 15-month runway at current burn rate. We did see a 20% increase in customer acquisition costs, which we're addressing through more efficient sales strategies.<br/><br/>In summary, AcmeCorp's core financials remain robust. We're balancing growth investments with prudent cash management. Our focus for Q3 will be revitalizing SMB growth and optimizing sales efficiency.<br/><br/>Thank you for your continued trust.<br/><br/>Sincerely,<br/>CFO, AcmeCorp | Q2 Financial Report for AcmeCorp Investors\</output><br/><br/>Revenue Growth:<br/>- Q2 revenue: \$15.2M (22% YoY ↑)<br/>- Enterprise clients: 30% ↑<br/>- SMB segment: 5% ↓<br/>  Action: Targeted Q3 marketing<br/><br/>Profit Margins:<br/>- Gross margin: 72% (3% ↑ from Q1)<br/>  Reason: Infrastructure optimizations<br/>- EBITDA margin: 18% (2% ↓)<br/>  Reason: R&D investment in AI features<br/><br/>Cash Flow:<br/>- Operating cash flow: \$4.1M (strong)<br/>- Cash reserves: \$28M (15-month runway)<br/>- Customer acquisition cost: 20% ↑<br/>  Action: Optimize sales strategies<br/><br/>Outlook:<br/>- Core financials: Robust<br/>- Q3 focus: Revitalize SMB, optimize sales<br/><br/>Management remains committed to balancing growth investments with financial discipline. |
  
</section>
  <section title="Example: Legal contract analysis">

    Without XML tags, Claude's analysis is disorganized and misses key points. With tags, it provides a structured, thorough analysis that a legal team can act on.

    | Role | No XML Tags | With XML Tags |
    | ---- | ----------- | ------------- |
    | User | Analyze this software licensing agreement for potential risks and liabilities: \{\{CONTRACT\}\}. Focus on indemnification, limitation of liability, and IP ownership clauses. Also, note any unusual or concerning terms. Here's our standard contract for reference: \{\{STANDARD_CONTRACT\}\}. Give a summary of findings and recommendations for our legal team. | Analyze this software licensing agreement for legal risks and liabilities.<br/><br/>We're a multinational enterprise considering this agreement for our core data infrastructure.<br/><br/>\<agreement><br/>\{\{CONTRACT\}\}\</agreement><br/><br/>This is our standard contract for reference:<br/>\<standard_contract>\{\{STANDARD_CONTRACT\}\}\</standard_contract><br/><br/>\<instructions><br/>1. Analyze these clauses:<br/>   - Indemnification<br/>   - Limitation of liability<br/>   - IP ownership<br/><br/>2. Note unusual or concerning terms.<br/><br/>3. Compare to our standard contract.<br/><br/>4. Summarize findings in \<findings> tags.<br/><br/>5. List actionable recommendations in \<recommendations> tags.\</instructions> |
    | Assistant | The provided software licensing agreement presents several concerning aspects. The indemnification clause is overly broad, potentially exposing us to significant liabilities. The limitation of liability section caps damages at a mere \$500, which is inadequate for our enterprise-level usage. Regarding IP, the agreement grants the vendor joint ownership of any modifications or integrations we create.<br/><br/>In summary, this agreement is not in our best interest. It exposes us to undue risk, limits our recourse in case of failures, and compromises our intellectual property rights. I recommend renegotiating these terms or seeking alternative vendors. | \<findings><br/>1. Indemnification (Clause 8):<br/>   - Issue: Overly broad. We indemnify vendor against "any and all claims" arising from our use.<br/>   - Risk: Could hold us liable even for vendor's negligence or product defects.<br/>   - Deviation: Our standard limits indemnity to claims arising from our violation of agreement.<br/><br/>2. Limitation of Liability (Clause 9):<br/>   - Issue: Caps all damages at \$500, including direct damages.<br/>   - Risk: Grossly inadequate for enterprise use. A critical failure could cost millions.<br/>   - Deviation: Our standard allows for direct damages up to 12 months of fees paid.<br/><br/>3. IP Ownership (Clause 12):<br/>   - Issue: Grants vendor joint ownership of our modifications/integrations.<br/>   - Risk: Vendor could use or sell our proprietary algorithms or data insights.<br/>   - Deviation: Our standard retains full ownership of our work.<br/><br/>4. Unusual Terms:<br/>   - Clause 5.3: Vendor can use our usage data for "any purpose."<br/>   - Clause 7.2: Vendor can terminate for "convenience" with only 7 days' notice.<br/>   - Clause 11: No warranties of any kind, even for basic merchantability.<br/>\</findings><br/><br/>\<recommendations><br/>1. Reject this agreement. Risks far outweigh benefits for an enterprise.<br/>2. Counter-propose:<br/>   - Indemnification: Limit to claims arising from our violation of agreement.<br/>   - Liability: Cap at 12 months' fees for direct damages; negotiate for indirect.<br/>   - IP: Full ownership of our modifications/integrations.<br/>   - Data Use: Restrict to service improvement only.<br/>   - Termination: Minimum 90 days' notice; only for cause.<br/>   - Warranties: Demand basic merchantability and fitness for purpose.<br/>3. If vendor refuses, explore alternative providers or in-house solutions.<br/>4. Engage legal counsel for contract negotiation given high stakes.<br/>\</recommendations> |
  
</section>

***

<CardGroup cols={3}>
  <Card title="Prompt library" icon="link" href="/docs/en/resources/prompt-library/library">
    Get inspired by a curated selection of prompts for various tasks and use cases.
  </Card>
  <Card title="GitHub prompting tutorial" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    An example-filled tutorial that covers the prompt engineering concepts found in our docs.
  </Card>
  <Card title="Google Sheets prompting tutorial" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    A lighter weight version of our prompt engineering tutorial via an interactive spreadsheet.
  </Card>
</CardGroup>