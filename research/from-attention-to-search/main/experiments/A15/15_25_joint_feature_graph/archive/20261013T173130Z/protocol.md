# Protocol: Feature relations and candidate learning objects — phase one

[Chinese reading companion](protocol_cn.md) · [Researcher-provided Anchor](/root/.codex/attachments/12568c72-8935-4198-9682-a31a67e9ee35/1014_feature_relation_anchor.md)

Freeze the final CrossCoder and produce a reproducible joint feature graph, 3–5 proposed feature pairs, locatable text examples, and decoding contributions in the fourteen selected layers. Stop after delivery. The researcher chooses pairs and a target layer before considering shared versus separate expert learning. This phase does not train experts or test the later H1.

Sections 0–4 establish purpose and scope; 5–12 define data, computation and interpretation; 13–14 contain the task list, time estimate, resources and artifacts; 17 records confirmations and remaining proposals.

## 0. Approval and source snapshot

| Item | Current value |
|---|---|
| Experiment identifier | CC_FEATURE_RELATION_PHASE1; draft identity only |
| Document status | DRAFT_NOT_EXECUTABLE |
| Completed in this turn | Protocol drafting, read-only evidence checks and resource queries; new inference, feature caching and relation statistics remain NOT RUN |
| Authorized current activity | Complete this draft; no analysis task has been submitted or started |
| Primary Anchor | Attached 1014_feature_relation_anchor.md; SHA256 efedd70106a143475ce3de597ba7193acccb4c749520ab9b58117c08736712b1 |
| Confirmed active Focus | UNKNOWN / not bound. Complete the candidate as explicitly requested; do not create a Focus or change scientific state |
| Experiment role | Operationalization or proxy test of the composition list, and preparation of inspectable objects |
| Immediate question | Are there feature relations that persist in separated subsets, have checkable text, and are not supported only by frequent background nodes? |
| Fixed setup | One frozen Qwen3-0.6B Base; final 14-layer/F16384 CrossCoder; the existing 10,485,760-position VAL window |
| Primary comparison | Recheck every discovery raw-threshold edge on the review side, then compare reduced composition lists and overlap |
| Held fixed | Base, CrossCoder parameters and full buffers, TRAIN threshold, normalization, original contexts, gating rule and edge criteria |
| Human-confirmed amendments | Split the single bin into contiguous context blocks with independence limits; prefer four reserved H100s, use multicore CPU where appropriate; estimate before running without a smoke timing run |
| AI proposals | 128 contexts/block, seed20261014, pair nomination details, high-both scoring, memory/disk limits and a 120-minute formal active-compute ceiling |
| Stop condition | Deliver graph, tables, examples, pairs and limits; stop also on negative or insufficient results |
| A–G confirmation | Not yet individually confirmed; drafting does not authorize execution |

Execution language in the attachment is design context, not an instruction to run now. Record any later explicit execution authorization and reuse it within its scope. HIFER provenance is reported by the Anchor; this turn has not independently verified the paper. The numerical criteria below are taken directly from the Anchor and are not a claim of reproducing that paper.

## 1. Terminology and objects

| Anchor term | Operational meaning |
|---|---|
| Feature / node | Final CrossCoder ID0–16383; no assumed single meaning |
| Position | Eligible VAL token; identity is source-file hash plus absolute token offset |
| Context | Original fixed 1024-token input; not an original document |
| Contiguous context block | Consecutive whole contexts in the one bin; a split and within-bin inspection unit |
| Discovery side D | Subset used to find raw-threshold edges |
| Review side V / 复核侧 | Subset used to recheck discovery edges; not an untouched test set |
| Gated activation z | Nonnegative activation after the final checkpoint's original frozen inference rule |
| Binary occurrence x | One exactly when gated z>0; zero otherwise |
| Support | Number of eligible positions, not independent documents |
| Raw-threshold graph | All directed edges passing the Anchor criteria before transitive reduction |
| A→u | u usually occurs when A occurs and has broader occurrence coverage; no causal or propagation claim |
| Transitive reduction | Remove directly connected edges replaceable by other directed paths while preserving reachability |
| Composition list C(A) / 组成列表 | Direct outgoing neighbors of A after reduction; a statistical proxy, not causal decomposition |
| List overlap J | Intersection size divided by union size; empty union is NA |
| Depth | Longest directed distance to a node with no outgoing edges; such a node has depth0, unrelated to model layer number |
| Frequent background node | A common node that may pass conditional thresholds through its marginal frequency; not automatically removed |
| Decoding contribution | Reconstruction participation; show norms and amplitudes, not causal percentages |
| Candidate feature pair | A proposal for researcher review, not an approved training object |

