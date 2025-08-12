# 故障排除

> 发现Claude Code安装和使用中常见问题的解决方案。

## 常见安装问题

### Windows安装问题：WSL中的错误

您可能在WSL中遇到以下问题：

**操作系统/平台检测问题**：如果您在安装过程中收到错误，WSL可能正在使用Windows的`npm`。请尝试：

* 在安装前运行`npm config set os linux`
* 使用`npm install -g @anthropic-ai/claude-code --force --no-os-check`进行安装（不要使用`sudo`）

**找不到Node错误**：如果您在运行`claude`时看到`exec: node: not found`，您的WSL环境可能正在使用Windows安装的Node.js。您可以通过`which npm`和`which node`来确认这一点，它们应该指向以`/usr/`开头的Linux路径，而不是`/mnt/c/`。要解决此问题，请尝试通过Linux发行版的包管理器或通过[`nvm`](https://github.com/nvm-sh/nvm)安装Node。

### Linux和Mac安装问题：权限或找不到命令错误

使用npm安装Claude Code时，`PATH`问题可能会阻止访问`claude`。
如果您的npm全局前缀不可用户写入（例如`/usr`或`/usr/local`），您也可能遇到权限错误。

#### 推荐解决方案：原生Claude Code安装

Claude Code有一个不依赖npm或Node.js的原生安装。

<Note>
  原生Claude Code安装程序目前处于测试阶段。
</Note>

使用以下命令运行原生安装程序。

**macOS、Linux、WSL：**

```bash
# 安装稳定版本（默认）
curl -fsSL https://claude.ai/install.sh | bash

# 安装最新版本
curl -fsSL https://claude.ai/install.sh | bash -s latest

# 安装特定版本号
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell：**

```powershell
# 安装稳定版本（默认）
irm https://claude.ai/install.ps1 | iex

# 安装最新版本
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# 安装特定版本号
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

此命令为您的操作系统和架构安装适当的Claude Code构建，并在`~/.local/bin/claude`处添加指向安装的符号链接。

<Tip>
  确保您的系统PATH中包含安装目录。
</Tip>

#### 替代解决方案：迁移到本地安装

或者，如果Claude Code可以运行，您可以迁移到本地安装：

```bash
claude migrate-installer
```

这会将Claude Code移动到`~/.claude/local/`并在您的shell配置中设置别名。未来更新不需要`sudo`。

迁移后，重启您的shell，然后验证您的安装：

在macOS/Linux/WSL上：

```bash
which claude  # 应该显示指向~/.claude/local/claude的别名
```

在Windows上：

```powershell
where claude  # 应该显示claude可执行文件的路径
```

验证安装：

```bash
claude doctor # 检查安装健康状况
```

## 权限和身份验证

### 重复的权限提示

如果您发现自己重复批准相同的命令，您可以使用`/permissions`命令允许特定工具在无需批准的情况下运行。请参阅[权限文档](/zh-CN/docs/claude-code/iam#configuring-permissions)。

### 身份验证问题

如果您遇到身份验证问题：

1. 运行`/logout`完全退出登录
2. 关闭Claude Code
3. 使用`claude`重启并再次完成身份验证过程

如果问题持续存在，请尝试：

```bash
rm -rf ~/.config/claude-code/auth.json
claude
```

这会删除您存储的身份验证信息并强制进行全新登录。

## 性能和稳定性

### 高CPU或内存使用率

Claude Code设计用于与大多数开发环境配合使用，但在处理大型代码库时可能会消耗大量资源。如果您遇到性能问题：

1. 定期使用`/compact`来减少上下文大小
2. 在主要任务之间关闭并重启Claude Code
3. 考虑将大型构建目录添加到您的`.gitignore`文件中

### 命令挂起或冻结

如果Claude Code似乎无响应：

1. 按Ctrl+C尝试取消当前操作
2. 如果无响应，您可能需要关闭终端并重启

### ESC键在JetBrains（IntelliJ、PyCharm等）终端中不工作

如果您在JetBrains终端中使用Claude Code，而ESC键没有按预期中断代理，这可能是由于与JetBrains默认快捷键的键绑定冲突。

要解决此问题：

1. 转到设置 → 工具 → 终端
2. 点击"覆盖IDE快捷键"旁边的"配置终端键绑定"超链接
3. 在终端键绑定中，向下滚动到"切换焦点到编辑器"并删除该快捷键

这将允许ESC键正确用于取消Claude Code操作，而不是被PyCharm的"切换焦点到编辑器"操作捕获。

## 获取更多帮助

如果您遇到此处未涵盖的问题：

1. 在Claude Code中使用`/bug`命令直接向Anthropic报告问题
2. 查看[GitHub存储库](https://github.com/anthropics/claude-code)了解已知问题
3. 运行`/doctor`检查您的Claude Code安装健康状况
4. 直接询问Claude关于其功能和特性 - Claude内置了对其文档的访问权限
