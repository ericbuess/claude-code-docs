---
title: Files API
url: https://platform.claude.com/docs/en/build-with-claude/files
description: Upload files once, reference them by file_id in Messages requests, and download outputs created by skills or the code execution tool.
---

## Compatibility
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): not eligible
- Platforms: Claude API, Claude Platform on AWS (beta), Microsoft Foundry (beta) [1]; not available on Amazon Bedrock, Google Cloud
1. On [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry), the Files API requires a [Hosted on Anthropic deployment](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).

The Files API lets you upload and manage files to use with the Claude API without re-uploading content with each request. This is particularly useful when using the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) to provide inputs (for example, datasets and documents) and then download outputs (for example, charts). You can [explore the API reference directly](https://platform.claude.com/docs/en/api/files/upload), in addition to this guide.

## File type support

Referencing a `file_id` in a Messages request is supported on all models that support the given file type. [Images](https://platform.claude.com/docs/en/build-with-claude/vision) are supported on all current Claude models. For [PDFs](https://platform.claude.com/docs/en/build-with-claude/pdf-support) and [other file types with the code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#model-compatibility), see the linked pages for model support.

## How the Files API works

The Files API provides a create-once, use-many-times approach for working with files:

* **Upload files** to Anthropic's secure storage and receive a unique `file_id`
* **Download files** that are created by skills or the code execution tool
* **Reference files** in [Messages](https://platform.claude.com/docs/en/api/messages/create) requests using the `file_id` instead of re-uploading content
* **Manage your files** with list, retrieve, and delete operations

<Warning id="workspace-scoped-access">
  **Uploaded files are accessible to your entire workspace, not scoped to an end user, conversation, or session.** Any API key in the same workspace can access any file uploaded there, and all of your keys share your organization's Default Workspace unless you have assigned them to separate [workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces#api-keys-and-resource-scoping). Never accept `file_id` values from end users or other untrusted sources: a user-supplied file ID would let one user of your application read content that another user uploaded. Treat file IDs as server-side references, and keep the mapping between your users and their files in your application.

  If you are building a multi-tenant application on the Files API, create a separate [workspace](https://platform.claude.com/docs/en/manage-claude/workspaces) for each tenant. The workspace is the isolation boundary for files, so a workspace per tenant gives each tenant's data hard isolation from every other tenant. Each organization can have up to 100 workspaces; contact your account team if you need more.
</Warning>

## How to use the Files API

### Uploading a file

Upload a file to be referenced in future API calls:

<CodeGroup>
  ```bash cURL
  FILE_ID=$(curl -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -F "file=@/path/to/document.pdf" | jq -r '.id')
  echo "$FILE_ID"
  ```

  ```bash CLI
  FILE_ID=$(ant files upload \
    --file /path/to/document.pdf \
    --transform id \
    --raw-output)
  echo "$FILE_ID"
  ```

  ```python Python
  uploaded = client.files.upload(
      file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
  )
  file_id = uploaded.id
  print(file_id)
  ```

  ```typescript TypeScript
  const uploaded = await client.files.upload({
    file: await toFile(
      fs.createReadStream("/path/to/document.pdf"),
      undefined,
      { type: "application/pdf" },
    ),
  });
  console.log(uploaded.id);
  ```

  ```csharp C#
  var uploaded = await client.Files.Upload(
      new FileUploadParams
      {
          File = new BinaryContent
          {
              Stream = File.OpenRead("/path/to/document.pdf"),
              FileName = "document.pdf",
              ContentType = new("application/pdf")
          }
      });

  var fileId = uploaded.ID;
  Console.WriteLine(fileId);
  ```

  ```go Go
  f, err := os.Open("/path/to/document.pdf")
  if err != nil {
  	log.Fatal(err)
  }
  defer f.Close()

  response, err := client.Files.Upload(context.Background(),
  	anthropic.FileUploadParams{
  		File: anthropic.File(f, "document.pdf", "application/pdf"),
  	})
  if err != nil {
  	log.Fatal(err)
  }

  fileID := response.ID
  fmt.Println(fileID)
  ```

  ```java Java
  FileMetadata file = client.files().upload(
      FileUploadParams.builder()
          .file(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("/path/to/document.pdf")))
              .filename("document.pdf")
              .contentType("application/pdf")
              .build())
          .build()
  );

  String fileId = file.id();
  System.out.println(fileId);
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  $file = $client->beta->files->upload(
      FileParam::fromResource(fopen('/path/to/document.pdf', 'rb'), contentType: 'application/pdf'),
  );

  $fileId = $file->id;
  echo $fileId;
  ```

  ```ruby Ruby
  file = client.files.upload(
    file: Anthropic::FilePart.new(
      Pathname("/path/to/document.pdf"),
      content_type: "application/pdf"
    )
  )

  file_id = file.id
  puts file_id
  ```
</CodeGroup>

The response from uploading a file includes:

```json Response
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file",
  "filename": "document.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1024000,
  "created_at": "2025-01-01T00:00:00Z",
  "downloadable": false,
  "expires_at": null
}
```

`downloadable` is `false` for files you upload. Only files created by [skills](https://platform.claude.com/docs/en/build-with-claude/skills-guide) or the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) can be downloaded. See [Downloading a file](https://platform.claude.com/docs/en/build-with-claude/files#downloading-a-file).

### Using a file in messages

Once uploaded, reference the file by passing the `id` from the upload response as `file_id`:

<CodeGroup>
  ```bash cURL
  curl -X POST https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Please summarize this document for me."
          },
          {
            "type": "document",
            "source": {
              "type": "file",
              "file_id": "$FILE_ID"
            }
          }
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: text
          text: Please summarize this document for me.
        - type: document
          source:
            type: file
            file_id: $FILE_ID
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {"type": "text", "text": "Please summarize this document for me."},
                  {
                      "type": "document",
                      "source": {
                          "type": "file",
                          "file_id": file_id,
                      },
                  },
              ],
          }
      ],
  )
  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Please summarize this document for me.",
          },
          {
            type: "document",
            source: {
              type: "file",
              file_id: uploaded.id,
            },
          },
        ],
      },
    ],
  });

  console.log(response);
  ```

  ```csharp C#
  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages =
          [
              new MessageParam
              {
                  Role = Role.User,
                  Content = new List<ContentBlockParam>
                  {
                      new TextBlockParam { Text = "Please summarize this document for me." },
                      new DocumentBlockParam
                      {
                          Source = new FileDocumentSource { FileID = fileId }
                      }
                  }
              }
          ]
      });

  Console.WriteLine(response);
  ```

  ```go Go
  msg, err := client.Messages.New(context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(
  				anthropic.NewTextBlock("Please summarize this document for me."),
  				anthropic.NewDocumentBlock(anthropic.FileDocumentSourceParam{
  					FileID: fileID,
  				}),
  			),
  		},
  	})
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(msg)
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024)
      .addUserMessageOfBlockParams(List.of(
          ContentBlockParam.ofText(TextBlockParam.builder()
              .text("Please summarize this document for me.")
              .build()),
          ContentBlockParam.ofDocument(DocumentBlockParam.builder()
              .fileSource(fileId)
              .build())
      ))
      .build();

  Message message = client.messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  // The PHP SDK supports file_id document and image sources only through $client->beta->messages with the files beta.
  $response = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  ['type' => 'text', 'text' => 'Please summarize this document for me.'],
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'file',
                          'file_id' => $fileId
                      ]
                  ]
              ]
          ]
      ],
      model: 'claude-opus-5',
      betas: ['files-api-2025-04-14'],
  );

  print_r($response);
  ```

  ```ruby Ruby
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Please summarize this document for me." },
          {
            type: "document",
            source: {
              type: "file",
              file_id: file_id
            }
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

### File types and content blocks

The Files API supports different file types that correspond to different content block types:

| File type                                                                                                                               | MIME type                                            | Content block type | Use case                            |
| --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------ | ----------------------------------- |
| PDF                                                                                                                                     | `application/pdf`                                    | `document`         | Text analysis, document processing  |
| Plain text                                                                                                                              | `text/plain`                                         | `document`         | Text analysis, processing           |
| Images                                                                                                                                  | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image`            | Image analysis, visual tasks        |
| [Datasets, others](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) | Varies                                               | `container_upload` | Analyze data, create visualizations |

#### Document blocks

For PDFs and text files, use the `document` content block:

```json
{
  "type": "document",
  "source": {
    "type": "file",
    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
  },
  "title": "Document Title", // Optional
  "context": "Context about the document", // Optional
  "citations": { "enabled": true } // Optional, enables citations
}
```

#### Image blocks

For images, use the `image` content block:

```json
{
  "type": "image",
  "source": {
    "type": "file",
    "file_id": "file_011CPMxVD3fHLUhvTqtsQA5w"
  }
}
```

#### Container upload blocks

To send a file to the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files), use the `container_upload` content block:

```json
{
  "type": "container_upload",
  "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
}
```

### Working with other file formats

For file types that the `document` block doesn't support (for example, .docx and .xlsx), convert the files to plain text and include the content directly in your message. Files that are already plain text, such as .csv and .md files, can either be read in this way or uploaded through the Files API with an explicit `text/plain` content type. To analyze datasets instead of reading them as text, upload them for the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) using a `container_upload` block.

The following examples read a text file and send its contents as plain text:

<CodeGroup>
  ```bash cURL
  # Read the text file
  # Note: For files with special characters, consider base64 encoding
  TEXT_CONTENT=$(cat document.txt)

  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @- <<EOF
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Here's the document content:\n\n${TEXT_CONTENT}\n\nPlease summarize this document."
          }
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  # The "@./path" reference inlines the file contents directly into the field.
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --transform 'content.#(type=="text").text' \
    --raw-output <<'YAML'
  messages:
    - role: user
      content:
        - type: text
          text: "Here's the document content:"
        - type: text
          text: "@./document.txt"
        - type: text
          text: "Please summarize this document."
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Read the text file
  with open("document.txt") as f:
      text_content = f.read()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": f"Here's the document content:\n\n{text_content}\n\nPlease summarize this document.",
                  }
              ],
          }
      ],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  import fs from "node:fs/promises";
  // ...
  const client = new Anthropic();

  // Read the text file
  const textContent = await fs.readFile("document.txt", "utf-8");

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: `Here's the document content:\n\n${textContent}\n\nPlease summarize this document.`
          }
        ]
      }
    ]
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Read the text file
  string textContent = await File.ReadAllTextAsync("document.txt");

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages = [new()
      {
          Role = Role.User,
          Content = $"Here's the document content:\n\n{textContent}\n\nPlease summarize this document."
      }]
  };

  var message = await client.Messages.Create(parameters);
  foreach (var block in message.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  // Read the text file
  textContent, err := os.ReadFile("document.txt")
  if err != nil {
  	log.Fatal(err)
  }

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			fmt.Sprintf("Here's the document content:\n\n%s\n\nPlease summarize this document.", string(textContent)),
  		)),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Read the text file
  String textContent = Files.readString(Path.of("document.txt"));

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024L)
      .addUserMessage("Here's the document content:\n\n" + textContent + "\n\nPlease summarize this document.")
      .build();

  Message response = client.messages().create(params);
  response.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> System.out.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  // Read the text file
  $textContent = file_get_contents("document.txt");

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => "Here's the document content:\n\n{$textContent}\n\nPlease summarize this document."
                  ]
              ]
          ]
      ],
      model: 'claude-opus-5',
  );

  foreach ($message->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Read the text file
  text_content = File.read("document.txt")

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Here's the document content:\n\n#{text_content}\n\nPlease summarize this document."
          }
        ]
      }
    ]
  )

  message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

