# Shared Update Directions, Selective Benefits, and the Missing Evidence for Harmful Interference

**Exploratory working manuscript — 27 September 2026**

This manuscript synthesizes the experimental records supplied in `shared_update_reasoning.zip`. It reports no new model runs, no independent reanalysis of raw arrays, and no literature-based novelty claim. Proposed studies are explicitly separated from completed measurements. Source identifiers refer to the accompanying original records.

## Abstract

When does learning from one dataset harm another through shared parameters? We examine three documented experiments that connect representation geometry, sparse-autoencoder directions, and local update consequences. In a fixed S7 checkpoint and a four-domain natural-text panel, distinct representation profiles coexist with beneficial cross-domain mean updates. An intervention on domain-enriched decoder spans supports conditional aggregate selectivity of local learning benefits, but does not identify harmful channels. A subsequent target-oriented reflection experiment controls update norm, distance from the ordinary source update, and source first-order progress. Reflection reduces target benefit relative to matched controls, yet all twelve cross-domain pair means remain beneficial at both tested step sizes. The registered criterion requiring actual target harm is therefore not met. We distinguish structural overlap, selective utility, relative benefit loss, and harmful interference. The remaining mechanistic question concerns data and prediction conditions that produce reproducible, naturally arising incompatible update requirements, rather than whether domains can be separated geometrically. [S1–S3]

## 1. Question and hypotheses

The research objective is to explain how a source dataset's learning changes another dataset's predictions through shared computation, and which data or target conditions determine the sign of this interaction. Domain identity alone is not an adequate mechanism: representations may differ while their required predictive adjustments remain compatible.

The candidate hypothesis is that shared computational use permits interaction, while systematically opposed correction requirements introduce adverse components. Net target harm occurs only when adverse effects outweigh beneficial components and finite-step effects. The strongest competing explanation for the present results is that domain-enriched directions primarily support useful, partly domain-selective adjustments within broadly compatible shared computation. Both explanations permit distinct domain activation profiles; only functional, signed consequences can distinguish them. These hypotheses are conditional on the model state, task, parameter block, and update rule. [T, §§1–3; S2, §2]

## 2. Local definition and theoretical bridge

Let $\theta$ denote a fixed model state and $\delta_A$ an update constructed from source data. Define

$$
I_{A\to B}(\delta_A)=L_B(\theta+\delta_A)-L_B(\theta).
$$

Positive values indicate harm relative to no update; negative values indicate help. Calling the effect interference from effective source learning additionally requires improvement on separate source readout records. An update can be worse than another update while still helping the target. Neither comparison establishes reduced long-run training efficiency, which requires a trajectory and an explicit resource baseline. [T, §1]

For a small update,

$$
I_{A\to B}=g_B^\top\delta_A+O(\|\delta_A\|^2).
$$

Under ordinary gradient descent this becomes $-\eta g_B^\top g_A+O(\eta^2)$. The first-order sign requires a remainder small enough not to dominate. Momentum or adaptive optimization must be analyzed using the actual parameter displacement, not automatically the raw source gradient. [T, §2]

For the selected linear block, let $a=Wc$ and $e=\partial\ell/\partial a$. Here $-e$, rather than $e$, is the local loss-reducing output direction. A single-position gradient contribution satisfies

$$
G=e c^\top,\qquad
\langle G_A,G_B\rangle_F=(c_A^\top c_B)(e_A^\top e_B).
$$

With fixed upstream computation, $\Delta a_B=\Delta W_Ac_B$ exactly. An ordinary source step therefore gives

$$
\Delta\ell_B^{(1)}=-\eta(c_A^\top c_B)(e_A^\top e_B).
$$

Input coupling transmits the update; its alignment with target loss sensitivity determines the first-order consequence. Positive input overlap and opposed correction requirements produce an adverse first-order term. Negative input inner products reverse this sign relation. For batches, the gradient inner product is a weighted sum over all source–target position pairs, not a product of domain-average vectors. These identities organize the mechanism analysis but do not identify the natural data attributes generating the gradients. [T, §3]

## 3. Experimental records and scope

