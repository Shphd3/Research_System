# Result summary: locating the task-signal effect hidden by net help

Protocol: [posthoc analysis contract](protocol.md)  
Full evidence: [detailed.md](detailed.md)  
Original registered result: [0927 Summary](../../../0927/docs/shared_update_research_pack/summary.md)  
Status: **analysis complete; posthoc exploratory; researcher interpretation pending**.

## 1. Purpose

Locate the harmful task-signal component of an effective A update on B, identify the larger offsetting help, and test whether frozen SAE common atoms or alternative geometric/readout spaces locate the signed effect. The original registered comparison found modulation without net B harm; this analysis uses the same saved 192 virtual updates and cannot change that verdict.

## 2. Hypothesis

The matched \(t=\pm1\) displacement component may hurt B under the flipped rule, while a larger signal-invariant component helps B. The stronger common-space explanation predicts that the harmful signed contribution is concentrated in a shared representation space. A rival is that static shared activation, variance, or easy task decoding does not describe the actual update or its loss effect.

## 3. Analysis method

For each nuisance-matched pair, decompose \(\Delta a_t=b+t s\), with \(b=(\Delta a_++\Delta a_-)/2\) and \(s=(\Delta a_+-\Delta a_-)/2\). Cross the two components with frozen SAE-full, raw SVD, centered PCA, SAE-restricted PCA, ridge-probe span, and three same-rank random spaces fitted without B loss on the independent structure set. Evaluate signed terms with the saved B derivative; verify \(I=C_{P,sig}+C_{P,even}+C_{\perp,sig}+C_{\perp,even}+R\). Reuse the original 2,000 family/repeat/pair bootstrap draws for conditional 95% intervals. Probe labels come only from the structure set and its decoding is evaluated on independent readouts. All 12 previously viewed families are included; the fitted spaces remain fixed within bootstrap draws.

## 4. Conclusion

**The prespecified native task-signal sign pattern holds within this viewed construction, but its locally harmful term is a small part of a net helpful update.** At step \(10^{-4}\), high-overlap flipped B has \(C_{sig}=+8.3126\times10^{-5}\) nat/target, 95% CI \([8.2860,8.3411]\times10^{-5}\). Its signal-invariant contribution plus remainder is \(-0.0067480\), yielding observed \(I=-0.0066649\), CI \([-0.0066800,-0.0066492]\). High-overlap A and same-rule B have negative task-signal contributions, \(-1.0335\times10^{-4}\) and \(-8.2701\times10^{-5}\). The signal interaction \(M_{sig}=+1.4510\times10^{-4}\), CI \([1.4458,1.4571]\times10^{-4}\), accounts for most of the registered \(M=+1.5206\times10^{-4}\). All required signs hold at the half step as well. These are derivative-weighted local contributions, not a causal intervention.

**The tested static spaces do not contain most of the harmful signed contribution.** At high overlap/flipped B/step \(10^{-4}\), SAE-full captures \(+2.6766\times10^{-6}\) of \(C_{sig}\), leaving \(+8.0449\times10^{-5}\) outside; its excess over three random rank-32 spaces has CI \([-0.066,0.305]\times10^{-6}\). Centered PCA-8 captures \(+0.9040\times10^{-6}\) and has a small positive excess over random rank-8 \([0.153,0.319]\times10^{-6}\), but its complement still carries \(+8.2222\times10^{-5}\). Raw SVD-8 likewise has a small positive excess; neither supports majority localization. Probe rank-3 reads task labels perfectly within group and 0.875 across groups at matched overlap, yet its signed contribution is only \(+0.1984\times10^{-6}\), with random-rank-3 excess spanning zero. These same qualitative results hold at the half step. The frozen SAE task-signal reconstruction guard remains failed; projection capture does not repair it.

The geometric reason for caution is visible in the separate readouts: raw SVD's first axis captures nearly all mean energy but only 3.4% of B's centered variance; centered PCA-8 captures 96.8% of B centered variance and nearly all *static* task difference, yet only 1.09% of the actual task-signal **update displacement** energy. SAE-full captures 3.22% of that displacement; the remainder of the large helpful even term also lies mainly outside SAE-full (\(-0.0067065\) outside versus \(-0.0002232\) inside). A static task direction, a readable label, and the actual update path are therefore distinct measurements here.

![Native signal, offset, four signed terms, and net outcome](../../figures/shared_update_signal_even_fourterm_net.png)

Reading: the flipped task-signal term changes sign, while the much larger negative even term keeps the net outcome helpful.

![Candidate-space displacement capture and signed contribution](../../figures/shared_update_same_rank_capture_signed.png)

Reading: every tested span captures only a small fraction of the dynamic task-signal displacement; rank-8 PCA's small excess does not imply most signed harm is there.

![Static geometry and probe decoding](../../figures/shared_update_static_geometry_probe.png)

Reading: large static variance capture and high decoding accuracy coexist with weak localization of the update's signed consequence.

**Boundary and next decision.** These intervals condition on fixed spaces and the viewed 12 families; they do not establish new-family prediction, SAE-atom causality, or isolation benefit. The original `MODULATION_WITHOUT_NET_HARM` remains in force. The researcher must decide whether the residual task-signal effect merits a new targeted representation intervention; this analysis neither authorizes nor performs it.
