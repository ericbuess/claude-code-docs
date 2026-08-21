---
title: Configure Inference hooks
url: https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration
description: Allow Inference hooks for your Claude Enterprise organization, connect your AI security server, and control enforcement, failure handling, and rollout.
---

<Note>
  Inference hooks are in beta and available to Claude Enterprise organizations. Configuring them requires the `organization:manage` permission, which the built-in Admin, Owner, and Primary owner roles hold, as does any custom role granted it.
</Note>

Inference hooks send prompts from your organization to an AI security server you choose, and hold each request for an allow or deny verdict before Claude processes it. This page walks through turning the feature on, connecting your server, and controlling enforcement. For what Inference hooks are and when to use them, see the [Inference hooks overview](https://platform.claude.com/docs/en/manage-claude/inference-hooks). For building the AI security server itself, see [Develop an Inference hooks integration](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint).

## Before you begin

You need:

* The `organization:manage` permission in claude.ai. The built-in **Admin**, **Owner**, and **Primary owner** roles hold it, as does any custom role it has been granted.
* An AI security server HTTPS endpoint that accepts verdict requests: an `https://` URL on port 443, on a publicly routable host, reachable without redirects. Reverse-tunnel hosts (ngrok and similar tunnel services) are not supported: Anthropic's network policy blocks them. Don't test through a tunnel; host your server on a domain you control. For the full [hosting requirements](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#receive-a-request), and to build the server and verify signed requests, see [Develop an Inference hooks integration](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint).

## Set up Inference hooks

There are three enforcement states: **off** (**Enforce verdicts** is off: your AI security server is never contacted and prompts are not inspected), **shadow** (**Enforce verdicts** is on with **Mode** set to **Shadow mode**: your AI security server receives prompts and returns verdicts, and nothing is blocked), and **enforcing** (**Enforce verdicts** is on with **Mode** set to **Allow the request** or **Block the request**: a deny blocks the request). The following steps take a new configuration from off to enforcing.

<Steps>
  <Step title="Allow Inference hooks for your organization">
    Go to claude.ai > **Organization settings** > **Data and privacy** and find the **Inference hooks** section. Turn on **Allow for your organization**.

    Turning this on unlocks the Inference hooks settings page and always forces **Enforce verdicts** off, so allowing the feature never starts inspection by itself: even a configuration that previously had enforcement on stays uninspected until you turn **Enforce verdicts** back on in the final step.
  </Step>

  <Step title="Open the Inference hooks settings page">
    Still in **Data and privacy**, open the **Inference hooks** section to reach the Inference hooks settings page. It lives under Data and privacy rather than as its own entry in the settings nav, so its breadcrumb reads **Data and privacy / Inference hooks**. Until you save an endpoint, the page warns that prompts aren't being inspected yet, and **Enforce verdicts** stays off with a **Requires endpoint** badge.
  </Step>

  <Step title="Configure your endpoint">
    Click **Configure** to open the **Configure endpoint** dialog and fill in:

    * **Endpoint URL:** the `https://` URL that receives verdict requests. Only `https://` URLs are accepted.
    * **Custom request headers:** up to 16 static headers sent with every verdict request so your AI security server can authenticate the caller. Header values are stored encrypted and never shown again; after saving, only the header names are displayed. Because values are write-only, saving any change to the headers requires re-entering every value. Changing the endpoint URL clears all stored header values so your credentials are never sent to a new destination; re-enter them after a URL change. Header names must use standard HTTP token characters with `-` rather than `_`, and must not collide with reserved names (request-framing headers such as `Content-*` and `Host`, proxy and cookie headers, client-address headers such as `X-Forwarded-*`, the `webhook-*` signature headers, and the `X-Anthropic-*` prefix). Values must be printable ASCII.

    The dialog covers only those two fields plus **Test connection**; it doesn't ask about failure handling, which you choose in step 6. Once an endpoint is saved, the button reads **Edit**.
  </Step>

  <Step title="Test the connection">
    Click **Test connection**. Claude sends a synthetic test prompt to the URL and headers currently in the form, not the saved values, so re-enter any stored header values before testing. On success, the result reports whether your AI security server returned an allow or a deny verdict for the test prompt, which surfaces a deny-everything default before you start enforcing.

    Common failure results:

    | Result                 | What to check                                                                                                                                         |
    | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
    | URL rejected           | The URL failed a structural check. Use an `https://` URL on port 443.                                                                                 |
    | Private or internal IP | The host resolves to a private or internal address. Use a publicly routable host.                                                                     |
    | Timeout                | The AI security server did not return a verdict within the timeout.                                                                                   |
    | Transport error        | DNS resolution, the TLS handshake, or the connection failed.                                                                                          |
    | Non-200 status         | The AI security server responded with a status other than 200. Verdicts must come back as HTTP 200; redirects are not followed and count as failures. |
    | Unparseable response   | The AI security server responded, but the body is not a valid verdict.                                                                                |
  </Step>

  <Step title="Save and store your signing secret">
    Save the endpoint configuration. The first save generates your webhook signing secret and reveals it once. Copy it and store it securely before closing the dialog: the secret cannot be retrieved later, only [rotated](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration#rotate-your-signing-secret).

    Your AI security server uses this secret to verify the signature on every request it receives. For the verification procedure, see [Verify the signature](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#verify-the-signature).
  </Step>

  <Step title="Choose failure handling and timeout">
    Under **Failure handling**, set **Mode** to choose what happens while the AI security server is unreachable or verdicts time out:

    * **Block the request:** stop inference when your AI security server can't deliver a verdict (fail closed).
    * **Allow the request:** let the request proceed to the model without inspection (fail open).

    The dropdown's third option, **Shadow mode**, is a rollout tool rather than a failure policy; see [Shadow mode](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration#shadow-mode).

    Then set **Prompt verdict timeout (ms)**: 1 to 10,000ms, with a default of 5,000ms. The budget covers the entire exchange, and a slower verdict counts as an unreachable server, so set the lowest value your server can reliably meet.

    Changes in this section save as you make them. On first save, the defaults are **Allow the request** and 5,000ms.
  </Step>

  <Step title="Choose a rollout percentage">
    Under **Rollout**, set **Requests inspected (%)** to run inspection on a percentage of requests while you bring your AI security server up. The value ranges from 0 to 100: 100 inspects everything, and 0 turns inspection off.

    Each request rolls once for its whole conversation turn, so a single conversation can be partially inspected across turns. Requests outside the sampled percentage proceed without inspection, even when failure handling is set to **Block the request**.
  </Step>

  <Step title="Turn on Enforce verdicts">
    To evaluate verdicts against live traffic without blocking anyone at first, set **Mode** to **Shadow mode** (step 6) before turning on enforcement; see [Shadow mode](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration#shadow-mode).

    Turn on **Enforce verdicts** to gate Claude on your AI security server's verdict for every governed prompt, then confirm in the dialog, which restates your failure handling choice. Allow about a minute for the change to reach every Anthropic server; requests already in flight finish under the old setting. Turning it off stops prompts from being sent to your AI security server, again within about a minute; your configuration is kept.
  </Step>
</Steps>

## Shadow mode

Shadow mode runs your hook against live traffic without blocking anything. Your AI security server receives governed prompts and returns verdicts exactly as it would when enforcing, but nothing is blocked: every request proceeds to the model, even when your server denies it or can't be reached, and the end user sees nothing. Use it to tune your policy against your organization's real traffic before you start enforcing.

To use shadow mode, set **Mode** to **Shadow mode** under **Failure handling**, then turn on **Enforce verdicts** so prompts flow to your AI security server. While it is active, the settings page shows a **Shadow mode — not blocking** badge. To leave shadow mode, set **Mode** back to **Allow the request** or **Block the request**; verdicts are enforced again once enforcement is on.

## Exclusions

Under **Exclusions**, select roles whose members are not covered by Inference hooks: their prompts are never sent to your AI security server. Only custom roles your organization created can be excluded; the built-in roles aren't offered. Pick them in the role selector, whose placeholder reads **Select roles to exclude**, and manage who holds each role from the roles admin page (**Manage roles**); changing exclusions requires identity management permission. The list is empty by default, and with no roles excluded, every governed request is inspected.

Exclusion applies to a user's interactive sessions; traffic authenticated by machine credentials is always inspected. If Claude can't resolve a requester's role membership, the request fails closed with a retryable error rather than proceeding uninspected. Changes to the exclusion list are recorded in the audit trail.

## Custom blocked prompt message

Under **Custom blocked prompt message**, set custom text of up to 500 characters that is appended to the error an end user sees when your AI security server denies a request (typically who to contact or where to request an exception). The final message is your AI security server's per-request `deny_reason` (when present), a blank line, then this text. With no custom text configured, a built-in default directs the user to contact their administrators; you can also switch the appended message off entirely so the user sees only the `deny_reason`.

## Monitor your AI security server

The endpoint health area of the Inference hooks settings page shows:

* **Endpoint status:** Healthy, Tripped, Not enforcing, or Not configured before an endpoint is saved.
* **Failures per minute:** webhook failures over the last two minutes, averaged.
* **Block rate:** denials as a share of your AI security server's verdicts, shown while the rollout percentage is below 100.
* **Circuit breaker tripped:** when the breaker last tripped, if it has.
* **Recent errors:** each entry is reduced to a timestamp, an error type, and a one-line reason. Entries never include request content or your endpoint URL.

The panel is best-effort: if Anthropic cannot read the counters it shows zero failures and no errors rather than an error of its own, so a healthy-looking panel is not by itself proof that your AI security server is healthy. **Failures per minute** counts every failure, including the network and DNS errors that never trip the circuit breaker, so it can be high while **Circuit breaker tripped** stays empty.

## Circuit breaker

Sustained webhook failures attributable to your AI security server trip the circuit breaker, which stops enforcement: your server is no longer contacted, and your **Failure handling** choice applies to every inspected request. With **Block the request** selected, users in your organization are blocked until you act. When the breaker trips, administrators are also notified in the claude.ai notification center.

To recover, fix the server, then turn **Enforce verdicts** back on to reset the breaker.

## Rotate your signing secret

Click **Rotate secret** under **Request signing** to replace your signing secret. Rotation is an immediate cutover: the new secret is generated and revealed once, the old secret can no longer be retrieved, and no request is ever signed with both secrets, so there is no overlap period to rely on.

Requests signed with the previous secret can still arrive briefly after rotation; [Verify the signature](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#verify-the-signature) covers how your AI security server should handle the switchover.

## Audit trail

Inference hooks activity is recorded in your organization's [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed): configuration changes, denials, and requests that proceeded without inspection under your failure handling setting. Denial records carry identifiers that let you join each denial to the matching record in your own system.

## Turn Inference hooks off

There are two levels of off:

* **Enforce verdicts** off, on the Inference hooks settings page: within about a minute, prompts from your organization stop being sent to your AI security server; requests already in flight finish under the old setting. The settings page stays available, so use this to pause enforcement while you work on your AI security server.
* **Allow for your organization** off, in **Data and privacy** settings: prompts are no longer inspected, and the Inference hooks settings become unavailable until you turn it back on. Your endpoint configuration, custom headers, and signing secret are kept either way; turning it back on forces **Enforce verdicts** off, so turn enforcement on again when you are ready.

## Next steps

<CardGroup cols={2}>
  <Card title="Develop an Inference hooks integration" href="https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint">
    Build the AI security server: the request and verdict schemas, signature verification, and operational semantics.
  </Card>

  <Card title="Inference hooks overview" href="https://platform.claude.com/docs/en/manage-claude/inference-hooks">
    What Inference hooks are, how the verdict round trip works, and what gets sent to your AI security server.
  </Card>
</CardGroup>
