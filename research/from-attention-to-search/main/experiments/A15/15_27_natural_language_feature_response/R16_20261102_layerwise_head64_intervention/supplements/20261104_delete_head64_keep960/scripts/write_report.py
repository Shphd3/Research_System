from pathlib import Path
import sys
import json,shutil
import pandas as pd
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);V=json.load(open(E/'audit/validation.json'));S=pd.read_csv(E/'analysis/summary_metrics.csv');C=pd.read_csv(E/'analysis/paired_contrasts.csv');J=pd.read_csv(E/'analysis/joint_patterns.csv');rr=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()]
if (E/'audit/manual_context_review.json').exists():
 print('Reviewed prose exists; keep it. Numeric regeneration is separate.');sys.exit(0)
def one(layer,scope,cond,metric,group='ALL',panel='natural'):
 return S[(S.panel==panel)&(S.layer==layer)&(S.scope==scope)&(S.condition==cond)&(S.metric==metric)&(S.group==group)].iloc[0]
def mean(*a,**kw):return one(*a,**kw)['mean']
def ci(*a,scale=1,**kw):
 r=one(*a,**kw);return f"{r['mean']*scale:.2f} [{r.ci_low*scale:.2f}, {r.ci_high*scale:.2f}]"
text=['# 删除头64、保留后960：与保留头64的配对对照\n','## 目的\n\n固定同一Qwen3-0.6B Base、文本、token位置和每层PCA，比较单层删除头64后正常运行剩余网络的最终预测，与旧保留头64条件逐位置对照。两个范围是仅当前位置与整个有效前缀。探索性面板，未训练或重拟合PCA。\n\n从行为与因素对照、表征的逐层组织、原生干预与可信度三条线阅读。先报告事实，再记录有边界的AI认识更新；研究者科学接受Unknown。\n','## 观察与关键数据\n\n本节先给实际曲线和原始汇总；机制阅读写入下方认识更新段落。\n\n![逐层相反操作](figures/01_keep_delete_layerwise.png)\n\n蓝线保留头64，橙线删除头64保留后960，灰线删除三个固定随机64维空间的平均。左右仅当前位置／整个前缀分别报告。彩色阴影按文档重采样95%逐点区间，灰带是随机种子范围。首选保持不是正确率；两种主操作保留维数不同。\n']
text.append('|层|仅当前：保留头64保持%|仅当前：删除头64保持%|整个前缀：保留头64保持%|整个前缀：删除头64保持%|仅当前：删除后真实目标损失|全前缀：删除后真实目标损失|\n|---|---:|---:|---:|---:|---:|---:|')
for l in range(1,29):text.append(f"|{l}|{100*mean(l,'target_only','keep_head64','top1_agreement'):.2f}|{100*mean(l,'target_only','delete_head64','top1_agreement'):.2f}|{100*mean(l,'all_prefix','keep_head64','top1_agreement'):.2f}|{100*mean(l,'all_prefix','delete_head64','top1_agreement'):.2f}|{mean(l,'target_only','delete_head64','NLL'):.4f}|{mean(l,'all_prefix','delete_head64','NLL'):.4f}|")
text.append('\n数据：175篇不同文档家族、700位置，每篇4位置。主指标先文档内平均再等权汇总；总体恰等于保持数/700，但区间仍以175文档为独立单位。NLL为真实后继负对数概率，单位nat，低为好；原模型2.3418nat。完整精度、文档与位置表在原始入口，未把同文档位置当独立文档。\n\n![词类分组](figures/03_recovery_by_original_type.png)\n\n词类按完整模型原首选固定：格式108位置/81篇，参考常见非格式386/163，其余非格式206/125；文档可出现在多个组。常见来自独立TRAIN频率，不代表粗语义；其余不代表细语义或上下文token。\n')
text.append('|层|范围|删除头64：格式保持%|删除头64：参考常见非格式保持%|删除头64：其余非格式保持%|\n|---|---|---:|---:|---:|')
for l in [1,7,14,21,28]:
 for sc,label in [('target_only','仅当前'),('all_prefix','全前缀')]:text.append(f"|{l}|{label}|{ci(l,sc,'delete_head64','top1_agreement','format',scale=100)}|{ci(l,sc,'delete_head64','top1_agreement','nonformat_common',scale=100)}|{ci(l,sc,'delete_head64','top1_agreement','nonformat_other',scale=100)}|")
