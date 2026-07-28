# Informative-Future Branch Signal And Its Use Boundary

## Abstract

A11 isolates one precise difference between next-token prediction (NTP) and
multi-token prediction (MTP). From the same current hidden state, NTP directly
supervises only the next token, whereas MTP may also supervise a later token
that reveals a branch variable not present in the next token. Controlled
experiments support that this informative future target creates an earlier
first-order task signal and that the signal can reach shared parameters. They
also show the central boundary: information formed at the current state need
not remain useful to the ordinary next-token head one position later. A11
therefore closes an objective-level mechanism result, not a long-context or
downstream-benefit claim.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| NTP | train the model to predict only the next token from each state | cross-entropy for $Y_{t+1}$ | baseline objective | absence of later information elsewhere in training |
| MTP | train the same shared state to predict several future tokens | losses for $Y_{t+1},\ldots,Y_{t+K}$ | adds earlier supervision paths | general performance improvement |
| branch variable $Z$ | the hidden choice that changes a later token while the immediate next token stays the same | $Z\in\{0,1\}$ in the minimal data | isolates new future information | natural-language semantics |
| informative future position | the first future position whose target still depends on $Z$ after earlier targets are known | $I(Z;Y_{t+j}\mid X_{\le t},Y_{t+1:t+j-1})>0$ | says when MTP adds a new direct signal | later functional use |
| formation | the current state moves in a direction that encodes $Z$ | hidden-state margin or semantic velocity | prerequisite for use | standard-head reliance |
| standard-head use | the ordinary next-token head benefits at the actual answer position | loss or causal output effect at $h_{t+1}$ | common outcome for NTP and MTP | real-task transfer |

## 2. The Minimal Data Model

The current prefix is matched across two branches. The immediate next token is
shared, while the second future token depends on the branch:

```text
branch Z=0:  <DECIDE> <SHARED> <BRANCH_0>
branch Z=1:  <DECIDE> <SHARED> <BRANCH_1>
```

At the hidden state produced by `<DECIDE>`, the next token `<SHARED>` contains
no information about $Z$. The later token `<BRANCH_Z>` does. This is a short
sequence by design: it removes retrieval, language ambiguity, and tree
composition so that the objective difference can be identified directly.

The decision-position objectives are

$$
L_{NTP}^{(t)}=\operatorname{CE}(q_1(h_t),Y_{t+1}),
$$

$$
L_{MTP}^{(t)}=L_{NTP}^{(t)}+
\lambda\operatorname{CE}(q_2(h_t),Y_{t+2}).
$$

Because $Y_{t+1}$ is branch-shared, its direct gradient cannot distinguish
$Z$. Because $Y_{t+2}$ is branch-dependent, the second term can.

## 3. Core Mechanism

For every informative future position $j$, let $u_{j,z}$ be the output
direction for branch $z$ and let $\bar u_j$ be the branch-common component.
The task-relevant first-order direction at horizon $K$ is

$$
v_z^{(K)}=
\sum_{j\le K:\,j\text{ informative}}
\lambda_j(u_{j,z}-\bar u_j).
$$

This model produces three falsifiable predictions:

1. no direct branch signal appears before the first informative future token;
2. covering that token turns the signal on;
3. additional targets help, do nothing, or hurt according to whether their
   centered output directions align, add no new information, or conflict.

The important variable is therefore not the numerical horizon $K$ by itself.
It is which informative targets are included and how their readout directions
combine.

## 4. Evidence Chain

### 4.1 Direct current-state signal

Controlled branch experiments match all local information and vary only the
future target. The measured hidden-state movement is zero before the first
informative position, becomes positive when that position is covered, receives
no incremental signal from a branch-shared target, and follows the predicted
sign under aligned versus conflicting output geometry.

Result: MTP supplies a direct first-order task signal at $h_t$ that NTP does
not receive at that same state.

### 4.2 Transmission to shared parameters

A useful hidden direction matters only if trainable shared parameters can
realize it. The parameter-space audit decomposes the update into the direct
MTP path and ordinary all-position background paths. The direct path is
reachable and predicts finite small-step movement, but the remaining language
model gradients are signed and can partially cancel it.

Result: the signal is not merely a fixed-head artifact, but positive direct
transmission does not guarantee a positive total update.

### 4.3 Formation does not imply use

The standard next-token head predicts the branch-dependent answer only after
the shared intervening token. Audits show positive usefulness at $h_t$ but
negative usefulness at $h_{t+1}$ across the tested seeds. Changing the output
head does not remove the sign reversal; changing the state position does.
Further bridge-token diagnostics do not produce stable held-out behavioral
gain.

Result: current-state formation is not sufficient for later standard-head use.
The state transition is an additional mechanism that must be tested rather
than assumed.

The subsequent model-local K/V audit made that test causal. Against a
shared-aux condition matched for active heads and nominal loss coefficients,
all capability and patch guards passed, but the registered strong behavioral
increment failed: $\bar\Gamma_{info}=0.01675$ and 0/5 seeds reached `0.10`.
Informative-MTP changed donor margins in 4/5 seeds, but this weak, seed-skewed
effect did not reliably control the answer.

The exact source-information follow-up then separated source formation from
use. Exact layer-2 `U03` K/V was perfectly branch-readable under NTP,
shared-aux, and informative-MTP in all five seeds, ruling out absolute linear
source emptiness. It did not identify an informative-MTP-specific readability
increment: mean $\Gamma_{\mathrm{read}}=-0.002299$ nat/example, with 4/5 seeds
nonpositive. The formal verdict remained insufficient because the registered
single-shuffle guard failed. A secondary 5/5 increase in Fisher separation was
driven mainly by within-branch nuisance contraction, suggesting geometric
organization of already-readable information rather than additional decoded
branch content.

## 5. What A11 Establishes

The stable A11 conclusion is:

> When an MTP horizon first covers a future token carrying branch information
> absent from the matched next token, MTP creates a direct first-order task
> signal at the current hidden state. That signal can reach shared parameters
> under the controlled assumptions, but its presence does not guarantee that
> the ordinary next-token head uses it at the later answer position.

This conclusion is specific enough to be falsifiable and broad enough to serve
as a prerequisite for structured workloads.

## 6. Claim Boundary

A11 does not show that the branch variable is long-range in the workload
sense, that multiple evidence items are composed, that larger models benefit
more, that curriculum helps, or that any natural-language benchmark improves.
It also does not show that every readable variable is causally used. The K/V
audits reject a reliable strong answer-control increment and do not identify
MTP-specific extra branch readability at one registered interface. The
secondary nuisance compaction does not establish total non-use, causal
consumption of geometry, or downstream benefit.

## 7. Handoff To A12

Before handing composition to A12, A11 has one remaining carrier-design gate:
construct a learnable `relay-required` task in which the answer cannot bypass
the early message and the matched control is not already saturated. Only then
can standard-head consumption be re-tested. A12 continues to own claims about
multi-item structured composition.

## 8. Anchor Chain And Source Map

1. [Informative-horizon supervision](/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor.md) — decisive [inclusion-law evidence](/Projects/from-attention-to-search/main/experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md).
2. [Hidden-to-parameter transmission](/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor.md) — decisive [transmission](/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md) and [all-position decomposition](/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md).
3. [Cross-position standard-head boundary](/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor.md) — decisive [position audit](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md), [end-to-end boundary](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md), [model-local K/V causal-use result](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md), and [exact source-information audit](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md).

Supporting variants that no longer change these conclusions are indexed under the [A11 experiment archive](/Projects/from-attention-to-search/main/experiments/A11/archive/README.md).
