---
name: ads-setup
description: Google Ads API 首次配置与认证。安装依赖、生成 refresh token、配置 google-ads.yaml。
---

# Google Ads 配置与认证

## 何时使用
- 首次使用 Google Ads skill
- Refresh token 过期（`RefreshError: invalid_grant`）
- 需要切换 Google 账号

## 执行步骤

### 1. 检查 Python 依赖
```bash
pip3 install google-ads google-auth-oauthlib --user
```

### 2. 检查配置文件
确认 `google ads/google-ads.yaml` 存在且包含以下字段：
```yaml
developer_token: <developer_token>
client_id: <client_id>
client_secret: <client_secret>
refresh_token: <refresh_token>
login_customer_id: <login_customer_id>
use_proto_plus: True
```

如果文件不存在，从 `google ads/google_ads_credentials.json` 中提取 `client_id` 和 `client_secret` 创建。

### 3. 重新认证（获取新 Refresh Token）

运行认证脚本：
```bash
python3 .agents/skills/google-ads/scripts/authenticate.py --client_secrets_path "google ads/google_ads_credentials.json"
```

执行后：
1. 浏览器会自动打开 Google 授权页面
2. 用户选择有 Google Ads 管理权限的账号
3. 如见"未验证应用"警告，点击 **高级 → 转至 (项目名)**
4. 点击 **允许** 授权
5. 复制终端输出的 `Refresh token` 值
6. 更新 `google ads/google-ads.yaml` 中的 `refresh_token` 字段

### 4. 验证连接
```bash
python3 .agents/skills/google-ads/scripts/list_accounts.py
```

成功应输出类似：
```
Accessible Customer Resource Names:
customers/6646561021
customers/8440667876
```

### 5. 建议：发布 OAuth 应用
提醒用户前往 [Google Cloud Console OAuth 同意屏幕](https://console.cloud.google.com/apis/credentials/consent)，将状态从 `Testing` 切换为 `In Production`，这样 refresh token 不会每 7 天过期。
