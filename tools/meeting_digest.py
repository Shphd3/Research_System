#!/usr/bin/env python3
"""Draft a meeting brief from exploration logs. Output is pending researcher confirmation."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ENTRY = re.compile(r'^## (\d{4})\b(.*)$', re.M)
FIELD = re.compile(r'^- (假设|先验→模型→计算|跑前预测|竞争解释|结果|研究者决定|链条位置)：(.*)$', re.M)
UPDATE = re.compile(r'^今日认识更新：(.+)$', re.M)


def entries(log: Path):
    text = log.read_text(encoding='utf-8')
    heads = list(ENTRY.finditer(text))
    for i, h in enumerate(heads):
        body = text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        fields = {k: v.strip() for k, v in FIELD.findall(body)}
        updates = [u.strip() for u in UPDATE.findall(body) if u.strip()]
        yield h.group(1), h.group(2).strip(), fields, updates


def build(root: Path, since: str, until: str) -> str:
    out = ['# 组会简报草稿（待研究者确认）', '',
           f'来源：`{root}` 下的探索日志，日期 {since}–{until}。本稿只汇总日志原文，不生成科学结论。', '']
    concl, hyp, analysis, pure = [], [], [], 0
    total = 0
    for log in sorted(root.glob('*/log.md')):
        for day, title, f, ups in entries(log):
            if not (since <= day <= until):
                continue
            total += 1
            pure += '纯理解' in f.get('链条位置', '')
            src = log.parent.name
            for u in ups:
                concl.append(f'- {u}（{src} {day}）')
            if f.get('假设'):
                chain = f.get('先验→模型→计算')
                hyp.append(f"- {f['假设']}" + (f"；依据：{chain}" if chain else '') + f"（{src}）")
            analysis.append(f"- **{src} {day} {title}**：结果 {f.get('结果', '—')}；"
                            f"决定 {f.get('研究者决定', 'Unknown')}；链条 {f.get('链条位置', '未标注')}")
    out += ['## 目的', '', '<研究者补一句：本次要回答的问题>', '',
            '## 结论（从“今日认识更新”中保留 2–3 条最重要的）', '', *(concl or ['- 无']), '',
            '## 假设（预期的认识更新）', '', *(hyp or ['- 无']), '',
            '## 实验分析（原始结果见链接）', '', *(analysis or ['- 无']), '',
            f'统计：{total} 条记录，其中“纯理解” {pure} 条。', '']
    return '\n'.join(out)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('explore_root', type=Path)
    p.add_argument('--since', required=True, help='MMDD inclusive')
    p.add_argument('--until', default='1231', help='MMDD inclusive')
    p.add_argument('--output', type=Path)
    a = p.parse_args(argv)
    text = build(a.explore_root, a.since, a.until)
    if a.output:
        a.output.write_text(text, encoding='utf-8')
    else:
        print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