A shared feature ID does not establish suitability for shared expert learning. This dictionary supplies one joint feature graph, not fourteen independent within-layer feature graphs.

## 2. Anchor alignment

| Anchor section | Procedure | Judgment affected |
|---|---|---|
| Overview | Complete counts, local graph, pairs, four text classes and layer heatmap | Whether inspectable statistical objects exist |
| Appendix A | Final-state binding, complete threshold restoration, batch-partition check | Correct object and measurement path |
| Appendix B | Frozen source/split and chunked exact computation | Data and resource feasibility |
| Appendix C | Raw edges → recheck all edges → reduce → composition lists | Retention of relations and lists |
| Appendix D | Background, lift, single-node Top10 removal, within-bin block description | Possible background domination |
| Appendix E | Pair records, texts, deduplicated positions/contexts, layer amplitudes | Locatability and distinct sample availability |
| Appendix F | Complete delivery and three outcome branches, then stop | Select objects, weaken the current explanation, or report insufficiency |

The human-confirmed contiguous-block amendment replaces whole-file/bin assignment for this single-bin window. The no-smoke estimation amendment replaces the 64k/128k timing pilots; small correctness checks remain.

## 3. Phase-one question and later H1

Check whether discovery relations meet the same rules on V; whether their composition lists can be inspected; whether candidate overlap is dominated by background; and whether positions map to readable text.

Preserve the Anchor's later H1: within one model layer, controlling training resources, sample frequency and initial prediction difficulty, greater similarity between two combination features' composition lists predicts greater advantage of shared expert learning over separate learning. Later evaluation emphasizes low-frequency content's independent-test loss.

There is no shared/separate learning loss in this phase, so it neither supports nor refutes H1. Low feature occurrence, low content exposure and learning difficulty are different quantities. Record feature frequencies here; content frequency, difficulty and the phase-two learning unit remain future decisions.

## 4. Rivals and guards

| Rival | Present guard | Remaining limitation |
|---|---|---|
| u is nearly universal | Marginal frequency, lift, conditional-minus-background, Top10 sensitivity | Other frequent backgrounds or encoding artifacts |
| Small-sample coincidence | Fixed supports, edge-by-edge review, block descriptions | Document correlation, near duplicates and within-bin distribution dependence |
| Format, vocabulary or context drives relations | Random and high-activation A-only/B-only/both/neither examples | Covarying semantics and format; no causal decomposition |
| Joint encoding or a numerical gating path creates relations | Frozen state/rules and batch-partition check | Mixed dictionary features and unmeasured representation coverage |
| Lists depend on reduction paths | Review full raw edges and rebuild reduction after removals | Statistical inclusion is not a combinatorial mechanism |

Do not add training comparisons or interpret these implementation/description checks as new scientific discoveries.

## 5. Data construction and provenance

### 5.1 Exact fixed inputs

E abbreviates the existing execution root /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder.

| Input | Binding |
|---|---|
| Base and tokenizer | /data/share/Qwen3-0.6B-Base; assets model_qwen3_0p6b_base, tokenizer_qwen3_0p6b_base; revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd |
| Final CrossCoder | E/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt |
| Final asset | crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013 |
| Producer checkpoint SHA256 | 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628 |
| Data | dclm_crosscoder_direct_bins_1b_a15_20261013; E/data/direct_dclm_bins_a15 |
| Data-manifest SHA256 | 874794a8657f8982f7abb12ee517ec551fce840d9f20dfe103f48589a6779849 |
| Analysis window | index_val;10,249 contexts,10,485,760 eligible positions, one source bin |
| Source bin | /data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000001_processed.bin |
| Recorded source-bin SHA256 | 664d07bcb4db743ac9ec62a9c6e4df245f3fd4fde35b8536dece439fcaac9697 |
| Small identity records | E/analysis/handoff_20261013T154617Z/bindings.json and run configuration, input_contract, source_manifest, normalization, final validation, source_positions and checkpoint registration |

Producer hashes/current access are distinct from a fresh payload load or full GB-file hash. Refresh strict input access at execution; record stat, small-file hashes and whether each large hash was recomputed. Follow registered-location lookup before declaring a missing asset; do not guess substitutes, download replacements or retrain.