text.append('\n![损失与能量](figures/02_loss_KL_energy.png)\n\n真实目标损失、与原输出分布的KL、实际保留的中心化能量分列，不能混成一个语义量。删除随机64与删除头64同样保留960维，但不匹配能量/范数；不能将头部特殊性全归于常见信息。\n\n![同位置四种情况](figures/04_joint_recovery_patterns.png)\n\n同位置配对后，两者均保持、仅保留时保持、仅删除时保持、两者均改变，四类合为100%。它们共享均值、其他位置和剩余网络，因此不能把四格比例叫独立信息量、功能交互或因果冗余。\n')
text.append('|层|范围|两者均保持%|仅保留时保持%|仅删除时保持%|两者均改变%|\n|---|---|---:|---:|---:|---:|')
for l in [1,7,14,21,28]:
 for sc,label in [('target_only','仅当前'),('all_prefix','全前缀')]:
  z=J[(J.panel=='natural')&(J.layer==l)&(J.scope==sc)&(J.group=='ALL')].set_index('pattern')['mean'];text.append(f"|{l}|{label}|{100*z['both']:.2f}|{100*z['keep_only']:.2f}|{100*z['delete_only']:.2f}|{100*z['neither']:.2f}|")
text.append('\n### 37篇固定读到the面板\n\n与自然面板分开，不用于重新选参数。\n\n|层|范围|删除头64保持%|保留头64保持%|删除后真实目标损失nat|\n|---|---|---:|---:|---:|')
for l in [1,7,14,21,28]:
 for sc,label in [('target_only','仅当前'),('all_prefix','全前缀')]:text.append(f"|{l}|{label}|{ci(l,sc,'delete_head64','top1_agreement',panel='the',scale=100)}|{ci(l,sc,'keep_head64','top1_agreement',panel='the',scale=100)}|{ci(l,sc,'delete_head64','NLL',panel='the')}|")
text.append('\n## 真实文本与原始候选\n\n[完整案例记录](casebook_cn.md)含全部28层的两个谱操作/两个范围，含9例原固定和另标结果后选。以下三例沿用旧面板位置。所有预测只能利用当前token及其前文。\n')
for i in [211,284,676]:
 m=rr[i];text.append(f"\n### {m['seq_id']}\n\n当前第{m['position']+1}个token（0基{m['position']}），ID{m['input_id']} {m['input_fragment']!r}。真实后继ID{m['target_id']} {m['target_fragment']!r}。完整可见前文：\n\n```text\n{m['visible_prefix']}\n```\n\n![实际候选](figures/05_case_{i:03d}.png)\n\n本例人工阅读待补；不根据片段自动定义语义层级。\n")
