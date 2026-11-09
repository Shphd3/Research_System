# A15_26: Previously Learned Computation In Conditional Orders And Low-Frequency Compositions

[中文](15_26_low_frequency_compositional_reuse_anchor_cn.md)

## 1. Problem Definition

**When a model has learned the component operations of an order system, does that learning help new conditional orders, can slower updates retain those capabilities, and do the remaining differences benefit from separate branches?** This is one bounded decision chain in the A15 question of which computations should be learned together or separately. Prior component learning, correct combined answers, causal reuse, update utility, branch utility and successful input routing are distinct claims.

A15_26 remains an independent parent Anchor. A15_24 owns frequency-based expert invocation; A15_25 owns feature relations; A15_11 separates accessible labels, useful actions and routing; A17_04 owns conditional-rule reversal. Their local findings motivate controls here but do not supply this round's results. The concurrent [R01 controlled-operation Protocol](../../../experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/protocol.md) and [Focus](../../../focus/focus_low_frequency_compositional_reuse.md) are now present under this same owner. They retain their own symbolic design and delegated execution scope. The current user separately adopted the V2 order six-stage design and bounded automatic execution; this order round does not overwrite R01 or its Focus, and neither round closes the scientific question.

The main task of the present V2 round is the order system below, with its specified symbolic auxiliary. In parallel, R01 is an authorized controlled-symbolic experiment with its own execution and reuse diagnostics; its current results are Unknown here. The original pre-V2 discussion snapshot is retained as history. Its selective single-operation rule revision is not an extra training obligation in this order round and is not described as globally unexecuted now that R01 exists. [The retained prior Anchor and exact source intake](../../../experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/sources/README.md) distinguish these versions.

If valid comparisons support a link, retain that link within this task. A valid negative weakens the tested link, not the entire MoE idea. Failed data/implementation or component eligibility makes dependent claims insufficient or not applicable. Natural-language pretraining, model scaling, joint router/expert search and universal hierarchy claims are outside this round.

## 2. Physical Priors

The researcher's confirmed core is the help and reuse of previously learned computation; completely freezing original weights is a stronger hypothesis. The motivating, unproved prior is that learned component processing can support new combinations while only some differences need further learning. Semantic task rules make this falsifiable; they do not locate neural modules.

Two qualifications matter. Frequent exposure does not imply mastery, so single operations must be measured. Shared use does not imply that shared parameters should stop changing, so normal, slow and frozen updates must all remain eligible competitors. Extra branch capacity and external task labels can help without revealing intrinsic expert structure.

## 3. Falsifiable Hypotheses

| Stage | Prediction | Strongest live rival and separator |
| --- | --- | --- |
| S1: base amount | Component-trained models calculate price times quantity on held-out numerical pairs. | A purported composition deficit may be an unlearned multiplication; test it directly. |
| S2: conditional components | Discount, threshold comparison, explicit shipping addition, and comparison-plus-addition each pass eligibility when the preceding amount is supplied. | Good averages hide one failed component; evaluate each separately and audit threshold equality. |
| S3: transfer | Correct component training improves combined-order learning relative to Base and a matched-format field-copy parent under the same subsequent supervision. | General training, arithmetic fluency and format familiarity; retain both controls and starting scores. This comparison alone cannot prove internal reuse. |
| S4: updates | With the same added branch, slower parent learning improves component retention without failing combined-order learning. | Everything merely learns more slowly; include joint-normal, frozen, globally slower and no-added-branch controls. |
| S5: exposure | Exchanging high/low exposure of the same discount-threshold pair changes its held-out accuracy, despite matched parameter marginals. Separately, update-policy gains may depend on exposure. | Fixed pair difficulty, amount distribution and shipping status; pair identities are exchanged and content strata retained. |
| S6: branches | Separate branches improve qualified order learning or exposure-to-eligibility over sharing after capacity and active-compute comparisons. A learned selector can then use the frozen branches from actual input. | More total capacity, semantic-label supervision, load and soft computation; compare both budget lines, hash grouping, and fixed-branch routing interventions. |

An internal-reuse diagnostic predicts a specific replacement-amount answer while keeping the recipient's subsequent rule fixed. Mere degradation or a readable amount is insufficient. Failure to identify a qualified carrier leaves internal reuse **Unknown**, even if learning succeeds.

## 4. Mathematical Model

All amounts are integer cents. Let unit price be \(p\), quantity \(q\), base amount \(b=pq\), discount percentage \(d\), discounted amount \(s=bd/100\), shipping threshold \(T\), and shipping fee \(f\). Inputs are chosen so \(s\) is an integer. The task defines

\[
y_{\mathrm{BASE}}=b,\qquad y_{\mathrm{DISCOUNT}}=s,\qquad
y_{\mathrm{SHIPPING}}=b+f\mathbf 1[b<T],\qquad
y_{\mathrm{BOTH}}=s+f\mathbf 1[s<T].
\]

Equality gives free shipping; shipping is never discounted. The prompt specifies the active rule and the model predicts only the final amount. These equations define labels, not the network's algorithm.

For an added branch at the final attention output, \(r(h)=B\,\mathrm{GELU}(Ah)\), with zero-initialized \(B\). The branch is added before the native residual addition. Original candidate weights receive normal, one-tenth, or zero learning rate; observed optimizer displacement is measured independently. The branch is an engineering intervention, not a known composition module.

Frequency changes apply only to the sixteen \((d,T)\) pairs of BOTH. A balanced cycle uses nine examples per pair; an 8:1 cycle uses sixteen for each high pair and two for each low pair. Each row and column has two high cells, so both cycles contain 144 examples and each marginal count is 36. This is a derivation of exposure matching, not a prediction of learning benefit.

