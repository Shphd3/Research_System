# A15_13_01: Can a Final-to-Middle Semantic Chain Improve One-Layer Hierarchical Intent Representations?

Thinking Card source: [15_13_01_clinc150_one_layer_backward_hierarchical_router_thinking_card_cn.md](15_13_01_clinc150_one_layer_backward_hierarchical_router_thinking_card_cn.md)

## 1. Problem Definition

This subanchor inherits the A15_13 question of whether high-layer semantics can
causally shape an earlier representation. The local decision is whether, after
a Qwen3-0.6B teacher has learned CLINC150 intent classification, changing only
the fifteenth Transformer block with a final-to-middle, parent-first residual
Router yields more linearly separable within-domain intent representations than
a compute-matched flat Router.

CLINC150 supplies 10 coarse domains and 150 fine intents, with 15 intents per
domain. The blocking uncertainty is no longer whether a synthetic rule teacher
can extrapolate; it is whether the proposed intervention adds value after a
real pretrained language model demonstrably solves the downstream task. A Pass
admits one larger or second-dataset replication. A Fail stops promotion of the
current one-layer algorithm. Evidence is Insufficient when the teacher, data,
implementation, functional, resource, or paired-seed guard fails.

## 2. Physical Priors

The human-confirmed prior is that fine intents inside one domain share a domain
property, and a learner may benefit from first establishing that parent path,
freezing it, and learning the unexplained within-parent distinctions next. The
observable that exposes this prior is held-out within-domain intent
separability after a one-layer intervention. The prior is weakened locally if
a flat intent Router matches or exceeds the staged hierarchy under the same
teacher, data order, active expert computation, and optimization budget.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts that a final-layer soft semantic distribution
used in the sequence one shared expert, ten parent experts, frozen parent path,
and fifteen child experts per parent will increase the paired held-out
parent-conditioned fine-intent probe score relative to a one-shot flat Router.
The strongest rival is generic conditional adaptation: the same gain should
then appear under flat routing or an ordinary dense residual continuation.

Oracle gold labels define an attainable supervision upper bound but do not
substitute for the primary learned-semantic condition. A positive Oracle with a
negative learned condition localizes failure to the final-layer supervision
chain; a negative Oracle means the complete architecture/objective package is
not an adequate realization.

## 4. Mathematical Model

For utterance $x$, let $h_{14}(x)$ be the final non-padding state after the
fifteenth Transformer block and let the frozen teacher produce fine-intent
posterior $q_T(y\mid x)$. Domain posterior is the sum over the 15 intents in
each domain. The learned hierarchy minimizes task loss plus semantic routing
loss,

$$
L=L_{\mathrm{NTP}}+L_{\mathrm{intent}}+0.2L_{\mathrm{domain}}
  +\lambda_c\operatorname{CE}(q_T(c\mid x),p_{14}(c\mid x))
  +\lambda_f\operatorname{CE}(q_T(f\mid c,x),p_{14}(f\mid c,x)).
$$

$L_{\mathrm{NTP}}$ is token-averaged next-token cross entropy on the visible
utterance; the other two task terms are final-state classification cross
entropies. During the child stage, the parent Router and parent experts are
frozen. The child Router reads $r=h_{14}-P_Ch_{14}$, where $P_C$ projects onto
the row space of the learned parent gate. This is an operational coarse
discriminant removal, not a claim that the entire coarse semantic component is
known.

## 5. Computational Realization

The verified official CLINC150 files provide 15,000 training, 3,000
development, and 4,500 confirmation utterances, balanced across 150 intents;
out-of-scope examples are excluded. Intent and domain labels may enter teacher
training and the Oracle condition. Confirmation labels never enter fitting,
checkpoint selection, pseudo-label creation, Router decisions, or threshold
tuning.

The base is the official Qwen3-0.6B-Base causal model with 28 Transformer
layers. A common teacher is fine-tuned on the training split and selected only
on development evidence. Stage two freezes the teacher, both classification
heads, and all original model weights. A zero-initialized residual expert
module is inserted after block index 14; gradients pass through the frozen
upper network into this module. Thus all trainable representation change is
localized to one block output.

The treatment grows from one shared bottleneck expert to ten domain experts,
freezes that parent path, and adds 15 child experts within each domain. The
flat control uses 150 fine-intent experts with two active experts, matching the
treatment's two active expert networks per example. A dense residual control
and a gold-label hierarchical Oracle separate ordinary continuation and label
quality from the learned backward chain.

## 6. Minimal Falsification Tests

The decisive comparison is learned hierarchical backward routing versus flat
learned-semantic routing on two paired teacher seeds. The primary metric is the
official test-set macro F1 of a frozen multinomial linear probe for the 15
fine intents trained separately within each domain on training representations
and selected on development representations, then averaged equally over the
10 domains. It is measured in percentage points. The paired bootstrap resamples
test utterances within intent and reports a 95% interval for the treatment
minus control difference.

Pass requires both seeds to improve, the pooled paired interval lower bound to
exceed zero, and final intent macro F1 to degrade by no more than one percentage
point relative to the flat control. Fail means the interval upper bound is at
or below zero or both seeds are non-positive while guards pass. Otherwise the
result is Insufficient. The X-MoE representation-collapse statistic,
$\operatorname{Tr}(\Sigma_W\Sigma_B^\dagger)$, effective rank, centroid margin,
k-nearest-neighbor F1, load entropy, and route-label agreement are secondary;
none can rescue a failed primary metric.

## 7. Current Evidence

The official dataset contains the required real hierarchy and fixed balanced
splits. The official Qwen model card establishes that Qwen3-0.6B-Base is a
28-layer causal language model. The parent A15_13 experiment directly observed
that its synthetic three-layer teacher failed the cross-template semantic
entrance, so that result did not test a qualified high-to-middle chain. No
Qwen3-0.6B CLINC150 training or one-layer intervention result exists at this
anchor's registration time.

## 8. Claim Boundary And Next Decision

A Pass would support only that this named one-layer, supervised real-intent
realization improves held-out linear accessibility without the registered task
degradation. It would not prove native unsupervised semantic discovery,
functional expert specialization, compute efficiency, general open-domain
hierarchies, or benefit at larger model scale. Router-label agreement and probe
quality remain weaker claims than counterfactual expert utility.

Exactly one next decision follows the complete run: decide whether to perform
one independent replication on a second real hierarchy or larger model. The
completion criterion is both teacher seeds, all four paired stage-two
conditions, the frozen primary analysis, functional guards, collapse audit,
and auditable result records.
