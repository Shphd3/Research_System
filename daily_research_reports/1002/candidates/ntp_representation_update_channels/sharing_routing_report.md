# When to share and when to learn separately: models, evidence and current understanding

Revised 2026-10-04 (Asia/Shanghai). This report reorganizes work completed on October 2–3 and retains the temporary candidate location chosen by the researcher. [中文](sharing_routing_report_cn.md) · [Reading guide](reading_guide.md). It explains the current stage of the research. The [Anchor](anchor.md) still owns the scientific design, and the [Protocol](protocol.md) still owns the experiment contract.

**Our current understanding is that separate learning can be useful when different inputs impose different learning demands that an allocation rule can exploit. Whether separation is worthwhile also depends on statistical pooling, the role of common computation, and the additional parameter and computation costs.** We have measured how different updates affect a fixed model and tested whether some of those differences support selection. We have not established that a new MoE improves long-term learning or downstream performance.

The report proceeds through purpose, observations, hypotheses, models and derivations, experimental checks and results analysis, and an update in understanding. Section 4 defines common objects and several restricted comparisons. Together, they do not constitute a theorem explaining the full training process of a language model. Section 5 explains what was measured and which explanations remain viable. Section 6 states how our understanding of the research question has changed, without repeating the numerical tables. The text contains the main argument; links provide the evidence and complete derivations.

## 1. Purpose: learn more with limited resources and retain what has been learned

The research aims to improve learning allocation in a mixture-of-experts model (MoE). When should different inputs update the same parameters, and when should they update separate experts, to improve acquisition of new knowledge and retention of existing knowledge?

Three objects matter. The **shared part** consists of parameters used and updated by multiple input groups. An **expert** is a parameter module that receives samples under an allocation rule and performs part of the computation. A **router** uses currently available input to decide which experts to invoke. Specialization can change the data and update history of each expert. It does not require dividing the input vector into disjoint blocks first.

Greater specialization is not the final measure of benefit. An expert might become worse at other tasks without improving at its own task. A claim that a small expert approaches a large Dense model also needs an explicit resource basis: computation activated for one sample, parameters stored by the whole system, device memory and elapsed time are different quantities. This research reports them separately. It does not choose their exchange rates against loss on the researcher's behalf.

We therefore distinguish four questions: can the architecture represent the target function; can finite training learn it; can subsequent learning retain it; and are those effects worthwhile under specified resources? SAE and spectral analysis are tools for examining representations and effects. They are not the research objective, and no tool is required to win.

## 2. Observations: what needs explaining

First, **the average effect of a shared update can differ from its effect on individual events.** At a fixed S7 state, we used each of four scientific-text domains to produce a small parameter update, then measured actual next-token loss on other texts. Mean loss decreased in all 16 source-domain–receiving-domain combinations. Yet, in every combination, about 44%–53% of events had loss increases beyond the specified resolution band. These are measurements of finite updates, not predictions based only on gradient signs. Average benefit therefore does not mean every text benefits. It remains unknown whether the harmed events form stable tasks that a router can identify. [Initial experiment and conditions](research_report.md)

Second, **some effect differences repeat, but they may be difficult to predict in advance.** Some relative effects persisted when the source texts were replaced by another sample from the same domain. Representations available before the update also improved effect prediction slightly. However, evaluating an effect after observing the actual next token differs from predicting future effects using only an earlier prefix. Prediction under the latter information condition was weaker. The [source-transfer study](source_transfer_addendum.md) and [domain-response analysis](domain_response_structure.md) examine these two levels.

Third, **the ability to predict differences has not consistently produced selection gains over a strong fixed action.** Later cached analyses selected an action from predicted costs, then read the actual finite loss under that action. Several representations outperformed random allocation with matching action-use rates, but did not consistently outperform the fixed action selected on the fitting records. A fixed linear learner using the full input also did not consistently dominate lower-dimensional representations. These observations concern a particular action bank and finite learner, not an MoE whose router and experts have already been trained together.

