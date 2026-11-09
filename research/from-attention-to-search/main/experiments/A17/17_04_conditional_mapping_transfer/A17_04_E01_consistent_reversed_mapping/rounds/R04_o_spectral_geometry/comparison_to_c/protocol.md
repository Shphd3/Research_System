# R04 supplement Protocol: O-operator differences A to C and B to C

## 0. Authorization and owners

Revision `a17_04_e01_r04_to_c_v1`. The researcher explicitly requests parameter-space A→C/B→C comparisons and explanation, excluding gradients. Write and freeze before measurement. This supplements [R04 Protocol](../protocol.md) and [Summary](../summary.md), under the same Focus/Anchor conditional-mapping question. Preserve previous frozen records and scientific states; mechanism acceptance/closure remain Unknown.

Role: parameter-space operationalization/proxy test. Existing checkpoints/bases, CPU only. No training, gradient, model forward, TEST, SAE or publication.

## 1. Purpose, objects and prior

Compare strongest O processing channels and endpoint differences for A/C versus B/C. The earlier expectation that A may be closer to compatible C than B is a candidate, not a presumed ordering. SVD gives W=Σ_i σ_i u_i v_iᵀ and Wc=Σ_i σ_i u_i(v_iᵀc). Large singular values describe strongly amplified input/output channels; they do not assign first/last/old-protection semantics from rank alone.

A continues with consistent new labels; B learns only reversed new labels; C starts from the same acquired-old state and mixes old supervision with reversed new labels. A/C new labels differ; B/C new labels agree but old supervision/exposure differ. C-A and C-B are endpoint differences, not executed training paths or identified repair directions.

## 2. Fixed inputs and resources

Reuse common old checkpoint, nine R02 families, existing DEV and saved R04 bases. Twelve necessary assets, including `analysis_a17_04_o_spectral_geometry_20261012_r04_v1`, pass [fresh selected strict access](/data/250010109/Research_System/assets/checks/2026-10-12_a17_r04_to_c_inputs.json). Freeze parent config/source/completion, all used basis/behavior hashes, new Protocol/source/config. Exact layer27 O key,1024×2048; separately convert saved FP32 operands to FP64. Fixed seeds29/43/71 and steps240/1200, primary1200; shared acquired-old model. Existing B1200 has24000 new answers; C1200 has12000 old+12000 new. New updates/exposure zero.

Execution root `/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry`; unique `runs/to_c_20261012_v1`. Eight CPU threads, FP64,20-minute bound,12 thin SVDs. Remote training Smoke is inapplicable; toy checks precede real processing. Never overwrite old runs.

## 3. Three comparisons

Endpoint differences are

\[
T_{AC}=W_C-W_A,\qquad T_{BC}=W_C-W_B.
\]

Report Frobenius/relative-old norms, full spectrum, sigma1, fixed top8/16/32 squared energy and boundary gaps, ratios to full C Frobenius/spectral norms, plus T_AC/T_BC U/V overlaps and signed cosine. Sigma1(T)=max_{||c||=1}||Tc|| is maximal linear output difference under the same unit input, not natural-data activation change.

For full-weight leading-k operators, use saved bases to construct

\[
W_{X,k}=U_{X,k}\operatorname{diag}(\sigma_{X,1:k})V_{X,k}^{\top},
\qquad
d_k(X,C)=\frac{\|W_{C,k}-W_{X,k}\|_F}{\|W_{C,k}\|_F}.
\]

X=A/B;16 primary,8/32 sensitivity. Report d_k and signed operator cosine, retaining gains, signs and input/output pairing. Leading16 of a difference is distinct from the difference of leading16 operators. Truncation differences/residual differences need not be orthogonal; do not call their norm ratios an energy partition.

For location relative to C, use full W_C leading-k bases as primary, and D_C=W_C-W0 bases as supplementary. Always label reference_kind. With P=U_C,k U_C,kᵀ and Q=V_C,k V_C,kᵀ,

\[
T=PTQ+PT(I-Q)+(I-P)TQ+(I-P)T(I-Q).
\]

The four Frobenius squared norms add exactly to ||T||F². Report both-in, output-in/input-out, output-out/input-in, both-out fractions and T-versus-reference U/V overlap. Full C top16 accounts for only approximately5.5% total matrix energy; outside it does not mean functionally irrelevant. D_C is a different reference.

## 4. Hypotheses, rivals and branches

Candidate: A/C leading operators may be closer than B/C. Opposite ordering weakens proximity as an old-retention proxy, not every directional-function hypothesis. Stable channel changes support descriptive linear-operator differences; rule semantics/causality remain open without actual readout linkage.

Strongest rival: A/C new requirements differ, B/C agree; supervision, exposure and Q/K/V change together. Ordering may reflect learning demands rather than old-rule protection. Cutoff ties, coefficient signs/scales also matter. Keep conclusions limited to O and fixed endpoints.

Branches: A/C closer→bounded geometric support, no module identity; B/C closer despite different old behavior→weaken distance proxy; rank/order/block mixtures→local differences without a single functional partition; identity/numerical failure→insufficient affected cells. Existing DEV old/new CE, accuracy and margin are behavior context, reported separately by panel and combined; no new prediction evidence.

## 5. Guards, outputs and completion

Reuse inspected parent CPU identity/SVD/overlap code; add differences, truncated operators and four-block calculations. Toy tests check nonnegative block fractions, sum/reconstruction and truncation distances. Real SVD reconstruction/orthogonality/energy errors ≤1e-10; block-sum error ≤1e-10. Start/end SHA binding and independent actual spectrum/truncation/block checks. No outcome-selected rank/checkpoint.

Save full spectra,12 actual basis files, difference/rank/truncation/reference-block tables, figures and provenance; register actual outputs and fresh selected access. Bilingual Summary/Detailed and manifest belong here; add a derived daily reading entry. Previous science/state remains unchanged.

Pre-execution result NOT RUN. Completion requires all fixed comparisons or named failures, linear meaning separated from behavioral causes, and preserved rivals. No parameter insertion/deletion or model-forward B/C cross-swap is part of this execution.
