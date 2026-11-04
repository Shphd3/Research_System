派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/protocol.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/protocol.md)；研究修改仍回到原件。

---

# S07 Protocol: residual-preserving feature-combination interventions

## Purpose and authorization

The current follow-up explicitly authorizes this supplement after the complete main S06 experiment. S06 raw files, results, scripts, selected candidates and3.96MBpackage are frozen and preserved. Test whether perturbing candidate combinations changes native candidate-answer tendencies relative to matched interventions. Existing Anchors15_27_06/07 retain scientific ownership; original and observational hypotheses are not rewritten.

## Objects and exact injection

For each native SAE site separately, original code z and original hidden h are frozen observations. Decoder is b+Wz with columns W[:,i]. Change only chosen coordinates to z'. Inject h'=h+W(z'-z), using no decoder bias in the change. Then h'=(b+Wz')+(h-b-Wz), so the original reconstruction residual remains exactly. Columns are used at their actual stored scale; no renormalization. Both hidden tensors have width1024, dictionaries30000/ReLU-Top32. Attention output is block27.o_proj before residual addition. MLP input is after residual and post_attention_layernorm; do not confuse sites or add another RMSNorm there. All parameters remain frozen.

## Candidate, text and control freeze

Exact selection and every discovery intensity/frequency are in data/selection.json and candidate_match_audit.csv, frozen before intervention responses. Common lists are the original explicit-discovery H2 lists; nonempty recruit/loss groups use the first3original ranked members. Nothing is selected on main heldout success. Typical child patterns average the8discovery normalized common vectors, then normalize this mean. Main96unchanged heldout prefixes=64explicit(all8labels) plus32property fine. The explicit32fine prefixes determine target effects; offdomain/parent/negative rows expose generalized output shifts. Property failure cases remain descriptive.

Delete: set group z to zero, all other members unchanged. Control1 deletes a same-size other-member list selected on discovery frequency count±2/64 and positive intensity ratio[.5,2]. If none exists use the deterministic closest list but mark unqualified; this cannot establish specificity. Report actual active deletions and injected norm for every row. Control2 uses a same-active-count positive random combination on other active coordinates, scaled to exact representation norm; it is an addition/random-direction norm control, not a deletion matching claim. Count and norm controls answer different rivals.

Strength: for v=z_common, r=L2(v), source q=v/r and destination typical t, interpolate w=(1-alpha)q+alpha*t; set v'=r*w/L2(w). Alpha0,.25,.5,1pre-fixed. r=0is a zero intervention/ineligible, not a rescued new list. v'>=0; all original positives remain positive, but original zeros can become positive and are separately labeled identity-changing. The rest of z stays fixed. Record every old/new coordinate, feature ID, original/changed raw norm and whether values exceed combined discovery child min/max.

Strength controls: use the same members and a fixed cyclic permutation of destination typical coordinates (component-shuffled discovery pattern), and the own-side typical pattern; additionally intervene on other discovery-matched members using their typical patterns. Match their decoder-space norm to the candidate condition using a fixed65-point beta grid, then20bisection when a crossing exists, beta in[0,1]. Matching uses measured representations only, never scores; norm ratio outside.9–1.1is explicitly unmatched. No output-driven direction/strength selection. For parents/offdomain texts apply both destination patterns; primary in-domain child edit moves toward the opposite child, a controlled label-conditioned edit rather than an automatic router.

## Reading model scores and distributions

Same exact suffix and complete four2token candidates as S06, summed log conditional probabilities including period, no calibration. Report old/new scores, correct-sibling margin, correctness, first-word full-vocabulary ranks/probabilities, full top20token strings/probabilities plus remaining mass, entropy and KL from original distribution, and normalized four-complete-candidate probabilities. Candidate-set probabilities and full-vocabulary probabilities have different denominators. No causal claim from rank alone.

Last-block specialization: at only the final-prefix colon, a block27output/MLP edit cannot change hidden states at later candidate positions within this forward because there is no later attention layer. Their final-layer keys/values are formed before the edit. Thus complete period scores are invariant under this intervention; the first-word logits change. Cache the exact block27input, attention output and actual MLP input and recompute the nonlinear frozen tail and final head. This retains all downstream computation, not first-order attribution. Full-hook forwards on preselectedF09cat/car, both sites, identity/deletion/alpha.5must agree within1e-4FP32 for all4complete scores; native baselines on96prefixes replay main. If equivalence fails, use full forward rather than loosening tolerance.

## Judgments and uncertainty

Primary8comparisons:2SAEs×2domains×(common deletion and opposite-patternalpha.5), explicit heldout families only. Unit=family mean over the two children. Positive effect is loss of original correct-vs-sibling log-score margin; compare candidate loss with qualified matched deletion or norm-matched same-member shuffle. Need>=6/8 eligible families,4096family bootstrap95% interval, exact sign-swap p and Holm.05across8. All replacement groups, otheralphas,property,per-class/offdomain and distributions are reported as secondary/exploratory. If candidate and random effects are similar, no targeted specificity. If matching/active support is inadequate, specificity insufficient even if an intervention changes logits. Broad offdomain/KL shifts limit a semantic-directed interpretation. Opposite or negligible effects weaken the candidate's proposed local role without proving global irrelevance. Repeated score effect supports only these directions under this model/site/position/strength, not uniqueness, a true concept conversion or MoE expert dispatch.

## Execution and artifacts

Main completion receipt and all main hashes saved first. CPU2threads,4x128capture,32-lane tail batches; no GPU/cloud job, training or permanent checkpoint writes. Scientific/data/numerical audits precede effects. Preserve amendment history if needed. Save per-condition latent edits, actual hidden deltas/norms, all scores/ranks/distribution summaries, controls, family tables, counterexamples, at least2figures and bilingual reports. Package main+supplement<20,000,000bytes; weights/full logits omitted with exact index. Stop after scoped delivery. Researcher scientific acceptance and closure Unknown.
