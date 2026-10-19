#!/usr/bin/env python3
"""Assemble a derived reading supplement from frozen input-spectrum evidence."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import difflib
import hashlib
import json
import shutil

S = Path('/data/250010109/Research_System')
E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
B = E/'analysis/report_spectrum/20261016_phi_input_spectrum'
C = E/'analysis_tools/report_spectrum'
D = S/'daily_research_reports/1016/crosscoder_phi_input_spectrum'
OLD = S/'daily_research_reports/1016/crosscoder_report_supplement'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str,r))+' |' for r in rows])

def main():
    for sub in ('data','figures','provenance','code'):
        (D/sub).mkdir(parents=True, exist_ok=True)
    summary = json.loads((B/'phi_input_hidden_summary.json').read_text())
    assert summary['main_common_estimable_original_and_residual_groups'] == 145
    assert summary['sample_N_per_group'] == 128
    main_results = summary['main_population']
    for p in B.glob('*.csv'):
        shutil.copy2(p,D/'data'/p.name)
    for p in B.glob('*_input_hidden_spectra.npz'):
        shutil.copy2(p,D/'data'/p.name)
    for p in B.glob('*.json'):
        shutil.copy2(p,D/'provenance'/p.name)
    for p in (B/'audit').iterdir():
        if p.is_file():
            shutil.copy2(p,D/'provenance'/('audit_'+p.name))
    for p in (B/'figures').iterdir():
        if p.suffix in ('.png','.pdf'):
            shutil.copy2(p,D/'figures'/p.name)
        elif p.suffix == '.csv':
            shutil.copy2(p,D/'data'/p.name)
        elif p.suffix == '.json':
            shutil.copy2(p,D/'provenance'/p.name)
    shutil.copy2(B.parent/'20261016_phi_input_access.json',D/'provenance/input_access.json')
    for name in ('phi_input_hidden.py','plot_phi_input_hidden.py','phi_context_diagnostic.py','build_phi_delivery.py'):
        shutil.copy2(C/name,D/'code'/name)
    scorer = E/'analysis_tools/relation_learning/data_routes.py'
    shutil.copy2(scorer,D/'code/frozen_data_routes.py')
    values = table(['条件','原第一方向占比','剩余第一方向占比','剩余总方差均值'],[
        [c,f"{main_results[c]['first_share_original_mean']:.4%}",f"{main_results[c]['first_share_residual_mean']:.4%}",
         f"{main_results[c]['remaining_trace_mean']:.2f}"] for c in 'RFN'])
    coverage = table(['条件','支持≥128位置的组','不足组','成员覆盖'],[
        [c,f"{summary['conditions'][c]['sufficient_groups']}/186",
         summary['conditions'][c]['insufficient_groups'],
         f"{summary['coverage']['all_supported_per_condition'][c]['member_fraction']:.2%}"] for c in 'RFN'])
    populations = list(csv.DictReader((B/'population_summary.csv').open()))
    strata = table(['大小层','组数','R原／剩余','F原／剩余','N原／剩余'],[
        [label,next(r['groups'] for r in populations if r['population']=='main_RFN' and r['stratum']==key),
         *[next(f"{float(r['first_share_original_mean']):.2%}／{float(r['first_share_residual_mean']):.2%}" for r in populations if r['population']=='main_RFN' and r['stratum']==key and r['condition']==c) for c in 'RFN']]
        for key,label in [('small','小：2–3成员'),('medium','中：4–19成员'),('large','大：≥20成员')]])
    english_values = values.replace('条件','Condition').replace('原第一方向占比','Original leading share').replace('剩余第一方向占比','Residual leading share').replace('剩余总方差均值','Mean residual trace')
    english_strata = strata.replace('大小层','Group size').replace('组数','Groups').replace('原／剩余','original / residual').replace('小：2–3成员','Small: 2–3').replace('中：4–19成员','Medium: 4–19').replace('大：≥20成员','Large: 20+')
    report = f"""# φ关系组对应输入的原始表征谱

本次沿用冻结的186个φ关系组及原学习实验的R/F/N胜组规则，读取同一EVAL512缓存中的真实第28层hidden。**在三条件共同支持的145组中，R的原第一方向及剩余第一方向占比均值都低于F和N；差异仍存在于各组最大方向之外，但并非每组、每种组大小都如此。** 这只描述规则选择出的输入集合，不证明φ因果、容量或学习收益。

