派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements/20261102_pc1_pc2_pc8_pc16/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements/20261102_pc1_pc2_pc8_pc16/summary.md)；研究修改仍回到原件。

---

# R13 supplement: rank1 PC1/PC2 and cumulative first8/first16

The current user authorized this frozen-native-decoder supplement. Same official Qwen checkpoint,pre-final-norm block27 cache,TRAIN PCA mean/basis,737 original positions in two exploratory panels. Keep TRAIN mean in every condition, then originalRMSNorm and tied head. PC1/k16/mean-only/full are reused with numeric replay; onlyPC2alone/k8 are new. No model/classifier/PCA/dictionary training and no new transformer activations.

The original plot categories are tokenizer-ID classes, not complete-word semantics. Reference frequency top1% excludes Unicode punctuation/whitespace-onlyIDs;1412referencecommon non-formatIDs,4547formatIDs. Actual natural full-top1 members are165commonIDs/386positions/163documents,31formatIDs/108positions/81documents,remaining206positions/125documents. The37/the panel has14commonIDs/16documents,oneformatID(newline)inonedocument,and20otherdocuments. Group document supports overlap. Common group includes digits,subwords,currency/mathsymbols such as dollar and equals; preserve these original definitions rather than silently reclassify.

Complete literal memberships are in inventory_cn.md and observed_original_top1_IDs_complete.csv, reference universe in reference_group_IDs_complete.csv. Raw fixed contexts remain English in text_cases_cn.md. Group recovery means average positions within each supportingdocument then average documents;2000document-bootstrap pointwise95%intervals. No group membership or sample selection changes. PC1vsPC2 matches dimension but not variance/energy; first8vs16 changes both. Mean-only remains the output-bias reference. The bilingual numerical result tables follow below.

|condition|natural common recovery|natural format recovery|natural other recovery|natural NLL|natural KL|
|---|---:|---:|---:|---:|---:|
|k1|2.15% [0.56, 4.14]|10.49% [4.94, 17.28]|0.00% [0.00, 0.00]|10.5938|8.2299|
|pc2|6.95% [4.50, 9.87]|3.70% [0.00, 8.64]|0.00% [0.00, 0.00]|9.5771|7.1800|
|k8|9.46% [6.29, 13.04]|27.57% [18.72, 36.83]|0.00% [0.00, 0.00]|8.4107|6.0992|
|k16|14.37% [10.69, 18.40]|26.13% [17.49, 35.19]|0.00% [0.00, 0.00]|7.4357|5.1193|

These measurements distinguish retained native predictions and output bias; they do not establish semantic granularity or mechanism. Scientific acceptance remainsUnknown. [Chinese complete result/plots](summary_cn.md),[protocol](../../../../../../../../../../UNAVAILABLE.md),[complete raw ID inventories](../../../../../../../../../../UNAVAILABLE.md),[paired group contrasts](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements/20261102_pc1_pc2_pc8_pc16/evidence/group_paired_contrasts.csv).

Pairednatural contrasts:PC2minusPC1common+4.81percentagepoints[1.64,8.08],format−6.79[−12.96,−1.23]. First16minusfirst8common+4.91[2.97,7.00],format−1.44[−7.00,3.91],so no established format decline. Other206full-top1positions never retain their originaltop1underthese4conditions;this is not absence of information. The/the panel recovers no originaltop1underPC1,PC2orfirst8,andonly2documentsunderfirst16. PC1outputsopening-parenthesis417times/comma207timesbutretainsoriginalsforonly1/9positions;highformatoutputcontainsbackgroundbias. PC2retains22the,2digit1and2inpositions.
