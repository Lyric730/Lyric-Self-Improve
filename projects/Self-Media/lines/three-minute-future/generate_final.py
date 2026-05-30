"""
Step 4: generate concise copy for selected 三分钟未来 items.

Input:
  daily/<date>/three-minute-future/work/selection.json

Output:
  daily/<date>/three-minute-future/work/final.json

Usage:
  python lines/three-minute-future/generate_final.py 2026-05-23 --vol 1
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
ACCOUNT_NAME = "@小刀のAI 实验室"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXED_COVER_IMAGE = (
    PROJECT_ROOT
    / "daily"
    / "2026-05-23"
    / LINE_NAME
    / "work"
    / "cover"
    / "constructivist-cover-bg-v1.png"
)


COPY_RULES = [
    {
        "match": ["微软", "人工工资"],
        "title": "AI 比人工更贵？",
        "fact": "微软称，某些 AI 使用成本已经高过直接支付人工工资。",
        "thought": "自动化先算账。省不省人，最后还得看账单。",
    },
    {
        "match": ["Meta", "裁员"],
        "title": "Meta 裁员还在继续",
        "fact": "报道称，Meta 五月裁掉约 8000 名员工，后续压力还在继续。",
        "thought": "AI 提效一旦落到人头，听起来就没那么轻松了。",
    },
    {
        "match": ["星巴克"],
        "title": "星巴克 AI 库存翻车",
        "fact": "北美门店试了 9 个月的 AI 库存系统，最后还是回到人工盘点。",
        "thought": "门店不是实验室。燕麦奶和牛奶分不清，效率就只是报表里的效率。",
    },
    {
        "match": ["高尔夫球包", "机器人"],
        "title": "机器人开始送球包",
        "fact": "釜山西部公寓试用配送机器人，住户把球包放到停车场，机器人送回家。",
        "thought": "机器人进入生活，往往不是先接管世界，而是先跑这些零碎活。",
    },
    {
        "match": ["机器人", "身份证"],
        "title": "人形机器人有了身份证",
        "fact": "全国首个人形机器人管理平台在北京发布，给设备建立身份和追溯信息。",
        "thought": "机器进入公共空间后，先被管理的不是能力，是责任。",
    },
    {
        "match": ["OpenAI", "绿卡"],
        "title": "OpenAI 研究员忙办绿卡",
        "fact": "一则 X 消息称，OpenAI 部分研究员可能因签证问题申请美国绿卡。",
        "thought": "AI 竞争拼模型，也拼人能不能留下来。",
    },
    {
        "match": ["远程办公", "初级招聘"],
        "title": "初级岗位减少，锅不全在 AI",
        "fact": "研究称，初级岗位招聘走弱，远程办公的影响可能比 AI 更大。",
        "thought": "把锅全甩给 AI 很方便，但劳动力市场通常没这么单线条。",
    },
    {
        "match": ["硬件"],
        "title": "AI 价值转向硬件",
        "fact": "Andreessen 认为，AI 的长期价值可能更多流向硬件和基础设施。",
        "thought": "模型越来越像水电，真正稀缺的可能是承载它的机器。",
    },
    {
        "match": ["加州", "AI", "工人"],
        "title": "加州提前应对 AI 冲击",
        "fact": "加州州长签署行政令，要求州政府评估 AI 对工人、企业和公共服务的影响。",
        "thought": "AI 进入劳动力市场后，真正要提前设计的是再培训、补偿和责任分配。",
    },
    {
        "match": ["WorkOS", "auth.md"],
        "title": "智能体也要有身份协议",
        "fact": "WorkOS 发布 auth.md，希望用开放协议解决智能体注册、授权和身份识别问题。",
        "thought": "当 AI 不再只是聊天窗口，身份和权限会变成新的基础设施。",
    },
    {
        "match": ["教皇", "人性"],
        "title": "教皇警告 AI 别夺走人性",
        "fact": "教皇里奥呼吁在 AI 时代保持深刻的人性，提醒技术不能只服务少数机构。",
        "thought": "AI 伦理最怕变成口号。真正的问题是，谁能约束那些掌握模型的人。",
    },
    {
        "match": ["Starbucks", "库存AI"],
        "title": "星巴克 AI 库存翻车",
        "fact": "星巴克停用计算机视觉库存系统，报道称它没有解决缺货问题，反而增加门店负担。",
        "thought": "门店不是实验室。识别更快不等于补货更准，最后还得看运营链条。",
    },
    {
        "match": ["日本航空", "机器人"],
        "title": "日本机场试用搬运机器人",
        "fact": "日本航空启动人形机器人试验，希望缓解机场高龄化和劳动力不足带来的压力。",
        "thought": "机器人最先落地的地方，往往不是科幻场景，而是没人愿意一直做的体力活。",
    },
    {
        "match": ["激光除草机器人"],
        "title": "AI 开始下地除草",
        "fact": "AI 视觉激光除草机器人可以识别杂草并精准清除，农业自动化继续向细分场景渗透。",
        "thought": "农业里的 AI 不一定显眼，但一旦稳定，就会直接改变人力和成本结构。",
    },
    {
        "match": ["LimX Luna"],
        "title": "人形机器人卖到 29.8 万",
        "fact": "逐际动力发布 LimX Luna 人形机器人，售价 29.8 万元，继续把机器人从实验室推向市场。",
        "thought": "价格开始被摆到台面上，说明行业正在从演示走向算账。",
    },
    {
        "match": ["Figure 03"],
        "title": "Figure 机器人连续分拣包裹",
        "fact": "Figure 03 完成 200 小时全自动作业直播，分拣近 25 万包裹并宣称零故障。",
        "thought": "机器人真正有说服力的不是摆拍，而是长时间、重复性、低错误率的工作记录。",
    },
    {
        "match": ["现代集团", "人形机器人"],
        "title": "现代加速人形机器人落地",
        "fact": "消息称现代集团组建专项团队，推进人形机器人在制造、物流等场景里的落地。",
        "thought": "车企做机器人并不奇怪，它们本来就懂工厂、供应链和复杂机器。",
    },
    {
        "match": ["美世报告", "裁员"],
        "title": "高管预计 AI 将带来裁员",
        "fact": "美世报告称，99% 高管预计 AI 两年内将引发裁员，企业组织调整仍在继续。",
        "thought": "AI 提效一旦进入财务表，员工最先感受到的往往不是工具，而是岗位变化。",
    },
    {
        "match": ["微短剧", "算力"],
        "title": "AI 微短剧被写进政策",
        "fact": "上海出台 AI 微短剧新政，支持企业租用智能算力，并对优秀剧本给予奖励。",
        "thought": "内容行业的 AI 化不只靠工具，还会被政策、算力和平台一起推动。",
    },
    {
        "match": ["中学生", "机器人足球"],
        "title": "中学生机器人足球赛开踢",
        "fact": "首届中学生人形机器人足球赛决出首站冠军，AI 自主决策成为比赛看点。",
        "thought": "教育里的机器人竞赛，表面是比赛，背后是在训练下一代的工程直觉。",
    },
    {
        "match": ["医疗", "大脑", "双手"],
        "title": "AI 医疗开始长出手脚",
        "fact": "医疗 AI 正从辅助诊断扩展到数据、机器人和流程协同，应用边界继续外扩。",
        "thought": "医疗最需要 AI，也最不能只靠 AI。效率之外，安全和责任链必须先讲清楚。",
    },
    {
        "match": ["日本", "人工智能机器人"],
        "title": "日本想普及 AI 机器人",
        "fact": "日本持续推动人工智能机器人普及，但高龄化、成本和落地场景仍是现实阻力。",
        "thought": "机器人不是买回来就能替人，真正难的是维护、调度和融入旧流程。",
    },
]


def load_selection(date: str) -> dict[str, Any]:
    path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "selection.json"
    if not path.exists():
        raise SystemExit(f"missing: {path} (run select_items.py first)")
    return json.loads(path.read_text(encoding="utf-8"))


def short_source(source: str) -> str:
    source = re.sub(r"^X：", "X / ", source)
    source = source.replace("（RSS）", "")
    source = source.replace("Hacker News 热门（buzzing.cc 中文翻译）", "Hacker News / Fortune")
    return source


def clean_title(title: str) -> str:
    title = re.sub(r"\s*-\s*[^-｜|]+$", "", title).strip()
    title = title.replace("。", "")
    return title[:24]


def copy_for_item(item: dict[str, Any]) -> dict[str, str]:
    raw_title = item.get("title", "")
    for rule in COPY_RULES:
        if all(term in raw_title for term in rule["match"]):
            return {
                "title": rule["title"],
                "fact": rule["fact"],
                "thought": rule["thought"],
            }

    tags = item.get("tags", [])
    title = clean_title(raw_title)
    fact = clean_title(raw_title)
    if "labor" in tags:
        thought = "AI 开始碰到招聘和工资，故事就不只是工具更新了。"
    elif "robotics" in tags:
        thought = "机器人真正进入生活，通常先从具体杂活开始。"
    elif "hardware" in tags:
        thought = "软件跑得再快，最后还是要落到机器和电力上。"
    else:
        thought = "这类消息值得看，是因为它已经离屏幕外的世界很近。"
    return {"title": title, "fact": fact, "thought": thought}


def image_path(item: dict[str, Any], used_images: set[str]) -> str:
    image = item.get("enrichment", {}).get("image", {})
    if image.get("status") == "downloaded" and image.get("path"):
        path = image["path"]
        if path in used_images:
            return ""
        used_images.add(path)
        return path
    return ""


def write_final(date: str, vol: int, selection: dict[str, Any]) -> Path:
    work_dir = PROJECT_ROOT / "daily" / date / LINE_NAME / "work"
    out_path = work_dir / "final.json"
    items = []
    used_images: set[str] = set()
    for index, item in enumerate(selection.get("items", []), 1):
        copy = copy_for_item(item)
        items.append(
            {
                "id": f"item-{index:02d}",
                "role": item.get("role", "inside"),
                "index": index,
                "title": copy["title"],
                "fact": copy["fact"],
                "thought": copy["thought"],
                "source": short_source(item.get("source", "")),
                "url": item.get("enrichment", {}).get("finalUrl") or item.get("url", ""),
                "tags": item.get("tags", []),
                "sourceRegion": item.get("sourceRegion"),
                "selectionScore": item.get("selectionScore"),
                "imagePath": image_path(item, used_images),
                "sourceScreenshotPath": "",
                "keywordImagePath": "",
                "keywordImageMeta": {},
                "rawTitle": item.get("title", ""),
            }
        )

    cover = {
        "title": "三分钟未来",
        "tagline": "AI 资讯 × 实时热点",
        "subtitle": "AI 不一定比人便宜",
        "topic": items[0]["title"] if items else "",
        "fact": items[0]["fact"] if items else "",
        "imageMode": "fixed-reuse-background",
        "imagePath": str(FIXED_COVER_IMAGE) if FIXED_COVER_IMAGE.exists() else "",
        "promptBrief": "生成 1080x1080 方形封面背景：固定使用新构成主义工业新闻海报语言，但具体视觉主体必须由当期 selection 决定。先提炼 1 个本期主视觉锚点，再补 2-3 个辅助锚点；辅助锚点只作为 fragments / shadows / cut panels / background evidence 出现。不能把上一期的成本单、政策文件、机器人、机场、门店等元素自动沿用为永久模板。实际送去生图模型的 prompt 必须压缩，禁止使用 infographic、diagram、table、chart、comparison、list、labels、UI、protocol、assessment、forms、channel、educational、presentation 等信息图触发词。不直接使用内页新闻图；不生成可读标题、栏目名、账号名或 logo 文案；画面需要暗色背景、强纵深、统一颗粒质感，并留出标题安全区。",
    }

    data = {
        "line": LINE_NAME,
        "name": "三分钟未来",
        "account": ACCOUNT_NAME,
        "publishDate": date,
        "contentDate": selection.get("contentDate", date),
        "contentStart": selection.get("contentStart", selection.get("contentDate", date)),
        "contentEnd": selection.get("contentEnd", selection.get("contentDate", date)),
        "coverageLabel": selection.get("coverageLabel", ""),
        "dateLabel": date.replace("-", "."),
        "vol": vol,
        "volLabel": f"VOL. {vol:03d}",
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "cover": cover,
        "items": items,
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--vol", type=int, default=1)
    args = parser.parse_args()

    selection = load_selection(args.date)
    out_path = write_final(args.date, args.vol, selection)
    print(f"OK final -> {out_path}")


if __name__ == "__main__":
    main()
