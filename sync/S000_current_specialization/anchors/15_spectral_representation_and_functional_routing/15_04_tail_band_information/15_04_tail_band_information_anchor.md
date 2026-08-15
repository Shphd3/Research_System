---
anchor_id: 15_04_tail_band_information
legacy_anchor_id: 15_01_11_shared_tail_semantic_relocation
status: completed_fail_local_random_or_nontail_relocation
canonical_language: en
companion_language: zh
thinking_card: 15_04_tail_band_information_thinking_card_cn.md
parent_line: 15_spectral_representation_and_functional_routing
updated: 2026-08-09
---

# A15_04 Does The Common Local-Rank Shift Enter A Cross-Layer Shared Broad Parameter Tail?

Researcher judgment: [Chinese Thinking Card](15_04_tail_band_information_thinking_card_cn.md). Chinese companion: [anchor](15_04_tail_band_information_anchor_cn.md).

## 1. Problem Definition

The [2026-08-07 meeting note](/daily_research_reports/0807/meeting_notes/notes.md) began from a method question: if every layer uses a low-rank Gate, which directions should it use? The discussion mixed three claims that A15 now treats separately:

| Original claim | Operational object | Current position |
| --- | --- | --- |
| deeper layers form finer or more compositional information | matched complex-minus-simple TAX/COMP targets and conditional linear novelty | no stable complexity-specific effect was established |
| an attention-induced update moves toward later MLP parameter ranks | actual MLP-input increment and the complete layer-local parameter spectrum | a target-common early-to-late shift remains; local rank does not identify one vector across layers |
| the shifted directions should be used for Gating | held-out functional utility under a matched routing intervention | untested here; covariance or geometric overlap is insufficient |

A15_04 owns only the unresolved bridge in the second row. A15_02_07 found no stable complex-minus-simple rank shift or conditionally new linear accessibility. The retained phenomenon is target-common: conditional-fine variance in the actual MLP-input increment moves toward later ranks in each layer's own parameter ordering from early to late depth. A15_02_06 separately found a U-shaped cross-layer parameter geometry, with especially high overlap in the lowest-gain endpoint band. Those observations can coexist without being related.

The researcher has now fixed the complete local parameter spectrum as 16 equal 256-dimensional bands: F1 is **head**, F2--F8 are **middle**, and F9--F16 are **tail**. This replaces the earlier proposal that treated only the bottom 256 directions as tail.

**Exactly one decision question:**

> For the attention-induced actual MLP-input increment in frozen Qwen3-8B, does late-layer conditional-fine variance become more enriched than early-layer variance in a cross-layer shared broad tail F9--F16, beyond dimension-matched random geometry and the shared head F1 and middle F2--F8, while the full F1--F16 pattern remains visible?

The representation is $\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)$. It is the change in the current layer's native MLP input caused by inserting the observed attention write $a_\ell$ while holding the pre-write residual $x_\ell$ fixed. It is not a subtraction of adjacent-layer covariance and does not by itself mean information-theoretic novelty. The researcher has confirmed one primary semantic object only: the within-parent between-child covariance of $\Delta n_\ell$, equally weighted over eight parents. Centering within each parent removes that parent's common class mean; it does not remove all information already present in earlier layers. The fixed set is the 512-record A15_02_06 set; the claim is restricted to it.

Pass permits a separate functional Protocol. Fail closes the broad shared-tail explanation. Insufficient evidence permits only provenance or estimation repair.

## 2. Physical Priors

1. Subtracting two curves expressed in different layer-local parameter eigenbases does not identify a direction that was newly created. A cross-layer direction claim requires projectors constructed and evaluated in the common hidden-coordinate system without using the tested layer.
2. $\Delta n_\ell$ isolates an attention-induced input change, while within-parent centering removes one named common semantic component. Neither operation proves that the remaining variance was absent from the old state.
3. A rightward spectral shift is a redistribution over the complete rank partition, so all 16 bands must be reported; one endpoint band cannot reveal whether the change is broad or localized.
4. Raw head, middle, and tail captures are not directly comparable because their dimensions are 256, 1,792, and 2,048. For any fixed covariance, their random expected capture fractions are respectively $1/16$, $7/16$, and $8/16$. A fair comparison must therefore divide capture by the matched random expectation.
5. Geometric enrichment does not imply MLP use. A low-gain space can contain readable variance while exerting little current output effect.

