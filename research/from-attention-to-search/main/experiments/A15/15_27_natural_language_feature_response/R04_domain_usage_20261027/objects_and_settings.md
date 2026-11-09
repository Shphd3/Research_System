# Adopted objects and settings

User amendment A01 authorizes native E16 last-block local SAE as primary and native A22 shared-z/last-layer reconstruction contribution as a separate analysis. Both use identical texts, independently selected discovery candidates and validation. The aggregate new sequence-forward cap remains512. The original blocked interface receipt is preserved; no branch-only encoder is introduced.

E16:30000 features, zero-based block27 MLP input after post-attention layernorm, original FP32 ReLU Top32, activation z>0, native contribution z times decoder-column norm. A22:16384 shared features, block1,3,...27 residual-post inputs, frozen TRAIN centering/vector-L2-RMS, original BF16 encoder GEMM and saved threshold. Last-layer native-scale contribution is shared z times decoder27 norm times TRAIN RMS27. This is not a final-layer-independent activation.

Both use the same frozen Qwen3-0.6B-Base only after weight/tokenizer identity qualification. Different dictionaries have distinct feature IDs. Hook/training differences prevent architecture-quality attribution. No LM or dictionary training, branch slicing, interventions, attention, new clustering, spectra, cross-model analysis, new tasks/resources or sealed TEST.

The original two experiments retain120 real English documents (60/domain; discovery/development/heldout30/10/20 per domain;192tokens, measure33–192) and72 controlled prefixes (12families;6discovery/6heldout; identical target tokens, suffix, absolute position and length). Each dictionary independently selects at most32 shared and32 biased candidates (16/domain); equal smaller even k>=8 if needed. Model/dictionary sparsity is unchanged. DCLM frequency uses a fully matching cache or up to256 traceable deduplicated reference windows. Paired domain edits measure context sensitivity, not physical distance.

Actual inputs are120real DCLM-sourcewebdocuments withURL/WARC/lineidentity,72controlledprefixes and256referencewindows. M2D2paragraphs were not used as independentarticles. Source qualification and both experiments completed;details/limits are in Detailed.

## Actual completion
Bothnativebranches completed456/512sequenceforwards;all8numericalchecks andstage reconstructionguards passed. Eachdictselected32shared+32biased;newresults in summary.md. Original blockedA22lastlayer-only requirement is historical. No thirdreadout or newresource.
