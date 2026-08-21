> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Test self-hosted environments end to end

> Verify a self-hosted runner image from CI: dispatch a session with the CLI, read Claude's replies through a Stop hook, and script the full loop.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; [Availability and limitations](/docs/en/self-hosted-environments#availability-and-limitations) covers the enablement path. This page is the CI test recipe; see the [quickstart](/docs/en/self-hosted-environments-quickstart) for setup and [Deploy to production](/docs/en/self-hosted-environments-deploy) for the fleet recipes.
</Note>

In a [self-hosted environment](/docs/en/self-hosted-environments), Claude Code [cloud sessions](/docs/en/claude-code-on-the-web) run on a runner image you build and maintain. Before rolling a new image to your production environment, drive a full session against a test environment from a script: create a session, read Claude's reply, send a follow-up, and read that reply too. This is the shape of a CI smoke test that verifies your runner image, git access, and any custom tools before you promote a change.

This recipe assumes you've already [set up an environment and a runner](/docs/en/self-hosted-environments-quickstart#set-up-an-environment-and-runner), and that your CI job starts the runner process on the same host as the test script, the natural setup for testing a new runner image. A Stop hook you install on the runner writes each turn's final reply to a local file, and the script reads it from there, so the only calls to the Anthropic API are the two dispatches themselves. If your test runners are on separate infrastructure, see [Remote test runners](#remote-test-runners).

## Install the capture hook on your test runner

The read-back works through a Claude Code [Stop hook](/docs/en/hooks#stop): when Claude finishes a turn, the hook receives the final assistant message as `last_assistant_message` in its stdin JSON and appends it to `$E2E_REPLY_DIR/<session_id>.txt`. Install it the same way as the [commit-nudge Stop hook](/docs/en/self-hosted-environments-configuration#prompt-sessions-to-push-their-work), on the runner host's `~/.claude/`, which the runner seeds into every session.

### Save the hook files

Save the two files below on the runner host:

* The settings block: merge into `~/.claude/settings.json` on the runner host
* The script: save as `~/.claude/hooks/e2e-stop-hook-capture.sh` on the runner host and make it executable

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "timeout": 10,
            "command": "\"$CLAUDE_CONFIG_DIR/hooks/e2e-stop-hook-capture.sh\""
          }
        ]
      }
    ]
  }
}
```

```sh theme={null}
#!/bin/sh
# Stop hook for testing a self-hosted environment end to end: writes each
# turn's final assistant reply to $E2E_REPLY_DIR/<session_id>.txt so a
# co-located test driver can read it without calling the Anthropic API.
# Install on the TEST runner only. Requires jq.

# No-op unless the driver is listening. Never fail the turn.
[ -n "${E2E_REPLY_DIR:-}" ] && [ -d "$E2E_REPLY_DIR" ] || exit 0

# CLAUDE_CODE_REMOTE_SESSION_ID is exported in cse_... form; the session
# id the dispatch CLI prints is in session_... form. Same id, different
# prefix.
sid=$(printf '%s' "${CLAUDE_CODE_REMOTE_SESSION_ID:-}" | sed 's/^cse_/session_/')
[ -n "$sid" ] || exit 0

# last_assistant_message is absent when the final assistant turn had no
# text, such as a tool-use-only turn. The `// empty` filter makes that a
# zero-byte write rather than the literal string "null".
jq -r '.last_assistant_message // empty' >> "$E2E_REPLY_DIR/$sid.txt" 2>/dev/null
exit 0
```

### Before you start the runner

Two things the hook depends on:

* Install it before you start the runner. The runner snapshots `~/.claude/` once at startup, so a hook added to a running runner takes effect only after a restart.
* Export `E2E_REPLY_DIR` to the runner process. The hook is a no-op when the variable is unset or the directory doesn't exist, so set it wherever you start the runner, such as the systemd unit, pod spec, or CI step. The test script below requires it too.

Install this hook only on runners serving your test environment. It writes every session's final reply to disk whenever `E2E_REPLY_DIR` exists, which is harmless on a throwaway CI runner but not something to carry into a production-environment runner image where the variable might be set by accident.

## Run the test loop

The `--environment` and `--ref` dispatch flags require Claude Code v2.1.224 or later on the machine that runs the script, the same floor as the runner itself. With the hook in place and a runner started on this host, the test script:

1. Creates a session on the test environment with `claude -p "<prompt>" --environment <environment-id> --output-format json`, run from a git checkout so the CLI can auto-detect the repository from the `origin` remote. The optional `--ref <branch>` bases the session's checkout on a named ref instead of local HEAD. The command creates the session, prints one line of JSON containing `session_id`, and exits without waiting for Claude's reply.
2. Waits for the reply to appear in `$E2E_REPLY_DIR/<session_id>.txt`, written by the Stop hook on the runner once the turn completes.
3. Sends a follow-up with `claude -p "<message>" --cloud <session_id> --output-format json` (see [Send a follow-up message to a running session](/docs/en/claude-code-on-the-web#send-follow-ups-from-the-cli)), which posts a user event to the existing session and exits.
4. Waits for the follow-up's reply the same way as step 2.

### `--environment` dispatch behavior

In a non-interactive run, with `-p` or a piped prompt, Claude Code creates the session, prints the session ID and a link to it, and exits. From a terminal, `claude --environment <id> "task"` starts an attached interactive cloud session on the environment instead.

The flag takes precedence over the [`remote.defaultEnvironmentId`](/docs/en/settings#available-settings) setting. It doesn't support `--output-format stream-json`, and can't be combined with flags that resume, attach to, or preconfigure a session, such as `--resume`, `--continue`, `--teleport`, `--session-id`, or `--init-only`. `--cloud` is rejected with a session ID or URL, and in non-interactive runs when it carries a description. A bare `--cloud` is treated as absent. From a terminal, you can pass the task as the `--cloud` description instead of a positional prompt.

## Example script

The script below runs the full loop against `$CLAUDE_TEST_ENVIRONMENT_ID`, your test environment's `ccpool_...` ID, shown in the environment's detail dialog on the admin page or returned by the [create-environment call](#create-a-dedicated-test-environment), and asserts on a sentinel phrase in each reply. Run it from a git checkout of the repository you want the session to work in, after starting a runner on this host with the capture hook installed and `E2E_REPLY_DIR` exported.

```bash theme={null}
#!/usr/bin/env bash
# End-to-end test against a self-hosted environment, using Stop-hook read-back.
# Prereqs: `claude auth login` has been run on this machine (see "Authenticate
# from CI" below); jq is installed; CLAUDE_TEST_ENVIRONMENT_ID names an
# environment whose runner is the one on this host, with the capture hook
# installed and E2E_REPLY_DIR in its environment.

