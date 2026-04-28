> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code overview

> Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.

export const InstallConfigurator = ({defaultSurface = 'terminal'}) => {
  const TERM = {
    mac: {
      label: 'macOS / Linux',
      cmd: 'curl -fsSL https://claude.ai/install.sh | bash'
    },
    win: {
      label: 'Windows'
    },
    brew: {
      label: 'Homebrew',
      cmd: 'brew install --cask claude-code'
    },
    winget: {
      label: 'WinGet',
      cmd: 'winget install Anthropic.ClaudeCode'
    }
  };
  const WIN_VARIANTS = {
    ps: 'irm https://claude.ai/install.ps1 | iex',
    cmd: 'curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd'
  };
  const TABS = [{
    key: 'terminal',
    label: 'Terminal'
  }, {
    key: 'desktop',
    label: 'Desktop'
  }, {
    key: 'vscode',
    label: 'VS Code'
  }, {
    key: 'jetbrains',
    label: 'JetBrains'
  }];
  const ALT_TARGETS = {
    desktop: {
      name: 'Desktop',
      tagline: 'The full agent in a native app for macOS and Windows.',
      installLabel: 'Download the app',
      installHref: 'https://claude.com/download?utm_source=claude_code&utm_medium=docs&utm_content=configurator_desktop_download',
      guideHref: '/en/desktop-quickstart'
    },
    vscode: {
      name: 'VS Code',
      tagline: 'Review diffs, manage context, and chat without leaving your editor.',
      installLabel: 'Install from Marketplace',
      installHref: 'https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code',
      altCmd: 'code --install-extension anthropic.claude-code',
      guideHref: '/en/vs-code'
    },
    jetbrains: {
      name: 'JetBrains',
      tagline: 'Native plugin for IntelliJ, PyCharm, WebStorm, and other JetBrains IDEs.',
      installLabel: 'Install from Marketplace',
      installHref: 'https://plugins.jetbrains.com/plugin/27310-claude-code-beta-',
      guideHref: '/en/jetbrains'
    }
  };
  const PROVIDERS = [{
    key: 'anthropic',
    label: 'Anthropic'
  }, {
    key: 'bedrock',
    label: 'Amazon Bedrock'
  }, {
    key: 'foundry',
    label: 'Microsoft Foundry'
  }, {
    key: 'vertex',
    label: 'Google Vertex AI'
  }];
  const PROVIDER_NOTICE = {
    bedrock: <>
        <strong>Configure your AWS account first.</strong> Running on Bedrock
        requires model access enabled in the AWS console and IAM credentials.{' '}
        <a href="/en/amazon-bedrock">Bedrock setup guide →</a>
      </>,
    vertex: <>
        <strong>Configure your GCP project first.</strong> Running on Vertex AI
        requires the Vertex API enabled and a service account with the right
        permissions.{' '}
        <a href="/en/google-vertex-ai">Vertex setup guide →</a>
      </>,
    foundry: <>
        <strong>Configure your Azure resources first.</strong> Running on
        Microsoft Foundry requires an Azure subscription with a Foundry resource
        and model deployments provisioned.{' '}
        <a href="/en/microsoft-foundry">Foundry setup guide →</a>
      </>
  };
  const iconCheck = (size = 14) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="20 6 9 17 4 12" />
    </svg>;
  const iconCopy = (size = 14) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="9" y="9" width="13" height="13" rx="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const iconArrowUpRight = (size = 14) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="7" y1="17" x2="17" y2="7" />
      <polyline points="7 7 17 7 17 17" />
    </svg>;
  const iconInfo = (size = 16) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="16" x2="12" y2="12" />
      <line x1="12" y1="8" x2="12.01" y2="8" />
    </svg>;
  const [target, setTarget] = useState(defaultSurface);
  const [team, setTeam] = useState(false);
  const [provider, setProvider] = useState('anthropic');
  const [pkg, setPkg] = useState(() => (/Win/).test(navigator.userAgent) ? 'win' : 'mac');
  const [winCmd, setWinCmd] = useState(false);
  const [copied, setCopied] = useState(null);
  const copyTimer = useRef(null);
  const handleCopy = async (text, key) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    clearTimeout(copyTimer.current);
    setCopied(key);
    copyTimer.current = setTimeout(() => setCopied(null), 1800);
  };
  const cardBodyCmd = (cmd, prompt) => {
    const on = copied === 'term';
    return <div className="cc-ic-card-body">
        <span className="cc-ic-prompt">{prompt || '$'}</span>
        <div className="cc-ic-cmd">{cmd}</div>
        <button type="button" className={'cc-ic-copy' + (on ? ' cc-ic-copied' : '')} onClick={() => handleCopy(cmd, 'term')}>
          {on ? iconCheck(13) : iconCopy(13)}
          <span>{on ? 'Copied' : 'Copy'}</span>
        </button>
      </div>;
  };
  const isWinInstaller = pkg === 'win';
  const isWinPrompt = pkg === 'win' || pkg === 'winget';
  const terminalCmd = isWinInstaller ? WIN_VARIANTS[winCmd ? 'cmd' : 'ps'] : TERM[pkg].cmd;
  const alt = ALT_TARGETS[target];
  const showNotice = team && provider !== 'anthropic';
  const STYLES = `
.cc-ic {
  --ic-slate: #141413;
  --ic-clay: #d97757;
  --ic-clay-deep: #c6613f;
  --ic-gray-000: #ffffff;
  --ic-gray-150: #f0eee6;
  --ic-gray-550: #73726c;
  --ic-gray-700: #3d3d3a;
  --ic-border-subtle: rgba(31, 30, 29, 0.08);
  --ic-border-default: rgba(31, 30, 29, 0.15);
  --ic-border-strong: rgba(31, 30, 29, 0.3);
  --ic-font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Courier New', monospace;
  font-family: 'Anthropic Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px; line-height: 1.5; color: var(--ic-slate);
  margin: 8px 0 32px;
}
.dark .cc-ic {
  --ic-slate: #f0eee6;
  --ic-gray-000: #262624;
  --ic-gray-150: #1f1e1d;
  --ic-gray-550: #91908a;
  --ic-gray-700: #bfbdb4;
  --ic-border-subtle: rgba(240, 238, 230, 0.08);
  --ic-border-default: rgba(240, 238, 230, 0.14);
  --ic-border-strong: rgba(240, 238, 230, 0.28);
}
.dark .cc-ic-check { background: transparent; }
.dark .cc-ic-card { border: 0.5px solid var(--ic-border-subtle); }
.dark .cc-ic-p-pill.cc-ic-active { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); }
.cc-ic *, .cc-ic *::before, .cc-ic *::after { box-sizing: border-box; }
.cc-ic a { text-decoration: none; }
.cc-ic a:not([class]) { color: inherit; }
.cc-ic button { font-family: inherit; cursor: pointer; }

.cc-ic-tab-strip {
  display: inline-flex; gap: 2px;
  padding: 4px; background: var(--ic-gray-150);
  border-radius: 10px; overflow-x: auto;
  max-width: 100%;
}
.cc-ic-tab {
  appearance: none; background: none; border: none;
  padding: 10px 18px; font-size: 15px; font-weight: 430;
  color: var(--ic-gray-550); border-radius: 7px;
  white-space: nowrap;
  transition: color 0.12s, background-color 0.12s;
}
.cc-ic-tab:hover { color: var(--ic-gray-700); }
.cc-ic-tab.cc-ic-active {
  color: var(--ic-slate); font-weight: 500;
  background: var(--ic-gray-000);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.dark .cc-ic-tab.cc-ic-active { box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4); }

.cc-ic-team-wrap { padding: 16px 0 20px; }
.cc-ic-team-toggle {
  display: flex; align-items: center; gap: 12px; font-family: inherit;
  padding: 12px 16px; font-size: 14px; font-weight: 430;
  color: var(--ic-gray-700); cursor: pointer; user-select: none;
  width: fit-content; background: var(--ic-gray-150);
  border: 0.5px solid var(--ic-border-subtle); border-radius: 8px;
  transition: border-color 0.15s;
}
.cc-ic-team-toggle:hover { border-color: var(--ic-border-default); }
.cc-ic-team-toggle.cc-ic-checked {
  background: rgba(217, 119, 87, 0.08);
  border-color: rgba(217, 119, 87, 0.25);
}
.cc-ic-check {
  width: 16px; height: 16px;
  border: 1px solid var(--ic-border-strong); border-radius: 4px;
  background: var(--ic-gray-000);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.cc-ic-check svg { color: #fff; display: none; }
.cc-ic-team-toggle.cc-ic-checked .cc-ic-check { background: var(--ic-clay-deep); border-color: var(--ic-clay-deep); }
.cc-ic-team-toggle.cc-ic-checked .cc-ic-check svg { display: block; }

.cc-ic-team-reveal { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }
.cc-ic-sales {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px;
  background: var(--ic-gray-000); border: 0.5px solid var(--ic-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-ic-sales-text { font-size: 13px; color: var(--ic-gray-700); line-height: 1.5; flex: 1; min-width: 200px; }
.cc-ic-sales-text strong { font-weight: 550; color: var(--ic-slate); }
.cc-ic-sales-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-ic-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--ic-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-ic-btn-clay:hover { background: var(--ic-clay); }
.cc-ic-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--ic-gray-700);
  border: 0.5px solid var(--ic-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-ic-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }

.cc-ic-provider-bar {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; background: var(--ic-gray-150);
  border-radius: 8px; font-size: 13px; flex-wrap: wrap;
}
.cc-ic-provider-bar .cc-ic-label { color: var(--ic-gray-550); flex-shrink: 0; }
.cc-ic-provider-pills { display: flex; gap: 4px; flex-wrap: wrap; }
.cc-ic-p-pill {
  appearance: none; border: none; background: transparent;
  padding: 6px 12px; border-radius: 6px;
  font-size: 13px; font-weight: 430; color: var(--ic-gray-700);
  white-space: nowrap;
}
.cc-ic-p-pill:hover { background: rgba(0, 0, 0, 0.04); }
.cc-ic-p-pill.cc-ic-active {
  background: var(--ic-gray-000); color: var(--ic-slate);
  font-weight: 500; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.cc-ic-provider-notice {
  display: flex; padding: 16px 18px;
  background: var(--ic-gray-000); border: 0.5px solid var(--ic-border-default);
  border-radius: 8px; gap: 14px; align-items: flex-start;
}
.cc-ic-provider-notice > svg { color: var(--ic-gray-550); margin-top: 2px; flex-shrink: 0; }
.cc-ic-provider-notice-body { font-size: 14px; line-height: 1.55; color: var(--ic-gray-700); }
.cc-ic-provider-notice-body strong { font-weight: 550; color: var(--ic-slate); }
.cc-ic-provider-notice-body a { color: var(--ic-clay-deep); font-weight: 500; }
.cc-ic-provider-notice-body a:hover { text-decoration: underline; }

.cc-ic-card { background: #141413; border-radius: 12px; overflow: hidden; }
.cc-ic-subtabs {
  display: flex; align-items: center;
  background: #1a1918;
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.08);
  padding: 0 8px; overflow-x: auto;
}
.cc-ic-subtab {
  appearance: none; background: none; border: none;
  padding: 12px 16px; font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  position: relative; white-space: nowrap;
}
.cc-ic-subtab:hover { color: rgba(255, 255, 255, 0.75); }
.cc-ic-subtab.cc-ic-active { color: #fff; }
.cc-ic-subtab.cc-ic-active::after {
  content: ''; position: absolute;
  left: 12px; right: 12px; bottom: -0.5px;
  height: 2px; background: var(--ic-clay);
}
.cc-ic-shell-switch {
  display: inline-flex; gap: 2px;
  margin: 14px 26px 0; padding: 3px;
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  font-family: inherit;
}
.cc-ic-shell-option {
  font: inherit; font-size: 12px; font-weight: 500;
  padding: 5px 12px; border-radius: 6px;
  background: transparent; border: none;
  color: rgba(255, 255, 255, 0.55);
  cursor: pointer; user-select: none; white-space: nowrap;
  transition: color 120ms ease, background-color 120ms ease;
}
.cc-ic-shell-option:hover { color: rgba(255, 255, 255, 0.85); }
.cc-ic-shell-option.cc-ic-active {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
}

.cc-ic-card-body { padding: 24px 26px; display: flex; align-items: flex-start; gap: 14px; }
.cc-ic-prompt {
  color: var(--ic-clay); font-family: var(--ic-font-mono);
  font-size: 17px; user-select: none; padding-top: 2px;
}
.cc-ic-cmd {
  flex: 1; font-family: var(--ic-font-mono);
  font-size: 17px; color: #f0eee6;
  line-height: 1.55; white-space: pre-wrap; word-break: break-word;
}
.cc-ic-copy {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255, 255, 255, 0.08);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.85);
  padding: 7px 13px; border-radius: 8px;
  font-size: 13px; font-weight: 500; flex-shrink: 0;
}
.cc-ic-copy:hover { background: rgba(255, 255, 255, 0.14); }
.cc-ic-copy.cc-ic-copied { background: var(--ic-clay-deep); border-color: var(--ic-clay-deep); color: #fff; }

.cc-ic-below {
  margin-top: 12px; font-size: 13px; color: var(--ic-gray-550);
  display: flex; gap: 16px; flex-wrap: wrap; align-items: baseline;
}
.cc-ic-below a { color: var(--ic-gray-700); border-bottom: 0.5px solid var(--ic-border-default); }
.cc-ic-below a:hover { color: var(--ic-clay-deep); border-bottom-color: var(--ic-clay-deep); }
.cc-ic-handoff {
  padding: 22px 24px;
  background: linear-gradient(180deg, #faf9f4 0%, #f3f1e9 100%);
  border: 0.5px solid var(--ic-border-default);
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(31, 30, 29, 0.04), 0 6px 16px -4px rgba(31, 30, 29, 0.06);
}
.dark .cc-ic-handoff {
  background: linear-gradient(180deg, #262624 0%, #1f1e1d 100%);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 6px 16px -4px rgba(0, 0, 0, 0.4);
}
.cc-ic-handoff-title {
  font-size: 16px; font-weight: 550; color: var(--ic-slate);
  letter-spacing: -0.01em; margin-bottom: 4px;
}
.cc-ic-handoff-sub {
  font-size: 14px; line-height: 1.5; color: var(--ic-gray-700);
  margin-bottom: 18px;
}
.cc-ic-handoff-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.cc-ic-handoff-alt {
  margin-top: 12px; font-size: 12px; color: var(--ic-gray-550);
}
.cc-ic-handoff-alt code {
  font-family: var(--ic-font-mono); font-size: 11px;
  background: var(--ic-gray-150); padding: 2px 6px;
  border-radius: 4px; color: var(--ic-gray-700);
}
.cc-ic-copy-sm {
  appearance: none; border: none;
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px;
  margin-left: 4px; vertical-align: middle;
  background: var(--ic-gray-150); color: var(--ic-gray-550);
  border-radius: 4px;
  transition: color 0.1s, background-color 0.1s;
}
.cc-ic-copy-sm:hover { color: var(--ic-gray-700); background: var(--ic-border-default); }
.cc-ic-copy-sm.cc-ic-copied { background: var(--ic-clay-deep); color: #fff; }

@media (max-width: 720px) {
  .cc-ic-tab { padding: 12px 14px; font-size: 14px; }
  .cc-ic-sales-actions { width: 100%; }
  .cc-ic-card-body { padding: 20px; }
  .cc-ic-cmd { font-size: 15px; }
}
`;
  return <div className="cc-ic not-prose">
      <style>{STYLES}</style>

      {}
      <div className="cc-ic-tab-strip" role="tablist">
        {TABS.map(t => <button key={t.key} type="button" role="tab" aria-selected={target === t.key} className={'cc-ic-tab' + (target === t.key ? ' cc-ic-active' : '')} onClick={() => setTarget(t.key)}>
            {t.label}
          </button>)}
      </div>

      {}
      <div className="cc-ic-team-wrap">
        <button type="button" role="switch" aria-checked={team} className={'cc-ic-team-toggle' + (team ? ' cc-ic-checked' : '')} onClick={() => setTeam(!team)}>
          <span className="cc-ic-check">{iconCheck(11)}</span>
          <span>
            I’m buying for a team or company (SSO, AWS/Azure/GCP, central billing)
          </span>
        </button>
      </div>

      {}
      {team && <div className="cc-ic-team-reveal">
          <div className="cc-ic-sales">
            <div className="cc-ic-sales-text">
              <strong>Set up your team:</strong> self-serve or talk to sales.
            </div>
            <div className="cc-ic-sales-actions">
              <a href="https://claude.ai/upgrade?initialPlanType=team&amp;utm_source=claude_code&amp;utm_medium=docs&amp;utm_content=configurator_team_get_started" className="cc-ic-btn-ghost">
                Get started
              </a>
              <a href="https://www.anthropic.com/contact-sales?utm_source=claude_code&amp;utm_medium=docs&amp;utm_content=configurator_team_contact_sales" className="cc-ic-btn-clay">
                Contact sales {iconArrowRight()}
              </a>
            </div>
          </div>

          <div className="cc-ic-provider-bar">
            <span className="cc-ic-label">Run on</span>
            <div className="cc-ic-provider-pills" role="radiogroup" aria-label="Provider">
              {PROVIDERS.map(p => <button key={p.key} type="button" role="radio" aria-checked={provider === p.key} className={'cc-ic-p-pill' + (provider === p.key ? ' cc-ic-active' : '')} onClick={() => setProvider(p.key)}>
                  {p.label}
                </button>)}
            </div>
          </div>

          {showNotice && <div className="cc-ic-provider-notice">
              {iconInfo()}
              <div className="cc-ic-provider-notice-body">
                {PROVIDER_NOTICE[provider]}
              </div>
            </div>}
        </div>}

      {}
      {target === 'terminal' && <div className="cc-ic-card">
          <div className="cc-ic-subtabs" role="tablist" aria-label="Install method">
            {Object.keys(TERM).map(k => <button key={k} type="button" role="tab" aria-selected={pkg === k} className={'cc-ic-subtab' + (pkg === k ? ' cc-ic-active' : '')} onClick={() => setPkg(k)}>
                {TERM[k].label}
              </button>)}
          </div>
          {isWinInstaller && <div className="cc-ic-shell-switch" role="tablist" aria-label="Shell">
              {[{
    k: 'ps',
    label: 'PowerShell'
  }, {
    k: 'cmd',
    label: 'CMD'
  }].map(({k, label}) => {
    const active = k === 'cmd' === winCmd;
    return <button key={k} type="button" role="tab" aria-selected={active} className={'cc-ic-shell-option' + (active ? ' cc-ic-active' : '')} onClick={() => setWinCmd(k === 'cmd')}>
                    {label}
                  </button>;
  })}
            </div>}
          {cardBodyCmd(terminalCmd, isWinPrompt ? '>' : '$')}
        </div>}

      {}
      {target === 'terminal' && <div className="cc-ic-below">
          {isWinInstaller && <span>
              Requires{' '}
              <a href="https://git-scm.com/downloads/win" target="_blank" rel="noopener">
                Git for Windows
              </a>.
            </span>}
          {(pkg === 'brew' || pkg === 'winget') && <span>
              Does not auto-update. Run{' '}
              <code>{pkg === 'brew' ? 'brew upgrade claude-code' : 'winget upgrade Anthropic.ClaudeCode'}</code>{' '}
              periodically.
            </span>}
          <a href="/en/troubleshooting">Troubleshooting</a>
        </div>}

      {alt && <div className="cc-ic-handoff">
          <div className="cc-ic-handoff-title">Claude Code for {alt.name}</div>
          <div className="cc-ic-handoff-sub">{alt.tagline}</div>
          <div className="cc-ic-handoff-actions">
            <a href={alt.installHref} className="cc-ic-btn-clay" {...alt.installHref.startsWith('http') ? {
    target: '_blank',
    rel: 'noopener'
  } : {}}>
              {alt.installLabel} {iconArrowUpRight(13)}
            </a>
            <a href={alt.guideHref} className="cc-ic-btn-ghost">
              {alt.name} guide {iconArrowRight(12)}
            </a>
          </div>
          {alt.altCmd && <div className="cc-ic-handoff-alt">
              or run <code>{alt.altCmd}</code>
              <button type="button" className={'cc-ic-copy-sm' + (copied === 'alt' ? ' cc-ic-copied' : '')} onClick={() => handleCopy(alt.altCmd, 'alt')} aria-label="Copy command">
                {copied === 'alt' ? iconCheck(11) : iconCopy(11)}
              </button>
            </div>}
        </div>}
    </div>;
};

