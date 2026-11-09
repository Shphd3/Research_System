# Normalized fixed routing and final-layer expert learning: frozen execution contract

Version2026-10-19 v1 plus the researcher scoring/condition supplement. [Verbatim Chinese v1](protocol_frozen_v1_cn.md), [Chinese supplement](supplement_cn.md), [frozen machine configuration](design_freeze.json), [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_21_activation_to_expert_learning/15_21_activation_to_expert_learning_anchor.md). The supplement supersedes the original single-calibration and five-condition clauses only. Execution is explicitly authorized by the researcher; this is not inferred from design confirmation.

## 1. Inputs and identities

Frozen Qwen3-0.6B Base at /data/share/Qwen3-0.6B-Base:28blocks, hidden1024. Frozen A22 14-selected-layer F16384 CrossCoder final checkpoint checkpoint_000999997440.pt. Input caches are the exact parent frequency_interval_moe/20261018T103820Z TRAIN130712/EVAL65402 valid next-token positions, with aligned raw final residual h, gated shared z, target, original block/position IDs. Reuse fixed reliable9615, low L964, high962, and T/R11 candidate9605; do not re-extract or refit lists. Input asset IDs and selected strict access snapshot are in the execution manifest. Different TRAIN/EVAL bin files do not establish document/near-duplicate independence; dictionary training saw these texts and EVAL has been inspected previously.

## 2. Stages and stop

Activation/profile and calibrated dispatch -> primary A/B/C paired training -> learned references and expanded fixed scores -> same-input function -> independent target-background/adapt scene -> spectra/report. No approval between stages. Numeric or input/gradient errors block only dependencies; negative results and empty experts do not. Main training deadline is2026-10-18T22:24:39Z (receipt+5h), report deadline23:09:39Z. No unequal-step endpoints or data-window reduction to finish. Four H100 Reserved only; no new Work/Codex conversation/reservation expansion. PARTIAL/NOT RUN are explicit.

## 3. Profiles and reconstruction

Separate shared z, binary hit, TRAIN p, block28 vector zD28 and c=z||D28||. Normalize/invert using actual centered vector RMS: normalized=(raw-TRAINmean)/rms; raw_hat=normalized_hat*rms+TRAINmean. Report raw and centered relative squared error and norms. Routing keeps sum14 decoder norm weights. Before learning register the first source-ordered complete continuous64-token window with at least two L atoms in each split; otherwise first complete window with note. Display at most4Top10,4other,8L atoms ranked by window peak c thenID, sort by global TRAIN p; missing categories unfilled. Common per-quantity color scales, no row normalization. Save all window positions, top5 L contribution positions and prev/current/next token fragments; following text is posthoc only. Whole-split positive conditional amplitude medians/IQR/support are separate from these selected examples. Original z/c remain invariant through expert training.

## 4. Four frozen scoring rules

Let a_i=z_i w_i with original sum14 norms; p_i=TRAIN hit fraction; m_i=TRAIN mean a_i conditional on positive activation. S0=mean_group a_i; S1=S0/mean_TRAIN S0; S2=mean_group(a_i/m_i); S3=mean_group(a_i/(p_i*m_i)). Group denominator is the original member count and inactive terms0. Each class of positive denominators uses median_positive*1e-6 floor. Original zeros contribute0, zero groups excluded from calibrated competition; no all-zero-denominator branch can proceed. Feature floor reference is the original reliable9615, shared by T/R11; group mean floors are separately per grouping. Save zero/floor triggers globally and candidate-wise. Do not compose the rules, impose quotas or remove common information from h. FP64 sparse accumulation rounds to FP32; S1 uses saved FP32 S0. Argmax/ties/all-zero inputs use the inherited source/block/position stateless hash seed20261019, retaining every input.

## 5. Conditions and comparisons

T/R11 times S0-S3 yields8fixed arms. A=T_S0, primary B=T_S1, C=R11_S1; D=Learned, E=LearnedLB. R11 is fixed rather than chosen from random candidates. Seeds11/22 are paired model/data seeds. T/R11 group sizes are1257,1347,1506,1629,1824,1189,523,330. Same-list S1/S2/S3-S0 and S3-S2, same-score T-R11, and LearnedLB-Learned are registered. B-A/B-C remain primary; no EVAL-best winner is relabeled preregistered. All safe scores enter training.

Learned P=softmax(Wr u), k=argmaxP, multiplierP_k, Wr no bias/no noise, independent seeded N(0,.02^2). Fixed multiplier1. LB=8sum_e stopgrad(hard full-batch fraction_e)*mean_fullbatch(P_e), coefficient.01 only E; D computes/logs same raw term at coefficient0. Fixed arms have no LB objective. No overflow drops.

## 6. Branch and frozen path

u=h/a, a=sqrt(mean_TRAIN ||h||^2/1024), one scalar without centering. E_e=Wdown[SiLU(Wgate u)*Wup u], three1024x1024 bias-free full matrices. Each3,145,728 parameters; total25,165,824; learned router adds8192. h_out=h+a*multiplier*E_k; original BF16 final RMSNorm/tied output head stay frozen but propagate input gradients. Wgate/up seeded N(0,1/1024 variance), down0; same seed expert states identical across conditions. Never all-zero initialization. Cached h/z avoid repeated teacher extraction but online cost is not free: the original14-layer joint dictionary requires frozen teacher representations, then routing sparse scores.

