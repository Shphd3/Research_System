# Last-layer memory: controlled low-exposure factual learning

This execution Protocol implements the researcher's [attached contract](user_execution_contract.md). The machine-readable authority for exact settings is [protocol_frozen.json](../../originals/experiment/protocol_frozen.json). Execution is authorized; scientific acceptance and question closure remain **Unknown**. No formal outcome is asserted here.

The question is whether shared trainable last-layer memory improves learning and retention of source-verifiable facts in a frozen small model, under matched supervision and update budgets. The primary rivals are ordinary additional parameter capacity, teacher-loss regularization, general increment shrinkage, and output-gate degeneration. This experiment does not equate small activation singular values with rare knowledge.

## Fixed model and computation

The student is the actual local official Qwen3-0.6B Base; the teacher is the original post-trained Qwen3-4B. The backbone, final RMSNorm and original output head remain frozen. Injection is at the last Transformer block output, before final RMSNorm. The shared dictionary has 256 keys/values, key width64 and hidden width1024. Queries, keys, signed values, output projection and sigmoid gate train. Memory and ordinary adapter each have exactly1,393,665 parameters; the adapter bottleneck is680.

Frozen-model states at gold-prefix answer positions may be cached. Final norm/head stay differentiable with respect to the increment. The full input sequence is causal; the future answer cannot influence the scored preceding-position hidden state. Independent generation receives only the question prompt, without source, teacher cache or gold answer prefix.

Only semantic answer tokens are supervised. Consecutive leading pure-whitespace tokens move into the known formatting prefix; a merged token containing actual content remains supervised. Complete model input IDs remain identical to the verified original cache. EOS is excluded. Generation prompts are unchanged and must generate any leading whitespace themselves. The current mask is `semantic_content_v4`.

For valid answer positions, loss is the token-normalized sum of native-head CE, teacher-to-student KL and the arm's increment penalty. KL uses temperature2, its temperature-squared factor, coefficient0.5, and exact common assigned support151669; CE uses all151936 native output rows. The267 undefined rows are excluded from KL. This is exact assigned-support KL, not native full-head KL or a top-k approximation. Teacher logits/backbone/readout are BF16; module parameters and penalty bases are FP32.

## Data and selection

Source texts are existing local Hotpot Wikipedia contexts. Explicit birth-year statements form atomic facts; original multi-hop Hotpot questions are not reused as atomic answers. Each fact retains original source record, title, byte offset, sentence and answer span. The underlying upstream revision is Unknown. Source-byte replay covers all selected facts;112 agent-reviewed examples and automated checks are distinct from human review, which is zero.

DEV facts, confirmation A/B facts, zero-exposure sentinel and reference families are isolated by declared person/title aliases. Family linkage is conservative rather than omniscient. Confirmation facts explicitly participate in training; their two alternate question templates are withheld from training and eligibility screening. The templates are controlled paraphrases, not a sample of unconstrained natural questions.

The fixed teacher/student eligibility screen uses the original training question and a separate screening question. Prefer teacher closed-book correctness on both. Otherwise require source-conditioned teacher correctness on both and label that cohort separately. Exclude stable-correct or unresolved students; retain mixed correctness and answer-format metadata. Source truth is never taken from a tested model's answer. No trained-module outcome selects facts.

The first4096 candidate facts yield the first complete2048-fact balanced experiment:1024 A,1024 B;38 closed-known and2010 source-conditioned teachers.128 separately isolated sentinel facts remain untrained. Larger stages use the remaining pre-frozen candidate population and the same eligibility rules. Previously screened facts are reused without rescreening. Supervision counts1 and8 are controlled exposure, **not** natural corpus frequency or Qwen pretraining exposure.

## Reference and controls

The original independent non-biographical WikiText reference failed its predeclared0.7 half-family overlap threshold:0.679476. It remains preserved and ineligible for spectral training. A larger pre-existing independent biographical reference passed the same threshold:903 families,32768 positions, overlap0.899848 and effective rank1024. The centered head64 explains74.03% of variance in that reference distribution. This is a biography-distribution basis; corpus-general or semantic interpretation remains unproved.

All six trained arms use the same data, actual quotas, order, seed, effective batch16, update budget, answer masks and teacher cache. The frozen baseline makes no updates. Arms are: ordinary adapter; CE-only memory; CE+KL memory; head64-penalized memory; fixed random64-penalized memory; total-norm L2 memory. Head/random share coefficient3.107190799106226; L2 uses0.19419942494413914 by the predeclared isotropic matching rule. Same dimension or this rule does not establish equal observed penalty strength.

DEV selected common learning rate0.001 by the saved two-architecture heldout-question rule; ties use the smaller rate. AdamW has zero weight decay, constant learning rate and clip1. The independently calibrated initial increment/reference-state norm ratio is0.001. Head penalty strength was calibrated on the trained DEV memory gradient, targeting median penalty/task ratio0.1; actual random and L2 ratios are retained. No formal score selects these values.

## Training and evaluation

Seeds1105 and1106 use a common family-assignment seed1105;1106 swaps low/high exposure assignment. Every fact has exactly1 or8 committed presentations. High/low final presentations share updates when possible to reduce recency differences. There is no distributed padding. Token normalization, full state, optimizer, RNG, cursor and exposure ledger are saved. Physical replay cost is distinct from the committed endpoint ledger.

Train A, evaluate the full A/B/sentinel panel, continue the same module and optimizer on disjoint B, then evaluate A retention and B acquisition. Each scale starts from the same seeded initialization rather than continuing a smaller-scale endpoint. Complete every arm before equally expanding to8192 and the maximum balanced eligible population up to20000, using measured throughput/storage/time rather than best-arm scores.

Primary success is correctness on **both** unseen questions per independent fact. Original-question accuracy and gold-prefix answer probability are separate. Scores are grouped by phase,1/8 exposure, teacher source and seed. Paired source-family bootstrap uses5000 resamples; question repetitions are not independent facts. Unresolved outputs remain explicit, with conservative estimates and bounds. Independent128-paragraph raw-text NLL tests bounded output preservation, not global general capability. Sentinel generation is separate; sentinel NLL is NOT RUN.

After B, fixed64A+64B+64sentinel diagnostics compare active, off, keys-only and values-only permutations with an identically batched baseline. A simultaneous common K/V permutation is only an invariance test. Correctness, prediction consistency and module dependence are distinct.

## Decision boundaries and execution evidence

Improvement over frozen Base can support added-module utility. Unique K/V benefit additionally needs a credible adapter comparison. A collapsed gate or otherwise untrained comparator cannot establish architectural superiority. Head-direction benefit needs comparison with no penalty, random directions and L2, while inspecting actual increment norms/gates. KL benefit is conditional on this teacher-conditioning policy and must not be attributed automatically to extra facts beyond gold supervision. Retention is judged together with B acquisition; a module that learns nothing new cannot claim useful retention.

Positive, negative, seed-inconsistent and insufficient results will all be retained. No SAE/CrossCoder training, original-weight writes, model/dataset downloads, publication or unrelated task changes are included. Current execution uses one authorized2×RTX5090 spot allocation after the required15-minute4H100-reserved attempt and documented H100 scheduling failures. Exact resources, fixes, checkpoints, raw outputs and per-task receipts remain execution-side.

Pre-formal engineering failures—teacher sampling-default override, pure-whitespace KL conflict, and the failing generic reference—are preserved. Current source-v4 semantic caches and actual GPU exact recovery passed before formal updates. See the source manifests, `resource_audit/implementation_review.json`, qualification receipts and per-plan formal-start certificates.
