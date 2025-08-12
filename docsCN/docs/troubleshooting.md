# 故障排查

> 发现并解决 Claude Code 安装与使用中的常见问题。

## 常见安装问题

### Windows（WSL）相关

- 平台检测错误：先运行 `npm config set os linux`；或使用 `npm install -g @anthropic-ai/claude-code --force --no-os-check`（不要用 sudo）。
- 找不到 Node：若运行 `claude` 提示 `exec: node: not found`，请确保 `which npm/node` 指向 Linux 路径（`/usr/...`），而不是 `/mnt/c/...`。建议通过发行版包管理器或 nvm 安装 Node。

### Linux/Mac 权限或 PATH 问题

- 使用 npm 安装时，若全局前缀不可写或 PATH 未配置，可能导致命令不可用。
- 推荐方案：使用原生安装（Beta），`curl -fsSL https://claude.ai/install.sh | bash`（Windows PowerShell 参见文档）。
- 备选方案：`claude migrate-installer` 迁移到本地安装，避免 sudo 需求。

迁移后可用以下命令验证：

```bash
which claude
claude doctor
```

## 权限与认证

- 反复弹出权限：使用 `/permissions` 配置无需确认的工具。详见 IAM 文档。
- 认证问题：`/logout` 完全登出后重启，再次登录；或删除本地 `~/.config/claude-code/auth.json` 后重试。

## 性能与稳定性

- 高 CPU/内存：对大型代码库，建议经常 `/compact`、分阶段重启、忽略构建目录。
- 命令卡住：先 Ctrl+C 取消；必要时重启终端。
- JetBrains 终端 ESC 无效：调整终端按键绑定，删除“Switch focus to Editor”的快捷键。

## 更多帮助

- 在 Claude 中使用 `/bug` 反馈
- 查看 GitHub 仓库的已知问题
- 运行 `/doctor` 检查安装健康状况
- 直接询问 Claude（其内置访问自身文档）

