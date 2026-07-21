> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Prompt library

> Copy-paste prompts for Claude Code, tagged by task and role.

export const PromptLibrary = ({text = {}, labels = {}, tagLabels = {}, phaseLabels = {}, sourceLabels = {}, catLabels = {}}) => {
  const RAW = useMemo(() => [{
    id: 'get-oriented-in-a',
    sdlc: 'discover',
    cat: 'Onboard',
    startN: 1,
    roles: [],
    prompt: 'give me an overview of this codebase: architecture, key directories, and how the pieces connect',
    nextHref: '/en/memory',
    src: 'workflows'
  }, {
    id: 'explain-unfamiliar-code',
    sdlc: 'discover',
    cat: 'Understand',
    roles: [],
    prompt: 'explain what {path} does and how data flows through it. write it up as {format}',
    slots: {
      path: 'src/scheduler/queue.ts',
      format: 'an HTML page with a diagram, then open it in my browser'
    },
    nextHref: '/en/output-styles',
    src: 'workflows'
  }, {
    id: 'find-where-something-happens',
    sdlc: 'discover',
    cat: 'Understand',
    startN: 2,
    roles: [],
    prompt: 'where do we {behavior}?',
    slots: {
      behavior: 'validate uploaded file types'
    },
    src: 'workflows'
  }, {
    id: 'see-what-depends-on',
    sdlc: 'discover',
    cat: 'Understand',
    roles: [],
    prompt: 'what would break if I deleted {target}?',
    slots: {
      target: 'the retryWithBackoff helper'
    },
    src: 'workflows'
  }, {
    id: 'trace-how-code-evolved',
    sdlc: 'discover',
    cat: 'Understand',
    roles: [],
    prompt: 'look through the commit history of {path} and summarize how it evolved and why',
    slots: {
      path: 'internal/auth/session.go'
    },
    src: 'best-practices'
  }, {
    id: 'scope-a-change-before',
    sdlc: 'discover',
    cat: 'Understand',
    roles: ['pm', 'design'],
    prompt: 'which files would I need to touch to {change}?',
    slots: {
      change: 'add a dark mode toggle to settings'
    },
    src: 'teams'
  }, {
    id: 'ask-the-codebase-a',
    sdlc: 'discover',
    cat: 'Understand',
    roles: ['pm'],
    prompt: 'I am a {role}. walk me through what happens when a user {action}, from the UI down to the result',
    slots: {
      role: 'PM',
      action: 'clicks Export to PDF'
    },
    nextHref: '/en/output-styles',
    src: 'teams'
  }, {
    id: 'plan-a-multi-file',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['pm', 'design'],
    prompt: 'plan how to refactor the {target} to {goal}. list the files you would change, but don\'t edit anything yet',
    slots: {
      target: 'payment module',
      goal: 'support multiple currencies'
    },
    src: 'workflows'
  }, {
    id: 'draft-a-spec-by',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['pm'],
    prompt: 'I want to build {feature}. interview me about implementation, UX, edge cases, and tradeoffs until we have covered everything, then write the spec to SPEC.md',
    slots: {
      feature: 'per-workspace rate limits'
    },
    nextHref: '/en/skills',
    src: 'best-practices'
  }, {
    id: 'turn-a-meeting-into',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['pm'],
    prompt: 'read {input} and write up the action items, then create a {tracker} ticket for each with acceptance criteria',
    slots: {
      input: '@meeting-notes.md',
      tracker: 'Linear'
    },
    needs: 'tracker',
    nextHref: '/en/skills',
    src: 'teams'
  }, {
    id: 'map-edge-cases-before',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['design', 'pm'],
    prompt: 'list the error states, empty states, and edge cases for {feature} that the design needs to cover',
    slots: {
      feature: 'the file upload flow'
    },
    src: 'teams'
  }, {
    id: 'turn-a-mockup-into',
    sdlc: 'design',
    cat: 'Prototype',
    roles: ['design', 'pm', 'marketing'],
    paste: 'mockup',
    prompt: 'here is a mockup. build a working prototype I can click through, matching the layout and states shown',
    src: 'teams'
  }, {
    id: 'implement-from-a-screenshot',
    sdlc: 'design',
    cat: 'Prototype',
    roles: ['design'],
    paste: 'design',
    needs: 'browser',
    prompt: 'implement this design, then take a screenshot of the result, compare it to the original, and fix any differences',
    nextHref: '/en/goal',
    src: 'best-practices'
  }, {
    id: 'follow-an-existing-pattern',
    sdlc: 'build',
    cat: 'Implement',
    roles: [],
    prompt: 'look at how {example} is implemented to understand the pattern, then build {new} the same way',
    slots: {
      example: 'the GitHub webhook handler',
      new: 'a Stripe webhook handler'
    },
    nextHref: '/en/memory',
    src: 'best-practices'
  }, {
    id: 'generate-docs-for-code',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['docs'],
    prompt: 'find {scope} without {format} comments and add them, matching the style already used in the file',
    slots: {
      scope: 'the public functions in src/auth/',
      format: 'JSDoc'
    },
    src: 'workflows'
  }, {
    id: 'add-a-small-well',
    sdlc: 'build',
    cat: 'Implement',
    roles: [],
    prompt: 'add a {endpoint} endpoint that returns {payload}',
    slots: {
      endpoint: '/health',
      payload: 'the app version and uptime'
    },
    src: 'workflows'
  }, {
    id: 'build-a-small-internal',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['pm', 'design', 'marketing', 'docs'],
    prompt: 'create a {tool} using HTML, CSS, and vanilla JavaScript, then open it in my browser',
    slots: {
      tool: 'drag-and-drop Kanban board with three columns'
    },
    src: 'teams'
  }, {
    id: 'work-an-issue-end',
    sdlc: 'build',
    cat: 'Implement',
    roles: [],
    prompt: 'read issue #{issue}, implement the fix, and run the tests',
    slots: {
      issue: '312'
    },
    needs: 'gh',
    src: 'workflows'
  }, {
    id: 'find-and-update-copy',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['design', 'docs', 'marketing'],
    prompt: 'find every place we say "{copy}" or a close variant, show me each one in context, then update them all to "{new}". leave tests and the changelog alone',
    slots: {
      copy: 'Sign up free',
      new: 'Start free trial'
    },
    src: 'teams'
  }, {
    id: 'draft-from-past-examples',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['docs', 'marketing', 'pm'],
    prompt: 'read the {examples} in {folder} to learn the structure and voice, then draft a new one for {topic}',
    slots: {
      examples: 'privacy impact assessments',
      folder: 'legal/pia/',
      topic: 'the new analytics integration'
    },
    nextHref: '/en/skills',
    src: 'legal'
  }, {
    id: 'write-tests-run-them',
    sdlc: 'build',
    cat: 'Test',
    startN: 4,
    roles: [],
    prompt: 'write tests for {path}, run them, and fix any failures',
    slots: {
      path: 'app/parsers/feed.py'
    },
    nextHref: '/en/memory',
    src: 'workflows'
  }, {
    id: 'drive-implementation-from-tests',
    sdlc: 'build',
    cat: 'Test',
    roles: [],
    prompt: 'write tests for {feature} first, then implement it until they pass',
    slots: {
      feature: 'the password reset flow'
    },
    src: 'ebook'
  }, {
    id: 'fill-gaps-from-a',
    sdlc: 'build',
    cat: 'Test',
    roles: [],
    prompt: 'read {report} and add tests for the lowest-covered files until each is above {target}%',
    slots: {
      report: 'coverage/coverage-summary.json',
      target: '80'
    },
    nextHref: '/en/goal',
    src: 'workflows'
  }, {
    id: 'migrate-a-pattern-across',
    sdlc: 'build',
    cat: 'Refactor',
    roles: [],
    prompt: 'migrate everything from {from} to {to}: identify every place that needs to change, then make the changes',
    slots: {
      from: 'the old logging API',
      to: 'the structured logger'
    },
    src: 'workflows'
  }, {
    id: 'port-code-between-languages',
    sdlc: 'build',
    cat: 'Refactor',
    roles: [],
    prompt: 'port {source} to {target}, keeping the same {keep}',
    slots: {
      source: 'this Python module',
      target: 'Rust',
      keep: 'public API and test behavior'
    },
    src: 'teams'
  }, {
    id: 'optimize-against-a-measurable',
    sdlc: 'build',
    cat: 'Refactor',
    roles: ['data'],
    prompt: 'optimize {target} to bring {metric} from {current} down to under {goal}',
    slots: {
      target: 'the search query',
      metric: 'p95 latency',
      current: '2s',
      goal: '500ms'
    },
    nextHref: '/en/goal',
    src: 'ebook'
  }, {
    id: 'fix-a-precise-visual',
    sdlc: 'build',
    cat: 'Refactor',
    roles: ['design'],
    prompt: 'the {element} extends {amount} beyond the {container} on {viewport}. fix it.',
    slots: {
      element: 'login button',
      amount: '20px',
      container: 'card border',
      viewport: 'mobile'
    },
    nextHref: '/en/desktop#preview-your-app',
    src: 'ebook'
  }, {
    id: 'review-your-changes-before',
    sdlc: 'build',
    cat: 'Review',
    startN: 5,
    roles: [],
    prompt: 'review my uncommitted changes and flag anything that looks risky before I commit',
    nextHref: '/en/commands',
    src: 'workflows'
  }, {
    id: 'review-a-pull-request',
    sdlc: 'build',
    cat: 'Review',
    roles: [],
    prompt: 'review PR #{pr} and summarize what changed, then list any concerns',
    slots: {
      pr: '247'
    },
    needs: 'gh',
    nextHref: '/en/code-review',
    src: 'workflows'
  }, {
    id: 'review-infrastructure-changes-before',
    sdlc: 'build',
    cat: 'Review',
    roles: ['security', 'ops'],
    paste: 'plan',
    prompt: 'here is my Terraform plan output. what is this going to do, and is anything here going to cause problems?',
    src: 'teams'
  }, {
    id: 'run-a-security-review',
    sdlc: 'build',
    cat: 'Review',
    roles: ['security'],
    prompt: 'use a subagent to review {path} for security issues and report what it finds',
    slots: {
      path: 'src/api/'
    },
    nextHref: '/en/sub-agents',
    src: 'best-practices'
  }, {
    id: 'review-content-before-sending',
    sdlc: 'build',
    cat: 'Review',
    roles: ['marketing', 'docs'],
    prompt: 'review {file} for {concerns} and list anything I should fix before it goes to {reviewer}',
    slots: {
      file: 'launch-post.md',
      concerns: 'unsupported claims, missing attributions, and brand-guideline issues',
      reviewer: 'legal'
    },
    nextHref: '/en/skills',
    src: 'legal'
  }, {
    id: 'course-correct-a-wrong',
    sdlc: 'build',
    cat: 'Steer',
    roles: [],
    prompt: 'that is not right: {feedback}. try a different approach',
    slots: {
      feedback: 'the function signature needs to stay backward-compatible'
    },
    nextHref: '/en/checkpointing',
    src: 'best-practices'
  }, {
    id: 'narrow-the-scope-of',
    sdlc: 'build',
    cat: 'Steer',
    roles: [],
    prompt: 'that is too much. keep only the changes to {scope} and undo your other edits',
    slots: {
      scope: 'the validation logic in src/forms/'
    },
    src: 'best-practices'
  }, {
    id: 'turn-a-correction-into',
    sdlc: 'build',
    cat: 'Steer',
    roles: [],
    prompt: 'you keep {mistake}. add a rule to CLAUDE.md so this stops happening',
    slots: {
      mistake: 'using default exports when this project uses named exports'
    },
    nextHref: '/en/memory',
    src: 'best-practices'
  }, {
    id: 'resolve-merge-conflicts',
    sdlc: 'ship',
    cat: 'Git',
    roles: [],
    prompt: 'resolve the merge conflicts in this branch and explain what you kept from each side',
    src: 'workflows'
  }, {
    id: 'commit-with-a-generated',
    sdlc: 'ship',
    cat: 'Git',
    roles: [],
    prompt: 'commit these changes with a message that summarizes what I did',
    src: 'workflows'
  }, {
    id: 'open-a-pull-request',
    sdlc: 'ship',
    cat: 'Git',
    roles: [],
    prompt: 'find the {tracker} ticket about {topic} and open a PR that implements it',
    slots: {
      tracker: 'Linear',
      topic: 'the login timeout'
    },
    needs: 'tracker',
    src: 'workflows'
  }, {
    id: 'draft-release-notes-from',
    sdlc: 'ship',
    cat: 'Release',
    roles: ['pm', 'docs', 'marketing'],
    prompt: 'compare {from} to {to} and draft release notes grouped by feature, fix, and breaking change',
    slots: {
      from: 'v2.3.0',
      to: 'v2.4.0'
    },
    nextHref: '/en/skills',
    src: 'workflows'
  }, {
    id: 'write-a-ci-workflow',
    sdlc: 'ship',
    cat: 'Release',
    roles: ['ops'],
    prompt: 'write a GitHub Actions workflow that {steps} on every push to {branch}',
    slots: {
      steps: 'runs the tests and deploys to staging',
      branch: 'main'
    },
    src: 'workflows'
  }, {
    id: 'find-and-fix-a',
    sdlc: 'operate',
    cat: 'Debug',
    startN: 3,
    roles: [],
    prompt: 'the {test} test is failing, find out why and fix it',
    slots: {
      test: 'UserAuth'
    },
    src: 'workflows'
  }, {
    id: 'investigate-a-reported-error',
    sdlc: 'operate',
    cat: 'Debug',
    roles: ['ops'],
    prompt: 'users are seeing {symptom} on {where}. investigate and tell me what is going on',
    slots: {
      symptom: '500 errors',
      where: '/api/settings'
    },
    nextHref: '/en/web-quickstart#pre-fill-sessions',
    src: 'workflows'
  }, {
    id: 'fix-a-build-error',
    sdlc: 'operate',
    cat: 'Debug',
    roles: ['ops'],
    paste: 'error',
    prompt: 'here is a build error. fix the root cause and verify the build succeeds',
    src: 'best-practices'
  }, {
    id: 'investigate-a-production-incident',
    sdlc: 'operate',
    cat: 'Incident',
    roles: ['ops', 'security'],
    prompt: '{symptom}. check the logs, recent deploys, and config changes, then tell me the most likely cause',
    slots: {
      symptom: 'the checkout endpoint started returning 500s an hour ago'
    },
    nextHref: '/en/mcp',
    src: 'workflows'
  }, {
    id: 'diagnose-from-a-console',
    sdlc: 'operate',
    cat: 'Incident',
    roles: ['ops', 'data'],
    paste: 'screenshot',
    prompt: 'here is a screenshot of {console}. walk me through why {resource} is failing and give me the exact commands to fix it',
    slots: {
      console: 'the GCP Kubernetes dashboard',
      resource: 'this pod'
    },
    src: 'teams'
  }, {
    id: 'query-logs-in-plain',
    sdlc: 'operate',
    cat: 'Incident',
    roles: ['security', 'ops', 'data'],
    prompt: 'show me all {events} for {scope} over {timeframe}. write the query, run it, and tell me what stands out',
    slots: {
      events: 'failed logins',
      scope: 'the auth service',
      timeframe: 'the past 24 hours'
    },
    needs: 'db',
    src: 'cybersecurity'
  }, {
    id: 'analyze-a-data-file',
    sdlc: 'operate',
    cat: 'Data',
    roles: ['data', 'pm', 'marketing'],
    paste: 'csv',
    prompt: 'read {file}, summarize the key patterns, and write the results to {output}',
    slots: {
      file: '@reports/q1-signups.csv',
      output: 'an HTML page with charts, then open it in my browser'
    },
    nextHref: '/en/mcp',
    src: 'teams'
  }, {
    id: 'generate-variations-from-performance',
    sdlc: 'operate',
    cat: 'Data',
    roles: ['marketing', 'data'],
    paste: 'csv',
    prompt: 'read {file}, find the underperforming {items}, and generate {n} new variations that stay under {limit} characters',
    slots: {
      file: '@ads-performance.csv',
      items: 'headlines',
      n: '20',
      limit: '90'
    },
    nextHref: '/en/mcp',
    src: 'teams'
  }, {
    id: 'turn-a-recurring-task',
    sdlc: 'operate',
    cat: 'Automate',
    roles: [],
    prompt: 'create a /{name} skill for this project that {steps}',
    slots: {
      name: 'ship',
      steps: 'runs the linter and tests, then drafts a commit message'
    },
    src: 'workflows'
  }, {
    id: 'add-a-hook-for',
    sdlc: 'operate',
    cat: 'Automate',
    roles: [],
    prompt: 'write a hook that {action} after every {event}',
    slots: {
      action: 'runs prettier',
      event: 'edit to a .ts or .tsx file'
    },
    src: 'best-practices'
  }, {
    id: 'connect-a-tool-with',
    sdlc: 'operate',
    cat: 'Automate',
    roles: [],
    prompt: 'set up the {server} MCP server so you can read my {data} directly',
    slots: {
      server: 'Sentry',
      data: 'error reports'
    },
    src: 'workflows'
  }, {
    id: 'capture-what-to-remember',
    sdlc: 'operate',
    cat: 'Automate',
    roles: ['pm', 'docs'],
    prompt: 'summarize what we did this session and suggest what to add to CLAUDE.md',
    src: 'teams'
  }], []);
  const PROMPTS = useMemo(() => {
    if (typeof window !== 'undefined') {
      const rawIds = new Set(RAW.map(p => p.id));
      RAW.forEach(p => {
        if (!text[p.id]) console.warn('[prompt-library] no text[] entry for id:', p.id);
      });
      Object.keys(text).forEach(k => {
        if (!rawIds.has(k)) console.warn('[prompt-library] orphaned text[] key:', k);
      });
    }
    return RAW.map(p => ({
      ...p,
      title: p.id,
      teaches: '',
      ...text[p.id] || ({})
    }));
  }, [RAW, text]);
  const L = labels;
  const TL = k => tagLabels[k] || k;
  const CAT_TAG = useMemo(() => ({
    Onboard: 'understand',
    Understand: 'understand',
    Plan: 'plan',
    Prototype: 'prototype',
    Implement: 'build',
    Test: 'test',
    Refactor: 'refactor',
    Review: 'review',
    Steer: 'steer',
    Git: 'git',
    Release: 'release',
    Debug: 'debug',
    Incident: 'debug',
    Data: 'data',
    Automate: 'automate'
  }), []);
  const TAGS = useMemo(() => ['understand', 'plan', 'prototype', 'build', 'test', 'refactor', 'review', 'steer', 'debug', 'git', 'release', 'data', 'automate', 'pm', 'design', 'docs', 'marketing', 'security', 'ops'], []);
  const tagsOf = p => [CAT_TAG[p.cat], ...p.roles || []];
  const doc = useMemo(() => {
    const p = typeof window !== 'undefined' ? window.location.pathname : '';
    const base = p.startsWith('/docs/') ? '/docs' : '';
    const m = p.slice(base.length).match(/^\/([a-z]{2}(?:-[A-Z]{2})?)\//);
    const locale = m ? m[1] : 'en';
    return href => {
      if (!href || href[0] !== '/' || href[1] === '/') return href;
      return base + (href.startsWith('/en/') ? '/' + locale + href.slice(3) : href);
    };
  }, []);
  const linkify = s => {
    const out = [];
    let last = 0;
    const re = /\[([^\]]+)\]\(([^)]+)\)/g;
    for (let m; m = re.exec(s); ) {
      if (m.index > last) out.push(s.slice(last, m.index));
      out.push(<a key={m.index} href={doc(m[2])}>{m[1]}</a>);
      last = re.lastIndex;
    }
    if (last < s.length) out.push(s.slice(last));
    return out;
  };
  const codeify = s => s.split(/(`[^`]+`)/g).map((part, i) => part[0] === '`' ? <code key={i}>{part.slice(1, -1)}</code> : part);
  const SOURCES = useMemo(() => ({
    'workflows': '/en/common-workflows',
    'teams': 'https://claude.com/blog/how-anthropic-teams-use-claude-code',
    'legal': 'https://claude.com/blog/how-anthropic-uses-claude-legal',
    'cybersecurity': 'https://claude.com/blog/how-anthropic-uses-claude-cybersecurity',
    'best-practices': '/en/best-practices',
    'ebook': 'https://resources.anthropic.com/hubfs/Scaling%20agentic%20coding%20across%20your%20organization.pdf'
  }), []);
  const [mounted, setMounted] = useState(false);
  const [q, setQ] = useState('');
  const [start, setStart] = useState(true);
  const [sel, setSel] = useState(null);
  const [openId, setOpenId] = useState(null);
  const [copied, setCopied] = useState(null);
  const [fills, setFills] = useState({});
  const copyTimer = useRef(null);
  useEffect(() => {
    setMounted(true);
    return () => clearTimeout(copyTimer.current);
  }, []);
  const setFill = (id, key, val) => setFills(f => ({
    ...f,
    [id + '.' + key]: val
  }));
  const fillOf = (p, key) => {
    const v = fills[p.id + '.' + key];
    return v !== undefined ? v : p.slots && p.slots[key] !== undefined ? p.slots[key] : '';
  };
  const assemble = p => p.prompt.replace(/\{(\w+)\}/g, (_, k) => fillOf(p, k) || p.slots && p.slots[k] || k);
  const preview = p => p.prompt.replace(/\{(\w+)\}/g, (_, k) => p.slots && p.slots[k] || k);
  const bodyText = p => preview(p) + ' ' + p.teaches.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') + ' ' + (p.next || '');
  const widthFor = s => (s || '').length + 3 + 'ch';
  const ql = q.trim().toLowerCase();
  const toggleTag = k => {
    setStart(false);
    setSel(s => !ql && s === k ? null : k);
  };
  const clear = () => {
    setStart(false);
    setSel(null);
    setQ('');
  };
  const results = useMemo(() => {
    const list = PROMPTS.filter(p => {
      if (ql) return p.title.toLowerCase().includes(ql) || bodyText(p).toLowerCase().includes(ql);
      if (start) return !!p.startN;
      if (sel) return tagsOf(p).includes(sel);
      return true;
    });
    if (ql) return list;
    if (start) return list.sort((a, b) => a.startN - b.startN);
    if (sel) return list.sort((a, b) => (a.roles || []).length - (b.roles || []).length || (b.sdlc === 'operate') - (a.sdlc === 'operate'));
    return list;
  }, [PROMPTS, ql, start, sel]);
  const matchSnippet = p => {
    if (!ql || p.title.toLowerCase().includes(ql)) return null;
    const txt = bodyText(p);
    const at = txt.toLowerCase().indexOf(ql);
    if (at < 0) return null;
    const lo = Math.max(0, at - 30), hi = Math.min(txt.length, at + ql.length + 50);
    return [lo > 0 ? '…' : '', txt.slice(lo, at), <mark key="m">{txt.slice(at, at + ql.length)}</mark>, txt.slice(at + ql.length, hi), hi < txt.length ? '…' : ''];
  };
  const grouped = useMemo(() => {
    if (start && !q.trim()) return [];
    const g = {};
    for (const p of results) {
      const key = p.sdlc + '|' + p.cat;
      (g[key] = g[key] || ({
        sdlc: p.sdlc,
        cat: p.cat,
        items: []
      })).items.push(p);
    }
    return Object.values(g);
  }, [results, start, q]);
  const copy = async (str, id) => {
    try {
      await navigator.clipboard.writeText(str);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = str;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    clearTimeout(copyTimer.current);
    setCopied(id);
    copyTimer.current = setTimeout(() => setCopied(null), 1600);
  };
  const promptBody = p => {
    if (!p.slots) return <code>{p.prompt}</code>;
    const parts = p.prompt.split(/(\{\w+\})/g);
    return <code>
        {parts.map((part, idx) => {
      const m = part.match(/^\{(\w+)\}$/);
      if (!m) return <span key={idx}>{part}</span>;
      const k = m[1];
      const val = fillOf(p, k);
      return <input key={idx} type="text" className="pl-slot" value={val} placeholder={p.slots[k] || k} aria-label={k} style={{
        width: widthFor(val || p.slots[k])
      }} onChange={e => setFill(p.id, k, e.target.value)} onFocus={e => e.target.select()} onClick={e => e.stopPropagation()} />;
    })}
      </code>;
  };
  const card = p => {
    const open = openId === p.id;
    const srcHref = SOURCES[p.src];
    const srcLabel = sourceLabels[p.src];
    const snip = matchSnippet(p);
    return <div key={p.id} className={'pl-card' + (open ? ' pl-open' : '')}>
        <button type="button" className="pl-head" onClick={() => setOpenId(open ? null : p.id)} aria-expanded={open}>
          <span className="pl-title">{p.title}</span>
          {!!p.startN && <span className="pl-chip">{L.startHere} · {p.startN}</span>}
        </button>
        {snip ? <div className="pl-match">{snip}</div> : <code className="pl-prompt-preview">{preview(p)}</code>}
        {open && <div className="pl-body">
            <div className="pl-label">{p.slots ? L.fillAndCopy : L.copyThis}</div>
            {p.needs && L.needs && L.needs[p.needs] && <div className="pl-hint pl-needs">
                <span className="pl-needs-label">{L.needsLabel}</span> {linkify(L.needs[p.needs])}
              </div>}
            {p.paste && L.paste && L.paste[p.paste] && <div className="pl-hint pl-paste">{L.paste[p.paste]}</div>}
            {p.slots && <div className="pl-hint">
                {L.hintBefore} <span className="pl-hint-chip">{L.hintChip}</span> {L.hintAfter}
              </div>}
            <div className="pl-prompt-box">
              <span className="pl-caret">{'❯'}</span>
              {promptBody(p)}
              <button type="button" className="pl-copy" onClick={() => copy(assemble(p), p.id)}>
                {copied === p.id ? L.copied : L.copy}
              </button>
            </div>
            <div className="pl-label">{L.whyWorks}</div>
            <div className="pl-teaches">{linkify(p.teaches)}</div>
            {p.nextHref && p.next && <div className="pl-next">
                <span className="pl-next-label">{L.makeItStick}</span>
                <a href={doc(p.nextHref)}>{codeify(p.next)} →</a>
              </div>}
            {srcLabel && <div className="pl-src">{L.from} {srcHref ? <a href={doc(srcHref)}>{srcLabel}</a> : srcLabel}</div>}
          </div>}
      </div>;
  };
  const STYLES = useMemo(() => `
.pl {
  --pl-accent: #D97757;
  --pl-accent-bg: rgba(217,119,87,0.07);
  --pl-bg: #fff;
  --pl-surface: #FAFAF7;
  --pl-border: #E8E6DC;
  --pl-border-subtle: rgba(31,30,29,0.08);
  --pl-text: #141413;
  --pl-text-2: #5E5D59;
  --pl-text-3: #73726C;
  --pl-text-4: #9C9A92;
  --pl-mono: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
  font-family: 'Anthropic Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px; color: var(--pl-text); margin: 8px 0 32px;
}
.dark .pl {
  --pl-bg: #1f1e1d;
  --pl-surface: #262624;
  --pl-border: #3d3d3a;
  --pl-border-subtle: rgba(240,238,230,0.08);
  --pl-text: #f0eee6;
  --pl-text-2: #bfbdb4;
  --pl-text-3: #91908a;
  --pl-text-4: #73726c;
}
.pl *, .pl *::before, .pl *::after { box-sizing: border-box; }
.pl button { font-family: inherit; cursor: pointer; }
.pl a { color: var(--pl-accent); text-decoration: none; }
.pl a:hover { text-decoration: underline; }

.pl-search {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px; background: var(--pl-surface);
  border: 1px solid var(--pl-border); border-radius: 12px;
  margin-bottom: 14px;
}
.pl-search input {
  flex: 1; border: none; outline: none; background: transparent;
  font-size: 16px; color: var(--pl-text);
}
.pl-search input::placeholder { color: var(--pl-text-4); }

.pl-tags { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 18px; }
.pl-tag {
  padding: 7px 14px; border: 1px solid var(--pl-border); background: var(--pl-bg);
  font-size: 14px; color: var(--pl-text-2); border-radius: 999px;
}
.pl-tag:hover { background: var(--pl-surface); }
.pl-tag.pl-on { background: var(--pl-text); border-color: var(--pl-text); color: var(--pl-bg); }
.pl-tag.pl-start { color: var(--pl-accent); font-weight: 500; }
.pl-tag.pl-start.pl-on { background: var(--pl-accent); border-color: var(--pl-accent); color: #fff; }
.pl-tags.pl-dim .pl-tag { opacity: 0.5; }
.pl-tags.pl-dim .pl-tag:hover { opacity: 1; }
.pl-sep { width: 1px; height: 22px; background: var(--pl-border); margin: 0 4px; }
.pl-clear { border: none; background: none; font-size: 13px; color: var(--pl-text-4); padding: 4px 6px; }
.pl-clear:hover { color: var(--pl-text-2); }
.pl-count { margin-left: auto; font-size: 14px; color: var(--pl-text-4); }

.pl-group-h {
  font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--pl-text-4); margin: 24px 0 12px;
}
.pl-group-h .pl-phase { color: var(--pl-text-3); }
.pl-card {
  border: 1px solid var(--pl-border-subtle); border-radius: 10px;
  margin-bottom: 12px; background: var(--pl-bg); overflow: hidden;
  padding: 14px 18px;
}
.pl-card.pl-open { border-color: var(--pl-border); background: var(--pl-surface); }
.pl-head {
  width: 100%; display: flex; align-items: baseline; gap: 12px;
  border: none; background: transparent; text-align: left; padding: 0;
}
.pl-head:focus-visible { outline: 2px solid var(--pl-accent); outline-offset: 2px; border-radius: 6px; }
.pl-title {
  flex: 1; font-size: 17px; font-weight: 500; color: var(--pl-text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-prompt-preview {
  display: block; font-family: var(--pl-mono); font-size: 13.5px; color: var(--pl-text-3);
  margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-chip {
  font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase;
  padding: 3px 9px; border-radius: 999px; flex-shrink: 0;
  background: var(--pl-accent-bg); color: var(--pl-accent);
}

.pl-body { margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--pl-border-subtle); }
.pl-label {
  font-size: 11.5px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--pl-text-4); margin: 12px 0 8px;
}
.pl-prompt-box {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px; background: #141413; color: #f0eee6;
  border-radius: 8px; font-family: var(--pl-mono); font-size: 15px;
}
.pl-caret { color: var(--pl-accent); flex-shrink: 0; }
.pl-prompt-box code { flex: 1; background: none; padding: 0; color: inherit; white-space: pre-wrap; line-height: 1.9; }
.pl-slot {
  font-family: var(--pl-mono); font-size: inherit;
  background: rgba(217,119,87,0.15); color: #f0eee6;
  border: none; border-bottom: 1.5px dashed var(--pl-accent);
  border-radius: 4px 4px 0 0; padding: 2px 6px; margin: 0 1px;
  outline: none; min-width: 6ch; max-width: 100%;
  box-sizing: content-box; cursor: text;
}
.pl-slot:hover { background: rgba(217,119,87,0.22); }
.pl-slot:focus { background: rgba(217,119,87,0.28); border-bottom-style: solid; }
.pl-slot::placeholder { color: rgba(240,238,230,0.4); font-style: italic; }
.pl-hint { font-size: 14px; color: var(--pl-text-3); margin: 0 0 10px; }
.pl-paste { color: var(--pl-text-2); }
.pl-needs { color: var(--pl-text-2); }
.pl-needs-label {
  display: inline-block; font-size: 10.5px; letter-spacing: 0.06em;
  text-transform: uppercase; padding: 2px 7px; margin-right: 6px;
  border-radius: 4px; background: var(--pl-accent-bg); color: var(--pl-accent);
}
.pl-hint-chip {
  font-family: var(--pl-mono); font-size: 0.92em;
  background: var(--pl-accent-bg); color: var(--pl-accent);
  border-bottom: 1.5px dashed var(--pl-accent);
  border-radius: 3px 3px 0 0; padding: 1px 5px;
}
.pl-copy {
  font-size: 12.5px; padding: 6px 12px; border-radius: 6px;
  background: var(--pl-accent); color: #fff; border: none; flex-shrink: 0;
}
.pl-teaches { display: block; font-size: 15.5px; color: var(--pl-text-2); margin: 4px 0 0; line-height: 1.6; }
.pl-match {
  display: block; font-size: 13.5px; color: var(--pl-text-3);
  margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-match mark { background: var(--pl-accent-bg); color: var(--pl-text); padding: 1px 2px; border-radius: 3px; }
.pl-next {
  display: flex; align-items: baseline; gap: 10px;
  margin: 14px 0 0; padding: 10px 12px;
  background: var(--pl-accent-bg); border-radius: 8px; font-size: 14.5px;
}
.pl-next-label {
  font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--pl-accent); font-weight: 600; flex-shrink: 0;
}
.pl-src { display: block; font-size: 14px; color: var(--pl-text-4); margin: 14px 0 0; }

.pl-show-all {
  display: block; width: 100%; padding: 14px; margin-top: 4px;
  border: 1px dashed var(--pl-border); border-radius: 10px;
  background: transparent; font-size: 15px; color: var(--pl-accent);
  text-align: center;
}
.pl-show-all:hover { background: var(--pl-accent-bg); border-style: solid; }

.pl-empty {
  padding: 32px; text-align: center; color: var(--pl-text-4);
  border: 1px dashed var(--pl-border); border-radius: 10px;
}
`, []);
  if (!mounted) return <div className="pl" style={{
    minHeight: 480
  }} />;
  return <div className="pl">
      <style>{STYLES}</style>

      <div className="pl-search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{
    color: 'var(--pl-text-4)'
  }}>
          <circle cx="11" cy="11" r="7" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input type="text" placeholder={L.search} value={q} onChange={e => {
    setQ(e.target.value);
    if (e.target.value) setStart(false);
  }} aria-label={L.search} />
      </div>

      <div className={'pl-tags' + (ql ? ' pl-dim' : '')}>
        <button type="button" className={'pl-tag pl-start' + (!ql && start ? ' pl-on' : '')} onClick={() => {
    setQ('');
    setStart(!start);
    if (!start) setSel(null);
  }}>
          ★ {L.startHere}
        </button>
        <span className="pl-sep" />
        {TAGS.map(k => <button key={k} type="button" aria-pressed={!ql && sel === k} className={'pl-tag' + (!ql && sel === k ? ' pl-on' : '')} onClick={() => {
    setQ('');
    toggleTag(k);
  }}>
            {TL(k)}
          </button>)}
        {(start || sel || q) && <button type="button" className="pl-clear" onClick={clear}>{L.clear}</button>}
        <span className="pl-count">{results.length} {results.length === 1 ? L.prompt : L.prompts}</span>
      </div>

      {results.length === 0 ? <div className="pl-empty">
          {L.noMatch} {ql ? <code>{q}</code> : null} <button type="button" className="pl-clear" onClick={clear}>{L.clear}</button>
        </div> : !ql && start ? <div>
          <div className="pl-group-h">{L.startHereHeader}</div>
          {results.map(card)}
          <button type="button" className="pl-show-all" onClick={clear}>
            {L.showAll && L.showAll.replace('{n}', PROMPTS.length)} →
          </button>
        </div> : grouped.map(g => <div key={g.sdlc + '|' + g.cat}>
            <div className="pl-group-h"><span className="pl-phase">{phaseLabels[g.sdlc] || g.sdlc}</span> · {catLabels[g.cat] || g.cat}</div>
            {g.items.map(card)}
          </div>)}
    </div>;
};

