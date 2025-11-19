# Be clear, direct, and detailed

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

When interacting with Claude, think of it as a brilliant but very new employee (with amnesia) who needs explicit instructions. Like any new employee, Claude does not have context on your norms, styles, guidelines, or preferred ways of working.
The more precisely you explain what you want, the better Claude's response will be.

<Tip>**The golden rule of clear prompting**<br/>Show your prompt to a colleague, ideally someone who has minimal context on the task, and ask them to follow the instructions. If they're confused, Claude will likely be too.</Tip>

## How to be clear, contextual, and specific

- **Give Claude contextual information:** Just like you might be able to better perform on a task if you knew more context, Claude will perform better if it has more contextual information. Some examples of contextual information:
    - What the task results will be used for
    - What audience the output is meant for
    - What workflow the task is a part of, and where this task belongs in that workflow
    - The end goal of the task, or what a successful task completion looks like
- **Be specific about what you want Claude to do:** For example, if you want Claude to output only code and nothing else, say so.
- **Provide instructions as sequential steps:** Use numbered lists or bullet points to better ensure that Claude carries out the task the exact way you want it to.

### Examples

    <section title="Example: Anonymizing customer feedback">

    Notice that Claude still makes mistakes in the unclear prompting example, such as leaving in a customer's name.

    | Role | Unclear Prompt | Clear Prompt |
    | --- | --- | --- |
    | User | Please remove all personally identifiable information from these customer feedback messages: \{\{FEEDBACK_DATA\}\} | Your task is to anonymize customer feedback for our quarterly review.<br/><br/>Instructions:<br/>1. Replace all customer names with "CUSTOMER_[ID]" (e.g., "Jane Doe" → "CUSTOMER_001").<br/>2. Replace email addresses with "EMAIL_[ID]@example.com".<br/>3. Redact phone numbers as "PHONE_[ID]".<br/>4. If a message mentions a specific product (e.g., "AcmeCloud"), leave it intact.<br/>5. If no PII is found, copy the message verbatim.<br/>6. Output only the processed messages, separated by "---".<br/><br/>Data to process: \{\{FEEDBACK_DATA\}\} |
    | Assistant (Claude's response) | Here are the anonymized customer feedback messages:<br/>1. I've been using your software for years, and it's been great. But lately, AcmeCloud has been crashing a lot. Fix it!<br/>2. XXX, your customer support rep, was incredibly helpful. He guided me through the whole process. My email is XXX if you want to send a survey.<br/>3. I'm John Smith, and I'm not happy. I've been on hold for 2 hours trying to reach someone at XXX. This is unacceptable! | CUSTOMER_001: I've been using your software for years, and it's been great. But lately, AcmeCloud has been crashing a lot. Fix it!<br/>---<br/>CUSTOMER_002: CUSTOMER_SERVICE_001, your customer support rep, was incredibly helpful. He guided me through the whole process. My email is EMAIL_002@example.com if you want to send a survey.<br/>---<br/>CUSTOMER_003: I'm CUSTOMER_003, and I'm not happy. I've been on hold for 2 hours trying to reach someone at PHONE_001. This is unacceptable! |
    
</section>
    <section title="Example: Crafting a marketing email campaign">

    Notice that Claude makes up details to fill in the gaps where it lacks context with the vague prompt.

    | Role | Vague Prompt | Specific Prompt |
    | --- | --- | --- |
    | User | Write a marketing email for our new AcmeCloud features. | Your task is to craft a targeted marketing email for our Q3 AcmeCloud feature release.<br/><br/>Instructions:<br/>1. Write for this target audience: Mid-size tech companies (100-500 employees) upgrading from on-prem to cloud.<br/>2. Highlight 3 key new features: advanced data encryption, cross-platform sync, and real-time collaboration.<br/>3. Tone: Professional yet approachable. Emphasize security, efficiency, and teamwork.<br/>4. Include a clear CTA: Free 30-day trial with priority onboarding.<br/>5. Subject line: Under 50 chars, mention "security" and "collaboration".<br/>6. Personalization: Use \{\{COMPANY_NAME\}\} and \{\{CONTACT_NAME\}\} variables.<br/><br/>Structure:<br/>1. Subject line<br/>2. Email body (150-200 words)<br/>3. CTA button text |
    | Assistant (Claude's response) | Here's a draft marketing email for our new features:<br/><br/>Subject: Boost Your Business with AcmeCloud's Latest Features<br/><br/>Dear Valued Customer,<br/><br/>We're excited to introduce three powerful features to AcmeCloud that will revolutionize your workflow:<br/><br/>1. Real-Time Collaboration: Work on documents simultaneously with your team. No more version control issues!<br/>2. AI-Powered Insights: Make data-driven decisions with AI that analyzes trends and automates tasks.<br/>3. Advanced Security Suite: End-to-end encryption, multi-factor auth, and threat detection keep your data safe.<br/><br/>Limited Offer: Upgrade now for a 20% first-year discount. Plus, refer a friend for an extra 10% off!<br/><br/>Best,<br/>The AcmeCloud Team | Subject line: AcmeCloud: Enterprise security meets real-time teamwork<br/><br/>Email body:<br/>Dear \{\{CONTACT_NAME\}\},<br/><br/>At \{\{COMPANY_NAME\}\}, you're scaling fast and eyeing the cloud. But with growth comes the challenge of keeping data secure while fostering collaboration. That's where AcmeCloud's Q3 release comes in, tailor-made for tech innovators like you.<br/><br/>1. Fort Knox for Your Files: Military-grade encryption now safeguards your data, both in motion and at rest. Your intellectual property stays yours, period.<br/>2. Sync Without Borders: Windows, Mac, or Linux—AcmeCloud speaks all languages. Unified version control means no more "final_v2_REALLY_FINAL.doc".<br/>3. Collaborate at Light Speed: Ditch the attachment ping-pong. Now your devs, designers, and data scientists co-create in real-time, slashing time-to-market.<br/><br/>Don't just take our word for it. Experience the AcmeCloud difference with our 30-day trial. And because we know time is your most precious asset, we're throwing in priority onboarding.<br/><br/>Elevate Your Team Now - Free 30-Day Trial |
    
</section>
    <section title="Example: Incident response">

    Notice that Claude outputs superfluous text and different formating with the vague prompt.
    | Role | Vague Prompt | Detailed Prompt |
    | --- | --- | --- |
    | User | Analyze this AcmeCloud outage report and summarize the key points.<br/><br/>\{\{REPORT\}\} | Analyze this AcmeCloud outage report. Skip the preamble. Keep your response terse and write only the bare bones necessary information. List only:<br/>1) Cause<br/>2) Duration<br/>3) Impacted services<br/>4) Number of affected users<br/>5) Estimated revenue loss. <br/><br/>Here's the report: \{\{REPORT\}\}|
    | Assistant (Claude's response) | Here's a summary of the key points from the AcmeCloud outage report:<br/><br/>On May 15th, a misconfigured load balancer update caused significant traffic routing issues, resulting in a service outage from 09:15 to 13:52 UTC. The 4-hour 37-minute disruption impacted our core file syncing service and admin dashboard, rendering them inaccessible. Additionally, the mobile app experienced partial functionality loss. Approximately 68% of our user base, totaling 1.3 million users, were affected. Based on our Service Level Agreements (SLAs) and average revenue per user, we estimate a financial impact of $420,000 in service credits and potential customer churn. | 1) Cause: Misconfigured load balancer update<br/>2) Duration: 4h 37m (09:15-13:52 UTC, May 15)<br/>3) Impacted: Core sync, admin dashboard (down); mobile app (partial)<br/>4) Affected users: 1.3M (68% of base)<br/>5) Est. revenue loss: $420,000 |
    
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