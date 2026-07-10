# PDF support

Process PDFs with Claude: extract text, analyze charts, and understand visual content from your documents.

---

<Note>
  This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

You can ask Claude about any text, pictures, charts, and tables in PDFs you provide. Some sample use cases:

* Analyzing financial reports and understanding charts/tables
* Extracting key information from legal documents
* Translation assistance for documents
* Converting document information into structured formats

## Before you begin

### Check PDF requirements

Claude works with any standard PDF. Ensure your request size meets these requirements:

| Requirement               | Limit                                                                   |
| ------------------------- | ----------------------------------------------------------------------- |
| Maximum request size      | 32 MB ([varies by platform](/docs/en/api/overview#request-size-limits)) |
| Maximum pages per request | 600 (100 when the request's context window is under 1M tokens)          |
| Format                    | Standard PDF (no passwords/encryption)                                  |

Both limits are on the entire request payload, including any other content sent alongside PDFs. For large PDFs, consider uploading with the [Files API](#option-3-files-api) and referencing by `file_id` to keep request payloads small.

<Tip>
  Dense PDFs (many small-font pages, complex tables, or heavy graphics) can fill the context window before reaching the page limit. Requests with large PDFs can also fail before reaching the page limit, even when using the Files API. Try splitting the document into sections; for large files, since each page is processed as an image, downsampling embedded images can also help.
</Tip>

Since PDF support relies on Claude's vision capabilities, it is subject to the same [limitations and considerations](/docs/en/build-with-claude/vision#limitations) as other vision tasks.

### Supported platforms and models

PDF support is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) (see [Amazon Bedrock PDF support](#amazon-bedrock-pdf-support)), [Google Cloud](/docs/en/build-with-claude/claude-on-vertex-ai), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). All [active models](/docs/en/about-claude/models/overview) support PDF processing.

### Amazon Bedrock PDF support

When using PDF support through the Converse API, part of [Claude on Amazon Bedrock (legacy)](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy), there are two distinct document processing modes:

<Note>
  **Important:** To access Claude's full visual PDF understanding capabilities in the Converse API, you must enable citations. Without citations enabled, the API falls back to basic text extraction only. Learn more about [working with citations](/docs/en/build-with-claude/citations).
</Note>

#### Document processing modes

1. **Converse Document Chat** (Original mode - Text extraction only)

   * Provides basic text extraction from PDFs
   * Cannot analyze images, charts, or visual layouts within PDFs
   * Uses approximately 1,000 tokens for a 3-page PDF
   * Automatically used when citations are not enabled

2. **Claude PDF Chat** (New mode - Full visual understanding)

   * Provides complete visual analysis of PDFs
   * Can understand and analyze charts, graphs, images, and visual layouts
   * Processes each page as both text and image for comprehensive understanding
   * Uses approximately 7,000 tokens for a 3-page PDF
   * **Requires citations to be enabled** in the Converse API

#### Key limitations

* **Converse API**: Visual PDF analysis requires citations to be enabled. There is currently no option to use visual analysis without citations (unlike the InvokeModel API).
* **InvokeModel API**: Provides full control over PDF processing without forced citations.

#### Common issues

If Claude isn't seeing images or charts in your PDFs when using the Converse API, you likely need to enable the citations flag. Without it, Converse falls back to basic text extraction only.

<Note>
  This is a known constraint with the Converse API. For applications that require visual PDF analysis without citations, consider using the InvokeModel API instead.
</Note>

<Note>
  Plain text files such as .txt, .csv, or .md can be used directly in document blocks: upload them to the Files API with MIME type `text/plain` and reference them by `file_id`. Binary formats such as .xlsx or .docx are not supported in document blocks and must be converted to text or PDF first. See [Working with other file formats](/docs/en/build-with-claude/files#working-with-other-file-formats).
</Note>

## Process PDFs with Claude

### Send your first PDF request

Let's start with a simple example using the Messages API. You can provide PDFs to Claude in three ways:

1. As a URL reference to a PDF hosted online
2. As a base64-encoded PDF in `document` content blocks
3. By a `file_id` from the [Files API](/docs/en/build-with-claude/files)

<Note>
  On Amazon Bedrock and Google Cloud, only base64-encoded sources are currently available. On Microsoft Foundry, the Files API is not supported for deployments hosted on Azure.
</Note>

#### Option 1: URL-based PDF document

The simplest approach is to reference a PDF directly from a URL:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{
          "role": "user",
          "content": [{
              "type": "document",
              "source": {
                  "type": "url",
                  "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
              }
          },
          {
              "type": "text",
              "text": "What are the key findings in this document?"
          }]
      }]
  }'
  ```

  ```bash CLI
  ant messages create --transform content --format yaml <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: url
            url: https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf
        - type: text
          text: What are the key findings in this document?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "url",
                          "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
                      },
                  },
                  {"type": "text", "text": "What are the key findings in this document?"},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const response = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "url",
              url: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
            }
          },
          {
            type: "text",
            text: "What are the key findings in this document?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Create document block with URL
  var documentParam = new DocumentBlockParam
  {
      Source = new UrlPdfSource
      {
          Url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
      },
  };

  // Create a message with document and text content blocks
  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<ContentBlockParam>
              {
                  documentParam,
                  new TextBlockParam("What are the key findings in this document?"),
              },
          },
      ],
  });

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewDocumentBlock(anthropic.URLPDFSourceParam{
  				URL: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
  			}),
  			anthropic.NewTextBlock("What are the key findings in this document?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Create document block with URL
  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(
      UrlPdfSource.builder()
        .url(
          "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
        )
        .build()
    )
    .build();

  // Create a message with document and text content blocks
  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text("What are the key findings in this document?")
            .build()
        )
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'url',
                          'url' => 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf',
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What are the key findings in this document?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo $message;
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new

  message = anthropic.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "url",
              url: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
            }
          },
          {type: "text", text: "What are the key findings in this document?"}
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