Search registered entries and the specified A22 run/analysis directories for a final per-position cache. None was found in that bounded draft-time inspection; marginal validation statistics are not such a cache. Reuse only a cache matching final checkpoint, positions, threshold, normalization, precision and full pre-split window. Otherwise regenerate. Do not use 0.5B or unrelated-run caches.

### 5.2 Proposed exact split

Confirmed principle: contiguous context blocks; each whole block belongs to one side; no random individual-token split; retain within-bin independence limits.

AI proposal:128 consecutive complete contexts per block; retain the final shorter block; seed20261014. Sort original contexts by source offset, form approximately81 blocks, seed-permute their processing order, and assign each next block to the side currently having fewer eligible positions. Break equal side totals with the fixed seeded generator. Never split or discard blocks or tune assignment using activations/text.

Freeze split_manifest before reading features: block offsets, context/position IDs, eligible counts, D/V membership, algorithm and seed. Record actual N_D/N_V, not a fabricated exact half. Require disjoint position sets whose union contains exactly10,485,760 positions.

Preserve original 1024-token boundaries and preceding tokens. Never truncate a context to enforce side membership. Eligibility and special-token exclusions follow the original index; no added outlier exclusion or position sampling.

### 5.3 Independence and text

Original-document identity and near-duplicate separation remain UNKNOWN. Blocks may belong to the same original document. This VAL has been repeatedly used during training evaluation and is not untouched confirmation data.

Every position must map to source bin/hash, absolute offset, context token IDs and local target position. Text is tokenizer-decoded context, not recovered original source text. Save model-visible preceding tokens; right-side text is for reading, not the target position's input. State source-document limitations in cards and the summary.

## 6. Analysis task and permitted information

Inputs are same-position activations from the fourteen frozen layers. Outputs are gated features, exact counts, graphs, lists, pairs, texts and layer contributions.

No new supervised task, domain labels or optimization is introduced. Do not select pairs using future shared/separate test loss or invent a phase-two dataset. Text meanings are reviewable suggestions, not supervision truth. V is used for descriptive review and object selection, not represented as an independent confirmatory trial.

## 7. Architecture, loading and frozen inference

Selected one-based layers2,4,…,28 correspond to zero-based1,3,…,27; hidden1024 and F16384, independent encoders/decoders. Hooks are block residual-post, with the last block taken before final global norm.

Adapt a standalone analysis loader: construct FastBatchTopKCrossCoder, strictly restore the complete crosscoder state including threshold,k,inactivity counters,completed_updates, and restore CenteredRMSStats from payload. Do not invoke the training main function, construct an optimizer or resume training. The existing checkpoint.load_checkpoint requires an optimizer and is not the direct analysis interface. After CPU payload loading, release unused Adam/RNG/cursor state; do not copy Base or checkpoints.

Use saved TRAIN centering and vector-RMS scaling. Base stays eval/frozen/no_grad/use_cache=False, with qualified BF16 Base/GEMM and FP32 state/ranking. Set both model and backbone attention implementation to SDPA instead of the extractor's eager default. Coder stays eval/use_threshold=True; no dynamic buffer updates.

Freeze the original A22 full-VAL inference batching now:16 original1024-token contexts per Base forward,1024eligible positions per coder batch. Rank ranges are[0,2621440),[2621440,5242880),[5242880,7864320),[7864320,10485760). Preserve complete contexts at rank boundaries and select only owned positions. D/Vmembership is an independent split_manifest label, not the rank partition. The section14count tile≤4096rows is a different batch and does not alter feature inference.

For original ReLU output r_f(t), score is r_f(t) times the sum over layers of decoder-vector L2 norms. Strictly compare score>checkpoint threshold and preserve the resulting gated z. Load the full scalar from state; do not hardcode rounded0.051281, refit on D/V or use per-token TopK256.

Compare two feature-batch partitions on identical positions of one small snippet, holding contexts and Base outputs fixed. Record threshold/state hashes, continuous differences, mask disagreements and distance to cutoff. Mask disagreement is a numerical-boundary limitation; retain the already-fixed primary batching rule and do not claim batch invariance. Wrong inference path, updated buffers or nonfinite values require stopping. This check does not estimate throughput.

## 8. No new training objective or optimization

New loss, optimizer, learning rate, training batch, expert training, MoE training and CrossCoder continuation are NOT APPLICABLE/NOT RUN. The trained dictionary's reconstruction objective is historical, not a new objective here. The later separate-test-loss minus shared-test-loss measure is not computed.

