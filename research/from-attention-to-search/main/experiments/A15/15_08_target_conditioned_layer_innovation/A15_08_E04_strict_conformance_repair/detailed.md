# Detailed: A15_08_E04 Strict-Conformance Repair

Primary Anchor: [A15_08 Target-Conditioned Layer Innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)  
Frozen Protocol and registered revision: [A15_08_E04_v1](protocol.md), SHA-256 `5072d76d9a44877e270b910424ea255ffee347dc17097640c88e20200d82a27d`  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE` after S0--S6  
Knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`; the evidence eligibility, direct measurements, and registered verdict are fixed.

## 0. Quick Recap

**Purpose:** replace the ineligible E03 confirmation run with one strictly
conforming fresh run without changing the scientific question or any selected
scientific object.

**Why E03 cannot carry the claim:** E03 did not instantiate every registered
namespaced identity field and its evidence bundle omitted exact extraction-
command receipts, complete simple episode/bootstrap arrays, and a full
registered-family manifest. It is therefore `INELIGIBLE_GUARD`; its measured
numbers remain diagnostic only and were neither pooled into nor used to select
E04.

**Hypotheses:** local H2 predicts that the residualized normalized layer-25
attention transition adds fresh terminal-code accessibility beyond the old
state and target-independent same-budget controls. Conditional on H2 passing,
H1' predicts that the two frozen target-conditioned innovation directions
retain at least 80% of the full gain and beat equal-rank random and
TRAIN-label-permutation controls.

**Experiment logic:** before an E04 run or data root existed, freeze the E04
Protocol/code, all E02 TRAIN/DEVELOPMENT-selected readouts, residualizers,
directions, ranks, thresholds, control recipes, and bootstrap rule. Then create
128 fully namespaced fresh episodes, extract one simple and one complex
condition, materialize balanced controls only after authorized label access,
and perform one registered paired-episode evaluation.

**Direct result:** in the primary complex condition,
\(G_{true}=0.767207\) nats/example with paired episode-bootstrap 95% interval
\([0.751296,0.785146]\). The rank-two gain was
\(G_2=0.255052\ [0.244938,0.264427]\), or 33.24% of the full point gain.

**Eligibility:** the final record audit reports `eligible=true`, all required
artifacts complete, 59 manifest entries, and all 39 required artifact families
present. All data-identity, overlap, extraction, bank, access-order, hash, and
finite-value guards passed.

**Verdict:** `H2_PASS_H1_FAIL`. The machine field `h1=FAIL` refers only to H1'
rank-two sufficiency, not to the meeting's global low-rank hypothesis.

**Claim boundary:** one target- and linear-family-specific result for one
normalized answer-token attention transition; not adjacent-block novelty,
global representation rank, native use, expert utility, or Router gain.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| \(X\) | matched state before the attention write | layer-25 post-attention normalization applied to the pre-write residual stream | \(X=N_{25}(h)\in\mathbb R^{4096}\) | registered old-state baseline | all information nonlinearly available from the model |
| \(Z\) | matched state after the same attention write | the same normalization applied after adding attention output \(a\) | \(Z=N_{25}(h+a)\in\mathbb R^{4096}\) | same-dimensional state comparison | an adjacent Transformer block or complete retention of \(X\) |
| \(U\) | exact computation change in the common hidden coordinate | direct matched-state subtraction | \(U=Z-X\) | gives a valid difference object without comparing unrelated PCA bases | new knowledge merely because it is nonzero |
| \(R_U\) | part of \(U\) not linearly predicted from \(X\) | frozen E02 TRAIN-only ridge residualizer | \(R_U=U-\widehat{\mathbb E}_{lin}[U\mid X]\) | removes the registered linear old-state prediction | nonlinear independence from \(X\) |
| \(Y_c\) | centered terminal target | centered one-hot vector over eight terminal codes | \(Y_c\in\mathbb R^8\) | names the supervised distinction | general semantics or factual knowledge |
| \(R_Y\) | target component not linearly predicted from \(X\) | target residual under the frozen old-state linear family | \(R_Y=Y_c-\widehat{\mathbb E}_{lin}[Y_c\mid X]\) | conditions the direction search on target structure beyond the registered \(X\) readout | absence of nonlinear target information in \(X\) |
| \(K_{new}\) | target-conditioned direction-ranking matrix | \(C_{UY}=\operatorname{Cov}(R_U,R_Y)\) and \(S_Y=\operatorname{Cov}(R_Y)\) | \(K_{new}=C_{UY}S_Y^{+}C_{UY}^{\top}\) | selects candidate \(R_U\) directions on E02 TRAIN/DEVELOPMENT only | a covariance of newly created knowledge or a deployable Router |
| \(G_{true}\) | gain from full residual update | old-state CE minus old-plus-full-\(R_U\) CE | nats/example | primary H2 effect | native use of the signal by Qwen3-8B |
| \(G_{state}\) | gain from reading the new state | old-state CE minus frozen \(Z\)-readout CE | nats/example | same-dimensional H2 sign guard | that \(Z\) contains all distinctions in \(X\) |
| \(G_2\) | gain from two frozen directions | old-state CE minus old-plus-top-two-\(R_U\) CE | nats/example | rank-two retrieval effect | 80% sufficiency by itself |
| \(T_{cap}\) | full gain beyond generic correction capacity | within each paired draw, \(G_{true}\) minus the higher-method q95 across 64 balanced-mismatch gains | nats/example | separates the registered target-independent correction rival | uniqueness against every possible control family |
| \(D_{80}\) | 80%-retention contrast | \(D_{80}=G_2-0.8G_{true}\) | nats/example | registered H1' sufficiency gate | the optimal compression rank |
| \(T_{random}\) | top-two gain beyond random rank-two directions | \(G_2\) minus within-draw higher-method q95 across 64 random controls | nats/example | equal-rank geometry null | 80% retention |
| \(T_{perm}\) | top-two gain beyond directions selected with permuted TRAIN targets | \(G_2\) minus within-draw higher-method q95 across 64 permutation controls | nats/example | target-conditioning null | target-independent deployment |
| episode bootstrap | uncertainty calculation that preserves the eight-target group | resample 128 complete episodes with replacement and apply the same sampled indices to treatments and controls | 2,000 draws, seed 8281 | respects the registered independence unit | population generality beyond this generator |
| conformance-only repair | fresh execution that changes validity guards but no scientific object | E04 adds the exact ID schema, structured stage receipts, complete secondary arrays, and full manifest | eligibility classification | prevents E03's record defects from being reinterpreted as valid evidence | independent replication of a different hypothesis |

