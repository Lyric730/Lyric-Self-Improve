# YOLOX 数据埋点审核文档

**版本**：v1.2 · 2026-04-29（修正 GA4 purchase 语义，移除 referralSource）
**目的**：给小刀老师审核用（不需要技术背景也能看懂），同时发给同事 / 杨林对齐
**数据去向**：Google Analytics 4（唯一目的地）
- Production property: `G-JP6DSCZRJT`（线上真实数据）
- Non-production property: `G-4SMM87VGMB`（本地 dev + beta 测试数据）

> **v1.2 变更说明**：注册流不再收集 referralSource；付费完成改发 GA4 推荐电商事件 `purchase`，携带 `transaction_id` / `value` / `currency` / `items`，用于 Monetization / revenue 报表和交易去重。

---

## 0. 一眼看懂

| 项 | 数字 |
|---|---|
| 已实装事件 | **14 个** |
| 占位待埋事件 | **1 个**（`onboarding_team_generated`）|
| 改动文件数 | 11 个（10 个业务组件 + 1 个统一封装层）|
| 发送目的地 | Google Analytics 4（前端 gtag.js 直连，未经过后端）|
| 本地已验证 | scroll_depth / lp_hero_input_submit（你之前截图确认）|
| 本地环境限制未验证 | agent_view / agent_instantiated / 付费链 / 注册 / 登录（prod Realtime 验证）|

---

## 1. 15 个事件速查表

| # | Event | 业务动作（PM 视角） | 埋在哪个文件 | 参数 | 状态 |
|---|---|---|---|---|---|
| 1 | `lp_hero_input_submit` | 首页主 CTA 点击 | `HomeLayout.tsx:359` | — | ✅ 实装 |
| 2 | `lp_auth_btn_click` | 导航栏"开始使用"点击 | `Header.tsx:40` | — | ✅ 实装 |
| 3 | `auth_register_complete` | 注册完成 | `RegisterLayout.tsx` + `google/callback:51` | — | ✅ 实装 |
| 4 | `auth_login_complete` | 登录完成 | `LoginLayout.tsx:37` + `google/callback:53` | — | ✅ 实装 |
| 5 | `onboarding_team_generated` | 团队生成完成 | **未埋** | — | ⚠️ 占位 |
| 6 | `store_card_click` | 商店列表页点卡片 | `AgentsStoreLayout.tsx:468` + `SkillsStoreLayout.tsx:215` | store_type / card_name | ✅ 实装 |
| 7 | `agent_view` | Agent 详情页打开 | `AgentDetailLayout.tsx:59` | agent_id | ✅ 实装 |
| 8 | `message_sent` | 在 channel / agent 发消息 | `useChannelConversationSession.ts:804` + `useAgentConversationSession.ts:1039` | — | ✅ 实装 |
| 9 | `agent_instantiated` | Agent 安装/雇佣成功 | `AgentDetailLayout.tsx:117` | agent_id | ✅ 实装（前端视角，**语义待和杨林 align**） |
| 10 | `agent_deleted` | 删除 Agent 成功 | `ClientHomeLayout.tsx:757` | agent_id | ✅ 实装 |
| 11 | `credits_low_modal_view` | 余额不足弹窗出现 | `useBillingController.ts:160` | — | ✅ 实装 |
| 12 | `credits_modal_open` | 充值弹窗打开 | `useBillingController.ts:96` | — | ✅ 实装 |
| 13 | `credits_package_select` | 选了某档充值包（Stripe 前）| `useBillingController.ts:126` | package_name | ✅ 实装 |
| 14 | `purchase` | 支付成功回站 | `useBillingController.ts` | transaction_id / value / currency / items | ✅ 实装（**前端兜底，后端 webhook 更可靠，待杨林补**）|
| 15 | `scroll_depth` | 首页滚动深度（25/50/75/100%）| `useScrollDepth.ts:43` | percent | ✅ 实装 |