text.append('\n## 假设、认识更新与竞争解释\n\nAI认识更新待实际结果阅读后补充。预先假设头64可能体现跨输入复用的模式；PCA方差不直接证明发生频率，常见token也不等同常见表征模式。信息存储、经后续网络的可用性与外部语义粒度分开判断。\n\n## 具体做法与可信度\n\n精确复用R16权重/tokenizer与28套独立PCA，原训练参考60篇/9600位置；原评估175/700自然位置+37/the，共180篇物理文档。每次只改一层residual-post，范数前。删除公式h新=h−(h−训练均值)QQ转置；均值保留，后960维保留。每层四个删除条件、两个范围；随后原后续层/finalnorm/head。没有新PCA或分类器拟合。模型BF16、投影FP32再转BF16、概率FP32；不另做温度/范数校准。\n\n原生状态和旧输出重放、补空间代数、空删除恒等、完整hook/后缀与causal mask检查通过后才运行。最大并列取最小ID，前10边界也稳定处理；原修正词类不变。按文档落盘，源文件哈希冻结，Spot恢复只复用同冻结的完整文档。2000次文档配对重采样，区间为逐点探索性，随机种子不当独立语料。\n')
text.append(f"\n实际新增{V['new_records']}条记录，其中含737条原生基线；复用保留条件{V['reused_keep_records']}条，合计{V['combined_records']}条。全部28层目标表征重放最大差{V['identity_h28layer_max_abs']:.6g}；原模型NLL最大差{V['identity_NLL_max_abs']:.6g}；原首选变化{V['identity_top1_changes']}个；复用保留汇总最大差{V['keep64_summary_max_abs_error']:.6g}；最后层两个范围完全相同。\n")
text.append('\n## 边界\n\n保留64与保留960维数/能量不同；删除头64与删除随机64只匹配维数。全前缀额外改变许多位置、总扰动更大；当前位置高恢复可能来自后续补偿或其他状态。删除后输出改变不是参数知识被擦除，保持首选也不代表其他候选完整。参考仅原两域60篇，评估已暴露，不能推为所有语料/模型结论；不把频率分组冒称粗细语义。\n\n[协议](protocol_cn.md) · [配置](manifest.json) · [原始数据与复算](assets_and_data_cn.md) · [执行细节](detailed_cn.md)。研究者接受与闭题Unknown；没有自动扩大实验。\n')
for b in [P,E]:(b/'summary_cn.md').write_text('\n'.join(text)+'\n')
eng='''# Delete head64, retain960: paired native results

## Purpose
Use exactlytheR16Qwen3Base/model/text/tokenizer and28PCAmeans/bases tocontrast one-layercomplementdeletionwitholdhead64retention. Separate current-onlyandwhole-prefix scopes; unchangedremainingnetwork/finalnorm/head. No model/classifier/PCA fitting.

## Observations and key data
Primary175documents/700naturalpositions;aux37/the separate,180physicaldocuments. See[fullrawobservationsandfixedinputexamples](summary_cn.md),[casebook](casebook_cn.md),[machine-readablelayeroverview](evidence/layerwise_overview.csv). Tablebelow is equal-documentmeans;originalfullNLL2.3418nat.

|Layer|Currentonlykeep64%|Currentonlydelete64%|Wholeprefixkeep64%|Wholeprefixdelete64%|CurrentonlydeleteNLL|WholeprefixdeleteNLL|
|---|---:|---:|---:|---:|---:|---:|
'''
for l in [1,4,7,14,21,25,28]:eng+=f"|{l}|{100*mean(l,'target_only','keep_head64','top1_agreement'):.2f}|{100*mean(l,'target_only','delete_head64','top1_agreement'):.2f}|{100*mean(l,'all_prefix','keep_head64','top1_agreement'):.2f}|{100*mean(l,'all_prefix','delete_head64','top1_agreement'):.2f}|{mean(l,'target_only','delete_head64','NLL'):.4f}|{mean(l,'all_prefix','delete_head64','NLL'):.4f}|\n"
eng+='''
## Hypotheses and bounded interpretation
Commonrepresentationpatterns areaWORKINGHYPOTHESIS,not PCAdefinition. Sharedmean/context/suffix prevent independent-informationorinteraction claims fromjointrecoverycells. Currentanalysisdoesnot establishcoarse/fine semantics, intrinsiclayerimportance, orparameterknowledgeerasure. AIinterpretationfollowsmanualreading;researcheracceptanceUnknown.

## Procedure and validity
Deletionh'=h-(h-mu)QQTpreservesTRAINmean. Random64deletions use3exactoldseeds;sameretainedrank960not energy-matched. All28layernative states/identityoutputs replayedagainstR16;keep64 replaysbefore reuse; complementalgebra/zerodeletion/fullmodelhook-suffix/causalguards and lastlayerscopeequality required. Deterministicmaxtie=minID;stabletop10boundaryties.2000documentbootstrap,pointwise exploratoryintervals, no newselection/fitting. Fixed9examples withcompletevisibleinputs/currentID/zeroandonebasedpositions;outcome-selectedjointcellfirstUIDcasesseparately labeled.

## Boundary
ExposedEnglishpanels,narroworiginalTRAINreference;rank/energy/norm/remainingnetworkall matter. No automaticnext experiment,trainingorpublication. ExactresultsandresourcesremainowningSummary/Detailed/manifests.
'''
for b in [P,E]:(b/'summary.md').write_text(eng)
print('Factual bilingual draft written; manual readings must be completed')
