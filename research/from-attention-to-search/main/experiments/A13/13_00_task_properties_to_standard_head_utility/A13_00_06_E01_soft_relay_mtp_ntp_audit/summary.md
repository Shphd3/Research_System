# A13_00_06_E01 Summary

## Direct Result

**Insufficient; Stage 0 stopped Stage 1.** The four registered penalties did
create the intended ordered *causal* path shift, and every NTP-only condition
eventually learned. However, `direct_0` reached 90% accuracy at the first
positive checkpoint (step 20) in 8/8 seeds. The frozen common-dynamic-range
gate therefore failed, so no shared-aux or informative-MTP result was run or
read.

This does not reject the MTP mechanism. It says the proposed utility trend is
not identifiable at the frozen measurement resolution: the easiest endpoint
is already saturated while the hard endpoint is still learning.

![Stage-0 NTP-only learning curves](figures/stage0_ntp_learning_curves.png)

![Stage-0 measured causal path effects](figures/stage0_causal_path_effects.png)

## NTP-Only Carrier Reading

All four paths reached final mean accuracy 1.0. Their measured use changed in
the intended direction at step 1,000:

| Path | NTP AULC, nats | Median step to 90% | Direct-deletion effect, nats | Wrong-relay effect, nats | Relay reliance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `direct_0` | 0.0730 | 20 | 9.276 | 0.000001 | 0.0000002 |
| `soft_2` | 0.2570 | 80 | 6.459 | 0.000033 | 0.0000058 |
| `soft_4` | 0.5115 | 230 | 4.363 | 2.728 | 0.345 |
| `hard` | 0.8508 | 310 | 0.000 | 11.886 | 1.000 |

Across paired seeds, direct-effect slope was negative in 8/8 seeds and relay-
effect and relay-reliance slopes were positive in 8/8. Thus the logit penalty
worked as a causal path intervention, but its realized effect was nonlinear:
`soft_2` still used almost exclusively the direct path.

## Primary Objective Result

There is none. By the approved contract, Stage 1 could run only after every
Stage-0 gate passed. It was not launched. Therefore neither

\[
U_r=\operatorname{AULC}_{\rm shared\text{-}aux,r}
-\operatorname{AULC}_{\rm informative\text{-}MTP,r}
\]

nor an MTP-versus-NTP-only system difference is available.

## Confound Reading

Hard-mask difficulty was not excluded; it was directly observed. NTP AULC
rose from 0.0730 to 0.8508 nats as relay reliance rose, while the normal direct
path saturated by step 20. Any apparent increase in \(U_r\) could therefore be a
ceiling/difficulty interaction.

Gradient dose was not tested because neither active auxiliary condition was
authorized. Stage-0 answer gradients cannot substitute for the missing
shared-aux versus informative-MTP gradient comparison.

## Claim Boundary

The result establishes only that the registered penalties create an ordered,
learnable shift from direct use to relay use. It does not establish whether
MTP utility grows continuously with relay dependence, whether a hard mask is
special, or whether measured gradient dose explains an objective difference.
It changes no claim about code, language, long context, planning, or MoE.

## Exactly One Next Decision

**Researcher approval is required for one measurement-only repair: preserve
all data, model, objectives, penalties, seeds, optimizer updates, and budgets,
but evaluate every step through step 40 before returning to the frozen
20-step cadence; rerun Stage 0, and permit Stage 1 only if the common-dynamic-
range gate then passes.**
