# How local updates connect grouping to learning

[Chinese companion](local_update_model_cn.md).

The objects are the four adapter parameter sets θ_e at a frozen training midpoint, the same donor batch, and subsequent fixed probe inputs. Change only which expert receives each donor input. Probe routes and true targets stay unchanged. Every virtual update resets to the same parameters.

Let G_d,e be the donor's average-loss gradient for expert e, G_p,e the probe gradient for the same parameters, and η the predeclared SGD step size. Under differentiability and a sufficiently small step, the first-order approximation is:

\[
L_p(\theta-\eta G_d)-L_p(\theta)
\approx -\eta\sum_e\langle G_{p,e},G_{d,e}\rangle.
\]

This explains why equal token counts need not produce equal learning effects. Inputs updating the same expert add their gradients; the resulting direction may approach or move away from what the fixed probe needs. This is a local approximation, not a proof that co-occurrence groups reduce conflict. Actual computation includes BF16 terminal projection and a finite step. The deciding readout is measured post-update probe CE, rather than replacing that measurement with an inner product.

More specifically, the single-position gradient of adapter output matrix U_e is b_t(D_e h_t)ᵀ. Here D_e h_t is that expert's low-rank projection of the full input, and b_t is the error signal propagated to the adapter output. Although b_t passes through the frozen norm/head, it still depends on the true next token and current prediction error. The co-occurrence graph uses only the joint distribution of positive activation events and does not contain b_t. Thus two positions with almost identical activation sets can still have opposite update directions because their true targets differ. The bridge from co-occurring inputs to inputs suited to joint updates requires additional evidence; input similarity alone does not establish it.

Within-bin exchange preserves each expert's token count and its coarse D-frequency-bin counts. It changes input-to-expert correspondence and update direction, while potentially also changing gradient magnitude. The second intervention therefore matches each expert's exchanged one-step adapter-parameter displacement L2 norm to the actual update. Hidden/logit displacement and functional-change magnitude are not matched. If a raw contrast disappears under this control, parameter-displacement magnitude is a candidate explanation. This does not identify load as the root cause: norms also depend on difficulty, representation scale, current parameters and gradient cancellation. A surviving contrast gives more direct support for local update direction in parameter space and its finite-step consequences.

R/F/N must also be compared. If every condition similarly favors its own actual routes, generic specialization after training is more consistent with the evidence than a co-occurrence-specific mechanism. A contrast appearing only in R still requires checking seeds, exchange fractions, probe support and actual loads. Each condition is measured at its own midpoint parameters; differences between these states are not same-state causal effects across conditions.

Two explicit bridges remain between structure and learning. After186 groups pass through one-winner selection and K4 mapping, other group scores no longer enter the routing decision. Similar frequency also need not imply similar next-token update requirements. The fraction of unselected score mass is neither representation deletion nor measured information loss: every expert still receives the full h. Consequently, structure beyond marginal frequency and usefulness of this fixed allocation can differ in truth value. Results update judgment about the current bridge without automatically closing every possible use of relationship grouping.