set -euo pipefail

: "${CLAUDE_TEST_ENVIRONMENT_ID:=${CLAUDE_TEST_POOL_ID:-}}"  # CLAUDE_TEST_POOL_ID is the legacy spelling
: "${CLAUDE_TEST_ENVIRONMENT_ID:?set CLAUDE_TEST_ENVIRONMENT_ID to a ccpool_... id served by a runner on this host}"
: "${E2E_REPLY_DIR:?set E2E_REPLY_DIR to the directory the Stop hook on your test runner writes to, and export it to the runner process}"
: "${TEST_REPO_REF:=main}"

[ -d "$E2E_REPLY_DIR" ] || {
  echo "FAIL: E2E_REPLY_DIR ($E2E_REPLY_DIR) does not exist. The Stop hook on the runner needs it." >&2
  exit 1
}

# Waits until $E2E_REPLY_DIR/<session_id>.txt contains $2, or fails after
# 90 seconds. Tune the timeout to your environment's cold-start time. The
# file is written by the Stop hook on the runner.
await_reply() {
  local expect="$2" f="$E2E_REPLY_DIR/$1.txt"
  local deadline=$(($(date +%s) + 90))
  while :; do
    if [ -f "$f" ] && grep -qF -- "$expect" "$f"; then
      return
    fi
    [ "$(date +%s)" -lt "$deadline" ] || {
      echo "FAIL: '$expect' not in $f within 90s. The Stop hook on the runner did not write it." >&2
      echo "-- $E2E_REPLY_DIR contents --" >&2; ls -la "$E2E_REPLY_DIR" >&2
      [ -f "$f" ] && { echo "-- $f --" >&2; cat "$f" >&2; }
      exit 1
    }
    sleep 1
  done
}

# 1. Create the session on the test environment. Run from a git checkout
# so the CLI can auto-detect the repo. --ref pins the checkout to a named
# ref regardless of local HEAD.
TURN1="e2e-probe-$(date +%s)-$$: say exactly 'ok: custom tools are reachable' and nothing else"
EXPECT1="ok: custom tools are reachable"
create_json=$(claude -p "$TURN1" --environment "$CLAUDE_TEST_ENVIRONMENT_ID" \
  --ref "$TEST_REPO_REF" --output-format json)
echo "create: $create_json"
SESSION_ID=$(jq -er '.session_id' <<<"$create_json")

# 2. Wait for the turn-1 reply.
await_reply "$SESSION_ID" "$EXPECT1"
echo "turn-1 reply ok"

# 3. Post a follow-up via the CLI.
TURN2="e2e-probe-followup-$(date +%s): say exactly 'ok: follow-up delivered' and nothing else"
EXPECT2="ok: follow-up delivered"
followup_json=$(claude -p "$TURN2" --cloud "$SESSION_ID" --output-format json)
echo "followup: $followup_json"
jq -e '.ok == true' <<<"$followup_json" >/dev/null

# 4. Wait for the turn-2 reply.
await_reply "$SESSION_ID" "$EXPECT2"
echo "turn-2 reply ok"