**统一封装层**：`src/lib/analytics.ts`（199 行）所有埋点只通过它调用 gtag，组件里不允许直写。

---

## 2. 公共参数（所有事件自动携带）

这些不是每个事件手加的，而是 `src/components/analytics/GoogleAnalytics.tsx` 里 `gtag('config')` 一次性设置，GA4 自动把它们附加到每个 event。

| 参数 | 值 | 来源 | 配置位置 |
|---|---|---|---|
| `app_version` | `"0.4.0"` | package.json 版本号 | `NEXT_PUBLIC_APP_VERSION` env 或 hardcode |
| `env` | `"production"` / `"beta"` / `"development"` | `NEXT_PUBLIC_APP_ENV` | gtag config 继承 |
| `event_timestamp` | 自动（微秒精度） | GA4 内置字段 | 无需设置 |
| `page_location` | 当前完整 URL | GA4 内置 | 无需设置 |
| `page_title` | 当前页标题 | GA4 内置 | 无需设置 |
| `client_id` | GA4 为每个匿名用户生成的 UUID | GA4 自动管理 | 无需设置 |
| `user_id` | 内部用户 UUID（登录后）| **⚠️ 待后端确认字段名** | `handleLoginSuccess` 里 `gtag('config', { user_id })` |

### 🔑 PII 禁令

**所有事件参数**都**禁止**放入：邮箱、姓名、手机号、物理地址、精确 IP、信用卡号。代码有运行时检测（包含 `@xxx.yy` 的字符串值 dev 模式 `console.warn`）。

---

## 3. 每个事件的详细审核页

---

### 3.1 `lp_hero_input_submit`

**业务意图**：首页主转化路径的入口点击。

**用户场景**（PM 视角）：
> 用户打开 yolox.ai 首页 → 在 Hero 的大输入框里打了字 → 点 "Build My Team" 按钮 → 此时触发。

**代码位置**：`src/features/home/components/HomeLayout.tsx:359`

**触发条件**：
```ts
const handleHeroSubmit = async () => {
  if (!hasHeroQuery || isSubmitting) return;
  trackLpHeroInputSubmit();  // ← 这一行
  const description = heroQuery.trim() || currentPlaceholderText;
  await submitDescription(description);
};
```
也就是说：**输入框必须有内容 + 不在提交中** → 点击按钮 → 触发。空点击不发。

**参数**：无。

**GA4 里会看到**：
```json
{
  "event": "lp_hero_input_submit",
  "app_version": "0.4.0",
  "env": "production",
  "page_location": "https://yolox.ai/",
  "client_id": "GA1.1.xxxxxx"
}
```

**本地验证**：✅ 已在 DevTools Console 确认（你之前截图看到的那条 cta_click 就是现在改名的这个）。

---

### 3.2 `lp_auth_btn_click`

**业务意图**：导航栏引流到注册/登录流。

**用户场景**：
> 用户**未登录**状态下，任意页面（首页、agents-store、skills-store 等）右上角有个"开始使用 / Get Start"按钮，用户点它 → 触发。
> 
> ⚠️ **边界**：如果用户**已登录**且在 store 页，这个按钮会变成"进入工作台 / Enter Workspace"，此时点击**不**触发（因为不是去登录流）。

**代码位置**：`src/components/layout/Header.tsx:40`

**触发条件**：
```ts
const handleActionClick = () => {
  if (actionHref !== "/login") return;  // ← 只在去 /login 时触发
  trackLpAuthBtnClick();
  ...
};
```

**参数**：无。

**本地验证**：未单独验证，但代码简单 + lint 通过，低风险。

---

### 3.3 `auth_register_complete` 🔴 Conversion

**业务意图**：核心业务转化 —— **新用户注册成功**。

**用户场景**：两条路径
1. **邮箱注册**：用户在 `/register` 页输邮箱 → 验证码 → 密码 → 点提交 → 注册 API 成功 → **触发**（自动登录之前）
2. **Google 注册**：用户在 `/register` 页点 "Continue with Google" → Google OAuth → 回跳 `/auth/google/callback` → 后端确认 → **触发**（只在 `state.source === "register"` 时）

