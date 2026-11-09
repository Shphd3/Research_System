# Protocol: A12_02_01_E01 Task-Rank Competition

## 0. Approval Snapshot

Approved under the user's planned-anchor instruction. Root-cause audit on oracle factors. Compare ranks 1 and 2 under NTP versus static MTP for five seeds. Primary metric is the rank-conditioned standard-loss gap. Pass: `gap_rank1 > 0.5`, `abs(gap_rank2) < 0.05`, and rank-1 MTP improves future MSE in 5/5. Cannot claim Transformer or language capacity.

## 1. Setup

Independent \(u,z\sim N(0,1)\); shared linear encoder \(h=W[u,z]\); separate linear standard-local, standard-future, and auxiliary-future readouts. \(L_N=2\operatorname{MSE}(u)+\operatorname{MSE}(z)\); \(L_{MTP}=L_N+2\operatorname{MSE}_{aux}(z)\). AdamW, 1000 steps, batch 256, identical data streams and seeds `971--975`.

## 2. Decision

Rank intervention is the only changed structural variable. Report per-seed and aggregate losses, encoder singular values, and effective rank. Failure weakens the low-rank competition model rather than MTP generally.