echo "PASS: test-environment round-trip (session $SESSION_ID)"
```

Replace the `TURN1`/`TURN2` prompts and `EXPECT1`/`EXPECT2` sentinels with whatever exercises your setup, such as asking Claude to run one of your custom MCP tools and asserting on its output.

## Remote test runners

If your test runners are on separate infrastructure, such as a persistent Kubernetes fleet your CI job can't share a filesystem with, swap the file write in the Stop hook for a POST to an endpoint your driver listens on:

```sh theme={null}
#!/bin/sh
# Variant of the capture hook for runners on separate infrastructure.
# Set E2E_REPLY_URL on the runner to an endpoint the driver controls.
[ -n "${E2E_REPLY_URL:-}" ] || exit 0
sid=$(printf '%s' "${CLAUDE_CODE_REMOTE_SESSION_ID:-}" | sed 's/^cse_/session_/')
[ -n "$sid" ] || exit 0
jq -r '.last_assistant_message // empty' | \
  curl -fsS -X POST --data-binary @- "$E2E_REPLY_URL/$sid" >/dev/null 2>&1
exit 0
```

On the driver side, run anything that accepts the POST and holds the reply until the test asks for it, such as a small HTTP listener inside the CI job or a webhook receiver you already run. The hook runs on your infrastructure, so the endpoint only needs to be reachable from your runners.

## Authenticate from CI

Both `claude -p ... --environment` and `claude -p ... --cloud` authenticate with a claude.ai OAuth token; API keys, such as `sk-ant-xxxxx`, aren't accepted for either call. Two approaches make a token available in CI.

### Long-lived CI host

Run `claude auth login` once interactively on the machine that executes the script, using a dedicated user account for automation. The token lives in the OS keychain on macOS, or in `~/.claude/.credentials.json` on Linux and Windows. The CLI refreshes the short-lived access token automatically on each invocation, but the underlying refresh-token grant is capped at 30 days from the initial login, so re-run `claude auth login` interactively on that host every 30 days.

### Ephemeral CI runners

There is no long-lived CI token for this today. The scope that grants remote-session control, `user:sessions:claude_code`, is capped server-side at 30 days, so `claude setup-token`, which mints a one-year inference-only token, doesn't cover it. The [environment secret](/docs/en/self-hosted-environments-quickstart#set-up-an-environment-and-runner) isn't accepted either, since it only authorizes a runner to register with the environment, not to create sessions.

To provision a stored login onto an ephemeral runner, set [`CLAUDE_CODE_OAUTH_REFRESH_TOKEN` and `CLAUDE_CODE_OAUTH_SCOPES`](/docs/en/env-vars#variables) so `claude auth login` exchanges the token without a browser; the same 30-day cap applies to the refresh grant. Contact your Anthropic account team if you need a machine-identity path that isn't bound to a human account.

## Create a dedicated test environment

Create and delete environments programmatically so each CI run gets a clean one; the runner your CI job starts registers into the fresh environment. The create and delete calls below are the same endpoints that the **Cloud environments** admin page on claude.ai uses, and they require the `anthropic-beta: ccr-byoc-2025-07-29` header.

### Mint the admin token

`$ADMIN_TOKEN` is a claude.ai OAuth access token for an account that holds an Owner or admin role, minted the same way as [Authenticate from CI](#authenticate-from-ci):

* **Mint it**: run `claude auth login` with an account that holds an Owner or admin role, then read the current access token from the OS keychain on macOS or `~/.claude/.credentials.json` on Linux and Windows.
* **Read it fresh each run**: the CLI rotates the access token, and the same 30-day refresh-grant cap applies, so don't store a copy.
* **Pass it via stdin**: as the example does, so the token never lands in curl's argument list or your build log.

### Create the environment

Capture the response without echoing it: `pool_secret` is a long-lived credential that can register runners into the environment, so store it as a masked CI secret and print only the environment ID. The `-H @-` form that keeps the token out of the process list requires curl 7.55 or later; older curl treats `@-` as a literal header and sends the request without authorization.

```bash theme={null}
create=$(curl -fsS -X POST -H @- \
  -H "anthropic-beta: ccr-byoc-2025-07-29" -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"name":"ci-test-environment"}' \
  https://api.anthropic.com/v1/code/runners/self-hosted/pools \
  <<<"Authorization: Bearer $ADMIN_TOKEN")
ENVIRONMENT_ID=$(jq -er .pool.pool_id <<<"$create")
ENVIRONMENT_SECRET=$(jq -er .pool_secret <<<"$create")
```

Until an [Owner or admin turns on **Allow self-hosted environments**](/docs/en/self-hosted-environments#availability-and-limitations) for the organization, the call fails with a `403` `permission_error` reading `self-hosted runners are disabled by your organization's policy`.

Start a runner on this host with `SELF_HOSTED_RUNNER_ENVIRONMENT_SECRET=$ENVIRONMENT_SECRET`, plus the capture hook and `E2E_REPLY_DIR` per [Install the capture hook](#install-the-capture-hook-on-your-test-runner), then run the test script.

### Delete the environment

Delete the environment when the run finishes, so each CI run starts clean:

```bash theme={null}
curl -fsS -X DELETE -H @- \
  -H "anthropic-beta: ccr-byoc-2025-07-29" -H "anthropic-version: 2023-06-01" \
  "https://api.anthropic.com/v1/code/runners/self-hosted/pools/$ENVIRONMENT_ID" \
  <<<"Authorization: Bearer $ADMIN_TOKEN"
```
