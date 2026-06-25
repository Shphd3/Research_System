---
parent_node: problem.agent_workflow
---

# Attention-Gated Low-Level Feature Matching

## Question

Can a high-level module improve low-level closed-loop perception-control by providing attention or relevance gating, instead of providing only a target frame or target state?

The sharper subproblem is:

```text
Given the same current frame, target frame, low-level feature extractor, and matching algorithm,
does high-level task-conditioned channel attention improve adjacent-frame feature matching for the task-relevant object?
```

This is a child problem of Agent / Belief Workflow. It tests whether the high-level interface to the low-level loop should be:

```text
target only
```

or:

```text
target + attention / relevance gating
```

The broader workflow claim is that high-level control does not need to directly output motor actions. It can instead modulate what the low-level controller should attend to, trust, or ignore.

## 2. Physical Priors
The physical prior is:

```text
Low-level control should not use all sensory variation equally; it should use the sensory evidence that is relevant to the current physical target.
```

In a physical scene, many signals are real but irrelevant:

```text
background texture
distractor objects
non-target colors
irrelevant tactile contacts
unreliable feature channels
sensor noise
motion-induced changes unrelated to the target
```

If the low-level loop uses all channels uniformly, irrelevant features can create false correspondences, noisy control errors, or wrong contact attribution. A high-level target can make the low-level loop easier by specifying:

```text
what state should be reached;
which sensory evidence should be trusted while reaching it.
```

For the first visual test, the task-relevant object is a red square. The high-level module should therefore be allowed to emphasize red-target and supporting edge channels while suppressing unrelated channels.

## Biological / Embodied Motivation

Animals do not process every sensory channel as equally relevant during action. Attention is action- and goal-conditioned:

```text
when reaching for an object, vision emphasizes the object and its reachable boundary;
when expecting contact, tactile attention shifts toward the predicted contact region;
when following a target, irrelevant background motion is suppressed;
when acting without vision, proprioception and path-integrated body state predict where touch should occur.
```

The useful abstraction is not semantic attention alone. It is physical relevance:

```text
which sensory signals are expected to help reduce the current control error?
```

This connects to the earlier path-integration intuition. A high-level belief can predict not only where the target is, but also which future sensory channels should become relevant after the agent moves.

## 4. Mathematical Model
Let the low-level observation at time \(t\) be \(o_t\), and let a fixed feature extractor produce a feature tensor:

$$
\phi_t = \phi(o_t) \in \mathbb{R}^{C \times H \times W}
$$

Let the high-level workflow maintain a belief \(b_t\) and a compact target \(z_t^\*\), such as a target frame, target object, target contact state, or target keyframe. The high-level module outputs an attention vector:

$$
a_t^{attn} = A_\psi(b_t, z_t^\*) \in [0,1]^C
$$

The low-level loop receives a gated feature tensor:

$$
\tilde{\phi}_t = a_t^{attn} \odot \phi_t
$$

where the same channel weights are applied over spatial positions. For adjacent-frame matching, descriptors are extracted from the gated feature tensor:

$$
d_t(p) = \operatorname{Normalize}
\left(
\operatorname{Patch}(\tilde{\phi}_t, p)
\right)
$$

Given a source point \(p_t\) and candidate target-frame points \(q_{t+1,j}\), the matcher selects:

$$
\hat j =
\arg\min_j
\left\|
d_t(p_t) - d_{t+1}(q_{t+1,j})
\right\|_2
$$

The attention hypothesis predicts that task-relevant attention should:

```text
increase correct target-object matches;
decrease localization error;
decrease wrong-object matches;
increase descriptor margin between the best and second-best match.
```

Descriptor margin is:

$$
\Delta =
\operatorname{dist}_{2nd}
-
\operatorname{dist}_{best}.
$$

A larger margin means the low-level match is less ambiguous.

## Workflow Interface

The workflow becomes:

```text
task / high-level target
  -> belief over relevant physical object or surface
  -> attention / relevance gating
  -> low-level feature matching or state estimation
  -> control error
  -> action
```

So the compact target interface should allow:

```text
z_t^interface = (z_t^target, a_t^attn)
```

where:

```text
z_t^target says what to reach;
a_t^attn says what evidence to trust.
```

For future visual-tactile control, this can generalize from channel attention to:

```text
spatial object attention;
tactile taxel attention;
contact-region attention;
modality reliability gating;
path-integrated predicted contact gating.
```

## Minimal Computational Test

Use a controlled synthetic adjacent-frame matching task:

```text
two neighboring RGB frames;
one red square target;
many non-red square distractors;
small frame-to-frame shift;
fixed low-level CNN-like feature bank;
same candidate feature points for every condition;
only channel attention changes.
```

Compare:

```text
uniform:
  all feature channels weighted equally

red_target_attention:
  red-target and supporting edge channels emphasized

irrelevant_blue_attention:
  a task-irrelevant blue channel is emphasized as a negative control
```

Metrics:

```text
match_accuracy
mean_location_error_px
wrong_object_rate
descriptor_margin
```

## Falsifiable Conclusion

The attention-gated interface is supported if task-correct attention improves matching reliability or precision over uniform features and irrelevant attention degrades it.

The hypothesis is weakened if:

```text
uniform features consistently match as well as or better than task attention;
irrelevant attention does not hurt;
attention only improves a private descriptor metric but not target-object matching;
improved matching does not improve any downstream closed-loop controller.
```

## Current Evidence

- [Channel Attention For Low-Level Feature Matching](experiment_channel_attention_feature_matching_report.md)

The current diagnostic result supports the narrower interface claim: red-target channel attention improves localization precision and descriptor margin, while irrelevant blue-channel attention suppresses the red target cue and degrades matching. It does not yet prove learned attention, spatial attention, visual-tactile attention, or downstream closed-loop control improvement.
