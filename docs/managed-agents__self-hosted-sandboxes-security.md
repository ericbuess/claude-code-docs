# Security model

Shared responsibility model for self-hosted sandbox environments.

---

Anthropic secures the control plane across all environments: session and work queue integrity, multi-tenant isolation, and agent-context minimization. When you self-host, the following responsibilities fall to you.

## What you own

* **Sandbox image quality and runtime hardening.** Anthropic does not inspect or verify your sandbox image. Follow best practices such as dropping unnecessary Linux capabilities, running as a non-root user, and using a read-only root filesystem.
* **Network egress controls.** Your sandbox's network access is determined by your VPC and firewall rules. Without egress restrictions, a compromised tool execution can reach arbitrary external hosts. Restrict outbound traffic to only the endpoints your tools require.
* **Service key storage and rotation.** The environment service key (`ANTHROPIC_ENVIRONMENT_KEY`) authorizes polling your environment's work queue and submitting results back to sessions. Store it in a secrets manager, not in environment files or sandbox images. Rotate it immediately if you suspect exposure.
* **Isolating untrusted workloads.** The environment service key is scoped to one environment's work queue. If you run untrusted code inside your sandbox, consider provisioning a separate workspace and environment for each trust boundary. This limits each key to a single user's sessions instead of a shared pool.
* **Tool-execution blast radius.** Tools run inside your sandbox with whatever permissions your process has. Apply least privilege to the process user and mount only the directories your tools require.
* **Log retention and session content.** Conversation content and tool outputs pass through your worker and stay in your environment. You are responsible for retaining, redacting, or deleting that data in compliance with your own policies. Anthropic has no visibility into what your worker does with session content once delivered.

## What Anthropic cannot do for you

* **Instantly invalidate a leaked key.** Anthropic can detect anomalous usage patterns, but cannot instantly invalidate a key. Treat `ANTHROPIC_ENVIRONMENT_KEY` like a database password: rotate it immediately if compromised.
* **Verify your worker build.** Anthropic does not inspect your sandbox image or runtime. A supply-chain compromise in your image is not detectable from the control plane.
* **Isolate tools inside your sandbox.** Anthropic's security boundary stops at the sandbox. How you isolate individual tool executions from each other inside that boundary is entirely your responsibility.
* **Enforce data retention in your environment.** Once session content reaches your worker, it is outside Anthropic's data lifecycle controls.
