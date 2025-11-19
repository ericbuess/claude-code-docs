# Chain complex prompts for stronger performance

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

When working with complex tasks, Claude can sometimes drop the ball if you try to handle everything in a single prompt. Chain of thought (CoT) prompting is great, but what if your task has multiple distinct steps that each require in-depth thought?

Enter prompt chaining: breaking down complex tasks into smaller, manageable subtasks.

## Why chain prompts?

1. **Accuracy**: Each subtask gets Claude's full attention, reducing errors.
2. **Clarity**: Simpler subtasks mean clearer instructions and outputs.
3. **Traceability**: Easily pinpoint and fix issues in your prompt chain.

***

## When to chain prompts

Use prompt chaining for multi-step tasks like research synthesis, document analysis, or iterative content creation. When a task involves multiple transformations, citations, or instructions, chaining prevents Claude from dropping or mishandling steps. 

**Remember:** Each link in the chain gets Claude's full attention!

<Tip>**Debugging tip**: If Claude misses a step or performs poorly, isolate that step in its own prompt. This lets you fine-tune problematic steps without redoing the entire task.</Tip>

***

## How to chain prompts

1. **Identify subtasks**: Break your task into distinct, sequential steps.
2. **Structure with XML for clear handoffs**: Use XML tags to pass outputs between prompts.
3. **Have a single-task goal**: Each subtask should have a single, clear objective.
4. **Iterate**: Refine subtasks based on Claude's performance.

### Example chained workflows:
- **Multi-step analysis**: See the legal and business examples below.
- **Content creation pipelines**: Research → Outline → Draft → Edit → Format.
- **Data processing**: Extract → Transform → Analyze → Visualize.
- **Decision-making**: Gather info → List options → Analyze each → Recommend.
- **Verification loops**: Generate content → Review → Refine → Re-review.

<Tip>**Optimization tip**: For tasks with independent subtasks (like analyzing multiple docs), create separate prompts and run them in parallel for speed.</Tip>

### Advanced: Self-correction chains

