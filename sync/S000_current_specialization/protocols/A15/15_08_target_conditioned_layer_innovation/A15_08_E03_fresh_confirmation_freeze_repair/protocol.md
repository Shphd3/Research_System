---
experiment_id: A15_08_E03_fresh_confirmation_freeze_repair
anchor_id: 15_08_target_conditioned_layer_innovation
status: APPROVED_FOR_IMPLEMENTATION_AND_ONE_FRESH_CONFIRMATION_RUN
canonical_language: en
approved_scope: implementation_tests_fresh_confirmation_extraction_and_one_evaluation
approved: 2026-08-10
design_frozen_at: 2026-08-10T18:53:00Z
registered_revision: A15_08_E03_v1
---

# Protocol: A15_08_E03 Fresh-Confirmation Freeze Repair

## 0. Approval And Repair Snapshot

- **Approval basis:** the researcher authorized completion of the logically
  correct first experiment without another approval pause. Independent audit
  found that E02 used confirmation labels structurally before its freeze; one
  fresh-confirmation eligibility repair is inside that delegated scope.
- **Why this is a new experiment:** E02 confirmation is open and remains
  `INELIGIBLE_PROTOCOL_CONFIRMATION_LABEL_PREUSE`. E03 changes the data-access
  order and uses wholly new confirmation episodes. It cannot amend or upgrade
  E02.
- **Question:** with every TRAIN/DEVELOPMENT-selected readout, residualizer,
  direction, control model, seed, and label-free bank recipe frozen before a
  new confirmation set exists, does the layer-25 normalized attention
  transition add terminal-code accessibility beyond the old state; if so, are
  the same two conditional-innovation directions sufficient?
- **Primary condition:** complex two-hop composition. Simple is secondary.
- **Not tested:** adjacent Transformer blocks, global representation rank,
  Shannon-information creation, natural language, native model use, expert
  utility, or Router gain.
- **Authorization boundary:** one implementation/test cycle, one fresh
  confirmation generation and extraction, and one evaluation. No rank ladder
  or Router experiment is authorized by this Protocol.

## 1. Frozen Scientific Objects

At the final `Answer:` token of Qwen3-8B block 25,

$$
X=N_{25}(h),\qquad Z=N_{25}(h+a),\qquad U=Z-X,
$$

and

$$
R_U=U-\widehat{\mathbb E}_{lin}[U\mid X].
$$

$U$ is the exact normalized attention transition, not knowledge by definition.
$R_U$ removes only the linear component predicted from $X$ under the frozen E02
TRAIN residualizer. It becomes evidence for added accessibility only through
the fresh held-out loss comparisons below.

E03 freezes and reuses only E02 objects selected from TRAIN/DEVELOPMENT:

| Object | Frozen source | Required SHA-256 |
| --- | --- | --- |
| old/new/full/top-two and 192 control readouts | `frozen_linear_models.npz` | `8793a01646bdb44aef809ccaedbbf0819cfdfe7cc982c90d5a59915dfb764173` |
| primary/random/permutation directions | `frozen_directions.npz` | `390bcc3d37859a6ac041861294f7e2d7f6a72cfb2e6a9b31b1def745dda671de` |
| E02 selection provenance | `frozen_selection_control_ledger.json` | `a0f468f9f27ea630a76edc62e0ed5a09e74589e7cab74ce2c27557547b947dce` |
| simple E02 TRAIN representation | `representations.pt` | `cca41dc103e3066d5ebd1d515e561aab8e95002ed41e1d1ac488cc5b839d720c` |
| complex E02 TRAIN representation | `representations.pt` | `4e1032c3c508f7849a58f17bd2c9310d0a6d4db08fc8eb806db19ad1c77d4919` |

The E02 confirmation maps, losses, gains, bootstrap samples, and result values
are forbidden inputs. E03 may read the E02 selection ledger only for named
TRAIN/DEVELOPMENT hyperparameters and hashes. It must recompute and freeze the
two update residualizer systems from E02 TRAIN rows only, verify agreement with
the frozen DEVELOPMENT reconstruction values, and never refit or reselect a
readout, direction, rank, ridge, or threshold.

## 2. Hypotheses And Strongest Rival

**H2 — target-conditioned added accessibility.** On fresh complex confirmation
episodes, the frozen full-$R_U$ correction lowers terminal-code cross-entropy
beyond the frozen old-state readout, the frozen $Z$ readout gives the same sign,
and the true gain exceeds the within-bootstrap q95 of 64 target-independent
balanced-bank controls.

**H1' — frozen rank-two sufficiency.** Only after H2 Pass, the same two E02
TRAIN/DEVELOPMENT-selected directions retain at least 80% of the full-$R_U$
gain and exceed the q95 of the same 64 random and 64 TRAIN-label-permutation
control models under paired episode resampling.