The superscript \(+\) denotes the Moore--Penrose pseudoinverse. Cross-entropy
(CE) is the negative log probability of the correct one of eight terminal
codes, so a positive gain means fewer nats of predictive loss.

## 2. Anchor Link And Decision Point

The owning [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)
separates two questions: first, whether a named deeper computation makes a
target distinction newly accessible beyond the shallower-state readout;
second, how compactly that accessible difference can be retrieved.

E04 decides exactly this bounded question:

> On fresh complex confirmation episodes, does frozen full \(R_U\) improve
> terminal-code prediction beyond \(X\), agree in sign with the same-dimensional
> \(Z\) comparison, and beat the 64 target-independent balanced-mismatch
> controls; conditional on that Pass, do the two frozen \(K_{new}\) directions
> retain at least 80% while beating 64 random and 64 TRAIN-label-permutation
> rank-two controls?

The registered answer is **yes for local H2 and no for H1' at rank two**.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| E03 boundary | E03 must remain ineligible and cannot be upgraded by E04 | no E03 result, loss, gain, bootstrap draw, direction, threshold, or hyperparameter entered E04; only pre-frozen collision hashes were used | Pass | [E04 Protocol](protocol.md), [prior-data guard](evidence/prior_confirmation_data_collision_hashes.json), [prior-map guard](evidence/prior_confirmation_map_content_hashes.json) | E03 remains `INELIGIBLE_GUARD`; E04 stands on fresh evidence |
| revision and scope | A15_08_E04_v1; one implementation/test cycle, one fresh generation/extraction, one evaluation and complete record | exactly that scientific scope; no rank ladder or Router run | Pass | [Protocol](protocol.md), [evaluation receipt](evidence/evaluation_receipt.json) | none |
| preconfirmation state | E04 run/data roots absent; zero label access; no materialized bank | both roots absent; access count zero; labels not loaded; bank not materialized | Pass | [freeze ledger](evidence/preconfirmation_freeze.json), [freeze receipt](evidence/preconfirmation_freeze_receipt.json) | none |
| frozen scientific inputs | exact hashes for E02 models, directions, selection ledger, two TRAIN representations, residualizers, rank, threshold, and nulls | all registered hashes verified; E02 TRAIN/DEVELOPMENT selections reused without refit | Pass | [freeze ledger](evidence/preconfirmation_freeze.json), [residualizer receipt](evidence/frozen_e02_train_residualizers_receipt.json) | none |
| exact identity schema | integer `episode`; namespaced `episode_id`, `map_id`, `pair_id`, `record_id`; exact `generation_id` | all six fields instantiated consistently on 2,048 records across 128 episodes | Pass | [data manifest](evidence/data_manifest.json), [public manifest](evidence/confirmation_public_manifest.json) | repairs E03 ID defect |
| fresh-data overlap | no comparable ID, context, or text collision with E01/E02/E03 | zero collisions across all six audited fields; historical raw data not loaded after freeze | Pass | [data manifest](evidence/data_manifest.json) | none |
| authorized label order | labels and actual bank arrays only after verified freeze | all seven events occurred in order; no early load or materialization | Pass | [final trace](evidence/eligibility_trace.jsonl), [eligibility audit](evidence/eligibility_audit.json) | none |
| extraction | Qwen3-8B layer 25; accuracy \(\geq .80\) simple and \(\geq .60\) complex; replay/output-projection/difference guards | accuracy .993164 simple and .776367 complex; reconstruction errors all zero | Pass | [simple manifest](evidence/simple_extraction_manifest.json), [complex manifest](evidence/complex_extraction_manifest.json) | none |
| success receipts | exact wrapper/child argv, timing, cwd, environment, inputs, outputs, hashes, and status for every successful stage | complete receipts for freeze, generation, both extractions, and evaluation | Pass | [freeze-stage](evidence/freeze_stage_receipt.json), [generation](evidence/generation_receipt.json), [simple extraction](evidence/simple_extraction_receipt.json), [complex extraction](evidence/complex_extraction_receipt.json), [evaluation](evidence/evaluation_receipt.json) | repairs E03 receipt defect |
| balanced mismatch family | 64 episode-local permutations; every \(8\times8\) cell 16; MI zero; all arrays distinct; no E02/E03 actual-map reuse | 64/64 valid; all cells 16; all MI exactly 0; zero prior reuse | Pass | [bank audit](evidence/materialized_confirmation_bank_audit.json), worker bank arrays identified in [full manifest](evidence/full_artifact_manifest.json) | none |
| uncertainty | 128 complete episodes; 2,000 paired draws, seed 8281; `method=higher` q95 recomputed inside each draw | exact registered arrays and computation | Pass | [complex arrays](evidence/complex_confirmation_arrays.npz), [result](evidence/result.json) | none |
| secondary simple arrays | record, episode, sampled-index, and bootstrap arrays for \(G_{true}\), \(G_{state}\), \(G_2\), and \(D_{80}\) | all 14 required arrays present | Pass | [simple arrays](evidence/simple_confirmation_arrays.npz) | repairs E03 secondary-array defect; remains non-verdict-bearing |
| full evidence manifest | all 39 registered families, with path, SHA-256, size, stage, completeness, and claim eligibility | 59 artifacts; 39/39 families; `all_complete=true` | Pass | [full manifest](evidence/full_artifact_manifest.json), [record audit](evidence/record_completeness_audit.json) | repairs E03 partial-manifest defect and qualifies S6 |

**Frozen Protocol revision:** `A15_08_E04_v1`, frozen at
2026-08-11 02:01:28 UTC before either fresh root existed. The Protocol itself
was frozen earlier at 01:42:30 UTC and hashes to
`5072d76d9a44877e270b910424ea255ffee347dc17097640c88e20200d82a27d`.

**Execution scope approved:** implementation/tests, one fresh confirmation
generation, one extraction per registered condition, one evaluation, and
completion of the evidence record.

**Amendments:** none after the scientific body was frozen. No observed E04
value changed a model, direction, rank, threshold, control recipe, seed,
bootstrap rule, or verdict mapping.

**Retries and exclusions:** four pre-scientific simple-extraction invocations
failed before a model forward pass or scientific output: missing
`transformers`, an ONNX/protobuf import incompatibility, missing `accelerate`,
and one command that omitted `--freeze-receipt` and exited in argument parsing.
An isolated virtual environment was also attempted but could not be completed
because the system interpreter lacked `ensurepip`/`python3.10-venv`. The
successful environment was locked before extraction. No generated record,
episode, tensor, or metric was excluded.