export const Experiment = ({flag, treatment, children}) => {
  const VID_KEY = 'exp_vid';
  const CONSENT_COUNTRIES = new Set(['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'RE', 'GP', 'MQ', 'GF', 'YT', 'BL', 'MF', 'PM', 'WF', 'PF', 'NC', 'AW', 'CW', 'SX', 'FO', 'GL', 'AX', 'GB', 'UK', 'AI', 'BM', 'IO', 'VG', 'KY', 'FK', 'GI', 'MS', 'PN', 'SH', 'TC', 'GG', 'JE', 'IM', 'CA', 'BR', 'IN']);
  const fnv1a = s => {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return h >>> 0;
  };
  const bucket = (seed, vid) => fnv1a(fnv1a(seed + vid) + '') % 10000 < 5000 ? 'control' : 'treatment';
  const [decision] = useState(() => {
    const params = new URLSearchParams(location.search);
    const preBucketed = document.documentElement.dataset['gb_' + flag.replace(/-/g, '_')];
    const force = params.get('gb-force');
    if (force) {
      for (const p of force.split(',')) {
        const [k, v] = p.split(':');
        if (k === flag) return {
          variant: v || 'treatment',
          track: false
        };
      }
    }
    if (navigator.globalPrivacyControl) {
      return {
        variant: 'control',
        track: false
      };
    }
    const prefsMatch = document.cookie.match(/(?:^|; )anthropic-consent-preferences=([^;]+)/);
    if (prefsMatch) {
      try {
        if (JSON.parse(decodeURIComponent(prefsMatch[1])).analytics !== true) {
          return {
            variant: 'control',
            track: false
          };
        }
      } catch {
        return {
          variant: 'control',
          track: false
        };
      }
    } else {
      const country = params.get('country')?.toUpperCase() || (document.cookie.match(/(?:^|; )cf_geo=([A-Z]{2})/) || [])[1];
      if (!country || CONSENT_COUNTRIES.has(country)) {
        return {
          variant: 'control',
          track: false
        };
      }
    }
    let vid;
    try {
      const ajsMatch = document.cookie.match(/(?:^|; )ajs_anonymous_id=([^;]+)/);
      if (ajsMatch) {
        vid = decodeURIComponent(ajsMatch[1]).replace(/^"|"$/g, '');
      } else {
        vid = localStorage.getItem(VID_KEY);
        if (!vid) {
          vid = crypto.randomUUID();
        }
        document.cookie = `ajs_anonymous_id=${vid}; domain=.claude.com; path=/; Secure; SameSite=Lax; max-age=31536000`;
      }
      try {
        localStorage.setItem(VID_KEY, vid);
      } catch {}
    } catch {
      return {
        variant: 'control',
        track: false
      };
    }
    const variant = preBucketed === '1' ? 'treatment' : preBucketed === '0' ? 'control' : bucket(flag, vid);
    return {
      variant,
      track: true,
      vid
    };
  });
  useEffect(() => {
    if (!decision.track) return;
    fetch('https://api.anthropic.com/api/event_logging/v2/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-service-name': 'claude_code_docs'
      },
      body: JSON.stringify({
        events: [{
          event_type: 'GrowthbookExperimentEvent',
          event_data: {
            device_id: decision.vid,
            anonymous_id: decision.vid,
            timestamp: new Date().toISOString(),
            experiment_id: flag,
            variation_id: decision.variant === 'treatment' ? 1 : 0,
            environment: 'production'
          }
        }]
      }),
      keepalive: true
    }).catch(() => {});
  }, []);
  return decision.variant === 'treatment' ? treatment : children;
};

Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done.

