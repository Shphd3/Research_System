# Summary: A15_13_E19 A/B Paired Router-Input Readout Re-audit

Primary Anchor: [A15_13_07](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `FULL_STATIC_MATRIX_COMPLETE`; registered qualification result `QUALIFICATION_FAILED`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 1. Purpose

Determine where parent and true-parent-conditioned child labels become stably readable at the exact maintained Router input A, while using MLP input B and a fixed nonlinear probe only as paired representation diagnostics.

## 2. Hypothesis

Site A should contain a reproducible three-block joint linear-readability plateau that survives both probe seeds and every frozen data, tensor, numerical, and shuffled-label qualification gate. The strongest rival is that the old block-9 description came from site B, one probe seed, packed-window dependence, or an invalid shuffled-label null.

## 3. Analysis Method

- Fit A/B-matched linear parent and conditional-child probes for seeds `170903/170907`, with the base frozen and all data, initialization, ordering, budget, mask, and aggregation held fixed; only A may select layers.
- Reconstruct contributing article identities and packed offsets, reject known cross-split article/title overlap, and run 2,000 paired connected-article-component resamples to expose packed-window dependence.
- Apply every frozen shuffled-label guard, and separately compare the linear head with the fixed `1024 → 32 → 3` GELU diagnostic; neither B nor the nonlinear probe may rescue or move an A candidate.

## 4. Conclusion

Verdict: `QUALIFICATION_FAILED`; the pre-authorized stop branch was taken and the A15.15 functional job was **not submitted**.

1. The point-estimate A-only selector produced the descriptive layer set **shallow `0`, primary `10`, deep `13`**. Both seeds independently selected primary block `10` with seed gap `0`, but **5 of 16 frozen null checks failed**. The candidate set is therefore not qualified and cannot authorize functional training.
2. The representation-site comparison is consistent and descriptive: A linear parent and child readouts first stabilize at block `10`, whereas B stabilizes at block `9`, for both seeds and both splits. B cannot move the maintained Router input or the A-only selector.
3. The fixed nonlinear diagnostic did not reveal a reproducible earlier A-site transition. At block `10`, its two-seed mean CE advantage over the linear head was only `0.008301/0.004896` nats for parent/child on development and `0.008019/0.005395` on historical confirmation. Its A-site parent onset was `10/10` across seeds, while child onset was `10/21`; this is not evidence that an earlier semantic code was hidden only by linear capacity.

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
|---|---|---|---|---|
| A-only two-seed point selector | primary `10`; shallow `0`; deep `13`; seed primaries `10/10` | Candidate existence and seed-gap guards pass | Descriptive candidate set only | [candidate_review.json](../../../../../../../../MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/runs/full-20260907T043632Z/analysis/candidate_review.json) |
| All 16 shuffled-label checks pass | 11 pass, 5 fail | Hard gate; no secondary metric can rescue it | **`QUALIFICATION_FAILED`** | [shuffle table](tables/shuffle_qualification.csv) |
| Exact tensor and causal-prefix contract | A/B `[28,2,192,1024]`; A/B mean absolute difference `1.652788`; both future-suffix prefix changes `0`; trainable base parameters `0` | Pass | Correct distinct read sites | [tensor contract](../../../../../../../../MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/runs/full-20260907T043632Z/preflight/tensor_contract.json) |
| Traceable articles and no known cross-split reuse | ambiguous selected occurrences `0`; normalized-title and exact-content overlaps all `0` | Pass, but some cells have only 1--5 connected components | Eligible guard with low-information interval limitation | [article manifest](../../../../../../../../MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/runs/full-20260907T043632Z/preflight/article_manifest.json) |

The five failed null rows are:

| Split | Site / seed / task | Median shuffled CE | CE rule | Median shuffled accuracy | Accuracy rule | Failed component |
|---|---|---:|---:|---:|---:|---|
| Development | A / 170903 / child | `1.153792` | `≤1.148612` | `0.314598` | `[0.28,0.39]` | CE |
| Historical confirmation | A / 170903 / child | `1.153555` | `≤1.148612` | `0.313553` | `[0.28,0.39]` | CE |
| Historical confirmation | B / 170903 / child | `1.148744` | `≤1.148612` | `0.313740` | `[0.28,0.39]` | CE |
| Development | B / 170907 / parent | `1.075425` | `[1.048612,1.148612]` | `0.405360` | `[0.28,0.39]` | Accuracy |
| Historical confirmation | B / 170907 / parent | `1.073470` | `[1.048612,1.148612]` | `0.408082` | `[0.28,0.39]` | Accuracy |

### Important Figures

![Paired linear A/B recovery](figures/01_ab_linear_recovery.png)

How to read: lower panels are the conditional-child task and upper panels the parent task; the red B curves cross the three-layer `0.95` rule at block `9`, while the blue A curves do so at block `10`. The shaded range is the two probe seeds, not independent model replicates.

![Router-input linear versus nonlinear readout](figures/02_a_linear_vs_nonlinear.png)

How to read: lower CE is better; the fixed nonlinear and linear A-site curves nearly overlap around block `10`, and the nonlinear diagnostic does not yield a reproducible earlier onset. This does not rule out every nonlinear code or prove optimization of the nonlinear probe was globally optimal.

![Shuffled-label qualification](figures/03_shuffle_qualification.png)

How to read: bars show shuffled median CE relative to random three-way CE; red marks a failure of any registered null component. Three red rows exceed the CE band and two red rows fail the separate accuracy band, so the combined gate fails even though every shuffled stable-onset check is absent.

### Claim Boundary

Can claim: under the frozen paired probe contract, site A has a descriptive joint linear-readability onset at block `10`, one block later than site B, and the fixed nonlinear diagnostic supplies no reproducible earlier A-site onset.

Cannot claim: that `{0,10,13}` is a qualified insertion set; that block `10` improves online routing, expert utility, or next-token prediction; that B should replace A; that the historically viewed confirmation split is new independent confirmation; or that connected-component intervals are highly informative in cells dominated by one giant packed component.

### Next Step Analysis

Decision: execute the already-confirmed `STOP_NO_FUNCTIONAL_LAUNCH` branch; no A15.15 job is authorized by E19.  
Why it follows: the Protocol defines any single hard-gate failure as sufficient for `QUALIFICATION_FAILED`; five occurred.  
Unresolved uncertainty: whether the null failures reflect probe/null optimization behavior, packed-window dependence, or a more basic mismatch between the frozen null rule and this paired-seed design.  
Completion criterion: the E19 static matrix, candidate review, and bounded canonical record exist; no relaxed threshold or substituted site is used.  
Stop or redirect condition: already met by the null failures.  
Resume action: `UNKNOWN` pending researcher confirmation of the result boundary and a separately approved next research decision.

## Evidence Map

- [Stable layers and candidate-point metrics](tables/readout_stable_layers.csv)
- [Two-seed linear recovery curves](tables/linear_recovery_mean.csv)
- [Linear versus nonlinear CE](tables/nonlinear_comparison.csv)
- [Connected-article-component bootstrap](tables/candidate_bootstrap.csv)
- [All shuffled-label checks](tables/shuffle_qualification.csv)
- [Figure contracts](tables/figure_contracts.json)
