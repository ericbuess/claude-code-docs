# Retrieve and delete chats, files, and projects

Access chat content, file attachments, and projects for claude.ai organizations through the Compliance API.

---

<Note>
  The endpoints on this page retrieve and delete claude.ai content and are available only to Claude Enterprise organizations, which have self-service access to the Compliance API. See [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

<Check>
  **Required scope:** `read:compliance_user_data` on the Compliance Access Key. The delete endpoints also require `delete:compliance_user_data`.

  **Prerequisite:** None for listing chats organization-wide. To filter the chat list to specific users, you need user IDs from [List organization users](/docs/en/manage-claude/compliance-org-data#list-organization-users). The other endpoints on this page take resource IDs directly.
</Check>

The endpoints on this page expose claude.ai chat content, file uploads, projects, and project attachments to compliance reviewers. They support eDiscovery (electronic discovery) exports, data loss prevention (DLP) enforcement, and account-deletion responses. Content is retained for as long as your organization's retention policy allows. Chats that a user has soft-deleted in claude.ai remain visible through the Compliance API with `deleted_at` populated; chats that have been hard-deleted (through the Compliance API itself, or after the organization's retention window expires) are not retrievable.

Both scopes are granted only on Compliance Access Keys (`sk-ant-api01-...`) created in claude.ai; see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access) to provision one. The `read:compliance_user_data` scope covers retrieval; `delete:compliance_user_data` is required only for the delete endpoints. The chat, file, project, and attachment endpoints are not available to Admin API keys (`sk-ant-admin01-...`); calls authenticated with an Admin API key return [403 Forbidden](/docs/en/manage-claude/compliance-errors#403-forbidden).

Endpoints on this page paginate two ways; see [Paginate results](/docs/en/manage-claude/compliance-activity-feed#paginate-results) for the full reference. Each section notes which scheme applies.

## Retrieve chats and messages

Use [List chats](/docs/en/api/compliance/apps/chats/list) to page through chat metadata, then [Get chat messages](/docs/en/api/compliance/apps/chats/messages/list) to fetch the full message content of one chat.

The chat list endpoint defaults to organization-wide scope: leave off `user_ids[]` to include every chat under your parent organization. Add `order_by=updated_at` to sort by last update time. This combination is the recommended way to export chats and keep an export current, because one paginated loop picks up both new and modified chats for every user without enumerating users first. The following request lists chats updated since a given date.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/apps/chats" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "order_by=updated_at" \
    --data-urlencode "updated_at.gte=2025-06-01T00:00:00Z" \
    --data-urlencode "limit=100"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
      "name": "Product Requirements Discussion",
      "created_at": "2026-04-10T08:09:10Z",
      "updated_at": "2026-04-10T09:10:11Z",
      "deleted_at": null,
      "href": "https://claude.ai/chat/abcdef01-2345-6789-abcd-ef0123456789",
      "model": "claude-opus-4-8",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq",
      "user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      }
    }
  ],
  "has_more": true,
  "first_id": "eyJrIjogInVwZGF0ZWRfYXQiLCAidCI6ICIyMDI2LTA0LTEwVDA5OjEwOjExKzAwOjAwIiwgImlkIjogImFiY2RlZjAxLS4uLiJ9",
  "last_id": "eyJrIjogInVwZGF0ZWRfYXQiLCAidCI6ICIyMDI2LTA0LTEwVDA5OjEwOjExKzAwOjAwIiwgImlkIjogImFiY2RlZjAxLS4uLiJ9"
}
```

Results sort ascending by the `order_by` field, oldest first, with ties broken by `id`. Pagination uses the standard `first_id`/`last_id`/`has_more` cursor fields described in [Paginate results](/docs/en/manage-claude/compliance-activity-feed#paginate-results). To walk forward toward newer chats, pass the response's `last_id` back as `after_id` on the next request.

That forward walk is also how you keep an export current across runs: persist the final page's `last_id` and resume from it as `after_id` on the next run. Because the list is ordered by `updated_at`, a chat that changes after your saved cursor reappears ahead of it, so each incremental run returns both brand-new chats and older chats that have since been modified. Process results idempotently, keyed by chat `id`, to handle those reappearances.

A few constraints apply to these organization-wide queries. Cursors are opaque and bound to the sort key, so an `after_id` issued under one `order_by` value is rejected with a 400 error under the other. Time-filter bounds must match the sort key too: pair `updated_at.*` bounds with `order_by=updated_at`, and `created_at.*` bounds with the default `order_by=created_at`. Backward pagination with `before_id` is not supported, and the `project_ids[]` filter is not available. See [List chats](/docs/en/api/compliance/apps/chats/list) for the full filter reference.

To scope the list to specific users instead (for example, a legal hold on named custodians), pass 1–10 `user_ids[]` values. Obtain the IDs from [List organization users](/docs/en/manage-claude/compliance-org-data#list-organization-users). User-filtered queries always sort by `created_at` (passing `order_by=updated_at` returns a 400 error) and support both `after_id` and `before_id`. Filtering by `project_ids[]` is only available in this user-filtered form.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/apps/chats" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
    --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
    --data-urlencode "limit=100"
  ```
