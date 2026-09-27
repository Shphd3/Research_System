# Protocol: 20260926 atom usage and update-direction intervention

## 0. Authorization and snapshot

Status: APPROVED_FOR_DELEGATED_EXPLORATORY_IMPLEMENTATION_SMOKE_AND_FULL.
Authorization: the researcher requested that Codex choose the observation object, produce the minimal atom figures, advance the experiment and submit it on four H100 Reserved GPUs, without another audit/permission round. This authorizes this bounded implementation and execution; it does not pre-confirm its result or promote a Focus/PROJECTS state. A-G below are AI-operationalized under that express delegation, not individually researcher-reviewed blocks. The latest instruction supersedes the Skill's interactive block-confirmation workflow for this task.

Primary [Anchor](anchor.md): can domain-enriched atom spans locate domain-selective beneficial components of a shared update? Role: exploratory mechanism/proxy test. Primary comparison: same-sized parameter updates redirected away from enriched versus matched control decoder spans. Primary quantity: target-specific loss-of-benefit contrast \(M\), defined below. Static figures are a complete descriptive deliverable independent of whether the intervention supports H1.

Execution profile: `h100-4-reserved`; image: `shphd-lite-0911`; surface: ACP; one allocation, four independent source workers. Runtime: the experiment's `scripts/runtime.sh`, existing `/data/250010109/dependency_packages/hf_transformers_qwen3` compatibility layer. Submission: repository `templates/execution/acp_submit_template.sh`. Hard full-runtime ceiling: 3,600 seconds; up to four GPU-hours. A bounded local smoke precedes submission and GPU identity/no-op/replay checks repeat in the job. No persistent optimizer trajectory, checkpoint write, resource fallback, confirmation-set opening, collaborator sync or publication is included.

## A. Question and boundary

Purpose: move from a static atom-use description to an observed representation/update/consequence connection. H1 and H0 are stated in the Anchor. Outcome can be help, harm or insufficient evidence. Finding harm is not a completion condition. Atom index has no intrinsic ordering; no Gaussian law is assumed or fitted from an index curve.

## B. Data and provenance

Input: `/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/selected.jsonl`, with cached `activations.npz`. Four domains: computer_science, mathematics, physics, biology; two subfields each; each domain has 128 fit and 128 readout records of exactly 256 tokens. Total 1,024 records. Use all preselected records without activation-dependent record filtering. Two batches have distinct complete inputs, but paper identities are unavailable and source data were previously inspected. Record is the resampling unit; this does not imply independence between papers. No new claim of untouched confirmation.

Static analysis: positive firing frequency, mean coefficient including zero, and mean squared coefficient, first per record then equal-weight domain average. Runtime decoder atoms are unit-normalized. Squared coefficient shares are contribution proxies, not additive original-representation/reconstruction energy because decoder directions need not be orthogonal. Show full-dictionary coverage, fixed-fit-order identity comparisons, separate per-token and domain aggregate concentration, and readout-batch replication. Top-32 structural sparsity is not an empirical discovery. Any residual-without-common-atom plot is explicitly secondary and never replaces the full result.

## C. Learning task

Natural next-token prediction on fixed positions 14,30,...,254, with targets at the next positions. Sixteen targets per record. Each record loss is its sixteen-target mean; group loss is the mean of 128 records. No answer labels, prompts, classifier training, or generated text are introduced.

## D. Model and selected directions

Exact checkpoint: frozen fresh S7 lambda_rec=0.1 after 21,000,000,000 training tokens, as identified by the existing resolved-assets manifest. Checkpoint state SHA256: `edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33`. Observe native block7 attention output after `attn.o`, before residual. Virtual updates affect only `model.blocks[7].attn.o.weight`, shape 1024x1024. All base tensors and SAE buffers remain unchanged.

For each domain select 32 matchable atoms by descending fit-only positive-frequency enrichment over the mean of the other domains; atom ID breaks ties. This count is an exploratory computational choice, not an inferred natural number of concepts. Match three control sets using seeds 17,29,43, excluding that domain's target set. Eligible controls must have pooled firing frequency AND mean squared coefficient each between 0.5 and 2 times the target's value. Greedily match in standardized log pooled frequency and squared-coefficient coordinates, taking a seeded choice among the nearest ten remaining eligible candidates; no repeats within a set. Skip target candidates for which this matching cannot be constructed, fill from the same fit-only enrichment ranking and rebuild controls against the complete final target set. Preserve the unrestricted top32 list and all skipped atoms/reasons; these still appear in the descriptive static analysis. This selection restriction was adopted before any scientific intervention readout because the two strongest mathematics-enriched atoms had no comparable control atoms. It narrows the primary claim to matchable enriched spans, not all domain information. Selection never uses readout losses. Record exact algorithm, epsilon, eligible candidates and matching discrepancies in `analysis/atom_sets.json`. Common top1 is selected by pooled fit mean squared coefficient; it is a rank-one descriptive control, not compared as if rank matched to the 32-atom sets.

Use the normalized decoder columns to obtain each span by a rank-revealing orthonormal decomposition. Record numerical rank and orthogonality. Abort an affected comparison if target/control ranks differ or normalization remainder is near zero. Overlapping atom sets and correlated dictionary directions are permitted and reported.

## E. Update and numerical model

For each source \(s\), compute \(G_s\) from all its fit records at the fixed sixteen positions. Use \(\delta_s=-\rho\|W\|_F G_s/\|G_s\|_F\), with \(\rho\in\{10^{-4},5\times10^{-5}\}\). Each branch resets to the same checkpoint. No optimizer or momentum is used.