**代码位置**：
- 邮箱流：`src/features/auth/components/RegisterLayout.tsx`
- Google 流：`src/app/(pages)/auth/google/callback/page.tsx:51`

**触发条件（邮箱流）**：
```ts
if (response.ok) {
  trackAuthRegisterComplete();
}
```
也就是：注册 API 成功后立即触发，避免自动登录失败导致漏记注册完成。

**参数**：无。

> **v1.1 砍的参数**：`method`（邮箱 vs Google 用 `page_location` 分析 —— `/register` 提交 vs `/auth/google/callback` 落点）+ `invite_code_used`（代码里本就没传，纯预留）

**⚠️ 已知限制**：Google 注册的"是否真是新用户"判断不精准 —— 用 `state.source === "register"` 作代理。**如果老用户从 /register 页点 Google OAuth**，会被误记为 register。彻底解决要后端返回 `isNewUser` 字段（见 Day 7 handoff）。

**本地验证**：未（需要真注册一个账号）。prod Realtime 验证。

---

### 3.4 `auth_login_complete`

**业务意图**：登录成功（用于 MAU 计算、活跃度分析）。**不是**转化事件。

**用户场景**：
1. **邮箱登录**：`/login` 页输邮箱密码 → 登录成功 → 触发
2. **Google 登录**：`/login` 页点 Continue with Google → OAuth → 回跳 callback → 触发（`state.source !== "register"`）

**代码位置**：
- 邮箱流：`src/features/auth/components/LoginLayout.tsx:37`
- Google 流：`src/app/(pages)/auth/google/callback/page.tsx:53`

**参数**：无。

> **v1.1 砍的参数**：`method`（邮箱 vs Google 用 `page_location` 分析，同 register）

**本地验证**：未。

---

### 3.5 `onboarding_team_generated` ⚠️ 占位

**业务意图**：平台 onboarding 流里"团队成员生成完成"的里程碑。

**用户场景**：（待确认）猜测：
> 新注册用户 → 进 /workspace 引导流 → 描述想做什么 → 后端 AI 生成推荐的 agent 团队 → 列表展示时触发。

**代码位置**：**未埋**（wrapper 已导出为 `trackOnboardingTeamGenerated()`）。

**原因**：我没定位到 onboarding 流的具体组件和"团队生成完成"的回调位置。需要和同事 / 杨林 align：
1. 这个事件应该在哪个 React 组件触发？
2. 触发时机是"后端返回成功数据" 还是"UI 渲染完成"？
3. 要不要带参数（team_size / generation_time 等）？

**需要你做的**：和同事/杨林问清楚上述 3 点，告诉我，我 5 分钟埋完。

---

### 3.6 `store_card_click`

**业务意图**：商店列表页 CTR 分析（哪些卡片最吸引点击）。

**用户场景**：
> 用户在 `/agents-store` / `/skills-store` / `/teams-store` 列表页，点击某张卡片 → 触发（跳 detail 页之前）。

**代码位置**：
- Agents + Teams（共用 Layout）：`src/features/agents-store/components/AgentsStoreLayout.tsx:468`
- Skills：`src/features/skills-store/components/SkillsStoreLayout.tsx:215`

**触发条件**（Agents 分支示例）：
```ts
onClick={() => {
  trackStoreCardClick({
    storeType: isAgentsCard ? "agent" : "team",
    cardName: (card as AgentCardItem).name ?? (card as TeamsCardItem).name ?? card.id,
  });
  if (isAgentsCard) {
    router.push(`/agents-store/${card.id}`);
  } else {
    router.push(`/teams-store/${card.id}`);
  }
}}
```

**参数**：

| 参数名 | 类型 | 示例值 |
|---|---|---|
| `store_type` | string | `"skill"` / `"agent"` / `"team"` |
| `card_name` | string | `"Email Triage"` |

