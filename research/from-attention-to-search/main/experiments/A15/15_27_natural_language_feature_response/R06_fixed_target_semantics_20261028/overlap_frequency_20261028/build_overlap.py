"""User-requested descriptive join of frozen R06 membership and existing R04 DCLM counts.

No model access, classification fitting, new hypothesis tests or reselection.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import shutil
import zipfile
import re

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import markdown

O = Path(__file__).resolve().parent
R = O.parent
R4 = R.parent / 'R04_domain_usage_20261027'
R5 = R.parent / 'R05_distance_attention_20261028'
E = Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response') / R.name / O.name
FONT = '/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis/report_assets/fonts/NotoSansCJKsc-Regular.otf'
fontManager.addfont(FONT)
plt.rcParams.update({'font.family': FontProperties(fname=FONT).get_name(), 'axes.unicode_minus': False, 'pdf.fonttype': 42})
COLORS = {'far_no_confirmed_drop': '#287a83', 'far_and_drop': '#c76b29', 'far_insufficient_no_confirmed_drop': '#875c8f'}
LABEL = {'far_no_confirmed_drop': '远处仍响应；近减远未达条件', 'far_and_drop': '远处仍响应；近处更强', 'far_insufficient_no_confirmed_drop': '远处证据不足；近减远也未达条件'}
MEANINGS = {'plant': ('植物', '工厂'), 'bank': ('河岸', '银行'), 'organ': ('身体器官', '管风琴'), 'bass': ('鱼', '低音乐器')}
ORDER = {'plant': 0, 'bank': 1, 'organ': 2, 'bass': 3}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def save(fig, name):
    fig.savefig(O / (name + '.png'), dpi=170, bbox_inches='tight')
    fig.savefig(O / (name + '.pdf'), bbox_inches='tight')
    plt.close(fig)


def rate_label(row):
    if row['DCLM_hits'] == 0:
        return '0/65,536†'
    rate = row['DCLM_frequency_percent']
    return f"{rate:.4f}%" + ('†' if row['reference_low_support'] else '')


def build_rows():
    near_path = R / 'analysis/near_results.json'
    far_path = R / 'analysis/far_results_readable.json'
    near = json.loads(near_path.read_text())
    far = json.loads(far_path.read_text())
    key = lambda x: (x['dictionary'], x['concept'], x['feature'], x['direction'])
    selected = {key(x): x for x in near if x['semantic_qualified']}
    assert len(selected) == 52 and set(selected) == {key(x) for x in far}
    frequency = {}
    source_paths = [near_path, far_path, R / 'config.json', R / 'analysis/pre_heldout_freeze.json', R / 'forward_ledger.jsonl']
    for k in ['SAE', 'CC']:
        p = R4 / f'forward/reference_{k}.npz'
        source_paths.append(p)
        with np.load(p) as a:
            hits = a['counts'].sum(0).astype(int)
            n = int(a['n_positions'].sum())
        assert n == 65536
        freq = hits / n
        cuts = np.quantile(freq[hits >= 20], [1 / 3, 2 / 3])
        bands = np.where(hits < 20, -1, (freq > cuts[0]).astype(int) + (freq > cuts[1]).astype(int))
        frequency[k] = (hits, n, bands, cuts)
    rows = []
    for f in far:
        n = selected[key(f)]
        # Read the saved frozen conditional criteria,then independently check their predicates.
        for endpoint in ['far_E', 'near_minus_far']:
            z = f[endpoint]
            expected = z['mean'] > .1 and z['CI'][0] > .1 and z['q'] < .05
            assert expected == z['conditional_criterion_met']
        B = f['far_E']['conditional_criterion_met']
        C = f['near_minus_far']['conditional_criterion_met']
        assert B or not C, 'If unexpected membership appears, preserve rather than force a partition.'
        category = 'far_and_drop' if C else 'far_no_confirmed_drop' if B else 'far_insufficient_no_confirmed_drop'
        hits, total, bands, _ = frequency[f['dictionary']]
        fid = f['feature']
        meanings = MEANINGS[f['concept']]
        row = dict(dictionary=f['dictionary'], concept=f['concept'], feature=fid, direction=f['direction'],
                   preferred_meaning=meanings[0 if f['direction'] == 1 else 1],
                   comparison_meaning=meanings[1 if f['direction'] == 1 else 0],
                   near_qualified=True, far_conditional_response=bool(B), near_stronger_conditional=bool(C),
                   category=category, category_cn=LABEL[category],
                   near_E=n['E']['mean'], near_E_CI_low=n['E']['CI'][0], near_E_CI_high=n['E']['CI'][1], near_E_q=n['E']['q'],
                   far_E=f['far_E']['mean'], far_E_CI_low=f['far_E']['CI'][0], far_E_CI_high=f['far_E']['CI'][1], far_E_q=f['far_E']['q'],
                   near_minus_far=f['near_minus_far']['mean'], delta_CI_low=f['near_minus_far']['CI'][0], delta_CI_high=f['near_minus_far']['CI'][1], delta_q=f['near_minus_far']['q'],
                   DCLM_hits=int(hits[fid]), DCLM_positions=total, DCLM_frequency=float(hits[fid] / total),
                   DCLM_frequency_percent=float(hits[fid] / total * 100),
                   DCLM_reference_band=['低', '中', '高'][int(bands[fid])] if bands[fid] >= 0 else '参考支持不足',
                   reference_low_support=bool(hits[fid] < 20),
                   normalized_scale=n['scale'], heldout_family_support=n['heldout_support'],
                   interpretation='远处与近减远均为近距筛选后的条件性/探索性；频率只是既有DCLM参考频率')
        rows.append(row)
    rows.sort(key=lambda x: (0 if x['dictionary'] == 'SAE' else 1, ORDER[x['concept']], x['feature']))
    count = Counter(x['category'] for x in rows)
    assert count == {'far_no_confirmed_drop': 41, 'far_and_drop': 10, 'far_insufficient_no_confirmed_drop': 1}
    assert sum(x['reference_low_support'] for x in rows) == 4
    source_hashes = {str(p): sha(p) for p in source_paths}
    assert len((R / 'forward_ledger.jsonl').read_text().splitlines()) == 517
    return rows, source_hashes, frequency


def overview(rows):
    fig, ax = plt.subplots(figsize=(12, 6.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.2); ax.axis('off')
    ax.add_patch(FancyBboxPatch((.3, .7), 11.4, 4.7, boxstyle='round,pad=.1', facecolor='#f4f6f7', edgecolor='#435763', linewidth=2))
    ax.text(.6, 5.05, '近距合格 A：52 个“字典×目标词×feature×方向”对象', fontsize=16, weight='bold')
    ax.add_patch(FancyBboxPatch((.7, 1.25), 8.45, 3.1, boxstyle='round,pad=.1', facecolor='#dfedef', edgecolor=COLORS['far_no_confirmed_drop'], linewidth=2))
    ax.text(1.0, 3.94, '远处仍响应 B：51', fontsize=16, color='#175c63', weight='bold')
    ax.text(1.0, 2.8, 'B 中未确认近减远差异：41\nSAE 23；CrossCoder 18\n“未确认减弱”不等于已证明相等', fontsize=12, linespacing=1.7)
    ax.add_patch(FancyBboxPatch((5.65, 1.55), 3.05, 1.95, boxstyle='round,pad=.1', facecolor='#f8e5d4', edgecolor=COLORS['far_and_drop'], linewidth=2))
    ax.text(7.17, 2.54, '近处更强 C：10\nSAE 2；CrossCoder 8\n这10个远处也仍响应', ha='center', va='center', fontsize=13, linespacing=1.6, color='#8b461a')
    ax.text(10.45, 3.55, 'A 内、B 外：1', ha='center', fontsize=12, color=COLORS['far_insufficient_no_confirmed_drop'], weight='bold')
    ax.text(10.45, 2.56, 'SAE f16034\norgan → 管风琴\n远处证据不足\n也未确认近减远', ha='center', va='center', fontsize=11, linespacing=1.6)
    ax.text(6, .21, 'C ⊂ B ⊂ A；三份名单不是三套互斥“长短程模块”。远处与近减远均为条件性／探索性。', ha='center', fontsize=11)
    ax.text(6, 5.93, 'R06：52、51、10 的实际重叠关系（框面积不表示数量）', ha='center', fontsize=17, weight='bold')
    save(fig, '01_三份名单的包含关系')


def all_objects(rows):
    fig, axs = plt.subplots(1, 2, figsize=(18, 15.8), sharex=True)
    for ax, k in zip(axs, ['SAE', 'CC']):
        sub = [x for x in rows if x['dictionary'] == k]
        for i, x in enumerate(sub):
            c = COLORS[x['category']]
            ax.axhline(i, color='#eef0f1', lw=.7, zorder=0)
            ax.plot([x['near_E'], x['far_E']], [i, i], color=c, lw=2, alpha=.85)
            ax.plot([x['far_E_CI_low'], x['far_E_CI_high']], [i-.10, i-.10], color=c, lw=1, alpha=.7)
            ax.scatter(x['near_E'], i, s=38, facecolor='white', edgecolor=c, lw=1.5, zorder=3)
            ax.scatter(x['far_E'], i, s=38, color=c, zorder=4)
            ax.text(2.65, i, rate_label(x), ha='right', va='center', fontsize=9, color='#9a3131' if x['reference_low_support'] else '#27343b')
            ax.text(2.69, i, f"{x['DCLM_hits']:,}", ha='left', va='center', fontsize=8.5, color='#9a3131' if x['reference_low_support'] else '#27343b')
        ax.set_yticks(range(len(sub)), [f"{x['concept']} · f{x['feature']} → {x['preferred_meaning']}" for x in sub], fontsize=9.5)
        ax.invert_yaxis(); ax.set_ylim(25.9, -1.8); ax.set_xlim(-.03, 2.88)
        ax.set_xticks([0, .5, 1, 1.5, 2]); ax.set_xlabel('相关编辑响应减无关编辑响应 E／发现集固定RMS', fontsize=11)
        ax.axvline(.1, color='#8b9297', ls='--', lw=1)
        ax.text(2.65, -1.05, 'DCLM频率', ha='right', fontsize=10, weight='bold')
        ax.text(2.69, -1.05, '命中数', fontsize=10, weight='bold')
        ax.set_title(f'{k}：26个合格对象', fontsize=15, pad=13)
        for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
    fig.suptitle('每行一个固定对象：具体feature、含义偏好、近远响应与独立DCLM频率', fontsize=19, y=.99)
    fig.subplots_adjust(left=.17, right=.97, wspace=.59, top=.93, bottom=.09)
    fig.text(.17, .042, '空心点＝16；实心点＝144；细横线＝远处95%家族区间。蓝绿＝远仍响应、差异未达条件；橙＝远仍响应且近更强；紫＝远处不足。', fontsize=10.5)
    fig.text(.17, .021, '频率分母均65,536；†＝参考命中<20，估计不稳；0次命中不是普遍频率为零。SAE f1205在organ和bass出现两行，但仍是同一坐标。', fontsize=10.5)
    save(fig, '02_全部52对象_含义频率近远响应')


def frequency_plot(rows):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), sharey=True)
    for ax, k in zip(axes, ['SAE', 'CC']):
        sub = [x for x in rows if x['dictionary'] == k]
        for x in sub:
            freq = x['DCLM_frequency_percent']
            pos = freq if freq > 0 else 100/65536/2
            c = COLORS[x['category']]
            ax.plot([pos, pos], [x['delta_CI_low'], x['delta_CI_high']], color=c, lw=.9, alpha=.45)
            marker = '<' if freq == 0 else '^' if x['reference_low_support'] else 'o'
            ax.scatter(pos, x['near_minus_far'], s=65 if x['reference_low_support'] else 45, marker=marker, facecolor='white' if x['reference_low_support'] else c, edgecolor=c, lw=1.3, zorder=3)
            if x['near_stronger_conditional'] or not x['far_conditional_response'] or x['feature'] in [557, 47, 23473]:
                offset={3959:(5,-18),7317:(-60,18),8586:(-78,-18),11886:(5,10),11136:(5,-15)}.get(x['feature'],(4,6))
                ax.annotate(f"{x['concept']} f{x['feature']}", (pos, x['near_minus_far']), xytext=offset, textcoords='offset points', fontsize=8)
        ax.set_xscale('log'); ax.set_xlim(.00045, 65); ax.axhline(0, color='#6b7379', lw=.8); ax.axhline(.1, color='#93989c', lw=.8, ls='--')
        ax.set_title(k, fontsize=15); ax.set_xlabel('DCLM参考激活率（%，对数轴）', fontsize=11)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    axes[0].set_ylabel('近距E − 远距E（固定发现RMS单位）', fontsize=11)
    fig.suptitle('频率与近远差异：描述这52个已筛选对象，不检验频率机制', fontsize=17)
    fig.subplots_adjust(bottom=.22, top=.86, wspace=.12)
    fig.text(.12, .105, '橙色＝近更强条件达标；蓝绿＝远仍响应但差异未达标；紫色＝远处证据不足。误差棒＝同家族近减远95%区间。', fontsize=10.5)
    fig.text(.12, .061, '空心三角＝DCLM命中<20；左箭头＝0次命中，仅为显示放在半个命中率位置。零命中坐标没有可靠频率排序。', fontsize=10.5)
    fig.text(.12, .022, '同一坐标在不同目标词下可重复出现；同词共享家族，点不是独立概念。无新增拟合、检验或模型前向。', fontsize=10.5)
    save(fig, '03_频率与近远差异_描述性')


def report(rows):
    by = Counter(x['category'] for x in rows)
    c = [x for x in rows if x['near_stronger_conditional']]
    freqstats = {}
    for k in ['SAE', 'CC']:
        freqstats[k] = {}
        for category in LABEL:
            rr = [x for x in rows if x['dictionary'] == k and x['category'] == category]
            if rr:
                v = [x['DCLM_frequency_percent'] for x in rr]
                freqstats[k][category] = dict(n=len(rr), min_percent=min(v), median_percent=float(np.median(v)), max_percent=max(v), low_reference_support=sum(x['reference_low_support'] for x in rr))
    dump(O/'membership_summary.json', dict(A=52, B=51, C=10, C_subset_B=True, B_subset_A=True,
        regions=dict(by), unique_coordinates=dict(SAE=25, CC=26), low_reference_support=4,
        zero_reference_hits=[{k:x[k] for k in ['dictionary','concept','feature','DCLM_hits']} for x in rows if x['DCLM_hits']==0],
        difference_candidate_concepts=dict(Counter(x['concept'] for x in c)), descriptive_frequency_summary=freqstats,
        new_forward=0, new_hypothesis_tests=0, reselection=False))
    lines=['# R06三份名单与DCLM频率：讨论用读图说明', '',
    '**先看结论：10个近处更强对象全部仍属于51个远处响应对象。这不是“10个短程、51个长程”两套名单。** 本补充只连接既有结果和既有参考频率，不新增模型前向、假设检验、拟合或候选选择；频率关系全部为事后描述。', '',
    '## 1. 三份名单怎样重叠', '',
    'A为近距D/E/L完整合格52对象；B为A内远处E满足冻结条件51对象；C为A内近减远E满足条件10对象。B/C沿用R06原有条件性/探索性判定，未重新定阈值。', '',
    '![包含关系](01_三份名单的包含关系.png)', '',
    '|互斥展示区|SAE|CrossCoder|合计|可以怎么说|', '|---|---:|---:|---:|---|',
    '|远处仍响应，近减远差异未达条件|23|18|41|未确认减弱；不能叫近远相等或完全保持|',
    '|远处仍响应，同时近处更强|2|8|10|有条件性减弱线索，远处没有消失|',
    '|远处证据不足，近减远也不足|1|0|1|不能归为短程或远处无响应|', '',
    '最后一个是SAE organ f16034，偏好管风琴：远E0.468，95%区间[0.165,0.812]，q0.053；近减远没有达条件。正均值、区间正仍不足以绕过既有校正规则。', '',
    '## 2. 每个对象的含义、响应和频率', '',
    '![完整对象清单](02_全部52对象_含义频率近远响应.png)', '',
    '每行是“字典×目标词×feature×方向”，不是一个新概念，也不是簇；箭头含义为发现阶段固定的偏好。空心点读16，实心点读144，实心点旁细横线是远E的95%家族区间。E是同方向相关编辑变化减去同义无关编辑变化，再除该对象发现集RMS；不是激活率，也不是功能重要性。', '',
    '52行涉及SAE25个不同坐标、CrossCoder26个不同坐标；SAE f1205在organ和bass都偏好乐器侧，所以出现两行。不同字典编号不对应；不能合并成51个跨字典同类feature。', '',
    'DCLM频率来自R04已匹配原生接口的256窗口/65,536token位置，直接用已有z>0命中数。SAE是E16局部接口，CC是原14层共享z接口，不是最后层独立频率。频率不进入本补充的名单选择。参考命中<20用†标记，不作可靠低/中/高分组；0次命中不等于普遍不存在。', '',
    '## 3. 哪些更强、哪些未确认减弱', '',
    '|字典与目标|候选feature|偏好|DCLM命中/65,536|DCLM参考频率|近E → 远E|近减远95%区间|',
    '|---|---|---|---:|---:|---:|---|']
    for x in c:
        lines.append(f"|{x['dictionary']} {x['concept']}|f{x['feature']}|{x['preferred_meaning']}|{x['DCLM_hits']:,}|{rate_label(x)}|{x['near_E']:.3f} → {x['far_E']:.3f}|[{x['delta_CI_low']:.3f}, {x['delta_CI_high']:.3f}]|")
    lines += ['', '以上10个全部远处仍有超无关编辑响应。8/10来自bass，另bank/organ各1；因此不能把这组频率构成外推为一般长短程规律。†为低参考支持，并不否定受控语义面板的响应；它限制的是参考频率判断。', '',
    '例如CC plant f557偏好植物，近E1.406、远1.358，近减远区间[-0.080,0.176]；参考命中898/65,536=1.3702%。这是“远处仍响应、没有确认明显减弱”的具体对象，不是证明两距离完全相等。CC bass f3641偏好鱼，近1.533、远1.097、差0.436，差区间[0.313,0.555]；但DCLM只命中19次，0.0290%，参考频率支持不足。', '',
    '## 4. 能怎样推进导师关于频率与长短程的讨论', '',
    '![频率与差异](03_频率与近远差异_描述性.png)', '',
    '每点仍是一个概念×feature对象，横轴为独立DCLM参考激活率，纵轴为近E减远E；橙色点满足原差异条件，三角为频率低支持。没有新相关检验、回归、频率匹配或null，所以这里不能声称频率与衰减已建立统计关系。', '',
    '**有证据的推进一：用响应轨迹而不是频率命名长短程。** 同一对象可同时近处合格、远处仍响应且远处较弱。41行未达差异条件，不是41行被证明稳定相等；10行也不是短程专属。原有频率与高低阶、长短程的直觉现在有了具体可核对的对象和反例，但尚无互斥分工。', '',
    '**有证据的推进二：远处候选并不只有一个频率水平。** SAE中，远处仍响应的f47 bank偏好银行，频率37.3260%；同样远处响应的f23609 bass偏好鱼只有7次参考命中，0.0107%，频率估计不稳。CC中，plant f557为1.3702%，bass f6981为23.7457%；差异对象也从低支持f3641的0.0290%到bank f8586的7.7026%。这给出了“频率不能直接充当响应距离标签”的实际例子，不能证明总体无关联。', '',
    '**仍无法回答：** 是否低频更易减弱/更依赖远处，是否高频更能保持，以及是否频率导致这种组织。候选先按近语义响应筛选、每字典同词只有8留出家族、10个差异对象中8个bass、同坐标会重复、4个参考低支持，加上句序和筛选偏差，都限制频率解释。两字典的频率与稀疏性不能混成一个总体排行。', '',
    '远处阶段没有诱饵版本，因此B只是远处相关编辑响应，不是远处完整语义资格。近远比较由近留出挑对象，保持同家族虽然改善可比性，仍有筛选和句序混杂，不能把差异归因于距离本身。', '',
    '## 5. 全部52行（含可追溯数值）', '',
    '|字典|目标词|feature|偏好含义|DCLM命中|DCLM频率|近E|远E|类别|', '|---|---|---|---|---:|---:|---:|---:|---|']
    for x in rows:
        lines.append(f"|{x['dictionary']}|{x['concept']}|f{x['feature']}|{x['preferred_meaning']}|{x['DCLM_hits']:,}|{rate_label(x)}|{x['near_E']:.3f}|{x['far_E']:.3f}|{x['category_cn']}|")
    lines += ['', '[完整CSV：原始频率、支持、近远效应、区间和q](all52_membership_frequency.csv)。每一行可由源JSON对象key及参考npz对应坐标重建，manifest列出源哈希。旧统计、候选、预算和报告未改写。', '',
              '## 图的解释边界', '',
              '图一允许读名单包含，不能读模块结构；图二允许读每对象响应及参考频率，不能把未确认减弱当等效或把贡献当重要性；图三只允许描述有限候选的频率分布，不建立频率机制或独立距离因果。所有新增连接/频率解读均为探索性。研究者机制接受及问题关闭仍Unknown。']
    (O/'读图说明_cn.md').write_text('\n'.join(lines) + '\n')


def package(source_hashes):
    E.mkdir(parents=True, exist_ok=False)
    for p in O.iterdir():
        if p.is_file() and p.suffix in ['.md', '.csv', '.json', '.png', '.pdf', '.py']:
            shutil.copy2(p, E/p.name)
    style = 'body{max-width:1200px;margin:32px auto;padding:0 24px;font:17px/1.8 system-ui;color:#26363e}img{max-width:100%}table{border-collapse:collapse;font-size:14px}td,th{border:1px solid #ccd5da;padding:6px}pre{overflow:auto}'
    body=markdown.markdown((O/'读图说明_cn.md').read_text(),extensions=['tables','fenced_code'])
    (O/'从这里开始.html').write_text('<!doctype html><meta charset="utf-8"><title>R06名单与频率</title><style>'+style+'</style>'+body)
    files=[p for p in O.iterdir() if p.is_file() and p.suffix in ['.md','.csv','.json','.png','.pdf','.py','.html'] and p.name not in ['package_receipt.json']]
    manifest={p.name:dict(sha256=sha(p),bytes=p.stat().st_size) for p in files}
    dump(O/'payload_manifest.json',manifest)
    dest=O/'R06_名单重叠与DCLM频率_讨论包.zip'
    with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for p in files+[O/'payload_manifest.json']:z.write(p,p.name)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for name,item in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==item['sha256']
    for p,h in source_hashes.items():assert sha(p)==h,p
    dump(O/'package_receipt.json',dict(path=str(dest),bytes=dest.stat().st_size,sha256=sha(dest),sources_unchanged=True,new_forwards=0,new_tests=0,files=len(files)+1))
    print(json.dumps(dict(zip=str(dest),bytes=dest.stat().st_size,report=str(E/'读图说明_cn.md')),ensure_ascii=False))


def main():
    assert not (O/'all52_membership_frequency.csv').exists(), 'Do not overwrite an earlier supplement.'
    rows, hashes, frequency = build_rows()
    with (O/'all52_membership_frequency.csv').open('w', newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    dump(O/'all52_membership_frequency.json',rows)
    dump(O/'source_manifest.json',dict(kind='requested descriptive reading supplement',new_forwards=0,new_hypothesis_tests=0,candidate_reselection=False,source_sha256=hashes,
        reference_interface='R04 native E16FP32Top32 and A22joint14BF16 savedTRAINnorm/gate;frequenciesz>0,not layerlocalCC',
        plotting='One row/point is concept-feature-direction object;dictionary IDs separate;zero frequency censored only for plotting,rawcounts retained',
        evidence_scope='51far and10drop are original conditional/exploratory criteria,not independentconfirmation;frequency joins areposthocdescriptive'))
    overview(rows);all_objects(rows);frequency_plot(rows);report(rows);package(hashes)


if __name__=='__main__':main()
