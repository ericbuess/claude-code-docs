# PDF support

Process PDFs with Claude. Extract text, analyze charts, and understand visual content from your documents.

---

You can now ask Claude about any text, pictures, charts, and tables in PDFs you provide. Some sample use cases:
- Analyzing financial reports and understanding charts/tables
- Extracting key information from legal documents
- Translation assistance for documents
- Converting document information into structured formats

## Before you begin

### Check PDF requirements
Claude works with any standard PDF. However, you should ensure your request size meets these requirements when using PDF support:

| Requirement | Limit |
|------------|--------|
| Maximum request size | 32MB |
| Maximum pages per request | 100 |
| Format | Standard PDF (no passwords/encryption) |

Please note that both limits are on the entire request payload, including any other content sent alongside PDFs.

Since PDF support relies on Claude's vision capabilities, it is subject to the same [limitations and considerations](/docs/en/build-with-claude/vision#limitations) as other vision tasks.

### Supported platforms and models

PDF support is currently supported via direct API access and Google Vertex AI. All [active models](/docs/en/about-claude/models/overview) support PDF processing.

PDF support is now available on Amazon Bedrock with the following considerations:

### Amazon Bedrock PDF Support

When using PDF support through Amazon Bedrock's Converse API, there are two distinct document processing modes:

<Note>
**Important**: To access Claude's full visual PDF understanding capabilities in the Converse API, you must enable citations. Without citations enabled, the API falls back to basic text extraction only. Learn more about [working with citations](/docs/en/build-with-claude/citations).
</Note>

#### Document Processing Modes

1. **Converse Document Chat** (Original mode - Text extraction only)
   - Provides basic text extraction from PDFs
   - Cannot analyze images, charts, or visual layouts within PDFs
   - Uses approximately 1,000 tokens for a 3-page PDF
   - Automatically used when citations are not enabled

2. **Claude PDF Chat** (New mode - Full visual understanding)
   - Provides complete visual analysis of PDFs
   - Can understand and analyze charts, graphs, images, and visual layouts
   - Processes each page as both text and image for comprehensive understanding
   - Uses approximately 7,000 tokens for a 3-page PDF
   - **Requires citations to be enabled** in the Converse API

#### Key Limitations

- **Converse API**: Visual PDF analysis requires citations to be enabled. There is currently no option to use visual analysis without citations (unlike the InvokeModel API).
- **InvokeModel API**: Provides full control over PDF processing without forced citations.

#### Common Issues

If customers report that Claude isn't seeing images or charts in their PDFs when using the Converse API, they likely need to enable the citations flag. Without it, Converse falls back to basic text extraction only.

<Note>
This is a known constraint with the Converse API that we're working to address. For applications that require visual PDF analysis without citations, consider using the InvokeModel API instead.
</Note>

