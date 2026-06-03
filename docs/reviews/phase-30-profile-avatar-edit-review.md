# Phase 30 Review - 个人资料卡编辑入口与头像编辑

## Scope

本阶段修正“我的”页个人信息卡编辑按钮样式，并把头像图片纳入会员资料编辑能力。

## Findings

- P1：编辑按钮不能继续使用大号 `yh-button` 材质，否则会在个人信息卡上方形成过宽横条。已改为资料卡右侧小切角按钮。
- P1：头像图片属于用户资料字段，但不能和段位、积分放在同一类可编辑资产里。已把 `avatarUrl` 加入资料白名单，同时继续剔除 `points / rankTitle`。
- P2：当前头像来源是微信临时路径或后续云文件地址。云环境启用后，正式流程必须先上传云存储，再保存 `avatarUrl`。

## Verification

- TDD red step: `node scripts\test-member-profile.js` failed first because `avatarUrl` was not included in the profile draft.
- TDD green step: `node scripts\test-member-profile.js` passed after adding `avatarUrl` to profile draft, normalization, validation, and service storage.
- Full miniprogram JS syntax check passed: 45 files checked.
- JSON check passed: 35 files checked.
- Production copy check passed: 21 files checked.
- UI asset edge check passed: 32 PNG assets checked.
- `git diff --check` passed with CRLF warnings only.
- WeChat DevTools CLI preview passed on port `30812`, AppID `wxe30b469d64636a2b`, package `734.0 KB` / `751623` bytes.

## Residual Risk

- `chooseAvatar` 在真机上需要用户主动选择头像；后续真机预览时要确认微信授权和头像临时路径表现。
- 云开发接入前，本地缓存不会把头像文件上传到云端，换设备或清缓存后仍会丢失。
