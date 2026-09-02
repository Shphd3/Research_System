# A15_13: Can Frozen Final-Layer Semantics Organize an Effective Middle Representation Through a Growing Expert Tree?

Thinking Card source: [15_13_semantic_supervision_middle_layer_formation_thinking_card_cn.md](15_13_semantic_supervision_middle_layer_formation_thinking_card_cn.md)

## 1. Problem Definition

The decision question is whether semantic labels formed at the answer-prefix state of a frozen third Transformer layer can supervise a newly added coarse-to-fine Router--expert tree after the second layer so that its effective representation is more robustly aligned with the true two-level semantics than a matched next-token-only hierarchy and a matched flat expert system. The true labels provide an upper bound; frozen third-layer pseudo-labels test whether the model can supply the supervision itself. A registered ablation asks whether removing the learned coarse discriminant direction from only the fine Router input improves within-parent fine routing.

The original second-layer state $h_2$ and every original model parameter remain frozen. The object being changed is the effective state $h_{2,\mathrm{eff}}$ produced by added residual experts. Pass therefore supports organization by a newly added module, not formation inside the original Block 2 parameters. Fail stops interpretation of the coarse-removal and pseudo-label mechanisms for this realization. Insufficient means the teacher, pseudo-label entrance, fairness, completion, replication, or language-function guards do not support a verdict.

## 2. Physical Priors

The human-confirmed prior is that child categories inside one parent share a parent property even when the children are mutually far apart. A staged system may first learn the parent partition, freeze that path, and then learn a local child partition under each parent. This does not require coarse semantics to occupy the largest-variance direction.

The learned binary coarse-Router discriminant is an operational proxy for one already used coarse direction. Removing it from the fine Router input tests whether that direction interferes with the local child decision. It is not assumed to be the complete parent-common subspace, and experts retain the complete $h_2$ input.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts that, with the same frozen teacher, architecture, initialization, data order, optimizer, and stage budget, correct coarse and fine Router supervision improves the true parent-conditioned fine-label low-tail margin of $h_{2,\mathrm{eff}}$ over the identical hierarchy trained only by next-token prediction. The strongest rival is generic adaptation: the topology, additional capacity, or continued language training causes any improvement without semantic supervision.

Dependent predictions are tested only after the primary link. Coarse-direction removal should outperform full-state fine routing if the learned coarse direction is an active interference term. Parallel parent and leaf residual experts should be no worse than sequential expert input if the two paths supply additive conditional corrections. Third-layer pseudo-labels can support the intended mechanism only if their truth-free partition is stable and non-collapsed, aligns with truth above permutation-random reference after freezing, and reproduces the Oracle direction.

## 4. Mathematical Model

For one answer-prefix position, let $h_2\in\mathbb R^d$ and $h_3\in\mathbb R^d$ be the frozen second- and third-layer states. A coarse Router predicts

$$
p_c(c\mid h_2)=\operatorname{softmax}(G_c(h_2)).
$$

After coarse training, define $w_C=W_c[1]-W_c[0]$ from the two rows of the linear Router and

$$
P_C=\frac{w_Cw_C^\top}{\lVert w_C\rVert_2^2},
\qquad r_2=(I-P_C)h_2.
$$

The main fine Router reads $r_2$ and predicts $p_f(f\mid c,h_2)=\operatorname{softmax}(G_f^{(c)}(r_2))$. The forward pass uses $\arg\max$ to select one predicted parent $c^*$ and one predicted child $f^*$, but scales each selected residual by its Router probability. The parallel effective state is

$$
h_{2,\mathrm{eff}}=h_2+p_c(c^*\mid h_2)E_{c^*}(h_2)
+p_c(c^*\mid h_2)p_f(f^*\mid c^*,h_2)E_{c^*,f^*}(h_2).
$$

Every sequence uses token-mean next-token cross entropy $L_{\mathrm{NTP}}$. Unsupervised routing optimizes only $L_{\mathrm{NTP}}$. Oracle and pseudo-label coarse or fine stages optimize

$$
L=L_{\mathrm{NTP}}+\lambda_{\mathrm{route}}L_{\mathrm{route}},
$$

