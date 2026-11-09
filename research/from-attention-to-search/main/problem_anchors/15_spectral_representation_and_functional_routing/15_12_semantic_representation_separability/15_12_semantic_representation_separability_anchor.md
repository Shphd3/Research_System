# A15_12: Fixed-Fact Cross-Expression Semantic Representation Separability


## 1. Problem Definition

The decision question is how much multigranular semantic information is
linearly and robustly readable from the actual Qwen3-30B-A3B MoE input at six
fixed depths when surface expression changes but the underlying set of 64
facts is held fixed. The required tasks are the eight-way parent label, eight
separate parent-conditioned eight-way child labels, and the global 64-way
parent--child label.

This is an absolute readout audit. It does not test whether the native Gate
uses the readout, whether an expert benefits from it, or whether supervision
can causally form a better representation.

## 2. Physical Priors

Semantic hierarchy and variance hierarchy are different objects. A direction
may carry little variance and remain discriminative, while a principal
component may carry high variance without separating labels. Linear
readability must therefore be measured by a held-out linear decision rule, not
by PCA, clustering, or a two-dimensional plot.

Parent-conditioned fine readability is also weaker than global semantic
routing. It grants the classifier the true parent before selecting a local
fine head. A single global linear Router instead requires all leaf scores to
coexist in one decision system. The 64-way task is therefore indispensable.

## 3. Falsifiable Hypotheses

The primary hypothesis is that at least one registered layer contains a
fixed-fact, cross-expression linear organization that is both predictive and
positive-margin for the parent, every parent-conditioned fine task, and the
global joint task on both held-out expression panels.

The strongest rival is partial organization: average parent or local fine
readability is high, but difficult samples cross a decision boundary or the
local tasks do not compose into a stable global 64-way separator. A second
rival is fixed-fact memorization; the present data cannot adjudicate it because
C4E and C5E reuse the same atomic facts.

## 4. Mathematical Model

For layer \(\ell\) let \(x_i^{(\ell)}\in\mathbb R^{2048}\) be the actual
`block.mlp` input at the final `Classification:` token. Training-half
isotropic normalization is

\[
z_i^{(\ell)}=\frac{x_i^{(\ell)}-\mu_\ell}{s_\ell},\qquad
s_\ell^2=\frac{1}{nd}\sum_i\lVert x_i^{(\ell)}-\mu_\ell\rVert_2^2.
\]

For a \(K\)-class linear head with scores
\(f_k(z)=w_k^\top z+b_k\), the geometric multiclass margin is

\[
\gamma_i=\min_{j\ne y_i}
\frac{(w_{y_i}-w_j)^\top z_i+b_{y_i}-b_j}
{\lVert w_{y_i}-w_j\rVert_2}.
\]

Balanced accuracy measures average classwise readout. The fifth percentile of
\(\gamma\) measures the low-tail boundary. The two are reported together and
cannot substitute for one another.

## 5. Computational Realization

The experiment reuses frozen Qwen3-30B-A3B activations at Blocks 4, 12, 20,
28, 36, and 44 from the completed A15_09 extraction. C4E half A contains 15
complete template families and is the only fitting/tuning surface. C4E half B
contains 15 unseen families. C5E contains 30 separately written families and
is evaluated without refitting.

Each layer fits ten L2-regularized multinomial logistic heads: one parent head,
one global 64-way head, and eight parent-specific fine heads. Hyperparameters
are chosen only by grouped cross-validation inside a registered training
surface. E01 fits C4E-A and freezes the heads for C4E-B and C5E. E02 fits C5E-A
and two C4E-A+C5E-A coverage controls to distinguish within-bank readability
from cross-bank boundary transfer. E03 freezes the original E01 heads and, if
the authorized RTX5090 extraction completes, evaluates one different TAX-C4A
fact package per semantic leaf without refitting.

## 6. Minimal Falsification Tests

The primary falsifier is a conjunction across all ten tasks and both
evaluation panels. A layer cannot be called expression-robust if a
parent-specific fine task is hidden by an average, if the global joint task
fails, or if the simultaneous low-tail margin lower bound is non-positive.