> **v1.1 砍的参数**：`card_id`（按同事 spec，用 card_name 已够用于列表 CTR 分析）

**和 agent_view 的关系**：
- `store_card_click`：**列表侧**点击（用户意图，可能点完没进详情页就关了 tab）
- `agent_view`：**详情页**mount（可能从列表来，也可能从外链直接来）

两者互补：前者看列表 CTR，后者看详情覆盖度。

**本地验证**：未（你本地 agents 列表空，验证跳过。prod 上有数据后可验）。

---

### 3.7 `agent_view`

**业务意图**：Agent 详情页被浏览（了解哪个 agent 被关注）。

**用户场景**：
> 用户打开 `/agents-store/<agentId>` 页面 → 页面 mount → **触发**（每次打开一次）。

**代码位置**：`src/features/agents-store/components/AgentDetailLayout.tsx:59`

**触发条件**：useEffect 挂 `agent.templateName` 依赖，首次渲染 + templateName 变化时触发。

**参数**：

| 参数名 | 类型 | 示例值 | 说明 |
|---|---|---|---|
| `agent_id` | string | `"email-triage-v2"` | agent 的 templateName |

> **v1.1 砍的参数**：`source`（"从哪进来"用 GA4 built-in `page_referrer` 替代，GA4 Exploration 报表可按 referrer 分组）

**本地验证**：未（agents 列表空，进不到 detail 页）。

---

### 3.8 `message_sent`

**业务意图**：产品**真实活跃度**核心指标。注册用户是否真的用产品说话？

**用户场景**：
> 用户登录 `/client-home` → 在 channel（频道）或某个 agent 的对话框里 → 输入消息 → 点 Send → **触发**（先于实际 WebSocket 发送）。

**代码位置**：
- channel：`src/features/client-home/hooks/useChannelConversationSession.ts:804`
- agent：`src/features/client-home/hooks/useAgentConversationSession.ts:1039`

**触发条件**：
```ts
if (!content.trim() && !attachments?.length) return "skip" as const;
trackMessageSent();
```
**必须过内容非空校验**（空消息不发埋点，防止 noise）。

**参数**：无（按同事 spec）。

> **v1.1 砍的参数**：`surface` / `target_id`（target_id 是高基数参数，Custom Dimension 不适合；surface "频道 vs agent" 用对应页面 `page_location` URL 模式侧面分析）

**本地验证**：未（需要登录后在 /client-home 发消息）。

---

### 3.9 `agent_instantiated` 🔴 Conversion · **语义待 align**

**业务意图**：业务核心转化 —— 用户把 agent 加入自己工作台。

**用户场景**（前端视角）：
> 用户在 agent detail 页点 "Install / Hire / 雇佣" 按钮 → 前端 POST `/v1/agents/install` → 后端返回 200 → **触发**。

**代码位置**：`src/features/agents-store/components/AgentDetailLayout.tsx:117`

**触发条件**：
```ts
const response = await fetchWithAuth(`${apiBaseUrl}/v1/agents/install`, {...});
if (response.ok) {
  trackAgentInstantiated({ agentId: agent.templateName?.trim() ?? "" });
  ...
}
```

**参数**：

| 参数名 | 类型 | 示例值 |
|---|---|---|
| `agent_id` | string | agent templateName |

> **v1.1 砍的参数**：`agent_name`（和 agent_id 语义重复）+ `source`（固定值 `"agents_store_detail"` 无分析价值，且用 `page_referrer` 可补充）

**🔑 语义待 align**（和同事对话里他的核心质疑）：
- **我的实现**：用户看到 Install API 成功返回的那一刻触发（user-visible "成功"）
- **同事的期望可能是**：后端 agent tool 真实完成初始化 / 写库 / 可用的那一刻触发
- **区别**：前者是"意图"，后者是"结果"。某些后端流程可能 API 200 但实际异步 tool 调用还没完成。