</CodeGroup>

The list response carries chat metadata only. To pull the actual chat content, attached files, and inline artifacts (structured documents Claude generates inside a chat), follow up with the messages endpoint for each chat ID:

<CodeGroup>
  ```bash cURL
  chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

The messages endpoint returns the chat's metadata plus a `chat_messages` array sorted by `created_at`. When `limit` is omitted, the full message set is returned in one response; pass `limit`, `after_id`, or `before_id` to page through very long chats. The endpoint also accepts `created_at.*` and `updated_at.*` range bounds (`gt`, `gte`, `lt`, `lte`) and an `order` parameter (`asc` or `desc`). See [Get chat messages](/docs/en/api/compliance/apps/chats/messages/list) for the full parameter list. For user messages, `created_at` is when the message was sent; for assistant messages, it is when Claude finished generating the message. Each message carries its text content and, when present, any uploaded files (typically on user messages), any tool-generated files, and any artifacts the assistant produced or updated (typically on assistant messages):

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "name": "Product Requirements Discussion",
  "created_at": "2026-04-10T08:09:10Z",
  "updated_at": "2026-04-10T09:10:11Z",
  "deleted_at": null,
  "href": "https://claude.ai/chat/abcdef01-2345-6789-abcd-ef0123456789",
  "model": "claude-opus-4-8",
  "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq",
  "user": {
    "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
    "email_address": "user@example.com"
  },
  "chat_messages": [
    {
      "id": "claude_chat_msg_01VnBPkLmtj7YdW5QrXKEA8c",
      "role": "user",
      "created_at": "2026-04-10T08:09:10Z",
      "content": [
        {
          "type": "text",
          "text": "Can you help me draft requirements for our new dashboard feature?"
        }
      ],
      "files": [
        {
          "id": "claude_file_01UaT9wBcDfGhJkLmNpQrSv7",
          "filename": "dashboard_mockup_v1.pdf",
          "mime_type": "application/pdf"
        }
      ]
    },
    {
      "id": "claude_chat_msg_01M8tFcHwbQ2kY6NpEjRZv4D",
      "role": "assistant",
      "created_at": "2026-04-10T08:09:11Z",
      "content": [
        {
          "type": "text",
          "text": "I'd be happy to help you draft requirements for your dashboard feature..."
        }
      ],
      "generated_files": [
        {
          "id": "claude_gen_file_01TbR8wAcCeFhJkLnPqStUvX",
          "filename": "requirements_summary.csv",
          "mime_type": "text/csv"
        }
      ],
      "artifacts": [
        {
          "id": "claude_artifact_01HqRsTuVwXyZa2BcDeFgH4J",
          "version_id": "claude_artifact_version_01KmNpQrSt3UvWxYz5AbCdEfG",
          "title": "Dashboard Requirements Draft",
          "artifact_type": "text/markdown"
        }
      ]
    }
  ],
  "has_more": false,
  "first_id": "eyJtc2dfdXVpZCI6ICIwZjcwYjA2Ni0uLi4ifQ==",
  "last_id": "eyJtc2dfdXVpZCI6ICJhNGUwYjE3Mi0uLi4ifQ=="
}
```

