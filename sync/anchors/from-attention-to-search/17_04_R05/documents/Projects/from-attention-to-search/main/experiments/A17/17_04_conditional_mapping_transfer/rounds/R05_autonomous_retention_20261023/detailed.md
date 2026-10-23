派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/detailed.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/detailed.md)；研究修改仍回到原件。

---

# R05 detailed execution record

Execution completed at 2026-10-22 17:25:36 UTC (2026-10-23 01:25:36 Asia/Shanghai). Read the [factual Summary](summary.md), then the separate [AI preliminary interpretation](ai_interpretation.md). The [original Protocol](protocol.md), [append-only amendments](amendments.md), and [single FFN qualification repair](protocol_ffn_repair_v2.md) retain distinct identities. Researcher acceptance and scientific closure remain `Unknown`.

## Question and model

This round tests whether selected parameter directions deserve reduced updating, whether residual updates benefit from separation, and whether native FFN experts and learned routing can use that arrangement. The candidate is a spectral selection rule, not an already established common computation. The main hypothesis requires preservation beyond ordinary updating and uniform slowing, with successful new learning. Capacity, optimizer coordinates, exposure, grouping information and router allocation remain separate rival explanations.

The conditional-list input visibly contains a mode, a command and three distinct words. Old mode maps command甲 to the first word and乙 to the last; reversed mode swaps the targets. Visible mode makes joint supervision consistent. Full-vocabulary accuracy, answer-only cross-entropy and conditional answer margins are separate measurements.

The model is the local official Qwen3-0.6B Base, with HF revision `da87bfb608c14b7cf20ba1ce41287e8de496c0cd` agreeing across six metadata records. Fresh SHA256 values bind model, config and tokenizer in `model_identity.json`; this is a byte identity, not a latest-upstream claim. The acquired-old E03 adapter contains the four layer-27 Q/K/V/O matrices after 1,200 updates and 24,000 answers, with SHA256 `48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75`. It requires the original Base model and is not a standalone checkpoint. Each continuation starts fresh Adam moments.

## Data and exposure

The registered dataset contains old, consistent and reversed worlds. This round reads only old and reversed: 4,800 TRAIN and 1,600 DEV examples. Each mode contributes 2,400 TRAIN and 800 DEV answers. Each DEV command by panel cell has 200 answers. Complete input-list IDs do not cross TRAIN and DEV. The unseen-order panel intentionally shares unordered groups with training; the unseen-combination panel does not. DEV is exposed and is not fresh confirmation. TEST labels are unused.

A and C use 20 new answers per update without old labels. B, D and E use 10 old plus 10 new answers per update with paired commands. Their raw scores cannot be compared across stages as a method effect. A complete 1,200-update trajectory has 24,000 valid answer targets; prefix and padding tokens are excluded. Seeds 29, 43 and 71 change declared continuation randomness while sharing one acquired-old checkpoint. They are not independent old-acquisition seeds.

Natural data come from the accessible registered DCLM global02 compressed source. The frozen first 192 usable nonduplicate documents are split into 128 TRAIN and 64 DEV documents, each taking the first 128 tokens. There are 127 prediction targets per document: 16,256 available TRAIN targets and 8,128 DEV targets. Text and token-window hashes are disjoint. R2 uses the exact same documents. Parent pretraining exposure is `Unknown`. Natural training does not receive reversed-list labels, so its new-list accuracy is a retention readout rather than a new-rule acquisition test.

## Computation and correctness

The first 27 frozen blocks are cached. The complete native last attention block remains differentiable in A/B/C. Native versus cached logits match exactly over all 6,400 list examples, with identical argmax. Training-batch shapes are separately checked. A computes one Adam candidate update and then filters the actual parameter displacement; it advances moments once. Orthogonal parameter directions are not assumed to be functionally independent.