<Note>
For non-PDF files like .csv, .xlsx, .docx, .md, or .txt files, see [Working with other file formats](/docs/en/build-with-claude/files#working-with-other-file-formats).
</Note>

***

## Process PDFs with Claude

### Send your first PDF request
Let's start with a simple example using the Messages API. You can provide PDFs to Claude in three ways:

1. As a URL reference to a PDF hosted online
2. As a base64-encoded PDF in `document` content blocks  
3. By a `file_id` from the [Files API](/docs/en/build-with-claude/files)

#### Option 1: URL-based PDF document

The simplest approach is to reference a PDF directly from a URL:

<CodeGroup>
   ```bash Shell
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-sonnet-4-5",
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
    ```python Python
    import anthropic

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "url",
                            "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
                        }
                    },
                    {
                        "type": "text",
                        "text": "What are the key findings in this document?"
                    }
                ]
            }
        ],
    )

    print(message.content)
    ```
    ```typescript TypeScript
    import Anthropic from '@anthropic-ai/sdk';

    const anthropic = new Anthropic();
    
    async function main() {
      const response = await anthropic.messages.create({
        model: 'claude-sonnet-4-5',
        max_tokens: 1024,
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'document',
                source: {
                  type: 'url',
                  url: 'https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf',
                },
              },
              {
                type: 'text',
                text: 'What are the key findings in this document?',
              },
            ],
          },
        ],
      });
      
      console.log(response);
    }
    
    main();
    ```
    ```java Java
    import java.util.List;

    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.MessageCreateParams;
    import com.anthropic.models.messages.*;

    public class PdfExample {
        public static void main(String[] args) {
            AnthropicClient client = AnthropicOkHttpClient.fromEnv();

            // Create document block with URL
            DocumentBlockParam documentParam = DocumentBlockParam.builder()
                    .urlPdfSource("https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf")
                    .build();

            // Create a message with document and text content blocks
            MessageCreateParams params = MessageCreateParams.builder()
                    .model(Model.CLAUDE_OPUS_4_20250514)
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
        }
    }
    ```
</CodeGroup>

#### Option 2: Base64-encoded PDF document

If you need to send PDFs from your local system or when a URL isn't available:

<CodeGroup>
    ```bash Shell
    # Method 1: Fetch and encode a remote PDF
    curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

    # Method 2: Encode a local PDF file
    # base64 document.pdf | tr -d '\n' > pdf_base64.txt

    # Create a JSON request file using the pdf_base64.txt content
    jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
        "model": "claude-sonnet-4-5",
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
    ```python Python
    import anthropic
    import base64
    import httpx

    # First, load and encode the PDF 
    pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
    pdf_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")

    # Alternative: Load from a local file
    # with open("document.pdf", "rb") as f:
    #     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Send to Claude using base64 encoding
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-5",
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
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "What are the key findings in this document?"
                    }
                ]
            }
        ],
    )

    print(message.content)
    ```
    ```typescript TypeScript
    import Anthropic from '@anthropic-ai/sdk';
    import fetch from 'node-fetch';
    import fs from 'fs';

    async function main() {
      // Method 1: Fetch and encode a remote PDF
      const pdfURL = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
      const pdfResponse = await fetch(pdfURL);
      const arrayBuffer = await pdfResponse.arrayBuffer();
      const pdfBase64 = Buffer.from(arrayBuffer).toString('base64');
      
      // Method 2: Load from a local file
      // const pdfBase64 = fs.readFileSync('document.pdf').toString('base64');
      
      // Send the API request with base64-encoded PDF
      const anthropic = new Anthropic();
      const response = await anthropic.messages.create({
        model: 'claude-sonnet-4-5',
        max_tokens: 1024,
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'document',
                source: {
                  type: 'base64',
                  media_type: 'application/pdf',
                  data: pdfBase64,
                },
              },
              {
                type: 'text',
                text: 'What are the key findings in this document?',
              },
            ],
          },
        ],
      });
      
      console.log(response);
    }
    
    main();
    ```

    ```java Java
    import java.io.IOException;
    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.util.Base64;
    import java.util.List;

    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.ContentBlockParam;
    import com.anthropic.models.messages.DocumentBlockParam;
    import com.anthropic.models.messages.Message;
    import com.anthropic.models.messages.MessageCreateParams;
    import com.anthropic.models.messages.Model;
    import com.anthropic.models.messages.TextBlockParam;

    public class PdfExample {
        public static void main(String[] args) throws IOException, InterruptedException {
            AnthropicClient client = AnthropicOkHttpClient.fromEnv();

            // Method 1: Download and encode a remote PDF
            String pdfUrl = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf";
            HttpClient httpClient = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(pdfUrl))
                    .GET()
                    .build();

            HttpResponse<byte[]> response = httpClient.send(request, HttpResponse.BodyHandlers.ofByteArray());
            String pdfBase64 = Base64.getEncoder().encodeToString(response.body());

            // Method 2: Load from a local file
            // byte[] fileBytes = Files.readAllBytes(Path.of("document.pdf"));
            // String pdfBase64 = Base64.getEncoder().encodeToString(fileBytes);

            // Create document block with base64 data
            DocumentBlockParam documentParam = DocumentBlockParam.builder()
                    .base64PdfSource(pdfBase64)
                    .build();

            // Create a message with document and text content blocks
            MessageCreateParams params = MessageCreateParams.builder()
                    .model(Model.CLAUDE_OPUS_4_20250514)
                    .maxTokens(1024)
                    .addUserMessageOfBlockParams(
                            List.of(
                                    ContentBlockParam.ofDocument(documentParam),
                                    ContentBlockParam.ofText(TextBlockParam.builder().text("What are the key findings in this document?").build())
                            )
                    )
                    .build();

            Message message = client.messages().create(params);
            message.content().stream()
                    .flatMap(contentBlock -> contentBlock.text().stream())
                    .forEach(textBlock -> System.out.println(textBlock.text()));
        }
    }
    ```

