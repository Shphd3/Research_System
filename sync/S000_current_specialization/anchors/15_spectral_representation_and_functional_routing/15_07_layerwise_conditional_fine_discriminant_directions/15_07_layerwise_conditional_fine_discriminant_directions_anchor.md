---
anchor_id: 15_07_layerwise_conditional_fine_discriminant_directions
status: EXECUTION_APPROVED_RUNNING
canonical_companion: 15_07_layerwise_conditional_fine_discriminant_directions_anchor_cn.md
active_focus: ../../../../../../daily_research_reports/backup/2026/08/0820/focus_stable_domain_discriminant_subspaces.md
parent_line: 15_spectral_representation_and_functional_routing
created: 2026-08-10
updated: 2026-08-20
---

# A15_07: Held-Out Function And Spectral Location Of Supervised Low-Rank Subspaces


## 1. Problem Definition

A15 has already shown on one opened controlled confirmation bank that the
candidate layer update at Qwen3-8B blocks 24 and 28 can add fine-class
classification function beyond the old state. A supervised reduced-rank ridge
regression (RRR) map retained that gain in eight requested input directions per
domain, while one shared basis needed 56 directions to retain at least 90% for
every domain. Those learned directions overlapped little across domains and
were concentrated outside the largest-variance principal-component analysis
(PCA) head. Because the confirmation bank used for those observations is now
open, it cannot validate the post-hoc rank-8, rank-56, or spectral-band claims.

For old normalized state $X_\ell$ and the same-token normalized state after
the attention write $Z_\ell$, define

$$
U_\ell=Z_\ell-X_\ell,\qquad
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell].
$$

$R_U$ is a candidate layer update after subtracting a TRAIN-fitted linear
prediction from the old state. It is not new knowledge and may still contain
nonlinear recoding, residualizer error, or task-irrelevant variation. A
**functional low-rank subspace** is therefore defined by held-out task gain
retained after projecting $R_U$, not by covariance rank, class count, or
coefficient rank alone.

**Single decision question:**

> After freezing the previously learned task-specific rank-8 and shared
> rank-56 subspaces, do they preserve the registered $R_U$ fine-class gain on
> fresh controlled expressions, which TRAIN-identifiable PCA bands carry that
> held-out function, and does the same qualitative relation—task-local low
> dimension but a larger shared dimension—replicate after a full-$R_U$ entry
> gate on natural hierarchical intent data?

The controlled track validates the exact prior candidates. The natural track
tests external transport and may stop at its entry gate. The two tracks are not
pooled into one p-value or used to rescue one another.

## 2. Physical Priors

1. **Task function and total variance are different objectives.** PCA orders
   reconstruction energy; a supervised correction orders reduction of
   classification loss beyond $X$. A useful direction can therefore lie in a
   lower-variance, but still TRAIN-identifiable, spectral band.
2. **Geometric alignment is not functional evidence.** Projector overlap says
   where a learned map points. A band is functionally sufficient only when
   keeping it helps on untouched data, and functionally necessary only when
   deleting it hurts the frozen low-rank correction.
3. **Several local task maps may require a larger union.** If domain-local
   maps point in partly different directions, one common basis can still serve
   all tasks but should require more dimensions than each local map. A natural
   replication is admissible only after full $R_U$ itself improves over $X$.

## 3. Falsifiable Hypotheses

**H1 — controlled held-out function.** On a sealed expression panel that uses
new templates and fact combinations, full $R_U$ passes the prior admission
gate at at least one registered block, the frozen task-specific rank-8 maps
retain at least 80% of full-$R_U$ gain for every domain, and the frozen shared
rank-56 basis retains at least 90% for every domain. A second panel containing
new source propositions is a stronger transport test; failure there limits the
claim to expression generalization rather than invalidating a pass on the
primary expression panel.

**H2 — functional spectral location.** Within the pooled TRAIN-identifiable
PCA span, the frozen supervised maps are not uniformly allocated across five
registered equal-width bands. A band is called function-bearing only when its
overlap exceeds a conditional Haar null and either its keep-only gain is
positive or deleting it reduces the frozen low-rank gain on sealed data.

