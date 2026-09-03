---
story_id: A15_spectral_representation_to_functional_routing
status: current_primary_synthesis
updated: 2026-08-15
canonical_language: en
companion_cn: 02_spectral_representation_to_functional_routing_cn.md
---

# From Spectral Redistribution To Target-Conditioned Layer Innovation

## 0. Terminology And Definitions

| Term | Concrete meaning in A15 | What it does not mean |
| --- | --- | --- |
| old token-local state | the state available at the token before the current attention write | all information available in the full sequence |
| layer update | the actual change induced at a named representation site | knowledge proved to be absent before the layer |
| actual $\Delta n_\ell$ | $RMSNorm_\ell(h_\ell+a_\ell)-RMSNorm_\ell(h_\ell)$ at the MLP-input site | raw attention output or causal MLP use |
| layer-added information | a target-conditioned improvement beyond the old token-local state on held-out data | larger variance, a covariance difference, or a later spectral rank |
| local spectral rank | a position in a basis recomputed and ordered within one layer | the same direction in another layer |
| direction identity | reproducible projector overlap in a common ambient coordinate system | semantic meaning or function |
| functional use | a controlled change in task loss or expert-relative utility caused by retaining, removing, or replacing a candidate signal | linear readability alone |
| exact transition $U$ | $Z-X$ for the same token, hook, normalization, and hidden coordinate | new knowledge by definition |
| conditional residual update $R_U$ | the part of $U$ not linearly predicted from the old state $X$ under the frozen residualizer | every nonlinear distinction absent from $X$ |
| conditional innovation matrix $K_{new}$ | a supervised operator selecting target-residual directions in $R_U$ | a matrix containing knowledge or a deployable Router |
| representation effective rank | the entropy effective rank or 80%-variance rank of a named update covariance | the rank needed to retain target-readout gain |
| common activation basis | one eigensystem fitted from equal-layer, trace-normalized TRAIN covariances of the matched long-range update | a parameter basis, target-sufficient basis, or Router coordinate |

## 1. Abstract

A15 began from a routing intuition: different Transformer layers may expose
different information, so a useful Router may need layer-specific inputs. The
line has established bounded facts about covariance access, learning speed,
semantic redistribution, and routing interventions. A15_08 now also supplies
one eligible definition-and-existence result for information added by a named
layer transition beyond its old token state.

The method has three audited roles, not three competing definitions. A
TRAIN-only pooled basis is a side diagnostic that puts matched old and new
states in one descriptive coordinate. The decision chain then records the
exact normalized attention transition $U=Z-X$, residualizes $U$ against $X$,
and requires fresh held-out target gain beyond the old-state readout and
target-independent same-budget controls. Only this decision chain adjudicates
added accessibility; the common basis and raw difference cannot do so alone.

A15_02_06 separates the former descriptive pipeline into four steps: audit
coordinate dependence with two parameter-only common bases; compare each
layer's Attention-write variance in the frozen Mean Response basis; compare
coarse, medium, and fine rank centroids plus same-layer curve shapes; and scan
all adjacent layers. The depth shift is basis-sensitive, the granularity order
is trajectory-level, the shape difference is distributed rather than one
continuous band, and adjacent signs alternate. Fixed-band study is therefore
removed from the route, while the common basis remains a descriptive ruler.

E03 cannot carry that conclusion: a final cold read found missing namespaced
`episode_id` and `map_id`, structured extraction receipts, complete simple
episode/bootstrap arrays, and a full registered-family manifest. Its numbers
are diagnostic only. E04 is the fresh conformance-only repair and the first
eligible result. On the controlled two-hop target, the full residual update
gives $0.767207$ nats/example of held-out gain
$[0.751296,0.785146]$. The registered two innovation directions are non-null
but retain only 33.24% of the gain, so rank-two sufficiency H1' fails. The
meeting's global low-rank H1 remains untested, and this local result does not
establish native use or Router value. The researcher has parked the local
task-readout-rank ladder. The active submitted child question asks whether
long-range-specific added accessibility strengthens across registered blocks 2--36 and
how the matched interaction update's representation rank changes in one
activation-derived common basis.

## 2. Research Question

The root question is:

