# A16_00_02_E01 Detailed Evidence Ledger

## 1. Question and verdict

Question: across paired early, middle, and late Vanilla/Centered states, does centering reduce the immediate held-out NLL cost of a truly differentiable Switch LB update, with corresponding reductions in Router-source/Gate opposition and routed expert-update conflict?

Typed verdicts:

| Claim | Verdict | Reason |
| --- | --- | --- |
| Centered outcome mediation | `fail` | seed 17 three-stage median interval crosses zero |
| Shared Router-source/Gate pathway | `fail` | only the 50M stage has joint positive cosine gains in both seeds |
| Within-expert conflict | `fail` | Centered negative-cosine mass is not lower at two stages per seed |
| Combined H1 | `fail` | all three registered clauses were required |

## 2. Frozen setup

- Model family: four Transformer blocks, hidden size 768, eight sparse experts plus one shared expert, top-1 routing.
- Arms: `vanilla_full`, `centered_full`.
- Seeds: 17, 29.
- Stages: step 64 = 50,331,648 tokens; step 7,629 = 5,999,689,728 tokens; step 12,716 = 10,000,269,312 tokens.
- DCLM optimizer batch: exact checkpoint data cursor, global 768 x 1,024 tokens, same hashes in the two shadow branches.
- WoS expert-conflict data: seven domains, 32 train documents/domain split into two groups.
- WoS held-out outcome data: 16 validation documents/domain, 112 documents total. Test remained untouched.
- LB coefficient: 0.01 in the counterfactual differentiable branch.

The full data and SHA-256 contract is in [protocol.md](protocol.md). Raw outputs remain under `/data/250010109/MoE_Router/outputs/a16_multistage_gradient_pathway/`.

## 3. Execution provenance

| Job | ACP id | Terminal state |
| --- | --- | --- |
| Vanilla seed 17 | `pt-l3732mt6` | `SUCCEEDED` |
| Vanilla seed 29 | `pt-v2d0r859` | `SUCCEEDED` |
| Centered seed 17 | `pt-46mo22r8` | `SUCCEEDED` |
| Centered seed 29 | `pt-9om553fw` | `SUCCEEDED` |

The qualified differentiable-LB smoke was `pt-vkxkk7o3` (`SUCCEEDED`). Earlier smoke attempts are retained in the worker ledger as engineering evidence; they are excluded from scientific results.

Unit and analysis tests: 13/13 passed. All 12 cells contain `gradients.json`, `wos_lm_only.json`, `wos_lm_lb.json`, `shadow_comparison.json`, and `validity.json` with `status=pass`.

## 4. Primary cell results

All NLL changes are nat/token. Positive \(\Delta NLL_{LB}\) means the effective LB component made the next held-out prediction worse.

| Arm | Seed | Stage | \(\Delta NLL_{LB}\) | 95% document interval | mean max-share change |
| --- | ---: | --- | ---: | ---: | ---: |
| Vanilla | 17 | 50M | +0.000845 | [+0.000695, +0.000999] | -0.00996 |
| Vanilla | 17 | 6B | -0.001631 | [-0.003152, -0.000111] | -0.00829 |
| Vanilla | 17 | 10B | +0.000482 | [-0.001183, +0.002053] | -0.01490 |
| Vanilla | 29 | 50M | +0.000617 | [+0.000451, +0.000788] | -0.01227 |
| Vanilla | 29 | 6B | -0.000789 | [-0.002405, +0.000739] | -0.00967 |
| Vanilla | 29 | 10B | +0.002019 | [+0.000418, +0.003541] | -0.00737 |
| Centered | 17 | 50M | +0.000006 | [-0.000096, +0.000108] | +0.00017 |
| Centered | 17 | 6B | -0.000165 | [-0.000657, +0.000327] | -0.00140 |
| Centered | 17 | 10B | +0.000239 | [-0.000247, +0.000736] | -0.00081 |
| Centered | 29 | 50M | -0.000013 | [-0.000118, +0.000099] | -0.00049 |
| Centered | 29 | 6B | -0.000104 | [-0.000568, +0.000352] | -0.00183 |
| Centered | 29 | 10B | -0.000134 | [-0.000622, +0.000353] | -0.00137 |

The machine-readable source is [cell_summary.csv](tables/cell_summary.csv).

![LB shadow cost](figures/figure1_lb_shadow_cost.png)

