# Detailed: A06_01_03_E06 Minimal-Prior M1/M2 Full Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

**Purpose:** test whether M2 continuous gradient weighting, which looked
promising in the 2-seed sanity check, remains useful across 8 controlled seeds.

**Hypothesis:** soft functional signal from per-token loss / hidden-gradient
norm may help select better centers than static all-token geometry.

**Conclusion:** weakened. M2 continuous does not beat raw all-token or M1 in
the full audit.

**Evidence:** route-only control mean `feature_NMI=1.000`; raw all-token
`0.863`; M1 `0.843`; M2 continuous `0.784`; M2 top-20% `0.756`.

## 1. Anchor Link And Decision Point

The anchor asks whether a no-label, no-position, no-route-prior center search
can find feature-controlling hidden-space gate centers. This full audit tests
the first two candidate operationalizations after a positive M2 sanity signal.

## 2. Protocol Compliance Audit

**Approved conditions match actual conditions:** yes. User approved the 8-seed
M1/M2 full audit. M3 was not run.

**Primary metric exists:** yes, held-out route-position `feature_NMI` in
`tables/full_sanity_methods.csv` and `tables/full_method_aggregate.csv`.

**Central figures/tables exist:** yes, table evidence is central. No central
figure is required for this audit.

**Seeds/checkpoints recorded:** yes, seeds `20260623` to `20260630`.

**Known good/bad/confusing reviewed:** yes. Route-only remains perfect. Raw
all-token is stronger at full calibration size. M2 continuous is seed-unstable.

**Success/failure/insufficient-evidence criteria applied:** yes. M2 continuous
is weakened because it does not beat raw all-token or M1 on mean `feature_NMI`.

## 3. Setup

**Data:** A06 controlled no-position `C4_all_position_scope`.

**Model:** one-layer Transformer plus top-1 MoE, `d_model=128`, `n_heads=4`,
`ffn_dim=256`, 4 features, 4 experts, sequence length 32, no positional
embedding.

**Full size:** each seed uses 12,288 calibration sequences and 12,288
evaluation sequences. Calibration produces 393,216 all-token hidden states.
The fitting cap is 20,000 states.

**Allowed method inputs:** all-token hidden states. M2 additionally uses
per-token next-token loss and hidden-gradient norm.

**Forbidden method inputs:** feature labels, position labels, slot offset, and
route-position membership. These are used only after center selection for
audits.

## 4. Metrics And Decision Rules

**Primary metric:** held-out route-position `feature_NMI`.

**Support criterion:** M2 continuous should beat raw all-token and M1 on mean
`feature_NMI`, with comparable or better load guards and no shortcut dominance.

**Weakening criterion:** M2 continuous matches or underperforms raw all-token /
M1, or improves only load / gap / label-free score.

## 5. Main Results

### Decision Evidence

| Method | Mean `feature_NMI` | Std | Min | Max | Mean max load | Mean active experts |
|---|---:|---:|---:|---:|---:|---:|
| route-only control | 1.000 | 0.000 | 1.000 | 1.000 | 0.250 | 4.000 |
| raw all-token | 0.863 | 0.073 | 0.707 | 1.000 | 0.469 | 3.000 |
| M1 static bootstrap margin | 0.843 | 0.090 | 0.707 | 1.000 | 0.469 | 2.875 |
| M2 continuous gradient weight | 0.784 | 0.126 | 0.621 | 1.000 | 0.530 | 2.750 |
| M2 top-20% gradient weight | 0.756 | 0.110 | 0.637 | 0.866 | 0.606 | 2.625 |

### Seed-Level Evidence

M2 continuous equals or beats raw in 4 of 8 seeds:

- `20260623`: raw `0.707`, M2 continuous `0.866`;
- `20260625`: raw `0.866`, M2 continuous `0.866`;
- `20260627`: raw `1.000`, M2 continuous `1.000`.
- `20260626`: raw `0.866`, M2 continuous `0.866`.

It is worse than raw in 4 of 8 seeds:

- `20260624`: raw `0.866`, M2 continuous `0.707`;
- `20260628`: raw `0.866`, M2 continuous `0.637`;
- `20260629`: raw `0.866`, M2 continuous `0.621`;
- `20260630`: raw `0.866`, M2 continuous `0.707`.

M2 continuous has the worst full-audit minimum among the three non-oracle
soft/static methods: `0.621`.

### Guard Evidence

Gradient extraction is valid: each seed has 380,928 valid functional tokens,
12,288 invalid last-position tokens, and zero non-finite gradient norms.

Leakage checklist passes: method selection uses hidden states and loss /
gradient norm; it does not use feature labels, position labels, or route
membership.

Shortcut guards are low for M2 continuous: position NMI is about `0.007-0.014`,
slot-start NMI is near zero, loss-bin NMI is about `0.001-0.007`, and
gradient-bin NMI is about `0.003-0.006`. This does not rescue the method; it
only says the failure is not explained by these simple guards.

M2 top-20% remains brittle. Many seeds show tiny high-norm clusters and one
large low-norm cluster, consistent with hard filtering being too aggressive.

## 6. Visualization Results

No central figure is used. The full-audit decision is table-based:

