# 卸载 Claude Code 文档镜像

## 快速卸载

### 适用于 v0.3+（安装在 ~/.claude-code-docs）

任意位置运行：
```bash
~/.claude-code-docs/uninstall.sh
```

或使用 docs 命令：
```bash
/docs uninstall
```

### 适用于 v0.2 或更旧版本（自定义安装位置）

进入安装目录并运行：
```bash
./uninstall.sh
```

## 会移除哪些内容

卸载程序将移除：

1. `/docs` 命令：`~/.claude/commands/docs.md`
2. `~/.claude/settings.json` 中的自动更新 Hook
3. 安装目录：
   - v0.3+：`~/.claude-code-docs`
   - v0.2 或更旧：你自定义的安装路径

## 手动卸载

如果你更倾向于手动卸载：

### 1. 移除命令文件
```bash
rm -f ~/.claude/commands/docs.md
```

### 2. 从 Claude 设置中移除 Hook
通过 Claude Code CLI 的 /hooks，或编辑 `~/.claude/settings.json` 删除与 claude-code-docs 相关的 PreToolUse Hook。

### 3. 删除安装目录

对于 v0.3+：
```bash
rm -rf ~/.claude-code-docs
```

旧版本：
```bash
rm -rf /path/to/your/claude-code-docs
```

## 多处安装

如果你曾多次安装（例如测试不同版本），卸载程序会提示发现其它位置。需要你手动分别移除。

查找所有安装：
```bash
find ~ -name "claude-code-docs" -type d 2>/dev/null | grep -v ".claude-code-docs"
```

## 备份

卸载时可能会把 `~/.claude/settings.json` 备份为 `~/.claude/settings.json.backup`。

## 完全移除后可能残留

- `~/.claude/settings.json.backup`（如执行了 Hook 移除）
- 你在安装目录中自定义添加的文件

## 重新安装

卸载后重新安装：
```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