This is a library of prompts to copy into Claude Code. Use it to explore ways of working you haven't tried, or when you're not sure where to start.

The prompts are collected from various Anthropic guides, including [Common workflows](/docs/en/common-workflows), [Best practices](/docs/en/best-practices), and [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code). They're starting points rather than scripts. Open **Why this works** under any prompt to see the pattern behind it so you can write your own.

export const labels = {
  startHere: "Start here",
  startHereHeader: "Five prompts to try first",
  showAll: "Show all {n} prompts",
  search: "Search prompts…",
  clear: "Clear",
  prompt: "prompt",
  prompts: "prompts",
  noMatch: "No prompts match",
  fillAndCopy: "Fill in and copy",
  copyThis: "Copy this prompt",
  hintBefore: "Type in the",
  hintChip: "highlighted",
  hintAfter: "fields to customize, then copy.",
  copy: "Copy",
  copied: "Copied",
  whyWorks: "Why this works",
  makeItStick: "Make it stick",
  from: "From",
  paste: {
    mockup: "Paste, drag, or @-mention your mockup image, then send this:",
    design: "Paste, drag, or @-mention your design image, then send this:",
    screenshot: "Paste, drag, or @-mention your screenshot, then send this:",
    plan: "Paste your plan output into the prompt first, then send this:",
    error: "Paste the error output into the prompt first, then send this:",
    csv: "Drag your file into the prompt, or replace the path below with an @-mention of your own:"
  },
  needsLabel: "Needs",
  needs: {
    tracker: "your issue tracker added as a [claude.ai connector](/docs/en/mcp#use-mcp-servers-from-claude-ai) or [MCP server](/docs/en/mcp).",
    gh: "the [gh CLI](https://cli.github.com) authenticated, or GitHub added as a [claude.ai connector](/docs/en/mcp#use-mcp-servers-from-claude-ai).",
    browser: "a way for Claude to render and screenshot the result. The [Desktop app](/docs/en/desktop#preview-your-app) has this built in. In the terminal, install the [Chrome extension](/docs/en/chrome) or a Playwright [MCP](/docs/en/mcp) server.",
    db: "your data warehouse or log store added as a [claude.ai connector](/docs/en/mcp#use-mcp-servers-from-claude-ai) or [MCP server](/docs/en/mcp)."
  }
};