</CodeGroup>

#### Option 3: Files API

For PDFs you'll use repeatedly, or when you want to avoid encoding overhead, use the [Files API](/docs/en/build-with-claude/files): 

<CodeGroup>
```bash Shell
# First, upload your PDF to the Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@document.pdf"

# Then use the returned file_id in your message
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -d '{
    "model": "claude-sonnet-4-5", 
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [{
        "type": "document",
        "source": {
          "type": "file",
          "file_id": "file_abc123"
        }
      },
      {
        "type": "text",
        "text": "What are the key findings in this document?"
      }]
    }]
  }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

# Upload the PDF file
with open("document.pdf", "rb") as f:
    file_upload = client.beta.files.upload(file=("document.pdf", f, "application/pdf"))

# Use the uploaded file in a message
message = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    betas=["files-api-2025-04-14"],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file_upload.id
                    }
                },
                {
                    "type": "text",
                    "text": "What are the key findings in this document?"
                }
            ]
        }
    ],
)

print(message.content)
```

```typescript TypeScript
import { Anthropic, toFile } from '@anthropic-ai/sdk';
import fs from 'fs';

const anthropic = new Anthropic();

async function main() {
  // Upload the PDF file
  const fileUpload = await anthropic.beta.files.upload({
    file: toFile(fs.createReadStream('document.pdf'), undefined, { type: 'application/pdf' })
  }, {
    betas: ['files-api-2025-04-14']
  });

  // Use the uploaded file in a message
  const response = await anthropic.beta.messages.create({
    model: 'claude-sonnet-4-5',
    max_tokens: 1024,
    betas: ['files-api-2025-04-14'],
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'document',
            source: {
              type: 'file',
              file_id: fileUpload.id
            }
          },
          {
            type: 'text',
            text: 'What are the key findings in this document?'
          }
        ]
      }
    ]
  });

  console.log(response);
}

main();
```

```java Java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.File;
import com.anthropic.models.files.FileUploadParams;
import com.anthropic.models.messages.*;

public class PdfFilesExample {
    public static void main(String[] args) throws IOException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Upload the PDF file
        File file = client.beta().files().upload(FileUploadParams.builder()
                .file(Files.newInputStream(Path.of("document.pdf")))
                .build());

        // Use the uploaded file in a message
        DocumentBlockParam documentParam = DocumentBlockParam.builder()
                .fileSource(file.id())
                .build();

        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_20250514)
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
    }
}
```
</CodeGroup>

### How PDF support works
When you send a PDF to Claude, the following steps occur:
<Steps>
  <Step title="The system extracts the contents of the document.">
    - The system converts each page of the document into an image.
    - The text from each page is extracted and provided alongside each page's image.
  </Step>
  <Step title="Claude analyzes both the text and images to better understand the document.">
    - Documents are provided as a combination of text and images for analysis.
    - This allows users to ask for insights on visual elements of a PDF, such as charts, diagrams, and other non-textual content.
  </Step>
  <Step title="Claude responds, referencing the PDF's contents if relevant.">
    Claude can reference both textual and visual content when it responds. You can further improve performance by integrating PDF support with:
    - **Prompt caching**: To improve performance for repeated analysis.
    - **Batch processing**: For high-volume document processing.
    - **Tool use**: To extract specific information from documents for use as tool inputs.
  </Step>