{values}

表中各组等权。原指标是λ₁/Σλ，剩余指标是λ₂/Σₖ≥₂λₖ，分母不同，不能把两项差值直接解释成某种机制的“解释百分比”。剩余总方差是每组去掉最大分量后方差之和的等权均值，单位为原模型hidden坐标的平方；它也不是容量。

## 原组如何选择输入

R是原φ关系组；F将同一13,807个feature按D频率排序，沿R的大小序列切段；N在D频率的10个等人数档内随机交换R组标签，逐组保留大小及频率档构成。三者各186组、逐组大小相同（2–735）；**它们不是此前固定14成员的同频／混频组。**

在每个位置，计算“激活成员数÷完整组大小”，用原保存D均值与标准差标准化，只让有成员激活的组竞争，最高分组获胜，并列按成员集合SHA固定顺序处理。即使最高分为负仍有胜组；无命中位置不借4专家回退标签伪造组。本次直接复用原评分函数和route maps，三条件所有523,136位置的重建四专家路由与缓存完全一致；另33个真实位置×3条件的99次独立胜组核对通过。谱在186组层面计算，不压成4专家，不改用任一成员激活。

每组固定取128个胜出位置，无放回、确定性伪随机抽样，位置名单不依hidden或谱。三条件都读取原学习EVAL512：512个context、523,136个位置、同一源文件；raw hidden是第28个block输出、最终RMSNorm之前的residual-post，BF16保存、FP64中心化求谱。该文件来自原CrossCoder TRAIN来源，区别于结构D/V的V；不是新独立文档确认。详细定义见[计算口径](methods_cn.md)和[冻结配置](provenance/frozen_config.json)。

## 支持与覆盖

{coverage}

主图使用三者共同支持且原/剩余方差均可估的145个组ID，每条线组数相同、组大小序列完全相同。覆盖145/186=77.96%的组、8,814/13,807=63.84%的成员；不能代表完整186组。全部558条组记录保留，支持不足记NA而非0；支持组的原和剩余零方差数量均为0。

N缺失的15组中有13个大组，涉及4,876个成员，另外2个小组涉及6个成员。这些大组在原胜组竞争下输入不足，不能降低样本数或换成任一成员命中补齐。R/N共同支持161组的补充仍只覆盖64.07%的成员，不能解决这一成员缺口。[完整支持表](data/per_group_winner_support.csv)和[逐组指标／缺失表](data/per_group_input_hidden_metrics.csv)可直接定位每个组。

## 原始协方差谱

以下四图均固定模型层28、每组128个位置、每条件145个有效组。按位置减去每组hidden均值，计算协方差特征值，逐组除以总方差，再对组等权平均。

![原始归一化谱](figures/figure7_phi_raw_spectrum.png)

**统计对象：** 三种胜组规则选择的输入，在真实第28层hidden中呈现的中心化协方差谱。  
**计算方法：** 每组128×1024原始hidden中心化，计算λⱼ/Σλ，再对共同145组等权平均；图展示127个可估方向，其余为样本秩限制。  
**实际观察：** 三条曲线总体接近，首方向均值R12.53%、F13.14%、N14.05%，R在首方向外的部分方向占比稍高，曲线并非处处有相同排序。  
**推断边界：** 能描述这些输入集合的方差集中程度，不能把曲线差异直接归因为φ、频率或模型容量。

[图7 PDF](figures/figure7_phi_raw_spectrum.pdf) · [全部1024方向作图数据](data/phi_input_normalized_spectrum_plot_data.csv)

![原第一方向占比分布](figures/figure8_phi_raw_first_share.png)

**统计对象：** 共同145个组ID在R/F/N下的原第一方向方差占比分布。  
**计算方法：** 每个浅色点是一组λ₁/Σλ，箱体为四分位范围、黑线为中位数、须为1.5倍四分位距范围内的点，菱形为组等权均值，所有离群点仍以散点显示。  
**实际观察：** R的均值最低但分布广泛重叠，R比N低的为85/145组，比F低的为78/145组，个别R组仍高度集中。  
**推断边界：** 不能把均值排序写成逐组优势或显著性结论；组不是独立文档重复。