Existing fresh-S7 training logs also show lower training cross-entropy than Dense in some intervals. Cross-entropy measures prediction error on the actual next token. We abbreviate it as CE; it uses natural logarithms, is measured in nats, and is better when lower. This observation belongs to the existing Dense-backbone training setup. It does not establish a benefit for this round's routing or common/specialized architectures, whose training has not completed.

## 3. Hypotheses: explanations that connect the observations to the purpose

The following restates the explanatory directions in the current design. It creates no new experiment contract or scientific approval.

| Hypothesis | Why it could hold | Equally important rival and distinguishing comparison |
|---|---|---|
| Inputs contain information about the relative utility of candidate computations, which a router can use to improve selection. | Updates from different sources affect the same event differently, and some of these relationships can be predicted from representations available before the target. | A predictor might estimate only difficulty common to all actions, or prefer one generally better action. Compare actual selected loss against strong fixed actions and controls with matching action-use rates. |
| A router can use a representation suited to its decision while experts retain the full input at their interfaces. | Deciding who should compute may require less information than performing the computation. | Compression may work because of lower estimation noise or suitable regularization, without retaining all useful information. Experts can also specialize while receiving identical inputs. |
| Common processing may help limited experts learn through reused computation or pooled data. | Several tasks may repeatedly need the same computation or jointly estimate the same regularity. | A serial structure may benefit from depth or optimization changes. Shared updates may also alter inputs on which old experts depend. Examine acquisition, retention, resources and finite effects through the shared path together. |

These hypotheses do not make a non-supporting result a rejection of the whole direction. A lack of selection gain from the current action bank limits the current selector; experts trained together may develop new differences. Conversely, that future possibility does not turn an unrealized present benefit into an established result.

## 4. Mathematical model: define common objects, then ask bounded questions

### 4.1 Fix the data, model state, computation interfaces and evaluation objects

The raw data consist of an observable prefix and its actual next token, denoted by random variables \(X\) and \(Y\). The data distribution is defined over these objects. Representations inside the model change with its parameters and architecture. Hidden vectors from different models therefore cannot be treated as one fixed data distribution.

Let \(\mathcal A\) denote the architecture: which parameters are tied and shared, which are kept separate, and how common modules connect to experts. Let \(\omega_s\) denote the complete state at training stage \(s\), including parameters, optimizer state and any other state that affects subsequent updates. Given stage data \(D_s\) and fixed or recorded randomness, the training rule is

\[
\omega_{s+1}=\mathcal U_{\mathcal A,s}(\omega_s,D_s).
\]

This equation defines the model. It does not claim that all architectures follow the same learning trajectory. Parameter updates must follow the actual optimizer. Ordinary gradient descent below is an explicitly restricted case.

At a fixed state, the prefix produces a causal state within the layer, \(h=h_{\omega,\mathcal A}(X)\). The router reads \(z=\phi(h)\) and selects an expert \(e=\pi(z)\). Write the expert's input as \(u\): the complete vector at that module's specified interface. A parallel structure may use \(u=h\); a serial structure may use \(u=h+C(h)\), where \(C\) is the common module. The latter supplies only the sum. It does not guarantee recovery of the earlier \(h\). In the old cached study, residual-matrix experts instead read the complete projection input \(c\), while native downstream computation retains the other residual information. These are related computation patterns, but their input tensors are not identical.

Let \(F_{\mathcal A}(\omega,X)\) be the full model prediction and \(\ell\) its loss. The language experiments use CE. Analytical examples may instead use half squared error. Half squared error is not an exact special case of CE; each conclusion retains its own conditions.

To evaluate learning and forgetting, let \(d\) identify the task being evaluated and let \(P_d^{\rm eval}\) be its fixed evaluation distribution. The index \(s\) continues to identify the training stage reached. Evaluation risk is

\[
R_{d,s}=\mathbb E_{(X,Y)\sim P_d^{\rm eval}}
\ell\bigl(F_{\mathcal A}(\omega_s,X),Y\bigr).
\]

Comparing the same task before and after its own training measures acquisition. Comparing its risk just after that training with its risk at later stages measures retention. The evaluation distribution of an old task must stay fixed to attribute changes to the model rather than to a changed task. Aggregating across tasks requires separately specified weights. Here we first retain the complete task-by-stage matrix. Parameters, activated computation and time are recorded separately; they are not directly subtracted from CE.

