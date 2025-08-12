# Hooks 参考

> 本页列出 Claude Code 支持的 Hook 类型、触发时机、配置方式与环境变量约定。

- Hook 类型：PreToolUse、PostToolUse、OnEditApplied、OnSessionStart 等
- 配置位置：项目或用户级 `settings.json`
- 命令形式：字符串 Shell 命令；建议非交互式、可重复执行
- 环境变量：Claude 会在执行时注入上下文（会话、工具、路径等），详见完整参考

示例：
```json
{
  "hooks": {
    "PostToolUse": "./scripts/after_tool.sh $CLAUDE_TOOL $CLAUDE_EXIT_CODE"
  }
}
```

