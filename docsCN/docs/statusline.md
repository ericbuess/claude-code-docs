# 状态栏（Status line）配置

> 在 Claude Code 界面底部显示自定义状态栏，呈现当前模型、工作目录、git 分支等上下文信息。

## 创建自定义状态栏

- 运行 `/statusline` 让 Claude 协助生成；或
- 在 `.claude/settings.json` 添加 `statusLine`：
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

工作原理：会话更新触发刷新（至多每 300ms 一次）；命令 stdout 第一行作为文本；支持 ANSI 颜色；当前会话上下文以 JSON 通过 stdin 传入。

提供 Bash/Python/Node 示例脚本，演示从 JSON 读取并输出状态文本、检测 git 分支等。

