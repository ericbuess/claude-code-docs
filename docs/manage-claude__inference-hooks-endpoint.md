---
title: Develop an Inference hooks integration
url: https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint
description: Build the AI security server that receives signed Inference hooks requests, verifies them, and returns allow or deny verdicts.
---

<Note>
  Inference hooks are in beta and available to Claude Enterprise organizations. Field names, request shapes, and headers may change before general availability.
</Note>

An Inference hooks integration is an AI security server: an HTTPS service that Anthropic calls. For each governed request, your server receives a signed `POST` carrying the conversation transcript and responds with an allow or deny verdict. This page documents the protocol for building that server: the request and verdict schemas, signature verification, and the operational contract.

For turning Inference hooks on and pointing them at your endpoint, see [Configure Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration). For what Inference hooks are and when to use them, see the [Inference hooks overview](https://platform.claude.com/docs/en/manage-claude/inference-hooks).

## Get a first verdict round trip

The smallest working integration is a server that reads each request and allows it. Run one of the following servers, expose it at a public `https://` URL (for example, behind a TLS-terminating reverse proxy on a host you control, not a reverse-tunnel service; see [Receive a request](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#receive-a-request)), then have your administrator [set it as the endpoint and test the connection](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration): the **Test connection** result reports the allow verdict your server returned.

<CodeGroup exclude="shell">
  ```python Python
  # Run with: python server.py
  from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


  class VerdictHandler(BaseHTTPRequestHandler):
      protocol_version = "HTTP/1.1"  # keep the connection open between verdicts

      def do_POST(self):
          # Drain the body; transcripts can be megabytes.
          self.rfile.read(int(self.headers.get("Content-Length", 0)))
          verdict = b'{"action": "allow"}'
          self.send_response(200)
          self.send_header("Content-Type", "application/json")
          self.send_header("Content-Length", str(len(verdict)))
          self.end_headers()
          self.wfile.write(verdict)


  ThreadingHTTPServer(("", 8000), VerdictHandler).serve_forever()
  ```

  ```typescript TypeScript
  // Run with: node server.ts
  import { createServer } from "node:http";

  createServer((request, response) => {
    // Drain the body before answering; transcripts can be megabytes.
    request.resume();
    request.on("end", () => {
      response.writeHead(200, { "Content-Type": "application/json" });
      response.end('{"action": "allow"}');
    });
  }).listen(8000);
  ```

  ```csharp C#
  #:sdk Microsoft.NET.Sdk.Web
  #:property PublishAot=false
  // Run with: dotnet run server.cs

  var app = WebApplication.Create();

  app.MapPost("/{**path}", async (HttpRequest request) =>
  {
      // Drain the body; transcripts can be megabytes.
      await request.Body.CopyToAsync(Stream.Null);
      return Results.Text("""{"action": "allow"}""", "application/json");
  });

  app.Run("http://0.0.0.0:8000");
  ```

  ```go Go
  // Run with: go run server.go
  package main

  import (
  	"io"
  	"log"
  	"net/http"
  )

  func main() {
  	http.HandleFunc("POST /", func(writer http.ResponseWriter, request *http.Request) {
  		// Drain the body so the connection can be reused; transcripts can be megabytes.
  		io.Copy(io.Discard, request.Body)
  		writer.Header().Set("Content-Type", "application/json")
  		writer.Write([]byte(`{"action": "allow"}`))
  	})
  	log.Fatal(http.ListenAndServe(":8000", nil))
  }
  ```

  ```java Java
  // Run with: java VerdictServer.java
  import com.sun.net.httpserver.HttpServer;

  void main() throws IOException {
      HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
      server.createContext("/", exchange -> {
          // Drain the body without buffering it; transcripts can be megabytes.
          exchange.getRequestBody().transferTo(OutputStream.nullOutputStream());
          byte[] verdict = "{\"action\": \"allow\"}".getBytes(StandardCharsets.UTF_8);
          exchange.getResponseHeaders().set("Content-Type", "application/json");
          exchange.sendResponseHeaders(200, verdict.length);
          try (OutputStream responseBody = exchange.getResponseBody()) {
              responseBody.write(verdict);
          }
      });
      server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
      server.start();
  }
  ```

  ```php PHP
  <?php
  // Run with: php -S 0.0.0.0:8000 server.php

  // Drain the body; transcripts can be megabytes.
  file_get_contents('php://input');

  http_response_code(200);
  header('Content-Type: application/json');
  echo '{"action": "allow"}';
  ```

  ```ruby Ruby
  # webrick is a regular gem in Ruby 3.4: gem install webrick, or add gem "webrick".
  # Run with: ruby server.rb
  require "webrick"

  server = WEBrick::HTTPServer.new(Port: 8000)
  server.mount_proc("/") do |request, response|
    request.body # Drain the body; transcripts can be megabytes.
    response.status = 200
    response["Content-Type"] = "application/json"
    response.body = '{"action": "allow"}'
  end
  server.start
  ```
</CodeGroup>

<Note>
  These servers accept every request, including unsigned ones. Add [signature verification](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#verify-the-signature) before you enforce.
</Note>

## Receive a request

Anthropic sends an HTTPS `POST` to the URL your administrator configures. The whole configured URL is the endpoint: there is no fixed path suffix, so choose any path that suits your server.

Host your AI security server where Anthropic can reach it: an `https://` URL on port 443, on a publicly routable host (private, loopback, and carrier-grade NAT ranges are refused at connect time), with a certificate that validates against the public CA trust store, responding without redirects. The configured URL must be the final destination. Reverse-tunnel hosts (ngrok and similar tunnel services) are not supported: Anthropic's network policy blocks them. Host your server on a domain you control. [Configure Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration) covers how your administrator sets and tests the URL.

Every request carries these fixed headers, along with any [custom request headers](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration) your administrator configured and, once your organization has a signing secret, the `webhook-*` signature headers described in [Verify the signature](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#verify-the-signature):

| Header            | Value              |
| ----------------- | ------------------ |
| `Content-Type`    | `application/json` |
| `User-Agent`      | `anthropic-dlp/1`  |
| `Accept-Encoding` | `identity`         |

There is one hook event today: the prompt frame, sent once per governed inference request, before inference begins. Anthropic holds the request until your AI security server responds or the verdict timeout elapses.

## The prompt frame

The request body is a JSON object with these fields:

| Field        | Type           | Description                                                                                                                                                                                                                                                              |
| ------------ | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`       | string         | The hook event. Always `"prompt"` today; other event types will be introduced in the future, so handle an unrecognized value gracefully (see [Forward compatibility](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#forward-compatibility)). |
| `request_id` | string         | Opaque per-inference-call identifier for correlation. Equals the `webhook-id` header.                                                                                                                                                                                    |
| `tenant_id`  | string or null | Opaque identifier for the organization the request belongs to.                                                                                                                                                                                                           |
| `actor`      | object         | The principal the request is attributed to, discriminated on `type` (`"user"` is the only value sent today): `id` (a tagged identifier, stable across requests for the same account) and `email_address` (when available). Both `id` and `email_address` can be null.    |
| `source`     | object         | The originating application: `application` (see [Source values](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#source-values)).                                                                                                              |
| `messages`   | array          | The conversation transcript up to the point of inference. See [Content blocks](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#content-blocks).                                                                                               |
| `session_id` | string or null | Opaque conversation identifier, when one exists. Don't parse it. For Claude Code it is a best-effort, client-asserted session identifier.                                                                                                                                |
| `model`      | string or null | Public model identifier for this request, when available.                                                                                                                                                                                                                |
| `metadata`   | object         | Reserved extension map of string keys to string values, sent empty today. Require nothing from it, and tolerate its absence, its presence, and any keys that appear.                                                                                                     |

<Note>
  Requests currently also carry deprecated legacy aliases of some of these fields. Read the field names documented on this page and ignore any others; the aliases exist only for earlier integrations.
</Note>

An example request body:

```json
{
  "type": "prompt",
  "request_id": "req_abc123",
  "tenant_id": "11111111-1111-1111-1111-111111111111",
  "actor": {
    "type": "user",
    "id": "user_01AbCdEfGhIjKlMnOpQrStUv",
    "email_address": "alice@example.com"
  },
  "source": {
    "application": "claude-ai"
  },
  "session_id": "22222222-2222-2222-2222-222222222222",
  "model": "claude-sonnet-4-5",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Summarize the attached report."
        },
        {
          "type": "attachment",
          "file_name": "q2-report.pdf",
          "media_type": "application/pdf",
          "size_bytes": 48213,
          "text": "Q2 revenue grew 14% quarter over quarter..."
        }
      ]
    }
  ],
  "metadata": {}
}
```

### Content blocks

Each entry in `messages` has a `role` of `user` or `assistant` (tool results appear under the `user` role, matching the public Messages API content model) and a `content` array of blocks discriminated by `type`:

| Block `type`  | Fields                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`        | `text`: the text content.                                                                                                                                                                                                                                                                                                                                                                    |
| `tool_use`    | `id`: the identifier the matching tool result references. `tool_name`: the tool's name. `input`: the arguments the model passed to the tool.                                                                                                                                                                                                                                                 |
| `tool_result` | `content`: the tool's output as text, with parts joined by newlines; binary parts such as images are replaced by placeholder markers, and raw bytes are never sent. `is_error`: whether the tool call failed. `tool_name`: the tool's name, so a policy can condition on tool identity without cross-referencing an earlier block. `tool_use_id`: the `id` of the matching `tool_use` block. |
| `attachment`  | `file_name`: the original file name or path. `media_type`: the attachment's media type. `size_bytes`: the size of the original file. `text`: the text content of the attachment when available, such as extracted document text, an audio transcript, or link metadata. Raw attachment bytes are never sent.                                                                                 |

A block whose `type` you don't recognize is a forward-compatible addition. The only field it guarantees is `type`; your policy may inspect whatever other fields are present, but must not reject the request because of an unrecognized type.

### What the transcript contains

The transcript is the conversation as the end user sees it, up to the point of inference: transcript text, tool calls and their results, extracted attachment text, and prior turns. It never includes system prompts, tool definitions, Anthropic-internal context, Claude's hidden reasoning, or raw file bytes.

A turn whose every block is excluded is omitted entirely, so don't assume strict user and assistant alternation.

Transcripts are sent untruncated, so a long conversation with large attachments produces a large request body, up to an upper bound of 10 MB. Raise your server's body limit to accept that ceiling. Several common defaults are much smaller, including nginx `client_max_body_size` at 1 MB and Express `express.json()` at 100 kB, and a rejected body counts as a webhook failure, so under **Allow the request** failure handling an oversized prompt would reach the model uninspected.

### Source values

`source.application` is an open string, not a closed enum. Known values are `claude-ai` and `claude-code`; [connection tests](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration) use `config-test`. New values may appear, and your server must not reject a request because of one it doesn't recognize.

Treat `source.application` as advisory routing metadata, not a trust boundary: don't rest a security-critical policy decision on it alone.

## Return a verdict

Respond with HTTP 200 and a JSON verdict body for both outcomes; the `action` field discriminates. To allow the request:

```json
{
  "action": "allow"
}
```

To deny it:

```json
{
  "action": "deny",
  "deny_reason": "This prompt appears to contain customer payment card data, which your organization's policy does not allow.",
  "reference_id": "scan_01HXPT4R9V"
}
```

| Field          | Constraints                                                     | Semantics                                                                                                                                                                                                                                                                                           |
| -------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `action`       | `"allow"` or `"deny"`; required                                 | `allow` lets inference proceed; `deny` rejects it.                                                                                                                                                                                                                                                  |
| `deny_reason`  | string or null; at most 500 characters, longer values truncated | Shown to the end user when `action` is `deny`; ignored on `allow`.                                                                                                                                                                                                                                  |
| `reference_id` | string or null; at most 50 characters from `[A-Za-z0-9._:/-]`   | Your own identifier for this evaluation. It's recorded on the denial's `inference_hooks_request_denied` [compliance activity](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) and never shown to the end user. Keep it opaque: no request content and no personal data. |

A deny is never discarded over a formatting problem: an oversize `deny_reason` is truncated, a malformed `reference_id` is silently dropped, and the `action` is still honored.

The reverse doesn't hold. Anything other than HTTP 200 with a parseable verdict is a webhook failure, and your organization's [failure handling](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration) applies instead of a verdict. In particular:

* Don't signal a deny with an error status. A non-200 response is a failure, not a deny.
* Any `action` value other than `allow` or `deny` is treated as a webhook failure.

Anthropic reads at most 64 KiB of the response body, and the body must be uncompressed. Redirects are not followed, and cookies are ignored. Unknown fields in the verdict body are ignored, so you can return a richer object alongside the fields documented here.

## Verify the signature

Requests are signed per the [Standard Webhooks](https://www.standardwebhooks.com/) specification, using three headers. Anthropic sends the header names in lowercase, and proxies are free to re-case them, so look them up case-insensitively.

| Header              | Contents                                                                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `webhook-id`        | Unique identifier for this delivery. Equals the body's `request_id`. Use it as an idempotency key and as the first component of the signed payload.                                                              |
| `webhook-timestamp` | Unix time in seconds, as a decimal string, when the request was signed. Reject a timestamp more than five minutes from your server's clock, in either direction.                                                 |
| `webhook-signature` | One or more space-separated `v1,<base64>` values, each an HMAC-SHA256 over `{webhook-id}.{webhook-timestamp}.{raw body bytes}`. Accept the request if any value matches yours, using a constant-time comparison. |

Two details cause most verification bugs:

* **Verify raw bytes.** Compute the HMAC over the body exactly as received, before any JSON parsing or re-encoding.
* **Decode the secret with a standard base64 decoder.** The signing secret is the value after the `whsec_` prefix, encoded with the standard base64 alphabet (`+` and `/`), as is the signature in the header. A URL-safe decoder derives the wrong key bytes whenever the secret contains `+` or `/`, which is most of the time.

Once your organization has a signing secret, every request Anthropic sends is signed, and [enabling Inference hooks requires one](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration), so reject any request that arrives unsigned. One exception: a connection test sent before your organization's first save arrives unsigned, because the signing secret doesn't exist yet. Accept unsigned requests until your administrator confirms the secret exists, then reject them.

[Rotating the secret](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration#rotate-your-signing-secret) is an immediate cutover, but requests signed with the previous secret can still arrive for about a minute afterward, plus anything already in flight. Have your AI security server accept signatures from both secrets during the switchover so those stragglers aren't rejected.

The following samples are server implementations, so there is no shell tab: an AI security server is a long-running HTTPS service rather than a one-shot request. Each sample uses only the language's standard library; the [Standard Webhooks](https://www.standardwebhooks.com/) project also publishes verification libraries for most languages.

<CodeGroup exclude="shell">
  ```python Python
  import base64
  import hashlib
  import hmac
  import time

  TOLERANCE_SECONDS = 300


  def verify(secret: str, headers: dict[str, str], body: bytes) -> bool:
      """Return True if the body was signed by Anthropic for this organization.

      Anthropic sends header names in lowercase, but proxies are free to
      re-case them, so normalize the lookup to lowercase.
      """
      lowercased = {name.lower(): value for name, value in headers.items()}
      try:
          message_id = lowercased["webhook-id"]
          timestamp = lowercased["webhook-timestamp"]
          signatures = lowercased["webhook-signature"]
      except KeyError:
          return False  # unsigned request: not from Anthropic

      try:
          signed_at = int(timestamp)
      except ValueError:
          return False
      if abs(time.time() - signed_at) > TOLERANCE_SECONDS:
          return False  # replayed, or the clocks disagree

      try:
          key = base64.b64decode(secret.removeprefix("whsec_"), validate=True)
      except ValueError:
          return False  # misconfigured secret: reject rather than crash

      payload = f"{message_id}.{timestamp}.".encode() + body
      expected = b"v1," + base64.b64encode(
          hmac.new(key, payload, hashlib.sha256).digest()
      )

      # Compare bytes: compare_digest on str raises on non-ASCII input.
      return any(
          hmac.compare_digest(expected, candidate.encode())
          for candidate in signatures.split()
      )
  ```

  ```typescript TypeScript
  import { createHmac, timingSafeEqual } from "node:crypto";
  import type { IncomingHttpHeaders } from "node:http";

  const TOLERANCE_SECONDS = 300;

  /**
   * Returns true if the body was signed by Anthropic for this organization.
   *
   * Node lowercases incoming header names, matching how Anthropic sends
   * them, so look them up in lowercase.
   */
  export function verify(secret: string, headers: IncomingHttpHeaders, body: Buffer): boolean {
    const messageId = headers["webhook-id"];
    const timestamp = headers["webhook-timestamp"];
    const signatures = headers["webhook-signature"];
    if (
      typeof messageId !== "string" ||
      typeof timestamp !== "string" ||
      typeof signatures !== "string"
    ) {
      return false; // unsigned request: not from Anthropic
    }

    const signedAt = Number(timestamp);
    if (
      !Number.isFinite(signedAt) ||
      Math.abs(Date.now() / 1000 - signedAt) > TOLERANCE_SECONDS
    ) {
      return false; // replayed, or the clocks disagree
    }

    const key = Buffer.from(secret.replace(/^whsec_/, ""), "base64");
    const payload = Buffer.concat([Buffer.from(`${messageId}.${timestamp}.`), body]);
    const expected = Buffer.from(
      "v1," + createHmac("sha256", key).update(payload).digest("base64")
    );

    return signatures.split(" ").some((candidate) => {
      const candidateBytes = Buffer.from(candidate);
      return (
        candidateBytes.length === expected.length && timingSafeEqual(candidateBytes, expected)
      );
    });
  }
  ```

  ```csharp C#
  using System.Security.Cryptography;
  using System.Text;

  static class InferenceHooks
  {
      private const int ToleranceSeconds = 300;

      /// <summary>
      /// Returns true if the body was signed by Anthropic for this organization.
      /// Anthropic sends header names in lowercase, but proxies are free to
      /// re-case them, so match them case-insensitively.
      /// </summary>
      public static bool Verify(string secret, IReadOnlyDictionary<string, string> headers, byte[] body)
      {
          // TryAdd keeps the first value if a proxy delivered case-duplicate
          // names; the copying constructor would throw on them instead.
          var lookup = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
          foreach (var (name, value) in headers)
          {
              lookup.TryAdd(name, value);
          }

          if (!lookup.TryGetValue("webhook-id", out var messageId) ||
              !lookup.TryGetValue("webhook-timestamp", out var timestamp) ||
              !lookup.TryGetValue("webhook-signature", out var signatures))
          {
              return false; // unsigned request: not from Anthropic
          }

          if (!long.TryParse(timestamp, out var signedAt) ||
              Math.Abs(DateTimeOffset.UtcNow.ToUnixTimeSeconds() - signedAt) > ToleranceSeconds)
          {
              return false; // replayed, or the clocks disagree
          }

          // Standard base64 alphabet: a URL-safe decoder derives the wrong key bytes.
          var encodedKey = secret.StartsWith("whsec_") ? secret["whsec_".Length..] : secret;
          byte[] key;
          try
          {
              key = Convert.FromBase64String(encodedKey);
          }
          catch (FormatException)
          {
              return false; // misconfigured secret: reject rather than crash
          }

          byte[] payload = [.. Encoding.UTF8.GetBytes($"{messageId}.{timestamp}."), .. body];
          var expected = Encoding.UTF8.GetBytes(
              "v1," + Convert.ToBase64String(HMACSHA256.HashData(key, payload)));

          // FixedTimeEquals is constant-time and returns false on a length mismatch.
          return signatures.Split(' ', StringSplitOptions.RemoveEmptyEntries).Any(candidate =>
              CryptographicOperations.FixedTimeEquals(Encoding.UTF8.GetBytes(candidate), expected));
      }
  }
  ```

  ```go Go
  package hooks

  import (
  	"crypto/hmac"
  	"crypto/sha256"
  	"encoding/base64"
  	"net/http"
  	"strconv"
  	"strings"
  	"time"
  )

  const toleranceSeconds = 300

  // verify reports whether body was signed by Anthropic for this organization.
  // net/http canonicalizes header names on lookup, so re-cased names still match.
  func verify(secret string, header http.Header, body []byte) bool {
  	messageID := header.Get("webhook-id")
  	timestamp := header.Get("webhook-timestamp")
  	signatures := header.Get("webhook-signature")
  	if messageID == "" || timestamp == "" || signatures == "" {
  		return false // unsigned request: not from Anthropic
  	}

  	signedAt, err := strconv.ParseInt(timestamp, 10, 64)
  	if err != nil {
  		return false
  	}
  	age := time.Now().Unix() - signedAt
  	if age > toleranceSeconds || age < -toleranceSeconds {
  		return false // replayed, or the clocks disagree
  	}

  	// Standard base64 alphabet: a URL-safe decoder derives the wrong key bytes.
  	key, err := base64.StdEncoding.DecodeString(strings.TrimPrefix(secret, "whsec_"))
  	if err != nil {
  		return false
  	}

  	mac := hmac.New(sha256.New, key)
  	mac.Write([]byte(messageID + "." + timestamp + "."))
  	mac.Write(body)
  	expected := "v1," + base64.StdEncoding.EncodeToString(mac.Sum(nil))

  	for _, candidate := range strings.Fields(signatures) {
  		if hmac.Equal([]byte(candidate), []byte(expected)) { // constant-time
  			return true
  		}
  	}
  	return false
  }
  ```

  ```java Java
  import java.nio.charset.StandardCharsets;
  import java.security.GeneralSecurityException;
  import java.security.MessageDigest;
  import java.time.Instant;
  import java.util.Base64;
  import java.util.HashMap;
  import java.util.Locale;
  import java.util.Map;
  import javax.crypto.Mac;
  import javax.crypto.spec.SecretKeySpec;

  public final class InferenceHookVerifier {
      private static final long TOLERANCE_SECONDS = 300;

      /**
       * Returns true if the body was signed by Anthropic for this organization.
       *
       * <p>Anthropic sends header names in lowercase, but proxies are free to
       * re-case them, so normalize the lookup to lowercase.
       */
      public static boolean verify(String secret, Map<String, String> headers, byte[] body) {
          Map<String, String> lowercased = new HashMap<>();
          headers.forEach((name, value) -> lowercased.put(name.toLowerCase(Locale.ROOT), value));

          String messageId = lowercased.get("webhook-id");
          String timestamp = lowercased.get("webhook-timestamp");
          String signatures = lowercased.get("webhook-signature");
          if (messageId == null || timestamp == null || signatures == null) {
              return false; // unsigned request: not from Anthropic
          }

          long signedAt;
          try {
              signedAt = Long.parseLong(timestamp);
          } catch (NumberFormatException _) {
              return false;
          }
          if (Math.abs(Instant.now().getEpochSecond() - signedAt) > TOLERANCE_SECONDS) {
              return false; // replayed, or the clocks disagree
          }

          // Standard base64 alphabet: a URL-safe decoder derives the wrong key bytes.
          byte[] key;
          try {
              key = Base64.getDecoder().decode(
                      secret.startsWith("whsec_") ? secret.substring("whsec_".length()) : secret);
          } catch (IllegalArgumentException _) {
              return false; // misconfigured secret: reject rather than crash
          }

          byte[] expected;
          try {
              Mac mac = Mac.getInstance("HmacSHA256");
              mac.init(new SecretKeySpec(key, "HmacSHA256"));
              mac.update((messageId + "." + timestamp + ".").getBytes(StandardCharsets.UTF_8));
              expected = ("v1," + Base64.getEncoder().encodeToString(mac.doFinal(body)))
                      .getBytes(StandardCharsets.UTF_8);
          } catch (GeneralSecurityException impossible) {
              // Every JVM ships HmacSHA256, so this never fires at runtime.
              throw new IllegalStateException(impossible);
          }

          for (String candidate : signatures.split(" ")) {
              if (MessageDigest.isEqual(candidate.getBytes(StandardCharsets.UTF_8), expected)) {
                  return true; // MessageDigest.isEqual is constant-time
              }
          }
          return false;
      }
  }
  ```

  ```php PHP
  const TOLERANCE_SECONDS = 300;

  /**
   * Returns true if the body was signed by Anthropic for this organization.
   *
   * Anthropic sends header names in lowercase, but proxies are free to
   * re-case them, so normalize the lookup to lowercase.
   */
  function verify(string $secret, array $headers, string $body): bool
  {
      $lowercased = array_change_key_case($headers, CASE_LOWER);
      $messageId = $lowercased['webhook-id'] ?? null;
      $timestamp = $lowercased['webhook-timestamp'] ?? null;
      $signatures = $lowercased['webhook-signature'] ?? null;
      if ($messageId === null || $timestamp === null || $signatures === null) {
          return false; // unsigned request: not from Anthropic
      }

      $signedAt = filter_var($timestamp, FILTER_VALIDATE_INT);
      if ($signedAt === false || abs(time() - $signedAt) > TOLERANCE_SECONDS) {
          return false; // replayed, or the clocks disagree
      }

      // Standard base64 alphabet: a URL-safe decoder derives the wrong key bytes.
      $encodedKey = str_starts_with($secret, 'whsec_') ? substr($secret, strlen('whsec_')) : $secret;
      $key = base64_decode($encodedKey, strict: true);
      if ($key === false) {
          return false;
      }

      $payload = "{$messageId}.{$timestamp}." . $body;
      $expected = 'v1,' . base64_encode(hash_hmac('sha256', $payload, $key, binary: true));

      foreach (explode(' ', $signatures) as $candidate) {
          if (hash_equals($expected, $candidate)) { // constant-time
              return true;
          }
      }
      return false;
  }
  ```

  ```ruby Ruby
  # base64 is a bundled gem in Ruby 3.4: Bundler-managed apps add gem "base64".
  require "base64"
  require "openssl"

  TOLERANCE_SECONDS = 300

  # Returns true if the body was signed by Anthropic for this organization.
  #
  # Anthropic sends header names in lowercase, but proxies are free to
  # re-case them, so normalize the lookup to lowercase.
  def verify(secret, headers, body)
    lowercased = headers.transform_keys(&:downcase)
    message_id = lowercased["webhook-id"]
    timestamp = lowercased["webhook-timestamp"]
    signatures = lowercased["webhook-signature"]
    if message_id.nil? || timestamp.nil? || signatures.nil?
      return false # unsigned request: not from Anthropic
    end

    signed_at = Integer(timestamp, exception: false)
    if signed_at.nil? || (Time.now.to_i - signed_at).abs > TOLERANCE_SECONDS
      return false # replayed, or the clocks disagree
    end

    # Standard base64 alphabet: a URL-safe decoder derives the wrong key bytes.
    begin
      key = Base64.strict_decode64(secret.delete_prefix("whsec_"))
    rescue ArgumentError
      return false # misconfigured secret: reject rather than crash
    end

    # Feed the body separately so its encoding never has to match the prefix's.
    hmac = OpenSSL::HMAC.new(key, "SHA256")
    hmac.update("#{message_id}.#{timestamp}.")
    hmac.update(body)
    expected = "v1," + Base64.strict_encode64(hmac.digest)

    signatures.split(" ").any? do |candidate|
      # fixed_length_secure_compare raises on a length mismatch, so screen lengths first.
      candidate.bytesize == expected.bytesize &&
        OpenSSL.fixed_length_secure_compare(candidate, expected)
    end
  end
  ```
</CodeGroup>

## Operational semantics

### Timeout and retry

Your administrator sets a verdict timeout between 1 and 10,000ms (5,000ms by default). The budget covers the entire exchange: connection, TLS handshake, request, and response.

Anthropic retries exactly once, after a 100ms delay, and only when the connection attempt fails. The retry shares the same timeout budget and carries the same `webhook-id` and the same signature. Once your AI security server has responded, the exchange is never retried.

### Webhook failures

Timeouts, non-200 statuses (redirects included), unparseable or oversized response bodies, and unreachable endpoints are all webhook failures. A webhook failure never becomes a deny; instead, your organization's [failure handling](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration) setting decides whether the affected request is blocked or proceeds without inspection.

### Circuit breaker

Sustained webhook failures attributable to your AI security server trip a circuit breaker that stops enforcement: Anthropic stops contacting your server, and failure handling applies to every request. Recovery happens on the admin side: fix the server, then have your administrator turn **Enforce verdicts** back on. See [Circuit breaker](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration#circuit-breaker).

### Latency

Enforcement adds your AI security server's round trip to the latency of every governed request in your organization. Keep the verdict fast, and load-test your server before rolling it out to a large organization.

### Source IP addresses

Requests to your AI security server originate from `160.79.106.0/24`, part of Anthropic's published [outbound IP ranges](https://platform.claude.com/docs/en/api/ip-addresses). Allowlist that block, not the inbound ranges on the same page, which don't cover it. Allowlisting narrows your server's exposure, but it is not a substitute for signature verification: the block carries Anthropic egress traffic beyond Inference hooks.

## Forward compatibility

The protocol grows without breaking correctly written servers. Your server must ignore:

* Unknown top-level fields on the prompt frame.
* Unknown keys in `metadata`.
* New `source.application` values.
* New `actor.type` values. `actor` is a union discriminated on `type`, and `"user"` is the only kind sent today; a future kind guarantees only that `type` is present.
* Content blocks with an unrecognized `type`.

Never reject a request because of an unrecognized block type or field; read the fields you know and skip the rest.

Other hook event types will be introduced in the future. A new event type is an addition your server can't handle by skipping a field: the request still needs a verdict. When the top-level `type` is a value you don't recognize, return an allow verdict rather than an error status; an error response is a [webhook failure](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#webhook-failures), and sustained failures trip the [circuit breaker](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#circuit-breaker).

## Design your integration

A production AI security server makes a few design choices beyond the wire protocol.

**Deduplicate on `webhook-id`.** The `webhook-id` header is unique per delivery and equals the body's `request_id`, and a connection-failure retry reuses it, so it works as an idempotency key. If you record verdicts, key the records on it.

**Record verdicts and join denials.** Store each verdict you return along with its `reference_id`. Every denial is recorded as an `inference_hooks_request_denied` compliance activity carrying the `reference_id` your server returned, so you can join denials in the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) to the matching records in your own system.

**Archive with an always-allow server.** To capture transcripts in real time without policing them, return `{"action": "allow"}` unconditionally and persist the frame after responding. This is a push-based alternative to polling the [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api), and answering before you persist keeps your round trip out of the user's critical path.

**Write `deny_reason` for the end user.** The text you return is what the user sees when their request is blocked, truncated at 500 characters. Tell them what to change, such as which kind of content to remove, rather than emitting a scanner code that only your team can interpret.

## Next steps

<CardGroup cols={2}>
  <Card title="Configure Inference hooks" href="https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration">
    Enable Inference hooks, connect and test your endpoint, and control enforcement, failure handling, and rollout.
  </Card>

  <Card title="Inference hooks overview" href="https://platform.claude.com/docs/en/manage-claude/inference-hooks">
    What Inference hooks are, how the verdict round trip works, and when to use them.
  </Card>
</CardGroup>