The following steps hold different parts of this full model fixed. Each change in the comparison is stated explicitly. The equations cannot be chained together without their conditions.

### 4.2 Step one: for a fixed update, who should share its effects?

First fix the other computation and the task weights. Let \(w\) be the parameter group to be updated, and let \(\delta\) be an already specified finite update. The new source task uses \(w+\delta\) under both sharing and separation. Under sharing, old tasks also use the updated parameters. Under separation, the new source receives a private copy with the same initial value, while old tasks continue using \(w\).

Let \(L_d(w)\) be task \(d\)'s risk and let \(p_d\) be its prespecified nonnegative weight in this comparison. The new-source terms are identical and cancel, giving

\[
R_{\rm share}-R_{\rm separate}
=\sum_{d\in\mathrm{old}}p_d\bigl[L_d(w+\delta)-L_d(w)\bigr].
\]

This is an exact finite-step relation. Under these controls, whether old tasks should also receive the update depends on their actual net change. It does not yet include the cost of copying parameters or of future learning, and it does not compare two separately optimized updates.

For a small-step approximation, let \(G_A\) be the source gradient, \(\eta\) the step size, and \(\delta=-\eta G_A\). With old-task gradient \(G_d\) and Hessian \(H_d\), smoothness gives

\[
L_d(w-\eta G_A)-L_d(w)
=-\eta\langle G_d,G_A\rangle
+\tfrac12\eta^2G_A^\top H_dG_A+o(\eta^2).
\]

The first term describes first-order help or harm for a small step; the second describes curvature. Aligned gradients do not guarantee a helpful finite step. For example, suppose two tasks favor scalar parameter values of 1 and 0.1. Moving from 0 to 0.5 helps the first and harms the second, although both initial gradients point in the same direction. Gradient similarity is therefore a local measurement, not a rule for deciding when to learn separately. [Exact examples](sharing_routing_mathematics.md)

### 4.3 Step two: with current computations fixed, what can be selected before the target appears?

Now freeze the model and candidate action bank. Each action \(e\) invokes a fixed computation. In this round's cache, it is a fixed residual matrix operating on its full input. Let \(\ell_e(X,Y)\) be the loss when action \(e\) is forced. Given the complete causal state \(h\) before routing, define the action's conditional risk as

\[
q_e(h)=\mathbb E[\ell_e(X,Y)\mid h].
\]

This is the average loss expected from the action under the information currently available. It is not the loss of a single event after its target is known. Using actual targets to fit the rule during training is valid. The restriction is that deployment cannot inspect the target it is about to predict.

First compare only accepting and rejecting one update. Let its actual loss difference be \(D=\ell_{\rm update}-\ell_{\rm unchanged}\). A rule observing only \(z\) should use \(\mathbb E[D\mid z]\). With no additional cost or joint capacity constraint, it should accept a negative conditional mean and reject a positive one.

This explains why the harmed-event fraction cannot directly specify a routing rule. In a binary CE example, the true target is 1 with probability 0.6. Changing the predicted probability from 0.5 to 0.6 harms the other 40% of events, but lowers mean CE by about 0.02014 nat. If all events have identical information available at routing time, accepting the update for all of them is already the best causal decision. Selecting only events that eventually benefit would require knowing the answer in advance. This counterexample rules out an inference; it does not estimate the causes of harm in the real corpus.

Next compare complete and compressed routing information. For finitely many actions, integrable losses and rules free to select using their respective available information, the optimal risks are

\[
R_h=\mathbb E\min_e q_e(h),\qquad
R_z=\mathbb E\min_e\mathbb E[q_e(h)\mid z]\ge R_h.
\]

Compression preserves ideal risk if and only if some choice based only on \(z\) still selects an optimal action at the complete state almost everywhere. The router need not reconstruct the whole input. It needs to retain distinctions that affect the current expert choice. One sufficient condition is that information removed from action costs contributes only a common offset, leaving the preferred action unchanged.