- `tables/full_method_aggregate.csv` decides the top-line result.
- `tables/full_sanity_methods.csv` gives seed-level primary metrics.
- `tables/full_leakage_checklist.csv` checks forbidden-input use.
- `tables/full_gradient_profile.csv` checks M2 feasibility.
- `tables/full_center_profile.csv` checks center generation and top20
  degeneracy.
- `tables/full_shortcut_audit.csv` checks simple shortcut explanations.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
|---|---|---|---|---|
| Hidden-state load | `tables/full_state_manifest.csv` | passed | none | data shape mismatch |
| Leakage audit | `tables/full_leakage_checklist.csv` | passed | none | label / position / route leakage |
| Gradient extraction | `tables/full_gradient_profile.csv` | passed | none | M2 implementation infeasibility |
| Center generation | `tables/full_center_profile.csv` | passed for M2 continuous; weak for top20 | top20 creates uneven clusters | empty-center failure for M2 continuous |
| Final audit | `tables/full_sanity_methods.csv` | M2 continuous failed support criterion | underperforms raw and M1 | M2 continuous as reliable route-relevance proxy |

**Falsified physical prior:** the broad prior that simple gradient-norm
weighting is a reliable route-relevance signal is weakened.

**Falsified mathematical model:** the current \(Q(C)\) plus soft gradient norm
does not predict better feature-center recovery.

**Falsified operationalization / proxy:** M1 static bootstrap margin, M2
continuous gradient weighting, and M2 top-20% gradient filtering as tested
here.

**Falsified implementation:** none.

**Falsified metric:** none.

**Remaining rival explanations:** the useful signal may require a different
functional object than gradient norm, a better center-selection score, or an
explicit self-discovered route-readout surface. Raw all-token may also become
strong simply because larger calibration data stabilizes generic centers.

## 8. Full Experiment Record

**Run name:** `full_m1_m2_8seed_20260626`

**Commands:**

```bash
python scripts/run_a06_19_minimal_prior_margin_aware_center_search.py \
  --config configs/a06_19_minimal_prior_margin_aware_center_search_full.json \
  --run-name full_m1_m2_8seed_20260626 \
  --seeds 20260623,20260624,20260625,20260626,20260627,20260628,20260629,20260630 \
  --methods raw_all_token,route_only_control,m1_static_bootstrap_margin,m2_gradient_weighted_continuous,m2_gradient_weighted_top20 \
  --num-shards 2 --shard-index 0 --device cuda:0
```

```bash
python scripts/run_a06_19_minimal_prior_margin_aware_center_search.py \
  --config configs/a06_19_minimal_prior_margin_aware_center_search_full.json \
  --run-name full_m1_m2_8seed_20260626 \
  --seeds 20260623,20260624,20260625,20260626,20260627,20260628,20260629,20260630 \
  --methods raw_all_token,route_only_control,m1_static_bootstrap_margin,m2_gradient_weighted_continuous,m2_gradient_weighted_top20 \
  --num-shards 2 --shard-index 1 --device cuda:1
```

```bash
python scripts/run_a06_19_minimal_prior_margin_aware_center_search.py \
  --config configs/a06_19_minimal_prior_margin_aware_center_search_full.json \
  --run-name full_m1_m2_8seed_20260626 \
  --aggregate-only --device cuda:0
```

**Execution:** local two-H100 run.

## 9. Interpretation

The sanity result was a false positive for method direction. It was useful as
an executability check, but not as evidence of a stable method.

The important update is negative: soft gradient-norm weighting is not a
reliable label-free route-relevance proxy in this controlled bridge. It can
help in some seeds, but it can also push centers into worse feature merges than
raw all-token.

The full run also changes the baseline picture. With larger calibration data,
raw all-token is much stronger than in the earlier small sanity and is close to
M1. That suggests the next diagnostic should not add another method first; it
should explain why raw all-token improves with sample size and why it still
falls short of route-only.

## 10. Claim Boundary

**Can claim:** M1 and M2, as implemented here, do not provide a reliable
minimal-prior center-search method in the controlled bridge.

**Cannot claim:** all functional signals fail, all gradient methods fail,
real-DCLM transfer is impossible, or preservation is impossible.

## 11. Next Decision

Do not test preservation with M1/M2 centers. Next diagnostic should isolate the
sample-size effect and feature-merge structure of raw all-token versus M2
continuous before adding M3 or another method.

## 12. Links And Artifact Map

**Anchor:**
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

**Protocol:** `protocol.md`

**Summary:** `summary.md`

**Code workspace:**
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

**Runner:**
`scripts/run_a06_19_minimal_prior_margin_aware_center_search.py`

**Full config:**
`configs/a06_19_minimal_prior_margin_aware_center_search_full.json`

**Curated config snapshot:**
`scripts/a06_19_minimal_prior_margin_aware_center_search_full.json`

**Result dir:**
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_19_minimal_prior_margin_aware_center_search/full_m1_m2_8seed_20260626`

**Key tables:**
`tables/full_method_aggregate.csv`,
`tables/full_sanity_methods.csv`,
`tables/full_gradient_profile.csv`,
`tables/full_leakage_checklist.csv`,
`tables/full_center_profile.csv`,
`tables/full_method_candidates.csv`,
`tables/full_shortcut_audit.csv`,
`tables/full_state_manifest.csv`

**Logs / checkpoints:** no checkpoints; terminal output only.

**Job id:** local run, no scheduler job id.
