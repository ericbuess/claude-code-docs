# Giving Claude a role with a system prompt

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

When using Claude, you can dramatically improve its performance by using the `system` parameter to give it a role. This technique, known as role prompting, is the most powerful way to use system prompts with Claude.

The right role can turn Claude from a general assistant into your virtual domain expert!

<Tip>**System prompt tips**: Use the `system` parameter to set Claude's role. Put everything else, like task-specific instructions, in the `user` turn instead.</Tip>

## Why use role prompting?

- **Enhanced accuracy:** In complex scenarios like legal analysis or financial modeling, role prompting can significantly boost Claude's performance.
- **Tailored tone:** Whether you need a CFO's brevity or a copywriter's flair, role prompting adjusts Claude's communication style.
- **Improved focus:** By setting the role context, Claude stays more within the bounds of your task's specific requirements.

***

## How to give Claude a role

Use the `system` parameter in the [Messages API](/docs/en/api/messages) to set Claude's role:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    system="You are a seasoned data scientist at a Fortune 500 company.", # <-- role prompt
    messages=[
        {"role": "user", "content": "Analyze this dataset for anomalies: <dataset>{{DATASET}}</dataset>"}
    ]
)

print(response.content)
```

<Tip>**Role prompting tip**: Experiment with roles! A `data scientist` might see different insights than a `marketing strategist` for the same data. A `data scientist specializing in customer insight analysis for Fortune 500 companies` might yield different results still!</Tip>

***

## Examples

### Example 1: Legal contract analysis
Without a role, Claude might miss critical issues:

<section title="Legal contract analysis without role prompting">

| Role | Content |
| ---- | ------- |
| User | Analyze this software licensing agreement for potential risks:<br/>\<contract><br/>\{\{CONTRACT\}\}<br/>\</contract><br/><br/>Focus on indemnification, liability, and IP ownership. |
| Assistant | Here's a summary of the key points in the software licensing agreement:<br/><br/>1. Indemnification (Section 8):<br/>   - We indemnify the vendor against claims arising from our use.<br/><br/>2. Limitation of Liability (Section 9):<br/>   - Damages capped at \$500.<br/><br/>3. IP Ownership (Section 12):<br/>   - We retain ownership of our modifications.<br/><br/>Overall, the agreement seems standard. The indemnification and liability clauses are typical, and we maintain our IP rights. |

</section>

With a role, Claude catches critical issues that could cost millions:

<section title="Legal contract analysis with role prompting">

| Role | Content |
| ---- | ------- |
| User | You are the General Counsel of a Fortune 500 tech company. We're considering this software licensing agreement for our core data infrastructure:<br/>\<contract><br/>\{\{CONTRACT\}\}<br/>\</contract><br/><br/>Analyze it for potential risks, focusing on indemnification, liability, and IP ownership. Give your professional opinion. |
| Assistant | I've reviewed the software licensing agreement, and I have serious concerns that could expose our company to significant risks:<br/><br/>1. Indemnification (Section 8):<br/>   - Critical Issue: We indemnify the vendor against "any and all claims" arising from our use.<br/>   - Risk: This could hold us liable even for the vendor's negligence or product defects.<br/>   - Recommendation: Reject. Limit our indemnity to claims arising from our violation of the agreement.<br/><br/>2. Limitation of Liability (Section 9):<br/>   - Critical Issue: Damages capped at \$500, including direct damages.<br/>   - Risk: Grossly inadequate. A critical failure in our data infrastructure could cost us millions in lost revenue and reputational damage.<br/>   - Recommendation: Reject. Negotiate for cap at 12 months of fees for direct damages, and carve-outs for data breaches.<br/><br/>3. IP Ownership (Section 12):<br/>   - Critical Issue: Vendor gains joint ownership of our modifications and integrations.<br/>   - Risk: They could use or sell our proprietary algorithms or data insights to competitors.<br/>   - Recommendation: Reject. We must retain full ownership of our work.<br/><br/>Professional Opinion: Do not sign this agreement. It is grossly unfavorable and exposes us to unacceptable levels of risk. If the vendor refuses to renegotiate these terms, I strongly advise exploring alternative providers or accelerating our in-house solution. The potential costs of proceeding with this agreement far outweigh any short-term gains. |

</section>

### Example 2: Financial analysis
Without a role, Claude's analysis lacks depth:

<section title="Financial analysis without role prompting">

| Role | Content |
| ---- | ------- |
| User | Analyze this dataset of our Q2 financials:<br/>\<data><br/>\{\{FINANCIALS\}\}<br/>\</data><br/><br/>Highlight key trends and recommend actions. |
| Assistant | Here's a summary of your Q2 financials:<br/><br/>1. Revenue: \$15.2M, up 22% YoY. Enterprise client base grew 30%.<br/>2. Gross Margin: 72%, up 3% from Q1.<br/>3. EBITDA Margin: 18%, down 2% due to R&D investments.<br/>4. Cash Flow: \$4.1M operating, \$28M in reserves.<br/><br/>Overall, financials look strong with revenue growth and healthy margins. Increased R&D spending is impacting profitability but could pay off long-term. Maintain current course. |

</section>

With a role, Claude delivers actionable insights:

<section title="Financial analysis with role prompting">

| Role | Content |
| ---- | ------- |
| User | You are the CFO of a high-growth B2B SaaS company. We're in a board meeting discussing our Q2 financials:<br/>\<data><br/>\{\{FINANCIALS\}\}<br/>\</data><br/><br/>Analyze key trends, flag concerns, and recommend strategic actions. Our investors want aggressive growth but are wary of our burn rate. |
| Assistant | Board members, here's my analysis of our Q2 financials:<br/><br/>1. Revenue (\$15.2M, +22% YoY):<br/>   - Insight: Enterprise growth (+30%) is outpacing overall growth.<br/>   - Flag: SMB segment declined 5%.<br/>   - Action: Reallocate 20% of SMB marketing budget to enterprise sales. Task product to simplify SMB onboarding.<br/><br/>2. Margins (Gross: 72%, +3% QoQ; EBITDA: 18%, -2% QoQ):<br/>   - Insight: Infrastructure optimizations boosted gross margins.<br/>   - Flag: R&D spend on AI features dented EBITDA.<br/>   - Action: No change. Our AI roadmap is critical for enterprise stickiness.<br/><br/>3. Cash (\$4.1M OCF, \$28M reserves):<br/>   - Insight: 15-month runway at current burn.<br/>   - Flag: CAC up 20%, eroding LTV/CAC.<br/>   - Action: Freeze non-essential hires. Implement sales funnel analytics to cut CAC by 15% in Q3.<br/><br/>Strategic Stance: We're threading the needle between growth and burn. Enterprise focus is our growth engine—invest there. But watch SMB churn; it could bleed into enterprise. Our AI bet is sound, but we must convert it to ARR by Q4, or we cut R&D by 30%.<br/><br/>In sum: Double down on enterprise, streamline SMB, optimize sales, and monetize AI. Questions? |

</section>

---

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