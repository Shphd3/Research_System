# Figure reading guide

[Chinese full captions with real examples and counterexamples](figures_cn.md).

1. [Heldout usage heatmap](figures/figure1_usage.png):rows fixedfeatures,columns20math+20biodocuments,color mean native contribution/discoverytokenRMS. Sidebars DCLMfrequency;*<20hits. Discovery fixes colorlimits and candidate order. This is usage,not naturalcluster proof. ExampleSAEf9730hits363/3200mathvs0bio;counterSAEf29506sharedpresencebutF11wordings haveoppositecontextdirections.
2. [Readability/frequency](figures/figure2_readability_frequency.png):Apoint=32dimprobe,graypoint=matchedrandomset;YheldoutBA,95%documentCI. Bpoint=feature,XDCLMrate,YheldoutJeffreyslog2math/bioratio withdescriptiveCI. ExampleCCf12314DCLM.2106%butheldoutbio1.9375%,math0. CounterCCbiasedprobe.975versusmatchedrandommean.95625andrandommax1.0. Classification doesnot establish purity,actualmodeluse,uniqueness or formationcausality.
3. [Fixedtarget response](figures/figure3_fixed_target.png):topcell=feature/family,math-minus-bio andabsoluteirrelevantedits normalizedbydiscoveryRMS;bottompoint=onefamilygroupE=D-U. ExampleCCf12314method contribution0→19.3588;counterexampleall6exampleversions0. Fourgroupconfirmationcriteria not met. Context terminology,preamble/edit-size/sense rivals remain;no physicaldistance mechanism.
