派生阅读副本；原件位置：`assets/symbolic_order_moe_v2.md`。
[精确原始文件](../../sources/assets/symbolic_order_moe_v2.md)；研究修改仍回到原件。

---

# V2 symbolic auxiliary data

Asset ID: `data_symbolic_moe_v2_20261024`.

The data live in [the execution workspace](../../UNAVAILABLE.md).
The [loader and deterministic schedules](../../UNAVAILABLE.md)
implement the original 32-symbol, four-F/four-G permutation task. Each operation
pair has 20 training, six validation and six test inputs. Every symbol occurs in
single-operation training. Parent validation/test change prompt wording and do
not establish generalization to previously untrained symbols.

[Current strict access](../../UNAVAILABLE.md)
covers the data, exact official Base and its tokenizer. The
[data audit](../../UNAVAILABLE.md),
[exposure audit](../../UNAVAILABLE.md)
and [API audit](../../UNAVAILABLE.md)
bind actual files, label rules, seed-dependent minibatch contents and exact
high/low exposure counts. These CPU checks do not establish learning or reuse.

The answer alphabet is `s0` through `s31`; actual tokenizer checks preserve
their multi-token encodings. Evaluation uses open generation and whole-answer
equality. The C parent uses different fixed permutations, so wrong-mapping
interference remains a rival explanation. Answer-symbol exposure frequencies
are saved rather than assumed matched.

## Actual saved outputs

[Current selected output access](../../UNAVAILABLE.md)
covers one saved engineering smoke state, three actual prefix caches and five
completed checkpoint families available at 2026-10-24 16:08 UTC. It covers neither
planned trajectories nor later saves. The [registration ledger](../../UNAVAILABLE.md)
lists exact IDs; each completed run owns `registration_actual.json` with its
actual member paths, sizes, counters, tensor interface and resume fields.

The [registration helper](../../UNAVAILABLE.md)
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

Final selected access: [52 actual output groups](../../sources/assets/checks/20261024T165200_order_v2_final_actual_outputs.json).
The [coverage record](../../UNAVAILABLE.md)
accounts for all 152 saved checkpoint files, four prefix caches and 32 derived
analysis groups. The checkpoint count separates 148 task-trajectory states,
three external-process engineering states and one original smoke state. All
three completed order diagnostic directories have their 36 actual files
registered. No completed state, cache or diagnostic-file handoff is missing.
The [terminal-job index](../../UNAVAILABLE.md)
contains full platform receipts for all five jobs belonging to this round;
each is terminal and successful. This completion statement does not change
failed task qualifications or the unknown internal-reuse claim.
