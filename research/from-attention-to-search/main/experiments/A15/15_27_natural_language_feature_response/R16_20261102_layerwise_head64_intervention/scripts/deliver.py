from pathlib import Path
import json,hashlib,shutil,datetime
import pandas as pd,numpy as np
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);S=pd.read_csv(E/'analysis/summary_metrics.csv');A=pd.read_csv(E/'analysis/position_metrics.csv');V=json.load(open(E/'audit/validation.json'));cov=pd.read_csv(E/'analysis/group_coverage.csv');pc=pd.read_csv(E/'analysis/PCA_and_identity.csv');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def pick(panel,layer,scope,metric,group='ALL',cond='head64',readout='continuation'):
 return S[(S.panel==panel)&(S.layer==layer)&(S.scope==scope)&(S.metric==metric)&(S.group==group)&(S.condition==cond)&(S.readout==readout)].iloc[0]
def val(*args,percent=False,**kwargs):
 r=pick(*args,**kwargs);f=100 if percent else 1;return f"{r['mean']*f:.2f} [{r.ci_low*f:.2f}, {r.ci_high*f:.2f}]"
base=S[(S.panel=='natural')&(S.condition=='identity')&(S.group=='ALL')&(S.metric=='NLL')]['mean'].iloc[0]
cn=['# 逐层只保留前64主成分：最终预测保持与改变\n', '## 目的\n\n固定Qwen3-0.6B Base及R13自然175篇/700位置，逐层单独去除中心化表征的其余960个方向，只保留该层自己参考PCA的前64维，然后继续原有剩余网络。主测量是最终概率最高token的ID是否保持，不是原文预测正确率，也不是层的独立重要性。\n\n本报告沿三条线呈现：行为与因素对照；表征的逐层谱与能量；原生输出干预及数值可信度。先展示观察，机制与科学接受待研究者阅读。\n', '## 观察与关键数据\n\n![逐层首选保持](figures/01_layerwise_top1_preservation.png)\n\n图测量每个原首选类别在单层头64干预后，最终首选仍为原ID的比例。每篇先在该类位置内平均，再对含该类的文档等权；阴影为文档重采样逐点95%区间。左右分别为全前缀和仅当前目标位置，不能混成一条曲线。图提供深度响应描述，不能单独排除能量变化或后续补偿。\n']
cn.append('|原首选类别|自然位置数|独立文档数|\n|---|---:|---:|')
for r in cov[cov.panel=='natural'].itertuples():cn.append(f'|{r.group}|{r.positions}|{r.documents}|')
cn.append('\n下表是同一自然面板的原始汇总摘录，百分数及文档95%区间：\n\n|干预层|范围|空白/标点保持%|参考常见非格式保持%|其余非格式保持%|真实后继NLL，nat|\n|---|---|---:|---:|---:|---:|')
for l in [1,4,7,10,14,18,21,24,28]:
 for scope,lab in [('all_prefix','全前缀'),('target_only','仅目标')]:cn.append(f"|{l}|{lab}|{val('natural',l,scope,'top1_agreement','format',percent=True)}|{val('natural',l,scope,'top1_agreement','nonformat_common',percent=True)}|{val('natural',l,scope,'top1_agreement','nonformat_other',percent=True)}|{val('natural',l,scope,'NLL')}|")