The band partition and random-normalized broad-band metric were Protocol-confirmed and have now been executed.

## 3. Falsifiable Hypotheses

**G0 — phenomenon gate.** The complete local F1--F16 spectrum of conditional-fine $\Delta n$ variance retains a positive early-to-late rank-centroid shift in both sealed expression halves.

G0 is an early-versus-late statement, not a claim of monotonic layer-by-layer movement.

**G1 — broad shared-tail geometry.** After correcting for band dimension, late-layer conditional-fine variance increases its enrichment in the cross-layer shared F9--F16 tail more than in shared F1 head or shared F2--F8 middle, and more than a matched random spectral partition.

The global shared space carries the only G1 verdict. Early-internal, late-internal, early-to-late, and late-to-early measurements diagnose whether any shared structure is globally stable, forms only late, or redirects between depth stages; none can replace or rescue the global verdict.

**Strongest rival.** The apparent tail effect is explained by tail's larger dimension, by a generic shared orientation, or by local rank redistribution without a common cross-layer direction. This rival predicts no tail-specific enrichment after matched random and head/middle controls.

Individual F1--F16 curves localize the pattern. They are not 16 separate primary hypotheses and cannot rescue a failed broad-tail decision.

## 4. Mathematical Model

Let $P_{\ell,k}$ be the local rank-256 projector for band $k\in\{1,\ldots,16\}$. Define broad local projectors

$$
P_{\ell,H}=P_{\ell,1},\qquad
P_{\ell,M}=\sum_{k=2}^{8}P_{\ell,k},\qquad
P_{\ell,T}=\sum_{k=9}^{16}P_{\ell,k},
$$

with ranks $r_H=256$, $r_M=1792$, and $r_T=2048$. For the global primary measurement, split blocks 1--35 into odd/even groups. For an evaluated layer in group $f$, construct the shared broad space from only the other group:

$$
M_G^{(-f)}=\frac{1}{|-f|}\sum_{j\in-f}P_{j,G},\qquad
Q_G^{(-f)}=\operatorname{TopEig}_{r_G}(M_G^{(-f)}),
$$

where $G\in\{H,M,T\}$. Shared rank-256 projectors $Q_k^{(-f)}$ are constructed analogously for every F1--F16 band and are reported separately.

Let $E=\{1,\ldots,12\}$ and $L=\{25,\ldots,35\}$. The same odd/even exclusion within $E$ and within $L$ gives early-internal $Q_{G,E}^{(-f)}$ and late-internal $Q_{G,L}^{(-f)}$. For cross-stage transfer, $Q_{G,E}$ is built from all early parameter projectors and evaluated only on late covariances, while $Q_{G,L}$ is built from all late projectors and evaluated only on early covariances. The parameter-only cross-stage overlap $\operatorname{tr}(Q_{G,E}Q_{G,L})/r_G$ distinguishes a persistent orientation from stage rotation. These stage-resolved quantities are diagnostic and do not enter $D_T$.

For conditional-fine covariance $B_{\ell,F}$, broad-space capture and dimension-normalized enrichment are

$$
c_{\ell,G}=\frac{\operatorname{tr}(Q_GB_{\ell,F})}{\operatorname{tr}(B_{\ell,F})},
\qquad
e_{\ell,G}=\frac{c_{\ell,G}}{r_G/4096}.
$$

$e=1$ is the matched random expectation. Define the early-to-late enrichment change

$$
T_G=\operatorname{median}_{\ell=25:35}e_{\ell,G}
-\operatorname{median}_{\ell=1:12}e_{\ell,G},
$$

and the proposed primary tail-specific statistic

$$
D_T=T_T-\max(T_H,T_M).
$$

$D_T>0$ means the broad tail's depth increase exceeds both other broad parameter regions after dimension correction. It cannot establish function.

## 5. Computational Realization

