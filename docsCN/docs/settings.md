# 设置

> 通过全局与项目级设置以及环境变量配置 Claude Code。

## 设置文件

- 用户设置：`~/.claude/settings.json`
- 项目设置：`.claude/settings.json`（纳入版本控制，团队共享）与 `.claude/settings.local.json`（本地偏好，已自动 gitignore）
- 企业受管策略：`/Library/Application Support/ClaudeCode/managed-settings.json`（macOS）、`/etc/claude-code/managed-settings.json`（Linux/WSL）、`C:\\ProgramData\\ClaudeCode\\managed-settings.json`（Windows）

示例（权限+环境变量）：
```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test:*)", "Read(~/.zshrc)"],
    "deny": ["Bash(curl:*)", "Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

### 可用键（节选）
- `apiKeyHelper`：生成临时凭据脚本（其输出作为 Authorization/X-Api-Key）
- `cleanupPeriodDays`：会话保留天数（默认 30）
- `env`：每次会话注入的环境变量
- `includeCoAuthoredBy`：在 Git 提交/PR 中添加“co-authored-by Claude”（默认 true）
- `hooks`：注册 Hook（见 Hooks 文档）
- `model`：覆盖默认模型
- `statusLine`：自定义状态栏（见 statusline）
- `forceLoginMethod`：限制登录方式（`claudeai` 或 `console`）
- `enableAllProjectMcpServers`/`enabledMcpjsonServers`/`disabledMcpjsonServers`：项目 `.mcp.json` 的服务器批量/白/黑名单
- `awsAuthRefresh`/`awsCredentialExport`：高级 AWS 凭据刷新/导出脚本

### 权限设置
- `allow`/`deny`：参见 IAM 权限规则；可用于排除敏感文件访问（取代已废弃的 ignorePatterns）
- `additionalDirectories`：额外可访问目录
- `defaultMode`：默认权限模式
- `disableBypassPermissionsMode`：可设为 "disable" 禁用绕过模式

### 优先级
1. 企业受管策略（最高，不可覆盖）
2. 命令行参数（本次会话临时覆盖）
3. 项目本地设置（.local.json）
4. 项目共享设置
5. 用户设置

### 子智能体（Subagents）
- 用户：`~/.claude/agents/`
- 项目：`.claude/agents/`
- Markdown+YAML frontmatter，定义名称、描述与工具权限（详见 Subagents 文档）。

## 环境变量（节选）
- `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_CUSTOM_HEADERS`
- `ANTHROPIC_MODEL`、`ANTHROPIC_SMALL_FAST_MODEL`、`ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`
- `CLAUDE_CODE_USE_BEDROCK`/`CLAUDE_CODE_USE_VERTEX` 及对应 SKIP_*、BASE_URL 等
- `CLAUDE_CODE_MAX_OUTPUT_TOKENS`、`MAX_THINKING_TOKENS`
- `DISABLE_*` 系列（自动更新/错误上报/遥测/非关键调用等）
- `HTTP_PROXY`、`HTTPS_PROXY`
- `MCP_TIMEOUT`、`MCP_TOOL_TIMEOUT`、`MAX_MCP_OUTPUT_TOKENS`
- `VERTEX_REGION_*` 各模型区域覆盖

提示：以上变量均可在 `settings.json` 的 `env` 中集中配置。

## 配置命令
- 列表：`claude config list`
- 查看：`claude config get <key>`
- 设置：`claude config set <key> <value>`（全局加 `-g`）
- 列表项添加/移除：`claude config add/remove <key> <value>`

## 工具一览
- Bash（需授权）、Edit/MultiEdit/Write/NotebookEdit（需授权）、Read/Grep/Glob/LS/Task/TodoWrite、WebFetch/WebSearch（需授权）等
- 可通过 `/allowed-tools` 或 settings.json 配置权限，配合 Hooks 实现前/后置操作

## 参阅
- IAM 与权限
- 监控与 OTel
- Devcontainer 安全隔离

