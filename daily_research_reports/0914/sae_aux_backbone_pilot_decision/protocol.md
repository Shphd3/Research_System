# Protocol: matched serial-SAE auxiliary-gradient development pair

## 0. Approval snapshot

Document status: `DRAFT_NOT_EXECUTABLE`.

Approval status: the researcher explicitly selected a fresh matched C/T pair,
`lambda_R=1`, identical anti-starvation rules, one bounded four-H100 forced
activity check, and 1024 development updates per arm on 2026-09-14. The remote
development approval cannot yet be applied because the exact panel source has
revealed one material unit-of-observation limitation and the stable owning
`problem_key` remains unconfirmed. The forced engineering qualification is
separately authorized and may run.

| Field | Frozen or pending value |
| --- | --- |
| Purpose | Estimate at one seed whether letting the sampled SAE reconstruction objective update the upstream LM changes raw pre-SAE domain readability, while separately measuring LM cost and SAE health. |
| Experiment role | Development-only operationalization/proxy test. |
| Primary Anchor / Focus | `BLOCKED`: no confirmed owner. Candidate parent A15 and candidate key `sae_aux_backbone_domain_readability`. |
| Control | Fresh serial SAE-mediated C with SAE-only AuxK and detached sampled main reconstruction input. |
| Treatment | Fresh serial SAE-mediated T with the same AuxK and live sampled main reconstruction input. |
| Unique difference | `model.aux_backbone_grad: false -> true` plus the condition label. |
| Held fixed | Full initial tensor state, forward path, architecture, data/order, RNG construction, objective coefficients and denominators, AdamW, schedules, global batch, DDP, clipping, checkpoints, panel and analysis. |
| Primary metric | At 268,435,456 valid prediction targets, T-minus-C macro-F1 from unit-normalized raw $h$ on the frozen M2D2 development rows, after fit-only regularization selection. |
| Cost metric | T-minus-C globally normalized held-out next-token NLL on the same fixed 1,048,576-target DCLM window. |
| Approved execution ceiling | One forced four-H100 qualification, then C and T each at most 1024 updates. No 4096 continuation, alternate lambda, or additional seed. |
| Pass / fail / insufficient | Engineering eligibility is PASS only if every identity, counter, replay, finite-scalar and artifact gate passes. Scientific direction is reported as positive, non-positive or insufficient; it does not itself approve 4096. |
| Cannot claim | Mechanism, SAE necessity, semantic understanding, downstream gain, lambda superiority, cross-seed reproducibility, or confirmation. |
| Pending decision | Confirm the candidate problem key/parent and accept or reject M2D2 official split rows as the development unit despite unavailable upstream document IDs. |

The superseded no-AuxK coefficient-0.1 draft is preserved read-only at
`history/protocol_v1_no_auxk_superseded.md`; it is not executable.

## 1. Definitions

The raw representation $h$ is the final Transformer's post-attention-residual,
post-`norm2`, pre-SAE 1024-vector. The serial forward path is

```text
final attention residual -> norm2 h -> TopK SAE reconstruction -> final MLP
```

`C` stops the sampled reconstruction input gradient; `T` leaves that input
live. Stop-gradient (`sg`) preserves a forward value but blocks its derivative.
AuxK is an SAE-only residual-reconstruction branch restricted to features that
have not fired within the natural activity window.

## 2. Anchor alignment and claim boundary — Block A

State: `BLOCKED` only on stable ownership. The local uncertainty, rival and
claim boundary are researcher-confirmed by the current instruction.

The tested local hypothesis is that the T gradient connection changes raw $h$
domain readability relative to an otherwise matched serial-SAE control. The
strongest rival is that an observed difference comes from unmatched AuxK,
initial state, data/RNG, optimization, forward architecture or measurement.
The fresh matched pair and identity gates address that rival. A one-seed
development difference cannot establish a general mechanism.

## 3. Data construction and provenance — Block B

State: `REOPENED_PENDING_HUMAN_CONFIRMATION` because source inspection changed
the unit from “document” to “official split row.”

LM training uses the frozen DCLM paired view and tokenizer already qualified by
the 0912 package. Both arms start at cursor zero, use the same deterministic
rank blocks and dedicated SAE-sampling RNG, and stop before cycling. The fixed
held-out LM window begins at validation sample 4096 and contains 512 sequences,
exactly 1,048,576 valid targets.

