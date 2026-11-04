# A17_04 R06: Loss-directed update protection under fixed new exposure

## 1. Problem Definition
At equal new-task learning opportunities, does projecting the proposed update against an old-TRAIN loss gradient retain old rules better than ordinary updating and initial Top-16 coefficient attenuation, and does its relative value depend on old supervision? This is a bounded round under owner 17_04, not a new architecture. The current user explicitly authorizes the design, implementation, internal checks and complete bounded execution without intermediate approval.

## 2. Physical Priors
A local loss gradient predicts infinitesimal loss change, not finite-step or long-term retention. A large weight singular value need not identify a functionally sensitive update. Correct old supervision may itself explain retention.

## 3. Falsifiable Hypotheses
H1: initial Top-16 selection misses sensitive directions; F has extra old/new utility. H2: any benefit is only a smaller step and slower new learning; compare D. H3: old supervision explains most benefit; compare F-minus-U within each supervision level. These explanations can coexist.

## 4. Mathematical Model
Inputs contain visible mode, command and three different words. Mode one maps 甲 to FIRST and 乙 to LAST; mode two reverses the mappings. One answer token is supervised. Let theta concatenate the four final attention matrices. The objective is (sum of 36 new losses + sum of k active old losses)/72, k in {0,4,36}. The new coefficient stays 36/72. Separate 64 old TRAIN probes give g=gradient(mean probe loss). AdamW produces displacement d after objective-gradient clipping; moments are retained unchanged. Let q=g dot d and z=||g||². If q>0 and z>1e-24, dF=d-g*q/z, otherwise dF=d. U uses d; F uses dF; D scales d to ||dF||, retaining its direction (zero d gives zero update). S applies d+(a-1)P(d), where P is the R05 initial full-W0 paired Top-16 rank-one coefficient projector per matrix, and a=.01+.09*(1+cos(pi*t/1200))/2. This 1200-step schedule is truncated, not compressed to 240. All methods compute the same probe gradient; F/D use its labels even at k=0.

## 5. Computational Realization
Reuse the exact acquired-old four-matrix adapter, official Qwen3-0.6B Base, original TRAIN/DEV splits and R05 frozen-prefix cache. Recompute the native final block and full-vocabulary answer logits. Match new examples, old slots, active-slot rotation and probes across methods for each continuation seed. Compare four methods by three k values by three seeds; no architecture change or label use from DEV/TEST for protection. Reuse historical results only as background because their batch/exposure/probe policies differ.

## 6. Minimal Falsification Tests
At fixed step 240, operational F support requires mean old F-minus-U gain >=5 percentage points, positive gain in every seed, and new accuracy loss <=5 points in every seed. Compare S and D too; F not better than D leaves direction attribution unsupported. Also report old behavior/cost at the second consecutive new DEV accuracy >=90% reading, without replacing the primary endpoint. Report F-minus-U separately across old-supervision levels; no universal law fitted to three levels. Failed learning and missing conditions remain visible.

## 7. Current Evidence
Historical R02 establishes conditional compatibility under joint supervision and forgetting under reversed-only continuation; its mixed branch has fewer new examples. R05 attenuates selected coefficients without old retention. No equivalent 36-new/72-denominator/64-probe F-versus-D comparison was found in the inspected 17_04 protocol/summary records. This round: NOT RUN at freeze. All three continuation orders share one acquired-old model.

## 8. Claim Boundary And Next Decision
This tests a local old-label-assisted update rule and supervision organization on one model/data setting. It does not prove independent modules, low-rank routing, MoE necessity, capacity release, a natural-language feature-frequency mechanism or that Top-16 has no function. Frequency changes both label count and objective weight. TEST remains unopened this round; DEV is already exposed. After complete factual reporting, the decision is whether functional update constraints merit further investigation versus supervision organization. Scientific acceptance and closure remain researcher-owned.
