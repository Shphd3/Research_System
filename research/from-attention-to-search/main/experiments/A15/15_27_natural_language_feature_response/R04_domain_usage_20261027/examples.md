# Worked real examples and counterexample

Illustrations were selected after frozen statistics for explanation only. Full exact texts,IDs and numbers are in the [Chinese companion](examples_cn.md);machine data are in analysis/*_context_feature_effects.npz.

CCf12314 at F09method(token1714,pos30):mathz0,bioz.03484364;native decoder27norm=1.48414743*TRAIN_RMS27(374.34951210)=555.58986611;native contribution0→19.35877. Secondwordingbio contribution17.73107;bioirrelevantedition15.83208. Only1/32biasedmembers changes in thisfamily. This is shared14-layer activation decoded at block27,not local encoding or explainedvariance.

SAEf12478 at F11difference(token6672,pos30):mathz0,bio5.27339/2.54142 acrosswordings;nativedecodernorm1. NativeMLP-input contribution equalsz;discoveryRMS1.16135. It hits579/3200heldoutbio and4/3200mathpositions.

SAEf9730:hits363/3200heldoutmath,0/3200bio;DCLM132/65536. In all6heldoutfamilies it is inactive at the generic target;documentlabel usage is not universal fixedtargetcontextresponse.

Counterexample:CCf12314 at F08example(token3110,pos32)is0inall6versions;wholebiasedgroupE=0. CCsharedgroupF08E=-.08341 versus F07+.08900. Singleexamples cannot override the6family confirmation.
