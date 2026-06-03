# 云瀚 UI 美术资产映射与抠图流程

状态：v0.1
用途：约束段位、宝箱、星级、榜单装饰等复杂美术资源如何从设计图变成小程序可用资产。
源图：`docs/design/imagegen-references/08-rank-leaderboard-assets-board.png`

## 1. 先定边界

这份文档只管“复杂美术资产”。按钮、玩法卡、面板、选项、比分布局、排行榜行仍然由 WXML/WXSS 实现。

必须走图片资产的内容：

| 类别 | 资产 | 原因 |
| --- | --- | --- |
| 段位 | 青铜、白银、黄金、铂金、钻石、星耀、王者徽章 | 金属层次复杂，代码硬画成本高且不像 |
| 星级 | 暂不接入 PNG，当前使用字符星 `★ / ☆` | 已生成星星 PNG 边缘不够干净；重新验收前不得接入正式页面 |
| 奖励 | 普通奖励宝箱、冲刺奖励宝箱、积分币 | 是情绪价值核心，不应用普通 CSS 方块替代 |
| 结算 | 段位提升、加分、减分、胜利横幅、服了确认章 | 需要仪式感和强反馈 |
| 排行榜 | Top 3 领奖台、大屏榜单标题、赞助位、刷新状态 | 电视大屏需要强视觉识别 |
| 赛季 | 第一赛季徽章、后续赛季徽章 | 后续运营活动扩展 |

## 2. 资产命名约定

正式 PNG 统一放到：

```text
miniprogram/assets/ui-kit/
```

命名用英文小写和短横线：

| 资产 | 文件名示例 |
| --- | --- |
| 黄金段位徽章 | `rank-gold.png` |
| 走位黄金 III 大徽章 | `rank-gold-iii-featured.png` |
| 新获得星 | 暂不使用 PNG，当前由字符星状态渲染 |
| 保护星 | 暂不使用 PNG，当前由字符星状态渲染 |
| 普通奖励宝箱 | `reward-crate-normal.png` |
| 续时冲刺宝箱 | `reward-crate-sprint.png` |
| 胜利横幅 | `settlement-victory-banner.png` |
| 服了确认章 | `settlement-accept-stamp.png` |
| 排行榜标题 | `tv-ranking-title.png` |

小程序引用必须使用根路径：

```xml
<image class="reward-card__asset" src="/assets/ui-kit/reward-crate-sprint.png" mode="aspectFit" />
```

`mode` 默认用 `aspectFit`，避免拉伸变形。

## 3. 抠图工作流

正式抠图不能靠手动截图覆盖文件。后续每一批资产都必须留下可复跑脚本或配置。

标准流程：

1. 在脚本或配置里写清楚每个资产的裁切框、输出文件名、安全边距。
2. 运行脚本生成 PNG。
3. 生成黑底预览图，检查是否接近设计稿质感。
4. 生成棋盘格透明预览图，检查透明边、脏边、缺边。
5. 运行边缘检测脚本。
6. 通过后再接入 WXML/WXSS 组件。
7. 接入后用微信开发者工具预览，确认没有变形、挤压、模糊。

边缘检测命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
```

通过输出：

```text
Edge check OK
```

## 4. 抠图验收标准

一张正式 PNG 同时满足这些条件才算过：

| 检查项 | 通过标准 |
| --- | --- |
| 完整性 | 左、右、上、下都没有截断主体 |
| 透明边 | 四条边没有非透明像素贴边 |
| 安全边距 | 主体周围留出透明缓冲，后续动画不会被裁掉 |
| 干净度 | 没有带入相邻资产、标题、分割线、卡片边框 |
| 可复跑 | 裁切参数在脚本或配置里，不靠口头记忆 |
| 组件适配 | 在小程序 `<image mode="aspectFit">` 下不变形 |
| 双预览 | 黑底预览和棋盘格预览都检查过 |

黑底预览能看质感，但容易隐藏透明边问题。棋盘格预览必须存在。

## 5. 裁切修正规则

如果用户指出“没截完整”，不要直接整体放大裁切框。

正确顺序：

1. 先确认缺的是哪一侧。
2. 只向缺失方向扩展裁切框。
3. 保持已经干净的一侧边界不变。
4. 重新生成 PNG 和两张预览图。
5. 跑边缘检测。

典型例子：

| 问题 | 修正方式 |
| --- | --- |
| 左边徽章缺一块 | `x` 减小，`width` 增加；右边界尽量不动 |
| 右边带入别的图 | `width` 减小或右边界左移 |
| 顶部皇冠被裁 | `y` 减小，`height` 增加 |
| 底部阴影贴边 | 增加透明安全边距，不一定扩大源图裁切 |

## 6. 当前资产状态

当前仓库已保存完整设计源图，并已预留正式资产目录；批量抠图结果还需要在下一轮落地。

已确定的源图：

```text
docs/design/imagegen-references/08-rank-leaderboard-assets-board.png
```

已落地的校验脚本：

```text
scripts/check-ui-kit-asset-edges.ps1
```

已落地的抠图脚本：

```text
scripts/extract-ui-kit-assets.ps1
```

当前已生成第一批 32 个 PNG 资产：

```text
miniprogram/assets/ui-kit/*.png
```

注意：第一批里包含的星星 PNG 资产当前不进入正式 `StarTrack`。原因是用户实际预览后确认边缘不干净、排列观感不稳定。正式页面先使用字符星 `★ / ☆` + 固定五格布局。只有重新生成星星资产，并通过完整性、透明边、脏边、微信端预览验收后，才允许切回 PNG。

当前预览图：

```text
docs/design/extracted-ui-assets-preview.png
docs/design/extracted-ui-assets-checker-preview.png
```

当前验收命令已通过：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
```

## 7. 不接受的做法

- 不接受用 CSS 画宝箱、徽章、胜利横幅。
- 不接受直接把整张设计图切成大图塞进页面。
- 不接受资产贴边后靠 WXML 外层 padding 补救。
- 不接受只看微信开发者工具截图，不看透明预览。
- 不接受每次靠聊天记录找裁切参数。