</Steps>

### Estimate your costs
The token count of a PDF file depends on the total text extracted from the document as well as the number of pages:
- Text token costs: Each page typically uses 1,500-3,000 tokens per page depending on content density. Standard API pricing applies with no additional PDF fees.
- Image token costs: Since each page is converted into an image, the same [image-based cost calculations](/docs/en/build-with-claude/vision#evaluate-image-size) are applied.

You can use [token counting](/docs/en/build-with-claude/token-counting) to estimate costs for your specific PDFs.

***

## Optimize PDF processing

### Improve performance
Follow these best practices for optimal results:
- Place PDFs before text in your requests
- Use standard fonts
- Ensure text is clear and legible
- Rotate pages to proper upright orientation
- Use logical page numbers (from PDF viewer) in prompts
- Split large PDFs into chunks when needed
- Enable prompt caching for repeated analysis

### Scale your implementation
For high-volume processing, consider these approaches:

#### Use prompt caching
Cache PDFs to improve performance on repeated queries:
<CodeGroup>
```bash Shell
# Create a JSON request file using the pdf_base64.txt content
jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
    "model": "claude-sonnet-4-5",
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
```python Python
message = client.messages.create(
    model="claude-sonnet-4-5",
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
                        "data": pdf_data
                    },
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": "Analyze this document."
                }
            ]
        }
    ],
)
```

```typescript TypeScript
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-5',
  max_tokens: 1024,
  messages: [
    {
      content: [
        {
          type: 'document',
          source: {
            media_type: 'application/pdf',
            type: 'base64',
            data: pdfBase64,
          },
          cache_control: { type: 'ephemeral' },
        },
        {
          type: 'text',
          text: 'Which model has the highest human preference win rates across each use-case?',
        },
      ],
      role: 'user',
    },
  ],
});
console.log(response);
```

```java Java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Base64PdfSource;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.DocumentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;

public class MessagesDocumentExample {

    public static void main(String[] args) throws IOException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Read PDF file as base64
        byte[] pdfBytes = Files.readAllBytes(Paths.get("pdf_base64.txt"));
        String pdfBase64 = new String(pdfBytes);

        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_20250514)
                .maxTokens(1024)
                .addUserMessageOfBlockParams(List.of(
                        ContentBlockParam.ofDocument(
                                DocumentBlockParam.builder()
                                        .source(Base64PdfSource.builder()
                                                .data(pdfBase64)
                                                .build())
                                        .cacheControl(CacheControlEphemeral.builder().build())
                                        .build()),
                        ContentBlockParam.ofText(
                                TextBlockParam.builder()
                                        .text("Which model has the highest human preference win rates across each use-case?")
                                        .build())
                ))
                .build();


        Message message = client.messages().create(params);
        System.out.println(message);
    }
}
```
</CodeGroup>

#### Process document batches
Use the Message Batches API for high-volume workflows:
<CodeGroup>
```bash Shell
# Create a JSON request file using the pdf_base64.txt content
jq -n --rawfile PDF_BASE64 pdf_base64.txt '
{
  "requests": [
      {
          "custom_id": "my-first-request",
          "params": {
              "model": "claude-sonnet-4-5",
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
                                "data": $PDF_BASE64
                            }
                        },
                        {
                            "type": "text",
                            "text": "Which model has the highest human preference win rates across each use-case?"
                        }
                    ]
                }
              ]
          }
      },
      {
          "custom_id": "my-second-request",
          "params": {
              "model": "claude-sonnet-4-5",
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
                                "data": $PDF_BASE64
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract 5 key insights from this document."
                        }
                    ]
                }
              ]
          }
      }
  ]
}
' > request.json

