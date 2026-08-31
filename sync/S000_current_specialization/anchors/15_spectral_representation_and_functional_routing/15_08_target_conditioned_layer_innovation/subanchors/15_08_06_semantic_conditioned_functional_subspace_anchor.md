---
anchor_id: 15_08_06_semantic_conditioned_functional_subspace
status: APPROVED_AND_FROZEN_FOR_EXECUTION
canonical_companion: 15_08_06_semantic_conditioned_functional_subspace_anchor_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
depends_on:
  - 15_08_03_function_admitted_update_representation_rank_anchor.md
  - 15_08_05_aligned_geometric_rank_scale_anchor.md
protocol: ../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E01_clinc150_semantic_conditioned_functional_subspace/protocol.md
created: 2026-08-18
updated: 2026-08-18
---

# A15_08_06: Semantic-Conditioned Geometry And Low-Dimensional Functional Subspace

## 0. Decision Snapshot

This anchor formalizes the 2026-08-18 meeting question. The user explicitly approved the complete design and requested execution on 2026-08-18. It does not supersede A15_08_05 object/scale alignment work and does not permit this experiment to be over-interpreted as a Router or expert-utility result.

The scientific question is:

> After matching class count and samples, is the broad covariance spectrum of a same-layer residual update partly explained by a union of stable but differently oriented domain-local subspaces; and, independently, at what projection dimension does $R_U$ retain 80% or 90% of the full update's held-out fine-intent added accessibility?

The two clauses are deliberately separate. A narrow covariance spectrum is a geometric statement. Retaining added classification gain is a functional statement. Neither establishes expert utility.

## 1. Meeting Alignment And Required Correction

The screenshot's high-level purpose matches the 0817 meeting theme:

1. globally broad update geometry may coexist with locally compact task structure;
2. high-dimensional representation does not imply high-dimensional gating;
3. PCA variance directions must be compared with supervised and random alternatives.

The original method is not yet sufficient for the phrase "mainly comes from several local subspaces." Lower within-domain rank alone can be caused by fewer classes, fewer samples, or easier lexical structure. The design therefore requires:

- equal class and sample counts in within-domain and cross-domain conditions;
- a direct orientation/stability test for domain-local subspaces;
- a union-growth test showing that different stable local subspaces broaden the combined span;
- a separate held-out functional-retention test.

Functional rank is not determined by class count $C$, classifier output dimension, or an algebraic ceiling. Its only operational definition here is how much held-out added gain survives after projecting $R_U$ to dimension $r$. Class count is used to match task size, never as a rank threshold, normalizer, or verdict criterion.

## 2. Current Evidence And Layer Choice

Within the prior registered same-$X$ linear-readout protocol, blocks 24 and 28 showed conditional fine-grained added accessibility. Their first registered passing PCA rank was 256; ranks 1--128 did not pass the full functional-retention criterion. The same TRAIN PCA spaces did not satisfy the registered stable representation-low-rank conjunction. These are prior-task, prior-protocol facts, not CLINC150 results.

Accordingly:

- blocks 24 and 28 are frozen before CLINC150 is opened for representation analysis;
- neither block is assumed to have full-$R_U$ gain on CLINC150;
- full-$R_U$ admission on the new task is a mandatory first gate;
- the two blocks are co-registered, with simultaneous inference; no best-looking block may be selected after TEST.

Block 25 has a bounded positive result in a different controlled A15_08 instance, but it is not added here because the screenshot and the later conversation explicitly fixed blocks 24 and 28 from the fine-grained layerwise result. Adding block 25 after seeing CLINC150 would create a selection ambiguity.

## 3. Objects And Non-Equivalent Ranks

For block $\ell$, let $h_\ell$ be the pre-attention residual, $a_\ell$ the post-output-projection attention write before residual addition, and $N_\ell$ the same post-attention RMSNorm. Define

$$
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),
$$

