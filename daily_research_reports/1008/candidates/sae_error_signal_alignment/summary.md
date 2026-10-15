# H2 candidate results: SAE-similar events and native error signals

**Both measurements and registered analyses completed. This is a fixed-checkpoint candidate diagnostic; researcher mechanism judgment remains Unknown.**

**The key boundary is positive overall mean advantage but negative advantage for different-next-token pairs in both models; native neighbors also have higher absolute mean delta cosine.** This supports a weak average association, not stable cross-target signal alignment from SAE similarity. Target stratification is descriptive, not a causal target intervention.

## Purpose

Test whether input-only SAE-code neighbors on natural text have more aligned true-next-token error signals, informing whether SAE routing warrants further study.

## Hypothesis

Within matched domain and position-bin pools, five SAE neighbors have higher mean delta cosine than twenty random references and positive absolute neighbor cosine. Delta is the derivative of native true-next-token CE, not SAE reconstruction loss or a synthetic target rule.

## Analysis method

Each model measures 1024 records and sixteen positions per record. Fit/readout each contain 512 records. Neighbor selection reads no targets, loss or gradients. Average within records and weight four domains equally; obtain 95% intervals from 2000 domain-stratified query-record bootstrap draws with fixed references and pairs. [Protocol](protocol.md) defines the analysis and verdicts; [Amendment 01](amendment_01.md) and [Amendment 02](amendment_02.md) record numerical implementation repairs.

S7 measures final Attention output; Qwen measures the final post-attention-normalized MLP input. Their actual projection input/output-gradient variables remain distinct. No LoRA, router training or new representation-space training occurs.

## Conclusion

| Model | SAE-neighbor delta cosine [95% interval] | Matched-random cosine [95% interval] | Paired advantage S [95% interval] | Registered verdict |
|---|---|---|---|---|
| S7 fresh | 0.0151 [0.0133, 0.0167] | 0.0052 [0.0048, 0.0057] | 0.0098 [0.0080, 0.0116] | SUPPORT_BOUNDED_H2 |
| Qwen3-0.6B-Base | 0.0308 [0.0270, 0.0345] | 0.0035 [0.0028, 0.0043] | 0.0273 [0.0234, 0.0310] | SUPPORT_BOUNDED_H2 |

Support requires positive lower bounds for both S and absolute neighbor cosine. Non-support requires a nonpositive upper bound for S; other outcomes are insufficient. The zero threshold does not establish routing utility.

| Registered secondary comparison | S7 fresh | Qwen3-0.6B-Base |
|---|---|---|
| Native-neighbor advantage | 0.0132 [0.0113, 0.0153] | 0.0312 [0.0270, 0.0353] |
| SAE minus native absolute neighbor cosine | -0.0030 [-0.0043, -0.0018] | -0.0037 [-0.0060, -0.0014] |
| Same-current-token advantage | 0.0081 [0.0014, 0.0143] | 0.0159 [0.0071, 0.0251] |
| Different-next-token advantage | -0.0044 [-0.0054, -0.0034] | -0.0474 [-0.0506, -0.0442] |
| Centered-delta diagnostic | 0.0137 [0.0117, 0.0156] | 0.0352 [0.0311, 0.0393] |
| Shuffled-delta control | 0.0003 [-0.0006, 0.0012] | -0.0011 [-0.0027, 0.0005] |

Native activation is a credible competitor; positive H2 does not establish SAE superiority. The same-current-token subgroup is strict and coverage-limited. Target comparisons stratify already-selected pairs without using targets for neighbor selection.

Both SAE-minus-native and different-target advantage intervals are negative. Same-current-token advantage remains positive, so exact current-token repetition alone does not explain the association. Shuffled-delta advantage intervals include zero. These observations constrain interpretation without identifying a causal target-overlap decomposition. Negative neighbor delta-cosine fractions are 49.1% for S7 and 49.8% for Qwen.

![Primary comparison](figures/h2_primary.png)

The first panel shows absolute neighbor/random error-signal alignment. The second shows paired neighbor advantage and its interval; assess relative advantage together with absolute alignment.

![Controls](figures/h2_controls.png)

Rows display registered alternatives and diagnostics with each comparison's matched-random baseline. They probe native similarity, lexical identity, target overlap, shared means and accidental pairing. Different subgroup coverage prevents a causal row-by-row decomposition.

![Domain diagnostic](figures/h2_domains.png)

Each cell is a model/domain SAE-neighbor advantage. This is an association display, not a cross-domain finite-update loss heatmap.

## Boundary and next decision

The test concerns activation codes, not isolated decoder atoms. Delta alignment is not complete parameter-gradient compatibility, finite-step loss improvement or long-term expert benefit. This historically exposed panel overlaps 768 records with the prior NTP-statistics panel; paper identities are unavailable. The hooks differ, so each model is judged separately without a pooled success claim.

Researcher next judgment remains Unknown. AI suggestion: assess native baselines, strict lexical controls, different-target results and effect sizes before deciding on independent-corpus confirmation or a real shared-update bridge.

Run owner: `/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/runs/diagnostic_v3_20261008T090146Z`. [Completion](evidence/completion.json), [preflight](evidence/preflight.json), [S7 statistics](evidence/s7_summary.json), [Qwen statistics](evidence/qwen_summary.json) and [selected result provenance](evidence/result_manifest.json). Raw arrays and event/record tables remain in execution.
