# Summary: exact-33B S7 controlled shared update

Primary Anchor: [controlled shared-update question](documents/anchor.md)  
Frozen Protocol: [approved protocol](documents/protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: complete, eligible primary loss comparison; SAE task-signal proxy unresolved; researcher judgment pending.

## 1. Purpose

Determine when an effective update from task A helps or harms task B at one shared parameter matrix, then examine whether a frozen SAE locates the relevant representation change.

## 2. Hypothesis

Greater overlap between A and B task-signal directions should magnify the contrast between agreeing and reversed answer rules, with net help under agreement and net harm under reversal. A rival is that correcting the model's shared background error helps B in every condition despite a rule-dependent contrast. SAE atom identity and similar activation are candidate structure, not a guaranteed functional path.

## 3. Analysis Method

- At the exact 33B checkpoint, compare B loss before and after ordinary A-only updates across low/high direction overlap and kept/reversed B rules. The registered interaction is \(M=(I_{H,flip}-I_{H,keep})-(I_{L,flip}-I_{L,keep})\); 12 paired direction families are the top-level uncertainty units, with 2,000 hierarchical bootstrap draws.
- Require independent A improvement, comparable initial errors, numerical closure and first-order qualification at both registered step sizes before interpreting B outcomes.
- On all 12 confirmation families, select shared SAE atoms using separate structure samples and the approved loose frequency/strength rule; measure task-signal reconstruction and signed contribution against the complement, PCA and same-rank random spaces.

## 4. Conclusion

**Frozen-rule verdict:** `MODULATION_WITHOUT_NET_HARM`. **Researcher scientific judgment:** `AWAITING_HUMAN_CONFIRMATION`.

1. **The controlled relation modulated B's benefit; it did not produce net B harm.** At step \(10^{-4}\), \(M=1.5206\times10^{-4}\) nats/target (95% paired bootstrap interval \([1.3617,1.6722]\times10^{-4}\)); at \(5\times10^{-5}\), \(M=7.6028\times10^{-5}\) (\([6.8078,8.3618]\times10^{-5}\)). Both lower bounds exceed the frozen detection threshold \(10^{-7}\). Yet high-overlap/reversed B loss changes were \(-0.0066649\) and \(-0.0033780\) nats/target, with both intervals wholly below zero. A improved on every registered update; all substantive and numerical guards passed. [Frozen verdict and intervals](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/verdict.json>); [family-level values](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/primary_by_family.csv>).
2. **The approved SAE definition found common activation, but the SAE did not qualify as a task-signal proxy here.** Each family selected 32 common atoms after the same-atom and similar-frequency/strength filter. The paired task-signal reconstruction relative-error medians were 1.006–1.159 in all 12 families, exceeding the prespecified 0.5 limit, although overall reconstruction error was about 0.10. At step \(10^{-4}\), the descriptive common-span signed contribution to \(M\) was \(5.56\times10^{-6}\), about 3.65% of the observed interaction; the complement contributed \(1.4653\times10^{-4}\), and same-rank PCA/random controls had similar common-span scale. These signed terms use B loss derivatives and are neither an independent prediction test nor an atom-causality test. [SAE qualification table](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/sae_reconstruction_checks.csv>); [signed decomposition](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/signed_decomposition.csv>).

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| \(M\) lower bound > \(\tau\) at both steps | \(1.3617\times10^{-4}\); \(6.8078\times10^{-5}\) | Full measurement and all guards pass | Direction/rule modulation observed | [verdict.json](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/verdict.json>) |
| High-overlap/reversed B loss lower bound > \(\tau\) at both steps for net harm | Upper bounds \(-0.0066492\); \(-0.0033701\) | Eligible | Net harm absent in the registered comparison | [verdict.json](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/verdict.json>) |
| SAE task-signal relative-error median ≤ 0.5 | 1.006–1.159 in 12/12 families | Common atoms exist; proxy guard fails | SAE task-signal proxy unresolved | [SAE qualification](</data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/sae_reconstruction_checks.csv>) |

### Important Figures

![Registered interaction and net effect](../../figures/shared_update_registered_contrast.png)

How to read: the left panel's positive \(M\) intervals show modulation at both step sizes; the right panel's negative high-overlap/reversed B changes show continued net help.

![SAE proxy qualification](../../figures/shared_update_sae_proxy_qualification.png)

How to read: 32 selected atoms per family do not rescue the task-signal error, which exceeds the dotted 0.5 qualification line for every family.

### Claim Boundary

**Can claim:** In this one exact-33B checkpoint and constructed internal binary task, direction overlap changed the rule-dependent size of an effective A update's benefit to B. The frozen SAE selected similarly activated common atoms, but failed the registered task-signal reconstruction guard.

**Cannot claim:** Net interference, natural-domain conflict, long-run joint-training cost, an SAE common atom causing the interaction, SAE-only prospective prediction, or a benefit from parameter isolation. The family-level bootstrap quantifies this fixed construction; it does not generalize across models or data-generating processes.

### Next Step Analysis

**Decision pending researcher:** Does the observed SAE proxy failure warrant a separate prospective SAE prediction test on untouched direction families? **AI_PROPOSAL:** first decide whether a corrected, outcome-blind representation proxy can pass the same task-signal guard; otherwise do not treat the current atom set as a prospective predictor. The completion criterion is a researcher-approved proxy and frozen held-out prediction rule, or a decision to stop that branch. Resume only after that decision; a second look at these 12 families cannot serve as an untouched prediction test.