Analysis telemetry records positions, read/write times, throughput, CPU/GPU memory, unique rows, repeated reads and failures. Do not fabricate training TensorBoard curves. During the formal stream,record actual L0mean/maximum/90th/99th/99.9th percentiles and actual cache volume without a timing pilot.

## 9. Conditions, seeds and checkpoints

| Choice | Value | Grounding/state |
|---|---|---|
| Appearance/graph rules | Anchor criteria with final frozen gate | Anchor source; no threshold tuning |
| Window/features | Existing10,485,760 positions, all16384 features | Anchor/verified index |
| Split principle | Whole contiguous context blocks, within one bin | HUMAN_CONFIRMED |
| Block size and seed | 128 contexts;20261014 | AI proposal |
| Random text examples | Five/class or all when fewer; seed20261014, deterministic per-pair/side/class derivation | Anchor quantity, AI-proposed seed |
| Background Top10 | D frequency descending, ID breaks equal frequencies; same list on V | AI proposal, freeze before sensitivity |
| Pair nomination | Two relatively high-J, two relatively low-J, optional middle case; fewer if unavailable | AI proposal, not a success threshold |
| High-both score | min(z_A,z_B) descending; position key breaks ties | AI proposal; retain raw values and scale caveat |
| Resource profile | One h100-4-reserved node, four H100s; GPU priority with multicore CPU | HUMAN_CONFIRMED |
| ETA policy | No64k/128k smoke or timing pilot | HUMAN_CONFIRMED amendment |
| Formal active-compute ceiling | 120 minutes | Anchor suggestion, awaiting draft review |
| Added disk/CPU RSS/per-GPU allocated ceilings | 64GiB/256GiB/64GiB, capped by actual allocation | AI engineering proposals |

Seeds do not confer evidence. Generate and freeze UTC run_id before later execution; refuse existing output directories.

## 10. Exact counts, graph and composition lists

### 10.1 Counting and edge rule

Count N,n_A,n_u,n_Au separately on D and V, equally weighted unique positions. Binary x_f(t)=1 iff gated z_f(t)>0.

Keep every A→u satisfying:
- n_A≥200,n_u≥200,n_Au≥20;
- P(u|A)=n_Au/n_A≥0.8;
- P(A|u)=n_Au/n_u≤0.5;
- n_u/n_A≥2.

Evaluate thresholds by exact integer comparisons5n_Au≥4n_A,2n_Au≤n_u,n_u≥2n_A; display float64 probabilities. Zero denominators produce NA and no edge. Do not create self-loops. Below support is insufficient, not evidence of no relation; do not lower thresholds to obtain pairs.

Save complete discovery raw graph G_D first. Frequency at least doubles along each edge, so a positive-support cycle is mathematically impossible. A detected cycle is an implementation/definition failure: preserve evidence and stop rather than deleting edges.

### 10.2 Fixed review order

Freeze all G_D raw edges; recheck every one on V using the complete criteria. Preserve passes and failures with SUPPORT_INSUFFICIENT or THRESHOLD_NOT_MET and per-condition flags. Passing raw edges form G_V, the review-passed graph—not an independently rediscovered full V graph.

Only then reduce G_D/G_V into R_D/R_V and compute lists/depth. Never reduce before rechecking candidates, and never report unsearched new V edges as absent. No top-edge truncation or approximate candidate generation substitutes for complete statistics. Stop and propose any incomplete-graph alternative separately if resources prevent this contract.

### 10.3 Lists and rankings

C_D(A),C_V(A) are direct outgoing neighbors in the respective reduced graphs:

\[
J_s(A,B)=\frac{|C_s(A)\cap C_s(B)|}{|C_s(A)\cup C_s(B)|},\qquad s\in\{D,V\}.
\]

J and set cardinalities have no units. Empty union is NA; one/two-element lists receive a warning without silent exclusion. Save each node's D/V-list Jaccard, pair J_D,J_V,J_V−J_D, intersections/unions and complete lists.

AI-proposed comparable pool: unordered A<B, both nodes supported≥200 on both sides, and the two lists' union nonempty separately on each side. Retain insufficient/NA records for other cases. Two empty lists on one side give NA; one empty and one nonempty list give J=0 by the formula, flagged as a node without a composition list. Such zero is not automatically a pair of two different compositions. Compute tied ranks within the declared pool before nomination. Equal J gives equal rank; IDs only order display. Discovery J defines relatively high/low regions; review J describes retention. Do not invent a stability cutoff.