Experts may still receive complete \(u\). For example, suppose the input contains a numerical value \(\xi\) and an equally likely positive or negative sign \(S\). They are independent, and the numerical value has variance 1. The target is \(S\xi\), and two fixed experts output \(\xi\) and \(-\xi\). The router needs only the sign to choose the expert; the expert needs the numerical value to perform the computation. If the entire computation retains only the sign, numerical variation remains even after conditioning on that sign, preventing zero prediction error. This example shows that the two roles can have different information requirements. It does not prove that every expert must retain uncompressed input.

The inequality above compares unrestricted ideal selection. A fitted learner has finite samples and a fixed function class. More inputs can be harder to estimate from, so worse fitting with complete input does not imply less information in that input. Prediction error is also distinct from selection utility. If two true action costs are \((0,0.1)\), predictions \((1,1.1)\) have a large offset but select correctly. Predictions \((0.1,0)\) have smaller mean squared error but select incorrectly. Experiments must therefore measure the actual loss caused by the final choice. [Complete proof and limits](sharing_routing_mathematics.md)

### 4.4 Step three: once experts learn, why might grouping become useful?

The comparison changes here. Earlier steps fixed one update or one action bank. We now compare different updates produced by shared and separate learning. We can no longer assume that the source-learning term cancels or that old tasks remain unchanged.

Start from a common initial value \(w\). Let \(g(X,Y)\) be the sample gradient and let \(K=\kappa(h)\) be a finite grouping. Fix the grouping before this comparison, using only information available before the target. It does not change with the parameter update being compared. Define the population mean gradient \(G=\mathbb E[g]\), group mean gradients \(G_k=\mathbb E[g\mid K=k]\), and group probabilities \(p_k\). Shared parameters receive \(-\eta G\); each private copy receives \(-\eta G_k\). The two use the same conditional learning rate. Parameter-copying costs are temporarily excluded.

With finite second moments, valid interchange of differentiation and expectation, and sufficient smoothness, the first-order risk improvement is \(\eta\|G\|^2\) under sharing and \(\eta\sum_kp_k\|G_k\|^2\) under separate learning. Using \(G=\sum_kp_kG_k\) and subtracting gives

\[
R_{\rm shared}-R_{\rm private}
=\eta\sum_kp_k\|G_k-G\|^2+O(\eta^2).
\]

This nonnegative first-order term comes from **different mean learning demands across input groups**. Variation in realized sample gradients does not necessarily contribute to it. If all prefixes are identical and targets randomly take positive or negative signs, sample gradients may oppose each other while every causal group still has the same mean gradient. The prefix then provides no basis for assigning different learning responsibilities.

The equation also depends on update normalization. If each private copy instead uses its gradient under the entire population objective, its update includes the group probability \(p_k\), changing the comparison. AdamW histories cannot automatically replace the SGD rule used here. The relation identifies a possible source of benefit; it does not establish that separate learning is always better.

A lack of differences between current experts also does not rule out useful future specialization. Consider a half-squared-error instance of the full model. The complete input is an equally likely positive or negative sign \(S\), and the target is always 1. Two linear experts without biases both compute \(\theta_e S\), starting from \(\theta_e=0\). Initially, either choice incurs loss 1/2, so there is no current selection gain.

Now prespecify an allocation by input sign and update each expert once per round using its group's conditional mean gradient. The sample gradient is \(\theta_e-S\), so the recurrence is \(\theta_e(t+1)=(1-\eta)\theta_e(t)+\eta S\), where \(t\) counts learning rounds. Its solution is

\[
\theta_\pm(t)=\pm[1-(1-\eta)^t],\qquad
R_t=\tfrac12(1-\eta)^{2t}.
\]

For \(0<\eta<2\), risk tends to zero, while both experts always receive the complete input. With its prescribed allocation, restricted function class and symmetric initialization, this example proves only that learning allocation can create useful differences that do not yet exist. Adding a bias lets a single expert solve the problem. The example does not show that a standard MoE automatically learns this routing rule or that separation is generally necessary. A fixed-bank test therefore cannot replace a training comparison. [Complete recurrence and conditions](sharing_routing_mathematics.md)

### 4.5 Step four: with finite samples, when should learning remain shared?

