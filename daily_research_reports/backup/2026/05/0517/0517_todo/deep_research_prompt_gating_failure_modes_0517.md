# Deep Research Prompt: MoE Gating Failure Modes, Training Dynamics, and Expert Specialization

## Role

You are a research collaborator helping audit a MoE / gating project. Your job is not to write a broad survey. Your job is to identify what the literature says about **why gating fails or does not produce clean expert specialization**, and map those mechanisms onto a controlled synthetic experiment.

## Project Context

We study expert specialization in sparse Mixture-of-Experts language models.

Current controlled setting:

```text
Task: next-token prediction on synthetic trigram corpus
Features / motifs:
  ABC: [1,2] -> 22
  DEF: [3,4] -> 23
  GHI: [6,7] -> 20
  JKL: [8,9] -> 21
Model: small Transformer + top-1 linear MoE FFN router
Question: do different feature representations get routed to different experts?
```

Current empirical status:

```text
E2.0:
- MoE reads back planted trigram features.
- shuffled unigram control cannot read back these features.
- P(expert | feature) is above random routing.
- dominant expert ablation damages readback.
- but there is no strict one-feature-one-expert mapping.

E2.1:
- feature identity remains visible in router input hidden space.
- router input centroids are separable; Fisher ratio is high.
- router boundary directions weakly align with feature-difference directions.
- router entropy is close to log(num_experts), margins are weak.
- multiple experts can support the same feature prediction under forced routing.

E2.2:
- reducing expert capacity does not force cleaner feature-aligned routing.
- increasing feature count to 16 does not force one-feature-one-expert.
- readback remains high while dominant expert ablation effect weakens.
```

Current working claim:

```text
representation separability != router specialization
```

Claim boundary:

```text
This is a controlled toy trigram NTP result. Do not claim it proves real LLM semantic specialization or failure.
```

## Research Goal

Find and synthesize the strongest existing views on:

1. MoE gating failure modes.
2. Router training dynamics.
3. Expert specialization vs expert redundancy.
4. The relationship between hidden-state geometry, token identity, frequency, load balancing, and routing.
5. Whether common/shared experts plus routed/specialized experts are motivated by common-dominated features.
6. Whether NTP loss alone should be expected to produce feature-aligned expert partition.

## Key Questions

### A. What is the router optimizing?

- Does the literature model router training as choosing experts that reduce downstream loss, not as clustering semantic features?
- How do gradients flow through top-k / top-1 routing?
- What happens when multiple experts can solve the same input?
- Does early routing history create expert co-adaptation / lock-in?

### B. Why might feature-separable hidden states fail to yield feature-specialized experts?

Investigate these candidate mechanisms:

```text
1. token ID shortcut
2. prefix-end token shortcut
3. target-token shortcut
4. hidden norm / activation scale routing
5. confidence / CE difficulty routing
6. low-variance but loss-relevant routing directions
7. load-balancing interference
8. expert redundancy / utility degeneracy
9. shared residual/attention/LM-head bypass
10. early routing history / expert co-adaptation
11. capacity constraints / token drop / batch dependence
12. common-feature domination
```

For each mechanism, answer:

```text
- What is the mechanism?
- Which papers support or contradict it?
- What empirical signature would distinguish it?
- How would we test it in our synthetic trigram setup?
- Would it imply an architecture change, an objective change, or only a measurement correction?
```

### C. What does “expert specialization” mean in the literature?

Separate at least four notions:

```text
routing specialization: tokens/features go to different experts
functional specialization: expert output causally contributes to different predictions
semantic/domain specialization: human-interpretable domain or concept alignment
systems specialization: load/latency/throughput benefits from sparse activation
```

Do not treat these as equivalent.

### D. What are known failure modes of load balancing?

Study:

- expert collapse;
- under-trained experts;
- over-specialized experts;
- load-balancing loss interfering with task loss;
- uniform-load objective conflicting with naturally Zipfian data;
- token dropping / capacity factor issues;
- loss-free balancing and expert-choice alternatives.

### E. What is the role of token frequency and Zipfian data?

Focus on the following distinction:

```text
token frequency Zipf != semantic feature frequency Zipf != syntactic construction frequency Zipf
```

Find whether existing MoE analyses show routing by:

- token identity;
- token frequency;
- syntactic class;
- domain;
- hidden-state similarity;
- task difficulty.

### F. What architecture ideas directly respond to common-dominated features?

Look for evidence around:

