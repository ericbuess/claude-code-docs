# Vision

> The Claude 3 and 4 families of models comes with new vision capabilities that allow Claude to understand and analyze images, opening up exciting possibilities for multimodal interaction.

This guide describes how to work with images in Claude, including best practices, code examples, and limitations to keep in mind.

***

## How to use vision

Use Claude’s vision capabilities via:

* [claude.ai](https://claude.ai/). Upload an image like you would a file, or drag and drop an image directly into the chat window.
* The [Console Workbench](https://console.anthropic.com/workbench/). If you select a model that accepts images (Claude 3 and 4 models only), a button to add images appears at the top right of every User message block.
* **API request**. See the examples in this guide.

***

## Before you upload

### Basics and Limits

You can include multiple images in a single request (up to 20 for [claude.ai](https://claude.ai/) and 100 for API requests). Claude will analyze all provided images when formulating its response. This can be helpful for comparing or contrasting images.

If you submit an image larger than 8000x8000 px, it will be rejected. If you submit more than 20 images in one API request, this limit is 2000x2000 px.

<Note>
  While the API supports 100 images per request, there is a [32MB request size limit](/en/api/overview#request-size-limits) for standard endpoints.
</Note>

### Evaluate image size

For optimal performance, we recommend resizing images before uploading if they are too large. If your image’s long edge is more than 1568 pixels, or your image is more than \~1,600 tokens, it will first be scaled down, preserving aspect ratio, until it’s within the size limits.

If your input image is too large and needs to be resized, it will increase latency of [time-to-first-token](/en/docs/about-claude/glossary), without giving you any additional model performance. Very small images under 200 pixels on any given edge may degrade performance.

<Tip>
  To improve [time-to-first-token](/en/docs/about-claude/glossary), we recommend
  resizing images to no more than 1.15 megapixels (and within 1568 pixels in
  both dimensions).
</Tip>

Here is a table of maximum image sizes accepted by our API that will not be resized for common aspect ratios. With the Claude Sonnet 3.7 model, these images use approximately 1,600 tokens and around \$4.80/1K images.

| Aspect ratio | Image size   |
| ------------ | ------------ |
| 1:1          | 1092x1092 px |
| 3:4          | 951x1268 px  |
| 2:3          | 896x1344 px  |
| 9:16         | 819x1456 px  |
| 1:2          | 784x1568 px  |

### Calculate image costs

Each image you include in a request to Claude counts towards your token usage. To calculate the approximate cost, multiply the approximate number of image tokens by the [per-token price of the model](https://claude.com/pricing) you’re using.

If your image does not need to be resized, you can estimate the number of tokens used through this algorithm: `tokens = (width px * height px)/750`

Here are examples of approximate tokenization and costs for different image sizes within our API’s size constraints based on Claude Sonnet 3.7 per-token price of \$3 per million input tokens:

| Image size                    | # of Tokens | Cost / image | Cost / 1K images |
| ----------------------------- | ----------- | ------------ | ---------------- |
| 200x200 px(0.04 megapixels)   | \~54        | \~\$0.00016  | \~\$0.16         |
| 1000x1000 px(1 megapixel)     | \~1334      | \~\$0.004    | \~\$4.00         |
| 1092x1092 px(1.19 megapixels) | \~1590      | \~\$0.0048   | \~\$4.80         |

### Ensuring image quality

When providing images to Claude, keep the following in mind for best results:

* **Image format**: Use a supported image format: JPEG, PNG, GIF, or WebP.
* **Image clarity**: Ensure images are clear and not too blurry or pixelated.
* **Text**: If the image contains important text, make sure it’s legible and not too small. Avoid cropping out key visual context just to enlarge the text.

***

## Prompt examples

Many of the [prompting techniques](/en/docs/build-with-claude/prompt-engineering/overview) that work well for text-based interactions with Claude can also be applied to image-based prompts.

These examples demonstrate best practice prompt structures involving images.

<Tip>
  Just as with document-query placement, Claude works best when images come
  before text. Images placed after text or interpolated with text will still
  perform well, but if your use case allows it, we recommend an image-then-text
  structure.
</Tip>

### About the prompt examples

The following examples demonstrate how to use Claude's vision capabilities using various programming languages and approaches. You can provide images to Claude in three ways:

1. As a base64-encoded image in `image` content blocks
2. As a URL reference to an image hosted online
3. Using the Files API (upload once, use multiple times)

The base64 example prompts use these variables:

<CodeGroup>
  ```bash Shell theme={null}
      # For URL-based images, you can use the URL directly in your JSON request
      
      # For base64-encoded images, you need to first encode the image
      # Example of how to encode an image to base64 in bash:
      BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64)
      
      # The encoded data can now be used in your API calls
  ```

  ```Python Python theme={null}
  import base64
  import httpx

  # For base64-encoded images
  image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  image1_media_type = "image/jpeg"
  image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

  image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
  image2_media_type = "image/jpeg"
  image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")

  # For URL-based images, you can use the URLs directly in your requests
  ```

  ```TypeScript TypeScript theme={null}
  import axios from 'axios';

  // For base64-encoded images
  async function getBase64Image(url: string): Promise<string> {
    const response = await axios.get(url, { responseType: 'arraybuffer' });
    return Buffer.from(response.data, 'binary').toString('base64');
  }

  // Usage
  async function prepareImages() {
    const imageData = await getBase64Image('https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg');
    // Now you can use imageData in your API calls
  }

  // For URL-based images, you can use the URLs directly in your requests
  ```

  ```java Java theme={null}
  import java.io.IOException;
  import java.util.Base64;
  import java.io.InputStream;
  import java.net.URL;

  public class ImageHandlingExample {

      public static void main(String[] args) throws IOException, InterruptedException {
          // For base64-encoded images
          String image1Url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
          String image1MediaType = "image/jpeg";
          String image1Data = downloadAndEncodeImage(image1Url);

          String image2Url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg";
          String image2MediaType = "image/jpeg";
          String image2Data = downloadAndEncodeImage(image2Url);

          // For URL-based images, you can use the URLs directly in your requests
      }

      private static String downloadAndEncodeImage(String imageUrl) throws IOException {
          try (InputStream inputStream = new URL(imageUrl).openStream()) {
              return Base64.getEncoder().encodeToString(inputStream.readAllBytes());
          }
      }

  }
  ```
</CodeGroup>

Below are examples of how to include images in a Messages API request using base64-encoded images and URL references:

### Base64-encoded image example

<CodeGroup>
  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": "'"$BASE64_IMAGE_DATA"'"
              }
            },
            {
              "type": "text",
              "text": "Describe this image."
            }
          ]
        }
      ]
    }'
  ```

  ```Python Python theme={null}
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
                      "type": "image",
                      "source": {
                          "type": "base64",
                          "media_type": image1_media_type,
                          "data": image1_data,
                      },
                  },
                  {
                      "type": "text",
                      "text": "Describe this image."
                  }
              ],
          }
      ],
  )
  print(message)
  ```

  ```TypeScript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  async function main() {
    const message = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: "image/jpeg",
                data: imageData, // Base64-encoded image data as string
              }
            },
            {
              type: "text",
              text: "Describe this image."
            }
          ]
        }
      ]
    });
    
    console.log(message);
  }

  main();
  ```

  ```Java Java theme={null}
  import java.io.IOException;
  import java.util.List;

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.*;

  public class VisionExample {
      public static void main(String[] args) throws IOException, InterruptedException {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();
          String imageData = ""; // // Base64-encoded image data as string

          List<ContentBlockParam> contentBlockParams = List.of(
                  ContentBlockParam.ofImage(
                          ImageBlockParam.builder()
                                  .source(Base64ImageSource.builder()
                                          .data(imageData)
                                          .build())
                                  .build()
                  ),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                          .text("Describe this image.")
                          .build())
          );
          Message message = client.messages().create(
                  MessageCreateParams.builder()
                          .model(Model.CLAUDE_3_7_SONNET_LATEST)
                          .maxTokens(1024)
                          .addUserMessageOfBlockParams(contentBlockParams)
                          .build()
          );

          System.out.println(message);
      }
  }
  ```
</CodeGroup>

### URL-based image example

<CodeGroup>
  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "url",
                "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
              }
            },
            {
              "type": "text",
              "text": "Describe this image."
            }
          ]
        }
      ]
    }'
  ```

  ```Python Python theme={null}
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
                      "type": "image",
                      "source": {
                          "type": "url",
                          "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                      },
                  },
                  {
                      "type": "text",
                      "text": "Describe this image."
                  }
              ],
          }
      ],
  )
  print(message)
  ```

  ```TypeScript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  async function main() {
    const message = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "url",
                url: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
              }
            },
            {
              type: "text",
              text: "Describe this image."
            }
          ]
        }
      ]
    });
    
    console.log(message);
  }

  main();
  ```

  ```Java Java theme={null}
  import java.io.IOException;
  import java.util.List;

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.*;

  public class VisionExample {

      public static void main(String[] args) throws IOException, InterruptedException {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          List<ContentBlockParam> contentBlockParams = List.of(
                  ContentBlockParam.ofImage(
                          ImageBlockParam.builder()
                                  .source(UrlImageSource.builder()
                                          .url("https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg")
                                          .build())
                                  .build()
                  ),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                          .text("Describe this image.")
                          .build())
          );
          Message message = client.messages().create(
                  MessageCreateParams.builder()
                          .model(Model.CLAUDE_3_7_SONNET_LATEST)
                          .maxTokens(1024)
                          .addUserMessageOfBlockParams(contentBlockParams)
                          .build()
          );
          System.out.println(message);
      }
  }
  ```
