派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/protocol.md)；研究修改仍回到原件。

---

# Protocol: fixed-token C-to-R frozen intervention

State DRAFT_NOT_EXECUTABLE. Only read-only asset/design preparation is authorized. The user must explicitly say “继续执行本协议” before model discovery, qualification or intervention. Core hypotheses are researcher-specified; exact numeric operational choices are AI proposals. No routine step-by-step approval is requested. The companion protocol and `protocol_config.json` carry identical settings.

## A. Question and alternatives

C/R are activation-response candidates; R is not the A17 parameter residual or h−C. At fixed token identity, does reducing C at block14 specifically impair actual block28 R-direction discrimination and the contextual prediction relative to matched edits? H1 dependence, H2 coactivation without detectable specific dependence, H3 generic damage/reconstruction/readout cross-talk. R/function co-effects are not proof that R mediates prediction. Decision matrix is `decision_table.csv`.

## B. Assets and splits

Use `model_qwen3_0p6b_base` at `/data/share/Qwen3-0.6B-Base`, saved revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd, original tokenizer, final A22 14layer/F16384 coder (`crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`, saved SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628). Do not substitute A17 official-a5 or another person's checkpoint.

Use original Tulu TRAIN1024dialogues/85548answer positions for discovery and exposed EVAL256/22446 for exploratory held-out analysis. Assets `data_tulu_sft_route_20261019t012300z` and `representation_tulu_sft_route_20261019t012300z` bind text/last-layer activation/joint-z cache. Join original id,dataset,prompt_sha256,row,input_ids,answer_start to cache block_id/position_id through original extract_sft.py. Remove discovery/EVAL prompt-hash overlap; near duplicates remain unknown. No DEV-based alternative selection, no TEST. DCLM10M is provenance/history only.

Keep complete prefixes, max512tokens; eligible answer-prediction position t has nonspecial current/next token, current piece contains a Unicode letter, and16scoreable answer targets remain. No window-truncated prefix or model-inferred label. Audit CPU joins before inference.

## C. Discovery and freeze

On TRAIN only, rank eligible token IDs by support then ID; each must have two most-supported distinct next tokens, yA/yB, each from≥64unique dialogues. Match identical v,dataset,16token answer-position bins,32token prefix-length bins and equal class-stratum weights. Take one position/dialogue/token by fixed SHA. Choose at most2tokens from TRAIN; never replace one due to EVAL insufficiency or intervention outcome.

Per token, candidate feature pool is union of top32absolute source14contribution features per class (≤64). Absolute amplitude is z_f*s14*||d14f||; also save relative amplitude against all-feature sum, zero denominator NA. C has≥80%hits in each class, MAD/positive median≤0.25, class gap≤0.25pooledSD; select up to2largest absolute contributors. R is disjoint, joint-z class gap≥0.8pooledSD; rank by gap, then ID. Orientation freezes here. Qualify the selected local readout; no layer/rescue search if it fails.

