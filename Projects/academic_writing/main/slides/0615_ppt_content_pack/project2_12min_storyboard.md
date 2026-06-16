# Project 2 Presentation Storyboard

Topic: **Why Sparse MoE Routers Collapse Before They Specialize**  
Subtitle: **An audit of expert-spectrum initialization and early routing amplification**  
Target length: **about 12 minutes**  
Deck shape: **12 main slides + 2 backup slides**  

## Story Logic

The presentation should not claim a finished routing method. The story is:

1. Sparse MoE performance depends on the router because the router controls which experts receive tokens and gradients.
2. Recent geometry-based MoE papers warn that routing patterns do not automatically prove domain expertise; they often reflect hidden-state geometry.
3. Our audit asks which geometry top-1 routing amplifies before useful specialization can form.
4. Earlier evidence shows that a common hidden-state direction can act like an expert-specific bias.
5. The latest 0615 result tests a natural method idea: initialize the router from each expert's principal input subspace after filtering the common direction.
6. The result is informative but negative: common-filtered expert-spectrum initialization improves step-0 load, but training by step 10 amplifies concentration again.
7. The updated mechanism claim is that early route concentration is not an initialization-only problem; it is a coupled router-hidden-state amplification problem.

Use template-inspired style: white background, HarmonyOS Sans, deep magenta accent `#881E55`, blue accent `#29AAE3`, compact academic layout, one main proof object per slide.

---

## Slide 01. Title

Time: 0:00-0:35

Title:

```text
Why Sparse MoE Routers Collapse Before They Specialize
```

Subtitle:

```text
An audit of expert-spectrum initialization and early routing amplification
```

Footer:

```text
Academic Writing Project 2 | 12-min research update
```

Visual:

- Small right-side schematic from `figures/s02_background_gap_diagram.png`.

Speaker purpose:

- Set the boundary: this is a mechanism audit and method-motivation talk, not a completed method paper.

---

## Slide 02. Background: MoE scaling is router-limited

Time: 0:35-1:30

Title:

```text
MoE scaling is router-limited, not only expert-limited
```

Bullets:

```text
- Sparse MoE activates only a few experts per token, so the router controls data and gradient flow.
- Load imbalance can make many experts under-trained even when the model has many parameters.
- Recent work suggests router decisions often reflect hidden-state geometry rather than clean domain expertise.
```

Visual:

- `figures/s02_background_gap_diagram.png`

Placement:

- Left text column, right figure panel.

Speaker purpose:

- Define sparse MoE, router, and route concentration.
- Introduce the literature boundary from Wang et al. (2026) and Ahrac et al. (2026): routing geometry is real, but it is not automatically semantic specialization.

---

## Slide 03. Research question

Time: 1:30-2:25

Title:

```text
Question: which geometry does top-1 routing amplify first?
```

Bullets:

```text
Working thesis:
Hidden states contain useful residual structure, but a shared common direction can create expert-specific routing bias.

Current question:
Can expert-aware router initialization reduce the early bias, or does training re-amplify it?
```

Visual:

- `figures/s03_storyline_ladder.png`

Placement:

- Full-width ladder with two short callouts: "common-logit bias" and "expert-spectrum init test".

Speaker purpose:

- Connect the seven-day meeting-brief sequence into one story: from false specialization signals, to common-logit mechanism, to the latest initialization stress test.

---

## Slide 04. Why this matters: consistency can be a false positive

Time: 2:25-3:15

Title:

```text
High route consistency can hide collapse
```

Bullets:

```text
- A feature can be routed consistently while many features share the same expert.
- Therefore route consistency alone is not evidence of useful specialization.
- The audit must track load, assignment structure, and intervention response together.
```

Visual:

- `figures/s04_baseline_collapse_heatmaps.png`

Placement:

- Wide heatmap strip across the bottom.

Speaker purpose:

- Explain why the project studies route concentration instead of only accuracy or consistency.

---

## Slide 05. Specialization is reachable under the right basin

Time: 3:15-4:05

Title:

```text
Specialization is reachable, but random top-1 often misses the basin
```

Bullets:

```text
- Slot-aware initialization produces stable slot-to-expert structure.
- Releasing an oracle router can preserve specialization after basin entry.
- The bottleneck is early basin entry, not the impossibility of specialization.
```

Visual:

- Main: `figures/s05_slot_init_positive_control_heatmaps.png`
- Small inset if space: `figures/s05_oracle_release_trajectory.png`

Placement:

- Heatmap strip on the right, three short evidence bullets on the left.

Speaker purpose:

- Rule out the rival explanation that the model simply cannot specialize.

---

## Slide 06. Mechanism candidate: common-logit bias

Time: 4:05-5:00

Title:

```text
Common-logit bias acts like an expert-specific offset
```

Formula:

```text
h_i = c + r_i
z_{i,e} = w_e^T c + w_e^T r_i
```

Bullets:

```text
- The common component c is shared by many tokens.
- The term w_e^T c is feature-independent but differs across experts.
- A larger common-logit can win top-1 routing before residual features matter.
```

Visual:

- `figures/s06_common_logit_model.png`

Placement:

- Formula and mechanism diagram as the central proof object.

Speaker purpose:

- Define the mechanism in a compact mathematical form.

---

## Slide 07. Controlled evidence: common-logit is early and intervention-relevant

Time: 5:00-6:05

Title:

```text
Controlled evidence: common-logit appears early and is intervention-relevant
```