[图8 PDF](figures/figure8_phi_raw_first_share.pdf) · [全部组点](data/phi_input_first_direction_plot_data.csv)

## 每组去掉第一主方向后的剩余谱

对每组自己的中心化hidden做SVD，减去完整第一分量σ₁u₁v₁ᵀ。剩余谱沿原λ₂、λ₃等重新排序，并除以剩余总方差；不是删除全局未中心化hidden的第一奇异方向，也不把第一方向称为common feature。两种计算使用相同128位置，去首方向后不重选样本。

![剩余归一化谱](figures/figure9_phi_residual_spectrum.png)

**统计对象：** 同一组输入在删除该组自身中心化第一主方向后的剩余hidden变化。  
**计算方法：** 原谱去掉λ₁后，按Σₖ≥₂λₖ重新归一化，逐组处理后等权平均；此处方向1对应原协方差方向2，最多126个可估方向。  
**实际观察：** 剩余第一方向均值R8.57%、F9.09%、N9.34%，R在这一指标上仍较低；三条剩余曲线仍很接近。  
**推断边界：** 差异并未仅局限于各自最大方向，但不能说已排除一个全局共同方向或认定某个feature导致差异。

[图9 PDF](figures/figure9_phi_residual_spectrum.pdf)

![剩余第一方向占比分布](figures/figure10_phi_residual_first_share.png)

**统计对象：** 删除各组第一主方向后，剩余方差中最大方向占比的逐组分布。  
**计算方法：** 每组计算λ₂/Σₖ≥₂λₖ，使用与图8完全相同的组和散点／箱体／均值定义；两张分布图纵轴范围相同。  
**实际观察：** R比N低的组增加为90/145，但仍有55组相反；R比F低的为74/145，接近各半，不能由平均差推出统一性质。  
**推断边界：** 该归一化指标比较最大方向之外的集中程度，不是可学习容量、语义多样性或专家学习收益；个别组的比值也不保证在去首方向后下降。

[图10 PDF](figures/figure10_phi_residual_first_share.pdf)

## 组大小、频率与上下文会改变怎样的解释

{strata}

**整体均值没有给出统一的组大小规律。** 中等组中R原谱比N更集中，删除首方向后差仅约−0.10个百分点；中等组的R原谱及剩余谱都比F集中。大组的剩余R与F几乎相同，而R与N仍有约−1.36个百分点差异。[按大小分层与配对差值](data/paired_group_contrasts.csv)保留相反方向，不能把整体排序归纳成“所有关系组更分散”。

主145组的“组内成员log₁₀D频率均值再对组等权平均”为R−2.2048、F−1.1732、N−2.2253。F的组平均频率分布与R明显不同；N保留频率档构成也不等于档内连续频率完全相同。[成员及频率表](data/group_members.csv)和[分人口汇总](data/population_summary.csv)给出原值，不能作频率异质性的单变量因果识别。

每组抽样涉及的context数中位数R106、F105、N103；单context最大位置占比的全组最大值为R32.03%、F7.81%、N14.06%。例如R组135的128个位置有41个来自同一context。因此相邻文本与重复上下文可能影响谱，单纯令样本数相同没有控制它们。

结果后附加的描述性诊断，仅保留三种条件中单context占比均不超过10%的共同136组，不改变主结果或样本。其原第一占比R12.55%／F13.17%／N14.03%，剩余占比R8.55%／F9.11%／N9.23%，平均排序保留。这说明观察排序不只局限于被剔出的9个强重复组，**不等于已经排除文本组成或文档重复**。[诊断口径](provenance/context_diagnostic_spec.json) · [诊断原值及描述性相关](provenance/context_diagnostic_result.json)。

主图每条件18,560个位置在该条件内互不重复，但各组可以共享context；R/F抽样位置重合644个，R/N重合679个。[上下文位置构成](data/sample_context_coverage.csv)及[位置重合记录](provenance/position_overlap_diagnostics.json)保留这些依赖，未将组或位置当独立重复计算p值。

## 这次认识更新到哪里

