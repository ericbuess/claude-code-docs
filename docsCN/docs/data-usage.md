# 数据使用

> 了解 Anthropic 针对 Claude/Claude Code 的数据使用政策。

## 数据政策

- 训练政策：默认不使用你在 Claude Code 中发送的代码或提示来训练生成式模型。
- 伙伴计划：若你通过特定渠道（如 Development Partner Program）明确同意，才可能用于训练（仅限直连 Anthropic API）。
- 反馈转录：你选择提交的反馈（如会话转录）仅用于排障与改进功能，不用于模型训练，并在 30 天内保留。
- 数据保留：可使用“零数据保留”组织的 API Key；本地客户端会将会话保留至多 30 天（可配置）。

## 隐私与安全

- 限制保留周期、限制访问
- 不使用反馈训练模型
- 详见商业条款与隐私政策

## 数据流与依赖

Claude Code 本地运行，通过网络与 LLM 通信，数据经 TLS 传输，不在本地加密存储。兼容常见 VPN 与 LLM 代理。更多安全信息参见 Anthropic Trust Center。

## 遥测服务

- Statsig：操作度量（延迟、可靠性、使用模式），不包含代码或路径；可通过 `DISABLE_TELEMETRY` 退出。
- Sentry：错误上报；可通过 `DISABLE_ERROR_REPORTING` 退出。
- /bug：将完整会话历史发送给 Anthropic（可选创建 GitHub issue）；可用 `DISABLE_BUG_COMMAND` 退出。

## 不同提供方的默认行为

使用 Bedrock/Vertex 时默认关闭非必要流量；也可统一通过 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 关闭。所有环境变量可放在 `settings.json` 中。

