# A06_03_04_E03 Tail-Safe Utility Certificate: Detailed Record

## 0. Decision Recap

**Purpose:** Test whether lower-tail pairwise expert utility prevents the
premature stopping produced by population-mean utility.

**Result:** q10 and lower-CVaR10 pass all registered method thresholds. q25
reduces but does not eliminate the safety failure. Task-position filtering is
not required.

**Decision:** Close the controlled certificate refinement. Move to a real
workload functional-heterogeneity audit before joint-training or architecture
claims.

## 1. Terminology / Definitions

| Term | Concrete meaning | Metric | Decides | Cannot prove |
|---|---|---|---|---|
| Pairwise utility | Forced-loss advantage of the incumbent over one challenger | \(D_{e,c}=\ell(E_c)-\ell(E_e)\) | Which expert is functionally better | Long-run causality |
| q10 | 10th percentile of per-token \(D_{e,c}\) | \(Q_{0.10}(D)\) | Whether at least the lower tail favors the incumbent | A latent semantic group |
| lower-CVaR10 | Mean utility among values at or below q10 | \(\mathbb E[D\mid D\le Q_{0.10}]\) | Severity of the worst utility tail | Systems risk |
| Premature stop | Certificate stops before sustained useful-route correction | binary per task cell | Safety of the phase switch | Downstream quality |
| Audition saving | Fraction of the 600 maximum two-expert updates avoided | \(1-N_{audition}/600\) | Training activated-compute proxy | Wall-clock speedup |

## 2. Protocol Compliance And Validity

| Requirement | Observed | Status |
|---|---:|---|
| Full seeds | 32 | pass |
| Task cells per condition | 128 | pass |
| Specialist held-out utility gap | 8.8947 | pass, required \(>5\) |
| Generalist utility gap | -0.00424 | pass, required absolute value \(<0.5\) |
| Useful-expert rank accuracy | 1.000 | pass |
| Minimum adjacent score-gap p05 | 0.4731 | pass, required \(\ge0.4\) |
| Initial top-1 load spread | 0 | pass |
| Fixed-600 correction reproduction | 1.000 | pass |
| q10 / CVaR generalist trigger | 0 / 0 | pass |
| Finite training and evaluation values | all | pass |
| ACP full run | `pt-oul045lr`, `SUCCEEDED` | pass |

The certificate matrix begins at NaN and cannot produce a finite minimum until
all 12 directed expert pairs have been observed. Non-finite training loss raises
an error. Quantiles are computed deterministically from the already executed
incumbent and challenger losses.

## 3. Data, Model, And Training

- Data: the A06_03_01_E01 context-defined four-task next-token construction, with
  instruction-dependent and background positions under full-sequence LM loss.
- Model: one causal-attention layer, residual and LayerNorm, no learned position
  embedding, four trained MLP experts, and weighted top-1 routing.
- Expert state: 200 expert-only exposure updates create specialists before the
  rank-4 router state is installed.
- Intervention: freeze experts and representation; vary only the functional
  used to aggregate per-token pairwise utility.
- Optimizer: router-only SGD, learning rate `0.001`.
- Horizon: at most 600 continuous pair auditions, total 800 updates.
- Replication: 32 seeds and four tasks per seed.

## 4. Mathematical Contract

For each routed incumbent/challenger pair,

\[
D_{e,c}(h)=\ell(E_c(h))-\ell(E_e(h)).
\]

The original mean rule tests

\[
\mathbb E[D_{e,c}]>0.
\]

The tail rules test

\[
Q_q(D_{e,c})>0
\]

or

\[
\operatorname{CVaR}^{low}_q(D_{e,c})
=\mathbb E[D_{e,c}\mid D_{e,c}\le Q_q(D_{e,c})]>0.
\]

Every directed pair statistic uses EMA decay 0.9. Stopping requires all 12
statistics to remain positive for nine assignment-stable updates.

## 5. Complete Decision Table

| Condition | Correction | Retention | Premature | Trigger | Median stop | Saving | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| fixed600 | 1.0000 | 1.0000 | 0 | 0 | 600.0 | 0 | reference |
| oracle route | 1.0000 | 1.0000 | 0 | 1.0000 | 242.5 | 0.5958 | oracle lower bound |
| mean | 0.9922 | 1.0000 | 0.1875 | 1.0000 | 220.5 | 0.6325 | unsafe |
| q25 | 1.0000 | 1.0000 | 0.0703 | 1.0000 | 245.5 | 0.5908 | fails 5% safety |
| q10 | 1.0000 | 1.0000 | 0 | 0.9375 | 294.0 | 0.5100 | pass |
| lower-CVaR10 | 1.0000 | 1.0000 | 0 | 0.6563 | 342.0 | 0.4300 | pass |
| task-oracle q10 | 1.0000 | 1.0000 | 0 | 1.0000 | 264.5 | 0.5592 | oracle source guard |

