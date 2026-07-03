---
anchor_id: A06_16_synthetic_to_realistic_proxy_bridge
parent_node: rq.feature_specialization.initialization_geometry
status: result_updated
created: 2026-06-23
canonical_language: en
---

# A06_16 Synthetic-To-Realistic Proxy Bridge Anchor

## 0. Thinking Card
父问题：真实数据上要形成 feature-level expert specialization，必须知道 label-free proxy 初始化到底在哪一步失效。
当前子问题：不能直接控制 attention 后 hidden state 的 $\beta/\lambda$；我们只能控制输入序列中的 feature slot、slot 位置和 nuisance cue，再测量 slot 末端 hidden state 中的有效强度。
当前判断：A06_16 修正了旧结论。旧 C0 失败来自 learned absolute positional embedding 与离散 slot start 的位置几何；same-model no-pos full run 后 C0-C3 的 residual k-means discovery 和 training preservation 全通过，C4 all-position 仍是 7/8 通过。
关键证据：canonical rerun `pt-vcl6tl57` 中 C0-C3 step-0 pseudo `feature_NMI=1.0`、final `feature_NMI=1.0`、final load imbalance=0、mapping change=0/128；C4 all-position pseudo NMI 均值 0.871。
最危险边界：不测试 RoPE；C4 仍有 1/8 失败；主跑使用 feature-specific slot-end token，不能证明 whole-slot compositional semantics；也不能推出 real-DCLM preservation。
下一步决策：不要在这个 no-pos controlled bridge 里继续把 preservation 当主断点；下一步应选择 C4 all-position robustness、RoPE/position encoding、whole-slot composition 或 real-DCLM preservation 中的一个边界。

Question: In a full no-learned-absolute-position synthetic bridge with movable heterogeneous feature slots, does the first failed contract occur in label-free proxy discovery or in training-time preservation?
Physical prior: stable input feature cues can create measurable residual feature centers after attention, but learned absolute positional geometry can itself become a nuisance axis, and training can erase routing margin after discovery.
Core model: the directly controlled variables are input sequence knobs; the measured hidden-state decomposition is $r_i=h_i-\bar h\approx \beta_{\mathrm{eff}}\mu_{f_i}+\lambda_{\mathrm{eff}}n_{z_i}+\epsilon_i$.
Model term being tested: how measured $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ and clustering scope affect discovery and preservation.
Primary metric: `first_failed_stage`, computed from oracle reachability, pseudo step-0 NMI, nuisance NMI, NMI drop, load, margin, and accuracy guards.
Falsifier: no-pos pseudo discovery fails in C0-C3 despite oracle reachability, C4 all-position remains uniformly low after GPU k-means, or measured $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ does not move with the input knobs.
Can claim: in the corrected no-pos full bridge, label-free residual k-means discovers the feature centers in C0-C3, same-model training preserves them, and C4 all-position discovery mostly works.
Cannot claim: RoPE behavior, robust all-position discovery under all position encodings, whole-slot composition, real-DCLM specialization, expert utility, or deployable routing.
Next decision: choose the next boundary branch: C4 all-position robustness, RoPE/position encoding, whole-slot composition, or real-DCLM preservation.

## 1. Problem Definition

Parent problem: real-data gating initialization needs a proxy partition that can be found from hidden states, implemented by the router, and preserved through training.

Sharper subproblem: A06_08/A06_09 succeeded in clean synthetic route-position training, while A06_12/A06_13 showed that real DCLM proxy routing is overwritten by ordinary training. A06_16 asks where the bridge from clean input features to more realistic input mixtures first breaks.

Decision question: under no-learned-absolute-position controlled input degradation, is the first failed contract label-free discovery or training preservation?

Not in scope: hand-constructed hidden states as the main evidence, real-text semantic claims, utility binding, utility-aware initialization, or a deployable anti-collapse method.

## 2. Physical Priors

P1: Stable input feature cues can become residual feature centers after attention.
Meaning: if a feature cue is consistently tied to the routed position, the post-attention hidden state should contain a measurable feature-conditioned residual direction.
Could be wrong if: oracle centroids cannot recover feature routing even when the input feature cue is clean.

