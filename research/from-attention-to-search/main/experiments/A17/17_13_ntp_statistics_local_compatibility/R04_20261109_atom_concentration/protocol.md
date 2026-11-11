# R04 Protocol: atom-concentration regularizer (A6) and atom co-activation fixed dispatch (A5)

Canonical Chinese text: `protocol_cn.md` (this file is its reading copy). Frozen before training on 2026-11-09; λ is filled once by the smoke rule.

- Parent A17_13, continues R03. Execution root `/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/`.
- Resource: researcher restricted training to the share cluster (4×H100 Reserved `h100-4-reserved-16c256g`), replacing the prompt's "4×H100 reserve".

**Uncertainty.** In R03 the overall-NLL order of five arms matched the order of median $\bar M$. Rival: $\bar M$ is a by-product of learning well, or A1's deficit comes from token-level partitioning alone. Separating comparisons: A6 vs A0 (optimize concentration directly, router-only gradient) and A5 vs A1 (both fixed dispatch; atom partition vs token partition).

**Arms.** Teacher = 33B-token dense-order-aligned MoE, block7.norm2 output → SAE TopK32 (30000 atoms), online per micro-batch, bf16 following A1's record (DEV top-32 per-index agreement 0.9896, exact-set 0.7059). $w_j=\min(\log(1/p_j)/7.6513,3)$.
- A6: native routing + $\lambda\mathcal L_{\text{conc}}$, $\mathcal L_{\text{conc}}=\frac1L\sum_l\sum_{j\in\mathcal J}w_jH_3(q_j^{(l)})/\sum_{j\in\mathcal J}w_j$, $q$ from $\mathrm{softmax}(W_r\,\mathrm{sg}(h))$; gradient only to $W_r$, added after the DDP CE reduction and before clipping. λ = median CE-gradient norm / median conc-gradient norm over 50 λ=0 smoke steps × 8 layers.
- A5: spectral clustering (normalized Laplacian, 8 eigenvectors by lobpcg, k-means seed 2026110902) of the DEV co-activation graph $W_{jk}=\#\{t:j,k\in A_t\}/\sqrt{n_jn_k}$ (29999 atoms with $n_j\ge20$); 4964 boundary moves to bring group token mass to 0.80–1.05 of the mean. Score $s_{t,e}=\sum_{j\in G_e}w_jz_{t,j}$, Top2$(s+b)$, gates 0.5, shared by all 8 layers.

**Preregistered EVAL $\bar M$ median at b=0:** A1 0.6969, A5 1.3375.

**Diff vs A0:** routing mode; 250-step rolling full checkpoints (keep 2, deletion receipts) + final full milestone + bf16 weight snapshots every 250 steps; conc logging; λ=0 smoke asserts A0 loss identity (1e-6) for 50 steps. Everything else unchanged.

**Predictions:** P1 A6 median $\bar M$ > A0 at 2000 (more so in low bins). P2 A6 bin0–2 NLL < A0 and overall not worse by >0.01. P3 A5 $\bar M$ > A1 and NLL < A1. P4 forgetting concentrates in high flip-rate quartiles for learnable routers; fixed arms have χ≈0 and less forgetting. Differences below neighbouring-checkpoint fluctuation are "insufficient". Single seed, 2000 steps.
