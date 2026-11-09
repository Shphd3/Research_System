# A06_03_01_E02 Result Summary: Specialist-Generalist Router Release

## Conclusion

Learned specialists keep a large task-value advantage after router release, but
their route margin grows slightly less than the margin of load-matched
generalists. Under router-only SGD at update 50, the paired
specialist-minus-generalist margin-growth contrast is -0.00324 with a
seed-clustered 95% confidence interval of \([-0.00413,-0.00245]\). The paired
generalist-minus-specialist task-loss difference is 0.9125 nats/task-token with
95% confidence interval \([0.8905,0.9438]\).

This certifies a metric separation, not a route collapse. Route NMI remains 1
for both starts, both margins increase, and specialists close a larger fraction
of their own routing excess. Counterfactual expert-identity utility therefore
does not calibrate confidence growth when the useful expert is already top-1.
The next causal question must place the useful specialist below top-1 and test
whether native weighted top-1 can discover it.

## Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Specialist | Expert trained only on one context-defined task | correct expert-only exposure | Has a unique useful identity | Natural-language semantics |
| Generalist | Expert trained equally on all four tasks | balanced shuffled exposure | Load-matched no-identity control | A useless expert |
| Counterfactual utility gap | Assigned expert loss advantage over the best competitor | \(G_f^{cf}=\min_{b\ne f}(L_{f,b}^{cf}-L_{f,f}^{cf})\) | Measures expert-identity value | Required confidence growth |
| Route margin | Assigned expert score lead over its closest competitor | \(m_f=s_f-\max_{b\ne f}s_b\) | Measures route confidence | Expert usefulness |
| Margin-growth contrast | Specialist minus generalist cumulative margin growth | \(D_m(T)=\operatorname{median}(\Delta m_f^{spec}-\Delta m_f^{gen})\) | Registered primary metric | Correction from a wrong route |
| Routing excess | Native task loss above the forced assigned-expert floor | \(E_f=L_f^{native}-L_{f,f}^{cf}\) | Separates route weighting from expert function | Wall-clock efficiency |

## Exact Setup

- Data: four equally frequent sequence-level modular tasks. Instruction \(f\)
  appears at sequence start; each later content \(c\) requires output
  \((c+f)\bmod4\).
- Sequence: length 33 with 16 content/output pairs; all 32 next-token positions
  enter the LM loss.
- Model: one causal-attention layer, residual plus LayerNorm, no learned
  positional embedding, four MLP experts, fixed readout, weighted top-1 router.
- Exposure: 200 expert-only AdamW updates. Correct exposure creates specialists;
  balanced shuffled exposure creates generalists.
- Release: 50 native full-sequence LM updates from exactly identical router and
  representation states.
- Primary: router-only SGD at learning rate \(10^{-4}\).
- Transfer: router-only AdamW at 0.001 and joint AdamW with new optimizer state.
- Evidence: 32 seeds, four tasks per seed, 128 paired task-seed cells.

## Primary Evidence

| Metric at release update 50 | Specialist | Generalist | Paired result |
| --- | ---: | ---: | ---: |
| Counterfactual utility gap at start | 8.8947 | -0.0042 | specialists have unique function |
| SGD margin growth | 0.10031 | 0.10337 | \(D_m=-0.00324\), CI \([-0.00413,-0.00245]\) |
| SGD native task loss | 0.6441 | 1.5576 | advantage 0.9125, CI \([0.8905,0.9438]\) |
| SGD normalized routing excess | 0.7612 | 0.8513 | specialist closes a larger fraction |
| Minimum route NMI | 1.0000 | 1.0000 | no route-identity loss |

The operational H3 rule is met: task value remains positive while the margin
contrast is negative. The interpretation is narrower than “utility
transmission fails.” The intervention changes confidence in an already correct
expert, whereas \(G_f^{cf}\) compares expert identities. A larger identity gap
need not require a larger confidence update once the correct identity is fixed.

## Optimizer Transfer

| Release mode | Margin-growth contrast at update 50 | 95% CI | Reading |
| --- | ---: | ---: | --- |
| Router-only SGD | -0.00324 | \([-0.00413,-0.00245]\) | reliable negative contrast |
| Router-only AdamW | -0.04668 | \([-0.05474,-0.03562]\) | same sign, larger scale |
| Joint AdamW | 0.00013 | \([-0.00465,0.00770]\) | no resolved difference |

Joint training drives both losses near zero and makes the specialist/generalist
margin contrast statistically unresolved. It cannot overwrite the frozen-path
causal comparison.

## Central Figures

### Margin-Growth Handoff

![Margin-growth contrast](figures/margin_growth_contrast.png)

- **Question:** Does specialist identity value create larger confidence growth?
- **Read:** Positive values favor specialists; bands are seed-clustered 95% CIs.
- **Observed:** SGD and router-only AdamW become reliably negative; joint AdamW
  returns toward zero.
- **Take-home:** Confidence growth is not calibrated by counterfactual identity
  utility under an already correct top-1 route.
- **Limitation:** It does not test discovery of an unselected useful expert.

### Task Value And Routing Excess

![Task loss and routing efficiency](figures/task_loss_and_routing_efficiency.png)

- **Question:** Do specialists preserve task value despite smaller margin growth?
- **Read:** Left is native task loss; right is loss above each condition's own
  forced floor, normalized by its initial value.
- **Observed:** Specialists remain much better and close more normalized excess.
- **Take-home:** Smaller margin growth is not worse task learning or collapse.
- **Limitation:** Activated compute and system throughput are identical.

### Local Pressure And Realized Movement

![Pressure and movement](figures/pressure_actual_movement.png)

- **Question:** Does the A06_03_01_E01 pressure ordering appear in the first release step?
- **Observed:** Median pre-release pressure is 121.94 for specialists and 146.99
  for generalists; median realized first-step margin movement is 0.002148 versus
  0.002175.
- **Take-home:** Higher residual pressure produces slightly larger confidence
  movement for generalists.
- **Limitation:** The plot does not identify the best unselected expert.

## Hypothesis Update

| Hypothesis | Verdict | Boundary |
| --- | --- | --- |
| Specialists retain native task value | Supported | controlled context task |
| Specialists receive larger margin growth | Rejected | correct top-1 start only |
| Negative contrast means specialization collapse | Rejected | NMI stays 1 and both margins grow |
| Router-only AdamW preserves the contrast sign | Supported | optimizer scale differs |
| Joint training preserves a nonzero contrast | Insufficient | CI crosses zero |

## Claim Boundary And Next Decision

**Supported:** learned expert function changes task loss while non-expert state is
identical; counterfactual identity utility and correct-route confidence growth
are distinct quantities; ordinary weighted top-1 preserves the supplied route
over this 50-step horizon.

**Not supported:** natural-language semantic specialization, from-scratch
discovery, route correction from a wrong expert, downstream compute savings, or
the necessity of a new gate.

**Next decision:** With learned specialists fixed, place the function-matched
expert at controlled initial score rank 2 or 4 and test whether weighted top-1
recovers it under full-sequence LM loss. Correction time and cumulative task
regret, not confidence growth from an already correct route, become primary.