**需要决定**：
1. **保持前端现状**（user-visible 语义）→ 前端 ship
2. **改为后端埋点**（等杨林在后端 tool 成功处用 GA4 Measurement Protocol 发）→ 前端移除这条
3. **双埋**（前端+后端，两个事件名区分）→ 最准确但复杂

**本地验证**：未（agents 列表空）。

---

### 3.10 `agent_deleted`

**业务意图**：agent 留存率计算用 —— 安装后多少被删。

**用户场景**：
> 用户在 /client-home 里右键某个 agent（或点菜单）→ 删除 → 确认 → 后端删除成功 → **触发**。

**代码位置**：`src/features/client-home/components/ClientHomeLayout.tsx:757`

**触发条件**：
```ts
const result = await clientHomeApi.deleteAgent(apiBaseUrl ?? "", confirmAgent.id);
if (!result.ok) {
  setDeleteError(result.message ?? t("deleteFailed"));
  return;
}
trackAgentDeleted({ agentId: confirmAgent.id });  // ← 只在成功后
```

**参数**：

| 参数名 | 类型 | 示例值 |
|---|---|---|
| `agent_id` | string | agent.id |

**本地验证**：未（需要先安装再删，本地 agents 列表空）。

---

### 3.11 `credits_low_modal_view`

**业务意图**：**付费漏斗第一步** —— 用户因余额不足被弹窗提示。

**用户场景**：
> 用户在 client-home 想发消息 / 做操作 → 余额检测 ≤ 0 → 弹出"余额不足"模态框 → **触发**（模态框显示的那一刻）。

**代码位置**：`src/features/client-home/hooks/useBillingController.ts:160`

**触发条件**：
```ts
useEffect(() => {
  if (showInsufficientCredits) {
    trackCreditsLowModalView();
  }
}, [showInsufficientCredits]);
```
这个 useEffect 监听 `showInsufficientCredits` state，变 true 就触发。

**参数**：无。

**本地验证**：未（需要账号余额 = 0 才能触发弹窗）。

---

### 3.12 `credits_modal_open`

**业务意图**：**付费漏斗第二步** —— 用户主动打开充值弹窗。

**用户场景**：
> 用户在 client-home 任意位置点"充值 / Top Up / Add Credits"按钮 → 充值包列表弹窗打开 → **触发**。
> 
> 也可能是 `credits_low_modal_view` 之后用户点"去充值"跳转过来（两个漏斗阶段连续）。

**代码位置**：`src/features/client-home/hooks/useBillingController.ts:96`

**触发条件**：
```ts
const openQuotaModal = useCallback(() => {
  setPurchaseError("");
  setIsQuotaModalOpen(true);
  trackCreditsModalOpen();  // ← 弹窗打开时触发
  ...
}, [...]);
```

**参数**：无。

**本地验证**：未（需要登录 + 触发充值流）。

---

### 3.13 `credits_package_select`

**业务意图**：**付费漏斗第三步** —— 用户选了某档（Stripe 跳转前的最后一步，**诊断弃单**的关键）。

**用户场景**：
> 用户在充值弹窗里看到多档（如 "Starter $10" / "Standard $30" / "Expansion $100"）→ 点某档 → 前端调 `/v1/billing/purchase` → 得到 Stripe checkout URL → 浏览器即将跳转 Stripe → **触发**。

**代码位置**：`src/features/client-home/hooks/useBillingController.ts:126`

**触发条件**：
```ts
setPurchaseSubmittingPackKey(pack.key);
setPurchaseError("");
trackCreditsPackageSelect({ packageName: pack.key });  // ← 触发在 API 调用前
const result = await clientHomeApi.purchaseBillingPack(apiBaseUrl ?? "", pack.key);
```

**参数**：

| 参数名 | 类型 | 示例值 |
|---|---|---|
| `package_name` | string | `"starter_10"` / `"standard_30"` / `"expansion_100"` **⚠️ 实际 pack.key 命名待后端确认**，同事 spec 写的是 `"beginner" / "standard" / "expansion"` 可能和实际 pack.key 不一致 |

