# Shared last-layer memory implementation

This is execution code, not scientific approval. The parent frozen student is the
official local Qwen3-0.6B Base. No backbone/SAE weights are updated. The injected
site is the final Transformer residual **before final RMSNorm**. The source data,
teacher behavior screen, DEV choices, and confirm freeze belong to the Protocol.

At d=1024, N=256, r=64, both memory and ordinary adapter contain exactly 1,393,665
trainable parameters. The adapter bottleneck is 680. Memory queries, keys, signed
values, output matrix, and sigmoid gate all train. Spectrum losses act on the
gated output after Wo and dtype conversion. Disabling returns the exact original
residual. Nominal and BF16-effective increment energies are separate diagnostics.

## CPU preparation and model cache stages

Run these commands using the qualified experiment environment. The current CPU
interface tests use `/root/anaconda3/envs/spectral-hier/bin/python`; this is not a
claim that its Transformers development version is the remote qualified version.
All paths below are examples; every output directory must be new.

```bash
python source/prepare_cache.py prepare --data data_prep/v3/confirm_ab_2048.jsonl --cache CACHE_AB --max-cache-gib 16
torchrun --nproc_per_node=4 source/prepare_cache.py student --cache CACHE_AB
torchrun --nproc_per_node=4 source/prepare_cache.py teacher --cache CACHE_AB
python source/verify_cache.py --cache CACHE_AB --out VERIFY_AB.json
python source/fit_spectrum.py --reference data_prep/v3/source_independent_reference.jsonl --exclude-data data_prep/v3/confirm_ab_2048.jsonl --out SPECTRUM
```

`prepare` checks full string-to-token-ID mapping equality, continuation token
equality and exact answer boundary concatenation. Native EOS differs: it is
recorded and excluded from supervised positions. CE covers all 151936 head rows;
KL is exact on the 151669 common **assigned** token IDs, renormalized on that
support. The remaining 267 native head rows lack defined token strings. This is
not native full-head KL. No top-k truncation occurs. KL includes temperature².

Teacher and student share the same gold answer prefix at every scored answer
position; their conditioning prompts differ. `candidate` teacher_mode explicitly
uses supplied source text and does not claim closed-book teacher knowledge.
The v4 semantic mask moves only consecutive individually pure-whitespace
leading tokens into the known gold prefix in both models; a token containing
any text remains supervised intact. No EOS loss is added. The cache stores BF16
full teacher logits and actual student
pre-norm hidden states, per fact, with offsets/targets. Full-logit storage is
planned and budget checked before allocation. Approximately 2048 five-token
answers require 2.9 GiB; 20k require 28 GiB. Use actual layout byte counts.

Each rank writes disjoint original indices without sampler padding. Completion
requires one receipt per fact. Stage completion hashes the complete actual file;
downstream loads check its size/mtime, all small payload hashes, and the readout
hash. They do not repeatedly read the full teacher payload. `verify_cache.py`
can additionally verify full file and every per-fact digest in one sequential
payload read. A detected change is not silently repaired.

## Matched training, restart, and A to B

```bash
torchrun --nproc_per_node=4 source/train_cached.py --cache CACHE_AB --out RUN_A --arm memory_head --phase A --splits confirm_a --spectrum SPECTRUM/spectrum.pt --global-batch 16 --grad-accum 1 --require-initial-gradients
torchrun --nproc_per_node=4 source/train_cached.py --cache CACHE_AB --out RUN_B --arm memory_head --phase B --splits confirm_b --spectrum SPECTRUM/spectrum.pt --global-batch 16 --grad-accum 1 --continue-from RUN_A/checkpoints/final.pt
```

Main arms: `none`, `adapter`, `memory_ce`, `memory_kl`, `memory_head` (`head64`),
`memory_random` (`random64`). Optional `memory_l2` uses the same total increment
energy. Adapter uses CE+KL matched to memory_kl. memory_ce has KL coefficient zero
but still records the raw KL diagnostic. None creates no optimizer or pretend
exposures; evaluate the original student. Pass the **same** independent spectrum
for every trainable arm to share initial scale calibration and diagnostics.
The spectral arms refuse failed stability, bad orthogonality, or wrong parent/site.

Every fact's global quota is exactly 1 or 8. Source/entity connected components
share assignment. The schedule records every presentation; low/high final
presentations share an effective update where feasible, with unmatched cases
explicit. DDP rank striding never pads. Gradient accumulation is normalized by
actual global valid answer tokens, not batch size or local means. Completed
updates alone advance the exposure ledger and token axis. No fixed lr schedule
is implied by a paper result: current implementation has constant lr, default
1e-3, AdamW, zero weight decay, clip1, tau2, KL0.5, penalty0.1. The Protocol must
freeze or amend those DEV choices before confirmation.

`--max-updates N` is a bounded segment. `--resume CKPT` restores module, Adam,
scheduler, all-rank RNG, tokens, updates, data cursor and actual exposures under
identical code/cache/objective/world-size contracts. A fresh run refuses output
with existing checkpoints/segment logs. A→B uses a **new** B output directory and
`--continue-from`; it preserves optimizer/RNG/cumulative counters and forbids
fact overlap. It requires the same combined cache. To measure retention, evaluate
A after A and after B; B-only scores do not measure retention.

