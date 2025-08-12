# 开发容器（Devcontainer）

> 了解 Claude Code 的参考开发容器，适合需要一致、隔离且更安全环境的团队。

提供参考配置与 Dockerfile，可直接使用或按需定制。容器附带网络防火墙策略，便于在无人值守时使用 `--dangerously-skip-permissions`（仍需谨慎）。

## 关键特性

- 生产就绪的 Node.js 20 环境
- 自定义防火墙，仅放行必要域名
- 预装 git、Zsh、fzf 等开发工具
- VS Code 扩展与设置
- 会话持久化
- 跨平台工作

## 快速开始

1. 安装 VS Code 与 Dev Containers 扩展
2. 克隆参考实现仓库
3. 在 VS Code 打开并选择“在容器中重新打开”

## 安全与自定义

- 默认拒绝策略，仅放行必要网络
- 可按需增删扩展、调整资源、放行目标域名、定制 Shell 与工具链

## 相关资源

- VS Code devcontainers 文档
- 安全最佳实践
- 企业代理配置