You can chain prompts to have Claude review its own work! This catches errors and refines outputs, especially for high-stakes tasks.

  <section title="Example: Self-correcting research summary">

    #### Prompt 1
    | Role | Content |
    | ---- | ------- |
    | User | Summarize this medical research paper.<br/><br/>\\{\{RESEARCH_PAPER}}\</paper><br/><br/>Focus on methodology, findings, and clinical implications. |
    | Assistant<br/>\{\{SUMMARY}} | Methodology: Double-blind RCT with 500 Type 2 diabetes patients. Group A (n=250) received novel GLP-1/GIP dual agonist; Group B (n=250) received standard GLP-1 agonist. 24-week trial, primary endpoint: HbA1c reduction.<br/><br/>Findings:<br/>- Group A: 1.8% mean HbA1c reduction<br/>- Group B: 1.1% mean HbA1c reduction<br/>- 68% of Group A vs. 52% of Group B achieved HbA1c \<7%<br/>- Group A: 5.2kg mean weight loss<br/>- Group B: 3.1kg mean weight loss<br/><br/>Safety: Similar adverse event profiles, no serious events attributed to treatment.<br/><br/>Clinical Implications: Dual agonist shows superior glycemic control and weight loss compared to standard therapy. Could be a game-changer, especially for obese diabetics. |
    
    #### Prompt 2
    | Role | Content |
    | ---- | ------- |
    | User | Your task is to provide feedback on a research paper summary. Here is a summary of a medical research paper:<br/>\<summary><br/>\{\{SUMMARY\}\}<br/>\</summary><br/><br/>Here is the research paper:<br/>\<br/>\{\{RESEARCH_PAPER\}\}<br/>\</paper><br/><br/>Review this summary for accuracy, clarity, and completeness on a graded A-F scale. |
    | Assistant<br/>\{\{FEEDBACK}} | 1. Accuracy: A<br/>   - Correctly reported key stats: HbA1c reductions, weight loss.<br/>   - Accurately noted safety profile and lack of serious adverse events.<br/>   - Assertion of "game-changer" is justified by significantly better outcomes.<br/><br/>2. Clarity: A-<br/>   - Concise and well-structured with clear sections.<br/>   - Good use of comparative language (e.g., "up 3% from Q1") for context.<br/>   - Minor issue: Acronyms like "RCT," "GLP-1," and "GIP" not defined. Consider spelling out first use.<br/><br/>3. Completeness: B+<br/>   - Covers all requested areas: methodology, findings, clinical implications.<br/>   - Missing: Baseline characteristics of groups (were they well-matched?).<br/>   - Missing: Any secondary endpoints (e.g., blood pressure, lipids).<br/>   - Consider: Long-term implications or need for further research.<br/><br/>Overall, the summary is accurate and clear, providing key insights for a quick grasp of the study. To elevate to A+, define acronyms, mention group baseline stats, note any secondary outcomes, and briefly touch on the need for long-term studies. |
    
     #### Prompt 3
    | Role | Content |
    | ---- | ------- |
    | User | Your task is to improve a paper summary given feedback. Here is the first draft of a medical research paper:<br/>\<summary><br/>\{\{SUMMARY\}\}<br/>\</summary><br/><br/>Here is the research paper:<br/>\<br/>\{\{RESEARCH_PAPER\}\}<br/>\</paper><br/><br/>Here is the feedback:<br/>\<feedback><br/>\{\{FEEDBACK\}\}<br/>\</feedback><br/><br/>Update the summary based on the feedback. |
    | Assistant | Methodology: Double-blind randomized controlled trial (RCT) with 500 Type 2 diabetes patients. Group A (n=250) received a novel glucagon-like peptide-1/glucose-dependent insulinotropic polypeptide (GLP-1/GIP) dual agonist; Group B (n=250) received a standard GLP-1 agonist. The 24-week trial's primary endpoint was HbA1c reduction. Groups were well-matched for age, BMI, and baseline HbA1c.<br/><br/>Findings:<br/>- Group A: 1.8% mean HbA1c reduction<br/>- Group B: 1.1% mean HbA1c reduction<br/>- 68% of Group A vs. 52% of Group B achieved HbA1c \<7%<br/>- Group A: 5.2kg mean weight loss<br/>- Group B: 3.1kg mean weight loss<br/><br/>Secondary endpoints showed improvements in blood pressure and lipid profiles for both groups, with Group A showing slightly better results.<br/><br/>Safety: Similar adverse event profiles, with no serious events attributed to either treatment.<br/><br/>Clinical Implications: The dual GLP-1/GIP agonist demonstrates superior glycemic control and weight loss compared to standard GLP-1 therapy. These results suggest it could be a significant advancement, particularly for obese diabetics. However, longer-term studies are needed to confirm sustained efficacy and safety, as well as to investigate potential benefits on cardiovascular outcomes. |
  
</section>

***

## Examples

  <section title="Example: Analyzing a legal contract (without chaining)">

    Note that Claude misses the instruction to provide proposed changes in its email draft.

    | Role | Content |
    | ---- | ------- |
    | User | You're our Chief Legal Officer. Review this SaaS contract for risks, focusing on data privacy, SLAs, and liability caps.<br/><br/>\<contract><br/>\{\{CONTRACT}}<br/>\</contract><br/><br/>Then draft an email to the vendor with your concerns and proposed changes. |
    | Assistant | After reviewing the SaaS contract, I've identified several concerns:<br/><br/>1. Data Privacy (Section 7):<br/>   - Issue: Vendor has broad rights to use client data for "service improvement."<br/>   - Risk: Could lead to unauthorized data sharing or monetization.<br/><br/>2. SLAs (Section 5):<br/>   - Issue: 99.5% uptime guarantee is below industry standard.<br/>   - Risk: Excessive downtime could impact our operations.<br/><br/>3. Liability (Section 9):<br/>   - Issue: Cap set at 3 months of fees.<br/>   - Risk: Inadequate for potential data breaches or service failures.<br/><br/>Draft email:<br/><br/>Dear \{\{VENDOR}},<br/><br/>After reviewing the SaaS agreement, we have concerns:<br/><br/>1. Data Privacy: We require that our data only be used for direct service provision, not broad "service improvement." Please amend Section 7.<br/><br/>2. SLAs: 99.5% uptime is insufficient. We need 99.99% with clearly defined penalties. Please revise Section 5.<br/><br/>3. Liability: The current cap of 3 months' fees is inadequate. We propose a cap of 12 months' fees, with no cap for data breaches or willful misconduct.<br/><br/>We value our potential partnership and believe these changes will set us up for success. Please send a revised agreement.<br/><br/>Best regards,<br/>\{\{CLO_NAME}} |
  