The records use one fresh S7 side-branch checkpoint trained with reconstruction coefficient 0.1 after 21 billion training tokens; this is a token count, not a parameter count. The text panel contains 1,024 records from computing, mathematics, physics, and biology, with two subfields per domain. Each record has 256 tokens. Each domain contributes 128 construction records and 128 readout records. Readouts had been inspected previously, and article-level independence was not established. [D2, §4; D3, §4]

The first experiment observes native final-block attention outputs and the actual input to the final down-projection matrix, while updating the latter. The atom and reflection experiments instead change the final attention output projection, a $1024\times2048$ matrix, so that the observed attention representation lies on the changed pathway. These effects should not be pooled as measurements of an identical intervention. The two later experiments use virtual, norm-normalized updates at relative sizes $10^{-4}$ and $5\times10^{-5}$, reset every branch to the same checkpoint, and evaluate sixteen predetermined next-token targets per record. They are not continuous training runs. [D1, §§2–3; P2, §§C–F and amendment A2; P3, §§7–9]

Reported confidence intervals use 2,000 paired record bootstrap draws stratified by domain and subfield. They condition on the fixed checkpoint, construction gradients, selected directions, and controls. The twelve ordered pairs, control seeds, and two step sizes are not independent experimental replications. [P2, §F; P3, §10]

## 4. Results

### 4.1 Structural separation does not establish harmful interaction

For sentence-mean attention outputs, the first uncentered energy direction accounts for 92.33%, while the squared mean vector accounts for 92.14% of average squared length. After centering, 108 directions are needed for 90% variance coverage; the first two axes explain only 29.42% of centered readout energy. Thus strong raw-energy concentration largely reflects a common mean and is not evidence for one-dimensional semantic variation. [S1, §4.1]

In the first experiment, all twelve cross-domain mean updates help at both step sizes. Individual-record loss increases occur in 31.25%–46.09% of records across cross-domain cells, but their stability under independently estimated source updates was not tested. Average help therefore does not establish universal record-level compatibility, while these single-update adverse records do not yet define a stable harmed subgroup. One full-step computing-source self-improvement interval also crosses zero slightly. [D1, §5]

### 4.2 Domain-enriched spans locate selective benefits

The fixed sparse autoencoder, which represents activations using a sparse set of decoder vectors, has 30,000 atoms. A common atom, 24605, is active at every observed token and accounts for 85.83%–90.50% of the readout domains' squared-coefficient proxy. Across the panel, 14,192 atoms are used. Excluding the common atom and renormalizing the remainder, 700–1,898 atoms are needed to cover 90% of the remaining proxy. These quantities are not additive native-representation energy because decoder directions are not orthogonal. The per-token count of 32 active atoms is imposed by the architecture. [S2, §§3–4]

The functional experiment chooses 32 matchable, frequency-enriched atoms for each domain using construction records. Three control sets approximately match pooled firing frequency and mean squared coefficient. For decoder-span projector $P$, the intervention replaces $\Delta W$ with $(I-P)\Delta W$, with norm restoration in the primary comparison. It removes a component of the update, not the baseline representation or existing knowledge. [P2, §§D–F]

The primary statistic first measures target-relative-to-other-domain benefit loss, contrasts enriched spans against matched spans, and averages over twelve cross-source combinations. It is not a comparison between all common and all domain-specific gradient components.

| Relative step | $M_{\mathrm{atom}}$ | Conditional 95% interval |
|---|---:|---:|
| $10^{-4}$ | $9.416966\times10^{-6}$ | $[5.497630\times10^{-6},1.349434\times10^{-5}]$ |
| $5\times10^{-5}$ | $4.678837\times10^{-6}$ | $[2.707425\times10^{-6},6.740931\times10^{-6}]$ |

Values are in nats per predicted token. The registered aggregate selectivity criterion passes, but the biology-specific interval crosses zero and one cross-source point contrast is negative. Complete updates still help every cross-domain mean at both steps. A separate common-atom-removal branch removes one direction without norm restoration; it is not rank- or treatment-matched to the primary 32-atom interventions. Its full condition-level numerical results are not included in the supplied package. [S2, §4; D2, §§6,12; P2, §F]

The supported interpretation is selective local utility. Under an unscaled removal, worsening target outcomes after removing a direction would instead suggest that the removed component was beneficial, not that it was already causing harm. Norm restoration complicates component attribution further. Neither observation establishes independent atom causality or harmful competition between domains.