Cache native attention context \(c\) and block input \(x\); replay \(a=(W+\delta)c\), residual addition, norm2, gated MLP, down projection, final norm and vocabulary head in FP32, with frozen upstream BF16 computation. Disable TF32. Verify this numerical model against a complete forward with the corresponding FP32 override hooks; document its difference from an all-native BF16 forward. Frozen SAE re-encoding is descriptive and must not update activity buffers.

## F. Conditions, analysis and outcomes

Per source and step: full update; unscaled common-top1 span removal; for each of four target domains, unscaled target-span removal, norm-restored target-span removal, and three norm-restored matched-control removals. Total 22 branches per step, 44 per source, 176 across four sources. Every branch evaluates all 512 readout records. For \(P=QQ^\top\), unscaled removal is \((I-P)\delta\) and norm-restored removal multiplies this by \(\|\delta\|_F/\|(I-P)\delta\|_F\). These remove a component of the update, not the base representation or atom itself.

Primary metric: redirected minus full loss \(R_{sbt}\); target selectivity \(S_{sb}=R_{sbb}-\operatorname{mean}_{t\ne b}R_{sbt}\); enriched-versus-control contrast \(E_{sb}=S^{target}_{sb}-\operatorname{mean}_{r=1}^3S^{control,r}_{sb}\); \(M=\operatorname{mean}_{s\ne b}E_{sb}\). All domain/source averages have equal weight. Units: nats per predicted token. Compute separately for both steps. Report all sixteen source/target contrasts, even though the primary excludes four self-source pairs.

Uncertainty: 2,000 paired bootstrap resamples within domain/subfield, with each resampled record shared across every branch; percentile 95% intervals, conditional on this checkpoint, fit gradients, chosen sets and control seeds. Seed 20260926. The twelve source/target pairs are not independent replicates. Requiring both step results is a conjunction; secondary per-cell intervals are descriptive, with no simultaneous population claim. No filtering of outliers, unsuccessful source groups or unfavorable branches from \(M\).

Source qualification: full-update independent source loss improvement has a strictly positive 95% lower bound for all four sources at both steps. SUPPORT requires qualification, \(M\) lower bound >0 at both steps, all four target-averaged point contrasts >0 at both steps, and positive aggregate target selectivity for unscaled target removals at both steps. Target averages use the other three sources; the unscaled guard uses the same twelve cross-source pairs as \(M\). All four self-source pairs remain separately reported. NON_SUPPORT requires qualified sources and \(M\) upper bound <=0 at both steps. All other cases are INSUFFICIENT/HETEROGENEOUS, with numerical failures INELIGIBLE. Report point values even when a gate fails. This is an exploratory conditional rule, not a calibrated universal discovery test.

Secondary diagnostics: source improvement and every cross-domain full-update effect; source gradient inner products and first-order predicted loss changes; removed/retained update norms and restoration factors; per-record native attention-output change; full-update SAE coefficient/support change; common-top1 removal consequences; control-set matching discrepancies. They explain limits and cannot rescue the primary gate.

## G. Stage, failure and artifact contract

1. Static portrait from existing cache; outputs two central figure families, raw profile arrays, concentration statistics and selection manifest. This stage is descriptive, not the intervention result.
2. Local implementation smoke on a separate small subset/output directory: identity, finite scalars, analytic projection/reset, native/full-replay equality, no-op repeat, nonzero real effect and unchanged checkpoint/buffers. Known-good zero delta must reproduce baseline; nonzero delta must alter \(a\) consistently with \(\delta c\). A fixed Top-32 count must not be interpreted as new sparsity evidence.
3. Submit one four-H100 Reserved job through the envelope resolver. Four source workers must report distinct physical devices and durable progress. Each repeats identity and numerical checks. Any failure writes a receipt and prevents a COMPLETE claim. Timeout terminates this experiment's workers. Do not alter unrelated jobs.
4. Aggregate only after all four complete receipts and all 176 branches are present. Write Summary, Chinese Summary, Detailed, figures and manifests; incomplete work remains explicitly NOT RUN/MISSING/INELIGIBLE by condition.

Execution root: `/data/250010109/MoE_Router/experiments/20260926_atom_mechanism`. Scripts, caches, worker results and logs stay there. Dated reading copies: `daily_research_reports/0926/figures/atom_usage_portrait.*`, `atom_contribution_concentration.*`, plus one intervention figure if complete. `detailed.md` owns source hashes, conformance, failures and job receipts. This Protocol owns only registration; observed values go into result records.

## Freeze ledger

The scientific body is frozen before the first intervention readout; static cached activation inspection preceded design and is acknowledged. `registration.json` records body/config/selection/code hashes at execution. Changes after that point require an append-only amendment with evidence impact. No human-confirmed result or scientific state transition is inferred from execution completion.

### Amendment A1: scalar-buffer fingerprint compatibility

Before any model readout, the first frozen engineering smoke failed while hashing a scalar integer activity buffer: PyTorch requires flattening a zero-dimensional tensor before a byte view. Change only `tensor_sha` from `value.view(uint8)` to `value.reshape(-1).view(uint8)`. No data, direction, update, metric or criterion changes. Preserve the failed smoke and the original registration. A new engineering attempt uses a separate output directory; the latest registration links its predecessor and updated code hash. Scientific eligibility is unchanged because no scientific branch ran.

### Amendment A2: verify the actual attention projection shape

The next startup check rejected a hard-coded 1024x1024 assertion. Direct checkpoint metadata inspection established `blocks.7.attn.o.weight` is FP32, shape1024x2048: attention context width differs from hidden-state width. Section D's originally recorded shape1024x1024 is incorrect and is superseded by1024x2048. Correct only that assertion; the actual checkpoint, matrix identity, Frobenius-normalized update formula and projection computation are unchanged and already shape-generic. No forward readout or scientific branch ran before this failure. Preserve both failed engineering attempts and record A2 in the registration lineage.
