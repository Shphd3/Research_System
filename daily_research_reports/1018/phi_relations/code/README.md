# Reproduction order

The scripts use the exact absolute execution owners recorded in the protocol. They read existing caches; none trains or forwards a model.

1. extract.py performs the one-time cache extraction and refuses to overwrite panel.npz. Do not rerun extraction over a completed owner.
2. analyze.py computes conditional estimates, full-count core decomposition and true-decoder contribution moments from the saved panel/counts.
3. qualify.py checks estimator identities with constructed inputs. chain_text.py retrieves the frozen full-cache chain examples.
4. validate_results.py checks frozen protocol digests, numerical identities and all 57 text/activation cases.
5. plot.py draws from saved result tables. build_report.py creates the selected reading copy. finalize.py verifies reading assets and builds manifests.

The reused tokenizer-only FrozenDecoder source and its digest are recorded under provenance/reused_text_decoder.json. Raw caches, checkpoint weights and fonts are not bundled. environment.json records the actual CPU package versions. The saved conditional sufficient statistics and panel.npz remain at the execution owner; there were no new eigendecompositions of the historical raw-hidden spectra.
