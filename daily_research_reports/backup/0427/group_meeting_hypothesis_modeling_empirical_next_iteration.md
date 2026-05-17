# Group Meeting Brief: From Mentor Intuition to a Testable Research Program

## 0. One-Sentence Position

The current project should not be presented as “Zipfian distribution directly implies hierarchical MoE.”

A defensible version is:

> Language-model hidden states appear to contain low-dimensional shared structure plus tail-oriented functional components. If those components can be exposed as sparse or subspace-localized features, then modular experts can be trained on more disentangled inputs, potentially improving continual learning by localizing updates and reducing interference.

---

## 1. Mentor Intuition, Cleaned Up

### Original intuition

The corpus follows a Zipfian token distribution. Therefore, language components may have different frequencies. If experts can be arranged hierarchically, high-frequency and low-frequency components may be processed at different levels. With enough experts, the representation may become more disentangled, broader, and more open.

### What must be corrected

The following inference is too strong:

$$
\text{Zipfian token frequency} \Rightarrow \text{hierarchical MoE should work}
$$

The corrected mechanism chain should be:

$$
\text{token/domain distribution is long-tailed}
$$

$$
\Downarrow
$$

$$
\text{hidden states may contain shared low-rank structure and tail-oriented functional components}
$$

$$
\Downarrow
$$

$$
\text{these components may be represented by sparse or localized features}
$$

$$
\Downarrow
$$

$$
\text{experts trained on those features may specialize functionally}
$$

$$
\Downarrow
$$

$$
\text{localized expert updates may reduce old/new interference in continual learning}
$$

Only the last two arrows justify MoE or hierarchical routing.

---

## 2. Strict Critique of My Current Idea

### Problem 1: “Semantic atoms” is not yet a scientific object

Saying “semantics are low-rank combinations of atoms” is not enough.

It mixes at least four different claims:

1. hidden states lie near a low-dimensional manifold;
2. features are sparse in some dictionary;
3. features are semantically meaningful;
4. features are useful for next-token prediction and continual learning.

These are not equivalent.

The immediate correction is:

> Do not try to prove that semantic atoms are real. First define an operational feature and ask whether it predicts domain, token frequency, expert advantage, or forgetting.

---

### Problem 2: Sparse dictionary features are not automatically “true features”

Sparse dictionary learning can produce sparse bases, but sparse bases are not necessarily identifiable as the true semantic basis.

A sparse basis may rotate, mix, or recombine underlying common/unique components while still satisfying the reconstruction and sparsity objective.

Therefore, observing sparse activation is not enough.

A dictionary feature must pass functional tests:

1. Does it activate non-uniformly across domains?
2. Does it activate non-uniformly across token-frequency buckets?
3. Does ablating it change next-token loss?
4. Does routing or expert assignment based on it reduce loss?
5. Does updating experts tied to it reduce forgetting?

---

### Problem 3: “More experts” does not imply “cleaner decomposition”

The claim

$$
\text{more experts} \Rightarrow \text{more disentangled representation}
$$

is false without extra conditions.

More experts can also mean:

1. noisy routing;
2. expert collapse;
3. duplicated experts;
4. data fragmentation;
5. worse optimization;
6. higher apparent specialization but no NTP gain.

Correct version:

> More experts are justified only if there is evidence that the input space contains multiple functionally distinct feature groups, and routing can select experts that reduce token-level NTP loss better than counterfactual experts.

---

### Problem 4: Zipfian token frequency is not the same as feature frequency

We must separate:

| Term | Meaning | How to measure |
|---|---|---|
| token frequency | how often a token appears in the corpus | count tokens |
| feature activation frequency | how often a learned feature fires | activation probability |
| variance band | PCA/SVD energy rank of hidden directions | eigenspectrum |
| gradient update frequency | how often a direction/parameter receives update | gradient statistics |

The safe hypothesis is not:

$$
\text{rare tokens} = \text{tail subspace}
$$

The safe hypothesis is:

> Some feature groups or subspaces may correlate with token frequency, domain identity, or old/new gradient interference. This must be measured, not assumed.

---

### Problem 5: Continual learning link is still underdefined

The mentor intuition talks about decomposition, but CL needs one more step:

> Which decomposition reduces which interference during which adaptation stage?

