"""Render the derived Anchor review atlas; never edits canonical research files."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATE = HERE.parent
ROOT = DATE.parent.parent
DATA = json.loads((HERE / "anchor_atlas_data.json").read_text())
ROWS = {r["index"]: r for r in DATA["rows"]}
FONT_PATH = ROOT / "daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf"
FIGURES = DATE / "figures"
FIGURES.mkdir(exist_ok=True)
DOCS = DATE / "docs"
DOCS.mkdir(exist_ok=True)

COLUMNS = [
    ("形成与路由基础", "A01—A10", "#245CAA", [
        ("A01 · 共同结构的定义与识别", list(range(0, 4))),
        ("A05 / 历史 A02 · 初始化与分路锁定", list(range(4, 11))),
        ("A06 · 从分区到专家功能", list(range(11, 17))),
        ("A07 · 嵌套骨架、干扰与功能绑定", list(range(17, 24))),
        ("A09 / 历史 A04 · 频率与稀有判别", [24, 25]),
        ("A10 · 频率谱与学习稳定性", [26, 27]),
    ]),
    ("监督、组合与复用", "A11—A14", "#197C79", [
        ("A11 · 监督信号如何变成功能", list(range(28, 35))),
        ("A12 · 组合任务与容量边界", list(range(35, 41))),
        ("A13 · 中继必要性与目标作用", list(range(41, 48))),
        ("A14 · 层级、关系复用与秩", list(range(48, 56))),
    ]),
    ("谱结构与新增可读性", "A15 · 前半", "#6D55AC", [
        ("A15_00 · 输入几何与门控偏好", list(range(56, 60))),
        ("A15_01 · 学习速度与反馈", list(range(60, 63))),
        ("A15_02 · 逐层语义与谱位置", list(range(63, 71))),
        ("A15_03 / 04 · 中尾固定带边界", [115, 71]),
        ("A15_05 · 谱坐标的功能准入", list(range(72, 78))),
        ("A15_06 · 在线谱路由与专家利用", list(range(78, 81))),
        ("A15_07 · 监督方向与跨域图谱", [81, 82]),
        ("A15_08 · 层新增信息与功能维度", list(range(83, 92))),
    ]),
    ("语义功能、自编码与更新", "A15 · 后半 / A16 / 草案", "#AE6131", [
        ("A15_09 / 10 · 方向复用与功能转移", [92, 93, 94]),
        ("A15_11 / 12 · 专家树与表达边界", [95, 96]),
        ("A15_13 · 语义监督与结构路由", list(range(97, 109))),
        ("A15_14 / 15 / 16 · 几何与功能位置", [109, 110, 111]),
        ("A15_17 · 自编码约束、复用与可分性", [112, 113, 114]),
        ("A16 · 负载控制与功能增量路由", list(range(116, 121))),
        ("待归属的近期草案 · 不计为正式项目 Anchor", [121, 122, 123]),
    ]),
]

ORDER = [i for _, _, _, groups in COLUMNS for _, ids in groups for i in ids]
assert len(ORDER) == len(set(ORDER)) == 124
assert set(ORDER) == set(ROWS)
assert sum(r["role"] == "归档" for r in ROWS.values()) == 3

WIDTH = 6680
MARGIN = 48
GAP = 32
COLW = (WIDTH - 2 * MARGIN - 3 * GAP) // 4
TEXTW = COLW - 56
HEADER = 468
GROUP_H = 64
CARD_GAP = 11
FONTS = {s: ImageFont.truetype(str(FONT_PATH), s) for s in [20, 22, 23, 24, 26, 28, 30, 32, 36, 42, 54, 66]}
OPERATIONS = []
BOUNDS = []


def wrap(text, size, width):
    lines, current = [], ""
    for ch in text:
        if current and FONTS[size].getlength(current + ch) > width:
            lines.append(current)
            current = ch
        else:
            current += ch
    if current:
        lines.append(current)
    return lines


def text(x, y, value, size=24, fill="#27364B"):
    OPERATIONS.append(("text", x, y, value, size, fill))


def rect(x, y, w, h, fill, radius=0, outline=None):
    OPERATIONS.append(("rect", x, y, w, h, fill, radius, outline))


def block(x, y, value, size, width, fill, line_height):
    lines = wrap(value, size, width)
    for n, line in enumerate(lines):
        text(x, y + n * line_height, line, size, fill)
    return len(lines) * line_height


def card(x, y, row, color):
    title = wrap(row["question"], 28, TEXTW)
    evidence = wrap("证据｜" + row["evidence"], 24, TEXTW)
    update = wrap("更新｜" + row["update_draft"], 24, TEXTW)
    height = 24 + 31 + len(title) * 39 + len(evidence) * 34 + len(update) * 34 + 12
    archive = row["role"] == "归档"
    draft = row["role"] == "未归属草案"
    fill = "#F0F2F5" if archive else ("#FFF7EB" if draft else "#FFFFFF")
    rect(x, y, COLW, height, fill, 12, "#DBE1EA")
    rect(x, y + 12, 5, height - 24, "#8A939F" if archive else color, 2)
    text(x + 25, y + 13, row["id"], 23, "#616D7D" if archive else color)
    badge = row["role"] + (" · 记录不同步/缺口" if row["record_lag"] else "")
    badge_w = FONTS[20].getlength(badge)
    id_w = FONTS[23].getlength(row["id"])
    assert id_w + badge_w + 78 < COLW, (row["id"], badge)
    text(x + COLW - 25 - badge_w, y + 16, badge, 20, "#7C8795")
    cy = y + 45
    for line in title:
        text(x + 25, cy, line, 28, "#152B46")
        cy += 39
    for line in evidence:
        text(x + 25, cy, line, 24, "#35465C")
        cy += 34
    for line in update:
        text(x + 25, cy, line, 24, "#176466" if not archive else "#64727C")
        cy += 34
    assert cy <= y + height - 4
    BOUNDS.append({"index": row["index"], "id": row["id"], "box": [x, y, x + COLW, y + height]})
    return height


text(MARGIN, 33, "全部 Anchor：研究问题 · 证据 · 认识更新", 66, "#112A46")
text(MARGIN, 135, "121 份项目 Anchor（118 非归档 + 3 归档）  ＋  3 份待归属草案  ｜  2026-09-26 阅读快照", 36, "#53657B")
text(MARGIN, 199, "Anchor = 研究设计卡；“更新”为 AI 依据来源压缩的待审表述。非归档不代表活跃，图中不作去留决定。", 30, "#41566D")
text(MARGIN, 246, "三个独立问题：① 结构如何形成？     ② 结构承载什么？     ③ 结构对分路、专家和共享更新有何作用？", 30, "#41566D")
text(MARGIN, 292, "可读 ≠ 原生使用；几何相似 ≠ 更新兼容；正确标签强制分路有效 ≠ 学得路由有效。各环节需要自己的证据。", 30, "#41566D")
text(MARGIN, 338, "读法：每栏自上而下。父子卡分别保留；灰色为归档，浅黄为草案。SAE = 稀疏自编码器。数值按各协议理解，勿跨卡直接比较。", 28, "#617185")
rect(MARGIN, 406, WIDTH - 2 * MARGIN, 2, "#D5DDE8")

ends = []
for column, (heading, subtitle, color, groups) in enumerate(COLUMNS):
    x, y = MARGIN + column * (COLW + GAP), HEADER
    rect(x, y, COLW, 104, color, 14)
    text(x + 24, y + 12, heading, 36, "#FFFFFF")
    text(x + 24, y + 61, subtitle, 23, "#EEF3FC")
    y += 123
    for group_name, ids in groups:
        text(x + 4, y + 9, group_name, 26, color)
        assert FONTS[26].getlength(group_name) < COLW
        y += GROUP_H
        for i in ids:
            y += card(x, y, ROWS[i], color) + CARD_GAP
        y += 13
    ends.append(y)

FOOTER = max(ends) + 32
HEIGHT = FOOTER + 387
rect(MARGIN, FOOTER, WIDTH - 2 * MARGIN, 318, "#E7EDF4", 16)
text(MARGIN + 25, FOOTER + 19, "判定时只需逐条回答：保留当前问题 / 合并导航 / 退出当前议程 / 待补证据。原始证据的删除另行逐项批准。", 32, "#223C59")
text(MARGIN + 25, FOOTER + 80, "范围：中英文伴随稿只计一份；父子问题不当作重复文件；历史阅读副本不另计 Anchor；A00 是跳转页。", 28, "#52657A")
text(MARGIN + 25, FOOTER + 127, "编号异常：A15_08_06 对应“8B 复现”和“语义子空间”两个不同问题；A14 的归档旧版与现版也有同号。", 28, "#52657A")
text(MARGIN + 25, FOOTER + 174, "证据边界：本图整理来源记录与补核结果，不是全量原始数组复算。已完成测量、有效结论和研究者认可分别处理。", 28, "#52657A")
text(MARGIN + 25, FOOTER + 221, "每张卡的完整 Anchor 路径、补核记录、来源摘要校验值及留白判定栏，见同日 docs/anchor_atlas_cn.md 与 report_assets/anchor_atlas_data.json。", 26, "#52657A")
text(MARGIN, FOOTER + 338, "Derived review view · AI_DRAFT_FOR_HUMAN_JUDGMENT · canonical Anchors / Focus / Graph unchanged · no deletions", 22, "#738296")

im = Image.new("RGB", (WIDTH, HEIGHT), "#F5F7FB")
draw = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
       '<title>Research System 全部 Anchor 判定总览</title>',
       '<desc>121 份项目 Anchor 及 3 份近期草案。每项包含问题、证据、AI 待审认识更新；去留未判定。</desc>',
       f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#F5F7FB"/>']
for op in OPERATIONS:
    if op[0] == "rect":
        _, x, y, w, h, fill, radius, outline = op
        draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=outline, width=1)
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{outline or "none"}"/>')
    else:
        _, x, y, value, size, fill = op
        assert x >= 0 and x + FONTS[size].getlength(value) <= WIDTH - 20, (value, x)
        assert y >= 0 and y + size <= HEIGHT
        draw.text((x, y), value, font=FONTS[size], fill=fill, anchor="lt")
        svg.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" dominant-baseline="text-before-edge" font-family="Noto Sans CJK SC,Microsoft YaHei,PingFang SC,sans-serif">{html.escape(value)}</text>')
svg.append("</svg>")
png = FIGURES / "anchor_atlas_all_20260926.png"
svgpath = FIGURES / "anchor_atlas_all_20260926.svg"
im.save(png, optimize=True)
svgpath.write_text("\n".join(svg) + "\n")
(HERE / "anchor_atlas_layout.json").write_text(json.dumps({"size": [WIDTH, HEIGHT], "cards": BOUNDS}, ensure_ascii=False, indent=2) + "\n")

md = ["# 全部 Anchor 判定图与逐条来源", "", "状态：`DERIVED_AI_DRAFT_FOR_HUMAN_JUDGMENT`。2026-09-26 来源快照；未修改任何科学状态或既有文件，未删除。", "",
      "项目范围内独立 Anchor 共 121 份：118 份非归档、3 份归档。另列 3 份近期待归属草案，总计 124 张卡。中英文伴随稿、日期阅读副本不重复计数。非归档不等于当前活跃；研究者的最终认识与去留判定保持空白。", "",
      "![全部 Anchor 判定总览](../figures/anchor_atlas_all_20260926.png)", "",
      "[矢量图，适合放大](../figures/anchor_atlas_all_20260926.svg) · [来源清单及 SHA-256](../report_assets/anchor_atlas_data.json) · [生成脚本](../report_assets/render_anchor_atlas.py)", "",
      "## 如何判定", "",
      "每张卡依次是：研究问题、来源记录中的证据、AI 压缩的有界认识更新。科学结论是否接受由你决定。本图没有将运行完成、工程通过、描述性相关或前驱实验转换为机制确认，也没有打开封存的确认数据。没有结果摘要只表示归档缺口，不能推断工作没有运行。", "",
      "可在最后一列填写：保留当前问题、合并导航、退出当前议程、待补证据；若要删除，另指明具体文件并批准。父子问题有包含关系不代表文件重复，反例与失败记录仍可能需要保留。", "",
      "## 范围与编号", "",
      "- A00 是入口跳转，不是独立 Anchor；未发现独立 A03/A08 Anchor。历史 A02 位于 05 线，A04 位于 09 线。", 
      "- 两份 A15_08_06 是不同问题，分别标为 8B 复现和语义子空间；没有更改编号。", 
      "- A14 的旧版归档与现版同号，但问题和证据不同；图中分别列出。", 
      "- 三份根目录日期草案尚未纳入 from 的正式 Anchor 所有权链；列出不代表激活新主线。", 
      "- 来源优先于本图。默认依据对应 Anchor 的证据与边界；发现结果记录更新时补核，并标出记录不同步或缺口。未逐一复算全部历史原始数组。", "",
      "## 逐条来源与留白判定", ""]
for heading, subtitle, color, groups in COLUMNS:
    md += [f"### {heading} · {subtitle}", ""]
    for group_name, ids in groups:
        md += [f"**{group_name}**", "", "| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |", "|---|---|---|---|---|"]
        for i in ids:
            r = ROWS[i]
            label = f"[{r['id']}]({r['anchor_path']}) · {r['role']}"
            for j, source in enumerate(r["supplemental_sources"], 1):
                label += f" · [补核{j}]({source['path']})"
            if r["record_lag"]:
                label += " · 记录不同步/缺口"
            fields = [label, r["question"], r["evidence"], r["update_draft"], "—"]
            md.append("| " + " | ".join(s.replace("|", "\\|") for s in fields) + " |")
        md.append("")
md += ["## 图件来源与复现", "", "图件是本清单的派生阅读视图，所有图件物理位于同日 figures/。`anchor_atlas_data.json` 保存每张卡的完整来源路径、SHA-256、补核记录与空白人工判定；没有复制原始运行日志或数据。", ""]
for p in [HERE / "anchor_atlas_data.json", FONT_PATH, png, svgpath]:
    md.append(f"- `{p}` — SHA-256 `{hashlib.sha256(p.read_bytes()).hexdigest()}`")
md += ["", "生成命令：", "", "```bash", f"python {Path(__file__).resolve()}", "```", ""]
(DOCS / "anchor_atlas_cn.md").write_text("\n".join(md))
print(json.dumps({"cards": len(ROWS), "size": [WIDTH, HEIGHT], "png": str(png), "svg": str(svgpath), "index": str(DOCS / "anchor_atlas_cn.md")}, ensure_ascii=False))
