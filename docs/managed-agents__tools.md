---
title: Tools
url: https://platform.claude.com/docs/en/managed-agents/tools
description: Configure tools available to your agent.
---

Claude Managed Agents provides a set of built-in tools that Claude can use autonomously within a [session](https://platform.claude.com/docs/en/managed-agents/sessions). You control which tools are available by specifying them in the agent configuration.

Claude Managed Agents also supports custom, user-defined tools. Your application executes these tools separately and returns the results to Claude, which uses them to continue the task. To give the agent tools from an MCP server, use the [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector) instead.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Available tools

The agent toolset includes the following tools. All are enabled by default when you include the toolset in your agent configuration. Each entry in the `configs` array is identified by its `name`, using the values in the Name column, and accepts an optional `type` field with the same value. The `web_search` and `web_fetch` entries accept additional settings; see [Restrict web search and web fetch domains](https://platform.claude.com/docs/en/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

| Tool       | Name         | Description                                    |
| ---------- | ------------ | ---------------------------------------------- |
| Bash       | `bash`       | Execute bash commands in a shell session       |
| Read       | `read`       | Read a file from the sandbox filesystem        |
| Write      | `write`      | Write a file to the sandbox filesystem         |
| Edit       | `edit`       | Perform string replacement in a file           |
| Glob       | `glob`       | Fast file pattern matching using glob patterns |
| Grep       | `grep`       | Text search using regex patterns               |
| Web fetch  | `web_fetch`  | Fetch content from a URL                       |
| Web search | `web_search` | Search the web for information                 |

When a tool output exceeds 100,000 characters (about 25,000 tokens), it is automatically written to a file in the [sandbox](https://platform.claude.com/docs/en/managed-agents/environments). The model receives a truncated preview with the file path and can read the full content from there.

## Configuring the toolset

Enable the full toolset with `agent_toolset_20260401` when creating an agent. Use the `configs` array to disable specific tools or override their settings. Each config entry can also set a `permission_policy` that controls whether the tool's calls are auto-approved or require confirmation. See [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies) for the available policy types.

Config entries for `web_search` and `web_fetch` also accept domain filters and other web settings; see [Restrict web search and web fetch domains](https://platform.claude.com/docs/en/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Coding Assistant",
    "model": "claude-opus-5",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "configs": [
          {"name": "web_fetch", "enabled": false}
        ]
      }
    ]
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Coding Assistant
  model: claude-opus-5
  tools:
    - type: agent_toolset_20260401
      configs:
        - name: web_fetch
          enabled: false
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
              "configs": [
                  {"name": "web_fetch", "enabled": False},
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-5",
    tools: [
      {
        type: "agent_toolset_20260401",
        configs: [{ name: "web_fetch", enabled: false }]
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = new("claude-opus-5"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
              Configs =
              [
                  new BetaManagedAgentsWebFetchToolConfigParams { Enabled = false },
              ],
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Coding Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-5",
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			Configs: []anthropic.BetaManagedAgentsAgentToolConfigParamsUnion{{
  				OfWebFetch: &anthropic.BetaManagedAgentsWebFetchToolConfigParams{
  					Enabled: anthropic.Bool(false),
  				},
  			}},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Coding Assistant")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .addConfig(BetaManagedAgentsWebFetchToolConfigParams.builder()
              .enabled(false)
              .build())
          .build())
      .build());
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebFetchToolConfigParams;

  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
              configs: [
                  BetaManagedAgentsWebFetchToolConfigParams::with(enabled: false),
              ],
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-5",
    tools: [
      {
        type: :agent_toolset_20260401,
        configs: [
          {name: :web_fetch, enabled: false}
        ]
      }
    ]
  )
  ```
</CodeGroup>

### Disabling specific tools

To disable a tool, set `enabled: false` in its config entry in the toolset object of your agent's `tools` array:

```json
{
  "type": "agent_toolset_20260401",
  "configs": [
    { "name": "web_fetch", "enabled": false },
    { "name": "web_search", "enabled": false }
  ]
}
```

### Enabling only specific tools

The `default_config` object sets the baseline for every tool in the set, and per-tool `configs` entries override it. To start with everything off and enable only what you need, set `default_config.enabled` to `false`:

```json
{
  "type": "agent_toolset_20260401",
  "default_config": { "enabled": false },
  "configs": [
    { "name": "bash", "enabled": true },
    { "name": "read", "enabled": true },
    { "name": "write", "enabled": true }
  ]
}
```

### Restrict web search and web fetch domains

To control which sites the agent's web tools can reach, set `allowed_domains` (the tool can reach only these hosts) or `blocked_domains` (the tool can never reach these hosts) on the `web_search` and `web_fetch` entries of the toolset's `configs` array. Each tool carries its own list, so `web_search` and `web_fetch` can have different restrictions. A listed domain covers that host and all of its subdomains. At runtime, a `web_fetch` call for a URL that its lists do not permit returns an error result to the agent (`is_error: true` on the `agent.tool_result` event, with content that names the error code `url_not_allowed`), and `web_search` omits results that its lists do not permit.

The following toolset limits `web_search` to two sites and localizes its results, and blocks one host for `web_fetch` while capping how much fetched content enters the context:

```json
{
  "type": "agent_toolset_20260401",
  "configs": [
    {
      "type": "web_search",
      "name": "web_search",
      "allowed_domains": ["docs.example.com", "arxiv.org"],
      "user_location": {
        "type": "approximate",
        "country": "US",
        "timezone": "America/Los_Angeles"
      }
    },
    {
      "type": "web_fetch",
      "name": "web_fetch",
      "blocked_domains": ["ads.example.com"],
      "max_content_tokens": 50000
    }
  ]
}
```

<Note>
  In the Python, TypeScript, Go, Java, C#, Ruby, and PHP SDKs, each `configs` entry is typed per tool: a union with one member per built-in tool, discriminated by `type`. `type` is optional when you construct an entry (the server infers it from `name`) and always present on responses. This typing does not change the JSON that an entry serializes to, so a request whose entries set only `name`, `enabled`, and `permission_policy` is valid with or without `type`. In SDKs where you construct entries from typed values rather than plain dictionaries or hashes (Go, Java, C#, and PHP), the element type of `configs` is the union itself: build each entry from its per-tool member type.
</Note>

The following request creates an agent with this toolset and prints the `configs` array from the response:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Research Agent",
    "model": "claude-opus-5",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "configs": [
          {
            "type": "web_search",
            "name": "web_search",
            "allowed_domains": ["docs.example.com", "arxiv.org"],
            "user_location": {
              "type": "approximate",
              "country": "US",
              "timezone": "America/Los_Angeles"
            }
          },
          {
            "type": "web_fetch",
            "name": "web_fetch",
            "blocked_domains": ["ads.example.com"],
            "max_content_tokens": 50000
          }
        ]
      }
    ]
  }
  EOF
  )
  jq '.tools[0].configs' <<< "$agent"
  ```

  ```bash CLI
  ant beta:agents create --transform tools.0.configs <<'YAML'
  name: Research Agent
  model: claude-opus-5
  tools:
    - type: agent_toolset_20260401
      configs:
        - type: web_search
          name: web_search
          allowed_domains: [docs.example.com, arxiv.org]
          user_location:
            type: approximate
            country: US
            timezone: America/Los_Angeles
        - type: web_fetch
          name: web_fetch
          blocked_domains: [ads.example.com]
          max_content_tokens: 50000
  YAML
  ```

  ```python Python
  client = Anthropic()

  agent = client.beta.agents.create(
      name="Research Agent",
      model="claude-opus-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
              "configs": [
                  {
                      "name": "web_search",
                      "allowed_domains": ["docs.example.com", "arxiv.org"],
                      "user_location": {
                          "type": "approximate",
                          "country": "US",
                          "timezone": "America/Los_Angeles",
                      },
                  },
                  {
                      "name": "web_fetch",
                      "blocked_domains": ["ads.example.com"],
                      "max_content_tokens": 50_000,
                  },
              ],
          }
      ],
  )

  for tool in agent.tools:
      if tool.type == "agent_toolset_20260401":
          print(json.dumps([config.to_dict() for config in tool.configs], indent=2))
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const agent = await client.beta.agents.create({
    name: "Research Agent",
    model: "claude-opus-5",
    tools: [
      {
        type: "agent_toolset_20260401",
        configs: [
          {
            name: "web_search",
            allowed_domains: ["docs.example.com", "arxiv.org"],
            user_location: {
              type: "approximate",
              country: "US",
              timezone: "America/Los_Angeles"
            }
          },
          {
            name: "web_fetch",
            blocked_domains: ["ads.example.com"],
            max_content_tokens: 50_000
          }
        ]
      }
    ]
  });

  for (const tool of agent.tools) {
    if (tool.type === "agent_toolset_20260401") {
      console.log(JSON.stringify(tool.configs, null, 2));
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Agents;

  AnthropicClient client = new();

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Research Agent",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
              Configs =
              [
                  new BetaManagedAgentsWebSearchToolConfigParams
                  {
                      AllowedDomains = ["docs.example.com", "arxiv.org"],
                      UserLocation = new()
                      {
                          Country = "US",
                          Timezone = "America/Los_Angeles",
                      },
                  },
                  new BetaManagedAgentsWebFetchToolConfigParams
                  {
                      BlockedDomains = ["ads.example.com"],
                      MaxContentTokens = 50_000,
                  },
              ],
          },
      ],
  });

  JsonSerializerOptions jsonOptions = new() { WriteIndented = true };
  foreach (var tool in agent.Tools)
  {
      if (tool.TryPickBetaManagedAgentsAgentToolset20260401(out var toolset))
      {
          Console.WriteLine(JsonSerializer.Serialize(toolset.Configs, jsonOptions));
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Research Agent",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			Configs: []anthropic.BetaManagedAgentsAgentToolConfigParamsUnion{
  				{OfWebSearch: &anthropic.BetaManagedAgentsWebSearchToolConfigParams{
  					AllowedDomains: []string{"docs.example.com", "arxiv.org"},
  					UserLocation: anthropic.BetaManagedAgentsUserLocationParam{
  						Country:  anthropic.String("US"),
  						Timezone: anthropic.String("America/Los_Angeles"),
  					},
  				}},
  				{OfWebFetch: &anthropic.BetaManagedAgentsWebFetchToolConfigParams{
  					BlockedDomains:   []string{"ads.example.com"},
  					MaxContentTokens: anthropic.Int(50000),
  				}},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }

  for _, tool := range agent.Tools {
  	switch toolset := tool.AsAny().(type) {
  	case anthropic.BetaManagedAgentsAgentToolset20260401:
  		configs := make([]json.RawMessage, len(toolset.Configs))
  		for i, config := range toolset.Configs {
  			configs[i] = json.RawMessage(config.RawJSON())
  		}
  		output, err := json.MarshalIndent(configs, "", "  ")
  		if err != nil {
  			panic(err)
  		}
  		fmt.Println(string(output))
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.agents.AgentCreateParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
  import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
  import com.anthropic.models.beta.agents.BetaManagedAgentsUserLocation;
  import com.anthropic.models.beta.agents.BetaManagedAgentsWebFetchToolConfigParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsWebSearchToolConfigParams;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var agent = client.beta().agents().create(AgentCreateParams.builder()
          .name("Research Agent")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
              .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
              .addConfig(BetaManagedAgentsWebSearchToolConfigParams.builder()
                  .allowedDomains(List.of("docs.example.com", "arxiv.org"))
                  .userLocation(BetaManagedAgentsUserLocation.builder()
                      .country("US")
                      .timezone("America/Los_Angeles")
                      .build())
                  .build())
              .addConfig(BetaManagedAgentsWebFetchToolConfigParams.builder()
                  .blockedDomains(List.of("ads.example.com"))
                  .maxContentTokens(50_000)
                  .build())
              .build())
          .build());

      for (var tool : agent.tools()) {
          if (tool.isAgentToolset20260401()) {
              var configs = tool.asAgentToolset20260401().configs();
              IO.println(ObjectMappers.jsonMapper().valueToTree(configs));
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsUserLocation;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebFetchToolConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebSearchToolConfigParams;
  // ...

  $client = new Client();

  $agent = $client->beta->agents->create(
      name: 'Research Agent',
      model: 'claude-opus-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
              configs: [
                  BetaManagedAgentsWebSearchToolConfigParams::with(
                      allowedDomains: ['docs.example.com', 'arxiv.org'],
                      userLocation: BetaManagedAgentsUserLocation::with(
                          country: 'US',
                          timezone: 'America/Los_Angeles',
                      ),
                  ),
                  BetaManagedAgentsWebFetchToolConfigParams::with(
                      blockedDomains: ['ads.example.com'],
                      maxContentTokens: 50_000,
                  ),
              ],
          ),
      ],
  );

  foreach ($agent->tools as $tool) {
      if ($tool instanceof BetaManagedAgentsAgentToolset20260401) {
          echo json_encode($tool->configs, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  agent = client.beta.agents.create(
    name: "Research Agent",
    model: "claude-opus-5",
    tools: [
      {
        type: :agent_toolset_20260401,
        configs: [
          {
            name: :web_search,
            allowed_domains: ["docs.example.com", "arxiv.org"],
            user_location: {type: :approximate, country: "US", timezone: "America/Los_Angeles"}
          },
          {
            name: :web_fetch,
            blocked_domains: ["ads.example.com"],
            max_content_tokens: 50_000
          }
        ]
      }
    ]
  )

  case agent.tools.first
  in Anthropic::Models::Beta::BetaManagedAgentsAgentToolset20260401 => toolset
    puts JSON.pretty_generate(toolset.configs.map(&:to_h))
  end
  ```
</CodeGroup>

In the Claude Console, set allowed or blocked domains from the `web_search` and `web_fetch` rows of the **Built-in tools** card on the agent form; set `max_content_tokens` and `user_location` in the **Raw** view of the agent's configuration.

In addition to `enabled` and `permission_policy`, the web tool entries accept the following settings:

| Setting              | Applies to                | Description                                                                                                                                                                                                     |
| -------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_domains`    | `web_search`, `web_fetch` | The only hosts the tool can reach. Cannot be combined with `blocked_domains` on the same entry.                                                                                                                 |
| `blocked_domains`    | `web_search`, `web_fetch` | Hosts the tool cannot reach.                                                                                                                                                                                    |
| `max_content_tokens` | `web_fetch`               | Caps the amount of fetched page content included in the context. Must be a positive integer. See [content limits](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool#content-limits). |
| `user_location`      | `web_search`              | Localizes search results. An object with the same fields as the Messages API [`user_location`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool#localization) parameter.           |

<Note>
  An environment's [`networking`](https://platform.claude.com/docs/en/managed-agents/environments#networking) settings control the sandbox's own outbound traffic. They do not affect `web_search` or `web_fetch`, which run on Anthropic's servers whether the environment is a cloud or self-hosted sandbox. The per-tool `allowed_domains` and `blocked_domains` lists are the way to restrict what these tools can reach.
</Note>

<Note>
  Organization-level web search and web fetch settings in the Claude Console apply to the Messages API and do not apply to Managed Agents sessions. To restrict an agent's web tools, configure `allowed_domains` or `blocked_domains` on its toolset instead.
</Note>

#### Domain list rules

* Set either `allowed_domains` or `blocked_domains` on an entry, not both. An entry that sets both is rejected.
* Each list holds 1 to 64 domains, each 1 to 255 characters. An empty list is rejected: to apply no restriction, omit the field or send `null`.
* Each domain is a registrable domain name, or a subdomain of one, written as a plain hostname: ASCII letters, digits, hyphens, underscores, and dots, with no scheme, port, credentials, wildcard, or whitespace, no label that begins or ends with a hyphen, and no path other than the optional `web_search` path suffix described later in this list. Use `example.com`, not `https://example.com`, `example.com:443`, or `*.example.com`. Hostnames are compared without regard to case, and a single trailing `/` is ignored.
* A listed domain matches that host and its subdomains: `example.com` covers `docs.example.com`, but `docs.example.com` does not cover `example.com` or `api.example.com`. A leading `www.` is a subdomain like any other, so `www.example.com` does not cover `example.com`; list the bare domain to cover both.
* IP addresses are not accepted in any form, whether IPv4, IPv6, bracketed, or numeric shorthand such as `127.1`. List the site's domain name instead.
* A bare top-level domain or registry suffix such as `com`, `co.uk`, or `gov.uk` is rejected, and so is a single-label name such as `intranet`. List a full domain such as `example.co.uk`.
* `localhost` and hosts ending in `.localhost`, `.local`, `.internal`, `.localdomain`, or `.invalid` are rejected.
* Use the `xn--` (Punycode) form for internationalized domain names; a domain that contains non-ASCII characters is rejected.
* A `web_fetch` domain cannot include a path: use `example.com`, not `example.com/*`. A `web_search` domain can carry a path suffix such as `example.com/blog`, in which the path cannot contain spaces, `?`, `#`, or any of the characters `$ , | ^ !`. Prefer plain hostnames for `web_search` too, because the search provider matches path suffixes as URL patterns rather than as strict host rules.
* Duplicate domains within a list are rejected. `www.example.com` and `example.com` count as different domains; see the earlier matching rule for what each covers.

#### When settings are validated

Format and limit violations are rejected with a 400 `invalid_request_error` when you [create an agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#create-an-agent) or [update an agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#update-an-agent), and when you create or update a session that supplies `tools`. For example, the message for an entry that sets both lists includes `Only one of allowed_domains or blocked_domains may be set.`, and the message for an empty list includes `allowed_domains: Empty list of domains is ambiguous. Provide at least one domain or null.` The message for a domain that breaks a format rule names its list and zero-based position, for example `allowed_domains.0: IP addresses are not supported; provide a plain hostname like "example.com"`.

The same requests also reject three settings that depend on the search and fetch providers: a domain in `allowed_domains` that Anthropic's crawler is not permitted to access, a `user_location.country` that the search provider does not support (the message ends in `user_location.country: not a country the search provider supports`), and a `user_location.timezone` that is not a valid IANA name. The session checks the configuration again when it first initializes the tool; if a setting that was accepted earlier is no longer valid at that point, the session emits a [`session.error`](https://platform.claude.com/docs/en/managed-agents/events-and-streaming) event and returns to `idle` without retrying. Fix the setting by [updating the session's tools](https://platform.claude.com/docs/en/managed-agents/session-operations#updating-the-agent-configuration), update the agent as well so that new sessions start with the corrected configuration, then send a new `user.message` to continue.

#### Multiagent sessions, outcomes, and mid-session updates

In a [multiagent session](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration), every domain list that applies to a thread is enforced at the same time: an agent in the roster of the coordinator is bound by its own `allowed_domains` and `blocked_domains`, by those of any agent that called it, and by the coordinator's current lists.

* Allowlists combine to the domains that all of them cover, and blocklists add together, so a roster agent can narrow what a tool reaches but never widen it. For example, a roster agent that sets `blocked_domains` keeps the coordinator's `allowed_domains` and blocks those hosts within it, and a roster agent that sets its own `allowed_domains` can reach only the hosts that both its list and the coordinator's list cover.
* If the combined allowlists have no domain in common, the tool stays available to that agent but every call fails with a `url_not_allowed` error stating that no domain is permitted, and the tool description tells the model so. Keep each roster agent's allowlist inside the coordinator's to avoid this.
* `max_content_tokens` and `user_location` are not combined: a thread uses the value from its own tool configuration if set, otherwise from the agent that called it, otherwise from the coordinator's current configuration.
* A `{"type": "self"}` roster entry has no web settings of its own and follows the coordinator's current settings.
* The grader in [outcome-driven sessions](https://platform.claude.com/docs/en/managed-agents/define-outcomes) runs without `web_search` and `web_fetch`, regardless of these settings.
* You can change the lists on an idle session by [updating its tools](https://platform.claude.com/docs/en/managed-agents/session-operations#updating-the-agent-configuration). The new lists apply to the rest of the session; in a multiagent session, every thread applies them from its next turn, while a roster agent's own lists stay as its agent definition set them when the session was created.

#### Differences from the Messages API tools

These settings use the same `allowed_domains` and `blocked_domains` vocabulary as [domain filtering](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools#domain-filtering) on the Messages API server tools, with the following differences on Managed Agents:

* Each list is capped at 64 domains.
* Domains listed for `web_fetch` cannot include a path.
* `max_uses`, `citations`, and `cache_control` are not available on the toolset.

## Custom tools

In addition to built-in tools, you can define custom tools. Custom tools are analogous to [user-defined client tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) in the Messages API.

Each custom tool defines a contract: you specify what operations are available and what they return, and Claude determines when and how to call them. The model never executes anything on its own. It emits a structured request, your code runs the operation, and the result flows back into the conversation. See [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#handling-custom-tool-calls) for how to receive custom tool calls and return results during a session.

If your sessions run in a self-hosted sandbox, the environment worker can [serve custom tools from your sandbox](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#serve-custom-tools-from-your-sandbox), including tools that wrap an MCP server inside your network.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Weather Agent",
    "model": "claude-opus-5",
    "tools": [
      {
        "type": "agent_toolset_20260401"
      },
      {
        "type": "custom",
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name"}
          },
          "required": ["location"]
        }
      }
    ]
  }
  EOF
  )
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:agents create < agent.yaml
    ```

    <File filename="agent.yaml">
      ```yaml
      name: Weather Agent
      model: claude-opus-5
      tools:
        - type: agent_toolset_20260401
        - type: custom
          name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required:
              - location
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Weather Agent",
      model="claude-opus-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
          },
          {
              "type": "custom",
              "name": "get_weather",
              "description": "Get current weather for a location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string", "description": "City name"},
                  },
                  "required": ["location"],
              },
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Weather Agent",
    model: "claude-opus-5",
    tools: [
      { type: "agent_toolset_20260401" },
      {
        type: "custom",
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: { location: { type: "string", description: "City name" } },
          required: ["location"]
        }
      }
    ]
  });
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Weather Agent",
      Model = new("claude-opus-5"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsCustomToolParams
          {
              Type = "custom",
              Name = "get_weather",
              Description = "Get current weather for a location",
              InputSchema = new()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(
                          new { type = "string", description = "City name" }
                      ),
                  },
                  Required = ["location"],
              },
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Weather Agent",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-5",
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}, {
  		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
  			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
  			Name:        "get_weather",
  			Description: "Get current weather for a location",
  			InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "City name",
  					},
  				},
  				Required: []string{"location"},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;
  import java.util.Map;

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Weather Agent")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .build())
      .addTool(BetaManagedAgentsCustomToolParams.builder()
          .type(BetaManagedAgentsCustomToolParams.Type.CUSTOM)
          .name("get_weather")
          .description("Get current weather for a location")
          .inputSchema(BetaManagedAgentsCustomToolInputSchema.builder()
              .properties(BetaManagedAgentsCustomToolInputSchema.Properties.builder()
                  .putAdditionalProperty("location", JsonValue.from(Map.of(
                      "type", "string",
                      "description", "City name")))
                  .build())
              .addRequired("location")
              .build())
          .build())
      .build());
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolInputSchema;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolParams;

  $agent = $client->beta->agents->create(
      name: 'Weather Agent',
      model: 'claude-opus-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
          BetaManagedAgentsCustomToolParams::with(
              type: 'custom',
              name: 'get_weather',
              description: 'Get current weather for a location',
              inputSchema: BetaManagedAgentsCustomToolInputSchema::with(
                  properties: ['location' => ['type' => 'string', 'description' => 'City name']],
                  required: ['location'],
              ),
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Weather Agent",
    model: "claude-opus-5",
    tools: [
      {type: :agent_toolset_20260401},
      {
        type: :custom,
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: :object,
          properties: {location: {type: "string", description: "City name"}},
          required: ["location"]
        }
      }
    ]
  )
  ```
</CodeGroup>

Once you've defined custom tools on the agent, the agent invokes them during a session.

### Best practices for custom tool definitions

* **Provide extremely detailed descriptions.** This is by far the most important factor in tool performance. Your descriptions should explain what the tool does and when to use it (and when not to). Explain what each parameter means and how it affects the tool's behavior. Call out any important caveats or limitations. The more context you can give Claude about your tools, the better it is at determining when and how to use them. Aim for three to four sentences for each tool description, more if the tool is complex.
* **Consolidate related operations into fewer tools.** Rather than creating a separate tool for every action (`create_pr`, `review_pr`, `merge_pr`), group them into a single tool with an `action` parameter. Fewer, more capable tools reduce selection ambiguity and make your tool surface easier for Claude to navigate.
* **Use meaningful namespacing in tool names.** When your tools span multiple services or resources, prefix names with the resource (for example, `db_query` or `storage_read`). This makes tool selection unambiguous as your library grows.
* **Design tool responses to return only high-signal information.** Return semantic, stable identifiers (for example, slugs or UUIDs) rather than opaque internal references, and include only the fields Claude needs to determine its next step. Bloated responses waste context and make it harder for Claude to extract what matters.

## Next steps

<CardGroup cols={2}>
  <Card title="MCP connector" icon="link" href="https://platform.claude.com/docs/en/managed-agents/mcp-connector">
    Connect MCP servers to your agents for access to external tools and data sources.
  </Card>

  <Card title="Permission policies" icon="lock" href="https://platform.claude.com/docs/en/managed-agents/permission-policies">
    Control when agent and MCP tools execute.
  </Card>

  <Card title="Session event stream" icon="lightning" href="https://platform.claude.com/docs/en/managed-agents/events-and-streaming">
    Send events, stream responses, and interrupt or redirect your session mid-execution.
  </Card>
</CardGroup>