Attempt 1's fixed-path wrapper receipt was overwritten by attempt 2 before the
operator noticed; its preserved file is therefore a reconstruction from the
immediately observed traceback, not raw stdout. This is an explicit retry-
record limitation. It does not enter the scientific aggregate: the attempt
failed at import, produced no output, and all required successful-stage
receipts and 39 registered artifact families pass the final audit.

**Environment repair:** the runtime added `transformers==4.51.0`,
`protobuf==3.20.3`, and `accelerate==1.6.0`; the frozen code and all scientific
inputs remained byte-identical. The complete runtime versions and the unused
`cudf` protobuf compatibility tradeoff are recorded in the
[environment lock](evidence/execution_environment_lock.json).

**Missing conditions or artifacts:** none among the registered E04 scientific
conditions or artifact families. The rank ladder and Router are intentionally
`NOT_RUN` and outside the approved scope.

**Post-hoc analyses:** document-level verification only. The independent
[cold-read audit](evidence/independent_cold_read_audit.json) rechecked 47/47
provenance and computation items, reconstructed the registered metrics from
the saved arrays, and found no fatal discrepancy. No post-hoc metric, band,
direction, rank, or threshold enters the registered verdict.

## 4. Actual Setup

**Research question:** the decision in Section 2.

**Data construction and provenance:** a synthetic composition task with eight
terminal codes. Each complete episode contains all eight codes once in the
simple condition and once in the complex two-hop condition. E04 uses prose-
table wording and the `innovation-e04-` namespace. Generation seed 8103
produced 128 confirmation-only episodes, 1,024 records per condition and 2,048
records total. There was no E04 TRAIN or DEVELOPMENT split.

**Freshness:** the collision audit compared `record_id`, `pair_id`,
`episode_id`, `map_id`, full context, and full text against E01, E02, and E03.
It found zero collisions. The actual prior data were used only before freeze
to create immutable collision hashes and were not loaded after freeze.

**Train / development / confirmation boundary:** E04 trained and selected
nothing. It reused E02 TRAIN/DEVELOPMENT-only assets. Each frozen residualizer
used 1,024 E02 TRAIN rows and was checked against 512 E02 DEVELOPMENT rows,
with zero confirmation rows, labels, logits, results, or data JSON read. Ridge
\(\lambda\) was 10 for simple and 1,000 for complex.

**Learning task and permitted supervision:** predict one of eight terminal
codes at the final Answer token with frozen linear readouts. E02 labels were
used only in the frozen TRAIN/DEVELOPMENT selection. E04 labels were opened
only after the freeze receipt had been verified, and they could evaluate but
not refit or select an object.

**Model / architecture / algorithm:** frozen `/data/share/Qwen3-8B`, bfloat16,
SDPA, `use_cache=False`; block index 24, reported layer 25; final prompt token
only. Each stored state has dimension 4,096.

**Input representation / position encoding:** original prompt tokens and the
model's native tokenizer/position mechanism were unchanged. The experiment
changed only which frozen feature or correction entered a terminal-code
linear readout.

**Training objective and constraints:** no E04 optimization. The E02-frozen
old-state, new-state, full-\(R_U\), top-two, 64 random-rank-two, and 64
TRAIN-label-permutation readouts/directions were immutable. E04 confirmation
could not select a ridge, direction, rank, control, condition, or threshold.

**Optimizer or update rule:** none in E04. Residualizers are closed-form frozen
ridge systems reconstructed from the E02 TRAIN representations.

**Training steps / tokens / batch size:** no training steps. Extraction batch
size 16; maximum prompt length 243 tokens simple and 246 complex.

**Checkpoints:** frozen Qwen3-8B, E02 `frozen_linear_models.npz`, E02
`frozen_directions.npz`, the E02 selection ledger, and the frozen TRAIN-only
residualizer. E04 learned no checkpoint.

**Seeds:** generation 8103; balanced mismatch recipes 8200--8263; frozen random
rank-two directions 6300--6363; frozen TRAIN-label-permutation directions
6400--6463; paired bootstrap 8281.

**Conditions and plain-language labels:**

| Label | Meaning | Decision role |
| --- | --- | --- |
| complex | two-hop composition requiring the full relation chain | primary condition |
| simple | simpler composition companion | secondary only; cannot change verdict |
| old \(X\) | frozen baseline readout of the pre-write state | comparator |
| new \(Z\) | frozen readout of the matched post-write state | H2 sign guard |
| old + full \(R_U\) | full residual-update correction added to old logits | H2 treatment |
| old + top-two \(R_U\) | correction from the two frozen target-conditioned directions | H1' treatment |
| balanced mismatch | episode-balanced target-independent correction | H2 generic-capacity rival |
| random rank two | equal-rank random direction | H1' geometry null |
| TRAIN-label permutation rank two | equal-rank direction selected using permuted TRAIN targets | H1' target-conditioning null |

**Changed variable:** the frozen state/correction supplied beyond the old-state
readout.

**Held fixed:** model, hook, answer token, records, target, readout family,
fitted budget, E02 selections, rank two, 80% threshold, 64-control budgets,
episode unit, bootstrap draws/seed, and verdict rules.

**Code / config / data identities:** full hashes are in Sections 10 and 14.
The central identities are Protocol `5072d76d...a27d`, evaluator
`87fe1d0d...2c69`, E02 readouts `8793a016...173`, directions
`390bcc3d...1de`, complex JSON `ddf914f6...32b`, and complex representation
`90c4b795...16`.

**Known setup limitations:** one model, one normalized attention transition,
one token position, one synthetic target family, one fresh generation seed,
and linear readout/correction families. E04 does not compare arbitrary layer
pairs and does not measure deployment performance.

## 5. Metrics And Registered Decision Rules

For each complex confirmation record,

\[
g_{true}=CE(f_X(X))-CE\!\left(f_X(X)+g_{full}(R_U)\right),
\]

\[
g_{state}=CE(f_X(X))-CE(f_Z(Z)),
\]

and \(g_2\) analogously replaces \(g_{full}(R_U)\) with the frozen top-two
correction. Capital \(G\) denotes the equal-weight mean over the 128 complete
episodes, in nats/example.

In each of 2,000 paired episode-bootstrap draws,

\[
T_{cap}=G_{true}-Q_{0.95}^{higher}(G_{mismatch,1:64}),
\]

\[
D_{80}=G_2-0.8G_{true},
\]

\[
T_{random}=G_2-Q_{0.95}^{higher}(G_{random,1:64}),\qquad
T_{perm}=G_2-Q_{0.95}^{higher}(G_{perm,1:64}).
\]