</CodeGroup>

### Files API image example

For images you'll use repeatedly or when you want to avoid encoding overhead, use the [Files API](/en/docs/build-with-claude/files):

<CodeGroup>
  ```bash Shell theme={null}
  # First, upload your image to the Files API
  curl -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@image.jpg"

  # Then use the returned file_id in your message
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "file",
                "file_id": "file_abc123"
              }
            },
            {
              "type": "text",
              "text": "Describe this image."
            }
          ]
        }
      ]
    }'
  ```

  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  # Upload the image file
  with open("image.jpg", "rb") as f:
      file_upload = client.beta.files.upload(file=("image.jpg", f, "image/jpeg"))

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
                      "type": "image",
                      "source": {
                          "type": "file",
                          "file_id": file_upload.id
                      }
                  },
                  {
                      "type": "text",
                      "text": "Describe this image."
                  }
              ]
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript theme={null}
  import { Anthropic, toFile } from '@anthropic-ai/sdk';
  import fs from 'fs';

  const anthropic = new Anthropic();

  async function main() {
    // Upload the image file
    const fileUpload = await anthropic.beta.files.upload({
      file: toFile(fs.createReadStream('image.jpg'), undefined, { type: "image/jpeg" })
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
              type: 'image',
              source: {
                type: 'file',
                file_id: fileUpload.id
              }
            },
            {
              type: 'text',
              text: 'Describe this image.'
            }
          ]
        }
      ]
    });

    console.log(response);
  }

  main();
  ```

  ```java Java theme={null}
  import java.io.IOException;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.util.List;

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.File;
  import com.anthropic.models.files.FileUploadParams;
  import com.anthropic.models.messages.*;

  public class ImageFilesExample {
      public static void main(String[] args) throws IOException {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          // Upload the image file
          File file = client.beta().files().upload(FileUploadParams.builder()
                  .file(Files.newInputStream(Path.of("image.jpg")))
                  .build());

          // Use the uploaded file in a message
          ImageBlockParam imageParam = ImageBlockParam.builder()
                  .fileSource(file.id())
                  .build();

          MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_3_7_SONNET_LATEST)
                  .maxTokens(1024)
                  .addUserMessageOfBlockParams(
                          List.of(
                                  ContentBlockParam.ofImage(imageParam),
                                  ContentBlockParam.ofText(
                                          TextBlockParam.builder()
                                                  .text("Describe this image.")
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

See [Messages API examples](/en/api/messages) for more example code and parameter details.

<AccordionGroup>
  <Accordion title="Example: One image">
    It’s best to place images earlier in the prompt than questions about them or instructions for tasks that use them.

    Ask Claude to describe one image.

    | Role | Content                       |
    | ---- | ----------------------------- |
    | User | \[Image] Describe this image. |

    Here is the corresponding API call using the Claude Sonnet 3.7 model.

    <Tabs>
      <Tab title="Using Base64">
        ```Python Python theme={null}
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image1_media_type,
                                "data": image1_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Describe this image."
                        }
                    ],
                }
            ],
        )
        ```
      </Tab>

      <Tab title="Using URL">
        ```Python Python theme={null}
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                            },
                        },
                        {
                            "type": "text",
                            "text": "Describe this image."
                        }
                    ],
                }
            ],
        )
        ```
      </Tab>
    </Tabs>
  </Accordion>

  <Accordion title="Example: Multiple images">
    In situations where there are multiple images, introduce each image with `Image 1:` and `Image 2:` and so on. You don’t need newlines between images or between images and the prompt.

    Ask Claude to describe the differences between multiple images.

    | Role | Content                                                                 |
    | ---- | ----------------------------------------------------------------------- |
    | User | Image 1: \[Image 1] Image 2: \[Image 2] How are these images different? |

    Here is the corresponding API call using the Claude Sonnet 3.7 model.

    <Tabs>
      <Tab title="Using Base64">
        ```Python Python theme={null}
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image 1:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image1_media_type,
                                "data": image1_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Image 2:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image2_media_type,
                                "data": image2_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "How are these images different?"
                        }
                    ],
                }
            ],
        )
        ```
      </Tab>

      <Tab title="Using URL">
        ```Python Python theme={null}
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image 1:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                            },
                        },
                        {
                            "type": "text",
                            "text": "Image 2:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg",
                            },
                        },
                        {
                            "type": "text",
                            "text": "How are these images different?"
                        }
                    ],
                }
            ],
        )
        ```
      </Tab>
    </Tabs>
  </Accordion>

  <Accordion title="Example: Multiple images with a system prompt">
    Ask Claude to describe the differences between multiple images, while giving it a system prompt for how to respond.

    | Content |                                                                         |
    | ------- | ----------------------------------------------------------------------- |
    | System  | Respond only in Spanish.                                                |
    | User    | Image 1: \[Image 1] Image 2: \[Image 2] How are these images different? |

    Here is the corresponding API call using the Claude Sonnet 3.7 model.

    <Tabs>
      <Tab title="Using Base64">
        ```Python Python theme={null}
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="Respond only in Spanish.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image 1:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image1_media_type,
                                "data": image1_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Image 2:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image2_media_type,
                                "data": image2_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "How are these images different?"
                        }
                    ],
                }
            ],
        )
        ```
      </Tab>

      <Tab title="Using URL">
        ```Python Python theme={null}
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="Respond only in Spanish.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image 1:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                            },
                        },
                        {
                            "type": "text",
                            "text": "Image 2:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg",
                            },
                        },
                        {
                            "type": "text",
                            "text": "How are these images different?"
                        }
                    ],
                }
            ],
        )
        ```
      </Tab>
    </Tabs>
  </Accordion>

  <Accordion title="Example: Four images across two conversation turns">
    Claude’s vision capabilities shine in multimodal conversations that mix images and text. You can have extended back-and-forth exchanges with Claude, adding new images or follow-up questions at any point. This enables powerful workflows for iterative image analysis, comparison, or combining visuals with other knowledge.

    Ask Claude to contrast two images, then ask a follow-up question comparing the first images to two new images.

    | Role      | Content                                                                            |
    | --------- | ---------------------------------------------------------------------------------- |
    | User      | Image 1: \[Image 1] Image 2: \[Image 2] How are these images different?            |
    | Assistant | \[Claude's response]                                                               |
    | User      | Image 1: \[Image 3] Image 2: \[Image 4] Are these images similar to the first two? |
    | Assistant | \[Claude's response]                                                               |

    When using the API, simply insert new images into the array of Messages in the `user` role as part of any standard [multiturn conversation](/en/api/messages) structure.
  </Accordion>
</AccordionGroup>

***

## Limitations

While Claude's image understanding capabilities are cutting-edge, there are some limitations to be aware of:

* **People identification**: Claude [cannot be used](https://www.anthropic.com/legal/aup) to identify (i.e., name) people in images and will refuse to do so.
* **Accuracy**: Claude may hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels.
* **Spatial reasoning**: Claude's spatial reasoning abilities are limited. It may struggle with tasks requiring precise localization or layouts, like reading an analog clock face or describing exact positions of chess pieces.
* **Counting**: Claude can give approximate counts of objects in an image but may not always be precisely accurate, especially with large numbers of small objects.
* **AI generated images**: Claude does not know if an image is AI-generated and may be incorrect if asked. Do not rely on it to detect fake or synthetic images.
* **Inappropriate content**: Claude will not process inappropriate or explicit images that violate our [Acceptable Use Policy](https://www.anthropic.com/legal/aup).
* **Healthcare applications**: While Claude can analyze general medical images, it is not designed to interpret complex diagnostic scans such as CTs or MRIs. Claude's outputs should not be considered a substitute for professional medical advice or diagnosis.

Always carefully review and verify Claude's image interpretations, especially for high-stakes use cases. Do not use Claude for tasks requiring perfect precision or sensitive image analysis without human oversight.

***

## FAQ

<AccordionGroup>
  <Accordion title="What image file types does Claude support?">
    Claude currently supports JPEG, PNG, GIF, and WebP image formats, specifically:

    * `image/jpeg`
    * `image/png`
    * `image/gif`
    * `image/webp`
  </Accordion>

  {" "}

  <Accordion title="Can Claude read image URLs?">
    Yes, Claude can now process images from URLs with our URL image source blocks in the API.
    Simply use the "url" source type instead of "base64" in your API requests.
    Example:

    ```json  theme={null}
    {
      "type": "image",
      "source": {
        "type": "url",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
      }
    }
    ```
  </Accordion>

  <Accordion title="Is there a limit to the image file size I can upload?">
    Yes, there are limits:

    * API: Maximum 5MB per image
    * claude.ai: Maximum 10MB per image

    Images larger than these limits will be rejected and return an error when using our API.
  </Accordion>

  <Accordion title="How many images can I include in one request?">
    The image limits are:

    * Messages API: Up to 100 images per request
    * claude.ai: Up to 20 images per turn

    Requests exceeding these limits will be rejected and return an error.
  </Accordion>

  {" "}

  <Accordion title="Does Claude read image metadata?">
    No, Claude does not parse or receive any metadata from images passed to it.
  </Accordion>

  {" "}

  <Accordion title="Can I delete images I've uploaded?">
    No. Image uploads are ephemeral and not stored beyond the duration of the API
    request. Uploaded images are automatically deleted after they have been
    processed.
  </Accordion>

  {" "}

  <Accordion title="Where can I find details on data privacy for image uploads?">
    Please refer to our privacy policy page for information on how we handle
    uploaded images and other data. We do not use uploaded images to train our
    models.
  </Accordion>

  <Accordion title="What if Claude's image interpretation seems wrong?">
    If Claude's image interpretation seems incorrect:

    1. Ensure the image is clear, high-quality, and correctly oriented.
    2. Try prompt engineering techniques to improve results.
    3. If the issue persists, flag the output in claude.ai (thumbs up/down) or contact our support team.

    Your feedback helps us improve!
  </Accordion>

  <Accordion title="Can Claude generate or edit images?">
    No, Claude is an image understanding model only. It can interpret and analyze images, but it cannot generate, produce, edit, manipulate, or create images.
  </Accordion>
</AccordionGroup>

***

## Dive deeper into vision

Ready to start building with images using Claude? Here are a few helpful resources:

* [Multimodal cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal): This cookbook has tips on [getting started with images](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/getting%5Fstarted%5Fwith%5Fvision.ipynb) and [best practice techniques](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/best%5Fpractices%5Ffor%5Fvision.ipynb) to ensure the highest quality performance with images. See how you can effectively prompt Claude with images to carry out tasks such as [interpreting and analyzing charts](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/reading%5Fcharts%5Fgraphs%5Fpowerpoints.ipynb) or [extracting content from forms](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/how%5Fto%5Ftranscribe%5Ftext.ipynb).
* [API reference](/en/api/messages): Visit our documentation for the Messages API, including example [API calls involving images](/en/docs/build-with-claude/working-with-messages#vision).

If you have any other questions, feel free to reach out to our [support team](https://support.claude.com/). You can also join our [developer community](https://www.anthropic.com/discord) to connect with other creators and get help from Anthropic experts.