The previous relation uses true population mean gradients and omits estimation error. We now retain the same initialization, fixed grouping, conditional step size and data for both schemes. Each group has a fixed positive integer number \(n_k\) of independent gradient samples. A single gradient within each group has mean \(\mu_k\) and covariance \(\Sigma_k\); samples are also independent across groups. Let \(\mu=\sum_kp_k\mu_k\). Shared learning uses the \(p_k\)-weighted average of the group sample means. Private learning uses each group's sample mean separately.

For an exact finite-step relation, further assume that every group's population risk is quadratic throughout the displacement, with the same positive semidefinite curvature matrix \(B\). Define

\[
V=\sum_kp_k\|\mu_k-\mu\|^2,\qquad
V_B=\sum_kp_k(\mu_k-\mu)^\top B(\mu_k-\mu),
\]

\[
N_B=\sum_k\frac{p_k(1-p_k)}{n_k}\operatorname{tr}(B\Sigma_k).
\]

The norms above are Euclidean norms of parameter vectors, and \(\operatorname{tr}\) denotes the sum of a matrix's diagonal entries. Here \(V\) measures differences in mean learning demand; \(V_B\) measures curvature along those differences; and \(N_B\) measures the extra noise cost of separate rather than pooled estimation. The derivation substitutes the updates into the quadratic risks and uses the identity that the expected quadratic form of a random vector equals the quadratic form of its mean plus the trace of curvature times covariance. The shared mean has noise covariance \(\sum_kp_k^2\Sigma_k/n_k\); the weighted noise contribution to private risk is \(\sum_kp_k\Sigma_k/n_k\). Subtraction yields the factor \(p_k(1-p_k)\), giving

\[
\mathbb E[R_{\rm shared}-R_{\rm private}]
=\eta V-\tfrac12\eta^2V_B-\tfrac12\eta^2N_B.
\]

The first term is the opportunity to exploit different mean demands separately. The other two terms are the finite-step and estimation costs in this conditional model. Evaluation concerns an independent population risk, not the fitting batch just used to estimate gradients.

A half-squared-error example makes the tradeoff concrete. Two equally probable groups have gradient means of plus and minus 1, single-sample variance 4, and common curvature and step size both equal to 1. With one independent observation per group, expected shared risk minus private risk is −0.50, favoring sharing. With four per group, it becomes +0.25, favoring private learning. The true group difference is unchanged; the amount of data changes which form of learning is more reliable. Repeated token exposures cannot substitute for the independent sample count in this example.

Different group curvatures, correlated samples, adaptive optimizers or choosing the grouping on the same data change this contract. The current language experiments have not estimated \(V,V_B,N_B\). The equation is therefore not a validated MoE decision threshold. Resource costs must still be reported separately. Until the researcher specifies how they are valued, parameter counts cannot simply be deducted from this risk difference. [Complete derivation and enumeration checks](sharing_routing_mathematics.md)

### 4.6 Step five: does common computation change representation, estimation or the learning path?

Return to architecture choice in the full model. Common computation may avoid storing the same regularity separately in every expert, or it may pool data from multiple tasks. These are different benefits. The first concerns storage within a specified function class; the second can reduce estimation error without changing the representable function class. Naming a branch “common” does not establish that it has learned reusable knowledge.

A serial connection also changes function composition. Represent the common module and expert \(k\) by linear residual matrices \(C\) and \(E_k\). With \(I\) the identity map, the parallel mapping is \(I+C+E_k\), whereas the serial mapping is \((I+E_k)(I+C)\). Expanding gives

\[
(I+E_k)(I+C)=I+C+E_k(I+C).
\]

If \(I+C\) is invertible, defining the parallel private matrix as \(\widetilde E_k=E_k(I+C)\) gives the same function and preserves matrix rank. Under these linear assumptions and the corresponding rank constraints, a cross term does not guarantee a larger function class. Nonlinear composition may change what finite experts can represent, but additional depth remains an explanation to distinguish.