The same bootstrap episode indices are applied to every treatment and control,
and each q95 is recomputed inside its draw with NumPy `method=higher`.
Reported intervals are percentile 95% intervals.

- H2 Pass requires strictly positive lower bounds for \(G_{true}\),
  \(G_{state}\), and \(T_{cap}\).
- H2 Fail requires a non-positive upper bound for \(G_{true}\); otherwise H2 is
  Insufficient.
- Only after H2 Pass, H1' Pass requires strictly positive lower bounds for
  \(D_{80}\), \(T_{random}\), and \(T_{perm}\).
- H1' Fail requires any one of those three upper bounds to be non-positive;
  otherwise H1' is Insufficient.
- Simple is secondary and cannot modify the verdict. E01/E02/E03 values cannot
  be pooled, averaged, used as priors, or used to select E04 wording or any
  scientific object.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full residual update adds accessibility | lower 95% bound of \(G_{true}>0\) | [complex arrays](evidence/complex_confirmation_arrays.npz), [per-record table](tables/confirmation_per_record_core.csv) | frozen E04 evaluator applies E02-frozen \(f_X\) and \(g_{full}\) | 128 complete episodes; 2,000 paired draws, seed 8281 | \(0.767207\ [0.751296,0.785146]\) nats/example | eligible | H2 component Pass | frozen linear correction family only |
| same-dimensional new state has the same sign | lower bound of \(G_{state}>0\) | [complex arrays](evidence/complex_confirmation_arrays.npz), [per-record table](tables/confirmation_per_record_core.csv) | old CE minus frozen \(Z\)-readout CE | same episodes and paired draws | \(0.754508\ [0.738226,0.773069]\) | eligible | H2 guard Pass | no containment claim for \(Z\) |
| effect exceeds registered generic correction capacity | lower bound of \(T_{cap}>0\) | [complex arrays](evidence/complex_confirmation_arrays.npz), [control table](tables/confirmation_control_per_episode_gains.csv) | recompute higher q95 across 64 balanced mismatch means inside every draw | paired episode bootstrap | \(0.766839\ [0.750643,0.784307]\) | eligible; 64/64 bank checks Pass | H2 control Pass | bounded to this target-independent family |
| rank two retains 80% | lower bound of \(D_{80}>0\) | [complex arrays](evidence/complex_confirmation_arrays.npz) | \(G_2-0.8G_{true}\) with frozen rank two | paired episode bootstrap | \(-0.358713\ [-0.369760,-0.348675]\) | eligible; read only after H2 Pass | **H1' Fail** | tests rank two only |
| rank two beats equal-rank random geometry | lower bound of \(T_{random}>0\) | [complex arrays](evidence/complex_confirmation_arrays.npz), [control table](tables/confirmation_control_per_episode_gains.csv) | within-draw higher q95 across 64 frozen random rank-two gains | paired episode bootstrap | \(0.034265\ [0.024293,0.040979]\) | eligible | random-null clause Pass | cannot rescue 80% retention |
| rank two beats TRAIN-label-permutation null | lower bound of \(T_{perm}>0\) | [complex arrays](evidence/complex_confirmation_arrays.npz), [control table](tables/confirmation_control_per_episode_gains.csv) | within-draw higher q95 across 64 frozen permutation-control gains | paired episode bootstrap | \(0.234832\ [0.224277,0.244831]\) | eligible | permutation-null clause Pass | cannot rescue 80% retention |
| the run can carry the registered verdict | access order, exact data schema, successful receipts, frozen hashes, complete banks and all required artifact families Pass | [trace](evidence/eligibility_trace.jsonl), [data manifest](evidence/data_manifest.json), [receipts](evidence/evaluation_receipt.json), [record audit](evidence/record_completeness_audit.json) | independent schema/order/hash/family audits | seven ordered events; 59 artifacts; 39/39 families | all audits `all_pass=true` or `eligible=true` | eligible | permits `H2_PASS_H1_FAIL` | failed setup attempts are non-scientific retry evidence |
| simple companion result | secondary only; cannot change verdict | [simple arrays](evidence/simple_confirmation_arrays.npz) | same frozen feature family, with no registered simple control family | 128 episodes; same 2,000 sampled-index draws | \(G_{true}=0.048998\ [0.033461,0.063827]\); \(D_{80}=-0.009264\ [-0.019817,0.002500]\) | complete but non-verdict-bearing | bounded secondary observation | cannot upgrade or downgrade H2/H1' |
| E03 numerical output cannot adjudicate this claim | E03 must satisfy its own frozen guards; E04 cannot amend it | E03 record plus E04 repair declaration | final cold-read classification | no pooling or averaging | `INELIGIBLE_GUARD` | ineligible | no scientific verdict from E03 | numbers may be diagnostic only |

## 7. Main Results

### 7.1 Eligible Decision Evidence: Complex Condition

| Quantity | Point estimate | Paired 95% interval | Registered role |
| --- | ---: | ---: | --- |
| \(G_{true}\) | 0.767207 | [0.751296, 0.785146] | H2 existence gate: Pass |
| \(G_{state}\) | 0.754508 | [0.738226, 0.773069] | H2 same-dimensional sign guard: Pass |
| \(G_2\) | 0.255052 | [0.244938, 0.264427] | rank-two retrieved gain; 33.24% of full point gain |
| \(T_{cap}\) | 0.766839 | [0.750643, 0.784307] | H2 balanced-mismatch guard: Pass |
| \(D_{80}\) | -0.358713 | [-0.369760, -0.348675] | H1' 80%-retention gate: **Fail** |
| \(T_{random}\) | 0.034265 | [0.024293, 0.040979] | random-rank-two null: Pass |
| \(T_{perm}\) | 0.234832 | [0.224277, 0.244831] | TRAIN-label-permutation null: Pass |

The point q95 gains of the three 64-control families were 0.000368 for
balanced mismatch, 0.220787 for random rank two, and 0.020221 for
TRAIN-label permutation. These point q95 values are descriptive; the verdict
uses the q95 recomputed inside every paired bootstrap draw.

| Frozen readout condition | Mean complex cross-entropy (nats/example) |
| --- | ---: |
| old state \(X\) | 2.066253 |
| new state \(Z\) | 1.311745 |
| old + full \(R_U\) | 1.299046 |
| old + top-two \(R_U\) | 1.811201 |

The H2 gate passes because all three required lower bounds are positive. H1'
fails because the entire \(D_{80}\) interval is negative; the two positive null
contrasts establish that the selected directions are not equivalent to those
registered nulls, but they do not satisfy the retention clause.

