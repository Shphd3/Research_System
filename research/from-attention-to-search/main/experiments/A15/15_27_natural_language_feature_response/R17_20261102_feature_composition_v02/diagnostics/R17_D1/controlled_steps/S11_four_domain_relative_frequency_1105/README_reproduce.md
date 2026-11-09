# S11 reproduction and payload guide

This round uses 96 NEW category frame families (32 development / 64 confirmation), 4608 controlled prefixes, and 12000 NEW independent reference documents. Old S06/S08/S09/S10 outputs are historical inputs to design/audit only. No old activation is counted as new. No training, intervention or router work is performed.

## Read the result

- summary_cn.md: concise Chinese scientific reading and decisive raw values.
- summary.md: English canonical measurement record.
- protocol.md / protocol_cn.md: frozen definitions, denominators, uncertainty and reverse-result rules.
- detailed.md / detailed_cn.md: implementation, provenance, audit and complete statuses.
- casebook_cn.md: original texts, sampling indices, IDs, native activations, preactivations and reference counts.
- results/primary_contrasts.csv: all192 contrasts (24 per reference ×2references ×4wordings), with all opposite/ineligible cells.
- results/family_profiles.csv / *_feature_audit.csv: actual denominators, family variation, full unthresholded feature audit.
- figures/: white-background PNG, editable-text SVG and PDF. Code is in code/figures.py; source font is an existing external asset, not bundled.

## Model-free replay

From this directory, with NumPy and SciPy installed:

```sh
OPENBLAS_NUM_THREADS=2 python code/portable_replay.py
```

This replays all192 actual point estimates and effective-family denominators from sparse native z and development-fixed weights. It does not rerun a model or generate new confirmation data. The full audit code/verify.py additionally requires original external checkpoint/source paths and historical inputs; it is not the portable entrypoint.

## Original execution environment

Execution root is `/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105`.
The original model/SAE paths and byte hashes are in frozen_plan.json. Both encoders are native1024→30000/ReLU/Top32, independently trained dictionaries. Attention reads block27.self_attn.o_proj output; MLPIN reads block27.mlp actual prehook input. IDs are not aligned.

The producer was run with local dependencies:

```sh
PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3 \
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 \
python -u code/run_all.py
```

Do not rerun this command in the completed output directory: it refuses to overwrite completed stages/locks. Full inference requires the named original assets and a separate explicitly authorized fresh run. `code/prepare.py` also refuses overwrite and uses actual local Arrow and DCLM source files; it is provenance, not a request to resample.

Postprocessing uses analyze_results.py, controls_and_audit.py, figures.py and verify.py. Its initial hashes were fixed before confirmation. Engineering amendments, when any, preserve the prior bytes and response-exposure times. Reports do not change frozen raw outputs or scientific acceptance.

## Packet boundaries

The final packet omits model/SAE weights, full large reference texts, per-family native hidden/preactivation states, and the large eight-body-position activation files. `data/reference_views.jsonl` retains every selected ID, exact model token IDs, visible prefix, source metadata, complete-text digest and external source index. Primary colon sparse activations, controlled text/sparse activations, all scores, fixed weights, complete statistical tables, code and figures are retained subject to the stated final packet manifest. `large_files_index.json` reports exact omitted paths/bytes/SHA256; do not assume an indexed file is included.

Scientific boundary: reference frequency is corpus/position dependent; magnitude profiles are distinct from direction replication; shared occurrence is not shared function; this round is neither a full marginal-conditioned joint-structure test nor a routing-efficiency result.


## Recorded runtime continuation and SC1

The original development and question-reference stages ran atCPU4. A measured1.6517x long-prefix speedup,withzero native hook error on16fixedprefixes, justified using the pre-existing8CPU quota for general-reference and confirmation. Original frozen science/data bytes remain unchanged;runtime_amendment.json andamendments.md bindthe actual CPU8continuation source and the original overall10800-second clock. code/run_remaining_cpu8.py is the actual checkpoint-gated local continuation,not a general rerun entrypoint. Both4/8candidate full-vs-cached scoring calibrations are retained.

SC1 freezes96additional furniture prefixes before mainconfirmation,using some furniture to matcha fruit target index inall96frames. It reuses the main fixed weights/signs without selection,and runs32development then64confirmation cases. This adds96forwards,not96new independent families. Its position/phrase sensitivity is descriptive,doesnot replace any ofthe4608primary texts,and cannotrescue a primary failure. Actual outputs andscores are underdata/*position_supplement* andresults/position_supplement*.


## Final compact packet selection

Complete full-wording feature/family/scale/CDF/quartile detail tables remain in the execution directory and are indexed inlarge_files_index.json. The packet retains the COMPLETE2016profile summaries,192primary/control-wording contrasts,allprimary native colon sparse z,development weights,all4704controlled texts/scores,feature_primary_explicit.csv(allfeatures inall6main pairs),family_primary.csv(all192contrasts×64families plusmain explicit pairprofiles),membership_primary_explicit.csv,andfrequency_cdf_primary_explicit.csv. Full permutation traces and historical large auxiliary snapshots are external;indices/seeds and complete summaries remain.

All12000reference exact token-ID inputs and sampling IDs remain indata/reference_input_index.jsonl. Fullreference text and fullvisible-prefix text are external;data/reference_key_examples.jsonl contains32fixedfirst examples(8/source) with visible text. Do not claim thepacket containsall12000reference texts. Alloriginal fullreference text/prefix files are indexed with paths/bytes/SHA256.

For model-free figure reproduction on the packet,copyresults/frequency_cdf_primary_explicit.csv toresults/frequency_cdf.csv beforecallingcode/figures.py; this is an explicitly named primary subset,sufficient for its displayed curves. It is not the full2016-profile CDFtable. Portable192condition replay needs no such copy. PDF exports remain external;allPNGandeditableSVGfiles are retained.

Detailed reference-document vector metrics are also externally indexed; reference_vector_summary.csv retains complete per-corpus/site counts and mean/median/min/max for every recorded scale/reconstruction/cutoff field.
