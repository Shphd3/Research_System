派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_01_fixed_target_domain_spectrum_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_01_fixed_target_domain_spectrum_anchor.md)；研究修改仍回到原件。

---

# A15_27_01: fixed-target domain response and spectral location

## 1. Problem Definition
Does changing only the visible math/biology context produce a direction of difference at an identical final target token that generalizes across wordings and heldout families? If it does, which portions of an independently fitted real-representation spectrum permit domain readout? EarlierR04document classification anddocumentmean differences do not establish fixed-target context generalization. This subquestion inheritsA15_27's visible-prefix response question and replaces feature proxies with realblock27residual-post. Two analyses answer one bounded question; clustering,causalmechanisms,routing andexpert allocation are out of scope.

## 2. Physical Priors
A causal target representation may depend on its visible prefix;futuretext must not change it. Rewording and family-heldout tests can restrict particularword/template explanations but cannot certify puresemantics. A PCA basis fitted on independent naturaltexts provides fixed directions of decreasing corpusvariance;variance rank is not semantic complexity.

## 3. Falsifiable Hypotheses
H1: a discovery-fixed math-minus-biology direction retains its sign across bothwordings andbothneutralendings in unseenfamilies. Rival: the apparent difference depends on specificterms/templates orlength and fails when these change. Length/targetID/position are paired,wording/family generalization is measured,remaining vocabulary overlap is reported. H2isconditional: ifH1replicates,its direction andsame-dimensionalreadoutability can be located in the fixedspectrum without assuminghead ortail superiority.

## 4. Mathematical Model
One observation is a1024-dimensional truehiddenvector h at a finaltarget,forfamilyf,domaind,wordingw,endinge. Discoverydelta is the meanmathvector minus meanbiologyvector,withfamilies/versions equal. Unitdirection u=delta/L2norm(delta);its sign andscoremidpoint are fixed ondiscovery. Heldoutpairedscore differences testgeneralization. For fixedorthonormalPCcolumns V,bandenergy=sum(u dot V_j)^2 over64directionrankbands;completebasis energies sum1without eigenvalue multiplication. Readoutminimizes meanbinarylogloss plus L2penalty in the chosen projectedspace withanintercept;onlydiscoverylabels fit weights,development selects thepenalty,familyheldout evaluates once. No language-model parameters change.

## 5. Computational Realization
Construct48pairedEnglishfamilies,two wordings/domain,two identicalneutralendings=384inputs. Each family/ending matches targetID andabsolute position acrossbothdomains andwordings using bounded natural framing,notrepetitive filler. Split24/12/12families beforeforward. Extract oneblock27output vector perinput beforefinalmodelnorm,BF16toFP32;runidenticalprefix/differentfuturechecks. ReuseR04realCC_hcommonPCA:60independentnaturaldiscoverydocuments×160positions,pooledmean,noextraunitstandardization,1024directions. This hook is the same as theCrossCoder finalinput,but noCrossCoderreconstruction orfeatureiscomputed. Comparehead/tail/randomsame-dimensional16,32,64,128,256andfullreadouts withidenticalglobal scaling anddevelopmentselection.

## 6. Minimal Falsification Tests
Hold the targetID/ending/position fixed,swap contexts,andtest the frozen direction on12heldoutfamilies. Family-level labelswaps preserve all versions;bootstrap families ratherthan individualrows. A pooledandfourcellpositivepairedscore result withpositive95%familyintervals andBH5q<.05supports bounded replication;failedcells orwideintervals restrictit. Spectralprojection is descriptiveifreplication fails. Equal-dimensionalreadoutcurves compareaccessibility,not deletion safety orallpossible classifiers. Causality/hookidentity failures stop dependent evidence ratherthan changingobjects.

## 7. Current Evidence
The authorized R07 experiment completed 384 main inputs and eight interface/causality/replay checks, 392 forwards in total. All checks reproduced the expected vectors exactly and the frozen model state remained unchanged. The discovery-fixed direction has a positive mean paired effect in all four heldout wording/ending cells; the pooled difference is 60.64 with a 95% family interval [46.79,75.29], and all five registered tests meet BH5 q<.05. Twelve of twelve family-averaged differences are positive, while seven of forty-eight individual variants reverse. The fixed zero-threshold classifier achieves only 60.42%; ending-dependent score offsets remain material.

The discovery unit mean-difference direction places 58.12% of its squared length in the first 64 old natural-text PCs. Heldout mean-direction cosine with discovery is 0.832. Separate, frozen linear readouts obtain 98.96% in the first 16 PCs, 90.63% in the last 16, and 97.92% in the last 64; the full-dimensional baseline is 98.96%. Thus low-dimensional head accessibility and substantial tail readability coexist. These are paired-context/domain associations, not a map of knowledge. Shared vocabulary and neutral framing remain alternatives. The complete numerical evidence belongs to the [R07 Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R07_fixed_target_domain_spectrum_20261029/summary.md) and [Detailed record](../../../../experiments/A15/15_27_natural_language_feature_response/R07_fixed_target_domain_spectrum_20261029/detailed.md). Human mechanism acceptance and closure remain Unknown.

## 8. Claim Boundary And Next Decision
The permitted answer concerns domain-associated context differences in these paired texts andthisfrozenmodel/interface. It doesnot locate mathknowledge,provepuresemanticcausality,naturalclusters,featureimportance,formationlayers,orjustifyexperts/routing. The researcher reviews the complete result andremaining lexical/template alternatives before selecting one next question;mechanismacceptance andclosure remainUnknown.
