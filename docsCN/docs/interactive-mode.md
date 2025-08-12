# 交互模式

> 键盘快捷键、输入模式与会话内交互功能参考。

## 键盘快捷键

- 通用控制：
  - Ctrl+C 取消当前输入或生成
  - Ctrl+D 退出会话
  - Ctrl+L 清屏（保留历史）
  - 上/下 访问历史
  - Esc + Esc 编辑上一条消息

- 多行输入：
  - 反斜杠 + Enter（通用）
  - macOS：Option+Enter
  - 运行 `/terminal-setup` 后可用 Shift+Enter
  - 直接粘贴代码/日志

- 快捷前缀：
  - `#` 开头：将内容加入 CLAUDE.md（存储提示）
  - `/` 开头：斜杠命令（见 Slash Commands）

## Vim 模式

通过 `/vim` 开启，或在 `/config` 永久启用。支持常见 NORMAL/INSERT 切换与移动/编辑命令（h j k l、w e b、0 $ ^、gg/G、x dd D、cw/cc/… 等）。

提示：在 iTerm2 与 VS Code 终端可用 `/terminal-setup` 安装 Shift+Enter 绑定。

## 历史记录

- 按目录存储；`/clear` 清除
- 上/下访问；部分终端支持 Ctrl+R 反向搜索
- 默认关闭 `!` 历史展开

## 参阅

- Slash commands（交互命令）
- CLI 参考
- 设置
- Memory 管理（CLAUDE.md）