**Strongest rival:** a same-budget correction branch or a target-correlated
control construction can mimic an update gain. The balanced bank recipes and
same-dimensional $Z$ versus $X$ comparison separate this rival. H1' remains a
rank-two retrieval claim, not the meeting hypothesis that the whole
representation is low rank.

## 3. Pre-Confirmation Freeze Contract

Before E03 confirmation JSON, tensors, labels, groups, logits, or paths exist,
write a content-hashed `preconfirmation_freeze.json` and receipt containing:

1. hashes of this Protocol and all E03 code/tests;
2. hashes of every frozen E02 input listed in Section 1;
3. a frozen TRAIN-only residualizer artifact for each condition, including old
   and update scalers, dual/primal prediction state, ridge, and a
   DEVELOPMENT-only reconstruction check;
4. the immutable readout/direction artifact hashes;
5. 64 mismatch seeds 6200--6263, a new confirmation split salt, and only the
   label-free bank algorithm identifier;
6. random seeds 6300--6363, permutation seeds 6400--6463, rank two, and the
   frozen selected models/directions;
7. fresh data seed 7103, 128 episodes, eight records per condition and episode,
   the fixed prose-table wording family, generation ID, and no-overlap guard;
8. 2,000 paired episode bootstrap draws with seed 7281 and NumPy
   `method="higher"` q95.

The freeze payload must not contain a confirmation label, target-source
contingency, index map, source label, per-record feature, loss, gain, or result.
Its receipt must state that the fresh confirmation root was absent at freeze
time. Tests must reject any recipe containing such fields and any attempt to
load fresh labels before a valid receipt is verified.

## 4. Fresh Confirmation Data

Generate only a new CONFIRMATION split after the Section 3 receipt:

| Split | Episodes | Records per condition | Seed | Wording |
| --- | ---: | ---: | ---: | --- |
| CONFIRMATION | 128 | 1,024 | 7103 | prose table |

Every episode contains all eight terminal targets once in both the simple and
complex conditions. Conditions share the same map context, intermediate state,
and terminal answer. Record, pair, map, episode, and generation IDs use a new
`innovation-e03-*` namespace. Exact prompt/context hashes must have zero
collision with every E01/E02 TRAIN/DEVELOPMENT/CONFIRMATION record.

The generated data manifest and SHA-256 values are appended to a data receipt.
They cannot change the already frozen seed, size, schema, or generator. Any
count, balance, pair, collision, or namespace failure is
`INELIGIBLE_GUARD`.

## 5. Model Extraction And Capability

- Frozen `/data/share/Qwen3-8B`, bfloat16, SDPA, `use_cache=False`.
- Block index 24 / reported layer 25; final prompt token only.
- Compute $X,Z,U$ in float32 with the same post-attention norm.
- Restricted-choice accuracy must be at least 0.80 simple and 0.60 complex.
- Replay max error $\le10^{-5}$, direct `o_proj` relative error $\le10^{-5}$,
  and stored $Z-X-U$ relative error $\le10^{-6}$.
- Extraction may read labels only after the preconfirmation receipt is verified.
  Capability is a validity guard and cannot select a model or rescue a verdict.

## 6. Post-Freeze Bank Materialization

Only after verifying the immutable preconfirmation receipt may the evaluator
open fresh labels and groups. For each seed, partition the 128 episodes into
blocks of eight. Within each block, use the frozen randomized base permutation
and all eight cyclic offsets in randomized order so that every target is paired
once with every source label.

For every bank:

- the $8\times8$ target-source contingency must have every cell equal to 16;
- empirical target-source mutual information must be zero to $10^{-12}$;
- every map must remain inside its episode and be a permutation;
- actual mapping arrays, not hashes containing split names, must differ from
  the E02 confirmation arrays and from one another except at chance-level
  coincidences allowed by the construction;
- no fitted weight or hyperparameter may change after materialization.

The materialized maps and audit are post-freeze evidence. A premature label
read, invalid receipt, reused E02 confirmation map, nonuniform bank, incomplete
family, or weight change yields `INELIGIBLE_GUARD`.

## 7. Metrics And Verdict Mapping

For every fresh complex confirmation record, compute

$$
g_{true}=CE(f_X(X))-CE(f_X(X)+g_{full}(R_U)),
$$

$$
g_{state}=CE(f_X(X))-CE(f_Z(Z)),
$$

and all 64 mismatch, random, and permutation gains with frozen models. Treat the
complete eight-target episode as the independent unit.

For each paired bootstrap draw,

$$
T_{cap}=G_{true}-Q_{0.95}^{higher}(G_{mismatch,1:64}),
$$

$$
D_{80}=G_2-0.8G_{true},\quad
T_{random}=G_2-Q_{0.95}^{higher}(G_{random,1:64}),
$$