The frozen natural panel uses M2D2 revision
`6ae613ba744ee56f645aee9c577d04f7e3d48b30`, eight categories, 100 fit rows and
50 development rows per category. Fit draws only from official `train.txt`;
development draws only from `valid.txt`; test is not read. Each stored input is
the first 257 tokenizer IDs, and the primary readout uses position 255.

M2D2 exposes only text, with no upstream document identifier. Therefore this
Protocol calls each unit an official split row/natural excerpt and does not
claim independently verified document-held-out sampling. Exact normalized-text
and token-prefix duplicates are excluded; high word-5gram overlap is guarded
as specified by the manifest. The immutable manifest and all source-archive
hashes live under the execution workspace `data/natural_panel_v1/`.

## 4. Learning task and supervision — Block C

State: `CONFIRMED`.

LM/SAE training receives only DCLM next-token targets and self-reconstruction
targets. Natural-domain labels never enter model initialization, LM/SAE
updates, sample order, stopping or checkpoint selection. After checkpoints are
frozen, a separate linear readout uses fit labels for model/regularization
selection and development labels only for the reported development estimate.

## 5. Model, information flow and variants — Block D

State: `CONFIRMED`.

Both arms use 8 blocks, hidden size 1024, intermediate size 3072, 16 query and
8 KV heads, head dimension 128, tied input/output embeddings, random seed 17,
and a width-30,000 nonnegative TopK SAE with $k=32$. Both use the identical
serial forward path. No native no-SAE arm, Router, MoE, sidecar, resampling,
pretrained warm start or third condition is introduced.

The tensor-state hash over names, shapes, dtypes and values must agree across
four ranks and later between the two step-zero checkpoints. A condition label
or common random seed alone is not sufficient evidence.

## 6. Objective, optimization and telemetry — Block E

State: `CONFIRMED`.

For sampled state $h_i$ and SAE $A$,

$$
r_i = \frac{\|A(x_i)-\operatorname{sg}(h_i)\|_2^2}
{\max(\|\operatorname{sg}(h_i)\|_2^2,1024\times10^{-4})},
\quad x_i=\operatorname{sg}(h_i)\;\text{in C},\;x_i=h_i\;\text{in T}.
$$

For the natural dead set, AuxK uses the largest 256 eligible encoder values to
reconstruct the detached main residual. Its branch input and target are
detached, so AuxK directly owns only SAE gradients. With global valid LM count
$N$ and sampled SAE count $M$,

$$
L = \frac{\sum\ell_{LM}}{N} + \frac{\sum r_i}{M}
  + \frac{1}{32}\frac{\sum a_i}{M}.
$$

Natural deadness means no selected main TopK value above $10^{-3}$ during more
than 10,000,000 globally sampled SAE positions. At 1024 updates each arm sees
33,554,432 sampled positions. The forced qualification never persists its
call-local dead mask into either training config or checkpoint lineage.

AdamW, betas, weight decay, learning rates, warmups, separate LM/SAE clipping,
bf16 autocast, global denominators and scheduler indexing match across arms.
The batch is 4 ranks x 2 sequences x 16 accumulation x 2048 valid targets =
262,144 valid targets/update. Required TensorBoard tags include raw/weighted LM,
main reconstruction and AuxK losses on token and update axes, learning rates,
both counters, dead count and AuxK activations.

## 7. Conditions, comparison and frozen analysis — Block F

State: `CONFIRMED` except the cost-alert threshold below remains `AI_PROPOSAL`.

Only the two registered configs may run. Their recursive diff allowlist is
exactly `condition` and `model.aux_backbone_grad`. The primary coordinate is
cumulative valid prediction targets; update is eligible as a secondary axis
because tokens/update is identical.

At exactly 1024 updates, unit-normalize raw $h$. Select logistic-regression
$C\in\{0.01,0.1,1,10\}$ by 5-fold stratified macro-F1 on fit rows only, refit on
all fit rows and report macro-F1 on development rows. Report T-minus-C in
percentage points. Report held-out NLL T-minus-C in nats/valid target.

