# V2.2 Research Plan: Static Feature-Family Dispatch

## 0. Goal

Close the advisor's clean mathematical case as a self-contained static result:

> Under globally spectrally isotropic and frequency-uniform feature-family distributions, when is static feature-family dispatch identifiable, and how can a label-free calibration-time router construct it?

This stage does **not** study preservation during training.

## 1. Current thesis

```text
Spectral isotropy gives a clean global metric.
Frequency uniformity makes equal-number family assignment mass-balanced.
Local feature recoverability makes feature-family dispatch identifiable.
BFSR uses these conditions by normalizing, clustering, assigning families, and routing by recovered family identity.
```

## 2. Method status

Primary method:

```text
BFSR-Cluster
```

Baselines / anchors:

```text
OracleFeature       non-admissible upper bound
Quantile-SPR        mass-only baseline
Random linear       ordinary static router baseline
```

## 3. Executed anchors

| ID | Hypothesis | Result status |
|---|---|---|
| H1 | Spectral isotropy alone is insufficient. | Supported by E2: expert information fraction about 0.002. |
| H2 | Uniform feature frequencies cause mass balance under equal-number family assignment. | Supported by E1 and E5. |
| H3 | Local recoverability causes feature-family dispatch. | Supported by E3 separation sweep. |
| H4 | Spectral normalization acts as metric repair. | Supported by E4 raw-vs-whitened ablation. |
| H5 | Quantile balancing is not enough for feature-family dispatch. | Supported by E1 and E5: low LoadCV but high split rate. |

## 4. Current results

Full-run setting:

```text
seeds: 0,1,2,3,4
d: 16
K: 32
E: 4
calibration examples: 8000
holdout examples: 16000
```

Key results:

```text
E1: BFSR-Cluster LoadCV 0.003, family consistency 0.990, cluster accuracy 0.986.
E2: admissible label-free methods expert information fraction about 0.002.
E3: separation 0.45 -> 2.50 gives cluster accuracy 0.063 -> 0.942 and family consistency 0.294 -> 0.956.
E4: whitening on distorted structured data gives cluster accuracy 0.250 -> 0.958; null information remains about 0.002.
E5: under frequency imbalance, equal-number BFSR LoadCV 0.149; mass-aware BFSR LoadCV 0.029.
```

## 5. Decision rule

The current E1--E5 results are sufficient for a group-meeting closure of the static clean case.

Do not expand the main paper claim unless a new experiment is explicitly opened.

## 6. Next possible stages

After the meeting, choose one:

### A. Static utility audit

Question:

```text
Does feature-family dispatch improve fixed-route expert learning on feature-dependent targets?
```

This is the next experiment if the group wants evidence for "better learning".

### B. Real hidden-state audit

Question:

```text
Do real route-relevant hidden states contain locally recoverable feature-family structure after spectral normalization?
```

This is the next experiment if the group wants to connect the synthetic clean case to language models.

### C. Training preservation

Question:

```text
Can a static feature-family partition remain stable under representation drift during training?
```

This should remain a later stage, not part of V2.2.

### D. Automatic K selection

Question:

```text
Can K be selected from calibration features without knowing the synthetic ground-truth family count?
```

This is a method-completeness issue, not necessary for the first clean case.

## 7. Writing rule

The paper should read as a self-contained static result, not as a changelog from V1/V2/V2.1.

Allowed final claim:

```text
Under globally spectrally isotropic, frequency-uniform, locally recoverable
feature-family distributions, BFSR constructs balanced static feature-family
dispatch by recovering families and assigning them to experts under a balanced
constraint.
```

Forbidden claims:

```text
spectral isotropy alone gives good routing
BFSR proves downstream task improvement
BFSR solves learned-router MoE training
BFSR solves route preservation
BFSR works on real hidden states without a real-data audit
```
