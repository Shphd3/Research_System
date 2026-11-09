---
experiment_id: A15_02_07_E02_controlled_composition_full
anchor_id: 15_02_07_matched_semantic_complexity
status: APPROVED_FOR_FULL_RUN
canonical_language: en
approved_scope: implementation_and_one_full_run
approved: 2026-08-08
---

# Protocol: Controlled Composition 10-Layer Full Run

## 0. Approval Snapshot

- **Question:** in the same rule context and answer space, does requiring a two-edge composition rather than one-edge lookup move attention-induced MLP-input variance and conditionally new accessibility toward later local parameter ranks with depth?
- **Purpose:** test genuine composition separately from TAX while repairing the prior composition capability failure, external-cache replay failure, old/new headroom confound, small readout, three-layer coverage, and unreadable curves.
- **Experiment role:** controlled operationalization and proxy test.
- **Full scope approved:** the 2026-08-08 researcher instruction authorizes one repaired ten-layer COMP full run, separate COMP plots, analysis, and result records.
- **Treatment / control:** complex query starts at source \(U\) and requires \(U\to V\to C\); simple query starts at the matched intermediate \(V\) and requires only \(V\to C\).
- **Changed variable:** whether the query must compose two explicit mappings or read one explicit mapping.
- **Held fixed:** exact context, terminal answer, answer vocabulary, record count, class balance, prompt family within split, frozen model, layers, parameter basis, covariance estimator, readout family, bootstrap, and figure transformation.
- **Primary H1 / H2:** sampled late-minus-early change in complex-minus-simple rank centroid / conditional log-loss gain.
- **Capability gate:** restricted-choice confirmation accuracy at least 0.80 simple and 0.60 complex.
- **Pass / Fail / Insufficient:** lower 95% paired-bootstrap bound above zero / upper bound below zero / guard failure or interval crossing zero. H1 also requires positive DEVELOPMENT direction.
- **Cannot claim:** natural-language hierarchy, shared direction identity, causal model use, free-generation capability, training utility, or equivalence to TAX.

## 1. Terminology And Definitions

- **Episode:** one random bijection \(U\to V\) and one random bijection \(V\to C\) over eight symbols.
- **Simple query:** the prompt supplies the relevant \(V\) symbol; one rule retrieves the terminal code.
- **Complex query:** the prompt supplies the matched \(U\) symbol; two rules must be composed to reach the same terminal code.
- **Replicate:** eight episodes from each split grouped by `episode mod 8`; eight replicates are the paired independence units.
- **Restricted-choice capability:** whether the correct next-token code has the largest logit among the eight single-token codes A--H. It is a gate, not the H1/H2 metric.
- \(n^{old}\), \(\Delta n\), local parameter rank, conditional gain, and `Disc($\Delta n$)` have the same definitions as E02.

## 2. Anchor Alignment

This experiment adjudicates only the Anchor's COMP branch. It realizes the requested true compositional relation without mixing it with a conditional-fine taxonomy. The strongest rival is that a curve difference reflects prompt, answer, capability, saturation, or sample imbalance rather than the need to combine two relations.

## 3. Tested Hypotheses

- **H1-COMP:** complex-minus-simple \(\Delta n\) rank centroid moves later from sampled early to sampled late layers.
- **H2-COMP:** complex-minus-simple conditional information gain supplied by \(\Delta n\) increases from sampled early to sampled late layers.
- H1 and H2 are separately adjudicated; TAX evidence cannot support either COMP clause.

## 4. Rival Explanations

| Rival | Registered separator |
| --- | --- |
| different target labels or contexts | paired simple/complex records share context and terminal code |
| class/sample imbalance | both conditions have 8 classes and exactly 8 records/class/replicate/split |
| model cannot perform composition | restricted-choice confirmation gate, simple and complex separately |
| old/new saturation | frozen old readout plus delta-only logit correction |
| external hardware cache mismatch | same-run repeated first batch and direct site identity |
| individual episode drives result | eight paired replicate units and 2,000 paired bootstraps |
| smoothing creates pattern | exact arrays determine every metric; smoothing is display-only |

## 5. Data Construction And Provenance

- Generated data: `composition_full.json`, SHA-256 `341202eedccf635760aa43d2bd2936601258f29198d2881c3add59ad09e413b1`.
- Total: 3,072 records = 3 splits × 64 episodes × 8 terminal targets × 2 conditions.
- Every episode contains all 8 \(U\to V\) and all 8 \(V\to C\) rules in a deterministic random order.
- Every source produces one paired simple and complex query with the same context and terminal target.
- Terminal codes A--H are verified single tokens when preceded by a space; the prompt ends at `Answer:` and never contains the answer after the readout.
- Each split has an independent RNG seed and rule/query wording family.
- Eight replicates each contain 8 episodes/split, hence 8 examples per class/condition/split.
- Data generation cannot inspect model outputs or confirmation accuracy.