**🔑 待确认**：pack.key 的实际命名约定是什么？同事 spec 和代码传的值可能不一致，需要和杨林对一下。

**本地验证**：未。

---

### 3.14 `purchase` 🔴 Conversion / Monetization · **建议双埋**

**业务意图**：**付费漏斗终点** —— 用户付款成功。

**用户场景**：
> 用户 Stripe 付完款 → 回跳 `/billing/success?session_id=xxx` → 再 redirect 到 `/client-home` → `useBillingController` 从 sessionStorage 读 `pendingPayment` → 确认 `result === "success"` → **触发**。

**代码位置**：`src/features/client-home/hooks/useBillingController.ts:205`

**参数**：

| 参数名 | 类型 | 示例值 | 说明 |
|---|---|---|---|
| `transaction_id` | string | `"order_abc123"` | 后端返回的 orderId，用于 GA4 purchase 去重 |
| `value` | number | `10` | **美元数值**（amountCents / 100）|
| `currency` | string | `"USD"` | ISO 4217 三字母代码 |
| `items` | array | `[{ item_id: "starter_10", ... }]` | GA4 ecommerce item 明细 |

**幂等保护**：成功 session 被消费后立即清理 sessionStorage，`paymentSessionHandledRef.current` 防当前实例重复处理。

**⚠️ 建议后端补双埋**（和杨林 align）：
- **原因**：用户付完 Stripe 直接关了浏览器、adblock 拦截等情况会让前端事件丢失 → GA4 里少一笔付费数据
- **业界最佳实践**：Stripe webhook 在服务端 call GA4 Measurement Protocol，100% 可靠 source of truth
- **如何去重**：用 `transaction_id` 作为 GA4 event 的唯一标识，前后端同时发也只算一笔

**本地验证**：未（需要真付 Stripe test checkout，本地配置复杂）。prod 上首笔付费时 Realtime 看。

---

### 3.15 `scroll_depth`

**业务意图**：内容页 engagement 深度测量。

**用户场景**：
> 用户在首页滚动 → 依次经过 25% / 50% / 75% / 100% 四个阈值 → 每个阈值**首次到达时触发一次**（本 mount 周期内不重复）。

**代码位置**：`src/lib/useScrollDepth.ts:43`（挂在 `HomeLayout.tsx` 组件开头 `useScrollDepth()`）

**触发条件**：
- 每次 scroll 或 resize 事件时计算：`(scrollTop + viewport) / documentHeight * 100`
- 过 25 发 25、过 50 发 50、以此类推
- 用 `useRef<Set<Threshold>>` 去重，每个阈值每 mount 只发一次
- 页面短到不能滚动（`total <= viewport`）→ 立即发 100%

**参数**：

| 参数名 | 类型 | 示例值 |
|---|---|---|
| `percent` | number | `25` / `50` / `75` / `100` |

> **v1.1 砍的参数**：`page_path`（GA4 built-in `page_location` 已覆盖）

**仅挂在首页**，其他页（detail、client-home 等）暂不挂。

**本地验证**：✅ 已验证（你之前截图看到 25/50/75 三条）。

---

## 4. 占位事件（本周未实装）

### `onboarding_team_generated`

- wrapper 函数已存在：`trackOnboardingTeamGenerated()`
- 未找到触发点
- 需要和同事/杨林 align 触发位置和时机

**本周就这一个占位**。其他事件要扩展（如 `copy_code_snippet` 博客代码块复制）等对应功能上线再补。

---

## 5. 和同事 v1 spec 的对照

按小刀老师要求"和他不一样的就按他的来（不要有别名）"，我的实现和他的 spec 对齐情况：