- shared experts + routed experts;
- common/unique feature decomposition;
- hierarchical MoE;
- expert-choice routing;
- similarity-preserving routing;
- cosine/geometric routing;
- supervised or contrastive router objectives;
- router entropy/margin control;
- auxiliary-loss-free balancing;
- top-2 routing / expert sharing.

For each idea, decide whether it addresses:

```text
common feature domination
router shortcut
expert redundancy
load imbalance
under-trained tail experts
reverse-index usefulness
```

## Required Sources

Start from primary sources, not blogs. Include at least:

1. Classic MoE / local experts:
   - Jacobs, Jordan, Nowlan, Hinton: Adaptive Mixtures of Local Experts.
2. Sparse MoE:
   - Shazeer et al., Sparsely-Gated Mixture-of-Experts.
   - GShard.
   - Switch Transformer.
   - ST-MoE.
3. Routing alternatives:
   - BASE Layers.
   - Expert Choice Routing.
   - auxiliary-loss-free / loss-free balancing.
   - expert threshold routing if relevant.
4. Expert specialization architectures:
   - DeepSeekMoE.
   - shared expert / routed expert designs.
   - OLMoE or comparable open MoE analyses if useful.
5. Routing analysis / interpretability:
   - OpenMoE routing analysis.
   - papers on token-ID routing, context-independent specialization, early routing learning.
   - recent papers arguing specialization reflects hidden-state geometry rather than human domain expertise.
   - recent counterarguments showing causal expert control or geometric routing if credible.

Use newer papers only if they are technically relevant and clearly separate speculation from evidence.

## Output Format

Produce the following sections.

### 1. One-sentence answer

State the strongest current literature-consistent explanation of our E2 result.

### 2. Taxonomy of gating failure modes

Markdown table:

| Failure mode | Mechanism | Literature evidence | Synthetic test | Expected signature | Architecture implication |
|---|---|---|---|---|---|

### 3. Training dynamics model

Explain how router and experts co-adapt over training. Include:

```text
initialization -> early routing bias -> expert utility gap -> gradient starvation / co-adaptation -> stable but non-feature-aligned routing
```

Identify where our current E2 evidence fits.

### 4. Specialization definitions

Clarify routing / functional / semantic / systems specialization and which papers use which meaning.

### 5. Relation to Zipf/common-specialized design

Answer:

```text
Does Zipfian frequency imply common experts?
Does it imply hierarchical MoE?
What must be measured before claiming that?
```

### 6. Direct implications for our next experiment

Prioritize the next 5 diagnostics. Each diagnostic must include:

```text
hypothesis
measurement
possible result
claim update
```

### 7. Claim audit

Use labels:

```text
supported / weakly supported / unsupported / contradicted / unclear
```

Audit these claims:

1. Feature representations can be separable without router specialization.
2. NTP loss does not necessarily require feature-aligned routing.
3. Token ID / frequency shortcuts can dominate routing.
4. Load balancing can conflict with natural feature distribution.
5. Common experts are justified by common-dominated representations.
6. H-MoE is necessary for real-language specialization.
7. MoE router buckets can serve as a KV reverse index.

### 8. 30-second advisor version

Give a concise explanation suitable for a group meeting.

## Strict Boundaries

Do not claim:

- real LLM experts are semantic specialists unless causally demonstrated;
- token frequency Zipf proves semantic feature Zipf;
- routing purity proves expert functionality;
- synthetic trigram behavior transfers to real LLMs;
- H-MoE is necessary before showing ordinary MoE failure modes;
- reverse index works before testing attention/KV retrieval recall.

## Search Queries To Use

Use variations of these queries:

```text
MoE router training dynamics expert specialization failure mode
Mixture of Experts token ID routing context independent specialization
OpenMoE routing decisions token IDs early routing learning
Switch Transformer load balancing router z-loss training instability
Expert Choice Routing under trained experts over specialized load imbalance
DeepSeekMoE shared experts common knowledge routed experts specialization
BASE Layers balanced assignment sparse expert routing
load balancing loss interferes with MoE specialization
expert redundancy Mixture of Experts forced routing utility
hidden state geometry explains expert specialization MoE
MoE routing frequency syntax gradient expert specialization
common routed experts Zipfian feature distribution MoE
```

## Final Deliverable Requirement

The final answer must be useful for designing experiments, not just a reading list. For every cited viewpoint, connect it to one of our synthetic diagnostics:

```text
E3.0 router behavior decomposition
E3.1 forced-routing utility matrix
E3.2 counterfactual shortcut test
E3.3 training dynamics trace
E3.4 shared-path bypass diagnostic
```
