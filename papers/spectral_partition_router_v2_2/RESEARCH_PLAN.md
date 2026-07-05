# V2.2 Research Plan: Static Feature-Level Specialization

## 0. Goal

The next stage is to close the advisor's clean mathematical case as a self-contained research story.

The paper should answer:

> Under globally spectrally isotropic and frequency-uniform feature distributions, when is static feature-level specialization identifiable, and how can a non-cheating router construct it?

This stage does **not** study preservation during training.

## 1. Current research thesis

The thesis is:

```text
Spectral isotropy gives a clean global metric.
Frequency uniformity gives the possibility of balanced expert usage.
Recoverable local feature families give the possibility of specialization.
Balanced feature-family assignment gives the routing mechanism.
Feature-dependent targets give measurable static utility.
```

The primary method is **BFSR: Balanced Feature-Specializing Routing**.

## 2. Why this is more causal than quantile-first routing

Quantile routing is a valid way to control probability mass, but it is not specific to the current feature assumption. It works for many distributions, including distributions without meaningful feature families. Therefore it is weakly causal for feature-level specialization.

The new method uses the assumptions more directly:

```text
Condition: feature families have uniform frequency.
Mechanism: assign equal numbers or equal masses of feature families to experts.
Effect: balanced expert usage.

Condition: feature families are locally recoverable.
Mechanism: recover families by unsupervised clustering in the normalized metric.
Effect: high feature consistency / specialization.

Condition: the global feature spectrum is isotropic.
Mechanism: use the normalized space as a clean metric for clustering and expert alignment.
Effect: avoid anisotropic confounds.

Condition: target is feature-dependent.
Mechanism: give each expert a coherent subset of feature families.
Effect: lower static expert-learning loss.
```

Quantile-SPR should remain as a baseline because it distinguishes mass balance from feature specialization.

## 3. Research objects

### 3.1 Data family

Synthetic controlled data should be generated from:

\[
F\sim \mathrm{Unif}(\{1,\ldots,K\}),
\qquad
X|F=k=\mu_k+\epsilon.
\]

The centers \(\mu_k\) should be constructed so that the aggregate distribution is globally isotropic or becomes isotropic after whitening:

\[
\Cov(\widetilde X)\approx I.
\]

The distribution should allow controlled variation along:

```text
feature separation
feature frequency imbalance
anisotropic distortion
feature-dependent vs feature-independent targets
expert alignment vs random expert geometry
```

### 3.2 Methods

Primary:

```text
BFSR-Cluster
BFSR-ExpertAligned
```

Anchors / controls:

```text
BFSR-OracleFeature       # upper bound, not non-cheating
BFSR-RandomGroup         # balanced feature grouping without geometry
Quantile-SPR             # mass without guaranteed feature coherence
Vanilla linear top-1     # ordinary static router
BalancedAssignment       # batch-count control, not valid main method
Random router            # lower bound
```

### 3.3 Metrics

Mass:

```text
LoadCV
max absolute mass error
expert usage entropy
```

Feature specialization:

```text
NMI(G,F)
purity
H(G|F)
I(G;F)
percentage of feature families split across experts
within-expert feature-family diversity
```

Feature recovery:

```text
cluster recovery accuracy up to permutation
Adjusted Rand Index
cluster purity
```

Static utility:

```text
validation loss after training fixed-route experts
per-feature validation loss
loss gap vs incoherent balanced controls
```

Distribution diagnostics:

```text
covariance condition number
operator norm |Cov-I|
feature separation
estimated family mass imbalance
```

## 4. Hypothesis-to-anchor map

