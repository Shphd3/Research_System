> 阅读副本 · 2026-09-26T15:08:45.352651+00:00 · 处理者 Codex
> 来源：[原始文件](../../../docs/atom_mechanism/anchor.md)
> 源文件 SHA256：`53f628000ef2104938ce1bc6069384cc1fea26ecfa9500e66ef70b2fa016c7ea`
> 这是来源文本的阅读副本，保留原来的时间、建议和证据边界；科研状态以原始记录为准。 其中 NOT RUN 是注册时状态，完成情况见同目录 Summary/Detailed；排除数学目标原子的角色边界以 Detailed 澄清为准。

# Atom usage and local learning consequences

## 1. Problem Definition

Do directions identified by matchable, domain-enriched SAE atom usage carry domain-selective benefits of a small shared-parameter update, beyond equally sized updates that avoid matched control directions? Matchable means that control atoms with comparable pooled frequency and squared activation exist; unmatched extreme atoms remain visible in the static portrait but are outside this primary mechanism test. This is a bounded extension of the current shared-learning mechanism question. An atom is a unit-length decoder direction of the fixed sparse autoencoder, not a verified semantic concept. The researcher explicitly delegated object selection, requested the minimal figures and a four-H100 Reserved experiment, and waived additional review/permission on 2026-09-26. The operational hypothesis and estimand below are AI choices within that delegated exploration, not a human-confirmed scientific conclusion. No existing Focus or project scientific state is changed.

## 2. Physical Priors

Candidate prior: stable domain-enriched activation can locate representation directions that carry domain-selective learning effects. The strongest rival is that these directions are descriptive markers; their apparent functional effects reflect ordinary perturbation size or shared computation. Large activation magnitude alone need not indicate either domain specificity or functional importance. A common dominant atom and weaker domain-dependent usage can coexist.

## 3. Falsifiable Hypotheses

H1: redirecting a source update away from a target domain's enriched-atom span preferentially removes benefit on that target, more than redirecting away from frequency/strength-matched control atom spans. H0: the target-specific contrast is absent or reversed; activation enrichment does not locate the proposed beneficial update channel in this setting. Inconsistent step sizes, ineligible source learning, or numerical failures leave the mechanism unresolved.

## 4. Mathematical Model

At the last attention output, \(a=Wc\), where \(c\) is the attention context and \(W\) the output projection. A small update produces the exact local change \(\Delta a=\Delta Wc\). All subsequent residual, normalization, gated MLP and prediction operations are retained. For a selected decoder span with orthonormal basis \(Q\), remove \(QQ^\top\Delta W\); for the primary comparison rescale the remainder to the original update's Frobenius norm. This changes update direction while matching total parameter-step size. It is a decoder-span intervention, not zeroing individual latent coefficients.

For source \(s\), selected target span \(b\), and readout domain \(t\), let \(R_{sbt}\) be redirected loss minus full-update loss, in nats per predicted token. Target selectivity is \(R_{sbb}-\operatorname{mean}_{t\ne b}R_{sbt}\). The primary quantity \(M\) subtracts the mean selectivity of three matched control spans, then averages the twelve \(s\ne b\) pairs. A positive \(M\) supports target-selective loss of benefit under redirection; it does not establish a universal interference law.

## 5. Computational Realization

Reuse the frozen fresh-S7 exact-21B-token checkpoint, its 30,000-atom Top-32 dictionary, and the fixed four-domain natural-text panel. Reuse the verified loader and capture implementation. Adapt the previous functional one-step framework from the last MLP down projection to the last attention output projection, so the SAE-observed representation can actually change. Reject down-only updates as a means of measuring change in this upstream observer. Fit records choose enriched atoms, matched controls and update gradients; separate readout records measure all consequences. These are previously inspected datasets, not a new sealed confirmation set.

## 6. Minimal Falsification Tests

Compare full updates with equal-norm redirections around target and matched control spans at a full and half step. Keep unrescaled target-span removal as a compensation check. Directly measure affected attention outputs, SAE activation changes and losses. Supporting evidence requires positive conditional 95% lower bounds for \(M\) at both steps, positive target-domain point contrasts for each of four targets, positive mean unrescaled target selectivity at both steps, and qualified source improvement. An upper bound at or below zero at both steps is non-supporting; other cases are insufficient or heterogeneous. Guards and the exact source-improvement criterion are in the Protocol.

## 7. Current Evidence

The preceding [same-panel result](../20260926_structure_update/summary_cn.md) established mean cross-domain help for last-MLP-down updates, but did not measure changing downstream representations or identify an atom mechanism. It cannot substitute for the new attention-projection experiment. Existing activation records are available for the minimal usage and concentration figures. New intervention results are NOT RUN at registration.

## 8. Claim Boundary And Next Decision

The maximum claim is a conditional, local functional role of fit-selected decoder spans in this fixed model and text panel. Neither semantic purity, long-term shared-training interference, isolation benefit, nor atom-by-atom causal independence is identified. The next decision is whether enriched spans merit a stronger independent mechanism test: support retains them as candidates; non-support stops treating this enrichment rule as a functional locator; insufficient evidence keeps the question open without changing the selection rule after seeing outcomes. Resume from the frozen [Protocol](protocol.md), then read Summary and Detailed evidence.
