# Build an orchestration mode

Build a session-level mode that grants standing consent for multi-agent fan-out, switched on and off with mid-conversation system messages.

---

An orchestration mode is a session-level switch: when it is on, the model puts maximum thoroughness behind every substantive request, scouting the task itself and then fanning work out to parallel subagents by default. When it is off, the same orchestration tool goes back to per-request opt-in.

The mode is not an API parameter. It is built entirely from documented pieces:

1. **An effort level:** requests run at a documented [Effort](/docs/en/build-with-claude/effort) value such as `xhigh`. There is no hidden level above the ones on that page.
2. **A mode reminder:** a [mid-conversation system message](/docs/en/build-with-claude/mid-conversation-system-messages) tells the model the mode is active, with a one-line refresher every several turns and an exit notice when the mode is turned off. The top-level `system` field never changes, so the cached prefix stays intact.
3. **Standing consent in the tool description:** the orchestration tool's description states that while the mode is on, the model should author and run a workflow for every substantive task without asking first.

<Note>
  This example uses mid-conversation system messages, which are currently available on Claude Opus 4.8 only. The fan-out itself multiplies token usage: a single request can spawn many subagent conversations, so reserve the mode for work that justifies the cost.
</Note>

## Set up the loop

The example is a single file. The constants control the effort level, the fan-out shape, and how often the mode refresher is re-sent. `MAX_CONCURRENT` caps how many subagents run at the same time (the PHP port is sequential and ignores it); `MAX_TOTAL_SUBTASKS` caps how many the model may queue in a single Workflow call. Splitting the two lets the model plan a large backlog without launching it all at once. The `DOC_TEST_MODE` check caps the loops to a single turn when that environment variable is set, so the automated docs harness can validate that the file compiles and finishes quickly without running the full orchestration; leave it unset when running the example yourself.

<CodeGroup>
  ```python Python
  import atexit
  import concurrent.futures
  import hashlib
  import json
  import os
  import shutil
  import subprocess
  import sys
  import tempfile
  import threading

  import anthropic

  client = anthropic.Anthropic()

  MODEL = "claude-opus-4-8"
  EFFORT = "xhigh"

  SYSTEM_PROMPT = "You are a helpful general-purpose agent. Answer the user's request directly."

  REQUEST_TIMEOUT_SECONDS = 600
  BASH_TIMEOUT_SECONDS = 60
  TOOL_RESULT_MAX_CHARS = 8000
  MAX_CONCURRENT = 10
  DOC_TEST_MODE = bool(os.environ.get("DOC_TEST_MODE"))
  MAX_TOTAL_SUBTASKS = 2 if DOC_TEST_MODE else 200
  MAX_SUBAGENT_TURNS = 1 if DOC_TEST_MODE else 15
  MAX_MAIN_TURNS = 1 if DOC_TEST_MODE else 30
  TURNS_BETWEEN_REFRESHERS = 10
  JOURNAL_PATH = os.environ.get("ORCH_JOURNAL") or "orchestration_journal.json"
  ```

  ```typescript TypeScript
  import { exec } from "node:child_process";
  import { createHash } from "node:crypto";
  import { rmSync } from "node:fs";
  import { mkdtemp, readFile, rename, writeFile } from "node:fs/promises";
  import { tmpdir } from "node:os";
  import { join } from "node:path";
  import { promisify } from "node:util";

  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const MODEL = "claude-opus-4-8";
  const EFFORT = "xhigh";

  const SYSTEM_PROMPT =
    "You are a helpful general-purpose agent. Answer the user's request directly.";

  const REQUEST_TIMEOUT_SECONDS = 600;
  const BASH_TIMEOUT_SECONDS = 60;
  const TOOL_RESULT_MAX_CHARS = 8000;
  const MAX_CONCURRENT = 10;
  const DOC_TEST_MODE = Boolean(process.env.DOC_TEST_MODE);
  const MAX_TOTAL_SUBTASKS = DOC_TEST_MODE ? 2 : 200;
  const MAX_SUBAGENT_TURNS = DOC_TEST_MODE ? 1 : 15;
  const MAX_MAIN_TURNS = DOC_TEST_MODE ? 1 : 30;
  const TURNS_BETWEEN_REFRESHERS = 10;
  const JOURNAL_PATH = process.env.ORCH_JOURNAL || "orchestration_journal.json";
  ```

  ```csharp C#
  using System.Diagnostics;
  using System.Security.Cryptography;
  using System.Text;
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  const string model = "claude-opus-4-8";
  var effort = Effort.Xhigh;

  const string systemPrompt = "You are a helpful general-purpose agent. Answer the user's request directly.";

  const int requestTimeoutSeconds = 600;
  // The other ports stream with max_tokens 64000. This port uses non-streaming
  // Messages.Create, and the API rejects non-streaming requests at that size.
  // 8192 is the non-streaming ceiling for Opus 4.0 and 4.1 and a conservative
  // choice for newer Opus models.
  const int requestMaxTokens = 8192;
  const int bashTimeoutSeconds = 60;
  const int toolResultMaxChars = 8000;
  const int maxConcurrent = 10;
  var docTestMode = Environment.GetEnvironmentVariable("DOC_TEST_MODE") is { Length: > 0 };
  int maxTotalSubtasks = docTestMode ? 2 : 200;
  int maxSubagentTurns = docTestMode ? 1 : 15;
  int maxMainTurns = docTestMode ? 1 : 30;
  const int turnsBetweenRefreshers = 10;
  var journalPath = Environment.GetEnvironmentVariable("ORCH_JOURNAL") is { Length: > 0 } p ? p : "orchestration_journal.json";
  ```

  ```go Go
  import (
  	"bytes"
  	"cmp"
  	"context"
  	"crypto/sha256"
  	"encoding/hex"
  	"encoding/json"
  	"errors"
  	"fmt"
  	"log"
  	"os"
  	"os/exec"
  	"path/filepath"
  	"strings"
  	"sync"
  	"time"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  var client = anthropic.NewClient()

  const (
  	modelID = "claude-opus-4-8"
  	effort  = anthropic.OutputConfigEffortXhigh

  	systemPrompt = "You are a helpful general-purpose agent. Answer the user's request directly."

  	requestTimeoutSeconds  = 600
  	bashTimeoutSeconds     = 60
  	toolResultMaxChars     = 8000
  	maxConcurrent          = 10
  	turnsBetweenRefreshers = 10
  )

  var (
  	docTestMode      = os.Getenv("DOC_TEST_MODE") != ""
  	maxTotalSubtasks = ifTest(2, 200)
  	maxSubagentTurns = ifTest(1, 15)
  	maxMainTurns     = ifTest(1, 30)
  	journalPath      = cmp.Or(os.Getenv("ORCH_JOURNAL"), "orchestration_journal.json")
  )

  func ifTest(test, normal int) int {
  	if docTestMode {
  		return test
  	}
  	return normal
  }

  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.core.RequestOptions;
  import com.anthropic.helpers.MessageAccumulator;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.OutputConfig;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.TextBlock;
  import com.anthropic.models.messages.ThinkingConfigAdaptive;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.ToolBash20250124;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import com.fasterxml.jackson.core.JsonProcessingException;
  import com.fasterxml.jackson.core.type.TypeReference;
  import com.fasterxml.jackson.databind.JsonNode;
  import com.fasterxml.jackson.databind.ObjectMapper;
  import java.io.IOException;
  import java.io.UncheckedIOException;
  import java.nio.charset.StandardCharsets;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.nio.file.StandardCopyOption;
  import java.security.MessageDigest;
  import java.time.Duration;
  import java.util.ArrayList;
  import java.util.Comparator;
  import java.util.HashMap;
  import java.util.HexFormat;
  import java.util.List;
  import java.util.Map;
  import java.util.Objects;
  import java.util.Optional;
  import java.util.concurrent.Callable;
  import java.util.concurrent.CancellationException;
  import java.util.concurrent.CompletableFuture;
  import java.util.concurrent.ExecutionException;
  import java.util.concurrent.ExecutorService;
  import java.util.concurrent.Executors;
  import java.util.concurrent.Future;
  import java.util.concurrent.TimeUnit;
  import java.util.concurrent.locks.ReentrantLock;
  import java.util.stream.Collectors;
  import java.util.stream.IntStream;

  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  static final String MODEL = "claude-opus-4-8";
  static final boolean DOC_TEST_MODE =
          !Objects.requireNonNullElse(System.getenv("DOC_TEST_MODE"), "").isEmpty();
  static final OutputConfig.Effort EFFORT = OutputConfig.Effort.XHIGH;

  static final String SYSTEM_PROMPT =
          "You are a helpful general-purpose agent. Answer the user's request directly.";

  static final int REQUEST_TIMEOUT_SECONDS = 600;
  static final RequestOptions REQUEST_OPTIONS =
          RequestOptions.builder().timeout(Duration.ofSeconds(REQUEST_TIMEOUT_SECONDS)).build();
  static final int BASH_TIMEOUT_SECONDS = 60;
  static final int TOOL_RESULT_MAX_CHARS = 8000;
  static final int MAX_CONCURRENT = 10;
  static final int MAX_TOTAL_SUBTASKS = DOC_TEST_MODE ? 2 : 200;
  static final int MAX_SUBAGENT_TURNS = DOC_TEST_MODE ? 1 : 15;
  static final int MAX_MAIN_TURNS = DOC_TEST_MODE ? 1 : 30;
  static final int TURNS_BETWEEN_REFRESHERS = 10;
  static final Path JOURNAL_PATH = Path.of(Optional.ofNullable(System.getenv("ORCH_JOURNAL"))
          .filter(s -> !s.isEmpty()).orElse("orchestration_journal.json"));
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Messages\TextBlock;
  use Anthropic\Messages\ToolUseBlock;

  $client = new Client();

  const MODEL = 'claude-opus-4-8';
  define('DOC_TEST_MODE', (string) getenv('DOC_TEST_MODE') !== '');
  const EFFORT = 'xhigh';

  const SYSTEM_PROMPT = 'You are a helpful general-purpose agent. Answer the user\'s request directly.';

  const REQUEST_TIMEOUT_SECONDS = 600;
  const BASH_TIMEOUT_SECONDS = 60;
  const TOOL_RESULT_MAX_CHARS = 8000;
  const MAX_CONCURRENT = 10;
  define('MAX_TOTAL_SUBTASKS', DOC_TEST_MODE ? 2 : 200);
  define('MAX_SUBAGENT_TURNS', DOC_TEST_MODE ? 1 : 15);
  define('MAX_MAIN_TURNS', DOC_TEST_MODE ? 1 : 30);
  const TURNS_BETWEEN_REFRESHERS = 10;
  define('JOURNAL_PATH', getenv('ORCH_JOURNAL') ?: 'orchestration_journal.json');
  ```

  ```ruby Ruby
  require "anthropic"
  require "digest"
  require "fileutils"
  require "json"
  require "open3"
  require "tmpdir"

  CLIENT = Anthropic::Client.new

  MODEL = "claude-opus-4-8"
  EFFORT = :xhigh

  SYSTEM_PROMPT = "You are a helpful general-purpose agent. Answer the user's request directly."

  REQUEST_TIMEOUT_SECONDS = 600
  BASH_TIMEOUT_SECONDS = 60
  TOOL_RESULT_MAX_CHARS = 8000
  MAX_CONCURRENT = 10
  DOC_TEST_MODE = !ENV["DOC_TEST_MODE"].to_s.empty?
  MAX_TOTAL_SUBTASKS = DOC_TEST_MODE ? 2 : 200
  MAX_SUBAGENT_TURNS = DOC_TEST_MODE ? 1 : 15
  MAX_MAIN_TURNS = DOC_TEST_MODE ? 1 : 30
  TURNS_BETWEEN_REFRESHERS = 10
  JOURNAL_PATH = ENV["ORCH_JOURNAL"].to_s.empty? ? "orchestration_journal.json" : ENV["ORCH_JOURNAL"]
  ```
</CodeGroup>

## Define the mode reminders

The reminders are short on purpose. They flip the mode and point at the tool description, where the heavyweight instructions live. The full text is sent once when the mode turns on, the refresher is re-sent only after several user turns, and the exit notice is sent once when the mode turns off.

<CodeGroup>
  ```python Python
  MODE_ENTER = (
      "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than "
      "the fastest one. Use the Workflow tool on every substantive task, sized to the problem's "
      "natural decomposition rather than the maximum the tool allows. See the Workflow tool's "
      "description for standing consent, granularity guidance, and quality patterns. Work solo "
      "only on conversational or trivial turns."
  )
  MODE_REFRESH = (
      "Orchestration mode is still on. Use the Workflow tool; see its standing consent section."
  )
  MODE_EXIT = (
      "Orchestration mode is off. The Workflow tool's standard opt-in rule applies again."
  )
  ```

  ```typescript TypeScript
  const MODE_ENTER =
    "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than " +
    "the fastest one. Use the Workflow tool on every substantive task, sized to the problem's " +
    "natural decomposition rather than the maximum the tool allows. See the Workflow tool's " +
    "description for standing consent, granularity guidance, and quality patterns. Work solo " +
    "only on conversational or trivial turns.";
  const MODE_REFRESH =
    "Orchestration mode is still on. Use the Workflow tool; see its standing consent section.";
  const MODE_EXIT =
    "Orchestration mode is off. The Workflow tool's standard opt-in rule applies again.";
  ```

  ```csharp C#
  const string modeEnter =
      "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than "
      + "the fastest one. Use the Workflow tool on every substantive task, sized to the problem's "
      + "natural decomposition rather than the maximum the tool allows. See the Workflow tool's "
      + "description for standing consent, granularity guidance, and quality patterns. Work solo "
      + "only on conversational or trivial turns.";
  const string modeRefresh =
      "Orchestration mode is still on. Use the Workflow tool; see its standing consent section.";
  const string modeExit =
      "Orchestration mode is off. The Workflow tool's standard opt-in rule applies again.";
  ```

  ```go Go
  const (
  	modeEnter = "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than " +
  		"the fastest one. Use the Workflow tool on every substantive task, sized to the problem's " +
  		"natural decomposition rather than the maximum the tool allows. See the Workflow tool's " +
  		"description for standing consent, granularity guidance, and quality patterns. Work solo " +
  		"only on conversational or trivial turns."
  	modeRefresh = "Orchestration mode is still on. Use the Workflow tool; see its standing consent section."
  	modeExit    = "Orchestration mode is off. The Workflow tool's standard opt-in rule applies again."
  )

  ```

  ```java Java
  static final String MODE_ENTER =
          "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than "
                  + "the fastest one. Use the Workflow tool on every substantive task, sized to the problem's "
                  + "natural decomposition rather than the maximum the tool allows. See the Workflow tool's "
                  + "description for standing consent, granularity guidance, and quality patterns. Work solo "
                  + "only on conversational or trivial turns.";
  static final String MODE_REFRESH =
          "Orchestration mode is still on. Use the Workflow tool; see its standing consent section.";
  static final String MODE_EXIT =
          "Orchestration mode is off. The Workflow tool's standard opt-in rule applies again.";
  ```

  ```php PHP
  const MODE_ENTER =
      'Orchestration mode is on: optimize for the most exhaustive, correct answer rather than '
      . 'the fastest one. Use the Workflow tool on every substantive task, sized to the problem\'s '
      . 'natural decomposition rather than the maximum the tool allows. See the Workflow tool\'s '
      . 'description for standing consent, granularity guidance, and quality patterns. Work solo '
      . 'only on conversational or trivial turns.';
  const MODE_REFRESH =
      'Orchestration mode is still on. Use the Workflow tool; see its standing consent section.';
  const MODE_EXIT =
      'Orchestration mode is off. The Workflow tool\'s standard opt-in rule applies again.';
  ```

  ```ruby Ruby
  MODE_ENTER =
    "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than " \
    "the fastest one. Use the Workflow tool on every substantive task, sized to the problem's " \
    "natural decomposition rather than the maximum the tool allows. See the Workflow tool's " \
    "description for standing consent, granularity guidance, and quality patterns. Work solo " \
    "only on conversational or trivial turns."
  MODE_REFRESH =
    "Orchestration mode is still on. Use the Workflow tool; see its standing consent section."
  MODE_EXIT =
    "Orchestration mode is off. The Workflow tool's standard opt-in rule applies again."
  ```
</CodeGroup>

## Grant standing consent in the tool description

The Workflow tool carries the real behavioral contract: the opt-in rule, the standing consent that applies while the mode is on, granularity guidance for sizing the fan-out, and the quality patterns the model can reach for (a verification wave, a completeness critic, multi-phase sequencing). Subagents also get a `report_findings` tool so their results come back as structured JSON instead of prose, and the bash tool is the Anthropic-defined `bash_20250124` tool run locally.