### 4.3 Target-oriented reflection weakens help without producing mean harm

Let $u,v$ be unit source and target construction gradients, $\chi=\langle u,v\rangle_F$, and $\gamma$ the update norm. The ordinary and target-reflected updates are

$$
\delta_0=-\gamma u,\qquad
\delta_T=\gamma(-u+2\chi v).
$$

For $0<\chi<1/\sqrt2$, reflection preserves source first-order improvement while making the target construction gradient predict harm. That sign is algebraically guaranteed on construction records, so it is not a discovery about ordinary source-data updates. The empirical question is transfer to other records and the finite-step nonlinear model. Matched reflections control parameter norm, deviation from the ordinary step, and source first-order progress. Targeted deletion is additionally compared against uniform shrinking to the same norm. [T, §§5–7; P3, §§8–10]

| Relative step | Reflection minus matched control, $M_{\mathrm{dir}}$ | Actual target change, $T$ | Shrink minus targeted deletion, $Z$ |
|---|---:|---:|---:|
| $10^{-4}$ | $8.0197655\times10^{-5}$ | $-7.3055722\times10^{-5}$ | $4.4049894\times10^{-5}$ |
| $5\times10^{-5}$ | $4.0176776\times10^{-5}$ | $-3.6642887\times10^{-5}$ | $2.2023582\times10^{-5}$ |

Both steps have positive aggregate confidence intervals for $M_{\mathrm{dir}}$ and $Z$, but negative intervals for $T$. All 152 branches pass source-benefit qualification. All twelve reflected cross-domain pair means remain helpful at both sizes. The registered classification is `INSUFFICIENT_OR_HETEROGENEOUS`, because the joint criterion requiring actual target harm fails. More specifically, the aggregate target-harm prediction is not merely imprecise: its observed sign is beneficial. [S3, §4]

At the larger step, matched controls reduce target loss by approximately 0.0001533; reflection still reduces it by approximately 0.0000731. Targeted deletion restores some benefit rather than rescuing a domain with demonstrated mean harm. The saved first-order decomposition is

$$
-0.00016041014+0.000086804014=-0.000073606124.
$$

The adverse modification cancels 54.11% of original first-order help. Reported aggregate nonlinear-versus-linear discrepancies are 0.7534% and 0.4371% at the two steps. The missing harm is therefore already present in the readout first-order prediction, rather than mainly caused by a finite-step reversal. The records do not identify why the construction-to-readout gradient relation differs. [D3, §§7,10]

## 5. Causal interpretation and limitations

The three experiments establish different links: structural description, conditional selective utility, and the consequences of an engineered directional change. They must not be collapsed into a completed causal chain from semantic distance to conflict and reduced training efficiency.

“Common direction” is particularly ambiguous. Common activation, overlap of update support, and the arithmetic mean of two gradients are different objects. Opposed components can occupy the same computational direction yet cancel in a gradient mean. A domain-enriched decoder direction also need not be domain-exclusive. The existing primary atom contrast neither decomposes gradients into exhaustive common/private parts nor compares their independent causal importance. [P2, §§D–F; T, §8]

The engineered update uses target construction gradients, while ordinary source data do not generate that reflected step. Source-progress matching is exact only to first order on construction records; parameter-norm matching does not equalize every representation displacement. The deletion/shrink comparison matches norm, not source progress. These constraints narrow, rather than invalidate, the observed relative directional effects. [T, §§6–7; D3, §9]

The package contains textual records and provenance metadata, but not implementation files, raw arrays, or referenced figures. Consequently, this manuscript audits reported definitions and results rather than independently reproducing them. Historical readout exposure, unestablished article independence, a single checkpoint, and conditional intervals further limit generalization. Long-run optimizer dynamics, isolation benefits, and independent interference prediction were not tested. [D2, §§4,10–13; D3, §§4,12,14]

## 6. Proposed next discriminating study

The next question should be whether a pre-specified data and prediction condition makes an **ordinary** source update both improve its source and reproducibly harm separate target records. Before new training, existing arrays should be inspected for construction/readout gradient stability and the decomposition of baseline help versus the adverse directional shift. The existing eighteen analytic cases validate equations; repeating them is not a new empirical test. [T, §4; D3, §10]

