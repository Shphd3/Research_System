from pathlib import Path
import json,hashlib,shutil,datetime,csv,re
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response')/E.name;ROOT=Path('/data/250010109/Research_System')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
R=[json.loads(l) for l in (E/'data/prefixes.jsonl').read_text().splitlines()]
# Frozen actual inputs remain immutable. Publish corrected length metadata separately and identify the stale legacy diagnostic.
oldlen=E/'audit/input_length_matching.csv'
if oldlen.exists() and not(E/'versions/input_length_matching_before_metadata_erratum.csv').exists():shutil.copy2(oldlen,E/'versions/input_length_matching_before_metadata_erratum.csv')
lengths=[];effective=[]
for r in R:
 a=next(x for x in R if x['family_id']==r['family_id'] and x['paraphrase_id']==r['paraphrase_id'] and x['context_type']=='A');b=next(x for x in R if x['family_id']==r['family_id'] and x['paraphrase_id']==r['paraphrase_id'] and x['context_type']=='B');z=dict(r);z['AB_prefix_token_length_difference']=len(a['prefix_token_ids'])-len(b['prefix_token_ids']);effective.append(z)
 if r['context_type']=='broad':lengths.append({'family_id':r['family_id'],'paraphrase_id':r['paraphrase_id'],'split':r['split'],'A_full_visible_prefix_tokens':len(a['prefix_token_ids']),'B_full_visible_prefix_tokens':len(b['prefix_token_ids']),'A_minus_B_prefix_tokens':z['AB_prefix_token_length_difference'],'A_answer_tokens':r['candidate_map']['A']['length'],'B_answer_tokens':r['candidate_map']['B']['length'],'U_answer_tokens':r['candidate_map']['U']['length'],'V_answer_tokens':r['candidate_map']['V']['length']})