</section>

  <section title="Example: Analyzing a legal contract (with chaining)">

    #### Prompt 1    
    | Role | Content |
    | ---- | ------- |
    | User | You're our Chief Legal Officer. Review this SaaS contract for risks, focusing on data privacy, SLAs, and liability caps.<br/><br/>\<contract><br/>\{\{CONTRACT}}<br/>\</contract><br/><br/>Output your findings in \<risks> tags. |
    | Assistant<br/>\{\{CONCERNS}} | 1. Data Privacy (Section 7):<br/>   - Issue: Vendor has broad rights to use client data for "service improvement."<br/>   - Risk: Could lead to unauthorized data sharing or monetization of client data.<br/>   - Impact: Potential breach of client trust, regulatory fines (GDPR, CCPA).<br/><br/>2. SLAs (Section 5):<br/>   - Issue: 99.5% uptime guarantee is below industry standard (typically 99.99%).<br/>   - Risk: Up to 43.8 hours of downtime per year vs. 52.6 minutes at 99.99%.<br/>   - Impact: Operational disruptions, revenue loss, client dissatisfaction.<br/><br/>3. Liability (Section 9):<br/>   - Issue: Liability cap set at 3 months of fees.<br/>   - Risk: Inadequate for potential data breaches, IP theft, or prolonged service failures.<br/>   - Impact: Insufficient compensation for damages that could far exceed the cap, like class-action lawsuits or regulatory fines. |
    
    #### Prompt 2    
    | Role | Content |
    | ---- | ------- |
    | User | Draft an email to a SaaS product vendor outlining the following concerns and proposing changes. Here are the concerns:<br/>\<concerns><br/>\{\{CONCERNS\}\}<br/>\</concerns><br/><br/>|
    | Assistant<br/>\{\{EMAIL}} | Dear \{\{VENDOR}},<br/><br/>After a thorough review of the proposed SaaS agreement, our legal team has identified several high-priority concerns that must be addressed before we can proceed:<br/><br/>1. Data Privacy (Section 7):<br/>   - Current: Broad rights to use client data for "service improvement."<br/>   - Concern: Potential unauthorized data sharing or monetization.<br/>   - Proposed Change: Limit data use to direct service provision. Any use for improvement, analytics, or marketing must be opt-in, revocable, and anonymized.<br/><br/>2. SLAs (Section 5):<br/>   - Current: 99.5% uptime guarantee.<br/>   - Concern: Up to 43.8 hours of downtime per year, risking operational disruptions.<br/>   - Proposed Change: 99.99% uptime with tiered service credits. E.g., 10% credit for \<99.99%, 25% for \<99.9%, 50% for \<99.5%.<br/><br/>3. Liability (Section 9):<br/>   - Current: Cap at 3 months of fees.<br/>   - Concern: Grossly inadequate for data breaches, IP theft, or prolonged outages.<br/>   - Proposed Change: 12 months' fees for general liability. Uncapped for data breaches, willful misconduct, IP infringement.<br/><br/>These changes are non-negotiable for us. They align with industry standards and our commitment to data security, operational excellence, and fiduciary responsibility. We value the potential of our partnership, and addressing these will set a strong foundation.<br/><br/>Please have your legal team review and incorporate these changes. We're happy to discuss further to ensure mutual understanding and agreement.<br/><br/>Best regards,<br/>\{\{CLO_NAME}} |
    
    #### Prompt 3    
    | Role | Content |
    | ---- | ------- |
    | User | Your task is to review an email and provide feedback. Here is the email:<br/>\<email><br/>\{\{EMAIL\}\}<br/>\</email><br/><br/>Give feedback on tone, clarity, and professionalism. |
    | Assistant | 1. Tone:<br/>   - Professional and assertive without being confrontational.<br/>   - Use of "non-negotiable" is strong but justified given the criticality of the issues.<br/>   - Collaborative language ("we value," "happy to discuss") balances the firmness, maintaining a constructive tone.<br/><br/>2. Clarity:<br/>   - Excellent structuring: Current state, concern, and proposed change for each issue.<br/>   - Technical terms (e.g., "EBITDA," "tiered service credits") are appropriate for a B2B SaaS context.<br/>   - Action items are clear: vendor's legal team to review and incorporate changes.<br/><br/>3. Professionalism:<br/>   - Focuses on mutual benefit and industry standards, not just our demands.<br/>   - Mentions broader responsibilities (data security, operational excellence, fiduciary duty), elevating the discussion.<br/>   - Offers further discussion, showing commitment to understanding and resolving issues.<br/><br/>Overall, the email strikes the right balance of assertiveness and collaboration. It clearly articulates our concerns, proposes specific solutions, and maintains a professional, partnership-oriented tone. No revisions needed; proceed with sending. |
  