本次把“原φ分组在原分配规则下对应哪些输入”落实到真实hidden，而不是用频率组替代关系组或用decoder贡献替代模型表征。在共同支持的145组中，R相对频率档匹配N的平均集中程度差异，在删除各自第一主方向后仍存在；但方向依组大小和具体组而变，且完整成员覆盖有实质缺口。

R/N共同161组的补充也给出同方向平均结果：原R12.29%／N14.25%，剩余R8.54%／N9.43%。各条件全部支持组的均值另附，因人口不同不替代主匹配比较。这些结果缩小了“差异是否仅在第一方向”的不确定性，**没有建立φ、频率到学习相容或容量的因果桥梁**。研究者对机制和下一步决策的判断仍为Unknown。

全部计算无新训练、无模型前向、无decoder加载、无建图参数或组成员修改。独立审计复核了515个支持组的哈希抽样、145/161人口、残谱删除首特征值、真实hidden直接SVD及来源边界；[审计证据](provenance/audit_result_audit.json)和[数值资格](provenance/numerical_qualification.json)可追溯。4张PNG均已实际查看，4图仅用小型派生数据重绘后逐字节一致；PDF已生成但未单独渲染检查。
"""
    (D/'report_cn.md').write_text(report)
    english = f"""# Raw representation spectra of inputs selected by the frozen φ groups

This supplement reuses the original 186 φ groups and the original learning R/F/N winner rules. It reads genuine cached block-28 hidden, before final RMSNorm. No decoder contribution, training, new forward, regrouping, or graph changes are involved.

Within the common supported population of 145 group IDs, R has a lower mean original leading variance share and a lower mean residual leading share than F and N. The distributions overlap and the ordering is heterogeneous across group sizes. This is a descriptive property of the selected input sets, not a causal φ effect, capacity estimate, or learning benefit.

{english_values}

The columns above respectively mean original leading share, residual leading share after each group's own centered PC1 is removed, and mean remaining total variance. Values are group-equal. Original and residual shares have different denominators, so their difference is not an explained-effect fraction.

## Selection and population

R is the original φ partition. F sorts the same 13,807 features by discovery frequency and fills R's group-size sequence. N permutes R labels within ten discovery-frequency bins, exactly preserving per-group bin counts and sizes. All conditions contain 186 groups, sizes 2–735. These are not the later fixed-size-14 same/mixed-frequency groups.

The original score standardizes each group's binary active-member fraction using saved D mean and standard deviation. Only hit groups compete; a negative maximum still wins. Saved member-hash order breaks ties. No-hit positions receive no group, regardless of the downstream four-expert fallback. Reconstructed expert routes match every cached position; 33 actual positions across three conditions also pass 99 independent row-wise group-winner checks. Spectra use the 186-way group winners, not four experts and not any-member hits.

All conditions use the same EVAL512 source, 523,136 eligible positions and 512 contexts. The file is from original CrossCoder TRAIN provenance, not structural validation V or a new independent-document confirmation. Each supported group samples exactly 128 winning positions without replacement using frozen deterministic priorities independent of hidden and spectra.

R/F/N support respectively 176/168/171 groups; 10/18/15 groups remain explicitly insufficient. The primary common 145 group IDs preserve the same group-size sequence and cover 8,814/13,807 members (63.84%). The R/N supplement includes 161 groups but only 64.07% of members. Missing support in N is concentrated in large groups. No estimable group has zero original or residual variance.

## Figures

All four figures use block 28, N=128 per group, and 145 groups per condition.

![Original normalized spectrum](figures/figure7_phi_raw_spectrum.png)

Object: covariance of genuine hidden at group-winning positions. Computation: center across positions, normalize each group's eigenvalues by its own trace, then average groups equally. Observation: first shares are R12.53%, F13.14%, N14.05%; curves are close and not uniformly ordered. Boundary: input-set variance organization, not frequency causation or capacity. The displayed 127 directions are a sample-rank limit.

![Original leading share distribution](figures/figure8_phi_raw_first_share.png)

Object: per-group original leading share. Computation: all points are shown; boxes are IQR, black lines medians, whiskers span points within 1.5 IQR, and diamonds equal-group means. Observation: R is lower than N in 85/145 groups and lower than F in 78/145, with broad overlap. Boundary: an average ordering is neither universal advantage nor independent-document statistical significance.