| ID | Hypothesis | Positive anchor | Falsifier / negative anchor |
|---|---|---|---|
| H1 | Spectral isotropy alone is insufficient. | Isotropic Gaussian with independent random labels gives low NMI for all non-cheating methods. | Any method gets high NMI when labels are independent of X. |
| H2 | Uniform feature frequencies cause mass balance under balanced family assignment. | Oracle and recovered feature assignment give LoadCV near 0 when K divisible by E. | Equal family assignment fails on truly uniform recovered families. |
| H3 | Local recoverability causes specialization. | As separation increases, cluster accuracy and NMI increase. | High NMI when cluster recovery is poor. |
| H4 | Spectral normalization acts as metric repair, not as a specialization source. | Whitening improves clustering under anisotropic distortion. | Whitening improves NMI on unstructured isotropic null data. |
| H5 | Quantile balancing is not enough for feature specialization. | Quantile-SPR has low LoadCV but lower NMI / utility than BFSR on feature-family data. | Quantile-SPR matches BFSR on feature coherence across all structured regimes. |
| H6 | Expert alignment helps only when expert geometry is aligned with feature families. | BFSR-ExpertAligned improves assignment utility with aligned experts. | Random expert geometry improves similarly. |
| H7 | Static utility requires feature-dependent target. | BFSR improves fixed-route expert loss when target depends on F. | BFSR improves equally when target is feature-independent. |
| H8 | Batch-count balancing is not a feature router. | BalancedAssignment gives LoadCV=0 but low feature consistency and unstable per-batch route identity. | BalancedAssignment yields coherent feature-family routing without labels or stable feature geometry. |

## 5. Research phases

### Phase 1: lock the clean feature construction

Deliverables:

```text
synthetic generator for isotropic feature-family mixtures
frequency-uniform option
separation sweep
anisotropic distortion option
feature-dependent and feature-independent target options
```

Exit criterion:

```text
Covariance diagnostics show isotropy in the clean setting,
while latent feature families remain recoverable when separation is high.
```

### Phase 2: implement BFSR and anchors

Deliverables:

```text
BFSR-OracleFeature
BFSR-Cluster
BFSR-ExpertAligned
BFSR-RandomGroup
Quantile-SPR baseline
BalancedAssignment control
```

Exit criterion:

```text
BFSR-OracleFeature verifies the theoretical upper bound.
BFSR-Cluster approaches it when feature recovery is easy.
```

### Phase 3: run identifiability anchors

Experiments:

```text
isotropic null with independent labels
isotropic structured mixture with separation sweep
raw anisotropic distortion vs whitened features
frequency imbalance sweep
```

Exit criterion:

```text
Every positive result has a matched negative control.
```

### Phase 4: run static utility audit

Train fixed-route experts under different routers on controlled tasks.

Exit criterion:

```text
BFSR improves loss only when the target is feature-dependent and feature families are recoverable.
```

### Phase 5: write group-meeting closure

The report should answer:

```text
What exactly was the clean case?
Why isotropy alone is insufficient?
What additional minimal condition made the problem solvable?
What method used that condition causally?
Which experiments close the stage?
What remains for the next stage?
```

## 6. Risks and decision rules

### Risk 1: BFSR-Cluster fails despite recoverable data

Check:

```text
cluster K known or not
separation too low
whitening implementation
cluster initialization
feature centers not actually balanced / isotropic
```

Decision:

```text
If OracleFeature succeeds but Cluster fails, the theory is fine but recovery algorithm is weak.
If OracleFeature fails, the problem definition or data construction is wrong.
```

### Risk 2: BFSR balances mass but does not improve utility

Check:

```text
target may not be feature-dependent enough
experts may be too expressive
training budget may hide specialization benefits
assignment objective may group incompatible features
```

Decision:

```text
Use capacity-limited experts and feature-conditioned targets for the static utility audit.
```

### Risk 3: Quantile-SPR matches BFSR

Interpretation:

```text
The data may be too easy or aligned with the quantile split direction.
```

Decision:

```text
Add multi-cluster arrangements where any single projection threshold cuts through feature families.
```

### Risk 4: Whitening improves everything, including null data

Interpretation:

```text
Possible artifact in labels, clustering, or evaluation.
```

Decision:

```text
Re-run the isotropic null with independent labels and report confidence intervals.
```

## 7. Writing rule

The paper should be self-contained. It should not read like a changelog from V1/V2/V2.1.

Allowed framing:

```text
We study a controlled static problem motivated by uniform feature dispatch.
```

Avoid framing:

```text
In the previous version we did X; now we change Y.
```

## 8. Expected final claim

If experiments support the hypotheses, the final claim should be:

> In globally spectrally isotropic and frequency-uniform feature distributions, static feature-level specialization is possible when local feature families are recoverable. BFSR exploits this condition directly by recovering feature families in the normalized space and assigning them to experts under a balanced constraint. It achieves balanced usage because family frequencies are uniform, and it improves static utility only when the task respects the same feature-family structure.

This is a clean closure of the static stage, not a claim about dynamic MoE training.
