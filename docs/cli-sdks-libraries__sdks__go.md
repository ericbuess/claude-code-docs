---
title: Go SDK
url: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go
description: Install and configure the Anthropic Go SDK with context-based cancellation and functional options
---

The Anthropic Go library provides convenient access to the Claude API from applications written in Go.

<Info>
  For API feature documentation with code examples, see the [API reference](https://platform.claude.com/docs/en/api/overview). This page covers Go-specific SDK features and configuration.
</Info>

## Installation

```go
import (
	"github.com/anthropics/anthropic-sdk-go" // imported as anthropic
)
```

Install with `go get`:

```bash
go get github.com/anthropics/anthropic-sdk-go
```

## Requirements

This library requires Go 1.24+.

## Usage

```go
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client := anthropic.NewClient(
		option.WithAPIKey("my-anthropic-api-key"), // defaults to os.LookupEnv("ANTHROPIC_API_KEY")
	)
	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is a quaternion?")),
		},
		Model: anthropic.ModelClaudeOpus5,
	})
	if err != nil {
		panic(err.Error())
	}
	for _, block := range message.Content {
		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
			fmt.Println(textBlock.Text)
		}
	}
}
```

For authentication options including Workload Identity Federation, see [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication).

<AccordionGroup>
  <Accordion title="Conversations">
    ```go
    messages := []anthropic.MessageParam{
    	anthropic.NewUserMessage(anthropic.NewTextBlock("What is my first name?")),
    }

    message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus5,
    	Messages:  messages,
    	MaxTokens: 1024,
    })
    if err != nil {
    	panic(err)
    }

    fmt.Printf("%+v\n", message.Content)

    messages = append(messages, message.ToParam())
    messages = append(messages, anthropic.NewUserMessage(
    	anthropic.NewTextBlock("My full name is John Doe"),
    ))

    message, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus5,
    	Messages:  messages,
    	MaxTokens: 1024,
    })
    if err != nil {
    	panic(err)
    }

    fmt.Printf("%+v\n", message.Content)
    ```
  </Accordion>

  <Accordion title="System prompts">
    ```go
    message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus5,
    	MaxTokens: 1024,
    	System: []anthropic.TextBlockParam{
    		{Text: "Be very serious at all times."},
    	},
    	Messages: messages,
    })
    if err != nil {
    	panic(err)
    }
    fmt.Printf("%+v\n", message.Content)
    ```
  </Accordion>

  <Accordion title="Streaming">
    ```go
    content := "What is a quaternion?"

    stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus5,
    	MaxTokens: 1024,
    	Messages: []anthropic.MessageParam{
    		anthropic.NewUserMessage(anthropic.NewTextBlock(content)),
    	},
    })

    message := anthropic.Message{}
    for stream.Next() {
    	event := stream.Current()
    	err := message.Accumulate(event)
    	if err != nil {
    		panic(err)
    	}

    	switch eventVariant := event.AsAny().(type) {
    	case anthropic.ContentBlockDeltaEvent:
    		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
    		case anthropic.TextDelta:
    			print(deltaVariant.Text)
    		}

    	}
    }

    if stream.Err() != nil {
    	panic(stream.Err())
    }
    ```
  </Accordion>

  <Accordion title="Tool calling">
    ```go
    messages := []anthropic.MessageParam{
    	anthropic.NewUserMessage(anthropic.NewTextBlock(content)),
    }

    toolParams := []anthropic.ToolParam{
    	{
    		Name:        "get_coordinates",
    		Description: anthropic.String("Accepts a place as an address, then returns the latitude and longitude coordinates."),
    		InputSchema: GetCoordinatesInputSchema,
    	},
    }
    tools := make([]anthropic.ToolUnionParam, len(toolParams))
    for i, toolParam := range toolParams {
    	tools[i] = anthropic.ToolUnionParam{OfTool: &toolParam}
    }

    for {
    	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus5,
    		MaxTokens: 1024,
    		Messages:  messages,
    		Tools:     tools,
    	})

    	if err != nil {
    		panic(err)
    	}

    	print(color("[assistant]: "))
    	for _, block := range message.Content {
    		switch block := block.AsAny().(type) {
    		case anthropic.TextBlock:
    			println(block.Text)
    			println()
    		case anthropic.ToolUseBlock:
    			inputJSON, _ := json.Marshal(block.Input)
    			println(block.Name + ": " + string(inputJSON))
    			println()
    		}
    	}

    	messages = append(messages, message.ToParam())
    	toolResults := []anthropic.ContentBlockParamUnion{}

    	for _, block := range message.Content {
    		switch variant := block.AsAny().(type) {
    		case anthropic.ToolUseBlock:
    			print(color("[user (" + block.Name + ")]: "))

    			var response interface{}
    			switch block.Name {
    			case "get_coordinates":
    				var input struct {
    					Location string `json:"location"`
    				}

    				err := json.Unmarshal([]byte(variant.JSON.Input.Raw()), &input)
    				if err != nil {
    					panic(err)
    				}

    				response = GetCoordinates(input.Location)
    			}

    			b, err := json.Marshal(response)
    			if err != nil {
    				panic(err)
    			}

    			println(string(b))

    			toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, string(b), false))
    		}

    	}
    	if len(toolResults) == 0 {
    		break
    	}
    	messages = append(messages, anthropic.NewUserMessage(toolResults...))
    }
    ```
  </Accordion>
</AccordionGroup>

## Request fields

The anthropic library uses the [`omitzero`](https://tip.golang.org/doc/go1.24#encodingjsonpkgencodingjson) semantics from the Go 1.24+ `encoding/json` release for request fields.

Required primitive fields (such as `int64` or `string`) feature the tag `` `json:"...,required"` ``. These fields are always serialized, even their zero values.

Optional primitive types are wrapped in a `param.Opt[T]`. These fields can be set with the provided constructors, such as `anthropic.String(string)` or `anthropic.Int(int64)`.

Any `param.Opt[T]`, map, slice, struct or string enum uses the tag `` `json:"...,omitzero"` ``. Its zero value is considered omitted.

The `param.IsOmitted(any)` function can confirm the presence of any `omitzero` field.

```go
p := anthropic.ExampleParams{
	ID:   "id_xxx",                // required property
	Name: anthropic.String("..."), // optional property

	Point: anthropic.Point{
		X: 0,                // required field will serialize as 0
		Y: anthropic.Int(1), // optional field will serialize as 1
		// ... omitted non-required fields will not be serialized
	},

	Origin: anthropic.Origin{}, // the zero value of [Origin] is considered omitted
}
```

To send `null` instead of a `param.Opt[T]`, use `param.Null[T]()`. To send `null` instead of a struct `T`, use `param.NullStruct[T]()`.

```go
p.Name = param.Null[string]()       // 'null' instead of string
p.Point = param.NullStruct[Point]() // 'null' instead of struct

param.IsNull(p.Name)  // true
param.IsNull(p.Point) // true
```

Request structs contain a `.SetExtraFields(map[string]any)` method which can send non-conforming fields in the request body. Extra fields overwrite any struct fields with a matching key.

<Warning>
  For security reasons, only use `SetExtraFields` with trusted data.
</Warning>

To send a custom value instead of a struct, use the generic function `param.Override` (for example, `param.Override[anthropic.FooParams](12)`).

```go
// In cases where the API specifies a given type,
// but you want to send something else, use [SetExtraFields]:
p.SetExtraFields(map[string]any{
	"x": 0.01, // send "x" as a float instead of int
})

// Send a number instead of an object
custom := param.Override[anthropic.FooParams](12)
```

### Request unions

Unions are represented as a struct with fields prefixed by "Of" for each of its variants, only one field can be non-zero. The non-zero field will be serialized.

Subproperties of the union can be accessed through methods on the union struct. These methods return a mutable pointer to the underlying data, if present.

```go
// Only one field can be non-zero, use param.IsOmitted() to check if a field is set
type AnimalUnionParam struct {
	OfCat *Cat `json:",omitzero,inline"`
	OfDog *Dog `json:",omitzero,inline"`
}

animal := AnimalUnionParam{
	OfCat: &Cat{
		Name: "Whiskers",
		Owner: PersonParam{
			Address: AddressParam{Street: "3333 Coyote Hill Rd", ZipCode: 0},
		},
	},
}

// Mutating a field
if address := animal.GetOwner().GetAddress(); address != nil {
	address.ZipCode = 94304
}
```

### Deserializing params

<Note>
  `param.SetJSON` requires SDK v1.20.0 or later.
</Note>

Param types (types ending in `Param`, such as `MessageNewParams` or `ToolUnionParam`) are designed for outgoing requests only. They marshal correctly to JSON but do not fully support round-trip deserialization. If you unmarshal raw JSON into a param struct, typed union fields like `OfBashTool20250124` will be nil even when the underlying JSON is valid.

If you need to reconstruct params from raw JSON (for example, from a database, middleware, or a previous request), call `UnmarshalJSON` to populate non-union fields, then use `param.SetJSON` to attach the raw bytes for correct re-serialization:

```go
// Serialize params (for example, for storage or forwarding)
b, err := json.Marshal(original)
if err != nil {
	panic(err)
}

// Later, reconstruct params from the stored JSON
var params anthropic.MessageNewParams
if err := params.UnmarshalJSON(b); err != nil {
	panic(err)
}
param.SetJSON(b, &params)

// params.Model and other scalar fields are populated by UnmarshalJSON.
// params.Tools[0].OfBashTool20250124 is nil (the union limitation),
// but the raw JSON is preserved. When params is marshaled again
// for the API call, the tools serialize correctly.
b2, _ := json.Marshal(params)
fmt.Println(string(b) == string(b2)) // true
```

For this use case, `param.SetJSON` (available since v1.20.0) is preferred over the more general `param.Override[T](any)` because it doesn't require spelling out the type parameter and makes the round-trip intent explicit.

## Response objects

All fields in response structs are ordinary value types (not pointers or wrappers). Response structs also include a special `JSON` field containing metadata about each property.

```go
type Animal struct {
	Name   string `json:"name,nullable"`
	Owners int    `json:"owners"`
	Age    int    `json:"age"`
	JSON   struct {
		Name        respjson.Field
		Owners      respjson.Field
		Age         respjson.Field
		ExtraFields map[string]respjson.Field
	} `json:"-"`
}
```

To handle optional data, use the `.Valid()` method on the JSON field. `.Valid()` returns true when the field is present, non-`null`, and was unmarshaled successfully.

If `.Valid()` is false, the corresponding field will be its zero value.

```go
raw := `{"owners": 1, "name": null}`

var res Animal
json.Unmarshal([]byte(raw), &res)

// Accessing regular fields

res.Owners // 1
res.Name   // ""
res.Age    // 0

// Optional field checks

res.JSON.Owners.Valid() // true
res.JSON.Name.Valid()   // false
res.JSON.Age.Valid()    // false

// Raw JSON values

res.JSON.Owners.Raw()                  // "1"
res.JSON.Name.Raw() == "null"          // true
res.JSON.Name.Raw() == respjson.Null   // true
res.JSON.Age.Raw() == ""               // true
res.JSON.Age.Raw() == respjson.Omitted // true
```

These `.JSON` structs also include an `ExtraFields` map containing any properties in the json response that were not specified in the struct. This can be useful for API features not yet present in the SDK.

```go
body := res.JSON.ExtraFields["my_unexpected_field"].Raw()
```

### Response unions

In responses, unions are represented by a flattened struct containing all possible fields from each of the object variants. To convert it to a variant use the `.AsFooVariant()` method or the `.AsAny()` method if present.

If a response value union contains primitive values, primitive fields will be alongside the properties but prefixed with `Of` and feature the tag `json:"...,inline"`.

```go
type AnimalUnion struct {
	// From variants [Dog], [Cat]
	Owner Person `json:"owner"`
	// From variant [Dog]
	DogBreed string `json:"dog_breed"`
	// From variant [Cat]
	CatBreed string `json:"cat_breed"`
	// ...

	JSON struct {
		Owner respjson.Field
		// ...
	} `json:"-"`
}

// If animal variant
if animal.Owner.Address.ZipCode == "" {
	panic("missing zip code")
}

// Switch on the variant
switch variant := animal.AsAny().(type) {
case Dog:
case Cat:
default:
	panic("unexpected type")
}
```

## Error handling

When the API returns a non-success status code, the SDK returns an error with type `*anthropic.Error`. This contains the `StatusCode`, `*http.Request`, and `*http.Response` values of the request, along with the JSON of the error body (much like other response objects in the SDK). The error also includes the `RequestID` from the response headers, which is useful for troubleshooting with Anthropic support.

To handle errors, use the `errors.As` pattern:

```go
_, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
	MaxTokens: 1024,
	Messages: []anthropic.MessageParam{{
		Content: []anthropic.ContentBlockParamUnion{{
			OfText: &anthropic.TextBlockParam{
				Text: "What is a quaternion?",
			},
		}},
		Role: anthropic.MessageParamRoleUser,
	}},
	Model: anthropic.ModelClaudeOpus5,
})
if err != nil {
	var apierr *anthropic.Error
	if errors.As(err, &apierr) {
		println("Request ID:", apierr.RequestID)
		println(string(apierr.DumpRequest(true)))  // Prints the serialized HTTP request
		println(string(apierr.DumpResponse(true))) // Prints the serialized HTTP response
	}
	panic(err.Error()) // POST "/v1/messages": 400 Bad Request (Request-ID: req_xxx) { ... }
}
```

When other errors occur, they are returned unwrapped; for example, if HTTP transport fails, you might receive `*url.Error` wrapping `*net.OpError`.

## Retries

Certain errors will be automatically retried 2 times by default, with a short exponential backoff. The SDK retries by default all connection errors, 408 Request Timeout, 409 Conflict, 429 Rate Limit, and >=500 Internal errors.

You can use the `WithMaxRetries` option to configure or disable this:

```go
// Configure the default for all requests:
client := anthropic.NewClient(
	option.WithMaxRetries(0), // default is 2
)

// Override per-request:
// ...
	client.Messages.New(
		context.TODO(),
		anthropic.MessageNewParams{
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{{
				Content: []anthropic.ContentBlockParamUnion{{
					OfText: &anthropic.TextBlockParam{
						Text: "What is a quaternion?",
					},
				}},
				Role: anthropic.MessageParamRoleUser,
			}},
			Model: anthropic.ModelClaudeOpus5,
		},
		option.WithMaxRetries(5),
	)
```

## Timeouts

Non-streaming Messages requests time out after 10 minutes by default; other requests have no default timeout. Use context to configure a timeout for a request lifecycle.

Note that if a request is [retried](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go#retries), the context timeout does not start over. To set a per-retry timeout, use `option.WithRequestTimeout()`.

```go
// This sets the timeout for the request, including all the retries.
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()
// ...
	client.Messages.New(
		ctx,
		anthropic.MessageNewParams{
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{{
				Content: []anthropic.ContentBlockParamUnion{{
					OfText: &anthropic.TextBlockParam{
						Text: "What is a quaternion?",
					},
				}},
				Role: anthropic.MessageParamRoleUser,
			}},
			Model: anthropic.ModelClaudeOpus5,
		},
		// This sets the per-retry timeout
		option.WithRequestTimeout(20*time.Second),
	)
```

## Long requests

<Warning>
  Consider using the streaming Messages API for longer running requests.
</Warning>

Avoid setting a large `MaxTokens` value without using streaming as some networks may drop idle connections after a certain period of time, which can cause the request to fail or [timeout](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go#timeouts) without receiving a response from Anthropic.

This SDK will also return an error if a non-streaming request is expected to be above roughly 10 minutes long. Calling `.Messages.NewStreaming()` or [setting a custom timeout](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go#timeouts) disables this error.

## File uploads

Request parameters that correspond to file uploads in multipart requests are typed as `io.Reader`. The contents of the `io.Reader` will by default be sent as a multipart form part with the file name of "anonymous\_file" and content-type of "application/octet-stream", so the recommended approach is to specify a custom content-type with the `anthropic.File(reader io.Reader, filename string, contentType string)` helper, which wraps any `io.Reader` with the appropriate file name and content type.

```go
// A file from the file system
file, err := os.Open("/path/to/file.json")
anthropic.FileUploadParams{
	File: anthropic.File(file, "custom-name.json", "application/json"),
}

// A file from a string
anthropic.FileUploadParams{
	File: anthropic.File(strings.NewReader("my file contents"), "custom-name.json", "application/json"),
}
```

The file name and content-type can also be customized by implementing `Name() string` or `ContentType() string` on the run-time type of `io.Reader`. Note that `os.File` implements `Name() string`, so a file returned by `os.Open` will be sent with the file name on disk.

## Pagination

This library provides some conveniences for working with paginated list endpoints.

You can use `.ListAutoPaging()` methods to iterate through items across all pages:

```go
iter := client.Messages.Batches.ListAutoPaging(context.TODO(), anthropic.MessageBatchListParams{
	Limit: anthropic.Int(20),
})
// Automatically fetches more pages as needed.
for iter.Next() {
	messageBatch := iter.Current()
	fmt.Println(messageBatch.ID)
}
if err := iter.Err(); err != nil {
	panic(err.Error())
}
```

Or you can use simple `.List()` methods to fetch a single page and receive a standard response object with additional helper methods like `.GetNextPage()`:

```go
page, err := client.Messages.Batches.List(context.TODO(), anthropic.MessageBatchListParams{
	Limit: anthropic.Int(20),
})
for page != nil {
	for _, batch := range page.Data {
		fmt.Println(batch.ID)
	}
	page, err = page.GetNextPage()
}
if err != nil {
	panic(err.Error())
}
```

## RequestOptions

This library uses the functional options pattern. Functions defined in the `option` package return a `RequestOption`, which is a closure that mutates a `RequestConfig`. These options can be supplied to the client or at individual requests. For example:

```go
client := anthropic.NewClient(
	// Adds a header to every request made by the client
	option.WithHeader("X-Some-Header", "custom_header_info"),
)

client.Messages.New(context.TODO(), // ...,
	// Override the header
	option.WithHeader("X-Some-Header", "some_other_custom_header_info"),
	// Add an undocumented field to the request body, using sjson syntax
	option.WithJSONSet("some.json.path", map[string]string{"my": "object"}),
)
```

The request option `option.WithDebugLog(nil)` may be helpful while debugging.

See the [full list of request options](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go/option).

## HTTP client customization

For request middleware (`option.WithMiddleware`) and replacing the default `http.Client` (`option.WithHTTPClient`), see [SDK middleware](https://platform.claude.com/docs/en/cli-sdks-libraries/middleware).

## Platform integrations

<Note>
  For detailed platform setup guides with code examples, see:

  * [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)
</Note>

The Go SDK supports the following platforms:

* **Agent Platform:** `import "github.com/anthropics/anthropic-sdk-go/vertex"`. Use `vertex.WithGoogleAuth(ctx, region, projectID)` or `vertex.WithCredentials(ctx, region, projectID, creds)`.
* **Bedrock:** `import "github.com/anthropics/anthropic-sdk-go/bedrock"`. Use `bedrock.NewMantleClient` for the Messages-API Bedrock endpoint (streams over SSE), or `bedrock.WithLoadDefaultConfig(ctx)` / `bedrock.WithConfig(cfg)` (`bedrock-runtime` path). Importing the `bedrock` package globally registers a decoder for `application/vnd.amazon.eventstream` with the SDK's streaming layer (through package `init()`). This applies whether you use the `bedrock-runtime` `WithConfig`/`WithLoadDefaultConfig` path or `NewMantleClient`.
* **Claude Platform on AWS:** `import anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"`. Use `anthropicaws.NewClient(ctx, cfg)` with an `anthropicaws.ClientConfig` value to construct a client; set `WorkspaceID` on the config or the `ANTHROPIC_AWS_WORKSPACE_ID` environment variable. The `anthropicaws` import alias avoids a name collision with `github.com/aws/aws-sdk-go-v2/aws` when both are imported. Available in beta.
* **Foundry:** Not currently supported in the Go SDK. See [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry) for supported SDKs.

Use `bedrock.NewMantleClient` for new projects; `bedrock.WithLoadDefaultConfig`/`WithConfig` remain for existing applications using the Bedrock `InvokeModel` API.

## Advanced usage

### Accessing raw response data (for example, response headers)

You can access the raw HTTP response data by using the `option.WithResponseInto()` request option. This is useful when you need to examine response headers, status codes, or other details.

```go
// Create a variable to store the HTTP response
var response *http.Response
message, err := client.Messages.New(
	context.TODO(),
	anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{{
			Content: []anthropic.ContentBlockParamUnion{{
				OfText: &anthropic.TextBlockParam{
					Text: "What is a quaternion?",
				},
			}},
			Role: anthropic.MessageParamRoleUser,
		}},
		Model: anthropic.ModelClaudeOpus5,
	},
	option.WithResponseInto(&response),
)
if err != nil {
	// handle error
}
fmt.Printf("%+v\n", message.Content)

fmt.Printf("Status Code: %d\n", response.StatusCode)
fmt.Printf("Headers: %+#v\n", response.Header)
```

### Making custom/undocumented requests

This library is typed for convenient access to the documented API. If you need to access undocumented endpoints, params, or response properties, the library can still be used.

#### Undocumented endpoints

To make requests to undocumented endpoints, you can use `client.Get`, `client.Post`, and other HTTP verbs. `RequestOptions` on the client, such as retries, will be respected when making these requests.

```go
var (
	// params can be an io.Reader, a []byte, an encoding/json serializable object,
	// or a "...Params" struct defined in this library.
	params map[string]any

	// result can be an []byte, *http.Response, a encoding/json deserializable object,
	// or a model defined in this library.
	result *http.Response
)
err := client.Post(context.Background(), "/unspecified", params, &result)
if err != nil {
	// ...
}
```

#### Undocumented request params

To make requests using undocumented parameters, you may use either the `option.WithQuerySet()` or the `option.WithJSONSet()` methods.

```go
params := FooNewParams{
	ID: "id_xxxx",
	Data: FooNewParamsData{
		FirstName: anthropic.String("John"),
	},
}
client.Foo.New(context.Background(), params, option.WithJSONSet("data.last_name", "Doe"))
```

#### Undocumented response properties

To access undocumented response properties, you may either access the raw JSON of the response as a string with `result.JSON.RawJSON()`, or get the raw JSON of a particular field on the result with `result.JSON.Foo.Raw()`.

Any fields that are not present on the response struct are saved and can be accessed through `result.JSON.ExtraFields`, which is a `map[string]respjson.Field`.

## Semantic versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backward-incompatible changes may be released as minor versions:

1. Changes to library internals that are technically public but not intended or documented for external use.
2. Changes that aren't expected to impact the vast majority of users in practice.

Backward-compatibility is taken seriously to ensure you can rely on a smooth upgrade experience.

Your feedback is welcome; open an [issue](https://github.com/anthropics/anthropic-sdk-go/issues) with questions, bugs, or suggestions.

## Additional resources

* [GitHub repository](https://github.com/anthropics/anthropic-sdk-go)
* [Go package documentation](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go)
* [API reference](https://platform.claude.com/docs/en/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