> Relative to the token-local state available before a named layer write, what
> target-relevant distinction becomes newly accessible after that write, and
> what separate evidence would show that the model or a Router uses it?

This question contains two clauses that must not be collapsed:

1. **incremental accessibility:** does the update improve held-out prediction
   of a frozen target beyond the old state under a named readout family;
2. **functional use:** does a controlled intervention on that update change
   task loss, expert-relative utility, or another registered functional target?

The first clause is now answered for one controlled layer-25 attention
transition and linear readout family. The second clause remains downstream.
The current direction extends the first clause across depth; it does not yet
test task-sufficient retrieval rank and does not train or evaluate a Router.

## 3. Why This Question Is Confusing

Five different observations have repeatedly been called “new information”:

1. a nonzero residual update;
2. a change in covariance or spectral shape;
3. a semantic label readable from the update alone;
4. a semantic label more readable after adding the update to the old state;
5. a signal whose intervention changes model or expert function.

Only items 4 and 5 can answer the present research question, and they answer
different parts of it. A nonzero update is a computational fact. A covariance
change is a second-moment fact. Update-only readability can be redundant with
the old state. Functional use requires an intervention or a loss-aligned
counterfactual target.

The ambient residual-stream coordinates are shared across blocks, so a vector
difference is algebraically meaningful when token, hook position, and
normalization site are matched. The eigenbases fitted separately in each layer
are nevertheless different. Subtracting equal rank indices compares two
ordered profiles, not two identified directions.

Two subtraction objects must not be conflated. At matched raw residual
boundaries, $r_{\ell+1}-r_\ell$ is the exact full-block write. By contrast,
$RMSNorm_{\ell+1}(r_{\ell+1})-RMSNorm_\ell(r_\ell)$ also changes the
layer-specific normalization map. For the attention-to-MLP question, the
clean within-layer object applies the same $RMSNorm_\ell$ to the matched states
before and after the attention write, as in the actual $\Delta n_\ell$ below.

## 4. Data And Evidence Layout

| Evidence block | Object | Decision already supported |
| --- | --- | --- |
| A15_00 | actual Router input and trained Gate | non-uniform spectral access; head preference is not raw-energy-only |
| A15_01 | controlled Gate learning and feedback | covariance scale changes finite-time learning speed; real-transfer claim remains bounded |
| A15_02 | frozen Qwen3-8B states, two parameter-only common bases, and attention-induced updates | Mean Response gives coarse < medium < fine, but depth shift is basis-sensitive, shape differences are distributed, and adjacent changes are non-monotonic; no universal fine-specific rank law or conditionally new linear signal is established |
| A15_04 | local and cross-layer MLP parameter spaces | local relocation is not a shared semantic tail; stable terminal geometry is decoupled from increasing late conditional-fine occupancy |
| A15_05 | compatibility and matched fixed-band dispatch | changing geometry or dispatch does not by itself provide functional admission |
| A15_06 | online local/relay spectral routing | covariance-rank identity has no reproducible cross-seed functional advantage |
| 2026-08-10 variance-interval audit | residual/input and raw attention output projected onto layer-local parameter ranks | the selected variance-growth interval does not reliably localize a domain-discriminative subspace and cannot define new information |
| A15_08 | one normalized layer-25 attention transition, conditional residual update, and fresh held-out target readouts | E04 is the first eligible local added-accessibility Pass; registered rank-two sufficiency fails at 33.24% retention |
| A15_08_01, E02 result | matched one-hop/two-hop by near/far worlds, blocks 2--36 normalized attention updates, and an activation-derived common basis | eligible typed Fail: $T_{depth}>0$ but $A_{2F}<0$; representation rank non-monotonic and descriptive only |

These blocks use different models, representation sites, targets, and
coordinate systems. Their results constrain one argument but must not be
treated as one pooled experiment.

## 5. Physical Intuition

A deterministic layer transforms and aggregates information already present
in the preceding full model state. It need not create information in the
strict Shannon sense. For a token-local Router, however, attention may make
contextual distinctions newly available at that token or make an existing
distinction easier for a restricted readout to access.

The useful intuition is therefore not “deep layers contain more variance” but:

> a layer update may reorganize or import context so that a target-relevant
> distinction becomes accessible beyond the old token-local state.

