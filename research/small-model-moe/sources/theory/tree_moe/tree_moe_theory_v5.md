# A tree-shaped mixture of experts versus a dense layer: theory with proofs

*Version 5. This version proves each claim from stated assumptions. It also corrects the capacity claim of version 4.*

## Summary

**What is compared.**

- A **dense layer**: one weight matrix of size $10{,}000 \times 10{,}000$.
- A **tree of experts**: 11 matrices, each $1{,}000 \times 1{,}000$, arranged as a tree. There is 1 root, then 2 subroots, then 8 leaves (4 under each subroot).

Both models learn from the same sentences. A perfect gate sends each sentence through 3 experts: the root, the right subroot and the right leaf. Training is plain gradient descent.

**What is proved** (sections 4 to 7, under assumptions A1 to A6):

1. **Theorem 1: the anisotropy note's capacity cannot tell the two models apart.** That capacity depends only on the list of feature strengths. Sorting the same features into experts does not change the list. So the tree, measured as one space, has the same capacity as a dense layer that holds the same features at right angles.

   **Correction.** Version 4 claimed about $6.4\times$ more capacity for the tree. That claim gave the dense layer and each expert separate power-law spectra. But both models see the same data, so their spectra are tied. Measured consistently, both come to about 189 in the worked example.

2. **Theorem 2: the tree changes who overlaps with whom, and evens out interference.** Assume features point in random directions, experts have equal widths, and each level is equally active. Then the tree gives every feature, common or rare, the same signal-to-interference ratio. The dense layer gives a leaf feature 8 times less than a root feature.

   In the tree, a leaf feature's ratio rises $2.4\times$, and a root feature's falls to $0.3\times$. So, under random placement, the tree moves signal-to-interference from common features to rare ones. It does not create more in total.

3. **Theorem 3: rare features learn at least 8 times faster per step.** This holds with large batches, plain gradient descent, and a separate step size for each expert. The factor is the product of the branching factors, $2 \times 4$, so it grows with every level of the tree.
4. **Theorem 4: compute per sentence.**

   - Per output number, a sentence uses $3{,}000$ weights instead of $10{,}000$, which is $3.3\times$ fewer.
   - For the whole layer, it uses $3\times 10^{6}$ weights instead of $10^{8}$, which is $33\times$ fewer.

   The extra factor of 10 comes from the tree's narrower output, $1{,}000$ numbers instead of $10{,}000$. Whether that narrower output loses anything has not been analyzed yet.

**Total compute to learn the long tail:**

- at least about $26\times$ less, which is $8\times$ from Theorem 3 times $3.3\times$ from Theorem 4;
- about $260\times$ less, if the narrower output turns out to lose nothing.

## 1. The question

A dense layer stores every feature in one shared space, so every feature overlaps a little with every other. A mixture of experts splits the layer into smaller matrices, and a gate sends each input to only some of them.

Our idea is to shape the experts like the tree of knowledge:

- general knowledge goes in the root;
- each subject, such as physics or math, gets a subroot;
- each subtopic, such as quantum mechanics or graph theory, gets a leaf.

We ask how this tree compares with a dense layer in three ways: capacity, how fast rare features are learned, and compute.

## 2. The two models

| | Dense | Tree of experts |
| --- | --- | --- |
| Shape | one matrix, $10{,}000 \times 10{,}000$ | 11 experts of $1{,}000 \times 1{,}000$ |
| Total weights | $10^{8}$ | $1.1 \times 10^{7}$ |
| Weights used per sentence | $10^{8}$ | $3 \times 10^{6}$ |
| Features that share a space with a leaf feature | all features | only features of the same leaf |

## 3. Setup and assumptions

**A1. Knowledge is a tree with 3 levels.** Each sentence follows one path: the root, one of 2 subroots, and one of 8 leaves. Every branch is equally likely. So expert $e$ is used by a fraction $\pi_e$ of the sentences:

$$\pi_{\text{root}} = 1, \qquad \pi_{\text{subroot}} = \tfrac{1}{2}, \qquad \pi_{\text{leaf}} = \tfrac{1}{8}.$$

**A2. Features.** Each feature $f$ belongs to exactly one expert, written $e(f)$. A few of the features are *label features*: SAE features that say which path a sentence takes. All the others are *detail features*.

