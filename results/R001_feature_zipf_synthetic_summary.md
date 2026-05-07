# R001 Feature-Zipf Synthetic Summary

Source:

- `daily_research_reports/0507/feature_zipf_synthetic_brief_report_0505.md`
- `experiments/E001_feature_zipf_synthetic.md`

## Stable Results

1. Feature-Zipf synthetic data is a better controlled setting than direct leaf-Zipf data because Zipf acts on sparse feature occurrence.
2. Oracle models show the constructed mechanism is recoverable.
3. Learned models beat random on loss and show weak feature selectivity.
4. Hierarchical MoE has a function-recovery signal, especially in variable-A.
5. Flat middle spectral routing is currently the strongest learned signal for sparse feature division.

## Safest Claim

Hierarchical MoE recovers part of the hierarchical computation mechanism on feature-Zipf synthetic data, especially at the function level. It has not yet shown a clear advantage over flat middle spectral MoE for sparse feature division.

## Main Limitation

The current evidence separates recoverability from learned routing success. Oracle proves the mechanism can be recovered, but learned hierarchical routing still falls far below oracle and does not dominate flat middle spectral routing.

## Next Diagnostic Need

Separate feature-level and function-level specialization with metrics and architecture controls, then explain why middle spectral routing is strong.
