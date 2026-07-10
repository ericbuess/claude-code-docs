# Files API

Upload files once, reference them by file_id in Messages requests, and download outputs created by skills or the code execution tool.

---

The Files API lets you upload and manage files to use with the Claude API without re-uploading content with each request. This is particularly useful when using the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool) to provide inputs (for example, datasets and documents) and then download outputs (for example, charts). You can [explore the API reference directly](/docs/en/api/files-create), in addition to this guide.

<Note>
  The Files API is in beta. Reach out through the [feedback form](https://forms.gle/tisHyierGwgN4DUE9) to share your experience with the Files API.
</Note>

<Note>
  This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Supported models

Referencing a `file_id` in a Messages request is supported on all models that support the given file type. [Images](/docs/en/build-with-claude/vision) are supported on all current Claude models. For [PDFs](/docs/en/build-with-claude/pdf-support) and [other file types with the code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool#model-compatibility), see the linked pages for model support.

The Files API is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). On Microsoft Foundry, the Files API requires a [Hosted on Anthropic deployment](/docs/en/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). It is not currently available on Amazon Bedrock or Google Cloud.

## How the Files API works

The Files API provides a create-once, use-many-times approach for working with files:

* **Upload files** to Anthropic's secure storage and receive a unique `file_id`
* **Download files** that are created by skills or the code execution tool
* **Reference files** in [Messages](/docs/en/api/messages/create) requests using the `file_id` instead of re-uploading content
* **Manage your files** with list, retrieve, and delete operations

## How to use the Files API

<Note>
  To use the Files API, you'll need to include the beta feature header: `anthropic-beta: files-api-2025-04-14`. The SDKs add this header automatically when you call methods on the `beta.files` namespace, so the SDK examples on this page don't pass it explicitly for file operations. Messages requests that reference a file do need it, which the SDK examples pass through their `betas` parameter.
</Note>

### Uploading a file

Upload a file to be referenced in future API calls:

<CodeGroup>
  ```bash cURL
  FILE_ID=$(curl -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@/path/to/document.pdf" | jq -r '.id')
  echo "$FILE_ID"
  ```

  ```bash CLI
  FILE_ID=$(ant beta:files upload \
    --file /path/to/document.pdf \
    --transform id \
    --raw-output)
  echo "$FILE_ID"
  ```

  ```python Python
  uploaded = client.beta.files.upload(
      file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
  )
  file_id = uploaded.id
  print(file_id)
  ```

  ```typescript TypeScript
  const uploaded = await client.beta.files.upload({
    file: await toFile(
      fs.createReadStream("/path/to/document.pdf"),
      undefined,
      { type: "application/pdf" },
    ),
  });
  console.log(uploaded.id);
  ```

  ```csharp C#
  var uploaded = await client.Beta.Files.Upload(
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

  response, err := client.Beta.Files.Upload(context.Background(),
  	anthropic.BetaFileUploadParams{
  		File: anthropic.File(f, "document.pdf", "application/pdf"),
  	})
  if err != nil {
  	log.Fatal(err)
  }

  fileID := response.ID
  fmt.Println(fileID)
  ```

  ```java Java
  FileMetadata file = client.beta().files().upload(
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
  $file = $client->beta->files->upload(
      FileParam::fromResource(fopen('/path/to/document.pdf', 'rb'), contentType: 'application/pdf'),
  );

  $fileId = $file->id;
  echo $fileId;
  ```

  ```ruby Ruby
  file = client.beta.files.upload(
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
  "downloadable": false
}
```

`downloadable` is `false` for files you upload. Only files created by [skills](/docs/en/build-with-claude/skills-guide) or the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool) can be downloaded. See [Downloading a file](#downloading-a-file).

### Using a file in messages

Once uploaded, reference the file by passing the `id` from the upload response as `file_id`:

<CodeGroup>
  ```bash cURL
  curl -X POST https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "model": "claude-opus-4-8",
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
  ant beta:messages create --beta files-api-2025-04-14 <<YAML
  model: claude-opus-4-8
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
  response = client.beta.messages.create(
      model="claude-opus-4-8",
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
      betas=["files-api-2025-04-14"],
  )
  print(response)
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
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
    betas: ["files-api-2025-04-14"],
  });

  console.log(response);
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Betas = [AnthropicBeta.FilesApi2025_04_14],
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = new List<BetaContentBlockParam>
                  {
                      new BetaTextBlockParam { Text = "Please summarize this document for me." },
                      new BetaRequestDocumentBlock
                      {
                          Source = new BetaFileDocumentSource { FileID = fileId }
                      }
                  }
              }
          ]
      });

  Console.WriteLine(response);
  ```

  ```go Go
  msg, err := client.Beta.Messages.New(context.Background(),
  	anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(
  				anthropic.NewBetaTextBlock("Please summarize this document for me."),
  				anthropic.NewBetaDocumentBlock(anthropic.BetaFileDocumentSourceParam{
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
      .model(Model.CLAUDE_OPUS_4_8)
      .addBeta("files-api-2025-04-14")
      .maxTokens(1024)
      .addUserMessageOfBetaContentBlockParams(List.of(
          BetaContentBlockParam.ofText(BetaTextBlockParam.builder()
              .text("Please summarize this document for me.")
              .build()),
          BetaContentBlockParam.ofDocument(BetaRequestDocumentBlock.builder()
              .source(BetaFileDocumentSource.builder()
                  .fileId(fileId)
                  .build())
              .build())
      ))
      .build();

  BetaMessage message = client.beta().messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
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
      model: 'claude-opus-4-8',
      betas: ['files-api-2025-04-14'],
  );

  print_r($response);
  ```

  ```ruby Ruby
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
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

| File type                                                                                                    | MIME type                                            | Content block type | Use case                            |
| ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ------------------ | ----------------------------------- |
| PDF                                                                                                          | `application/pdf`                                    | `document`         | Text analysis, document processing  |
| Plain text                                                                                                   | `text/plain`                                         | `document`         | Text analysis, processing           |
| Images                                                                                                       | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image`            | Image analysis, visual tasks        |
| [Datasets, others](/docs/en/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) | Varies                                               | `container_upload` | Analyze data, create visualizations |

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

To send a file to the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files), use the `container_upload` content block:

```json
{
  "type": "container_upload",
  "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
}
```

### Working with other file formats

For file types that the `document` block doesn't support (for example, .docx and .xlsx), convert the files to plain text and include the content directly in your message. Files that are already plain text, such as .csv and .md files, can either be read in this way or uploaded through the Files API with an explicit `text/plain` content type. To analyze datasets instead of reading them as text, upload them for the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) using a `container_upload` block.

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
    "model": "claude-opus-4-8",
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
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --transform 'content.0.text' \
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
      model="claude-opus-4-8",
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

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  import fs from "node:fs/promises";
  // ...
  const client = new Anthropic();

  // Read the text file
  const textContent = await fs.readFile("document.txt", "utf-8");

  const response = await client.messages.create({
    model: "claude-opus-4-8",
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

  const block = response.content[0];
  if (block.type === "text") {
    console.log(block.text);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Read the text file
  string textContent = await File.ReadAllTextAsync("document.txt");

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new()
      {
          Role = Role.User,
          Content = $"Here's the document content:\n\n{textContent}\n\nPlease summarize this document."
      }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Read the text file
  textContent, err := os.ReadFile("document.txt")
  if err != nil {
  	log.Fatal(err)
  }

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
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

  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Read the text file
  String textContent = Files.readString(Path.of("document.txt"));

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Read the text file
  text_content = File.read("document.txt")

  message = client.messages.create(
    model: "claude-opus-4-8",
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

  puts message.content.first.text
  ```
</CodeGroup>

<Note>
  For .docx files containing images, convert them to PDF format first, then use [PDF support](/docs/en/build-with-claude/pdf-support) to take advantage of the built-in image parsing. This allows using citations from the PDF document.
</Note>

### Managing files

#### List files

Retrieve a list of your uploaded files. The endpoint is paginated: each request returns up to `limit` files (20 by default), and the `before_id` and `after_id` parameters fetch the adjacent page. See the [List Files API reference](/docs/en/api/files-list). The SDKs return the first page and provide auto-pagination helpers. The CLI example bounds the total with `--max-items`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files list \
    --max-items 10
  ```

  ```python Python
  client = anthropic.Anthropic()
  files = client.beta.files.list()
  print(files)
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const files = await client.beta.files.list();
  console.log(files);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var files = await client.Beta.Files.List();
  Console.WriteLine(files);
  ```

  ```go Go
  client := anthropic.NewClient()

  files, err := client.Beta.Files.List(context.TODO(), anthropic.BetaFileListParams{})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(files)
  ```

  ```java Java
  import com.anthropic.models.beta.files.FileListPage;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      FileListPage files = client.beta().files().list();
      System.out.println(files);
  }
  ```

  ```php PHP
  $client = new Client();

  $files = $client->beta->files->list();
  print_r($files);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  files = client.beta.files.list
  puts files
  ```
</CodeGroup>

#### Get file metadata

Retrieve information about a specific file:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files retrieve-metadata \
    --file-id "$FILE_ID"
  ```

  ```python Python
  file = client.beta.files.retrieve_metadata(file_id)
  print(file)
  ```

  ```typescript TypeScript
  const file = await client.beta.files.retrieveMetadata(uploaded.id);
  console.log(file);
  ```

  ```csharp C#
  var file = await client.Beta.Files.RetrieveMetadata(fileId);
  Console.WriteLine(file);
  ```

  ```go Go
  metadata, err := client.Beta.Files.GetMetadata(
  	context.TODO(),
  	fileID,
  	anthropic.BetaFileGetMetadataParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(metadata)
  ```

  ```java Java
  FileMetadata metadata = client.beta().files().retrieveMetadata(fileId);

  System.out.println(metadata);
  ```

  ```php PHP
  $file = $client->beta->files->retrieveMetadata($fileId);
  echo $file;
  ```

  ```ruby Ruby
  file = client.beta.files.retrieve_metadata(file_id)
  puts file
  ```
</CodeGroup>

#### Delete a file

Remove a file from your workspace:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files delete \
    --file-id "$FILE_ID"
  ```

  ```python Python
  client.beta.files.delete(file_id)
  ```

  ```typescript TypeScript
  await client.beta.files.delete(uploaded.id);
  ```

  ```csharp C#
  await client.Beta.Files.Delete(fileId);
  ```

  ```go Go
  _, err = client.Beta.Files.Delete(
  	context.TODO(),
  	fileID,
  	anthropic.BetaFileDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  client.beta().files().delete(fileId);
  ```

  ```php PHP
  $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  client.beta.files.delete(file_id)
  ```
</CodeGroup>

### Downloading a file

Download files that were created by [skills](/docs/en/build-with-claude/skills-guide) or the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool). Files you upload cannot be downloaded. The `file_id` of a generated file appears in the [`code_execution_tool_result` content block](/docs/en/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) of the Messages response that created it:

<CodeGroup>
  ```bash cURL
  curl -X GET "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    --output downloaded_file.txt
  ```

  ```bash CLI
  ant beta:files download \
    --file-id "$FILE_ID" \
    --output downloaded_file.txt
  ```

  ```python Python
  file_content = client.beta.files.download(file_id)

  file_content.write_to_file("downloaded_file.txt")
  ```

  ```typescript TypeScript
  const content = await client.beta.files.download(uploaded.id);

  const bytes = Buffer.from(await content.arrayBuffer());
  await fsp.writeFile("downloaded_file.txt", bytes);
  ```

  ```csharp C#
  using var fileContent = await client.Beta.Files.Download(fileId);
  await using var source = await fileContent.ReadAsStream();
  await using var destination = File.Create("downloaded_file.txt");
  await source.CopyToAsync(destination);
  ```

  ```go Go
  func downloadFile(client anthropic.Client, fileID string) error {
  	resp, err := client.Beta.Files.Download(
  		context.TODO(),
  		fileID,
  		anthropic.BetaFileDownloadParams{},
  	)
  	if err != nil {
  		return err
  	}
  	defer resp.Body.Close()

  	fileContent, err := io.ReadAll(resp.Body)
  	if err != nil {
  		return err
  	}

  	return os.WriteFile("downloaded_file.txt", fileContent, 0644)
  }

  ```

  ```java Java
  try (HttpResponse response = client.beta().files().download(fileId)) {
      try (InputStream body = response.body()) {
          Files.copy(body, Path.of("downloaded_file.txt"),
              StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  $fileContent = $client->beta->files->download($fileId);

  file_put_contents("downloaded_file.txt", $fileContent);
  ```

  ```ruby Ruby
  file_content = client.beta.files.download(file_id)

  File.binwrite("downloaded_file.txt", file_content.read)
  ```
</CodeGroup>

<Note>
  A file is downloadable only when its metadata shows `"downloadable": true`, which is the case for files created by skills or the code execution tool. Downloading a file you uploaded returns a 400 error.
</Note>

## File storage and limits

### Storage limits

* **Maximum file size:** 500 MB per file
* **Total storage:** 500 GB per organization

### File lifecycle

* Files are scoped to the workspace of the API key that uploaded them. Any API key in the same workspace can reference them
* Files cannot be modified or renamed after upload. To change a file's content, upload a new file and delete the old one
* Files persist until you delete them with the `DELETE /v1/files/{file_id}` endpoint
* Deleted files cannot be recovered
* Files are inaccessible through the API shortly after deletion, but they may persist in active Messages API calls and associated tool uses
* Files that users delete will be deleted in accordance with Anthropic's [data retention policy](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data). For ZDR eligibility across all features, see [API and data retention](/docs/en/manage-claude/api-and-data-retention)

## Error handling

Common errors when using the Files API include:

* **File not found (404):** The specified `file_id` doesn't exist or you don't have access to it
* **Invalid file type (400):** The file type doesn't match the content block type (for example, using an image file in a document block)
* **Not downloadable (400):** Files you upload have `"downloadable": false` and cannot be downloaded. Only files created by skills or the code execution tool can be downloaded
* **Exceeds context window size (400):** The file is larger than the context window size (for example, using a 500 MB plain text file in a `/v1/messages` request)
* **Invalid filename (400):** The file name doesn't meet the length requirements (1-255 characters) or contains forbidden characters (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, or Unicode characters 0-31)
* **File too large (413):** File exceeds the 500 MB limit
* **Storage limit exceeded (400):** Your organization has reached the 500 GB storage limit

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

During the beta period:

* File-related API calls are limited to approximately 100 requests per minute
* [Contact us](mailto:sales@anthropic.com) if you need higher limits for your use case

## Next steps

<CardGroup cols={3}>
  <Card title="PDF support" icon="file" href="/docs/en/build-with-claude/pdf-support">
    Process PDFs with Claude. Extract text, analyze charts, and understand visual content from your documents.
  </Card>

  <Card title="Code execution tool" icon="terminal" href="/docs/en/agents-and-tools/tool-use/code-execution-tool">
    Run Python and bash code in a sandboxed container to analyze data, generate files, and iterate on solutions.
  </Card>

  <Card title="Vision" icon="image" href="/docs/en/build-with-claude/vision">
    Process and analyze visual input and generate text and code from images.
  </Card>
</CardGroup>