When a sentence passes through expert $e$, that expert has $k$ active features out of its $n$, and each active feature's value has variance $s$. So feature $f$ appears with probability

$$p_f = \frac{k}{n}\,\pi_{e(f)},$$

and its variance, averaged over all sentences, is $p_f\, s$.

**A3. Each level is equally active.** Every level contributes $k$ active features to each sentence. So a sentence has $3k$ active features in total.

**A4. The gate is perfect.** It reads the label features and always picks the right path. Its cost is not counted.

**A5. Placement.** Write $W$ for the width of a space: $W = D = 10{,}000$ for the dense layer and $W = d = 1{,}000$ for an expert. Each feature $f$ has a unit direction $u_f \in \mathbb{R}^{W}$ in its space.

Theorem 1 holds for any placement. Theorem 2 assumes the directions are random and independent. That is the standard model for features packed into a space with more features than dimensions.

**A6. Training.** Training is plain gradient descent on squared error, with no momentum and no Adam. Each expert averages its gradient over the sentences routed to it, so each expert has its own step size.

## 4. Theorem 1: capacity

**Definition (from the anisotropy note).** For a space whose input covariance is $\Sigma$, the capacity is

$$C = \frac{(\operatorname{tr}\Sigma)^2}{\operatorname{tr}(\Sigma^2)}.$$

This equals $1/\mathcal{I}$, where $\mathcal{I}$ is the normalized squared overlap of two independent inputs. In words, $C$ is the effective number of dimensions the space uses.

**Lemma 1 (capacity of separate spaces side by side).** Treat the tree as one space made of its experts placed side by side. Its covariance is then block diagonal, $\Sigma = \bigoplus_e \Sigma_e$, with one block per expert. Write

