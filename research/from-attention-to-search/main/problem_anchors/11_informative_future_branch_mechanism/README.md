# A11: Informative-Future Branch Mechanism

A11 isolates the objective-level difference between next-token prediction (NTP) and multi-token prediction (MTP) on the smallest matched branch. It does not own compositional workload claims; those belong to A12.

Current story:

- [English canonical story](../../stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md)
- [Chinese companion](../../stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md)

## Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| informative future target | a later token whose label still depends on branch variable \(Z\) after the matched local prefix is fixed | \(I(Z;Y_{t+j}\mid X_{\le t},Y_{t+1:t+j-1})>0\) | identifies when MTP adds a new direct path | behavioral benefit |
| standard head | the ordinary next-token head used for the final NTP/MTP comparison | \(q_1\) at the actual answer position | fixes a common outcome | full language-model quality |
| formation-versus-use boundary | information can enter \(h_t\) without helping the later standard head | positive current-state signal but nonpositive later usefulness | prevents a causal overclaim | structured-task success |

## Parent Anchors

Each directory contains one complete parent anchor. A subanchor is retained only when a control or falsifier is still needed to audit that parent conclusion.

| Order | Parent anchor | Stable knowledge update | Status |
|---|---|---|---|
| 1 | [11_01 Informative-horizon supervision](11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor.md) / [中文](11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor_cn.md) | A direct current-state signal begins when the objective covers a future target carrying new branch information; output-direction alignment, not horizon length alone, controls the increment. | completed, supported |
| 2 | [11_02 Hidden-to-parameter transmission](11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor.md) / [中文](11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor_cn.md) | The direct direction reaches shared parameters in the controlled model, while all-position background terms remain signed. | completed, conditional support |
| 3 | [11_03 Cross-position standard-head boundary](11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor.md) / [中文](11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor_cn.md) | Exact source K/V is generically branch-readable, but informative-MTP adds no registered readability or stable strong answer-control increment over matched shared-aux; a secondary nuisance-compaction pattern remains. | completed; relay-required carrier gate active |

The line is read as

\[
\text{informative future target}
\rightarrow
\text{direct current-state signal}
\rightarrow
\text{shared-parameter transmission}
\rightarrow
\text{cross-position use boundary}.
\]

## Claim Boundary

A11 establishes an earlier direct first-order task signal from informative future targets, conditional shared-parameter reachability, and a cross-position sufficiency failure. It does not establish long-range composition, tree reasoning, scale effects, curriculum benefit, real-workload transfer, or Router/MoE value.

The completed [11_03_02 causal-use subanchor](11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor.md) strengthens that boundary. The registered strong answer-switching increment over matched shared-aux failed. The exact source K/V follow-up found perfect branch readability under every objective but no informative-MTP-specific registered readability increment; its 5/5 Fisher nuisance compaction remains secondary geometric evidence.

## Exactly One Next Decision

Validate a learnable `relay-required` carrier with no direct answer bypass and a non-saturated shared-aux baseline. No K/V/Q/layer or shared-unembedding sweep is authorized before this carrier gate.

Decision-bearing experiment records are indexed in [the A11 experiment registry](../../experiments/A11/README.md). Nondecisive historical variants are archived there rather than represented as separate anchors.
