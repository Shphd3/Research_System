# Protocol: A15_17_E07 15B Sidecar Persistence Audit

## 0. Approval snapshot

| Field | Frozen value |
|---|---|
| Document / block status | `APPROVED_FOR_LOCAL_SMOKE_THEN_PASS_GATED_5090_4_SPOT_FULL`; A–G confirmed by researcher authorization in the 0920 conversation; consistency `PASS` subject to operational Smoke gates |
| Purpose / role | Robustness check of the A15_17 native-write question at an earlier, exact 15B point; not a new primary result |
| Anchor / Focus | [A15_17 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md); [0920 Focus](../../../../focus/legacy/0920_focus_three_model_sae_representation_audit.md) |
| Tested clause / rival | Whether the Dense–SALL difference in cross-expression-readable native attention write is already observable at 15B, versus scale, shared direction, templates, or an SAE-only readout difference |
| Treatment / control | Original all-eight-layer sidecar SALL at exactly 15,000,000,000 valid training tokens versus Dense at exactly the same token count; no M2/S7 substitution |
| Held fixed | Same P_rel_v2, N8_v1, PAWS_wiki_final input IDs and fit/dev/test splits as E06, same tokenizer, read site, layer numbers, two poolings, probe capacity and fit-only transforms |
| Decision quantity | 15B SALL−Dense P `test_joint` relation-family-equal linear accuracy at native \(a\), layers 4 and 8, last content token; descriptive persistence contrast, never a replacement for E06's 21B primary |
| Support / non-support / insufficient | Same-direction, qualified 15B contrast supports only earlier-instance persistence; opposite/zero trend limits persistence, not the 21B verdict; interval spanning zero or failed qualification is insufficient |
| Execution | First a sequential local single-H100-40GB-MIG Smoke for both exact checkpoints; only after both PASS and a measured local ETA, submit one single-node 4×RTX5090 Spot read-only full task via the repository submission template; no startup polling requested |
| Cannot claim | Across-seed causal SAE effect, broad semantic superiority, actual model use, a universal 32-dimensional space, capacity or continual-learning gain |

The researcher explicitly requested and preapproved this ordered wave, documentation, local Smoke, and pass-gated full submission on 2026-09-20. This does not authorize model or offline-SAE training, checkpoint mutation, commit, push, or publication.

## 1. Definitions and alignment

\(a\) is the native output of each attention `o` projection, after \(W_O\) and before residual addition. Human layers 1–8 map to code indices 0–7. `last` is the last valid content token; `mean` averages exactly those content-token vectors. For SALL only, \(z\) is the Top-K sparse code, \(\hat a\) its reconstruction and \(e=a-\hat a\) its error. The normal sidecar forward path sends \(a\), not \(\hat a\), to the residual/MLP. A linear probe establishes readable information for its fixed task, not model consumption. CKA is a centered sample-structure alignment diagnostic, not a semantic score.

E06 owns the 21B primary decision. E07 asks only whether an exact 15B pair displays a compatible or differing pattern on the same frozen inputs. The strongest rival is scale/template/observer change without transferable relation direction in raw \(a\). This is a single-run-lineage association, not randomized training causality. The 15B SALL run is a 4-rank continuation from its own 8-rank parent at 9,174,381,056 tokens; the branch must be shown when joining earlier points. Dense's training continuation is separately verified. No inter-model initialization identity is assumed.

## 2. Data, supervision, and model identity

Reuse the E06 frozen joint data manifest SHA-256 `49345f555d231811f02a2fb38c83a0aea690b2df19943bc93f1f7dc61886a061`, without regenerating or resplitting: P_rel_v2 200 entity groups, four relation families, eight templates, two directions, fit/dev/test entity groups 120/40/40 and template IDs 0–3/4–5/6–7; `test_joint` contains 640 sentences in 40 independent entity groups. P's 64 canonical examples have a delegated AI review, not independent human annotation. N8_v1 has eight M2D2 academic categories and 300/100/200 records per category for fit/dev/test; its category is not token-level truth and its `source_group_id` is a published record rather than a whole paper. PAWS_wiki_final has 8,000/2,000/2,000 official-split pairs after exact sentence isolation; unavailable source-root mapping makes it a diagnostic, not source-family-confirmed generalization. All are tokenized with `/data/share/Qwen3-0.6B-Base`, tokenizer JSON SHA-256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`.

The probe sees only the frozen \(a\) vector and fit label; P's four family-specific binary classifiers predict direction of the first versus second referent, N8 predicts eight record categories, and PAWS scores a pair of separately encoded sentences by cosine similarity. No confirmation label enters model forward, transform fitting, hyperparameter or layer choice. Invalid labels, empty content, unpaired examples, or mismatched input hashes fail closed. Use exact 15B Dense and original SALL checkpoints and their own source roots from the generated `model_manifest_15b.json`; preflight verifies complete milestone manifest, token count, file size, source hashes and architecture, while Smoke loader validates full state-file SHA. The model is eight-layer, hidden size 1024; SALL online SAEs have width 30,000 and inference Top-K 32 at all eight attention writes. The source code, checkpoint, and optimizer remain unmodified.

## 3. Analysis and verdict contract