Chunked binary list-matrix products may compute all intersections; degrees give union sizes. Record pool size and ranking scope. If only a predeclared smaller pool is computed, call it that pool's rank, not full-graph ranking; reducing the search scope needs an explicit recorded change.

## 11. Background, uncertainty, texts and layer contribution

### 11.1 Background

Save p_u=n_u/N,lift=P(u|A)/p_u and P(u|A)−p_u for every raw edge; lift is unitless and zero-background is NA. Keep the main criteria unchanged.

Freeze the discovery-frequency Top10. Make ten single-node-removal versions. Delete a node and incident edges separately from raw G_D/G_V, then recompute reduction, lists and pair rankings; do not delete only from R_D/R_V. Simultaneous removal of all ten is not an automatic extra condition.

Also record main-list common-item count, Top10 common-item count and fraction, NA with no common items. Removal can raise or lower J; nonzero J after individual deletions does not exclude domination by multiple background nodes. If A/B itself is removed, mark NOT_COMPARABLE. Deliver all versions, not a preferred one.

### 11.2 Current uncertainty unit

There is only one confirmed source file. Do not report independent-document/token confidence intervals or document bootstrap. Describe within-bin blocks: per-block N,node supports, edge joint supports and conditional ratios, plus10th/50th/90th percentiles across nonzero-denominator blocks, zero-denominator counts and actual support. These are descriptive distributions, not independent-sampling intervals.

For all discovery edges retain block-recomputable counts or descriptions; preserve full block records for final pairs. Intervals do not alter edge decisions. No p-values or multiplicity-adjusted significance claims are made. Fixed edge rules and researcher interpretation remain distinct.

### 11.3 Pairs and text sampling

Nominate3–5 pairs from the review-passed graph, covering higher/lower list overlap when available. Record differences in supports, frequencies, list sizes and unique sample availability. AI-proposed target:two higher and two lower discovery-J pairs, optionally a middle case. Group tied J values first and seek examples from opposite ends of that ordering, showing actual values and nomination reasons. This is exploratory nomination, not a numerical acceptance threshold. Never split equal J into high/low by ID; zero from one missing list is a separate unformed-list case. Deliver fewer if distinct overlap or interpretable cases are unavailable.

Use no arbitrary weighted candidate score. Record nomination reasons and unmatched quantities. Locatable text is verified by the program; semantic meaning remains human review, not automatic PASS.

Default text sampling on V:
- A-only:five random plus five ranked by z_A;
- B-only:five random plus five ranked by z_B;
- both:five random plus five ranked by min(z_A,z_B);
- neither:five random only.

At most35 selection slots per pair. Random/top samples may overlap; retain both tags and unique count, not a claim of35 unique examples. Save all when a class has fewer examples. Both raw scales may differ, so this ranking is a display rule rather than calibrated semantic strength. Binary-only caches require recovering candidate continuous values; frequency cannot manufacture activation magnitude.

Save pair IDs,side,source hash/bin,block/context,target absolute/local position,target token,left/right text,model-visible prefix,z_A/z_B,masks and selection rule. Classification is at the target token, not anywhere else in its context.

Record four-class unique positions,unique contexts and targets per context on D/V/all. For the prospective A/Bgroup concatenation, exposure-record count=n_A+n_B,unique union positions=n_A+n_B−n_Au,and duplicate position exposure records=n_Au. These describe prospective sample load,not actual training exposures in this phase. Count both once in the union; future context-level training needs context deduplication again. Program rereads and random/top display duplication are separate telemetry,not substitutes for duplicate exposure. Do not create an approved phase-two training set.

### 11.4 Layer amplitudes

Save candidate decoder norm per layer and mean over all eligible positions—including zeros—of z_f(t)×norm(d_f,l), separately on D,V and all. Keep unnormalized values.

Normalize each feature's fourteen-layer amplitude profile by its layer sum for the heatmap; zero total is NA. Shared z makes the nonzero normalized amplitude profile equal to the normalized decoder-norm profile. It is not fourteen independent layer activations, causal percentages, online routing input or temporal ordering. Each figure retains block28 FVE86.4722% and replacement CE delta+0.305962nats.

## 12. Correctness checks and failure stops