<CodeGroup>
  ```python Python
  WORKFLOW_TOOL = {
      "name": "Workflow",
      "description": (
          "Orchestrate a multi-agent workflow: split a large task into independent subtasks "
          "and run them as parallel agents, then collect their results.\n\n"
          "Opt-in: only use this tool when the user explicitly asks for a workflow, or when a "
          "system message confirms that orchestration mode is on.\n\n"
          "Quality patterns: adversarial verification (a second wave of agents checks the first "
          "wave's findings against the source), a completeness critic (one agent hunts for what "
          "the others missed), and multi-phase sequencing (understand, design, implement, and "
          "review as separate workflow calls, reading results between phases). A useful default "
          "is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n"
          "Granularity: scope each subtask to a distinct concern, component, or question rather "
          "than per line or per file section. Scale the count to what the user asked for: a "
          "focused review of a module of a few hundred lines rarely needs more than about ten "
          "subtasks; a broad audit of a large codebase can justify more.\n\n"
          "Standing consent: while a system message confirms orchestration mode is on, that "
          "opt-in is standing. Author and run a workflow for every substantive task by default, "
          "and lean toward verifying findings adversarially. Work solo only on conversational "
          "turns or trivial mechanical edits. When a system message says the mode is off, "
          "revert to the opt-in rule above."
      ),
      "input_schema": {
          "type": "object",
          "properties": {
              "subtasks": {
                  "type": "array",
                  "items": {"type": "string"},
                  "description": "Independent subtask prompts to run as parallel agents",
              }
          },
          "required": ["subtasks"],
      },
  }

  BASH_TOOL = {"type": "bash_20250124", "name": "bash"}

  REPORT_TOOL = {
      "name": "report_findings",
      "description": (
          "Report the final findings for your subtask. Call this exactly once, when you are "
          "done investigating; it ends your task."
      ),
      "input_schema": {
          "type": "object",
          "properties": {
              "summary": {"type": "string", "description": "Two or three sentences of synthesis"},
              "findings": {
                  "type": "array",
                  "items": {
                      "type": "object",
                      "properties": {
                          "claim": {"type": "string", "description": "The finding, one sentence"},
                          "evidence": {
                              "type": "string",
                              "description": "How it was verified (file, line, or command output)",
                          },
                          "severity": {"type": "string", "enum": ["high", "medium", "low", "info"]},
                      },
                      "required": ["claim", "evidence", "severity"],
                  },
              },
          },
          "required": ["summary", "findings"],
      },
  }
  ```

  ```typescript TypeScript
  const WORKFLOW_TOOL: Anthropic.Tool = {
    name: "Workflow",
    description:
      "Orchestrate a multi-agent workflow: split a large task into independent subtasks " +
      "and run them as parallel agents, then collect their results.\n\n" +
      "Opt-in: only use this tool when the user explicitly asks for a workflow, or when a " +
      "system message confirms that orchestration mode is on.\n\n" +
      "Quality patterns: adversarial verification (a second wave of agents checks the first " +
      "wave's findings against the source), a completeness critic (one agent hunts for what " +
      "the others missed), and multi-phase sequencing (understand, design, implement, and " +
      "review as separate workflow calls, reading results between phases). A useful default " +
      "is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n" +
      "Granularity: scope each subtask to a distinct concern, component, or question rather " +
      "than per line or per file section. Scale the count to what the user asked for: a " +
      "focused review of a module of a few hundred lines rarely needs more than about ten " +
      "subtasks; a broad audit of a large codebase can justify more.\n\n" +
      "Standing consent: while a system message confirms orchestration mode is on, that " +
      "opt-in is standing. Author and run a workflow for every substantive task by default, " +
      "and lean toward verifying findings adversarially. Work solo only on conversational " +
      "turns or trivial mechanical edits. When a system message says the mode is off, " +
      "revert to the opt-in rule above.",
    input_schema: {
      type: "object",
      properties: {
        subtasks: {
          type: "array",
          items: { type: "string" },
          description: "Independent subtask prompts to run as parallel agents",
        },
      },
      required: ["subtasks"],
    },
  };

  const BASH_TOOL: Anthropic.ToolBash20250124 = { type: "bash_20250124", name: "bash" };

  const REPORT_TOOL: Anthropic.Tool = {
    name: "report_findings",
    description:
      "Report the final findings for your subtask. Call this exactly once, when you are " +
      "done investigating; it ends your task.",
    input_schema: {
      type: "object",
      properties: {
        summary: { type: "string", description: "Two or three sentences of synthesis" },
        findings: {
          type: "array",
          items: {
            type: "object",
            properties: {
              claim: { type: "string", description: "The finding, one sentence" },
              evidence: {
                type: "string",
                description: "How it was verified (file, line, or command output)",
              },
              severity: { type: "string", enum: ["high", "medium", "low", "info"] },
            },
            required: ["claim", "evidence", "severity"],
          },
        },
      },
      required: ["summary", "findings"],
    },
  };
  ```

  ```csharp C#
  Tool workflowTool = new()
  {
      Name = "Workflow",
      Description =
          "Orchestrate a multi-agent workflow: split a large task into independent subtasks "
          + "and run them as parallel agents, then collect their results.\n\n"
          + "Opt-in: only use this tool when the user explicitly asks for a workflow, or when a "
          + "system message confirms that orchestration mode is on.\n\n"
          + "Quality patterns: adversarial verification (a second wave of agents checks the first "
          + "wave's findings against the source), a completeness critic (one agent hunts for what "
          + "the others missed), and multi-phase sequencing (understand, design, implement, and "
          + "review as separate workflow calls, reading results between phases). A useful default "
          + "is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n"
          + "Granularity: scope each subtask to a distinct concern, component, or question rather "
          + "than per line or per file section. Scale the count to what the user asked for: a "
          + "focused review of a module of a few hundred lines rarely needs more than about ten "
          + "subtasks; a broad audit of a large codebase can justify more.\n\n"
          + "Standing consent: while a system message confirms orchestration mode is on, that "
          + "opt-in is standing. Author and run a workflow for every substantive task by default, "
          + "and lean toward verifying findings adversarially. Work solo only on conversational "
          + "turns or trivial mechanical edits. When a system message says the mode is off, "
          + "revert to the opt-in rule above.",
      InputSchema = new InputSchema
      {
          Properties = new Dictionary<string, JsonElement>
          {
              ["subtasks"] = JsonSerializer.SerializeToElement(new
              {
                  type = "array",
                  items = new { type = "string" },
                  description = "Independent subtask prompts to run as parallel agents",
              }),
          },
          Required = ["subtasks"],
      },
  };

  ToolBash20250124 bashTool = new();

  Tool reportTool = new()
  {
      Name = "report_findings",
      Description =
          "Report the final findings for your subtask. Call this exactly once, when you are "
          + "done investigating; it ends your task.",
      InputSchema = new InputSchema
      {
          Properties = new Dictionary<string, JsonElement>
          {
              ["summary"] = JsonSerializer.SerializeToElement(new
              {
                  type = "string",
                  description = "Two or three sentences of synthesis",
              }),
              ["findings"] = JsonSerializer.SerializeToElement(new
              {
                  type = "array",
                  items = new
                  {
                      type = "object",
                      properties = new
                      {
                          claim = new { type = "string", description = "The finding, one sentence" },
                          evidence = new
                          {
                              type = "string",
                              description = "How it was verified (file, line, or command output)",
                          },
                          severity = new { type = "string", @enum = new[] { "high", "medium", "low", "info" } },
                      },
                      required = new[] { "claim", "evidence", "severity" },
                  },
              }),
          },
          Required = ["summary", "findings"],
      },
  };
  ```

  ```go Go
  var workflowTool = anthropic.ToolUnionParam{
  	OfTool: &anthropic.ToolParam{
  		Name: "Workflow",
  		Description: anthropic.String("Orchestrate a multi-agent workflow: split a large task into independent subtasks " +
  			"and run them as parallel agents, then collect their results.\n\n" +
  			"Opt-in: only use this tool when the user explicitly asks for a workflow, or when a " +
  			"system message confirms that orchestration mode is on.\n\n" +
  			"Quality patterns: adversarial verification (a second wave of agents checks the first " +
  			"wave's findings against the source), a completeness critic (one agent hunts for what " +
  			"the others missed), and multi-phase sequencing (understand, design, implement, and " +
  			"review as separate workflow calls, reading results between phases). A useful default " +
  			"is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n" +
  			"Granularity: scope each subtask to a distinct concern, component, or question rather " +
  			"than per line or per file section. Scale the count to what the user asked for: a " +
  			"focused review of a module of a few hundred lines rarely needs more than about ten " +
  			"subtasks; a broad audit of a large codebase can justify more.\n\n" +
  			"Standing consent: while a system message confirms orchestration mode is on, that " +
  			"opt-in is standing. Author and run a workflow for every substantive task by default, " +
  			"and lean toward verifying findings adversarially. Work solo only on conversational " +
  			"turns or trivial mechanical edits. When a system message says the mode is off, " +
  			"revert to the opt-in rule above."),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"subtasks": map[string]any{
  					"type":        "array",
  					"items":       map[string]any{"type": "string"},
  					"description": "Independent subtask prompts to run as parallel agents",
  				},
  			},
  			Required: []string{"subtasks"},
  		},
  	},
  }

  var bashTool = anthropic.ToolUnionParam{
  	OfBashTool20250124: &anthropic.ToolBash20250124Param{},
  }

  var reportTool = anthropic.ToolUnionParam{
  	OfTool: &anthropic.ToolParam{
  		Name: "report_findings",
  		Description: anthropic.String("Report the final findings for your subtask. Call this exactly once, when you are " +
  			"done investigating; it ends your task."),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"summary": map[string]any{"type": "string", "description": "Two or three sentences of synthesis"},
  				"findings": map[string]any{
  					"type": "array",
  					"items": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"claim": map[string]any{"type": "string", "description": "The finding, one sentence"},
  							"evidence": map[string]any{
  								"type":        "string",
  								"description": "How it was verified (file, line, or command output)",
  							},
  							"severity": map[string]any{"type": "string", "enum": []string{"high", "medium", "low", "info"}},
  						},
  						"required": []string{"claim", "evidence", "severity"},
  					},
  				},
  			},
  			Required: []string{"summary", "findings"},
  		},
  	},
  }

  ```

  ```java Java
  static final Tool WORKFLOW_TOOL = Tool.builder()
          .name("Workflow")
          .description("Orchestrate a multi-agent workflow: split a large task into independent subtasks "
                  + "and run them as parallel agents, then collect their results.\n\n"
                  + "Opt-in: only use this tool when the user explicitly asks for a workflow, or when a "
                  + "system message confirms that orchestration mode is on.\n\n"
                  + "Quality patterns: adversarial verification (a second wave of agents checks the first "
                  + "wave's findings against the source), a completeness critic (one agent hunts for what "
                  + "the others missed), and multi-phase sequencing (understand, design, implement, and "
                  + "review as separate workflow calls, reading results between phases). A useful default "
                  + "is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n"
                  + "Granularity: scope each subtask to a distinct concern, component, or question rather "
                  + "than per line or per file section. Scale the count to what the user asked for: a "
                  + "focused review of a module of a few hundred lines rarely needs more than about ten "
                  + "subtasks; a broad audit of a large codebase can justify more.\n\n"
                  + "Standing consent: while a system message confirms orchestration mode is on, that "
                  + "opt-in is standing. Author and run a workflow for every substantive task by default, "
                  + "and lean toward verifying findings adversarially. Work solo only on conversational "
                  + "turns or trivial mechanical edits. When a system message says the mode is off, "
                  + "revert to the opt-in rule above.")
          .inputSchema(Tool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                          "subtasks", Map.of(
                                  "type", "array",
                                  "items", Map.of("type", "string"),
                                  "description", "Independent subtask prompts to run as parallel agents"))))
                  .putAdditionalProperty("required", JsonValue.from(List.of("subtasks")))
                  .build())
          .build();

  static final ToolBash20250124 BASH_TOOL = ToolBash20250124.builder().build();

  static final Tool REPORT_TOOL = Tool.builder()
          .name("report_findings")
          .description("Report the final findings for your subtask. Call this exactly once, when you are "
                  + "done investigating; it ends your task.")
          .inputSchema(Tool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                          "summary", Map.of("type", "string", "description", "Two or three sentences of synthesis"),
                          "findings", Map.of(
                                  "type", "array",
                                  "items", Map.of(
                                          "type", "object",
                                          "properties", Map.of(
                                                  "claim", Map.of(
                                                          "type", "string",
                                                          "description", "The finding, one sentence"),
                                                  "evidence", Map.of(
                                                          "type", "string",
                                                          "description", "How it was verified (file, line, or command output)"),
                                                  "severity", Map.of(
                                                          "type", "string",
                                                          "enum", List.of("high", "medium", "low", "info"))),
                                          "required", List.of("claim", "evidence", "severity"))))))
                  .putAdditionalProperty("required", JsonValue.from(List.of("summary", "findings")))
                  .build())
          .build();
  ```

  ```php PHP
  const WORKFLOW_TOOL = [
      'name' => 'Workflow',
      'description' =>
          'Orchestrate a multi-agent workflow: split a large task into independent subtasks '
          . "and run them as parallel agents, then collect their results.\n\n"
          . 'Opt-in: only use this tool when the user explicitly asks for a workflow, or when a '
          . "system message confirms that orchestration mode is on.\n\n"
          . 'Quality patterns: adversarial verification (a second wave of agents checks the first '
          . 'wave\'s findings against the source), a completeness critic (one agent hunts for what '
          . 'the others missed), and multi-phase sequencing (understand, design, implement, and '
          . 'review as separate workflow calls, reading results between phases). A useful default '
          . "is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n"
          . 'Granularity: scope each subtask to a distinct concern, component, or question rather '
          . 'than per line or per file section. Scale the count to what the user asked for: a '
          . 'focused review of a module of a few hundred lines rarely needs more than about ten '
          . "subtasks; a broad audit of a large codebase can justify more.\n\n"
          . 'Standing consent: while a system message confirms orchestration mode is on, that '
          . 'opt-in is standing. Author and run a workflow for every substantive task by default, '
          . 'and lean toward verifying findings adversarially. Work solo only on conversational '
          . 'turns or trivial mechanical edits. When a system message says the mode is off, '
          . 'revert to the opt-in rule above.',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'subtasks' => [
                  'type' => 'array',
                  'items' => ['type' => 'string'],
                  'description' => 'Independent subtask prompts to run as parallel agents',
              ],
          ],
          'required' => ['subtasks'],
      ],
  ];

  const BASH_TOOL = ['type' => 'bash_20250124', 'name' => 'bash'];

  const REPORT_TOOL = [
      'name' => 'report_findings',
      'description' =>
          'Report the final findings for your subtask. Call this exactly once, when you are '
          . 'done investigating; it ends your task.',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'summary' => ['type' => 'string', 'description' => 'Two or three sentences of synthesis'],
              'findings' => [
                  'type' => 'array',
                  'items' => [
                      'type' => 'object',
                      'properties' => [
                          'claim' => ['type' => 'string', 'description' => 'The finding, one sentence'],
                          'evidence' => [
                              'type' => 'string',
                              'description' => 'How it was verified (file, line, or command output)',
                          ],
                          'severity' => ['type' => 'string', 'enum' => ['high', 'medium', 'low', 'info']],
                      ],
                      'required' => ['claim', 'evidence', 'severity'],
                  ],
              ],
          ],
          'required' => ['summary', 'findings'],
      ],
  ];
  ```

  ```ruby Ruby
  WORKFLOW_TOOL = {
    name: "Workflow",
    description:
      "Orchestrate a multi-agent workflow: split a large task into independent subtasks " \
      "and run them as parallel agents, then collect their results.\n\n" \
      "Opt-in: only use this tool when the user explicitly asks for a workflow, or when a " \
      "system message confirms that orchestration mode is on.\n\n" \
      "Quality patterns: adversarial verification (a second wave of agents checks the first " \
      "wave's findings against the source), a completeness critic (one agent hunts for what " \
      "the others missed), and multi-phase sequencing (understand, design, implement, and " \
      "review as separate workflow calls, reading results between phases). A useful default " \
      "is hybrid: scout inline first to discover the work-list, then fan out over it.\n\n" \
      "Granularity: scope each subtask to a distinct concern, component, or question rather " \
      "than per line or per file section. Scale the count to what the user asked for: a " \
      "focused review of a module of a few hundred lines rarely needs more than about ten " \
      "subtasks; a broad audit of a large codebase can justify more.\n\n" \
      "Standing consent: while a system message confirms orchestration mode is on, that " \
      "opt-in is standing. Author and run a workflow for every substantive task by default, " \
      "and lean toward verifying findings adversarially. Work solo only on conversational " \
      "turns or trivial mechanical edits. When a system message says the mode is off, " \
      "revert to the opt-in rule above.",
    input_schema: {
      type: "object",
      properties: {
        subtasks: {
          type: "array",
          items: {type: "string"},
          description: "Independent subtask prompts to run as parallel agents"
        }
      },
      required: ["subtasks"]
    }
  }.freeze

  BASH_TOOL = {type: "bash_20250124", name: "bash"}.freeze

  REPORT_TOOL = {
    name: "report_findings",
    description:
      "Report the final findings for your subtask. Call this exactly once, when you are " \
      "done investigating; it ends your task.",
    input_schema: {
      type: "object",
      properties: {
        summary: {type: "string", description: "Two or three sentences of synthesis"},
        findings: {
          type: "array",
          items: {
            type: "object",
            properties: {
              claim: {type: "string", description: "The finding, one sentence"},
              evidence: {
                type: "string",
                description: "How it was verified (file, line, or command output)"
              },
              severity: {type: "string", enum: ["high", "medium", "low", "info"]}
            },
            required: ["claim", "evidence", "severity"]
          }
        }
      },
      required: ["summary", "findings"]
    }
  }.freeze
  ```
</CodeGroup>

## Run the bash tool locally

The bash handler runs the requested command with a timeout, captures combined stdout and stderr, and truncates the result so a runaway command can't flood the context window. Commands run in the directory you launch the example from, so pointing it at a project means starting it there; when `DOC_TEST_MODE` is set, the harness instead gives bash a small throwaway fixture directory that is removed on exit. There is no sandbox here: the command runs with the permissions of the process that launched the example. For clarity this example runs each call in a fresh subshell rather than maintaining the persistent session the `bash_20250124` contract describes; a production agent should back the tool with a long-lived shell so that working directory, environment, and the `restart` action behave as documented.

