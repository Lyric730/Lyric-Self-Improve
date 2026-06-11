# 云瀚台球小程序 Agent 交接文档

状态：v1.0
日期：2026-06-11
适用对象：下一位接手本项目的 Codex / AI agent / 开发者

## 1. 先读结论

当前项目已经从“高保真原型 / UI Kit 还原”推进到“微信小程序上线链路补齐”阶段。页面、服务层、统一云函数入口、云数据库 schema、老板/员工/球友/大屏四类角色的主要路径都已经有代码和文档。

但它还不能直接交给门店营业使用。当前最大阻塞不是 UI，而是云端上线验证：

1. 最新 `cloudfunctions/yunhanApi` 需要重新部署到微信云环境。
2. 首个老板账号必须在真实云环境初始化。
3. 老板配置、员工授权、员工开台、球友挑战、结算、大屏榜单必须跑一遍真实云端闭环。

如果下一个 agent 只做一件事，优先做“云函数部署成功 + 真机跑通首个老板和员工开台链路”，不要继续堆 UI。

## 2. 源头路径和仓库状态

真实项目根目录：

```text
F:\Making money\taiqiuxcx
```

注意：当前 Codex 环境有时会显示另一个路径：

```text
F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx
```

那个路径只剩少量配置和临时目录，不是当前 Git 主项目。下一个 agent 不要在那个目录里改小程序代码。

当前主要分支：

```text
codex/launch-page-polish
```

远端：

```text
https://github.com/Lyric730/Lyric-Self-Improve.git
```

最近功能性提交：

```text
b226515 Add operation runbook and staff role management
```

截至 2026-06-11，工作区可能还存在两个未跟踪截图：

```text
screen/current-devtools.png
screen/wechat-devtools-front.png
```

这两个文件是开发者工具截图，不属于核心交付。不要误提交，除非用户明确要求留存截图。

## 3. 项目是什么

这是“云瀚台球俱乐部”微信小程序，第一阶段目标是复刻/重做台球厅天梯挑战系统。

核心业务：

1. 顾客在店内扫码进入某张球桌的挑战。
2. 两个顾客选择抢 5 / 抢 7 / 抢 10、底分和倍率。
3. 比赛计分。
4. 满最低时间后允许有效结算。
5. 云函数结算积分、随机奖励和段位。
6. 排行榜和电视大屏展示店内氛围。
7. 员工只做简单操作：设置球桌到点时间、扫码绑定开台会员、核销积分、处理异常。
8. 老板配置玩法、积分、防刷分、大屏和人员权限。

最高产品原则：

```text
机制简单，操作简单。
```

## 4. 当前已完成的能力

### 4.1 小程序页面

页面列表在 `miniprogram/app.json`：

- 球友端：挑战首页、等待对手、接受挑战、玩法选择、底分倍率、开局确认、计分、时间不足、结算、不服、结果。
- 会员端：我的数据、排行榜、积分礼遇、会员码、我的。
- 运营端：门店初始化、员工端、老板端、电视大屏。

### 4.2 云函数

统一云函数：

```text
cloudfunctions/yunhanApi
```

已包含模块：

- `auth`：`whoami`、`bootstrapOwner`
- `player`：挑战首页、个人数据、排行榜、积分礼遇
- `member`：会员码、个人资料保存
- `staff`：会员扫码查询、积分核销、球桌到点时间、异常比赛作废
- `admin`：老板配置、人员权限
- `match`：创建房间、加入房间、配置玩法、开赛、计分、预览结算、确认结算、读取结算
- `screen`：大屏榜单

### 4.3 数据库集合设计

核心集合：

- `store_members`
- `operation_logs`
- `matches`
- `match_score_events`
- `settlements`
- `points_ledger`
- `member_points`
- `table_sessions`
- `admin_configs`
- `screen_tokens`

集合和索引说明见：

```text
docs/cloud-database-schema.md
docs/cloud-database-console-checklist.md
```

### 4.4 老板 / 员工权限

已完成：

- 首个老板账号初始化页：`/pages/setup-owner/setup-owner`
- 老板端“人员权限”面板：扫码会员码后可设置 `staff` / `screen` / `player`
- 云函数 `admin.setMemberRole` 禁止修改已有 `owner`
- 云函数 `admin.setMemberRole` 禁止老板把自己降权
- `my-hub` 读取云端角色后会写入本地权限缓存，避免真实老板/员工被本地默认 `player` 拦住

### 4.5 开台逻辑

第一版不接原有开台软件 API。

员工端只做：

1. 选择球桌。
2. 设置到点时间。
3. 可选扫码绑定开台会员。
4. 保存。

云端写：

- `table_sessions`
- 如绑定会员，写 `member_points` 和 `points_ledger(type = table_bonus)`

挑战首页会根据 `table_sessions` 判断球桌是否已开台。

### 4.6 防刷分

已接入店内定位 gate：

