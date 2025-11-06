# Claude Code on the web

> Run Claude Code tasks asynchronously on secure cloud infrastructure

<Note>
  Claude Code on the web is currently in research preview.
</Note>

## What is Claude Code on the web?

Claude Code on the web lets developers kick off Claude Code from the Claude app. This is perfect for:

* **Answering questions**: Ask about code architecture and how features are implemented
* **Bugfixes and routine tasks**: Well-defined tasks that don't require frequent steering
* **Parallel work**: Tackle multiple bug fixes in parallel
* **Repositories not on your local machine**: Work on code you don't have checked out locally
* **Backend changes**: Where Claude Code can write tests and then write code to pass those tests

Claude Code is also available on the Claude iOS app. This is perfect for:

* **On the go**: Kick off tasks while commuting or away from laptop
* **Monitoring**: Watch the trajectory and steer the agent's work

Developers can also move Claude Code sessions from the Claude app to their terminal to continue tasks locally.

## Who can use Claude Code on the web?

Claude Code on the web is available in research preview to:

* **Pro users**
* **Max users**

Coming soon to Team and Enterprise premium seat users.

## Getting started

1. Visit [claude.ai/code](https://claude.ai/code)
2. Connect your GitHub account
3. Install the Claude GitHub app in your repositories
4. Select your default environment
5. Submit your coding task
6. Review changes and create a pull request in GitHub

## How it works

When you start a task on Claude Code on the web:

1. **Repository cloning**: Your repository is cloned to an Anthropic-managed virtual machine
2. **Environment setup**: Claude prepares a secure cloud environment with your code
3. **Network configuration**: Internet access is configured based on your settings
4. **Task execution**: Claude analyzes code, makes changes, runs tests, and checks its work
5. **Completion**: You're notified when finished and can create a PR with the changes
6. **Results**: Changes are pushed to a branch, ready for pull request creation

## Moving tasks between web and terminal

### From web to terminal

After starting a task on the web:

1. Click the "Open in CLI" button
2. Paste and run the command in your terminal in a checkout of the repo
3. Any existing local changes will be stashed, and the remote session will be loaded
4. Continue working locally

## Cloud environment

### Default image

We build and maintain a universal image with common toolchains and language ecosystems pre-installed. This image includes:

* Popular programming languages and runtimes
* Common build tools and package managers
* Testing frameworks and linters

#### Checking available tools

To see what's pre-installed in your environment, ask Claude Code to run:

```bash  theme={null}
check-tools
```

This command displays:

* Programming languages and their versions
* Available package managers
* Installed development tools

#### Language-specific setups

The universal image includes pre-configured environments for:

* **Python**: Python 3.x with pip, poetry, and common scientific libraries
* **Node.js**: Latest LTS versions with npm, yarn, and pnpm
* **Java**: OpenJDK with Maven and Gradle
* **Go**: Latest stable version with module support
* **Rust**: Rust toolchain with cargo
* **C++**: GCC and Clang compilers

### Environment configuration

When you start a session in Claude Code on the web, here's what happens under the hood:

1. **Environment preparation**: We clone your repository and run any configured Claude hooks for initialization. The repo will be cloned with the default branch on your GitHub repo. If you would like to check out a specific branch, you can specify that in the prompt.

2. **Network configuration**: We configure internet access for the agent. Internet access is limited by default, but you can configure the environment to have no internet or full internet access based on your needs.

3. **Claude Code execution**: Claude Code runs to complete your task, writing code, running tests, and checking its work. You can guide and steer Claude throughout the session via the web interface. Claude respects context you've defined in your `CLAUDE.md`.

4. **Outcome**: When Claude completes its work, it will push the branch to remote. You will be able to create a PR for the branch.

<Note>
  Claude operates entirely through the terminal and CLI tools available in the environment. It uses the pre-installed tools in the universal image and any additional tools you install through hooks or dependency management.
</Note>

**To add a new environment:** Select the current environment to open the environment selector, and then select "Add environment". This will open a dialog where you can specify the environment name, network access level, and any environment variables you want to set.

**To update an existing environment:** Select the current environment, to the right of the environment name, and select the settings button. This will open a dialog where you can update the environment name, network access, and environment variables.

<Note>
  Environment variables must be specified as key-value pairs, in [`.env` format](https://www.dotenv.org/). For example:

  ```
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Dependency management

Configure automatic dependency installation using [SessionStart hooks](/en/hooks#sessionstart). This can be configured in your repository's `.claude/settings.json` file:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Create the corresponding script at `scripts/install_pkgs.sh`:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
exit 0
```

Make it executable: `chmod +x scripts/install_pkgs.sh`

#### Local vs remote execution

By default, all hooks execute both locally and in remote (web) environments. To run a hook only in one environment, check the `CLAUDE_CODE_REMOTE` environment variable in your hook script.

```bash  theme={null}
#!/bin/bash

# Example: Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
```

#### Persisting environment variables

SessionStart hooks can persist environment variables for subsequent bash commands by writing to the file specified in the `CLAUDE_ENV_FILE` environment variable. For details, see [SessionStart hooks](/en/hooks#sessionstart) in the hooks reference.

## Network access and security

### Network policy

#### GitHub proxy

For security, all GitHub operations go through a dedicated proxy service that transparently handles all git interactions. Inside the sandbox, the git client authenticates using a custom-built scoped credential. This proxy:

* Manages GitHub authentication securely - the git client uses a scoped credential inside the sandbox, which the proxy verifies and translates to your actual GitHub authentication token
* Restricts git push operations to the current working branch for safety
* Enables seamless cloning, fetching, and PR operations while maintaining security boundaries

#### Security proxy

Environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes. All outbound internet traffic passes through this proxy, which provides:

* Protection against malicious requests
* Rate limiting and abuse prevention
* Content filtering for enhanced security

### Access levels

By default, network access is limited to [allowlisted domains](#default-allowed-domains).

You can configure custom network access, including disabling network access.

### Default allowed domains

When using "Limited" network access, the following domains are allowed by default:

#### Anthropic Services

* api.anthropic.com
* statsig.anthropic.com
* claude.ai

#### Version Control

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* raw\.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### Container Registries

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com

#### Cloud Platforms

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### Package Managers - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Package Managers - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Package Managers - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### Package Managers - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Package Managers - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Package Managers - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* spring.io
* repo.spring.io

#### Package Managers - Other Languages

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Linux Distributions

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Development Tools & Platforms

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### Cloud Services & Monitoring

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* \*.sentry.io

#### Content Delivery & Mirrors

* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Schema & Configuration

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

<Note>
  Domains marked with `*` indicate wildcard subdomain matching. For example, `*.gcr.io` allows access to any subdomain of `gcr.io`.
</Note>

### Security best practices for customized network access

1. **Principle of least privilege**: Only enable the minimum network access required
2. **Audit regularly**: Review allowed domains periodically
3. **Use HTTPS**: Always prefer HTTPS endpoints over HTTP

## Security and isolation

Claude Code on the web provides strong security guarantees:

* **Isolated virtual machines**: Each session runs in an isolated, Anthropic-managed VM
* **Network access controls**: Network access is limited by default, and can be disabled

<Note>
  When running with network access disabled, Claude Code is allowed to communicate with the Anthropic API which may still allow data to exit the isolated Claude Code VM.
</Note>

* **Credential protection**: Sensitive credentials (such as git credentials or signing keys) are never inside the sandbox with Claude Code. Authentication is handled through a secure proxy using scoped credentials
* **Secure analysis**: Code is analyzed and modified within isolated VMs before creating PRs

## Pricing and rate limits

Claude Code on the web shares rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel will consume more rate limits proportionately.

## Limitations

* **Repository authentication**: You can only move sessions from web to local when you are authenticated to the same account
* **Platform restrictions**: Claude Code on the web only works with code hosted in GitHub. GitLab and other non-GitHub repositories cannot be used with cloud sessions

## Best practices

1. **Use Claude Code hooks**: Configure [sessionStart hooks](/en/hooks#sessionstart) to automate environment setup and dependency installation.
2. **Document requirements**: Clearly specify dependencies and commands in your `CLAUDE.md` file. If you have an `AGENTS.md` file, you can source it in your `CLAUDE.md` using `@AGENTS.md` to maintain a single source of truth.

## Related resources

* [Hooks configuration](/en/hooks)
* [Settings reference](/en/settings)
* [Security](/en/security)
* [Data usage](/en/data-usage)