<div data-gb-slot="overview-install-configurator">
  <Experiment flag="overview-install-configurator" treatment={<InstallConfigurator />} />
</div>

## Get started

Choose your environment to get started. Most surfaces require a [Claude subscription](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) or [Anthropic Console](https://console.anthropic.com/) account. The Terminal CLI and VS Code also support [third-party providers](/en/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    The full-featured CLI for working with Claude Code directly in your terminal. Edit files, run commands, and manage your entire project from the command line.

    To install Claude Code, use one of the following methods:

    <Tabs>
      <Tab title="Native Install (Recommended)">
        **macOS, Linux, WSL:**

        ```bash theme={null}
        curl -fsSL https://claude.ai/install.sh | bash
        ```

        **Windows PowerShell:**

        ```powershell theme={null}
        irm https://claude.ai/install.ps1 | iex
        ```

        **Windows CMD:**

        ```batch theme={null}
        curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
        ```

        If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

        [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

        <Info>
          Native installations automatically update in the background to keep you on the latest version.
        </Info>
      </Tab>

      <Tab title="Homebrew">
        ```bash theme={null}
        brew install --cask claude-code
        ```

        Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

        <Info>
          Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
        </Info>
      </Tab>

      <Tab title="WinGet">
        ```powershell theme={null}
        winget install Anthropic.ClaudeCode
        ```

        <Info>
          WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
        </Info>
      </Tab>
    </Tabs>

    You can also install with [apt, dnf, or apk](/en/setup#install-with-linux-package-managers) on Debian, Fedora, RHEL, and Alpine.

    Then start Claude Code in any project:

    ```bash theme={null}
    cd your-project
    claude
    ```

    You'll be prompted to log in on first use. That's it! [Continue with the Quickstart →](/en/quickstart)

    <Tip>
      See [advanced setup](/en/setup) for installation options, manual updates, or uninstallation instructions. Visit [troubleshooting](/en/troubleshooting) if you hit issues.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    The VS Code extension provides inline diffs, @-mentions, plan review, and conversation history directly in your editor.

    * [Install for VS Code](vscode:extension/anthropic.claude-code)
    * [Install for Cursor](cursor:extension/anthropic.claude-code)

    Or search for "Claude Code" in the Extensions view (`Cmd+Shift+X` on Mac, `Ctrl+Shift+X` on Windows/Linux). After installing, open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), type "Claude Code", and select **Open in New Tab**.

    [Get started with VS Code →](/en/vs-code#get-started)
  </Tab>

  <Tab title="Desktop app">
    A standalone app for running Claude Code outside your IDE or terminal. Review diffs visually, run multiple sessions side by side, schedule recurring tasks, and kick off cloud sessions.

    Download and install:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel and Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)

    After installing, launch Claude, sign in, and click the **Code** tab to start coding. A [paid subscription](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing) is required.

    [Learn more about the desktop app →](/en/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Run Claude Code in your browser with no local setup. Kick off long-running tasks and check back when they're done, work on repos you don't have locally, or run multiple tasks in parallel. Available on desktop browsers and the Claude iOS app.

    Start coding at [claude.ai/code](https://claude.ai/code).

    [Get started on the web →](/en/web-quickstart)
  </Tab>

  <Tab title="JetBrains">
    A plugin for IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs with interactive diff viewing and selection context sharing.

    Install the [Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) from the JetBrains Marketplace and restart your IDE.

    [Get started with JetBrains →](/en/jetbrains)
  </Tab>
</Tabs>

## What you can do

Here are some of the ways you can use Claude Code:

<AccordionGroup>
  <Accordion title="Automate the work you keep putting off" icon="wand-magic-sparkles">
    Claude Code handles the tedious tasks that eat up your day: writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes.

    ```bash theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Build features and fix bugs" icon="hammer">
    Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works.

    For bugs, paste an error message or describe the symptom. Claude Code traces the issue through your codebase, identifies the root cause, and implements a fix. See [common workflows](/en/common-workflows) for more examples.
  </Accordion>

  <Accordion title="Create commits and pull requests" icon="code-branch">
    Claude Code works directly with git. It stages changes, writes commit messages, creates branches, and opens pull requests.

    ```bash theme={null}
    claude "commit my changes with a descriptive message"
    ```

    In CI, you can automate code review and issue triage with [GitHub Actions](/en/github-actions) or [GitLab CI/CD](/en/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Connect your tools with MCP" icon="plug">
    The [Model Context Protocol (MCP)](/en/mcp) is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read your design docs in Google Drive, update tickets in Jira, pull data from Slack, or use your own custom tooling.
  </Accordion>

  <Accordion title="Customize with instructions, skills, and hooks" icon="sliders">
    [`CLAUDE.md`](/en/memory) is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists. Claude also builds [auto memory](/en/memory#auto-memory) as it works, saving learnings like build commands and debugging insights across sessions without you writing anything.

    Create [custom commands](/en/skills) to package repeatable workflows your team can share, like `/review-pr` or `/deploy-staging`.

    [Hooks](/en/hooks) let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.
  </Accordion>

  <Accordion title="Run agent teams and build custom agents" icon="users">
    Spawn [multiple Claude Code agents](/en/sub-agents) that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.

    For fully custom workflows, the [Agent SDK](/en/agent-sdk/overview) lets you build your own agents powered by Claude Code's tools and capabilities, with full control over orchestration, tool access, and permissions.
  </Accordion>

  <Accordion title="Pipe, script, and automate with the CLI" icon="terminal">
    Claude Code is composable and follows the Unix philosophy. Pipe logs into it, run it in CI, or chain it with other tools:

    ```bash theme={null}
    # Analyze recent log output
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # Automate translations in CI
    claude -p "translate new strings into French and raise a PR for review"

    # Bulk operations across files
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    See the [CLI reference](/en/cli-reference) for the full set of commands and flags.
  </Accordion>

  <Accordion title="Schedule recurring tasks" icon="clock">
    Run Claude on a schedule to automate work that repeats: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge.

    * [Routines](/en/routines) run on Anthropic-managed infrastructure, so they keep running even when your computer is off. They can also trigger on API calls or GitHub events. Create them from the web, the Desktop app, or by running `/schedule` in the CLI.
    * [Desktop scheduled tasks](/en/desktop-scheduled-tasks) run on your machine, with direct access to your local files and tools
    * [`/loop`](/en/scheduled-tasks) repeats a prompt within a CLI session for quick polling
  </Accordion>

  <Accordion title="Work from anywhere" icon="globe">
    Sessions aren't tied to a single surface. Move work between environments as your context changes:

    * Step away from your desk and keep working from your phone or any browser with [Remote Control](/en/remote-control)
    * Message [Dispatch](/en/desktop#sessions-from-dispatch) a task from your phone and open the Desktop session it creates
    * Kick off a long-running task on the [web](/en/claude-code-on-the-web) or [iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684), then pull it into your terminal with `claude --teleport`
    * Hand off a terminal session to the [Desktop app](/en/desktop) with `/desktop` for visual diff review
    * Route tasks from team chat: mention `@Claude` in [Slack](/en/slack) with a bug report and get a pull request back
  </Accordion>
</AccordionGroup>

## Use Claude Code everywhere

Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them.

Beyond the [Terminal](/en/quickstart), [VS Code](/en/vs-code), [JetBrains](/en/jetbrains), [Desktop](/en/desktop), and [Web](/en/claude-code-on-the-web) environments above, Claude Code integrates with CI/CD, chat, and browser workflows:

| I want to...                                                                    | Best option                                                                                                        |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Continue a local session from my phone or another device                        | [Remote Control](/en/remote-control)                                                                               |
| Push events from Telegram, Discord, iMessage, or my own webhooks into a session | [Channels](/en/channels)                                                                                           |
| Start a task locally, continue on mobile                                        | [Web](/en/claude-code-on-the-web) or [Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Run Claude on a recurring schedule                                              | [Routines](/en/routines) or [Desktop scheduled tasks](/en/desktop-scheduled-tasks)                                 |
| Automate PR reviews and issue triage                                            | [GitHub Actions](/en/github-actions) or [GitLab CI/CD](/en/gitlab-ci-cd)                                           |
| Get automatic code review on every PR                                           | [GitHub Code Review](/en/code-review)                                                                              |
| Route bug reports from Slack to pull requests                                   | [Slack](/en/slack)                                                                                                 |
| Debug live web applications                                                     | [Chrome](/en/chrome)                                                                                               |
| Build custom agents for your own workflows                                      | [Agent SDK](/en/agent-sdk/overview)                                                                                |

## Next steps

Once you've installed Claude Code, these guides help you go deeper.

* [Quickstart](/en/quickstart): walk through your first real task, from exploring a codebase to committing a fix
* [Store instructions and memories](/en/memory): give Claude persistent instructions with CLAUDE.md files and auto memory
* [Common workflows](/en/common-workflows) and [best practices](/en/best-practices): patterns for getting the most out of Claude Code
* [Settings](/en/settings): customize Claude Code for your workflow
* [Troubleshooting](/en/troubleshooting): solutions for common issues
* [code.claude.com](https://code.claude.com/): demos, pricing, and product details