Identical function classes do not guarantee identical update paths. In the serial structure, changing the common module changes both its output and the input received by the expert. An old expert's function can therefore change even when its parameters are frozen. Now consider an additive scalar special case with fixed old-expert output and half squared error. Let the old combined prediction be \(\hat y_{\rm old}\), its target be \(y\), and its error be \(\varepsilon=\hat y_{\rm old}-y\). Suppose the old expert has compensated for the old common module's error. Increasing the common output by \(\Delta\) increases the combined prediction by the same \(\Delta\), so the old loss changes by

\[
\Delta L=\varepsilon\Delta+\tfrac12\Delta^2.
\]

This additive formula does not directly apply to the serial nonlinear model discussed above. It shows that a more accurate common estimate in isolation need not make the whole old prediction more accurate. We must evaluate the loss of the combined computation. In a language model, the shared backbone also includes Attention, embeddings and normalization. A condition without an extra common FFN is not a condition without any sharing. [Capacity and learning dynamics](capacity_mathematics.md)

The full model now connects current selection, learning updates, finite samples and computation structure through a common set of objects. Each part retains its own assumptions. It does not supply unmeasured causal relationships for the real training process.

## 5. Experimental checks and results analysis: which step does each result support?

### 5.1 How the implementation corresponds to the model

The old S7 analysis fixes the model at 33 billion cumulative training tokens. Here 33B is a token count, not a parameter count. The final-block Attention projection receives a 2048-dimensional input \(c\) and produces a 1024-dimensional output \(a=Wc\). Let \(M_d\) be the mean gradient matrix from a source domain's texts. Its candidate action applies displacement \(-\eta M_dc\). We pass that displacement through the native residual computation, MLP, normalization and vocabulary head to measure actual CE change. No Attention follows this site, so the complete action table supports selection at individual token positions.

Each action here is a fixed residual computation receiving its full input. Selecting different actions across events generally does not correspond to one uniform parameter update, and these actions are not newly trained nonlinear MoE experts. Router features come from history, position and representations available before the target; actual targets are used for fitting and evaluation. Fitting and readout records are separate. The old readout panel has already been exposed, and article-level independence has not been established. The evidence below is exploratory.

| Relation to check in the derivation | Completed corresponding check | Relation still not covered |
|---|---|---|
| How one finite update affects different users | Replay source updates through the native model tail and measure actual CE changes | Net benefit of long-term shared or private training |
| Whether available representations support current action selection | Source transfer, actual finite selection, usage controls and group controls | Effects after joint router and expert learning |
| Whether more complete input improves this learner | Compare eight input families under fixed actions and supervision | Information sufficiency with unlimited samples or a universally optimal routing interface |
| How group differences compete with estimation noise | Quadratic-model derivation and independent enumeration | Population gradient, curvature and noise quantities in language models |
| Whether common and serial computation improve acquisition and retention | Six-arm comparison and mechanism diagnostics implemented; execution state is in Section 5.5 | Architecture benefits and their mechanism after completed training |

Enumeration of mathematical counterexamples checks derivations and computation. It is not validation on natural text. Placing these checks in one table does not make them the same kind of evidence.

### 5.2 Result analysis one: predictable effects do not yet identify separate learning responsibilities

In the initial fixed-source experiment, all 16 source-domain–receiving-domain mean CE changes were negative, ranging from about −0.001953 to −0.000182 nat. An adverse event was defined by \(\Delta\mathrm{CE}>10^{-5}\) nat, and adverse fractions ranged from 43.97% to 52.81%. Each receiving domain contained 256 records with 16 positions per record. This supports coexistence of average benefit and event-level heterogeneity, not a stable separation rule. [Complete finite-response table](evidence/finite_panel_summary.csv)

In the source-transfer test, A and B were two sets of records drawn within each source domain. Relative to the history baseline, the SAE-augmented predictor improved response prediction error by 0.481% [0.383%, 0.574%] for A→B and 0.602% [0.502%, 0.695%] for B→A. Relative error improvement was computed within each source domain and then averaged equally across the four domains. These percentages describe **error in predicting update effects**, not a percentage decrease in language-model CE. Ordinary projections also helped. [Complete source-transfer table](evidence/source_transfer_finite_readout.csv)

