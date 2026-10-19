#!/usr/bin/env python3
"""Redraw two frozen CrossCoder results; never trains or changes graph data."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
R = E / 'analysis/relation_learning/20261015T164000Z'
DEFAULT_OUTPUT = E / 'analysis/report_spectrum/20261016_figures12'
DEFAULT_FONT = Path('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf')
COLORS = {'R': '#3264A0', 'F': '#D78230', 'N': '#338C66'}
LABELS = {'R': '关系', 'F': '频率', 'N': '匹配随机'}


def digest(path):
    return {'path': str(path), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def write_csv(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save(fig, out, stem):
    for ext in ('png', 'pdf'):
        fig.savefig(out / f'{stem}.{ext}', dpi=220, facecolor='white')
    plt.close(fig)


def run(out, font):
    out.mkdir(parents=True, exist_ok=True)
    font_manager.fontManager.addfont(str(font))
    plt.rcParams.update({
        'font.family': font_manager.FontProperties(fname=font).get_name(),
        'font.size': 17, 'axes.titlesize': 24, 'axes.labelsize': 19,
        'xtick.labelsize': 17, 'ytick.labelsize': 16, 'legend.fontsize': 15,
        'axes.spines.top': False, 'axes.spines.right': False,
        'figure.facecolor': 'white', 'axes.facecolor': 'white',
        'pdf.fonttype': 42, 'axes.unicode_minus': False,
    })
    summary_path = R / 'structure/full_repair_summary.json'
    controls_path = R / 'structure/full_group_controls.csv'
    metrics_path = R / 'analysis_outputs/learning_metrics.csv'
    summary = json.loads(summary_path.read_text())
    with controls_path.open(newline='') as f:
        controls = list(csv.DictReader(f))
    assert len(controls) == summary['groups'] == summary['qualified_groups'] == summary['strict_qualified_groups'] == 186
    assert all(r['qualified'] == 'True' and r['strict_qualified'] == 'True' for r in controls)
    observed = float(np.mean([float(r['observed_strict_SD']) for r in controls]))
    matched = float(np.mean([float(r['meanmatched_strict_SD']) for r in controls]))
    assert abs(observed - summary['observed_strict_SD_groupweighted']) < 1e-14
    assert abs(matched - summary['meanmatched_strict_SD_groupweighted']) < 1e-14
    assert round(observed, 9) == 0.353310533 and round(matched, 9) == 0.604781172
    write_csv(out / 'figure1_plot_data.csv', ['condition', 'groups', 'group_equal_log10_frequency_sd'], [
        {'condition': '关系组', 'groups': 186, 'group_equal_log10_frequency_sd': observed},
        {'condition': '匹配随机组', 'groups': 186, 'group_equal_log10_frequency_sd': matched},
    ])
    fig, ax = plt.subplots(figsize=(8.2, 6.2), layout='constrained')
    ax.bar([0, 1], [observed, matched], width=.56,
           color=[COLORS['R'], COLORS['N']], edgecolor='none')
    ax.set_xticks([0, 1], ['关系组', '匹配随机组'])
    ax.set_xlabel('组别', labelpad=13)
    ax.set_ylabel('log频率标准差', labelpad=11)
    ax.set_title('组内频率差异', pad=18)
    ax.set_ylim(0, .73)
    ax.set_yticks([0, .2, .4, .6])
    ax.yaxis.grid(True, color='#E7E7E7', linewidth=.7)
    ax.set_axisbelow(True)
    for x, y in enumerate([observed, matched]):
        ax.text(x, y+.018, f'{y:.9f}', ha='center', va='bottom', fontsize=16)
    save(fig, out, 'figure1_frequency_difference')

    with metrics_path.open(newline='') as f:
        metrics = list(csv.DictReader(f))
    assert len(metrics) == 54
    seeds = sorted({int(r['seed']) for r in metrics})
    assert seeds == [20261016, 20261017, 20261018]
    steps = sorted({int(r['step']) for r in metrics})
    assert steps == [0, 510, 1530, 3060, 4590, 6120]
    exposures = np.array(sorted({int(r['tokens_seen']) for r in metrics}))
    assert np.array_equal(exposures, np.array(steps) * 256)
    baseline_values = np.array([float(r['low_loss']) for r in metrics if int(r['step']) == 0])
    assert np.ptp(baseline_values) == 0
    baseline = float(baseline_values[0])
    write_csv(out / 'figure2_seed_plot_data.csv',
              ['arm', 'condition', 'seed', 'step', 'training_exposures', 'low_feature_conditional_loss_nat'], [
        {'arm': r['arm'], 'condition': LABELS[r['arm']], 'seed': r['seed'],
         'step': r['step'], 'training_exposures': r['tokens_seen'],
         'low_feature_conditional_loss_nat': r['low_loss']} for r in metrics])
    write_csv(out / 'overall_loss_table.csv',
              ['arm', 'condition', 'seed', 'step', 'training_exposures', 'overall_loss_nat'], [
        {'arm': r['arm'], 'condition': LABELS[r['arm']], 'seed': r['seed'],
         'step': r['step'], 'training_exposures': r['tokens_seen'],
         'overall_loss_nat': r['overall']} for r in metrics])
    fig, ax = plt.subplots(figsize=(9.4, 6.4), layout='constrained')
    mean_rows = []
    final_mean = {}
    for arm in ['R', 'F', 'N']:
        curves = []
        for seed in seeds:
            rows = sorted([r for r in metrics if r['arm'] == arm and int(r['seed']) == seed], key=lambda r: int(r['step']))
            assert len(rows) == len(exposures)
            assert np.array_equal([int(r['tokens_seen']) for r in rows], exposures)
            values = np.array([float(r['low_loss']) for r in rows])
            curves.append(values)
            ax.plot(exposures, values, color=COLORS[arm], linewidth=.9, alpha=.42, zorder=2)
        mean = np.mean(curves, axis=0)
        final_mean[arm] = float(mean[-1])
        ax.plot(exposures, mean, color=COLORS[arm], linewidth=3.1,
                label=LABELS[arm], zorder=3)
        mean_rows.extend({'arm': arm, 'condition': LABELS[arm],
                          'training_exposures': int(x), 'mean_low_feature_conditional_loss_nat': float(y),
                          'seeds': 3} for x, y in zip(exposures, mean))
    ax.axhline(baseline, color='#505050', linestyle='--', linewidth=1.8, label='原模型', zorder=1)
    ax.set_title('预测损失', pad=17)
    ax.set_xlabel('训练曝光', labelpad=12)
    ax.set_ylabel('损失（nat）', labelpad=12)
    ax.set_xlim(-30_000, 1_600_000)
    ax.set_ylim(2.35, 3.48)
    ax.set_xticks([0, 400_000, 800_000, 1_200_000, 1_600_000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '0' if x == 0 else f'{x / 1e4:g}万'))
    ax.yaxis.grid(True, color='#E7E7E7', linewidth=.7)
    ax.legend(loc='upper left', frameon=False, ncol=2)
    save(fig, out, 'figure2_prediction_loss')
    write_csv(out / 'figure2_mean_plot_data.csv', list(mean_rows[0]), mean_rows)

    captions = f'''# 图1：组内频率差异

1. 统计对象：固定发现侧 D 得到的全部 186 个非单元素关系组，以及逐组匹配的随机组；186 组均满足本次复核资格，未使用旧的 142 组合格子集。
2. 计算方法：对每组成员的验证侧 V 激活频率取 log10，计算总体标准差（ddof=0），再对组等权平均；随机组与对应关系组大小相同，D 侧平均 log10 频率相差不超过 0.1 dex，每组先对匹配抽样取均值，再对 186 组等权平均。
3. 实际观察：关系组为 {observed:.9f}，匹配随机组为 {matched:.9f}，前者小 {matched-observed:.9f}；图中只画两根柱，无误差条，柱高不是 186 组标准差的合并计算。
4. 推断边界：这说明当前关系分组的 V 侧组内频率更接近，但该匹配对照没有复刻 phi 选边及完整建图过程，因此不能排除 phi 对频率相近组合的选择偏好，也不能推出语义组合或共同学习收益；检验该替代解释需另看完整流程的固定边际命中数随机化结果。

来源：`{summary_path}`、`{controls_path}`；对应列 `observed_strict_SD` 和 `meanmatched_strict_SD`。

# 图2：预测损失

1. 统计对象：关系、频率、匹配随机三种已有分发下的 3 个配对种子，固定低频 feature 条件验证损失；细线是种子，粗线是算术均值，虚线是冻结原模型。
2. 计算方法：低频 feature 名单由 D 侧可靠 feature 频率最低四分之一预先确定（3916 个），仅估计固定学习评估缓存中至少命中 20 次的 3737 个；先对每个 feature 激活位置的真实下一个 token 交叉熵求均值，再对这 3737 个 feature 等权平均，横轴为累计有效预测目标曝光（最终 1,566,720），各 feature 可共享文本位置。
3. 实际观察：原模型为 {baseline:.6f} nat；最终关系、频率、匹配随机三组种子均值分别为 {final_mean['R']:.6f}、{final_mean['F']:.6f}、{final_mean['N']:.6f} nat，三者都高于原模型，本轮关系分发未显示预定的低频条件损失收益。
4. 推断边界：这里的“低频”修饰 D 侧 feature 的激活频率，并非输出 token 频率或知识准确率；结果限于已有冻结模型、终端适配器、分发和训练预算，不能据此否定所有同频学习方案。

来源：`{metrics_path}`；绘图读取 `low_loss`，总体损失单独保存在 `overall_loss_table.csv`，未混入此图。
'''
    (out / 'captions_cn.md').write_text(captions, encoding='utf-8')
    manifest = {
        'operation': 'Redraw existing frozen numerical results only; no training, no graph parameter change',
        'sources': [digest(p) for p in [summary_path, controls_path, metrics_path]],
        'script': digest(Path(__file__).resolve()), 'runtime_font_resource': digest(font),
        'font_is_not_bundled': True, 'style': {'white_background': True, 'palette': COLORS,
            'no_errorbars': True, 'figure1_group_equal': True, 'figure2_no_overall_loss': True},
        'validation': {'qualified_groups': len(controls), 'full_strict_qualification': True,
            'learning_rows': len(metrics), 'paired_seeds': seeds, 'updates': steps,
            'training_exposures': exposures.tolist(), 'initial_loss_identical': True,
            'original_model_low_loss': baseline, 'final_low_loss_seed_means': final_mean},
        'outputs': [digest(p) for p in sorted(out.iterdir()) if p.is_file() and p.name != 'source_manifest.json'],
    }
    (out / 'source_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'output': str(out), **manifest['validation']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--font', type=Path, default=DEFAULT_FONT)
    args = parser.parse_args()
    run(args.output_dir, args.font)
