# 将 Claude Code 添加到您的 IDE

> 了解如何将 Claude Code 添加到您喜爱的 IDE

Claude Code 与流行的集成开发环境 (IDE) 无缝集成，以增强您的编码工作流程。这种集成允许您直接在您首选的开发环境中利用 Claude 的功能。

## 支持的 IDE

Claude Code 目前支持两个主要的 IDE 系列：

* **Visual Studio Code**（包括 Cursor 和 Windsurf 等流行分支）
* **JetBrains IDEs**（包括 PyCharm、WebStorm、IntelliJ 和 GoLand）

## 功能

* **快速启动**：使用 `Cmd+Esc`（Mac）或 `Ctrl+Esc`（Windows/Linux）直接从编辑器打开 Claude Code，或点击 UI 中的 Claude Code 按钮
* **差异查看**：代码更改可以直接在 IDE 差异查看器中显示，而不是在终端中。您可以在 `/config` 中配置此功能
* **选择上下文**：IDE 中的当前选择/标签页会自动与 Claude Code 共享
* **文件引用快捷键**：使用 `Cmd+Option+K`（Mac）或 `Alt+Ctrl+K`（Linux/Windows）插入文件引用（例如，@File#L1-99）
* **诊断共享**：IDE 中的诊断错误（lint、语法等）会在您工作时自动与 Claude 共享

## 安装

### VS Code

1. 打开 VSCode
2. 打开集成终端
3. 运行 `claude` - 扩展将自动安装

今后您也可以在任何外部终端中使用 `/ide` 命令连接到 IDE。

<Note>
  这些安装说明也适用于 VS Code 分支，如 Cursor 和 Windsurf。
</Note>

### JetBrains IDEs

从市场安装 [Claude Code 插件](https://docs.anthropic.com/s/claude-code-jetbrains) 并重启您的 IDE。

<Note>
  当您在集成终端中运行 `claude` 时，插件也可能会自动安装。必须完全重启 IDE 才能生效。
</Note>

<Warning>
  **远程开发限制**：使用 JetBrains 远程开发时，您必须通过 `Settings > Plugin (Host)` 在远程主机中安装插件。
</Warning>

## 配置

两种集成都与 Claude Code 的配置系统兼容。要启用 IDE 特定功能：

1. 通过在内置终端中运行 `claude` 将 Claude Code 连接到您的 IDE
2. 运行 `/config` 命令
3. 将差异工具设置为 `auto` 以进行自动 IDE 检测
4. Claude Code 将根据您的 IDE 自动使用适当的查看器

如果您使用外部终端（而不是 IDE 的内置终端），您仍然可以在启动 Claude Code 后使用 `/ide` 命令连接到您的 IDE。这允许您即使从单独的终端应用程序运行 Claude 时也能受益于 IDE 集成功能。这适用于 VS Code 和 JetBrains IDEs。

<Note>
  使用外部终端时，为确保 Claude 默认访问与您的 IDE 相同的文件，请从与您的 IDE 项目根目录相同的目录启动 Claude。
</Note>

## 故障排除

### VS Code 扩展未安装

* 确保您从 VS Code 的集成终端运行 Claude Code
* 确保安装了与您的 IDE 对应的 CLI：
  * 对于 VS Code：`code` 命令应该可用
  * 对于 Cursor：`cursor` 命令应该可用
  * 对于 Windsurf：`windsurf` 命令应该可用
  * 如果未安装，使用 `Cmd+Shift+P`（Mac）或 `Ctrl+Shift+P`（Windows/Linux）并搜索"Shell Command: Install 'code' command in PATH"（或您的 IDE 的等效命令）
* 检查 VS Code 是否有安装扩展的权限

### JetBrains 插件不工作

* 确保您从项目根目录运行 Claude Code
* 检查 JetBrains 插件是否在 IDE 设置中启用
* 完全重启 IDE。您可能需要多次执行此操作
* 对于 JetBrains 远程开发，确保 Claude Code 插件安装在远程主机中，而不是本地客户端上

如需更多帮助，请参考我们的[故障排除指南](/zh-CN/docs/claude-code/troubleshooting)或联系支持。
