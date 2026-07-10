# Cloud environment setup

Customize cloud sandboxes for your sessions.

---

Environments define the sandbox configuration where your agent runs. You create an environment once, then reference its ID each time you start a session. Multiple sessions can share the same environment, but each session gets its own isolated sandbox (a fresh Linux container).

This page covers `type: cloud` environments. To run sandboxes on your own infrastructure, see [Self-hosted sandboxes](/docs/en/managed-agents/self-hosted-sandboxes).

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Create an environment

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  environment=$(curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<'EOF'
  {
    "name": "python-dev",
    "config": {
      "type": "cloud",
      "networking": {"type": "unrestricted"}
    }
  }
  EOF
  )
  environment_id=$(jq -r '.id' <<< "$environment")

  echo "Environment ID: $environment_id"
  ```

  ```bash CLI
  ant beta:environments create \
    --name "python-dev" \
    --config '{type: cloud, networking: {type: unrestricted}}'
  ```

  ```python Python
  environment = client.beta.environments.create(
      name="python-dev",
      config={
          "type": "cloud",
          "networking": {"type": "unrestricted"},
      },
  )

  print(f"Environment ID: {environment.id}")
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "python-dev",
    config: {
      type: "cloud",
      networking: { type: "unrestricted" },
    },
  });

  console.log(`Environment ID: ${environment.id}`);
  ```

  ```csharp C#
  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "python-dev",
      Config = new BetaCloudConfigParams
      {
          Networking = new BetaUnrestrictedNetwork(),
      },
  });

  Console.WriteLine($"Environment ID: {environment.ID}");
  ```

  ```go Go
  environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
  	Name: "python-dev",
  	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
  		OfCloud: &anthropic.BetaCloudConfigParams{
  			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
  				OfUnrestricted: &anthropic.BetaUnrestrictedNetworkParam{},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("Environment ID: %s\n", environment.ID)
  ```

  ```java Java
  var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
      .name("python-dev")
      .config(BetaCloudConfigParams.builder()
          .networking(BetaUnrestrictedNetwork.builder().build())
          .build())
      .build());
  IO.println("Environment ID: " + environment.id());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'python-dev',
      config: ['type' => 'cloud', 'networking' => ['type' => 'unrestricted']],
  );
  echo "Environment ID: {$environment->id}\n";
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "python-dev",
    config: {
      type: "cloud",
      networking: {type: "unrestricted"}
    }
  )

  puts "Environment ID: #{environment.id}"
  ```
</CodeGroup>

Use a unique, descriptive `name` so you can tell environments apart.

## Use the environment in a session

Pass the environment ID as a string when [creating a session](/docs/en/managed-agents/sessions).

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  session=$(curl -fsS https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id"
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id
  )
  ```
</CodeGroup>

## Configuration options

### Packages

The `packages` field pre-installs packages into the sandbox before the agent starts. Packages are installed by their respective package managers and cached across sessions that share the same environment. When multiple package managers are specified, they run in alphabetical order (apt, cargo, gem, go, npm, pip). You can optionally pin specific versions. Unpinned packages install the latest version.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  environment=$(curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<'EOF'
  {
    "name": "data-analysis",
    "config": {
      "type": "cloud",
      "packages": {
        "pip": ["pandas", "numpy", "scikit-learn"],
        "npm": ["express"]
      },
      "networking": {"type": "unrestricted"}
    }
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:environments create <<'YAML'
  name: data-analysis
  config:
    type: cloud
    packages:
      pip:
        - pandas
        - numpy
        - scikit-learn
      npm:
        - express
    networking:
      type: unrestricted
  YAML
  ```

  ```python Python
  environment = client.beta.environments.create(
      name="data-analysis",
      config={
          "type": "cloud",
          "packages": {
              "pip": ["pandas", "numpy", "scikit-learn"],
              "npm": ["express"],
          },
          "networking": {"type": "unrestricted"},
      },
  )
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "data-analysis",
    config: {
      type: "cloud",
      packages: {
        pip: ["pandas", "numpy", "scikit-learn"],
        npm: ["express"]
      },
      networking: { type: "unrestricted" }
    }
  });
  ```

  ```csharp C#
  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "data-analysis",
      Config = new BetaCloudConfigParams
      {
          Packages = new()
          {
              Pip = ["pandas", "numpy", "scikit-learn"],
              Npm = ["express"],
          },
          Networking = new BetaUnrestrictedNetwork(),
      },
  });
  ```

  ```go Go
  environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
  	Name: "data-analysis",
  	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
  		OfCloud: &anthropic.BetaCloudConfigParams{
  			Packages: anthropic.BetaPackagesParams{
  				Pip: []string{"pandas", "numpy", "scikit-learn"},
  				Npm: []string{"express"},
  			},
  			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
  				OfUnrestricted: &anthropic.BetaUnrestrictedNetworkParam{},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  _ = environment
  ```

  ```java Java
  var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
      .name("data-analysis")
      .config(BetaCloudConfigParams.builder()
          .packages(BetaPackagesParams.builder()
              .pip(List.of("pandas", "numpy", "scikit-learn"))
              .npm(List.of("express"))
              .build())
          .networking(BetaUnrestrictedNetwork.builder().build())
          .build())
      .build());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'data-analysis',
      config: [
          'type' => 'cloud',
          'packages' => [
              'pip' => ['pandas', 'numpy', 'scikit-learn'],
              'npm' => ['express'],
          ],
          'networking' => ['type' => 'unrestricted'],
      ],
  );
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "data-analysis",
    config: {
      type: "cloud",
      packages: {
        pip: %w[pandas numpy scikit-learn],
        npm: %w[express]
      },
      networking: {type: "unrestricted"}
    }
  )
  ```
</CodeGroup>

Supported package managers:

| Field   | Package manager           | Example                                     |
| ------- | ------------------------- | ------------------------------------------- |
| `apt`   | System packages (apt-get) | `"ffmpeg"`                                  |
| `cargo` | Rust (cargo)              | `"ripgrep@14.0.0"`                          |
| `gem`   | Ruby (gem)                | `"rails:7.1.0"`                             |
| `go`    | Go modules                | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm`   | Node.js (npm)             | `"express@4.18.0"`                          |
| `pip`   | Python (pip)              | `"pandas==2.2.0"`                           |

