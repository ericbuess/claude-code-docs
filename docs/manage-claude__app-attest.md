---
title: App Attest for iOS and macOS apps
url: https://platform.claude.com/docs/en/manage-claude/app-attest
description: Let genuine installations of your iOS or macOS app call the Claude API without shipping an API key or running a proxy, using Apple's App Attest service.
---

App Attest authenticates iOS and macOS apps that call the Claude API directly from the device, with usage billed to your workspace. This page explains how App Attest works, how to register your app in the Claude Console, and how to revoke an app integration.

Apps use App Attest through the [Claude for Foundation Models](https://github.com/anthropics/ClaudeForFoundationModels) Swift package, which is in beta: it requires the OS 27 betas, and APIs might change before general availability. For the Swift configuration, see [Apple Foundation Models](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production).

## How App Attest works

Each installation of your app uses Apple's [App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity) service to prove that it is a genuine, unmodified build of the app you registered. Anthropic then issues the device a short-lived access token that bills usage to your workspace. The app ships no API key, and there is no proxy for you to operate.

App Attest authentication is available only when your app calls the Claude API directly. It is not available through Amazon Bedrock, Google Cloud, or Microsoft Foundry.

The first time your app uses Claude on a device, the app requests a challenge from Anthropic, attests the device with Apple's `DCAppAttestService`, and exchanges the verified attestation for an access token. The Claude for Foundation Models package runs this flow automatically and requests new tokens as they expire; there is no attestation code for you to write.

Tokens are scoped to your workspace, expire after one hour, and authorize only [Messages API](https://platform.claude.com/docs/en/api/messages/create) calls. They carry no end-user identity: App Attest identifies your app, not the person using it, so handle any per-user logic in your app.

## Set up App Attest

<Note>
  App Attest requires a physical device. The Simulator, and hardware without a Secure Enclave, cannot perform App Attest. While developing in the Simulator, authenticate with an [API key](https://platform.claude.com/docs/en/manage-claude/authentication#api-keys) instead.
</Note>

To set up App Attest, you need your Apple Developer Team ID and the admin, owner, or primary owner role in your organization. Configure your Xcode project and register your app in the [Claude Console](https://platform.claude.com/):

1. In Xcode, add the **App Attest** capability to your app target under **Signing & Capabilities**.
2. In your workspace's settings in the Claude Console, open **App integrations**.
3. Click **Create app integration** and enter a name, your Apple Developer Team ID, and one or more bundle IDs (up to 32).
4. Copy the client ID (`clid_...`) from the integration's **Overview** tab and pass it to your app's Claude configuration.

## Revoke an app integration

To stop a compromised or retired app, revoke its integration: in your workspace's settings in the Claude Console, open **App integrations**, select the integration, and click **Revoke**, then confirm. Revoking an integration revokes its outstanding tokens, and its registered devices can no longer request new ones. Revocation is permanent, so create a new app integration to restore access.

## Next steps

<CardGroup cols={2}>
  <Card title="Apple Foundation Models" icon="code" href="https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production">
    Configure App Attest in the Claude for Foundation Models Swift package
  </Card>

  <Card title="Authentication" icon="lock" href="https://platform.claude.com/docs/en/manage-claude/authentication">
    Compare API keys, Workload Identity Federation, and App Attest
  </Card>
</CardGroup>
