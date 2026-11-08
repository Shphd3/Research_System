# FP32 audit of small primary margins

The registered BF16 result remains intact. A post-hoc numerical rule selects every main prompt with absolute correct-minus-other margin below0.06nat, plus its paired fact.24states/122prompts were reloaded and rescored by native FP32 forward/head/logsoftmax with TF32 disabled, taking169.36s under300s. No text, training, primary score or threshold changed.

Eleven choices flip and eleven state/gap paired counts change by one family. The table labels actual billions of pretraining tokens, gap, primary BF16 successes/24 and selected-pair FP32 sensitivity successes/24.

|模型|实际B token|间隔|注册BF16 成功/24|边界配对改用FP32后/24|
|---|---|---|---|---|
|Baseline|0|16|0|1|
|Baseline|0|1024|1|0|
|Baseline|0.5|256|4|3|
|Baseline|1|1024|5|6|
|Baseline|22.9155|1024|22|21|
|Baseline|37.2218|16|18|19|
|Baseline|37.2218|1024|19|20|
|Dense|0|16|1|0|
|Dense|0.5|1024|5|4|
|Dense|21|16|20|19|
|Dense|34.0764|16|22|21|

Every first sampled crossing at60/80/90percent remains unchanged in this selected-pair sensitivity. Dense5/10B near23/far19 and15Bfar21/17Bfar19 remain. Latest Dense34.076B is22/22in primary BF16 but21/22after selected-pair FP32. Tiny initial/early margins also change. This is not a full FP32 trajectory or a universal error bound. The0.026nat smoke example does not bound all precision differences. Reuse fresh primary whole-file SHA with unchanged size/mtime, then native strict-load again; no redundant GB hashing. [Raw audit](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/audit/precision_audit.json), [scope](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/audit/amendment_A02.json).