where $L_{\mathrm{route}}$ is cross entropy on the active coarse or parent-conditional fine Router. In fine training, the supervised parent $q_c$ chooses the fine Router entering cross entropy, $L_{\mathrm{fine}}=\operatorname{CE}(G_f^{(q_c)}(r_2),q_f)$, while predicted $(c^*,f^*)$ still determines the language-model expert path. No expert classifier, prototype, margin, contrastive, reconstruction, or load-balancing term is permitted. Experts receive gradients only from the language loss of samples selecting them.

## 5. Computational Realization

The controlled language generator uses four affine rules over $\mathbb Z_{11}$: $u+1$, $u+3$, $-u+3$, and $-u+1$. Each complete causal sequence contains three demonstrations and one query. The generator records parent $c$, within-parent child $f$, leaf $2c+f$, semantic group, and surface template, but no semantic label is rendered. Training and held-out splits use disjoint semantic keys; out-of-distribution evaluation withholds complete surface-template combinations.

One three-layer causal Transformer first trains jointly with full-sequence next-token prediction only. Its embeddings, all three blocks, normalization, and tied language head then freeze. Pseudo-label construction receives only normalized frozen answer-prefix $h_3$ and group identifiers; truth is forbidden until a nested parent-then-child partition, centers, and assignments are durable. Stage two adds either a matched flat system or a coarse-to-fine hierarchy after Block 2. Flat next-token-only, Flat-Oracle, and Flat-Pseudo share one architecture and initialization family. The hierarchy trains the coarse Router and parent experts, freezes that path and its projection, then trains parent-conditional fine Routers and four leaf experts. The main expert computation is parallel; a sequential-input variant and a joint-coarse variant are registered ablations.

Training, development, and confirmation roles are separated. Training examples fit the teacher, added modules, and pseudo-label centers. Development data freeze the one shared probe regularization choice. Test truth is opened only after all final-step checkpoints and analysis rules are frozen.

## 6. Minimal Falsification Tests

The decisive comparison is Oracle-supervised hierarchy minus the architecture-identical next-token-only hierarchy on TEST-OOD. The primary metric is the worse of the two parent-specific fifth-percentile normalized binary margins for true fine labels, measured from $h_{2,\mathrm{eff}}$ by one shared L2-logistic readout. Its unit is normalized signed distance; higher is better. It measures difficult-tail linear accessibility and cannot prove native Router use or expert utility.

Pass requires both seed effects above zero, a positive pooled one-sided 95% paired group-bootstrap lower bound, and all language guards. Fail requires both seed effects non-positive or a non-positive pooled upper bound with all guards valid. Other mixed directions are Insufficient. Only after Pass are full-state versus residual fine routing, parallel versus sequential expert input, hierarchy versus flat topology, pseudo-label entrance, and pseudo-label downstream effects interpreted in that order.

## 7. Current Evidence

The meeting record establishes the motivating algorithm: split a manageable representation, freeze or preserve the explained coarse path, then recompute a local split inside each expert's conditional distribution; it also asks for a simple, fully interpretable first case. The later technical alignment proposes using frozen final-layer labels to supervise newly added earlier experts and directly comparing true with model-generated labels.

Historical E02-R showed that the repaired tiny-model task can be learned, but its per-expert semantic classification heads did not produce a replicated Oracle gain and its discovered labels were unstable or chance-aligned. Historical E03 on Qwen3-0.6B and CLINC150 found a near tie between learned hierarchy and flat routing. These results leave the broad prior unresolved and identify objective-to-architecture coupling as the live operational uncertainty. E04 removes per-expert label heads and isolates Router-only supervision; it is approved but not yet run.

## 8. Claim Boundary And Next Decision

The strongest allowed positive claim is that, in this controlled frozen-teacher language task, correct or admissible third-layer labels improve the true coarse--fine geometry of a newly added effective second-layer representation through a named dynamic Router--expert tree, without registered language degradation. It cannot establish that original Block 2 parameters changed, the removed direction is all coarse information, clustering discovers open-domain semantics, routing choices cause expert utility, experts specialize functionally, or the result transfers to larger natural-language models.

Exactly one next decision follows E04: decide whether the Oracle-supervised hierarchy reproducibly beats the identical next-token-only hierarchy. Completion requires both paired seeds, all registered conditions and ablations, fixed-final checkpoints, retained representation artifacts, the primary figure, and a bounded Pass, Fail, or Insufficient result. Only a Pass opens interpretation of coarse removal and pseudo-label supervision.
