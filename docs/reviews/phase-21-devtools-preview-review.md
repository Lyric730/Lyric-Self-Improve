# Phase 21 审查：开发者工具预览通道

日期：2026-06-01

## 范围

本阶段只解决微信开发者工具里的本地预览问题，不改变正式业务权限。

涉及文件：

- `miniprogram/utils/dev-preview.js`
- `miniprogram/pages/challenge-home/challenge-home.js`
- `miniprogram/pages/challenge-home/challenge-home.wxml`
- `miniprogram/pages/challenge-home/challenge-home.wxss`
- `miniprogram/pages/waiting-room/waiting-room.js`
- `miniprogram/pages/waiting-room/waiting-room.wxml`

## 审查结论

P0 / P1：未发现会影响正式小程序启动的问题。

P1：该入口依赖 `wx.getSystemInfoSync().platform === "devtools"`。如果后续需要在真机预览里走完整流程，不能继续靠这个入口，需要用真实云环境或专门的体验版测试账号。

P2：预览角色写入 `yunhanUserRole` 后，会在开发者工具 storage 内保留。若需要恢复普通球友视角，可以清理 storage，或后续补一个“球友端”预览按钮。

## 已验证

```powershell
node --check miniprogram\utils\dev-preview.js
node --check miniprogram\pages\challenge-home\challenge-home.js
node --check miniprogram\pages\waiting-room\waiting-room.js
node scripts\check-production-copy.js
node scripts\check-json-files.js
```

## 后续要求

- 云环境创建后，球友流程应优先改成真实房间状态推进，而不是依赖开发者工具预览入口。
- 员工端和老板端正式入口应来自真实角色接口，不应对普通球友展示。