$$
U_\ell=Z_\ell-X_\ell,\qquad
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{\mathrm{lin}}[U_\ell\mid X_\ell].
$$

$U_\ell$ is an exact same-token computational update under the same normalization. $R_{U,\ell}$ is the part not predicted by the frozen TRAIN-fitted linear family. It is not "new knowledge" and may include nonlinear re-encoding of $X$, task-irrelevant variation, and estimation error.

This Anchor keeps four notions separate:

| Quantity | Question | Primary measurement |
| --- | --- | --- |
| algebraic/sample rank | how many nonzero sample directions exist? | matrix/covariance rank |
| variance or geometric rank | how many directions carry update variance? | $r_{90}^{var}$, entropy rank |
| functional rank | how many frozen coordinates retain held-out added gain? | $G_r/G_{full}$ |
| Router decision rank | how many coordinates preserve expert-relative utility ordering? | out of scope here |

## 4. Data Choice And Why It Fits

CLINC150 is an English task-oriented-dialogue intent-classification dataset with ten domains and 150 in-scope intents, fifteen per domain.
Each intent has 100/20/30 TRAIN/validation/test examples; this experiment excludes OOS and uses 22,500 in-scope examples.

This exact balance permits a 15-intent within-domain task to be compared with a 15-intent cross-domain task without changing class count or per-class sample count.

Illustrative, paraphrased examples:

| Condition | Example intents and utterance meaning | What it tests |
| --- | --- | --- |
| within banking | `transfer`: move money between accounts; `freeze_account`: stop account activity; `balance`: ask available funds | the words are all financial, so success requires fine action distinctions rather than a coarse topic cue |
| within travel | `book_flight`: reserve a trip; `flight_status`: ask whether a flight is delayed; `lost_luggage`: report missing baggage | several intents share travel/flight vocabulary, creating a genuine fine-grained task |
| matched cross-domain | `transfer`, `schedule_meeting`, `book_flight`, `rewards_balance`, plus eleven intents from other domains | class/sample count is unchanged, but coarse domain differences become available |
| global 150 | every in-scope intent | descriptive global geometry only; not a causal comparator to a 15-way task |

The data fit the experiment because they have a real parent--child hierarchy, balanced classes, natural paraphrases, and untouched official splits. Limitations remain: utterances are short crowdsourced assistant requests; lexical shortcuts may exist; intent similarity is not expert utility; the official raw JSON needs a separately frozen, complete 10-by-15 domain mapping before execution.

MASSIVE is parked as a replication candidate. It has explicit scenario/intent fields but unequal intents per scenario, so it is less clean for the first matched local-versus-cross-domain adjudication.

## 5. Conditions

1. **Global-150:** all in-scope intents. Descriptive only.
2. **Within-domain-15:** ten tasks, one for each domain.
3. **Matched-cross-domain-15:** for each target domain, deterministic 15-intent sets drawn from the other nine domains, with identical per-intent split sizes and at most two intents from any source domain.

The main geometry contrast is Within-domain-15 versus Matched-cross-domain-15. Global-150 cannot create a Pass because its class count and row count differ.

## 6. Falsifiable Hypotheses

### H-ADMIT: the object transfers to the real task

For at least one pre-registered block, correctly paired full $R_U$ must improve held-out domain-conditioned 15-way intent prediction beyond the same frozen $X$ logits, duplicate-$X$, and matched-mismatch controls under simultaneous inference.

If H-ADMIT fails, functional rank is `INSUFFICIENT_NO_FULL_GAIN`; a ratio to a nonexistent full gain is not interpreted.

### H-GEO: local concentration plus different orientations explain part of the broad mixture

At matched class/sample counts:

1. within-domain normalized $r_{90}^{var}$ is lower than matched cross-domain normalized $r_{90}^{var}$;
2. each domain's frozen local discriminant subspace is more stable across TRAIN halves than it overlaps other domains;
3. the effective dimension of the union of the ten local subspaces exceeds a same-domain resampling null.

