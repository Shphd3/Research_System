# S13 append-only runtime and interpretation notes

## A1: startup compatibility and full-answer qualification (before development selection)

The new container lacked transformers/tokenizers/PDFreader. Dependencies are isolated under /tmp; no model/data/SAE substitution occurred. Initial model loading failed because an unrelated installed ONNX package used old protobuf generated descriptors. Preserve versions/inference_failed_protobuf.log. A process-local PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python flag repairs this import; no package downgrade or checkpoint edit. The subsequent old-prefix native calibration has maximum SAE-code error0 and cache/full-score qualification passes.

New16answers have unequal token lengths, unlike oldS11's eight2-tokenanswers. A supplementary development-only4-prefix/full-teacherforcing calibration must pass <=1e-4 before candidate selection/confirmation. These4replays are not additional independent samples and do not choose text/thresholds. The frozen score formula remains full conditional log-probability sum; token means are sensitivity.

## A2: separate statistical excess and original conditional-role retention (before development selection)

The registered excess criterion is unchanged. Additionally report whether each confirmation edge still meets its original HIFER-inspired direction/frequency/conditional thresholds (.8,.5,2). A positive beyond-margin excess alone is called excess replication, not proof that the original threshold-defined role persisted. Full conditional-role support requires both; this diagnostic cannot rescue an unpassed excess test. This prevents two different objects from being called the same replication.

Within-pair frequency quantiles use NumPy linear interpolation; meanofpairquantiles differs from the quantile of the family-equal mixtureCDF. Quantile and descriptor-subset intervals condition on the existing reference axis; only primary mean contrasts have joint reference/context uncertainty. No primary frequency rule changed.

## A3: match the production thread configuration in numeric calibration (2026-11-05T14:15:59.232838+00:00, before development selection)

Two supplementary checks used1CPUthread against producer8-thread FP32hiddenstates. Their scores agreed within1.46e-5nat, but an absolute MLP hidden-coordinate difference1.3733e-4 exceeded the unchanged1e-4native gate. Unpadding/batch1 alone did not repair it. Repeat under the actual8-thread production configuration passes all4prefixes and16variable-length answers,score max7.63e-6nat; no tolerance changed. Preserve both failed logs/scripts and passing variable_answer_calibration.json. This is runtime qualification,not new research support.

## A4: parent-to-child use of the fixed sibling edge (2026-11-05T14:15:59.232838+00:00, before development selection)

In addition to primary sibling effects, apply each fixed sibling-selected edge unchanged to its directparent and each child. Parentstrata use separate exact-margin Curveball chains on their8actualparentlabels. Report conditionalprobability differences/pairedclusterintervals,Holm32perwording,center>=10and6clusters eachside. No parent-specific edge reselection,noinventedparentfinegold,noexpecteddirection; typed exploratory,never a primaryfrequencyrescue. This implements the user's explicit coarse-to-fine relation question.
