派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/protocol.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/protocol.md)；研究修改仍回到原件。

---

# Protocol: Dense weight spectral dynamics (W01)

## 0. Approval Snapshot

Document status: APPROVED_FOR_BOUNDED_CPU_READ_ONLY_ANALYSIS by the current explicit user request. Scientific acceptance remains Unknown. Purpose: distinguish stability of weight magnitude,isolated first directions and top64 subspaces across all compatible saved states. Parent: existing Dense checkpoint spectral dynamics Anchor15_27_05_01; this is a separately recorded parameter-space extension, not a reinterpretation of its representation results. Four CPU threads,zero GPUs,900seconds,3GiB output. New training and extra resources are excluded.

## 1. Terminology / Definitions

One observation is one native saved two-dimensional weight matrix W[out,in] at one checkpoint. Its uncentered SVD W=U diag(s) V^T has left/output directions U and right/input directions V. No text panel,mean subtraction,covariance divisor or classification fit enters this experiment. Singular values are nonnegative magnitudes; only singular vectors/subspaces have orientations. One-dimensional normalization gains are excluded; tied output embedding is the same matrix, not a second measurement.

## 2. Anchor Alignment

The researcher explicitly changed the object from paired-text representations to weights. Parameter-space dynamics may explain a different part of training change but do not establish representation dynamics or functional change. Keep all old findings and the old protocol intact. Scope and results link from an appended parent record after completion.

## 3. Tested Hypothesis

Question: for each module,are the largest singular magnitude,identifiable leading directions and top64 input/output spaces continuing to change late in0.5B–33B? No universal ordering or positive stabilization outcome is assumed. A stable s1 with moving U/V weakens a scalar-only stability claim; fewer principal-angle changes may support only within-window stability under explicit tolerances.

## 4. Rival Explanations

Sign ambiguity,near-degenerate sorted components,unequal token gaps and incomplete checkpoints can mimic or misstate instability. Gauge changes and coordinated changes across adjacent modules may alter raw parameter coordinates without the same functional change. No functional equivalence,semantic or router-utility claim is made.

## 5. Data Construction And Provenance

Use exactly the12 readable checkpoints in the copied manifest,0.5/1/3/5/10/15/17/19/21/22.018691584/31/33B;8 manifested missing states remain missing. Asset checkpoint_family_dense_spectral_dynamics_20261101 passes current strict access. Verify every payload digest and embedded tokens/step. No new data,split or model is constructed. Each checkpoint is loaded on CPU in isolation with torch mmap,and released afterward.

## 6. Learning Task And Permitted Supervision

No learning or labels. Deterministic numerical decomposition only. Zero forwards,optimizer steps or new training.

## 7. Model / Architecture And Frozen Variants

Same native Dense trajectory,8blocks,hidden1024,281431040parameters. All57 independent 2D matrices:embed.weight151936×1024; per block q2048×1024,k/v1024×1024,o1024×2048,gate/up3072×1024,down1024×3072. Validate exact names and shapes at each state. Excluded 1D gains are enumerated rather than called missing.

## 8. Training Objective And Optimization

NOT_APPLICABLE. For W compute the smaller FP64 Gram W^TW or WW^T,all1024 singular magnitudes and its eigenvectors. Recover opposite-side leading65 vectors by Wv/s or W^Tu/s. No whitening,centering,scale fitting,Procrustes or module aggregation before the per-module results. This reuses the prior spectral-distance idea but adapts to two-sided weight SVD;prior activation-covariance code is not used as a weight estimator.

## 9. Conditions, Seeds, And Checkpoints

684 module-state decompositions,57modules×12checkpoints. Compare all11adjacent pairs and12endpoint pairs separately,left and right. Exact deterministic algorithm;no randomized approximation or stochastic seed needed. The preflight timed0.5Bq and embedding to estimate runtime;this is disclosed,not treated as a formal full result.

## 10. Primary Metric And Frozen Analysis Plan

For each matrix save all singular values,s1,Frobenius energy,sum(s²),s1²/sum(s²),relative gaps after1and64,numerical rank,top65U/V and residuals. For each pair report absolute and symmetric relative s1 change,sign-invariant first direction angle arccos(abs(u_a^Tu_b)) and the same for v,degrees,plus top64 principal angles,RMS/max angle and normalized projection distance sqrt(mean(sin²(theta))). Report raw and per-billion-token changes. Adjacent points retain actual gap;endpoint curves do not establish stabilization.