B synthesizes a shared candidate part and complementary residual updates on the same old matrices. Full private residuals match per-mode available space but increase total effective degrees of freedom. Row controls match total effective degrees of freedom while reducing each mode's space. Restricted atoms require their Gram inverse to enforce both constraints; masking after projection would not suffice. B's coefficient optimizer and A's dense optimizer are different coordinate systems. The original four parent matrices remain frozen, with version and final-byte guards.

C performs the same current-weight SVD computation at updates 400 and 800 in all three arms. Dynamic adopts the new candidate; sham discards it and resets Adam at matched times; fixed discards it without resetting. Effective matrices and immediate outputs are preserved when the candidate changes. Previously protected directions can update after reselection; this is part of the tested intervention.

R1 D trains only native SwiGLU down projections, keeping gate/up fixed. Its ordinary experts fail DEV learning qualification. The single preregistered R2 repair trains gate/up/down inside each native expert, synthesizing matrices before nonlinearities. All affected D/E/F controls are rerun under separate configs, caches and run roots. This does not establish which added projection is necessary. Both rounds remain visible, and no second scientific repair is allowed.

E uses hard top-1 forward selection with amplitude one and an explicit straight-through softmax derivative. Learned training computes both expert outputs for this derivative; oracle/random routing and inference execute selected tokens only. Fixed-expert and joint phases have separate 600-update budgets and fresh optimizers. Router capacities are disclosed; equal-dimensional random summaries control summary information. Additional count-preserving random permutations compare allocation content at exactly the learned endpoint's expert load. Known-mode oracle regret is a reference comparison, not a mathematical minimum over experts. D's qualification failure bounds all E mechanism claims.

## Execution and recovery

Preparation `pt-f56663oz` and native smoke `pt-9qqk82pm` each used one H100 reserved GPU and finished before the four worker submissions. Independent-process replay restores update 1 and reproduces update 2 for weights, Adam, RNG, cursor, counters, candidate basis and deterministic metrics. Architecture-specific smoke and replay receipts remain separate; one smoke does not certify every architecture.

The original workers were `pt-z87v2rmc`, `pt-0io1qihh`, `pt-blfpdpa0` and `pt-39scm6j4`. All use the explicitly selected `h100-1-reserved` profile: share-space, share-cluster, n6ls.iu.i40.1, one worker and the envelope's shphd-lite-0911 image. Two single-expert natural readouts failed before their training step because a readout referenced expert 1 in a one-expert bank. The count-one guard was repaired; original failed attempts and source differences were archived, and both affected cases were rerun. This was an engineering repair, not another scientific configuration.

Worker 0 later failed when renaming the shared scheduler temporary state file. Its child had already completed and saved the full single-protected R2 endpoint. The controller receipt was reconciled from that evidence without retraining. The exact competing writer remains `Unknown`. A start-event audit found no unexpected duplicate task claims; only the two documented engineering retries occurred. The three remaining original workers finished their current children and exited successfully.

The full 165-task scope was preserved before migration. The replacement scheduler uses atomic per-task claim directories, UUID temporary files and independent result files, with no shared state writes or automatic claim stealing. A four-process CPU contention check verified unique execution and genuine failure/block propagation. Four replacement single-GPU jobs are `pt-hxd8mf12`, `pt-ofhikcrn`, `pt-8zx2597i` and `pt-hqiyhp78`. They run only the remaining tasks. Maximum concurrent allocation remains four GPUs. `queue_v2/results` is the final scheduler authority; `queue/state.json` is a derived compatibility snapshot after the original writers exited. The temporarily drained legacy plan was restored to the full scope.

An isolated loopback adapter resolved the old ACP client's strict parsing of the new service_time_expression metadata. Credentials, ACLs, global CLI, resource envelope and canonical submission template were unchanged. Durable mounted pod logs survive platform log expiry. No new resource profile, Spot fallback, unrelated job interruption, commit, push or publication was used. Machine submission, task and version timestamps define the audit chronology; manually estimated early note headings do not.

## Original frequency test and result boundaries