<Note>
  For .docx files containing images, convert them to PDF format first, then use [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) to take advantage of the built-in image parsing. This allows using citations from the PDF document.
</Note>

### Managing files

#### List files

Retrieve a list of your uploaded files. The endpoint is paginated: each request returns up to `limit` files (20 by default, and at most 1,000), and the response's `next_page` cursor fetches the next page when passed back as the `page` parameter. Files are ordered newest first. See the [List Files API reference](https://platform.claude.com/docs/en/api/files/list). The SDKs return the first page and provide auto-pagination helpers. The CLI example bounds the total with `--max-items`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant files list \
    --max-items 10
  ```

  ```python Python
  client = anthropic.Anthropic()
  files = client.files.list()
  print(files)
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const files = await client.files.list();
  console.log(files);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var files = await client.Files.List();
  Console.WriteLine(files);
  ```

  ```go Go
  client := anthropic.NewClient()

  files, err := client.Files.List(context.TODO(), anthropic.FileListParams{})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(files)
  ```

  ```java Java
  import com.anthropic.models.files.FileListPage;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      FileListPage files = client.files().list();
      System.out.println(files);
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // list() paginates with afterID, beforeID, and limit; page and ids[] are not parameters here.
  $client = new Client();

  $files = $client->beta->files->list();
  echo $files;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  files = client.files.list
  puts files
  ```
</CodeGroup>

To check a known set of files in one request instead of paging, pass up to 100 file IDs as `ids[]` query parameters. An `ids[]` request always returns a single page (`next_page` is `null`), and any ID that does not resolve to a file in your workspace is silently omitted from `data`; compare the returned IDs against the requested IDs to detect misses. `ids[]` cannot be combined with `page` or `limit`.

#### Get file metadata

Retrieve information about a specific file:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant files retrieve-metadata \
    --file-id "$FILE_ID"
  ```

  ```python Python
  file = client.files.retrieve_metadata(file_id)
  print(file)
  ```

  ```typescript TypeScript
  const file = await client.files.retrieveMetadata(uploaded.id);
  console.log(file);
  ```

  ```csharp C#
  var file = await client.Files.RetrieveMetadata(fileId);
  Console.WriteLine(file);
  ```

  ```go Go
  metadata, err := client.Files.GetMetadata(context.TODO(), fileID)
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(metadata)
  ```

  ```java Java
  FileMetadata metadata = client.files().retrieveMetadata(fileId);

  System.out.println(metadata);
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  $file = $client->beta->files->retrieveMetadata($fileId);
  echo $file;
  ```

  ```ruby Ruby
  file = client.files.retrieve_metadata(file_id)
  puts file
  ```