Only the conjunction supports the bounded statement that a union of different stable local subspaces contributes to global breadth. It still does not establish that it is the only or dominant source; within-intent nuisance covariance may remain broad.

### H-FUNC: a low-dimensional projection of $R_U$ retains added function

Let $D_i$ be the known domain and $Y_i$ the 15-way intent within that domain. Freeze an $X$-only head $b_d$. For a rank-$r$ input projection $P_r$ and correction head $A_r$,

$$
s_i^{(r)}=b_{D_i}(X_i)+R_{U,i}P_rA_r.
$$

Define equal-domain held-out cross-entropy gain

$$
G_r=\frac1{10}\sum_{d=1}^{10}
\left[
CE_d(b_d(X))-CE_d(s^{(r)})
\right].
$$

The matched unrestricted correction defines $G_{full}$. Functional rank is defined directly from the $R_U$ projection curve:

$$
r_{func}(\eta)=\min\{r:G_r\ge\eta G_{full}\},\qquad \eta\in\{0.8,0.9\}.
$$

Every curve must show both $0.8G_{full}$ and $0.9G_{full}$ and report $r_{func}(0.8)$ and $r_{func}(0.9)$. A threshold is called confirmed only when the simultaneous 95% lower bound of $G_r-\eta G_{full}$ is positive and the result exceeds the equal-rank random control; otherwise report the point estimate or `NA`.

The supervised construction is fixed to **reduced-rank ridge regression (RRR)**. With $T_{corr}$ denoting the correction target left by the $X$ baseline, TRAIN solves

$$
\min_{P_r^\top P_r=I,\,A_r}
\|T_{corr}-R_UP_rA_r\|_F^2+\lambda\|A_r\|_F^2.
$$

$P_r$ is a learnable input projection and $A_r$ a learnable correction head; together they form a rank-$r$ linear low-rank module. TRAIN fits the module, validation chooses $\lambda$, and TEST evaluates it once. A projection shared across all ten domains is a secondary robustness analysis, not the definition of low functional rank.

### H-PCA: variance order is or is not aligned with task function

At every frozen rank, compare:

1. TRAIN PCA head;
2. TRAIN PCA tail within the identifiable nonzero spectrum;
3. equal-rank Haar random subspaces;
4. the supervised RRR subspace;
5. full $R_U$.

Supervised Pass with PCA Fail supports an objective mismatch on this intent task. Comparable PCA and supervised performance means PCA happens to align with intent accessibility here; it still does not prove expert utility.

## 7. Why PCA Alignment Is Not Router Optimality

PCA solves

$$
v_{PCA}=\arg\max_{\|v\|=1}\operatorname{Var}(v^\top x),
$$

whereas routing should preserve expert-relative utility or compatibility. A nuisance counterexample is

$$
x=(a,\epsilon y),\qquad \operatorname{Var}(a)\gg\operatorname{Var}(\epsilon y),
$$

where $a$ is utterance length or style and $y$ determines which expert is useful. PCA selects $a$; the useful decision is in the low-variance coordinate.

A linear gate can align to covariance heads because those directions produce larger, more stable gradients and are easier to learn under finite optimization. Load balance can make the marginal expert counts uniform while leaving the conditional assignment unrelated to expert utility. Thus

$$
\text{easy to learn}\ne\text{intent-discriminative}\ne\text{expert-utility optimal}.
$$

The present experiment adjudicates only the middle clause.

## 8. Decisive Analyses

### 8.1 Geometry

- total centered covariance spectrum;
- within-intent and between-intent covariance decomposition;
- $r_{80}^{var}$, $r_{90}^{var}$, entropy rank, and cumulative variance;
- TRAIN-to-validation/test projector capture;
- fixed-rank principal-angle overlap and union effective dimension.

The within/between decomposition is mandatory: otherwise broad lexical or paraphrase variation could be mistaken for a union of semantic subspaces.

