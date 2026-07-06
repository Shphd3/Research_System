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
Feature-dependent targets are a downstream optional utility audit, not the current stage claim.
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

Downstream condition: target is feature-dependent.
Mechanism: give each expert a coherent subset of feature families.
Effect: optional later static expert-learning audit.
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
feature-dependent vs feature-independent targets, parked for downstream utility
expert alignment vs random expert geometry, parked for downstream expert-identity audits
```

### 3.2 Methods

Primary:

```text
BFSR-Cluster
```

Anchors / controls:

```text
BFSR-OracleFeature       # upper bound, not non-cheating
Quantile-SPR             # mass without guaranteed feature coherence
Vanilla linear top-1     # ordinary static router
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
family consistency: average max_e P(G=e | F=k)
feature split rate
expert information fraction I(G;F)/H(G)
NMI(G,F), as a supplementary metric because G is coarser than F when K>E
```

Feature recovery:

```text
cluster recovery accuracy up to permutation
Adjusted Rand Index
cluster purity
```

Parked static utility:

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
| H1 | Spectral isotropy alone is insufficient. | Isotropic Gaussian with independent random labels gives near-zero expert information fraction for all non-cheating methods. | Any valid method gets high information fraction when labels are independent of X. |
| H2 | Uniform feature frequencies cause mass balance under balanced family assignment. | Oracle and recovered feature assignment give LoadCV near 0 when K divisible by E. | Equal family assignment fails on truly uniform recovered families. |
| H3 | Local recoverability causes specialization. | As separation increases, cluster accuracy and family consistency increase. | High family consistency when cluster recovery is poor. |
| H4 | Spectral normalization acts as metric repair, not as a specialization source. | Whitening improves clustering under anisotropic distortion. | Whitening improves information fraction on unstructured isotropic null data. |
| H5 | Quantile balancing is not enough for feature specialization. | Quantile-SPR has low LoadCV but lower feature-family consistency than BFSR on recoverable feature-family data. | Quantile-SPR matches BFSR on feature consistency across all structured regimes. |
| H6 | Feature-frequency uniformity is the mass premise for equal-number assignment. | Equal-number family assignment fails under frequency imbalance, while mass-aware assignment repairs load. | Equal-number assignment stays balanced under strong frequency imbalance without using masses. |
| H7 | Expert alignment is downstream. | Parked until the static family-dispatch story is accepted. | N/A for current stage. |
| H8 | Static utility is downstream. | Parked until the static family-dispatch story is accepted. | N/A for current stage. |

## 5. Research phases

### Phase 1: lock the clean feature construction

Deliverables:

```text
synthetic generator for isotropic feature-family mixtures
frequency-uniform option
separation sweep
anisotropic distortion option
feature-dependent and feature-independent target options parked for downstream utility
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
Quantile-SPR baseline
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

### Phase 4: parked static utility audit

Train fixed-route experts under different routers on controlled tasks only after the static dispatch stage is accepted.

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

### Risk 2: downstream utility does not follow from static dispatch

Check:

```text
target may not be feature-dependent enough
experts may be too expressive
training budget may hide specialization benefits
assignment objective may group incompatible features
```

Decision:

```text
Treat this as a downstream audit. Do not weaken the static dispatch result unless the paper tries to claim utility.
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

> In globally spectrally isotropic and frequency-uniform feature distributions, static feature-family dispatch is possible when local feature families are recoverable. BFSR exploits this condition directly by recovering feature families in the normalized space and assigning them to experts under a balanced constraint. It achieves balanced usage because family frequencies are uniform, while utility and training preservation remain downstream questions.

This is a clean closure of the static stage, not a claim about dynamic MoE training.