A new controlled dataset should vary input reuse and prediction compatibility without choosing conditions from observed target harm. Construction and untouched readout records should be separated, with article-level separation where applicable. If identical visible inputs are assigned contradictory targets as a positive control, this is an explicitly artificial target contradiction, not evidence that natural semantic distance causes interference. Direction-removal claims require matched controls and retained source learning.

Stable harm with the predicted separating effects would justify studying an independent detector. Continued help would instead motivate explaining beneficial transfer or explicitly studying adverse components beneath net help. Unstable signs or failed source qualification leave the mechanism unresolved; they do not justify selecting only adverse examples. Sparse-autoencoder-based prediction and budget-controlled training methods come after this evidence, not before it. This section is a proposal, not an executed experiment.

## 7. Figure strategy

Three complementary displays are needed. First, show domain records in one construction-fitted representation coordinate system, with empirical projected distributions and separate centered-variance and uncentered-energy spectra. Second, show atom frequency and squared-coefficient profiles under one fixed construction-derived order; domain-specific resorting cannot support comparisons of atom identity. Third, connect a frozen orthonormal output basis to signed local consequences:

$$
h_{A\to B,j}=\mathbb E_B[(q_j^\top e_B)(q_j^\top\Delta a_B)].
$$

Positive terms increase first-order loss; negative terms decrease it. Derivative and aggregation conventions must agree, without double-normalizing the sixteen-target mean. Include the residual subspace when only selected axes are shown, and plot actual loss changes against a zero baseline. This decomposition is a proposed diagnostic derived from the local framework, not a completed new finding. [T, §3]

A sample distribution over a coordinate value, an atom-usage profile over identifiers, and a ranked energy spectrum have different horizontal axes. None establishes that each semantic group has a Gaussian profile over atom indices. Existing atom results instead show a dominant shared component and a broad remainder. [S2, §4]

For longitudinal analysis, a frozen reference encoder, dictionary, and ordering preserve measurement identity, while reconstruction and scale drift must be monitored. Separately trained dictionaries require explicit direction/response matching with ambiguous, split, merged, and unmatched atoms retained. Coordinate comparability alone does not establish stable semantic identity or explain a training mechanism. These are proposed measurement conventions, not completed longitudinal results.

## 8. Conclusion

The documented evidence supports domain-structured representations, conditional domain-selective update benefits, and directional modulation of cross-domain help. It does not establish that common directions cause harmful interference or that domain separation improves training efficiency. The strongest knowledge update is that structural distinction and selective utility can coexist with net cross-domain benefit. The next mechanism test should address independently defined data conditions producing reproducible ordinary-update incompatibility; only then should geometric signals be evaluated as interference detectors and used to motivate training methods. [S1–S3]

## Source records

- **S1:** [Native structure and one-step updates, Chinese summary](sources/shared_update_reasoning/experiment_copies/20260926_structure_update/summary_cn.md).
- **D1:** [Native structure and one-step updates, detailed record](sources/shared_update_reasoning/experiment_copies/20260926_structure_update/detailed.md).
- **S2:** [Atom usage and update channels, Chinese summary](sources/shared_update_reasoning/experiment_copies/20260926_atom_mechanism/summary_cn.md).
- **P2:** [Atom intervention protocol](sources/shared_update_reasoning/experiment_copies/20260926_atom_mechanism/protocol.md).
- **D2:** [Atom intervention detailed record](sources/shared_update_reasoning/experiment_copies/20260926_atom_mechanism/detailed.md).
- **S3:** [Controlled directional conflict, Chinese summary](sources/shared_update_reasoning/experiments/20260926_direction_conflict/summary_cn.md).
- **P3:** [Controlled directional conflict protocol](sources/shared_update_reasoning/experiments/20260926_direction_conflict/protocol.md).
- **D3:** [Controlled directional conflict detailed record](sources/shared_update_reasoning/experiments/20260926_direction_conflict/detailed.md).
- **T:** [Supplied theoretical derivation](sources/shared_update_reasoning/03_theory_derivation_cn.md).