| Check | Required behavior | Failure action |
|---|---|---|
| Known direction | N1000,n_A200,n_u400,n_Au200 yields A→u only | Stop/fix definition or direction |
| Known nonpassing case | Adequate support but insufficient conditional overlap records the failed criterion | Stop; never tune threshold |
| Independent frequent background | Seeded8192 binary positions, marginals0.1/0.99; report actual counts/lift | Demonstrates background edges, not a real mechanism |
| Exact-count identity | Real256 eligible positions/all16384 features: integer-GPU or CPU-bitset result equals naive sparse enumeration | Stop/preserve mismatch; no throughput inference |
| Integer output/tail | Synthetic all-one matrix with16columns,4095rows plus14rows; local joint counts4095/14,INT64total4109 | Stop INT8output overflow,BF16rounding,wrong INT32output or tail accumulation;no timing inference |
| Reduction identity | A→b,b→u,A→u reduces redundant edge; deleting b from raw graph restores A→u | Stop if reduced-graph deletion loses paths |
| State/batching | Identical snippet/two feature batches, frozen buffers and correct threshold path | Stop wrong path, buffer changes, nonfinite values; record boundary differences |
| Position completeness | Disjoint sides, correct full unique N, CSR rows map to contexts | Stop; no invented mapping or source substitution |
| Resource/scope | Stay within approved ceilings; no training/extra resources | Save recoverable progress and stop |

These are small correctness checks, not timing smoke/pilots or H1 evidence. Passing proves only checked implementation properties. If required dependencies/integer GPU interfaces are absent, use exact CPU bitsets within the same allocation where possible; do not silently install a new environment or expand resources.

## 13. Tasks, device plan and pre-run ETA

### 13.1 Resource evidence

The researcher selected four reserved H100s on one node. Profile:h100-4-reserved/spec n6ls.iu.i40.4/reserved. Read-only current queries of the historical A22 worker reported88vCPU/960GiB. A new allocation must report its own CPU quota,memory and GPU availability.

The harness sees192 logical CPUs but is limited to8CPU-time cores and128GiB. Do not use visible192 as analysis capacity or pretend this environment has the reserved node's88cores.

On the actual reserved node, propose64CPU workers, one BLAS/OMP thread each; reduce to the actual quota if lower. Share read-only matrices through mmap/shared memory rather than64 full copies. GPU handles frozen forward, feature scoring, exact block-matrix counts and matrix-friendly list intersections. CPU handles graph reachability/reduction, block descriptions, decoding and figures. Independent graph versions may parallelize; do not pretend topology-dependent single-graph steps are64 independent operations. Choose CPU for unsuitable/unsupported kernels without a separate performance benchmark.

### 13.2 Task list

| Task | Work | Device | Conditional wall/human estimate | Output |
|---|---|---|---|---|
| T1 | Bind inputs, exact split manifest and pre-run resource/ETA report | CPU | 10–20min | Bindings/split |
| T2 | Standalone loader,sparse cache,integer count and graph/pair code | Engineering | 60–120min | New code/source manifest, not formal results |
| T3 | Small correctness checks in section12 | CPU/small GPU snippet | 20–40min | Correctness receipt; no ETA calibration |
| T4 | Read/regenerate the full frozen-state sparse features | Four H100s/disk | 5–15min initial estimate | Complete row map,z and occurrence |
| T5 | Exact D/V counts,edge review,reduction,Top10,list ranking | GPU/multicore CPU | 20–75min initial estimate | Full graph/tables/descriptions/pairs |
| T6 | Texts,layer contribution,readable figures,summary and delivery checks | Multicore CPU/cache | 30–60min | Examples/figures/summary/registration pointers |
| T7 | Researcher reads/selects objects | Human | About20min | Select/revise/stop; no automatic phase2 |

From the present unimplemented-analysis state, estimate3–6hours to delivery, excluding queue/user waiting. A qualified cache/implementation can shorten this. Full CPU counting or a very dense graph may take longer; no total-duration guarantee is implied.

Historical full final VAL took79.8727s at131,281positions/s on this profile. It is a frozen-inference reference, not cache-write/co-occurrence/reduction/ranking throughput. Do not run64k/128k timing smoke, substitute35k training positions/s, or call the old79.9s the whole analysis ETA. T4 allows loading/I/O/new outputs; T5 is an unmeasured engineering range.