## Generation and probability evaluation

```bash
torchrun --nproc_per_node=4 source/evaluate_live.py --data data_prep/v3/confirm_ab_2048.jsonl --out EVAL --checkpoint RUN_A/checkpoints/final.pt --splits confirm_a --views all
torchrun --nproc_per_node=4 source/evaluate_cached.py --cache CACHE_AB --out PROBS --checkpoint RUN_A/checkpoints/final.pt --splits confirm_a --spectrum SPECTRUM/spectrum.pt
```

Omit checkpoint for frozen baseline. Live generation receives question only,
without source/teacher/gold continuation. It uses the prior phase plain Base
prompt, greedy decoding, maximum32 new tokens. The first completed nonempty
answer line stops each sequence separately; leading empty lines do not stop.
Native EOS also stops. Raw text, actual token IDs, first-line parse, stop reason,
prompt, model content hashes and checkpoint hash remain available. Parent model
hash mismatch is rejected. Generation accuracy and gold-prefix answer
probability are separate metrics. Score helpers can be imported directly:
`FirstAnswerLine(tokenizer,prompt_width,batch_size)`, `first_line(raw)`,
`score(answer,row)`. score returns True/False/None with a reason. Multiple years,
uncertainty and approximate/negated years require review; `1980s` is not1980.

Both evaluators accept `--intervention off`, `keys_only`, or `values_only`, plus
fixed `--intervention-seed`. A common K/V permutation is only an invariance unit
test and is not presented as a destructive intervention. Record paired facts,
cost, and failed counterexamples before interpreting a memory mechanism.

## Independent general LM holdout

```bash
python source/prepare_lm_cache.py --data data_prep/v3/natural_v3/general_lm.jsonl --cache CACHE_LM --exclude-data data_prep/v3/confirm_ab_2048.jsonl --exclude-data data_prep/v3/source_independent_reference.jsonl
torchrun --nproc_per_node=4 source/prepare_cache.py student --cache CACHE_LM
torchrun --nproc_per_node=4 source/evaluate_cached.py --cache CACHE_LM --without-teacher --out LM_EVAL --checkpoint RUN_A/checkpoints/final.pt
```

Each observed token after the first is a next-token target; no EOS is appended.
This is a fixed, bounded paragraph corpus and does not establish general global
capability. Family exclusion checks verify declared identifiers, not pretraining
membership or all semantic overlap. The LM cache has no teacher file. Repeat
baseline, A, B and off evaluations on the identical fixed LM cache.

## Verification status

CPU interface tests cover exact vector/sum loss parity and gradient flow,
first-line per-sequence stopping, year scoring edge cases, and exact exposure
ledgers. Independent audit also tested dense/chunked CE/KL, native BF16 RMSNorm,
all trainable gradients, off identity, joint permutation invariance versus
single-side mismatch, and real 2-rank Gloo complete/interrupted/resumed training
including module/Adam/scheduler/state/identity/all-rank RNG exact equality.
Negative tests reject changed schedule/head dimension/non-resume output and
small/large/readout payload modifications. Actual GPU cache, teacher behavior,
real reference spectrum and architecture efficacy remain unverified until the
authorized experiment produces results.

## Generation repair recorded in implementation amendment v3

HF4.53.3 can replace `GenerationConfig(do_sample=False)` with the local Qwen3
model's `do_sample=True`, because False equals the global default and the local
generation_config declares Transformers>=4.50. The input config is deep-copied;
logging the original object can misleadingly retain False. Early DEV behavior
screens using that path are affected and must remain separate from corrected
results. This does not affect direct-forward hidden/logit cache construction.
Live evaluation now passes explicit `do_sample=False`, `num_beams=1`, and
`use_model_defaults=False` to generate, and records the resolved configuration.
A CPU regression against the actual local Transformers4.53.3 source reproduces
the old override and verifies the corrected greedy configuration.

## Semantic mask repair recorded in implementation amendment v4

The earlier DEV year cache supervised one separator-space token and four digit
tokens. That space was strongly discouraged by the native teacher format and
contributed substantial unrelated KL. V4 excludes only consecutive leading
tokens whose individual nonempty decoded text is entirely whitespace, moving
those exact IDs into each model's known gold prefix. Complete input ID sequences
stay identical. A merged token such as ` Paris` remains one supervised content
token. Blank semantic answers are rejected. The original student/teacher prompt
functions and greedy generation are unchanged; closed generation still produces
its own leading whitespace. All earlier-mask DEV training is excluded from
hyperparameter selection and formal conclusions.

Fresh `prepare_cache.py` layouts declare
`answer_mask_policy.version=semantic_content_v4`. The CPU migration tool
`dev_tools/repack_semantic_cache.py --parent-cache OLD --out NEW` first verifies
all parent full-file/per-fact digests. It copies only retained hidden/logit rows,
preserves each full model input, copies the readout byte-for-byte, then verifies
the derived cache. Its provenance is explicitly
`CPU_DERIVED_FROM_GENUINE_GPU_CACHE`; it never claims a new GPU forward.
Original caches and the exact v3 source snapshot remain available. The changed
cache_io identity requires a new actual GPU exact-recovery qualification.