Bullets:

```text
- Common margin rises before slot margin becomes decisive.
- Cancelling the common-logit improves slot NMI while preserving accuracy.
- This supports common-logit as a causal contributor in the controlled setting.
```

Visuals:

- `figures/s07_common_vs_slot_margin_timing.png`
- `figures/s07_common_cancellation_metrics.png`

Placement:

- Two equal columns with a bottom caption: `slot NMI improves while accuracy stays at 1.000`.

Speaker purpose:

- Show that common-logit is not just a descriptive story; intervention changes routing structure.

---

## Slide 08. Real text makes the claim narrower

Time: 6:05-7:00

Title:

```text
Real-text step 0: common direction matters, but it is not the whole story
```

Bullets:

```text
- After removing top-1% high-frequency tokens, random linear routers still show step-0 load bias.
- Centering / common removal reduces the bias, but does not eliminate all structure.
- This moves the question from static bias to early training amplification.
```

Visuals:

- `figures/s09_realtext_step0_common_vs_residual.png`
- `figures/s09_realtext_raw_vs_centered_load.png`

Placement:

- Two panels, same height, with one sentence conclusion under them.

Speaker purpose:

- Tighten the claim boundary before presenting the latest experiments.

---

## Slide 09. 0614 result: step-10 concentration is not gate-only

Time: 7:00-8:00

Title:

```text
Step-10 concentration is a coupled gate-hidden effect
```

Bullets:

```text
- Freezing only the router or only the experts does not explain the full spike.
- Freezing the prefix before layer 5 suppresses most of the early amplification.
- Cross-checkpoint replay shows a large interaction term between router and hidden states.
```

Visuals:

- `figures/s11_freeze_split_key_numbers.png`
- `figures/s11_replay_heatmap_common_margin.png`

Placement:

- Left: key-number card. Right: replay heatmap.

Speaker purpose:

- Establish the mechanism update that prepares the audience for why initialization alone may fail.

---

## Slide 10. 0615 method test: expert-spectrum initialization

Time: 8:00-9:10

Title:

```text
0615 test: initialize the router from expert input geometry
```

Bullets:

```text
- Expert principal input subspaces are measurable and differ across experts.
- Their overlap with the hidden-state common direction is low.
- Therefore expert-spectrum initialization is computationally well-defined, but not yet a specialization claim.
```

Key numbers:

```text
expert-expert subspace overlap: about 0.0116
expert-common overlap: about 0.0166
raw spectrum utility correlation: about 0.2328
```

Visual:

- Use a simple pipeline diagram in the PPT:
  `expert input matrices -> principal subspaces -> common filtering -> linear top-1 router`

Placement:

- Text left, pipeline right.

Speaker purpose:

- Present the method idea fairly: it has a computable basis, but the claim boundary is strict.

---

## Slide 11. 0615 result: step-0 improves, step-10 fails

Time: 9:10-10:20

Title:

```text
Common-filtered spectrum improves step 0, but fails by step 10
```

Bullets:

```text
- Step 0 after removing top-1% high-frequency tokens: max load improves from 19.98% to 13.97%.
- Step 10: max load worsens from 83.16% to 93.51%.
- Better initialization balance does not guarantee stable early routing dynamics.
```

Visual:

- `figures/s12_0615_spectrum_init_stress_test.png`

Placement:

- Large central chart. Add small right-side verdict tag: `supported at step 0; not supported at step 10`.

Speaker purpose:

- Deliver the main latest result without overstating it as a method success.

---

## Slide 12. Updated conclusion and next decision

Time: 10:20-11:55

Title:

```text
Three conclusions: geometry is useful, but initialization is not enough
```

Bullets:

```text
1. Expert input geometry is measurable and not identical to the common direction.
2. Common-filtered initialization reduces step-0 load bias.
3. Step-10 concentration is driven by early router-hidden-state amplification, not initialization alone.
```

Next decision:

```text
Do not scale the current linear initialization experiment yet.
Next: audit whether step-0 route winners are reinforced by early hidden-state change and router updates.
Branch: test whether an oracle or learned bridge can express expert-spectrum matching better than a linear top-1 router.
```

Visual:

- `figures/s12_next_mechanism_hypothesis.png`

Placement:

- Three conclusion cards across the top, next-decision diagram below.

Speaker purpose:

- End with a research decision, not a broad claim.

---

## Backup 13. Claim boundary

Title:

```text
What this result does and does not claim
```

Can say:

```text
- Expert-spectrum directions are measurable and differ across experts.
- Common-filtered initialization improves step-0 balance.
- Current linear top-1 initialization cannot prevent step-10 concentration.
```

Cannot say:

```text
- Expert spectrum is useless.
- Domain specialization has been explained.
- The result generalizes to pretrained large MoEs, top-2/top-4 routing, or load-balancing losses.
```

---

## Backup 14. References

Title:

```text
References
```

References:

```text
- Shazeer et al., Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer, 2017.
- Fedus et al., Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity, 2021.
- Zoph et al., ST-MoE: Designing Stable and Transferable Sparse Expert Models, 2022.
- Wang et al., The Myth of Expert Specialization in MoEs: Why Routing Reflects Geometry, Not Necessarily Domain Expertise, 2026.
- Ahrac et al., Routers Learn the Geometry of Their Experts: Geometric Coupling in Sparse Mixture-of-Experts, 2026.
```
