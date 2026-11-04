派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/anchor.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/anchor.md)；研究修改仍回到原件。

---

# Complement deletion of head64

## 1. Problem Definition
Under15_27_05/R16, does deleting the SAME layer's TRAIN PCA first64 centered directions, while retaining960, change native next-token prediction differently from retainingonly64? The researcher directly authorized both current-only andwhole-prefix frozen forward experiments. No new model/text/PCA/task or classifier.

## 2. Physical Priors
Prediction can depend on retained directions, source-position states andremaining computation. Common patterns are a WORKING_HYPOTHESIS,not a definition of PCA variance. Deletion andretention do not have symmetric effects through a nonlinear network.

## 3. Falsifiable Hypotheses
H1: the depth/scope response of head64deletion neednot mirror head64retention. H2: frozen common/format/other output groups maydiffer, butno semantic hierarchy is presumed. Rivals: rank/energy/norm, generic off-manifold perturbation, different downstream recovery and output alignment. Same-rank random64deletion and perposition energy helpbound,not fully eliminate them.

## 4. Mathematical Model
At ONE residual-post layer per condition, h'=h-(h-mu)QQ^T, Q=that layer's original R16first64 eigenvectors. This retainsmu and replaces only centered headcoordinates byzero. Oldkeep64=mu+(h-mu)QQ^T remains an immutable comparator. Whole-prefix changesall valid positions; current-only independently changesonetarget position. Final predictions come fromunchanged remainingnetwork,nativefinalnorm andhead.

## 5. Computational Realization
Same180physicaldocuments/737positions (175/700natural primary,37/the auxiliary), same28R16PCA andfrequency reference. Run deletionhead64 andthreefixed rank64random deletions. Reuse oldkeep64 results afternative/oldcondition replay checks. Save top10IDs/probabilities, originaltop1P/rank,actualsuccessorP/rank/NLL,KL/entropy,retainedenergy andperturbationnorm. NoPCArefit.

## 6. Minimal Falsification Tests
Require checkpoint/token/all-layer native targetstate replay; identity; complement algebra vsfull960basis inFP64; actual fullmodelhook vssuffix; lastlayerscopeequality. Freeze tiedmax=minID. Paired documentbootstrap. Keep/delete outcomes classifiedperposition asboth/keeponly/deleteonly/neither,withoutcalling this functional interaction. Numerical failures blockdependent rows; weakgroupcoverage orwideintervals remaininsufficient.

## 7. Current Evidence
R16keeper results arecomplete; deletion conditions were NOT_RUN atinitialfreeze. Completed supplement has207097combinedrecords;current-onlykeep64/delete64preservation at1/14/25/28is77.43/50.71%,74.71/57.43%,34.29/51.43%,23.00/32.57%. Stage-dependent relative advantage,notsemanticpartition. [Summary](summary.md) ownsmeasurements. Theycannotbe inferred fromretention. Supplement Summary/Detailed ownactualmeasurement.

## 8. Claim Boundary And Next Decision
Exposed English panel,onecheckpoint,oneR16TRAIN reference; equalranknot equalenergy. Correlates ofcommonIDretention cannotestablish coarse/fine semantic content orindependentlayerimportance. Deliverboundedrecognition update,retainfailures andleave acceptance/closureUnknown. Noautomaticnexttraining/run.
