> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Add components to a plugin

> Add skills, hooks, MCP servers, and every other component type to a Claude Code plugin, with an example that validates for each.

export const Piece = ({id, children}) => <div className="pe-piece" data-piece={id}>{children}</div>;

export const PluginExplorer = ({children}) => {
  const PIECES = [{
    id: 'manifest',
    name: 'Manifest',
    path: '.claude-plugin/plugin.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: '.claude-plugin/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'plugin.json'
    }],
    href: '/en/plugins/manifest-reference#manifest-file',
    linkText: 'Go to the manifest reference'
  }, {
    id: 'skills',
    name: 'Skills',
    path: 'skills/review/SKILL.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'skills/'
    }, {
      depth: 1,
      kind: 'folder',
      text: 'review/'
    }, {
      depth: 2,
      kind: 'file',
      text: 'SKILL.md'
    }],
    href: '/en/plugins/components#skills',
    linkText: 'Go to the Skills section'
  }, {
    id: 'commands',
    name: 'Commands',
    path: 'commands/about.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'commands/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'about.md'
    }],
    href: '/en/plugins/components#commands',
    linkText: 'Go to the Commands section'
  }, {
    id: 'agents',
    name: 'Agents',
    path: 'agents/security-reviewer.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'agents/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'security-reviewer.md'
    }],
    href: '/en/plugins/components#agents',
    linkText: 'Go to the Agents section'
  }, {
    id: 'hooks',
    name: 'Hooks',
    path: 'hooks/hooks.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'hooks/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'hooks.json'
    }],
    href: '/en/plugins/components#hooks',
    linkText: 'Go to the Hooks section'
  }, {
    id: 'monitors',
    name: 'Monitors',
    path: 'monitors/monitors.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'monitors/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'monitors.json'
    }],
    href: '/en/plugins/components#monitors',
    linkText: 'Go to the Monitors section'
  }, {
    id: 'output-styles',
    name: 'Output styles',
    path: 'output-styles/terse.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'output-styles/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'terse.md'
    }],
    href: '/en/plugins/components#themes-and-output-styles',
    linkText: 'Go to the Themes and output styles section'
  }, {
    id: 'themes',
    name: 'Themes',
    path: 'themes/dracula.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'themes/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'dracula.json'
    }],
    href: '/en/plugins/components#themes-and-output-styles',
    linkText: 'Go to the Themes and output styles section'
  }, {
    id: 'workflows',
    name: 'Workflows',
    path: 'workflows/audit-routes.js',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'workflows/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'audit-routes.js'
    }],
    href: '/en/workflows#distribute-a-workflow-in-a-plugin',
    linkText: 'Go to Distribute a workflow in a plugin'
  }, {
    id: 'bin',
    name: 'Executables',
    path: 'bin/hello-plugin',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'bin/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'hello-plugin'
    }],
    href: '/en/plugins/components#executables',
    linkText: 'Go to the Executables section'
  }, {
    id: 'scripts',
    name: 'Scripts',
    path: 'scripts/format.sh',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'scripts/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'format.sh'
    }],
    href: '/en/plugins/components#hooks',
    linkText: 'Go to the Hooks section'
  }, {
    id: 'settings',
    name: 'Default settings',
    path: 'settings.json',
    lines: [{
      depth: 0,
      kind: 'file',
      text: 'settings.json'
    }],
    href: '/en/plugins/components#default-settings',
    linkText: 'Go to the Default settings section'
  }, {
    id: 'mcp',
    name: 'MCP servers',
    path: '.mcp.json',
    lines: [{
      depth: 0,
      kind: 'file',
      text: '.mcp.json'
    }],
    href: '/en/plugins/components#mcp-servers',
    linkText: 'Go to the MCP servers section'
  }, {
    id: 'lsp',
    name: 'LSP servers',
    path: '.lsp.json',
    lines: [{
      depth: 0,
      kind: 'file',
      text: '.lsp.json'
    }],
    href: '/en/plugins/components#lsp-servers',
    linkText: 'Go to the LSP servers section'
  }];
  const [selectedId, setSelectedId] = useState('manifest');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const rootRef = useRef(null);
  useEffect(() => {
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => document.removeEventListener('fullscreenchange', onFsChange);
  }, []);
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen(); else rootRef.current.requestFullscreen().catch(() => {});
  };
  const selected = PIECES.find(p => p.id === selectedId) || PIECES[0];
  const onTreeKeyDown = e => {
    const keys = ['ArrowDown', 'ArrowUp', 'Home', 'End'];
    if (keys.indexOf(e.key) === -1) return;
    const i = PIECES.findIndex(p => p.id === selectedId);
    let next = i;
    if (e.key === 'ArrowDown') next = Math.min(PIECES.length - 1, i + 1);
    if (e.key === 'ArrowUp') next = Math.max(0, i - 1);
    if (e.key === 'Home') next = 0;
    if (e.key === 'End') next = PIECES.length - 1;
    e.preventDefault();
    if (next === i) return;
    const id = PIECES[next].id;
    setSelectedId(id);
    const el = document.getElementById('pe-node-' + id);
    if (el) el.focus();
  };
  const FolderIcon = () => <svg className="pe-icon" width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M1.5 4.5a1 1 0 0 1 1-1h3.2l1.3 1.5h6a1 1 0 0 1 1 1V12a1 1 0 0 1-1 1h-10.5a1 1 0 0 1-1-1z" />
    </svg>;
  const FileIcon = () => <svg className="pe-icon" width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 1.5h5.5L13 5v9.5H4z" />
      <path d="M9.5 1.5V5H13" />
    </svg>;
  return <div ref={rootRef} className={isFullscreen ? 'pe-root pe-fullscreen not-prose' : 'pe-root not-prose'} data-selected={selected.id}>
      <style>{`
        .pe-root {
          --pe-mono: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
          --pe-accent: #D97757;
          --pe-accent-text: #A8502F;
          --pe-accent-bg: rgba(217,119,87,0.10);
          --pe-bg: #FFFFFF;
          --pe-surface: #FAFAF7;
          --pe-hover: #F0EEE6;
          --pe-border: #E8E6DC;
          --pe-text: #141413;
          --pe-text-2: #3D3D3A;
          --pe-text-3: #5E5D59;
          font-family: inherit;
          background: var(--pe-bg);
          color: var(--pe-text);
          border: 1px solid var(--pe-border);
          border-radius: 12px;
          margin: 1.5rem 0;
          overflow: hidden;
          box-sizing: border-box;
        }
        .dark .pe-root {
          --pe-accent-text: #EBA98F;
          --pe-accent-bg: rgba(217,119,87,0.18);
          --pe-bg: #1A1918;
          --pe-surface: #232221;
          --pe-hover: #2E2D2B;
          --pe-border: #3A3936;
          --pe-text: #F1EFE9;
          --pe-text-2: #D6D4CA;
          --pe-text-3: #B8B5AD;
        }
        .pe-root *, .pe-root *::before, .pe-root *::after { box-sizing: border-box; }
        .pe-head { display: flex; align-items: flex-start; gap: 12px; padding: 18px 24px 16px; border-bottom: 1px solid var(--pe-border); }
        .pe-head-text { flex: 1; min-width: 0; }
        .pe-fs-btn { flex-shrink: 0; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--pe-border); border-radius: 6px; background: var(--pe-surface); color: var(--pe-text-2); font-size: 15px; line-height: 1; cursor: pointer; }
        .pe-fs-btn:hover { background: var(--pe-hover); }
        .pe-fs-btn:focus-visible { outline: 2px solid var(--pe-accent); outline-offset: 2px; }
        .pe-fullscreen { border-radius: 0; height: 100vh; display: flex; flex-direction: column; overflow: auto; }
        .pe-fullscreen .pe-body { flex: 1; }
        .pe-title { font-size: 19px; font-weight: 600; line-height: 1.3; color: var(--pe-text); margin: 0; }
        .pe-sub { font-size: 15px; line-height: 1.5; color: var(--pe-text-3); margin: 4px 0 0; }
        .pe-sub code { font-family: var(--pe-mono); font-size: 0.88em; padding: 1px 5px; border-radius: 4px; background: var(--pe-surface); border: 1px solid var(--pe-border); }
        .pe-body { display: flex; align-items: stretch; }
        .pe-tree-pane { width: 270px; flex-shrink: 0; background: var(--pe-surface); border-right: 1px solid var(--pe-border); padding: 16px 0 12px; }
        .pe-panel { flex: 1; min-width: 0; padding: 16px 24px 24px; }
        .pe-caption { font-size: 13px; font-weight: 600; color: var(--pe-text-3); margin: 0 0 10px; }
        .pe-tree-pane .pe-caption { padding: 0 16px; }
        .pe-rootline { display: flex; align-items: center; gap: 7px; padding: 3px 16px; font-family: var(--pe-mono); font-size: 13.5px; color: var(--pe-text-3); }
        .pe-node {
          display: block; width: 100%; margin: 0; padding: 3px 16px 3px 30px; text-align: left; cursor: pointer;
          background: transparent; color: var(--pe-text-2);
          border: none; border-left: 3px solid transparent;
          font-family: var(--pe-mono); font-size: 13.5px; line-height: 1.4;
        }
        .pe-node:hover { background: var(--pe-hover); }
        .pe-node:focus-visible { outline: 2px solid var(--pe-accent); outline-offset: -2px; }
        .pe-node[aria-pressed="true"] { background: var(--pe-accent-bg); border-left-color: var(--pe-accent); color: var(--pe-accent-text); font-weight: 600; }
        .pe-line { display: flex; align-items: center; gap: 7px; padding: 2px 0; }
        .pe-line-tree { flex-wrap: wrap; }
        .pe-line-tree .pe-req { flex-basis: 100%; margin: 2px 0 0 22px; white-space: normal; width: fit-content; max-width: calc(100% - 22px); }
        .pe-line span { overflow-wrap: anywhere; }
        .pe-piece { display: none; font-size: 16px; line-height: 1.6; color: var(--pe-text-2); }
        .pe-root[data-selected="manifest"] .pe-piece[data-piece="manifest"],
        .pe-root[data-selected="skills"] .pe-piece[data-piece="skills"],
        .pe-root[data-selected="commands"] .pe-piece[data-piece="commands"],
        .pe-root[data-selected="agents"] .pe-piece[data-piece="agents"],
        .pe-root[data-selected="hooks"] .pe-piece[data-piece="hooks"],
        .pe-root[data-selected="monitors"] .pe-piece[data-piece="monitors"],
        .pe-root[data-selected="output-styles"] .pe-piece[data-piece="output-styles"],
        .pe-root[data-selected="themes"] .pe-piece[data-piece="themes"],
        .pe-root[data-selected="workflows"] .pe-piece[data-piece="workflows"],
        .pe-root[data-selected="bin"] .pe-piece[data-piece="bin"],
        .pe-root[data-selected="scripts"] .pe-piece[data-piece="scripts"],
        .pe-root[data-selected="settings"] .pe-piece[data-piece="settings"],
        .pe-root[data-selected="mcp"] .pe-piece[data-piece="mcp"],
        .pe-root[data-selected="lsp"] .pe-piece[data-piece="lsp"] { display: block; }
        .pe-piece p { margin: 0 0 10px; }
        .pe-piece p:last-child { margin-bottom: 0; }
        .pe-piece code { font-family: var(--pe-mono); font-size: 0.88em; padding: 1px 5px; border-radius: 4px; background: var(--pe-surface); border: 1px solid var(--pe-border); }
        .pe-piece .code-block { margin: 12px 0 0; }
        .pe-piece pre code { padding: 0; border: none; background: none; }
        .pe-piece a { color: var(--pe-accent-text); }
        .pe-line-compact { display: none; }
        .pe-icon { flex-shrink: 0; }
        .pe-req { margin-left: 8px; padding: 0 6px; border-radius: 999px; font-size: 11px; line-height: 18px; letter-spacing: .02em; color: var(--pe-accent-text); border: 1px solid var(--pe-border); background: var(--pe-surface); white-space: nowrap; font-weight: 500; vertical-align: middle; }
        .pe-name { font-size: 22px; font-weight: 600; line-height: 1.25; letter-spacing: -0.2px; color: var(--pe-text); margin: 0; }
        .pe-path { font-family: var(--pe-mono); font-size: 13.5px; color: var(--pe-accent-text); margin: 4px 0 0; overflow-wrap: anywhere; }
        .pe-block { margin: 20px 0 0; }
        .pe-link {
          display: inline-block; margin: 24px 0 0; padding: 8px 14px; border-radius: 8px;
          font-size: 14.5px; font-weight: 600; text-decoration: none;
          color: var(--pe-accent-text); background: var(--pe-accent-bg); border: 1px solid var(--pe-accent);
        }
        .pe-link:hover { filter: brightness(0.97); }
        .pe-link:focus-visible { outline: 2px solid var(--pe-accent); outline-offset: 2px; }
        @media (max-width: 700px) {
          .pe-head { padding: 16px 16px 14px; }
          .pe-body { flex-direction: column; }
          .pe-tree-pane { width: 100%; border-right: none; border-bottom: 1px solid var(--pe-border); }
          .pe-line-tree { display: none; }
          .pe-line-compact { display: flex; }
          .pe-panel { padding: 16px 16px 20px; }
        }
      `}</style>

      <div className="pe-head">
        <div className="pe-head-text">
          <div className="pe-title">What goes in a plugin</div>
          <div className="pe-sub">This example plugin, <code>my-plugin</code>, has one of every kind of component, each in its default location. Select a file or folder to read what it’s for and see what goes in it.</div>
        </div>
        <button type="button" className="pe-fs-btn" onClick={toggleFullscreen} aria-label={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'} title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}>
          {isFullscreen ? '⤡' : '⛶'}
        </button>
      </div>

      <div className="pe-body">
        <div className="pe-tree-pane">
          <div className="pe-caption" id="pe-tree-caption">Plugin directory</div>
          <div role="group" aria-labelledby="pe-tree-caption" onKeyDown={onTreeKeyDown}>
            <div className="pe-rootline"><FolderIcon /><span>my-plugin/</span></div>
            {PIECES.map(p => <button key={p.id} id={'pe-node-' + p.id} type="button" className="pe-node" aria-pressed={p.id === selected.id} aria-label={p.name + ', ' + p.path} onClick={() => setSelectedId(p.id)}>
                {p.lines.map((line, i) => <span key={i} className="pe-line pe-line-tree" style={{
    paddingLeft: line.depth * 18 + 'px'
  }}>
                    {line.kind === 'folder' ? <FolderIcon /> : <FileIcon />}
                    <span>{line.text}</span>
                    {p.required && i === p.lines.length - 1 ? <span className="pe-req">{p.required}</span> : null}
                  </span>)}
                <span className="pe-line pe-line-compact">
                  <FileIcon />
                  <span>{p.path}</span>
                  {p.required ? <span className="pe-req">{p.required}</span> : null}
                </span>
              </button>)}
          </div>
        </div>

        <div className="pe-panel" role="region" aria-labelledby="pe-panel-caption" aria-live="polite" aria-atomic="true">
          <div className="pe-caption" id="pe-panel-caption">Selected piece</div>
          <div className="pe-name">{selected.name}{selected.required ? <span className="pe-req">{selected.required}</span> : null}</div>
          <div className="pe-path">{selected.path}</div>

          <div className="pe-block">{children}</div>

          <a className="pe-link" href={selected.href}>{selected.linkText}</a>
        </div>
      </div>
    </div>;
};