| 同事 v1 | 我的实现 | 是否一致 | 备注 |
|---|---|:---:|---|
| `lp_page_view` | 未埋 | ❌ | GA4 自动 page_view 已覆盖，无需额外埋（见 §2 解释）|
| `lp_hero_input_submit` | 已埋 | ✅ | 命名 + 无参数 |
| `lp_auth_btn_click` | 已埋 | ✅ | 命名 + 无参数 |
| `auth_page_view` | 未埋 | ❌ | 同上 GA4 自动 |
| `auth_register_complete` | 已埋 | ✅ | 命名 + 无参数 |
| `auth_login_complete` | 已埋 | ✅ | 命名 + 无参数（v1.1 砍了 method）|
| `onboarding_page_view` | 未埋 | ❌ | 同上 GA4 自动 |
| `onboarding_team_generated` | **占位** | ⚠️ | 触发点未定位 |
| `store_page_view` | 未埋 | ❌ | 同上 GA4 自动 |
| `store_card_click` | 已埋 | ✅ | 和同事 spec 完全一致：`store_type` + `card_name` |
| `workspace_page_view` | 未埋 | ❌ | 同上 GA4 自动 |
| `message_sent` | 已埋 | ✅ | 命名 + 无参数（v1.1 砍了 surface / target_id，完全对齐同事 spec）|
| `agent_instantiated` | 已埋（前端视角）| ⚠️ | **语义待和杨林 align**（见 §3.9）|
| `agent_deleted` | 已埋 | ✅ | 命名 + agent_id 参数 |
| `credits_low_modal_view` | 已埋 | ✅ | 命名 + 无参数 |
| `credits_modal_open` | 已埋 | ✅ | 命名 + 无参数 |
| `credits_package_select` | 已埋 | ✅ | **package_name 的取值需对齐**（pack.key vs beginner/standard/expansion）|
| `purchase` | 已埋 | ✅ | GA4 ecommerce 标准字段：transaction_id / value / currency / items |

**未按同事 spec**（我主动不做）：
- ❌ 5 个 `*_page_view` 变体（GA4 自动 page_view 已覆盖）
- ❌ 公共参数（app_version / env / timestamp / user_id）"每事件手加"（我走 gtag config 一次性设置更优）

**v1.0 → v1.1 参数砍除记录**（7 个事件砍 10 个参数）：

| 事件 | 砍掉的参数 | 替代方案 |
|---|---|---|
| `auth_register_complete` | method, referral_source, invite_code_used | method 用 page_location；referralSource 已移除 |
| `auth_login_complete` | method | 同上 |
| `store_card_click` | card_id | 按同事 spec，card_name 够用 |
| `agent_view` | source | GA4 built-in `page_referrer` |
| `message_sent` | surface, target_id | surface 用 page_location；target_id 高基数不适合 dimension |
| `agent_instantiated` | agent_name, source | agent_name 和 id 重复；source 固定值无价值 |
| `scroll_depth` | page_path | GA4 built-in `page_location` |

---

## 6. GA4 侧配置 checklist（小刀老师代操作）

这些要在 analytics.google.com Admin 里建，**代码没法替你做**。

### 6.1 Custom dimensions（可选，2 个）

| Dimension name | User property | 用途 |
|---|---|---|
| `app_version` | `app_version` | 看哪个版本号在跑 / 分版本漏斗 |
| `env` | `env` | 过滤 production 数据 |

**建法**：Admin → Property → Custom definitions → Create custom dimension → 填上表。

### 6.2 Conversions 标记（3 个一级事件）

Admin → Events → 找到以下事件 → toggle **Mark as conversion**：

- `auth_register_complete`
- `agent_instantiated`
- `purchase`

⚠️ 要**事件真实触发过一次之后**，才会在 Events 列表里出现。所以：
- 等第一个真实注册 / 安装 / 付费发生后，再去标 Conversion
- 或者在本地 dev 发几条测试事件，24h 后在 non-production property 里标

---

## 7. 审核 Checklist · 你要确认的事

逐条打勾：

