# Phase 63 Review：上线使用路径与员工授权闭环

## 结论

本阶段可归档。已补齐一份面向真实门店的操作手册，并补上老板端“扫码会员码设置员工 / 大屏 / 普通球友”的最小闭环。

## 处理的问题

### P1：初始化 owner 后仍没有员工授权路径

此前有首个老板初始化，但没有产品化的员工授权入口。真实门店里，前台员工不能靠开发者手工改数据库获得权限。

处理：

- 老板端新增“人员权限”面板。
- 老板扫码员工会员码后，可设置为 `staff` / `screen` / `player`。
- 云函数新增 `admin.getMemberForRole` 和 `admin.setMemberRole`。
- `setMemberRole` 写入 `store_members`，并通过 admin 操作日志留痕。

### P1：不能允许误改老板账号

如果老板端授权功能可以把 owner 改成 player 或 staff，会导致门店失去老板权限。

处理：

- 禁止修改当前老板自己的身份。
- 禁止通过人员权限入口修改已有 owner 账号。

### P2：会员码解析逻辑重复

员工端原本自己维护一份二维码解析逻辑，老板端再复制会增加不一致风险。

处理：

- 新增 `miniprogram/utils/member-code-parser.js`。
- 员工端和老板端共用同一套 `parseMemberOpenid`。

### P1：正式环境云端角色没有写入本地权限缓存

老板端和员工端页面进入时会先看本地角色缓存。如果“我的”页只读取云端角色但不写入缓存，真实老板或员工仍可能被本地默认 `player` 拦截。

处理：

- `access-control` 新增 `setCurrentRole`。
- `my-hub` 读取 `auth.whoami` 后写入当前云端角色。
- `setup-owner` 初始化成功后立即写入 `owner`。

### P2：使用路径只存在聊天里

老板、员工和球友各自怎么用小程序，没有一份单独文档。

处理：

- 新增 `docs/miniapp-operation-runbook.md`。
- 文档按云端准备、初始化老板、老板配置、员工授权、员工开台、球友挑战、大屏榜单、上线验收拆开。

## 验证

待执行：

- `node scripts/test-ops-services.js`
- `powershell -ExecutionPolicy Bypass -File scripts/verify-launch-ready.ps1`

## 残余风险

- 本阶段仍未解决微信开发者工具 `41002 system error` 导致的云函数部署失败。
- 员工授权必须在最新 `yunhanApi` 部署成功后才能真机验证。
- 浏览器大屏的正式部署方式仍未收口。
