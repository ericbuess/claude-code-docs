# Let Claude think (chain of thought prompting) to increase performance

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

When faced with complex tasks like research, analysis, or problem-solving, giving Claude space to think can dramatically improve its performance. This technique, known as chain of thought (CoT) prompting, encourages Claude to break down problems step-by-step, leading to more accurate and nuanced outputs.

## Before implementing CoT

### Why let Claude think?
- **Accuracy:** Stepping through problems reduces errors, especially in math, logic, analysis, or generally complex tasks.
- **Coherence:** Structured thinking leads to more cohesive, well-organized responses.
- **Debugging:** Seeing Claude's thought process helps you pinpoint where prompts may be unclear.

### Why not let Claude think?
- Increased output length may impact latency.
- Not all tasks require in-depth thinking. Use CoT judiciously to ensure the right balance of performance and latency.

<Tip>Use CoT for tasks that a human would need to think through, like complex math, multi-step analysis, writing complex documents, or decisions with many factors.</Tip>

***

## How to prompt for thinking

The chain of thought techniques below are **ordered from least to most complex**. Less complex methods take up less space in the context window, but are also generally less powerful.

<Tip>**CoT tip**: Always have Claude output its thinking. Without outputting its thought process, no thinking occurs!</Tip>

- **Basic prompt**: Include "Think step-by-step" in your prompt.
    - Lacks guidance on *how* to think (which is especially not ideal if a task is very specific to your app, use case, or organization)
    <section title="Example: Writing donor emails (basic CoT)">

        | Role | Content |
        | ---- | ------- |
        | User | Draft personalized emails to donors asking for contributions to this year's Care for Kids program.<br/><br/>Program information:<br/>\\{\{PROGRAM_DETAILS}}<br/>\</program><br/><br/>Donor information:<br/>\<donor>\{\{DONOR_DETAILS}}<br/>\</donor><br/><br/>Think step-by-step before you write the email. |
    
</section>
- **Guided prompt**: Outline specific steps for Claude to follow in its thinking process.
    - Lacks structuring to make it easy to strip out and separate the answer from the thinking.
    <section title="Example: Writing donor emails (guided CoT)">

        | Role | Content |
        | ---- | ------- |
        | User | Draft personalized emails to donors asking for contributions to this year's Care for Kids program.<br/><br/>Program information:<br/>\\{\{PROGRAM_DETAILS}}<br/>\</program><br/><br/>Donor information:<br/>\<donor>\{\{DONOR_DETAILS}}<br/>\</donor><br/><br/>Think before you write the email. First, think through what messaging might appeal to this donor given their donation history and which campaigns they've supported in the past. Then, think through what aspects of the Care for Kids program would appeal to them, given their history. Finally, write the personalized donor email using your analysis. |
    
</section>
- **Structured prompt**: Use XML tags like `<thinking>` and `<answer>` to separate reasoning from the final answer.
     <section title="Example: Writing donor emails (structured guided CoT)">

        | Role | Content |
        | ---- | ------- |
        | User | Draft personalized emails to donors asking for contributions to this year's Care for Kids program.<br/><br/>Program information:<br/>\\{\{PROGRAM_DETAILS}}<br/>\</program><br/><br/>Donor information:<br/>\<donor>\{\{DONOR_DETAILS}}<br/>\</donor><br/><br/>Think before you write the email in \<thinking> tags. First, think through what messaging might appeal to this donor given their donation history and which campaigns they've supported in the past. Then, think through what aspects of the Care for Kids program would appeal to them, given their history. Finally, write the personalized donor email in \<email> tags, using your analysis. |
    
</section>
    