![Residual normalized spectrum](figures/figure9_phi_residual_spectrum.png)

Object: hidden variation outside each group's own first centered principal direction. Computation: remove the full rank-one SVD component and renormalize λ₂,λ₃,… by remaining variance. Observation: residual first shares are R8.57%, F9.09%, N9.34%. Boundary: this is not removal of one global uncentered direction, nor identification of a common feature; at most 126 sample directions remain.

![Residual leading share distribution](figures/figure10_phi_residual_first_share.png)

Object: group-wise residual leading shares. Computation: λ₂ divided by remaining trace, using unchanged positions and group IDs. Observation: R is lower than N in 90/145 groups, but 55 go the other way; R/F counts are 74/71. Boundary: residual concentration does not measure semantic diversity, capacity, or learning compatibility; renormalization need not lower every group's ratio.

## Heterogeneity and source limitations

{english_strata}

Rows are small (2–3), medium (4–19), and large (20+) groups; each condition cell gives original/residual shares. Medium groups reverse the original R/N average ordering, and R is more concentrated than F in both states. Large-group residual R/F means are nearly equal. A universal group-size claim is unsupported.

Mean member log10 D frequency, averaged equally across the main groups, is R−2.2048, F−1.1732, N−2.2253. F differs materially in group-average frequency; N's bin matching does not exactly match continuous frequency. Median selected-context counts are 106/105/103; maximum single-context shares are 32.03%/7.81%/14.06%. Same-condition selected positions are disjoint, but contexts and cross-condition positions can overlap.

A clearly post-outcome descriptive check retains 136 common group IDs whose maximum single-context share is at most 10% in every condition, without changing any samples. Original shares are R12.55%/F13.17%/N14.03%; residual shares are R8.55%/F9.11%/N9.23%. The average ordering persists outside the nine excluded groups; text-composition and document-repetition explanations remain unresolved.

The R/N intersection of 161 groups also yields original means 12.29%/14.25% and residual means 8.54%/9.43%. All-supported condition-specific results are retained separately, without substituting differently covered populations for the main comparison.

See [methods](methods.md), [complete metrics and missingness](data/per_group_input_hidden_metrics.csv), [population tables](data/population_summary.csv), [paired size strata](data/paired_group_contrasts.csv), [frozen configuration](provenance/frozen_config.json), and [independent audit](provenance/audit_result_audit.json). Four PNGs were viewed and independently replotted byte-identically; PDFs were generated but not independently rendered. Researcher-owned mechanism judgment and question closure remain Unknown.
"""
    (D/'report.md').write_text(english)
    (D/'README_cn.md').write_text("""# φ关系组输入谱补充

先读[中文报告和四图](report_cn.md)；定义与所有边界见[计算口径](methods_cn.md)。[English](report.md) · [英文方法](methods.md)。

R是冻结186个φ组，F/N是原学习实验的对照，按原胜组规则取真实hidden。主图为共同支持145组、每组128位置，另外保留186组全记录及R/N共同161组。四图各有PNG/PDF；每组谱、位置ID、逐组支持及上下文表、冻结配置、数值资格、审计和代码均保留。

重画四图只需NumPy、Matplotlib和已有中文字体，从本目录运行：

~~~bash
python code/plot_phi_input_hidden.py --root data --selection provenance/plot_selection.json --out /tmp/phi-input-spectrum-replot
~~~

此命令不读取模型、decoder或原始缓存。[独立重绘证据](provenance/replot_verification.json)验证4张PNG逐字节一致。完整统计重算脚本仍需要冻结的执行侧真实hidden缓存和原评分源码，不把已保存谱冒充新计算。

完整抽样位置及逐组原/余特征值在data下三份NPZ；跨全部523,136位置的胜组标签只留执行侧。模型、缓存、字体及日志不进入报告。支持不足直接记NA，原/余方差为零也不会记为0占比。
""")
    (D/'data_dictionary_cn.md').write_text("""# 数据与来源

主要组统计由执行侧phi_input_hidden.py产生，作图CSV由plot_phi_input_hidden.py产生，结果后上下文诊断由phi_context_diagnostic.py复算。统计来源由provenance/frozen_config.json冻结；provenance/cache_identity_check.json是本轮完整字节SHA校验，input_access.json是本轮严格访问检查。