### 7.2 Bounded Secondary Evidence: Simple Condition

| Quantity | Point estimate | Paired 95% interval | Boundary |
| --- | ---: | ---: | --- |
| \(G_{true}\) | 0.048998 | [0.033461, 0.063827] | secondary only |
| \(G_{state}\) | 0.093247 | [0.079625, 0.106614] | secondary only |
| \(G_2\) | 0.029934 | [0.024171, 0.036182] | secondary only |
| \(D_{80}\) | -0.009264 | [-0.019817, 0.002500] | secondary only; crosses zero |

The simple mean cross-entropies were 1.335710 old, 1.242464 new state,
1.286713 old plus full \(R_U\), and 1.305777 old plus top-two \(R_U\). The Protocol
registered no simple control family, so these values cannot enter the primary
H2/H1' verdict.

### 7.3 Failed, Ambiguous, Ineligible, Missing, And Not-Run Evidence

- **Failed setup attempts:** attempts 1--4 produced no scientific output and
  are excluded from all aggregates. They diagnose runtime environment and
  invocation issues only.
- **E03:** `INELIGIBLE_GUARD`; its numerical output is not confirmation
  evidence for the Anchor.
- **Ambiguous:** none among the registered E04 complex metrics; the H2 and H1'
  rules map them unambiguously to Pass and Fail respectively.
- **Missing:** no required E04 condition, success receipt, array family, table,
  figure, or manifest family is missing.
- **Not run:** ranks 3--7, other layers, natural-language datasets, native
  interventions, expert-utility tests, and Router experiments.

## 8. Visualization Result

### Fresh Confirmation H2 And H1' Gates

![E04 fresh-confirmation gates](figures/figure_e04_fresh_confirmation_gates.png)

**Purpose:** display the registered decision quantities and their uncertainty
without introducing a new analysis.

**Setup:** primary complex condition; 128 equal-weight complete episodes; E02-
frozen readouts/directions; E04-only confirmation data.

**Metric definition and unit:** cross-entropy gain or paired contrast in
nats/example, as defined in Section 5.

**Raw source and lineage rows:** [confirmation_metrics.csv](tables/confirmation_metrics.csv),
[complex arrays](evidence/complex_confirmation_arrays.npz), and the first six
rows of Section 6.

**Aggregation and uncertainty:** means over 128 complete episodes and
percentile 95% intervals from 2,000 paired draws; higher-method q95 recomputed
inside each control contrast draw.

**How to read:** values and intervals above zero pass their positive-bound
clause. The negative \(D_{80}\) interval fails rank-two retention.

**Expected under registered outcomes:** H2 Pass requires positive intervals for
\(G_{true}\), \(G_{state}\), and \(T_{cap}\); H1' Pass additionally requires positive
intervals for \(D_{80}\), \(T_{random}\), and \(T_{perm}\).

**Observed result:** all H2 intervals are positive; \(D_{80}\) is strictly
negative; both equal-rank null contrasts are positive.

**Take-home:** local added accessibility is eligible and positive, while two
frozen directions do not retain 80% of the full gain.

**Remaining uncertainty:** the smallest sufficient linear rank above two and
whether any retrieved signal supports downstream routing.

**What this figure does not prove:** adjacent-block novelty,
whole-representation low rank, Shannon-information creation, native use,
expert utility, or Router gain.

**Anchor update implication:** record local H2 Pass and H1' rank-two Fail, then
open only the fresh-data rank ladder.

The machine-readable [plot contract](evidence/plot_contracts.json) gives the
same source, aggregation, allowed conclusion, and limitation. The PDF version
is [available here](figures/figure_e04_fresh_confirmation_gates.pdf).

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| S0 implementation | RED receipt; 26-test green JUnit; compile receipt | Passed | none after implementation | missing ID/receipt/simple-array/full-manifest guards in E04 code | scientific execution validity still required |
| S1 freeze | ledger, stage receipt, residualizer receipt, prior collision guards, first trace event | Passed | none | result-driven model/direction/rank/threshold selection; pre-freeze E04 label access | fresh execution and extraction |
| S2 data | full/simple/complex JSON identities, public/data manifests, generation receipt | Passed | none | E01/E02/E03 identity/context/text reuse; missing E04 namespaced fields | model capability and feature validity |
| S3 extraction setup | four retained failure records plus environment lock | Failed attempts, then repaired before scientific success | missing packages/import compatibility/one incomplete command | silent scientific retry selection; no model output existed in failed attempts | successful extraction guards |
| S3 successful extraction | simple and complex manifests/receipts, representations and logits | Passed | none | wrong data hash, incomplete records, low capability, hook/replay/projection/difference failures | functional readout result |
| S4 banks | 64 materialized arrays and bank audit | Passed | none | target-source imbalance, nonzero MI, duplicate bank, or E02/E03 actual-map reuse | null-family coverage remains bounded to these banks |
| S5 evaluation | arrays, three tables, result, final trace/audit, figure and contract, evaluation receipt | Passed | none | nonfinite metrics, changed objects, wrong bootstrap unit, missing primary arrays | record completeness |
| S6 record | full manifest and record-completeness audit | Passed | none | partial evidence-family record of the E03 type | human confirmation of knowledge wording |

**Falsified physical prior:** none at the global level. E04 does not adjudicate
whole-representation low rank. The local H2 prior is supported under the
registered readout family.

**Falsified mathematical model:** the rank-two sufficiency clause is falsified
for this frozen \(K_{new}\) ordering and 80% criterion. The full-\(R_U\) local
added-accessibility object is not falsified.

**Falsified operationalization / proxy:** using only the first two
conditional-innovation directions as a sufficient representation of the full
eligible gain is rejected. The full residual-update readout remains valid for
the bounded H2 question.

**Falsified implementation:** none in the eligible scientific run; all frozen
hash, identity, extraction, bank, and output guards passed. The pre-scientific
environment failures are preserved operational failures, not scientific
conditions.

**Falsified metric:** none. The registered paired episode-bootstrap rule and
verdict thresholds were executed exactly.

**Remaining rival explanations:** the full effect may require rank 3--7, a
higher linear rank, or nonlinear structure; the result may be specific to the
synthetic target, one layer transition, one answer position, or one model. The
registered generic-correction and equal-rank null explanations are rejected
only within their named families.

## 10. Full Experiment Record