export const tagLabels = {
  understand: "Understand",
  plan: "Plan",
  prototype: "Prototype",
  build: "Build",
  test: "Test",
  refactor: "Refactor",
  review: "Review",
  steer: "Steer",
  debug: "Debug",
  git: "Git",
  release: "Release",
  data: "Data",
  automate: "Automate",
  pm: "Product",
  design: "Design",
  docs: "Docs",
  marketing: "Marketing",
  security: "Security",
  ops: "On-call"
};

export const phaseLabels = {
  discover: "Discover",
  design: "Design",
  build: "Build",
  ship: "Ship",
  operate: "Operate"
};

export const sourceLabels = {
  workflows: "Common workflows",
  teams: "How Anthropic teams use Claude Code",
  legal: "How Anthropic uses Claude in Legal",
  cybersecurity: "How Anthropic uses Claude in Cybersecurity",
  "best-practices": "Best practices",
  ebook: "Scaling agentic coding guide"
};

export const catLabels = {
  Onboard: "Onboard",
  Understand: "Understand",
  Plan: "Plan",
  Prototype: "Prototype",
  Implement: "Implement",
  Test: "Test",
  Refactor: "Refactor",
  Review: "Review",
  Steer: "Steer",
  Git: "Git",
  Release: "Release",
  Debug: "Debug",
  Incident: "Incident",
  Data: "Data",
  Automate: "Automate"
};