| 文件 | 内容及口径 |
| --- | --- |
| data/group_members.csv | R/F/N全部41,421条成员行；每条件13,807成员，每行带n_D、N_D、p_D。 |
| data/per_group_winner_support.csv | 全558组条件行；未采样前胜出位置、context和原D胜出数，包含零支持。 |
| data/per_group_input_hidden_metrics.csv | 全558行的抽样数、状态、频率、context、原方差、删去方差、剩余方差及两占比；空值为明确不可估。 |
| data/population_summary.csv | 主145组、R/N161组、按大小分层和每条件全部支持组的等权汇总；人口不同不能混为同一比较。 |
| data/paired_group_contrasts.csv | 同组ID大小匹配的R-F/R-N差值和方向计数，差值并非相同文本上的干预效应。 |
| data/sample_context_coverage.csv | 实际抽样位置的context构成，context不是已验证独立文档。 |
| data/phi_input_normalized_spectrum_plot_data.csv | 原/余全部1024方向的组等权平均占比，以及哪些方向画出。 |
| data/phi_input_first_direction_plot_data.csv | 主145组的逐组原/余第一占比。 |
| data/R_input_hidden_spectra.npz等三文件 | 全186组的抽样行/绝对位置ID、原/余特征值及归一化谱、各条件支持和可估标记；不足行保留NA，不含原始hidden或decoder。 |
| provenance/plot_selection.json | 主145组及R/N161组的共同支持/可估名单，原谱与剩余谱使用同一名单。 |

计算代码和原评分源码副本在code；代码默认执行路径依赖真实缓存，作图通过显式参数可只读报告内小数据。主score/分组、位置抽样、中心化和删首分量均已独立复核，详见provenance中audit文件。数值资格只是计算核验，不是科学批准。
""")
    source_manifest = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'execution_root': str(B), 'report_root': str(D),
        'inputs': [
            {'path':str(B/n),'sha256':sha(B/n)} for n in [
                'frozen_config.json','phi_input_hidden_summary.json','support_only_summary.json',
                'cache_identity_check.json','plot_selection.json','audit/result_audit.json']],
        'source_code': [{'path':str(C/n),'sha256':sha(C/n)} for n in ['phi_input_hidden.py','plot_phi_input_hidden.py','phi_context_diagnostic.py']],
        'selected_evidence_payloads': 'four PNG/PDF pairs; three small derived NPZ containing spectra and sampling IDs; CSV tables, no hidden matrices or model weights',
        'new_training_updates':0, 'new_model_forwards':0, 'graph_changes':0,
        'scientific_approval':'Unknown', 'question_closure':'Unknown',
    }
    (D/'provenance/source_manifest.json').write_text(json.dumps(source_manifest,indent=2)+'\n')
    marker = '**追加：原φ关系组对应输入的原始表征谱。**'
    p = OLD/'report_cn.md'
    body = p.read_text()
    if marker not in body:
        body += '\n'+marker+' 已沿用原R/F/N胜组定义完成原谱与逐组去第一主方向后的剩余谱；主比较145个共同支持组，每组128位置，覆盖63.84%成员。[四图、覆盖缺口与分析](../crosscoder_phi_input_spectrum/report_cn.md)。这与上文固定14成员组的谱分析是不同对象。\n'
        p.write_text(body)
    changes = OLD/'modification_list_cn.md'
    if marker not in changes.read_text():
        with changes.open('a') as f:
            f.write('\n## 后续追加\n\n'+marker+' 仅在原补充报告末尾增加一段入口，链接本次原186组R/F/N的独立四图补充。未删除、改写或重排已有标题和段落，未将旧14成员谱替换为φ组谱；全定义、指标及缺口只在新补充中维护。\n')
    original = (OLD/'sources/user_report_transcription_cn.md').read_text()
    (OLD/'source_diff.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True),body.splitlines(True),
        fromfile='sources/user_report_transcription_cn.md',tofile='report_cn.md')))
    print(json.dumps({'report':str(D/'report_cn.md'),'groups':145,'figures':4,'files':len(list(D.rglob('*')))},ensure_ascii=False))

if __name__ == '__main__':
    main()