### 8.2 Function

- frozen $X$-only baseline;
- full correctly paired $R_U$ correction;
- duplicate-$X$ and mismatch controls;
- rank curves for PCA head, identifiable PCA tail, 64 nested Haar random bases, supervised RRR, and full $R_U$;
- both $0.8G_{full}$ and $0.9G_{full}$ lines, with the two empirical functional ranks read separately;
- equal-domain macro CE gain as primary, macro accuracy as secondary;
- a small nonlinear $X$-only rival reported as a re-encoding diagnostic, not used to redefine the linear-accessibility claim.

### 8.3 Data isolation

TRAIN learns residualizers, one basis per frozen candidate dimension, heads, and nulls. Validation chooses regularization separately at every dimension. TEST evaluates the entire frozen curve once and cannot select layer, rank grid, cross-domain set, method, threshold, plot range, or wording.

## 9. Typed Knowledge Updates

| Eligible result | Allowed update |
| --- | --- |
| local spectra narrower, stable local orientations differ, and union dimension grows | different domain-local subspaces contribute to broad mixture geometry |
| spectra remain broad but $r_{func}(0.8)$ and/or $r_{func}(0.9)$ is small | high-rank expression and low-dimensional gating-relevant intent accessibility coexist; the mixture explanation is unnecessary |
| local spectra narrow but functional retention fails | geometric concentration is not functional concentration |
| supervised passes while PCA fails | maximum variance is the wrong ordering for this task; learned conditional directions are required |
| PCA and supervised both pass | variance head is task-aligned on this dataset, but Router utility remains open |
| full $R_U$ has no matched held-out gain | the prior local effect does not transfer to this dataset/layer; functional rank is unidentifiable |
| neither geometry nor function is compact | the registered linear local-low-rank hypothesis fails for this object, task, and layers |

## 10. Audit Of The Referenced Conversation

| Conversation or screenshot choice | Audit | Frozen resolution |
| --- | --- | --- |
| MASSIVE, block 25, fixed $r\le32$ | internally coherent but not the final confirmed design | park MASSIVE; use CLINC150 and blocks 24/28; define empirical rank with two retention thresholds |
| CLINC150, blocks 24/28 | aligned with balanced local-versus-cross comparison and prior fine-task evidence | retain, but re-admit full $R_U$ on CLINC150 first |
| compare all intents with one domain | confounded by 150-way versus 15-way class count and row count | Global-150 is descriptive; matched 15-way contrast is decisive |
| lower within-domain rank proves union of local spaces | insufficient; orientation may be the same and nuisance may shrink | require stability, principal-angle, union-growth, and within/between covariance analyses |
| use class count or head dimension to determine rank | not equivalent to whether a low-dimensional projection preserves $R_U$ function | determine rank directly with $r_{func}(0.8)$ and $r_{func}(0.9)$ |
| supervised learning rule left open | permits method drift | fix supervised RRR with learnable $P_r,A_r$ |
| call $R_U$ new information | too strong | call it a linearly unpredictable candidate update; claim only held-out added accessibility |
| intent classification proves Router value | objective mismatch | this experiment only admits an interpretable candidate; expert-utility testing is downstream |

The main thesis is not wrong. The operational claim was under-specified. The corrected thesis is:

> broad update geometry may arise from several stable local subspaces and may still contain a compact shared task statistic, but geometry, task accessibility, and expert utility must be separately admitted.

## 11. Claim Boundary And Next Decision

A positive result can establish only a CLINC150- and linear-readout-bounded relationship between semantic conditioning, update covariance, and held-out intent accessibility at blocks 24/28. It cannot establish intrinsic semantic rank, nonlinear novelty, model-native use, expert specialization, reduced forgetting, or Router improvement.

The sole next decision after human review is whether the paired Protocol should be approved unchanged for implementation. Until every pending block is confirmed, no data download, extraction, fitting, TEST opening, or experiment execution is authorized.