</section>
  <section title="Example: Multitenancy strategy review">

    #### Prompt 1    
    | Role | Content |
    | ---- | ------- |
    | User | As a senior solutions architect, review and analyze this multitenancy strategy for our new enterprise SaaS product.<br/><br/>\<strategy><br/>\{\{STRATEGY}}<br/>\</strategy><br/><br/>Focus on scalability, security, and cost-effectiveness. |
    | Assistant<br/>\{\{ANALYSIS}} | 1. Scalability:<br/>   + Database sharding by tenant reduces contention, supports high growth.<br/>   + Microservices allow independent scaling of components.<br/>   - Shared app servers could bottleneck under extreme load.<br/>   - No mention of auto-scaling or load balancing for app tier.<br/><br/>2. Security:<br/>   + Tenant data isolation via sharding mitigates data leaks.<br/>   + JWT with short expiry and refresh tokens is industry best practice.<br/>   - No mention of encryption (at rest, in transit) or key management.<br/>   - IAM strategy lacks detail on roles, permissions, or RBAC.<br/><br/>3. Cost-effectiveness:<br/>   + Shared app servers reduce idle resource costs.<br/>   + Serverless functions for infrequent tasks optimize costs.<br/>   - Per-tenant DB could increase costs at scale vs. optimized multi-tenant DB.<br/>   - No discussion of reserved instances or spot instances for cost saving. |
    
    #### Prompt 2    
    | Role | Content |
    | ---- | ------- |
    | User | Draft a strategy review document for engineering leadership based on this analysis of a multitenancy strategy.<br/><br/>\<strategy><br/>\{\{STRATEGY}}<br/>\</strategy><br/><br/>\<analysis><br/>\{\{ANALYSIS}}<br/>\</analysis><br/><br/>Include an executive summary, detailed analysis, and recommendations. |
    | Assistant<br/>\{\{STRATEGY_DOC}} | # Multitenancy Strategy Review: SaaS Enterprise Product<br/><br/>## Executive Summary<br/>The proposed strategy demonstrates a solid foundation in scalability and security principles but has gaps in implementation details. It excels in data isolation and component-level scaling but lacks robust app-tier scaling and advanced security measures. Cost optimizations are present but may falter at high scale. With targeted enhancements, this strategy can effectively support our enterprise SaaS ambitions.<br/><br/>## Detailed Analysis<br/><br/>### 1. Scalability: B+<br/><br/>Strengths:<br/>- Database sharding by tenant is excellent. It minimizes query latency, supports high data growth, and facilitates seamless per-tenant scaling.<br/>- Microservices architecture allows scaling individual components based on demand, crucial for handling diverse enterprise workloads.<br/><br/>Weaknesses:<br/>- Shared application servers risk becoming a bottleneck. As tenant count and traffic grow, these could degrade performance across all tenants.<br/>- Absence of auto-scaling and load balancing for the app tier is a critical oversight. These are essential for handling traffic spikes without over-provisioning.<br/><br/>### 2. Security: B-<br/><br/>Strengths:<br/>- Sharded databases provide strong tenant data isolation, mitigating risks of data leaks or unauthorized access between tenants.<br/>- JWT with short expiry and refresh tokens align with OWASP best practices, reducing token vulnerability windows.<br/><br/>Weaknesses:<br/>- No mention of data encryption at rest or in transit (TLS 1.3). This is non-negotiable for enterprise data.<br/>- Key management strategy is missing. How are encryption keys, JWT secrets, and DB credentials managed and rotated?<br/>- IAM lacks depth. We need RBAC with well-defined roles, attribute-based access control (ABAC) for fine-grained permissions, and integration with enterprise identity providers (SAML, OIDC).<br/><br/>### 3. Cost-effectiveness: B<br/><br/>Strengths:<br/>- Shared app servers reduce idle capacity costs, good for steady-state traffic.<br/>- Serverless for infrequent tasks (e.g., reporting) is smart; pay only when these resources are used.<br/><br/>Weaknesses:<br/>- Per-tenant databases may not be cost-effective at scale compared to a well-designed multi-tenant database with robust data partitioning.<br/>- No mention of cost-saving measures like reserved instances for predictable workloads or spot instances for fault-tolerant tasks.<br/>- Lack of app-tier auto-scaling could lead to over-provisioning, increasing costs.<br/><br/>## Recommendations<br/><br/>1. **App Tier Resilience**: Implement auto-scaling with Kubernetes or cloud-native services (EKS, GKE). Deploy across availability zones with a CDN for static assets.<br/><br/>2. **Security Hardening**:<br/>   a. Encrypt data at rest (AES-256) and in transit (TLS 1.3).<br/>   b. Use a managed KMS (AWS KMS, GCP KMS) for key management.<br/>   c. Enhance IAM with RBAC, ABAC, and SAML/OIDC for enterprise SSO.<br/><br/>3. **Cost Optimization**:<br/>   a. Evaluate columnar multi-tenant DB (e.g., Snowflake) vs. sharding at scale.<br/>   b. Use reserved instances for app servers, spot instances for non-critical workloads.<br/>   c. Implement proactive monitoring and right-sizing to avoid overprovisioning.<br/><br/>4. **Proof of Concept (PoC)**: Before full implementation, conduct a PoC with a high-scale simulation:<br/>   a. Test sharded DB vs. optimized multi-tenant DB for cost and performance.<br/>   b. Stress-test app tier with simulated enterprise-level traffic spikes.<br/>   c. Conduct third-party security audit, focusing on data isolation and access controls.<br/><br/>With these enhancements, our multi-tenancy strategy will be enterprise-grade: scalable, secure, and cost-effective. The PoC will validate our design choices and instill confidence in our enterprise clients. |
    
    #### Prompt 3    
    | Role | Content |
    | ---- | ------- |
    | User | Grade this strategy review document for clarity, actionability, and alignment with enterprise priorities. <br/><br/>\<br/>\{\{PRIORITIES}}<br/>\</priorities><br/><br/>\<strategy_doc><br/>\{\{STRATEGY_DOC}}<br/>\</strategy_doc> |
    | Assistant | 1. Clarity: A<br/>   + Clear structure with Executive Summary, Detailed Analysis, and Recommendations.<br/>   + Analysis uses a grading system (B+, B-) for quick grasp of strengths/weaknesses.<br/>   + Technical terms (RBAC, ABAC, TLS) are explained or contextualized, aiding non-technical leadership.<br/>   + Visual aids (bullet points, indentation) enhance readability.<br/><br/>2. Actionability: A-<br/>   + Recommendations are specific and technical (e.g., "Implement auto-scaling with Kubernetes").<br/>   + PoC plan with clear objectives provides a roadmap.<br/>   + Missing: Timelines, resource requirements, or team assignments for each recommendation.<br/>   + Consider: Add a "Next Steps" section with immediate actions, roles, and a high-level timeline.<br/><br/>3. Enterprise Alignment: A+<br/>   + Directly addresses enterprise priorities:<br/>     - Scalability: Discusses handling enterprise-level traffic spikes.<br/>     - Security: Focuses on data isolation, encryption, and enterprise IAM.<br/>     - Cost: Strategies align with enterprise FinOps (reserved instances, right-sizing).<br/>   + PoC with "high-scale simulation" and security audit shows commitment to enterprise-grade quality.<br/>   + Language resonates with enterprise concerns: "unacceptable risk," "enterprise-grade," "instill confidence."<br/><br/>Overall, the document excels in clarity and enterprise alignment. The actionability is strong but could be elevated to A+ with a "Next Steps" section. The technical depth, coupled with clear explanations, makes this highly effective for both technical and non-technical leadership. Great work! |
  
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