## 7. Training and engineering checks

Three complete TRAIN epochs, batch512, micro128 (64/32 only for actual OOM with unchanged effectivebatch), per-epoch PCG64 no-replacement order shared by seed, tail152 retained. Each run768updates/392136valid supervised exposures. AdamW lr3e-4, betas(.9,.95), eps1e-8, wd.01, clip1; ceil5%=39warmupupdates then cosine to.1lr. FP32 parameters/Adam, BF16 GEMMs, FP32 CE. Each micro CE is weighted actualmicro/fullactualbatch; LB computed once on fullbatch. Save initial/everyepoch complete state plus64-step recovery: weights, optimizer, RNG, exact orders/cursor, counters/config. Write token- and update-indexed TensorBoard task/objective/component/counter tags.

Before formal training, a fresh copy fits64positions up to100steps; check all source next-token labels, zero-branch exact logits, expert gradients, learned-router CE gradient after first expert update, and exact next update after save/restore. Ten full steps measure throughput/memory. Formal starts from pristine initialization. Finite worsening is retained, not tuned away. NaN/Inf/actual implementation error stops the affected run and preserves evidence. Reuse only truly architecture-compatible checkpoints; the parent GELU/centered branch is incompatible.

## 8. Evaluation and registered judgment

Step0/everyepoch: full EVAL NLL and fixed TRAIN diagnostic. Primary endpoint epoch3. Overall position NLL and low-feature macro M_L are separate: average NLL over each fixed L feature's hit positions, then equal-feature average over estimable features; report supports/overlap/NA. Low union, nonunion, high inputs and TRAIN-defined frequency bands supplement it. B must improve both A and C by delta M_L<=-.01nat/token and overall delta<=+.01 for both seeds to give limited support. Full differences always shown.1000paired original-context-block bootstraps seed20261019 are descriptive, not independent population confirmation. Resampled features without hits are NA.

Report actual expert position/context load, update/exposure counts, all reliable p/assigned reception/q/q-over-p, low macro/median/zero reception, Top10 actual q and original head-gap B including infinity/NA. List ownership does not imply actual arrival. Do not equate balanced load, reception, geometry or learning.

## 9. Same-input function and spectra

Freeze a context-balanced seed20261019 EVAL probe capped1024 plus512L-hit positions, deduplicated. Force each expert on identical h with gate1; compare outputs/norms/cosine/NLL. For natural-route replacements preserve original selected gate and replace expert with each other expert or zero branch; report overall/L delta. Learned gate1 probes differ from natural softmax amplitude.

Wgate/up/down: initial/final/delta full spectra, Frobenius norms and top16 display; normalize sigma^2 by full Frobenius^2, zero initial down=NA. Same-probe centered response covariance uses rows=input positions, uniform weights; trace and shape separate. Expert IDs across strategies are not inherent functional matches. Spectra are not direction similarity or capacity evidence. No pruning/PCA training.

## 10. Target-conditioned held-out update

TRAIN-only choose first L ID with>=256hits and>=20contexts, fallback original200/20; otherwise NOT RUN. C_train/EVAL are target-hit subsets and B their complements; EVAL<50hits/<5contexts gives insufficient evidence without replacing target. Independently train T_S1 seed11 background on B_train for2epochs, original fullTRAIN statistics frozen. It may see unlabeled routing statistics, not target supervised updates. Pre-adapt recommendations: list owner, modal natural C_train route, lowest forced C_train NLL expert (ID tie). Clone one background state8ways; only expertj updates, same target samples/order, forcedgate1,32stepsbatch64, AdamWlr1e-4/otherparamsunchanged, resetoptimizer, no schedule. Evaluate0/8/32 C_eval forcedj absoluteNLL and before-after gain; B_eval uses frozen natural background routes for harm. Safeoracle: harm<=.01, rank absolute final C_evalNLL; gain rank separate. One target/onebackgroundseed, not truly unseen knowledge/deployed assignment.

## 11. Resource and provenance

At most4H100,32GiB Torch allocated/GPU,256GiB aggregateCPU RSS,64GiB new execution disk. No transformer or dictionary training/whole co-occurrence rerun. Source/config hashes, input IDs, job/platform vs internal state, actual costs and failed engineering attempts are distinct. Source assets stay execution-side.

## 12. Delivery and claim boundary

One-page Chinese overview, full Summary/Detailed, all condition and paired tables, random/strong-response source text as defined, core plots and figure explanations, metrics/training logs/checkpoint asset manifests and public reasoning audit. Organize purpose, hypotheses, model, comparisons, observations, interpretation and boundaries. Previous phi organization did not alter actual routes; T training cannot establish phi utility. No frozen-base result proves from-scratch pretraining capacity. No post-result scientific repair is silently substituted for the registered test.

## 13. Authority

User authorizes this complete finite round and in-scope engineering fixes. Preserve old results. No commit/push, extra hardware or follow-on experiment. Researcher judgment/state transition remains Unknown. Any next experiment is an AI proposal requiring a new decision.