The old-stage vs direct-adaptation distinction is crucial.

If we care about catastrophic forgetting of a learned module, the protocol should include an old-stage state before new-domain adaptation.

---

## 3. Clean Hypotheses

### H0: Shared-head plus tail-oriented functional components

A pretrained LM hidden state contains a low-rank shared component and additional tail-oriented components.

A simple model is:

$$
x = \mu + V_c z_c + r_t
$$

where:

- $x$ is a hidden state;
- $\mu$ is the mean hidden vector;
- $V_c z_c$ is the shared high-variance component;
- $r_t$ is the residual after removing the shared head.

This does not yet prove semantic atoms. It only defines a geometry.

---

### H1: Sparse feature hypothesis

There exists a dictionary $D$ and sparse code $a$ such that:

$$
r_t \approx Da
$$

with sparse activation:

$$
\|a\|_0 \ll m
$$

or, for a continuous relaxation:

$$
\|a\|_1 \text{ is small.}
$$

But the key claim is not merely reconstruction. The key claim is functional:

> Some sparse features are non-uniform across domains, token-frequency buckets, and next-token prediction loss contribution.

---

### H2: Feature frequency and domain specificity

For feature $j$, define activation frequency:

$$
p_j = \mathbb{P}(|a_j|>\tau)
$$

Define domain-conditional activation:

$$
p_{j,d}=\mathbb{P}(|a_j|>\tau \mid d)
$$

A useful feature should show one of the following:

1. high common activation across domains;
2. domain-specific activation;
3. token-frequency-bucket-specific activation;
4. functional loss contribution.

Domain specificity can be measured using entropy:

$$
H_j = -\sum_d q_{j,d}\log q_{j,d}
$$

where:

$$
q_{j,d}=\frac{p_{j,d}}{\sum_{d'}p_{j,d'}}
$$

Lower $H_j$ means more domain-specific activation.

---

### H3: Expert specialization from sparse/tail-oriented input

Experts should not merely receive more parameters. They should receive inputs that expose distinct functional components.

For a routed model:

$$
h_{\text{out}} = h + E_c(x) + \sum_i g_i(z_r)E_i(z_e)
$$

where:

- $E_c$ is the common branch;
- $E_i$ are experts;
- $g_i$ is the router;
- $z_r$ is router input;
- $z_e$ is expert input.

Candidate expert inputs:

1. raw hidden $x$;
2. PCA tail residual $x_t$;
3. `u50_ext` variance-band input;
4. sparse dictionary code $a$;
5. reconstructed sparse residual $Da$;
6. domain-specific sparse feature subset $D_{S_d}a_{S_d}$.

Expert specialization must be measured by counterfactual NTP loss, not just routing entropy.

For selected expert $e^\star(t)$:

$$
G_{\text{second}}(t)=\ell_{\text{second-best}}(t)-\ell_{e^\star(t)}(t)
$$

Positive $G_{\text{second}}$ means the selected expert is actually better.

---

### H4: Continual-learning isolation hypothesis

If expert inputs expose sparse/tail-oriented functional components, then updating only the relevant experts during new-domain adaptation should reduce old-domain forgetting.

Old-task forgetting:

$$
F_{\text{old}}=L_{\text{old}}^{\text{after new-stage}}-L_{\text{old}}^{\text{before new-stage}}
$$

New-task learning:

$$
G_{\text{new}}=L_{\text{new}}^{\text{before new-stage}}-L_{\text{new}}^{\text{after new-stage}}
$$

A structure is useful only if it lowers $F_{\text{old}}$ at matched or comparable $G_{\text{new}}$.

---

## 4. Current Empirical Evidence

### Evidence 1: Shared-head / tail-oriented geometry is plausible

Previous representation audits support the existence of shared high-variance structure and motivate common/tail splitting.

This supports the geometry part of the story, not the full hierarchical MoE claim.

---

### Evidence 2: Single-layer tail-conditioned block has had positive signals

Earlier Phase4/5/6 style experiments support the value of single-layer combined tail-conditioned routed blocks and suggest that expert-tail input is more reliable than router-only tail input.

This supports:

$$
\text{expert input matters}
$$

more strongly than:

$$
\text{router-only geometry is solved.}
$$

---