export const text = {
  "get-oriented-in-a": {
    title: "Get oriented in a new repository",
    teaches: "Describe what you want to know, not which files to read. Claude explores the project on its own and returns a summary of how it fits together.",
    next: "Run `/init` to set up `CLAUDE.md` so Claude remembers this every session"
  },
  "explain-unfamiliar-code": {
    title: "Explain unfamiliar code",
    teaches: "Name the file and say what format you want the answer in. Swap the HTML page for a diagram, bullet points, or whatever fits how you learn.",
    next: "Set an output style so Claude always explains in your preferred format"
  },
  "find-where-something-happens": {
    title: "Find where something happens",
    teaches: "Search by behavior instead of by filename. The search works even when you don't know what the file is called or which directory it lives in."
  },
  "see-what-depends-on": {
    title: "Check what breaks before you delete",
    teaches: "Ask before you remove anything. The list of callers and downstream effects tells you whether you're looking at a one-line cleanup or a change you need to coordinate."
  },
  "trace-how-code-evolved": {
    title: "Trace how code evolved",
    teaches: "Point at commit history when the question is why, not what. Claude reads the log and blame for whatever version control you use and explains the decisions behind the current implementation."
  },
  "scope-a-change-before": {
    title: "Scope a change before you start",
    teaches: "Size the work before you commit it to a roadmap. The file list tells you whether you're looking at one component or a cross-cutting change."
  },
  "ask-the-codebase-a": {
    title: "Ask the codebase a product question",
    teaches: "State your role so the answer is pitched at the right level. Claude explains what the product actually does from the source code, without you needing to read it.",
    next: "Set an output style so Claude always pitches answers at this level"
  },
  "plan-a-multi-file": {
    title: "Plan a multi-file change before touching code",
    teaches: "Adding \"don't edit yet\" separates exploration from changes, so you see the approach before any code moves. To make plan-first the default on every prompt, press Shift+Tab for [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)."
  },
  "draft-a-spec-by": {
    title: "Draft a spec by interview",
    teaches: "Ask to be interviewed instead of writing the spec yourself. Claude asks you structured questions until the requirements are complete, then writes the result to a file.",
    next: "Save your interview questions as a `/spec` skill so every spec starts the same way"
  },
  "turn-a-meeting-into": {
    title: "Turn a meeting into tickets",
    teaches: "Skip the transcription step. Claude pulls action items from the unstructured input and writes them straight into your tracker via [MCP](/docs/en/mcp), so you review the tickets, not the transcript.",
    next: "Save this as a `/tickets` skill"
  },
  "map-edge-cases-before": {
    title: "Map edge cases before building",
    teaches: "Ask for what's missing, not what's there. Claude lists the error states, empty states, and edge cases a happy-path design tends to skip."
  },
  "turn-a-mockup-into": {
    title: "Turn a mockup into a working prototype",
    teaches: "A clickable prototype answers questions a static mockup can't. Hand the working code to engineering instead of explaining the interactions in a doc."
  },
  "implement-from-a-screenshot": {
    title: "Implement from a screenshot and self-check",
    teaches: "This gives Claude a verification loop: it renders, compares against the source image, and iterates without you pointing out each gap.",
    next: "Use `/goal` to keep Claude iterating until the screenshots match"
  },
  "follow-an-existing-pattern": {
    title: "Follow an existing pattern",
    teaches: "Point at code you already like. Without a reference, Claude defaults to general best practices. With one, it matches the conventions your codebase actually uses.",
    next: "Ask Claude to write the pattern it followed into `CLAUDE.md` so future sessions match it without the reference"
  },
  "add-a-small-well": {
    title: "Add a small, well-defined feature",
    teaches: "State the inputs and outputs, not how to build it. Claude finds where similar code lives and adds yours alongside it."
  },
  "build-a-small-internal": {
    title: "Build a small internal tool from scratch",
    teaches: "You don't need a project, a framework, or a build step. Describe the tool and ask Claude to open it so you see it working immediately."
  },
  "work-an-issue-end": {
    title: "Work an issue end to end",
    teaches: "Give the issue number, not a summary. Claude reads the full ticket itself, so requirements you'd forget to mention come through, and it validates the change before reporting back."
  },
  "find-and-update-copy": {
    title: "Find and update copy across the codebase",
    teaches: "Ask for variants and say what to skip. Claude finds phrasings a literal search would miss and leaves test fixtures and history untouched, so you review only the copy users actually see."
  },
  "draft-from-past-examples": {
    title: "Draft a document from past examples",
    teaches: "Point at a folder of finished work instead of describing your style. Claude learns the structure and voice from what you've already shipped, so the first draft reads like one of yours.",
    next: "Save the voice as a skill so every draft starts there"
  },
  "write-tests-run-them": {
    title: "Write tests, run them, fix failures",
    teaches: "Ask for write, run, and fix together so Claude iterates without stopping for instructions.",
    next: "Run `/init` so Claude learns your test command automatically"
  },
  "drive-implementation-from-tests": {
    title: "Drive implementation from tests",
    teaches: "Test-driven development: the tests define when the work is complete, and Claude iterates on the implementation until they pass."
  },
  "fill-gaps-from-a": {
    title: "Fill gaps from a coverage report",
    teaches: "Point at the coverage report instead of guessing what's untested. Claude reads the actual numbers and writes tests for the files that need them most.",
    next: "Set this as a `/goal` so Claude keeps writing tests until coverage hits the target"
  },
  "port-code-between-languages": {
    title: "Port code to another language",
    teaches: "Say what to preserve, not just the target language. Naming the API or behavior that must stay the same gives Claude a contract to check the port against."
  },
  "generate-docs-for-code": {
    title: "Generate docs for undocumented code",
    teaches: "Name the scope and the format. Claude finds what's missing and matches the comment style already in the file, so the new docs read like the rest."
  },
  "migrate-a-pattern-across": {
    title: "Migrate a pattern across the codebase",
    teaches: "Describe the old pattern and the new one. Asking Claude to identify every place first means the call sites are listed in the response, so you can check none were missed."
  },
  "optimize-against-a-measurable": {
    title: "Optimize against a measurable target",
    teaches: "Stating the metric and target gives Claude a clear definition of done.",
    next: "Set this as a `/goal` so Claude keeps measuring and iterating until it hits the number"
  },
  "fix-a-precise-visual": {
    title: "Fix a precise visual bug",
    teaches: "Precise visual feedback gets a precise fix. State the exact element, measurement, and viewport.",
    next: "Add a preview tool so Claude screenshots and verifies the fix itself"
  },
  "review-your-changes-before": {
    title: "Review your changes before you commit",
    teaches: "Catch problems while they're still cheap to fix. Claude reads the changed files in full, not just the diff lines, so it spots issues a quick self-review misses.",
    next: "Run `/code-review` for the same check in one command"
  },
  "review-a-pull-request": {
    title: "Review a pull request",
    teaches: "Claude reviews with the whole codebase in context, not just the diff. It reads the changed code and what it calls, so it catches problems a diff-only review would miss.",
    next: "Turn this on for every PR with Code Review"
  },
  "review-infrastructure-changes-before": {
    title: "Review infrastructure changes before applying",
    teaches: "Plan output is dense and hard to scan. Pasting it gets you a plain-language summary of what's actually going to change before you apply it."
  },
  "run-a-security-review": {
    title: "Run a security review with a subagent",
    teaches: "A [subagent](/docs/en/sub-agents) runs the audit in its own context window and reports back a summary, so a long security review doesn't fill up your main session. The built-in general-purpose subagent handles this without extra setup.",
    next: "Set up a dedicated security-review subagent your whole team can use"
  },
  "review-content-before-sending": {
    title: "Catch issues before formal review",
    teaches: "Get a first pass before a human spends time on it. Name the concerns you want checked so the review is focused, then fix what it finds and send a cleaner draft.",
    next: "Capture your review checklist as a skill your whole team can run"
  },
  "course-correct-a-wrong": {
    title: "Course-correct a wrong approach",
    teaches: "Name the constraint Claude missed, not just that it's wrong. A specific reason gives Claude a concrete constraint to satisfy on the retry, instead of guessing again.",
    next: "Press `Esc` twice to open the rewind menu and restore code and conversation so the retry starts clean"
  },
  "narrow-the-scope-of": {
    title: "Narrow the scope of a change",
    teaches: "When the direction is right but the change went too broad, ask Claude to keep part of it rather than rewinding everything. A stated boundary keeps a small fix from becoming a refactor."
  },
  "turn-a-correction-into": {
    title: "Turn a correction into a rule",
    teaches: "A correction in chat isn't shared with your team. A rule in the project's [CLAUDE.md](/docs/en/memory) is shared once you commit it, and Claude reads it at the start of every session.",
    next: "Open `/memory` to review what Claude wrote"
  },
  "resolve-merge-conflicts": {
    title: "Resolve merge conflicts",
    teaches: "Say what state you want, not which markers to keep. Asking for the reasoning makes the merge reviewable instead of a black box."
  },
  "commit-with-a-generated": {
    title: "Commit with a generated message",
    teaches: "Let Claude derive the message from the diff. It matches your repository's existing commit style."
  },
  "open-a-pull-request": {
    title: "Open a pull request from a ticket",
    teaches: "Skip the context switch between tracker, editor, and GitHub. One prompt reads the spec, makes the change, and opens the PR."
  },
  "draft-release-notes-from": {
    title: "Draft release notes from git history",
    teaches: "Give two reference points and the structure you want. Claude reads the commit log between them and drafts a changelog you can edit.",
    next: "Save this as a `/changelog` skill"
  },
  "write-a-ci-workflow": {
    title: "Write a CI workflow",
    teaches: "Describe when it should run and what it should do; the YAML is generated for you, matched to your project's build and test commands."
  },
  "find-and-fix-a": {
    title: "Find and fix a failing test",
    teaches: "Describe the symptom; you don't need to know which file is broken. Claude runs the test to see the failure, traces it into source, and fixes it."
  },
  "investigate-a-reported-error": {
    title: "Investigate a reported error",
    teaches: "Describe the symptom and location; Claude reads the relevant code path and traces likely causes. Paste stack traces or logs if you have them.",
    next: "Put a deeplink in your runbook that opens Claude with this prompt pre-filled"
  },
  "fix-a-build-error": {
    title: "Fix a build error at the root",
    teaches: "Asking for root cause and verification prevents surface-level patches that suppress the error without fixing it."
  },
  "investigate-a-production-incident": {
    title: "Investigate a production incident",
    teaches: "List the evidence sources to correlate, not the steps to take. Claude reads logs, git history, and config together to narrow the cause.",
    next: "Connect Sentry or your log store via MCP"
  },
  "query-logs-in-plain": {
    title: "Query logs in plain English",
    teaches: "Ask the question instead of writing the SQL. Claude builds the query, runs it against your connected logs, and shows both the query and the result so you can check what ran."
  },
  "diagnose-from-a-console": {
    title: "Diagnose from a console screenshot",
    teaches: "Cloud consoles show you the problem but not the commands to fix it. Claude reads the screenshot and translates the dashboard into the kubectl, gcloud, or aws commands to run."
  },
  "analyze-a-data-file": {
    title: "Analyze a data file",
    teaches: "A one-off question doesn't need a one-off script. Point at a file in your project folder and Claude reads it directly, finds the patterns, and writes the output where you ask.",
    next: "Connect the data source via MCP instead of exporting files"
  },
  "generate-variations-from-performance": {
    title: "Generate variations from performance data",
    teaches: "State the constraint at the start so generation stays within the limit. Claude reads the metrics, picks what to replace, and produces alternatives that fit.",
    next: "Connect the ad platform via MCP instead of exporting a file"
  },
  "turn-a-recurring-task": {
    title: "Turn a recurring task into a skill",
    teaches: "Name the steps once; reuse them as a command. Claude writes a [skill](/docs/en/skills) anyone on your team can run."
  },
  "add-a-hook-for": {
    title: "Add a hook for repeat behavior",
    teaches: "Hooks make a behavior automatic instead of something you have to remember to ask for. Describe the trigger and action and Claude writes the [hook](/docs/en/hooks) configuration."
  },
  "connect-a-tool-with": {
    title: "Connect a tool with MCP",
    teaches: "Connect the source once instead of pasting data every session. After [MCP](/docs/en/mcp) setup, Claude reads from the tool directly when you ask about it."
  },
  "capture-what-to-remember": {
    title: "Capture what to remember for next time",
    teaches: "Ask before you forget. Claude knows what it had to figure out this session and proposes [CLAUDE.md](/docs/en/memory) entries so the next session starts with that context."
  }
};