### 事件名 + 参数
- [ ] 14 个已实装事件名和同事 v1 spec 一致（见 §5 对照表）
- [ ] 1 个占位（`onboarding_team_generated`）触发点已和同事/杨林确认
- [ ] 付费完成使用 GA4 `purchase`，并携带 transaction_id / value / currency / items
- [ ] `credits_package_select.package_name` 的实际取值（pack.key）和同事期望的 `beginner/standard/expansion` 对齐过

### 语义
- [ ] `agent_instantiated` 语义决定：**前端 API 200 视角** vs **后端 tool 真实完成**（见 §3.9）
- [ ] `purchase` 是否要后端 Stripe webhook 双埋（见 §3.14）
- [ ] `auth_register_complete` 的 Google 注册是否要后端加 `isNewUser` 字段精准判断（见 §3.3 Known Limitation）

### 数据配置
- [ ] GA4 3 个 Custom dimension 已建（§6.1）
- [ ] GA4 3 个 Conversion 标记已打开（§6.2，等事件真触发后做）
- [ ] user_id 的后端字段名 + 是否要前端在登录时 set（§2 表格）

### 代码
- [ ] 所有埋点通过 `src/lib/analytics.ts`，无组件直写 gtag 的（我已 grep 过无异常）
- [ ] 无 PII 参数泄漏（运行时检测已做，dev 模式 warn）

---

## 8. 附录

### 8.1 完整涉及文件清单

**统一封装层**：
- `src/lib/analytics.ts`（199 行）
- `src/lib/useScrollDepth.ts`（63 行）
- `src/components/analytics/GoogleAnalytics.tsx`（公共参数注入）

**业务埋点组件**：
- `src/components/layout/Header.tsx`
- `src/features/home/components/HomeLayout.tsx`
- `src/features/auth/components/RegisterLayout.tsx`
- `src/features/auth/components/LoginLayout.tsx`
- `src/app/(pages)/auth/google/callback/page.tsx`
- `src/features/agents-store/components/AgentsStoreLayout.tsx`
- `src/features/agents-store/components/AgentDetailLayout.tsx`
- `src/features/skills-store/components/SkillsStoreLayout.tsx`
- `src/features/client-home/components/ClientHomeLayout.tsx`
- `src/features/client-home/hooks/useBillingController.ts`
- `src/features/client-home/hooks/useAgentConversationSession.ts`
- `src/features/client-home/hooks/useChannelConversationSession.ts`

**文档**：
- `docs/seo/analytics-events.md`（开发 spec，v2.0）
- `docs/seo/analytics-audit.md`（**本文件**，审核向）
- `docs/seo/analytics-dashboard.md`（Looker Studio 搭建清单）
- `docs/seo/analytics-alerts.md`（里程碑告警清单）
- `docs/seo/utm-guidelines.md`（UTM 规范）

### 8.2 数据流全链

```
组件 trackXxx()
    ↓
src/lib/analytics.ts (统一封装)
    ↓
window.gtag('event', name, params)
    ↓
gtag.js script (GoogleAnalytics.tsx 注入)
    ↓
HTTPS POST https://www.google-analytics.com/g/collect
    ↓
Google 服务器
    ↓
GA4 property (G-JP6DSCZRJT 或 G-4SMM87VGMB)
    ↓
analytics.google.com (你登录查看)
```

### 8.3 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | v1.0 | 初版审核文档，覆盖 14 实装 + 1 占位 |
| 2026-04-23 | v1.1 | 按同事反馈"非必要不加参数"砍 10 个扩展参数（7 个事件），保留 `referral_source` 和 ecommerce 三字段 |
| 2026-04-29 | v1.2 | 付费完成改发 GA4 `purchase`，移除 referralSource UI 和参数 |

---

## 审核完后告诉我

- ✅ **全通过** → 可以发同事，可以 ship prod
- ⚠️ **某某事件定义要改** → 告诉我哪个 / 改什么 → 我调代码
- ⚠️ **某某参数要加 / 删** → 同上
- ⚠️ **和同事 / 杨林对齐后有反馈** → 告诉我 → 我按反馈改