Of the error improvement across the two predictions evaluated on their own sources, 99.02% came from the within-domain mean of the A/B responses. This is not the fraction of knowledge common to all four domains, and it does not rule out differences across domains. The subsequent cross-domain analysis specifically corrected this confusion about the object being measured. The result limits a claim that we have already predicted fine differences in learning effects between sources. It does not establish that information about those differences is absent. [Error decomposition](evidence/source_transfer_gain_accounting.csv)

### 5.3 Result analysis two: input-dependent selection information exists, but a strong fixed action remains difficult to beat

The first cached selection study used A/B source actions and previously frozen first-order response predictors. The second used four actions built from all of F-half0, actual finite-CE supervision on F-half1, and a new common baseline. The action bank, labels and baseline changed between the two studies. Their numerical difference cannot be attributed entirely to the input interface.

The second study compared eight feature families: a history/position/norm baseline, plus 64 principal components of the output, preprojection input, post-residual state or combined state; a random output projection; SAE coordinates; or the full combined state. All transformations and linear fitting used only 512 fitting records. Evaluation used 1024 old readout records with 16 positions each. The fixed action was also selected using only actual finite CE on the fitting records.

The table below uses the same four actions with rejection disallowed to explain the distinction between two controls. Here \(x\) is the residual before Attention plus the current Attention output, and \((c,x)\) is the full combined input. Values are in micro-nats, or \(10^{-6}\) nat per selected event. Positive values mean that the first policy has lower loss. These comparisons explain the judgment; they do not select a winner. [All 80 rows](evidence/cached_router_inputs.csv) retain the eight families, both action sets and every receiving scope.

| Comparison | Actual selection gain and conditional 95% interval |
|---|---:|
| x-PCA64 policy versus the fixed action selected on fitting records | +13.94 [−35.76, 62.14] |
| The same policy versus random allocation with matching within-category use rates | +193.62 [147.92, 239.09] |
| Full-(c,x) policy versus the same fixed action | −49.39 [−106.71, 8.49] |
| x-PCA64 policy versus the full-(c,x) policy | +63.33 [9.33, 119.60] |

The within-category random control preserves the policy's action-use rates within each known category to examine matching within groups. It is not another trained category router. Beating this control indicates a usable association in the current input-dependent allocation. The fixed action is already strong, however, so that association may still provide no additional benefit from adopting the policy. In the complete eight-family comparison, every feature-added family beats category-usage random allocation under both action sets. Yet none of the 16 pooled policies provides stable evidence of beating the fixed action selected on finite fitting losses.

Intervals use 2000 category-stratified, paired whole-record bootstrap draws, keeping all 16 positions together. They condition on the fixed sources, fitted learners and old readout panel. They exclude source-population uncertainty and are not corrected for multiple comparisons. A practically acceptable benefit has not been defined. Worse fitting with complete input is consistent with estimation noise, regularization or differences between fitting and readout distributions. It does not establish that the complete interface contains less information. The [execution receipt](evidence/cached_router_inputs_receipt.json) and [independent reconstruction](evidence/cached_router_inputs_audit.json) preserve numerical provenance.

### 5.4 Result analysis three: old training curves provide a separate clue, not evidence for the new routing design

Over 31–33B cumulative valid training targets, existing Dense and fresh-S7 pure LM training CE values were 3.233073 and 3.230724 nat per valid target, respectively, a difference of about −0.002349. These compare the existing Dense backbone and its training configurations. They are not training results for this round's common/specialized design or new router. Later updates are not paired, and neighboring training intervals are not independent seeds.

This observation supports a descriptive claim of lower training CE in the specified interval. It does not establish fewer tokens, less computation or less time to reach the same held-out quality, or improved general downstream performance. The old 21B domain-classification probe measures representation readability; it does not replace general downstream tasks. The [training curve and provenance](evidence/training_curve_20_33b.json) and [training/downstream evidence inventory](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/training_and_downstream_evidence.md) retain the lineage and complete conditions.

### 5.5 New execution facts and scientific results still unavailable

During this rewrite on October 4, we inspected persistent files without modifying them. All times below are Asia/Shanghai. These are local execution records, not a query of current platform state.