At each of layers 4 and 8 and both poolings, fit four P family classifiers on fit only after fit-only centering/global-RMS scaling. Use logistic regression `lbfgs`, `max_iter=5000`, `tol=1e-4`, L2 with \(C\in\{0.01,0.1,1,10,100\}\); choose a common \(C\) by dev-joint four-family mean accuracy, breaking ties toward lower \(C\). Preserve convergence failures. On untouched `test_joint`, weight the four directions/templates equally within each family, then four families and 40 entity groups equally. Report SALL−Dense percentage-point difference, 2,000 paired entity-group bootstrap draws (seed 20260920), percentile 95% interval, paired group sign-flip test with 20,000 draws, and Holm adjustment over layers 4/8. A positive interval excluding zero with adjusted \(p<0.05\) is a qualified same-direction *secondary* pattern; a negative excluded-zero interval opposes persistence; crossing zero is insufficient, never equivalence. Report exact point and intervals even if unfavorable. No 15B finding rescues, rejects, or changes E06's registered 21B primary.

For the eight-layer light scan use the first 32 fit and 16 dev-joint P entity groups, fixed \(C=1\) and no confirmation data. At most one layer outside 4/8 is selected by the largest absolute dev P SALL−Dense gap, lower-layer tie break, exploratory only. For P, N8 and PAWS save both `last` and `mean` from each forward and report them separately; P-last, N8/PAWS-mean are preferred, with the other pool a sensitivity. Report raw norms, spectrum, between/within \(B,W,B/W\), standard and U-corrected linear CKA with exact sample-ID/input-hash alignment and fit-only first-PC sensitivity. These locate change but cannot define semantic quality. N8 readout and PAWS cosine AUROC/AP bound transfer, not a combined semantic total. Teacher-forced N8 test NLL (255 predictions per 256-token window) and existing behavior results preserve adverse cost.

SALL's online dictionary is a secondary observer: on fixed small input, report pre-TopK rank-32/rank-33/tail distributions, positive-score counts, selected atom combinations, \(a,z,\hat a,e\) and reconstruction fidelity, plus matched-rank 32-capacity fit/dev/test readouts comparing \(\hat a\), \(e\) and their concatenation. Selected atoms in a panel are not a semantic-feature count. Information readable from \(e\) alone does not prove loss from \(\hat a\). No offline dictionary, altered inference K, or intervention is in scope.

## 4. Ordered stages, guards, and artifacts

| Stage | Input and operation | Why / gate | Artifact and handoff |
|---|---|---|---|
| Identity/data | Two exact 15B checkpoint manifests, source code/config hashes, frozen E06 input manifest | Prevent model or data relabeling; mismatch stops model loading | `manifests/model_manifest_15b.json`, validation receipt |
| Local Smoke | Sequentially load Dense then SALL on visible H100 MIG; all-layer \(x+a\) valid-token residual identity, sidecar-source equality, finite dual pools, right-padding relative RMS ≤0.02, causal prefix difference ≤0.1, state sample unchanged, exact input IDs and checkpoint SHA | Qualifies only local engineering; left padding remains unsupported; custom model has no KV-cache API | Two case JSON files, `SMOKE_PASS.json`, terminal receipt; any failure blocks full |
| Full extraction | Four independent 5090 workers split case/panel shards; right-pad only; each shard stores IDs, hashes, labels, both poolings and eight layers; online observer uses small fixed subset | Prevent case/panel loss, changed state and pooled-position drift; GPU runtime preflight checks four RTX5090, >30 GiB each, SM120 layer | Per-worker chunk hashes and manifests, `COLLECTION_PASS.json` |
| Analysis | Dev-only scan, 4/8 P/N8/PAWS readouts, geometry/CKA, observer, N8 cost, semantic controls | Separate raw main path from observer and adverse behavior | Distinct stage JSONs; complete result is pending, not asserted by submission |

The full runner refuses absent Smoke PASS, mismatched code/data/model/protocol hashes, incompatible target GPU/memory, duplicate or missing case-panel ownership, incomplete chunks, changed state, and missing analysis output. A failed PAWS source-root guard keeps PAWS explicitly diagnostic; P/N8 eligibility is judged separately. Partial output is retained with FAIL receipt and cannot become a result. No material post-start change to data, cases, metric, split, exclusions or decision rule may be silently substituted; append before/after, reason, visible results, approval and eligibility impact.

Execution workspace: `/data/250010109/MoE_Router/experiments/20260920_sae_representation_15b_early_audit/`; 15B Smoke/full have distinct immutable `runs/` roots. This Protocol owns the scientific/execution contract; future `detailed.md` owns actual commands, job ID, deviations, failures and result lineage. Four-GPU ETA must distinguish local-H100-MIG measurement from unmeasured RTX5090 extrapolation. Submission is the endpoint of this conversation; the user explicitly does not request startup observation.

## 5. Confirmation and freeze ledger

| Block | Status | Basis |
|---|---|---|
| A question/boundary | `CONFIRMED` | Researcher requests 15B next wave under existing A15_17 question; E06 21B remains primary |
| B data/provenance | `CONFIRMED` | E06 frozen panels and known N8/PAWS grouping limits reused byte-identically |
| C probe task | `CONFIRMED` | v2 P relation/N8/PAWS definitions retained without new labels |
| D models/site | `CONFIRMED`, load gate pending | v2 main 15B Dense/SALL pair; no M2/S7 scope expansion |
| E probe optimization | `CONFIRMED` | E06 exact fit/dev procedure reused |
| F comparison/verdict | `CONFIRMED` | 15B is descriptive persistence; same 4/8 P contrast, no primary replacement |
| G execution | `CONFIRMED`, Smoke gate pending | Researcher explicitly permits local Smoke then one 4×5090 Spot full without polling |

Registered scientific revision: this file as frozen before first 15B Smoke; code and data SHA receipts are external to this file to avoid self-reference. Cross-block check: same phenomenon, compatible task/site, fit/dev/test isolation, paired group uncertainty, resource and failure gates are explicit. No 15B semantic or behavior result has been observed when this Protocol was registered.