<CodeGroup>
  ```python Python
  # Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  # points it at a throwaway fixture directory instead, removed on exit.
  if DOC_TEST_MODE:
      WORK_DIR = tempfile.mkdtemp(prefix="orchestration-")
      atexit.register(shutil.rmtree, WORK_DIR, ignore_errors=True)
      with open(os.path.join(WORK_DIR, "sample.py"), "w") as fixture:
          fixture.write(
              "def fib(n):\n"
              "    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n"
              "print(fib(10))\n"
          )
  else:
      WORK_DIR = os.getcwd()


  def run_bash(command: str) -> tuple[str, bool]:
      """Run a shell command and return (output, is_error). No sandbox: example code only."""
      print(f"[bash] {command}", file=sys.stderr)
      try:
          proc = subprocess.run(
              ["bash", "-c", command],
              cwd=WORK_DIR,
              capture_output=True,
              text=True,
              errors="replace",
              timeout=BASH_TIMEOUT_SECONDS,
          )
      except subprocess.TimeoutExpired:
          return f"command timed out after {BASH_TIMEOUT_SECONDS}s", True
      output = (proc.stdout + proc.stderr).strip() or "(no output)"
      if len(output) > TOOL_RESULT_MAX_CHARS:
          output = output[:TOOL_RESULT_MAX_CHARS] + f"\n(truncated at {TOOL_RESULT_MAX_CHARS} chars)"
      if proc.returncode != 0:
          output = f"(exit code {proc.returncode})\n{output}"
      return output, proc.returncode != 0


  def handle_bash_block(block) -> tuple[str, bool]:
      if block.input.get("restart") is True:
          return "Shell restarted.", False
      command = block.input.get("command")
      if not isinstance(command, str) or not command:
          return "bash error: no command was provided.", True
      return run_bash(command)
  ```

  ```typescript TypeScript
  const execShell = promisify(exec);

  // Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  // points it at a throwaway fixture directory instead, removed on exit.
  const WORK_DIR = DOC_TEST_MODE
    ? await mkdtemp(join(tmpdir(), "orchestration-"))
    : process.cwd();
  if (DOC_TEST_MODE) {
    await writeFile(
      join(WORK_DIR, "sample.py"),
      "def fib(n):\n" +
        "    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n" +
        "print(fib(10))\n",
    );
    process.on("exit", () => rmSync(WORK_DIR, { recursive: true, force: true }));
  }

  // Run a shell command and return its output. No sandbox: example code only.
  async function runBash(command: string): Promise<{ output: string; isError: boolean }> {
    console.error(`[bash] ${command}`);
    let stdout = "";
    let stderr = "";
    let exitCode = 0;
    try {
      ({ stdout, stderr } = await execShell(command, {
        shell: "/bin/bash",
        cwd: WORK_DIR,
        timeout: BASH_TIMEOUT_SECONDS * 1000,
        maxBuffer: 16 * 1024 * 1024,
      }));
    } catch (error) {
      const failure = error as {
        stdout?: string;
        stderr?: string;
        code?: number | string;
        killed?: boolean;
      };
      if (failure.killed && failure.code !== "ERR_CHILD_PROCESS_STDIO_MAXBUFFER") {
        return { output: `command timed out after ${BASH_TIMEOUT_SECONDS}s`, isError: true };
      }
      stdout = failure.stdout ?? "";
      stderr = failure.stderr ?? "";
      exitCode = typeof failure.code === "number" ? failure.code : 1;
    }
    let output = (stdout + stderr).trim() || "(no output)";
    const codePoints = [...output];
    if (codePoints.length > TOOL_RESULT_MAX_CHARS) {
      output =
        codePoints.slice(0, TOOL_RESULT_MAX_CHARS).join("") +
        `\n(truncated at ${TOOL_RESULT_MAX_CHARS} chars)`;
    }
    if (exitCode !== 0) {
      output = `(exit code ${exitCode})\n${output}`;
    }
    return { output, isError: exitCode !== 0 };
  }

  async function handleBashBlock(
    block: Anthropic.ToolUseBlock,
  ): Promise<{ output: string; isError: boolean }> {
    const input = block.input as { command?: string; restart?: boolean };
    if (input.restart === true) {
      return { output: "Shell restarted.", isError: false };
    }
    if (!input.command) {
      return { output: "bash error: no command was provided.", isError: true };
    }
    return runBash(input.command);
  }
  ```

  ```csharp C#
  // Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  // points it at a throwaway fixture directory instead, removed on exit.
  var workDir = Environment.CurrentDirectory;
  if (docTestMode)
  {
      workDir = Directory.CreateTempSubdirectory("orchestration-").FullName;
      File.WriteAllText(Path.Combine(workDir, "sample.py"),
          "def fib(n):\n" +
          "    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n" +
          "print(fib(10))\n");
      var fixtureDir = workDir;
      AppDomain.CurrentDomain.ProcessExit += (_, _) =>
      {
          try { Directory.Delete(fixtureDir, recursive: true); }
          catch { /* Best-effort cleanup; the OS tmp sweeper handles leftovers. */ }
      };
  }

  // Run a shell command and return its output plus an error flag. No sandbox: example code only.
  async Task<(string Output, bool IsError)> RunBash(string command)
  {
      Console.Error.WriteLine($"[bash] {command}");
      using var process = Process.Start(new ProcessStartInfo("bash")
      {
          ArgumentList = { "-c", command },
          WorkingDirectory = workDir,
          RedirectStandardOutput = true,
          RedirectStandardError = true,
      });
      if (process is null)
      {
          return ("bash error: the shell process failed to start.", true);
      }
      var stdoutTask = process.StandardOutput.ReadToEndAsync();
      var stderrTask = process.StandardError.ReadToEndAsync();
      using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(bashTimeoutSeconds));
      try
      {
          await process.WaitForExitAsync(timeout.Token);
      }
      catch (OperationCanceledException)
      {
          process.Kill(entireProcessTree: true);
          // Let the reader tasks finish before the process is disposed.
          try
          {
              await Task.WhenAll(stdoutTask, stderrTask);
          }
          catch
          {
              // The output is discarded on timeout, so reader failures are ignored too.
          }
          return ($"command timed out after {bashTimeoutSeconds}s", true);
      }
      var output = (await stdoutTask + await stderrTask).Trim();
      if (output.Length == 0)
      {
          output = "(no output)";
      }
      if (output.Length > toolResultMaxChars)
      {
          output = output[..toolResultMaxChars] + $"\n(truncated at {toolResultMaxChars} chars)";
      }
      if (process.ExitCode != 0)
      {
          output = $"(exit code {process.ExitCode})\n{output}";
      }
      return (output, process.ExitCode != 0);
  }

  // Execute one bash tool call requested by the model.
  async Task<(string Output, bool IsError)> HandleBashBlock(ToolUseBlock block)
  {
      if (block.Input.TryGetValue("restart", out var restart) && restart.ValueKind == JsonValueKind.True)
      {
          return ("Shell restarted.", false);
      }
      var command = block.Input.TryGetValue("command", out var rawCommand) && rawCommand.ValueKind == JsonValueKind.String
          ? rawCommand.GetString()!
          : "";
      if (command.Length == 0)
      {
          return ("bash error: no command was provided.", true);
      }
      return await RunBash(command);
  }
  ```

  ```go Go
  // Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  // points it at a throwaway fixture directory instead, removed on exit.
  var workDir = func() string {
  	if !docTestMode {
  		dir, err := os.Getwd()
  		if err != nil {
  			log.Fatal(err)
  		}
  		return dir
  	}
  	dir, err := os.MkdirTemp("", "orchestration-")
  	if err != nil {
  		log.Fatal(err)
  	}
  	fixture := "def fib(n):\n" +
  		"    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n" +
  		"print(fib(10))\n"
  	if err := os.WriteFile(filepath.Join(dir, "sample.py"), []byte(fixture), 0o644); err != nil {
  		log.Fatal(err)
  	}
  	return dir
  }()

  // runBash runs a shell command and returns its output plus an error flag.
  // No sandbox: example code only.
  func runBash(ctx context.Context, command string) (string, bool) {
  	fmt.Fprintf(os.Stderr, "[bash] %s\n", command)
  	ctx, cancel := context.WithTimeout(ctx, bashTimeoutSeconds*time.Second)
  	defer cancel()
  	cmd := exec.CommandContext(ctx, "bash", "-c", command)
  	cmd.Dir = workDir
  	combined, err := cmd.CombinedOutput()
  	if errors.Is(ctx.Err(), context.DeadlineExceeded) {
  		return fmt.Sprintf("command timed out after %ds", bashTimeoutSeconds), true
  	}
  	output := strings.TrimSpace(string(combined))
  	if output == "" {
  		output = "(no output)"
  	}
  	if runes := []rune(output); len(runes) > toolResultMaxChars {
  		output = string(runes[:toolResultMaxChars]) + fmt.Sprintf("\n(truncated at %d chars)", toolResultMaxChars)
  	}
  	if err == nil {
  		return output, false
  	}
  	var exitErr *exec.ExitError
  	if errors.As(err, &exitErr) {
  		return fmt.Sprintf("(exit code %d)\n%s", exitErr.ExitCode(), output), true
  	}
  	return fmt.Sprintf("(%s)\n%s", err, output), true
  }

  // handleBashBlock executes one bash tool call requested by the model.
  func handleBashBlock(ctx context.Context, block anthropic.ToolUseBlock) (string, bool) {
  	var input struct {
  		Command string `json:"command"`
  		Restart bool   `json:"restart"`
  	}
  	if err := json.Unmarshal(block.Input, &input); err != nil {
  		return fmt.Sprintf("bash error: could not parse input: %s", err), true
  	}
  	if input.Restart {
  		return "Shell restarted.", false
  	}
  	if input.Command == "" {
  		return "bash error: no command was provided.", true
  	}
  	return runBash(ctx, input.Command)
  }

  ```

  ```java Java
  record ToolOutput(String output, boolean isError) {}

  // Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  // points it at a throwaway fixture directory instead, removed on exit.
  static final Path WORK_DIR = createWorkDir();

  static Path createWorkDir() {
      if (!DOC_TEST_MODE) {
          return Path.of(System.getProperty("user.dir"));
      }
      try {
          var dir = Files.createTempDirectory("orchestration-");
          Files.writeString(dir.resolve("sample.py"), """
                  def fib(n):
                      return n if n < 2 else fib(n - 1) + fib(n - 2)

                  print(fib(10))
                  """);
          Runtime.getRuntime().addShutdownHook(new Thread(() -> {
              try (var paths = Files.walk(dir)) {
                  paths.sorted(Comparator.reverseOrder()).forEach(p -> {
                      try { Files.deleteIfExists(p); } catch (IOException ignored) {}
                  });
              } catch (IOException ignored) {
                  // Best-effort cleanup; the OS tmp sweeper handles leftovers.
              }
          }));
          return dir;
      } catch (IOException error) {
          throw new UncheckedIOException(error);
      }
  }

  // Run a shell command and return its output plus an error flag. No sandbox: example code only.
  ToolOutput runBash(String command) throws InterruptedException {
      System.err.println("[bash] " + command);
      Process process;
      try {
          process = new ProcessBuilder("bash", "-c", command)
                  .directory(WORK_DIR.toFile())
                  .redirectErrorStream(true)
                  .start();
      } catch (IOException error) {
          return new ToolOutput("(" + error + ")", true);
      }
      // Drain stdout on another thread so a filled pipe cannot stall the timeout wait below.
      CompletableFuture<String> outputReader = CompletableFuture.supplyAsync(() -> {
          try (var stdout = process.getInputStream()) {
              return new String(stdout.readAllBytes(), StandardCharsets.UTF_8);
          } catch (IOException error) {
              return "";
          }
      });
      if (!process.waitFor(BASH_TIMEOUT_SECONDS, TimeUnit.SECONDS)) {
          process.destroyForcibly();
          outputReader.cancel(true);
          return new ToolOutput("command timed out after " + BASH_TIMEOUT_SECONDS + "s", true);
      }
      String output = outputReader.join().trim();
      if (output.isEmpty()) {
          output = "(no output)";
      }
      if (output.length() > TOOL_RESULT_MAX_CHARS) {
          output = output.substring(0, TOOL_RESULT_MAX_CHARS)
                  + "\n(truncated at " + TOOL_RESULT_MAX_CHARS + " chars)";
      }
      int exitCode = process.exitValue();
      if (exitCode != 0) {
          return new ToolOutput("(exit code " + exitCode + ")\n" + output, true);
      }
      return new ToolOutput(output, false);
  }

  // Execute one bash tool call requested by the model.
  ToolOutput handleBashBlock(ToolUseBlock block) throws InterruptedException {
      Map<String, JsonValue> input = (Map<String, JsonValue>) block._input().asObject().orElse(Map.of());
      JsonValue restart = input.getOrDefault("restart", JsonValue.from(false));
      if (Boolean.TRUE.equals(restart.asBoolean().orElse(false))) {
          return new ToolOutput("Shell restarted.", false);
      }
      JsonValue raw = input.get("command");
      String command = raw != null && raw.asString().isPresent() ? raw.asStringOrThrow() : "";
      if (command.isEmpty()) {
          return new ToolOutput("bash error: no command was provided.", true);
      }
      return runBash(command);
  }
  ```

  ```php PHP
  // Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  // points it at a throwaway fixture directory instead, removed on exit.
  if (DOC_TEST_MODE) {
      $workDir = sys_get_temp_dir() . '/orchestration-' . bin2hex(random_bytes(8));
      if (!mkdir($workDir, 0700)) {
          throw new RuntimeException("could not create working directory {$workDir}");
      }
      file_put_contents(
          $workDir . '/sample.py',
          "def fib(n):\n"
          . "    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n"
          . "print(fib(10))\n",
      );
      register_shutdown_function(function () use ($workDir): void {
          foreach (glob($workDir . '/*') ?: [] as $entry) {
              @unlink($entry);
          }
          @rmdir($workDir);
      });
  } else {
      $workDir = getcwd() ?: '.';
  }
  define('WORK_DIR', $workDir);

  /**
   * Run a shell command and return [output, isError]. The coreutils timeout command
   * enforces the time limit. No sandbox: example code only.
   */
  function runBash(string $command): array
  {
      fwrite(STDERR, "[bash] {$command}\n");
      // Requires GNU coreutils 'timeout'. On macOS: brew install coreutils, or replace with gtimeout.
      exec(
          'cd ' . escapeshellarg(WORK_DIR) . ' && timeout ' . BASH_TIMEOUT_SECONDS
              . ' bash -c ' . escapeshellarg($command) . ' 2>&1',
          $outputLines,
          $exitCode,
      );
      if ($exitCode === 124) {
          return ['command timed out after ' . BASH_TIMEOUT_SECONDS . 's', true];
      }
      $output = trim(implode("\n", $outputLines));
      if ($output === '') {
          $output = '(no output)';
      }
      if (mb_strlen($output) > TOOL_RESULT_MAX_CHARS) {
          $output = mb_substr($output, 0, TOOL_RESULT_MAX_CHARS)
              . "\n(truncated at " . TOOL_RESULT_MAX_CHARS . ' chars)';
      }
      if ($exitCode !== 0) {
          $output = "(exit code {$exitCode})\n{$output}";
      }
      return [$output, $exitCode !== 0];
  }

  /** Execute one bash tool call requested by the model. */
  function handleBashBlock(ToolUseBlock $block): array
  {
      if (($block->input['restart'] ?? null) === true) {
          return ['Shell restarted.', false];
      }
      $command = $block->input['command'] ?? '';
      if (!is_string($command) || $command === '') {
          return ['bash error: no command was provided.', true];
      }
      return runBash($command);
  }
  ```

  ```ruby Ruby
  # Run bash where the example was launched. In DOC_TEST_MODE the docs harness
  # points it at a throwaway fixture directory instead, removed on exit.
  WORK_DIR =
    if DOC_TEST_MODE
      Dir.mktmpdir("orchestration-").tap do |dir|
        File.write(File.join(dir, "sample.py"), <<~PYTHON)
          def fib(n):
              return n if n < 2 else fib(n - 1) + fib(n - 2)

          print(fib(10))
        PYTHON
        at_exit { FileUtils.remove_entry(dir, true) }
      end
    else
      Dir.pwd
    end

  # Tool input arrives as a Hash or as a raw JSON string from the streaming
  # accumulator; normalize either shape to a string-keyed Hash.
  def parse_tool_input(raw)
    return raw.transform_keys(&:to_s) if raw.is_a?(Hash)
    parsed = JSON.parse(raw.to_s) rescue nil
    parsed.is_a?(Hash) ? parsed : {}
  end

  # Run a shell command and return [output, is_error]. No sandbox: example code only.
  def run_bash(command)
    warn "[bash] #{command}"
    begin
      stdin, stdout_and_stderr, wait_thr = Open3.popen2e("bash", "-c", command, pgroup: true, chdir: WORK_DIR)
      stdin.close
      reader = Thread.new { stdout_and_stderr.read.scrub }
      # Enforce the time limit with a monotonic-clock deadline so a timed-out command is
      # terminated rather than left running in the background.
      deadline = Process.clock_gettime(Process::CLOCK_MONOTONIC) + BASH_TIMEOUT_SECONDS
      until wait_thr.join(0.1)
        next if Process.clock_gettime(Process::CLOCK_MONOTONIC) < deadline

        begin
          Process.kill("-TERM", wait_thr.pid)
        rescue Errno::ESRCH
        end
        unless wait_thr.join(2)
          begin
            Process.kill("-KILL", wait_thr.pid)
          rescue Errno::ESRCH
          end
        end
        wait_thr.join(5)
        reader.join(1) || reader.kill
        stdout_and_stderr.close rescue nil
        return ["command timed out after #{BASH_TIMEOUT_SECONDS}s", true]
      end
      status = wait_thr.value
      output = reader.value.strip
      stdout_and_stderr.close
      output = "(no output)" if output.empty?
      if output.length > TOOL_RESULT_MAX_CHARS
        output = "#{output[0, TOOL_RESULT_MAX_CHARS]}\n(truncated at #{TOOL_RESULT_MAX_CHARS} chars)"
      end
      output = "(exit code #{status.exitstatus})\n#{output}" unless status.success?
      [output, !status.success?]
    rescue Errno::ENOENT => e
      return ["bash error: #{e.message}", true]
    end
  end

  # Execute one bash tool call requested by the model.
  def handle_bash_block(block)
    input = parse_tool_input(block.input)
    return ["Shell restarted.", false] if input["restart"] == true

    command = input["command"]
    return ["bash error: no command was provided.", true] unless command.is_a?(String) && !command.empty?

    run_bash(command)
  end

  # Convert response content to request-shaped params. The streaming accumulator
  # returns tool_use input as a raw JSON string and includes response-only fields,
  # so reshape each block to the request schema before echoing it back.
  def assistant_content_param(content)
    content.map do |block|
      case block.type
      when :tool_use
        input = parse_tool_input(block.input)
        {type: "tool_use", id: block.id, name: block.name, input: input}
      when :text
        {type: "text", text: block.text}
      when :thinking
        {type: "thinking", thinking: block.thinking, signature: block.signature}
      when :redacted_thinking then {type: "redacted_thinking", data: block.data}
      else
        block.to_h
      end
    end
  end
  ```
</CodeGroup>

## Run one subagent

Each workflow subtask becomes its own small agent loop with the bash tool, running at the same effort as the main loop. A per-request timeout bounds each API call so a dropped connection degrades one subagent instead of stalling the whole run.