</CodeGroup>

#### Delete a file

Remove a file from your workspace:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant files delete \
    --file-id "$FILE_ID"
  ```

  ```python Python
  client.files.delete(file_id)
  ```

  ```typescript TypeScript
  await client.files.delete(uploaded.id);
  ```

  ```csharp C#
  await client.Files.Delete(fileId);
  ```

  ```go Go
  _, err = client.Files.Delete(context.TODO(), fileID)
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  client.files().delete(fileId);
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  client.files.delete(file_id)
  ```
</CodeGroup>

### Downloading a file

Download files that were created by [skills](https://platform.claude.com/docs/en/build-with-claude/skills-guide) or the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool). Files you upload cannot be downloaded. The `file_id` of a generated file appears in the [`bash_code_execution_tool_result` content block](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) of the Messages response that created it:

<CodeGroup>
  ```bash cURL
  curl -X GET "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    --output downloaded_file.txt
  ```

  ```bash CLI
  ant files download \
    --file-id "$FILE_ID" \
    --output downloaded_file.txt
  ```

  ```python Python
  file_content = client.files.download(file_id)

  file_content.write_to_file("downloaded_file.txt")
  ```

  ```typescript TypeScript
  const content = await client.files.download(uploaded.id);

  const bytes = Buffer.from(await content.arrayBuffer());
  await fsp.writeFile("downloaded_file.txt", bytes);
  ```

  ```csharp C#
  using var fileContent = await client.Files.Download(fileId);
  await using var source = await fileContent.ReadAsStream();
  await using var destination = File.Create("downloaded_file.txt");
  await source.CopyToAsync(destination);
  ```

  ```go Go
  func downloadFile(client anthropic.Client, fileID string) error {
  	resp, err := client.Files.Download(context.TODO(), fileID)
  	if err != nil {
  		return err
  	}
  	defer resp.Body.Close()

  	out, err := os.Create("downloaded_file.txt")
  	if err != nil {
  		return err
  	}
  	defer out.Close()

  	_, err = io.Copy(out, resp.Body)
  	return err
  }

  ```

  ```java Java
  try (HttpResponse response = client.files().download(fileId)) {
      try (InputStream body = response.body()) {
          Files.copy(body, Path.of("downloaded_file.txt"),
              StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  $fileContent = $client->beta->files->download($fileId);

  file_put_contents("downloaded_file.txt", $fileContent);
  ```

  ```ruby Ruby
  file_content = client.files.download(file_id)

  File.binwrite("downloaded_file.txt", file_content.read)
  ```
</CodeGroup>

<Note>
  A file is downloadable only when its metadata shows `"downloadable": true`, which is the case for files created by skills or the code execution tool. Downloading a file you uploaded returns a 400 error.
</Note>

## File storage and limits

### Storage limits

* **Maximum file size:** 500 MB per file
* **Total storage:** 1 TB per organization

### File lifecycle

* Files are scoped to the workspace of the API key that uploaded them. Any API key in the same workspace can reference them; never accept file IDs from untrusted sources (see the [workspace access warning](https://platform.claude.com/docs/en/build-with-claude/files#workspace-scoped-access))
* Files cannot be modified or renamed after upload. To change a file's content, upload a new file and delete the old one
* Files persist until you delete them with the `DELETE /v1/files/{file_id}` endpoint or they reach their `expires_at`
* Deleted files cannot be recovered
* Files are inaccessible through the API shortly after deletion, but they may persist in active Messages API calls and associated tool uses
* Files that users delete will be deleted in accordance with Anthropic's [data retention policy](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data). For ZDR eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)

### File expiration

To have a file expire automatically, include an `expires_in_seconds` form field when you upload it. The value is an integer number of seconds between 3,600 (1 hour) and 7,776,000 (90 days). The resulting `expires_at` timestamp (RFC 3339) appears on every file response and is `null` for files uploaded without an expiration. Expiration is set once at upload and cannot be changed.

When a file reaches its `expires_at`:

* Downloading its content (`GET /v1/files/{file_id}/content`) returns a 404 error
* A Messages request that references the file fails before inference
* Its metadata (`GET /v1/files/{file_id}`) remains readable for up to 30 days, with `expires_at` in the past
* It continues to appear in list responses during that window; compare `expires_at` to the current time to filter expired files

Deleting an expired file with `DELETE /v1/files/{file_id}` removes its metadata immediately instead of waiting for the 30-day window to elapse.

<Note>
  Expiration is a lifecycle feature, not a guaranteed-deletion control. After `expires_at`, file content is no longer retrievable through the API and is released from your storage quota; the underlying content may be retained for a limited period thereafter for safety review before permanent deletion, and file metadata remains visible for up to 30 days after expiration. To remove a file before its scheduled expiration, use `DELETE /v1/files/{file_id}`.
</Note>

### Audit logging

If your organization has the [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) enabled, its [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) records Files API operations made with a Claude API key or from the Claude Console: each upload (`POST /v1/files`), content download (`GET /v1/files/{file_id}/content`), and deletion (`DELETE /v1/files/{file_id}`) appears as a `platform_file_uploaded`, `platform_file_content_downloaded`, or `platform_file_deleted` activity. Listing files and retrieving file metadata are not recorded. Operations that occur while the Compliance API is off are not recorded and cannot be recovered later, so [set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access) before you rely on this audit trail. On [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#monitoring-and-logging), audit file operations with AWS CloudTrail data events instead.

## Error handling

Common errors when using the Files API include:

* **File not found (404):** The specified `file_id` doesn't exist or you don't have access to it
* **Invalid file type (400):** The file type doesn't match the content block type (for example, using an image file in a document block)
* **Not downloadable (400):** Files you upload have `"downloadable": false` and cannot be downloaded. Only files created by skills or the code execution tool can be downloaded
* **Exceeds context window size (400):** The file is larger than the context window size (for example, using a 500 MB plain text file in a `/v1/messages` request)
* **Invalid filename (400):** The file name doesn't meet the length requirements (1-255 characters) or contains forbidden characters (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, or Unicode characters 0-31)
* **File too large (413):** File exceeds the 500 MB limit
* **Storage limit exceeded (400):** Your organization has reached the 1 TB storage limit

```json Output
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "File `file_011CNha8iCJcU1wXNR6q4V8w` not found."
  },
  "request_id": "req_011CQFYcrRp7mCHLDsAYT8Qt"
}
```

## Usage and billing

Files API operations are free:

* Uploading files
* Downloading files
* Listing files
* Getting file metadata
* Deleting files

File content used in Messages requests is priced as input tokens.

### Rate limits

File-related API calls are limited to approximately 500 requests per minute. To request a higher limit, [contact sales](mailto:sales@anthropic.com).

## Next steps

<CardGroup cols={3}>
  <Card title="PDF support" icon="file" href="https://platform.claude.com/docs/en/build-with-claude/pdf-support">
    Process PDFs with Claude. Extract text, analyze charts, and understand visual content from your documents.
  </Card>

  <Card title="Code execution tool" icon="terminal" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool">
    Run Python and bash code in a sandboxed container to analyze data, generate files, and iterate on solutions.
  </Card>

  <Card title="Vision" icon="image" href="https://platform.claude.com/docs/en/build-with-claude/vision">
    Process and analyze visual input and generate text and code from images.
  </Card>
</CardGroup>
