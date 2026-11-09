# Detailed: actual R02 procedure and eligibility

The [Summary](summary.md) gives separateQ1/Q2/Q3answers;the [object comparison](object_comparison.md) distinguishes old definitions. The frozen[Protocol](protocol.md) owns execution. This record owns actual observations and failures;scientific acceptance/closure remainUnknown.

## Objects and controls

Primary:existingofficialQwen3-0.6B(28layers,hidden1024,BF16eval/no-gradSDPA)andnativeE16FP32ReLUTop32SAE,F30000. Capturezero-based27post-attention-normalizedMLPinput,beforeMLP. No input unit normalization or decoder-bias subtraction. Save rawz,c=z×saveddecodercolumnL2norm,andc/actualhooknorm separately;bias is separate and contribution magnitude is not explained variance.

BothR01splits are exposed discovery. Its64candidates,7groups,scales andnuisance coefficients remain fixed. PrimaryQ1groupsG01/G02/G04/G06/G07depend onoldDcoassignment>=.70,not newfrequency. Q2primary=G02/G04onbass,BH2;othergroups/types and64×2feature tests aresecondary. Q3uses7×2group tests,BH14,andseparateBH128secondaryfeatures. Secondary results cannot rescue primary failures.

New12cases contain6bass order×selected-item scenarios and6person occupation×object bindings. Fourconditions×2distances=96,plus12matchedcue2-neutraland12weekdaycontrols=120. Text is Codexconstructed natural language andcontrolled editing,not unmodified corpus. Bass itself was chosen fromexposedR01evidence;newwordings/entities/sourcegroups do not overlapR01andwere not selected usingR02response. Threepositions have the same token within each case:bassID21529orisID374. Factorial/control positions andfinal near/far lengths/positions/lastfive tokens match. Cue2gap6/7versus48/49defines bins;cue1gap is separately recorded. Early near/far positions differ,somain stage comparisons use short only. Beforecue2,allowed candidate sets contain no future unique label. Length112–139.

## Independent reference and real-corpus descriptions

Freeze16TRAINbins×64disjoint256-token windows=1024,burn16,245760counted positions. Model/hash/hook/FP32encoder/Top32match the panel. Frequency=count/N;report counts,hit windows,descriptive tokenWilsonCI andprimary2000window-blockbootstrapCI. Windows are not verified independent original documents;intervals reflect window-resampling variability,not universal language coverage. Eligibility requires20hitsand8hit windows. Zero/NAare retained;Jeffreys.5smoothing is only for bootstrap logs,notpoint replacement.

The availableCrossCoder uses14residual-post vectors normalized bysavedTRAINmean/RMS,one sharedF16384z,andstrict saved score threshold.051281172782182693,not per-tokenTop256. Native layer contribution=z_f×rms_l×decodercolumnnorm;mean/bias stay separate. Fresh model/dictionary/source/cache identities match19files. Cachedrows0–7join to the samecontext's first8tokens,M/um/ia/:/Folk/Hero/or/Cold,not8documents. Separate fixedfirst8reference windows have a constantposition127SAEdescription;the windows were fixed before inference,the position selected before descriptive cache inspection,no response filtering. Neither sample replaces controlled confirmation. Dictionary IDs are not aligned;layer contributions are not independent activations or a generation chain.

## Qualification and bounded diagnosis

Reference meanNMSE=.05990,p90=.10544;panel360readouts mean=.07916,p90=.09556. Both reconstruction gates and decoder identities(~1e-7)pass;four identical-condition replays havez difference0. OriginallongB01early-prefixhrelative errors=.01561/.01080 exceed.01;firststagezmaxerror2.7818exceeds.4267. Short truncated checks haveherror0andzerror~4e-6/6e-6. Eight fixed diagnostic calls compare truncation andsame-shape masking under original tolerances,but do not resolve the discrepancy or uniquely identify the cause. This is observed numerical execution-path inconsistency,notproof of future lexical leakage.

OriginalProtocol/code/text/candidates/thresholds are unchanged;[E1](amendments.md)records8extra diagnostic calls. R02=1160forwards;R01+R02=1452<=1500. Main120andreference1024remainfixed. No training,activation replacement,sealedTEST,new resources orpurchase. Existing40GBH100MIGonly. Originalpanelqualification remainsFAIL;allnew-panel statistics are conditional descriptions. Frozen mechanical tests are preserved but never promoted to confirmation. [Eligibility](provenance/analysis_eligibility.json).