Held-out label association is calibrated by template-preserving permutation
of the evaluation labels with fixed predictions. This is a conditional
held-out prediction test, not a full retraining permutation and not a pristine
confirmation experiment. Cluster bootstrap resamples complete template
families. Confusion and class-distance-normalized variance localize failures
but do not own the verdict.

## 7. Current Evidence

**Evidence wording status:** `AI_EVIDENCE_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
The numerical records below passed their registered audits; the interpretation
and claim wording remain pending researcher confirmation.

The 2026-08-28 meeting record establishes the conceptual corrections that
semantic hierarchy is not a PCA variance ordering, distance clustering is not
linear separation, and a high average probe score does not imply a positive
low-tail margin. A prior native-Router-input audit on a different 19,200-row
dataset reported substantially above-chance average parent readability but
negative fifth-percentile score margins; its probe flow and unnormalized
margin are not directly comparable to the present audit.

A15_09 already verified the present activation identities and found stable but
null-subordinate overlap between coarse and parent-local fine Fisher spaces.
It did not measure absolute parent, conditional-fine, or 64-way joint
separability. A15_10 tested cross-parent functional subspace transfer rather
than the present absolute full-space readout.

Eligible A15_12_E01 and E02 measurements are computation-complete and
independently reproduced.
E01 fits 60 C4E-A heads and evaluates 120 task cells. All cells are associated
with the labels, and C4E-B has positive registered low-tail lower bounds at all
six blocks. The unchanged C4E-A boundary has a negative all-task observed
bottleneck on C5E at every block, primarily through parent-conditional fine
tasks. This establishes strong same-bank readability but rejects one stable
C4E-learned boundary across the C5E expression bank.

E02 compares C4E-A, C5E-A, matched two-bank, and full two-bank training on
frozen C4E-B and C5E-B panels. Its one simultaneous band protects all 48
regime-panel-layer cells; 22 have positive lower bounds. C5E-A-to-C5E-B has
positive observed all-task margins at all blocks and 99.1%--100% mean task
accuracy, but only Blocks 4, 12, and 44 have positive simultaneous lower
bounds. Neither single-bank head is certified in the opposite bank at any
block. Therefore Blocks 4, 12, and 44 specifically establish
expression-bank-conditioned boundary incompatibility distinct from internal
unreadability; Blocks 20, 28, and 36 retain internal C5E low-tail fragility as
a rival. Full two-bank training supplies a common certified boundary for both
panels at Blocks 4, 12, 20, and 44, but it jointly changes coverage and sample
count.

All E02 completion counts, 200 registered artifact hashes, 10,000 shared
family-bootstrap draws, 48 lower bounds, and 36 paired raw-unit contrasts were
independently recomputed. Row-level atom-order overlap exclusion changes no
bottleneck sign. These findings remain fixed-fact evidence.

## 8. Claim Boundary And Next Decision

Pending researcher confirmation of the evidence wording, the strongest
admissible positive claim is layer-local. Blocks 4, 12, and 44
support robust within-bank readout but incompatible single-bank boundaries;
full two-bank training supports one certified common boundary at Blocks 4, 12,
20, and 44. This does not establish a universal expression-invariant semantic
axis, and no result yet reaches a different fact package.

The evidence cannot establish semantic generalization to facts unseen during
Qwen pretraining, native Gate use, low-budget Router realizability, expert
utility, language-model improvement, causal representation formation, or a
universal semantic geometry law.

Exactly one next decision remains: apply the 60 frozen E01 heads to TAX-C4A,
which uses a different six-atom package for each semantic leaf. TAX-C4A also
changes length and surface naturalness, so success supports transfer to that
one joint-shift panel, while failure does not isolate fact identity. Do not
promote a representation-shaping or Router-capacity architecture until this
fact-package boundary is recorded. E03 itself still does not test an
architecture or expert utility; its result can only decide whether a separate
architecture Anchor and Protocol should be opened.