$$T_e = \operatorname{tr}\Sigma_e \quad \text{(expert } e\text{'s signal)}, \qquad \tilde\pi_e = \frac{T_e}{\sum_{e'} T_{e'}} \quad \text{(its share of the total signal)},$$

and let $C_e$ be expert $e$'s own capacity. Then

$$C_{\text{tree}} = \frac{1}{\displaystyle\sum_e \tilde\pi_e^{2}/C_e} \;\le\; \sum_e C_e,$$

with equality only when each expert's share of the signal, $\tilde\pi_e$, is proportional to its capacity $C_e$.

*Proof.*

1. The blocks do not overlap, so
$$\operatorname{tr}\Sigma = \sum_e T_e, \qquad \operatorname{tr}(\Sigma^2) = \sum_e \operatorname{tr}(\Sigma_e^2) = \sum_e \frac{T_e^2}{C_e}.$$
2. Dividing,
$$C_{\text{tree}} = \frac{\left(\sum_e T_e\right)^2}{\sum_e T_e^2/C_e} = \frac{1}{\sum_e \tilde\pi_e^{2}/C_e}.$$
3. By the Cauchy–Schwarz inequality,
$$1 = \Big(\sum_e \tilde\pi_e\Big)^2 = \Big(\sum_e \frac{\tilde\pi_e}{\sqrt{C_e}}\,\sqrt{C_e}\Big)^2 \le \Big(\sum_e \frac{\tilde\pi_e^{2}}{C_e}\Big)\Big(\sum_e C_e\Big).$$
4. Equality holds when $\tilde\pi_e/\sqrt{C_e} \propto \sqrt{C_e}$, that is, when $\tilde\pi_e \propto C_e$. $\blacksquare$

**Theorem 1 (sorting features into experts does not change capacity).** Suppose the dense layer can place all features at right angles to each other. Then

$$C_{\text{dense}} = C_{\text{tree}}.$$

*Proof.* With the features at right angles, the eigenvalues of the dense covariance are exactly the feature variances $\{p_f\, s\}_f$. Inside each expert the features are also at right angles, so the block-diagonal tree covariance has the same eigenvalues. And $C$ depends only on the eigenvalues. $\blacksquare$

**What this means.** This capacity measures how many dimensions the data occupies. It says nothing about which features share a space, so it cannot detect what the tree does.

**Worked example, and the error in version 4.** Suppose each expert's own spectrum follows $1/i$ over its 1,000 dimensions. Then $C_e = 34$ for every expert. Each expert's signal is proportional to how often it is used, so the signal shares are $\tilde\pi_{\text{root}} = \tfrac13$, $\tilde\pi_{\text{subroot}} = \tfrac16$, and $\tilde\pi_{\text{leaf}} = \tfrac{1}{24}$.

| Quantity | Value |
| --- | ---: |
| One expert, $C_e$ | 34 |
| Plain sum $\sum_e C_e$ over 11 experts (version 4) | 375 |
| Tree as one space, Lemma 1 | 189 |
| Dense layer holding the same features at right angles, Theorem 1 | 189 |
| Unrelated $1/i$ spectrum over $10{,}000$ dimensions (version 4's comparison) | 58 |

Version 4 compared $375$ with $58$ and got $6.4$. Those two numbers cannot both describe the same data:

- the plain sum gives every expert full weight, but each leaf carries only $\tfrac{1}{24}$ of the signal;
- the dense layer's spectrum is not an unrelated $1/i$ law, because it is made of the experts' spectra put together.

Measured consistently, both models come to 189.

## 5. Theorem 2: who overlaps with whom

**Definition.** The **interference** on feature $f$ is the frequency-weighted squared leak of the other features in the same space onto $f$'s direction:

$$I_f = \sum_{g \ne f,\ \text{same space}} p_g\, s\, (u_f^{\top} u_g)^2.$$

It has two meanings at once:

- the crosstalk when $f$ is read along its own direction;
- the extra push $f$'s weights get from training steps on other sentences.

The **signal-to-interference ratio** is

$$\mathrm{SIR}_f = \frac{p_f\, s}{\mathbb{E}[I_f]}.$$

Write $A_{\text{space}} = \sum_{g \in \text{space}} p_g$ for the expected number of active features in a space.

**Lemma 2.** If the directions in a space of width $W$ are random and independent, then $\mathbb{E}\big[(u_f^{\top}u_g)^2\big] = 1/W$. So

$$\mathrm{SIR}_f = \frac{p_f\, W}{A_{\text{space}} - p_f} \;\approx\; \frac{p_f\, W}{A_{\text{space}}}.$$

*Proof.* Because $u_g$ is uniform on the sphere, $\mathbb{E}[u_g u_g^{\top}] = I/W$. So

$$\mathbb{E}\big[(u_f^{\top}u_g)^2\big] = u_f^{\top}\,\mathbb{E}[u_g u_g^{\top}]\,u_f = u_f^{\top}\frac{I}{W}u_f = \frac{1}{W}.$$

Summing over $g$ gives the result. As a numerical check, 1,000 random pairs gave $1.03\times10^{-3}$ for $W=1{,}000$ and $1.06\times10^{-4}$ for $W=10{,}000$. $\blacksquare$

**Theorem 2.** For a feature $f$ held by expert $e$,

$$\frac{\mathrm{SIR}^{\text{tree}}_f}{\mathrm{SIR}^{\text{dense}}_f} = \frac{d}{D}\cdot\frac{A_{\text{total}}}{A_e}.$$

Under A3, $A_{\text{total}} = 3k$ and $A_e = k\,\pi_e$, so the ratio is

$$\frac{d}{D}\cdot\frac{3}{\pi_e}.$$

*Proof.* Apply Lemma 2 in each space. The frequency $p_f$ is the same in both models, so it cancels. $\blacksquare$

| Feature | $\pi_e$ | Dense SIR, in units of $D/n$ | Tree SIR, in units of $d/n$ | Tree ÷ dense |
| --- | ---: | ---: | ---: | ---: |
| Root | $1$ | $1/3$ | $1$ | $0.3$ |
| Subroot | $1/2$ | $1/6$ | $1$ | $0.6$ |
| Leaf | $1/8$ | $1/24$ | $1$ | $\mathbf{2.4}$ |

**Corollary 2a (the tree evens out interference).** In the tree, every feature has the same ratio, whatever its level:

$$\mathrm{SIR}_f = \frac{d}{n}.$$

In the dense layer, the ratio depends on how often the feature's branch is used:

$$\mathrm{SIR}_f = \frac{\pi_e\, D}{3n},$$

so a leaf feature is 8 times worse off than a root feature. The tree lifts the worst-off features, the rare ones, by $\tfrac{d}{D}\cdot 3\cdot 8 = 2.4$, at the cost of the common ones.

**Corollary 2b (the total is fixed).** Under random placement, fix the tree's total width at $D_{\text{tot}} = \sum_e d_e$, and choose each expert's width in proportion to its activity, $d_e \propto A_e$. Then every feature gets

$$\mathrm{SIR}_f = \frac{p_f\, D_{\text{tot}}}{A_{\text{total}}},$$

which is exactly what a dense layer of width $D_{\text{tot}}$ gives. So no tree can beat a dense layer of the same total width for every feature at once. The tree moves SIR from some features to others, and with equal widths it moves it toward the rare features.

**Corollary 2c (deeper trees).** Take a tree with $L$ levels and branching factors $b_1,\dots,b_{L-1}$, so a leaf has $\pi_{\text{leaf}} = 1/\prod_j b_j$. With equal expert widths $d$, a leaf feature gains

$$\frac{\mathrm{SIR}^{\text{tree}}}{\mathrm{SIR}^{\text{dense}}} = \frac{d}{D}\cdot L\cdot\prod_{j} b_j.$$

So the gain for the deepest features doubles with each added binary level. The reason is that the leaf's share of activity halves while its width stays the same.

**Limits of Theorem 2.**

- It assumes random placement. A trained dense layer might place frequent features closer to right angles to everything else, and the theorem does not cover that case.
- Earlier work in this series found that, while features fit with room to spare, interference does not slow plain gradient descent. Interference matters when the space is crowded, as it is for real language. There, it sets the error with which each feature can be read.

## 6. Theorem 3: step size and learning speed

**Theorem 3.** Assume large batches, plain gradient descent, and a separate step size for each expert. Then a leaf expert can shrink the error of its features per step at least

$$\frac{\lambda_{\max}}{\lambda_{\text{leaf}}} \;\ge\; \frac{1}{\pi_{\text{leaf}}} = 2\times 4 = 8$$

times faster than the dense layer can. Here $\lambda_{\max}$ is the variance along the dense layer's strongest direction, and $\lambda_{\text{leaf}}$ is a leaf feature's variance.

*Proof.*

1. Full-batch gradient descent on squared error multiplies the error along a direction of variance $\lambda$ by $(1-\eta\lambda)$ at each step. This is stable only if $\eta < 2/\lambda_{\max}$.
2. In the dense layer, the strongest direction is at least as strong as a root feature, so $\lambda_{\max} \ge \tfrac{k}{n}s$. A leaf feature has $\lambda_{\text{leaf}} = \tfrac{k}{n}s\cdot\tfrac18$. So the fraction of a leaf direction's error removed per step is at most
$$\eta\,\lambda_{\text{leaf}} < \frac{2\lambda_{\text{leaf}}}{\lambda_{\max}} \le \frac{2}{8}.$$
3. A leaf expert averages over only its own sentences. On those sentences, its features have variance $\tfrac{k}{n}s$, the same as its strongest direction. So its fraction per step can approach 2.
4. The ratio of the two limits is at least 8. $\blacksquare$

**How general it is.** The factor equals $\prod_j b_j = 1/\pi_{\text{leaf}}$, so it doubles with each added binary level.

**Simulation check.** A dense layer with room to spare (width $2{,}000$ for $220$ features) was compared with the tree at batch size $512$. To learn 70% of the long-tail signal, the tree needed $6$ to $9\times$ fewer sentences in each of 3 runs.

**Limits of Theorem 3.**

- It needs each expert to have its own step size. With one shared step size, the gain disappears.
- With small batches, noise rather than the step-size limit sets the speed, and the gain shrinks. With room to spare and one sentence per step, the simulation showed no gain ($1.0$ to $1.1\times$).

## 7. Theorem 4: compute

**Theorem 4.** Per sentence and per output number, the dense layer uses $D = 10{,}000$ weights, and the tree uses $\sum_{e \in \text{path}} d_e = 3{,}000$. That is $3.3\times$ fewer.

For the whole layer per sentence, the dense layer uses $D^2 = 10^{8}$ weights, and the tree uses $3d^2 = 3\times10^{6}$. That is $33\times$ fewer.

*Proof.* Count the weights each sentence touches. $\blacksquare$

The $33\times$ contains a factor of 10 from the tree's narrower output: $1{,}000$ numbers instead of $10{,}000$. That factor is earned only if the narrower output loses nothing, which has not been analyzed. The three experts on a path add their outputs into the same $1{,}000$ dimensions.

**Total compute to learn the long tail, with large batches.** Multiplying Theorem 3 by Theorem 4 gives

$$\text{at least } 8 \times 3.3 \approx 26\times \text{ less compute, and } 8\times 33 \approx 260\times \text{ less if the narrower output holds up.}$$

## 8. What is proved, assumed or measured

| Statement | Status |
| --- | --- |
| The anisotropy note's capacity is equal for both models when the features fit (Theorem 1) | Proved |
| $C_{\text{tree}} = 1/\sum_e(\tilde\pi_e^2/C_e) \le \sum_e C_e$ (Lemma 1) | Proved |
| The tree evens out SIR, a leaf gains $2.4\times$, and the gain doubles per binary level (Theorem 2) | Proved, under random placement |
| No tree beats a dense layer of equal total width for every feature at once (Corollary 2b) | Proved, under random placement |
| A leaf learns at least $8\times$ faster per step with large batches (Theorem 3) | Proved, with a separate step size per expert |
| $3.3\times$ less compute per output (Theorem 4) | Proved, by counting |
| $33\times$ less compute for the whole layer | Assumed: needs the narrower output to lose nothing |
| A power-law spectrum inside each expert | Assumed |
| A perfect gate, tree-shaped knowledge, equal activity per level | Assumed |
| A step-size gain of $6$ to $9\times$ with room to spare | Measured, 3 runs |

## 9. Tests that could prove this wrong

1. **The shared output.** Measure how much the root, subroot and leaf outputs overlap in their shared $1{,}000$ dimensions, and include that in Theorem 2. This decides whether the factor of 10 in Theorem 4 holds.
2. **Learned placement.** In a trained dense layer, measure $I_f$ for rare features and compare it with Lemma 2's prediction, $p_f\,s\,A/W$. If training already shields rare features from common ones, Theorem 2's gain shrinks.
3. **Uneven activity.** Measure $A_e$ for each expert on real data. Theorem 2 then predicts each feature's gain as $\tfrac{d}{D}\cdot\tfrac{A_{\text{total}}}{A_e}$.
4. **Step size.** With large batches, count the steps each model needs to learn the leaf features. Prediction: about $8\times$ fewer steps for the tree, and about $16\times$ if each subtopic splits in two again.

## 10. Conclusions

1. **The tree does not win on the anisotropy note's capacity.** That capacity depends only on the list of feature strengths, and sorting features into experts does not change the list. The $6.4\times$ of version 4 is withdrawn.
2. **The tree changes who interferes with whom.** With equal widths, every feature gets the same signal-to-interference ratio. Rare features gain $\tfrac{d}{D}\,L\prod_j b_j$, which is $2.4\times$ here and doubles with each added binary level. Common features lose a little.
3. **Rare features learn at least $8\times$ faster per step** with large batches, because each expert sets its own step size. This factor also doubles with each added binary level.
4. **Compute.** Per output, the tree uses $3.3\times$ fewer weights per sentence; for the whole layer, $33\times$ fewer if the narrower output holds up. So the total compute to learn the long tail is at least about $26\times$ less, and about $260\times$ less if the narrower output holds up.

## Appendix: terms

| Term | Meaning |
| --- | --- |
| Expert | One small weight matrix in a mixture of experts |
| Gate | The part that chooses which experts a sentence goes through; assumed perfect here |
| SAE (sparse autoencoder) | A network that writes each input as a few directions taken from a large learned set of features |
| $\pi_e$ | The fraction of sentences that pass through expert $e$ |
| Capacity $C$ | $(\operatorname{tr}\Sigma)^2/\operatorname{tr}(\Sigma^2)$: the effective number of dimensions a space uses |
| Interference $I_f$ | The frequency-weighted squared leak of the other features onto $f$'s direction |
| SIR | Signal-to-interference ratio, $p_f s/\mathbb{E}[I_f]$ |
| Cauchy–Schwarz inequality | $\left(\sum_i a_i b_i\right)^2 \le \left(\sum_i a_i^2\right)\left(\sum_i b_i^2\right)$ |
| Step size $\eta$ | How far gradient descent moves at each step; it must satisfy $\eta < 2/\lambda_{\max}$ |
| Branching factor $b_j$ | How many children a node has at level $j$: 2 at the root and 4 at each subroot here |
