# Native Dense LM baseline: authorized 10B-to-50B continuation

Authorized by the researcher's 2026-09-14 instruction in conversation
`01a09d65-20da-7421-99fe-a69d05db392c`. This extends the completed native
Dense trajectory from its exact 10B full-state checkpoint to a cumulative 50B
prediction-token target on the same eight-RTX5090 topology.

The child run must restore model weights, AdamW moments, LambdaLR state,
optimizer update, cumulative tokens, data cursor, and all eight rank RNG states
from the complete parent checkpoint. The parent contract remains immutable;
the child records both the parent contract hash and its own 50B continuation
contract. The effective global batch remains 262,144 valid prediction tokens.

The LR schedule is unchanged: 1,000-update linear warmup followed by a constant
peak LR of `3e-4`. The parent checkpoint is at update 38,150 with scheduler
`last_epoch=38,150`; both optimizer groups and LambdaLR `_last_lr` are `3e-4`.
Consequently the first continuation update remains at `3e-4`: there is no
warmup restart and no token-budget-dependent decay endpoint.

The same fixed readable 30B-token source view is cycled as before. Permanent
optimization-aligned full-state child milestones are 15B, then every 2B from
17B through 49B, plus the exact 50B endpoint. A matched post-update snapshot is
also retained at the first complete optimizer update at or after 13B; it does
not shorten an update or alter the token/LR trajectory. Two 1,000-update rolling
recovery checkpoints are kept.
All original 0/0.5/1/3/5/10B parent milestones and Smoke evidence are preserved.

Submission uses the repository execution template with profile `5090-8-spot`,
the current `shphd-lite-0911` image and the existing isolated PyTorch 2.8 /
CUDA 12.8 runtime. This is an operational extension only and changes no model,
data, optimizer, loss, representation, or scientific hypothesis.

## 2026-09-28 capacity-qualified continuation

The researcher explicitly authorized another `5090-8-spot` continuation after
the previous segment stopped.  The newest complete source is recovery
step 84,000 at 22,018,691,584 valid prediction tokens; the computed but
uncheckpointed tail through step 84,913 / 22,258,029,056 tokens is discarded.

To use the 32GB cards more fully without changing the frozen global batch, the
new job tests the descending physical-microbatch list 16, 8, 4, 2 in memory,
always regrouping the original eight logical `mbs2/acc8` lanes and keeping
262,144 valid targets per optimizer update.  It selects the largest candidate
with two finite updates and peak reserved memory at or below 94 percent of the
physical device capacity, records that choice before formal optimization, and
then continues the same model/optimizer/scheduler/data/RNG trajectory toward
50B.  The qualification uses an in-memory fork and cannot mutate the source
checkpoint.  No loss, model, CE, optimizer, schedule, checkpoint target, data,
or token-budget change is authorized.  This performance migration is not
claimed to be bitwise equivalent to the prior segment.

### Eight-H100 replacement

The researcher stopped the 2026-09-28 eight-RTX5090 attempt after GPU
preflight and before it created a capacity receipt, run directory, optimizer
update, or checkpoint. Its source remains the complete 22.018691584B
checkpoint. The replacement uses one `h100-8-spot` node and capacity-tests
microbatch 16, 8, 4, 2 with accumulation 1, 2, 4, 8, selecting the largest
candidate passing the same two-update finite-loss and 94-percent-memory gate.
Microbatch 16 is the maximum factorization compatible with the frozen
262,144-token update. No other contract field changes.

### Researcher capacity override and direct Full

The H100 capacity process completed two in-memory Dense updates at every tested
batch size but its receipt code failed afterward because the native Dense
engine does not return a `total_loss` key.  This is not OOM or a training
non-finite result.  Match the canonical Dense trainer by defining
`total_loss = lm_loss`, stop all Smoke work, and use the researcher's explicit
non-OOM judgment to submit direct Full at microbatch 16 / accumulation 1.
The source checkpoint, global batch, trajectory, and all non-performance
contract fields remain unchanged.

### H100 exhaustion and RTX5090 replacement

Neither direct eight-H100 Full job obtained a worker.  Both were stopped and
verified `SUSPENDED` before any pod or run artifact existed.  The researcher
replaced them with `5090-8-spot`.  Dense returns to the already exercised
microbatch 2 / accumulation 8 partition rather than transferring the H100-only
mbs16 capacity judgment to 32GB RTX5090 cards.  The complete 22.018691584B
source and every non-resource contract field remain unchanged.
