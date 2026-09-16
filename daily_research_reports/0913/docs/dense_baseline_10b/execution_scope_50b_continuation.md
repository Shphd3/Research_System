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