## 5. Computational Realization

**Establish the task and its prerequisites.** Independently calculate labels, split complete orders by the numerical pair \((p,q)\), audit canonical single-operation inputs separately, and score unrestricted native generation. Train component parent P and field-copy parent C from the exact same Qwen3-0.6B Base identity; retain untrained Base B. This distinguishes missing components from new composition and general prior training.

**Compare adaptation and exposure.** P, B and C receive the same joint adaptation for transfer. From each eligible P compare no-added-branch U, normal-joint J, slow-parent S, frozen-parent F, globally slower G and read-only Z. Reuse J balanced across stages. Exact 10% old-example replay is common; J/S/F also receive a zero-old-loss sensitivity condition with unchanged new examples and new-loss weight. Exchange BOTH pair frequencies while matching actual exposure schedules across methods. The [Protocol](../../../experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/protocol.md) owns rates, counts, seeds, gates and finite revisions.

**Test branches and input selection.** Freeze P and compare shared width 32, four private width-32 branches, shared width 128, four private width-8 branches and four width-32 hash-grouped branches. Semantic-label routing is a supervised reference. Train a separate hidden-to-64-to-four selector on frozen private branches, using only final-answer loss and the last prompt token's pre-branch hidden state. Preserve soft and hard-top-one deployment results and matched routing interventions.

**Constrain functional interpretation.** Change only discount/threshold, compare equal-base-amount orders with different surfaces, add true/wrong/swapped intermediate amounts as information-changing diagnostics, and scale the learned branch by 0/0.5/1. One preregistered final-attention, last-prompt-token position admits at most two candidates: full-vector swap and a rank-one direction estimated from controlled paired differences on diagnostic data. Lock selection before one confirmation evaluation; reject answer-copy and recipient-rule transfer explanations where not separated. No qualified candidate means no identified reuse carrier. No new SAE/CrossCoder is trained.

The auxiliary task retains 32 symbols, four F and four G permutations, their fixed 20/6/6 combination-input split, and all three parent seeds. It tests transfer and U/F/J/S under balanced, unbalanced and exchanged pair exposure; it does not repeat S6 or count as natural-language feature evidence.

## 6. Minimal Falsification Tests

S1 and every S2 component require validation accuracy at least 95%; held-out numerical tests and enriched boundaries are reported separately. Combined-order eligibility requires each family at least 90% and overall at least 95%; S5 additionally requires at least 90% on its low-exposure subset. These are package-defined practical thresholds, not statistical laws.

An S4 policy qualifies as retention only if component macro accuracy falls no more than one percentage point from P, every component remains at least 95%, and combination accuracy falls no more than two points relative to J. S6 benefit requires eligibility and either at least two points higher combination macro accuracy or at least 20% fewer exposures to stable eligibility, without more than one point old-component degradation. Stable speed eligibility requires two consecutive saved points; unreached thresholds are right-censored.

Show every parent seed before means/ranges and paired, numerical-family-clustered uncertainty. A positive point estimate alone does not settle a small effect. Parent failure after the one permitted qualification revision allows a direct P-J feasibility trajectory, while dependent protection/reuse comparisons become NOT_APPLICABLE. If all combined learners fail, retain the prescribed learning comparisons and restrict S6 to shared/oracle qualification rather than declaring routing ineffective. Valid negative, insufficient and not-applicable outcomes all remain deliverable.

## 7. Current Evidence

Task state: **design mapping and implementation preparation**. Question state: **OPEN**. Design state: **V2 bounded execution authorized; runtime freeze and engineering gates pending**. Result state: **NOT RUN** for the V2 order and auxiliary symbolic round at this revision. Researcher mechanism acceptance and question closure: **Unknown**. Runtime facts will be reported in the owning result records; this authorization is not a result.

Historical findings change controls rather than answer this question. [A15_24](../../../experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/summary_cn.md) found no stable low-frequency benefit from a forced high-frequency path. [A15_25_02](../../../experiments/A15/15_25_02_learning_history_representation/20261023/summary_cn.md) restored old accuracy from 0% to 80.88% with a 16-dimensional state difference but required same-question mixed-model donors and did not qualify the CrossCoder reconstruction. [A15_11's H100 sensitivity](../../../experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md) supported a grouping obstruction but no tree or utility-supervision advantage over its matched flat comparison.

[A17_04 R02](../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary_cn.md) found old accuracy 0% after reversed-only learning while mixed supervision could express both rules; exposure differed. [R05](../../../experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/summary_cn.md) did not validate top-coefficient protection, and failed expert-learning prerequisites constrained routing. These are different tasks; this round does not reuse their trained rule state.

## 8. Claim Boundary And Next Decision

R01 and this V2 order round retain distinct Protocols, datasets, exposure budgets and run IDs; shared ownership does not make their symbolic matrices interchangeable. The authorized finite order pipeline can establish bounded task learning, update tradeoffs, exposure effects and branch/selector utility. Correct semantic labels, frozen parameters, zero-output branch identity, linear readability and whole-vector transfer each leave causal alternatives. Internal reuse requires its own qualified, specific intervention. Synthetic orders and permutations do not establish natural-language MoE benefit or an optimal hierarchy.

The next decision is whether the first locked, eligibility-audited V2 results support any link in the proposed chain and which single unresolved link deserves a new hypothesis. Complete the finite authorized matrix or its evidenced qualification branches, audit saved endpoints and deliver observations separately from AI cause analysis; retain negative and Unknown outcomes. Extra experiments beyond the registered revision bounds remain a new research decision.
