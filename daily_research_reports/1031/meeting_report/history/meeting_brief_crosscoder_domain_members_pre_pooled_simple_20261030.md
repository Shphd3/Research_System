# Meeting brief: discriminators, near-single-domain use and real tokens

Purpose: distinguish stable math/biology discrimination, sparse single-domain use, spectral location and token/context response using the unchanged A22 shared-z dictionary and cached natural documents. Scientific acceptance remains Unknown; exposed heldout statistics are exploratory.

## Belief update1: discrimination and near-single-domain use select different frequency compositions

R10 starts from16,384coordinates, either-domain≥5active discovery documents and oriented zero-inclusive document-mean AUC≥.75, yielding433math/527biology. High reference-frequency shares are66.7%/54.3%among classified members.

The discovery-frozen near-domain subset requires≥5preferred active documents,≤1/30opposite document and≥95%preferred positive positions:31math/24biology. Classified30/22members have low/middle/high9/19/2and12/9/1, median DCLM rates.400%/.217%. Thus near-single-domain use shifts lower, without implying global rarity. Heldout19/31and21/24retain the rule; all55remain. Strict14/15is separate, with8/13remaining strict. Original cuts.259399%/1.344299%and≥20reference hits apply; log-bin majority labels differ.

![Frequency](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/figure_frequency_near_domain.png)

Read columns as populations and y as member fractions; top labels give classified/frozen counts. DCLM nativez>0over65,536positions measures feature frequency, not token frequency or spectral location.

## Belief update2: similar spectral location can coexist with different actual use

Parent960unit-decoder PC overlap.9493and64PCoverlap.9686fall within the finer matched-PC reference.9466–.9576. First64means10.03%/11.52%,PC1only.053%/.120%,also within matched references. Geometry does not establish a special location beyond dictionary composition.

![Parent spectrum and actual use](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figures/figure3_overlap_and_use.png)

Top plots use unit-direction squared projection in one common pooled-discovery spectrum. Bottom uses the sum of scaledz×decoder vectors before projection and squaring. First64group-vector energy changes with input:mathgroup51.93%onmath/27.27%onbiology;biologygroup20.88%/49.70%. These are group-vector energy shares, not full-h variance explained. Near55geometry is separate:.8303PC/.9562binned,within same-size matched.8203–.8459. Do not compare different group sizes as special separation, or spectral distribution as function.

## Belief update3: near-single-domain use is not lexical exclusivity; partial same-token context association remains, but principal cause and semantics are unresolved

Fixed discovery-positivep90thresholds and≥5events/2heldout-document composition support retain25/31mathand18/24biology,with six per group insufficient. Normalize within features then average equally. Token categories freeze discovery INPUT coverage, not activation:shared≥5documents/domain;domain-associated≥5preferredand≤1opposite;remainingother/low-support. Evaluate40old-heldoutdocuments/6,400positions.

![FigureA](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/figureA_token_categories_and_names.png)

Read top x as categories,y as equal-member high-position fractions;gray bars use all available positions,diamonds match document exposure. Shared shares33.2%/31.7%,own-domain5.4%/10.2%,unclassified61.2%/58.0%. Neither a shared majority nor semantic domain-exclusive tokens are established. Shared input background37.0%;matched34.9%/38.2%. Math own-domain5.4%versus5.1%matched is small;biology10.2%versus2.4%is a panel composition shift.

Bottom shows actual top8IDs,including punctuation.Math includes`the`,`of`,`a`,comma,`in`,`sum`,`=`,`}`;biology includes`cells`,`cell`,period,`the`,comma.`cells`5.17%comes from3/18members.`Bat`comes from one member/one document and is retained without a group-level claim.Biology`the`is below its document-matched background.Commonness alone is not preference.

![FigureB](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/figureB_same_token_context.png)

Match exact target/previous-token IDs,genre,40-position-bin and sentence/paragraph boundary without activations;source level additionally matches host. All34eligible shared IDs are attempted;5reach≥5local-documentpairs. MainID279` the`has118math/171biologypositions across20documents/domain. Average high indicators across ALL31/24members,including zeros,within document pairs and then across pairs equally.15pairs/24positions give preferred-minus-other+1.22pp[.43,2.15]mathand+1.39[.14,3.06]biology;only6/31and5/24have any matched high support. Source matching leaves6pairs/10positions,one host,8.5%/5.8%of opportunities;biologyinterval[0,4.51]touches zero. Other4sufficiently paired IDs'intervals touch zero. These are1,000document-pair-bootstrap exploratory intervals,not all-token or all-member replication.

Bottom examples retain the first discovery-ranked member/domain:f16271respondsz=.0934above.0817after a math prefix versus0after a biology prefix.Fixedf1391is0on both matched prefixes and is insufficient coverage,not replaced.Cases illustrate;all pairs drive inference.Current identity alone does not explain every response,but terminology,topic,format and source remain live explanations.Full syntactic/semantic matching is absent.

## Prior visible context and later referents remain separate

6,400activation-blind40-token prior windows have randomizedIDs,rule proposals,five categories and blank human-review fields.Human review PENDING.Version1mistook no lexicon hit for generic narration;it is preserved,andv2requires a positive discourse cue or marks undetermined.No unreviewed semantic percentages support the main claims.`polygon`is a lexicon-miss counterexample;low-response`species`shows a term need not activate.

Fourthe/TheIDs have333positions;ID279has289and223following-first-word types,with211occurrences unseen in the discovery structure and48supported by≤2single-domain documents.All55×289=15,895rows keep prior text,z,thresholds,separate future previews and blank human noun-phrase/referent labels.Later lexical text is posthoc description only.The domain specificity of referents remains unanswered;missing labels are not a null result.

## Q&A and evidence

Why useful?Fixing word IDs and local environment weakens a current-identity-only account;document-matched backgrounds separate input commonness from composition shift.Why not semantics or function?Source/previous vocabulary remain confounded,human referent labels are missing,oldheldout is exposed,and no intervention/task benefit was measured.

[Full five-part Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary.md) · [Definitions/results/reproduction](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/supplement_near_domain_tokens.md) · [Members](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/near95_members.csv) · [Per-member top10tokens](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/per_member_token_top10.csv).18audit categories pass.Three main figures/three appendices;0new forwards/training/PCAfits.Stop after cache-supported delivery.Historical16+16brief bytes are retained in[history](history/meeting_brief_crosscoder_domain_members_pre_near_domain_20261030.md);different denominators must not be pooled.