## 6. Learning Task And Supervision

The model is frozen. H1 uses confirmation target labels only to form 8 class centers. H2 uses TRAIN labels for fitting and DEVELOPMENT labels for ridge selection. CONFIRMATION labels are opened only for registered capability and H1/H2 reporting. The output is one of eight terminal codes; all task and replicate weights are equal.

## 7. Model, Layers, And Parameter Basis

- Frozen local Qwen3-8B, bfloat16 SDPA.
- Layers: 1, 5, 9, 13, 17, 21, 25, 29, 33, 36.
- Primary early sample: 1, 5, 9. Primary late sample: 25, 29, 33. Layer 36 is displayed only as the final boundary.
- Representation: exact post-attention RMSNorm increment \(\Delta n\) at `Answer:`.
- Parameter basis: native input Gram \(K_\ell=W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}\) from ten verified A15_02_06 files. Cross-layer ranks are order statistics only.

## 8. Readout Objective And Conditional Novelty

For centered one-hot TRAIN target \(Y_c\), base ridge solves

\[
\min_W N^{-1}\lVert Y_c-X_{old}W\rVert_F^2+\lambda\lVert W\rVert_F^2.
\]

After DEVELOPMENT selection freezes \(W\), the increment solves

\[
\min_U N^{-1}\lVert Y_c-L_{base}-X_{\Delta n}U\rVert_F^2+\lambda_\Delta\lVert U\rVert_F^2.
\]

The grid is \(\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}\); ties choose larger regularization. The primary conditionally new readout amount is

\[
CIG=CE^{conf}_{base}-CE^{conf}_{base+\Delta n}.
\]

`Disc($\Delta n$)=\log8-CE^{conf}_{\Delta n}` is reported separately as update readability and cannot rescue H2.

## 9. Conditions, Seeds, And Independence

- Conditions: simple one-edge versus complex two-edge, paired within context and target.
- Independence unit: eight replicate IDs, not layers, episodes, records, or directions.
- H1 paired bootstrap: 2,000, seed 2721. H2: seed 2722.
- Generation seeds: 2301 TRAIN, 2302 DEVELOPMENT, 2303 CONFIRMATION.
- No episode, target, task, layer, or direction may be filtered after output inspection.

## 10. Primary Metrics

For each replicate \(q\), condition \(d\), and eight terminal class centers:

\[
b^{(q)}_{\ell,d,i}=\frac17\sum_{k=1}^8(\mu_{qk,i}-\bar\mu_{q,i})^2,
\qquad b_{\ell,d,i}=\frac18\sum_qb^{(q)}_{\ell,d,i}.
\]

With normalized mass \(\pi_i=b_i/\sum_jb_j\):

\[
R_\ell=\sum_i\left(\pi_{\ell,complex,i}-\pi_{\ell,simple,i}\right)\frac{i-0.5}{4096}.
\]

The H1 statistic is median \(R\) on layers 25/29/33 minus median \(R\) on layers 1/5/9. The H2 statistic applies the same contrast to
\(G_\ell=CIG_{\ell,complex}-CIG_{\ell,simple}\).

H1 Pass requires positive confirmation point estimate, positive paired-bootstrap lower 95% bound, and positive DEVELOPMENT estimate. H2 Pass requires positive confirmation point estimate and positive lower bound. An upper bound below zero is Fail; otherwise Insufficient.

## 11. Mandatory Guards And Figures

1. Exact same-run first-batch attention replay.
2. Direct `o_proj` relative identity below \(10^{-5}\) at layers 1, 21, 36.
3. Projection reconstruction relative error below \(10^{-4}\) at every layer.
4. Exact schema and 8-class/8-replicate/split balance.
5. Mean augmented `Disc` over ten layers exceeds 0.1 nats/example in each condition.
6. Confirmation restricted-choice accuracy: simple \(\ge0.80\), complex \(\ge0.60\).
7. All direction variances finite/nonnegative and normalized masses sum to one.
8. Separate COMP ten-layer raw/normalized figure, exact thin lines plus centered 129-rank linear-domain mean before `log10`.
9. Separate COMP H1/H2 metric figure, complete task/replicate values, source tables, and manifests.

Failure of the capability gate makes H1/H2 `insufficient_guard`, even if a curve looks ordered.

## 12. Known Cases

- A single-direction class difference peaks in that direction.
- Identical class centers refuse normalization.
- Zero \(\Delta n\) yields zero conditional gain.
- Swapping simple and complex labels negates \(R\) and \(G\).
- Constant curves remain constant under smoothing.
- A model choosing one terminal code for every prompt fails balanced restricted-choice capability.

## 13. Stage Contract