# Then make the API call using the JSON file
curl https://api.anthropic.com/v1/messages/batches \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json
```
```python Python
message_batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "doc1",
            "params": {
                "model": "claude-sonnet-4-5",
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
                                    "data": pdf_data
                                }
                            },
                            {
                                "type": "text",
                                "text": "Summarize this document."
                            }
                        ]
                    }
                ]
            }
        }
    ]
)
```

```typescript TypeScript
const response = await anthropic.messages.batches.create({
  requests: [
    {
      custom_id: 'my-first-request',
      params: {
        max_tokens: 1024,
        messages: [
          {
            content: [
              {
                type: 'document',
                source: {
                  media_type: 'application/pdf',
                  type: 'base64',
                  data: pdfBase64,
                },
              },
              {
                type: 'text',
                text: 'Which model has the highest human preference win rates across each use-case?',
              },
            ],
            role: 'user',
          },
        ],
        model: 'claude-sonnet-4-5',
      },
    },
    {
      custom_id: 'my-second-request',
      params: {
        max_tokens: 1024,
        messages: [
          {
            content: [
              {
                type: 'document',
                source: {
                  media_type: 'application/pdf',
                  type: 'base64',
                  data: pdfBase64,
                },
              },
              {
                type: 'text',
                text: 'Extract 5 key insights from this document.',
              },
            ],
            role: 'user',
          },
        ],
        model: 'claude-sonnet-4-5',
      },
    }
  ],
});
console.log(response);
```

```java Java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.*;
import com.anthropic.models.messages.batches.*;

public class MessagesBatchDocumentExample {

    public static void main(String[] args) throws IOException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Read PDF file as base64
        byte[] pdfBytes = Files.readAllBytes(Paths.get("pdf_base64.txt"));
        String pdfBase64 = new String(pdfBytes);

        BatchCreateParams params = BatchCreateParams.builder()
                .addRequest(BatchCreateParams.Request.builder()
                        .customId("my-first-request")
                        .params(BatchCreateParams.Request.Params.builder()
                                .model(Model.CLAUDE_OPUS_4_20250514)
                                .maxTokens(1024)
                                .addUserMessageOfBlockParams(List.of(
                                        ContentBlockParam.ofDocument(
                                                DocumentBlockParam.builder()
                                                        .source(Base64PdfSource.builder()
                                                                .data(pdfBase64)
                                                                .build())
                                                        .build()
                                        ),
                                        ContentBlockParam.ofText(
                                                TextBlockParam.builder()
                                                        .text("Which model has the highest human preference win rates across each use-case?")
                                                        .build()
                                        )
                                ))
                                .build())
                        .build())
                .addRequest(BatchCreateParams.Request.builder()
                        .customId("my-second-request")
                        .params(BatchCreateParams.Request.Params.builder()
                                .model(Model.CLAUDE_OPUS_4_20250514)
                                .maxTokens(1024)
                                .addUserMessageOfBlockParams(List.of(
                                        ContentBlockParam.ofDocument(
                                        DocumentBlockParam.builder()
                                                .source(Base64PdfSource.builder()
                                                        .data(pdfBase64)
                                                        .build())
                                                .build()
                                        ),
                                        ContentBlockParam.ofText(
                                                TextBlockParam.builder()
                                                        .text("Extract 5 key insights from this document.")
                                                        .build()
                                        )
                                ))
                                .build())
                        .build())
                .build();

        MessageBatch batch = client.messages().batches().create(params);
        System.out.println(batch);
    }
}
```
</CodeGroup>

## Next steps

<CardGroup cols={2}>
  <Card
    title="Try PDF examples"
    icon="file"
    href="https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal"
  >
    Explore practical examples of PDF processing in our cookbook recipe.
  </Card>

  <Card
    title="View API reference"
    icon="code"
    href="/docs/en/api/messages"
  >
    See complete API documentation for PDF support.
  </Card>
</CardGroup>