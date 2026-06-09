# Phase 62 店内定位反刷分 Gate 审查

日期：2026-06-09

## 结论

本阶段可归档。挑战首页已经接入定位 gate：小程序端获取用户定位，云函数端读取老板配置的门店经纬度和定位范围，计算距离后决定是否允许发起有效挑战。

## 已处理风险

### P1：挑战首页只校验开台，不校验是否在店内

此前 `player.getChallengeHome` 只返回登录和球桌到点检查。用户如果拿到桌码，有机会在店外尝试发起挑战。

处理：`getChallengeHomeData()` 增加 `location` 检查项；当门店坐标已配置且用户拒绝定位或超出范围时，`canStartChallenge` 会被前端拦截。

### P1：门店坐标没有配置入口

只有 100 米范围值不够，系统还需要知道门店经纬度。

处理：老板端反刷分配置新增 `storeLatitude / storeLongitude`，小程序端和云函数端校验一致。

### P2：定位授权失败不能让页面崩掉

用户可能拒绝定位，或者 DevTools 没有真实定位能力。

处理：挑战首页把定位失败包装成 `locationDenied`，仍请求云函数，由云函数返回正式业务提示。

## 残余风险

### P1：未配置门店坐标时暂不拦截

当前策略：如果老板端没有填写门店经纬度，云函数返回 `location.skipped = true`，不阻止顾客开局。

原因：避免上线前坐标未配置导致所有顾客无法发起挑战。

处理：上线验收必须填写真实门店坐标，并用真机验证 100 米范围。

### P2：定位精度和坐标系需要真机验收

小程序使用 `gcj02` 坐标，门店经纬度也应使用同一坐标系。若从地图平台复制坐标，需要确认坐标系一致。

处理：真机在店内测试一次距离，店外 100 米外再测试一次。

## 验证

- `node scripts\test-admin-config-validator.js`
- `node --check miniprogram\pages\challenge-home\challenge-home.js`
- `node --check miniprogram\services\player-service.js`
- `node --check cloudfunctions\yunhanApi\index.js`
- `node --check cloudfunctions\yunhanApi\admin-config-validator.js`