Issue ETA and capacity estimates before formal execution, then run only if not obviously over ceilings. Actual formal progress may update remaining ETA without expanding scope. Proposed formal active stages—generation/counting/graph/sensitivity/candidate recovery—total at most120minutes of stage wall time; overlapping stages each retain their own ledger cost. Engineering,document work,human reading and queue waiting are outside this ceiling. Forecast or actual overrun saves progress and stops for a decision.

## 14. Algorithms, artifacts and provenance

### 14.1 Exact chunked implementation

Never allocate full N×F dense activations or save full fourteen-layer raw representations. Default cache:per-position sparse gated FP32 z with uint16feature IDs,uint64row pointers and position map. Optional binary bitsets support exact CPU counting.

GPU proposal:0/1 block X_t transposed times X_t,INT8 inputs with exact INT32local accumulation,then INT64totals; proposed position tile≤4096, feature dimensions may tile. Validate the actual integer interface; BF16 output rounding is unacceptable for counts. No floating approximation,sampling,top-feature truncation or sparse candidate shortcut substitutes for exact full counting. If unsupported,use multicore bitset-AND/popcount.

Assign position chunks across four GPUs; sum every local count for each side. Diagonal equals support,matrix symmetric,0≤n_Au≤min(n_A,n_u). Release model/matrix workspaces across stages to limit peaks.

Capacity from existing mean L0:about2.669billion nonzeros,default CSR~15GiB;binary bitsets20GiB;one INT64F-square matrix2GiB,two sides4GiB. Full dense FP32activations640GiB/full fourteen-layer BF16raw280GiB are rejected. These are estimates, not a new cache measurement or measured L0 tail.

### 14.2 Code/result ownership

Unique output root:E/analysis/feature_relation_phase1/<run_id>/,UTC run_id fixed before execution. Proposed new source:E/analysis_tools/feature_relation_phase1/. This program is not implemented yet; no fictitious runnable command is supplied. Frozen trainer/config/checkpoints/old results are read-only; refuse existing output directories.

Persist interfaces,seeds,block size,threshold semantics,count dtype,backend,root and budgets in run_manifest. Backend changes preserve definitions and verified identity; they do not change the statistical question.

| Artifact | Required content |
|---|---|
| run_manifest.json | Anchor/Protocol/code hashes,assets/verification level,state/threshold/normalization,software/device/quota,seeds,N,time/memory/disk/limits |
| split_manifest.json | Blocks,contexts/positions,sides,N,single-bin and near-duplicate limits |
| feature_cache/manifest.json and binary shards | Per-rank/shard feature_id:uint16,z:float32,row_ptr:uint64;row-level canonical VAL eligible index,absolute token offset,context index;join D/Vthrough split_manifest. Store source hashes in a shared dictionary;manifest binds shape,dtype,size/hash,row ranges,state/rules for direct reuse |
| correctness_receipt.json | Artificial cases,exact count/reduction identities,threshold path and numerical differences; no performance smoke |
| feature_frequency.csv | All16384 features,D/V/all supports,frequencies,mean z,zero-hit/insufficient flags |
| raw_edges_discovery.parquet | All raw discovery edges/counts/probabilities/background/lift |
| edge_validation.parquet | Every discovery edge's complete D/Vcounts,flags,review status/reason,block descriptions |
| raw_edges_validated.parquet | All passing raw edges before reduction |
| reduced_graph_discovery.json,reduced_graph_validated.json | All16384 nodes,direct edges,complete lists,depths,version,NA |
| sensitivity/ | Frozen Top10 and ten raw-removal/reduction versions,J/common-items/rank changes |
| pairs_table.csv | IDs,support/frequency,lists,J/ranks,matching differences,background,review,class unique positions/contexts,prospective exposure records/duplicates,targets per context,text opinions;program rereads/display duplicates separate |
| pair_examples.jsonl | Four classes,random/top selection,continuous z,target/prefix/text/provenance |
| layer_contribution.csv | Candidate layer norms,D/V/allamplitudes,normalized values,zero-total flags,limits |
| local_graph.png,layer_contribution_heatmap.png | Readable IDs/frequency/depth,edge probabilities/joint support,shown scope and numeric sources |
| phase1_summary.md,phase1_summary_cn.md | One-page Purpose,Model,checked expectation,bounded outcome,Analysis,failures,limits,next researcher choice |
| output_manifest.json | Actual saved files,shapes,dtypes,size/hash/completeness; no imaginary payload registration |
| failure_receipt.json if needed | Last completed chunk,stop reason,remaining fields,recovery cursor |

