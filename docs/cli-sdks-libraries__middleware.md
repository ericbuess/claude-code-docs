---
title: SDK middleware
url: https://platform.claude.com/docs/en/cli-sdks-libraries/middleware
description: Intercept and modify requests and responses in the Anthropic SDKs.
---

The Anthropic SDKs provide a middleware (or interceptor) hook that lets you run code before a request is sent and after the response is received. Use middleware for cross-cutting concerns such as logging, custom retries, request annotation, and refusal fallback handling.

```mermaid
sequenceDiagram
    autonumber
    participant App as Your code
    participant M1 as Middleware A
    participant M2 as Middleware B
    participant Core as SDK core
    participant API as Claude API
    App->>M1: request
    M1->>M2: next(request)
    M2->>Core: next(request)
    Core->>API: HTTP request
    API-->>Core: HTTP response
    Core-->>M2: response
    M2-->>M1: response
    M1-->>App: response
```

Each middleware can inspect or replace the request before calling `next()`, and the response after `next()` returns.

## Registering middleware

Each middleware is a function that receives the outgoing request and a `next` callable. Call `next` to forward the request to the rest of the chain (or directly to the SDK core if this is the last middleware), and return its response. Anything before the `next` call runs on the way out; anything after runs on the way back.

<CodeGroup exclude="shell">
  ```python Python
  def logging_middleware(request: APIRequest, call_next: CallNext) -> APIResponse[Any]:
      # Before the request
      print(f"-> {request.method} {request.url}")

      # Forward the request to the rest of the chain
      response = call_next(request)

      # After the request
      print(f"<- {response.status_code}")

      return response


  client = Anthropic(middleware=[logging_middleware])
  ```

  ```typescript TypeScript
  import type { Middleware } from "@anthropic-ai/sdk";

  const loggingMiddleware: Middleware = async (request, next, ctx) => {
    // Before the request
    ctx.logger.debug("->", request.method, request.url);

    // Forward the request to the rest of the chain
    const response = await next(request);

    // After the request
    ctx.logger.debug("<-", response.status, request.url);

    return response;
  };

  const client = new Anthropic({ middleware: [loggingMiddleware] });
  ```

  ```csharp C#
  AnthropicClient client = new()
  {
      Handlers =
      [
          Handler.Create(async (request, next, cancellationToken) =>
          {
              // Before the request
              Console.WriteLine($"Sending {request.Method} {request.RequestUri}");

              // Forward the request to the next handler
              var response = await next(request, cancellationToken);

              // After the request
              Console.WriteLine($"Received {(int)response.StatusCode}");

              return response;
          }),
      ],
  };
  ```

  ```go Go
  client := anthropic.NewClient(
  	option.WithMiddleware(func(req *http.Request, next option.MiddlewareNext) (*http.Response, error) {
  		// Before the request
  		start := time.Now()
  		slog.Info("sending request", "method", req.Method, "url", req.URL)

  		// Forward the request to the rest of the chain
  		res, err := next(req)
  		if err != nil {
  			return nil, err
  		}

  		// After the request
  		slog.Info("received response", "status", res.StatusCode, "duration", time.Since(start))

  		return res, nil
  	}),
  )
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.builder()
      .fromEnv()
      .addInterceptor(Interceptor.syncOnly((nextClient, request, requestOptions) -> {
          // Before the request
          IO.println(request.method() + " /" + String.join("/", request.pathSegments()));

          // Forward the request to the next handler
          HttpResponse response = nextClient.execute(request, requestOptions);

          // After the request
          IO.println(response.statusCode());

          return response;
      }))
      .build();
  ```

  ```php PHP
  $loggingMiddleware = function (RequestInterface $request, callable $next): ResponseInterface {
      // Before the request
      error_log("-> {$request->getMethod()} {$request->getUri()}");

      // Forward the request to the rest of the chain
      $response = $next($request);

      // After the request
      error_log("<- {$response->getStatusCode()}");

      return $response;
  };

  $client = new Client(requestOptions: ['middleware' => [$loggingMiddleware]]);
  ```

  ```ruby Ruby
  logging_middleware = lambda do |request, call_next|
    # Before the request
    puts "-> #{request.method.upcase} #{request.url}"

    # Forward the request to the rest of the chain
    response = call_next.call(request)

    # After the request
    puts "<- #{response.status}"

    response
  end

  client = Anthropic::Client.new(middleware: [logging_middleware])
  ```
</CodeGroup>

## Middleware ordering

When you register multiple middleware, they apply in the order given: the first middleware's "before" code runs first, and its "after" code runs last. Middleware registered on the client runs before middleware passed as a per-request option.

In the Go SDK, repeated `option.WithMiddleware` calls concatenate (client first, then method). In the other SDKs, pass an array; later entries wrap inner.

## Replacing the HTTP client

Each SDK also accepts a custom HTTP client (for proxy configuration, custom TLS, or connection pooling). Only one HTTP client is used per SDK client; setting it replaces the default. The custom HTTP client receives requests after all middleware has run.

## Built-in middleware

The SDKs ship a refusal-fallback middleware that automatically retries requests Claude Fable 5 declines on a fallback model. See [Detect and retry on a fallback model](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) for setup and per-language examples.
