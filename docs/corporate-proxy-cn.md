# 企业代理配置

> 了解如何配置 Claude Code 以使用企业代理服务器，包括环境变量配置、身份验证和 SSL/TLS 证书处理。

Claude Code 通过环境变量支持标准的 HTTP/HTTPS 代理配置。这允许您将所有 Claude Code 流量通过组织的代理服务器路由，以实现安全、合规和监控目的。

## 基本代理配置

### 环境变量

Claude Code 遵循标准代理环境变量：

```bash
# HTTPS 代理（推荐）
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP 代理（如果 HTTPS 不可用）
export HTTP_PROXY=http://proxy.example.com:8080
```

<Note>
  Claude Code 目前不支持 `NO_PROXY` 环境变量。所有流量都将通过配置的代理路由。
</Note>

<Note>
  Claude Code 不支持 SOCKS 代理。
</Note>

## 身份验证

### 基本身份验证

如果您的代理需要基本身份验证，请在代理 URL 中包含凭据：

```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  避免在脚本中硬编码密码。请使用环境变量或安全凭据存储。
</Warning>

<Tip>
  对于需要高级身份验证（NTLM、Kerberos 等）的代理，请考虑使用支持您的身份验证方法的 LLM Gateway 服务。
</Tip>

### SSL 证书问题

如果您的代理使用自定义 SSL 证书，您可能会遇到证书错误。

确保设置正确的证书包路径：

```bash
export SSL_CERT_FILE=/path/to/certificate-bundle.crt
export NODE_EXTRA_CA_CERTS=/path/to/certificate-bundle.crt
```

## 网络访问要求

Claude Code 需要访问以下 URL：

* `api.anthropic.com` - Claude API 端点
* `statsig.anthropic.com` - 遥测和指标
* `sentry.io` - 错误报告

确保这些 URL 在您的代理配置和防火墙规则中被列入白名单。这在容器化或受限网络环境中使用 Claude Code 时尤其重要。

## 其他资源

* [Claude Code 设置](/zh-CN/docs/claude-code/settings)
* [环境变量参考](/zh-CN/docs/claude-code/settings#environment-variables)
* [故障排除指南](/zh-CN/docs/claude-code/troubleshooting)