The old A15_24 frequency experiment has a different model path: original Base, a 14-layer CrossCoder, Tulu, eight nonlinear residual experts at final residual-post, and top-2 half-weight composition. This round returns to those exact assets for T_F/T_H seeds 11 and 22. It runs six fixed-weight branches over all 10,340 original DEV positions with the original batch size 128 and dispatch shape. All four H100 replays reproduce the saved original route and Base NLL exactly, passing the unchanged gate. Earlier failed numerical replays remain preserved.

The matched interventions measure immediate branch contribution and loss non-additivity, with paired whole-dialogue uncertainty. The residual expert outputs themselves add linearly; frozen normalization and cross-entropy can produce non-additive loss. These measurements do not identify a unique training mechanism behind the old frequency result.

R2's ordinary and multi-normal new TRAIN accuracies are 96.708% and 96.208%, while DEV is 82.375% and 83.125%. Every TRAIN command cell reaches 95%, but the weakest DEV cells are 51% and 54%. These actual full-vocabulary readouts establish a TRAIN-to-DEV gap. They do not establish a unique capacity or information-access cause. The separate Summary and judgment cards carry the complete endpoint tables and qualified AI interpretation.

All eight FFN natural-continuation endpoints worsen their own initial natural DEV NLL. Relative reductions in deterioration must not be presented as absolute learning gains. Per-document intervals are conditional on these fixed endpoints, not independent model-seed confirmation.

## Evidence trace and completion

Execution root: `/data/250010109/MoE_Router/experiments/20261023_autonomous_retention`. `inputs` preserves the original ZIP and V3 prompt bytes. `input_documents_manifest.json`, `model_identity.json`, `reuse_decisions.json` and `retention_vs_R02.patch` bind source identity and adaptation. Original and repair configs remain separate. Per-task logs/freezes bind commands and source/config hashes. Cases preserve per-example evaluation, full optimizer/RNG/cursor state, bases, actual checkpoint saves and TensorBoard events. `analysis` holds factual aggregates, bootstrap results, fairness checks and execution inventory; `audit` and asset access snapshots bind actual saved states.

`analysis/execution_manifest.json` inventories the fixed 89-case main matrix, excluding smoke, engineering retries and readout-only tasks. All 165 required tasks now have DONE receipts. The main matrix has 89 completed cases: 85 trained trajectories and four zero-update references, totaling 86,000 updates and 1,720,000 valid training targets. These counts exclude engineering attempts and readout-only diagnostics. All four replacement controllers saved completion receipts and exited naturally. Completion of execution does not establish a hypothesis or close the question.

## Terminal accounting and audit boundary

The final ledger contains no unrun, failed or blocked required task. Original engineering failures remain archived: two single-expert readouts and the original worker-0 scheduler receipt failure. Their successful recovery does not erase those attempts. The final execution manifest identifies actual checkpoints, per-example evaluations, TensorBoard files and the restored full plan. Saved states include optimizer/RNG/cursor information and require the recorded parent model; independent-process resume evidence is limited to the actually tested structural families.

R1's 19 D/E/F cases lack per-case environment version/precision receipts. They retain runtime/source evidence and are marked bounded, rather than retroactively receiving measured environment records. R2's 19 cases have their actual environment receipts. The actual saved-asset registration and independent fairness results are linked by the final artifact manifest.

The existing navigation checks still report the pre-existing untracked diffusion literature entry and missing 15_25_01 ownership-map anchor. R05 introduces no additional ownership error. No commit, push or external publication was performed. Source math delimiters are checked; rendered math verification is not claimed. Researcher scientific acceptance, mechanism judgment and question closure remain Unknown.

One R2 F/dense_protected source-version identity remains bounded: task freeze and later environment disk hash straddle the single-expert readout guard repair. The environment hash reads disk bytes, not imported bytecode, so the exact imported version is Unknown. Both preserved versions have identical F training/evaluation paths because F uses route `'none'` and does not enter the changed oracle-single-expert branch. Final source lookup also includes the 18 real migrated queue_v2 freeze receipts. The final registration reuses the fresh 686-state payload audit explicitly and adds provenance without retraining or replacing earlier immutable entries.