### Evidence 3: H3 direct-adaptation audit failed

The H3 causal audit showed that direct new-domain adaptation from a frozen pretrained backbone plus initial replacement block did not produce the expected CL object.

In that protocol:

- matched dense and raw two-branch improved old loss;
- real variance-band split did not beat dense, raw two-branch, or random split;
- `u50_ext` did not establish causal advantage.

This does not necessarily refute Phase8 old-stage results, because H3 and Phase8 measured different CL starting states.

---

### Evidence 4: Protocol mismatch is now the main issue

Phase8p* tested old-stage module forgetting.

H3 tested direct adaptation from an initial replacement block.

Therefore, the immediate empirical question is:

> Does the Phase8 old-stage signal survive H3-style controls?

This motivates the Phase8-H3 bridge experiment.

---

## 5. Quick Experimental Validation Plan for This Week

### Experiment A: Sparse Feature Audit

Purpose:

> Test whether dictionary / sparse-code features show non-uniform domain, token-frequency, and functional behavior.

Steps:

1. Collect hidden states at Qwen3-0.6B layer 8.
2. Use DCLM + WoS calibration data.
3. Compute centered hidden states and tail-oriented candidates.
4. Fit a sparse dictionary / SAE on:
   - raw hidden $x$;
   - centered hidden $x-\mu$;
   - full tail residual $x_t$;
   - `u50_ext`.
5. For each feature $j$, compute activation frequency:

$$
p_j = \mathbb{P}(|a_j|>\tau)
$$

6. Compute domain specificity entropy $H_j$.
7. Compute token-frequency-bucket activation profile.
8. Compute feature overlap between domains using Jaccard similarity.
9. Run feature ablation or reconstruction intervention and measure NTP loss change.

Minimal outputs:

- activation-frequency histogram;
- feature-domain heatmap;
- domain overlap matrix;
- token-frequency-bucket activation table;
- top features by NTP-loss contribution;
- comparison of PCA bands vs dictionary features.

Pass condition:

> Sparse features are not only sparse, but also show domain/token-frequency non-uniformity and measurable NTP-loss contribution.

Fail condition:

> Features are sparse but not functionally interpretable or not linked to NTP loss.

---

### Experiment B: Phase8-H3 Bridge Old-Stage Audit

Purpose:

> Align the CL protocol with Phase8 old-stage while adding H3-style controls.

Main groups:

1. matched dense;
2. wide dense if needed;
3. raw two-branch;
4. random split;
5. head16 split;
6. u50 split;
7. ext split;
8. u50_ext split;
9. full_tail_resid split;
10. dense replay.

Routing groups if non-routing split survives:

1. uniform expert mixture;
2. flat raw MoE;
3. router-raw / expert-tail;
4. router-tail / expert-tail;
5. oracle router upper bound.

Pass condition:

> `u50_ext` or another real split beats dense, raw two-branch, random split, and head16 under old-stage matched-learning forgetting.

Routing pass condition:

> routed model beats non-routing split and uniform expert mixture, and selected experts have positive counterfactual NTP gap.

---

## 6. What I Should Say in the Group Meeting

### 6.1 Problem

We want to understand whether a modular / MoE architecture can support faster adaptation with less forgetting.

The mentor intuition is that language has long-tail structure, and therefore different experts may need to process different frequency or semantic components.

But I do not want to jump directly from Zipfian tokens to hierarchical MoE. I am trying to insert a measurable mechanism:

$$
\text{long-tail data} \rightarrow \text{sparse/tail-oriented features} \rightarrow \text{expert specialization} \rightarrow \text{localized CL updates}
$$

---

### 6.2 Hypothesis

My current main hypothesis is:

> Hidden states contain shared low-rank structure plus tail-oriented sparse functional components. If experts receive inputs exposing those components, they can specialize in a way that is relevant to next-token prediction and possibly reduces forgetting under old-stage continual learning.

---

### 6.3 Modeling

I model hidden states as:

$$
x = \mu + V_cz_c + Da + \epsilon
$$

where:

- $V_cz_c$ is shared high-variance common structure;
- $Da$ is a sparse feature reconstruction;
- $a$ is sparse feature activation;
- $\epsilon$ is residual noise.

Experts are modeled as:

