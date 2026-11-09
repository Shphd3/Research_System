from common import *
import numpy as np,shutil
S08=R.parent/'S08_dataset_support_overlap_1104';pp=rows(S08/'data/panel.jsonl');assert len(pp)==771;assert not (R/'frozen_plan.json').exists()
# Hash the complete original S08 tree before any new computation; read-only input.
manifest={str(p.relative_to(S08)):sha(p) for p in S08.rglob('*') if p.is_file() and '__pycache__' not in p.parts};dump(R/'evidence/S08_original_hashes.json',manifest)
seed=2026110409;split=[];index={}
for d in DATASETS:
 order=sorted([i for i,p in enumerate(pp) if p['dataset']==d],key=lambda i:hashlib.sha256((str(seed)+'S09'+pp[i]['id']).encode()).hexdigest())
 for tag,ii in [('discovery',order[:128]),('heldout',order[128:])]:
  index[d+'__'+tag]=ii
  for i in ii:split.append(dict(id=pp[i]['id'],dataset=d,split=tag,original_index=i,full_token_count=pp[i]['full_token_count'],visible_length=pp[i]['visible_length'],positions=pp[i]['positions'],token_ids=pp[i]['position_token_ids'],token_decoded=pp[i]['position_decoded']))
jsonl(R/'data/document_split.jsonl',split);dump(R/'data/split_indices.json',index)
plan=dict(UTC=now(),owner_anchor='15_27_06',authorization='Current direct user requests cache-only A-marginals/B-joint distinction; execute, preserve S08, stop for review after delivery',seed=seed,source=str(S08),source_panel_sha256=sha(S08/'data/panel.jsonl'),source_cache_sha256=sha(S08/'cache/activations.npz'),datasets=DATASETS,missing=['Numina'],SAEs=SITES,discovery_N=128,heldout_N=129,positions=list(range(8)),features=30000,k=32,selected_features=24,selected_features_rule='Discovery pooled position count >=32 and active in>=12 discovery documents, <=80% of3072position rows; highest pooled counts, tie featureID. Full276pairs define score; no holdout feature selection.',pair_rule='Within all i<j. Cross same S08 cyclic-offset rule with newly fixed split/hash order: offsets1..(N-1)/2 for odd heldout129,8256distinct pairs/group. Discovery overlap is descriptive; main heldout.',null_chains=4,null_draws_per_chain=64,burn_sweeps=100,thin_sweeps=10,sweep='ceil(number_of_rows/2) unordered-row pair proposals per stratum; include failed and unchanged trades',null_modes=['position','position_token3'],null_strata='dataset x split x quantile; exploratory adds current token class: three discovery-pooled most frequent literal token IDs vs OTHER, fixed across datasets',A='Discovery p(feature|dataset,quantile), independent Bernoulli rows, rowcount random with expected32;256whole heldout-size simulated datasets; compute actual per-pair Jaccard, no ratio-of-expectations substitution. Also exact-heldout-marginal+k32 conditional null: descriptive, not discovery forecast. Report gap reproduction ratio without clipping/causal interpretation.',A_bias='Plugin sum(p^2) for within has finite discovery estimation bias; report unbiased intersection sum c(c-1)/(128*127) as separate audit, not an exact Jaccard. Discovery probability uncertainty not included in conditional heldout CIs; MCSE separately.',B='Curveball with uniform allocation of row-exclusive union, common unchanged; exact binary row and column counts. Failed trades retained. Candidate pair vectors averaged8positions/document. Discovery own-null residual direction v_d and contrast v_AB frozen before heldout.',B_primary='6own and6dataset-differential signed projections, two explicitly separate Holm6families, one-sided conditional-null p. Heldout whole-document999bootstrap CI conditional on discovery directions and estimated null center. Require lowerCI>0, Holm<.05, null mixing adequate. Opposite sign not-support; intervals spanning0insufficient. Near-zero calibrated result no detected excess for these statistics, not absence of all possible joint structure.',B_secondary='24member-count histogram, discovery-top8 exact binary patterns+OTHER,12illustrative pairs selected only on discovery among276 (6pooled-positive,6max-dataset-residual-range, min4coactivating discovery docs in any source); report all selected heldout values, failures and raw coactivation-minus-p_i*p_j. No classifier.',mixing='Four-chain split-Rhat<=1.10 and conservative autocorrelation ESS>=100 for decision-bearing scalar traces; original-edge retention within .05of margin-constrained expectation on average, all counts exact. If fails, one preallowed burn500/thin50rerun same statistic; preserve first. If still fails flag insufficient, continue independent conditions. Report locked columns, low-n token strata and changed-trade rates.',controls='S08 metadata length/format/source/token differences retained. No independent format matching in S08 or here. Token-stratified conditional null exploratory, directions frozen from base discovery; no rescue of failed primary. Complete question/position sampling unchanged. No new texts, forwards, weights, training, interventions or router.',CPU_threads=2,GPU=0,scientific_acceptance='Unknown',question_closure='Unknown')
dump(R/'frozen_plan.json',plan)
protocol='''# S09 protocol: marginal frequencies versus joint activation structure

Direct current user authorization covers this bounded cache-only analysis, design/statistics/figures/delivery, followed by waiting for review. Existing Anchor15_27_06 owns the member-composition question. Role: proxy audit/robustness check. No resampling of original texts, no model/SAE forward or training/interventions, no alteration of S08. This round separates A (frequency reproduction of S08 overlap) from B (beyond-margin coactivation and cross-source replication).

## Fixed objects and split

Reuse the exact S08 official Qwen3-0.6B-Base block27Attention-output and actual MLP-input native30000/ReLU-Top32 caches. Their IDs, hashes/hooks/preprocessing in source frozen_plan; dictionaries independent. Use original8quantile positions, all771question-only documents:257per Magicoder-OSS train problem, GSM8K train question, MMLU test question. Numina absent in recorded bounded search. Within source sort SHA256(seed2026110409+'S09'+original ID),128discovery/129heldout, whole documents intact. Save exact IDs/positions/tokens. These are previously exposed S08 documents with a new internal confirmation split frozen before new coactivation selection, not external fresh replication. Hash complete original tree before/after.

## A: frequency references and Jaccard

Compute every discovery p(feature|source,quantile). Generate256independent whole heldout-size Bernoulli panels, independent features/rows and source-specific position marginals. Expected rowcount32, actual counts variable and reported. Calculate each simulated support intersection/union then mean of8aligned-position Jaccards; never substitute expected intersection into Jaccard. Actual heldout uses all distinct within pairs and equal-number cyclic cross pairs:8256/group, documents are independent units. Report source-specific withinA/withinB/cross and pooled gap, observed-reference difference and gap reproduction ratio (not clipped, not a causal explained fraction). Conditional-on-discovery reference MCSE separate from999heldout-document bootstrap intervals. Also report analytic independent intersection E[I]=sum p_A p_B, plugin within bias and unbiased discovery U-statistic sum c(c-1)/(n(n-1)); none is an exact E[J].

For a precise Top32 comparison also use B's heldout conditional fixed-margin null. It preserves test feature counts and row32 and is descriptive rather than a discovery-only prediction. For complete within pairs, mean intersection=sum c(c-1)/(n(n-1)) is fixed by column counts; Jaccard can differ because I/(64-I) is nonlinear. Exact cross all-pair mean intersection is likewise fixed; the frozen equal-count cross graph may fluctuate with row assignment. Save intersection distributions and check this identity.

## B: joint statistics and zero model

Per source/split/quantile use Curveball row trades: uniformly choose distinct rows, keep shared members, uniformly partition their exclusive union preserving each row size, including unchanged/failed trades. This preserves every feature count and every row32 exactly. Use4independent chains,100burn sweeps,10sweeps between64draws/chain (256null panels). Sweep=ceil(n/2) row-pair proposals. Library/code/seed versions saved. Uniform-stationary reference follows the Curveball construction [Carstens2015](https://doi.org/10.1103/PhysRevE.91.042812); finite-time mixing is checked, never inferred from that theorem. Current token is not fixed by the primary null. Exploratory token-stratified null additionally conditions on global discovery-top3literal token IDs versus OTHER within each quantile, with small/locked strata reported. No independent format matching; formatting remains an open rival.

Select24feature IDs by discovery-only pooled count>=32, document coverage>=12 and<=80%row prevalence, descending count/tie ID. Define all276unordered pairs before seeing pair effects. For each document average the276binary pair products over its8positions. For each source discovery residual r_d=real mean pair vector - own exact-margin null mean. Freeze unit direction v_d=r_d/||r_d|| and, separately, v_AB=(r_A-r_B)/||r_A-r_B||. Heldout own score=v_d dot heldout residual; between-source score=v_AB dot(heldout residual_A-residual_B). These are statistics, not semantic directions. Null centers and own constrained comparisons prevent marginal differences alone being labeled dataset-specific joint structure. Save all276components and discovery directions before reading heldout joint values. Near-zero discovery norm makes its dependent test insufficient.

Two separate primary families: six own-structure tests, six cross-source residual-contrast tests. Each uses one-sided conditional-null rank p=(1+#null>=real)/(257), Holm within its own six tests,999whole-document bootstrap intervals conditional on frozen direction/null center. Signed positive heldout replication+lowerCI>0+Holm<.05+adequate mixing supports only the named statistic. Opposite prediction under adequate checks is unsupported; broad intervals or mixing/selection insufficiency are insufficient. Within-source rejection alone does not establish cross-source differences. Null samples are algorithmic controls, never additional independent documents.

Secondary: member-count distribution on24IDs, discovery-top8exact24-bit patterns+OTHER, and12illustrative pairs (6pooled positive excess,6largest dataset residual range;>=4coactivating discovery docs in any source) from the276fixed universe. Report raw coactivation, p_i*p_j contrast, fixed-degree null excess and all heldout counterexamples. These do not rescue primary failures. No readout/classifier is needed.

## Diagnostics, uncertainty and delivery

Verify every snapshot row32, unique IDs and exact original column counts. Record proposals/changed trades, original-support retention versus constrained expectation, unique snapshots, frozen columns, low-n strata, four-chain split-Rhat<=1.10 and conservative ESS>=100 for decision-bearing scalar traces. Mean retention discrepancy>.05, failed constraints or mixing failures trigger at most one preallowed longer100→500burn/10→50thin sensitivity, retaining original; unresolved cells insufficient. Whole-document bootstrap keeps8positions together; fixed discovery and estimated null mean uncertainties explicitly conditional, Monte Carlo standard errors separate. P-values conditional on margin null do not imply topic/format/source exchangeability or causation.

Save text/ID provenance links, split/config/hash freeze, discovery-only candidates/directions, actual null constraints/mixing, real/reference tables and all6source/SAE contrasts. Produce A actual/reference plot, B discovery/heldout versus null plot and transparent pattern/token-control supplement. Independent set/count/statistic replay, bilingual Summary/Detailed, concise daily report and small review packet. Preserve S08 byte-for-byte and all failed/negative cases. No commit/push/publication; scientific acceptance and closure Unknown. Stop at delivery for researcher review.
'''
(R/'protocol.md').write_text(protocol)
cn='''# S09 协议：单成员频率与联合结构

本轮由当前用户直接授权完整执行。已有15_27_06拥有科学问题；这里只补充指标辨别。A问单成员频率能复制多少重叠；B问固定行成员数与列次数后还有没有联合结构、该结构是否随数据集变化并在留出复现。二者不能互相替代。

原S08三源各257篇、两套原生SAE、每篇原8个分位位置不变。用固定种子2026110409的ID哈希顺序各取128发现/129留出，文档所有位置同组；保存ID/token/位置。S08已暴露，这不是新采集的外部复现。Numina仍未找到；无模型前向、训练、干预或原结果修改。

A用发现集每源每位置的全部feature频率，模拟256个独立Bernoulli留出规模面板，逐位置实际计算Jaccard。该参照每行期望32但不强制32，实际数量需报告；B的留出固定边际+固定32零模型是另一项描述性参照，不冒充发现集预测。交集期望可解析求和，不能直接代入Jaccard作精确期望；另报告发现频率估计的有限样本偏差。每侧真实/参照/差值、同域与跨域差的复制比例都保留，比例不裁剪且不称为因果解释率。

B在源×划分×分位内做Curveball等价双边交换，保留共同成员、随机重分配排他成员，失败/不变交易也保留，严格保持每行32和每列次数。4链，各burn100扫、每10扫采样一次64次，共256面板。扫=ceil(行数/2)次选行对。逐样本核查约束、交换、原成员保留、固定列、Rhat/ESS。Rhat>1.10、ESS<100或保留率偏离约束期望>.05时，只允许一次500burn/50thin的事前固定重跑，保留旧结果；仍不足就报告不足。

发现集按边际频率和文档覆盖选24个成员，固定全部276对；每篇对8个位置的共同激活做平均，减本源零模型期望，得到发现残差向量。冻结各源单位方向及每数据集对的残差差方向，之后才读取留出联合统计。检验留出沿相同方向的超额激活，以及两源残差的方向差。各6个主检验分两组Holm校正；999次整篇bootstrap区间是给定发现方向和估计零模型中心后的条件区间，MC误差另报。单个源存在联合结构不等于跨源不同。

次要统计为24成员中激活个数分布、发现集最常见8种精确组合+OTHER，以及最多12个发现集示例成员对；全部留出结果和反例报告，不能补救主要失败。探索零模型额外按发现集最常见3个当前token及OTHER分层，候选方向仍冻结。S08及本轮都没有独立格式匹配；长度、词面、格式、来源、主题和近重复仍是边界。

支持仅限冻结统计在留出正向复现、文档区间下限>0、Holm<.05且混合合格；方向相反为该预测未支持，宽区间/混合不足为证据不足，真实接近零模型只说明这些统计没测出超额结构。完整公式、选择规则和执行顺序见同目录英文协议与frozen_plan。科研接受/关闭Unknown；交付后等待审阅。
''';(R/'protocol_cn.md').write_text(cn)
C.mkdir(parents=True,exist_ok=True)
for name in ['protocol.md','protocol_cn.md']:shutil.copy2(R/name,C/name)
dump(R/'evidence/protocol_freeze.json',dict(UTC=now(),status='EXECUTION_AUTHORIZED_BY_CURRENT_USER',hashes={str(R/n):sha(R/n) for n in ['protocol.md','protocol_cn.md','frozen_plan.json','data/document_split.jsonl','data/split_indices.json']},selection_and_results='NOT_COMPUTED_AT_FREEZE'))
# Only now inspect discovery activation counts/select members.
ac=np.load(S08/'cache/activations.npz');assert list(ac['ids'])==[p['id'] for p in pp];freq={};selection={};tokcounts={}
for s in SITES:
 ii=ac[s+'__indices'][:,:8];vv=ac[s+'__values'][:,:8];assert np.all(vv>0);assert ii.shape==(771,8,32)
 disc=np.concatenate([index[d+'__discovery'] for d in DATASETS]);cnt=np.bincount(ii[disc].ravel(),minlength=30000);coverage=np.zeros(30000,int)
 for row in ii[disc]:coverage[np.unique(row)]+=1
 eligible=np.where((cnt>=32)&(coverage>=12)&(cnt<=.8*len(disc)*8))[0];features=sorted(eligible,key=lambda f:(-cnt[f],f))[:24];assert len(features)==24;selection[s]=dict(features=[int(f) for f in features],pooled_discovery_counts=[int(cnt[f]) for f in features],pooled_discovery_document_coverage=[int(coverage[f]) for f in features])
 for d in DATASETS:
  rowsi=index[d+'__discovery'];freq[s+'__'+d]=np.stack([np.bincount(ii[rowsi,t].ravel(),minlength=30000)/len(rowsi) for t in range(8)])
np.savez_compressed(R/'data/discovery_marginals.npz',**freq);dump(R/'data/feature_universe.json',selection)
for d in DATASETS:
 for i in index[d+'__discovery']:
  for tok in pp[i]['position_token_ids']:tokcounts[tok]=tokcounts.get(tok,0)+1
tops=sorted(tokcounts,key=lambda f:(-tokcounts[f],f))[:3];dump(R/'data/token_classes.json',dict(token_ids=tops,discovery_counts=[tokcounts[t] for t in tops],other='all other IDs'))
dump(R/'evidence/selection_freeze.json',dict(UTC=now(),feature_universe_sha256=sha(R/'data/feature_universe.json'),discovery_marginals_sha256=sha(R/'data/discovery_marginals.npz'),heldout_coactivation_read=False,token_classes_sha256=sha(R/'data/token_classes.json')))
print('PREPARED',selection,'tokens',tops,flush=True)
