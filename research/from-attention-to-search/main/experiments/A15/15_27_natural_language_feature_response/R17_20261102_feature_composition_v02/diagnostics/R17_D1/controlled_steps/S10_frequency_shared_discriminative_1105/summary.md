# S10: reference frequency of shared and discriminative SAE coordinates

Purpose: test whether coarse and fine category relations use shared or discriminative coordinates in different independently defined frequency ranges. H1 predicts higher-frequency cross-parent sharing; H2 predicts a shift of finer discrimination toward lower frequencies; H3 separates membership, same-support amplitudes and beyond-marginal coactivation. AI operational interpretation only; scientific acceptance and closure remain Unknown.

## Data and model

Reuse all384S06rows and native sparse responses. F01–F08 selects new S10 lists; new statistics on F09–F16 are posthoc exploratory. Freeze16newN01–N16templates, sixlabels and fourwordings=384prefixes before confirmation; old category phrases repeat in three wordings, and a fourth is an additional lexical control.48minimal-context controls are separate. Frozen official Qwen3-0.6B Base,28blocks,width1024. Native30000-coordinate ReLU/Top32 at block27Attention o_proj output and actual MLP input. Dictionaries/IDs are distinct. No training or intervention.

Reference:384S09discovery questions,128/source, original first<=128tokenIDs followed by newline Description:, finalcolon sampled. Main frequency=count/384. Unseen and1–7counts are separate. Supported counts are tertile-binned without splitting ties: ATTN low8–11,mid12–18,high19+ (118/86/101coordinates); MLPIN low8–11,mid12–32,high33+ (66/55/61). This is neither universal corpus frequency nor word/spectral frequency.

## Measurements and interpretation

| site | pair | low | mid | high | insufficient | unseen |
| --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal_vehicle | 8.179369 | 7.099762 | 43.098268 | 28.097256 | 13.525345 |
| ATTN_SAE | car_bicycle | 5.851588 | 12.136973 | 41.836324 | 28.83844 | 11.336676 |
| ATTN_SAE | cat_dog | 10.023285 | 8.910096 | 35.627042 | 30.497994 | 14.941583 |
| MLPIN_SAE | animal_vehicle | 2.433307 | 10.09363 | 67.218342 | 12.470777 | 7.783945 |
| MLPIN_SAE | car_bicycle | 5.785445 | 8.362726 | 60.98819 | 13.558887 | 11.304752 |
| MLPIN_SAE | cat_dog | 3.290864 | 9.180722 | 60.140811 | 17.98535 | 9.402253 |


New explicit high-share cross-minus-sibling comparisons pass3/4Holm tests; Attention vehicle is unresolved. ATTN cross43.10%vs cat/dog35.63%,difference.074712[.019469,.134935]; MLPIN67.22%vs60.14%,difference.070775[.038498,.102014]. MLPINcat/dogdoes not add a higher low+mid share. High-frequency opportunity and family background remain explanations; natural-reference pairs themselves have95.62%/98.60%high sharing. S09's82.9–97.0%gap reproduction concerns natural-body positions only, not this hierarchy panel.

| site | pair | locked_count | supported_count | low_mid_count | high_count | insufficient_count | unseen_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal_vehicle | 16 | 8 | 2 | 6 | 5 | 3 |
| ATTN_SAE | cat_dog | 2 | 0 | 0 | 0 | 1 | 1 |
| ATTN_SAE | car_bicycle | 9 | 3 | 1 | 2 | 5 | 1 |
| ATTN_SAE | pooled_children | 21 | 11 | 4 | 7 | 6 | 4 |
| MLPIN_SAE | animal_vehicle | 24 | 10 | 4 | 6 | 6 | 8 |
| MLPIN_SAE | cat_dog | 1 | 1 | 0 | 1 | 0 | 0 |
| MLPIN_SAE | car_bicycle | 9 | 4 | 1 | 3 | 4 | 1 |
| MLPIN_SAE | pooled_children | 16 | 11 | 5 | 6 | 3 | 2 |


H2 lacks a consistent lower-frequency shift. Cat/dog2/1locked candidates with0/1supported are insufficient. Vehicle9/9candidates have3/4supported. Fixed signed low+mid mass shares: coarse .0962/.3284 vs vehicle-fine .0833/.2128, ATTN/MLPIN. MLPINexplicit has a local opposite direction; other wordings do not establish a stable gradient. The ratio-difference bootstrap is conditional/descriptive, not the originally generic H2sign/Holm primary test; no invalid p is asserted. Unknown-frequency and negative mass stay in denominators; .975resample stability is a post-result guard. Feature-wise family tests/BH are separate and do not reselect main frequency lists.

MLPIN24399is main-reference low(10/384): animal16/16,vehicle0/16, mean z7.292602vs0, with synonym/property replication. MLPIN8048is high(281/384): car16/16,bicycle3/16, but property weakens.24399is instead high under the original S09body-position axis(33/3072);8048becomes insufficient there. Frequency is conditional on source/position.

H3same-support fixed-list q directions replicate3/4explicit conditions: ATTNcat/dog13eligible,.063218[.053309,.074040]; ATTNcar/bicycle13,.011457[.005491,.016499]; MLPINcat/dog15,.040067[.037043,.043311]. MLPINvehicle11/16fails prespecified12eligibility. Matched random-list controls are insufficient. Cat/dognew-phrase projections reverse at both sites(−.010648/−.011056), with weak model behavior. Four exact-degree joint contrast intervals all cross0 despite passed constraints/mixing; no clear beyond-marginal replication, not proof of absence.

## Bounded judgments

H1: local descriptive support, not marginal-controlled semantic sharing. H2: no consistent directional support; animal insufficient and aggregate frequency-gradient inference limited. H3: local membership/amplitude support, beyond-marginal joint evidence insufficient. Frequent/shared/discriminative are not expert function, causal necessity or improved efficiency. New frames are independent of S10selection, not new lexical concepts; older heldout analyses are exploratory. Two named20261104source documents remain unavailable in bounded searches, so advisor wording is attributed to the user's account only.

Independent cached arithmetic verification:12298checks,zero failures; joint audit300checks. [Chinese complete summary](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/summary_cn.md),[Detailed](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/detailed.md),[cases](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/casebook_cn.md),[Protocol](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/protocol.md),[amendments](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/amendments.md),[reproduce](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/reproduce.md).

Only suggested next question: under a broader, still position-matched independent reference, does the coarse/fine discrimination frequency distribution remain stable for behaviorally reliable new paraphrases?
