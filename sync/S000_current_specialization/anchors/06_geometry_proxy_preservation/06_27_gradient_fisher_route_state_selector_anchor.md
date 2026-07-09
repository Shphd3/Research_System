# Anchor: A06_27 Gradient/Fisher Route-State Selector

## 0. Thinking Card

**Phenomenon:** all-position hidden-state clustering improves with warmup but
still mixes route-relevant and non-route populations. Route-position centers
remain the strongest positive control.

**Mechanism guess:** loss gradients may identify hidden states that affect the
supervised prediction. Gradient magnitude may select task-relevant positions;
gradient direction or Fisher-weighted geometry may separate features inside
that selected population.

**Key variables:** hidden state $h_{i,p}$, loss gradient
$g_{i,p}=\nabla_{h_{i,p}}\mathcal L_i$, gradient energy
$E_{i,p}=\|g_{i,p}\|_2^2$, Fisher-like matrix
$F=\mathbb E[g_{i,p}g_{i,p}^{\top}]$, router row $w_e$, and matched margin.

**Observable metric:** immediate feature NMI after router reinitialization,
guarded by margin p05, preserve fraction, and slot-start NMI.

**Rival explanations:** the signal may only recover the supervised position;
it may classify target class through gradient direction without producing
stable router margins; it may remain dominated by all-position nuisance
geometry.

**Decision:** promote embedding-gradient top1/direction as the next method
candidate because the full run beats all-position clustering, approaches or
matches route-position control, and gives positive lower-tail margin.

## 1. Problem Definition

The parent A06 problem asks how to discover and preserve feature-level routing
without feature labels. A06_25 showed that warmup strengthens all-position
feature geometry but does not close the route-position gap. A06_26 showed that
MPI-style spectral routing improves over vanilla routing but does not create a
positive-margin feature partition.

The current decision question is:

Can label-free gradient or Fisher signals select route-relevant hidden states
from the all-position pool and initialize router rows that separate uniform
features with stable positive margins?

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Gradient energy | How strongly a hidden state affects loss | Squared gradient norm at a token position | $E_{i,p}=\|g_{i,p}\|_2^2$ | Tests whether task relevance is visible without labels | Feature semantics |
| Fisher-like matrix | Loss-sensitive directions | Outer product average of gradients | $F=\mathbb E[g g^\top]$ | Tests whether distance should be measured in loss-relevant directions | True Fisher in a full probabilistic model |
| Route-relevant state | State used to predict the target | Hidden state at or near the supervised route position | Token-position population | Needed for valid router initialization | Real-DCLM route selection |
| Feature NMI | Feature/route agreement | NMI(feature id, selected expert) | 0--1 | Primary feature separation metric | Utility |
| Margin p05 | Lower-tail safety buffer | 5th percentile of matched logit gap | Logit difference | Guards preservation | Optimality |

## 3. Physical Prior

If the prediction loss depends on a hidden state, its gradient should be
nonzero or structured. A useful selector must do more than locate the supervised
position: it must produce feature-separated router rows with positive margins.

## 4. Core Mathematical Model

For sample $i$ and position $p$:

$$
g_{i,p}=\nabla_{h_{i,p}}\mathcal L_i,\qquad
E_{i,p}=\|g_{i,p}\|_2^2.
$$

For Fisher-weighted geometry:

$$
F=\mathbb E[g_{i,p}g_{i,p}^{\top}],\qquad
d_F(h_a,h_b)=(h_a-h_b)^\top F(h_a-h_b).
$$

The router margin for feature $f$ is:

$$
\gamma_f=w_{a(f)}^\top \mu_f-\max_{e\ne a(f)}w_e^\top \mu_f.
$$

## 5. Minimal Test

Use the same uniform no-position slot bridge as A06_25/A06_26. Compare:

- all-position centered clustering;
- route-position centered clustering;
- oracle feature centers;
- gradient-magnitude selection;
- gradient-weighted clustering;
- gradient-direction clustering;
- Fisher-subspace clustering.

The primary metric is immediate feature NMI. Margin p05 is the preservation
guard. Slot-start NMI and selected-position diagnostics guard against position
shortcuts.

## 6. Supported / Weakened / Insufficient Outcomes

**Supported:** embedding-gradient top1 and embedding-gradient direction exceed
all-position clustering, match route-position control at warmup 40, have
positive margin p05, preserve after training, and do not route by slot start.

**Weakened:** Fisher-only subspace clustering improves feature NMI but margin
p05 remains negative, so it is not a method candidate.

**Insufficient:** route-position/oracle controls fail, target accuracy fails,
the full seed/slot coverage is incomplete, or selection diagnostics are missing.

## 7. Current Evidence

Full run `a06_27_gradient_fisher_full_local2gpu_20260705` completed all
`32/32` seed/slot cells and produced `5760` trajectory rows.

At warmup 40, embedding-gradient top1 reaches immediate feature NMI `1.000`,
margin p05 `10.083`, matched preserve `1.000`, final feature NMI `1.000`, and
final margin p05 `9.609`. Embedding-gradient direction also reaches immediate
and final feature NMI `1.000` with positive margins. All-position centered
clustering remains below this level (`0.876` immediate NMI and `-4.399` margin
p05 at warmup 40).

Signal diagnostics show that post-hidden gradients are exactly route-local and
embedding gradients place most nonnegative mass on route/slot positions
(`route_share=0.923`, `slot_share=0.968`, `target_share=0.000` at warmup 40).
This supports route-state selection, not direct semantic feature discovery.

Source records:

- `../../experiments/A06/A06_27_gradient_fisher_route_state_selector/summary.md`
- `../../experiments/A06/A06_27_gradient_fisher_route_state_selector/detailed.md`

## 8. Claim Boundary And Next Decision

The claim boundary is the synthetic uniform no-position one-layer Transformer
plus one-layer MoE setting. This anchor cannot claim real-DCLM transfer,
semantic experts, common/rare routing, or expert utility.

Next decision: test a margin-thickened embedding-gradient selector method.
The minimal follow-up should use embedding-gradient top1 or direction to select
route-relevant states, build router rows from selected hidden centers, and
compare row scaling, row projection, or refresh schedules under the same
feature NMI plus margin p05 guards. A harder objective-locality guard is needed
before transferring this claim beyond the synthetic pointwise-loss bridge.
