派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/definitions_A02.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/definitions_A02.md)；研究修改仍回到原件。

---

# R11 A02: definitions and reporting changes

Counts,denominators and claims are distinct. New three-domain values cannot be spliced into old two-domain denominators.

| Object | Actual definition/denominator | Boundary |
|---|---|---|
|Document response|Mean native z including zeros at32–191;equal documents|Tokens are not independent documents|
|Three-domain S|Minimum of two oriented pairwise document AUCs;half ties;60×60D comparisons|MainS≥.75,noHreplacement|
|Main|Full16,384,ownDsupport≥5andS≥.75;129/133/27|DisjointIDsnot spatial evidence|
|Near|Within main,eachopponent≤3/60Ddocs,preferred positive-position share≥95%;2/5/1|Finite-panel label|
|Strict|Within main,bothopponentszeroD;1/0/0|0retainedinH;distinctfromlegacy7/9|
|Feature occurrence|IndependentDCLMz>0/65,536,min20hits|Originalcuts.2593994%/1.3442993%|
|Log sensitivity|Cuts.4517255%/6.6865057%|Never replaces original bins|
|Input-token frequency|Dcounts/28,800;type-tertilelow1,mid2,high≥3|Hunknownseparate;notfeaturefrequency|
|Shared token|D≥5docsineachof3or exactly2withthirdzero|Availability,not semanticcommonness|
|D-single token|OneDdomain≥5docs,bothotherszero|Notautomaticallytechnicalterm|
|Unit projection|Squared unitdecoderPCinnerproducts,sum1024=1|Noz/eigenvalue/normweighting|
|Spectral overlap|Sumper-PCminimaofmember-equalgroupmeans|NotID,directionorfunctionoverlap|
|Primary/secondary basis|FixedR10/newthree-domainDcommonmeanPCA|R07sameasR10,notindependent|
|Activation/contribution|Nativezstrength/groupreconstructionareotherobjects|Geometryisnotenergy|

Relative to R10,new data,sample size,opponent domains and Sdefinition change jointly;differences cannot be attributed solely to physics. R10originally fit math/biology common Dtext;R11preregistered it as fixed primary and treats new three-domain PCA separately. Token categories are now frozen on new D/evaluated on H. Old globalTop16is9math/7bio,legacystrict16is7math/9bio,oldper-domain16is16+16;mapping columns remain distinct. See[Summary](summary_A02.md)and[alltables](reproduce_A02.md).
