# Protocol: A06_03_01_E01 Trainable Expert Utility Binding

## 0. Approval Snapshot

**Approval status:** Approved for execution under the persistent research goal on 2026-07-10.

**Purpose:** Test whether a correct route partition creates trainable expert function on a held-out context-defined next-token task, rather than only preserving geometric route identity.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`

**Decision question:** Does correct route-conditioned exposure create a positive held-out counterfactual feature-expert utility gap beyond a balanced identity-shuffled control?

**Physical prior tested:** Stable task-conditional expert updates are required for expert function to differentiate.

**Core model term:** \(G_f^{cf}=\min_{b\ne a(f)}(L_{f,b}^{cf}-L_{f,a(f)}^{cf})\).

**Falsifier:** Correct exposure does not exceed the load- and update-matched shuffled exposure on held-out \(G_f^{cf}\).

**Experiment role:** Root-cause audit and operationalization test, not method construction.

**Primary metric:** Held-out task-position \(G_f^{cf}\) for frozen-representation expert-only exposure.

**Minimal setup:** Four equally frequent sequence-level transformation tasks, one-layer no-position causal Transformer, four identically initialized trainable MLP experts, fixed oracle exposure during training, full-sequence LM loss, and held-out content orders.

**Conditions:** correct expert-only exposure; balanced-shuffled expert-only exposure; correct joint expert-plus-representation exposure; balanced-shuffled joint exposure; step-0 baseline.

**Pass:** At least 90% of expert-only feature-seed cells have positive \(G_f^{cf}\); the seed-clustered 95% CI lower bound for paired correct-minus-shuffle median \(G_f^{cf}\) is positive; all validity guards pass.

**Fail:** Correct and shuffled expert-only exposure have indistinguishable held-out gaps under matched compute, while the task and positive learnability guards pass.

**Insufficient:** Fewer than 32 seeds, update-count mismatch, train/test overlap, non-learnable task, counterfactual-state mismatch, or failed full-LM/route validity guards.

**Cannot claim:** Natural-language semantic experts, label-free routing, real downstream benefit, long-context scaling, or deployable gating.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Context-defined task | A sequence-start instruction determines later token outputs | modular offset \(f\in\{0,1,2,3\}\) | task id | moves beyond token identity | natural semantics |
| Task position | A content token whose next token is instruction-dependent | odd predictor positions in the 33-token sequence | 16 positions/sequence | isolates the conditional operator | full-LM quality |
| Correct exposure | Task \(f\) always updates expert \(a(f)=f\) | forced expert permutation is identity | one expert active/token | creates stable conditional updates | deployable routing |
| Balanced shuffle | Task-to-expert mapping cycles through all four offsets | \(a_t(f)=(f+t)\bmod4\) | equal pair counts | matches load while deleting stable identity | every real confound |
| Counterfactual loss | Loss after forcing one expert and holding other components fixed | \(L_{f,e}^{cf}\) | cross-entropy, nats/token | compares expert function directly | long-run route stability |
| Utility gap | Assigned-expert advantage over the best competitor | \(G_f^{cf}\) | nats/token | primary binding metric | natural semantic specialization |
| Binding time | First checkpoint after which the paired correct-minus-shuffle median gap stays positive | \(T_{bind}\) | optimizer updates | controlled training efficiency | wall-clock/system efficiency |
| Router pressure | Predicted margin movement from one task-loss gradient step | \(-\langle g_a-g_b,\mu_f\rangle\) | logit-margin per unit step | tests utility-to-gate transmission | long-run convergence |

## 2. Anchor Alignment

**Decision question:** Whether a supplied route partition creates held-out task-specific expert utility.

**Physical prior:** Conditional expert-update distributions, not route labels alone, generate functional specialization.

**Falsifier:** No correct-versus-shuffle difference with matched expert updates.

**Claim boundary:** Controlled context operator only; no natural-language or downstream benchmark claim.

## 3. Tested Hypotheses

- **H1:** Correct expert-only exposure produces positive held-out \(G_f^{cf}\) in at least 90% of feature-seed cells and exceeds balanced shuffle with positive clustered-CI lower bound.
- **H2:** H1 survives with exactly frozen representation state, ruling out representation drift as necessary.
- **H3:** Correct exposure produces more positive task-gradient router pressure than balanced shuffle.
- **H4:** Both exposure conditions can preserve the oracle route label during training, while only correct exposure produces functional binding.

## 4. Rival Explanations

1. Expert update count or load creates apparent differentiation. Balanced shuffle exactly matches active tokens and per-expert updates.
2. Representation drift creates the gap. Expert-only conditions freeze every non-expert parameter and audit exact state equality.
3. Experts memorize train sequences. Evaluation uses disjoint content orders and reports train-test sequence hashes.
4. Full-LM background positions cause the result. Task-position and all-position counterfactual losses are both reported.
5. Router geometry alone creates the result. Counterfactual evaluation forces every expert with probability one, removing route scores from the utility comparison.

## 5. Data / Model / Routing / Objective

### Data

- Four task instructions, each equally frequent.
- Vocabulary: four instruction tokens, four content tokens, and four output tokens.
- Transformation: instruction \(f\) maps content value \(c\) to output value \((c+f)\bmod4\).
- Sequence: one instruction token followed by 16 content/output pairs; length 33.
- Standard autoregressive targets are the next tokens in the sequence; all 32 predictor positions enter the LM loss.
- Main task positions are the 16 content-token predictors.
- Per seed: 32 training sequences and 32 held-out sequences, eight per task, with disjoint content orders.

### Model

- Hidden dimension 64; four attention heads; one causal attention layer; residual plus LayerNorm; no learned positional embedding.
- A fixed strength-1.0 broadcast of the sequence instruction embedding is added to every position before LayerNorm. This is a known-good context-visibility control, not a proposed gate.
- Four MLP experts with hidden width 128 and identical initial parameters.
- Expert output is a residual update to the routed hidden state.
- Fixed tied-style readout, so the exposure phase cannot hide utility in an independently trained output head.
- Router rows are initialized from task-position hidden centers to p05 matched margin 0.5 and frozen during exposure.

### Training

- Full-sequence cross-entropy over all 32 next-token positions.
- Exposure steps: 200; checkpoints 0, 10, 25, 50, 100, 200.
- Expert AdamW learning rate 0.001; representation AdamW learning rate 0.0005; betas 0.9/0.999; weight decay \(10^{-4}\).
- 32 seeds. Smoke uses two seeds and 20 steps.
- Each condition activates exactly one expert per token and processes the same sequences.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Correct expert-only | H1/H2 | representation drift | primary causal condition | primary | positive gap and correct > shuffle | no difference | task not learned | utility trajectory |
| Balanced-shuffle expert-only | H1/H4 | count/load artifact | matched negative control | primary | near-zero or lower gap | same as correct | count mismatch | utility trajectory |
| Correct joint | transfer guard | frozen bridge artifact | closer to native co-training | secondary | preserves positive effect | effect disappears | route visibility fails | transfer table |
| Balanced-shuffle joint | transfer control | representation-only gain | isolates identity under drift | secondary | below correct joint | equals correct joint | state mismatch | transfer table |
| Step-0 baseline | metric guard | initialization asymmetry | verifies identical experts | validity | gap near zero | initial feature-specific gap | init mismatch | loss matrix |
| Router-pressure audit | H3 | utility cannot affect gate | tests transmission | secondary | correct pressure > shuffle | no pressure difference | native route invalid | pressure plot |

Full checkpoints: 0, 10, 25, 50, 100, 200. Seeds: 0--31.

## 7. Primary Metric And Decision Rule

For every seed, task \(f\), condition, and checkpoint, force expert \(e\) on held-out task positions and compute \(L_{f,e}^{cf}\). Then compute \(G_f^{cf}\).

The primary decision uses the final expert-only cells:

1. positive-cell rate under correct exposure;
2. paired correct-minus-shuffle \(G_f^{cf}\) at the same seed/task;
3. seed-clustered bootstrap 95% CI for the median paired difference.

Pass requires positive-cell rate \(\ge0.90\) and CI lower bound \(>0\). A positive gap without a correct-versus-shuffle difference is not functional binding evidence because load can explain it.

## 8. Secondary Metrics

- \(T_{bind}\) and area under the median utility-gap trajectory.
- Held-out assigned-expert task loss and all-position loss.
- Feature-by-expert counterfactual loss matrix.
- Task-gradient and full-LM-gradient router boundary pressure.
- Native route NMI and low-tail margin before and after exposure.
- Expert update-count parity and parameter-state parity.
- Train/test sequence overlap count.
- Joint-versus-expert-only utility gap.

## 9. Known Good / Bad / Confusing Cases

- Known good: separately trained task experts should make the assigned diagonal lower than competitors.
- Known bad: identical step-0 experts must have zero counterfactual gap up to numerical tolerance.
- Known confusing: full-LM loss includes instruction-to-content and output-to-next-content positions that do not require the operator. The task-position metric is primary; all-position loss is a guard.
- Known boundary: oracle exposure directly supplies task identity to expert assignment. This tests function formation, not routing discovery.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- |
| Data | Are tasks balanced and train/test disjoint? | exact counts and zero overlap | data audit CSV | validity table |
| Initialization | Are expert states identical and router margins positive? | max expert diff \(\le10^{-7}\); route NMI 1 | init audit | validity table |
| Exposure | Are active expert counts exactly matched? | max count difference 0 | update-count CSV | detailed record |
| Counterfactual evaluation | Are non-expert states held fixed? | state hash unchanged | state audit | validity table |
| Binding | Does correct exposure exceed shuffle? | primary decision rule | gap trajectory and matrix | summary |
| Transmission | Does learned utility create router pressure? | correct > shuffle with positive paired median | pressure CSV/plot | summary if decisive |

## 11. Plot Contracts

### Figure 1: Held-Out Utility-Gap Trajectory

- Question: When and only under which exposure does functional binding emerge?
- Metric: median \(G_f^{cf}\) with seed-clustered interval.
- Unit: nats per task token.
- X-axis: expert-training updates; Y-axis: held-out utility gap.
- Allowed conclusion: correct exposure creates faster/stronger held-out expert binding than matched shuffle.
- Limitation: does not show natural-language transfer.

### Figure 2: Final Counterfactual Loss Matrix

- Question: Is the assigned diagonal functionally better for each task?
- Metric: mean \(L_{f,e}^{cf}\) over seeds at task positions.
- Rows: context-defined tasks; columns: forced experts.
- Allowed conclusion: task-expert functional correspondence under the tested exposure.
- Limitation: oracle assignment was supplied during training.

### Figure 3: Utility-To-Router Pressure

- Question: Does learned utility transmit into a task-aligned router gradient?
- X-axis: \(G_f^{cf}\); Y-axis: assigned-boundary pressure.
- Allowed conclusion: local transmission on this bridge.
- Limitation: not long-run sparse-routing stability.

## 12. Success / Failure / Insufficient Evidence

**Supported:** H1 and all validity guards pass. H3 may be separately supported or weakened.

**Weakened:** A positive correct gap exists but fails the matched-control CI rule; joint training destroys the expert-only effect; or utility forms without router pressure.

**Failed:** Correct and shuffled exposure are indistinguishable despite learnable task and valid controls.

**Insufficient:** Any preregistered validity guard fails.

## 13. What This Cannot Claim

The experiment cannot establish natural-language semantic experts, label-free feature discovery, real downstream improvement, communication savings, scaling laws, MTP value, or a deployable gate.

## 14. Review Notes

- The primary exposure choice is expert-only with frozen representation because it isolates expert function formation.
- Joint exposure is retained as a secondary transfer check using the same primary metric.
- The feature was upgraded from repeated token identity to a sequence-level instruction-defined transformation so that the result bears on long-horizon conditional prediction.
- Run 01 (`a06_38_full_4gpu_20260710_01`) completed 32 seeds but failed validity: minimum native initial route NMI was 0.9198. Its utility results are retained only as an invalid-run diagnostic.
- Protocol amendment for run 02: add a fixed instruction-state broadcast so the supplied partition is natively readable at every task position. No hypothesis, condition, metric, threshold, optimizer, or seed-count change is allowed.
