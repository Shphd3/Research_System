派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/literature_methods.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/literature_methods.md)；研究修改仍回到原件。

---

# Methods note: Towards Monosemanticity and sentence-local feature relations

Status: design and asset-feasibility work only; H1 and H2 are `NOT RUN`.
Source: Bricken et al. (Anthropic, 2023), *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning*. The researcher identified this paper. Official section anchors below were checked against the source HTML on 2026-10-28.

## What the paper contributes

The paper's [“Finite State Automata” section](https://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-fsa) describes feature assemblies connected through predicted tokens, including self-loops and alternating features. These are distinguished from ordinary internal circuits.

Its [sensitivity example](https://transformer-circuits.pub/2023/monosemantic-features/index.html#feature-arabic-sensitivity) shows related features covering different tokens. [Feature splitting](https://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-feature-splitting) concerns changes across dictionary sizes; splitting and merging need not form a tree. [Activation intervals](https://transformer-circuits.pub/2023/monosemantic-features/index.html#global-analysis-interp-intervals) can differ in interpretability. The paper also separates [data correlations from model properties](https://transformer-circuits.pub/2023/monosemantic-features/index.html#global-analysis-about-model).

## Our adaptation to this round

The following are analysis choices for this question, not procedures claimed to have been validated by that paper.

1. **Use the self-loop/alternation distinction as motivation for H1/H2.** H1 measures reuse of the same native feature coordinate at a later token. H2 measures association through the independently existing graph when the earlier coordinate no longer appears. Preserve graph cycles and bidirectional edges; neither token order nor node degree supplies a semantic hierarchy.
2. **Distinguish observed sequences from a token-mediated functional explanation.** With cached activations we can observe the pattern `feature at i → token at j → feature at j` only as a sequence of measurements. We do not measure whether the first feature changes the token probability or causes the later feature. No output intervention or fresh functional experiment is added here.
3. **Read the entire sentence before assigning meaning.** Show every token in selected mathematical and biological sentences. Pair the displayed feature IDs with their activation values, token IDs, position and omitted-feature count. Use both supportive examples and a counterexample. A label such as “mathematical context” remains an interpretation unless existing independent evidence supports it.
4. **Keep activity strength separate from binary persistence.** Apply the native activation rule and predeclared frequency strata for the primary statistics. Use cached strengths to read the heatmap; do not choose a new threshold because a low-activation case looks less interpretable. CrossCoder shared latent activity is not separate activity at each layer.
5. **Make background controls carry the statistical claim.** Same-domain, different-document matching and margin-preserving randomization address this round's rivals. Degree-aware checks are required for graph coverage. These controls are our design; the paper does not supply their specific matching rules, thresholds, or significance justification.

## What this does not establish

Even a positive result would support sentence-local coordinate persistence or old-graph association under the registered controls. It would not establish information preservation, a causal feature circuit, semantic abstraction, or a hierarchy. Dictionary-size feature splitting must not be relabeled as within-sentence feature replacement. The original paper motivates patterns worth looking for; it does not validate the identity or meaning of our cached features or old graph.

## Brief comparison: Cunningham et al. (2023)

*Sparse Autoencoders Find Highly Interpretable Features in Language Models* asks whether sparse dictionaries yield interpretable and behaviorally useful units. Its [Section 3](https://arxiv.org/html/2309.08600v2#S3) generates descriptions from activating text and tests predictions on other text. [Section 4](https://arxiv.org/html/2309.08600v2#S4) uses counterfactual feature patching for indirect object identification. [Section 5.3](https://arxiv.org/html/2309.08600v2#S5.SS3) builds a feature relation example using upstream-feature ablations and downstream-activation changes. Those arrows have intervention-based meaning. For our round, the useful distinction is between interpreting activation patterns and testing a functional relation; the latter remains outside this cache-only scope.
