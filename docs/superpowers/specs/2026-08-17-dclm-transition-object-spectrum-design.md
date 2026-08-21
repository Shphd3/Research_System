# DCLM Transition-Object Spectrum Comparison Design

## Purpose

This audit asks whether covariance-spectrum conclusions change when the measured Transformer object or RMSNorm placement changes. It is a geometry audit, not a functional-information or Router experiment.

## Frozen data and model

- Frozen model: `/data/share/Qwen3-8B`, 36 blocks, hidden width 4,096.
- Data: the first 2,048 `uint32` token IDs from the first canonical DCLM training shard.
- Statistical rows: the same 2,048 token positions for every layer and object.
- One deterministic forward pass, no training, labels, tuning, or sample replacement.

## Frozen activation objects

For block $\ell$, let $h_\ell$ be the raw residual entering Attention, $a_\ell$ the raw Attention write after `o_proj`, $r_\ell=h_\ell+a_\ell$ the post-Attention residual before RMSNorm, $X_\ell=N_\ell(h_\ell)$, and $Z_\ell=N_\ell(r_\ell)$, where $N_\ell$ is that block's post-Attention RMSNorm.

The analysis covers:

1. adjacent raw Attention-write difference $a_{\ell+1}-a_\ell$;
2. adjacent pre-Attention raw-residual difference $h_{\ell+1}-h_\ell$;
3. adjacent normalized old-state difference $X_{\ell+1}-X_\ell$;
4. adjacent post-Attention raw-residual difference $r_{\ell+1}-r_\ell$;
5. adjacent actual-MLP-input difference $Z_{\ell+1}-Z_\ell$;
6. same-layer exact normalized update $U_\ell=Z_\ell-X_\ell$;
7. raw post-Attention residual state $r_\ell$;
8. actual normalized MLP-input state $Z_\ell$ as the RMSNorm companion.

Adjacent differences have 35 curves; same-layer objects have 36 curves.

## Spectrum computation

For every token-by-hidden matrix $M\in\mathbb R^{2048\times4096}$, subtract its token mean and compute the sample-space Gram covariance $G=MM^\top/2047$. Sort its eigenvalues descending, clip only negative numerical roundoff to zero, and normalize them as $p_j=\lambda_j/\sum_k\lambda_k$. Centering makes the exact rank at most 2,047; plots retain the 2,048-rank x-axis and floor zero shares at $10^{-12}$ only for log display.

Every individual figure uses rank 1--2,048, log y-axis $[10^{-12},1]$, the same layer colormap, and identical coordinates. One 2x4 grid shows all objects, and one aggregate plot overlays the layer-median spectrum for every object. Tables report covariance trace, $r_{80}$, and effective rank.

## Interpretation boundary

The audit may establish that spectral shape and apparent rank are sensitive to hook and normalization definitions in this model and DCLM slice. It cannot identify new information, semantic function, native feature use, intrinsic population rank, or Router utility.