A Claude Code plugin is built from components, such as skills, agents, hooks, and MCP servers. Each component has a default folder in the plugin, an optional manifest key in `.claude-plugin/plugin.json` that replaces or adds to that folder, and a name the user sees. For each key's full field table, see the [manifest reference](/docs/en/plugins/manifest-reference#fields).

Use this page to add a component to a plugin that already loads.

After you add a component, run `/reload-plugins` in a running session or start a new one so Claude Code loads it. To check the component's file before loading it, run [`claude plugin validate .`](/docs/en/plugins/cli-reference#plugin-validate) in your shell from the plugin directory.

<Note>
  These cases are covered on other pages:

  * **Building your first plugin**: start with [Create a plugin](/docs/en/plugins/create)
  * **Installing someone else's plugin**: see [Install plugins](/docs/en/plugins/install)
  * **Your plugin's users are on claude.ai or in Cowork**: a different set of components loads there. See [Plugins on claude.ai and in Cowork](https://claude.com/docs/plugins/overview)
</Note>

## Explore the plugin directory

The explorer shows an example plugin, `my-plugin`, that has one of every kind of component in its default location:

* A review skill and an `about` command
* A security-review subagent
* A hook that formats files after Claude edits them, and the `scripts/` folder it calls
* A log monitor
* An output style and a color theme
* A route-audit workflow
* A `hello-plugin` executable
* Default settings
* A local MCP server and a Go language server