<PromptLibrary text={text} labels={labels} tagLabels={tagLabels} phaseLabels={phaseLabels} sourceLabels={sourceLabels} catLabels={catLabels} />

## What makes these prompts work

The prompts above share a few patterns. Recognizing them helps you adapt any prompt here to your own task.

**Describe the outcome, not the steps.** Say what you want and let Claude find the files. The prompt below works without naming a single file path.

```text theme={null}
add rate limiting to the public API and make sure existing tests still pass
```

**Give it a way to check its own work.** Ask for run, test, compare, or verify in the same prompt so Claude iterates instead of stopping after one attempt.

```text theme={null}
write the migration, run it against the dev database, and confirm the schema matches
```

**Point at a reference.** Name an existing file, test, or pattern to match so the new code is consistent with what you already have.

```text theme={null}
add a settings page that follows the same layout as the profile page
```

**State the measurable target.** When the goal is performance or coverage, give the metric and threshold so completion is unambiguous.

```text theme={null}
get the bundle size under 200KB and show me what you removed
```

**Give it the artifact.** Paste errors, logs, screenshots, and plan output directly in the prompt, or type `@` to reference a file. Claude reads the source instead of your description of it.

```text theme={null}
why is the build failing? @build.log
```

**Say how you want the answer.** Name the format, length, or audience so the explanation fits how you'll use it. To make a format the default for every response, set an [output style](/docs/en/output-styles).

