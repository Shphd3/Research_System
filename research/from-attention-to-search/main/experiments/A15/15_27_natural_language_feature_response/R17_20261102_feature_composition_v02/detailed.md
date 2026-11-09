# R17 Detailed execution record

Completed UTC: 2026-11-02T16:37:17.482054+00:00. Scientific acceptance, mechanism judgment, question closure and next decision remain Unknown. This record owns execution facts; the four numbered Anchors own design.

## Model and representation

Freeze official Qwen3-0.6B-Base and A22 checkpoint000999997440. Joint input: odd blocks1–27, width1024; output16384 nonnegative atoms. The last-layer hook is block27 before final norm, not MLP output. BF16 model/encoder; FP32 raw decoder. Inference uses learned threshold0.051281172782182693 on post-ReLU times summed layer decoder norms, then active=z>0; no batch top-k reselection. Last-layer raw reconstruction is bias+sum z_i D_i, with the residual retained. Define d_i=norm(D_i), u_i=z_i*d_i, r=norm(u_C), q=u_C/(r+1e−12), b_i=1(z_i>0). Decoder columns are not orthogonal, so norm(u) is not representation energy. Shared z does not originate exclusively in the last layer.

## Data, selection and fitting

384 unique full texts:48 square-matrix certificate families×3 conditions×2 wordings plus96 nonmatrix controls. Labels are globally invertible1/singular0, coarse Unknown. Related theorem clusters stay within splits6/3/3, giving24/12/12 families; fine-label probe rows96/48/48. Sizes2–49 vary with family; literal uniqueness does not imply semantic independence. The96 controls derive from12 mathematical topics with numbered variants. Word/length/negation are not perfectly balanced, retained as rivals rather than repaired after exposure. Token-count/global-active-count/global-norm tercile summaries were added after main-result inspection using discovery-only cutpoints; they are posthoc diagnostics, not prespecified validation. Constructed-source effects cannot be separately estimated.

Natural reference: existing R15 documents600, positions76800, split300/150/150. Only discovery38400 positions defines frequency groups, eligibility20 positives and5 documents, boundaries127/579 with ties intact. Existing keyword-screened webpages are neither representative natural-language prevalence nor globally unseen; overlap with A22 training remains unknown.

C is discovery top8 positive minimum standardized matrix-vs-control contrasts. F is discovery top8 absolute fine-label contrast. Best_single means the first F atom by discovery ranking. C16/32 and direct off/on transitions test truncation. H3 selects equal16-member arms from frequency pools. H4 freezes at most8 high-frequency atoms,20 pairs/80 state configurations,29 eligible and10 selected using discovery only; nonzero states split at discovery positive q75.

L2 logistic probes use the same C grid0.01/0.1/1/10/100, lbfgs, max_iter5000, balanced class weights. Discovery fits preprocessing and coefficients; development selects mean unweighted log loss. Main heldout48 rows contain12 families and only3 independent theorem groups. Family bootstrap2000, theorem-group sensitivity, seed20261103. H1 multiplicity5, H2 one, H3 two, H4 2M=20. Random seeds11021–11040; atom matching uses same frequency group plus log-count/document-coverage distance≤0.35. Random mean losses are averages of model losses, not the loss of the separately recorded average probability.

## H4 text correspondence

Validation events select at most50 distinct documents/configuration, one visible-prefix position each. Controls activate both atoms but not that state; match cohort and position quartile, length ratio0.5–2; exclude all hit documents and reuse no control document within configuration.208 paired contexts,91 unmatched hits. Documents may recur across configurations. Write blind-id/text-only files first, apply conservative automatic square-matrix certificate labels, then merge response metadata. This is not independent human annotation; missing/undetermined content is not false. Target labels are absent in both matched groups. An independent one-prefix-per-validation-document sample has141 non-target/9 undetermined/0 fine labels. Zero-event empirical bootstrap intervals do not prove zero population prevalence.

## Recoveries and amendments

Dependency/import issues were repaired with logs retained. Variable-batch BF16 smoke failed(hidden4.0,z0.012112) before formal extraction. Freeze physical shape8×64 with discarded repeat padding, retain thresholds/tolerances; all no-op/head/replay/fixed-shape batch checks then exact0. The existing natural cache is reused under its verified source interface.

After the first complete analysis,19 description rows were found to reference n without binding it. Add only the definition of n as row count; preserve labels, splits, hypotheses and statistical rules, then recompute all responses/readouts. Old results remain in versions/v02_0_before_notation_fix. Earlier H1 C/union losses were about0.649/0.384, now0.652/0.636: do not mix versions or treat correction as fresh confirmation. Subsequently exclude every H4 hit document from controls and require the length ratio; previous matching/labels remain in versions/v02_1_before_disjoint_context_matching. Both corrections occurred after target inspection.

## Validation and status

All required input asset accesses passed strict checks.384 texts unique, families and theorem groups do not cross splits; coarse labels remain null. Frozen-model probes only, CPU two threads, GPU0/no cloud job. Predictions H1/H2/H3/H4=7104/2496/7872/45888; all nonaggregated losses independently recomputed(max8.83e−12),3840 metric summaries checked(max3.34e−16). Serialized H2 main-model replay passes1e−10. Mean per-row reconstruction NMSE0.0508394, median relative residual length0.225870; raw ledger max9.54e−7. These reconstruction errors are not no-op identity failures. H1/H3 random20 seeds complete; H4 nine configurations complete20 each, one fails all20 matches. Optional shuffle and native answer scoring were not run, as permitted. Twelve figures rendered from identified tables; math was source-checked only. All applicable computation is complete, including negative/insufficient branches.

[Summary and interpretation](summary.md) · [full Chinese Detailed](detailed_cn.md) · [amendments](amendments.md) · [raw evidence and reproducibility](dataset_guide.md) · [fixed cases](casebook_cn.md) · [validation receipt](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/evidence/final_numeric_validation.json)
