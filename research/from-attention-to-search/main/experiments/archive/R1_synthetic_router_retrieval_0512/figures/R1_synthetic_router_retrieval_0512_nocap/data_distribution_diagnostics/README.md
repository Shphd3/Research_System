# Data Distribution Diagnostics

Checks whether the synthetic NTP data has Zipf-like latent features and hierarchical spectral structure.

Key reading:

- Atom activations are long-tailed: Zipf fit alpha 0.70, R2 0.81.
- NTP token labels are heavy-tailed: Zipf fit alpha 1.88, R2 0.74.
- Paths are intentionally balanced, not Zipfian: normalized entropy 1.000.
- Hidden states have broad spectrum: effective rank 43.9 / 64.
- Path hierarchy is weak in PCA/mean geometry: path between-trace ratio 0.000065.

Interpretation:

The hierarchy exists in sparse atom co-activation metadata, not as clean path-separated clusters in raw $h_t$ PCA space. This is compatible with R1's weak-support conclusion: router ranking has signal, but bucket semantics are mixed.
