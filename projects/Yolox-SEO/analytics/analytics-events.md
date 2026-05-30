# GA4 事件 Schema（YOLOX）

**版本**：v2.3 · 2026-04-29（v2.2 基础上补 GA4 自动事件参考 + 重复关系处理 + 用例对照表）
**交付等级**：🟢 结实 — 埋点清单的唯一依据；新人 / 4 个月后回看 5 分钟入门
**配套代码**：`src/lib/analytics.ts`（所有事件必须通过这里发，不允许组件里直写 `gtag(...)`）

> **v2.3 新增**：§11 GA4 自动事件参考（Enhanced Measurement 11 个）+ §12 重复关系处理（含 2026-04-29 关闭 GA4 `scroll` 决策）+ §13 用例对照表（"我想看 X 用哪个事件"）。15 个自定义事件 schema 不变。
>
> **v2.2 变更理由**：付费完成改发 GA4 推荐电商事件 `purchase`，携带 `transaction_id` / `value` / `currency` / `items`，确保 Monetization / revenue 报表和交易去重语义正确；注册流移除 referralSource UI 和自定义参数。

---

## 0. v1 → v2 变更摘要

按同事方案 rename + 补漏：

| v1 (废弃) | v2 (现行) | 说明 |
|---|---|---|
| `sign_up` | `auth_register_complete` | rename |
| `agent_install` | `agent_instantiated` | rename |
| `pack_purchase` | `purchase` | 使用 GA4 推荐电商事件（value/currency/transaction_id/items）|
| `cta_click(location: "home_hero")` | `lp_hero_input_submit` | rename，去参数 |
| `pricing_view` / `compare_page_view` / `video_play` / `copy_code_snippet` | — | 删除（未实装 placeholder，等对应功能上线再建）|
| — | `auth_login_complete` | 新增 |
| — | `lp_auth_btn_click` | 新增（Header 登录按钮）|
| — | `onboarding_team_generated` | 新增（占位，触发点待确认）|
| — | `store_card_click` | 新增（列表页卡片点击）|
| — | `message_sent` | 新增（频道 / agent 发消息）|
| — | `agent_deleted` | 新增 |
| — | `credits_low_modal_view` | 新增（漏斗起点）|
| — | `credits_modal_open` | 新增（漏斗中段）|
| — | `credits_package_select` | 新增（漏斗关键诊断）|

共 **15 个事件**。

## 0.1 v2.0 → v2.1 变更摘要（砍参数）

按"非必要不加参数"方针：

| 事件 | v2.0 参数 | v2.1 参数 | 变动 |
|---|---|---|---|
| `auth_register_complete` | method + referral_source + invite_code_used | **（无）** | 全砍 |
| `auth_login_complete` | method | **（无）** | 砍 method |
| `store_card_click` | store_type + card_id + card_name | **store_type + card_name** | 砍 card_id |
| `agent_view` | agent_id + source | **agent_id** | 砍 source（用 GA4 built-in `page_referrer`）|
| `message_sent` | surface + target_id | **（无）** | 全砍（surface 用 page_location 侧面分析）|
| `agent_instantiated` | agent_id + agent_name + source | **agent_id** | 砍 agent_name / source |
| `scroll_depth` | percent + page_path | **percent** | 砍 page_path（用 GA4 built-in `page_location`）|

**保留的扩展参数**（必要）：
- `purchase.value / currency / transaction_id / items` — GA4 ecommerce 预定义字段，Monetization 报表自动消费

**GA4 Custom Dimension 配额账**（免费版 50 event-scope + 25 user-scope）：
- 仅需注册 `app_version` / `env`（如要按版本和环境做自定义报表）

---

## 1. 通用约定

### 1.1 公共参数（自动附带，无需每事件手加）

所有事件自动携带以下参数（在 `GoogleAnalytics.tsx` 里 `gtag('config')` 一次设置，所有后续事件继承）：

