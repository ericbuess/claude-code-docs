---
description: Search Claude documentation using natural language queries
---

You are helping the user search through locally mirrored Claude documentation.

When the user provides a query:
1. Use the lookup_paths.py script to search for relevant paths
2. Read the paths_manifest.json to find matching documentation
3. Read the actual markdown files from the docs/ directory
4. Present the most relevant information
5. Suggest related documentation pages

Example usage:
- User: "how do I use tool use with python?"
- You should: Search for "tool use python", find relevant paths like /en/docs/build-with-claude/tool-use, read the content, and provide a helpful summary with code examples

The documentation is located in: /home/rudycosta3/claude-code-docs/docs/
The path manifest is: /home/rudycosta3/claude-code-docs/paths_manifest.json
Search utility: /home/rudycosta3/claude-code-docs/scripts/lookup_paths.py

Always cite the specific documentation page you're referencing.