<CodeGroup>
  ```python Python
  def run_subagent(model: str, prompt: str) -> str:
      """One subagent: a small nested agent loop with the bash tool plus report_findings.
      Subagents inherit the main loop's effort level."""
      subagent_system = (
          "You are one agent in a larger parallel fan-out, assigned a single subtask. "
          "Investigate it directly, using bash to check facts rather than guessing, and finish "
          "by calling report_findings exactly once. Return findings, not narration."
      )
      messages = [{"role": "user", "content": prompt}]
      for _ in range(MAX_SUBAGENT_TURNS):
          with client.messages.stream(
              model=model,
              max_tokens=64000,
              system=subagent_system,
              thinking={"type": "adaptive"},
              output_config={"effort": EFFORT},
              tools=[BASH_TOOL, REPORT_TOOL],
              messages=messages,
              timeout=REQUEST_TIMEOUT_SECONDS,
          ) as stream:
              response = stream.get_final_message()
          messages.append({"role": "assistant", "content": response.content})
          if response.stop_reason == "pause_turn":
              continue
          if response.stop_reason != "tool_use":
              text = "".join(block.text for block in response.content if block.type == "text")
              if response.stop_reason == "max_tokens":
                  text += "\n\n(warning: subagent response was truncated at max_tokens)"
              return text
          tool_results = []
          report = None
          for block in response.content:
              if block.type != "tool_use":
                  continue
              if block.name == "report_findings":
                  report = json.dumps(block.input, indent=2)
                  output, is_error = "Findings recorded.", False
              elif block.name == "bash":
                  output, is_error = handle_bash_block(block)
              else:
                  output, is_error = f"unknown tool: {block.name}", True
              tool_results.append(
                  {
                      "type": "tool_result",
                      "tool_use_id": block.id,
                      "content": output,
                      "is_error": is_error,
                  }
              )
          if report is not None:
              return report
          messages.append({"role": "user", "content": tool_results})
      return "(subagent hit the turn limit before finishing)"
  ```

  ```typescript TypeScript
  // One subagent: a small nested agent loop with the bash tool plus report_findings.
  // Subagents inherit the main loop's effort level.
  async function runSubagent(model: string, prompt: string): Promise<string> {
    const subagentSystem =
      "You are one agent in a larger parallel fan-out, assigned a single subtask. " +
      "Investigate it directly, using bash to check facts rather than guessing, and finish " +
      "by calling report_findings exactly once. Return findings, not narration.";
    const messages: Anthropic.MessageParam[] = [{ role: "user", content: prompt }];
    for (let turn = 0; turn < MAX_SUBAGENT_TURNS; turn++) {
      const response = await client.messages
        .stream(
          {
            model,
            max_tokens: 64000,
            system: subagentSystem,
            thinking: { type: "adaptive" },
            output_config: { effort: EFFORT },
            tools: [BASH_TOOL, REPORT_TOOL],
            messages,
          },
          { signal: AbortSignal.timeout(REQUEST_TIMEOUT_SECONDS * 1000) },
        )
        .finalMessage();
      messages.push({ role: "assistant", content: response.content });
      if (response.stop_reason === "pause_turn") {
        continue;
      }
      if (response.stop_reason !== "tool_use") {
        let text = response.content
          .filter((block): block is Anthropic.TextBlock => block.type === "text")
          .map((block) => block.text)
          .join("");
        if (response.stop_reason === "max_tokens") {
          text += "\n\n(warning: subagent response was truncated at max_tokens)";
        }
        return text;
      }
      const toolResults: Anthropic.ToolResultBlockParam[] = [];
      let report: string | null = null;
      for (const block of response.content) {
        if (block.type !== "tool_use") {
          continue;
        }
        let output: string;
        let isError: boolean;
        if (block.name === "report_findings") {
          report = JSON.stringify(block.input, null, 2);
          output = "Findings recorded.";
          isError = false;
        } else if (block.name === "bash") {
          ({ output, isError } = await handleBashBlock(block));
        } else {
          output = `unknown tool: ${block.name}`;
          isError = true;
        }
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: output,
          is_error: isError,
        });
      }
      if (report !== null) {
        return report;
      }
      messages.push({ role: "user", content: toolResults });
    }
    return "(subagent hit the turn limit before finishing)";
  }
  ```

  ```csharp C#
  // One subagent: a small nested agent loop with the bash tool plus report_findings.
  // Subagents inherit the main loop's effort level.
  async Task<string> RunSubagent(string prompt)
  {
      const string subagentSystem =
          "You are one agent in a larger parallel fan-out, assigned a single subtask. "
          + "Investigate it directly, using bash to check facts rather than guessing, and finish "
          + "by calling report_findings exactly once. Return findings, not narration.";
      List<MessageParam> messages = [new() { Role = Role.User, Content = prompt }];
      for (var turn = 0; turn < maxSubagentTurns; turn++)
      {
          using var deadline = new CancellationTokenSource(TimeSpan.FromSeconds(requestTimeoutSeconds));
          var response = await client.Messages.Create(new MessageCreateParams
          {
              Model = model,
              MaxTokens = requestMaxTokens,
              System = subagentSystem,
              Thinking = new ThinkingConfigAdaptive(),
              OutputConfig = new OutputConfig { Effort = effort },
              Tools = [bashTool, reportTool],
              Messages = messages,
          }, cancellationToken: deadline.Token);
          messages.Add(new()
          {
              Role = Role.Assistant,
              Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
          });
          if (response.StopReason == StopReason.PauseTurn)
          {
              continue;
          }
          if (response.StopReason != StopReason.ToolUse)
          {
              var text = string.Concat(
                  response.Content.Select(block => block.TryPickText(out var textBlock) ? textBlock.Text : ""));
              if (response.StopReason == StopReason.MaxTokens)
              {
                  text += "\n\n(warning: subagent response was truncated at max_tokens)";
              }
              return text;
          }
          List<ContentBlockParam> toolResults = [];
          string? report = null;
          foreach (var block in response.Content)
          {
              if (!block.TryPickToolUse(out var toolUse))
              {
                  continue;
              }
              string output;
              bool isError;
              if (toolUse.Name == "report_findings")
              {
                  report = JsonSerializer.Serialize(
                      toolUse.Input, new JsonSerializerOptions { WriteIndented = true });
                  output = "Findings recorded.";
                  isError = false;
              }
              else if (toolUse.Name == "bash")
              {
                  (output, isError) = await HandleBashBlock(toolUse);
              }
              else
              {
                  output = $"unknown tool: {toolUse.Name}";
                  isError = true;
              }
              toolResults.Add(new ToolResultBlockParam(toolUse.ID) { Content = output, IsError = isError });
          }
          if (report is not null)
          {
              return report;
          }
          messages.Add(new() { Role = Role.User, Content = toolResults });
      }
      return "(subagent hit the turn limit before finishing)";
  }
  ```

  ```go Go
  // runSubagent runs one subagent: a small nested agent loop with the bash tool plus
  // report_findings. Subagents inherit the main loop's effort level.
  func runSubagent(ctx context.Context, model string, prompt string) (string, error) {
  	subagentSystem := "You are one agent in a larger parallel fan-out, assigned a single subtask. " +
  		"Investigate it directly, using bash to check facts rather than guessing, and finish " +
  		"by calling report_findings exactly once. Return findings, not narration."
  	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(prompt))}
  	for range maxSubagentTurns {
  		var response anthropic.Message
  		err := func() error {
  			ctx, cancel := context.WithTimeout(ctx, requestTimeoutSeconds*time.Second)
  			defer cancel()
  			stream := client.Messages.NewStreaming(ctx, anthropic.MessageNewParams{
  				Model:        model,
  				MaxTokens:    64000,
  				System:       []anthropic.TextBlockParam{{Text: subagentSystem}},
  				Thinking:     anthropic.ThinkingConfigParamUnion{OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{}},
  				OutputConfig: anthropic.OutputConfigParam{Effort: effort},
  				Tools:        []anthropic.ToolUnionParam{bashTool, reportTool},
  				Messages:     messages,
  			})
  			defer stream.Close()
  			for stream.Next() {
  				if err := response.Accumulate(stream.Current()); err != nil {
  					return err
  				}
  			}
  			return stream.Err()
  		}()
  		if err != nil {
  			return "", err
  		}
  		messages = append(messages, response.ToParam())
  		if response.StopReason == anthropic.StopReasonPauseTurn {
  			continue
  		}
  		if response.StopReason != anthropic.StopReasonToolUse {
  			var text strings.Builder
  			for _, block := range response.Content {
  				if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  					text.WriteString(textBlock.Text)
  				}
  			}
  			if response.StopReason == anthropic.StopReasonMaxTokens {
  				text.WriteString("\n\n(warning: subagent response was truncated at max_tokens)")
  			}
  			return text.String(), nil
  		}
  		var toolResults []anthropic.ContentBlockParamUnion
  		var report string
  		var reportRecorded bool
  		for _, block := range response.Content {
  			toolUse, ok := block.AsAny().(anthropic.ToolUseBlock)
  			if !ok {
  				continue
  			}
  			var output string
  			var isError bool
  			switch toolUse.Name {
  			case "report_findings":
  				report = string(toolUse.Input)
  				var pretty bytes.Buffer
  				if err := json.Indent(&pretty, toolUse.Input, "", "  "); err == nil {
  					report = pretty.String()
  				}
  				reportRecorded = true
  				output = "Findings recorded."
  			case "bash":
  				output, isError = handleBashBlock(ctx, toolUse)
  			default:
  				output, isError = fmt.Sprintf("unknown tool: %s", toolUse.Name), true
  			}
  			toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, output, isError))
  		}
  		if reportRecorded {
  			return report, nil
  		}
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))
  	}
  	return "(subagent hit the turn limit before finishing)", nil
  }

  ```

  ```java Java
  // One subagent: a small nested agent loop with the bash tool plus report_findings.
  // Subagents inherit the main loop's effort level.
  String runSubagent(String model, String prompt) throws InterruptedException {
      String subagentSystem = "You are one agent in a larger parallel fan-out, assigned a single subtask. "
              + "Investigate it directly, using bash to check facts rather than guessing, and finish "
              + "by calling report_findings exactly once. Return findings, not narration.";
      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder().role(MessageParam.Role.USER).content(prompt).build());
      for (int turn = 0; turn < MAX_SUBAGENT_TURNS; turn++) {
          MessageCreateParams params = MessageCreateParams.builder()
                  .model(model)
                  .maxTokens(64000L)
                  .system(subagentSystem)
                  .thinking(ThinkingConfigAdaptive.builder().build())
                  .outputConfig(OutputConfig.builder().effort(EFFORT).build())
                  .addTool(BASH_TOOL)
                  .addTool(REPORT_TOOL)
                  .messages(messages)
                  .build();
          MessageAccumulator accumulator = MessageAccumulator.create();
          try (var stream = client.messages().createStreaming(params, REQUEST_OPTIONS)) {
              stream.stream().forEach(accumulator::accumulate);
          }
          Message response = accumulator.message();
          messages.add(response.toParam());
          StopReason stopReason = response.stopReason().orElse(null);
          if (StopReason.PAUSE_TURN.equals(stopReason)) {
              continue;
          }
          if (!StopReason.TOOL_USE.equals(stopReason)) {
              String text = response.content().stream()
                      .flatMap(block -> block.text().stream())
                      .map(TextBlock::text)
                      .collect(Collectors.joining());
              if (StopReason.MAX_TOKENS.equals(stopReason)) {
                  text += "\n\n(warning: subagent response was truncated at max_tokens)";
              }
              return text;
          }
          List<ContentBlockParam> toolResults = new ArrayList<>();
          String report = null;
          for (ContentBlock block : response.content()) {
              if (block.toolUse().isEmpty()) {
                  continue;
              }
              ToolUseBlock toolUse = block.toolUse().get();
              ToolOutput result;
              if (toolUse.name().equals("report_findings")) {
                  report = toolUse._input().convert(JsonNode.class).toPrettyString();
                  result = new ToolOutput("Findings recorded.", false);
              } else if (toolUse.name().equals("bash")) {
                  result = handleBashBlock(toolUse);
              } else {
                  result = new ToolOutput("unknown tool: " + toolUse.name(), true);
              }
              toolResults.add(ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()
                      .toolUseId(toolUse.id())
                      .content(result.output())
                      .isError(result.isError())
                      .build()));
          }
          if (report != null) {
              return report;
          }
          messages.add(MessageParam.builder()
                  .role(MessageParam.Role.USER)
                  .contentOfBlockParams(toolResults)
                  .build());
      }
      return "(subagent hit the turn limit before finishing)";
  }
  ```

  ```php PHP
  /**
   * Consume a message stream and assemble the final assistant turn from its events:
   * the full content-block list plus the stop reason, equivalent to what a
   * non-streaming create call returns.
   */
  function drainMessageStream(iterable $events): array
  {
      $stringValue = fn ($value) => $value instanceof BackedEnum ? $value->value : $value;
      $blocks = [];
      $jsonBuffers = [];
      $stopReason = null;
      foreach ($events as $event) {
          $type = $stringValue($event->type);
          if ($type === 'content_block_start') {
              $blocks[$event->index] = $event->contentBlock;
              $jsonBuffers[$event->index] = '';
          } elseif ($type === 'content_block_delta') {
              $block = $blocks[$event->index];
              $delta = $event->delta;
              $deltaType = $stringValue($delta->type);
              if ($deltaType === 'text_delta') {
                  $blocks[$event->index] = $block->withText($block->text . $delta->text);
              } elseif ($deltaType === 'input_json_delta') {
                  $jsonBuffers[$event->index] .= $delta->partialJSON;
              } elseif ($deltaType === 'thinking_delta') {
                  $blocks[$event->index] = $block->withThinking($block->thinking . $delta->thinking);
              } elseif ($deltaType === 'signature_delta') {
                  $blocks[$event->index] = $block->withSignature($delta->signature);
              }
          } elseif ($type === 'message_delta') {
              $stopReason = $stringValue($event->delta->stopReason);
          }
      }
      foreach ($jsonBuffers as $index => $buffer) {
          if ($buffer !== '' && $blocks[$index] instanceof ToolUseBlock) {
              $decoded = json_decode($buffer, true);
              $blocks[$index] = $blocks[$index]->withInput(is_array($decoded) ? $decoded : []);
          }
      }
      return [array_values($blocks), $stopReason];
  }

  /**
   * One subagent: a small nested agent loop with the bash tool plus report_findings.
   * Subagents inherit the main loop's effort level.
   */
  function runSubagent(Client $client, string $model, string $prompt): string
  {
      $subagentSystem =
          'You are one agent in a larger parallel fan-out, assigned a single subtask. '
          . 'Investigate it directly, using bash to check facts rather than guessing, and finish '
          . 'by calling report_findings exactly once. Return findings, not narration.';
      $messages = [['role' => 'user', 'content' => $prompt]];
      for ($turn = 0; $turn < MAX_SUBAGENT_TURNS; $turn++) {
          $stream = $client->messages->createStream(
              model: $model,
              maxTokens: 64000,
              system: $subagentSystem,
              thinking: ['type' => 'adaptive'],
              outputConfig: ['effort' => EFFORT],
              tools: [BASH_TOOL, REPORT_TOOL],
              messages: $messages,
              requestOptions: ['timeout' => REQUEST_TIMEOUT_SECONDS],
          );
          [$content, $stopReason] = drainMessageStream($stream);
          $messages[] = ['role' => 'assistant', 'content' => $content];
          if ($stopReason === 'pause_turn') {
              continue;
          }
          if ($stopReason !== 'tool_use') {
              $text = '';
              foreach ($content as $block) {
                  if ($block instanceof TextBlock) {
                      $text .= $block->text;
                  }
              }
              if ($stopReason === 'max_tokens') {
                  $text .= "\n\n(warning: subagent response was truncated at max_tokens)";
              }
              return $text;
          }
          $report = null;
          $toolResults = [];
          foreach ($content as $block) {
              if (!$block instanceof ToolUseBlock) {
                  continue;
              }
              if ($block->name === 'report_findings') {
                  $report = json_encode($block->input, JSON_PRETTY_PRINT);
                  $output = 'Findings recorded.';
                  $isError = false;
              } elseif ($block->name === 'bash') {
                  [$output, $isError] = handleBashBlock($block);
              } else {
                  $output = "unknown tool: {$block->name}";
                  $isError = true;
              }
              $toolResults[] = [
                  'type' => 'tool_result',
                  'tool_use_id' => $block->id,
                  'content' => $output,
                  'is_error' => $isError,
              ];
          }
          if ($report !== null) {
              return $report;
          }
          $messages[] = ['role' => 'user', 'content' => $toolResults];
      }
      return '(subagent hit the turn limit before finishing)';
  }
  ```

  ```ruby Ruby
  # One subagent: a small nested agent loop with the bash tool plus report_findings.
  # Subagents inherit the main loop's effort level.
  def run_subagent(model, prompt)
    subagent_system =
      "You are one agent in a larger parallel fan-out, assigned a single subtask. " \
      "Investigate it directly, using bash to check facts rather than guessing, and finish " \
      "by calling report_findings exactly once. Return findings, not narration."
    messages = [{role: "user", content: prompt}]
    MAX_SUBAGENT_TURNS.times do
      stream = CLIENT.messages.stream(
        model: model,
        max_tokens: 64_000,
        system_: subagent_system,
        thinking: {type: :adaptive},
        output_config: {effort: EFFORT},
        tools: [BASH_TOOL, REPORT_TOOL],
        messages: messages,
        request_options: {timeout: REQUEST_TIMEOUT_SECONDS}
      )
      response = stream.accumulated_message
      messages << {role: "assistant", content: assistant_content_param(response.content)}
      next if response.stop_reason == :pause_turn

      unless response.stop_reason == :tool_use
        text = response.content.select { |block| block.type == :text }.map(&:text).join
        text += "\n\n(warning: subagent response was truncated at max_tokens)" if response.stop_reason == :max_tokens
        return text
      end

      report = nil
      tool_results = []
      response.content.each do |block|
        next unless block.type == :tool_use

        input = parse_tool_input(block.input)
        case block.name
        when "report_findings"
          report = JSON.pretty_generate(input)
          output, is_error = "Findings recorded.", false
        when "bash"
          output, is_error = handle_bash_block(block)
        else
          output, is_error = "unknown tool: #{block.name}", true
        end
        tool_results << {
          type: "tool_result",
          tool_use_id: block.id,
          content: output,
          is_error: is_error
        }
      end
      return report unless report.nil?

      messages << {role: "user", content: tool_results}
    end
    "(subagent hit the turn limit before finishing)"
  end
  ```
