# R20: member turnover without average loss of code-level fact separation

In this object-fact task at gaps16–128tokens, the observations favor membership reorganization with retained fact-contrast magnitude, rather than uniform attenuation. Common members retain a very similar relative arrangement, while member identity and the direction of the small A-minus-B contrast change. These are fixed-SAE code measurements, not a measure of total model memory.

Three analysis paths are kept distinct: (1)behavior and factor controls; (2)representations and layerwise organization; (3)functional interventions and measurement quality. Functional interventions were not run by scope; numerical and reconstruction quality were audited.

## Question, objects and original evidence

The alternatives were stable composition, turnover with retained differences, and attenuated fact differences. R19's selected-six direction did not resolve magnitude. We reuse all144main prefixes and retain all12old heldout families, with12discovery families exploratory. Prior heldout responses were exposed; this is a reanalysis, not untouched confirmation.

The model is frozen Qwen3-0.6B Base. Native SAEs observe block27Attention.o_proj output and actual post-residual/post-normalizationMLP input, separately; each has30000coordinates/ReLU Top32. Prefix length320, p319colon tokenID25. Gap=p−e−1excludes both endpoints; e302/254/190gives16/64/128. Missing selected coordinates are actual postTop32zero; no favorable-family filtering is used.

## Main observations

Across16→128, mean common members are24.79/32Attention and27.92/32MLP; entries/exits7.21and4.08. Their equality follows the fixed budget. Common-member raw norm ratios are0.9675/0.9876and common direction cosines0.9976/0.9987. A stable large common vector does not imply a stable small fact difference.

Raw full-code fact-difference norm ratios are1.0456/1.1839; total code RMS-scale ratios0.9679/0.9874. Relative separation divides the A-minus-Bnorm by RMS of the two row norms, removing uniform scale. Its ratios are1.0803,95%familyCI[0.9899,1.1725],and1.1989,[1.0976,1.3307]. Whole-code magnitude does not uniformly shrink. Full raw fact-direction cosines are0.5978/0.7307; unit-row contrasts give0.5929/0.7260. Fixed-six unit-row contrasts across all12families give0.9427/0.9614; the old strict six/family subsets0.9678(N6)/0.9713(N11)are reproduced exactly. Selected-six stability cannot substitute for the whole code or magnitude.

About88%/83%of turnover instances meet the predeclared cutoff-near rule, and about99%of entrants already have a positive encoder response belowTop32at near distance. Rectified preTopK direction cosines are0.8833/0.9080. This is a truncation diagnostic, not a newly trained SAE or an intervention. Turnover is not equivalent to new/erased semantics, nor is every threshold crossing merely noise.

## Frequency, controls and behavior

In72main heldout positions, reference-high/middle/low observed members are136/50/18Attention and63/30/25MLP. Low groups cover70and72positions,all12families. Reference-zero/insufficient remain separate. Frequency is fixed from independent300document/38400position native reference corpora, not word frequency, spectral position or training exposure.

Attention's4.33high-frequency entrants are close to4.43expected from reference-weighted opportunity. MLP's0.708low entrants exceed natural/discovery-task expectations0.321/0.402at the mean, but family intervals cross zero. Dictionary sizes, left-at-risk counts, rank-matched exits and conditional entry opportunities are reported; raw group counts do not establish importance.

New execution comprises228control conditions:192new texts and36same-textposition-IDvariants. Reverse weather and length-matched office filler each use72prefixes; fixed evidence e190adds48near/midprefixes and reuses24old far rows; uniform positionIDs+64uses36rows in six template-covering families. Four smoke rows are reused; six old rows calibrate exact scoring. No weights,optimizer or training change occurs.

Relative fact-separation128/16ratios under reverse/content/fixed-e areAttention1.123/1.104/1.079andMLP1.138/1.118/1.137(allN12). None shows mean attenuation. Office replacement also changes repetition/lexical content. Uniform position-index shifts retain32/32members with max candidate-score discrepancy about3.9e−5nat. This computational coordinate shift does not add visible text. Because d=p−e−1,these controls do not identify an unrestricted pure-distance effect.

Original full-candidate paired accuracy remains12/12at every distance; mean margins6.4209/6.6187/6.8925nat. Item-only64is11/12and is retained separately. Reverse16has one failure(F28stamp,margin−0.084757); reverse64/128and office/fixed-e remain12/12. All failed texts/scores are preserved. Filler order can matter even near the answer.

## Cases, operational hypotheses and knowledge update

The frozen rule selectsF11(relatively high retention,yet slightly smaller contrasts),F15(largest turnover without weaker contrast),F27(small mixed changes),andF19(Attention ratio0.79versusMLP1.89,all answers correct). Full two-fact/three-distance texts and all union members are linked in the casebook. No other family is deleted.

H1retention≥90%is not supported at either site. H2relative magnitude within[0.8,1.25]is supported forAttention(Holm p0.01465); MLP is insufficient because its growth interval extends above1.25,not because of attenuation. H3mean attenuation≥20%is not supported at either site. These are registered AI operational tolerances, not universal ability criteria. Six tests use Holm;8192whole-family bootstrap and six-template sensitivity retain all families. Exact paired sign-swap tests assume symmetric family location errors.

The knowledge update is that successful fact use in this window can coexist with membership turnover and small shared-member strength changes,without average loss of code-level fact-separation magnitude. The fact-difference direction reorganizes, and the choice of members/truncation affects apparent stability.


Template sensitivity qualifies this result: aggregating to six template means and enumerating64sign patterns gives Attention H2raw p0.03125,Holm p0.1875,insufficient; MLP is also insufficient. Family-primary verdicts stay unchanged, but equivalence is not confirmed across independent templates.

## Measurement limit and one next question

SAE reconstruction of actual hook-input A-minus-Bdifferences has median relative error about0.994/0.984,much worse than ordinary row reconstruction. Code norms are therefore not total factual information. Shared templates,exposed holdout,limited reference corpus and the local gap range also limit claims. No causal necessity,general memory law,semantic atom identity or router benefit is established.

AI-suggested sole next question: which of these reorganized,but not on-average attenuated,fact differences are actually used to read out the answer? No intervention/training design is executed automatically; scientific acceptance remains pending review.

[Numeric annex](numeric_evidence.md),[cases](casebook.md),[frequency](frequency.md),[Detailed](detailed.md),and[artifact index](artifacts.md)retain complete evidence. Coverage: old-data analysis,cases/frequency,228controls and numerical quality DONE_VALID; discovery-only observations remain exploratory; figures,code/configuration,short talks and reproducible evidence are delivered. STOP for review.