Functional margin M=logp(true next token)−logp(other class's frozen next token). Both single tokens; not a semantic feature name inferred from high activation. At native discovery and held-out baselines, each class must have≥60%contexts with M>0 and mean M≥0.20nat; otherwise the candidate lacks qualification for disrupting an existing contextual function. No candidate replacement or correctness-only filtering. Save target NLL, full16target CE and off-target positions2–16 CE. Frequency is recorded after selection: TRAIN hit-rate and token counts, positive-frequency quartiles, zero frequency NA; descriptive only with2candidates.

Discovery forward cap512 (≤256/token). Save5fixed-random examples/class and up to5counterexamples/type (low R in preferred class; high R in opposite class), with text/source/IDs/targets/selection rule; absence NA. Before any EVAL intervention outcome, freeze all IDs,layers,targets,readout vectors,matching sets and samples to hashed selection_freeze.json. Current IDs NOT_SELECTED.

## D. Dictionary and local readout qualification

Hooks are residual-post before final global RMSNorm. Fix source block14(index13,coder6) and target28(index27,coder13) as midpoint-to-final, not effect-selected. x_l=(h_l−mu_l)/s_l with frozen TRAIN mean[14,1024],scalar vector RMS[14]. Encoder u=ReLU(sum_l x_l E_l+b_enc); w_f=sum_l||d_lf||; z_f=u_f*1[u_f*w_f>tau]. Load complete tau/buffers, no refit/per-tokenTop256. Decode xhat_l=b_dec,l+sum_f z_f d_lf. Preserve original BF16GEMM/FP32master/score semantics.

Never re-encode intervened multi-layer values. Construct N from target-layer C directions, source-layer raw C directions in residual coordinates, and up to8highest-absolute-target28-contribution nuisance decoders selected on discovery, excludingR. Residualize d28R against N by SVD tolerance1e−6, normalize to q. Retained norm fraction must be≥0.20. Raw local r=q^T(x28−b_dec28); record discovery SD and standardize only once in S_R below; it is a directional score, not independent feature activation. Context discrimination S_R=sign(class)*(r−frozen discovery midpoint)/SD_discovery; retain raw scores.

Qualify on discovery and native held-out baselines: actual-vs-reconstructed local-score correlation≥0.80; RMS(q^T(x−xhat))/SD(r)≤0.50; local-score correlation with native joint z_R≥0.50; discovery class mean gap≥0.50SD in the prespecified direction, no posthoc sign reversal. Historical DCLM FVE14/28=0.994707923/0.864722113 and final replacement CE cost~0.305962nat are not current Tulu qualification. All thresholds are explicit operational proposals.

Numerical rules: nonfinite values fail; denominators≤1e−8 are undefined, except perfectly constant C with class gap≤1e−8 may count as stable. Native-cache NLL replay and native/zero-hook differences require absolute error≤2e−4nat; primary effects additionally exceed5times the corresponding no-op span. Native/zero-hook repeats use same precision/batches and record logit/loss/readout numerical noise; current runtime replay not yet done. Before the first authorized load, verify actual full weight hashes against saved SHA; mismatch stops, no download/substitution. Future qualification forwards≤512, including required cache replay/no-ops. Failure stops without relaxed gates, new dictionary training or extra layer search.

## E. Intervention and matched controls

Native frozen eval/no_grad/use_cache=False model is baseline; never reconstruct the whole activation as model baseline. For single position t, h14'=h14−alpha*s14*sum_C z0_f d14f,alpha0.05/0.10. z0 is from unperturbed complete forward, fixed across candidates. Keep other tokens,bias,other contributions and original residual; record BF16writeback error. This is offline all-layer-informed dosing, not online routing.

Each context has20independent conditions: native1,no-op1,C2,random5directions×2doses10,other3sets×2doses6. Fixed seed271828+context IDs, same random direction at both doses. Other sets match feature count and discovery activation/absolute amplitude (20%tolerance), excludeC/R, selected before held-out outcomes. Match each final actual displacement norm to C within2%; max32CPUscale adjustments, factor[0.5,2], no extra forwards. Unmatched contexts exclude the complete condition group, report reason; no outcome-based exclusion. C displacement/||h−mu14|| must be0.1%–2%, writeback error≤25%, actual/intended cosine≥0.95. Effective intervention and precise matching are qualifications, not H1 evidence.

Capture actual delta_h28 and delta_h14. After verifying native residual interfaces, delta_h28−delta_h14 is downstream block-write change; project using q/s28 to distinguish direct carry from later computation. H1 additionally requires same-direction positive corrected evidence after this carry removal. Raw projection alone cannot establish propagation. This does not identify a full circuit.

## F. Estimation and decision rules

Per token held-out max96contexts,24–48unique dialogues/class after matching. Insufficiency does not trigger token replacement. Conditions independent from the same origin; incomplete groups remain missing, not selectively mixed. All conclusions exploratory.

Effects e_R=S_R(native)−S_R(edit), e_M=M(native)−M(edit), positive means impairment. Average5random and3other sets within each context separately; compare C−each family. Cluster bootstrap10000draws,seed20261026,bydialogue with matched class/source strata; reuse document resampling keys across candidates. Direction draws are not model seeds. Report per-class/candidate/direction counts and values.

At most2candidates×2metrics×2families=8elementary one-sided tests, Bonferroni family alpha0.05, lower bootstrap quantile0.00625. At primary dose0.10, H1 operational support requires both control families: point Rdifference≥0.10discoverySD and margin damage≥0.02nat, corrected lower bounds>0; carry-adjusted Rcontrast same-direction lower bound>0 as additional conservative guard. Dose0.05secondary only, no rescue by changing dose/sign/absolute metric.

Generic-damage guard: each C-minus-control extra off-target CE (positions2–16) upper one-sided bound≤0.02nat/target. Otherwise H3 not excluded, even if both main metrics move. Report full16target and per-position losses as well. This guard does not prove model-wide specificity.

With passed qualification/effective intervention, upper corrected bounds below both practical thresholds weaken only dependence of at least that registered size. Broad intervals are insufficient, not independence. R-only/function-only results receive the narrower decision-table interpretation. No expert benefit, independent modules or pretraining order claim.

## G. Budget, authorization and outputs

Current forwards/interventions/training all0. After explicit future instruction: discovery≤512+qualification≤512+main≤3840=registered plan≤4864sequence forwards. Hard user cap12000counts every retry/baseline/cache-generation/intervention/score forward; max512tokens/sequence, no autoregressive generation/multitoken answer branch. Unspent cap does not authorize more candidates/layers/doses/samples. Resources unavailable or qualification/budget inadequate means stop and report; no allocation,training,deletion,router change or candidate model save.

Hash preparation protocol/config now; before authorized execution freeze actual worker/input manifests/scientific body. Freeze selection separately before held-out outcomes. Append amendments with whether outcomes were seen; do not overwrite historical results. Payloads execution-side under existing CrossCoder project. Deliver analysis only:1page summary,≤2main figures if evidence supports them,real random/counterexamples,paired tables and reproduction files. No meeting speaking script.

A–G ledger: researcher core and boundary explicit; numerical operational definitions proposed; metadata access/source binding passed, tensor loading/native replay/candidate/readout qualification NOT RUN; intervention authorization withheld. The later explicit protocol instruction enables only this bounded sequence, not a new routine per-step review flow.
