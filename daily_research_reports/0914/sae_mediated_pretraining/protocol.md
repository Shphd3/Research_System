# Protocol: SAE-Mediated live-reconstruction 50B pretraining

## 0. Approval snapshot

Document status: `APPROVED_FOR_SEGMENTED_FORMAL_50B_EXECUTION`.

Researcher confirmation: on 2026-09-14 the researcher selected the single
SAE-Mediated model, confirmed that AuxK must remain SAE-only, and approved a
shortened Smoke. After that Smoke passed, the researcher clarified that the
intended comparison requires formal 50B training, ordered the mistakenly
submitted 1024-step run stopped and deleted, and approved submission of the
segmented 50B run.

Purpose: construct and qualify one jointly trained serial SAE-mediated language
model while measuring LM cost and SAE health against the existing native Dense
trajectory at matched valid-token coordinates.  This is method construction,
not a causal C/T test.

Condition: `sae_mediated_live_recon_auxk_sae_only`.  There is no new C arm.
The existing native Dense trajectory is read-only contextual baseline evidence.

Approved execution ceiling: the completed 8-step four-H100 Smoke followed by
one fresh seed-17 50B formal run, executed in bounded 31h30 segments that all
resume the same run root and frozen contract. No new C arm, alternate lambda or
additional seed.

Cannot claim: that backbone gradient mediation causes an improvement, that
AuxK revives natural dead features, that representation quality improves, or
that one seed establishes stable long-run behavior.

## 1. Model and gradient contract

For pre-SAE state $h$ and SAE $A$,

$$
L=L_{LM}+L_R+\frac{1}{32}L_{AuxK}.
$$

$L_{LM}$ traverses the SAE.  $L_R$ uses live $h$ as encoder input and detached
$h$ as target, so it updates the SAE and upstream LM.  AuxK uses a detached
input and detached main residual, so it updates only the SAE.  Targets and
normalization denominators remain detached.  The architecture is 8 layers,
hidden size 1024, FFN 3072, tied embeddings, and width-30,000 TopK-32 SAE.

## 2. Data and optimization

Training uses DCLM manifest SHA-256
`8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`,
seed 17, sequence length 2048, four ranks, microbatch 2 and accumulation 16.
Each full update has 262,144 valid prediction targets.  AdamW, schedules,
sampling RNG, global loss denominators, separate clipping and checkpoint state
reuse the qualified 0912 trainer. The fixed 30B source prefix cycles to the
50,000,000,000-valid-target endpoint.

Exact milestones remain aligned with the Dense optimization boundaries at
0/0.5/1/3/5/10/15/17/19/.../49/50B. Additional permanent snapshots target
0.1/0.3/7/13B and are taken after the first complete optimizer update at or
beyond each target, recording target and actual coordinates. They must not
shorten a batch or add a partial optimizer update. Rolling recovery is every
1000 updates with the latest two retained.

The frozen M2D2 fit/development panel is a row-level natural-text diagnostic;
it is not document-held-out confirmation because upstream document IDs are not
available.

## 3. Evidence and stopping

Engineering eligibility requires finite LM/total/reconstruction/AuxK scalars, exact
global denominators, monotonic token/update coordinates, complete TensorBoard
audit, finite independent LM/SAE gradients, synchronized replicas, exact
resume replay, complete checkpoints and no failure receipt.  AuxK may remain
naturally zero before the 10M sampled-position window; forced-branch evidence
is inherited only when the model/SAE/engine/checkpoint hashes remain unchanged.

Stop immediately on a non-finite objective or gradient, counter/replay failure,
replica divergence, source/config/data hash mismatch, incomplete checkpoint,
wall/storage limit or explicit STOP. Smoke PASS supports entry into the
registered formal 50B run but is not scientific support for the hypothesis.

## 4. Observability and artifacts

TensorBoard records globally normalized LM and total loss, raw and weighted
main reconstruction and AuxK terms, both learning rates, LM/SAE gradient norms,
valid-token throughput, cumulative valid targets, optimizer update, effective
tokens/update, SAE sampled positions, dead count and AuxK activations on the
registered axes.  JSONL remains the raw ledger.  Required artifacts are source
identity, resolved config, initial full/backbone tensor hashes, gradient and
resume receipts, TensorBoard audit, checkpoints, terminal/training receipts and
failure history.

## 5. Execution contract

Execution uses the current envelope defaults `h100-4-reserved` and
`shphd-lite-0911`, one node and four processes, through
`templates/execution/acp_submit_template.sh`. Formal training uses a fresh run
root and never resumes the Smoke or deleted 1024 run. Each 31h30 segment resumes
only that same formal run. Startup supervision ends after worker health, first
bounded progress, TensorBoard presence and replay status establish an
evidence-based ETA.

Blocks A-G: `CONFIRMED`. Cross-block consistency: `PASS` for the formal 50B
method-comparison construction scope. The next researcher decision follows the
50B endpoint evidence; segment completion alone does not trigger a scientific
state transition.
