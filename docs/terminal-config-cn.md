# 优化您的终端设置

> Claude Code在终端正确配置时效果最佳。遵循这些指南来优化您的体验。

### 主题和外观

Claude无法控制您终端的主题。这由您的终端应用程序处理。您可以随时通过`/config`命令将Claude Code的主题与您的终端匹配。

### 换行

您有几种选项可以在Claude Code中输入换行符：

* **快速转义**：输入`\`然后按Enter键创建新行
* **键盘快捷键**：设置键绑定来插入新行

#### 设置Shift+Enter（VS Code或iTerm2）：

在Claude Code中运行`/terminal-setup`来自动配置Shift+Enter。

#### 设置Option+Enter（VS Code、iTerm2或macOS Terminal.app）：

**对于Mac Terminal.app：**

1. 打开设置 → 配置文件 → 键盘
2. 勾选"使用Option作为Meta键"

**对于iTerm2和VS Code终端：**

1. 打开设置 → 配置文件 → 键
2. 在常规下，将左/右Option键设置为"Esc+"

### 通知设置

通过正确的通知配置，永远不会错过Claude完成任务的时机：

#### 终端铃声通知

在任务完成时启用声音警报：

```sh
claude config set --global preferredNotifChannel terminal_bell
```

**对于macOS用户**：不要忘记在系统设置 → 通知 → \[您的终端应用]中启用通知权限。

#### iTerm 2系统通知

对于iTerm 2在任务完成时的警报：

1. 打开iTerm 2偏好设置
2. 导航到配置文件 → 终端
3. 启用"静音铃声"和过滤警报 → "发送转义序列生成的警报"
4. 设置您偏好的通知延迟

请注意，这些通知特定于iTerm 2，在默认的macOS终端中不可用。

#### 自定义通知钩子

对于高级通知处理，您可以创建[通知钩子](/zh-CN/docs/claude-code/hooks#notification)来运行您自己的逻辑。

### 处理大型输入

在处理大量代码或长指令时：

* **避免直接粘贴**：Claude Code可能难以处理非常长的粘贴内容
* **使用基于文件的工作流程**：将内容写入文件并要求Claude读取它
* **注意VS Code限制**：VS Code终端特别容易截断长粘贴

### Vim模式

Claude Code支持Vim键绑定的子集，可以通过`/vim`启用或通过`/config`配置。

支持的子集包括：

* 模式切换：`Esc`（到NORMAL），`i`/`I`，`a`/`A`，`o`/`O`（到INSERT）
* 导航：`h`/`j`/`k`/`l`，`w`/`e`/`b`，`0`/`$`/`^`，`gg`/`G`
* 编辑：`x`，`dw`/`de`/`db`/`dd`/`D`，`cw`/`ce`/`cb`/`cc`/`C`，`.`（重复）
