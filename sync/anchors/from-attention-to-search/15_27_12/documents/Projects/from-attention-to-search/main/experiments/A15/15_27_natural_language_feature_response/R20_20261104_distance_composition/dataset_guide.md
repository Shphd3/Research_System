派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/dataset_guide.md)；研究修改仍回到原件。

---

# Data and methods

The actual panel has372conditions:144R19main prefixes,192new literal prefixes(reverse72,office72,fixed-e-near/mid48),and36same-textposition-IDvariants. A fixed-e distant point reuses the old main128row;24far rows are aliases in that analysis,not additional samples. The new scored LM calls are228control conditions plus6old calibrations;4new smoke conditions are included in228and not rerun. A further no-opforward checks hook identity without adding an observation. Old cached hook inputs are re-encoded288times(two dictionaries×144prefixes),with zero LM forwards and exact Top32agreement.

panel.jsonlretains complete English prefixes,alltokenIDs/offsets,last-item/answer positions and full candidate IDs. Each native postTop32code has30000coordinates; indices/values list all32positive coordinates and every other coordinate is post-truncation zero. Inactive does not imply a zero encoder response. IMPORTANT: the cache key `pre_relu` is a legacy field name for `relu(encoder(h))` BEFORE TopK,not the signed linear pre-ReLU vector. It is a threshold diagnostic,not another trained dictionary. h and reconstruction retain actual1024-dimensional hook input and native decoder reconstruction.

ATTN_SAEcaptures block27.self_attn.o_projoutput before residual; MLPIN_SAEcaptures actualblock27.mlpinput after residual and post_attention_layernorm. Native metadata matches layer/model configuration; the exact official model/tokenizer and both weight/loader hashes are in the frozen configuration. No dictionary ID is shared across sites. No normalization precedes native encoding. The sourceSAEs were previously trained; none was trained or modified inR20.

Gap d=p−e−1excludes both endpoints,e=last object token. Baseline/reverse/office prefixes have320tokens,p319colonID25,e302/254/190. Fixed-e has e190,p207/255/319. Pos64retains identical text and token positions but supplies allpositionIDs+64; visiblep319corresponds suppliedID383. It is a computational encoding-index test,not64addedvisible tokens. Full candidate strings include leading space,item and period,with equal token counts within each family.

The12old heldout families remain primary;12discovery families remain exploratory. Both old behavior and sparse results were exposed before this round. New controls reuse the same families and shared six templates,not new independent families. Facts/distances/controls stay together under family bootstrap. The four case rules are fixed inProtocol; all others remain in raw tables.

Full-code fact separation is ||zA-zB||/sqrt((||zA||²+||zB||²)/2). Raw difference norm,totalcode scale and direction are separately stored. Common-member changes and allentering/exiting strengths are retained. Coordinate squared-change sums and decoder-norm-weighted absolute changes do not equal hidden-space energy,output contribution or causal importance. Fixed6members use literal zeros and allfamilies; old strict-support is only a replay sensitivity.

Frequency labels exactly reuse each native D1reference:300natural discoverydocuments,38400positions;count≥20anddocumentcoverage≥5for high/middle/low. Attention edges35/70;MLP33/62;tied boundaries upward. Insufficient and zero groups are separate. Both source cache/table/metadata hashes are current and bins are recomputed. Reference occurrence is not training exposure,word frequency,spectral location or semantic importance. Natural- and discovery-task-weighted conditional opportunities and rank-matched exits are descriptive models,not hidden causal controls.

Frozenconfig.jsoncontains three inherited,unused R19provenance fields(prefix_count292,new_prefixes96,panel_sha256ofR19). Actual execution used the correctR20panel_rows372/new_forward_rows228and literal IDlists. effective_config.jsonscopes those legacy fields and supplies currentSHA/counts/actual assetIDs. The frozen original is retained; A1qualifies metadata only. No numerical input or result was changed.