$$
T_{perm}=G_2-Q_{0.95}^{higher}(G_{perm,1:64}).
$$

Report percentile 95% intervals.

- H2 Pass: lower bounds of $G_{true}$, $G_{state}$, and $T_{cap}$ are all
  strictly positive.
- H2 Fail: the upper bound of $G_{true}$ is non-positive.
- Otherwise: H2 Insufficient.
- Only after H2 Pass, H1' Pass requires positive lower bounds for $D_{80}$,
  $T_{random}$, and $T_{perm}$.
- H1' Fail: any one of their upper bounds is non-positive.
- Otherwise: H1' Insufficient.

Allowed joint labels are `H2_PASS_H1_PASS`, `H2_PASS_H1_FAIL`,
`H2_PASS_H1_INSUFFICIENT`, `H2_FAIL_H1_NOT_ADJUDICATED`,
`H2_INSUFFICIENT_H1_NOT_ADJUDICATED`, and `INELIGIBLE_GUARD`.

E02 values cannot be pooled, averaged, used as a prior, or used to choose the
E03 wording. Simple-condition evidence cannot upgrade the primary verdict.

## 8. Required Tests, Evidence, And Stage Stops

| Stage | Input | Output | Stop rule |
| --- | --- | --- | --- |
| S0 implementation | code plus synthetic fixtures | test log | any test failure |
| S1 preconfirmation freeze | E02 TRAIN/DEV artifacts plus label-free recipe | hashed freeze + receipt | fresh confirmation exists, forbidden field, hash mismatch, or DEV mismatch |
| S2 fresh data | frozen seed/schema | JSON + manifest + overlap audit | count, balance, namespace, or collision failure |
| S3 extraction | verified receipt + fresh JSON | simple/complex tensors and logs | capability or hook guard failure |
| S4 post-freeze banks | verified receipt + fresh labels/groups | 64 maps + audits | any invalid/reused map or incomplete family |
| S5 one evaluation | frozen models/directions + fresh tensors/maps | per-record/episode arrays, bootstrap, verdict | any nonfinite value, weight/hash change, or missing array |
| S6 records | eligible evidence | summary, detailed, Anchor, daily report | lineage or cold-read failure |

Required mutation tests include premature-label access, forbidden recipe fields,
changed frozen hashes, a reused E02 confirmation map, a mapping-hash-only false
positive, nonuniform contingency, episode leakage, and result computation before
receipt verification.

## 9. Outputs And Claim Boundary

Worker run root:
`runs/a15-08-e03-fresh-confirmation-freeze-repair-20260810/`.

Canonical record root:
`Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E03_fresh_confirmation_freeze_repair/`.

Required artifacts include Protocol/code/input hashes, preconfirmation freeze and
receipt, fresh data/overlap manifest, extraction manifests/logs, post-freeze bank
maps/audits, all per-record/per-episode/per-control/bootstrap arrays, result JSON,
environment receipt, plot contracts, figures, and artifact manifest.

Even an eligible joint Pass establishes only target- and linear-family-specific
added accessibility for one normalized layer-25 attention transition and the
registered rank-two sufficiency clause. It does not establish adjacent-layer
novelty, whole-representation low rank, native use, expert utility, or Router
gain.

**Exactly one post-result decision:** if H2 passes and H1' fails, open one
fresh-data rank-ladder design; if both pass, open one independent functional
admission design; if H2 is insufficient, open only a precision decision; if H2
fails, close this named linear object. No downstream branch is active before an
eligible E03 verdict.

The scientific body is frozen as `A15_08_E03_v1` before E03 data generation.
After the first generation command, changes require an append-only amendment
stating before/after values, timing, authorization basis, and eligibility impact.

### Pre-execution clarification A1 — actual-map reuse guard without an E02 map input

- **Time:** 2026-08-10T19:01:44Z, before E03 preconfirmation freeze or data
  generation.
- **Ambiguity:** Section 1 forbids E02 confirmation maps as E03 runtime inputs,
  while Section 6 requires a guard against exact reuse of an E02 actual mapping
  array and rejects split-name mapping-key hashes as insufficient.
- **Controlling realization:** before E03 starts, compute and hard-freeze only
  the canonical byte SHA-256 of each of the 64 E02 confirmation index arrays and
  the ordered list hash. Do not load the E02 bank NPZ during any E03 stage.
  After E03 labels are opened and its arrays are materialized, hash each actual
  E03 index array in the same canonical dtype/shape convention and require zero
  exact slice-hash collision with the frozen E02 list.
- **Boundary:** the hashes are provenance guards only. They cannot construct an
  E03 map, fit a model, select a seed, or enter a loss or metric.
- **Eligibility impact:** none. This resolves the guard implementation before
  any E03 data or result exists and preserves the stronger forbidden-input rule.
