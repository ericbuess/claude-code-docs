> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Verify session identity in self-hosted environments

> Verify the CLAUDE_CODE_SESSION_ACCESS_TOKEN JWT so services on your network can trust requests from sessions in your self-hosted environment.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; an [Owner or admin](/docs/en/cloud-environments#organization-shared-environments) enables them by turning on **Allow self-hosted environments** on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments). This page covers session identity verification; see the [quickstart](/docs/en/self-hosted-environments-quickstart) for setup and [Deploy to production](/docs/en/self-hosted-environments-deploy) for the fleet recipes.
</Note>

A [self-hosted environment](/docs/en/self-hosted-environments) lets [Claude Code on the web](/docs/en/claude-code-on-the-web) sessions run on infrastructure you operate instead of on Anthropic's. Because the session runs inside your network, Claude can call your internal services directly. Those services need a way to confirm that a request really came from a Claude Code session in your environment, and to identify which user created that session.

Every session in a self-hosted environment receives a signed JSON Web Token (JWT) in the `CLAUDE_CODE_SESSION_ACCESS_TOKEN` environment variable. A session presents the token like any bearer credential; for example, a script Claude runs can call your service with `curl -H "Authorization: Bearer $CLAUDE_CODE_SESSION_ACCESS_TOKEN"`. Anthropic signs the token and publishes the verification keys at a public JWKS endpoint. Your services fetch those keys, verify the signature, and read the claims to decide what access to grant.

## The session token

Before you write verification code, know what the token establishes and the shape your JWT library will see.

### What the token proves

A valid token establishes some facts and deliberately not others:

* **Proves**: Anthropic issued the token for a specific session in a specific environment, and how the session was created: by a user in your organization, or with an organization service key
* **Doesn't prove**: which process on the runner host presents it. The token sits in an environment variable inside the session, so any code Claude runs, and any tool or MCP server the session starts, can read and present it.

Two consequences for your services:

* Verify the `aud` claim against your environment ID, the `ccpool_...` value shown with your environment on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments), to reject tokens issued to any other organization's environment.
* Scope credentials you derive from the token to what a single coding session should be able to do, not to everything the creating user can do. See [Scope derived credentials](#scope-derived-credentials).

### Token format

The value of `CLAUDE_CODE_SESSION_ACCESS_TOKEN` has an `sk-ant-cc-` prefix followed by a standard three-part JWT:

```text theme={null}
sk-ant-cc-<base64url header>.<base64url payload>.<base64url signature>
```

Strip the prefix before passing the value to a JWT library. Tokens issued to Anthropic-hosted cloud sessions carry an `sk-ant-si-` prefix instead and are signed by a different key set, so reject any value that doesn't start with `sk-ant-cc-`.

The signature algorithm is `ES256`, which is ECDSA on the P-256 curve with SHA-256. The token header carries a `kid` that identifies which key in the JWKS signed it.

## Verify the token

Verification runs in one of two places. Services on your network verify the token cryptographically against Anthropic's published keys, and wrapper scripts inside the session can use the runner binary's built-in decoder instead.

### Verify the token from your service

Anthropic publishes the verification keys at a public, unauthenticated endpoint:

```text theme={null}
https://api.anthropic.com/v1/code/.well-known/jwks.json
```

The response is a standard [JSON Web Key Set](https://www.rfc-editor.org/rfc/rfc7517). Anthropic rotates the signing keys periodically, and keys from before a rotation remain in the set long enough that tokens they signed continue to verify, so don't pin a single key. The endpoint sets `Cache-Control: public, max-age=300`, so caching the key set and refetching every five minutes is safe.

Verify each incoming token against these checks:

<Steps>
  <Step title="Check the prefix">
    Reject the value if it doesn't start with `sk-ant-cc-`, then remove that prefix. The remainder is a standard compact JWT.
  </Step>

  <Step title="Verify the signature">
    Fetch the JWKS, select the key whose `kid` matches the token header, and verify the `ES256` signature. Reject tokens whose `alg` header is not `ES256`. If a token arrives with a `kid` that isn't in your cached key set, refetch the JWKS once before rejecting it: after a rotation, new tokens are signed with a key your cached set doesn't have yet.
  </Step>

  <Step title="Verify the issuer">
    Reject the token if `iss` is not exactly `ccr`.
  </Step>

  <Step title="Verify the audience against your environment">
    The `aud` claim is an array. Reject the token unless it contains your environment ID, which has the form `ccpool_...`. The environment ID is shown in your environment's detail dialog on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments), and appears as the `ccr:pool_id` claim in any of the environment's session tokens. This check is what scopes the token to your environment and rejects tokens issued to other organizations.
  </Step>

  <Step title="Verify the role">
    Reject the token if `ccr:role` is not exactly `session_worker`. Other tokens issued for self-hosted environments, such as environment secrets, runner tokens, and work orders, are signed by the same key set but carry different roles.
  </Step>

  <Step title="Verify expiry">
    Reject the token if `exp` is in the past. Anthropic issues session tokens with a four-hour lifetime by default and a maximum of eight hours. The runner refreshes the token before expiry and pushes the new value to the session, so subprocesses that Claude starts after a refresh inherit it. One session can therefore present several distinct valid tokens to your service over its lifetime.
  </Step>

  <Step title="Read the identity">
    The creating user's identity is in the `act` claim: `act.sub` is their Anthropic user ID in the prefixed form `user:<id>`, and `act.email`, when the creating surface recorded one, is their email address. Sessions created with an organization service key carry no user identity, so treat a session as user-created only when `act.sub` carries the `user:` prefix, rather than testing whether identity claims are absent. See the [claims reference](#claims-reference) for the full structure and the flat duplicate claims.
  </Step>
</Steps>

The checks map directly onto standard JWT libraries. The examples below implement the full sequence in Node.js with [`jose`](https://www.npmjs.com/package/jose), which handles JWKS fetching, caching, and `kid` selection, and in Python with [`PyJWT`](https://pyjwt.readthedocs.io/) and its built-in JWKS client.

<Tabs>
  <Tab title="Node.js (jose)">
    ```typescript theme={null}
    import { createRemoteJWKSet, jwtVerify } from "jose";

    const JWKS = createRemoteJWKSet(
      new URL("https://api.anthropic.com/v1/code/.well-known/jwks.json")
    );

    const PREFIX = "sk-ant-cc-";
    const EXPECTED_POOL_ID = "ccpool_...";

    export async function verifySessionToken(raw: string) {
      if (!raw.startsWith(PREFIX)) {
        throw new Error("not a self-hosted runner session token");
      }
      const jwt = raw.slice(PREFIX.length);

      const { payload } = await jwtVerify(jwt, JWKS, {
        issuer: "ccr",
        audience: EXPECTED_POOL_ID,
        algorithms: ["ES256"],
      });

      if (payload["ccr:role"] !== "session_worker") {
        throw new Error("token is not a session_worker token");
      }

      const act = payload.act as { email?: string; sub?: string };
      return {
        sessionId: payload["ccr:session_id"] as string,
        poolId: payload["ccr:pool_id"] as string,
        orgId: payload["ccr:org_id"] as string,
        creatorEmail: act?.email,
        creatorSub: act?.sub,
      };
    }
    ```
  </Tab>

  <Tab title="Python (PyJWT)">
    ```python theme={null}
    import jwt
    from jwt import PyJWKClient

    JWKS_URL = "https://api.anthropic.com/v1/code/.well-known/jwks.json"
    PREFIX = "sk-ant-cc-"
    EXPECTED_POOL_ID = "ccpool_..."

    jwks = PyJWKClient(JWKS_URL)


    def verify_session_token(raw: str) -> dict:
        if not raw.startswith(PREFIX):
            raise ValueError("not a self-hosted runner session token")
        token = raw.removeprefix(PREFIX)

        signing_key = jwks.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            issuer="ccr",
            audience=EXPECTED_POOL_ID,
        )

        if payload.get("ccr:role") != "session_worker":
            raise ValueError("token is not a session_worker token")

        act = payload.get("act") or {}
        return {
            "session_id": payload["ccr:session_id"],
            "pool_id": payload["ccr:pool_id"],
            "org_id": payload["ccr:org_id"],
            "creator_email": act.get("email"),
            "creator_sub": act.get("sub"),
        }
    ```
  </Tab>
</Tabs>

### Verify the token inside the session

[Wrapper scripts](/docs/en/self-hosted-environments-configuration#wrapper-scripts) run inside the session, before Claude starts. Instead of calling a JWT library, they can run the runner binary's `self-hosted-runner decode-token` subcommand. The subcommand reads the token from a positional argument, from `CLAUDE_CODE_SESSION_ACCESS_TOKEN`, or from piped stdin, in that order, then strips the prefix, verifies the signature against the JWKS endpoint, checks expiry, and prints the claims as JSON. The subcommand performs the signature and expiry checks only; it doesn't check `iss`, `aud`, or `ccr:role`. When your wrapper's auth decision depends on those claims, read them from the printed JSON and compare them explicitly.

This command extracts the creator identity, preferring the SSO provider's subject, then the email address, then the always-present Anthropic user ID:

```bash theme={null}
"$CLAUDE_RUNNER_CLAUDE_BIN" self-hosted-runner decode-token | jq -re '.act.attested_by.sub // .act.email // .act.sub'
```

Wrappers receive the absolute path to the runner's own binary in `CLAUDE_RUNNER_CLAUDE_BIN`; use that path rather than a PATH-resolved `claude` so the decode runs on the same binary the runner itself uses.

Use `jq -re` rather than `jq -r` so a missing claim causes a non-zero exit. With `-r` alone, a missing claim prints the literal string `null` and exits zero, which silently passes a bad value downstream. Pass `--no-verify` to `decode-token` only for offline inspection where the JWKS endpoint is unreachable.

## Claims reference

The table below lists the session token claims relevant to verification. Read identity from the `ccr:*` namespace and the `act` chain; the flat `account_email`, `organization_uuid`, and `account_uuid` claims are backward-compatibility duplicates that may be removed. Sessions created with an organization service key omit `act.email`, `ccr:account_id`, `account_email`, and `account_uuid`. The two email claims are optional for user-created sessions too: Anthropic records them at session creation only when the creating request's credentials carry an email, and a session dispatched from the CLI can lack both, so key identity on `act.sub` or `ccr:account_id` rather than on email. Tokens can also carry additional claims beyond this table; ignore claims you don't recognize.

| Claim               | Type             | Description                                                                                                                                                                                                                                                                                                                                                                                           |
| :------------------ | :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `iss`               | string           | Always `ccr`.                                                                                                                                                                                                                                                                                                                                                                                         |
| `sub`               | string           | `ccr:session:<session_id>`.                                                                                                                                                                                                                                                                                                                                                                           |
| `aud`               | array of strings | Always contains `anthropic-api`. For sessions in self-hosted environments the array also contains your environment ID, such as `ccpool_...`. Verify the environment ID, not `anthropic-api`.                                                                                                                                                                                                          |
| `exp`               | number           | Expiry as a Unix timestamp. Four-hour default lifetime, eight-hour maximum.                                                                                                                                                                                                                                                                                                                           |
| `iat`               | number           | Issued-at as a Unix timestamp.                                                                                                                                                                                                                                                                                                                                                                        |
| `jti`               | string           | Unique token identifier.                                                                                                                                                                                                                                                                                                                                                                              |
| `ccr:role`          | string           | Always `session_worker` for session tokens.                                                                                                                                                                                                                                                                                                                                                           |
| `ccr:session_id`    | string           | The session ID. Same value as the suffix of `sub`.                                                                                                                                                                                                                                                                                                                                                    |
| `ccr:pool_id`       | string           | Your environment ID. Same value that appears in `aud`.                                                                                                                                                                                                                                                                                                                                                |
| `ccr:org_id`        | string           | Your Anthropic organization ID.                                                                                                                                                                                                                                                                                                                                                                       |
| `ccr:account_id`    | string           | The creating user's Anthropic account ID: the value of `act.sub` without the `user:` prefix, a tagged `user_...` ID. The same value the [spawn-runner hook](/docs/en/self-hosted-environments-configuration#the-spawn-runner-hook)'s `CLAUDE_RUNNER_ACCOUNT_ID` carries and [`--lock-to-account`](/docs/en/self-hosted-environments-reference#runner-cli-flags) accepts, so the three compare as equal strings. |
| `account_email`     | string           | Duplicate of `act.email`; absent whenever `act.email` is.                                                                                                                                                                                                                                                                                                                                             |
| `organization_uuid` | string           | Your Anthropic organization UUID.                                                                                                                                                                                                                                                                                                                                                                     |
| `account_uuid`      | string           | The creating user's Anthropic account UUID.                                                                                                                                                                                                                                                                                                                                                           |
| `act`               | object           | [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693) delegation chain. See [The `act` chain](#the-act-chain).                                                                                                                                                                                                                                                                                           |

### The `act` chain

The `act` claim records the full delegation path from the user who created the session down to the [environment](/docs/en/self-hosted-environments#key-concepts) whose secret admitted the runner, and the identity that created that secret. The creating user is the outermost actor, so `act.sub` identifies them directly.

| Path              | Description                                                                                                                                                                                                                                              |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `act.sub`         | The creating user's Anthropic user ID, in the form `user:<id>`.                                                                                                                                                                                          |
| `act.email`       | The creating user's email address, when one was recorded at session creation. Don't require it; key on `act.sub`.                                                                                                                                        |
| `act.attested_by` | The upstream identity provider's attestation for the creating user, when available. `act.attested_by.sub` is the subject your SSO provider, such as Google or Okta, issued. Prefer this over `act.email` when mapping to identities in your own systems. |
| `act.act`         | The runner that spawned the session. `act.act.sub` is `ccr:runner:<runner_id>`.                                                                                                                                                                          |
| `act.act.act`     | The environment. `act.act.act.sub` is `ccr:pool:<pool_id>`.                                                                                                                                                                                              |
| `act.act.act.act` | The identity that created the environment secret the runner registered with. The chain ends here.                                                                                                                                                        |

## Scope derived credentials

The session token identifies the creating user, but don't treat it as equivalent to that user logging in directly. The token sits in an environment variable inside the session, so any code Claude runs, and any tool or MCP server the session starts, can read and present it.

Verification is also offline: a token that verifies against the JWKS stays valid until its `exp`, whatever has happened to the session since, and Anthropic doesn't publish a revocation feed for session tokens. Bound anything you derive from the token accordingly.

When your service exchanges the token for internal credentials, issue credentials scoped to what one coding session should reach:

* **Limit capabilities**: grant read and write access to the resources the session needs for coding tasks, not administrative capabilities the user holds elsewhere.
* **Limit lifetime**: bound derived credentials to the token's `exp`, or shorter.
* **Audit as the session**: record the `ccr:session_id` and `jti` alongside the user identity so you can trace actions back to a specific session.

## Related environment variables

The creator identity also appears in plain environment variables on two surfaces that never verify the token:

* **The [`spawn-runner` hook](/docs/en/self-hosted-environments-configuration#the-spawn-runner-hook), on the orchestrator**: the hook runs before any runner exists for a queued session and receives the creator identity in variables such as `CLAUDE_RUNNER_ACCOUNT_EMAIL` and `CLAUDE_RUNNER_ACCOUNT_ID`. The orchestrator reads them from the work order, the signed single-use token that authorizes spawning one runner, without verifying the work order's signature itself; the claims are trusted because the work order arrives over the orchestrator's connection to Anthropic, which the environment secret authenticates.
* **[Wrapper scripts](/docs/en/self-hosted-environments-configuration#wrapper-scripts), inside the session**: wrappers receive `CCR_SESSION_ACCOUNT_EMAIL`, the creator's email pre-extracted from the token without signature verification. The variable is suitable for labelling, such as commit trailers, not for auth decisions.

Use the plain variables for orchestrator-side decisions such as selecting a machine image. Use `CLAUDE_CODE_SESSION_ACCESS_TOKEN` when a downstream service needs independent cryptographic proof rather than trusting the runner's environment.

## What's next

* [Self-hosted environments](/docs/en/self-hosted-environments): the environment, runner, and session model; the [quickstart](/docs/en/self-hosted-environments-quickstart) and [Deploy to production](/docs/en/self-hosted-environments-deploy) hold setup and operations
* [Customize sessions](/docs/en/self-hosted-environments-configuration): wrapper scripts that consume the token, and the `spawn-runner` hook
* [Reference](/docs/en/self-hosted-environments-reference): CLI flags, environment variables, and metrics
