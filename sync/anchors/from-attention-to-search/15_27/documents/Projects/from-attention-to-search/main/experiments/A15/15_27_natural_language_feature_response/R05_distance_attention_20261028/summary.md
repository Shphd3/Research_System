派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/summary.md)；研究修改仍回到原件。

---

# R05: Distant-content responses and Attention endpoint coactivation

We ask which frozen features reproducibly respond to distant prefix content, then describe independent DCLM rates, Attention endpoint sharing and joint-dictionary layer contributions. B compares relevant versus unrelated edits at16/48/80/112/144tokens; A compares high versus middle Attention positions within matched32token bins.

All authorized inference is complete:960Bprefixes,120ArealR04documents,16checks/failedattempts=1096/1096. No training, interventions, new resources, sealedTEST or additional reference forwards. Native E16block27MLPinput is the local primary readout; A22forms sharedz from14odd-block residual-post inputs. Its last-layer magnitude is sharedz times native last decoder norm, not independent last-layer activation.

B selected20SAE/25CC candidates using discovery only. None met all heldout/minimumeffect/support/pooledBH conditions at any distance; no far or near-with-far-attenuation category was confirmed. This is insufficient evidence, not absence. The heldout split also changes target nouns; repetitive neutral padding and edit-size/order differences constrain generalization. CCf447 has last-layer contributions9.920/0forplantat144inonewording but0/0in the alternative wording.

A provides bounded support for near-distance association: in40heldoutdocuments, CC high-frequency features show1.934869%versus1.515126%joint-hit rate at1–32tokens,difference0.419742percentagepoints,95%CI[0.372916,0.466901],pooledq=.0285. All25B-insufficientCCcandidates jointly differ by1.153664points,alsoq=.0285. These overlapping sets are not independent causal evidence. The high-frequency far-bin difference is0.043742points,CI[.023089,.064679],below the prespecified.1pointminimum. Same-ID matched support is4/6/7/8/7documents,below10,so not estimable. Small positive estimates do not pass a test against the nonzero minimum.

Layer profiles describe fixed decoder organization. Forf447,the heldout far sharedz mean.002118929 times native block27norm633.710117 gives1.342787contribution;divide independent A-discovery layerRMS609.319126 to obtain.002203750. A single sharedz drives all14layers,so profile shape cannot show information emergence or propagation.

All120A-doc token CSRactivations exactly match R04.1937offline audits passed. Eager-switch and initial attention-helper failures are retained and rejected. Final causalQKprobabilities were validated againstFP64reference on every officialAforward without extra prefixes;maximum probability absolute error<7.4e-7 and weightedVrelativeerror.002136. Probability and representation units remain separate.

Knowledge updates: a large distant local response does not establish a robust cross-wording feature; near Attention sharing does not confirm distant-content dependence. Only suggested next question,notrun: doesf447respond at144tokens withfixedplant across independent natural wordings and nonrepetitive fillers?

See [Chinese first reading](%E6%98%8E%E6%97%A9%E5%85%88%E8%AF%BB%E8%BF%99%E4%B8%AA.md),[Detailed](detailed.md),[figures](figures_cn.md),and[exact settings](protocol.md). Mechanism acceptance/question closure remain Unknown.