- One GPU Smoke attempt for capacity job `pt-uasnh61d` recorded failure at 19:40 on October 3, with training step and valid targets seen both equal to zero. The error reports a Float/BFloat16 dtype mismatch in `index_copy_()`. This records that failure; it does not diagnose its root cause or show that the architecture is ineffective. [Original failure record](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/runs/gpu_smoke_20261003T114015046497Z/common_parallel_continuous/failure_1791027646839763462.json)
- The [scheduler record](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/probe_33b_01/scheduler.json) for exact-33B panel job `pt-meoxfrko` records `COMPLETE_MEASUREMENTS` at 20:25 on October 3. Dense, fresh S7 and SALL each have a `COMPLETE_AGGREGATE` receipt. At this inspection, none of the three models had an `analysis/receipt.json`. This report does not treat saved measurements as completed utility analysis, and draws no update in understanding from the new arrays.

The previous report's Pending observation at 18:44 on October 3 is therefore only a historical snapshot. Numerical interpretations in this report still come from the completed and independently reconstructed old analyses described above. This rewrite establishes no new scientific conclusion about six-arm architecture effects, new-panel utility or general downstream benefits.

## 6. Update in understanding: how we now think about sharing and separate learning

The following is an AI synthesis of the current evidence at this stage. It does not establish a new mechanism or close the scientific question.

**First, learning relationships must be tied to specific computation and state.** Whether a text benefits depends on which update acts on which model state and on the downstream computation through which its effect passes. Domain names can organize comparisons, but cannot directly determine sharing groups. We now have grounds to study these conditional relationships further, rather than labeling a harmed event as a task that should be isolated.

**Second, sharing and separation each have identifiable potential benefits.** Separation can give different parameter responses to different mean learning demands across inputs. Sharing can reuse computation and pool limited data to estimate a common regularity. The conditional derivations show that the choice can change with data quantity, update size and estimation error. The question is which differences deserve separate parameters, not how to maximize specialization itself. We have not measured a complete criterion for language models.

**Third, routing information is valuable relative to differences between experts.** A representation that describes content, predicts the target or reconstructs current activations does not automatically select the right expert. The router needs information about the relative utility of candidate computations. Experts perform those computations and may continue to read the full input at their interfaces. Identical inputs can still support specialization through different parameters and learning responsibilities. Whether compression helps depends on selection quality, estimation difficulty and actual cost together.

**Fourth, current selection and future specialization require separate study.** Fixed-action tests show that some input information has not consistently produced gains over a strong fixed action. This limits the present implementation's utility, but does not rule out training allocation creating expert differences later. Using actual targets to update routers and experts during training is valid. We do not need to predict every local loss change accurately before studying learning allocation.

**Fifth, a common module does not automatically add capacity.** It may save duplicated storage or improve estimation, but it may also change inputs on which old experts rely. Serial coupling can change representation or learning paths; it is not an established necessary condition. If future experiments show improvement, they will need to distinguish reusable common regularities, data pooling, depth and optimization history. If they show deterioration, they must distinguish failure to acquire knowledge from disruption of knowledge already learned.

These five points are bounded updates in understanding. They make the question more specific, but do not identify a winning MoE architecture or require SAE or spectral methods. Two constraints remain on our own interpretation: a strong fixed-action control is not an entry requirement for research on joint training, and lower training CE in the existing S7 does not validate a new routing architecture that has not been trained.

**AI suggestion for the next question:** under explicit resource measures and comparable initial functions, does assigning the same kind of training samples to shared parameters or separately learning experts produce a better acquisition–retention relationship? Can a router learn a useful allocation from visible input alone? The existing capacity comparison first tests tying versus separation under known-domain allocation. The new panel first tests information and utility at fixed states. They provide different evidence, and neither automatically establishes a better learned router. This is a research suggestion, not a new execution contract or closure of the current question.

Complete calculations, individual results and historical attempts remain in the [mathematical explanation](sharing_routing_mathematics.md), [previous report snapshot](history/20261004_before_reading_rewrite/sharing_routing_report.md) and [research process](research_process.md). The snapshot preserves its original bytes; its relative links are interpreted from the original directory. Use this report and the reading guide as the current reading entrypoints.
