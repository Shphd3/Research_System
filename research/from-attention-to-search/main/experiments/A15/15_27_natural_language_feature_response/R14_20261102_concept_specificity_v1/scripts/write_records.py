from pathlib import Path
import sys,json,hashlib,datetime,shutil,csv
sys.path.insert(0,str(Path(__file__).resolve().parent));from prepare import E,P,BASE,sha,dump,now
anchor=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_05_spectral_semantic_granularity_anchor.md')
protocol='''# Protocol: R14 concept specificity v1

## 0. Approval snapshot
APPROVED_FOR_FROZEN_FORWARD_AND_COMPLETE_ANALYSIS by the researcher's 1102 prompt and final priority amendment. No further approval for routine implementation. Primary owner: 15_27_05 spectral semantic granularity. Purpose: identify task-specific, less replaceable frequency-group contributions to externally defined concept contrasts. Main endpoint: full-minus-group-deleted symmetric concept contrast, above same-cardinality random deletion and norm-matched perturbations. All other spectral conditions are completed but secondary. Scope: one frozen official Qwen3-0.6B-Base, A22, at most two RTX5090 Spot; no training/new conversations/H100. Scientific acceptance and question closure Unknown.

## 1. Objects
A family contains upper concept U, wrong upper concept V, two siblings A/B, broad prefix x0 and A/B cue prefixes xA/xB, each in two genuine paraphrases. A position is the state predicting one candidate answer token. A feature is one shared coefficient jointly encoded from blocks 1,3,...,27; not 14 independent dictionaries. Frequency means z>0 in 65536 independent-reference DCLM positions, not output word frequency or spectral order. Spectrum means the centered covariance eigenbasis in the raw final-block coordinates.

## 2. Anchor alignment and evidence layers
Prior R12/R13 readouts show accessibility but not actual decoder use. R13 native decoding shows prediction/frequency recovery but no externally established semantic ordering. This round changes the final residual-post vector and holds earlier computation and native decoder fixed. Natural-language paired cues define the particular distinction; deletion is not a unique-encoding claim. Presence/amplitude decomposition is not adjudicated by whole-group deletion. Existing Dense dynamics is context only, with a different model and no A22 transfer.

## 3. Hypothesis and rivals
Some frequency group might have task-specific contribution beyond matched deletions, with cue-linked effects across independently specified families. Rivals: vector magnitude, group cardinality, general prediction corruption, answer frequency/length/template preference, redundancy, weak full-model ability. No presumption head/coarse or low-frequency/fine.

## 4. Data and independence
Exactly 48 authored families (16/domain), first4 development and next12 evaluation per domain; 288 prefixes=72 development+216 evaluation. 36 independent evaluation families, not216 independent prefixes. Six fixed evaluation examples: families05,06 per domain; all families retained regardless of full-model behavior. Two globally shared templates; not independent template generalization. A/B cue names absent verbatim; aliases manually audited by AI before output, not human blind review. Definitions cited to named textbook/reference sections. Broad context intentionally insufficient to choose A/B. No held-out candidate concepts duplicated across family split. Sources and AI review text in data/families.jsonl. V is semantically wrong but same answer slot; residual length/frequency mismatch remains measured. Exact tokens/lengths/boundaries in data/prefixes.jsonl. No data fitting or classifier fitting. Reference spectrum math/bio-only means physics is a transfer domain, not three-domain fitted PCA.

## 5. Model, layer and dictionary
Official path/model hashes in manifest. Qwen28 blocks,1024 hidden, tied output head. Intervention at zero-based block27 residual-post BEFORE final RMSNorm. Apply native norm once and frozen head. Native model inference BF16/SDPA, same qualified runtime as R13; projections FP64 then BF16; log softmax FP32. Fixed row batch64 decoder evaluation; native sequence-shaped vs cached-head BF16 kernel differences diagnosed on development. Acceptance gates: identical no-op/all-PC and empty deletion decoded with same shape exactly equal; cached repeated forward h bit-equal in same shape; causal future-masking candidate scores difference<=0.05 nat; native sequence-head vs cached-head difference<=0.05 nat/token and<=0.5 logit, declared finite-precision boundary. Do not compare kernels as semantic effects.
A22 checkpoint fixed hash09b432..., 14 selected blocks1,3,...,27,16384 features. Frozen TRAIN mean/vector-L2 RMS, threshold0.051281172782182693, use_threshold rule with sum of14 layer decoder L2 norms; no gate retuning. Encode at each candidate scoring position (including after the first subword), padded1024 positions to preserve qualified GEMM path. Last-layer raw contribution is z times FP32 decoder times TRAIN RMS27. Bias+TRAINmean added once only for complete reconstruction. Feature deletion subtracts that group's contribution from original h and leaves residual/bias/other groups untouched. Linear FP32 reconstruction used for additive accounting; native BF16 dictionary decode also checked on smoke and discrepancy reported as rounding, not extra unexplained residual.

## 6. Scoring and answer boundary
Prefix ends newline Answer:, no chat template. Each candidate is leading space + complete term + period; period INCLUDED, EOS excluded. Full prefix+answer tokenizer must retain prefix IDs exactly. Score every answer token at its preceding position, including terminal period, with the same condition; cannot use just first subword. L is summed log probability in natural-log units. r(x)=L(A|x)-L(B|x); gA=r(xA)-r(x0); gB=r(x0)-r(xB); J=(gA+gB)/2=[r(xA)-r(xB)]/2. J cancels broad preference; report gA/gB/r(x0) separately. A-side correct iff r(xA)>0, B-side iff r(xB)<0; tie incorrect. Both-correct uses both sides per paraphrase, then family average. Upper judgement is L(U)-L(V) in each context; tie incorrect. Never subtract the raw accuracies/loss magnitudes of these two different tasks as a fine-specificity score. U and siblings not mutually exclusive; A/B-vs-U auxiliary only.

## 7. Conditions and frozen randomization
Exact unique conditions and alias mapping: data/conditions.json. B1[0,1), B2[1,16), B3[16,64), B4[64,128), B5[128,256), B6[256,512), B7[512,768), B8[768,1024); H[0,16). Retain=mu+P(h-mu); delete=h-P(h-mu), not zero-centered retention. Full identity, mean-only; nested k1/16/64/128/256/512/768/1024; separate retain/delete each band and H; H+B3..8 and matched total-rank head extensions. Random retain/delete at all relevant ranks; random additions orthogonal to H. Seeds11021/11022/11023, matrices frozen before outputs. Spectral norm-matched perturbation: h-random_removed*||target_removed||/||random_removed|| per scoring position; not an orthogonal projection. Zero denominator gives zero perturbation and logged mismatch, no infinities.
Frequency group membership reuses R13 exactly: low20..170 hits4469 members; middle171..881 hits4437; high>=882 hits4451. Insufficient positive2278 and zero749 members separately logged, not silently reassigned; they remain in original model/reconstruction. All target groups,3 same-count random groups sampled from qualified complement of target, and3 per-position norm-matched versions. These groups include all members rather than prior tiny readout subsets. Target support/l0/response and signed contributions saved. Random group exclusion of target prevents accidental partial deletion of the target itself; not a null drawn from every dictionary member.

## 8. Main analysis and decision mapping
For each family average two paraphrases; then mean12 families per domain. Overall equal weight3 domains. Difference=J_full-J_deleted, positive denotes lost cue distinction. For each target group report loss versus each of3 random controls, their mean, each of3 norm-matched controls and mean. Bootstrap4000 paired family draws within domains (seed21102), reused across conditions. Pointwise95% intervals for all conditions; six primary group-by-control-type overall excess contrasts additionally use99.1667% Bonferroni intervals. No p-value fishing. Support requires excess above both matched controls, cue-consistent cases and family/domain consistency; descriptive consistency ledger for all12 families/domain. If not, write not established, separating redundancy, broad corruption and power. Simultaneous lower bounds>0 are strong quantitative support, not semantic/causal proof. Upper U/V and first-position overall prediction distortion/entropy/word-frequency mass reported separately. Count specific-correct-to-wrong changes while full and intervened U/V remain correct in both cue contexts, with explicit eligible denominator; compare controls, no absolute cross-task score subtraction.
Length-matched A/B subset and matched U/V separately; primary summed sequence scores unchanged. Per-token average scores sensitivity reported separately and cannot replace primary. Candidate NLL is synthetic-task candidate NLL, not natural corpus perplexity. Full failures kept, not filtered; conditional-on-full-correct rows descriptive with denominator, all-family endpoints primary.

## 9. Output distribution diagnostics
All first-answer positions only, BEFORE candidate is visible. Frozen DCLM4194304-token reference reused from R13 with tokenizer lineage limitation inherited; alpha0.5, specials separately. Probability-weighted log frequency and highest1% vocabulary-ID mass; output entropy; relative KL of full to intervention; deterministic top20 probability-descending then token-number ascending (retrieve all exact boundary ties so not relying on low-precision topk ordering). Conditional candidate log probabilities and token fragments retained. These diagnostics are broad corruption checks, not semantic specificity labels.

## 10. Smoke and execution
Inherited measurement/source/token-boundary fixes cited, no redundant historical replay. New-text development smoke only: boundary/shift/padding/causality, native final layer/head, all-PC no-op, empty-group deletion, group+residual reconstruction original scale, fixed threshold/buffers, random orthogonality/rank, chunk/replay equivalence and numerical finite. All new guards must pass before evaluation scores. No new fitting. Forward caches per sequence, coefficients at all scored positions; cache hashes include model/text/position/basis/conditions/config. Completed chunks never overwritten; spot resume verifies freeze. Use one visible GPU from5090-2-spot allocation. Submission via repository template and registered image/runtime; reused protocol-local ACP workspace compatibility proxy from R13 fixes API schema, not hardware. Estimate<=2GB cache,10–35 active minutes before observed throughput; actual resource/time recorded. Ordinary failures repaired with archived old versions and amendments; no data/criterion edits after evaluation access.

## 11. Deliverables and cannot claim
All unique+aliased conditions, all prefixes/candidates/position scores, first-position distributions, family r/g/J/U-V and correct counts, raw group vectors/support/spectral fractions with cross terms/residual; source/protocol/config/code manifests, checks, runtime logs and figures. report_cn.md uses SAE-mediated Model ->1102->目的->结论->实验分析; main result ordered by frequency deletion, spectral curves appendix. Four figure groups, six fixed families plus diagnostic max/min/near-zero selected by explicit effect metric. One next question only after all applicable work. No free generation, routing, Dense expansion, new models/layers/training, globally ranked feature importance, unique code or presence/amplitude mechanism; independent external human annotation remains absent.

## 12. Freeze and amendments
User authorized full execution and delegated ordinary implementation choices in latest prompt; final priority paragraph supersedes original spectral-first narrative. A–G audit confirmed within this delegated scope, not researcher scientific acceptance. This protocol is written before scores. Preserve initial protocol/config/data and hashes; append amendments.md before any changed computation. No after-the-fact exclusion/selection. Implementation errors invalidate/recompute only affected conditions. Conclusive scientific state remains Unknown pending researcher review.
'''
anchortxt='''# R14: Task-bound feature-frequency contributions

## 1. Purpose and parent
Continue 15_27_05 spectral semantic granularity. Advisor asks what different components support in real language. Current question: in biology/mathematics/physics cue-driven sibling distinctions, which frequency group contributes less replaceably under frozen final-state deletion? This is a round extension under the same scientific owner, not a new routing line.

## 2. Existing knowledge
R12: head reads coarse/fine labels, no stable dedicated middle/tail increment above matched dimension; residual remains readable. R13 presence/amplitude: information in occurrence, amplitude changes judgments, unique bilateral complement not established. R13 native: true-target accuracy differs from fidelity; mean-only creates strong background formatting, not hierarchy. Dense trajectory uses different model; no transferring A22 to it. See inherited_evidence.md and hashes for actual tables/audits, not summary alone.

## 3. Hypothesis and credible rivals
Task-specific less-replaceable frequency contribution is possible. Alternatives: redundancy, feature cardinality, perturbation magnitude, broad output damage, answer lengths/frequency, weak baseline, family-specific cues. Spectral position, feature activation frequency and output frequency independently defined.

## 4. Computational model
Frozen28block Qwen,raw block27 pre-final norm. Shared-z A22 uses14layers. Remove vG=sum(z_j*d27_j*TRAIN_RMS27) from original state; residual remains. All candidate positions, complete sequence scoring. Spectral retain mu+P(h-mu), delete h-P(h-mu). r=L_A-L_B;J=[r(xA)-r(xB)]/2; upper L_U-L_V measured separately. No classifier/dictionary training.

## 5. Constructible comparison
Exactly48 families,288 prefixes;36 evaluation families3 domains. All conditions and frozen inputs in protocol/manifest. Main comparison full-minus-group-deleted J beyond same-count random group and per-position norm matching. Hold weights/head/data fixed. Spectral retain/delete/add conditions connect actual group-vector spectra; nonorthogonal groups may cancel, so do not sum energies.

## 6. Evidence and decisions
Positive task-bound support needs matched-control excess, identifiable cue and independent-family consistency. Absence means not established with separate redundancy/general damage/low-power explanations. U/V judged on own scale and explicit flip patterns; not subtraction of unequal task accuracy scales. Full-model failures retained. No significant-looking subset rescue.

## 7. Round record
Question/hypothesis/setup/controls/data and confirmation split frozen in protocol.md. Result NOT RUN at initial writing. Actual evidence, deviations and bounded updates will be appended after execution, without replacing initial state.

## 8. Boundary and next decision
No global frequency ranking, unique encoding, coarse-to-fine mechanism, amplitude-versus-occurrence proof, routing benefit or free-generation claim. AI suggestions and scientific acceptance remain distinguishable; researcher acceptance Unknown. Complete all requested conditions, then propose exactly one unresolved question.
'''
for name,txt in [('protocol.md',protocol),('anchor.md',anchortxt)]:
 (E/name).write_text(txt);(P/name).write_text(txt)