| 参数 | 说明 | 示例 | 配置位置 |
|---|---|---|---|
| `app_version` | 应用版本 | `"0.4.0"` | `NEXT_PUBLIC_APP_VERSION` env 或 hardcode |
| `env` | 环境 | `"production"` / `"beta"` / `"development"` | `NEXT_PUBLIC_APP_ENV` |
| `event_timestamp` | 事件触发时间（微秒）| 自动 | GA4 默认字段 |
| `user_id` | 内部用户 UUID（**禁止**邮箱）| `"u_abc123"` | 登录成功后 `gtag('config', { user_id })` 设一次 |

### 1.2 命名规范

- **事件名**：snake_case，全小写（`auth_register_complete` ✅ / `authRegisterComplete` ❌）
- **参数名**：snake_case
- **参数值（字符串）**：snake_case 或具体标识符

### 1.3 参数值类型

GA4 仅接受 `string` / `number` / `boolean`。不传 `undefined`（发出去变字面量 `"undefined"`）。

### 1.4 🔑 PII 禁令

绝不放入事件参数：邮箱、姓名、手机号、物理地址、IP、信用卡号。

代码层有运行时检测（`src/lib/analytics.ts` 的 `trackEvent` 对包含 `@xxx.yy` 的字符串值 dev 模式 `console.warn`）。

---

## 2. Landing Page

| Event | 触发位置 | 参数 | Wrapper 函数 |
|---|---|---|---|
| `lp_hero_input_submit` | `HomeLayout.tsx` 的 `handleHeroSubmit`（Hero "Build My Team" CTA）| — | `trackLpHeroInputSubmit()` |
| `lp_auth_btn_click` | `Header.tsx` 的 `handleActionClick`（仅当 actionHref === "/login"）| — | `trackLpAuthBtnClick()` |

> **关于 page_view**：GA4 自动发 `page_view` 事件 + `page_location` / `page_title` 参数覆盖。**不需要额外埋** `lp_page_view` / `auth_page_view` 等变体。

---

## 3. Auth / Onboarding

| Event | 触发位置 | 参数 | Wrapper |
|---|---|---|---|
| `auth_register_complete` | email 流：`RegisterLayout.tsx` 注册 API 成功后<br>Google 流：`/auth/google/callback` 且 `state.source === "register"` | — | `trackAuthRegisterComplete()` |
| `auth_login_complete` | email 流：`LoginLayout.tsx:handleLoginSuccess`<br>Google 流：`/auth/google/callback` 且 `state.source !== "register"` | — | `trackAuthLoginComplete()` |
| `onboarding_team_generated` | **触发点待确认**（平台 onboarding 流里"团队生成完成"的回调）| — | `trackOnboardingTeamGenerated()` |

### Conversion 标记（GA4 Admin 手动配）

- `auth_register_complete` → ✅ Conversion
- `auth_login_complete` → ❌（不是转化，只是活跃度）

---

## 4. Store

| Event | 触发位置 | 参数 | Wrapper |
|---|---|---|---|
| `store_card_click` | `AgentsStoreLayout.tsx`（agents + teams 共用）+ `SkillsStoreLayout.tsx` 的卡片 onClick | `store_type`: `"skill"` / `"agent"` / `"team"`<br>`card_name`: 卡片显示名 | `trackStoreCardClick({ storeType, cardName })` |
| `agent_view` | `AgentDetailLayout.tsx` mount useEffect，按 `agent.templateName` 依赖 | `agent_id`: agent templateName | `trackAgentView({ agentId })` |

### store_card_click 和 agent_view 的关系

- **store_card_click**：用户在**列表页**上点卡片（跳 detail 前的最后一步）
- **agent_view**：**detail 页** mount（可能从 list 点进来，也可能从外部链接直接进来）

两者互补：`store_card_click` 看**列表 CTR**，`agent_view` 看**detail 覆盖度**。

> **分流（"从哪来"的分析）** 用 GA4 built-in `page_referrer` 字段替代自定义 source 参数。GA4 Exploration / Free-form 报表里可直接按 `page_referrer` 分组。

---

## 5. Workspace

