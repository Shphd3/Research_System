# R04 native feature domain analysis

Assets `data_a15_27_r04_domain_native_dual_20261027` and `analysis_a15_27_r04_native_sae_joint_cc_domain_20261027` register actual fixedtexts,native activations/counts,decoder scales,probes and boundedcontextanalysis. [Summary](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/summary.md) and [current selected output access](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/provenance/output_access.json).

E16 is nativeFP32Top32block27MLPinput. A22is native14-layerjointzwith TRAINnormalization/BF16encoder/savedthreshold; final-layer native contribution is sharedz*TRAIN_RMS27*decoder27norm. Not a last-layer-independentencoder. SameBasebytes/tokenizer,texts;separatefeaturecoordinates/candidates/validation.

456/512newBaseforwards,120documents,72controlledprefixes,256DCLMwindows/65536positions/254documentgroups. Bothdicts32biaseddirectionsrecurandprobesreadlabels,but no fixedtargetgroup meets combinedconfirmation. Specificsource/style,terminology/preamble/edit-size andsparse-support boundaries remain. No LM/dictionarytraining,resources,intervention,attention,spectra,reclustering or sealedTEST. Registration/access does not grant scientific acceptance.