**H3 — natural external replication.** On the official English MASSIVE
TRAIN/DEVELOPMENT/TEST split, at least one registered block first shows a
positive full-$R_U$ loss gain over $X$ beyond matched duplicate-$X$ and
within-domain mismatched-$R_U$ controls. Conditional on that gate, a supervised
task-local subspace reaches 90% of full-$R_U$ gain in fewer dimensions than a
single shared basis needed to reach the same all-task threshold, and their
spectral locations are measured under the same conditional baseline.

**Strongest rival.** The earlier result may be a small-sample synthetic or
opened-confirmation artifact: the exact spaces may fail on new expression
families, and natural prompts may have no independent $R_U$ gain after $X$.
That outcome weakens transport, not the arithmetic correctness of the earlier
opened-bank result.

## 4. Mathematical Model

For task/domain $p$, let the frozen supervised correction map be
$B_p\in\mathbb R^{4096\times C_p}$, with orthonormal input basis $Q_p$ from its
left singular vectors. The prior controlled candidates use
$\operatorname{rank}(Q_p)=8$ and shared basis
$Q_{sh}\in\mathbb R^{4096\times56}$ learned from equally Frobenius-normalized
task maps.

Let $V=[v_1,\ldots,v_{d_{id}}]$ be PCA of pooled TRAIN $R_U$, retaining only
numerically identified nonzero directions. Partition the ordered columns into
five registered bands $V_b$. For a rank-$r_p$ projector $P_p=Q_pQ_p^\top$,

$$
C_{p,b}=\frac{\lVert V_b^\top Q_p\rVert_F^2}{r_p}.
$$

$C_{p,b}$ is the fraction of subspace orientation in band $b$. Under a
uniform rank-$r_p$ orientation conditioned on the same identifiable span,
$\mathbb E[C_{p,b}]=d_b/d_{id}$; the ambient $r_p/4096$ baseline is invalid
when the learned maps lie almost entirely in a smaller TRAIN span.

For the frozen map, define its band component
$B_{p,b}=V_bV_b^\top B_p$. With frozen $X$-only logits $f_X(x)$, keep-only and
drop-one predictions are

$$
f^{keep}_{p,b}=f_X+B_{p,b}^\top R_U,\qquad
f^{drop}_{p,b}=f_X+(B_p-B_{p,b})^\top R_U.
$$

Held-out cross-entropy reduction over $f_X$ is the functional unit. Keep-only
tests sufficiency; the loss of gain from drop-one tests necessity. Neither
alone is a causal claim about native model use.

## 5. Computational Realization

### Controlled confirmation

- Freeze Qwen3-8B, blocks 24/28, token and hooks, E03 TRAIN residualizers and
  standardizers, task-specific rank-8 states, shared rank-56 bases and heads,
  and pooled TRAIN PCA before any new activation is opened.
- Construct two balanced panels with eight domains, eight fine classes and 30
  rows per cell. C4-expression uses old source propositions only in unseen
  templates and combinations. C4-atom uses independently sourced, frozen new
  propositions and separate templates. Exact text, source revision, label
  leakage, record ID, normalized text, template and proposition receipts are
  hashed before representation extraction.
- Fit nothing and choose nothing on either panel. Evaluate full $R_U$, the
  frozen task rank-8 maps, the frozen shared rank-56 heads, matched random
  rotations, spectral keep-only and spectral drop-one variants.

### Natural external replication

- Use MASSIVE 1.0 English `en-US`, where `scenario` is the coarse domain,
  `intent` is the fine class, `utt` is the permitted text, and `partition` is
  the official TRAIN/DEVELOPMENT/TEST role. Select five domains using only
  TRAIN/DEVELOPMENT schema and counts: email, transport, and the four most
  frequent TRAIN intents from each of IoT, play and question answering. Every
  task has four intents; no TEST value enters selection.
- Prompt each row as `User request: <utt>\nClassification:`. Fit the same type
  of TRAIN-only linear residualizer and TRAIN standardizer. Within each domain,
  use $X$ to fit a base classifier and RRR on $R_U$ to fit a correction. Use
  DEVELOPMENT only for ridge selection. TEST is opened once after code,
  selected labels, hyperparameters, controls and thresholds are frozen.
- First compare full $R_U$ with duplicate-$X$, within-domain mismatched-$R_U$
  and label-permutation controls. Only admitted layers receive local ranks
  $\{1,2,3\}$, shared ranks $\{1,2,3,5,8,12,15\}$ and five-band analyses.

