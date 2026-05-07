# Experiment Return (Round 6)

## acp_lite_vs_hybrid

- Round executed: Round 6 Instance-level PPL Divergence Audit (acp_lite_vs_hybrid)
- Result summary: Group A/B/C proportions = `0.2467/0.3979/0.3554`; deep-layer agreement in Group C = `0.1296`.
- Reliability audit: sentence_count=`10000`, checkpoint_step_1=`60000`, checkpoint_step_2=`60000`, length_vs_R_i_corr=`0.0376`.
- Hypothesis update: Group B is larger than Group C, so divergent cases lean more often toward the first-order baseline. Group C does not show a strong extra deep-layer agreement drop relative to Group B, so routing disagreement is not unique to second-order wins. Deep-layer entropy delta in Group C (`H2-H1=0.0934`) should be interpreted layerwise rather than through a global mean. Weak token-length correlation (`r=0.0376`); length is unlikely to be the main driver of Group differences.
- Suggested checkpoint delta: keep `checkpoint-60000` as the comparison anchor unless a later aligned checkpoint is required for a follow-up stability check.

## acp_lite_vs_quadratic_low_rank

- Round executed: Round 6 Instance-level PPL Divergence Audit (acp_lite_vs_quadratic_low_rank)
- Result summary: Group A/B/C proportions = `0.2396/0.4162/0.3442`; deep-layer agreement in Group C = `0.0703`.
- Reliability audit: sentence_count=`10000`, checkpoint_step_1=`60000`, checkpoint_step_2=`60000`, length_vs_R_i_corr=`0.0626`.
- Hypothesis update: Group B is larger than Group C, so divergent cases lean more often toward the first-order baseline. Group C does not show a strong extra deep-layer agreement drop relative to Group B, so routing disagreement is not unique to second-order wins. Deep-layer entropy delta in Group C (`H2-H1=-0.1350`) should be interpreted layerwise rather than through a global mean. Weak token-length correlation (`r=0.0626`); length is unlikely to be the main driver of Group differences.
- Suggested checkpoint delta: keep `checkpoint-60000` as the comparison anchor unless a later aligned checkpoint is required for a follow-up stability check.

