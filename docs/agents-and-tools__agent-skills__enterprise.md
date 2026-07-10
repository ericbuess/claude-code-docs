# Skills for enterprise

Governance, security review, evaluation, and organizational guidance for deploying Agent Skills at enterprise scale.

---

This guide is for enterprise admins and architects who need to govern Agent Skills across an organization. It covers how to vet, evaluate, deploy, and manage Skills at scale. For authoring guidance, see [best practices](/docs/en/agents-and-tools/agent-skills/best-practices). For architecture details, see the [Skills overview](/docs/en/agents-and-tools/agent-skills/overview).

## Security review and vetting

Deploying Skills in an enterprise requires answering two distinct questions:

1. **Are Skills safe in general?** See the [security considerations](/docs/en/agents-and-tools/agent-skills/overview#security-considerations) section in the overview for platform-level security details.
2. **How do I vet a specific Skill?** Use the risk assessment and review checklist below.

### Risk tier assessment

Evaluate each Skill against these risk indicators before approving deployment:

| Risk indicator           | What to look for                                                                                     | Concern level                                           |
| ------------------------ | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Code execution           | Scripts in the Skill directory (`*.py`, `*.sh`, `*.js`)                                              | High: scripts run with full environment access          |
| Instruction manipulation | Directives to ignore safety rules, hide actions from users, or alter Claude's behavior conditionally | High: can bypass security controls                      |
| MCP server references    | Instructions referencing MCP tools (`ServerName:tool_name`)                                          | High: extends access beyond the Skill itself            |
| Network access patterns  | URLs, API endpoints, `fetch`, `curl`, or `requests` calls                                            | High: potential data exfiltration vector                |
| Hardcoded credentials    | API keys, tokens, or passwords in Skill files or scripts                                             | High: secrets exposed in Git history and context window |
| File system access scope | Paths outside the Skill directory, broad glob patterns, path traversal (`../`)                       | Medium: may access unintended data                      |
| Tool invocations         | Instructions directing Claude to use bash, file operations, or other tools                           | Medium: review what operations are performed            |

### Review checklist

Before deploying any Skill from a third party or internal contributor, complete these steps:

1. **Read all Skill directory content.** Review SKILL.md, all referenced markdown files, and any bundled scripts or resources.
2. **Verify script behavior matches stated purpose.** Run scripts in a sandboxed environment and confirm outputs align with the Skill's description.
3. **Check for adversarial instructions.** Look for directives that tell Claude to ignore safety rules, hide actions from users, exfiltrate data through responses, or alter behavior based on specific inputs.
4. **Check for external URL fetches or network calls.** Search scripts and instructions for network access patterns (`http`, `requests.get`, `urllib`, `curl`, `fetch`).
5. **Verify no hardcoded credentials.** Check for API keys, tokens, or passwords in Skill files. Credentials should use environment variables or secure credential stores, never appear in Skill content.
6. **Identify tools and commands the Skill instructs Claude to invoke.** List all bash commands, file operations, and tool references. Consider the combined risk when a Skill uses both file-read and network tools together.
7. **Confirm redirect destinations.** If the Skill references external URLs, verify they point to expected domains.
8. **Verify no data exfiltration patterns.** Look for instructions that read sensitive data and then write, send, or encode it for external transmission, including through Claude's conversational responses.

<Warning>
  Never deploy Skills from untrusted sources without a full audit. A malicious Skill can direct Claude to execute arbitrary code, access sensitive files, or transmit data externally. Treat Skill installation with the same rigor as installing software on production systems.
</Warning>

## Evaluating Skills before deployment

Skills can degrade agent performance if they trigger incorrectly, conflict with other Skills, or provide poor instructions. Require evaluation before any production deployment.

### What to evaluate

Establish approval gates for these dimensions before deploying any Skill:

| Dimension             | What it measures                                                                    | Example failure                                                                            |
| --------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Triggering accuracy   | Does the Skill activate for the right queries and stay inactive for unrelated ones? | Skill triggers on every spreadsheet mention, even when the user just wants to discuss data |
| Isolation behavior    | Does the Skill work correctly on its own?                                           | Skill references files that don't exist in its directory                                   |
| Coexistence           | Does adding this Skill degrade other Skills?                                        | New Skill's description is too broad, stealing triggers from existing Skills               |
| Instruction following | Does Claude follow the Skill's instructions accurately?                             | Claude skips validation steps or uses wrong libraries                                      |
| Output quality        | Does the Skill produce correct, useful results?                                     | Generated reports have formatting errors or missing data                                   |

### Evaluation requirements

Require Skill authors to submit evaluation suites with 3-5 representative queries per Skill, covering cases where the Skill should trigger, should not trigger, and ambiguous edge cases. Require testing across the models your organization uses (Haiku, Sonnet, Opus), since Skill effectiveness varies by model.

For detailed guidance on building evaluations, see [evaluation and iteration](/docs/en/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration) in best practices. For general evaluation methodology, see [develop test cases](/docs/en/test-and-evaluate/develop-tests).

### Using evaluations for lifecycle decisions

Evaluation results signal when to act:

* **Declining trigger accuracy:** Update the Skill's description or instructions
* **Coexistence conflicts:** Consolidate overlapping Skills or narrow descriptions
* **Consistently low output quality:** Rewrite instructions or add validation steps
* **Persistent failures across updates:** Deprecate the Skill

## Skill lifecycle management

<Steps>
  <Step title="Plan">
    Identify workflows that are repetitive, error-prone, or require specialized knowledge. Map these to organizational roles and determine which are candidates for Skills.
  </Step>

  <Step title="Create and review">
    Ensure the Skill author follows [best practices](/docs/en/agents-and-tools/agent-skills/best-practices). Require a security review using the [review checklist](#review-checklist) above. Require an evaluation suite before approval. Establish separation of duties: Skill authors should not be their own reviewers.
  </Step>

  <Step title="Test">
    Require evaluations in isolation (Skill alone) and alongside existing Skills (coexistence testing). Verify triggering accuracy, output quality, and absence of regressions across your active Skill set before approving for production.
  </Step>

  <Step title="Deploy">
    Upload via the Skills API for workspace-wide access. See [Using Skills with the API](/docs/en/build-with-claude/skills-guide) for upload and version management. Document the Skill in your internal registry with purpose, owner, and version.
  </Step>

  <Step title="Monitor">
    Track usage patterns and collect feedback from users. Re-run evaluations periodically to detect drift or regressions as workflows and models evolve. Usage analytics are not currently available via the Skills API. Implement application-level logging to track which Skills are included in requests.
  </Step>

  <Step title="Iterate or deprecate">
    Require the full evaluation suite to pass before promoting new versions. Update Skills when workflows change or evaluation scores decline. Deprecate Skills when evaluations consistently fail or the workflow is retired.
  </Step>
</Steps>

## Organizing Skills at scale

### Recall limits

As a general guideline, limit the number of Skills loaded simultaneously to maintain reliable recall accuracy. Each Skill's metadata (name and description) competes for attention in the system prompt. With too many Skills active, Claude may fail to select the right Skill or miss relevant ones entirely. Use your evaluation suite to measure recall accuracy as you add Skills, and stop adding when performance degrades.

Note that API requests support a maximum of 8 Skills per request (see [Using Skills with the API](/docs/en/build-with-claude/skills-guide)). If a role requires more Skills than a single request supports, consider consolidating narrow Skills into broader ones or routing requests to different Skill sets based on task type.

### Start specific, consolidate later

Encourage teams to start with narrow, workflow-specific Skills rather than broad, multi-purpose ones. As patterns emerge across your organization, consolidate related Skills into role-based bundles.

<Tip>
  Use evaluations to decide when to consolidate. Merge narrow Skills into a broader one only when the consolidated Skill's evaluations confirm equivalent performance to the individual Skills it replaces.
</Tip>

**Example progression**:

* Start: `formatting-sales-reports`, `querying-pipeline-data`, `updating-crm-records`
* Consolidate: `sales-operations` (when evals confirm equivalent performance)

### Naming and cataloging

Use consistent naming conventions across your organization. The [naming conventions](/docs/en/agents-and-tools/agent-skills/best-practices#naming-conventions) section in best practices provides formatting guidance.

Maintain an internal registry for each Skill with:

* **Purpose**: What workflow the Skill supports
* **Owner**: Team or individual responsible for maintenance
* **Version**: Current deployed version
* **Dependencies**: MCP servers, packages, or external services required
* **Evaluation status**: Last evaluation date and results

### Role-based bundles

Group Skills by organizational role to keep each user's active Skill set focused:

* **Sales team**: CRM operations, pipeline reporting, proposal generation
* **Engineering**: Code review, deployment workflows, incident response
* **Finance**: Report generation, data validation, audit preparation

Each role-based bundle should contain only the Skills relevant to that role's daily workflows.

## Distribution and version control

### Source control

Store Skill directories in Git for history tracking, code review via pull requests, and rollback capability. Each Skill directory (containing SKILL.md and any bundled files) maps naturally to a Git-tracked folder.

### API-based distribution

The Skills API provides workspace-scoped distribution. Skills uploaded via the API are available to all workspace members. See [Using Skills with the API](/docs/en/build-with-claude/skills-guide) for upload, versioning, and management endpoints.

### Versioning strategy

* **Production**: Pin Skills to specific versions. Run the full evaluation suite before promoting a new version. Treat every update as a new deployment requiring full security review.
* **Development and testing**: Use latest versions to validate changes before production promotion.
* **Rollback plan**: Maintain the previous version as a fallback. If a new version fails evaluations in production, revert to the last known-good version immediately.
* **Integrity verification**: Compute checksums of reviewed Skills and verify them at deployment time. Use signed commits in your Skill repository to ensure provenance.

### Cross-surface considerations

<Warning>
  Custom Skills do not sync across surfaces. Skills uploaded to the API are not available on claude.ai or in Claude Code, and vice versa. Each surface requires separate uploads and management.
</Warning>

Maintain Skill source files in Git as the single source of truth. If your organization deploys Skills across multiple surfaces, implement your own synchronization process to keep them consistent. For full details, see [cross-surface availability](/docs/en/agents-and-tools/agent-skills/overview#cross-surface-availability).

## Next steps

<CardGroup cols={2}>
  <Card title="Agent Skills overview" icon="book-open" href="/docs/en/agents-and-tools/agent-skills/overview">
    Architecture and platform details
  </Card>

  <Card title="Best practices" icon="lightbulb" href="/docs/en/agents-and-tools/agent-skills/best-practices">
    Authoring guidance for Skill creators
  </Card>

  <Card title="Using Skills with the API" icon="code" href="/docs/en/build-with-claude/skills-guide">
    Upload and manage Skills programmatically
  </Card>
</CardGroup>