1. Freeze the 512 A15_02_06 records. The new H100 replay failed exact 5090-cache identity and was excluded; Protocol amendment A2 recovered residual-coordinate $\Delta n_\ell$ only from the original exact-replay eigencoordinates after independently validating the complete saved parameter basis and quantization stability.
2. Use 16 fixed local parameter bands of width 256. Report for every layer and band: absolute between-class variance per direction, normalized local variance share, shared-band capture, and random-normalized shared-band enrichment.
3. Separately construct the broad shared H/M/T projectors above. Do not sum independently constructed shared-band captures, because their consensus spaces need not remain mutually orthogonal.
4. Use odd/even layers among blocks 1--35 for the global primary fit/evaluation; repeat the exclusion within early and late windows, then measure both early-built-on-late and late-built-on-early transfer. Block 36 is descriptive only.
5. Use a matched random 16-band orthogonal partition in each random draw. Its F1, F2--F8, and F9--F16 unions provide dimension-matched H/M/T nulls for global and stage-resolved measurements, and the same draw is applied to every layer.
6. Use the sealed design/confirmation expression halves and clustered parent/template uncertainty. Directions and layers are repeated measurements, not independent samples. Stage-resolved results receive one non-primary interpretation label and cannot change G1.

The full 16-band data are mandatory evidence. The global broad H/M/T summary carries the one decision; stage-resolved geometry explains the accepted global result or localizes why it failed.

## 6. Minimal Falsification Tests

| Verdict | Inspectable rule | Route implication |
| --- | --- | --- |
| Pass: `broad_shared_tail_geometry` | G0 holds; broad-tail $T_T$ is positive and exceeds its matched random interval; the 95% lower bound of $D_T$ is positive; odd/even evaluated layers and both expression halves do not reverse the broad-tail sign | allow a separate functional test |
| Fail: `local_random_or_nontail_relocation` | G0 holds, but broad tail does not beat matched random, or its dimension-normalized increase does not exceed head/middle, or only local F1--F16 redistribution works | close the broad shared-tail interpretation |
| Insufficient | raw-$\Delta n$ replay, G0, shared-tail estimation, or expression/layer-group reliability is unstable | repair provenance or estimation only |

The decisive falsifier is not whether F16 alone is high or whether a late-only space looks strong. It is whether the global F9--F16 broad shared space has a tail-specific depth enrichment after dimension matching. If only the local rank centroid or one stage-local space moves, the meeting intuition has not yet yielded a globally reusable cross-layer coordinate.

## 7. Current Evidence

1. The local phenomenon reproduces. The median local-rank centroid rises from 0.369909 early to 0.471137 late, giving $T_{rank}=0.101228$ with grouped-bootstrap 95% interval [0.087289, 0.113888]. Local broad-tail enrichment also rises by 0.247581, interval [0.210290, 0.276835].
2. The global shared broad tail moves in the opposite direction. Its enrichment falls from 1.053568 early to 0.950114 late: $T_T=-0.103453$, interval [-0.142083, -0.076752]. Shared middle rises by 0.228442, so $D_T=-0.331895$, interval [-0.412888, -0.271072]. Actual $T_T$ and late tail enrichment are both below their 512-Haar q95 controls. Odd/even layers and both expression halves all retain the negative tail sign.
3. The full F1--F16 pattern localizes the mismatch: F9--F13 increase while F14--F16 decrease, especially F16. The registered F9--F16 union therefore fails; a post-hoc narrower tail cannot replace it.
4. Global odd/even tail consensus overlap is above Haar (0.694019 versus 0.500301), so a cross-layer parameter-tail orientation exists. The semantic result nevertheless fails because late conditional-fine variance is not enriched in it.
5. Stage diagnostics are `mixed_stage_geometry`: early/late tail projector overlap exceeds Haar, but late-internal and early-built-on-late semantic enrichments do not. This pattern cannot rescue the global Fail.

The complete evidence and provenance record is [A15_04_E01 summary](/Projects/from-attention-to-search/main/experiments/A15/15_04_tail_band_information/A15_04_E01_shared_tail_geometry/summary.md).

## 8. Claim Boundary And Next Decision

A15_04 establishes only that local conditional-fine rank relocation does not enter the registered globally shared F9--F16 tail on this frozen 512-record set. It does not show that tail directions are unused, random, nonfunctional, or unsuitable for every nonlinear method. The positive shared-middle change also does not establish that middle is a functional module. No MLP-use, task-function, deletion, or Router experiment is admissible from this Fail.

**Exactly one next decision:** close fixed-band localization as the route from parameter geometry to added information and pass the question to A15_08's residual-relative held-out accessibility criterion. **Completion criterion:** any future coordinate must add frozen-target accessibility beyond the old-state readout and matched controls before functional admission. **Resume action:** do not reopen a middle/tail audit or Router experiment from this Fail.