All source code, caches, raw runs and logs live under
`/data/250010109/MoE_Router`. This Anchor owns no run command or artifact
manifest; those are frozen in the linked Protocol.

## 6. Minimal Falsification Tests

The primary controlled estimand is the weaker-panel, weaker-domain held-out
gain retention of the frozen task rank-8 and shared rank-56 systems, after the
full-$R_U$ entry gate. H1 passes on C4-expression only if simultaneous 95%
lower bounds exceed 0.80 and 0.90 respectively. C4-atom is reported as a
separate stronger-transfer outcome.

H2 requires, for at least one admitted layer and band, both overlap above the
conditional-Haar 95th percentile and positive held-out functional evidence
from keep-only or drop-one. A high overlap without function is location only;
function without excess overlap means the map is distributed within the
registered partition.

The natural track first requires a simultaneous 95% lower bound above zero for
full-$R_U$ cross-entropy gain beyond the stronger matched control. If this gate
fails, all natural low-rank and spectral verdicts are `NOT_APPLICABLE`. If it
passes, H3 requires the all-task 90% crossing of the shared basis to be larger
than the maximum local-task 90% crossing. Point crossings whose interval does
not clear the threshold are reported `UNCERTAIN`, not rounded into a pass.

The statistical unit is an example nested inside a fixed named domain; paired
stratified bootstrap resamples examples within every domain-by-class cell.
Domains are equally weighted. Claims are conditional on these named domains,
model and layers, not on a population of all domains or models.

## 7. Current Evidence

1. The opened E03 result established positive full-$R_U$ held-out gain at
   blocks 24 and 28 on the earlier controlled bank. Task-specific requested
   rank 8 recovered the registered 80%/90% curves, while PCA needed many more
   coordinates. This is the candidate source, not confirmation for H1.
2. The opened shared analysis found an all-task 90% crossing at 56 shared
   dimensions versus 8 requested dimensions per task. Off-diagonal task-basis
   overlap was 0.0127 at block 24 and 0.0179 at block 28. Because more than
   99.98% of each learned task basis lies in the 639-dimensional TRAIN PCA
   span, the relevant random-overlap expectation is about $8/639=0.0125$, not
   $8/4096$. Thus block 24 is near the conditional random baseline and block
   28 only modestly above it; “nearly disjoint” remains a conditional geometric
   description rather than proof of unrelated semantics.
3. The opened spectral diagnostic used a different rank-7 centered
   discriminant projector. It placed roughly 68--70% of mass in PCA ranks
   257--639, but it cannot by itself locate the exact rank-8 and shared rank-56
   functional maps or show held-out band function.
4. CLINC150 is a natural hierarchical negative boundary: under the previous
   registered admission statistic, full $R_U$ did not clear the old-state and
   mismatch controls at blocks 24 or 28. It therefore supplied no admissible
   natural low-rank verdict. MASSIVE is a new external dataset, not a rescue of
   CLINC150.
5. The present C4 and MASSIVE results are `NOT RUN` at Anchor revision time.

## 8. Claim Boundary And Next Decision

A complete Pass can support only this bounded statement: for frozen Qwen3-8B
blocks 24/28 and the registered linear tasks, supervised low-rank correction
directions retain function on new controlled expressions, align with specified
TRAIN-identifiable spectral bands for functional rather than variance reasons,
and show the same local-versus-shared dimension ordering on one natural
hierarchical intent dataset after a full-$R_U$ gate.

A controlled-only Pass with natural failure supports an existence result under
the controlled construction and weakens external transport. A failure on the
primary expression panel weakens the stability of the exact prior spaces. A
natural entry failure says only that this dataset/hook/layer combination does
not admit downstream low-rank interpretation.

No outcome establishes native causal use, new knowledge, expert utility,
Router quality, LoRA mechanism, forgetting resistance, or transfer across
models, languages and layers.

**Exactly one next decision:** after the two tracks produce canonical
`summary.md` and `detailed.md`, decide whether “functional low rank outside the
PCA head, with a larger shared union” is credible enough to become a candidate
prior for a separate Router experiment. Completion requires the researcher to
state the direct result, updated judgment, cannot-claim boundary and this one
decision in the active Focus; only then may a reader-facing daily report be
written.