**Worker root:**
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_e01_layer25_conditional_innovation/`

**Scientific run root:**
`runs/a15-08-e04-strict-conformance-repair-20260811/`

**Freeze root:**
`preconfirmation_freezes/a15-08-e04-20260811/`

**Chronology:**

| UTC time | Event | Direct record |
| --- | --- | --- |
| 01:59--02:00 | strict-conformance RED observed, then 26 tests green and four modules compiled | [RED](evidence/s0_tdd_red_receipt.json), [green JUnit](evidence/s0_green_tests.xml), [compile](evidence/s0_compile_receipt.json) |
| 02:01:20--02:01:28 | S1 freeze completed while E04 run/data roots were absent | [freeze-stage receipt](evidence/freeze_stage_receipt.json) |
| 02:01:48--02:01:51 | 128 fresh episodes generated | [generation receipt](evidence/generation_receipt.json) |
| before 02:12:54 | four failed pre-scientific simple-extraction invocations and one incomplete venv setup recorded | [retry records](evidence/retries/attempt1_missing_transformers.json) and [environment lock](evidence/execution_environment_lock.json) |
| 02:12:54--02:14:00 | simple extraction completed | [simple receipt](evidence/simple_extraction_receipt.json) |
| 02:14:07--02:15:07 | complex extraction completed | [complex receipt](evidence/complex_extraction_receipt.json) |
| 02:15:34--02:15:49 | one registered evaluation completed | [evaluation receipt](evidence/evaluation_receipt.json) |
| 02:15:52 | S6 completeness audit completed | [record audit](evidence/record_completeness_audit.json) |

**Exact successful commands:**

```bash
/usr/bin/python3.10 analyze_e04.py freeze \
  --e02-analysis-root runs/a15-08-e02-fresh-balanced-repair-20260810/analysis \
  --e02-run-root runs/a15-08-e02-fresh-balanced-repair-20260810 \
  --protocol /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/protocol.md \
  --freeze-root preconfirmation_freezes/a15-08-e04-20260811 \
  --fresh-run-root runs/a15-08-e04-strict-conformance-repair-20260811 \
  --fresh-data-root runs/a15-08-e04-strict-conformance-repair-20260811/data
```

```bash
/usr/bin/python3.10 build_data_e04.py \
  --output runs/a15-08-e04-strict-conformance-repair-20260811/data \
  --freeze-receipt preconfirmation_freezes/a15-08-e04-20260811/preconfirmation_freeze_receipt.json \
  --episodes 128
```

```bash
/usr/bin/python3.10 extract_e04.py \
  --freeze-receipt preconfirmation_freezes/a15-08-e04-20260811/preconfirmation_freeze_receipt.json \
  --data runs/a15-08-e04-strict-conformance-repair-20260811/data/composition_simple.json \
  --output runs/a15-08-e04-strict-conformance-repair-20260811/simple \
  --batch-size 16 --device cuda:0
```

```bash
/usr/bin/python3.10 extract_e04.py \
  --freeze-receipt preconfirmation_freezes/a15-08-e04-20260811/preconfirmation_freeze_receipt.json \
  --data runs/a15-08-e04-strict-conformance-repair-20260811/data/composition_complex.json \
  --output runs/a15-08-e04-strict-conformance-repair-20260811/complex \
  --batch-size 16 --device cuda:0
```

```bash
/usr/bin/python3.10 analyze_e04.py evaluate \
  --freeze-receipt preconfirmation_freezes/a15-08-e04-20260811/preconfirmation_freeze_receipt.json \
  --fresh-run-root runs/a15-08-e04-strict-conformance-repair-20260811 \
  --fresh-data-root runs/a15-08-e04-strict-conformance-repair-20260811/data \
  --output runs/a15-08-e04-strict-conformance-repair-20260811/analysis