pd.DataFrame(lengths).to_csv(oldlen,index=False);(E/'data/prefixes_effective_metadata.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in effective))
dump(E/'audit/length_metadata_erratum.json',{'frozen_input':'data/prefixes.jsonl','legacy_field':'AB_prefix_token_length_difference','error':'initial clue-only diagnostic and not refreshed after text repair;not used for model inputs,primary metrics or answer-length sensitivity','corrected_view':'data/prefixes_effective_metadata.jsonl','corrected_full_prefix_lengths':'audit/input_length_matching.csv','model_inputs_identical':all(a['prefix_token_ids']==b['prefix_token_ids'] and a['candidate_map']==b['candidate_map'] for a,b in zip(R,effective)),'recomputation':'metadata only;zero model forward,zero changed scores'})
# Exact source and factual records.
S=pd.read_csv(E/'analysis/summary.csv');C=pd.read_csv(E/'analysis/primary_feature_contrasts.csv');rec=json.load(open(E/'terminal_receipt.json'));val=json.load(open(E/'audit/independent_reaggregation.json'));assert val['pass'];oldrec=json.load(open(E/'versions/data_v1p2/terminal_receipt.json'));total_seconds=oldrec['elapsed_seconds']+rec['elapsed_seconds']+55.069196939468384
summarycn='''# R14：频率组对具体概念区分的即时贡献

[完整报告](report_cn.md) · [协议](protocol.md) · [实际执行与修订](detailed_cn.md) · [完整文本与原始分数](casebook_cn.md) · [复算](reproduce.md)

目的：在生物、数学、物理的具体概念配对上，检验删除低／中／高参考频率成员组后，区分损失能否超过同成员数和范数匹配对照。模型、字典、输出头全部冻结，没有新分类器或训练。操作对象是Qwen3-0.6B-Base最后块、最终归一化前的状态；A22系数来自14层联合编码，删组保留原始残差。

'''+(E/'analysis/recognition_text_cn.md').read_text()+'''

![主要匹配对照](figures/03_frequency_deletion_matched_controls.png)

三域各12独立评估家族，共36；216评估前缀来自两措辞×三前文，不当作216独立样本。完整模型具体判断102/144，上位判断204/216；删低／中／高组分别为99/102/91次具体正确、203/193/173次上位正确。两个任务量尺不同，不比较绝对降幅来宣称细语义专属性。每个指标按家族配对重采样4000次，主六比较另给同时区间。

全部167独立条件与19别名已交付。最终数据1.3，CPU两线程，GPU0；原5090排队任务未分配设备后停止。新CPU路径在开发样本上原生／缓存／因果／恒等差异均0，全部2640位置的完整方向重建评分一致。独立汇总最大误差1.78e-15。修正的20前缀、80模型分支与166评分位置重算，其余2474位置的表征与系数逐值一致；旧数据1.2及全部原始分数保留。
'''
(P/'summary_cn.md').write_text(summarycn)
summary='''# R14: Task-bound feature-frequency deletion effects

Purpose: determine whether deleting a low/middle/high reference-frequency feature group from a frozen native final representation harms cue-driven sibling-concept distinctions more than matched controls. The dictionary is the same 14-layer shared-code A22, not independent per-layer dictionaries. Group deletion acts on the last-layer raw decoder sum and retains the reconstruction residual. No language model, dictionary or classifier was trained.

The current panel does not establish frequency specialization. Across36 held-out evaluation families (12/domain), full-model symmetric cue contrast is1.539352; low/middle/high deletion gives1.558407/1.440587/1.152103. High-group excess loss over same-count random groups is0.357905 with pointwise95%[0.048827,0.675208], but the six-primary-comparison simultaneous interval crosses0[-0.030736,0.777969]. Excess over norm-matched perturbations is0.161457,95%[-0.171627,0.498732], and all three domain intervals cross0. Upper judgments also fall204/216 to173/216, and overall output divergence is4.657972 versus1.557875–1.861499 for norm-matched controls. These are task-bound frozen-output effects, not global importance or unique encoding.

Full sibling accuracy is102/144, but only31/72 paraphrase pairs have both sides correct and10/36 families have all four cue decisions correct. In a fixed ribosome/lysosome example, high deletion raises cue contrast4.122943 to4.720354 while shifting the lysosome-context margin-2.823071 to+1.319360 and making it wrong. Baseline candidate preference and cue sensitivity are distinct; baseline shift alone cannot explain the registered contrast loss because the broad baseline cancels algebraically. Linear-sum CrossCoder reconstruction yields contrast0.955978 and89/144 correct; this score ratio is not information retention.

Data1.3 repairs20 literal-upper-name prefixes identified solely from text; original data1.2, all167 outputs and sources are preserved. This repair moves the high same-count simultaneous lower bound+0.025086 to-0.030736, so that local positive inference does not survive. A false high-response counterexample label on inactive members was corrected without changing primary results. All mandatory167 unique conditions and19 algebraic aliases are complete. Independent reaggregation from raw positions agrees within1.78e-15. Final execution used existing CPU2threads/BF16,0GPUs after the approved5090 pool did not allocate; new native/causal/cache/identity gates passed. No new model or layer was substituted. Reuse of the old PCA basis is not independent replication.

The only proposed next uncertainty is whether extra high-group cue loss remains when overall output damage is matched. No new experiment was started for that proposal. Researcher scientific acceptance and question closure remain Unknown. See [Chinese report](report_cn.md), [Detailed](detailed.md), [Protocol](protocol.md), [amendments](amendments.md), and [raw reproduction entry](reproduce.md).
'''
(P/'summary.md').write_text(summary)
shutil.copy2(E/'amendments.md',P/'amendments.md')
detailedcn=f'''# R14实际执行与审计

本文件记录实际版本，不以摘要自证。完整实验分析在[报告](report_cn.md)，全部原始表入口在[复算](reproduce.md)。科研接受和关闭Unknown。

## 实际范围

固定48家族、288前缀，12开发家族／36评估家族；实际唯一评分位置2640，完整候选计分token3504（包括共享首位置在四候选中的重复计分）。167独立条件、19别名；全部完成。原生模型／字典／分类器训练0。模型Qwen3-0.6B-Base官方权重cd2a512...；字典A22 09b432...，block1,3,…,27共享系数，最后block27原始坐标删除，之后只接一次原生最终归一化和输出头。

最初5090任务pt-oqno0y4q一直未分配设备，已停止，未使用GPU。A9明确改用现有CPU两线程、同一BF16前向、同一权重和测点；新CPU推理上下文通过开发检查，未私换字典。所有本轮对比均在同一CPU路径，不能冒称跨硬件独立复现。CPU初版{oldrec['elapsed_seconds']:.2f}秒，纠正增量{rec['elapsed_seconds']:.2f}秒，开发检查55.07秒，累计约{total_seconds/60:.2f}分钟；原生模型前向1152+80+9=1241次。所有可续用缓存、完成条件和原始分数分块保存。

## 审计分级与修复

|级别|证据位置|影响|最小修复与重算|
|---|---|---|---|
|实现／数据错误，已修复|audit/pre_correction_all_candidate_name_scan.json；amendments A10|20前缀、7家族显式给出上位名称，不能作干净上位控制；3家族的具体线索前文也受影响|全部20文字规则命中前缀统一更正；80模型分支、166评分位置重算；其他2474位置h和z逐值一致。旧版完整保留，全部家族统计重算|
|实现／导出错误，已修复|versions/member_responses_before_A11.csv；amendments A11|原稀疏池中位数差为0，部分全零成员被误称高响应反例；不影响主效应|只保留符合原规则的非零候选，否则记未找到；固定Top2不变；无新前向|
|元数据错误，已修复展示口径|audit/length_metadata_erratum.json|旧AB_prefix_token_length_difference不是最终完整前文长度差；从未进入主评分或候选长度子集|冻结输入原件保留；data/prefixes_effective_metadata.jsonl和audit/input_length_matching.csv提供正确长度；输入token与候选完全相同，分数不变|
|表达问题，已修复|figures/archive/03_before_explicit_lower_legend.png|下排两种控制颜色原图例不够清楚，单位未直接写在纵轴|增图例、自然对数单位、收窄正值标签；未改点和区间|
|证据缺口|summary.csv、primary_feature_contrasts.csv|每域12家族、全模型只有10/36家族四个具体判断全对；同时区间与范数匹配区间不能建立选择性贡献|不筛去失败家族，不调阈值，结论为尚未建立；无需为得到正结果重算|
|解释边界|同上及error_transition_counts.csv|高频删除影响大不等于全局最重要；上位与整体输出也损伤；J与正确率可分离|分开报告线索分数、宽泛偏置、计数、上位与分布损伤；不把旧幅值／有无假设包装成已证明|

## 版本对结论的影响

版本1.2全部数据、167原始条件及源代码保存在 execution/versions/data_v1p2。更正依据是穷尽文字检查，不是模型是否答对。高频同人数额外损失0.406482→0.357905，同时区间下界+0.025086→-0.030736；高频范数匹配额外损失0.205296→0.161457，两版区间均跨零。[版本影响表](evidence/data_correction_primary_impact.csv)完整保留，不把更正称为独立复现。

## 实现与数值证据

- 原生／缓存／因果／恒等／完整PC输出在三域开发检查均0差；空组0差，冻阈值0.051281172782182693。原生BF16字典解码与FP32线性重建有0.17%–0.24%相对向量差，明示精度定义，不声称完全相同。组贡献用FP32原尺度线性和；完整重建以同一线性和及偏置/中心构成。
- 所有2640位置的全方向评分与真正恒等相同。独立汇总167条件、每条件36评估家族、24个领域／总体主对照行，最大误差{val['max_main_value_absolute_error']:.3g}。
- 候选shift、可见前文、完整答案、终止句号、目标片段和padding均有逐条索引核对。只改变最后层读出输入；后续文本仍为固定候选teacher forcing，不是自由生成或持续回灌删除。
- 随机正交性最大偏差低于2e-13。理想范数匹配最大偏差约1e-13；实际BF16高频平均相对差约0.022%、中频约0.12%–0.14%、低频约0.21%–0.33%，低频个别位置最大约11.6%，零目标5位置同时为零扰动。详表保留，不能把低效应轻率解释为无信息。
- 全部统计按家族而非同文档/措辞重复位置进行，4000次三域分层配对重采样，总体三域等权。主六对照同时区间；其他为明确标记的点式95%区间，未以挑选显著项作结果。

## 资源与全部材料

冻结Protocol原件、每次修订、manifest、输入/输出哈希、代码、数据、原始位置分数、完整候选分数、成员与谱投影、背景对照、失败与修复记录均在[复算入口](reproduce.md)。本轮没有训练任务改动、H100计算、提交Git、推送或发布。唯一下一步见Summary，未自主执行。
'''
(P/'detailed_cn.md').write_text(detailedcn)
(P/'detailed.md').write_text('''# R14 actual execution and audit

[Chinese Detailed](detailed_cn.md) contains complete setup, protocol conformance, version changes, issues and bounded reading. The frozen Protocol remains unchanged and amendments are append-only. Input identity, ownership and scientific acceptance remain distinct.

Completed:48families/288prefixes,36evaluation families,2640unique scored positions,167unique conditions+19aliases. All full-candidate tokens including period were scored; no EOS, classifier or training. All first-position output diagnostics are before any answer fragment enters the prefix. Actual final interface is official Qwen block27 residual-post BEFORE final RMSNorm; joint A22 coefficients use blocks1,3,...,27. Raw group deletion retains decoder bias, TRAINmean and original reconstruction residual. Spectral retention adds the TRAIN-side reference mean once; deletion subtracts only the centered projection.

Execution changed from unallocated approved5090 Spot to existing CPU2threads/BF16 under explicit A9, preserving checkpoint, tokenizer, measurement and equations. CPU inference uses the frozen A22 threshold and an explicitly qualified BF16 autocast context. No CUDA training guard is asserted as a CPU scientific qualification; the new native, causal, replay, no-op and reconstruction gates supply that evidence. CPU is not claimed bit-identical to prior5090 data; every current contrast is same-runtime. The GPU allocation was stopped while unallocated, not used as scientific evidence.

A10 repaired20literal-upper-name prefixes in7families using a text-only rule, after v1.2 outputs existed but before reading numeric results for selection. All167old outputs, code, data and affected caches are preserved.80candidate branches and166positions were recomputed;1072unchanged model caches were verified by exact input IDs/indices and known parent checkpoint/freeze.2474unchanged final states and joint coefficients are bit-exact; all unchanged per-condition scores are exact. Current data1.3 is the reporting version. Candidate-length diagnostic metadata has a separate corrected view with identical actual model tokens; no scoring uses the stale field.

A11 removed false high-response counterexamples when the original sparse-pool rule returned all-zero members; it did not alter predeclared top-two members, primary effects, data or thresholds. Missing qualified counterexamples are reported NOT_FOUND rather than replacing the rule. Figure legend/unit edits change no numeric evidence. Pointwise versus simultaneous intervals are distinguished. Negative, baseline-failure and small-support results remain in the evidence.

Independent reaggregation checks every main family score, count, six-primary-control contrast and interval from raw position arrays; maximum error1.78e-15. Exact all-PC identity applies to all2640positions. No-op/cache/causal gates are also retained. Numeric precision and applied norm matching errors are reported rather than hidden. Researcher acceptance and question closure remain Unknown.

All raw/cached artifacts are execution-side; see [reproduction](reproduce.md), [coverage](coverage.csv), [manifest](manifest.json), [amendments](amendments.md), [Summary](summary.md) and [Chinese report](report_cn.md). No commit/push/publication was authorized or done.
''')
# Coverage includes alias relationships, not fictitious independent runs.
conds=json.load(open(E/'data/conditions.json'));coverage=[{'item':c['condition'],'kind':c['kind'],'status':'DONE_VALID','source':str(E/'analysis'/f'condition_{c["condition"]}.npz'),'independent_conditions':1} for c in conds['unique']]
coverage += [{'item':a,'kind':'algebraic_alias','status':'DONE_VALID_ALIAS','source':b,'independent_conditions':0} for a,b in conds['aliases'].items()]
pd.DataFrame(coverage).to_csv(P/'coverage.csv',index=False)
(P/'reproduce.md').write_text(f'''# Reproduce R14

Research owner: `{P}`. Execution owner: `{E}`. Actual dataset is1.3, initial protocol plus amendmentsA1–A11 and the metadata erratum. Do not rerun prepare over a frozen result. The old1.2 payload is retained under versions/data_v1p2, not merged silently. Scientific acceptance isUnknown.

## Read first

- [Report](report_cn.md), [Summary](summary_cn.md), [Detailed](detailed_cn.md).
- [Actual manifest](manifest.json), [initial frozen protocol](provenance/protocol_frozen_v1.md), [amendments](amendments.md), [condition coverage](coverage.csv).
- [Full input/candidate metadata with corrected length diagnostics]({E}/data/prefixes_effective_metadata.jsonl); [immutable actual model input source]({E}/data/prefixes.jsonl); [all positions]({E}/data/positions.jsonl); [family review]({E}/audit/semantic_review_48families.json).
- [Group members and three random seeds]({E}/data/feature_groups.json); [condition operations and aliases]({E}/data/conditions.json).
- [Every candidate token log probability]({E}/analysis/candidate_token_logprob.csv.gz), [every complete candidate score]({E}/analysis/candidate_sequence_scores.csv.gz), [prefix scores]({E}/analysis/prefix_scores.csv.gz), [family scores]({E}/analysis/family_metrics.csv).
- [Primary contrasts]({E}/analysis/primary_feature_contrasts.csv), [each random control]({E}/analysis/individual_random_contrasts.csv), [all paired contrasts]({E}/analysis/all_paired_contrasts.csv), [error transitions]({E}/analysis/error_transition_counts.csv), [length sensitivities]({E}/analysis/length_sensitivity.csv).
- [Group spectral projections]({E}/analysis/group_spectral_contributions.csv.gz), [cross terms]({E}/analysis/group_spectral_cross_terms.csv.gz), [all16384member support]({E}/analysis/all_feature_support.csv), [representative responses]({E}/analysis/representative_member_responses.csv), [unavailable counterexample slots]({E}/analysis/member_counterexample_eligibility.json).

## CPU reaggregation from existing raw arrays

```bash
cd {E}
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
/root/anaconda3/envs/spectral-hier/bin/python scripts/analyze.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/spectrum_members.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/validate.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/correction_impact.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/render.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/casebook.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/report.py
```

These steps do not load a new classifier or train anything. They overwrite derived current views; preserve a new version before making scientific changes. Fresh forward reproduction uses `scripts/run_cpu_corrected.py`, actual exact model/CC weights from manifest, the same mounted transformers dependency,CPU2threads and frozen preflight. Source cache1.2 is accepted only through declared parent-freeze and exact per-sequence input-ID/index checks; corrected positions are never reused from the old text. `run_gpu.py` is the original authorized implementation, not an instruction to launch another allocation. No new run is started by this document.

## Numeric verification

[Independent raw reaggregation](provenance/independent_reaggregation.json) covers all167conditions/36evaluation families and paired control intervals. [Correction cache reuse](provenance/correction_reuse_validation.json) checks unchanged h/z and every untouched score. [Actual norm matching](evidence/applied_norm_matching_audit.csv) includes BF16 rounding differences and zeros. GPU and CPU phases are distinct in receipts; the only submitted job was stopped unallocated. Current scientific figures come from1.3, never an illustrative sketch.
''')
# Selected small factual evidence, not full activation payloads.
selected=['summary.csv','primary_feature_contrasts.csv','individual_random_contrasts.csv','error_transition_counts.csv','data_correction_primary_impact.csv','data_correction_impact.csv','applied_norm_matching_audit.csv','evaluation_first_position_group_support.csv']
for n in selected:shutil.copy2(E/'analysis'/n,P/'evidence'/n)
for n in ['conditions.json','families.jsonl']:shutil.copy2(E/'data'/n,P/'evidence'/n)
for n in ['independent_reaggregation.json','result_validation.json','correction_reuse_validation.json','corrected_cache_reuse.json','spectrum_provenance.json','length_metadata_erratum.json','source_audit_final.json','semantic_review_48families.json','crosscoder_normalization_metadata.json']:
 if (E/'audit'/n).exists():shutil.copy2(E/'audit'/n,P/'provenance'/n)
for n in ['freeze.json','terminal_receipt.json','config.json','figure_manifest.json']:shutil.copy2(E/n,P/'provenance'/('effective_'+n))
# Save analysis code as selected provenance; code remains execution-owned.
(P/'scripts').mkdir(exist_ok=True)
for f in (E/'scripts').glob('*.py'):shutil.copy2(f,P/'scripts'/f.name)
manifest=json.load(open(E/'manifest.json'));manifest.update(status='COMPLETED_BOUNDED_NATIVE_ANALYSIS',conditions_unique=167,aliases=19,positions=2640,evaluation_families=36,data_version='1.3',GPU_used=0,CPU_threads=2,actual_model_forwards=1241,total_active_CPU_wall_seconds=total_seconds,scientific_acceptance='Unknown',question_closure='Unknown',primary_finding='FREQUENCY_SPECIALIZATION_NOT_ESTABLISHED',length_metadata_corrected_view=str(E/'data/prefixes_effective_metadata.jsonl'),deprecated_field_note='AB_prefix_token_length_difference in immutable source is a legacy clue-only diagnostic; see corrected metadata view;model inputs and scores identical')
dump(E/'manifest.json',manifest);dump(P/'manifest.json',manifest)
# Every selected figure/table is traceable to its exact execution source.
entries=[]
for folder in ['figures','evidence','provenance','scripts']:
 for f in (P/folder).glob('*'):
  if f.is_file():entries.append({'path':str(f.relative_to(P)),'sha256':sha(f),'bytes':f.stat().st_size,'origin':str(E/'analysis'/f.name) if folder=='evidence' and (E/'analysis'/f.name).exists() else str(E/folder/f.name),'role':'selected evidence/provenance;not new authority'})
dump(P/'selected_evidence_manifest.json',{'run':E.name,'data_version':'1.3','primary_source':str(E),'entries':entries,'omitted':'model/CC checkpoints,complete raw/cache payloads remain execution-side;see manifest/reproduce','scientific_acceptance':'Unknown'})
print('FINALIZED',P,'activeCPUminutes',total_seconds/60)