`files`, `generated_files`, and `artifacts` can each be `null` on a given message. `files` are binary uploads (PDFs, images, spreadsheets) the user attached to the message. `generated_files` are binary files the assistant created during the conversation through tool use (for example, PDFs, spreadsheets, or slide decks). `artifacts` are versioned documents (for example, code or markdown) the assistant generated or updated in its response; an artifact can be revised across multiple assistant turns in the same chat, and each revision appears as a new `version_id` under the same artifact `id`. Pass each entry's `id` (or `version_id` for artifacts) to the matching content endpoint in [Retrieve files and artifacts](#retrieve-files-and-artifacts) to download it.

## Retrieve files and artifacts

Files and artifacts are downloaded by ID, not listed independently. The IDs come from the chat messages endpoint in [Retrieve chats and messages](#retrieve-chats-and-messages) (the `files`, `generated_files`, and `artifacts` arrays on each message) or, for project-level uploads, from the [project attachments endpoint](#retrieve-projects-and-attachments).

Pick the endpoint that matches your ID type and the data you need. The same file content endpoint serves both chat files and project files.

| You have                       | You want                                | Use this endpoint                                                                               |
| ------------------------------ | --------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `claude_file_*` ID             | The file's binary content               | [Download file content](/docs/en/api/compliance/apps/chats/files/download)                      |
| `claude_file_*` ID             | The file's metadata only                | [Get file metadata](/docs/en/api/compliance/apps/chats/files/retrieve)                          |
| `claude_gen_file_*` ID         | A tool-generated file's binary content  | [Download a Claude-generated file](/docs/en/api/compliance/apps/chats/generated_files/download) |
| `claude_gen_file_*` ID         | A tool-generated file's metadata only   | [Get generated-file metadata](/docs/en/api/compliance/apps/chats/generated_files/retrieve)      |
| `claude_artifact_version_*` ID | One artifact version's text             | [Download artifact content](/docs/en/api/compliance/apps/artifacts/download)                    |
| `claude_artifact_version_*` ID | The artifact version's metadata only    | [Get artifact metadata](/docs/en/api/compliance/apps/artifacts/retrieve)                        |
| `claude_proj_doc_*` ID         | A project document's plain-text content | [Get project document content](/docs/en/api/compliance/apps/projects/documents/retrieve)        |
| `claude_proj_doc_*` ID         | A project document's metadata only      | [Get project document metadata](/docs/en/api/compliance/apps/projects/documents/metadata)       |

The file content endpoint streams the original upload as a chunked binary response with these headers:

* `Content-Disposition: attachment; filename*=utf-8''<percent-encoded filename>` carries the original upload file name in RFC 5987 extended form. The extended form is used for every file name, not only non-ASCII ones.
* `Content-Type` carries the upload's MIME type.
* `Content-MD5` carries the file's MD5 digest, base64-encoded as specified in RFC 1864.
* `Transfer-Encoding: chunked` is always set.

<CodeGroup>
  ```bash cURL
  file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

  curl --fail-with-body -sS -OJ \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content"
  ```
</CodeGroup>

The `-OJ` flags tell curl to save the response under the file name from `Content-Disposition`, which is the original file name the user uploaded.

The artifact content endpoint returns the text body of one artifact version. Pass the `version_id` from one of the entries in an assistant message's `artifacts` array, not the artifact's stable `id`. Each new version of an artifact has its own `version_id`, and the Compliance API serves the exact bytes of that version.

## Retrieve projects and attachments

Projects bundle related chats together with custom instructions, knowledge base content, and attached files or text documents. The Compliance API exposes project metadata, project details, and the list of attachments belonging to a project.

* [List projects](/docs/en/api/compliance/apps/projects/list)
* [Get project details](/docs/en/api/compliance/apps/projects/retrieve)
* [List project attachments](/docs/en/api/compliance/apps/projects/attachments/list)
* [Get project document content](/docs/en/api/compliance/apps/projects/documents/retrieve)

Project results are sorted by creation date ascending. Attachment results are sorted by `created_at` ascending, with ties broken by `id`. Project list and attachment list responses paginate with an opaque `next_page` page token instead of the `first_id`/`last_id` cursors used by chats and the Activity Feed. Pass the token back as the `page` query parameter on the next request.

### Project files versus project documents

A project attachment is one of two distinct shapes, identified by the `type` discriminator on each entry:

Entries with `type` of `project_file` are binary uploads (PDFs, images, spreadsheets) whose IDs start with `claude_file_`; download them with [Download file content](/docs/en/api/compliance/apps/chats/files/download). Entries with `type` of `project_doc` are plain-text documents (always `text/plain`) whose IDs start with `claude_proj_doc_`; fetch them with [Get project document content](/docs/en/api/compliance/apps/projects/documents/retrieve).

A consumer that walks the attachment list must branch on `type` and call the matching content endpoint for each entry. The following request lists one page of attachments; paginate by passing `next_page` back as the `page` parameter until `has_more` is `false`.

<CodeGroup>
  ```bash cURL
  project_id="claude_proj_01KGp4eZNug9ri4kE35RSppq"

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/apps/projects/$project_id/attachments" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "claude_file_01UaT9wBcDfGhJkLmNpQrSv7",
      "created_at": "2026-04-10T08:09:10Z",
      "filename": "dashboard_mockup_v1.pdf",
      "mime_type": "application/pdf",
      "type": "project_file"
    },
    {
      "id": "claude_proj_doc_01YnT8sBcWvUtXzQpMkRfDgH",
      "created_at": "2026-04-10T08:09:11Z",
      "filename": "requirements.md",
      "mime_type": "text/plain",
      "type": "project_doc"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

## Delete content

<Warning>
  Every successful delete is permanent and immediate. There is no recovery window.
</Warning>

The Compliance API exposes hard-delete endpoints for chats, files, project documents, and entire projects. A hard-deleted chat cannot be restored, and it stops appearing in list responses afterward (whereas a chat soft-deleted from claude.ai still appears with `deleted_at` populated).

* [Delete chat](/docs/en/api/compliance/apps/chats/delete): also removes the chat's messages and any files attached to those messages.
* [Delete file](/docs/en/api/compliance/apps/chats/files/delete): handles both chat files and project files.
* [Delete project document](/docs/en/api/compliance/apps/projects/documents/delete): removes a single project document by ID.
* [Delete project](/docs/en/api/compliance/apps/projects/delete): see [Detach chats before deleting a project](#detach-chats-before-deleting-a-project).

All four endpoints require the `delete:compliance_user_data` scope, which is granted separately from the read scope when the Compliance Access Key is created.

The following request deletes one chat. The same pattern applies to the other delete endpoints; only the URL changes.

<CodeGroup>
  ```bash cURL
  # WARNING: This operation PERMANENTLY deletes the chat, all of its messages,
  # and any attached files. Deletion is immediate and cannot be undone. It
  # requires the `delete:compliance_user_data` scope, which is granted separately
  # from `read:compliance_user_data` when the Compliance Access Key is created.
  # Ensure you have explicit authorization before running this.

  chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

  curl --fail-with-body -sS -X DELETE \
    "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "type": "claude_chat_deleted"
}
```

Each successful delete returns a small confirmation envelope with an `id` and a `type` discriminator. The chat endpoint returns `claude_chat_deleted`; check the `type` field before treating the delete as confirmed. See the response schema on each delete endpoint's [API reference](/docs/en/api/compliance/apps) page for the exact `type` value the other endpoints return.

### Detach chats before deleting a project

A project cannot be deleted while any chats remain attached to it. The API returns 409 with this body:

```json
{
  "error": {
    "type": "conflict_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

To resolve, list the project's chats with `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (the `project_ids[]` filter requires at least one `user_ids[]` value; enumerate IDs through [List organization users](/docs/en/manage-claude/compliance-org-data#list-organization-users)), delete each one with `DELETE /v1/compliance/apps/chats/{claude_chat_id}` (or move it out of the project from claude.ai), and then retry the project delete.

## Next steps

<CardGroup cols={2}>
  <Card title="API reference" href="/docs/en/api/compliance/apps">
    The full request and response schema for every chat, file, project, and artifact endpoint.
  </Card>

  <Card title="List organizations, users, roles, groups, and settings" href="/docs/en/manage-claude/compliance-org-data">
    Enumerate the people and teams associated with the chats and projects on this page.
  </Card>
</CardGroup>