Each file is the smallest valid example of its format, there to show the shape rather than to be useful: a real skill or agent carries full instructions and often supporting files, and a real hook or monitor does real work. The sections after the explorer use the same files as their examples and link to fuller ones. Select a file or folder to read what it's for, see what goes in it, and find the section that covers it.

<PluginExplorer>
  <Piece id="manifest">
    The [manifest](/docs/en/plugins/manifest-reference) is the `plugin.json` file in a plugin's `.claude-plugin/` directory. It contains the plugin's metadata and the `userConfig` values that Claude Code prompts the user for. Only `name` is required. In this one, `description` is the text users see for the plugin in `/plugin`, and `version` keeps users on that version until you change it:

    ```json theme={null}
    {
      "name": "my-plugin",
      "version": "1.0.0",
      "description": "Review, formatting, and database tools for this team"
    }
    ```
  </Piece>

  <Piece id="skills">
    A [skill](/docs/en/skills) is a `SKILL.md` file. Save each skill in its own directory under `skills/`. Claude reads every skill's `description`, and when what the user asks for matches it, such as asking Claude to review a pull request here, Claude loads the skill's instructions and follows them. The user can also run it directly as `/my-plugin:review`:

    ```markdown theme={null}
    ---
    description: Reviews a pull request for style and test coverage. Use when asked to review code.
    ---

    Review the changed files. Report style problems first, then missing tests.
    ```
  </Piece>

  <Piece id="commands">
    A command is a single Markdown file the user runs by name. Commands are the older format: a skill runs by name the same way and can also carry supporting files in its own directory, so write new ones as skills and keep `commands/` for files you already have. This file becomes `/my-plugin:about` and takes the same frontmatter as a skill:

    ```markdown theme={null}
    ---
    description: Summarize the repository
    ---

    Summarize what this repository does in three sentences.
    ```
  </Piece>

  <Piece id="agents">
    A [subagent](/docs/en/sub-agents) is a separate assistant, with its own instructions and its own context window, that Claude can delegate a task to and get a result back from. Each Markdown file under `agents/` defines one: the frontmatter names it and says when to use it, and the body is its system prompt. This one is named `my-plugin:security-reviewer`, and the user can invoke it with `@agent-my-plugin:security-reviewer`:

    ```markdown theme={null}
    ---
    name: security-reviewer
    description: Reviews code changes for security issues. Use after edits to authentication or input handling.
    model: sonnet
    ---

    You are a security reviewer. Read the changed files and report injection, authentication, and secrets-handling risks.
    ```
  </Piece>

  <Piece id="hooks">
    A [hook](/docs/en/hooks-guide) runs something automatically at a point in Claude Code's lifecycle, such as after every file edit: a shell command, an HTTP request, an MCP tool call, a prompt to a model, or a subagent. Save the plugin's hooks in `hooks/hooks.json` at the plugin root. This one runs the plugin's `scripts/format.sh` after Claude writes or edits a file:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Piece>

  <Piece id="monitors">
    A monitor is a shell command that Claude Code starts in the background when the session starts and keeps running until it ends, using the [Monitor tool](/docs/en/tools-reference#monitor-tool). What it prints reaches Claude as notifications. A `when` field can instead start it the first time a named skill runs. This one tails an error log:

    ```json theme={null}
    [
      {
        "name": "error-log",
        "command": "tail -F ./logs/error.log",
        "description": "Application error log"
      }
    ]
    ```
  </Piece>

  <Piece id="output-styles">
    A plugin can include [output styles](/docs/en/output-styles), which change how Claude formats and phrases its replies. Save each output style as `output-styles/<name>.md`. This one appears in `/output-style` as `my-plugin:terse`:

    ```markdown theme={null}
    ---
    name: terse
    description: Answer in as few words as possible
    keep-coding-instructions: true
    ---

    Keep every reply short. Skip preambles and summaries.
    ```
  </Piece>

  <Piece id="themes">
    A plugin can include [color themes](/docs/en/terminal-config#create-a-custom-theme) for the Claude Code interface. Save each theme as `themes/<slug>.json`. This one appears in `/theme` as `Dracula`, marked as from `my-plugin`:

    ```json theme={null}
    {
      "name": "Dracula",
      "base": "dark",
      "overrides": {
        "claude": "#bd93f9",
        "error": "#ff5555"
      }
    }
    ```
  </Piece>

  <Piece id="workflows">
    The `workflows/` folder holds [workflow](/docs/en/workflows) `.js` files: a `meta` block, then a script body that orchestrates several subagents. This one runs as `/my-plugin:audit-routes`:

    ```javascript theme={null}
    export const meta = {
      name: 'audit-routes',
      description: 'Audit every route handler for missing auth checks',
    }

    const found = await agent('List every .ts file under src/routes/.', {
      schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } },
    })

    const audits = await pipeline(found.files, file =>
      agent(`Audit ${file} for missing authentication checks.`, { label: file }),
    )

    return audits.filter(Boolean)
    ```
  </Piece>

  <Piece id="bin">
    `bin/` is how a plugin ships a command-line tool. While the plugin is enabled, Claude Code puts this folder on the `PATH` of the shell it runs commands in, so Claude, or a skill's instructions, can run the tool by name without the user installing anything. With this [executable](#executables) in place, `hello-plugin` is a command Claude can run:

    ```bash theme={null}
    #!/bin/bash
    echo "hello from my-plugin"
    ```
  </Piece>

  <Piece id="scripts">
    The hook in `hooks/hooks.json` runs a script, and this folder is where the example keeps it. The name `scripts/` is a convention, not something Claude Code looks for: the hook points at the file by its path, `${CLAUDE_PLUGIN_ROOT}/scripts/format.sh`. A formatter script might look like this:

    ```bash theme={null}
    #!/bin/bash
    npx prettier --write .
    ```
  </Piece>

  <Piece id="settings">
    A `settings.json` at the plugin root holds [settings](/docs/en/settings-reference) that apply while the plugin is enabled, so a plugin can change how the session behaves and not only add components. Only two keys take effect from a plugin, [`agent`](/docs/en/settings-reference#agent) and [`subagentStatusLine`](/docs/en/settings-reference#subagentstatusline); every other key is dropped. See [Default settings](#default-settings).

    This one sets `agent`, which runs the session's main thread as the plugin's own `security-reviewer` agent, so that agent's system prompt, tool restrictions, and model apply to the whole session:

    ```json theme={null}
    {
      "agent": "security-reviewer"
    }
    ```
  </Piece>

  <Piece id="mcp">
    An [MCP server](/docs/en/mcp) gives Claude tools from an external system. Declare it in `.mcp.json` at the plugin root. This one starts a local server from a script inside the plugin, and appears in `/mcp` as `plugin:my-plugin:db`:

    ```json theme={null}
    {
      "mcpServers": {
        "db": {
          "command": "node",
          "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
        }
      }
    }
    ```
  </Piece>

  <Piece id="lsp">
    An LSP server gives Claude [diagnostics and code navigation](/docs/en/plugins/code-intelligence) for a language. Declare the server in `.lsp.json` at the plugin root. This one connects the Go language server for `.go` files:

    ```json theme={null}
    {
      "gopls": {
        "command": "gopls",
        "args": ["serve"],
        "extensionToLanguage": {
          ".go": "go"
        }
      }
    }
    ```
  </Piece>
</PluginExplorer>

## Add each kind of component

Each section below covers one kind of component: where its files go in the plugin, an example that validates, what the user sees once the plugin loads, and the manifest key that changes the default location. Add the ones your plugin needs; none is required.

### Skills

A [skill](/docs/en/skills) is a `SKILL.md` file that Claude can load when its description matches the task. The user can also run it as a command. Save each skill in its own directory under `skills/`:

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── review/
        └── SKILL.md
```

Give the `SKILL.md` a `description` so Claude knows when to use it:

```markdown skills/review/SKILL.md theme={null}
---
description: Reviews a pull request for style and test coverage. Use when asked to review code.
---

Review the changed files. Report style problems first, then missing tests.
```

After you load the plugin, `/my-plugin:review` runs the skill. The command name and who can invoke it follow these rules:

* **Command name**: `/<plugin>:<directory>`, so `skills/review/SKILL.md` in `my-plugin` is `/my-plugin:review`. If you set `name` in the frontmatter, it replaces the last segment and the plugin prefix stays. See [how a skill gets its command name](/docs/en/skills#how-a-skill-gets-its-command-name)
* **Who invokes it**: Claude, the user, or both, controlled by frontmatter. See [Control who invokes a skill](/docs/en/skills#control-who-invokes-a-skill)

You can also place skills outside the default `skills/` directory:

* **Additional directories**: list them in the `skills` manifest key. They add to the default `skills/` scan rather than replacing it, unlike `commands` and `agents`
* **A single skill at the plugin root**: with no `skills/` directory and no `skills` manifest key, a `SKILL.md` at the plugin root loads as one skill. Set `name` in its frontmatter, because otherwise a marketplace install names the skill after its [cache directory](/docs/en/plugins/loading#find-plugins-on-disk) rather than your plugin

To include instructions in a plugin, write them as a skill. Claude Code doesn't load a `CLAUDE.md` at the plugin root, and `claude plugin validate` warns `CLAUDE.md at the plugin root is not loaded as project context`.

For frontmatter fields and supporting files, see [Skills](/docs/en/skills).

### Commands

A command is a single Markdown file the user runs by name, such as `/my-plugin:about`.

<Note>
  Commands are the older format, and [skills](#skills) supersede them for new work. A skill runs by name the same way, and it can also carry supporting files in its directory. Keep `commands/` for files you're moving over from `.claude/commands/`.
</Note>

Save a command at `commands/<file>.md` and it becomes `/<plugin>:<file>`. A subdirectory adds a segment, so `commands/db/migrate.md` is `/my-plugin:db:migrate`.

Command files take the same frontmatter as skills.

#### Define commands in the manifest

You only need this if you want to keep command files somewhere other than `commands/`, or to define a short command inside `plugin.json` without a separate Markdown file. Set the `commands` manifest key, and Claude Code reads it instead of scanning `commands/`. The key takes a path, an array of paths, or an object that maps each command name to either a `source` file or inline `content`.

This manifest defines `/my-plugin:about` inline, with no Markdown file:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "commands": {
    "about": {
      "content": "Summarize what this repository does in three sentences.",
      "description": "Summarize the repository"
    }
  }
}
```

Load the plugin and run `/my-plugin:about` in the session to confirm it loaded.

For the full key syntax, see [`commands`](/docs/en/plugins/manifest-reference#commands).

### Agents

A [subagent](/docs/en/sub-agents) is a separate assistant, with its own instructions and context window, that Claude can delegate a task to. Each Markdown file under `agents/` defines one:

```markdown agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code changes for security issues. Use after edits to authentication or input handling.
model: sonnet
---

You are a security reviewer. Read the changed files and report injection, authentication, and secrets-handling risks.
```

This agent is named `my-plugin:security-reviewer`, and the user can [invoke it explicitly](/docs/en/sub-agents#invoke-subagents-explicitly) with `@agent-my-plugin:security-reviewer`. The name form is `<plugin>:<name>`, where `<name>` comes from the frontmatter, or from the file name when there is none.

The `agents` manifest key replaces the `agents/` scan.

#### Organize agents in subfolders

You can put plugin agent files in subfolders of `agents/`. Claude Code [loads them recursively](/docs/en/sub-agents#choose-the-subagent-scope) and joins the plugin name, each subfolder name, and the file name with colons to form the agent's scoped name. For example, `agents/review/security.md` in a plugin named `my-plugin` loads as `my-plugin:review:security`. Two settings change that name:

* Frontmatter `name`: it replaces only the file name, so `name: audit` in `agents/review/security.md` loads as `my-plugin:review:audit`
* Manifest [`agents`](/docs/en/plugins/manifest-reference#fields) field: a file you list there loads without subfolder names, so `"agents": "./custom/review/security.md"` loads as `my-plugin:security`

#### Frontmatter fields in plugin agents

A plugin agent's frontmatter follows these rules:

* **Supported fields**: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `omitClaudeMd`, `isolation`, `color`, and the `cacheTtl` key of `experimental`. The only valid `isolation` value is `"worktree"`. See [supported frontmatter fields](/docs/en/sub-agents#supported-frontmatter-fields) for what each one does
* **Ignored fields**: `permissionMode`, `hooks`, `mcpServers`, and `initialPrompt`. An agent file can't add hooks or MCP servers on its own, so add those as plugin [hooks](#hooks) and [MCP servers](#mcp-servers) instead
* **Frontmatter that doesn't parse**: the agent still loads with every field ignored. It's named after the file, and its description reads `Agent from my-plugin plugin`. Run [`claude plugin validate`](/docs/en/plugins/cli-reference#plugin-validate) in your shell to find these files

For what each field does and the precedence rules, see [Subagents](/docs/en/sub-agents#supported-frontmatter-fields).

### Hooks

A [hook](/docs/en/hooks-guide) runs something automatically at a point in Claude Code's lifecycle, such as after every file edit: a shell command, an HTTP request, an MCP tool call, a prompt to a model, or a subagent. Save the plugin's hooks in `hooks/hooks.json` at the plugin root, under a top-level `"hooks"` key, in the same shape as the `hooks` object in `settings.json`. That lets you copy an existing settings hook in unchanged.

This hook runs a bundled script after every `Write` or `Edit`:

```json hooks/hooks.json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh\""
          }
        ]
      }
    ]
  }
}
```

Save the script at `scripts/format.sh` and make it executable.

Load the plugin and ask Claude to edit a file. A `PostToolUse` hook that exits 0 shows nothing in the transcript, so confirm it ran with [debug logging](/docs/en/hooks#debug-hooks) or by what the script itself changes.

Hooks in `hooks/hooks.json` and in the `hooks` manifest key both load. For every event and its payload, see [Hook events](/docs/en/hooks#hook-events).

#### When plugin hooks fire

A plugin's hooks don't wait for one of the plugin's skills or commands to be used. Claude Code registers them when a session loads the plugin, and they fire on their events from then on. To limit when a hook runs, narrow its `matcher`.

If a hook never fires, see [hooks that don't fire](/docs/en/plugins/troubleshooting#failed-to-load-hooks-from-and-hooks-that-dont-fire).

#### Environment, quoting, and matching MCP tools

The hook's environment, the quoting of `${CLAUDE_PLUGIN_ROOT}`, and matchers for the plugin's own MCP tools work as follows:

* **Environment**: every hook process receives `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` in its environment, plus `CLAUDE_PLUGIN_OPTION_<KEY>` for each [user configuration](#user-configuration) value, so your script can read them from there
* **Quoting**: when `command` has no `args`, it runs through a shell, so wrap the `${CLAUDE_PLUGIN_ROOT}` path in double quotes, as the `hooks/hooks.json` example under [Hooks](#hooks) does, to keep the expanded path one shell word. When you pass `args` instead, each element is passed as one argument with no shell and needs no quoting. See [exec form and shell form](/docs/en/hooks#exec-form-and-shell-form)
* **Matching the plugin's own MCP tools**: a tool from an [MCP server this plugin declares](#mcp-servers) is named `mcp__plugin_<plugin>_<server>__<tool>`, so write that full name in the matcher. A matcher on the server name alone never fires. See [Match MCP tools](/docs/en/hooks#match-mcp-tools)

### MCP servers

An MCP server gives Claude tools from an external system. Declare it in `.mcp.json` at the plugin root, in the same shape as a [project `.mcp.json`](/docs/en/mcp#project-scope). This `.mcp.json` declares one server named `db`:

```json .mcp.json theme={null}
{
  "mcpServers": {
    "db": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
    }
  }
}
```

You can also omit the `mcpServers` wrapper and put `db` at the top level of the file.

Load the plugin and run `/mcp` to confirm the server appears as `plugin:my-plugin:db`.

`claude plugin validate` checks `.mcp.json` and reports a server entry that Claude Code would drop at load time as an error. Requires Claude Code v2.1.281 or later.

For where a bad entry shows up at load time, see [MCP servers that don't start](/docs/en/plugins/troubleshooting#invalid-mcp-server-config-for-and-mcp-servers-that-dont-start).

The `mcpServers` manifest key takes an inline server map, a path to a JSON file, or an array of those. When a manifest server has the same name as one in `.mcp.json`, the manifest server replaces it.

#### Reach users on claude.ai and Cowork

A local stdio server, such as the `db` server under [MCP servers](#mcp-servers), runs in Claude Code and in a Cowork session that runs on your machine in the Claude Desktop app, but not on claude.ai. To reach users there too, reference a remote server by its `https://` URL, which claude.ai and Cowork offer to the user as a connector.

#### Server names, tool names, and reloads

The server's names, variable substitution, and reload behavior follow these rules:

* **Server name**: `plugin:<plugin>:<server>`, so the `db` server in `my-plugin` is `plugin:my-plugin:db` in `/mcp`. Use the same form to name the server in an [`mcp_tool` hook](/docs/en/hooks#mcp-tool-hook-fields)
* **Tool names**: `mcp__plugin_<plugin>_<server>__<tool>`, so a `query` tool on that `db` server is `mcp__plugin_my-plugin_db__query`. That is the name to use in [permission rules](/docs/en/permissions) and [hook matchers](#hooks)
* **Substitution**: `${CLAUDE_PLUGIN_ROOT}` and the other [path variables](#path-variables-and-persistent-data) are substituted in `command`, `args`, and `env`. No quoting is needed in `args`, because each element is passed as one argument
* **Reload**: when the user runs `/reload-plugins` and [the reload applies](/docs/en/plugins/cli-reference#reloads-that-change-mcp-tools), a server whose configuration is unchanged keeps its connection. A server whose configuration changed reconnects, and one you removed disconnects

#### Include a packaged MCPB server

The `mcpServers` key also accepts a packaged server as an [MCPB file](https://github.com/modelcontextprotocol/mcpb), whose extension is `.mcpb` or the older `.dxt`. Point the key at the file, as a path inside the plugin or an `https://` URL:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "mcpServers": "./servers/db.mcpb"
}
```

The server takes its name from the `name` in the bundle's manifest.

For transports and authentication, see [MCP](/docs/en/mcp#plugin-provided-mcp-servers).

### LSP servers

An LSP server gives Claude diagnostics and code navigation for a language. If an [official code intelligence plugin](/docs/en/plugins/code-intelligence) already covers your language, install that instead of writing one. Otherwise declare the server in `.lsp.json` at the plugin root:

```json .lsp.json theme={null}
{
  "gopls": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

The file maps each server name directly to its configuration, with no wrapper object around the map. `command` is the binary's name, with its arguments in `args`. `extensionToLanguage` needs at least one extension, each starting with `.`.

`claude plugin validate` doesn't read this file. When any entry is invalid, the whole file is skipped at load and `Invalid LSP server config for ".lsp.json"` appears in the `/plugin` **Errors** tab.

Your plugin configures the connection but doesn't install the server binary, and each file extension gets one server:

* **Missing binary**: Claude Code starts `command` by name from the user's `PATH`. When the binary isn't there, the server fails to start and `claude --debug` logs `LSP server <name> failed to start`
* **Extension conflicts**: when two enabled servers claim the same extension, the first registered handles those files and the other isn't used for them, whether the servers come from one plugin or two. The `/plugin` **Errors** tab shows the warning `LSP server "<name>" is not used for <ext> files`

The `lspServers` manifest key takes the same map inline, a path to a JSON file, or an array of those, and its servers add to the ones in `.lsp.json`. When a manifest server has the same name as one in `.lsp.json`, the manifest server replaces it.

For `transport`, timeouts, restarts, and the other fields, see [`lspServers`](/docs/en/plugins/manifest-reference#lspservers).

Send log output to stderr, not stdout. Claude Code reads a server's stdout as protocol messages only, and accepts message headers up to 64 KiB and a message body up to 32 MiB.

Claude Code disconnects a server that exceeds either limit or writes non-protocol output to stdout, and counts the disconnect as a crash for `restartOnCrash` and `maxRestarts`. When you run with `--debug`, Claude Code writes an error naming the cause to the debug log.

### Executables

Files in `bin/` at the plugin root are on the `PATH` of the Bash tool's shell while the plugin is enabled, so Claude can run them as bare commands. Add an executable script:

```bash bin/hello-plugin theme={null}
#!/bin/bash
echo "hello from my-plugin"
```

Make it executable with `chmod +x bin/hello-plugin` and load the plugin. When you ask Claude to run `hello-plugin`, the Bash tool result shows the script's output.

Plugin `bin/` directories come after the user's own `PATH` entries, so a plugin can't shadow `git`, `ls`, or another system command.

claude.ai and Cowork don't install a plugin that has a top-level `bin/` directory, including one you [distribute through claude.ai organization settings](/docs/en/plugins/host-marketplace#distribute-through-organization-settings).

### Default settings

To set defaults that apply while the plugin is enabled, add a `settings.json` at the plugin root, or put the same object inline in the `settings` manifest key. Two keys take effect, `agent` and `subagentStatusLine`, and every other key is dropped.

Set `agent` to run one of the plugin's own agents as the main thread:

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Load the plugin and start a session. Claude then answers in the main conversation with the `security-reviewer` agent's system prompt and model.

For everything the key controls, see the [`agent` setting](/docs/en/settings-reference#agent).

When the same key is set in more than one place, these rules decide which value applies:

* **File over manifest**: when both exist and `settings.json` sets at least one supported key, `settings.json` applies and the manifest's `settings` is ignored
* **User settings over plugin defaults**: across settings sources, plugin defaults are the lowest layer, so a user's own `agent` in `~/.claude/settings.json` overrides yours
* **Two plugins set the same key**: the value from the plugin loaded last applies, and `claude --debug` logs `overrides setting`

For the `subagentStatusLine` shape, see [subagent status lines](/docs/en/statusline#subagent-status-lines).

### Themes and output styles

A plugin can include color themes and output styles. Both appear in the same pickers as the user's own. For either one, setting the manifest key replaces the folder scan.

| Component    | Save as                   | Format                                                                                                                      | Appears in                            | Manifest key          |
| :----------- | :------------------------ | :-------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ | :-------------------- |
| Theme        | `themes/<slug>.json`      | The [custom theme file](/docs/en/terminal-config#create-a-custom-theme) format users write in `~/.claude/themes/`                | `/theme`, under the file's `name`     | `experimental.themes` |
| Output style | `output-styles/<name>.md` | The [custom output style](/docs/en/output-styles#create-a-custom-output-style) format, with `name` and `description` frontmatter | `/output-style`, as `<plugin>:<name>` | `outputStyles`        |

Plugin themes are read-only, so when a user edits one in `/theme`, the edit is saved as a copy in their own themes directory.

This theme recolors the prompt accent and error text on the dark preset:

```json themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555"
  }
}
```

### Channels

A [channel](/docs/en/channels) lets an outside system such as a chat app send messages into a session. In a plugin, a channel is one of the MCP servers plus a `channels` entry that binds to it and can prompt for its own configuration. This manifest binds a channel to a `telegram` server and asks for a bot token:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "telegram": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": { "BOT_TOKEN": "${user_config.bot_token}" }
    }
  },
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        }
      }
    }
  ]
}
```

`server` must match a key in `mcpServers`. The per-channel `userConfig` takes the same shape as the [top-level `userConfig` key](#user-configuration).

For what the server must implement and how users enable a channel plugin, see [Package as a plugin](/docs/en/channels-reference#package-as-a-plugin) in the channels reference. For the field table, see [`channels`](/docs/en/plugins/manifest-reference#channels).

### Monitors

A monitor is a shell command that runs in the background for the whole session. What it prints reaches Claude as notifications, so Claude can react to a log or a status change without being asked to watch it. Save the entries in `monitors/monitors.json`:

```json monitors/monitors.json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

The command runs in a shell, in the working directory the session started in.

A monitor's command is limited in where it starts and what it can reference:

* **Interactive sessions only**: plugin monitors start in an interactive session and never in non-interactive mode with the `-p` flag. They also start only where the [Monitor tool](/docs/en/tools-reference#monitor-tool) is available
* **No user configuration**: `command` gets the [path variables](#path-variables-and-persistent-data) and `${ENV_VAR}` from the environment, but never `${user_config.*}`. A monitor that references one doesn't start, and monitor processes don't receive `CLAUDE_PLUGIN_OPTION_<KEY>` either
* **Disabling mid-session**: if you disable a plugin mid-session, Claude Code doesn't stop monitors that are already running. They stop when the session ends

The `experimental.monitors` manifest key takes the same array inline or a path to a JSON file, and is read instead of `monitors/monitors.json`.

For the `when` trigger and the other fields, see [`monitors`](/docs/en/plugins/manifest-reference#monitors).

<h2 id="user-configuration">
  Ask the user for configuration values
</h2>

Declare the values your plugin needs from the user in the `userConfig` manifest key, so users don't edit `settings.json` themselves. Each option appears in a dialog with its `title` as the label and its `description` beneath it.

Set `"sensitive": true` for a token or password. The dialog then masks the input, and the value is stored in secure storage rather than `settings.json`.

This manifest asks for an endpoint and a token:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "userConfig": {
    "api_url": {
      "type": "string",
      "title": "API URL",
      "description": "Base URL of your team's API"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token for your team's API",
      "sensitive": true
    }
  }
}
```

### When the configuration dialog appears

The dialog appears only in the interactive `/plugin` interface. It opens for any option that isn't set yet when the user does any of the following:

* Installs the plugin in `/plugin`
* Runs `/plugin install <plugin>@<marketplace>` inside a session
* Enables the plugin from the **Installed** tab in `/plugin`

To open the same dialog at any time, the user runs `/plugin configure <plugin>@<marketplace>`.

The `claude plugin install` shell command never prompts for `userConfig` values. To set values from the shell, pass each one as `--config KEY=VALUE`. When options remain unset, the command prints a `userConfig options not yet set` line that names both ways to set them. [The `userConfig` dialog never appears](/docs/en/plugins/troubleshooting#the-userconfig-dialog-never-appears) quotes the line.

For the option fields, where each value is stored, how a component references a saved value, and which fields reject `${user_config.*}`, see [User configuration](/docs/en/plugins/manifest-reference#user-configuration).

<h2 id="path-variables-and-persistent-data">
  Reference plugin paths and store data
</h2>

You don't know where your plugin will be installed, so refer to its files and data through these variables rather than fixed paths. They're substituted in skill, command, and agent content, in hook and monitor commands, and in MCP and LSP server configurations. They're also exported to hook, MCP, and LSP processes:

* **`${CLAUDE_PLUGIN_ROOT}`**: the plugin's install directory. Each version has its own [cache directory](/docs/en/plugins/loading#find-plugins-on-disk), so the path changes when the plugin updates. Don't write state there
* **`${CLAUDE_PLUGIN_DATA}`**: a directory that survives updates, for `node_modules`, virtual environments, and caches. It resolves to `~/.claude/plugins/data/<id>/` and is created when first referenced
* **`${CLAUDE_PROJECT_DIR}`**: the project root, the same value hooks receive

In the data directory path, `<id>` is the plugin identifier with every character other than letters, digits, `_`, and `-` replaced by `-`, so `my-plugin@my-marketplace` becomes `my-plugin-my-marketplace`.

On Windows, the substituted paths use forward slashes so a shell doesn't read backslashes as escapes.

### Install dependencies into the data directory

For a marketplace-installed plugin, Claude Code installs eligible [Node.js package dependencies](/docs/en/plugins/loading#node-js-package-dependencies) automatically when it caches the plugin, so you may not need to install them yourself. When you do, this `SessionStart` hook installs `node_modules` into `${CLAUDE_PLUGIN_DATA}` on first run and again after an update changes `package.json`:

```json hooks/hooks.json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

After the first session, `~/.claude/plugins/data/<id>/node_modules` exists. An MCP server can then set `NODE_PATH` to `${CLAUDE_PLUGIN_DATA}/node_modules` in its `env`. For which fields substitute which variable, see [Environment variables](/docs/en/plugins/manifest-reference#environment-variables).

## Next steps

* [Plugin manifest reference](/docs/en/plugins/manifest-reference): `plugin.json` fields, path rules, and the standard layout
* [Test plugins with evals](/docs/en/plugin-evals): check that the components you added change Claude's behavior the way you intend
* [Publish and distribute a plugin](/docs/en/plugins/publish): version the plugin and put it in a marketplace
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting): what to do when a component doesn't load or a hook doesn't fire
