from common import *
import shutil,re
timestamp=now();archive=R/'evidence/pre_result_owners';assert not archive.exists();archive.mkdir();resolution=[]
anchor=(C/'anchor.md').resolve();focus=P/'main/focus/focus_remote_target_near_competitor_composition.md'
for f in [anchor,anchor.with_name(anchor.stem+'_cn.md'),focus,focus.with_name(focus.stem+'_cn.md'),C/'protocol.md',C/'protocol_cn.md']:
 dst=archive/f.name;shutil.copyfile(f,dst);resolution.append(dict(original_path=str(f),original_sha256=sha(f),preserved_path=str(dst)))
for f in [anchor,anchor.with_name(anchor.stem+'_cn.md')]:
 s=f.read_text();start=s.index('## 7.');end=s.index('## 8.',start)
 text=(f'''## 7. Current Evidence

R19factual results completed at{timestamp}. [Summary]({C/'summary.md'}) and [Detailed]({C/'detailed.md'}) own all results; [numeric annex]({C/'numeric_evidence.md'}) retains every heldout family and declared sensitivity. MLP-input H1supported(N12,cos0.7449,Holm p0.001465); H2supported(N11,cos0.9713,p0.002441). H3local only(rho0.6364,Holm p0.0568,template p0.25),with clear counterexamples. Attention six-member coverage5far/6near-far is below the frozen8minimum,so H1–H3insufficient. Binary joint directions do not replicate; both amplitude conditional-null tests passp0.01556but family intervals cross0,so H4stable-family criterion is insufficient. All288formal+4smoke forwards and196exact old-score replays complete. Old136source/owner files remain byte-identical. No training/intervention; scientific acceptanceUnknown. Original pre-run owners and Protocols are archived with hashes; only factual status and presentation corrections were added.

''' if not f.stem.endswith('_cn') else f'''## 7. 当前证据

R19于{timestamp}完成事实记录。[Summary]({C/'summary_cn.md'})与[执行记录]({C/'detailed_cn.md'})拥有结果，[数值附录]({C/'numeric_evidence.md'})保留所有留出家族及预定敏感性。MLP输入H1支持（12家族，cos0.7449，Holm p0.001465），H2支持（11家族，cos0.9713，p0.002441）；H3仅局部支持（ρ0.6364，Holm p0.0568，模板内p0.25），保留反例。Attention六成员覆盖远矩阵5、近远6，低于8门槛，H1–H3证据不足。二元联合方向未复现；两幅值条件重排p0.01556通过，但家族区间跨0，H4稳定家族条件仍证据不足。288正式+4smoke全部完成，196旧评分精确重放，旧136源/owner文件字节保持。无训练或激活干预，科学接受Unknown。运行前owner/Protocol有哈希归档；仅更新事实状态并追加展示修正。

''')
 f.write_text(s[:start]+text+s[end:])
for f in [focus,focus.with_name(focus.stem+'_cn.md')]:
 s=f.read_text().replace('`AUTHORIZED_EXECUTION`','`COMPLETED_AWAITING_REVIEW`').replace('`NOT_RUN`','`FACTUAL_COMPLETE_SCIENTIFIC_REVIEW_PENDING`');s+=f'\nResult record: [Summary]({C/"summary_cn.md" if f.stem.endswith("_cn") else C/"summary.md"}). STOP before any functional intervention/training design; question_state and scientific_acceptance remain unchanged.\n';f.write_text(s)