$$
h_{\text{out}} = h + E_c(x) + \sum_i g_i(z_r)E_i(z_e)
$$

The scientific question is which input $z_e$ and $z_r$ exposes useful functional components:

- raw hidden;
- PCA tail residual;
- `u50_ext`;
- dictionary sparse code;
- dictionary-reconstructed sparse residual.

---

### 6.4 Empirical Study So Far

1. We have evidence for shared-head / tail-oriented geometry.
2. Earlier Phase8-style old-stage experiments had weak positive CL signals for `u50_ext`.
3. H3 direct-adaptation causal audit failed: dense and raw two-branch were stronger, and `u50_ext` did not beat random split.
4. The key interpretation is protocol mismatch: Phase8 old-stage measures forgetting from a learned old-task state, whereas H3 direct adaptation often improves old loss rather than causing forgetting.

---

### 6.5 Next Iteration

I will do two fast validations:

1. **Sparse feature audit**: check whether dictionary features are domain-specific, token-frequency-specific, and NTP-functional.
2. **Phase8-H3 bridge**: rerun the old-stage CL protocol but add H3 controls: random split, raw two-branch, head16, full_tail_resid, and matched dense.

This directly answers:

> Is the earlier `u50_ext` signal a real variance-band / feature-specific effect, or only an artifact of protocol, projection, or parameter budget?

---

## 7. Slides / Talking Structure

### Slide 1: Motivation

- Goal: fast adaptation with less forgetting.
- Dense updates are global and may interfere with old knowledge.
- MoE may help only if experts receive functionally disentangled inputs.

### Slide 2: Mentor intuition and correction

- Original: Zipfian token distribution motivates hierarchical experts.
- Correction: Zipfian alone is not enough.
- Need mechanism: long-tail data → sparse/tail features → expert specialization → localized updates.

### Slide 3: Mathematical model

$$
x = \mu + V_cz_c + Da + \epsilon
$$

$$
h_{\text{out}} = h + E_c(x) + \sum_i g_i(z_r)E_i(z_e)
$$

### Slide 4: Existing evidence

- Shared-head / tail-oriented geometry exists.
- Tail-conditioned block had positive signals in earlier old-stage experiments.
- H3 causal audit failed under direct-adaptation protocol.

### Slide 5: Key contradiction

Phase8 and H3 use different CL starting points.

- Phase8: old-stage module → new adaptation → forgetting.
- H3: initial replacement block → new adaptation → old loss often improves.

Therefore, the next experiment should align the protocol.

### Slide 6: Next experiment

Phase8-H3 bridge:

- keep old-stage;
- add H3 controls;
- test dense / raw / random / head / u50 / ext / u50_ext / full_tail;
- then test routing only if split survives.

### Slide 7: Sparse dictionary quick audit

- Fit sparse dictionary / SAE on layer-8 hidden states.
- Measure activation frequency, domain specificity, token-frequency profile, and NTP-loss contribution.
- Use this to decide whether sparse features are useful expert inputs.

### Slide 8: Decision gates

- If `u50_ext` fails against random under old-stage: revise variance-band hypothesis.
- If sparse features are non-functional: dictionary line pauses.
- If routed experts have positive counterfactual NTP gap: continue router alignment.
- If oracle routing beats learned routing: router objective is bottleneck.

---

## 8. Final Short Version for Verbal Presentation

I am trying to turn the mentor intuition into a measurable mechanism. I do not think Zipfian token frequency alone justifies hierarchical MoE. The safer hypothesis is that hidden states contain shared low-rank structure plus sparse or tail-oriented functional components, and experts may specialize only if their inputs expose those components.

The current problem is that our earlier Phase8 results and the newer H3 audit used different CL protocols. Phase8 had an old-stage adapted module before new-domain adaptation, while H3 started directly from an initial replacement block. This likely explains why Phase8 saw forgetting-like behavior but H3 often saw old loss improve.

So my next step is not to directly add more experts. I will first run a Phase8-H3 bridge: keep the old-stage protocol but add H3-level controls such as raw two-branch, random split, head16, full_tail_resid, and matched dense. In parallel, I will run a quick sparse dictionary audit to see whether learned features are actually domain-specific, token-frequency-specific, and functional for next-token prediction. Only if these pass should we move toward finer experts or hierarchy.
