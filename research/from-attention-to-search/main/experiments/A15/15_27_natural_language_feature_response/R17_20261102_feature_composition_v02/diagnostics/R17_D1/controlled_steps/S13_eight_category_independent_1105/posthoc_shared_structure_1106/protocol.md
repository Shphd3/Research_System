# S13 supplementary set decomposition and sharing scope

Status: authorized cache-only exploratory analysis, fixed before new decomposition outputs. UTC freeze is in evidence/analysis_freeze.json. This supplements S13 under the existing member-composition question, not a new research route, blind confirmation, router proposal or replacement of any S11–S13 result.

Purpose: answer the advisor's separate questions at meeting H-01 P052/P058 (sharing extending to less common members) and P064 (where distinguishing members lie). Reuse exact S13 data: DEV24 frames/8 clusters and CONF48 frames/16 clusters, 24 labels, four wordings, two independent native SAE dictionaries. No new texts, model forward, training, intervention, new null simulation or readout fitting. Scientific acceptance and closure remain Unknown.

## Assets and units

S13 official Qwen3-0.6B Base, block27 Attention o_proj output / actual MLP input, 30000/ReLU/Top32, final Description: colon. Independent dictionary IDs. Exact text/token/position and native sparse positive-z support are authoritative. Cache rows follow the filtered panel split order. Both Q6000 questions (2000 each Magicoder/GSM8K/MMLU) and G6000 DCLM are exact S11 caches. Count<5 is insufficient reference support, zero is unobserved, neither renamed low frequency. No reference amplitudes are needed for the frequency axis. No weight loading.

One frame contains all label versions; three related frames form one scene cluster. Point estimates: frame means then equal scene-cluster means; bootstrap 2000 whole CONF clusters, seed2026110613. Intervals condition on fixed reference counts and fixed descriptive rules, NOT S13 joint reference/text intervals. All new statistics on CONF are posthoc/exploratory. No p-value-based discovery or new hypothesis acceptance.

## Two distinct partitions

Fixed parent blocks: animal/vehicle, fruit/furniture, clothing/instrument, flower/cutlery. For each domain and frame/wording/site let C=intersection of its fixed parent-block supports and F=intersection of its two children. Define R=C∩F, L=C\F, E=F\C. R,L,E are disjoint. Report C,R,L,F,E counts; R/C retention, E/F extra share, R/F overlap. Each fraction uses its own observed denominator; empty sets are missing, not zero reference means. Extra means absent from the *coarse shared intersection*, not absent from both parent texts and not temporally newly created.

For each nonempty group report member-equal mean/linear quartiles of Q/G frequencies, supported/unobserved fractions, and raw z / z/fullTop32L2 in all four constituent rows (parent, comparison parent, child A, child B). Across frames, preserve family-equal CDFs and averages of within-frame quantiles; pooled member-event quantiles are an explicitly separate object. Export every member-event ID and four raw amplitudes.

Explain the mean decrease exactly where R>0:

D=mean(C)-mean(F)
 = |E|/|F| * [mean(R)-mean(E)]
 + |L|/|C| * [mean(L)-mean(R)].

Both terms retain signs. Term1 is dilution/reweighting by extra F members; term2 is composition of coarse-only members. Show absolute pp contributions and intervals. Their ratio to D is descriptive and can exceed100% if terms oppose; not causal attribution. Verify identity per frame; if R=0 report identity unavailable, no filled value.

Separately for own parent P and children A/B, partition their union into seven exact regions: PAB, AB_only, PA_only, PB_only, P_only, A_only, B_only. Codes specify positive membership; all missing sides mean not selected Top32. Export every region ID/value/frequency, all counts and amplitude changes. Shared siblings not in P differs from E above; never equate these partitions. Child-only need not be semantically exclusive. No reanalysis of preactivation is needed; S13 already found most Top32 exits still had positive encoder response.

## Continuous frequency and auxiliary bins