for f in [C/'protocol.md',C/'protocol_cn.md']:
 s=f.read_text();s+=f'''\n## Amendment A1 / 展示修正：{timestamp}

After all heldout results were visible, corrected the case-display implementation: comparing only Tprojection sign missed opposite-diagonal counterexamples. Keep preselectedF23; show all heldout failuresF23/F27/F28and first successful nonpositive-diagonalMLPF11. Original figure code/selection are at `{R/'evidence/presentation_v1'}`. Correct plot legend overlap/headroom and verify formal matched rows separately from smoke. No text/token,split,member,frequency group,contrast,null,test or primary verdict changed. This is an in-scope presentation/verification correction under the user's complete-analysis request, not a new experiment or scientific acceptance. Original complete Protocol bytes are preserved at `{archive/f.name}` with the original freeze hash. Full visibility/scope are recorded in `evidence/presentation_amendment.json`.

全部留出已见后，修正只比较T符号而漏反例的展示实现。保留预选F23，另列全部失败F27/F28及首个非正对角仍正确的MLPF11；原展示、原协议字节与时间保留。图例/顶部空间、smoke验证范围属呈现与实现修正。未改文本/token、划分、成员、频率、比较、null、检验或主要判断；不增加实验或科学权限。
''';f.write_text(s)
dump(R/'evidence/design_result_resolution.json',dict(UTC=timestamp,scope='Factual result update of new15_27_11owner only; no R18owner edit or scientific acceptance',originals=resolution,current=[dict(path=x['original_path'],sha256=sha(x['original_path'])) for x in resolution],original_protocol_body_preserved=True,scientific_acceptance='Unknown'))
art='''# Artifact and replay index

Canonical records: [Anchor](anchor.md),[Protocol](protocol.md),[Summary](summary.md),[Detailed](detailed.md),[numeric evidence](numeric_evidence.md),[literal cases](casebook_cn.md),[data guide](dataset_guide.md). English canonical; Chinese companions preserve the same evidence and pending states.

|Object|Actual location|Content|
|---|---|---|
|Full actual prefixes, token IDs, roles|EXEC/data/panel_portable.jsonl|292literal rows; clean display metadata; frozen text/tokens unchanged|
|Frozen input|EXEC/data/panel.jsonl|Original input retained; inherited suffix metadata audited|
|Clean pair table|EXEC/data/text_pairing.csv|384paired comparisons and matching flags|
|Legacy mismatch audit|EXEC/data/R18_comparison_audit.jsonl|48explicit old non-one-factor comparisons|
|Candidates and frequency|EXEC/data|Both complete native reference tables/bins and discovery-only C/R/scales/joint directions|
|All raw candidate scores|EXEC/results/behavior_smoke.jsonl;EXEC/results/behavior_discovery.jsonl;EXEC/results/behavior_heldout.jsonl|Every candidate token logp and full/item/period score|
|All native sparse activations and h|EXEC/cache/discovery.npz;EXEC/cache/heldout.npz|Top32IDs/values reconstruct30000post-TopK coordinates; actual1024hookinputs retained execution-side|
|All member lists|EXEC/results/membership_pairs.jsonl|768site-specific pairs, exact shared/entered/exited IDs/values|
|Readable raw positives|EXEC/tables/sparse_activations.csv|Every formal positive coordinate,reference group,token and position|
|Individual/member/geometry/frequency tables|EXEC/tables|Every family,raw/relative fixed values,T/N/I,missingness,behaviors,frequency support,marginals,sensitivities|
|Full conditional-null statistic traces|EXEC/cache/*_null.npz|Both splits/sites,4×64draws,all pool pairs,degree snapshots|
|Scoring and complete analysis|EXEC/code|run.py;select.py;analyze.py;joint_heldout.py;supplement.py;offline_replay.py;all actual figure/report/package code|
|Provenance and checks|EXEC/evidence|Freeze,strict assets,run incidents,old-byte protection,token/numeric/degree checks,figure review,package receipt|
|Figures|EXEC/figures;./figures|Two independent site overviews,two literalF23panels,frequency groups,joint nulls|
|Conversation memory|MEMORY|Append-only operational log; noncanonical|
|Small result packet|ZIP|Under20MB;raw sparse/text/score/null inputs,documents,code and fresh-extraction replay|

The packet omits pretrained weights/fullh/compiledlibrary; omitted_assets.jsonlists actual path,size,SHAand unsaved preactivations. No checkpoint was trained or modified. Full model/SAEconfiguration and source hashes are in config.json. R18is unchanged. No commit/push/external publication.
'''.replace('EXEC',str(R)).replace('MEMORY',str(SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md')).replace('ZIP',str(SYS/'daily_research_reports/1104/20261104_R19_remote_target_competitor_composition.zip'))
(C/'artifacts.md').write_text(art);(C/'artifacts_cn.md').write_text('# 实际文件与复算入口\n\n[完整路径清单](artifacts.md)列出真实全文/token、384配对、全部逐候选分数、两SAE的Top32、逐家族/频率/联合null数据、图与代码。[认识更新](summary_cn.md)、[原文例与反例](casebook_cn.md)、[数值附录](numeric_evidence.md)为阅读入口。\n\n执行根：`'+str(R)+'`。小包按本轮明确请求包含关键原始数据、稀疏缓存、null轨迹及可复算代码；权重与完整h仅列真实地址/大小/SHA。对话记忆是操作记录，不授予科学判断。原R18原件保持，无commit/push/外部发布。\n')
rep='''# Reproduction

## Without model inference

Extract the ZIPand run `python code/offline_replay.py` from its root. Python3.10+,NumPy1.24.4andSciPy1.12.0suffice. The script independently reconstructs sparse vectors from every saved ID/value, verifies all raw token sums and paired memberships, recomputes primary effect means/intervals/p/Holm and four joint-null projections/p-values. No absolute data path,model,GPUor network is needed. This does not regenerate conditional-null draws; their full statistic traces, seeds and source code are included for audit.

## Exact forward environment and algorithm

Original execution uses torch2.3.0a0+6ddf5cf85e.nv24.04and the existingQwen3-capable Transformers tree. Set `PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3`, `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`, `TOKENIZERS_PARALLELISM=false`; use2CPUthreads,FP32,SDPAand2×328physicalshape. Model/tokenizer and both nativeSAEweights/loaders/hashes are in config.json; omitted_assets.jsonstates which external payloads are required. Existing inference completed; rerunning a stage requires a fresh output location, because run.pyrefuses to overwrite saved scores/caches.

The actual sequence was prepare.py→record_design.py→run.py smoke→run.py discovery→select.py→candidate/analysis hash gates→run.py heldout→analyze.py+j oint_heldout.py→supplement.py→quality_coverage.py→figures.py→verify.py→offline_replay.py→reports/curation/package. The space in j oint is typographic only: the actual filename is joint_heldout.py. NativeSAEencoding is encoder(x),ReLU,Top32without input normalization/decoder-bias subtraction. Hooks capture block27o_projoutputand actualMLPpreinputat319,with no activation modification. Full candidate conditional scores include every item token and period. Complete source and numerical checks are retained.

## What can be audited

See evidence/freeze.jsonandpre_result_ownersfor exact pre-run owner/Protocolbytes; design_result_resolution.jsonresolves later factual-owner updates without erasing old hashes. candidates_and_joint_frozen.jsonandanalysis_code_frozen_before_heldout.jsonprecede heldout starts. reference validation replays old natural counts/groups. verification.jsonchecks292tokenizations,196score replays,136protected old files and6144degree constraints. Presentation correction changes no hypothesis/test. Package receipt checksCRC,size,SHA,links,new-directory extraction and offline replay. Scientific acceptance remainsUnknown; no intervention/training is run or designed automatically.
'''.replace('j oint_heldout.py','joint_heldout.py').replace(' The space in j oint is typographic only: the actual filename is joint_heldout.py.','')
(C/'reproduce.md').write_text(rep);(C/'reproduce_cn.md').write_text('''# 复算说明

小包解压后，在根目录运行`python code/offline_replay.py`，只需Python/NumPy/SciPy，无模型、GPU或网络。从真实稀疏ID/数值和逐token评分出发，复算成员、六项主检验点值/区间/校正p及四项联合统计。null完整统计轨迹与种子/原代码保留；该离线入口不重新生成null样本。

重新前向需外部模型/SAE权重，见config与包内omitted_assets.json；原环境PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3，PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python，TOKENIZERS_PARALLELISM=false。CPU2线程、FP32、SDPA、2×328；分阶段脚本拒绝覆盖现有评分。训练与激活干预均未运行。

[完整算法与执行顺序](reproduce.md)、[数据字段](dataset_guide_cn.md)、[执行记录](detailed_cn.md)保留原协议、冻结门、展示修正、失败版本、旧原件保护和检验分母。本轮不需要为审阅结果再运行前向。
''')
brief=SYS/'daily_research_reports/1104/meeting_report/meeting_brief_R19_remote_target_competitor_cn.md'
brief.write_text(f'''# 远处目标与近处竞争：相同成员，不同强弱，仍不足以完整解释错误

我们要看模型利用远处物品事实时，近处竞争词怎样改变同一批SAE成员。当前结果支持MLP输入中一组六成员的事实差异跨近词和近远条件保持；竞争时成员强弱与模型偏好一起改变。行为解释仍有反例，未通过全部预定门槛。Attention因共同支持不足保持证据不足。

## 先讲抽屉里的 magnet

F23远处说`The drawer was packed with the magnet.`，最后问抽屉装了什么。保持完整320token、远物品e190、答案前冒号p319不动，只把近处另一个容器的object换成battery（近词末token309）。完整全文和候选逐token分数见[原文]({C/'casebook_cn.md'})。

MLP输入#17390从7.418升到9.967，低频#25508从3.941降到3.272，#16240从15.728升到18.058，#27076从13.515降到11.247；同一组同时激活但搭配改变。battery/magnet完整候选分数由−14.919/−10.371变成−8.837/−9.626，模型由正确转为错误。固定近处词后单独改变远目标仍影响这些成员，目标分量没有全部消失。所选坐标中目标投影0.600、近词投影0.663，相反差−0.063；作差等式是定义，不是机制证明。

![真实成员与候选偏好]({C/'figures/MLPIN_SAE_F23_case.png'})

图的下六行是严格匹配矩阵；上六行是旧主距离任务，中间黑线表示文本框架改变，不能跨线当作单因素竞争效果。颜色只用于观察每个成员的相对变化，格内是真实激活。

## 总体上保持了什么，失败在哪里

24家族按整家族分12发现/12表征留出，模板两侧共享。补96条匹配文本，所有292前向及原196条评分重放通过。主三个距离仍各12/12成对；匹配中性11/12、一致12/12、相反9/12，正确分差平均降3.814nat（区间2.847–4.912）。

MLP六共同成员的事实差异H1cos0.745（12族）、近远H2cos0.971（11族）通过。竞争变化与行为损失ρ0.636，Holm p0.0568、模板内p0.25，仅局部支持；Attention远矩阵只有5族、近远6族严格共同激活，低于8族门槛。不能把这当成两个位置的显著差异。

反例F11：组合相反差−0.023仍成对答对；F27：差仍+0.531却有误判。F28中性已错，不能把所有失败起点都归给竞争。二元共同出现超边际证据未保持；幅值重排两侧p0.0156，但家族区间跨0，稳定组合的主要判定证据不足。高/中/低频共同参与已见，参考低频不等于在本任务少见。

![跨家族总体]({C/'figures/MLPIN_SAE_membership_geometry.png'})

左上展示成员复用和更换，右上展示事实差异方向；下方保留每个家族，红色为相反条件成对失败。可见表征指标与行为不一一对应，不能靠成功例宣布统一机制。

## 两个现场追问

为什么这组对照能区分解释？因为远目标A/B与近词A/B分别改变；相反对角T−N可以拆为固定近词的目标差和固定目标的近词差。旧主任务/竞争直接比较没有这个识别条件。

为什么还不能说这几个feature导致错误？我们只比较配对前缀在同一答案位置的稀疏表征；反例、候选先验、其他成员、后续句号评分和字典重建损失仍存在。没有激活干预，也没有跨任务验证。

[完整认识更新]({C/'summary_cn.md'}) · [每家族与频率数据]({C/'numeric_evidence.md'}) · [执行与原始文件]({C/'artifacts_cn.md'})。本轮停止。待共同审阅后再决定是否设计功能实验；科学接受Unknown。
''')
idx=SYS/'daily_research_reports/1104/README_cn.md';s=idx.read_text();s+='\n- [远处目标与近处竞争的SAE组合：真实例、反例、总体与边界](meeting_report/meeting_brief_R19_remote_target_competitor_cn.md)；结果包：`20261104_R19_remote_target_competitor_composition.zip`。\n';idx.write_text(s)
print('FINAL_DOCS',timestamp)
