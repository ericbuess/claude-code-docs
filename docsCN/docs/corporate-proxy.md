# 企业代理配置

> 配置 Claude Code 使用公司代理，包括环境变量、认证与证书处理。

## 基本代理配置

通过标准环境变量：

```bash
export HTTPS_PROXY=https://proxy.example.com:8080
export HTTP_PROXY=http://proxy.example.com:8080
```

注意：当前不支持 `NO_PROXY` 与 SOCKS 代理。

## 认证

- 基础认证：在代理 URL 中包含用户名密码（不建议明文写入脚本）。
- 证书问题：为自签名或公司证书设置正确的证书包路径：

```bash
export SSL_CERT_FILE=/path/to/certificate-bundle.crt
export NODE_EXTRA_CA_CERTS=/path/to/certificate-bundle.crt
```

## 网络放行

需要访问：`api.anthropic.com`、`statsig.anthropic.com`、`sentry.io`。请在代理与防火墙中放行。

## 相关资源

- 设置
- 环境变量参考
- 故障排查

