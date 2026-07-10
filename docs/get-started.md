# Get started with Claude

Make your first API call to Claude and build a simple web search assistant.

---

## Prerequisites

* An Anthropic [Console account](/)
* An [API key](/settings/keys)

## Call the API

<Tabs>
  <Tab title="cURL">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The cURL command below reads it from `$ANTHROPIC_API_KEY`.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Make your first API call">
        Send a `POST` request to the Messages API:

        ```bash cURL
        curl https://api.anthropic.com/v1/messages \
          -H "content-type: application/json" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -d '{
            "model": "claude-opus-4-8",
            "max_tokens": 1000,
            "messages": [
              {
                "role": "user",
                "content": "What should I search for to find the latest developments in renewable energy?"
              }
            ]
          }'
        ```

        Claude returns a JSON response containing the assistant's message:

        ```json Output
        {
          "id": "msg_013mHbppMPd2PrVJzGMZPt2D",
          "type": "message",
          "role": "assistant",
          "model": "claude-opus-4-8",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
            }
          ],
          "stop_reason": "end_turn",
          "usage": {
            "input_tokens": 21,
            "output_tokens": 305
          }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="CLI">
    <Steps>
      <Step title="Install the CLI">
        Install the Anthropic CLI with Homebrew:

        ```bash
        brew install anthropics/tap/ant
        ```

        For other installation methods, see [Installation](/docs/en/cli-sdks-libraries/cli/quickstart#installation) in the CLI quickstart.
      </Step>

      <Step title="Authenticate">
        Log in with your Anthropic account:

        ```bash
        ant auth login
        ```

        This opens a browser-based OAuth flow. After authorizing, confirm your credential with:

        ```bash
        ant auth status
        ```

        On a remote host without a browser, pass `--no-browser` to get a URL you can open on another device, then paste the returned code back into the terminal. If `ANTHROPIC_API_KEY` is set in your environment, it takes precedence over the login credentials. For non-interactive environments such as CI, see [CLI authentication options](/docs/en/cli-sdks-libraries/cli/authentication).
      </Step>

      <Step title="Make your first API call">
        Run `ant messages create` from your terminal:

        ```bash CLI
        ant messages create \
          --model claude-opus-4-8 \
          --max-tokens 1000 \
          --message '{
            role: user,
            content: "What should I search for to find the latest developments in renewable energy?"
          }'
        ```

        The CLI prints the JSON response:

        ```json Output
        {
          "id": "msg_01N1ycuCkM5Mzd7WhTU4fwST",
          "type": "message",
          "role": "assistant",
          "model": "claude-opus-4-8",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest developments in renewable energy:\n\n## General Search Terms\n- \"Renewable energy news 2025\"\n- ..."
            }
          ],
          "stop_reason": "end_turn",
          "usage": { "input_tokens": 21, "output_tokens": 305 }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Python">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Create a project and install the SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        python3 -m venv .venv && source .venv/bin/activate
        pip install anthropic
        ```
      </Step>

      <Step title="Create your code">
        Create a file called `quickstart.py`:

        ```python Python
        import anthropic

        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": "What should I search for to find the latest developments in renewable energy?",
                }
            ],
        )

        for block in message.content:
            if block.type == "text":
                print(block.text)
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        python quickstart.py
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="TypeScript">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Create a project and install the SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        npm init -y
        npm pkg set type=module
        npm install @anthropic-ai/sdk
        ```
      </Step>

      <Step title="Create your code">
        Create a file called `quickstart.ts`:

        ```typescript TypeScript
        import Anthropic from "@anthropic-ai/sdk";

        const client = new Anthropic();

        const message = await client.messages.create({
          model: "claude-opus-4-8",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: "What should I search for to find the latest developments in renewable energy?"
            }
          ]
        });

        for (const block of message.content) {
          if (block.type === "text") {
            console.log(block.text);
          }
        }
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        npx tsx quickstart.ts
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="C#">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Create a project and install the SDK">
        Create a new console project and add the Anthropic package:

        ```bash
        dotnet new console -n ClaudeQuickstart
        cd ClaudeQuickstart
        dotnet add package Anthropic
        ```
      </Step>

      <Step title="Create your code">
        Replace the contents of `Program.cs`:

        ```csharp C#
        using Anthropic;
        using Anthropic.Models.Messages;

        var client = new AnthropicClient();

        var message = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1000,
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = "What should I search for to find the latest developments in renewable energy?",
                },
            ],
        });

        foreach (var block in message.Content)
        {
            if (block.TryPickText(out var textBlock))
            {
                Console.WriteLine(textBlock.Text);
            }
        }
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        dotnet run
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Go">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Create a project and install the SDK">
        Create a new module and add the Anthropic SDK:

        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        go mod init claude-quickstart
        go get github.com/anthropics/anthropic-sdk-go
        ```
      </Step>

      <Step title="Create your code">
        Create a file called `main.go`:

        ```go Go
        package main

        import (
        	"context"
        	"fmt"
        	"log"

        	"github.com/anthropics/anthropic-sdk-go"
        )

        func main() {
        	client := anthropic.NewClient()

        	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
        		Model:     anthropic.ModelClaudeOpus4_8,
        		MaxTokens: 1000,
        		Messages: []anthropic.MessageParam{
        			anthropic.NewUserMessage(anthropic.NewTextBlock("What should I search for to find the latest developments in renewable energy?")),
        		},
        	})
        	if err != nil {
        		log.Fatal(err)
        	}

        	for _, block := range message.Content {
        		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
        			fmt.Println(textBlock.Text)
        		}
        	}
        }
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        go run .
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Java">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Set up your project">
        You need a JDK (25 or later) and either [Gradle](https://gradle.org/install/) or [Maven](https://maven.apache.org/install.html) on your `PATH`. Create a directory for your project with a Java source directory inside it:

        ```bash
        mkdir -p claude-quickstart/src/main/java && cd claude-quickstart
        ```

        Then add a build file. Find the current SDK version on [Maven Central](https://central.sonatype.com/artifact/com.anthropic/anthropic-java).

        <Tabs>
          <Tab title="Gradle">
            Save this as `build.gradle.kts`:

            ```kotlin
            plugins {
                application
            }

            repositories {
                mavenCentral()
            }

            java {
                toolchain {
                    languageVersion = JavaLanguageVersion.of(25)
                }
            }

            dependencies {
                implementation("com.anthropic:anthropic-java:2.47.1")
            }

            application {
                mainClass = "QuickStart"
            }
            ```
          </Tab>

          <Tab title="Maven">
            Save this as `pom.xml`:

            ```xml
            <project xmlns="http://maven.apache.org/POM/4.0.0">
              <modelVersion>4.0.0</modelVersion>
              <groupId>com.example</groupId>
              <artifactId>quickstart</artifactId>
              <version>1.0-SNAPSHOT</version>
              <properties>
                <maven.compiler.release>25</maven.compiler.release>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
              </properties>
              <dependencies>
                <dependency>
                  <groupId>com.anthropic</groupId>
                  <artifactId>anthropic-java</artifactId>
                  <version>2.47.1</version>
                </dependency>
              </dependencies>
            </project>
            ```
          </Tab>
        </Tabs>
      </Step>

      <Step title="Create your code">
        Save this as `QuickStart.java` in your project's Java source directory (usually `src/main/java/`):

        ```java Java
        import com.anthropic.client.okhttp.AnthropicOkHttpClient;
        import com.anthropic.models.messages.Message;
        import com.anthropic.models.messages.MessageCreateParams;
        import com.anthropic.models.messages.Model;

        static void main() {
            var client = AnthropicOkHttpClient.fromEnv();

            var params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1000)
                .addUserMessage(
                    "What should I search for to find the latest developments in renewable energy?"
                )
                .build();

            Message message = client.messages().create(params);
            for (var block : message.content()) {
                block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
            }
        }
        ```
      </Step>

      <Step title="Run your code">
        <Tabs>
          <Tab title="Gradle">
            ```bash
            gradle run
            ```
          </Tab>

          <Tab title="Maven">
            ```bash
            mvn compile exec:java -Dexec.mainClass=QuickStart
            ```
          </Tab>
        </Tabs>

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="PHP">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Create a project and install the SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
        ```
      </Step>

      <Step title="Create your code">
        Create a file called `quickstart.php`:

        ```php PHP
        <?php
        require 'vendor/autoload.php';

        use Anthropic\Client;
        use Anthropic\Messages\Model;
        use Anthropic\Messages\TextBlock;

        $client = new Client();

        $message = $client->messages->create(
            model: Model::CLAUDE_OPUS_4_8,
            maxTokens: 1000,
            messages: [
                [
                    'role' => 'user',
                    'content' => 'What should I search for to find the latest developments in renewable energy?',
                ],
            ],
        );

        foreach ($message->content as $block) {
            if ($block instanceof TextBlock) {
                echo $block->text . PHP_EOL;
            }
        }
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        php quickstart.php
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Ruby">
    <Steps>
      <Step title="Set your API key">
        Export your API key as an environment variable. The SDK reads `ANTHROPIC_API_KEY` automatically.

        ```bash
        export ANTHROPIC_API_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Create a project and install the SDK">
        ```bash
        mkdir claude-quickstart && cd claude-quickstart
        bundle init
        bundle add anthropic
        ```
      </Step>

      <Step title="Create your code">
        Create a file called `quickstart.rb`:

        ```ruby Ruby
        require "anthropic"

        client = Anthropic::Client.new

        message = client.messages.create(
          model: Anthropic::Model::CLAUDE_OPUS_4_8,
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: "What should I search for to find the latest developments in renewable energy?"
            }
          ]
        )

        message.content.each do |block|
          puts block.text if block.type == :text
        end
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        bundle exec ruby quickstart.rb
        ```

        ```text Output wrap
        Here are some effective search strategies to find the latest developments in renewable energy:

        ## General Search Terms
        - "Renewable energy news 2025"
        - ...
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Next steps

You made your first API call. Next, learn the Messages API patterns you'll use in every Claude integration.

<Card title="Working with the Messages API" icon="messages" href="/docs/en/build-with-claude/working-with-messages">
  Learn multi-turn conversations, system prompts, stop reasons, and other core patterns.
</Card>

Once you're comfortable with the basics, explore further:

<CardGroup cols={3}>
  <Card title="Models overview" icon="brain" href="/docs/en/about-claude/models/overview">
    Compare Claude models by capability and cost.
  </Card>

  <Card title="Features overview" icon="list" href="/docs/en/build-with-claude/overview">
    Browse all Claude capabilities: tools, context management, structured outputs, and more.
  </Card>

  <Card title="Client SDKs" icon="code-brackets" href="/docs/en/cli-sdks-libraries/overview">
    Reference documentation for Python, TypeScript, C#, and other client libraries.
  </Card>
</CardGroup>