## Old groups andQ1

Originalcandidate/groups reproduce. ExposedoldHG02r=.83562,G04r=.65630remain unchanged inR01. New conditional null matches6target activation-counts and6response-counts within1case,logRMSwithin1SD,nearest20,withoutreplacement. G02member pools2/2/1cannot produce3distinct matches;twoG04pools areempty. Both have0validmatchedgroups,below800draws/20uniquegroups. This does not reject their old correlation,but leaves the target-support rival unresolved.

Q1dispersion=meanunorderedmember-pair absolute log-frequency difference,then equalweight acrossfivefixedgroups. G01=.453,G02=1.211,G04=2.949,G06=.687;G07includesf5596with18hits<20,making the primary globalstatisticNA. Each of500nulls permutes complete4-versionfeaturetuples within target,retaining marginals/target support,andreruns support,RMS,rank,cap64,globalamplitudeOLS,correlation,average-linkagecut.5/min3,and200bootstrapstability>=.70. Only392nulls arevalid,below400;no extra draws or group deletion. Primaryp remainsNA,not nonsignificance or refutation. G04f1818/f1205counts4634/45withwindowCI[.01393,.02442]/[.0000692,.0003418]are anabout103-fold descriptive counterexample to a universal all-members-same-frequency rule,not a replacement for the incomplete globalnull test.

## ConditionalQ2/Q3readouts

BasssemanticcontrastS=(10+01−00−11)/2=instrument−fish;peopleretain4edit edges. Q2usesgroupRMS afterfixedoldDfeaturescaling,notpercentage or variance share. G02short/long=.00998/.10349,delta+.09351,CI[−.00463,.26918];G04=.02564/.01196,delta−.01368. Memberminimumsupports1/6and3/6arebelow4. G04's bootstrapinterval excludes0butexactdistancep=.125andcontextguardfails;selecting the interval alone would violate the contract. Directgroupdifference=.10719,p=.0625andqualificationfails. Distance/order/recency varyjointly.

At eachpositionI=11−10−01+00,andbassI=−2Sexactly,not independent evidence. Registeredgain=norm(I2)−norm(I1)−norm(Ifinal−I2),withsame-positionrealcue-minusweekdayguard. Exactonesidedpvalues form anintersection-unionmaximum,BH14;bothCIbounds,support,templates,andpredefinedsemanticmappingmustpass. Unequal advancement lengths andSAEnonlinearity remain rivals.

G02interactionRMS=0/.32075/.01996,gain=.00889withCIcrossing0;G04=0/.16422/.05127,gain=.00430withCIcrossing0. Everybasscasefavors compatible candidates inonly2/4conditions;personmappinglikewise fails. Thus there is no completeQ3support even ignoring the numericalgate. Personisandbassare separate;inactiveoldbassfeatures onpersonreadouts do not show a lostsemantic hierarchy. Allsinglecue,joint,interaction,weekdayandneutral-advancecomponents atallthreepositions remain saved.

## Figures,examples anddelivery

[Figure1](figures/figure1_relations_frequency.png)usesfixedtreeorder,newnear/fardifferencesandmatchedreferencecounts. Graymeans insufficient support/NA,notzero. [Figure2](figures/figure2_distance_effects.png)shows same-final-position semantic effects/candidate preferences;dashedlineslackmember support. [Figure3](figures/figure3_progressive_integration.png)showsinteraction,single/jointedits andirrelevant/neutral controls;no single rising line establishes integration. Titles/captions retain failedqualification. Separate rendering changes layout only.

[Examples](examples.md)give oldbank/f6401success,newB01bass/f19601visible-prefixconsistency,andf1818nonadditivitywithoutsemanticcorrespondence. No newscientific success passes every confirmation guard. [Artifact manifest](artifact_manifest.md)owns allcode/data/hashes,actualsaved asset IDs andfailure eligibility. Registration/access never upgrades science. Two reportable updates andoneAI-suggested next experiment appear only at the end of theSummary;no follow-up is executed.