Representation rank is a separate geometric hypothesis. It may be measured on
the same frozen updates, but it remains descriptive until a threshold is
approved and cannot replace the held-out gain test. Task-sufficient compression
is a further question and is currently parked. Spectral location is never the
definition of added accessibility.

## 6. Definitions And Metrics

For a pre-attention residual $h_\ell$ and attention write $a_\ell$, define

$$
n_\ell^{old}=RMSNorm_\ell(h_\ell),
\qquad
\Delta n_\ell=RMSNorm_\ell(h_\ell+a_\ell)-n_\ell^{old}.
$$

$\Delta n_\ell$ is a concrete computational update at the MLP-input site. It
is not, by definition, new semantic information.

For a frozen target $Y$ and readout family $\mathcal F$, define held-out risk
$\mathcal R_{test}$. A candidate incremental-accessibility quantity is

$$
G_\ell(Y;\mathcal F)
=
\mathcal R_{test}\!\left(f_0(n_\ell^{old})\right)
-
\mathcal R_{test}\!\left(f_1(n_\ell^{old},\Delta n_\ell)\right),
$$

where fitting and model selection exclude the test data. $G_\ell>0$ means the
update adds predictive value under the named target, readout family, and data
split. It cannot prove information-theoretic novelty or native model use.

A functional metric must separately compare an intact computation with a
matched intervention on the candidate update. Its unit and target depend on
the approved question: task loss for semantic function, or counterfactual
expert regret for routing function. Readability cannot substitute for this
intervention.

For the executed A15_08 object, the same layer-25 post-attention normalization
is used on both states:

$$
X=N_{25}(h),\qquad Z=N_{25}(h+a),\qquad U=Z-X.
$$

The historical E04 label-free common basis $V_{pool,E04}$ is fitted from TRAIN-only pooled,
episode-centered $X$ and $Z$. It describes where old state, new state, and
update variance lie; it does not decide novelty. The decision-bearing update is

$$
R_U=U-\widehat{\mathbb E}_{lin}[U\mid X],
$$

For centered one-hot target $Y_c$, also define

$$
R_Y=Y_c-\widehat{\mathbb E}_{lin}[Y_c\mid X].
$$

The concrete confirmation gains are

$$
G_{true}=CE(f_X(X))-CE(f_X(X)+g_{full}(R_U)),
$$

$$
G_{state}=CE(f_X(X))-CE(f_Z(Z)),\qquad
G_2=CE(f_X(X))-CE(f_X(X)+g_2(P_2^{\top}R_U)).
$$

All are nats/example and positive means lower held-out loss. Let
$Q_{mis},Q_{random},Q_{perm}$ be the higher-method 95th percentiles across the
64 matched control families inside each paired episode bootstrap draw. Then

$$
T_{cap}=G_{true}-Q_{mis},\qquad
D_{80}=G_2-0.8G_{true},
$$

$$
T_{random}=G_2-Q_{random},\qquad
T_{perm}=G_2-Q_{perm}.
$$

H2 requires positive lower 95% bounds for $G_{true}$, $G_{state}$, and
$T_{cap}$. Gated H1' requires positive lower bounds for $D_{80}$,
$T_{random}$, and $T_{perm}$; a nonpositive upper bound for any one yields
H1' Fail. These metrics establish bounded linear accessibility, not native use.

The active A15_08_01 proposal reuses the within-layer identity at every block,
but it does not reuse the E04 task-rank ladder. For condition
$c\in\{1N,1F,2N,2F\}$, let $G_{\ell,c}$ be the held-out cross-entropy reduction
from adding a frozen correction based on $R_{U,\ell,c}$ to the frozen old-state
readout. Define the necessity-by-distance interaction

$$
I_\ell
=(G_{\ell,2F}-G_{\ell,2N})
-(G_{\ell,1F}-G_{\ell,1N}).
$$

The proposed primary contrast compares the median $I_\ell$ in blocks 25--36
with the median in blocks 1--12. All 36 $G_{\ell,c}$ and $I_\ell$ values must
still be plotted; adjacent-layer differences are descriptive slopes, not
independent samples.

## 7. Mathematical Model