| Event | 触发位置 | 参数 | Wrapper |
|---|---|---|---|
| `message_sent` | channel 流：`useChannelConversationSession.ts:sendChannelMessage`<br>agent 流：`useAgentConversationSession.ts:sendAgentMessage`（过 content 非空校验后立即触发）| — | `trackMessageSent()` |
| `agent_instantiated` | `AgentDetailLayout.tsx:handleInstall` 的 `response.ok` 分支 | `agent_id`: templateName | `trackAgentInstantiated({ agentId })` |
| `agent_deleted` | `ClientHomeLayout.tsx:handleDeleteAgent` 的 `result.ok === true` 分支 | `agent_id`: agent.id | `trackAgentDeleted({ agentId })` |

### Conversion 标记

- `agent_instantiated` → ✅ Conversion（业务核心转化）

---

## 6. Credits / Billing 漏斗

| Event | 触发位置 | 参数 | Wrapper |
|---|---|---|---|
| `credits_low_modal_view` | `useBillingController.ts` 的 `showInsufficientCredits` state 变 true 的 useEffect | — | `trackCreditsLowModalView()` |
| `credits_modal_open` | `useBillingController.ts:openQuotaModal` | — | `trackCreditsModalOpen()` |
| `credits_package_select` | `useBillingController.ts:handlePurchasePack`（Stripe redirect 前）| `package_name`: pack.key（如 `"starter_10"`）| `trackCreditsPackageSelect({ packageName })` |
| `purchase` | `useBillingController.ts` 消费 `pendingPayment.result === "success"` 后 | `transaction_id`: orderId<br>`value`: amountCents / 100<br>`currency`: `"USD"`<br>`items`: 购买包 item | `trackCreditsPurchaseComplete({ packageName, value, currency, transactionId })` |

### 漏斗链

```
credits_low_modal_view（触发充值）
  ↓
credits_modal_open（用户主动打开充值弹窗，两种路径之一）
  ↓
credits_package_select（选了某档）
  ↓
[ Stripe checkout（站外）]
  ↓
purchase（回站幂等触发）
```

### Conversion 标记

- `purchase` → ✅ Conversion / Monetization（业务核心转化）

### 幂等保护

`useBillingController` 消费成功 session 后立即清理 sessionStorage，并用 `paymentSessionHandledRef.current` 防止当前 React 实例内重复处理。

---

## 7. Engagement

| Event | 触发位置 | 参数 | Wrapper |
|---|---|---|---|
| `scroll_depth` | `src/lib/useScrollDepth.ts`，挂 `HomeLayout` | `percent`: `25` / `50` / `75` / `100` | `trackScrollDepth({ percent })` |

> **页面维度** 用 GA4 built-in `page_location` / `page_title` 替代自定义 `page_path` 参数。

---

## 8. 完整事件清单（速查）

| # | Event | 层级 | Conversion? | 参数 |
|---|---|---|---|---|
| 1 | `lp_hero_input_submit` | 2 | ❌ | — |
| 2 | `lp_auth_btn_click` | 2 | ❌ | — |
| 3 | `auth_register_complete` | 1 | ✅ | — |
| 4 | `auth_login_complete` | 2 | ❌ | — |
| 5 | `onboarding_team_generated` | 2 | ❌ | — |
| 6 | `store_card_click` | 2 | ❌ | store_type / card_name |
| 7 | `agent_view` | 2 | ❌ | agent_id |
| 8 | `message_sent` | 2 | ❌ | — |
| 9 | `agent_instantiated` | 1 | ✅ | agent_id |
| 10 | `agent_deleted` | 2 | ❌ | agent_id |
| 11 | `credits_low_modal_view` | 2 | ❌ | — |
| 12 | `credits_modal_open` | 2 | ❌ | — |
| 13 | `credits_package_select` | 2 | ❌ | package_name |
| 14 | `purchase` | 1 | ✅ | transaction_id / value / currency / items |
| 15 | `scroll_depth` | 3 | ❌ | percent |

---

## 9. GA4 Admin 配置 checklist

### Custom dimensions（User scope，必建）

| Dimension name | User property | 来源 |
|---|---|---|
| `app_version` | `app_version` | gtag config |
| `env` | `env` | gtag config |

### Conversions 标记（Event scope）

在 Admin → Events 找到以下，toggle "Mark as conversion"：
- `auth_register_complete`
- `agent_instantiated`
- `purchase`

