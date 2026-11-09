# How researchers group SAE features

Focused literature survey, 5 September 2026

The question is whether features extracted by a sparse autoencoder can be organized into groups that could later guide expert routing. The literature offers concrete algorithms for this. It does not offer one established algorithm that universally recovers semantic groups, nor do the studies below establish that their groups are suitable for growing an MoE during training.

The most useful starting comparison is between three ways of finding relationships: features that activate together, broad features that accompany narrower ones, and features that remain related after accounting for the activity of other features. The sections below explain the algorithms used for each. Matryoshka SAEs offer a complementary way to preserve broad and specific features during feature learning itself.

## What exactly gets clustered?

An SAE learns a dictionary of feature directions and a sparse list of activation strengths for each input. Keeping only a few features active does not automatically organize the dictionary into clusters. TopK SAE training is an established approach to controlling how many features participate in each reconstruction; it is a feature-learning method rather than a separate clustering algorithm. [Gao et al., 2024](https://arxiv.org/abs/2406.04093)

There are two different grouping problems. We can group **examples**, such as documents with similar feature activations. Or we can group **features**, such as several features associated with mathematical reasoning. This survey concerns the second problem. Clustering examples can subsequently help evaluate routing, but it should not be confused with discovering feature groups.

Each feature has two useful descriptions: its decoder direction, which describes what it contributes to reconstruction, and its activation history, which records where it appears. Geometry-based methods compare directions. Activity-based methods compare activation histories. These need not produce the same groups.

## 1. Coactivation followed by spectral clustering

**Paper:** Li et al., *The Geometry of Concepts: Sparse Autoencoder Feature Structure* (2024 preprint). [Methods, Section 4](https://arxiv.org/html/2410.19750v1)

The authors record feature activity within 256-token blocks from 50,000 documents, using a Gemma-2-2B layer-12 SAE with roughly 16,000 features. They calculate pairwise associations using several measures, including Jaccard similarity and the Phi coefficient. Jaccard measures shared activation relative to activation of either feature; Phi is correlation between binary activation indicators.

They then apply **spectral clustering**: use the association matrix to construct a lower-dimensional representation of the feature relationships and partition that representation into groups. They also cluster decoder directions using cosine similarity and compare the two partitions.

The study finds broad groups associated with code/math and different kinds of prose. Phi gave the strongest correspondence with geometric grouping in their comparison; this was not a test of which metric produces the best expert routing.

**Use for this project:** a direct baseline for discovering broad feature groups. Its block-level counting can connect related features that occur at different tokens. The number of groups and the context window remain design choices. A partition at several resolutions is not automatically a consistent hierarchy.

## 2. Broad-to-specific feature families

**Paper:** O’Neill et al., *Disentangling Dense Embeddings with Sparse Autoencoders* (2024). [Methods, Section 4.2](https://arxiv.org/html/2408.00657v1)

This study trains SAEs on scientific-abstract embeddings. It counts feature co-occurrences and divides each row by that feature’s frequency, producing directional conditional-activation scores. It thresholds the relationships, builds a **maximum spanning tree**—a cycle-free selection of strong connections—and orients edges from more frequent to less frequent features. Traversing the resulting directed structure produces parent–child families.

The reported construction first filters features using automated interpretability scores. Those scores are additional information used by the published procedure, even though the feature activations themselves are learned without topic labels.

**Use for this project:** the closest reviewed method to the proposed “broad field, then specialty” organization. However, frequent does not necessarily mean semantically broad, and a tree restricts multiple-parent composition. The evidence comes from document embeddings, not a growing token-level MoE. The attached router document’s conditional coactivation tests are related in spirit, but its thresholds and transitive reduction are not the same algorithm.

## 3. Correlation graphs and connected components

**Paper:** Deng et al., *Sparse Feature Coactivation Reveals Causal Semantic Modules in Large Language Models* (2025 submission; April 2026 revision, listed as ACL 2026). [Methods, Section 2](https://arxiv.org/html/2506.18141v3)

For each prompt, the authors select strongly active features and compare their activation traces across token positions. They connect features in adjacent layers when Pearson correlation exceeds 0.9, remove features with corpus activation density above 1%, and extract **weakly connected components**: groups connected by paths after ignoring edge direction.

They test groups by suppressing or amplifying their activations and measuring changes in model predictions. Results on controlled concept–relation tasks provide evidence beyond visual cluster coherence.

**Use for this project:** a reference for testing whether a candidate group matters to behavior. This is a prompt-specific, cross-layer method, not a global clustering algorithm for the one SAE proposed near the final block. Its top-feature selection and thresholds should not be treated as universal defaults. Graph edges are statistical relationships; the intervention experiments supply the behavioral evidence.

## 4. Conditional relationships followed by community detection

**Paper:** Bhalla et al., *Do Sparse Autoencoders Capture Concept Manifolds?* (April 2026 preprint). [Paper](https://arxiv.org/html/2604.28119v1)

A concept may vary continuously—for example, temperature—while different SAE features respond to different ranges. Features belonging to the same concept can therefore alternate rather than activate together. The paper finds that SAEs can distribute continuous structure across many features instead of capturing it with one compact group.

The proposed method fits an **Ising model**, a statistical model of binary activity that estimates pairwise relationships while accounting for other observed features. It uses positive and negative relationship magnitudes as graph weights. Louvain community detection groups features with strong connections within groups relative to a graph baseline. The paper checks recovered groups using PCA, which measures how much variation a few directions explain.

**Use for this project:** an advanced candidate for groups missed by positive coactivation. Conditional association is not proof of causality, and absolute negative relationships can also reflect competition unrelated to a shared concept. This recent preprint motivates a comparison, not a universal replacement for simpler methods.

The [authors’ released repository](https://github.com/goodfire-ai/sae-manifold) implements decoder cosine, coactivation, correlation, mutual information, and inverse-Ising relationships, with Leiden or spectral clustering. The paper’s Louvain description and repository’s Leiden/spectral options should be distinguished when reproducing results.

## 5. Learn several levels of abstraction together

**Paper:** Bussmann et al., *Learning Multi-Level Features with Matryoshka Sparse Autoencoders* (ICML 2025). [Paper and proceedings](https://proceedings.mlr.press/v267/bussmann25a.html)

Matryoshka SAEs train nested dictionaries. A small dictionary must reconstruct inputs on its own; larger dictionaries add further features and must also reconstruct them. This creates pressure to retain useful broad features while adding more specific ones. The authors report improved results on several interpretability-related tasks, with a reconstruction tradeoff.

**Use for this project:** a feature-learning alternative worth comparing if broad features disappear as the dictionary grows. It is not a post-hoc clustering algorithm, does not itself return a semantic parent–child graph, and does not show that the underlying language model learns broad concepts before specific ones over training time. Dictionary size, network depth, and training time are different axes.

## 6. The older connection: topographic organization

**Paper:** Hyvärinen, Hoyer, and Inki, *Topographic Independent Component Analysis* (2001). [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/11440596/)

This work starts from the observation that learned components can retain dependencies even when the learning method aims for independence. It uses those dependencies to organize components topographically: related components receive neighboring positions in an organized representation.

**Use for this project:** a historical precedent for organizing learned features by their statistical relationships. It is a different model family, rather than evidence that ordinary SAE training has always included a standard semantic clustering stage. It also illustrates the distinction between encouraging organization while learning features and discovering organization afterward.

## What I would compare first

These are proposed research choices, not reported experimental results for this project.

| Question | First method | Comparison that matters |
|---|---|---|
| Are there recurring broad groups? | Block-level Phi association plus spectral clustering | Token-level associations and decoder-cosine groups |
| Are some groups broad-to-specific families? | Conditional activation and directed feature-family construction | A non-tree graph that preserves multiple parents |
| Do related features alternate rather than coactivate? | Ising relationships plus community detection | Positive-association graphs on the same examples |
| Are broad features being lost during SAE learning? | Matryoshka SAE | A standard SAE with comparable reconstruction and activation budgets |

For the first diagnostic, freeze one model checkpoint and one SAE. Discover groups using one document split, then test whether their relationships persist in another. Compare against shuffled activation records and repeat the clustering to separate data structure from algorithmic instability. This is cheaper and easier to interpret than immediately growing and training experts.

If groups recur on held-out data beyond the shuffled comparison, retain them as candidate structure. If they disappear, revise the grouping scale or relationship measure before adding experts. If they recur but reflect punctuation, formatting, or document source rather than the desired distinctions, revise what the method is detecting. Semantic names should be interpretations of activating examples, not evidence by themselves.

## What changes in our current idea

My earlier explanation that “features belong together when they switch on together” was a useful baseline but incomplete. The literature distinguishes at least three relationships: features that participate together, alternatives that describe different values of one concept, and broad features that contain narrower cases. They call for different measurements.

The next research question is therefore: **which relationship identifies groups that deserve shared expert capacity?** A statistical cluster, a semantic family, and a group that benefits from the same learning updates are not automatically identical. The papers reviewed supply ways to discover and test candidate groups; the link to growing experts remains the project’s hypothesis.

For training-time tracking, keep a fixed reference set and compare activation behavior across checkpoints. Refit SAEs can split, merge, or reorder features independently of changes in the language model. A cluster appearing in a later SAE is not sufficient evidence that the model has just learned a new concept.

This is a focused survey of directly relevant primary methods, not an exhaustive review. No model training, clustering experiment, or code reproduction was run for this survey.
