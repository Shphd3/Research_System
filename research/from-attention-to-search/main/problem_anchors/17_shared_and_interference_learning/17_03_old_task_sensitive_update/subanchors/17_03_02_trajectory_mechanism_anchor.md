# A17_03_02: Intermediate-state update effects on old-error repair

## 1. Question
Which immediate update effects, at saved intermediate states, are compatible with the smaller old-error repair count in the restricted 100-step trajectory? This refines old_task_sensitive_update; it does not define a new Focus.

## 2. Physical prior
Shared parameters permit both beneficial transfer and competing answer changes. A CE-sensitive subspace is unsigned. A fixed subspace and downstream response can change relevance as training proceeds. These are candidate explanations, not demonstrated functions.

## 3. Falsifiable hypothesis
At intermediate states, removing and amplifying components may give less improvement to initially incorrect old predictions than full updates. The strongest rival is accumulated state/history rather than the immediate operator; generic candidate-probability adaptation and full-vocabulary competitors remain live.

## 4. Model
Use the registered Qwen3 Base and last attention o_proj only. At each ordinary/protected saved state, recompute the CE gradient on the identical next20 training answers. Use the ordinary original next-step norm s as an external shared reference. Define d=-s*g/||g||, u=Q^T*Q*d, v=d-u; compare d, v, and v*s/||v||. Q is the unchanged original rank16 old-CE basis. Paired margins satisfy m_new=b+h and m_old=b-h exactly; b and h are output coordinates, not internal modules. Retain pool mass, pair-access/selection CE, and strongest full-vocabulary competitor margin.

## 5. Computation
First count repairs/losses at saved steps1/16/50/100 relative to the old endpoint. Then restore ordinary and protected states at steps1/16/50; evaluate three independent finite updates per state. No selection of states by new outcomes; all36 state/history cases are measured. Smoke uses four step16 seed29 histories with20 paired dev lists, then independent exact replay. Full uses all400 paired dev lists,108 cells. No cumulative training or new SAE.

## 6. Minimal falsifier
Compare out_norm-full on the originally wrong old subset within each state, then compare that effect across the two histories. Reduced old-margin improvement/repair supports the immediate-operator candidate only locally. Absent, opposite or heterogeneous effects leave the 100-step explanation unresolved. A history contrast includes its gradient and downstream sensitivity and does not isolate a unique mediator.

## 7. Evidence
E01 supplies saved trajectories and output records; E02 supplies qualified restoration and component measurement. This new round is NOT_RUN before submission. Existing dev is exposed, not blind confirmation.

## 8. Boundary and next judgment
Completion means qualified cells, trajectory counts, independent recomputation, actual output registration and bilingual results. It does not require a favorable mechanism. Do not infer rule algorithms, complete trajectory mediation, unavoidable task conflict, expert benefit or natural-text generalization. The user requested completion of round one in this conversation; implementation/smoke/finite full analysis is authorized. Scientific mechanism/closure remains Unknown.


### Completion / 完成

Smoke12/replay4/Full108 qualified; results are heterogeneous. [Summary](../../../../experiments/A17/17_03_old_task_sensitive_update/A17_03_E03_trajectory_mechanism/summary_cn.md) owns factual interpretation. Mechanism/closure Unknown.