---

## 10. 验收清单

- [ ] `src/lib/analytics.ts` 所有 wrapper 和 Event union type 对应
- [ ] 所有事件名 snake_case
- [ ] 所有参数 snake_case，无 camelCase
- [ ] `GoogleAnalytics.tsx` 已 set `app_version` + `env`
- [ ] 登录成功时 set `user_id`（🔴 待后端返回 userId）
- [ ] 无 PII 参数
- [ ] GA4 Admin 必要 Custom dimension 建好（`app_version` / `env`）
- [ ] GA4 Admin 3 个 Conversion 标记打开
- [ ] GA4 Realtime 能看到所有一级事件触发

---

## 11. GA4 自动事件参考（Enhanced Measurement）

GA4 出厂自带 **Enhanced Measurement**，开通就自动采集事件，**不需要任何代码**。位置：GA4 → 管理 → 数据流 → 选 web stream → Enhanced Measurement 齿轮。

### 11.1 不可关的 3 个核心事件

| 事件 | 触发 | 主要参数 | 用例 |
|---|---|---|---|
| `session_start` | 30 分钟无活动后再访问 = 新会话 | — | 会话基数；渠道分析的单位 |
| `first_visit` | 用户首次访问（按 device_id 算）| — | 新访客 vs 老访客统计 |
| `user_engagement` | 页面焦点 ≥10s | `engagement_time_msec` | 互动时长；GA4 没传统跳出率，用这个反向算 |

### 11.2 Enhanced Measurement 可开关 8 个

| 事件 | 我们的状态 | 触发 | 主要参数 |
|---|---|---|---|
| `page_view` | ✅ 启用 | 页面加载（含 SPA 路由切换）| `page_location` / `page_title` / `page_referrer` |
| `scroll` | ❌ **已关**（2026-04-29，与 `scroll_depth` 重复，详见 §12.1）| 滚动到 90% | `percent_scrolled: 90` |
| `click` | ✅ 启用 | 点击外链（域名 ≠ yolox.ai）| `link_url` / `link_domain` / `outbound: true` |
| `view_search_results` | ✅ 启用 | URL 含 `?s=` `?q=` `?search=` 等 | `search_term` |
| `file_download` | ✅ 启用 | 下载 pdf/docx/xlsx/zip 等 | `file_name` / `file_extension` |
| `video_start` / `video_progress` / `video_complete` | ✅ 启用（站内目前无视频）| YouTube 嵌入视频播放 | `video_title` / `video_percent` |
| `form_start` / `form_submit` | ✅ 启用 | 任意表单字段 focus / 提交 | `form_id` / `form_destination` |

> **配置原则**：除非和我们自定义事件**直接重复**（如 `scroll` vs `scroll_depth`），其他 GA4 自动事件全部保留。它们是兜底数据 + 通用指标的来源，关掉得不偿失。

---

## 12. GA4 自动 vs 自定义事件 · 重复关系处理

### 12.1 直接重复（已处理）

| GA4 自动 | 我们的 | 关系 | 决策 |
|---|---|---|---|
| `scroll`（仅 90%）| `scroll_depth`（25/50/75/100）| **粒度重复**：GA4 粗，我们细 4 倍 | ❌ **关 GA4 scroll**（2026-04-29 操作），保留我们的 |
| `form_start` / `form_submit` | `lp_hero_input_submit` / `auth_register_complete` | **范围重叠**：GA4 覆盖所有表单（含我们没埋的边角），我们覆盖核心转化点 | ✅ **都保留**，事件名不同 GA4 不会双计；GA4 当兜底，我们做精确决策 |
| `click`（外链）| `lp_auth_btn_click`（站内 CTA） | **scope 不同**：GA4 只追外链，我们追站内特定按钮 | ✅ **都保留**，互不干扰 |

### 12.2 GA4 推荐事件命名（[Recommended Events](https://support.google.com/analytics/answer/9267735)）

GA4 有一套推荐事件命名规范，按它命名能享受预定义报告（如 Monetization）。我们的对齐情况：