## 5. Centered mediation

| Seed | Stage | \(M\) | 95% interval | source cosine gain | Gate cosine gain |
| --- | --- | ---: | ---: | ---: | ---: |
| 17 | 50M | +0.000839 | [+0.000655, +0.001030] | +0.0267 | +0.1933 |
| 17 | 6B | -0.001466 | [-0.002962, +0.000022] | -0.0071 | -0.2185 |
| 17 | 10B | +0.000242 | [-0.001482, +0.001928] | -0.0088 | -0.3167 |
| 29 | 50M | +0.000630 | [+0.000413, +0.000850] | +0.0272 | +0.2282 |
| 29 | 6B | -0.000685 | [-0.002300, +0.000894] | -0.0066 | -0.4249 |
| 29 | 10B | +0.002152 | [+0.000545, +0.003764] | -0.0086 | -0.5068 |

The 50M mediation is the only stage that is positive with an interval above zero in both seeds. The 6B point estimates have the opposite sign, while only seed 29 has a precise positive 10B mediation. Full results are in [centering_mediation.csv](tables/centering_mediation.csv).

## 6. Gradient and expert interpretation

At 50M, Vanilla Gate cosines are strongly opposed (mean -0.771/-0.762); Centered raises them to -0.577/-0.534 and sharply reduces LB gradient norms because its load is already broad. At later stages, Vanilla contains layer-specific positive Gate alignments while Centered remains more consistently negative, so averaging does not support a global conflict-reduction mechanism.

The last layer has no same-layer direct LB derivative into its own experts, as required. Earlier experts receive LB gradients only through later Router-source dependencies; this is the reported `expert_upstream` pathway.

Within-expert conflict is conditioned on which documents are routed to an expert. Vanilla's near-zero negative mass coexists with much higher maximum expert shares. Thus a zero value can arise because collapsed routing retains a homogeneous group and should not be interpreted as better specialization. The registered lower-conflict prediction nevertheless fails.

Layer-level sources: [gradient_pathways.csv](tables/gradient_pathways.csv), [expert_conflict_by_layer.csv](tables/expert_conflict_by_layer.csv), and [load_by_layer.csv](tables/load_by_layer.csv).

![Pathway cosine gains](figures/figure3_pathway_cosine_gains.png)

![Conflict and hard load](figures/figure4_expert_conflict_and_load.png)

## 7. Plot contracts and visual audit

1. **Figure 1:** asks whether the effective LB shadow step raises held-out WoS NLL. The y-axis is paired LM+LB minus LM-only NLL; intervals resample 112 documents. It cannot establish long-run training effects.
2. **Figure 2:** asks whether centering reduces that cost. Positive bars favor Centered. It is the primary result figure and cannot identify the gradient pathway causing the effect.
3. **Figure 3:** asks whether centering makes LM/LB gradients less opposed. Values are Centered minus Vanilla cosine; positive means less opposition. Layer means summarize registered pathway tables and cannot prove outcome benefit.
4. **Figure 4:** separates routed expert-update conflict from hard-load response. Negative left-panel bars mean Centered has more measured negative mass; negative right-panel bars mean Vanilla's LB step reduces maximum share more. Neither panel is a quality metric by itself.

All four rendered PNGs were opened and visually checked after final label revision. Axes, signs, seed/stage labels, intervals, and legends are legible.

## 8. Amendments and evidence boundary

Two append-only Protocol amendments govern interpretation:

1. same-layer expert direct LB derivatives must be zero, while later-layer LB may reach earlier experts through the representation path;
2. both shadow branches disable activation checkpointing because the source re-entrant path detached the nested LB tensor.

The repaired LM-only branch is tensor-exact relative to the original LM-only update. The repaired LM+LB branch changes 130 model tensors and all eight optimizer shards. Therefore the measured one-step intervention is effective and auditable, but the original source trajectories did not receive that effective gradient.

## 9. Claim boundary and next decision

Established: centering removes a repeatable early-state LB cost; the effect is not uniformly persistent; the proposed global shared-path and expert-conflict mediators fail.

Not established: long-run LB harm, centering's 30B causal mechanism, useful expert specialization, or superiority of dynamic bias.

Next decision: test Centered with dynamic expert bias against Centered with truly differentiable LB and Centered without extra load control, using hard load plus held-out NLL/FLOP as co-primary evidence.

