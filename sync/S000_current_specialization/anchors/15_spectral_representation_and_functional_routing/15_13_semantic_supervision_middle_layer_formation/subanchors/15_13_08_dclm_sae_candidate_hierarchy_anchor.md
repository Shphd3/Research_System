# A15_13_08: Does the Qualified Final-Layer SAE Admit a Reproducible Candidate Containment Hierarchy?

## 1. Problem Definition

The parent problem is to construct an unsupervised coarse--fine semantic teacher whose layerwise readability can later nominate Router and LoRA insertion layers. E16 established only that the final-layer DCLM sparse autoencoder (SAE) is technically qualified. The blocking uncertainty is whether its sparse feature activations admit a nontrivial hierarchy under the senior project's activation-containment construction. The present decision is limited to reproducing that graph form; exact historical node counts are explicitly out of scope.

## 2. Physical Priors

The human-confirmed prior is that a more specific SAE feature may reuse several broader features. If so, the specific feature should almost always co-activate with its constituents, while each constituent should also activate without the specific feature. A frequency-only or corpus-local coincidence can produce the same relation on one sample, so frozen relations must be checked on a disjoint DCLM source.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts at least one multi-step directed acyclic candidate hierarchy, with some discovery relations retaining their direction on the disjoint replication source. The strongest rival predicts a flat, cyclic, empty, or replication-unstable graph caused by firing frequency and sample-specific co-activation. A nontrivial graph weakens only the flat-or-empty rival; it does not establish semantic composition.

## 4. Mathematical Model

For token $t$, let $A_f(t)=1$ when SAE feature $f$ has positive Top-32 activation. A candidate composite $C$ points to constituent $U$ when $P(A_U=1\mid A_C=1)$ is high, the reverse conditional probability is lower, and $U$ fires more often than $C$. For a candidate with constituent set $\mathcal U(C)$, graph depth is

$$
d(C)=1+\max_{U\in\mathcal U(C)}d(U),
$$

with $d(U)=0$ for terminal nodes. This depth is an activation-relation depth, not a semantic granularity label.

## 5. Computational Realization

The frozen Qwen3-0.6B-Base final-layer MLP input is encoded by the completed 30,000-feature ReLU Top-32 SAE. Discovery activations come from the frozen DCLM training view and replication activations from the separately stored DCLM validation file. Candidate constituents are limited to the 4,096 most frequent discovery features. Relations are selected only from discovery activations, frozen, and then evaluated without reselection on replication activations. Two figures use the same layered layout as the historical PDF: all discovery candidates and the replication-qualified subgraph.

## 6. Minimal Falsification Tests

The decisive artifact test requires a valid sparse cache, an acyclic graph, maximum discovery depth of at least two, and at least one relation passing the frozen replication rule. A flat or empty acyclic graph is a valid negative result. A nontrivial discovery graph with no replicated relation is replication-unstable. Missing identities, incomplete caches, cycles, or absent figures are insufficient evidence. Exact agreement with the historical 1,047-node graph is never required.

## 7. Current Evidence

E16 consumed 1,000,001,536 DCLM tokens and produced a reload-exact, non-collapsed SAE with final held-out normalized reconstruction error 0.053382. E17 then completed the method-and-visual-form reproduction on independent DCLM discovery and replication sources. The discovery graph contains 1,212 groups, 2,616 edges, 1,279 nodes, and maximum depth two. Twenty-four frozen groups, 91 edges, and 53 nodes pass every replication gate, retaining maximum depth two; the registered verdict is `NONTRIVIAL_REPLICATED`. The historical six-level visual depth was not reproduced. The strict joint-gain gate is the principal contraction: 96.62% of candidates retain minimum one-sided containment, but only 1.98% pass joint gain and the full replication contract.

## 8. Claim Boundary And Next Decision

The positive E17 result supports only that this SAE contains a small, reproducible, nontrivial candidate activation-containment graph. Its shallow, hub-dominated structure cannot establish semantic parent--child relations, coarse or fine labels, causal composition, Router utility, expert utility, or task gain. The one next decision is whether to approve a separately frozen M2D2 semantic qualification of the 24 replicated groups and 53 retained nodes using coarse-label concentration, parent-conditioned fine-label concentration, and frequency/coverage-matched controls.