The response returns Claude's analysis as text blocks in `content`, with token consumption in `usage`:

```json Output
{
  "id": "msg_01Hfp8YuFjQ55VgWbpdHDehB",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-4-8",
  "content": [
    {
      "type": "text",
      "text": "This document is an addendum to the Claude 3 model card, reporting updated evaluation results. The key findings include..."
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 300
  }
}
```

#### Option 2: Base64-encoded PDF document

If you need to send PDFs from your local system or when a URL isn't available:

<CodeGroup>
  ```bash cURL
  # Method 1: Fetch and encode a remote PDF
  curl -sL "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

  # Method 2: Encode a local PDF file
  # base64 document.pdf | tr -d '\n' > pdf_base64.txt

  # Create a JSON request file using the pdf_base64.txt content
  jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{
          "role": "user",
          "content": [{
              "type": "document",
              "source": {
                  "type": "base64",
                  "media_type": "application/pdf",
                  "data": $PDF_BASE64
              }
          },
          {
              "type": "text",
              "text": "What are the key findings in this document?"
          }]
      }]
  }' > request.json

  # Send the API request using the JSON file
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @request.json
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --transform content \
    --format yaml <<'YAML'
  messages:
    - role: user
      content:
        - type: document
          source:
            type: base64
            media_type: application/pdf
            data: "@./document.pdf"
        - type: text
          text: What are the key findings in this document?
  YAML
  ```

  ```python Python
  import base64
  import httpx

  # First, load and encode the PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_data = base64.standard_b64encode(
      httpx.get(pdf_url, follow_redirects=True).content
  ).decode("utf-8")

  # Alternative: Load from a local file
  # with open("document.pdf", "rb") as f:
  #     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

  # Send to Claude using base64 encoding
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": pdf_data,
                      },
                  },
                  {"type": "text", "text": "What are the key findings in this document?"},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  // Method 1: Fetch and encode a remote PDF
  const pdfURL =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  const pdfResponse = await fetch(pdfURL);
  const arrayBuffer = await pdfResponse.arrayBuffer();
  const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

  // Method 2: Load from a local file
  // import { readFile } from "node:fs/promises";
  // const pdfBase64 = (await readFile('document.pdf')).toString('base64');

  // Send the API request with base64-encoded PDF
  const anthropic = new Anthropic();
  const response = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdfBase64
            }
          },
          {
            type: "text",
            text: "What are the key findings in this document?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Method 1: Download and encode a remote PDF
  var pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  using var httpClient = new HttpClient();
  var pdfBase64 = Convert.ToBase64String(await httpClient.GetByteArrayAsync(pdfUrl));

  // Method 2: Load from a local file
  // var pdfBase64 = Convert.ToBase64String(await File.ReadAllBytesAsync("document.pdf"));

  // Create document block with base64 data
  var documentParam = new DocumentBlockParam
  {
      Source = new Base64PdfSource { Data = pdfBase64 },
  };

  // Create a message with document and text content blocks
  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<ContentBlockParam>
              {
                  documentParam,
                  new TextBlockParam("What are the key findings in this document?"),
              },
          },
      ],
  });

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  // First, load and encode the PDF
  pdfURL := "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  resp, err := http.Get(pdfURL)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  pdfBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	panic(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Alternative: Load from a local file (add "os" to the imports)
  // pdfBytes, err := os.ReadFile("document.pdf")
  // pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Send to Claude using base64 encoding
  client := anthropic.NewClient()
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  				Data: pdfBase64,
  			}),
  			anthropic.NewTextBlock("What are the key findings in this document?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Method 1: Download and encode a remote PDF
  String pdfUrl =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  HttpClient httpClient = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

  HttpResponse<byte[]> response = httpClient.send(
    request,
    HttpResponse.BodyHandlers.ofByteArray()
  );
  String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

  // Method 2: Load from a local file
  // byte[] fileBytes = Files.readAllBytes(Path.of("document.pdf"));
  // String pdfBase64 = Base64.getEncoder().encodeToString(fileBytes);

  // Create document block with base64 data
  DocumentBlockParam documentParam = DocumentBlockParam.builder()
    .source(Base64PdfSource.builder().data(pdfBase64).build())
    .build();

  // Create a message with document and text content blocks
  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(documentParam),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text("What are the key findings in this document?")
            .build()
        )
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  // First, load and encode the PDF
  $pdf_url = 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf';
  $pdf_data = base64_encode(file_get_contents($pdf_url));

  // Alternative: Load from a local file
  // $pdf_data = base64_encode(file_get_contents('document.pdf'));

  // Send to Claude using base64 encoding
  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'base64',
                          'media_type' => 'application/pdf',
                          'data' => $pdf_data,
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What are the key findings in this document?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo $message;
  ```

  ```ruby Ruby
  require "open-uri"

  # First, load and encode the PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_bytes = URI.open(pdf_url, "rb") { |f| f.read }
  pdf_data = [pdf_bytes].pack("m0") # Base64-encode without newlines

  # Alternative: Load from a local file
  # pdf_data = [File.binread("document.pdf")].pack("m0")

  # Send to Claude using base64 encoding
  anthropic = Anthropic::Client.new
  message = anthropic.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdf_data
            }
          },
          {type: "text", text: "What are the key findings in this document?"}
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

#### Option 3: Files API

For PDFs you'll use repeatedly, or when you want to avoid encoding overhead, use the [Files API](/docs/en/build-with-claude/files) (beta):

<CodeGroup>
  ```bash cURL
  # First, upload your PDF to the Files API
  FILE_ID=$(curl -sS -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@document.pdf" | jq -r '.id')

  # Then use the returned file_id in your message
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -d @- <<EOF
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [{
        "type": "document",
        "source": {
          "type": "file",
          "file_id": "$FILE_ID"
        }
      },
      {
        "type": "text",
        "text": "What are the key findings in this document?"
      }]
    }]
  }
  EOF
  ```

  ```bash CLI
  # First, upload your PDF to the Files API
  FILE_ID=$(ant beta:files upload \
    --file ./document.pdf \
    --transform id \
    --raw-output)

  # Then use the returned file_id in your message
  ant beta:messages create \
    --beta files-api-2025-04-14 \
    --transform content \
    --format yaml <<YAML
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: file
            file_id: $FILE_ID
        - type: text
          text: What are the key findings in this document?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Upload the PDF file
  with open("/path/to/document.pdf", "rb") as f:
      file_upload = client.beta.files.upload(file=("document.pdf", f, "application/pdf"))

  # Use the uploaded file in a message
  message = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      betas=["files-api-2025-04-14"],
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {"type": "file", "file_id": file_upload.id},
                  },
                  {"type": "text", "text": "What are the key findings in this document?"},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  import Anthropic, { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const anthropic = new Anthropic();

  // Upload the PDF file
  const fileUpload = await anthropic.beta.files.upload({
    file: await toFile(fs.createReadStream("/path/to/document.pdf"), undefined, {
      type: "application/pdf"
    })
  });

  // Use the uploaded file in a message
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "file",
              file_id: fileUpload.id
            }
          },
          {
            type: "text",
            text: "What are the key findings in this document?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  using Messages = Anthropic.Models.Messages;

  var client = new AnthropicClient();

  // Upload the PDF file
  var fileUpload = await client.Beta.Files.Upload(new FileUploadParams
  {
      File = new BinaryContent
      {
          Stream = File.OpenRead("/path/to/document.pdf"),
          FileName = "document.pdf",
          ContentType = new("application/pdf"),
      },
  });

  // Use the uploaded file in a message
  var message = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Betas = [AnthropicBeta.FilesApi2025_04_14],
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<BetaContentBlockParam>
              {
                  new BetaRequestDocumentBlock
                  {
                      Source = new BetaFileDocumentSource { FileID = fileUpload.ID },
                  },
                  new BetaTextBlockParam("What are the key findings in this document?"),
              },
          },
      ],
  });

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  // Upload the PDF file
  pdfFile, err := os.Open("/path/to/document.pdf")
  if err != nil {
  	panic(err)
  }
  defer pdfFile.Close()

  fileUpload, err := client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
  	File: anthropic.File(pdfFile, "document.pdf", "application/pdf"),
  })
  if err != nil {
  	panic(err)
  }

  // Use the uploaded file in a message
  message, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(
  			anthropic.NewBetaDocumentBlock(anthropic.BetaFileDocumentSourceParam{
  				FileID: fileUpload.ID,
  			}),
  			anthropic.NewBetaTextBlock("What are the key findings in this document?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Upload the PDF file
  FileMetadata file = client
    .beta()
    .files()
    .upload(FileUploadParams.builder().file(Path.of("/path/to/document.pdf")).build());

  // Use the uploaded file in a message
  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .addBeta("files-api-2025-04-14")
    .maxTokens(1024)
    .addUserMessageOfBetaContentBlockParams(
      List.of(
        BetaContentBlockParam.ofDocument(
          BetaRequestDocumentBlock.builder()
            .source(
              BetaFileDocumentSource.builder()
                .fileId(file.id())
                .build()
            )
            .build()
        ),
        BetaContentBlockParam.ofText(
          BetaTextBlockParam.builder()
            .text("What are the key findings in this document?")
            .build()
        )
      )
    )
    .build();

  BetaMessage message = client.beta().messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  // Upload the PDF file
  $file_upload = $client->beta->files->upload(
      file: FileParam::fromResource(fopen('/path/to/document.pdf', 'r'), contentType: 'application/pdf'),
  );

  // Use the uploaded file in a message
  $message = $client->beta->messages->create(
      maxTokens: 1024,
      betas: ['files-api-2025-04-14'],
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'file',
                          'file_id' => $file_upload->id,
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What are the key findings in this document?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo $message;
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new

  # Upload the PDF file
  file_upload = File.open("/path/to/document.pdf", "rb") do |f|
    anthropic.beta.files.upload(
      file: Anthropic::FilePart.new(f, filename: "document.pdf", content_type: "application/pdf")
    )
  end

  # Use the uploaded file in a message
  message = anthropic.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {type: "file", file_id: file_upload.id}
          },
          {type: "text", text: "What are the key findings in this document?"}
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

### How PDF support works

When you send a PDF to Claude, the following steps occur:

<Steps>
  <Step title="The system extracts the contents of the document.">
    * The system converts each page of the document into an image.
    * The text from each page is extracted and provided alongside each page's image.
  </Step>

  <Step title="Claude analyzes both the text and images to better understand the document.">
    * Documents are provided as a combination of text and images for analysis.
    * This allows users to ask for insights on visual elements of a PDF, such as charts, diagrams, and other non-textual content.
  </Step>

  <Step title="Claude responds, referencing the PDF's contents if relevant.">
    Claude can reference both textual and visual content when it responds. You can further improve performance by integrating PDF support with:

    * [Prompt caching](#use-prompt-caching): To improve performance for repeated analysis.
    * [Batch processing](#process-document-batches): For high-volume document processing.
    * [Tool use](/docs/en/agents-and-tools/tool-use/overview): To extract specific information from documents for use as tool inputs.
  </Step>
</Steps>

### Estimate your costs

The token count of a PDF file depends on the total text extracted from the document as well as the number of pages:

* Text token costs: Each page typically uses 1,500-3,000 tokens per page depending on content density. Standard API pricing applies with no additional PDF fees.
* Image token costs: Since each page is converted into an image, the same [image-based cost calculations](/docs/en/build-with-claude/vision#evaluate-image-size) are applied.

You can use [token counting](/docs/en/build-with-claude/token-counting) to estimate costs for your specific PDFs.

## Optimize PDF processing

### Improve performance

Follow these best practices for optimal results:

* Place PDFs before text in your requests
* Use standard fonts
* Ensure text is clear and legible
* Rotate pages to proper upright orientation
* Use logical page numbers (from PDF viewer) in prompts
* Split large PDFs into chunks when needed
* Enable prompt caching for repeated analysis

### Scale your implementation

For high-volume processing, consider these approaches:

#### Use prompt caching

Cache PDFs with [prompt caching](/docs/en/build-with-claude/prompt-caching) to improve performance on repeated queries:

<CodeGroup>
  ```bash cURL
  curl -sL "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
  # Create a JSON request file using the pdf_base64.txt content
  jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{
          "role": "user",
          "content": [{
              "type": "document",
              "source": {
                  "type": "base64",
                  "media_type": "application/pdf",
                  "data": $PDF_BASE64
              },
              "cache_control": {
                  "type": "ephemeral"
              }
          },
          {
              "type": "text",
              "text": "Which model has the highest human preference win rates across each use-case?"
          }]
      }]
  }' > request.json

  # Then make the API call using the JSON file
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @request.json
  ```

  ```bash CLI
  ant messages create --transform content --format yaml <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: document
          source:
            type: base64
            media_type: application/pdf
            data: "@./document.pdf"
          cache_control:
            type: ephemeral
        - type: text
          text: Which model has the highest human preference win rates across each use-case?
  YAML
  ```

  ```python Python
  import base64
  import httpx

  # First, load and encode the PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_data = base64.standard_b64encode(
      httpx.get(pdf_url, follow_redirects=True).content
  ).decode("utf-8")

  # Create a message with the cached document
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": pdf_data,
                      },
                      "cache_control": {"type": "ephemeral"},
                  },
                  {
                      "type": "text",
                      "text": "Which model has the highest human preference win rates across each use-case?",
                  },
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  // First, load and encode the PDF
  const pdfURL =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  const pdfResponse = await fetch(pdfURL);
  const arrayBuffer = await pdfResponse.arrayBuffer();
  const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

  // Create a message with the cached document
  const anthropic = new Anthropic();
  const response = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdfBase64
            },
            cache_control: { type: "ephemeral" }
          },
          {
            type: "text",
            text: "Which model has the highest human preference win rates across each use-case?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Download and encode the PDF
  var pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  using var httpClient = new HttpClient();
  var pdfBase64 = Convert.ToBase64String(await httpClient.GetByteArrayAsync(pdfUrl));

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new List<ContentBlockParam>
              {
                  new DocumentBlockParam
                  {
                      Source = new Base64PdfSource { Data = pdfBase64 },
                      CacheControl = new CacheControlEphemeral(),
                  },
                  new TextBlockParam("Which model has the highest human preference win rates across each use-case?"),
              },
          },
      ],
  });

  Console.WriteLine(message);
  ```

  ```go Go
  // First, load and encode the PDF
  pdfURL := "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  resp, err := http.Get(pdfURL)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  pdfBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	panic(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Create a document block with cache control
  client := anthropic.NewClient()
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{
  				OfDocument: &anthropic.DocumentBlockParam{
  					Source: anthropic.DocumentBlockParamSourceUnion{
  						OfBase64: &anthropic.Base64PDFSourceParam{
  							Data: pdfBase64,
  						},
  					},
  					CacheControl: anthropic.NewCacheControlEphemeralParam(),
  				},
  			},
  			anthropic.NewTextBlock("Which model has the highest human preference win rates across each use-case?"),
  		),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Download and encode the PDF
  String pdfUrl =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  HttpClient httpClient = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

  HttpResponse<byte[]> response = httpClient.send(
    request,
    HttpResponse.BodyHandlers.ofByteArray()
  );
  String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessageOfBlockParams(
      List.of(
        ContentBlockParam.ofDocument(
          DocumentBlockParam.builder()
            .source(Base64PdfSource.builder().data(pdfBase64).build())
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        ),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text(
              "Which model has the highest human preference win rates across each use-case?"
            )
            .build()
        )
      )
    )
    .build();

  Message message = client.messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  // Load and encode the PDF
  $pdf_url = 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf';
  $pdf_data = base64_encode(file_get_contents($pdf_url));

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'base64',
                          'media_type' => 'application/pdf',
                          'data' => $pdf_data,
                      ],
                      'cache_control' => ['type' => 'ephemeral'],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Which model has the highest human preference win rates across each use-case?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo $message;
  ```

  ```ruby Ruby
  require "open-uri"

  # Load and encode the PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_bytes = URI.open(pdf_url, "rb") { |f| f.read }
  pdf_data = [pdf_bytes].pack("m0") # Base64-encode without newlines

  anthropic = Anthropic::Client.new

  message = anthropic.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdf_data
            },
            cache_control: {type: "ephemeral"}
          },
          {
            type: "text",
            text: "Which model has the highest human preference win rates across each use-case?"
          }
        ]
      }
    ]
  )

  puts(message.content)
  ```
</CodeGroup>

#### Process document batches

Use the [Message Batches API](/docs/en/build-with-claude/batch-processing) to process many PDFs in one request:

<CodeGroup>
  ```bash cURL
  curl -sL "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt
  # Create a JSON request file using the pdf_base64.txt content
  jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
      "requests": [
      {
          "custom_id": "my-first-request",
          "params": {
              "model": "claude-opus-4-8",
              "max_tokens": 1024,
              "messages": [{
                  "role": "user",
                  "content": [{
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": $PDF_BASE64
                      }
                  },
                  {
                      "type": "text",
                      "text": "Which model has the highest human preference win rates across each use-case?"
                  }]
              }]
          }
      },
      {
          "custom_id": "my-second-request",
          "params": {
              "model": "claude-opus-4-8",
              "max_tokens": 1024,
              "messages": [{
                  "role": "user",
                  "content": [{
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": $PDF_BASE64
                      }
                  },
                  {
                      "type": "text",
                      "text": "Extract 5 key insights from this document."
                  }]
              }]
          }
      }]
  }' > request.json

  # Then make the API call using the JSON file
  curl https://api.anthropic.com/v1/messages/batches \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @request.json
  ```

  ```bash CLI
  ant messages:batches create <<'YAML'
  requests:
    - custom_id: my-first-request
      params:
        model: claude-opus-4-8
        max_tokens: 1024
        messages:
          - role: user
            content:
              - type: document
                source:
                  type: base64
                  media_type: application/pdf
                  data: "@./document.pdf"
              - type: text
                text: >-
                  Which model has the highest human preference win rates
                  across each use-case?
    - custom_id: my-second-request
      params:
        model: claude-opus-4-8
        max_tokens: 1024
        messages:
          - role: user
            content:
              - type: document
                source:
                  type: base64
                  media_type: application/pdf
                  data: "@./document.pdf"
              - type: text
                text: Extract 5 key insights from this document.
  YAML
  ```

  ```python Python
  import base64
  import httpx

  # First, load and encode the PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_data = base64.standard_b64encode(
      httpx.get(pdf_url, follow_redirects=True).content
  ).decode("utf-8")

  # Create a batch of requests that use the document
  client = anthropic.Anthropic()
  message_batch = client.messages.batches.create(
      requests=[
          {
              "custom_id": "my-first-request",
              "params": {
                  "model": "claude-opus-4-8",
                  "max_tokens": 1024,
                  "messages": [
                      {
                          "role": "user",
                          "content": [
                              {
                                  "type": "document",
                                  "source": {
                                      "type": "base64",
                                      "media_type": "application/pdf",
                                      "data": pdf_data,
                                  },
                              },
                              {
                                  "type": "text",
                                  "text": "Which model has the highest human preference win rates across each use-case?",
                              },
                          ],
                      }
                  ],
              },
          },
          {
              "custom_id": "my-second-request",
              "params": {
                  "model": "claude-opus-4-8",
                  "max_tokens": 1024,
                  "messages": [
                      {
                          "role": "user",
                          "content": [
                              {
                                  "type": "document",
                                  "source": {
                                      "type": "base64",
                                      "media_type": "application/pdf",
                                      "data": pdf_data,
                                  },
                              },
                              {
                                  "type": "text",
                                  "text": "Extract 5 key insights from this document.",
                              },
                          ],
                      }
                  ],
              },
          },
      ]
  )

  print(message_batch)
  ```

  ```typescript TypeScript
  // First, load and encode the PDF
  const pdfURL =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  const pdfResponse = await fetch(pdfURL);
  const arrayBuffer = await pdfResponse.arrayBuffer();
  const pdfBase64 = Buffer.from(arrayBuffer).toString("base64");

  // Create a batch of requests that use the document
  const anthropic = new Anthropic();
  const response = await anthropic.messages.batches.create({
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-4-8",
          max_tokens: 1024,
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "document",
                  source: {
                    type: "base64",
                    media_type: "application/pdf",
                    data: pdfBase64
                  }
                },
                {
                  type: "text",
                  text: "Which model has the highest human preference win rates across each use-case?"
                }
              ]
            }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-4-8",
          max_tokens: 1024,
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "document",
                  source: {
                    type: "base64",
                    media_type: "application/pdf",
                    data: pdfBase64
                  }
                },
                {
                  type: "text",
                  text: "Extract 5 key insights from this document."
                }
              ]
            }
          ]
        }
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  // Download and encode the PDF
  var pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  using var httpClient = new HttpClient();
  var pdfBase64 = Convert.ToBase64String(await httpClient.GetByteArrayAsync(pdfUrl));

  var batch = await client.Messages.Batches.Create(new BatchCreateParams
  {
      Requests =
      [
          new()
          {
              CustomID = "my-first-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus4_8,
                  MaxTokens = 1024,
                  Messages =
                  [
                      new()
                      {
                          Role = Role.User,
                          Content = new List<ContentBlockParam>
                          {
                              new DocumentBlockParam
                              {
                                  Source = new Base64PdfSource { Data = pdfBase64 },
                              },
                              new TextBlockParam("Which model has the highest human preference win rates across each use-case?"),
                          },
                      },
                  ],
              },
          },
          new()
          {
              CustomID = "my-second-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus4_8,
                  MaxTokens = 1024,
                  Messages =
                  [
                      new()
                      {
                          Role = Role.User,
                          Content = new List<ContentBlockParam>
                          {
                              new DocumentBlockParam
                              {
                                  Source = new Base64PdfSource { Data = pdfBase64 },
                              },
                              new TextBlockParam("Extract 5 key insights from this document."),
                          },
                      },
                  ],
              },
          },
      ],
  });

  Console.WriteLine(batch);
  ```

  ```go Go
  // First, load and encode the PDF
  pdfURL := "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  resp, err := http.Get(pdfURL)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  pdfBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	panic(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  // Create a batch of requests that use the document
  client := anthropic.NewClient()
  batch, err := client.Messages.Batches.New(context.TODO(), anthropic.MessageBatchNewParams{
  	Requests: []anthropic.MessageBatchNewParamsRequest{
  		{
  			CustomID: "my-first-request",
  			Params: anthropic.MessageBatchNewParamsRequestParams{
  				Model:     anthropic.ModelClaudeOpus4_8,
  				MaxTokens: 1024,
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(
  						anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  							Data: pdfBase64,
  						}),
  						anthropic.NewTextBlock("Which model has the highest human preference win rates across each use-case?"),
  					),
  				},
  			},
  		},
  		{
  			CustomID: "my-second-request",
  			Params: anthropic.MessageBatchNewParamsRequestParams{
  				Model:     anthropic.ModelClaudeOpus4_8,
  				MaxTokens: 1024,
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(
  						anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  							Data: pdfBase64,
  						}),
  						anthropic.NewTextBlock("Extract 5 key insights from this document."),
  					),
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", batch)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Download and encode the PDF
  String pdfUrl =
    "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
  HttpClient httpClient = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(pdfUrl)).GET().build();

  HttpResponse<byte[]> response = httpClient.send(
    request,
    HttpResponse.BodyHandlers.ofByteArray()
  );
  String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

  BatchCreateParams params = BatchCreateParams.builder()
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("my-first-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024)
            .addUserMessageOfBlockParams(
              List.of(
                ContentBlockParam.ofDocument(
                  DocumentBlockParam.builder()
                    .source(Base64PdfSource.builder().data(pdfBase64).build())
                    .build()
                ),
                ContentBlockParam.ofText(
                  TextBlockParam.builder()
                    .text(
                      "Which model has the highest human preference win rates across each use-case?"
                    )
                    .build()
                )
              )
            )
            .build()
        )
        .build()
    )
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("my-second-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024)
            .addUserMessageOfBlockParams(
              List.of(
                ContentBlockParam.ofDocument(
                  DocumentBlockParam.builder()
                    .source(Base64PdfSource.builder().data(pdfBase64).build())
                    .build()
                ),
                ContentBlockParam.ofText(
                  TextBlockParam.builder()
                    .text("Extract 5 key insights from this document.")
                    .build()
                )
              )
            )
            .build()
        )
        .build()
    )
    .build();

  MessageBatch batch = client.messages().batches().create(params);
  System.out.println(batch);
  ```

  ```php PHP
  $client = new Client();

  // Load and encode the PDF
  $pdf_url = 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf';
  $pdf_data = base64_encode(file_get_contents($pdf_url));

  $batch = $client->messages->batches->create(
      requests: [
          [
              'custom_id' => 'my-first-request',
              'params' => [
                  'model' => 'claude-opus-4-8',
                  'max_tokens' => 1024,
                  'messages' => [
                      [
                          'role' => 'user',
                          'content' => [
                              [
                                  'type' => 'document',
                                  'source' => [
                                      'type' => 'base64',
                                      'media_type' => 'application/pdf',
                                      'data' => $pdf_data,
                                  ],
                              ],
                              [
                                  'type' => 'text',
                                  'text' => 'Which model has the highest human preference win rates across each use-case?',
                              ],
                          ],
                      ],
                  ],
              ],
          ],
          [
              'custom_id' => 'my-second-request',
              'params' => [
                  'model' => 'claude-opus-4-8',
                  'max_tokens' => 1024,
                  'messages' => [
                      [
                          'role' => 'user',
                          'content' => [
                              [
                                  'type' => 'document',
                                  'source' => [
                                      'type' => 'base64',
                                      'media_type' => 'application/pdf',
                                      'data' => $pdf_data,
                                  ],
                              ],
                              [
                                  'type' => 'text',
                                  'text' => 'Extract 5 key insights from this document.',
                              ],
                          ],
                      ],
                  ],
              ],
          ],
      ],
  );

  echo $batch;
  ```

  ```ruby Ruby
  require "open-uri"

  # Load and encode the PDF
  pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
  pdf_bytes = URI.open(pdf_url, "rb") { |f| f.read }
  pdf_data = [pdf_bytes].pack("m0") # Base64-encode without newlines

  anthropic = Anthropic::Client.new

  message_batch = anthropic.messages.batches.create(
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-4-8",
          max_tokens: 1024,
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "document",
                  source: {
                    type: "base64",
                    media_type: "application/pdf",
                    data: pdf_data
                  }
                },
                {
                  type: "text",
                  text: "Which model has the highest human preference win rates across each use-case?"
                }
              ]
            }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-4-8",
          max_tokens: 1024,
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "document",
                  source: {
                    type: "base64",
                    media_type: "application/pdf",
                    data: pdf_data
                  }
                },
                {
                  type: "text",
                  text: "Extract 5 key insights from this document."
                }
              ]
            }
          ]
        }
      }
    ]
  )

  puts(message_batch)
  ```
</CodeGroup>

Batches process asynchronously. To check progress and retrieve results once processing ends, see [Batch processing](/docs/en/build-with-claude/batch-processing).

## Next steps

<CardGroup cols={2}>
  <Card title="Vision" icon="image" href="/docs/en/build-with-claude/vision">
    Claude's vision capabilities allow it to understand and analyze images, opening up exciting possibilities for multimodal interaction.
  </Card>

  <Card title="Try PDF examples" icon="file" href="https://platform.claude.com/cookbook/multimodal-getting-started-with-vision">
    Explore practical examples of PDF processing in the cookbook recipe.
  </Card>

  <Card title="View API reference" icon="code" href="/docs/en/api/messages/create">
    See complete API documentation for PDF support.
  </Card>
</CardGroup>