(E/'amendments.md').write_text('# Amendments\n\nInitial v1: no scores opened. Final user revision fixes frequency-group deletion as primary; all spectral conditions retained.\n')
# Compact Chinese companions; full technical contract above is canonical.
(P/'anchor_cn.md').write_text('# R14：具体概念区分中的频率组贡献\n\n主问题：生物、数学、物理的具体概念区分中，删除哪一频率组造成的损失超过同成员数随机删除和逐位置范数匹配扰动？重要性只限这些任务与干预。\n\n继承读出、原生解码及幅值／有无的边界；三层证据分别是可读信息、冻结输出删除效应、外部概念与上下文线索。不能相互替代。完整科学合同见[Anchor](anchor.md)，精确操作见[协议](protocol.md)。初始状态：未运行；研究者科学接受Unknown。\n')
(P/'protocol_cn.md').write_text('# R14 冻结协议中文导读\n\n已获本轮完整前向、分析、修复与报告授权，无新模型或分类器训练；最多两张5090 spot、优先一张。正式操作合同见[protocol.md](protocol.md)。\n\n48概念家族，三领域各4开发、12评估；288前缀，216评估前缀但只有36独立评估家族。每家族上位U、错误上位V、同层A/B，宽泛／指向A／指向B各两种措辞。所有完整答案与结束句号逐片段评分，不含结束符。\n\n主要终点为完整模型的对称线索区分量减去频率组删除后的量；同时比较三种随机同成员数组和逐评分位置等扰动范数。J=[r(A线索)-r(B线索)]/2，r为完整候选A与B的对数概率差；宽泛基线在J中消去，因此gA、gB和宽泛偏好同时报告。上位U-V单独报告，不能将两个任务绝对降幅相减宣称细语义专属。\n\n按家族先平均措辞、再分域平均，总体三域等权；4000次配对家族重采样。全部对照和谱段条件落在conditions.json，不按结果改样本或阈值。当前资料是AI语义审核，并非人类盲标；两种全局模板不构成独立模板泛化。\n')
# Link new round once from parent and CrossCoder's existing anchor.
link=f'\n\nR14 authorized 1102 round: [task-bound concept specificity]({P}/anchor.md), [protocol]({P}/protocol.md). Frequency-group deletion is primary; full spectral matrix secondary. Initial state NOT RUN; scientific acceptance Unknown.\n'
if E.name not in anchor.read_text():anchor.write_text(anchor.read_text()+link)
cn=anchor.with_name(anchor.stem+'_cn.md')
if cn.exists() and E.name not in cn.read_text():cn.write_text(cn.read_text()+link)
# Exact inherited files plus decisive raw tables, no historical checks rerun.
rels=['R12_spectral_semantic_granularity_20261031/summary_cn.md','R12_spectral_semantic_granularity_20261031/analysis/contrasts.csv','R13_feature_presence_amplitude_20261101/summary_cn.md','R13_feature_presence_amplitude_20261101/analysis/paired_contrasts.csv','R13_feature_presence_amplitude_20261101/analysis/target_word_form_audit.csv','R13_20261101_native_spectral_decoding/summary_cn.md','R13_20261101_native_spectral_decoding/audit_review_20261101/issues.json','R13_20261101_native_spectral_decoding/evidence/addition_control_contrasts.csv','checkpoint_spectral_dynamics/20261101/summary_cn.md']
records=[]
for rel in rels:
 for root in [P.parent,BASE]:
  q=root/rel
  if q.exists():records.append({'path':str(q),'sha256':sha(q)});break
 else:records.append({'path':rel,'status':'NOT_FOUND'})
dump(E/'audit/inherited_sources.json',records)
(P/'inherited_evidence.md').write_text('# Inherited evidence and repaired interfaces\n\n'+ '\n'.join('- '+str(r) for r in records)+'\n\nR13 native fresh-cache replacement retained original model/measurement/basis; no repeating failed legacy cache. Top-k ties deterministic. Candidate token boundary is recomputed for complete new answers. R13 encoding audit: isolated token ` the` need not be a whole word. This round uses complete candidate sequences, not a fixed-token semantic proxy. Dense is a separate-model background, not an A22 asset. Referenced-thread read API was called for both IDs but returned empty content; canonical records are the evidential source, not invented chat contents.\n')
print('Written',P)