</CodeGroup>

## Journal results so reruns resume

A fan-out that spawns dozens of subagents is expensive to restart from scratch. A small content-addressed journal makes it idempotent: before dispatching a subagent, look up the SHA-256 of its prompt in a local JSON file, and return the recorded result if one exists. Interrupt the run, rerun it, and only the subtasks that never finished are recomputed. The journal deduplicates across runs, not within a single fan-out wave; delete the journal file to start fresh.

<CodeGroup>
  ```python Python
  _journal_lock = threading.Lock()


  def _load_journal() -> dict:
      try:
          with open(JOURNAL_PATH) as file:
              return json.load(file) or {}
      except (OSError, json.JSONDecodeError):
          return {}


  def journaled(prompt: str, compute) -> str:
      """Return a cached result for this exact prompt, or compute and persist it. This
      makes the fan-out resumable: interrupt the run, rerun it, and only the subtasks
      that never finished are recomputed. Delete the journal file to start fresh."""
      key = hashlib.sha256(prompt.encode()).hexdigest()
      cached = _load_journal().get(key)
      if cached is not None:
          print(f"[journal] cache hit for {key[:12]}", file=sys.stderr)
          return cached
      result = compute()
      try:
          with _journal_lock:  # fan-out writes from many threads
              journal = _load_journal()
              journal[key] = result
              temp = f"{JOURNAL_PATH}.tmp"
              with open(temp, "w") as file:
                  json.dump(journal, file)
              os.replace(temp, JOURNAL_PATH)  # atomic on POSIX and Windows
      except OSError as error:  # the journal is best-effort; never discard a computed result
          print(f"[journal] write failed: {error}", file=sys.stderr)
      return result
  ```

  ```typescript TypeScript
  let journalWriteChain = Promise.resolve();

  async function loadJournal(): Promise<Record<string, string>> {
    try {
      return JSON.parse(await readFile(JOURNAL_PATH, "utf8")) ?? {};
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") {
        console.error(`[journal] discarding unreadable journal: ${error}`);
      }
      return {};
    }
  }

  // Return a cached result for this exact prompt, or compute and persist it. This
  // makes the fan-out resumable: interrupt the run, rerun it, and only the subtasks
  // that never finished are recomputed. Delete the journal file to start fresh.
  async function journaled(prompt: string, compute: () => Promise<string>): Promise<string> {
    const key = createHash("sha256").update(prompt).digest("hex");
    const cached = (await loadJournal())[key];
    if (cached !== undefined) {
      console.error(`[journal] cache hit for ${key.slice(0, 12)}`);
      return cached;
    }
    const result = await compute();
    // Chain writes so concurrent subagents do not clobber each other's entries.
    // The chain is kept settled so one failed write does not poison later ones.
    await (journalWriteChain = journalWriteChain
      .then(async () => {
        const journal = await loadJournal();
        journal[key] = result;
        const temp = `${JOURNAL_PATH}.tmp`;
        await writeFile(temp, JSON.stringify(journal));
        await rename(temp, JOURNAL_PATH);
      })
      .catch((error) => console.error(`[journal] write failed: ${error}`)));
    return result;
  }
  ```

  ```csharp C#
  SemaphoreSlim journalLock = new(1, 1);

  async Task<Dictionary<string, string>> LoadJournal()
  {
      try
      {
          return JsonSerializer.Deserialize<Dictionary<string, string>>(await File.ReadAllTextAsync(journalPath)) ?? [];
      }
      catch (Exception error) when (error is IOException or UnauthorizedAccessException or JsonException)
      {
          return [];
      }
  }

  // Return a cached result for this exact prompt, or compute and persist it. This
  // makes the fan-out resumable: interrupt the run, rerun it, and only the subtasks
  // that never finished are recomputed. Delete the journal file to start fresh.
  async Task<string> Journaled(string prompt, Func<Task<string>> compute)
  {
      var key = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(prompt))).ToLowerInvariant();
      if ((await LoadJournal()).TryGetValue(key, out var cached))
      {
          Console.Error.WriteLine($"[journal] cache hit for {key[..12]}");
          return cached;
      }
      var result = await compute();
      await journalLock.WaitAsync(); // fan-out writes from many tasks
      try
      {
          var journal = await LoadJournal();
          journal[key] = result;
          var temp = journalPath + ".tmp";
          await File.WriteAllTextAsync(temp, JsonSerializer.Serialize(journal));
          File.Move(temp, journalPath, overwrite: true);
      }
      catch (Exception error) when (error is IOException or UnauthorizedAccessException or NotSupportedException)
      {
          // The journal is best-effort; never discard a computed result.
          Console.Error.WriteLine($"[journal] write failed: {error.Message}");
      }
      finally
      {
          journalLock.Release();
      }
      return result;
  }
  ```

  ```go Go
  var journalMutex sync.Mutex

  func loadJournal() map[string]string {
  	data, err := os.ReadFile(journalPath)
  	if err != nil {
  		return map[string]string{}
  	}
  	var journal map[string]string
  	if err := json.Unmarshal(data, &journal); err != nil || journal == nil {
  		return map[string]string{}
  	}
  	return journal
  }

  // journaled returns a cached result for this exact prompt, or computes and persists
  // it. This makes the fan-out resumable: interrupt the run, rerun it, and only the
  // subtasks that never finished are recomputed. Delete the journal file to start fresh.
  func journaled(prompt string, compute func() (string, error)) (string, error) {
  	sum := sha256.Sum256([]byte(prompt))
  	key := hex.EncodeToString(sum[:])
  	if cached, ok := loadJournal()[key]; ok {
  		fmt.Fprintf(os.Stderr, "[journal] cache hit for %s\n", key[:12])
  		return cached, nil
  	}
  	result, err := compute()
  	if err != nil {
  		return "", err
  	}
  	journalMutex.Lock() // fan-out writes from many goroutines
  	defer journalMutex.Unlock()
  	journal := loadJournal()
  	journal[key] = result
  	data, _ := json.Marshal(journal)
  	temp := journalPath + ".tmp"
  	if err := os.WriteFile(temp, data, 0o644); err != nil {
  		fmt.Fprintf(os.Stderr, "[journal] write failed: %s\n", err)
  	} else if err := os.Rename(temp, journalPath); err != nil {
  		fmt.Fprintf(os.Stderr, "[journal] write failed: %s\n", err)
  		_ = os.Remove(temp)
  	}
  	return result, nil
  }

  ```

  ```java Java
  static final ObjectMapper JOURNAL_MAPPER = new ObjectMapper();
  static final ReentrantLock JOURNAL_LOCK = new ReentrantLock();

  Map<String, String> loadJournal() {
      try {
          return Objects.requireNonNullElseGet(
                  JOURNAL_MAPPER.readValue(Files.readString(JOURNAL_PATH), new TypeReference<HashMap<String, String>>() {}),
                  HashMap::new);
      } catch (IOException error) {
          return new HashMap<>();
      }
  }

  // Return a cached result for this exact prompt, or compute and persist it. This
  // makes the fan-out resumable: interrupt the run, rerun it, and only the subtasks
  // that never finished are recomputed. Delete the journal file to start fresh.
  String journaled(String prompt, Callable<String> compute) throws Exception {
      var digest = MessageDigest.getInstance("SHA-256").digest(prompt.getBytes(StandardCharsets.UTF_8));
      String key = HexFormat.of().formatHex(digest);
      String cached = loadJournal().get(key);
      if (cached != null) {
          System.err.println("[journal] cache hit for " + key.substring(0, 12));
          return cached;
      }
      String result = compute.call();
      JOURNAL_LOCK.lock(); // fan-out writes from many threads
      try {
          Map<String, String> journal = loadJournal();
          journal.put(key, result);
          Path temp = JOURNAL_PATH.resolveSibling(JOURNAL_PATH.getFileName() + ".tmp");
          Files.writeString(temp, JOURNAL_MAPPER.writeValueAsString(journal));
          Files.move(temp, JOURNAL_PATH, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
      } catch (IOException error) {
          // The journal is best-effort; never discard a computed result.
          System.err.println("[journal] write failed: " + error);
      } finally {
          JOURNAL_LOCK.unlock();
      }
      return result;
  }
  ```

  ```php PHP
  function loadJournal(): array
  {
      $raw = @file_get_contents(JOURNAL_PATH);
      if ($raw === false) {
          return [];
      }
      $decoded = json_decode($raw, true);
      return is_array($decoded) ? $decoded : [];
  }

  /**
   * Return a cached result for this exact prompt, or compute and persist it. This
   * makes the fan-out resumable: interrupt the run, rerun it, and only the subtasks
   * that never finished are recomputed. Delete the journal file to start fresh.
   */
  function journaled(string $prompt, callable $compute): string
  {
      $key = hash('sha256', $prompt);
      $journal = loadJournal();
      if (array_key_exists($key, $journal)) {
          fwrite(STDERR, '[journal] cache hit for ' . substr($key, 0, 12) . "\n");
          return $journal[$key];
      }
      $result = $compute();
      $journal = loadJournal();
      $journal[$key] = $result;
      $temp = JOURNAL_PATH . '.tmp';
      $encoded = json_encode($journal, JSON_INVALID_UTF8_SUBSTITUTE);
      if ($encoded === false || @file_put_contents($temp, $encoded) === false || !@rename($temp, JOURNAL_PATH)) {
          fwrite(STDERR, '[journal] write failed: ' . (error_get_last()['message'] ?? json_last_error_msg()) . "\n");
          @unlink($temp);
      }
      return $result;
  }
  ```

  ```ruby Ruby
  JOURNAL_LOCK = Mutex.new

  def load_journal
    JSON.parse(File.read(JOURNAL_PATH)) || {}
  rescue SystemCallError, JSON::ParserError
    {}
  end

  # Return a cached result for this exact prompt, or compute and persist it. This
  # makes the fan-out resumable: interrupt the run, rerun it, and only the subtasks
  # that never finished are recomputed. Delete the journal file to start fresh.
  def journaled(prompt)
    key = Digest::SHA256.hexdigest(prompt)
    cached = load_journal[key]
    unless cached.nil?
      warn "[journal] cache hit for #{key[0, 12]}"
      return cached
    end
    result = yield
    begin
      JOURNAL_LOCK.synchronize do # fan-out writes from many threads
        journal = load_journal
        journal[key] = result
        temp = "#{JOURNAL_PATH}.tmp"
        File.write(temp, JSON.generate(journal))
        File.rename(temp, JOURNAL_PATH)
      end
    rescue SystemCallError => error # the journal is best-effort; never discard a computed result
      warn "[journal] write failed: #{error}"
    end
    result
  end
  ```
</CodeGroup>

## Fan out, then verify

The fan-out accepts up to `MAX_TOTAL_SUBTASKS` prompts, runs them through the journal with at most `MAX_CONCURRENT` in flight (sequential in the PHP port), and isolates failures so one broken subagent degrades to an error string instead of ending the run. Once the first wave finishes, a second wave reuses the same subagent path to try to refute each result: every verifier re-derives the claims from the source, defaulting to refuted when uncertain. Both the original result and its verdict are returned to the orchestrator so it can weigh them together.