P2: Nuisance cues can compete with the feature center in hidden space.
Meaning: decoy tokens, position patterns, or irrelevant context may create residual directions that clustering prefers over the intended feature.
Could be wrong if: increasing nuisance in the input does not increase measured nuisance alignment or reduce feature-to-nuisance separation.

P3: Preservation depends on routing margin after discovery.
Meaning: even if pseudo centers recover the feature at step 0, training can move router rows or hidden states enough to erase the initial assignment.
Could be wrong if: high step-0 NMI and margin collapse for reasons not visible in router/hidden replay diagnostics.

## 3. Falsifiable Hypotheses

H1: Discovery is the first bottleneck.
Supported if: oracle centroids still route the feature, measured feature signal remains present, but label-free pseudo centers fail step-0 feature NMI or become nuisance-aligned.
Weakened if: pseudo centers keep high step-0 feature NMI across the bridge conditions.

H2: Preservation is the first bottleneck.
Supported if: pseudo centers pass step-0 feature NMI, but training causes large NMI drop while target accuracy remains acceptable.
Weakened if: pseudo init preserves feature NMI, load, and margin through training.
Current status: weakened in the same-model no-pos rerun because C0-C3 preserve `feature_NMI=1.0` through 1600 steps.

H3: Route-position specificity is a necessary boundary.
Supported if: route-position clustering succeeds while all-position clustering fails or becomes nuisance-aligned.
Weakened if: all-position clustering recovers the same feature partition with similar held-out NMI and low nuisance alignment.
Current status: weakened in the no-pos GPU-kmeans run because C4 passes in 7/8 seeds.

## 4. Mathematical Model

Directly controlled object: input sequence $x_i$ with a length-4 feature slot, feature label $f_i$, nuisance cue $z_i$, slot start $s_i$, and routed position $p_i^\star=s_i+3$ at the last token of the slot.

Observed hidden state after attention:
$$
h_i = T_\theta(x_i, p^\star),\qquad r_i=h_i-\bar h.
$$

Effective hidden-state decomposition:
$$
r_i \approx \beta_{\mathrm{eff}}\mu_{f_i}+\lambda_{\mathrm{eff}}n_{z_i}+\epsilon_i.
$$

The experiment does not set $\beta_{\mathrm{eff}}$ or $\lambda_{\mathrm{eff}}$ directly. It changes input knobs and estimates these quantities from hidden states:
$$
\hat\mu_f=\mathbb{E}[r_i\mid f_i=f],\qquad
\hat n_z=\mathbb{E}[r_i-\hat\mu_{f_i}\mid z_i=z].
$$

Operational strength estimates:
$$
\beta_{\mathrm{eff}}=\operatorname{mean}_f\|\hat\mu_f\|,\qquad
\lambda_{\mathrm{eff}}=\operatorname{mean}_z\|\hat n_z\|.
$$

Pseudo-center initialization:
$$
\{\hat c_k\}_{k=1}^{K}=\operatorname{Cluster}(\{r_i:i\in C\}),\qquad
w_e(0)=\alpha\frac{\hat c_e}{\|\hat c_e\|}.
$$

Training trajectory:
$$
a_i(t)=\arg\max_e w_e(t)^\top h_i(t),\qquad S_t=NMI(f_i,a_i(t)).
$$

Mechanism relation: as input nuisance increases or feature cues weaken, the measured ratio $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ should fall. The first stage whose contract breaks determines whether the next anchor should target discovery or preservation.

## 5. Computational Realization