Primary axis is p=count/6000, each reference separate. Auxiliary low/middle/high are thirds of the *supported independent-reference dictionary coordinates* sorted by frequency, with linear 1/3 and2/3 quantiles: low<=q1, middle(q1,q2], high>q2. Equal frequencies never split. Count<5 is insufficient; count0 separate. Save actual thresholds and bin dictionary denominators, activated/group-event fractions. These are relative dictionary bins, not semantic/knowledge labels and not selected-panel quantiles. Show continuous means/quantiles even if nearly all selected members fall into one bin.

## Feature coverage and candidate rules

Compute every ever-active feature's label presence, conditional/unconditional raw z and full-L2-normalized z, across frames and clusters, separately DEV/CONF and four wordings; inactive values are0 for incidence/unconditional means, excluded for conditional means. Record total scale, length, position and original behavior eligibility. Stable label: presence>=.75 and >=.75 of clusters having presence>=2/3. Stable sibling: joint presence with the same criterion.

Fix candidates using DEV explicit only, while acknowledging DEV/CONF are already exposed. Cross-parent candidate: stable in >=4 parent labels and both children stable in >=4 domains. Sibling-local candidate for domain d: stable sibling joint presence in d, mean presence across the14 other fine labels<=.25, and at most1 other domain with sibling coactivation>=.5. Fine-incidence candidate: one child's presence>=.75, other's<=.25, magnitude difference>=.5, and consistent sign in >=6/8 clusters. Shared-strength candidate: stable sibling coactivation, raw and normalized mean differences have the same sign, >=.75 of coactive frames have that normalized sign and >=6/8 clusters the same mean sign. This is a single-member strength difference, not interaction.

Export all candidates. Representatives: at most2 broad/site sorted by coverage thenID; at most1 sibling-local/site/domain sorted by mean Q/G reference percentile among eligible candidates (lower first); at most1 incidence and1 shared-strength/site/domain sorted by DEV effect thenID. No CONF replacement; absent category remains absent. Classifications may overlap; categories are operational usage patterns, not semantic ground truth. CONF reports same IDs, all direction reversals, coverage failures and wording sensitivity. Thresholds are descriptive cutoffs, not power guarantees. No full-dictionary significance scan.

Show label coverage and reference frequency separately. Compute all feature parent/fine stable coverage and cluster occurrence distributions on CONF explicit, with original DEV candidates distinguished. In addition, for E member-events report whether the same coordinate is broad/shared across other labels versus truly meeting sibling-local rules; absent from one coarse intersection must not be interpreted as narrow sharing.

## Controls, cases and delivery

All four existing wordings are computed separately; interpretation of implicit wordings only where original S13 frozen full-sequence behavior gates passed. Mean-token sensitivity remains a qualification, not a replacement criterion. For all seven alternative direct-parent baselines, reuse cached rows to compute descriptive decomposition summaries; child-mixture is average over four actual cross-parent fine-pair decompositions, not a synthetic support union. Fixed original block remains main. No null/mechanism claim is added.

Cases: original N004 animal/cat/dog; the median explicit MLP animal D frame (ID tie break); explicit domain/site with lowest retention (choose family median retention for its case). Keep all cases even when ordinary/counter to the layered interpretation. Fixed DEV representative features shown in first coactive CONF family and one non-coactive/direction counterexample when available, no invented examples. Full case table has exact texts, indices, z/q, Q/G counts, category and cluster coverage.

One main figure (original blocks, counts and reference means) plus coverage-frequency and seven-region case audit. White background, raw values, separate SAE/reference axes, cluster intervals or family dots. PNG/SVG and figure input CSV. Chinese report follows purpose, conclusion (raw evidence then analysis), mechanism intuition/hypotheses, experiment analysis. It first answers meeting H-01; distinguishes observation, compatible interpretation and remaining question. English companion and reproducible source index; preserve original reports. At most one next question. Save full tables/scripts/config, audit set/count/decomposition identities and input hashes; compact review archive excludes weights and unrelated old outputs.