cn.append(f'\n完整模型真实后继NLL为{base:.4f} nat。不是所有原首选都等于原文后继，首选保持与目标NLL必须分开读。\n\n![损失和能量](figures/02_layerwise_loss_and_energy.png)\n\n上排是真实后继负对数概率，越低越好；下排是中心化表征平方范数保留比例。灰线/带是三个随机64维种子的均值/范围，不是文档置信区间。两排没有混用单位。相同64维仍未匹配扰动能量，因此不据此将变化归因于纯谱位置。前缀总体扰动和相对范数另存逐位置表。\n')
cn.append('### 与旧最后层结果的关系\n\n28层主实验均在同一60篇参考文本上重新原生前向、独立拟合各层均值/PCA。旧R13最后层均值和谱另列legacy_head64，不能和新基底混为同一数值复现。最后层没有后续注意力层，因此当前目标的全前缀/仅目标条件应一致；代码对每篇每个最后层条件断言logits完全相同。\n')
for cond in ['head64','legacy_head64']:cn.append(f"- 自然面板最后层{cond}：首选保持{val('natural',28,'all_prefix','top1_agreement',cond=cond,percent=True)}%；NLL {val('natural',28,'all_prefix','NLL',cond=cond)}。")
cn.append(f"\n旧谱重放737位置：与R13目标NLL最大差{V['legacy_max_NLL_diff']:.6g} nat；首选变化{V['legacy_top1_differences']}个。当前无干预与旧记录首选差异{len(V['baseline_top1_differences'])}个，详情保留审计。\n")
cn.append('### 37篇读到the后的固定位置对照\n\n与700自然位置分别报告，不混合平均。格式类只有1篇，不能当成有稳定组间曲线。\n\n|层|范围|全组首选保持%|真实后继NLL，nat|\n|---|---|---:|---:|')
for l in [1,7,14,21,28]:
 for scope,lab in [('all_prefix','全前缀'),('target_only','仅目标')]:cn.append(f"|{l}|{lab}|{val('the',l,scope,'top1_agreement',percent=True)}|{val('the',l,scope,'NLL')}|")
cn.append('\n### 真实输入和改变后的实际token\n\n[固定及另标后选案例的完整前文/逐层输出](casebook_cn.md)保留当前tokenID、0基/1基位置、真实后继、原模型前10及28层的前3候选。主卡对若干层展示继续原网络和直接输出头诊断；完整28层和所有逐位置前10仍可复算。\n')
rr=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()]
for i in c['fixed_cases']:
 r=rr[i]
 if r['seq_id'] in ['R11_A02_134','R11_A02_242','R11_A02_434']:
  cn.append(f"\n#### {r['seq_id']}：第{r['position']+1}个token\n\n当前ID{r['input_id']} {r['input_fragment']!r}，真实后继ID{r['target_id']} {r['target_fragment']!r}。完整可见输入：\n\n```text\n{r['visible_prefix']}\n```\n\n![逐层实际候选](figures/03_case_{i:03d}.png)\n\n本卡实际变化的人工阅读见本轮附加说明；不能从这一例命名普遍语义层级。\n")