```

**Successful execution environment:** Python 3.10.12; PyTorch
2.3.0a0+6ddf5cf85e.nv24.04; NumPy 1.24.4; Transformers 4.51.0;
Tokenizers 0.21.4; Safetensors 0.8.0; Accelerate 1.6.0; Protobuf 3.20.3;
ONNX 1.16.0; CUDA 12.4; requested device `cuda:0` on one of two visible NVIDIA
H100 80GB HBM3 GPUs.

**Retry record:**

| Attempt | Failure boundary | Preserved evidence | Scientific-output status | Eligibility use |
| --- | --- | --- | --- | --- |
| 1 | import failed: `transformers` absent | [reconstructed receipt](evidence/retries/attempt1_missing_transformers.json) | none | excluded; record limitation disclosed |
| 2 | import failed: ONNX 1.16.0 / protobuf 4.24.4 incompatibility | [failure receipt](evidence/retries/attempt2_protobuf_abi.json) | none | excluded |
| 3 | model-construction import path required missing `accelerate` | [failure receipt](evidence/retries/attempt3_missing_accelerate.json) | none | excluded |
| 4 | argument parser rejected missing `--freeze-receipt` | [failure receipt](evidence/retries/attempt4_missing_freeze_argument.json) | none; model and data not loaded | excluded |

No retry selected among scientific outputs: there was one successful simple
extraction, one successful complex extraction, and one evaluation.

## 11. Interpretation

The direct subtraction \(U=Z-X\) is valid because \(X\) and \(Z\) are matched states
in the same hidden coordinate, but a nonzero \(U\) is not by itself evidence of
new knowledge. E04 tests the narrower object \(R_U\), the portion not linearly
predicted from \(X\), by asking whether a frozen readout correction improves an
untouched fresh target and exceeds a registered same-budget target-independent
family.

The eligible H2 Pass means that, for this target and linear family, the named
attention transition makes terminal-code information more accessible than the
old-state readout exposes. The positive \(G_{state}\) provides the registered
same-dimensional sign check. The positive \(T_{cap}\) rejects the particular
rival that any target-independent correction of the same fitted form would
produce the gain.

The H1' Fail narrows the representation claim. The two selected directions are
not null: they beat both equal-rank control families. Yet they preserve only
33.24% of the full point gain, and \(D_{80}\) is negative in every part of its
95% interval. Therefore target relevance and low-dimensional sufficiency are
different claims. The experiment establishes the former for full \(R_U\) and
rejects the latter at rank two.

This result does not locate the complete signal in a spectral band, determine
its minimal rank, or show that a Router can use it. Those are downstream
questions, and only the rank ladder is admitted next.

## 12. Claim Boundary

**Can claim:** for the controlled two-hop target, frozen Qwen3-8B, final Answer
token, and the named normalized layer-25 attention transition, the registered
full-\(R_U\) linear correction contains terminal-code accessibility beyond the
old-state readout and the registered target-independent correction family. The
two frozen conditional-innovation directions are informative but insufficient
to retain 80% of that gain.

**Cannot claim:** adjacent-block novelty, that a deeper layer retains all
shallower information, whole-representation low rank, Shannon-information
creation, factual knowledge storage, nonlinear uniqueness, native model use,
natural-language generality, expert utility, or Router gain.

## 13. Next Decision

**Decision:** freeze one fresh-data rank-ladder design over
\(r\in\{3,4,5,6,7\}\) on the same \(R_U\) object, with equal-rank random and
TRAIN-label-permutation control budgets and the unchanged 80% held-out-
retention gate.

**Completion criterion:** return the smallest rank whose \(D_{80}\),
\(T_{random}\), and \(T_{perm}\) lower 95% bounds are all positive; if none passes,
record "no sufficient linear compression through rank seven" without changing
the threshold.

**Resume action:** draft only that fresh-data rank-ladder Protocol from the
frozen E04 object and gates. Do not change the task, reopen spectral-band
selection, or add a Router experiment.

## 14. Artifact Manifest

The machine [full-experiment manifest](evidence/full_artifact_manifest.json)
is the complete path/hash/size/stage/eligibility ledger. It contains **59
artifacts**, reports `all_complete=true`, and covers all **39 required
families**. The [record-completeness audit](evidence/record_completeness_audit.json)
independently records `all_required_artifacts_complete=true`,
`access_order_all_pass=true`, and `eligible=true`.

### 14.1 Complete Required-Family Inventory

| Stage | Required families present | Count |
| --- | --- | ---: |
| S0 | `s0_red_receipt`, `s0_green_junit`, `s0_compile_receipt`, `protocol` | 4 |
| S1 | `freeze_ledger`, `freeze_receipt`, `freeze_stage_receipt`, `residualizer`, `prior_data_guard`, `prior_map_guard`, `eligibility_trace` | 7 |
| S2 | `full_json`, `simple_json`, `complex_json`, `public_manifest`, `data_manifest`, `generation_receipt` | 6 |
| S3 | `simple_representation`, `simple_logits`, `simple_extraction_manifest`, `simple_extraction_receipt`, `complex_representation`, `complex_logits`, `complex_extraction_manifest`, `complex_extraction_receipt` | 8 |
| S4 | `banks`, `bank_audit` | 2 |
| S5 | `complex_arrays`, `simple_arrays`, `per_record_table`, `control_episode_table`, `metrics_table`, `result`, `eligibility_audit`, `evaluation_receipt`, `plot_contract`, `figure_png`, `figure_pdf`, `analysis_manifest` | 12 |
| **Total** | all registered families | **39** |

### 14.2 Canonical Decision And Audit Artifacts

| Artifact | Purpose | Producer / revision | Source inputs | SHA-256 | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | frozen scientific contract | A15_08_E04_v1 | approved Anchor decision | `5072d76d9a44877e270b910424ea255ffee347dc17097640c88e20200d82a27d` | yes | yes | frozen before data |
| [preconfirmation_freeze.json](evidence/preconfirmation_freeze.json) | code/input/config/root-absence ledger | S1 freeze | Protocol, E02 frozen assets, S0 receipts | `5f5698b5cc20dd0cbbbf0e477bc1fc9f22a220083ca84bda0c563c5117875d38` | yes | yes | no E04 labels/results |
| [freeze_stage_receipt.json](evidence/freeze_stage_receipt.json) | exact S1 execution receipt | S1 | freeze command and inputs | `934ea6107a37a48df9036e1f273de04b457082699ad7717fef5910f8458d962f` | yes | yes | status complete |
| [data_manifest.json](evidence/data_manifest.json) | fresh-data identity, schema, balance, overlap | S2 | seed 8103 and freeze receipt | `c293e816932ca5e962d672a5e7c636a72a190cc7aa17d8bda2f05c8ce4dd16e3` | yes | yes | zero collisions |
| [generation_receipt.json](evidence/generation_receipt.json) | exact S2 command/environment/output hashes | S2 | freeze and prior-data receipts | `ed62da359e11debed03df39108b599fcbbf48953906fa4e95614e67167ec5e60` | yes | yes | status complete |
| [simple_extraction_manifest.json](evidence/simple_extraction_manifest.json) | secondary extraction guards | S3 | simple JSON, Qwen3-8B | `287a12295754a443ea965dd94ae324438b80d429d889a5333239c45b4ea19f70` | yes | no | secondary only |
| [simple_extraction_receipt.json](evidence/simple_extraction_receipt.json) | exact successful simple command receipt | S3 | freeze/generation/simple JSON | `14b87cf78d0b88475e54ef3375d9f94eb75e41cd4a2fd2564ef336342ad2cd55` | yes | no | secondary only |
| [complex_extraction_manifest.json](evidence/complex_extraction_manifest.json) | primary extraction guards | S3 | complex JSON, Qwen3-8B | `e7d924dd2929e07d91fc80a395d094d1cc7638b7628a67f40c72c42db8c8b7b5` | yes | yes | all guards pass |
| [complex_extraction_receipt.json](evidence/complex_extraction_receipt.json) | exact successful complex command receipt | S3 | freeze/generation/complex JSON | `f94f755863c90b0e7d0d3b13ab7f74d407c91e4b81ad42c93fdba682a433449b` | yes | yes | status complete |
| [materialized_confirmation_bank_audit.json](evidence/materialized_confirmation_bank_audit.json) | 64-bank structure/reuse audit | S4 | frozen recipes, E04 labels, prior-map hashes | `3aa8862359fc3076b56ff70cd392f832c1bf8e57d251383723ca33a9f706b609` | yes | yes | 64/64 valid |
| [complex_confirmation_arrays.npz](evidence/complex_confirmation_arrays.npz) | complete primary record/episode/control/bootstrap arrays | S5 | frozen models, primary extraction, banks | `f26c20690d5e844b7f46deb87fd2069138bfd9f9258b7d0a5650a3e945093974` | yes | yes | 27 arrays |
| [simple_confirmation_arrays.npz](evidence/simple_confirmation_arrays.npz) | complete secondary record/episode/bootstrap arrays | S5 | frozen models, simple extraction | `ab5a41cb0fe31c23776f6d12b2c838ef3965f18601fcd225e50a94ace757899c` | yes | no | 14 arrays; secondary |
| [confirmation_metrics.csv](tables/confirmation_metrics.csv) | central metric and CI table | S5 | primary and secondary arrays | `af8edda2e52c182066b36bc38eca29b4615db1c871f7422fe3d599685f0e9622` | yes | primary rows yes | canonical compact table |
| [confirmation_per_record_core.csv](tables/confirmation_per_record_core.csv) | per-record primary effects | S5 | complex extraction and frozen models | `c3413802e000a7abf0ce6205b89141baacf2611c7c4c8c40af7fe95d7315c8b4` | yes | yes | 1,024 primary records |
| [confirmation_control_per_episode_gains.csv](tables/confirmation_control_per_episode_gains.csv) | per-episode control-family effects | S5 | complex arrays and banks | `53b61efca910f693108e5a5b3fe041c92d239ea2dc904611c35d04a473da8101` | yes | yes | 64 controls/family |
| [result.json](evidence/result.json) | registered values, verdict, and guards | S5, A15_08_E04_v1 | arrays, receipts, frozen hashes | `ac2dc73e358fa3220a48dc60bd477a75772d64ea202b95468854ee7dafbafbb3` | yes | yes | `H2_PASS_H1_FAIL` |
| [eligibility_audit.json](evidence/eligibility_audit.json) | final seven-event access audit | S5 | final trace | `a541e5e0c431d2b7a8233d81a59ab63be1e77963ac749401bf95ea8d97bc7be9` | yes | yes | `all_pass=true` |
| [evaluation_receipt.json](evidence/evaluation_receipt.json) | exact S5 command/environment/output hashes | S5 | both successful extraction receipts | `11295bea30a7012f86625b725fb9c3defa3bdd192fac3b85c7a60c65f7d78d30` | yes | yes | status complete |
| [plot_contracts.json](evidence/plot_contracts.json) | figure interpretation boundary | S5 | metrics and arrays | `bdaabefe855fe2e2e6d880fd91c365e72a9945bd1d6739a1950403dbb3c34b6e` | yes | yes | no extra claim |
| [figure PNG](figures/figure_e04_fresh_confirmation_gates.png) | visual verdict evidence | S5 | metrics table | `cf979c67b4353856c6a3ef8e07ad30d50daa473036e6d7dc4bc04bf20bea3f38` | yes | yes | audited above |
| [full_artifact_manifest.json](evidence/full_artifact_manifest.json) | exact 59-entry full ledger | S5/S6 | all S0--S5 artifacts | `6ab62f63d1a87998e4a3694ca595915ed54423eb65df9a9fbaf46965d693c5dd` | yes | yes | 39/39 families |
| [record_completeness_audit.json](evidence/record_completeness_audit.json) | S6 final qualification | S6 | full manifest and final trace | `2341fe032e1270a5ef2e661602b3a44774dd06bf7bb122167ba8bf937514bcec` | yes | yes | `eligible=true` |

### 14.3 Worker-Resident Heavy Artifacts

These files are intentionally not duplicated into the research mainline. Their
absolute paths, sizes, producer stages, and full hashes are in the full
manifest.

| Artifact family | Purpose | SHA-256 identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- |
| complex JSON | primary fresh records | `ddf914f633e57183394fbcc37727e917ff09cfc106ead97e421b1b76eacac32b` | yes | yes | 1,024 records |
| complex representations | primary \(X,Z,U\) tensors | `90c4b7959878f611fb7299607d33c0dc486fe13421bd041c32a93df6bac11e16` | yes | yes | shape \(1024\times4096\) |
| complex restricted logits | capability evidence | `f6e35716c319bc9adabec89945a49249f360969c862e909c221654b2a89fbb28` | yes | yes | shape \(1024\times8\) |
| simple JSON | secondary fresh records | `e07f26f940ad2a1c9500789cef02cf9df01cdd3d8c6d7f2f1a61ec0b0c3f976d` | yes | no | secondary |
| simple representations | secondary \(X,Z,U\) tensors | `0d1c6a3fd62693a94b71aee12b9d04b08a7bc68f60a720598080ec0d0d70a3e8` | yes | no | shape \(1024\times4096\) |
| simple restricted logits | secondary capability evidence | `6500414e3ef5a31b56da1b032f63ea7c51f849779956a9e8892408aa65f8cdc6` | yes | no | shape \(1024\times8\) |
| frozen residualizer | E02 TRAIN-only \(X\to U\) systems | `b5a90703a96033446427cddf4ebf33d8b9f43b093a748df04460584b9c872d37` | yes | yes | 134 MB worker artifact |
| materialized banks | 64 E04 actual index maps and contingencies | `6d098c357c7998465a0ade4b8abee8ba5ce10a00484520705c7548607e7dad56` | yes | yes | all cells 16, MI 0 |

### 14.4 Post-Manifest Reader Audit

The [independent cold-read audit](evidence/independent_cold_read_audit.json)
(SHA-256 `966c17ebde36a103eb7f4850ee6c98943847507a5e44d082f4b7dc20e19bfbdd`)
was written after the frozen S0--S5 full manifest. It reports 47/47 checks
passing, independently reproduces every decision-bearing estimate, and
verifies all 59 manifest paths, sizes, and hashes. It also preserves the
nonfatal boundary that attempts 1 and 4 have reconstructed rather than full
raw failure receipts. This audit is S6 reader verification, not a new
scientific input and not a retroactive manifest member.

## 15. Links

- **Anchor:** [A15_08 Target-Conditioned Layer Innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)
- **Protocol:** [protocol.md](protocol.md)
- **Summary:** [summary.md](summary.md)
- **E03 predecessor Protocol:** [A15_08_E03](../A15_08_E03_fresh_confirmation_freeze_repair/protocol.md), retained as an ineligible predecessor rather than amended
- **Code workspace:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_e01_layer25_conditional_innovation/`
- **Runner:** `analyze_e04.py`, `build_data_e04.py`, `extract_e04.py`, `e04_receipts.py`; exact frozen hashes are in [preconfirmation_freeze.json](evidence/preconfirmation_freeze.json)
- **Data / manifest:** [data_manifest.json](evidence/data_manifest.json), [confirmation_public_manifest.json](evidence/confirmation_public_manifest.json)
- **Result evidence:** [result.json](evidence/result.json), [metrics table](tables/confirmation_metrics.csv), [full manifest](evidence/full_artifact_manifest.json)
- **Figure directory:** [figures](figures/figure_e04_fresh_confirmation_gates.png)
- **Logs / checkpoints:** no learned E04 checkpoint; structured receipts and retry evidence are under [evidence](evidence/evaluation_receipt.json)
- **Reproduction commands:** Section 10; exact argv and environments are preserved in stage receipts
- **Job IDs:** none; execution was local in the shared worker container