SAE reconstruction, training activity, natural dead count, fixed-panel feature
coverage and domain selectivity are separate explanatory columns. Training
activity counts and fixed-panel coverage must never be conflated. Raw $h$ is
the primary representation result; reconstructed and sparse views cannot rescue
a non-positive raw-$h$ result.

Typed endpoint branches:

- positive direction: eligible raw-$h$ T-minus-C macro-F1 $>0$;
- non-positive direction: eligible difference $\leq0$;
- joint degradation flag: raw-$h$ difference $\leq0$ and T-minus-C NLL $>0$;
- insufficient: any identity, data, replay, coordinate, artifact or fitting
  gate fails.

`AI_PROPOSAL`: label an NLL increase of at least 0.02 nat/target as a clear
cost alert. This threshold cannot govern execution until the researcher accepts
it. In all cases 4096 remains unauthorized, so no automatic continuation can
occur.

## 8. Execution and reproducibility — Block G

State: `CONFIRMED` for implementation, forced qualification and the requested
1024 ceiling; application to development waits for Blocks A/B/F promotion.

Code lives only at
`/data/250010109/MoE_Router/experiments/20260914_sae_aux_backbone_paired_auxk`.
It reuses the qualified T+AuxK package and ultimately the exact 0912 submitted
source. It does not modify old runs. The execution envelope resolves one
`h100-4-reserved` node, four processes and image `shphd-lite-0911`; submission
uses the repository ACP template.

The forced four-card gate must prove full-size nonzero finite AuxK, SAE-only
AuxK gradients, C/T main-gradient ownership, global DDP counts, synchronized
activity state, exact activity-buffer checkpoint restore and restoration of the
natural rule. Development then stops at 1024 updates or earlier on nonfinite
loss/gradient, counter or replay failure, replica divergence, hash mismatch,
wall/storage ceiling or explicit STOP.

Expected artifacts include source identity/config diff, panel manifest, forced
activity receipt, pair identity, run-local resolved configs/certificates,
raw/weighted JSONL and TensorBoard scalars, physical/logical update counts,
resume receipts, checkpoints, terminal receipts, and later
`metrics/representation.csv` and `metrics/sae_quality.csv`.

## 9. Stage contract

| Stage | Goal | Input / operation | Pass | Failure / handoff |
| --- | --- | --- | --- | --- |
| Local preflight | Protect source and pair identity | Isolated copy, 27 tests, recursive config diff | all PASS | preserve failure, repair, rerun |
| Forced four-H100 check | Exercise dead branch without waiting 10M samples | full-size call-local forced candidates, one DDP update and real recovery checkpoint | all gradient/count/state gates PASS | no development submission |
| Panel freeze | Fix development evidence before training | official M2D2 train/valid rows, deterministic selection and hashes | exact 1200 rows and manifest PASS | `DATA_BLOCKED` |
| C development | Produce matched control endpoint | fresh seed-17 C to 1024 | operational receipt/checkpoint/telemetry PASS | stop pair interpretation |
| T development | Produce treatment endpoint | fresh seed-17 T to 1024 | same gates and step-zero tensor hash equals C | stop pair interpretation |
| Paired readout | Measure raw representation and cost | frozen checkpoints/panel/rule | complete CSVs and provenance | researcher judges next budget |

## 10. Block, freeze and amendment ledger

| Block | State | Source |
| --- | --- | --- |
| A question / boundary / ownership | `BLOCKED` on owner/key | researcher instruction plus unresolved repository ownership |
| B data | `REOPENED_PENDING_HUMAN_CONFIRMATION` | frozen M2D2 manifest; row/document limitation discovered after instruction |
| C learning task | `CONFIRMED` | researcher instruction, 2026-09-14 |
| D architecture | `CONFIRMED` | researcher instruction, 2026-09-14 |
| E objective / optimization | `CONFIRMED` | researcher instruction, 2026-09-14 |
| F comparison / evidence | `CONFIRMED` except proposed numeric cost alert | researcher instruction plus frozen development analysis |
| G execution | `CONFIRMED` for stated ceiling, pending A/B/F applicability | researcher instruction, 2026-09-14 |

Cross-block consistency: `BLOCKED` until A/B/F are confirmed. Design is not
frozen. No observed result may be written into this body. After first paired
development execution, any material change requires an append-only amendment
with eligibility impact.