- 小程序端请求 `wx.getLocation({ type: "gcj02" })`
- 云函数读取老板端配置的 `storeLatitude / storeLongitude / geoFence`
- 默认范围：100 米
- 如果老板端没有填门店经纬度，云函数不会阻断开局，只返回 `location.skipped = true`

上线前必须填真实门店坐标并真机测试。

### 4.7 段位和积分

已完成：

- 全部游戏模式共用一个段位。
- 结算后 `match.settle` 会写回双方 `store_members.rankState / rankTitle`。
- 胜方积分变化、败方扣分、随机奖励和段位变化由服务端计算。
- 开台赠分会写积分流水。

仍需真实云端验证：

- 重复点击结算不能重复加减积分。
- 比赛中断或云函数中途失败时是否有残留 `settling` 单。
- 双方快速加减盘的并发覆盖风险。

## 5. 关键文档地图

下一个 agent 建议按这个顺序读：

1. `AGENTS.md`：项目约束和协作规则。
2. `docs/agent-handoff.md`：当前交接入口，也就是本文。
3. `docs/miniapp-operation-runbook.md`：门店真实使用路径。
4. `docs/cloud-function-cutover-checklist.md`：云函数上线前必测接口。
5. `docs/cloud-init-runbook.md`：云环境、集合、首个 owner 初始化。
6. `docs/cloud-database-console-checklist.md`：控制台创建集合、索引、环境变量。
7. `docs/cloud-database-schema.md`：数据库字段和索引设计。
8. `docs/api-service-layer-contract.md`：前端服务层和云函数边界。
9. `docs/backend-integration-readiness-plan.md`：后端接入计划和历史阶段。
10. `docs/dev-log.md`：完整阶段记录，文件很长，优先看末尾。

UI 相关再读：

- `docs/ui-design-style-guide-yunhan.md`
- `docs/design/`
- `.impeccable.md`

产品规则再读：

- `docs/prd-taiqiu-ladder-mvp.md`
- `docs/ladder-simple-operation-plan.md`
- `docs/ladder-plan/`

## 6. 验证命令

本地完整验证：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1
```

该脚本会跑：

- 运营服务层兜底测试
- 结算引擎测试
- 老板配置校验
- 会员资料测试
- 云函数契约测试
- 云数据库文档检查
- 服务层边界检查
- JSON 检查
- 正式页面文案检查
- 页面路由检查
- UI 资产边缘检查
- 小程序 JS 语法检查
- 云函数 JS 语法检查

最近一次完整通过记录：

```text
2026-06-10：Launch verification OK
```

部署云函数前检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId 'cloudbase-d9gg155lc1ee1d72e'
```

