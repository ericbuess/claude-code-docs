# Claude Code GitHub Actions

> 将 Claude Code 集成进你的 GitHub 工作流，用 `@claude` 实现自动分析代码、创建 PR、实现功能与修复 Bug。

当前为 Beta。其构建基于 Claude Code SDK，可用于自定义自动化。

## 优势

- 即刻创建 PR
- 将 Issue 变成代码
- 遵循你的 CLAUDE.md 规范
- 简单上手，安全默认

## 设置

- 终端中运行 `/install-github-app` 快速安装（需仓库管理员权限；直连 Anthropic API 场景）
- 手动：安装 GitHub App、添加 `ANTHROPIC_API_KEY` 到仓库 Secrets、复制示例工作流

## 用法示例

- 在 Issue/PR 评论中 @claude 触发实现/建议/修复

## 最佳实践

- 在仓库根目录维护 `CLAUDE.md`
- 使用 GitHub Secrets 管理密钥
- 关注 CI 与 API 成本

## 与 Bedrock / Vertex 集成

- 通过 OIDC/Workload Identity 配置云端认证，使用你的云内模型调用与计费
- 在仓库 Secrets 中配置相应参数，并在工作流中使用

## 故障排查

- 未响应 `@claude`、CI 未运行、认证错误：检查 App 安装、触发条件、权限与 Secrets

## 进阶

- 可自建 GitHub App 以获得自定义身份与权限控制
- 使用 Action 参数自定义会话回合、超时等