| GA4 推荐 | 我们的 | 是否对齐 | 说明 |
|---|---|---|---|
| `purchase` | `purchase` | ✅ **对齐**（v2.2 起）| 完全采用 GA4 推荐命名 + 标准 ecommerce 字段（value/currency/transaction_id/items），自动进 Monetization 报表 |
| `sign_up` | `auth_register_complete` | ❌ **不对齐** | GA4 推荐命名太粗，无法区分邮箱 / Google / 邀请码渠道；保留我们更语义化的命名 |
| `login` | `auth_login_complete` | ❌ **不对齐** | 同上 |

### 12.3 完全没重复（我们独有的业务事件）

`agent_view` / `agent_instantiated` / `agent_deleted` / `message_sent` / `store_card_click` / `credits_modal_open` / `credits_package_select` / `credits_low_modal_view` / `onboarding_team_generated` / `lp_hero_input_submit` / `lp_auth_btn_click` / `scroll_depth` —— 这些都是产品业务事件，GA4 不会替你埋。

---

## 13. 用例对照表（"我想看 X，用哪个事件"）

| 业务问题 | 用哪个事件 | 来源 |
|---|---|---|
| 上周新访客多少 | `first_visit` | GA4 自动 |
| DAU / 总互动时长 / 跳出率 | `user_engagement` | GA4 自动 |
| 上周来了多少 session | `session_start` | GA4 自动 |
| Landing page 表现（流量 + 注册转化）| `page_view` × `page_location` 过滤 + `auth_register_complete` | GA4 自动 + 我们 |
| 首页谁读到底 | `scroll_depth` (percent=100) | 我们 |
| 用户最常去哪个外站 | `click` × `link_domain` | GA4 自动 |
| 站内搜索词 | `view_search_results` × `search_term` | GA4 自动 |
| 上周注册多少 | `auth_register_complete` | 我们 |
| 注册渠道归因 | `session_default_channel_group`（GA4 built-in 渠道分组）+ `auth_register_complete` Conversion | GA4 自动（v2.2 起 referral_source 自报已移除）|
| onboarding 完成率 | `onboarding_team_generated` ÷ `auth_register_complete` | 我们 |
| 哪类商店卡片最热 | `store_card_click` × `store_type` / `card_name` | 我们 |
| 列表 → detail 转化 | `agent_view` ÷ `store_card_click` (store_type=agent) | 我们 |
| 装机最多 agent | `agent_instantiated` × `agent_id` | 我们 |
| 装了又删的 agent（流失诊断）| `agent_deleted` × `agent_id` | 我们 |
| DAU 后实际用了产品 | `message_sent` 唯一用户 | 我们 |
| 充值漏斗 4 段 | `credits_low_modal_view` → `credits_modal_open` → `credits_package_select` → `purchase` | 我们 |
| 哪档套餐卖得好 | `credits_package_select` / `purchase` × `package_name` | 我们 |
| GMV | `purchase` (sum `value`) | 我们 |

> **零流量期归因警告**：v2.2 移除自报 `referral_source` 后，渠道归因完全依赖 GA4 built-in `session_default_channel_group`。该字段在月 signup < 100 时统计上不可靠（playbook §2.2.2 关于 self-reported attribution 的论点）。AI 搜索（ChatGPT / Perplexity）来的访客 GA4 通常归到 "Direct" 或 "Referral"，区分能力差。考虑后续在 SEO 里程碑达成（DR > 20 / 月 signup > 100）时讨论是否恢复自报字段。

---

## 14. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-22 | v1.0 | 初版（sign_up / agent_install / pack_purchase / cta_click 等）|
| 2026-04-23 | v2.0 | 按同事方案重命名 + 补漏 9 个事件 + 公共参数走 gtag config |
| 2026-04-23 | v2.1 | 按同事反馈"非必要不加参数"砍 10 个扩展参数，保留 referral_source + ecommerce 三字段 |
| 2026-04-29 | v2.2 | 付费完成改发 GA4 `purchase`，移除 referralSource UI 和参数 |
| 2026-04-29 | v2.3 | 补 §11 GA4 自动事件参考 + §12 重复关系处理（含关闭 GA4 `scroll`）+ §13 用例对照表 |