- Input family: A06_08/A06_09 one-layer Transformer + top-1 MoE route-position task, with slot length fixed at 4 and routing at the slot's last position.
- Direct knobs: heterogeneous feature-slot pattern, slot start position, feature cue strength, nuisance cue strength, nuisance type, and clustering scope; hidden-state strengths are measured, not assigned.
- Feature cue examples: feature-specific 4-token slot templates or feature-specific token sets sampled inside the slot; the slot tokens need not all be identical. The current main run uses a feature-specific slot-end token to keep oracle reachability valid, so last-token-only shortcuts remain a claim boundary.
- Nuisance cue examples: decoy token, irrelevant context token, or position/context pattern that is independent of the target feature.
- Uniformity guard: feature id, nuisance id, and slot start are sampled from a strict balanced Cartesian product.
- Conditions: clean feature-only input, mild nuisance input, moderate nuisance input, weak feature plus nuisance input, route-position clustering, all-position clustering, oracle centroid, random/equal-norm random, and label-shuffled guard.
- Stage readout: first evaluate oracle reachability and measured hidden geometry; then label-free step-0 routing; train only cells whose discovery stage passes.
- Expected artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/stage_contract_table.csv`, `tables/effective_geometry_table.csv`, `figures/bridge_first_failed_stage.png`, and `figures/nmi_trajectory_by_bridge_cell.png`.

## 6. Minimal Falsification Tests

Test 1: input-to-hidden geometry audit.
Question: do input knobs actually change measured feature and nuisance strength in post-attention hidden states?
Primary read: $\beta_{\mathrm{eff}}$, $\lambda_{\mathrm{eff}}$, feature separability, and nuisance separability.
Insufficient if: the measured hidden geometry does not move with the intended input knobs.

Test 2: stage contract discovery.
Question: does label-free clustering recover the operational feature under each bridge condition?
Primary read: held-out step-0 feature NMI relative to oracle, with load and nuisance NMI guards.
Supports discovery: pseudo NMI remains close to oracle and above random/global controls.
Weakens discovery: oracle works but pseudo NMI falls or becomes nuisance-aligned.

Test 3: stage contract preservation.
Question: if discovery passes, does training preserve the discovered partition?
Primary read: NMI trajectory and final NMI drop, with target accuracy as a constraint.
Supports preservation: high step-0 NMI remains high after training.
Weakens preservation: high step-0 NMI collapses while accuracy remains acceptable.

Test 4: route-position boundary.
Question: is the current discovery method dependent on a known routed position?
Primary read: route-position clustering versus all-position clustering, both evaluated on held-out route-position samples.
Supports the boundary: route-position succeeds and all-position fails or aligns with nuisance.
Weakens the boundary: all-position recovers the same feature partition.

## 7. Current Evidence

- A06_06: oracle feature centroids can implement the synthetic feature partition at step 0.
- A06_07: global centering/projection/whitening mainly improve load, not feature NMI.
- A06_08: route-position residual k-means recovers synthetic pseudo-feature centers with held-out `feature_NMI=1.0` in the clean setting.
- A06_09: the A06_08 pseudo init is preserved during the current synthetic route-position target training.
- A06_10/A06_11: real DCLM proxy clusters are measurable and raw-center rows can initialize strong raw-input proxy routing.
- A06_12/A06_13: ordinary real DCLM training does not preserve proxy routing; the first failed real-data contract is training feedback override.
- A06_14/A06_15: utility binding and utility-aware initialization are parked until preservation is restored.
- A06_16: the original pos-on run `pt-an9ktx73` exposed a positional-geometry confound: learned absolute `pos_emb` plus discrete slot starts made residual k-means cluster by position. The first no-pos full run `pt-7oabnyza` showed discovery success but had a cross-model preservation confound. Per user instruction, old problematic results were deleted and same-model full rerun `pt-vcl6tl57` became canonical: C0-C3 pass discovery and preservation across 8/8 seeds; C4 all-position discovery passes 7/8 seeds.

## 8. Claim Boundary And Next Decision

Can claim: in the corrected no-pos slot-end bridge, route-position label-free residual k-means can discover the feature centers in C0-C3, same-model target training preserves that partition through 1600 steps, and all-position GPU k-means mostly recovers the same feature partition in C4. The old discovery failure was a learned absolute positional-geometry artifact.

Cannot claim: direct control of attention hidden states, RoPE behavior, robust all-position discovery under all position encodings, real-language semantic feature discovery, whole-slot compositional semantics, DCLM preservation, expert utility, deployable gating, or that a preservation intervention solves real-data training behavior.

Next decision:
- Choose one next boundary branch: C4 all-position robustness, RoPE/position encoding, whole-slot composition, or real-DCLM preservation.
- Treat utility binding as parked until the real-data preservation branch is restored.