Let centered old state be $H$ and centered layer update be $U$. If the next
state is $H'=H+U$, then

$$
\Sigma_{H'}-\Sigma_H
=
\Sigma_U
+\operatorname{Cov}(H,U)
+\operatorname{Cov}(U,H).
$$

The covariance change contains the update variance and two signed cross terms.
It is generally not positive semidefinite and is not the covariance of “new
knowledge.” Even $\Sigma_U$ is only the covariance of the computational update;
calling it new information still requires a target-conditioned comparison.

If each layer separately diagonalizes a covariance or parameter operator,

$$
K_\ell=V_\ell\Gamma_\ell V_\ell^\top,
$$

then rank $j$ in $V_\ell$ and rank $j$ in $V_{\ell+1}$ are not an identified
pair. Eigenvalue or rank-profile differences describe spectral redistribution.
Projector overlap or principal angles in the common ambient coordinates are
needed for direction identity, but they still do not establish semantics or
function.

For centered target residual $R_Y$, A15_08 defines

$$
K_{new}=C_{UY}S_Y^+C_{UY}^{\top},\qquad
C_{UY}=n^{-1}R_U^{\top}R_Y,\qquad
S_Y=n^{-1}R_Y^{\top}R_Y.
$$

Generalized eigenvectors of $K_{new}$ against $\Sigma_{R_U}+\rho I$ are valid
supervised candidate directions. $K_{new}$ is a selector, not the new knowledge
itself. Only fresh held-out gain can admit the resulting coordinates. A15_07's
different cross-expression discriminant proposal remains parked unrun.

A15_08_01 deliberately does not extend those generalized directions. Within
each matched world and target it instead defines the target-label-free
long-range interaction update

$$
D_\ell
=(R_{U,\ell,2F}-R_{U,\ell,2N})
-(R_{U,\ell,1F}-R_{U,\ell,1N}).
$$

After within-world target centering, let $\Sigma_{D,\ell}^{tr}$ be its TRAIN
covariance. Its full eigenspectrum yields entropy effective rank and the rank
capturing 80% of variance. Cross-layer comparison uses the proposed common
activation operator

$$
\Sigma_{common}
=\frac1{36}\sum_{\ell=1}^{36}
\frac{\Sigma_{D,\ell}^{tr}}{\operatorname{tr}(\Sigma_{D,\ell}^{tr})},
\qquad
\Sigma_{common}=V_{common}\Lambda_{common}V_{common}^{\top}.
$$

Trace normalization prevents one high-energy layer from owning the basis, and
equal layer weight treats depth symmetrically. A layer's cumulative energy in
the frozen common rank is descriptive representation geometry; it is not a
directionwise decomposition of $G_{\ell,c}$.

## 8. Proposition State

**Proposition 1 — residual subtraction.** At matched residual-stream hook
positions, $h_{\ell+1}-h_\ell$ or a named $\Delta n_\ell$ is a valid
computational difference. It is not automatically a knowledge difference.

**Proposition 2 — covariance subtraction.** A covariance difference mixes
update variance with old-update cross terms. Its eigenvectors cannot be called
new-information directions without an additional target-conditioned test.

**Proposition 3 — layer-local rank.** Similar layer-local spectral profiles do
not imply common directions. Common directions do not imply common semantic or
functional roles.

**Proposition 4 — conditional accessibility.** Positive held-out incremental
risk reduction licenses only a target-, decoder-, and dataset-bounded claim.
Functional use remains a separate clause.

**Proposition 5 — current bounded result.** In the first eligible record, E04,
the registered controlled two-hop target and layer-25 transition have positive
conditional accessibility beyond old-state and same-budget rivals. Two
registered directions are useful but not sufficient: they retain 33.24%,
below the frozen 80% gate. E03 is an ineligible qualification lesson, not
support for this proposition.

**Proposition 6 — current submitted extension.** A matched necessity-by-distance
interaction can separate generic relocation and generic two-hop effects at all
36 blocks, while a pooled TRAIN activation basis makes their update spectra
descriptively comparable. The design and one four-GPU run are approved and
submitted; no depth law or low-rank conclusion exists before eligible evidence
is complete.

These are bookkeeping propositions, not a theorem that deep layers contain or
do not contain new semantic information.

## 9. Mechanism Decomposition

The clean causal order is:

$$
\text{parameter-common-coordinate audit}
\rightarrow
\text{Attention-write variance spectra and granularity shape}
\rightarrow
\text{descriptive semantic geometry}
\not\Rightarrow
\text{layer-added information}.
$$

The decision-bearing order is:

$$
\text{old token-local state}
\rightarrow
\text{named layer update}
\rightarrow
\text{incremental target accessibility across depth}
\quad + \quad
\text{descriptive representation-rank trajectory}
\rightarrow
\text{optional task-sufficient retrieval test}
\rightarrow
\text{functional intervention}
\rightarrow
\text{Router design}.
$$

Skipping a stage creates the recurring A15 error: variance is treated as
information, information as direction identity, direction identity as
function, or function as training benefit.

## 10. Evidence From Anchors

| Parent | Safest current reading | Route implication |
| --- | --- | --- |
| A15_00 | the trained Gate preferentially accesses transferable high-variance structure while retaining weaker non-head access | access geometry is real but not a semantic selector |
| A15_01 | covariance anisotropy causally biases finite-time learning in controlled systems | formation speed does not select a useful target |
| A15_02 | Mean Response gives coarse < medium < fine, but depth shift is basis-sensitive, coarse/fine shapes mostly overlap, and adjacent changes are non-monotonic | retain the common basis for description; stop using rank location, fixed bands, or normalized variance as added information |
| A15_04 | shared tail and narrower terminal-tail semantic-entry explanations are closed for the registered objects | parameter stability is not semantic chronology |
| A15_05 | fixed bands fail compatibility or matched quality admission | changed dispatch is not useful dispatch |
| A15_06 | local spectral methods have seed-specific effects but no reproducible covariance-identity certificate | do not back-project a method point estimate into band semantics |
| A15_07 | technically specified, parked by the researcher, and unrun | preserve as a distinct inactive proposal; it does not own A15_08 |
| A15_08 | E04 is the first eligible local H2 Pass and rank-two H1' Fail; A15_08_01 E01 is standardization Insufficient and E02 is `H2_LC_FAIL_CONTROL_DEGRADATION` | decide whether direct absolute $G_{\ell,2F}$ should replace interaction growth; task rank and function stay parked |

## 11. Decisive Experiment Evidence

The A15_02_06 common-coordinate sequence contains one positive and one negative
result. The fine-only centroid increases by $+0.03171$ from early to late depth
in the Mean Response basis, whereas Rank Consensus gives $-0.00755$ with an
interval crossing zero, so the depth shift is basis-sensitive. Once Mean
Response is frozen, coarse, medium, and fine have ordered trajectory-level
centroids and fine-minus-coarse is $+0.008175$. Yet same-layer coarse/fine
curves mostly overlap: the average difference is a loss of head share plus
small, distributed increases at many later locations, not one continuous fine
band. Across all 35 adjacent transitions, 16 are positive, 11 negative, and 8
unresolved. This supports a conditional association between parameter-response
rank and semantic granularity, not variance redistribution as added information.

At actual $\Delta n$, the balanced taxonomy audit found reliable
conditional-fine residuals but a fine-minus-coarse late-minus-early rank shift
of $-0.009573$ with a wholly nonpositive registered interval. In the matched
ten-layer taxonomy run, the update was readable alone while its linear gain
beyond the old state was approximately zero. This is direct evidence that
update-only readability and conditional novelty are different objects.

The shared-tail audit reproduced local rightward redistribution but found
global shared-tail enrichment decreasing from early to late depth. A later
pre-fixed terminal-width audit found above-random cross-layer parameter overlap
at widths 128, 256, 512, and 2,048, while conditional-fine enrichment decreased
at every width. Stable parameter geometry therefore does not track late
semantic entry.

Fixed-band matched dispatch changed routes by 4.98%--21.88%, yet every true
band had worse held-out next-token loss than the full native Router. The
motion-matched online control also failed to show a reproducible advantage for
covariance-rank identity across two seeds.

The 2026-08-10 variance-interval audit found raw attention-output variance only
0.060--0.140 times the residual/input variance in selected intervals and no
stable domain-probe advantage over equal-dimensional random directions. This
closes that variance-growth selector. It does not falsify layer-added
information, because variance magnitude and source-domain prediction are not
necessary measures of target-conditioned novelty.

A15_08 then evaluated the target-conditioned object directly. E01 was
scientifically ineligible because its cyclic control was an invertible target
relabeling. E02 repaired that algebra but opened confirmation labels before the
selection freeze, so its numbers remained diagnostic. E03 froze the intended
scientific choices before fresh confirmation, but its final qualification
cold read found four missing Protocol contracts: namespaced `episode_id` and
`map_id`, structured extraction receipts, complete simple episode/bootstrap
arrays, and a full registered-family manifest. E03 is therefore
`INELIGIBLE_GUARD`; all of its numbers are diagnostic only.

E04 is a fresh conformance-only repair: it leaves the E02-frozen scientific
object, readouts, directions, rank, thresholds, control families, and decision
rules unchanged while completing those four contracts. It is the first
eligible `H2_PASS_H1_FAIL` record. On 128 complex episodes,
$G_{true}=0.767207$ $[0.751296,0.785146]$,
$G_{state}=0.754508$ $[0.738226,0.773069]$, and
$T_{cap}=0.766839$ $[0.750643,0.784307]$, so local H2 passes. The two
directions give $G_2=0.255052$ $[0.244938,0.264427]$, retaining 33.24% of
the full point gain. Their $D_{80}=-0.358713$
$[-0.369760,-0.348675]$ fails the registered 80% gate. Positive
$T_{random}=0.034265$ $[0.024293,0.040979]$ and
$T_{perm}=0.234832$ $[0.224277,0.244831]$ show that the pair is non-null
under the two registered equal-rank controls, but neither can rescue rank-two
sufficiency.

The separate E02 TRAIN-only common-basis diagnostic explains why variance-
first selection was misleading; it is descriptive and is not an E04
eligibility gate. Complex update variance puts 98.41% of its mass in pooled
ranks 1--256, while the two target-conditioned candidate directions put only
37.90% there and reach median mass at rank 374. The seven nonzero $K_{new}$
eigenvalues are nearly flat enough that the first two hold only 31.17% of their
total. The safe update is not “new information lives in the middle”; it is that
raw update energy is head-concentrated while target-related candidate geometry
is much more distributed, and the full functional location remains unresolved.

## 12. Counterexamples And Rival Explanations

- **Small variance, unique signal:** an update can have low variance yet change
  a target decision consistently. Variance magnitude cannot rule it out.
- **Large variance, redundant signal:** an update can be easily decoded alone
  while adding no predictive value beyond the old state.
- **Stable spectrum, rotating directions:** similar rank profiles can coexist
  with near-orthogonal raw directions.
- **Stable directions, changing semantics:** a shared parameter subspace can
  remain geometrically stable while semantic occupancy decreases.
- **Semantic separation without function:** a supervised discriminant can
  classify child labels yet fail to predict task or expert utility.
- **Functional effect without spectral identity:** a useful intervention need
  not align with a preselected covariance band.

Eligible E04 excludes the registered same-budget target-independent rival for
this local linear object. E03 excludes nothing scientifically because its
record is ineligible. Nonlinear novelty, native use, and transfer remain live
rivals outside the present claim.

## 13. Claim Boundary

**Established:** A15 has a real spectral access and learning-dynamics object;
semantic representations change with layer; layer-local rank, shared parameter
geometry, fixed-band dispatch, and variance growth are not sufficient
definitions of new or useful information. For one registered layer-25
transition, eligible E04 establishes target- and linear-family-specific added
accessibility and rejects registered rank-two sufficiency. E03 supplies only a
qualification lesson and diagnostic pattern.

**Not established:** a universal deeper-versus-shallower law, that the whole
representation is low or high rank, that the increment is generally long-range
or fine-grained, that direct state or covariance subtraction alone isolates
knowledge, that any direction is natively used, or that a layer-specific Router
improves expert function.

The A15_08_01 chain is now adjudicated. E01 exposed a structural-null block-1
old state and closed as `H2_LC_INSUFFICIENT_STANDARDIZATION`. E02 evaluated
blocks 2--36 and passed all validity guards. It found positive
$T_{depth}=0.006102$ $[0.004119,0.007669]$ but negative
$A_{2F}=-0.011422$ $[-0.013994,-0.009812]$, so the registered verdict is
`H2_LC_FAIL_CONTROL_DEGRADATION`. Representation rank is non-monotonic and
descriptive only.

**Do not infer:** $\Sigma_U$ is automatically new-knowledge covariance,
conditional-fine labels are the correct routing target, or failure of a
variance selector means no layer-added signal exists.

## 14. Anchor Decomposition And Current State

- A15_03 was never run and is now archived outside the active route; band
  location is no longer a planning node.
- A15_04 remains closed for shared broad-tail and pre-fixed terminal-tail
  semantic-entry claims.
- A15_07 remains `parked_by_researcher_unrun` with no scientific verdict.
- A15_08 is the active parent. E01, E02, and E03 are ineligible evidence-
  qualification records; E03 specifically remains `INELIGIBLE_GUARD` because
  the frozen identity and record-completeness contracts were not instantiated.
  Fresh conformance-only E04 is the first eligible `H2_PASS_H1_FAIL` record.
- The exact old state, update, target, incremental criterion, and rank-two gate
  are now frozen and adjudicated. Minimal sufficient task-readout rank remains
  unresolved but is parked by the researcher.
- A15_08_01 E02 completed blocks 2--36 in one TRAIN-only activation-derived
  common basis. A stronger necessity-by-distance interaction did not correspond
  to larger absolute remote two-hop gain, so interaction growth is rejected as
  sufficient evidence of more deep long-range information.

## 15. Relation To The Mainline

A15 supports the broader functional-specialization program by determining
whether a representation coordinate deserves functional testing. It does not
replace A06's expert-utility contract or A16's load-control mechanism. E02 now
shows that a relative interaction trend is not enough; the next measurement
must protect the absolute target cell before any functional promotion.

## 16. Exactly One Next Decision

Decide whether a successor should directly adjudicate the layerwise absolute
$G_{\ell,2F}$ trajectory against matched target-independent corrections. The
descriptive-only representation-rank boundary and exclusion of task-rank and
Router work remain fixed.

## Source Map

- [A15 line index](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/README.md)
- [A15_02_05 balanced-taxonomy result](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md)
- [A15_02_06 shared parameter bases and Attention projection](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E02_shared_parameter_basis_attention_projection/summary.md)
- [A15_02_06 semantic granularity and curve shape](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E03_shared_basis_semantic_granularity/summary.md)
- [A15_02_06 all adjacent transitions](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md)
- [0813 coarse/fine shape and Top-K candidate report](/daily_research_reports/backup/2026/08/0813/docs/daily_report_coarse_fine_spectral_shape_and_topk.md)
- [A15_02_07 matched-taxonomy result](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md)
- [A15_04 shared-tail result](/Projects/from-attention-to-search/main/experiments/A15/15_04_tail_band_information/A15_04_E01_shared_tail_geometry/summary.md)
- [A15_04 terminal-space decoupling result](/Projects/from-attention-to-search/main/experiments/A15/15_04_tail_band_information/A15_04_E02_deep_tail_parameter_semantic_decoupling/summary.md)
- [A15_05 matched fixed-band dispatch](/Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary.md)
- [A15_06 local-random identity control](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md)
- [A15_07 parked unrun Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)
- [A15_08 active Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)
- [A15_08_01 active submitted child Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor.md)
- [A15_08_01 E02 result](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/summary.md)
- [A15_08 E02 TRAIN-only common-basis record](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E02_fresh_balanced_mismatch_repair/detailed.md)
- [A15_08 E03 qualification lesson](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E03_fresh_confirmation_freeze_repair/summary.md)
- [A15_08 E04 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/protocol.md)
- [A15_08 E04 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md)
- [A15_08 E04 Detailed](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/detailed.md)
- [2026-08-10 meeting note](/daily_research_reports/backup/2026/08/0810/meeting_notes/note.md)
- [2026-08-10 variance-interval report](/daily_research_reports/backup/2026/08/0810/docs/DAILY_SUMMARY_ADVISOR_VARIANCE_INTERVAL_20260810.md)