### Networking

The `networking` field controls the sandbox's outbound network access. It does not affect the allowed domains for the `web_search` or `web_fetch` tools.

| Mode           | Description                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `unrestricted` | Full outbound network access, except for a general safety blocklist. This is the default.                                                                    |
| `limited`      | Restricts sandbox network access to the hosts in `allowed_hosts`. Set `allow_package_managers` and `allow_mcp_servers` to `true` to allow additional access. |

The following example creates an environment with `limited` networking:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "api-access",
      "config": {
        "type": "cloud",
        "networking": {
          "type": "limited",
          "allowed_hosts": ["api.example.com"],
          "allow_mcp_servers": true,
          "allow_package_managers": true
        }
      }
    }'
  ```

  ```bash CLI
  ant beta:environments create <<'YAML'
  name: api-access
  config:
    type: cloud
    networking:
      type: limited
      allowed_hosts:
        - api.example.com
      allow_mcp_servers: true
      allow_package_managers: true
  YAML
  ```

  ```python Python
  environment = client.beta.environments.create(
      name="api-access",
      config={
          "type": "cloud",
          "networking": {
              "type": "limited",
              "allowed_hosts": ["api.example.com"],
              "allow_mcp_servers": True,
              "allow_package_managers": True,
          },
      },
  )
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "api-access",
    config: {
      type: "cloud",
      networking: {
        type: "limited",
        allowed_hosts: ["api.example.com"],
        allow_mcp_servers: true,
        allow_package_managers: true
      }
    }
  });
  ```

  ```csharp C#
  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "api-access",
      Config = new BetaCloudConfigParams
      {
          Networking = new BetaLimitedNetworkParams
          {
              AllowedHosts = ["api.example.com"],
              AllowMcpServers = true,
              AllowPackageManagers = true,
          },
      },
  });
  ```

  ```go Go
  environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
  	Name: "api-access",
  	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
  		OfCloud: &anthropic.BetaCloudConfigParams{
  			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
  				OfLimited: &anthropic.BetaLimitedNetworkParams{
  					AllowedHosts:         []string{"api.example.com"},
  					AllowMCPServers:      anthropic.Bool(true),
  					AllowPackageManagers: anthropic.Bool(true),
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  _ = environment
  ```

  ```java Java
  var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
      .name("api-access")
      .config(BetaCloudConfigParams.builder()
          .networking(BetaLimitedNetworkParams.builder()
              .allowedHosts(List.of("api.example.com"))
              .allowMcpServers(true)
              .allowPackageManagers(true)
              .build())
          .build())
      .build());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'api-access',
      config: [
          'type' => 'cloud',
          'networking' => [
              'type' => 'limited',
              'allowed_hosts' => ['api.example.com'],
              'allow_mcp_servers' => true,
              'allow_package_managers' => true,
          ],
      ],
  );
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "api-access",
    config: {
      type: "cloud",
      networking: {
        type: "limited",
        allowed_hosts: %w[api.example.com],
        allow_mcp_servers: true,
        allow_package_managers: true
      }
    }
  )
  ```
</CodeGroup>

<Info>
  For production deployments, use `limited` networking with an explicit `allowed_hosts` list. Follow the principle of least privilege by granting only the minimum network access your agent requires, and regularly audit your allowed domains.
</Info>

When using `limited` networking:

* `allowed_hosts` specifies domains the sandbox can reach. Specify bare hostnames or wildcard patterns (such as `*.example.com`). Do not include a URL scheme, port, or path.
* `allow_mcp_servers` allows outbound access to MCP server endpoints configured on the agent, beyond those listed in the `allowed_hosts` array. Defaults to `false`.
* `allow_package_managers` allows outbound access to public package registries (such as PyPI and npm) beyond those listed in the `allowed_hosts` array. Defaults to `false`.

## Environment lifecycle

* Environments persist until explicitly archived or deleted.
* Each session gets its own sandbox instance, even when multiple sessions reference the same environment. Sessions do not share filesystem state.
* Environments are not versioned. If you update an environment frequently, keep your own record of the changes so you can tell which configuration each session used.

## Manage environments

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  # List environments
  environments=$(curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  # Retrieve a specific environment
  env=$(curl -fsS "https://api.anthropic.com/v1/environments/$environment_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  # Archive an environment (read-only, existing sessions continue)
  curl -fsS -X POST "https://api.anthropic.com/v1/environments/$environment_id/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Delete an environment (only if no sessions reference it)
  curl -fsS -X DELETE "https://api.anthropic.com/v1/environments/$environment_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  # List environments
  ant beta:environments list

  # Retrieve a specific environment
  ant beta:environments retrieve --environment-id "$ENVIRONMENT_ID"

  # Archive an environment (read-only, existing sessions continue)
  ant beta:environments archive --environment-id "$ENVIRONMENT_ID"

  # Delete an environment (only if no sessions reference it)
  ant beta:environments delete --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  # List environments
  environments = client.beta.environments.list()

  # Retrieve a specific environment
  env = client.beta.environments.retrieve(environment.id)

  # Archive an environment (read-only, existing sessions continue)
  client.beta.environments.archive(environment.id)

  # Delete an environment (only if no sessions reference it)
  client.beta.environments.delete(environment.id)
  ```

  ```typescript TypeScript
  // List environments
  const environments = await client.beta.environments.list();

  // Retrieve a specific environment
  const env = await client.beta.environments.retrieve(environment.id);

  // Archive an environment (read-only, existing sessions continue)
  await client.beta.environments.archive(environment.id);

  // Delete an environment (only if no sessions reference it)
  await client.beta.environments.delete(environment.id);
  ```

  ```csharp C#
  // List environments
  var environments = await client.Beta.Environments.List();

  // Retrieve a specific environment
  var env = await client.Beta.Environments.Retrieve(environment.ID);

  // Archive an environment (read-only, existing sessions continue)
  await client.Beta.Environments.Archive(environment.ID);

  // Delete an environment (only if no sessions reference it)
  await client.Beta.Environments.Delete(environment.ID);
  ```

  ```go Go
  // List environments
  environments, err := client.Beta.Environments.List(ctx, anthropic.BetaEnvironmentListParams{})
  // ...

  // Retrieve a specific environment
  env, err := client.Beta.Environments.Get(ctx, environment.ID, anthropic.BetaEnvironmentGetParams{})
  // ...

  // Archive an environment (read-only, existing sessions continue)
  _, err = client.Beta.Environments.Archive(ctx, environment.ID, anthropic.BetaEnvironmentArchiveParams{})
  // ...

  // Delete an environment (only if no sessions reference it)
  _, err = client.Beta.Environments.Delete(ctx, environment.ID, anthropic.BetaEnvironmentDeleteParams{})
  ```

  ```java Java
  // List environments
  var environments = client.beta().environments().list();
  // Retrieve a specific environment
  var env = client.beta().environments().retrieve(environment.id());
  // Archive an environment (read-only, existing sessions continue)
  client.beta().environments().archive(environment.id());
  // Delete an environment (only if no sessions reference it)
  client.beta().environments().delete(environment.id());
  ```

  ```php PHP
  // List environments
  $environments = $client->beta->environments->list();
  // Retrieve a specific environment
  $env = $client->beta->environments->retrieve($environment->id);
  // Archive an environment (read-only, existing sessions continue)
  $client->beta->environments->archive($environment->id);
  // Delete an environment (only if no sessions reference it)
  $client->beta->environments->delete($environment->id);
  ```

  ```ruby Ruby
  # List environments
  environments = client.beta.environments.list

  # Retrieve a specific environment
  env = client.beta.environments.retrieve(environment.id)

  # Archive an environment (read-only, existing sessions continue)
  client.beta.environments.archive(environment.id)

  # Delete an environment (only if no sessions reference it)
  client.beta.environments.delete(environment.id)
  ```
</CodeGroup>

## Pre-installed runtimes

Cloud sandboxes include common runtimes out of the box. See [Cloud sandbox reference](/docs/en/managed-agents/cloud-sandboxes-reference) for the full list of pre-installed languages, databases, and utilities.

## Next steps

<CardGroup cols={2}>
  <Card title="Cloud sandbox reference" icon="book" href="/docs/en/managed-agents/cloud-sandboxes-reference">
    Pre-installed packages, databases, and utilities available in cloud sandboxes.
  </Card>

  <Card title="Start a session" icon="play" href="/docs/en/managed-agents/sessions">
    Create a session to run your agent and start running tasks.
  </Card>
</CardGroup>