cn.append('## 假设与竞争解释\n\n本轮不预设浅粗深细。可观察的只是冻结三类原首选在逐层压缩后的保持差异。常见类可能包含数字、子词和数学符号；其余非格式不是外部语义细类。后续网络补偿、参考位置分布、剩余能量、随机投影尺度和来源模板都仍是竞争解释。直接输出头的未投影/投影中间层读出是诊断，不能单凭怪词说该层没有语义，也不能据它排名真实生成能力。\n\n## 具体做法\n\n同一模型权重、tokenizer和R13固定192token窗口，固定形状1x256并mask有效192；causal attention保证每位置只能读前文。每层残差block输出，norm之前；其自身60篇R04发现文本第33至192个token共9600位置拟合中心化FP64 PCA。只拟合统计量，不训练模型、分类器或lens。参考文本和评估按文档家族/精确token窗口核对不重合；训练侧不等于预训练未见。\n\n投影是训练均值加中心化向量在64列正交方向上的投影，BF16原生激活，FP32干预，FP32logsoftmax。全前缀改所有有效前文位置；仅目标每位置单独复制序列，只改一个位置。缓存未改的层状态后只运行后缀，先与完整模型实际hook校验。无干预/完整1024维校验、每层均值和三固定随机64维参照，以及旧末层谱均保留。\n\n参考常见使用原4,194,304个TRAIN token频率，151651有效ID的前1516个，按计数降序/ID升序；边界计数275，必须按原集合而不是仅计数判断成员。格式优先：解码后全是Unicode空白或标点P类。特殊ID另列。保留旧阈值/频率分组，不从评估定义common。\n\n## 边界\n\n早层投影后最终预测变化小，既可能表示保留信号够用，也可能是剩余网络补偿；不证明该层独自有完整信息。反之大变化也可能来自更大扰动或较少剩余修复机会。主实验将其余960维删去，未单独回答删除头64的必要性。全前缀还同时改变随后层可用的前文注意力状态；与仅目标的差异可定位范围效应，不能独自识别补偿机制。\n\n评估已暴露，文档有限；区间为逐点探索性95%，不支持挑最极端层后宣布唯一最重要层。参考只含原60篇两域文本，且拟合位置32..191，前缀更早位置受分布外投影；主结果不能冒称广泛语料普遍规律。全维实现一致不等于机制证据。\n\n[精确协议](protocol.md) · [输入/资产清单](manifest.json) · [执行记录](detailed_cn.md) · [完整原始输出入口](assets_and_data_cn.md) · [附录均值/随机参照](figures/A01_classwise_controls.png)。科学机制判断、研究者接受和闭题仍Unknown。本轮不自动扩大实验。\n')
eng=f'''# Layerwise head64 intervention: observations

## Purpose
Measure final native next-token preservation after a SINGLE Qwen3-0.6B-Base block residual-post is replaced by its TRAIN mean plus centered top64 PCA projection, followed by the unchanged suffix. This is intervention sensitivity, not intrinsic layer importance. No shallow/coarse or deep/fine order is assumed.

## Observations and key data
Natural panel175documents/700positions; separate37document/the panel. Independent layer-specific PCA uses the same60R04discovery documents/9600positions for every layer, no evaluation fit. Detailed complete values and original inputs are in [Chinese Summary](summary_cn.md), [casebook](casebook_cn.md), [raw evidence](assets_and_data.md). Original full NLL={base:.6f}nat. Old last-layer basis remains separately labeled legacy_head64. Raw records={V['raw_records']}; identity guard passes all28layers. Full original-top1 reference mismatches={len(V['baseline_top1_differences'])}, legacy top1 differences={V['legacy_top1_differences']}; maximum old-basis NLL replay error={V['legacy_max_NLL_diff']:.6g}nat.

## Hypotheses
No direction is presupposed. Same-rank random spaces, mean-only and scope controls distinguish descriptive effects, while energy, source and downstream compensation remain rivals. Common/other ID classes are not semantic granularity.

## Method
Single-layer all-prefix and independently replicated target-only interventions; frozen native norm/head and remaining network. Direct middle-layer head reading includes both raw and projected states, diagnostic only. Record full top1 probability/rank, actual successor NLL/probability/rank, KL(full||condition), native top10, centered energy and perturbation norms. Document means then equal-document aggregation;2000seed20261105 percentile bootstraps. Three random seeds are controls, not independent corpora. Fixed cases selected before new outcomes; outcome-selected examples labeled separately.

## Boundary
Exposed English windows, same narrow reference cohort and checkpoint. Equal rank is not matched energy. Early preservation could reflect sufficient retained signal or downstream compensation; standalone full information is not proven. No layer importance or semantic hierarchy judgment is promoted. Scientific acceptance/closure Unknown, no further experiment automatically authorized.
'''
for b in [P,E]:
 (b/'summary_cn.md').write_text('\n'.join(cn)+'\n');(b/'summary.md').write_text(eng)
 guide=f'''# Actual assets and recomputation

Execution root: {E}
Model/checkpoint/tokenizer/input IDs and hashes: manifest.json; original mainline:R13; no Dense/R15 cohort mixing.
Raw per-position candidate records: {E}/analysis/raw_outputs.jsonl (all conditions native top10 IDs/probabilities).
Metrics: {E}/analysis/position_metrics.csv; document_metrics.csv; summary_metrics.csv; scope_contrasts.csv; group_coverage.csv; head64_token_transitions.csv; legacy_replay.csv; PCA_and_identity.csv.
Reference: data/reference_documents.jsonl (60docs), data/reference_cache/*.npy (native residual activations); data/bases/layer01..28.npz (means/full eigensystems); data/random1031..1033.npy. Evaluation: data/evaluation_documents.jsonl; data/positions.jsonl exact737current+successor IDs/fullvisibleprefixes; data/eval_targets/*.npz actual untouched target vectors for all28layers. Reference/endpoints do not provide unseen-pretraining status.
Recompute with frozen scripts/run_gpu.py --stage fit_smoke, then --stage evaluate --rank0/1 only on authorized5090; analysis/render/deliver onCPU with2threads. Use unchanged freeze inputs, skip only valid complete chunks, no resampling. run_gpu.py performs no optimization. Per-document complete JSONs are resume units.
Code/protocol/input freeze: freeze.json plus provenance/prestart_implementation_review.json. Numerical audits: audit/03_numerics_smoke.json and audit/validation.json. Resources/logs: execution_certificate.md, terminal_rank0/1.json,acp_receipts/pod/*.log,logs/rank0/1.log. Manifest completion is separate from immutable design.
Project evidence is a selected small copy, not every raw tensor. No commit/push/publication; scientific acceptance Unknown.
'''
 (b/'assets_and_data.md').write_text(guide)
 (b/'assets_and_data_cn.md').write_text('# 原始资产与复算入口\n\n以下路径保留完整逐位置结果、输入和token位置，不将同文档多位置当作独立文档。\n\n'+guide.split('\n',1)[1])
 detail=f'''# R16 execution and eligibility record

Status: engineering measurements completed, scientific acceptance Unknown. Completed {now}.
Purpose: final-output sensitivity to single-layer own-reference head64 retention.
Protocol freezes all conditions/scopes/reference/positions before new outputs. Sources and checkpoint are hashed in manifest/freeze; ordinary prestart integrity/cast guard repair is recorded without changing scientific conditions.
Stage1 native reference:60fixedTRAINdocuments,9600same positions independently per28layers; native BF16 capture, FP64 cov/eigh. Stage2 smoke: all28fullPC reconstruction and no-op suffix; full-model hook vs suffix at1/14/28; causal prefix, oldcache replay, frozen parameters. See audit/03_numerics_smoke.json.
Stage3 two5090 independent document shards, atomic complete document chunks and saved untouched target states. Scopes use separate sequence copies; all-prefix can include future valid teacher-forcing tokens only because causal masks protect earlier targets. Stage4 CPU equal-document group aggregation,2000pointwise bootstrap, full target PCAidentity and oldbasis replay, figures and fixed input examples. No optimizer/model/classifier/lens training, H100, new data download or question expansion.
Numerical validation PASS;28layerfullPC target guards;rawrecords{V['raw_records']};baseline differences{len(V['baseline_top1_differences'])};legacy maxNLLdiff{V['legacy_max_NLL_diff']:.6g}. Complete evidence:audit/validation.json.
Actual perrank runtime/device/memory in terminal_rank0/1.json; platform receipts/logs separate. Outputs and exceptions remain execution-side. Full round setup, controls, data/exposed split, result and boundary are preserved in Protocol, Summary, evidence and casebook; no source result overwritten. Navigation checker reported preexisting unrelated organization/untracked entries; it does not validate science.
'''
 (b/'detailed.md').write_text(detail);(b/'detailed_cn.md').write_text('# 执行细节与可用性\n\n'+detail.split('\n',1)[1])
 tasks=[('model/token/data audit','DONE_VALID'),('28TRAINPCAfits','DONE_VALID'),('native/suffix/fullPC/shift guards','DONE_VALID'),('28layer x5conditions x2scopes','DONE_EXPLORATORY'),('legacylastlayer replay','DONE_VALID'),('raw/projected directhead diagnostic','DONE_EXPLORATORY'),('docintervals/fixedcases/rawoutput','DONE_EXPLORATORY')]
 for r in tasks:pass
 (b/'evidence/coverage.json').write_text(json.dumps([{'task':k,'status':v,'evidence':str(E/'audit/validation.json')} for k,v in tasks],indent=2)+'\n')
print('factual reports written, manual observed-case reading pending')
