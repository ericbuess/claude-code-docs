# Versions

When making API requests, you must send an `anthropic-version` request header. For example, `anthropic-version: 2023-06-01`. If you are using our [client SDKs](/docs/en/api/client-sdks), this is handled for you automatically.

---

For any given API version, we will preserve:

* Existing input parameters
* Existing output parameters

However, we may do the following:

* Add additional optional inputs
* Add additional values to the output
* Change conditions for specific error types
* Add new variants to enum-like output values (for example, streaming event types)

Generally, if you are using the API as documented in this reference, we will not break your usage.

## Version history

We always recommend using the latest API version whenever possible. Previous versions are considered deprecated and may be unavailable for new users.

* `2023-06-01`  
   * New format for [streaming](/docs/en/build-with-claude/streaming) server-sent events (SSE):  
         * Completions are incremental. For example, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude." ` instead of `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.  
         * All events are [named events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents), rather than [data-only events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages).  
         * Removed unnecessary `data: [DONE]` event.  
   * Removed legacy `exception` and `truncated` values in responses.
* `2023-01-01`: Initial release.