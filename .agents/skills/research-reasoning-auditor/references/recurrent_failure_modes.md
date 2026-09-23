# Recurrent Research Reasoning Failure Modes

Use this file as a guardrail when the research discussion becomes conceptually
mixed. These are reasoning patterns to detect, not personality labels.

## 1. Desired Result Becomes The Purpose

**Symptom**

The purpose says the method should make a representation "better", "more
separable", "more organized", or "more efficient" before the actual uncertainty
has been stated.

**Why it fails**

The desired answer is smuggled upstream into the question. A negative result
then looks like experiment failure rather than a legitimate scientific update.

**Repair question**

What is unknown even if the expected improvement never occurs?

---

## 2. Observation Becomes Mechanism

**Symptom**

A measured change such as lower effective rank, higher feature reuse, a cleaner
cluster, or higher probe accuracy is immediately explained as the mechanism.

**Why it fails**

The observation constrains explanations but does not uniquely identify one.

**Repair question**

What competing mechanism would produce the same observation?

---

## 3. Proxy Becomes The Scientific Object

**Symptom**

The discussion moves directly from a proxy metric to a semantic or functional
claim: probe accuracy becomes "the model knows", route purity becomes "expert
specialization", feature reuse becomes "semantic organization".

**Why it fails**

The metric measures an observable property, not necessarily the intended
construct.

**Repair question**

What does this metric directly measure, and what stronger claim still requires
another test?

---

## 4. Cause And Effect Are Reversed

**Symptom**

The experiment starts from a metric that is easy to compute, predicts how it
should move, and then constructs a causal explanation and research purpose
around that expected movement.

**Why it fails**

The downstream readout has become the upstream scientific question. This makes
the story circular.

**Repair question**

If this metric did not exist, what unresolved phenomenon would still motivate
the experiment?

---

## 5. Only The Favored Hypothesis Is Modeled

**Symptom**

The plan asks whether evidence "supports our explanation" but does not state a
credible alternative that fits the current observations.

**Why it fails**

Almost any positive-looking result can be assimilated into the preferred story.

**Repair question**

What is the strongest rival explanation that would make the current observation
unsurprising?

---

## 6. The Experiment Confirms But Does Not Discriminate

**Symptom**

Several hypotheses predict the same metric direction, yet that metric is used
as the main test.

**Why it fails**

The experiment can confirm compatibility, but it cannot change the relative
belief between explanations.

**Repair question**

On which observable do the hypotheses make different predictions?

---

## 7. Metrics Are Stacked Without A Construct Map

**Symptom**

Effective rank, anisotropy, feature reuse, Fisher ratio, linear-probe accuracy,
clustering, and task metrics are presented together as if they jointly prove one
mechanism.

**Why it fails**

They live at different evidence levels and may be statistically dependent or
measure unrelated constructs.

**Repair question**

For each metric, what exact claim can it support and which claim can it not
support?

---

## 8. Mathematics Arrives Before The Question Is Identified

**Symptom**

A sophisticated geometric statistic, decomposition, or optimization objective is
introduced before the uncertain causal or functional relation is clear.

**Why it fails**

Mathematical precision can make an ill-posed scientific question look precise.

**Repair question**

What scientific distinction would remain if the current mathematical tool were
removed?

---

## 9. Historical Or Structural Confounds Are Treated As Mechanism

**Symptom**

Two models differ in the current target variable but also differ in training
history, architecture, data order, checkpoint age, or optimization path.

**Why it fails**

The observed difference cannot be assigned to the intended cause.

**Repair question**

What alternative difference between the conditions could carry the same effect?

---

## 10. Story Coherence Is Mistaken For Identification

**Symptom**

The explanation becomes increasingly smooth: observation A is said to cause B,
which explains C, which motivates D, and the narrative feels convincing.

**Why it fails**

A coherent chain can contain several unsupported arrows. Narrative continuity is
not evidence.

**Repair question**

Which single arrow in the story is least directly tested?

---

# Example: SAE Representation Geometry

A problematic chain is:

~~~text
stronger SAE regularization
-> representation is reconstructed by fewer shared features
-> representation becomes lower-dimensional
-> domain information is better organized
-> linear classification and Fisher ratio should improve
~~~

The first two observed changes do not identify the third semantic claim.

A cleaner formulation is:

**Observed**

Stronger sparse-autoencoder (SAE) regularization is associated with higher
cross-sample feature reuse and lower effective rank in the backbone
representation.

**Unknown**

What information is being concentrated by this geometric change?

**H1: selective organization**

Domain-discriminative information is retained or made more accessible while the
representation concentrates.

**Rival: global/shared compression**

Shared directions become dominant while domain-specific distinctions are
unchanged or weakened.

**Separating prediction**

The two explanations can agree on lower effective rank and higher feature reuse,
so those metrics cannot separate them. They differ on domain-specific
discriminative structure: linear accessibility, Fisher-style between-domain
versus within-domain geometry, and—if the scientific claim requires it—later
functional or intervention evidence.

**Boundary**

A better linear probe or Fisher ratio would show greater domain accessibility or
separation. It would not by itself show that the base model uses those
directions, that SAE caused a semantic reorganization through a particular
mechanism, or that downstream task behavior improved.

The correct research move is therefore not to ask whether the already-observed
low-rank geometry is "good". It is to ask what information that concentration
preserves, amplifies, or discards, and to choose a test that separates those
possibilities.