<CodeGroup>
  ```python Python
  def normalize_subtasks(raw) -> list[str]:
      """Accept the subtasks input in whatever shape the model emits: an array, the array
      JSON-encoded as a single string, or a newline-separated list."""
      if isinstance(raw, str):
          try:
              raw = json.loads(raw)
          except json.JSONDecodeError:
              raw = raw.splitlines() if "\n" in raw else [raw]
      if not isinstance(raw, list):
          return []
      return [task.strip() for task in raw if isinstance(task, str) and task.strip()]


  def verify_prompt_for(subtask: str, result: str) -> str:
      return (
          "Adversarially verify the subagent result below: try to REFUTE it. Re-derive the "
          "claims yourself with bash rather than trusting the result, and look for evidence "
          "that contradicts them. Default to refuted if uncertain. Call report_findings with "
          "summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command "
          "output that decided it.\n\n"
          f"Subtask: {subtask}\n\nResult to verify:\n{result}"
      )


  def run_workflow(model: str, raw_subtasks) -> tuple[str, bool]:
      """Run subtasks as parallel subagents, then run a second verification wave over
      the results, and return both. MAX_TOTAL_SUBTASKS bounds how many the model can
      queue; MAX_CONCURRENT bounds how many run at once."""
      all_subtasks = normalize_subtasks(raw_subtasks)
      subtasks = all_subtasks[:MAX_TOTAL_SUBTASKS]
      dropped = len(all_subtasks) - len(subtasks)
      if not subtasks:
          return "Workflow error: no usable subtasks were provided.", True
      print(f"[workflow] fanning out {len(subtasks)} agents", file=sys.stderr)

      def run_one(prompt: str) -> str:
          try:
              return journaled(prompt, lambda: run_subagent(model, prompt))
          except Exception as error:  # isolation boundary: one bad subagent should not end the run
              return f"(subagent failed: {type(error).__name__}: {error})"

      with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as pool:
          results = list(pool.map(run_one, subtasks))
          print(f"[workflow] verifying {len(results)} results", file=sys.stderr)
          verify_prompts = [verify_prompt_for(task, result) for task, result in zip(subtasks, results)]
          verdicts = list(pool.map(run_one, verify_prompts))

      joined = "\n\n".join(
          f"[agent {index + 1}: {task}]\n{result}\n\n[verify {index + 1}]\n{verdict}"
          for index, (task, result, verdict) in enumerate(zip(subtasks, results, verdicts))
      )
      if dropped > 0:
          joined = (
              f"(note: {dropped} subtasks beyond MAX_TOTAL_SUBTASKS={MAX_TOTAL_SUBTASKS} were not "
              "run; rerun them in a follow-up Workflow call)\n\n" + joined
          )
      return joined, False
  ```

  ```typescript TypeScript
  // Accept the subtasks input in whatever shape the model emits: an array, the array
  // JSON-encoded as a single string, or a newline-separated list.
  function normalizeSubtasks(raw: unknown): string[] {
    let value = raw;
    if (typeof raw === "string") {
      try {
        value = JSON.parse(raw);
      } catch {
        value = raw.includes("\n") ? raw.split("\n") : [raw];
      }
    }
    if (!Array.isArray(value)) {
      return [];
    }
    return value
      .filter((task): task is string => typeof task === "string")
      .map((task) => task.trim())
      .filter((task) => task.length > 0);
  }

  function verifyPromptFor(subtask: string, result: string): string {
    return (
      "Adversarially verify the subagent result below: try to REFUTE it. Re-derive the " +
      "claims yourself with bash rather than trusting the result, and look for evidence " +
      "that contradicts them. Default to refuted if uncertain. Call report_findings with " +
      "summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command " +
      "output that decided it.\n\n" +
      `Subtask: ${subtask}\n\nResult to verify:\n${result}`
    );
  }

  // Map with a concurrency limit: at most `limit` tasks are in flight at once.
  async function mapWithLimit<In, Out>(
    items: readonly In[],
    limit: number,
    task: (item: In) => Promise<Out>,
  ): Promise<Out[]> {
    const results = new Array<Out>(items.length);
    let cursor = 0;
    const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
      while (cursor < items.length) {
        const index = cursor++;
        results[index] = await task(items[index]);
      }
    });
    await Promise.all(workers);
    return results;
  }

  // Run subtasks as parallel subagents, then run a second verification wave over
  // the results, and return both. MAX_TOTAL_SUBTASKS bounds how many the model can
  // queue; MAX_CONCURRENT bounds how many run at once.
  async function runWorkflow(
    model: string,
    rawSubtasks: unknown,
  ): Promise<{ output: string; isError: boolean }> {
    const allSubtasks = normalizeSubtasks(rawSubtasks);
    const subtasks = allSubtasks.slice(0, MAX_TOTAL_SUBTASKS);
    const dropped = allSubtasks.length - subtasks.length;
    if (subtasks.length === 0) {
      return { output: "Workflow error: no usable subtasks were provided.", isError: true };
    }
    console.error(`[workflow] fanning out ${subtasks.length} agents`);

    const runOne = async (prompt: string): Promise<string> => {
      try {
        return await journaled(prompt, () => runSubagent(model, prompt));
      } catch (error) {
        // Isolation boundary: one bad subagent should not end the run.
        const reason = error instanceof Error ? `${error.name}: ${error.message}` : String(error);
        return `(subagent failed: ${reason})`;
      }
    };

    const results = await mapWithLimit(subtasks, MAX_CONCURRENT, runOne);
    console.error(`[workflow] verifying ${results.length} results`);
    const verifyPrompts = subtasks.map((task, index) => verifyPromptFor(task, results[index]));
    const verdicts = await mapWithLimit(verifyPrompts, MAX_CONCURRENT, runOne);

    let joined = subtasks
      .map(
        (task, index) =>
          `[agent ${index + 1}: ${task}]\n${results[index]}\n\n[verify ${index + 1}]\n${verdicts[index]}`,
      )
      .join("\n\n");
    if (dropped > 0) {
      joined =
        `(note: ${dropped} subtasks beyond MAX_TOTAL_SUBTASKS=${MAX_TOTAL_SUBTASKS} were not ` +
        "run; rerun them in a follow-up Workflow call)\n\n" +
        joined;
    }
    return { output: joined, isError: false };
  }
  ```

  ```csharp C#
  // Accept the subtasks input in whatever shape the model emits: an array, the array
  // JSON-encoded as a single string, or a newline-separated list.
  List<string> NormalizeSubtasks(JsonElement raw)
  {
      List<string> tasks = [];
      if (raw.ValueKind == JsonValueKind.Array)
      {
          tasks = raw.EnumerateArray()
              .Where(item => item.ValueKind == JsonValueKind.String)
              .Select(item => item.GetString()!)
              .ToList();
      }
      else if (raw.ValueKind == JsonValueKind.String)
      {
          var single = raw.GetString()!;
          try
          {
              tasks = JsonSerializer.Deserialize<List<string>>(single) ?? [];
          }
          catch (JsonException)
          {
              tasks = [.. single.Split('\n')];
          }
      }
      return tasks.Where(task => task != null).Select(task => task.Trim()).Where(task => task.Length > 0).ToList();
  }

  string VerifyPromptFor(string subtask, string result) =>
      "Adversarially verify the subagent result below: try to REFUTE it. Re-derive the "
      + "claims yourself with bash rather than trusting the result, and look for evidence "
      + "that contradicts them. Default to refuted if uncertain. Call report_findings with "
      + "summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command "
      + "output that decided it.\n\n"
      + $"Subtask: {subtask}\n\nResult to verify:\n{result}";

  // Run subtasks as parallel subagents, then run a second verification wave over
  // the results, and return both. maxTotalSubtasks bounds how many the model can
  // queue; maxConcurrent bounds how many run at once.
  async Task<(string Output, bool IsError)> RunWorkflow(JsonElement rawSubtasks)
  {
      var allSubtasks = NormalizeSubtasks(rawSubtasks);
      var subtasks = allSubtasks.Take(maxTotalSubtasks).ToList();
      var dropped = allSubtasks.Count - subtasks.Count;
      if (subtasks.Count == 0)
      {
          return ("Workflow error: no usable subtasks were provided.", true);
      }
      Console.Error.WriteLine($"[workflow] fanning out {subtasks.Count} agents");

      using SemaphoreSlim gate = new(maxConcurrent);
      async Task<string> RunOne(string prompt)
      {
          await gate.WaitAsync();
          try
          {
              return await Journaled(prompt, () => RunSubagent(prompt));
          }
          catch (Exception error)
          {
              // Isolation boundary: one bad subagent should not end the run.
              return $"(subagent failed: {error.GetType().Name}: {error.Message})";
          }
          finally
          {
              gate.Release();
          }
      }

      var results = await Task.WhenAll(subtasks.Select(RunOne));
      Console.Error.WriteLine($"[workflow] verifying {results.Length} results");
      var verifyPrompts = subtasks.Select((task, index) => VerifyPromptFor(task, results[index])).ToList();
      var verdicts = await Task.WhenAll(verifyPrompts.Select(RunOne));

      var joined = string.Join(
          "\n\n",
          subtasks.Select((task, index) =>
              $"[agent {index + 1}: {task}]\n{results[index]}\n\n[verify {index + 1}]\n{verdicts[index]}"));
      if (dropped > 0)
      {
          joined = $"(note: {dropped} subtasks beyond maxTotalSubtasks={maxTotalSubtasks} were not run; "
              + "rerun them in a follow-up Workflow call)\n\n" + joined;
      }
      return (joined, false);
  }
  ```

  ```go Go
  // normalizeSubtasks accepts the subtasks input in whatever shape the model emits: an
  // array, the array JSON-encoded as a single string, or a newline-separated list.
  func normalizeSubtasks(raw json.RawMessage) []string {
  	var tasks []string
  	if err := json.Unmarshal(raw, &tasks); err != nil {
  		var single string
  		if err := json.Unmarshal(raw, &single); err != nil {
  			return nil
  		}
  		if err := json.Unmarshal([]byte(single), &tasks); err != nil {
  			tasks = strings.Split(single, "\n")
  		}
  	}
  	cleaned := make([]string, 0, len(tasks))
  	for _, task := range tasks {
  		if trimmed := strings.TrimSpace(task); trimmed != "" {
  			cleaned = append(cleaned, trimmed)
  		}
  	}
  	return cleaned
  }

  func verifyPromptFor(subtask, result string) string {
  	return "Adversarially verify the subagent result below: try to REFUTE it. Re-derive the " +
  		"claims yourself with bash rather than trusting the result, and look for evidence " +
  		"that contradicts them. Default to refuted if uncertain. Call report_findings with " +
  		"summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command " +
  		"output that decided it.\n\n" +
  		"Subtask: " + subtask + "\n\nResult to verify:\n" + result
  }

  // mapWithLimit runs task over items with at most limit goroutines in flight.
  func mapWithLimit(items []string, limit int, task func(string) string) []string {
  	results := make([]string, len(items))
  	semaphore := make(chan struct{}, limit)
  	var waitGroup sync.WaitGroup
  	for index, item := range items {
  		waitGroup.Add(1)
  		semaphore <- struct{}{}
  		go func() {
  			defer waitGroup.Done()
  			defer func() { <-semaphore }()
  			results[index] = task(item)
  		}()
  	}
  	waitGroup.Wait()
  	return results
  }

  // runWorkflow runs subtasks as parallel subagents, then runs a second verification wave
  // over the results, and returns both. maxTotalSubtasks bounds how many the model can
  // queue; maxConcurrent bounds how many run at once.
  func runWorkflow(ctx context.Context, model string, rawSubtasks json.RawMessage) (string, bool) {
  	allSubtasks := normalizeSubtasks(rawSubtasks)
  	subtasks := allSubtasks
  	if len(subtasks) > maxTotalSubtasks {
  		subtasks = subtasks[:maxTotalSubtasks]
  	}
  	dropped := len(allSubtasks) - len(subtasks)
  	if len(subtasks) == 0 {
  		return "Workflow error: no usable subtasks were provided.", true
  	}
  	fmt.Fprintf(os.Stderr, "[workflow] fanning out %d agents\n", len(subtasks))

  	runOne := func(prompt string) string {
  		report, err := journaled(prompt, func() (string, error) { return runSubagent(ctx, model, prompt) })
  		if err != nil {
  			// Isolation boundary: one bad subagent should not end the run.
  			return fmt.Sprintf("(subagent failed: %s)", err)
  		}
  		return report
  	}

  	results := mapWithLimit(subtasks, maxConcurrent, runOne)
  	fmt.Fprintf(os.Stderr, "[workflow] verifying %d results\n", len(results))
  	verifyPrompts := make([]string, len(subtasks))
  	for index, task := range subtasks {
  		verifyPrompts[index] = verifyPromptFor(task, results[index])
  	}
  	verdicts := mapWithLimit(verifyPrompts, maxConcurrent, runOne)

  	sections := make([]string, len(subtasks))
  	for index, task := range subtasks {
  		sections[index] = fmt.Sprintf("[agent %d: %s]\n%s\n\n[verify %d]\n%s",
  			index+1, task, results[index], index+1, verdicts[index])
  	}
  	joined := strings.Join(sections, "\n\n")
  	if dropped > 0 {
  		joined = fmt.Sprintf("(note: %d subtasks beyond maxTotalSubtasks=%d were not run; "+
  			"rerun them in a follow-up Workflow call)\n\n", dropped, maxTotalSubtasks) + joined
  	}
  	return joined, false
  }

  ```

  ```java Java
  // Accept the subtasks input in whatever shape the model emits: an array, the array
  // JSON-encoded as a single string, or a newline-separated list.
  List<String> normalizeSubtasks(JsonValue raw) {
      List<String> tasks = new ArrayList<>();
      if (raw.asArray().isPresent()) {
          for (JsonValue item : (List<JsonValue>) raw.asArray().get()) {
              tasks.add(item.asString().isPresent() ? item.asStringOrThrow() : item.toString());
          }
      } else if (raw.asString().isPresent()) {
          String single = raw.asStringOrThrow();
          try {
              String[] parsed = new ObjectMapper().readValue(single, String[].class);
              if (parsed != null) {
                  for (String task : parsed) {
                      tasks.add(task);
                  }
              }
          } catch (JsonProcessingException error) {
              for (String task : single.split("\n")) {
                  tasks.add(task);
              }
          }
      }
      return tasks.stream()
              .filter(task -> task != null)
              .map(String::trim)
              .filter(task -> !task.isEmpty())
              .toList();
  }

  String verifyPromptFor(String subtask, String result) {
      return "Adversarially verify the subagent result below: try to REFUTE it. Re-derive the "
              + "claims yourself with bash rather than trusting the result, and look for evidence "
              + "that contradicts them. Default to refuted if uncertain. Call report_findings with "
              + "summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command "
              + "output that decided it.\n\n"
              + "Subtask: " + subtask + "\n\nResult to verify:\n" + result;
  }

  List<String> runAll(ExecutorService pool, List<String> prompts, String model) throws InterruptedException {
      List<Callable<String>> jobs = prompts.stream()
              .<Callable<String>>map(prompt -> () -> journaled(prompt, () -> runSubagent(model, prompt)))
              .toList();
      List<String> results = new ArrayList<>();
      for (Future<String> future : pool.invokeAll(jobs)) {
          try {
              results.add(future.get());
          } catch (ExecutionException | CancellationException error) {
              // Isolation boundary: one bad subagent should not end the run.
              Throwable cause = error.getCause() != null ? error.getCause() : error;
              results.add("(subagent failed: " + cause + ")");
          }
      }
      return results;
  }

  // Run subtasks as parallel subagents, then run a second verification wave over
  // the results, and return both. MAX_TOTAL_SUBTASKS bounds how many the model can
  // queue; MAX_CONCURRENT bounds how many run at once.
  ToolOutput runWorkflow(String model, JsonValue rawSubtasks) throws InterruptedException {
      List<String> allSubtasks = normalizeSubtasks(rawSubtasks);
      List<String> subtasks = allSubtasks.stream().limit(MAX_TOTAL_SUBTASKS).toList();
      int dropped = allSubtasks.size() - subtasks.size();
      if (subtasks.isEmpty()) {
          return new ToolOutput("Workflow error: no usable subtasks were provided.", true);
      }
      System.err.println("[workflow] fanning out " + subtasks.size() + " agents");

      List<String> results;
      List<String> verdicts;
      try (ExecutorService pool = Executors.newFixedThreadPool(MAX_CONCURRENT, Thread.ofVirtual().factory())) {
          results = runAll(pool, subtasks, model);
          System.err.println("[workflow] verifying " + results.size() + " results");
          List<String> verifyPrompts = IntStream.range(0, subtasks.size())
                  .mapToObj(index -> verifyPromptFor(subtasks.get(index), results.get(index)))
                  .toList();
          verdicts = runAll(pool, verifyPrompts, model);
      }
      String joined = IntStream.range(0, subtasks.size())
              .mapToObj(index -> "[agent " + (index + 1) + ": " + subtasks.get(index) + "]\n" + results.get(index)
                      + "\n\n[verify " + (index + 1) + "]\n" + verdicts.get(index))
              .collect(Collectors.joining("\n\n"));
      if (dropped > 0) {
          joined = "(note: " + dropped + " subtasks beyond MAX_TOTAL_SUBTASKS=" + MAX_TOTAL_SUBTASKS
                  + " were not run; rerun them in a follow-up Workflow call)\n\n" + joined;
      }
      return new ToolOutput(joined, false);
  }
  ```

  ```php PHP
  /**
   * Accept the subtasks input in whatever shape the model emits: an array, the array
   * JSON-encoded as a single string, or a newline-separated list.
   */
  function normalizeSubtasks(mixed $raw): array
  {
      if (is_string($raw)) {
          try {
              $raw = json_decode($raw, true, flags: JSON_THROW_ON_ERROR);
          } catch (JsonException) {
              $raw = str_contains($raw, "\n") ? explode("\n", $raw) : [$raw];
          }
      }
      if (!is_array($raw)) {
          return [];
      }
      $tasks = array_map('trim', array_filter($raw, 'is_string'));
      return array_values(array_filter($tasks, fn ($task) => $task !== ''));
  }

  function verifyPromptFor(string $subtask, string $result): string
  {
      return 'Adversarially verify the subagent result below: try to REFUTE it. Re-derive the '
          . 'claims yourself with bash rather than trusting the result, and look for evidence '
          . 'that contradicts them. Default to refuted if uncertain. Call report_findings with '
          . "summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command "
          . "output that decided it.\n\n"
          . "Subtask: {$subtask}\n\nResult to verify:\n{$result}";
  }

  /**
   * Run subtasks through the journal, then run a second verification wave over the
   * results, and return both. PHP's standard runtime has no lightweight thread pool,
   * so both waves run sequentially here (MAX_CONCURRENT is unused); the SDK examples
   * in other languages fan them out in parallel.
   */
  function runWorkflow(Client $client, string $model, mixed $rawSubtasks): array
  {
      $allSubtasks = normalizeSubtasks($rawSubtasks);
      $subtasks = array_slice($allSubtasks, 0, MAX_TOTAL_SUBTASKS);
      $dropped = count($allSubtasks) - count($subtasks);
      if ($subtasks === []) {
          return ['Workflow error: no usable subtasks were provided.', true];
      }
      fwrite(STDERR, '[workflow] running ' . count($subtasks) . " agents\n");

      $runOne = function (string $prompt) use ($client, $model): string {
          try {
              return journaled($prompt, fn () => runSubagent($client, $model, $prompt));
          } catch (Throwable $error) {
              // Isolation boundary: one bad subagent should not end the run.
              return '(subagent failed: ' . $error::class . ': ' . $error->getMessage() . ')';
          }
      };

      $results = array_map($runOne, $subtasks);
      fwrite(STDERR, '[workflow] verifying ' . count($results) . " results\n");
      $verifyPrompts = array_map(verifyPromptFor(...), $subtasks, $results);
      $verdicts = array_map($runOne, $verifyPrompts);

      $sections = [];
      foreach ($subtasks as $index => $task) {
          $sections[] = '[agent ' . ($index + 1) . ": {$task}]\n{$results[$index]}"
              . "\n\n[verify " . ($index + 1) . "]\n{$verdicts[$index]}";
      }
      $joined = implode("\n\n", $sections);
      if ($dropped > 0) {
          $joined = '(note: ' . $dropped . ' subtasks beyond MAX_TOTAL_SUBTASKS=' . MAX_TOTAL_SUBTASKS
              . " were not run; rerun them in a follow-up Workflow call)\n\n" . $joined;
      }
      return [$joined, false];
  }
  ```

  ```ruby Ruby
  # Accept the subtasks input in whatever shape the model emits: an array, the array
  # JSON-encoded as a single string, or a newline-separated list.
  def normalize_subtasks(raw)
    if raw.is_a?(String)
      begin
        raw = JSON.parse(raw)
      rescue JSON::ParserError
        raw = raw.include?("\n") ? raw.split("\n") : [raw]
      end
    end
    return [] unless raw.is_a?(Array)
    raw.select { |task| task.is_a?(String) }.map(&:strip).reject(&:empty?)
  end

  def verify_prompt_for(subtask, result)
    "Adversarially verify the subagent result below: try to REFUTE it. Re-derive the " \
      "claims yourself with bash rather than trusting the result, and look for evidence " \
      "that contradicts them. Default to refuted if uncertain. Call report_findings with " \
      "summary 'refuted: <why>' or 'confirmed: <why>', citing the file:line or command " \
      "output that decided it.\n\n" \
      "Subtask: #{subtask}\n\nResult to verify:\n#{result}"
  end

  # Map with a concurrency limit: at most `limit` threads are in flight at once.
  def map_with_limit(items, limit)
    results = Array.new(items.length)
    queue = Queue.new
    items.each_with_index { |item, index| queue << [index, item] }
    workers = Array.new([limit, items.length].min) do
      Thread.new do
        until queue.empty?
          index, item = queue.pop(true) rescue break
          results[index] = yield item
        end
      end
    end
    workers.each(&:join)
    results
  end

  # Run subtasks as parallel subagents, then run a second verification wave over
  # the results, and return both. MAX_TOTAL_SUBTASKS bounds how many the model can
  # queue; MAX_CONCURRENT bounds how many run at once.
  def run_workflow(model, raw_subtasks)
    all_subtasks = normalize_subtasks(raw_subtasks)
    subtasks = all_subtasks.first(MAX_TOTAL_SUBTASKS)
    dropped = all_subtasks.length - subtasks.length
    return ["Workflow error: no usable subtasks were provided.", true] if subtasks.empty?

    warn "[workflow] fanning out #{subtasks.length} agents"
    run_one = lambda do |prompt|
      journaled(prompt) { run_subagent(model, prompt) }
    rescue => error # isolation boundary: one bad subagent should not end the run
      "(subagent failed: #{error.class}: #{error.message})"
    end

    results = map_with_limit(subtasks, MAX_CONCURRENT, &run_one)
    warn "[workflow] verifying #{results.length} results"
    verify_prompts = subtasks.zip(results).map { |task, result| verify_prompt_for(task, result) }
    verdicts = map_with_limit(verify_prompts, MAX_CONCURRENT, &run_one)

    joined = subtasks.each_with_index.map do |task, index|
      "[agent #{index + 1}: #{task}]\n#{results[index]}\n\n[verify #{index + 1}]\n#{verdicts[index]}"
    end.join("\n\n")
    if dropped > 0
      joined =
        "(note: #{dropped} subtasks beyond MAX_TOTAL_SUBTASKS=#{MAX_TOTAL_SUBTASKS} were not " \
        "run; rerun them in a follow-up Workflow call)\n\n#{joined}"
    end
    [joined, false]
  end
  ```
</CodeGroup>

## Toggle the mode with mid-conversation system messages

The agent appends the user's message first, then any system messages that are due: the exit notice, the full mode text on entry, or the periodic refresher. Placing the system message after the user turn keeps every cached byte ahead of it untouched, and satisfies the placement rule that a system message follows a user turn.

<CodeGroup>
  ```bash cURL
  # One orchestration-mode turn: the mode reminder rides in the messages array as a
  # {"role": "system"} entry placed after the user turn it applies to. The response
  # stops at the first tool call. The agent loop that executes tool calls and fans
  # out subagents is shown in the SDK tabs; the Workflow description is condensed
  # here, the SDK examples carry the full standing-consent text.
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "model": "claude-opus-4-8",
    "max_tokens": 64000,
    "system": "You are a helpful general-purpose agent. Answer the user's request directly.",
    "thinking": {"type": "adaptive"},
    "output_config": {"effort": "xhigh"},
    "tools": [
      {
        "name": "Workflow",
        "description": "Orchestrate a multi-agent workflow: split a large task into independent subtasks and run them as parallel agents, then collect their results. Opt-in: only use this tool when the user explicitly asks for a workflow, or when a system message confirms that orchestration mode is on. Granularity: scope each subtask to a distinct concern rather than per line or file section; a review of a small module rarely needs more than about ten. Standing consent: while a system message confirms orchestration mode is on, author and run a workflow for every substantive task by default; work solo only on conversational turns or trivial mechanical edits.",
        "input_schema": {
          "type": "object",
          "properties": {
            "subtasks": {
              "type": "array",
              "items": {"type": "string"},
              "description": "Independent subtask prompts to run as parallel agents"
            }
          },
          "required": ["subtasks"]
        }
      },
      {"type": "bash_20250124", "name": "bash"}
    ],
    "messages": [
      {
        "role": "user",
        "content": "Explore the current directory, then give a thorough review: what it does, code-quality issues, and concrete improvements."
      },
      {
        "role": "system",
        "content": "Orchestration mode is on: optimize for the most exhaustive, correct answer rather than the fastest one. Use the Workflow tool on every substantive task, sized to the problem's natural decomposition rather than the maximum the tool allows. See the Workflow tool's description for standing consent, granularity guidance, and quality patterns. Work solo only on conversational or trivial turns."
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  # One orchestration-mode turn: the mode reminder rides in the messages array as a
  # system-role entry placed after the user turn it applies to. The response stops
  # at the first tool call. The agent loop that executes tool calls and fans out
  # subagents is shown in the SDK tabs; the Workflow description is condensed here,
  # the SDK examples carry the full standing-consent text.
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 64000
  system: You are a helpful general-purpose agent. Answer the user's request directly.
  thinking: {type: adaptive}
  output_config: {effort: xhigh}
  tools:
    - name: Workflow
      description: >-
        Orchestrate a multi-agent workflow: split a large task into independent
        subtasks and run them as parallel agents, then collect their results.
        Opt-in: only use this tool when the user explicitly asks for a workflow,
        or when a system message confirms that orchestration mode is on.
        Granularity: scope each subtask to a distinct concern rather than per
        line or file section; a review of a small module rarely needs more than
        about ten. Standing consent: while a system message confirms
        orchestration mode is on, author and run a workflow for every
        substantive task by default; work solo only on conversational turns or
        trivial mechanical edits.
      input_schema:
        type: object
        properties:
          subtasks:
            type: array
            items: {type: string}
            description: Independent subtask prompts to run as parallel agents
        required: [subtasks]
    - {type: bash_20250124, name: bash}
  messages:
    - role: user
      content: >-
        Explore the current directory, then give a thorough review: what it
        does, code-quality issues, and concrete improvements.
    - role: system
      content: >-
        Orchestration mode is on: optimize for the most exhaustive, correct
        answer rather than the fastest one. Use the Workflow tool on every
        substantive task, sized to the problem's natural decomposition rather
        than the maximum the tool allows. See the Workflow tool's description
        for standing consent, granularity guidance, and quality patterns. Work
        solo only on conversational or trivial turns.
  YAML
  ```

  ```python Python
  class ModeAgent:
      """An agent loop whose orchestration mode is toggled with mid-conversation system messages."""

      def __init__(self, model: str, mode_on: bool = True):
          self.model = model
          self.mode_on = mode_on
          self.messages: list[dict] = []
          self._mode_announced = False
          self._exit_pending = False
          self._turns_since_reminder = 0

      def set_mode(self, mode_on: bool) -> None:
          """Turn the mode on or off. The notice is delivered with the next user turn."""
          if mode_on == self.mode_on:
              return
          if not mode_on:
              if self._mode_announced:
                  self._exit_pending = True
          else:
              self._exit_pending = False
          self.mode_on = mode_on

      def _due_system_messages(self) -> list[dict]:
          """System messages owed on this turn: an exit notice, the full mode text on entry,
          or a one-line refresher every TURNS_BETWEEN_REFRESHERS user turns."""
          due = []
          if self._exit_pending:
              self._exit_pending = False
              self._mode_announced = False
              due.append({"role": "system", "content": MODE_EXIT})
          if self.mode_on:
              if not self._mode_announced:
                  self._mode_announced = True
                  self._turns_since_reminder = 0
                  due.append({"role": "system", "content": MODE_ENTER})
              elif self._turns_since_reminder >= TURNS_BETWEEN_REFRESHERS:
                  self._turns_since_reminder = 0
                  due.append({"role": "system", "content": MODE_REFRESH})
          return due

      def turn(self, user_input: str) -> str:
          # Mid-conversation system messages follow the user turn they apply to, which keeps
          # the cached prefix ahead of them untouched.
          self.messages.append({"role": "user", "content": user_input})
          self.messages.extend(self._due_system_messages())
          self._turns_since_reminder += 1

          for _ in range(MAX_MAIN_TURNS):
              with client.messages.stream(
                  model=self.model,
                  max_tokens=64000,
                  system=SYSTEM_PROMPT,  # static for the whole session
                  thinking={"type": "adaptive"},
                  output_config={"effort": EFFORT},
                  tools=[WORKFLOW_TOOL, BASH_TOOL],
                  messages=self.messages,
                  timeout=REQUEST_TIMEOUT_SECONDS,
              ) as stream:
                  response = stream.get_final_message()
              self.messages.append({"role": "assistant", "content": response.content})

              if response.stop_reason == "pause_turn":
                  continue
              if response.stop_reason != "tool_use":
                  text = "".join(block.text for block in response.content if block.type == "text")
                  if response.stop_reason == "max_tokens":
                      # Drop the truncated assistant message so later turns don't build on it.
                      self.messages.pop()
                      text += "\n\n(warning: response was truncated at max_tokens)"
                  return text

              tool_results = []
              for block in response.content:
                  if block.type != "tool_use":
                      continue
                  if block.name == "Workflow":
                      output, is_error = run_workflow(self.model, block.input.get("subtasks", []))
                  elif block.name == "bash":
                      output, is_error = handle_bash_block(block)
                  else:
                      output, is_error = f"unknown tool: {block.name}", True
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": output,
                          "is_error": is_error,
                      }
                  )
              self.messages.append({"role": "user", "content": tool_results})
          return "(hit the main loop turn limit before finishing)"
  ```

  ```typescript TypeScript
  // An agent loop whose orchestration mode is toggled with mid-conversation system messages.
  class ModeAgent {
    private readonly model: string;
    private modeOn: boolean;
    private readonly messages: Anthropic.MessageParam[] = [];
    private modeAnnounced = false;
    private exitPending = false;
    private turnsSinceReminder = 0;

    constructor(model: string, modeOn = true) {
      this.model = model;
      this.modeOn = modeOn;
    }

    // Turn the mode on or off. The notice is delivered with the next user turn.
    setMode(modeOn: boolean): void {
      if (modeOn === this.modeOn) {
        return;
      }
      if (!modeOn) {
        if (this.modeAnnounced) {
          this.exitPending = true;
        }
      } else {
        this.exitPending = false;
      }
      this.modeOn = modeOn;
    }

    // System messages owed on this turn: an exit notice, the full mode text on entry,
    // or a one-line refresher every TURNS_BETWEEN_REFRESHERS user turns.
    private dueSystemMessages(): Anthropic.MessageParam[] {
      const due: Array<{ role: "system"; content: string }> = [];
      if (this.exitPending) {
        this.exitPending = false;
        this.modeAnnounced = false;
        due.push({ role: "system", content: MODE_EXIT });
      }
      if (this.modeOn) {
        if (!this.modeAnnounced) {
          this.modeAnnounced = true;
          this.turnsSinceReminder = 0;
          due.push({ role: "system", content: MODE_ENTER });
        } else if (this.turnsSinceReminder >= TURNS_BETWEEN_REFRESHERS) {
          this.turnsSinceReminder = 0;
          due.push({ role: "system", content: MODE_REFRESH });
        }
      }
      // The published SDK types message roles as "user" | "assistant"; typed support for
      // mid-conversation system messages ships with the SDK release that includes them.
      return due as unknown as Anthropic.MessageParam[];
    }

    async turn(userInput: string): Promise<string> {
      // Mid-conversation system messages follow the user turn they apply to, which keeps
      // the cached prefix ahead of them untouched.
      this.messages.push({ role: "user", content: userInput });
      this.messages.push(...this.dueSystemMessages());
      this.turnsSinceReminder += 1;

      for (let turn = 0; turn < MAX_MAIN_TURNS; turn++) {
        const response = await client.messages
          .stream(
            {
              model: this.model,
              max_tokens: 64000,
              system: SYSTEM_PROMPT, // static for the whole session
              thinking: { type: "adaptive" },
              output_config: { effort: EFFORT },
              tools: [WORKFLOW_TOOL, BASH_TOOL],
              messages: this.messages,
            },
            { signal: AbortSignal.timeout(REQUEST_TIMEOUT_SECONDS * 1000) },
          )
          .finalMessage();
        this.messages.push({ role: "assistant", content: response.content });

        if (response.stop_reason === "pause_turn") {
          continue;
        }
        if (response.stop_reason !== "tool_use") {
          let text = response.content
            .filter((block): block is Anthropic.TextBlock => block.type === "text")
            .map((block) => block.text)
            .join("");
          if (response.stop_reason === "max_tokens") {
            // Drop the truncated assistant message so later turns do not build on it.
            this.messages.pop();
            text += "\n\n(warning: response was truncated at max_tokens)";
          }
          return text;
        }

        const toolResults: Anthropic.ToolResultBlockParam[] = [];
        for (const block of response.content) {
          if (block.type !== "tool_use") {
            continue;
          }
          let output: string;
          let isError: boolean;
          if (block.name === "Workflow") {
            const input = block.input as { subtasks?: unknown };
            ({ output, isError } = await runWorkflow(this.model, input.subtasks ?? []));
          } else if (block.name === "bash") {
            ({ output, isError } = await handleBashBlock(block));
          } else {
            output = `unknown tool: ${block.name}`;
            isError = true;
          }
          toolResults.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: output,
            is_error: isError,
          });
        }
        this.messages.push({ role: "user", content: toolResults });
      }
      return "(hit the main loop turn limit before finishing)";
    }
  }
  ```

  ```csharp C#
  // An agent loop whose orchestration mode is toggled with mid-conversation system messages.
  List<MessageParam> messages = [];
  var modeOn = true;
  var modeAnnounced = false;
  var exitPending = false;
  var turnsSinceReminder = 0;

  // Turn the mode on or off. The notice is delivered with the next user turn.
  void SetMode(bool nextModeOn)
  {
      if (nextModeOn == modeOn)
      {
          return;
      }
      if (!nextModeOn)
      {
          if (modeAnnounced)
          {
              exitPending = true;
          }
      }
      else
      {
          exitPending = false;
      }
      modeOn = nextModeOn;
  }

  // The Role property is an open enum, so the mid-conversation "system" role can be assigned
  // as a raw string; a dedicated constant ships with the SDK release.
  MessageParam SystemMessage(string content) => new() { Role = "system", Content = content };

  // System messages owed on this turn: an exit notice, the full mode text on entry,
  // or a one-line refresher every turnsBetweenRefreshers user turns.
  List<MessageParam> DueSystemMessages()
  {
      List<MessageParam> due = [];
      if (exitPending)
      {
          exitPending = false;
          modeAnnounced = false;
          due.Add(SystemMessage(modeExit));
      }
      if (modeOn)
      {
          if (!modeAnnounced)
          {
              modeAnnounced = true;
              turnsSinceReminder = 0;
              due.Add(SystemMessage(modeEnter));
          }
          else if (turnsSinceReminder >= turnsBetweenRefreshers)
          {
              turnsSinceReminder = 0;
              due.Add(SystemMessage(modeRefresh));
          }
      }
      return due;
  }

  // Send one user turn through the loop, executing tool calls until the model stops.
  async Task<string> Turn(string userInput)
  {
      // Mid-conversation system messages follow the user turn they apply to, which keeps
      // the cached prefix ahead of them untouched.
      messages.Add(new() { Role = Role.User, Content = userInput });
      messages.AddRange(DueSystemMessages());
      turnsSinceReminder++;

      for (var turn = 0; turn < maxMainTurns; turn++)
      {
          using var deadline = new CancellationTokenSource(TimeSpan.FromSeconds(requestTimeoutSeconds));
          var response = await client.Messages.Create(new MessageCreateParams
          {
              Model = model,
              MaxTokens = requestMaxTokens,
              System = systemPrompt, // static for the whole session
              Thinking = new ThinkingConfigAdaptive(),
              OutputConfig = new OutputConfig { Effort = effort },
              Tools = [workflowTool, bashTool],
              Messages = messages,
          }, cancellationToken: deadline.Token);
          messages.Add(new()
          {
              Role = Role.Assistant,
              Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
          });

          if (response.StopReason == StopReason.PauseTurn)
          {
              continue;
          }
          if (response.StopReason != StopReason.ToolUse)
          {
              var text = string.Concat(
                  response.Content.Select(block => block.TryPickText(out var textBlock) ? textBlock.Text : ""));
              if (response.StopReason == StopReason.MaxTokens)
              {
                  // Drop the truncated assistant message so the next turn does not build on it.
                  messages.RemoveAt(messages.Count - 1);
                  text += "\n\n(warning: response was truncated at max_tokens)";
              }
              return text;
          }

          List<ContentBlockParam> toolResults = [];
          foreach (var block in response.Content)
          {
              if (!block.TryPickToolUse(out var toolUse))
              {
                  continue;
              }
              string output;
              bool isError;
              if (toolUse.Name == "Workflow")
              {
                  toolUse.Input.TryGetValue("subtasks", out var rawSubtasks);
                  (output, isError) = await RunWorkflow(rawSubtasks);
              }
              else if (toolUse.Name == "bash")
              {
                  (output, isError) = await HandleBashBlock(toolUse);
              }
              else
              {
                  output = $"unknown tool: {toolUse.Name}";
                  isError = true;
              }
              toolResults.Add(new ToolResultBlockParam(toolUse.ID) { Content = output, IsError = isError });
          }
          messages.Add(new() { Role = Role.User, Content = toolResults });
      }
      return "(hit the main loop turn limit before finishing)";
  }
  ```

  ```go Go
  // modeAgent is an agent loop whose orchestration mode is toggled with mid-conversation
  // system messages.
  type modeAgent struct {
  	model              string
  	modeOn             bool
  	messages           []anthropic.MessageParam
  	modeAnnounced      bool
  	exitPending        bool
  	turnsSinceReminder int
  }

  func newModeAgent(model string) *modeAgent {
  	return &modeAgent{model: model, modeOn: true}
  }

  // setMode turns the mode on or off. The notice is delivered with the next user turn.
  func (agent *modeAgent) setMode(modeOn bool) {
  	if modeOn == agent.modeOn {
  		return
  	}
  	if !modeOn {
  		if agent.modeAnnounced {
  			agent.exitPending = true
  		}
  	} else {
  		agent.exitPending = false
  	}
  	agent.modeOn = modeOn
  }

  // dueSystemMessages returns the system messages owed on this turn: an exit notice, the
  // full mode text on entry, or a one-line refresher every turnsBetweenRefreshers user turns.
  func (agent *modeAgent) dueSystemMessages() []anthropic.MessageParam {
  	// MessageParamRole is an open string type, so the mid-conversation "system" role can
  	// be expressed directly; a dedicated constant ships with the SDK release.
  	systemMessage := func(content string) anthropic.MessageParam {
  		return anthropic.MessageParam{
  			Role:    anthropic.MessageParamRole("system"),
  			Content: []anthropic.ContentBlockParamUnion{anthropic.NewTextBlock(content)},
  		}
  	}
  	var due []anthropic.MessageParam
  	if agent.exitPending {
  		agent.exitPending = false
  		agent.modeAnnounced = false
  		due = append(due, systemMessage(modeExit))
  	}
  	if agent.modeOn {
  		if !agent.modeAnnounced {
  			agent.modeAnnounced = true
  			agent.turnsSinceReminder = 0
  			due = append(due, systemMessage(modeEnter))
  		} else if agent.turnsSinceReminder >= turnsBetweenRefreshers {
  			agent.turnsSinceReminder = 0
  			due = append(due, systemMessage(modeRefresh))
  		}
  	}
  	return due
  }

  // turn sends one user turn through the loop, executing tool calls until the model stops.
  func (agent *modeAgent) turn(ctx context.Context, userInput string) (string, error) {
  	// Mid-conversation system messages follow the user turn they apply to, which keeps
  	// the cached prefix ahead of them untouched.
  	agent.messages = append(agent.messages, anthropic.NewUserMessage(anthropic.NewTextBlock(userInput)))
  	agent.messages = append(agent.messages, agent.dueSystemMessages()...)
  	agent.turnsSinceReminder++

  	for range maxMainTurns {
  		var response anthropic.Message
  		err := func() error {
  			ctx, cancel := context.WithTimeout(ctx, requestTimeoutSeconds*time.Second)
  			defer cancel()
  			stream := client.Messages.NewStreaming(ctx, anthropic.MessageNewParams{
  				Model:        agent.model,
  				MaxTokens:    64000,
  				System:       []anthropic.TextBlockParam{{Text: systemPrompt}}, // static for the whole session
  				Thinking:     anthropic.ThinkingConfigParamUnion{OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{}},
  				OutputConfig: anthropic.OutputConfigParam{Effort: effort},
  				Tools:        []anthropic.ToolUnionParam{workflowTool, bashTool},
  				Messages:     agent.messages,
  			})
  			defer stream.Close()
  			for stream.Next() {
  				if err := response.Accumulate(stream.Current()); err != nil {
  					return err
  				}
  			}
  			return stream.Err()
  		}()
  		if err != nil {
  			return "", err
  		}
  		agent.messages = append(agent.messages, response.ToParam())

  		if response.StopReason == anthropic.StopReasonPauseTurn {
  			continue
  		}
  		if response.StopReason != anthropic.StopReasonToolUse {
  			var text strings.Builder
  			for _, block := range response.Content {
  				if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  					text.WriteString(textBlock.Text)
  				}
  			}
  			if response.StopReason == anthropic.StopReasonMaxTokens {
  				// Drop the truncated assistant message rather than leave a clipped turn in history.
  				agent.messages = agent.messages[:len(agent.messages)-1]
  				text.WriteString("\n\n(warning: response was truncated at max_tokens)")
  			}
  			return text.String(), nil
  		}

  		var toolResults []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			toolUse, ok := block.AsAny().(anthropic.ToolUseBlock)
  			if !ok {
  				continue
  			}
  			var output string
  			var isError bool
  			switch toolUse.Name {
  			case "Workflow":
  				var input struct {
  					Subtasks json.RawMessage `json:"subtasks"`
  				}
  				if err := json.Unmarshal(toolUse.Input, &input); err != nil {
  					output, isError = fmt.Sprintf("Workflow error: could not parse input: %s", err), true
  				} else {
  					output, isError = runWorkflow(ctx, agent.model, input.Subtasks)
  				}
  			case "bash":
  				output, isError = handleBashBlock(ctx, toolUse)
  			default:
  				output, isError = fmt.Sprintf("unknown tool: %s", toolUse.Name), true
  			}
  			toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, output, isError))
  		}
  		agent.messages = append(agent.messages, anthropic.NewUserMessage(toolResults...))
  	}
  	return "(hit the main loop turn limit before finishing)", nil
  }

  ```

  ```java Java
  // An agent loop whose orchestration mode is toggled with mid-conversation system messages.
  class ModeAgent {
      private final String model;
      private boolean modeOn;
      private final List<MessageParam> messages = new ArrayList<>();
      private boolean modeAnnounced = false;
      private boolean exitPending = false;
      private int turnsSinceReminder = 0;

      ModeAgent(String model) {
          this(model, true);
      }

      ModeAgent(String model, boolean modeOn) {
          this.model = model;
          this.modeOn = modeOn;
      }

      // Turn the mode on or off. The notice is delivered with the next user turn.
      void setMode(boolean modeOn) {
          if (modeOn == this.modeOn) {
              return;
          }
          if (!modeOn) {
              if (modeAnnounced) {
                  exitPending = true;
              }
          } else {
              exitPending = false;
          }
          this.modeOn = modeOn;
      }

      // System messages owed on this turn: an exit notice, the full mode text on entry,
      // or a one-line refresher every TURNS_BETWEEN_REFRESHERS user turns.
      private List<MessageParam> dueSystemMessages() {
          List<MessageParam> due = new ArrayList<>();
          if (exitPending) {
              exitPending = false;
              modeAnnounced = false;
              due.add(systemMessage(MODE_EXIT));
          }
          if (modeOn) {
              if (!modeAnnounced) {
                  modeAnnounced = true;
                  turnsSinceReminder = 0;
                  due.add(systemMessage(MODE_ENTER));
              } else if (turnsSinceReminder >= TURNS_BETWEEN_REFRESHERS) {
                  turnsSinceReminder = 0;
                  due.add(systemMessage(MODE_REFRESH));
              }
          }
          return due;
      }

      // MessageParam.Role is an open enum, so the mid-conversation "system" role can be
      // expressed with Role.of; a dedicated constant ships with the SDK release.
      private MessageParam systemMessage(String content) {
          return MessageParam.builder()
                  .role(MessageParam.Role.of("system"))
                  .content(content)
                  .build();
      }

      // Send one user turn through the loop, executing tool calls until the model stops.
      String turn(String userInput) throws InterruptedException {
          // Mid-conversation system messages follow the user turn they apply to, which keeps
          // the cached prefix ahead of them untouched.
          messages.add(MessageParam.builder().role(MessageParam.Role.USER).content(userInput).build());
          messages.addAll(dueSystemMessages());
          turnsSinceReminder++;

          for (int turn = 0; turn < MAX_MAIN_TURNS; turn++) {
              MessageCreateParams params = MessageCreateParams.builder()
                      .model(model)
                      .maxTokens(64000L)
                      .system(SYSTEM_PROMPT) // static for the whole session
                      .thinking(ThinkingConfigAdaptive.builder().build())
                      .outputConfig(OutputConfig.builder().effort(EFFORT).build())
                      .addTool(WORKFLOW_TOOL)
                      .addTool(BASH_TOOL)
                      .messages(messages)
                      .build();
              MessageAccumulator accumulator = MessageAccumulator.create();
              try (var stream = client.messages().createStreaming(params, REQUEST_OPTIONS)) {
                  stream.stream().forEach(accumulator::accumulate);
              }
              Message response = accumulator.message();
              messages.add(response.toParam());

              StopReason stopReason = response.stopReason().orElse(null);
              if (StopReason.PAUSE_TURN.equals(stopReason)) {
                  continue;
              }
              if (!StopReason.TOOL_USE.equals(stopReason)) {
                  String text = response.content().stream()
                          .flatMap(block -> block.text().stream())
                          .map(TextBlock::text)
                          .collect(Collectors.joining());
                  if (StopReason.MAX_TOKENS.equals(stopReason)) {
                      // Drop the truncated assistant message so it does not poison later turns.
                      messages.removeLast();
                      text += "\n\n(warning: response was truncated at max_tokens)";
                  }
                  return text;
              }

              List<ContentBlockParam> toolResults = new ArrayList<>();
              for (ContentBlock block : response.content()) {
                  if (block.toolUse().isEmpty()) {
                      continue;
                  }
                  ToolUseBlock toolUse = block.toolUse().get();
                  ToolOutput result = switch (toolUse.name()) {
                      case "Workflow" -> {
                          Map<String, JsonValue> input =
                                  (Map<String, JsonValue>) toolUse._input().asObject().orElse(Map.of());
                          JsonValue rawSubtasks = input.getOrDefault("subtasks", JsonValue.from(List.of()));
                          yield runWorkflow(model, rawSubtasks);
                      }
                      case "bash" -> handleBashBlock(toolUse);
                      default -> new ToolOutput("unknown tool: " + toolUse.name(), true);
                  };
                  toolResults.add(ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()
                          .toolUseId(toolUse.id())
                          .content(result.output())
                          .isError(result.isError())
                          .build()));
              }
              messages.add(MessageParam.builder()
                      .role(MessageParam.Role.USER)
                      .contentOfBlockParams(toolResults)
                      .build());
          }
          return "(hit the main loop turn limit before finishing)";
      }
  }
  ```

  ```php PHP
  /** An agent loop whose orchestration mode is toggled with mid-conversation system messages. */
  class ModeAgent
  {
      private array $messages = [];
      private bool $modeAnnounced = false;
      private bool $exitPending = false;
      private int $turnsSinceReminder = 0;

      public function __construct(
          private readonly Client $client,
          private readonly string $model,
          private bool $modeOn = true,
      ) {
      }

      /** Turn the mode on or off. The notice is delivered with the next user turn. */
      public function setMode(bool $modeOn): void
      {
          if ($modeOn === $this->modeOn) {
              return;
          }
          if ($modeOn) {
              $this->exitPending = false;
          } elseif ($this->modeAnnounced) {
              $this->exitPending = true;
          }
          $this->modeOn = $modeOn;
      }

      public function turn(string $userInput): string
      {
          // Mid-conversation system messages follow the user turn they apply to, which keeps
          // the cached prefix ahead of them untouched.
          $this->messages[] = ['role' => 'user', 'content' => $userInput];
          array_push($this->messages, ...$this->dueSystemMessages());
          $this->turnsSinceReminder++;

          for ($turn = 0; $turn < MAX_MAIN_TURNS; $turn++) {
              $stream = $this->client->messages->createStream(
                  model: $this->model,
                  maxTokens: 64000,
                  system: SYSTEM_PROMPT, // static for the whole session
                  thinking: ['type' => 'adaptive'],
                  outputConfig: ['effort' => EFFORT],
                  tools: [WORKFLOW_TOOL, BASH_TOOL],
                  messages: $this->messages,
                  requestOptions: ['timeout' => REQUEST_TIMEOUT_SECONDS],
              );
              [$content, $stopReason] = drainMessageStream($stream);
              $this->messages[] = ['role' => 'assistant', 'content' => $content];

              if ($stopReason === 'pause_turn') {
                  continue;
              }
              if ($stopReason !== 'tool_use') {
                  $text = '';
                  foreach ($content as $block) {
                      if ($block instanceof TextBlock) {
                          $text .= $block->text;
                      }
                  }
                  if ($stopReason === 'max_tokens') {
                      // Drop the truncated assistant message so the next turn does not build on it.
                      array_pop($this->messages);
                      $text .= "\n\n(warning: response was truncated at max_tokens)";
                  }
                  return $text;
              }

              $toolResults = [];
              foreach ($content as $block) {
                  if (!$block instanceof ToolUseBlock) {
                      continue;
                  }
                  if ($block->name === 'Workflow') {
                      [$output, $isError] =
                          runWorkflow($this->client, $this->model, $block->input['subtasks'] ?? []);
                  } elseif ($block->name === 'bash') {
                      [$output, $isError] = handleBashBlock($block);
                  } else {
                      $output = "unknown tool: {$block->name}";
                      $isError = true;
                  }
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => $output,
                      'is_error' => $isError,
                  ];
              }
              $this->messages[] = ['role' => 'user', 'content' => $toolResults];
          }
          return '(hit the main loop turn limit before finishing)';
      }

      /**
       * System messages owed on this turn: an exit notice, the full mode text on entry,
       * or a one-line refresher every TURNS_BETWEEN_REFRESHERS user turns.
       */
      private function dueSystemMessages(): array
      {
          $due = [];
          if ($this->exitPending) {
              $this->exitPending = false;
              $this->modeAnnounced = false;
              $due[] = ['role' => 'system', 'content' => MODE_EXIT];
          }
          if ($this->modeOn) {
              if (!$this->modeAnnounced) {
                  $this->modeAnnounced = true;
                  $this->turnsSinceReminder = 0;
                  $due[] = ['role' => 'system', 'content' => MODE_ENTER];
              } elseif ($this->turnsSinceReminder >= TURNS_BETWEEN_REFRESHERS) {
                  $this->turnsSinceReminder = 0;
                  $due[] = ['role' => 'system', 'content' => MODE_REFRESH];
              }
          }
          return $due;
      }
  }
  ```

  ```ruby Ruby
  # An agent loop whose orchestration mode is toggled with mid-conversation system messages.
  class ModeAgent
    def initialize(model, mode_on: true)
      @model = model
      @mode_on = mode_on
      @messages = []
      @mode_announced = false
      @exit_pending = false
      @turns_since_reminder = 0
    end

    # Turn the mode on or off. The notice is delivered with the next user turn.
    def set_mode(mode_on)
      return if mode_on == @mode_on

      if mode_on
        @exit_pending = false
      else
        @exit_pending = true if @mode_announced
      end
      @mode_on = mode_on
    end

    def turn(user_input)
      # Mid-conversation system messages follow the user turn they apply to, which keeps
      # the cached prefix ahead of them untouched.
      @messages << {role: "user", content: user_input}
      @messages.concat(due_system_messages)
      @turns_since_reminder += 1

      MAX_MAIN_TURNS.times do
        stream = CLIENT.messages.stream(
          model: @model,
          max_tokens: 64_000,
          system_: SYSTEM_PROMPT, # static for the whole session
          thinking: {type: :adaptive},
          output_config: {effort: EFFORT},
          tools: [WORKFLOW_TOOL, BASH_TOOL],
          messages: @messages,
          request_options: {timeout: REQUEST_TIMEOUT_SECONDS}
        )
        response = stream.accumulated_message
        @messages << {role: "assistant", content: assistant_content_param(response.content)}

        next if response.stop_reason == :pause_turn

        unless response.stop_reason == :tool_use
          text = response.content.select { |block| block.type == :text }.map(&:text).join
          if response.stop_reason == :max_tokens
            @messages.pop # drop the truncated assistant message from the history
            text += "\n\n(warning: response was truncated at max_tokens)"
          end
          return text
        end

        tool_results = []
        response.content.each do |block|
          next unless block.type == :tool_use

          input = parse_tool_input(block.input)
          case block.name
          when "Workflow"
            output, is_error = run_workflow(@model, input["subtasks"] || [])
          when "bash"
            output, is_error = handle_bash_block(block)
          else
            output, is_error = "unknown tool: #{block.name}", true
          end
          tool_results << {
            type: "tool_result",
            tool_use_id: block.id,
            content: output,
            is_error: is_error
          }
        end
        @messages << {role: "user", content: tool_results}
      end
      "(hit the main loop turn limit before finishing)"
    end

    private

    # System messages owed on this turn: an exit notice, the full mode text on entry,
    # or a one-line refresher every TURNS_BETWEEN_REFRESHERS user turns.
    def due_system_messages
      due = []
      if @exit_pending
        @exit_pending = false
        @mode_announced = false
        due << {role: "system", content: MODE_EXIT}
      end
      if @mode_on
        if !@mode_announced
          @mode_announced = true
          @turns_since_reminder = 0
          due << {role: "system", content: MODE_ENTER}
        elsif @turns_since_reminder >= TURNS_BETWEEN_REFRESHERS
          @turns_since_reminder = 0
          due << {role: "system", content: MODE_REFRESH}
        end
      end
      due
    end
  end
  ```
</CodeGroup>

## Run it

<Warning>
  The bash tool in this example runs model-written commands directly on your machine with no sandbox, and the fan-out runs several of those agents in parallel. Run it in a directory and environment you are comfortable exposing, and add sandboxing before adapting it for anything beyond local experimentation.
</Warning>

<CodeGroup>
  ```python Python
  if __name__ == "__main__":
      task = (
          sys.argv[1]
          if len(sys.argv) > 1
          else "Explore the current directory, then give a thorough review: what it does, "
          "code-quality issues, and concrete improvements."
      )
      agent = ModeAgent(MODEL)
      print(agent.turn(task))
      agent.set_mode(False)
      print(agent.turn("Briefly summarize what you found above, no fan-out needed."))
  ```

  ```typescript TypeScript
  const task =
    process.argv[2] ??
    "Explore the current directory, then give a thorough review: what it does, " +
      "code-quality issues, and concrete improvements.";
  const agent = new ModeAgent(MODEL);
  console.log(await agent.turn(task));
  agent.setMode(false);
  console.log(await agent.turn("Briefly summarize what you found above, no fan-out needed."));
  ```

  ```csharp C#
  var task = args.Length > 0
      ? args[0]
      : "Explore the current directory, then give a thorough review: what it does, "
          + "code-quality issues, and concrete improvements.";
  Console.WriteLine(await Turn(task));
  SetMode(false);
  Console.WriteLine(await Turn("Briefly summarize what you found above, no fan-out needed."));
  ```

  ```go Go
  func main() {
  	if err := run(context.Background()); err != nil {
  		log.Fatal(err)
  	}
  }

  func run(ctx context.Context) error {
  	if docTestMode {
  		defer os.RemoveAll(workDir)
  	}
  	task := "Explore the current directory, then give a thorough review: what it does, " +
  		"code-quality issues, and concrete improvements."
  	if len(os.Args) > 1 {
  		task = os.Args[1]
  	}
  	agent := newModeAgent(modelID)
  	answer, err := agent.turn(ctx, task)
  	if err != nil {
  		return err
  	}
  	fmt.Println(answer)

  	agent.setMode(false)
  	summary, err := agent.turn(ctx, "Briefly summarize what you found above, no fan-out needed.")
  	if err != nil {
  		return err
  	}
  	fmt.Println(summary)
  	return nil
  }

  ```

  ```java Java
  void main(String[] args) throws InterruptedException {
      String task = args.length > 0
              ? args[0]
              : "Explore the current directory, then give a thorough review: what it does, "
                      + "code-quality issues, and concrete improvements.";
      ModeAgent agent = new ModeAgent(MODEL);
      IO.println(agent.turn(task));
      agent.setMode(false);
      IO.println(agent.turn("Briefly summarize what you found above, no fan-out needed."));
  }
  ```

  ```php PHP
  $task = $argv[1] ??
      'Explore the current directory, then give a thorough review: what it does, '
      . 'code-quality issues, and concrete improvements.';
  $agent = new ModeAgent($client, MODEL);
  echo $agent->turn($task), PHP_EOL;
  $agent->setMode(false);
  echo $agent->turn('Briefly summarize what you found above, no fan-out needed.'), PHP_EOL;
  ```

  ```ruby Ruby
  task = ARGV[0] ||
    "Explore the current directory, then give a thorough review: what it does, " \
    "code-quality issues, and concrete improvements."
  agent = ModeAgent.new(MODEL)
  puts agent.turn(task)
  agent.set_mode(false)
  puts agent.turn("Briefly summarize what you found above, no fan-out needed.")
  ```
</CodeGroup>

Start the example from the directory you want the agents to work in, for example the root of a repository to review:

```bash
python orchestration_mode.py "Review this repository for flaky tests and propose fixes."
```

With the mode on, expect the model to scout with a few bash commands, dispatch the Workflow tool unprompted, and synthesize the subagent reports into a final answer. Trivial or conversational requests stay solo, as the reminder instructs.

## Toward a production harness

This example is deliberately small. A harness meant for real workloads would typically add:

* **Sandboxed orchestration scripts:** let the model emit a short orchestration program (branching, loops, and reduce steps) and run it inside an isolated interpreter, rather than accepting only a flat list of subtask strings.
* **Durable journaling:** replace the local JSON file with a store that survives process restarts and is safe under concurrent writers across machines.
* **Budget enforcement:** track total subagents launched across the whole session, not just per Workflow call, and refuse to exceed a hard cap so a runaway plan cannot exhaust your quota.

The patterns in this example (the mode reminders, standing consent in the tool description, journaling, and a verification wave) carry over unchanged; only the execution substrate around them gets more robust.

## Related

<CardGroup cols={2}>
  <Card title="Mid-conversation system messages" icon="message" href="/docs/en/build-with-claude/mid-conversation-system-messages">
    The mechanism the mode reminders use, and how it interacts with prompt caching.
  </Card>

  <Card title="Effort" icon="gauge" href="/docs/en/build-with-claude/effort">
    The effort levels the API accepts and how to choose one.
  </Card>

  <Card title="Tool use with Claude" icon="wrench" href="/docs/en/agents-and-tools/tool-use/overview">
    Defining tools, handling tool calls, and tool results.
  </Card>

  <Card title="Bash tool" icon="terminal" href="/docs/en/agents-and-tools/tool-use/bash-tool">
    The Anthropic-defined bash tool this example executes locally.
  </Card>
</CardGroup>