q10 triggers in 30/32 seeds and lower-CVaR10 in 21/32. Non-triggering seeds
continue audition to 600, so they sacrifice saving rather than safety. q25
still stops prematurely in 9/128 cells; the mean stops prematurely in 24/128.

## 6. Mechanism Interpretation

The aggregation functional is the only intervention. q10 waits a median 73.5
updates longer than the mean, and lower-CVaR10 waits 121.5 updates longer. This
delay removes all registered premature stops while retaining positive median
savings.

The result supports the narrow mechanism that mean utility can be positive
while a lower utility tail is unresolved. It does not prove that each low-tail
token belongs to a stable semantic class; q10 is a distributionally robust
statistic, not a discovered feature label.

The all-position q10 pass also rejects the need for oracle task-position
selection in this controlled system. MTP or another semantic-credit estimator
is therefore not required for the current stopping contract.

## 7. Visualization Results

### Figure 1: Tail-Certificate Reliability And Saving

![Tail-certificate reliability and saving](figures/tail_certificate_tradeoff.png)

- **Purpose:** Jointly audit safety and activated-compute saving.
- **Setup:** Same specialists, rank-4 state, and training trajectory family;
  only utility aggregation changes.
- **How to read:** Correction must exceed 0.9, premature stop must be at most
  0.05, and saving must exceed 0.3.
- **Observed:** q10 and lower-CVaR10 pass all three requirements; q25 misses the
  premature-stop requirement.
- **Take-home:** A useful tail depth exists in the tested four-expert system.
- **Uncertainty:** The exact 10% level is not claimed universal.

### Figure 2: Phase-Switch Margin Dynamics

![Tail-certified phase-switch dynamics](figures/tail_stop_margin_trajectories.png)

- **Purpose:** Show how conservative certificates alter switch timing and final
  route geometry.
- **Setup:** Median useful-expert margin through the 800-update horizon.
- **How to read:** Positive margin means the useful expert is above its strongest
  competitor; curve bends reflect different stop times.
- **Observed:** Tail rules delay switching and preserve positive final margins.
- **Take-home:** Safety is obtained by waiting, after which ordinary top-1
  exploits the corrected identity.
- **Uncertainty:** Median curves cannot adjudicate task-cell tail failures; the
  cell-level table is primary.

## 8. Hypothesis Adjudication

| Hypothesis | Verdict | Evidence |
|---|---|---|
| H1 at least one non-oracle tail rule passes | supported | q10 and lower-CVaR10 pass |
| H2 mean is Pareto-optimal | rejected | safe rules retain 43--51% median saving |
| H3 task-position tail is required | rejected | all-position q10 passes |
| H4 token tail is the wrong unit | rejected on this surface | token-level q10/CVaR pass |

## 9. Operational Run Record

The first local smoke used the default Python environment and failed before
model execution because of an ONNX/protobuf package incompatibility. Repeating
the two-seed smoke in the protocol-matched `spectral-hier` environment passed
all validity guards. No experiment logic or threshold changed.

- Smoke: `a06_45_smoke_20260711_02`, two seeds, local H100.
- Full job: `pt-oul045lr`, four H100 GPUs, `SUCCEEDED`.
- Full run: `a06_45_full_4gpu_20260711_01`.
- Existing earlier aggregation and the formal rerun have identical
  `condition_summary.csv` SHA-256:
  `e869318c15c4ab889ef2c3702a2c5b237bd9a5c2cf6f8f87c26f6f005327202f`.
- The decision JSON differs only in generation timestamp.

## 10. Claim Boundary And Next Decision

**Supported:** Tail-safe stopping for continuous bounded audition in a frozen,
four-expert synthetic specialist system.

**Not supported:** Joint co-adaptation, natural-language/code specialization,
pretrained-LLM transfer, many-expert statistics, inference-time audition, or
systems speedup.

**Next decision:** Before transferring the Router, determine whether a real
repository-level code workload contains stable held-out expert utility gaps and
nonzero oracle routing headroom. If not, semantic Router design should stop for
that workload.

## 11. Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`
- Protocol: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E03_tail_safe_certificate/protocol.md`
- Summary: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E03_tail_safe_certificate/summary.md`
- Curated figures: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E03_tail_safe_certificate/figures/`
- Curated tables: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E03_tail_safe_certificate/tables/`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_45_tail_safe_utility_certificate.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_45_tail_safe_utility_certificate.json`
- Submitter: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_45_tail_safe_utility_certificate_4gpu_acp.sh`
- Raw results: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_45_tail_safe_utility_certificate/a06_45_full_4gpu_20260711_01/`
- Logs: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a06_45_full_4gpu_20260711_01_*.log`
- ACP job: `pt-oul045lr`.

Reproduction:

```bash
A0645_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_45_full_4gpu_20260711_01 bash scripts/submit_a06_45_tail_safe_utility_certificate_4gpu_acp.sh
```