部署云函数：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId 'cloudbase-d9gg155lc1ee1d72e' -Deploy
```

或使用微信开发者工具 CLI：

```powershell
& 'F:\微信web开发者工具\cli.bat' cloud functions deploy --project 'F:\Making money\taiqiuxcx' --env cloudbase-d9gg155lc1ee1d72e --names yunhanApi
```

如果 CLI 端口变化，先看：

```text
docs/wechat-devtools-cli.md
```

## 7. 当前最大阻塞

### P0：最新云函数尚未重新部署成功

2026-06-09 最近一次部署失败：

```text
getCloudAPISignedHeader failed
ret = 41002
errmsg = system error
```

已确认：

- `cloud env list` 能看到 `cloudbase-d9gg155lc1ee1d72e`
- `cloud functions list` 能看到 `yunhanApi`
- 本地 `verify-launch-ready` 通过

判断：

- 不是本地语法错误。
- 大概率是微信开发者工具云开发登录态、签名、工具状态或微信云接口临时问题。

下一步：

1. 在微信开发者工具中重新打开项目。
2. 确认已登录正确微信开发者账号。
3. 打开云开发面板，确认环境 `cloudbase-d9gg155lc1ee1d72e`。
4. 手动右键 `cloudfunctions/yunhanApi`，选择“上传并部署：云端安装依赖”。
5. 或重新用 CLI 部署。
6. 部署成功后，立刻跑第 8 节的真机验收。

## 8. 接下来要做的任务

### Stage A：云端部署恢复

目标：让真实云环境运行最新 `yunhanApi`。

任务：

1. 修复或绕过 `41002 system error`。
2. 重新部署 `yunhanApi`。
3. 确认云函数版本包含：
   - `admin.getMemberForRole`
   - `admin.setMemberRole`
   - `player.getChallengeHome` 定位 gate
   - `staff.updateTableDueTime` 开台赠分
   - `match.settle` 段位写回
4. 记录部署结果到 `docs/dev-log.md`。

完成标准：

- 云开发控制台显示 `yunhanApi` 部署成功。
- 云函数测试面板能调用 `auth.whoami`。

### Stage B：首个老板账号初始化

目标：真实门店有一个 `owner`。

任务：

1. 在云函数环境变量设置 `BOOTSTRAP_OWNER_SECRET`。
2. 打开 `/pages/setup-owner/setup-owner`。
3. 用老板微信输入密钥。
4. 绑定首个老板。
5. 验证 `store_members.role = owner`。

完成标准：

- 老板在“我的”页能进入老板端和员工端。
- `auth.whoami` 返回 `role = owner`。

### Stage C：老板配置和员工授权

目标：老板能配置门店规则，并把前台微信设成员工。

任务：

1. 老板端保存玩法、积分、防刷分、大屏配置。
2. 填真实门店经纬度。
3. 员工打开会员码。
4. 老板扫码，把员工设为 `staff`。
5. 员工重进“我的”，确认能进入员工端。

完成标准：

- `admin_configs` 有真实配置。
- `store_members` 中测试员工 `role = staff`。
- `operation_logs` 有老板授权记录。

### Stage D：员工开台和开台赠分

目标：员工能完成第一版开台动作。

任务：

1. 员工进入前台工作台。
2. 选择 `T01`。
3. 设置到点时间。
4. 扫开台会员码。
5. 保存。
6. 检查会员积分是否增加开台赠分。
7. 重复保存，确认不会重复赠分。

完成标准：

- `table_sessions` 写入或更新。
- `points_ledger(type = table_bonus)` 写入。
- `member_points.balance` 增加一次，不重复增加。

### Stage E：球友挑战闭环

目标：真实跑通一场抢 5。

任务：

1. 店内真机扫码进入挑战首页。
2. 授权定位。
3. 发起挑战。
4. 第二个微信加入。
5. 选择抢 5。
6. 选择底分和倍率。
7. 双方确认。
8. 进入计分。
9. 满最低时间后结算。
10. 重复点击结算，确认不会重复加减积分。

完成标准：

- `matches` 状态完整流转。
- `match_score_events` 有加减盘记录。
- `settlements` 有结算单。
- `points_ledger` 有双方积分流水。
- `member_points` 余额正确。
- `store_members.rankState / rankTitle` 写回。

### Stage F：排行榜和大屏

目标：确认榜单读取真实数据。

任务：

1. 跑完至少一场有效结算。
2. 打开个人端排行榜。
3. 检查店内总榜、同段位榜、好友榜空态。
4. 打开小程序大屏页。
5. 检查大屏读取 `screen.getBoard`。

完成标准：

- 榜单不再依赖本地样例数据。
- 大屏显示真实店内榜单和老板端配置文案。

### Stage G：球桌二维码和门店落地

目标：让顾客无需开发者工具即可进入对应球桌。

任务：

1. 确定每张球桌的 `tableId`，例如 `T01` 到 `T12`。
2. 生成小程序码或二维码。
3. 二维码必须携带对应 `tableId`。
4. 打印张贴。
5. 员工用每张桌测一次挑战首页能否识别球桌。

完成标准：

- 每张桌扫码进入对应球桌。
- 未开台桌不能发起有效挑战。
- 已开台桌在店内定位通过后可发起挑战。

## 9. 当前不要优先做的事

这些不是下一步最高优先级：

- 继续大规模改 UI 质感。
- 继续生成新的 image-2 风格图。
- 继续扩展新玩法。
- 接萤石云视频系统。
- 做积分商城或抽奖。
- 做复杂赛季运营后台。

原因：真实云端闭环尚未验证，继续做这些会把风险堆厚。

## 10. 容易踩坑

### 10.1 不要相信前端角色

前端本地角色缓存只是为了页面路由体验。正式权限必须以 `yunhanApi` 里 `assertRole` 查询 `store_members` 为准。

### 10.2 不要直接改数据库当作产品路径

手工改 `store_members.role` 只能用于救急。正式流程应通过老板端“人员权限”扫码授权。

### 10.3 不要把开台理解成收银开台

第一版只记录球桌到点时间，不替代现成开台软件收费。

### 10.4 不要让顾客看到内部状态

页面不能出现：

- mock
- 模拟
- 调试
- PM 说明
- 内部校验
- 临时
- 占位

检查命令：

```powershell
node scripts/check-production-copy.js
```

### 10.5 不要把图片资产硬画

复杂资产原则上用 `miniprogram/assets/ui-kit/` 下 PNG。星星当前例外，使用字符星 `★ / ☆`。

### 10.6 不要提交临时截图

`screen/current-devtools.png` 和 `screen/wechat-devtools-front.png` 如仍未跟踪，默认不要提交。

## 11. 下一个 agent 的建议开局

建议下一次打开项目后直接执行：

```powershell
cd "F:\Making money\taiqiuxcx"
git status --short --branch
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1
```

如果验证通过，立刻处理云函数部署：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId 'cloudbase-d9gg155lc1ee1d72e' -Deploy
```

如果仍失败，不要继续改 UI，先把失败日志写进：

```text
docs/dev-log.md
```

然后换手动部署路径：

```text
微信开发者工具 -> cloudfunctions/yunhanApi -> 上传并部署：云端安装依赖
```

部署成功后，从 `docs/miniapp-operation-runbook.md` 的顺序开始真机验收。