| Stage | Operation | Evidence | Stop / eligibility rule |
| --- | --- | --- | --- |
| Preflight | Protocol/data/basis/GPU/schema checks | `preflight.json` | mismatch stops |
| Unit tests | balance, covariance, ridge no-op, smoothing | `unit_tests.log` | failure stops |
| Extract | 3,072 records, ten hooks, same-run replay | layer tensors, restricted logits, manifest | representation guard failure makes result insufficient |
| Capability | confirmation restricted-choice accuracy | capability table | threshold failure makes branch insufficient |
| H1 | replicate class centers and paired bootstrap | curves and H1 ledger | exact arrays only |
| H2 | frozen base plus delta correction | readout ledger | confirmation cannot select ridge |
| Render | COMP-only ten-layer and metric figures | PNG/PDF/contract | figures opened at full resolution |
| Finalize | typed branch outcome | result/manifest | no cross-branch pooling |

## 14. Output And Reproducibility

Worker code and raw outputs live under
`XingyuD/MoE_Routing_Experiments/active/a15_01_10_e02_e03_tax_comp_10layer_full/`.
Canonical E03 Protocol, summary, detailed record, and curated COMP figures live in this directory. The run stores Protocol, data, basis, environment, tensor, table, and figure hashes. No graph, sync, commit, push, or external package is authorized.

## 15. Typed Outcomes

- `joint_pass`, `h1_only`, `h2_only`, and `joint_fail` have their literal separate-clause meanings.
- `insufficient_mixed`: at least one CI crosses zero or H1 DEVELOPMENT reverses.
- `insufficient_guard`: capability, representation, provenance, numerical, or artifact guard fails.

## 16. Claim Boundary

An eligible result concerns only controlled in-context one-edge versus two-edge mapping under the registered prompt family. It cannot prove natural composition, free-generation reliability, shared directions, causal use by the MLP, knowledge storage, model training consequences, or equivalence to TAX.

## 17. Confirmation And Freeze Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question/boundary | CONFIRMED | Anchor separation of COMP and 2026-08-08 full-run request |
| B data/provenance | CONFIRMED | researcher request for true composition; deterministic paired construction |
| C task/supervision | CONFIRMED | same context/target, untouched confirmation |
| D model/architecture | CONFIRMED | frozen Qwen3-8B, requested ten layers, verified bases |
| E objective | CONFIRMED | delegated repair of H2 saturation and small-probe failure |
| F comparison/evidence | CONFIRMED | capability gate, H1/H2 metrics, separate COMP figures |
| G execution | CONFIRMED | explicit implementation and full-run authorization; two local H100s |

Cross-block consistency: `PASS`. This file is frozen before the first E03 model forward. Any outcome-changing modification requires an append-only amendment and explicit eligibility impact.

## 18. Append-Only Amendments

### Amendment A1 — remove rule-retrieval disorder after failed capability preflight

- **Time:** 2026-08-08, after the first E03 capability-only forward and before any ten-layer E03 extraction.
- **Before Protocol hash:** `c03262c11fe0197136c510bcda8b605cc832b041c572b4db0747f9b185f1ed9d`.
- **Before data hash:** `341202eedccf635760aa43d2bd2936601258f29198d2881c3add59ad09e413b1`.
- **Observed preflight:** restricted-choice simple accuracy 0.953125 passed; complex accuracy 0.53125 failed the registered 0.60 gate on 8 confirmation episodes / 128 paired records.
- **Before construction:** all sixteen \(U\to V\) and \(V\to C\) rules were randomly interleaved, so complex queries changed both relational depth and rule-retrieval disorder.
- **After construction:** preserve the same eight classes, bijections, targets, episodes, replicates, splits, record count, conditions, and answer tokens, but place sorted \(U\to V\) rules in Table 1 and sorted \(V\to C\) rules in Table 2. Add a label-free instruction to consult Table 1 and then Table 2 for a source query.
- **After data hash:** `bd8f29581c502c157785609ff8e87c157734e3e4caf934abcd2ba95c6f68ac77`.
- **Reason:** remove an unregistered retrieval-order nuisance so the condition difference more closely isolates one-edge lookup versus two-edge composition.
- **Affected blocks:** B data construction, C diagnostic task, F capability evidence. H1/H2 estimators, thresholds, layers, basis, readout, bootstrap, figures, and claim boundary are unchanged.
- **Approval:** the researcher explicitly authorized repair of smoke problems and full execution; this is the smallest capability-preserving repair after the registered preflight failure.
- **Eligibility:** the first capability preflight is retained as failed/ineligible evidence for the amended data. The amended data must pass the same unchanged 0.80/0.60 gate before E03 full extraction is eligible.
- **Execution boundary:** no TAX object changes. No full run, publication, sync, commit, or push is implied beyond the already approved E02/E03 local execution.