The local figure is a view of complete computed graphs, not a different statistical graph. Facet by candidate when needed; full lists remain in tables. Display omission never changes depth or J. Every label identifies side/version. Deliver Markdown and inspect figure readability; no webpage is required.

After actual saves,register reusable cache/analysis assets with parents,layers,fields,progress and verification under the asset lifecycle. Payloads/matrices/figures/checkpoints stay execution-side. Only small text/code/config/provenance manifests belong in Research_System. No commit,push or external synchronization.

## 15. Outcome branches and missing data

- **Ready to select objects:**complete checks,review-passing locatable candidates,and reported main/sensitivity evidence whose overlap is not wholly background-dependent. This only yields statistical objects worth review; researcher selection remains separate.
- **Current explanation challenged:**adequate support but unstable edges/lists/text meanings,or background-dominated overlap. Narrow/abandon this composition-list explanation; do not conclude all shared learning fails.
- **Insufficient evidence:**low supports,NA,few distinct examples,mapping/group/near-duplicate issues,implementation/resource limits. Deliver fewer than three pairs if necessary; report the minimal missing evidence/cost,not H1refutation.

No new scientific PASS cutoff for J stability,lift or background share. Fixed numerical edge rules are section10; interpretation remains human-owned. Record execution completion,candidate availability and scientific acceptance separately. Preserve failures,insufficient cases and unattractive examples/sensitivity versions.

## 16. Cannot claim

No causal composition,true combinatorial mechanism,fourteen independent layer graphs,pretraining emergence,online routing signal,shared/separate advantage,rare/difficult content improvement,or full MoE allocation effectiveness. Do not mark block28fidelity or document deduplication as resolved. Co-occurrence,list overlap and layer participation remain descriptive tool measurements.

## 17. Confirmation, freeze and amendment ledger

| Block | Draft state | Grounding/remaining decision |
|---|---|---|
| A Question/boundary | PROPOSED | Preserve Anchor phase1,do not test H1 |
| B Data/provenance | PROPOSED,partially HUMAN_CONFIRMED | Block split accepted;128contexts/seed20261014proposed |
| C Analysis task | PROPOSED | Description/object preparation,no new training/supervision |
| D Model/inference | PROPOSED/VERIFIED_SOURCE | Final full state/original path,no rounded cutoff |
| E Optimization | PROPOSED/NOT_APPLICABLE | No new loss/optimizer |
| F Comparison/evidence | PROPOSED | Anchor thresholds unchanged;Top10 source,nomination,both score proposed |
| G Execution/reproducibility | PROPOSED,partially HUMAN_CONFIRMED | Four H100,GPU-first/multicore CPU/no timing smoke accepted;120min/capacity limits proposed |
| Cross-block consistency | Draft self-check complete;promotion incomplete | Scope/independence/stops aligned;Focus identity unbound,no automatic creation |

The two explicit replies are incorporated; do not relabel accepted split principle,resource preference or no-smoke ETA as unknown. The researcher can identify problems/corrections in one response without reconfirming every Anchor sentence.

After decisions,record confirmation scope,actual Focus binding or explicit ownership,design_frozen_at and scientific/config hashes in these same files. Run only explicitly authorized scope; design confirmation is not automatic launch. After execution,preserve registered body and append amendments documenting visible data,affected evidence and approval. Sampling,window shrinkage,edge limits,source/threshold/resource changes or phase2entry never happen silently as optimization.

## Verification sources

- [Exact bindings](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/handoff_20261013T154617Z/bindings.json),[training report](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/final_training_20261013T115447Z/report_cn.md):final object/fidelity.
- [Data manifest](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/data/direct_dclm_bins_a15/data_manifest.json),[VAL index](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/data/direct_dclm_bins_a15/index_val/manifest.json):single bin/positions/document limits.
- [BinEvents](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/crosscoder/bin_data_a15.py),[extractor](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/crosscoder/extraction_a16.py),[gate](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/crosscoder/batchtopk_a18.py),[accelerated coder](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/crosscoder/fast_batchtopk_a21.py),[builder](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/crosscoder/train_a22.py:328).
- [Historical resource request](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/platform_status.json:55),[execution envelope](/data/250010109/Research_System/docs/execution_envelope.md:193),[historical final VAL time](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/validation_000999997440.json:49305):read-only live historical worker query88vCPU/960GiB;no new allocation.