```text theme={null}
explain how the payment retry logic works as an HTML page with a diagram, then open it in my browser
```

For more on each pattern, see [best practices](/docs/en/best-practices).

## Where these come from

These prompts are based on patterns from published Anthropic resources. Each card links to its source:

* [Common workflows](/docs/en/common-workflows): step-by-step guides for the core tasks
* [Best practices](/docs/en/best-practices): prompting patterns and project setup
* [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code): real workflows from engineering, product, design, and data teams, with deep dives on [legal](https://claude.com/blog/how-anthropic-uses-claude-legal), [marketing](https://claude.com/blog/how-anthropic-uses-claude-marketing), and [cybersecurity](https://claude.com/blog/how-anthropic-uses-claude-cybersecurity)
* [Scaling agentic coding guide](https://resources.anthropic.com/hubfs/Scaling%20agentic%20coding%20across%20your%20organization.pdf): the enterprise adoption guide

For video walkthroughs of these patterns, see the free [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) course on Anthropic Academy.

## Related resources

The prompts on this page are starting points. Once one works for your project, the next step is making it repeatable: save it as a [skill](/docs/en/skills) so anyone on your team can run it as a `/command`, and record the conventions Claude learned in [CLAUDE.md](/docs/en/memory) so every session starts with that context instead of Claude relearning it. For larger or riskier changes, [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) shows you the file list before any edits happen.

If you're introducing Claude Code across a team, see [administration](/docs/en/admin-setup) for managed settings and policy, and [costs and usage](/docs/en/costs) for how this work is billed on your plan.
