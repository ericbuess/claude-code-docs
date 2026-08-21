---
title: Security model
url: https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security
description: Shared responsibility model for self-hosted sandbox environments.
---

Anthropic secures the control plane across all environments: session and work queue integrity, multitenant isolation, and agent-context minimization. When you self-host, the following responsibilities fall to you.

## What you own

* **Sandbox image quality and runtime hardening.** Anthropic does not inspect or verify your sandbox image. Follow best practices such as dropping unnecessary Linux capabilities, running as a non-root user, and using a read-only root filesystem.
* **Network egress controls.** Your sandbox's network access is determined by your VPC and firewall rules. Without egress restrictions, a compromised tool execution can reach arbitrary external hosts. Restrict outbound traffic to only the endpoints your tools require.
* **Service key storage and rotation.** The environment service key (`ANTHROPIC_ENVIRONMENT_KEY`) authorizes polling your environment's work queue and submitting results back to sessions. Store it in a secrets manager, not in environment files or sandbox images. Rotate it immediately if you suspect exposure.
* **Isolating untrusted workloads.** The environment service key is scoped to one environment's work queue. If you run untrusted code inside your sandbox, consider provisioning a separate workspace and environment for each trust boundary. This limits each key to a single user's sessions instead of a shared pool.
* **Per-session credentials.** Each work item your worker claims can carry a per-session `secret`, which the SDK worker uses in place of the environment service key. Access to [memory stores](https://platform.claude.com/docs/en/managed-agents/memory) requires the `secret`: the memory store endpoints reject the environment key (see [Use memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores)). Pass the `secret` only into the sandbox that serves that session, keep it out of images and shared volumes, and never log it.
* **Tool-execution blast radius.** Tools run inside your sandbox with whatever permissions your process has. Apply least privilege to the process user and mount only the directories your tools require.
* **Log retention and session content.** Conversation content and tool outputs pass through your worker and stay in your environment. You are responsible for retaining, redacting, or deleting that data in compliance with your own policies. Anthropic has no visibility into what your worker does with session content once delivered.
* **Memory store contents.** [Memory stores](https://platform.claude.com/docs/en/managed-agents/memory) remain hosted by Anthropic, including their version history. When a session attaches one, the worker keeps a working copy under `/mnt/memory/` in your sandbox for the session's duration and syncs changes back. The worker deletes that copy when the session ends, but a worker that exits without running its teardown leaves it behind. Cleaning up leftover copies, the permissions on that path, and isolation between sessions that share a filesystem are your responsibility.
* **Read-only memory stores.** A store attached with `read_only` access is protected from upload, not from local modification. The worker's `write` and `edit` tools refuse to write under its directory, nothing there syncs back, and the memory store endpoints reject writes to it made with the session's `secret`. Other processes in the sandbox, including commands the agent runs through the `bash` tool, can still change the local copy, and later tool calls in that session read the changed copy until that memory next changes in the store. If the agent must not be able to alter even its local view of such a store, disable the `bash` tool for that agent.

## What Anthropic cannot do for you

* **Know that your key leaked.** Anthropic can detect anomalous usage patterns, but cannot know your key was compromised. If you suspect `ANTHROPIC_ENVIRONMENT_KEY` leaked, revoke it and generate a replacement immediately. Revocation is validated on every request, so it takes effect on the worker's next call.
* **Verify your worker build.** Anthropic does not inspect your sandbox image or runtime. A supply-chain compromise in your image is not detectable from the control plane.
* **Isolate tools inside your sandbox.** Anthropic's security boundary stops at the sandbox. How you isolate individual tool executions from each other inside that boundary is entirely your responsibility.
* **Enforce data retention in your environment.** Once session content reaches your worker, it is outside Anthropic's data lifecycle controls.