A first vector is identifiable only when(s1−s2)/s1>=.05 at BOTH points and s1 is nonzero. Otherwise its individual angle is UNIDENTIFIABLE;save raw diagnostic only and report the joint leading block whose outer relative gap passes. Top64 distances compare each state's ordered subspace;they do not track identical semantic features. Record boundary gaps and rank. If the64/65gap is near numerical error(<1e-10),label cutoff unresolved rather than claim stability. Weak gaps<.05 remain sensitivity warnings,not an automatic claim of physical instability.

## 11. Secondary Metrics And Guards

Engineering sensitivity grid is AI_PROPOSAL,not a researcher-justified convergence tolerance. For s1 use raw symmetric fractional thresholds1/3/5percent and perB.25/1/2percent. For first-vector angles use raw5/10/20degrees and rates1/3/5degrees/B. For top64 projection distance use raw.05/.1/.2 and rates.005/.01/.02perB. For each cross-product,report the earliest start of a terminal suffix with at least3consecutive observed intervals all satisfying BOTH bounds,and no later observed rebound;all required directions must be identifiable. Missing states are never interpolated. Call any resulting time a conditional within-window tolerance onset,never final convergence. If no threshold-robust onset exists,answer“not established” and retain curves. No weight-entry bootstrap:the full saved matrix is the object,not a random sample. Numerical error is separate from single-run uncertainty.

## 12. Known Good / Known Bad / Known Confusing Cases

Identity gives zero angles/distances;paired sign reversal gives zero;left/right orthogonal rotation preserves s but can move directions;a near-degenerate leading pair invalidates single-vector identity. Compare one real query matrix with direct FP64 SVD. Require relative spectral/eigen residual<1e-8 and basis orthogonality<1e-8;nonzero recovery and rank guards. Stop affected matrices on failed guards;do not relax after observing results.

## 13. Scientific Procedure And Stage Contracts

Preflight:verify asset,schema,counters and runtime bound. Smoke:known cases and direct-SVD agreement. Collection:sequentially hash/load each checkpoint,compute all57cached module decompositions,release. Pair analysis:derive left/right1and64metrics and threshold sensitivity. Delivery:full tables,one core figure at a time,source hashes,summary and detailed;preserve insufficient or non-stable results. Numerical failure blocks its dependent result,not all unrelated modules.

## 14. Algorithm, Output, And Provenance Contract

Execution:/data/250010109/MoE_Router/experiments/20261101_dense_weight_spectral_dynamics. Canonical record:weight_spectral_dynamics beside this protocol. Config lists exact modules,states,tolerances,budget and algorithm. Freeze protocol,config,manifest andcode before full decomposition. Cache identity includes checkpoint payload+manifest,module shape,preprocessing and algorithm/config hashes. Atomic per-module completion with payload hash;resume only qualified entries. Large basis payloads remain execution-side. Record actual resource use and counts. No commit,push,new chat,new GPU or remote submission.

## 15. Success / Failure / Insufficient Evidence

Engineering success=684decompositions plus complete per-module magnitude/direction/subspace/threshold tables with failed/missing items explicit. Stability supports only the named module,side,tolerance and observed window. Continued changes or late rebounds weaken its stated tolerance hypothesis;near-degeneracy,missing progress or numerical failure leave a clause insufficient. No aggregate pass rescues missing conditions.

## 16. What This Cannot Claim

Final mathematical convergence,behavioral or semantic stability,representation stability from weights alone,or router optimality. No numerical noise interval is a repeated-training uncertainty interval. Tied embedding weight left space is vocabulary coordinates,not text-sample coordinates.

## 17. Block Confirmation, Freeze, And Amendment Ledger

User explicitly requested all-checkpoint per-module weight spectroscopy and then leading64spaces. Matrix scope follows native2Dtensors;both sides are required to disambiguate orientation. Operational settings are frozen before batch;engineering tolerances remain sensitivity candidates. Current protocol is a new extension;the original representation protocol is preserved. Any post-start change must append its before/after,reason,visible results,authorization and affected eligibility.
