# Cloud sandbox reference

Pre-installed packages, databases, and utilities available in cloud sandboxes.

---

Cloud sandboxes run as isolated Linux containers on Anthropic-managed infrastructure. They come pre-installed with a comprehensive set of programming languages, databases, and utilities. The agent can use these immediately without any installation steps.

These specifications apply to `cloud` environments. Self-hosted sandboxes run on your infrastructure with whatever your worker provides.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Programming languages

| Language | Version | Package manager |
| -------- | ------- | --------------- |
| Python   | 3.12+   | pip, uv         |
| Node.js  | 20+     | npm, yarn, pnpm |
| Go       | 1.22+   | go modules      |
| Rust     | 1.77+   | cargo           |
| Java     | 21+     | maven, gradle   |
| Ruby     | 3.3+    | bundler, gem    |
| PHP      | 8.3+    | composer        |
| C/C++    | GCC 13+ | make, cmake     |

## Databases

| Database          | Description                                        |
| ----------------- | -------------------------------------------------- |
| SQLite            | Pre-installed, available immediately               |
| PostgreSQL client | `psql` client for connecting to external databases |
| Redis client      | `redis-cli` for connecting to external instances   |

<Note>
  Database servers (such as PostgreSQL and Redis) are not running in the sandbox by default. The sandbox includes client tools for connecting to external database instances. SQLite is fully available for local use.
</Note>

## Utilities

### System tools

* `git` - Version control
* `curl`, `wget` - HTTP clients
* `jq` - JSON processing
* `tar`, `zip`, `unzip` - Archive tools
* `ssh`, `scp` - Remote access (requires network enabled)
* `tmux`, `screen` - Terminal multiplexers

### Development tools

* `make`, `cmake` - Build systems
* `docker` - Container management (limited availability)
* `ripgrep` (`rg`) - Fast file search
* `tree` - Directory visualization
* `htop` - Process monitoring

### Text processing

* `sed`, `awk`, `grep` - Stream editors
* `vim`, `nano` - Text editors
* `diff`, `patch` - File comparison

## Sandbox specifications

| Property         | Value                                              |
| ---------------- | -------------------------------------------------- |
| Operating system | Ubuntu 22.04 LTS                                   |
| Architecture     | x86\_64 (amd64)                                    |
| Memory           | Up to 8 GB                                         |
| Disk space       | Up to 10 GB                                        |
| Network          | Disabled by default (enable in environment config) |
