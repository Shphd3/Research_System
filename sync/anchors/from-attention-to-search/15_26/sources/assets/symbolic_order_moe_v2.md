# V2 symbolic auxiliary data

Asset ID: `data_symbolic_moe_v2_20261024`.

The data live in [the execution workspace](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_data/).
The [loader and deterministic schedules](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_engine/data.py)
implement the original 32-symbol, four-F/four-G permutation task. Each operation
pair has 20 training, six validation and six test inputs. Every symbol occurs in
single-operation training. Parent validation/test change prompt wording and do
not establish generalization to previously untrained symbols.

[Current strict access](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/symbolic_input_access.json)
covers the data, exact official Base and its tokenizer. The
[data audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_data/audit.json),
[exposure audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_data/exposure_audit.json)
and [API audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/symbolic_api_audit.json)
bind actual files, label rules, seed-dependent minibatch contents and exact
high/low exposure counts. These CPU checks do not establish learning or reuse.

The answer alphabet is `s0` through `s31`; actual tokenizer checks preserve
their multi-token encodings. Evaluation uses open generation and whole-answer
equality. The C parent uses different fixed permutations, so wrong-mapping
interference remains a rival explanation. Answer-symbol exposure frequencies
are saved rather than assumed matched.

## Actual saved outputs

[Current selected output access](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/actual_output_access_20261024T160859729494Z.json)
covers one saved engineering smoke state, three actual prefix caches and five
completed checkpoint families available at 2026-10-24 16:08 UTC. It covers neither
planned trajectories nor later saves. The [registration ledger](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/registration_actual.json)
lists exact IDs; each completed run owns `registration_actual.json` with its
actual member paths, sizes, counters, tensor interface and resume fields.

The [registration helper](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source/register_actual.py)
registers completed runs through `register_completed_run(result, cfg)` and may
be called again for new completed trajectories. It preserves existing catalog
entries under cooperating writer locks. Endpoint SHA-256 hashes are freshly
computed; milestone and large-cache hashes are explicitly `NOT_RECOMPUTED`.
All outputs require the exact registered official Base; these saved increments
do not contain the complete model. Failed scientific qualification remains a
valid saved output and is not converted into a qualified model by registration.

Later calls preserve registered families and reuse their historical verification
after checking the current member set, paths and sizes. The current ledger marks
this as reused evidence, with no new payload hash or tensor deserialization.
Newly completed families retain the full first-registration metadata and counter
checks. Completed external-process engineering saves, native predictions,
diagnostic activation vectors/directions, matched-component readouts and reload
reports are registered as separate actual-output groups. A completion marker is
required for each group; planned or partly written files are excluded.

Final selected access: [52 actual output groups](checks/20261024T165200_order_v2_final_actual_outputs.json).
The [coverage record](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/actual_output_coverage.json)
accounts for all 152 saved checkpoint files, four prefix caches and 32 derived
analysis groups. The checkpoint count separates 148 task-trajectory states,
three external-process engineering states and one original smoke state. All
three completed order diagnostic directories have their 36 actual files
registered. No completed state, cache or diagnostic-file handoff is missing.
The [terminal-job index](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/final_job_terminal_index.json)
contains full platform receipts for all five jobs belonging to this round;
each is terminal and successful. This completion statement does not change
failed task qualifications or the unknown internal-reuse claim.
