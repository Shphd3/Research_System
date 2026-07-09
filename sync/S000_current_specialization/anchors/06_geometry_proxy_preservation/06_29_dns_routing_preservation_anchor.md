# Anchor: A06_29 DNS Routing Preservation Audit

## 0. Thinking Card

**Phenomenon:** A06_28 showed that full-LM long training erodes route-feature margins even when initialization starts from clean oracle or route-position centers.

**Mechanism guess:** the router may drift toward a common hidden-state component during full-LM optimization. If routing uses a common-subtracted hidden state, or if router rows are constrained away from the common direction, the feature margin may be preserved longer.

**Key variables:** common direction $c$, raw hidden state $h$, DNS router input $h_{\mathrm{dns}}=h-c$, router row $w_e$, feature NMI, margin p05, common alignment $\cos(w_e,c)$, and target accuracy.

**Causal relation:** reducing router access to common components should reduce common-driven drift and preserve the feature-specific score gap.

**Observable metric:** margin p05 through 2000 full-LM steps, guarded by feature NMI, target accuracy, and common-alignment diagnostics.

**Rival explanations:** margin erosion may not be caused by common drift; DNS may preserve margins only by harming LM learning; noisy gradient-selected initialization may be too weak even with DNS; router freezing or lower router LR may preserve margin without proving common causality.

**Decision:** the audit is complete. Mean-DNS routing alone is not supported. Router-row projection is the strongest partial preservation clue, but no tested condition preserves positive margin through 2000 full-LM steps.

## 1. Problem Definition

Parent problem: preserve feature-specialized routing under full-LM optimization.

Sharper subproblem: test whether common-subtracted routing and router-side preservation interventions can keep positive margins for gradient-selected or center-initialized routers.

Decision question: Does DNS-style routing or router-side preservation prevent long full-LM training from eroding feature margins?

Not in scope: real language transfer, semantic experts, rare-feature routing, or final method optimality.

## 2. Physical Priors

P1: If common components dominate router gradients, raw routing should show increasing common alignment and margin erosion.

P2: If DNS removes the harmful common component from the router input, DNS routing should preserve margin better than raw routing at comparable LM accuracy.

P3: If row drift is the main problem, row projection, lower router LR, or early freeze should preserve margin even without changing expert computation.

## 3. Falsifiable Hypotheses

H1: `embedding-gradient top1 + DNS` has higher margin p05 than raw embedding-gradient top1 after long full-LM training.

H2: `denoised gradient selector + DNS` improves over raw gradient top1 + DNS by selecting a cleaner state pool.

H3: router-row projection, lower router LR, or early router freeze improves long-run margin without unacceptable target-accuracy regression.

## 4. Mathematical Model

DNS router input:

$$
h_{\mathrm{dns}}=h-c.
$$

Raw router score:

$$
s_e=w_e^\top h.
$$

DNS router score:

$$
s_e^{dns}=w_e^\top(h-c).
$$

Row projection:

$$
w_e \leftarrow w_e - (w_e^\top \hat c)\hat c,\qquad \hat c=c/\|c\|.
$$

Margin:

$$
\mathrm{margin}(i)=s_{e^*(f_i)}(h_{r_i})-\max_{e\ne e^*(f_i)}s_e(h_{r_i}).
$$

Falsifier: all DNS and preservation variants remain negative-margin while target accuracy is preserved.

## 5. Computational Realization

Input objects: same A06_28 synthetic no-position full-LM bridge.

Common direction: calibration all-position hidden mean at warmup 40.

Denoised gradient selector: position-normalized embedding-gradient energy,
computed without route-position labels:

$$
z_{i,p}=\frac{E^{emb}_{i,p}-\mu_p}{\sigma_p+\epsilon}.
$$

Algorithm stages:

1. Warm up the model for 40 full-LM steps.
2. Build raw and DNS initialization rows.
3. Train to 2000 full-LM steps with selected router interventions.
4. Track feature NMI, margin p05, common alignment, and target accuracy.

Expected artifacts: protocol, runner, summary, detailed report, tables, and figures.

## 6. Minimal Falsification Tests

Test: DNS preservation audit under full-LM long training.

Primary metric: margin p05 at checkpoints 160/500/1000/2000.

Pass: one DNS or preservation condition keeps higher margin p05 than raw gradient top1 and does not strongly reduce target accuracy.

Fail: DNS and preservation variants do not improve margin, or only improve margin by damaging LM learning.

Insufficient: clean center controls fail immediately, seed/slot coverage is incomplete, or checkpoint 2000 is missing.

## 7. Current Evidence

Observation: A06_28 long-train audit shows that raw full-LM training drives gradient-selected top1 margin from -1.828 at step 160 to -9.142 at step 2000, while oracle and route-position centers also cross below zero by 1000--2000 steps.

Interpretation: long-run full-LM optimization introduces a preservation problem beyond selector quality.

Observation: A06_29 completed 32/32 seed-slot cells with full-LM warmup 40 and 2000 post-reinit steps. At step 2000, raw gradient top1 has feature NMI 0.684 and margin p05 -10.702. Gradient top1 + DNS is worse, with NMI 0.561 and margin p05 -12.271. The position-normalized denoised selector + DNS is worse again, with NMI 0.464 and margin p05 -15.586. Row projection is the best tested intervention for the denoised selector, improving final margin to -8.960 and NMI to 0.608, but still failing positive-margin preservation.

Interpretation: the simple mean-DNS input view is not enough to explain or fix margin erosion. The useful signal is more consistent with a router-row constraint than with subtracting the mean hidden vector from router input. The current position-normalized gradient denoising rule removes useful route/slot signal and should not be promoted.

Evidence links:

- `../../experiments/A06/A06_28_long_train_margin_audit/summary.md`
- `../../experiments/A06/A06_28_long_train_margin_audit/detailed.md`
- `../../experiments/A06/A06_29_dns_routing_preservation_audit/summary.md`
- `../../experiments/A06/A06_29_dns_routing_preservation_audit/detailed.md`
- `../../experiments/A06/A06_29_dns_routing_preservation_audit/figures/a06_29_dns_margin_trajectory.png`
- `../../experiments/A06/A06_29_dns_routing_preservation_audit/figures/a06_29_dns_final_step2000.png`

## 8. Claim Boundary And Next Decision

Can claim:

- Mean-DNS routing alone does not preserve feature margins in the controlled synthetic full-LM bridge.
- The tested position-normalized denoised gradient selector is weaker than raw embedding-gradient top1.
- Router-row projection provides the clearest partial preservation improvement among tested interventions.

Cannot claim:

- Common components are irrelevant in all forms.
- A better common operator or stronger projection method cannot work.
- Row projection solves preservation; it improves but remains negative-margin.
- Real-DCLM transfer, semantic specialization, or final method optimality.

Next decision: isolate row projection without the failed denoised selector by comparing raw gradient top1, raw gradient top1 + row projection, route center + row projection, and oracle center + row projection under the same full-LM long-training audit.