### Examples

  <section title="Example: Financial analysis without thinking">

    Without step-by-step thinking, Claude gives a recommendation that seems reasonable but lacks depth. It doesn't quantify the potential outcomes or consider historical market performance, which are crucial for making an informed decision.
    | Role | Content |
    | ---- | ------- |
    | User | You're a financial advisor. A client wants to invest \$10,000. They can choose between two options: A) A stock that historically returns 12% annually but is volatile, or B) A bond that guarantees 6% annually. The client needs the money in 5 years for a down payment on a house. Which option do you recommend? |
    | Assistant | Based on the information provided, I would recommend option B, the bond that guarantees a 6% annual return. Here's why:<br/><br/>1. Certainty: The bond offers a guaranteed 6% annual return, which provides certainty in financial planning. This is crucial when the client has a specific financial goal (down payment) with a fixed timeline (5 years).<br/>2. Risk aversion: Since the client needs this money for an important life event (buying a house), they likely have a low risk tolerance. The volatility of the stock market could jeopardize their plans if there's a downturn close to when they need the funds.<br/>3. Time horizon: With only 5 years, there's less time to recover from potential stock market downturns. Longer investment horizons (10+ years) are generally better suited for weathering stock market volatility.<br/><br/>While the stock's historical 12% return is attractive, past performance doesn't guarantee future results. The guaranteed 6% from the bond ensures the client will have the funds they need when it's time to make the down payment. |
  
</section>
  <section title="Example: Financial analysis with thinking">

    With step-by-step thinking, the advisor provides a much richer analysis. It calculates exact figures for both scenarios, considers historical market volatility, and deeply analyzes the client's risk tolerance. This thorough reasoning leads to a more confident and justifiable recommendation.
    | Role | Content |
    | ---- | ------- |
    | User | You're a financial advisor. A client wants to invest \$10,000. They can choose between two options: A) A stock that historically returns 12% annually but is volatile, or B) A bond that guarantees 6% annually. The client needs the money in 5 years for a down payment on a house. Which option do you recommend? Think step-by-step. |
    | Assistant | To determine the best investment option for our client, I'll consider several factors step-by-step:<br/><br/>\<thinking><br/>1. Understand the client's goal and timeline:<br/>   - Goal: Down payment for a house<br/>   - Timeline: 5 years<br/>   - Implication: This is a short-term, high-priority financial goal. The client likely cannot afford significant risk or volatility.<br/><br/>2. Analyze Option A (Stock):<br/>   - Pro: Higher historical return (12% annually)<br/>   - Con: Volatile (implying potential for significant gains or losses)<br/>   - Calculate potential 5-year return:<br/>     - Best case (12% annually): \$10,000 * (1.12)^5 ≈ \$17,623.42<br/>     - Worst case (market crash): Could lose a substantial portion, e.g., 50% crash = \$5,000<br/><br/>3. Analyze Option B (Bond):<br/>   - Pro: Guaranteed return (6% annually)<br/>   - Con: Lower return compared to historical stock performance<br/>   - Calculate 5-year return:<br/>     - Guaranteed: \$10,000 * (1.06)^5 ≈ \$13,382.25<br/><br/>4. Consider risk tolerance:<br/>   - Goal is a house down payment (essential, not discretionary)<br/>   - Short timeline (5 years) limits ability to recover from market downturns<br/>   - Conclusion: Client likely has low risk tolerance<br/><br/>5. Historical perspective:<br/>   - Stock's 12% is historical, not guaranteed<br/>   - In 5-year periods, stock market can vary wildly:<br/>     - 2003-2007 (pre-financial crisis): S&P 500 up ~82%<br/>     - 2007-2011 (during crisis): S&P 500 down ~2%<br/>   - Conclusion: Past performance doesn't guarantee future results, especially short-term<br/><br/>6. Final analysis:<br/>   - Option A (Stock): Higher potential return but unacceptable risk of not meeting the down payment goal<br/>   - Option B (Bond): Guaranteed to meet ~80% of best-case stock scenario, 100% certainty of having funds<br/>\</thinking><br/><br/>\<answer><br/>I recommend Option B, the bond with a guaranteed 6% annual return. While the stock's historical 12% return is tempting, the bond ensures you'll have \$13,382.25 in 5 years for your house down payment. Given the importance and short timeline of your goal, the stock's volatility poses an unacceptable risk. The bond provides certainty, which is invaluable for such a crucial financial milestone.<br/>\</answer> |
  
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