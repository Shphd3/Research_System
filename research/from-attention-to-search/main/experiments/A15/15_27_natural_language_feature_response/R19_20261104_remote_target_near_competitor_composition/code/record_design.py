from common import *
import shutil,re
cfg=json.load(open(R/'config.json'));A=P/'main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_11_remote_target_near_competitor_composition_anchor.md';F=P/'main/focus/focus_remote_target_near_competitor_composition.md';stamp=now()
assert not A.exists()
anchor=r'''# Remote target facts and nearby competing objects in reused SAE combinations

## 1. Problem Definition

The researcher authorizes a new bounded step after R18 behavior: describe how target-fact content, distance and nearby competing words jointly change reused feature members/strengths, and whether those changes accompany candidate preference. R18's main facts succeeded24/24at16/64/128, while its opposite-item diagnostic succeeded17/24at128. That diagnostic changed both target and nearby word across A/B and used different filler from main. The present local representation question therefore needs a matched factorial frame, rather than treating those old rows as a single-factor treatment. The decision is which part of the proposed combination account has heldout descriptive support. Model/SAE training and activation interventions remain outside scope. R18 sources remain immutable.

## 2. Physical Priors

Changing visible words can affect both a sparse dictionary and answer probabilities; overlap, relative strength, lexical response and causal use are different objects. A fixed Top32budget forces entry/exit accounting and generates nontrivial overlap constraints. Single-feature frequency and positive-value marginals can produce apparent combinations, so joint evidence needs matched reference statistics. These motivate controls, not assumed semantic labels for atoms.

## 3. Falsifiable Hypotheses

H1content: a discovery-fixed common member list retains a target-fact contrast across fixed nearby contexts in new families. H2distance: the same fixed members retain aligned within-family A-minus-B contrasts from16to128, beyond swapping the far fact labels. H3competition: replacing a nearby unidentified object with the opposite item changes the combination and weakens the diagonal target contrast; its family-level change covaries with candidate-margin loss. H4joint, a separate identification check: discovery-fixed pairs exhibit heldout joint occurrence or joint strength beyond their respective exact-margin or positive-value-marginal references. The rival is generic question/word/format response plus marginal occurrence/strength, without replicated target-associated organization. Support may be local or insufficient; no branch is repaired by reselecting heldout atoms.

## 4. Mathematical Model

At the last prefix token p319, z is one native SAE's30000-dimensional nonnegative Top32activation; dictionaries are separate. A fixed list C gives raw z_C and relative q_C=z_C/||z_C||2. Strict common-list geometry requires every selected coordinate positive in all rows needed for that contrast; zeros/coverage are retained separately. Labels A/B identify a family's two words, not a universal semantic axis. Each heldout family's own near or neutral A−B difference is an explicitly paired reference, not a learned cross-family predictor.

In the matched128frame let x_ab denote z_C or q_C when the distant target is a and nearby word is b, with b=A/B; x_a0has a nearby unidentified object. Let delta0=x_A0−x_B0. Define T=((x_AA−x_BA)+(x_AB−x_BB))/2, N=((x_AA−x_AB)+(x_BA−x_BB))/2, and I=(x_AA−x_BA)−(x_AB−x_BB). The old opposite diagonal satisfies x_AB−x_BA=T−N exactly; the congruent diagonal is T+N. These are algebraic identities, not discoveries. Empirical quantities are their actual values, alignment/projection onto delta0, member changes and association with full-candidate margin loss. Positive target projection despite a failed answer is observable separation in this chosen dictionary/list, not proof that the model generally retains the information. Full-sequence scores include later candidate-token/period predictions; a p319feature association cannot localize all of that score to p319.

## 5. Computational Realization

Preserve R18 and reuse its exact official Base model/tokenizer plus native block27Attention-o_proj-output and post-normalizationMLP-input SAEs, each30000/Top32. Reuse144main prefixes,48opposite prefixes and4smoke prefixes; add96prefixes to complete target A/B × nearby unidentified/A/B at128. All prefixes320tokens; main d16/64/128 and matched d128use p−e−1 with both endpoints excluded and e the last item token. Matched target/near comparisons differ only in the named role's phrase, at fixed target e190/p319/question/filler. Across main distances absolute fact location/filler order still change; this is not a pure distance mechanism.

Twenty-four old behavioral families are newly partitioned12discovery/12representation-heldout: first two/last two of each existing four-family template stratum. Behavior is already exposed; new heldout sparse responses remain sealed until discovery selection/joint directions are frozen. Select a primary six-member common list, a nested three-member sensitivity and up to six responsive candidates using discovery only. Existing independently computed native reference groups use300natural discovery documents/38400positions, count/coverage eligibility and exact old bin edges. Preserve high/middle/low/insufficient/zero counts without forcing low-frequency participation.

## 6. Minimal Falsification Tests

Measure all384clean paired comparisons. H1uses neutral-to-fixed-near target-contrast alignment; H2uses16-to128paired-difference cosine and fact-swapped sign references. H3requires negative relative diagonal retention change plus behavior loss and a positive family association; matched-neutral behavior and strict common-member coverage protect interpretation. Complete candidate and item-only sensitivities stay separate. Six site×H1/H2/H3primary tests use Holm correction, family intervals and explicit insufficient branches; reference adequacy is at least8/12families. H4uses a separate four-test family for binary and strength residual replication at both sites, fixed on discovery. Binary Curveball preserves full-dictionary column counts and actual32members/row within condition/split; positive-value permutations preserve actual support and each feature's positive-value multiset. Forced margins, failed mixing, empty pair lists and low support remain insufficient. Exact implementation choices and thresholds are in Protocol; they are delegated operational choices, not universal scientific standards.

## 7. Current Evidence

R18's factual endpoint is preserved with its sentence-final-period sensitivity: main64word-only23/24but complete answer24/24;16/128stay24/24. Old main/opposite filler and simultaneous-word confounds have been verified from full original text. Before this new inference the matched behavior and SAE results are NOT RUN. A construction audit establishes token/role matching, not the hypothesis. Reference frequency counts and bins were replayed from the old native sparse cache. New results will link Summary with support, failure and missingness, without assigning scientific acceptance.

## 8. Claim Boundary And Next Decision

This round can support constructed-word conditional associations, reuse and jointly structured sparse responses at two frozen hooks. It cannot identify semantic atoms, a unique mechanism, causal necessity, cross-SAE ID equivalence or training/router value. Shared templates, lexical overlap, fixed-label conventions, dictionary loss and small family counts remain limits. Complete all independent factual/statistical work, deliver a readable example/counterexample and an under20MBreproducible packet, then STOP for researcher review before designing functional interventions or training. Scientific acceptance and next experimental choice remain Unknown.
'''
cn='''# 远处目标与近处竞争物品的SAE组合

## 1. Problem Definition

本轮由研究者明确授权：在R18之后，看目标事实、距离和近处竞争信息如何共同改变被复用的SAE成员／强弱，及其与候选偏好的关系。旧R18主条件三档均24/24，竞争诊断17/24；但旧竞争A/B同步交换两个位置的物品，主／竞争的填充也不同。因此本轮补齐匹配的析因框架，再判定哪些组合描述在留出家族成立。R18文件不改；不训练、不做激活干预。

## 2. Physical Priors

可见词同时影响字典响应与模型分数，但重叠、相对强弱、词面响应和因果使用不是同一对象。Top32预算约束换入／换出，边际频率与单成员幅值也可制造搭配现象。它们是对照理由，不是预设feature语义。

## 3. Falsifiable Hypotheses

H1事实：发现侧固定的共同列表，在近处词固定时仍有可复现的目标事实差异。H2距离：同一列表的家族内A−B差异从16到128保持同向，超过远处标签交换参照。H3竞争：近处不明物品换成相反候选后，组合和对角事实差异改变，并与家族候选边际损失相关。H4联合识别：发现侧固定的少数成员对，在留出中有超出出现边际或正幅值边际的共同出现／联合强度。竞争解释是问题／词面／格式与边际统计即可描述现象。失败或不足不触发留出重选。

## 4. Mathematical Model

在答案前最后token p319分别读两套原生SAE的30000维非负Top32激活z。固定列表C有原始z_C和相对向量q_C=z_C除以列表L2范数。严格共同列表几何要求所需行的每个候选都为正，缺失／零值另报。家族A/B是两个实际物品词，不是跨家族统一语义轴；留出家族自身近距或中性A−B差只作配对参照，不冒充跨家族学出的预测器。

匹配128框架中，x_ab表示远处目标a、近处词b下的固定列表向量；x_a0是近处不明物品。中性目标差delta0=x_A0−x_B0。T为固定近处词时目标A−B差的平均；N为固定目标时近处A−B差的平均；I是目标差随近处词改变的差。相反搭配的对角差x_AB−x_BA恒等于T−N，同向搭配为T+N。恒等式不是发现；需要测实际T、N、交互、与中性差的方向／投影和行为损失的关系。所选列表仍有同向目标差而答案错，只说明当前可观察量与判断分离。完整答案串分数还含后续候选token／句号，不能都定位在p319。

## 5. Computational Realization

复用官方Base模型／tokenizer及第28块Attention o_proj输出、归一化后MLP输入两套独立30000／Top32字典。复用144主文本、48旧相反搭配及4smoke；新增96条，补成远处A/B×近处不明/A/B。全前缀320token；主d16/64/128、匹配d128，d=p−e−1排除两端，e取物品最后token。匹配事实／近处对照只改对应位置词，保持e190、p319、问题和填充。旧主距离仍同时改变绝对位置与填充顺序，不声称纯距离机制。

旧24行为家族按每4家族模板分层，前2发现、后2留出，各12。行为已接触；新留出SAE响应直到固定候选和联合方向后才读取。仅发现侧选主要6个共同成员、嵌套3个敏感性及最多6个响应成员。频率直接沿用旧300自然发现文档／38400位置的各字典计数与分组；高／中／低／支持不足／零均保留，不凑低频成员。

## 6. Minimal Falsification Tests

完整384个干净配对：H1看固定近处词时的目标差与中性目标差同向；H2看16→128配对差余弦与标签交换参照；H3看对角保留量降低、候选边际下降及两者家族相关。中性条件行为和共同列表覆盖先检查，完整评分／去句号敏感性分开。每字典H1–H3共6主检验Holm，家族区间、至少8/12资格及不足分支预定。H4另有二值／强度×两字典4项检验。Curveball保持每条件／划分全字典列次数和每行实际32；幅值重排保持实际支持与每成员正值多重集合。强制边际、混合不足、空候选和低支持保持证据不足，细节见Protocol。

## 7. Current Evidence

R18旧结果与句号敏感性保持：64去句号23/24、完整24/24，16／128仍24/24。旧比较的两个词同步改变及填充混杂已由全文验证。本轮推理前，匹配行为和SAE结果NOT RUN；构造核验不等于假设通过。参考频率从旧原生稀疏缓存重放一致。新Summary将保留支持、失败、缺失，不授予科学接受。

## 8. Claim Boundary And Next Decision

本轮只支持固定模型、构造物品词、两真实hook下的条件关联、成员复用与联合统计；不识别语义原子、唯一机制、因果必要性、跨字典同ID或训练／router收益。共享模板、词面包含、字典遗漏和小样本保留。完成全部适用统计、完整例／反例与小于20MB可复算包后停止，等待研究者共同审阅，再讨论功能干预或训练。科学接受与下一决定Unknown。
'''
A.write_text(anchor);Ac=A.with_name(A.stem+'_cn.md');Ac.write_text(cn)
for name,src in [('anchor.md',A),('anchor_cn.md',Ac)]:
 (C/name).symlink_to(src)
F.write_text(f'''# Remote target and nearby competitor combinations

problem_key: `远处目标信息与近处竞争信息的 feature 组合`
anchor_id: `15_27_11`
question_state: `USER_ACTIVATED`
design_state: `FROZEN_BOUNDED_OBSERVATIONAL_COMPOSITION`
task_state: `AUTHORIZED_EXECUTION`
result_state: `NOT_RUN`
scientific_acceptance: `Unknown`

The current user explicitly authorizes all three comparisons and three analysis layers, existing model/SAE forwards, necessary matched supplements, validation/figures and an under20MB packet, then researcher review. Three steps: freeze role-matched texts and family splits; discovery-select and holdout-check membership/strength/joint patterns; relate to behavior and deliver raw evidence. Support is bounded descriptive replication; failure weakens the proposed pattern; missing coverage/mixing/behavior support remains insufficient. No automatic interventions or training. R18 remains byte-preserved.

[Anchor]({A}) · [Protocol]({C/'protocol.md'}). Next decision: researcher reviews the bounded combination account before any functional experiment.
''')
F.with_name(F.stem+'_cn.md').write_text(f'''# 远处目标与近处竞争的组合

问题标识：远处目标信息与近处竞争信息的 feature 组合；15_27_11。用户本轮明确激活并授权完整观察性分析与小于20MB结果包，之后共同审阅。三步：匹配文本／家族划分冻结→发现固定成员与联合方向、留出检查→行为联系、完整数据／图／报告。支持只作有界描述；失败削弱模式；覆盖／混合／行为不足保留证据不足。四独立状态见[英文Focus]({F.name})；无自动干预／训练，R18字节保留。
''')
protocol=f'''# Protocol: R19 remote-target/near-competitor SAE combinations

## 0. Approval snapshot

APPROVED_FOR_BOUNDED_LOCAL_ANALYSIS at {stamp}, by the current user's explicit complete-execution request. [Focus]({F}) and [Anchor]({A}) hold this same user-activated question. Role: observational comparison plus operationalization/robustness audit. Engineering operationalizations below are delegated choices, not independent scientific acceptance. Freeze before smoke; then discovery selection/joint directions must be hashed before any heldout feature forward. No training, classifier, dictionary fit, SVD, activation intervention, resource escalation or automatic next round.

## 1. Objects and observable

Two native SAEs separately: Attention block27.o_proj output before residual; actual block27.mlp input after residual and post-attention normalization. Each30000atoms,ReLU Top32,active iff saved selected z>0. Answer starts320; last prefix p319tokenID25for main records. Distance d=p−e−1excludes both endpoints; e is last item token. Save full actual text/token IDs/offsets, evidence/near IDs, all Top32 IDs/values, cutoff32/33, h and decoder column norms. Sparse IDs/values reconstruct all30000post-TopK activations exactly; inactive coordinates are zero. Full preactivations are not a required saved output.

## 2. Existing-data audit and matched supplements

R18source roots and exact protected file hashes: evidence/R18_protected_snapshot.json. Never change those sources. Main A/B only changed target word; main distances moved the same filler stock at fixed length. Old main vs lure changed filler/local clause; old lure A/B also swapped near word. They are legacy diagnostics, not clean target-only contrasts.

Read292prefixes:144old main,48old opposite,96new matched-neutral/congruent and4smoke. Each family has main16/64/128×targetA/B plus matched128×targetA/B×nearN/A/B=12rows. NearN usesobjector small object matched to candidate token count; it has no identifiable competitor, not an absent near clause. Keep the old opposite frame's exact rest-of-text and replace only role phrases. Main distances remain co-manipulated with absolute evidence position/filler order. Text_pairing.csvhas384clean comparisons, with both actual IDs and changed/held-fixed flags; legacy mismatch audit48rowsseparate. Existing neutral-target R18behavior baselines are copied read-only as prior diagnostics, not given new SAE forwards.

## 3. Split and prior exposure

24families F05–F28. Within each old4familyH1–H6template group, first2discovery,last2heldout:12/12. Family is the independent resampling unit; both facts/all distances/allnear contexts stay together. Templates are shared across the split, so this is new-family—not new-template—replication; template-cluster sensitivity uses six strata. R18behavior is already exposed; only new sparse-response validation is gated. No result-dependent family replacement. Illustrative case fixed before inference: first heldout family in original R18opposite-pair failures (F23); counterexample is first heldout family contradicting its observed pattern, or explicitly none. All family cases remain available.

## 4. Model, reference frequency and reuse

Exact official Base/tokenizer from R18 config, same two pretrained SAE weights/loaders as S06. Current strict asset checks are stored; exact full hashes in config. FP32 CPU2threads,SDPA,physical2×328right-padded shape, same native output head and complete leading-space noun phrase plus period. Old scores replay with max absolute total error<2e−5; capture hooks must be no-op, lane-prefix difference<1e−5. Native Top32 must exactly match manual ReLU/TopK encoding. Weights hashed before/after every stage. No trainable parameter or optimizer. Existing C++Curveball source from S09 is reused byte-for-byte; a small independent Python/set check validates constraints. Do not reuse CrossCoder IDs or frequency labels.

Frequency labels directly reuse each native dictionary's D1natural discovery300docs/38400positions. Positive count≥20anddocument coverage≥5; same-count tied boundaries retained. Attention count edges35/70and MLP-input33/62: low eligible counts below first,middle fromfirst to belowsecond,high≥second; zero and insufficient separate. Count/position cache and bin replay pass before this run. Save complete reference table and source hashes. Frequencies are a natural-corpus reference proxy, not training exposure or semantic role. Do not force candidates into all groups.

## 5. Stage contract

Prepare/freeze: verify every role-only paired edit, true token gap, unchanged local question/e/p and actual family split. Smoke4rows: native scorer old-response replay, no-op hooks, lane equality, exact encoder. Discovery144rows: all12discovery families×12conditions, native behavior first alongside extraction; only then select candidates and compute discovery nulls. Freeze both sites' candidates, scales, pair lists and signed joint directions. Heldout144rowscannot begin without that gate. Complete all analysis even if one hypothesis/site is ineligible; preserve named failures. Per-stage CPU wall ceiling3600seconds. No GPU/cloudjob. All actual outputs execution-side at{R}; canonical records at{C}.

## 6. Discovery-only member selection

On six main rows/family only, for each atom count families active in ALL six. Eligible common candidates require≥8/12families. Compute content score=sqrt(mean of within-family/distance(A−B)^2)/sqrt(mean main z^2); zero RMS ineligible. Rank common family count descending, then score descending, then atomID. Primary C=first6(or all if fewer), nested first3sensitivity. At least3members needed for combination geometry; never enlarge after heldout. Responsive R=up to6remaining atoms active in any main row in≥6families, rank same content score thenID. Pool U=CunionR≤12. Selection is not based on downstream behavior or heldout/null significance.

Primary relative q normalizes the SAME C list by its per-rowL2norm. For H1/H3strict geometry every C member must be active in all six matched-far rows; H2strict geometry requires all four near/far main rows. Record every actual support/zero, unused family and denominator; at least8eligible families needed for a primary decision. Also report fixed-list-with-zeros and first3sensitivities as descriptive, never rescue a failed primary. Raw z and decoder-norm-weighted per-atom changes accompany q; sums of absolute per-atom changes are not hidden-space energy or causal contribution.

## 7. Layer1 membership

For all384clean pairs save exact shared/entered/exited IDs and raw values, intersection/union,Jaccard and counts, separately per site and frequency group. Content factA/B, main same-fact distances and matched neutral→opposite/congruent comparisons each receive family-equal summaries. Fixed32implies equal entry/exit counts when both have32positive members. Fact-swapped near/far comparisons distinguish generic common-member overlap from fact-aligned reuse; no atom-name semantics inferred.

## 8. Layer2 within-family geometry and behavior

No universal A−Bsemantic direction is assumed across unrelated item pairs. In Crelative space, near delta16=q_main16,A−q_main16,Band far delta128analogous. H2primary=cos(delta16,delta128), with exact family sign swaps and95%family bootstrap. Also report64,full-supportJaccard matching vs fact swap and projection retention, not only centered midpoint geometry.

Matched128reference delta0=q_A0−q_B0. Define T,N,Iand opposite/congruent diagonals as in Anchor. H1primary=mean of cos(q_AA−q_BA,delta0)andcos(q_AB−q_BB,delta0), requiring both conditional norms>1e−6and delta0norm>1e−6. These neutral/near target contrasts use disjoint condition rows, with a family reference rather than a trained prediction. Save each raw/relative vector and per-feature T/N/I. Exact identities are quality checks only.

H3pattern loss=1−dot(delta_opp,delta0)/||delta0||². Behavior loss=family mean correct-candidate margin(neutral)minus(opposite), using full candidate scores, with item-only sensitivity. H3primary=Spearman family association(patternloss,behaviorloss),9999family-label permutations,one-sided positive; require positive mean pattern loss and positive mean behavior loss with95%CIs,plus positive association interval and Holm pass. Template-stratified exact2^6permutation sensitivity is reported separately. Neutral behavior<80%paired or fewer8strict families means insufficient task/geometry support, not ignored rows. Positive Tprojection with a failed pair supports only observable direction retention in C; nonpositive/reduced projection describes weakness, not global information erasure. Ratios near-zero denominator remain NA; all raw norms retained.

## 9. Layer3 beyond marginal occurrence and strength

U fixed from discovery. Consider all its unordered pairs (≤66). Within each of six condition strata and split, save single occurrence/positive amplitude/RMS and pair coactivation/standardized strength product. Scale amplitude by discovery-main per-feature RMS (fixed before heldout), not per-row total; row normalization can itself induce dependence.

Binary reference: S09Curveball full30000column counts and32unique positions/row exactly preserved; strata are condition×split, each24rows=2facts×12families. This asks pooled within-condition joint structure; it does not preserve semantic family labels or prove a mechanism. Four chains,100burn sweeps,64draws×10thin; failed/no-op trades counted, actual constraints checked every draw, lockedsites and retention reported. If row active counts are not32, binary null is unavailable rather than padded by invented members. MixingRhat≤1.10,ESS≥100on decision scalar; a single preallowed burn500/thin50retry if inadequate, both runs retained. Degenerate margin-forced traces are NOT evidence of structure or successful mixing.

Amplitude reference: preserve actual full binary support and each feature's exact positive-value multiset WITHIN condition, independently permute positives across its active rows. This preserves feature occurrence and row activation counts, but not row total amplitude/norm.256independentdraws(4seeds×64), no MCMC claim. Joint product=z_i/RMS_i×z_j/RMS_j; difference from this reference isolates joint strength conditional on this support and marginal multiset, not pure semantics.

Discovery pair selection: require both active together in≥4distinct families in at least one stratum and nondegenerate null variation in≥2strata. Per kind select up to4pairs ranked by absolute mean observed-minus-null residual across six strata, tie IDs. Both positive and negative discovery residuals allowed. Freeze the6×pairs residual vector's unit direction; no eligible pair or zero vector means insufficient. Heldout omnibus score projects actual-minus-own-null into that fixed direction. Four site×kindtests use a separate Holm4family and conditional-null p=(1+tailcount)/257;95%family bootstrapconditional on fixed nullcenter/direction. Save full null traces, selected-pair values, per-family contributions and finite Monte Carlo limitation. No ratios of expected intersections substituted into Jaccard, no broad all-combinations claim.

## 10. Decision rules and uncertainty

For H1/H2, lower95%family interval>0andexact sign-swap Holm6p≤.05with≥8familiessupports bounded replication. Negative upper interval or opposite prediction is not supported; a wide interval, poor coverage or weak behavior is insufficient. H3requires all declared conjunctions; if combinations change but association/behavior link fails, mark LOCAL_SUPPORT for the descriptive component and not a full behavioral explanation. Six primary p-values include two sites×three hypotheses; invalid p=1preserves multiplicity. H4separate Holm4as above. No scientific acceptance or unique causal interpretation follows from any pass. Only descriptive comparisons with at least one supported component may be local; never upgrade underpowered zero into a negative mechanism.

Family bootstrap4096,seed2026110419; paired conditions stay together. Template-cluster intervals resample six full strata; report small support and shared-template limitation. Old behavioral outcomes are exposed and never called fresh confirmation. All missing,failed,zero,reference-insufficient and degenerate values remain explicit. Both sites are separately interpreted; any claimed difference requires direct paired effect-difference interval, not one significant/one not.

## 11. Outputs, scope and amendments

Deliver per-family full texts/IDs/scores/sparse activations and pairing table; discovery selection/directions/frequency metadata; membership/strength/behavior and joint-null figures; complete predefinedF23case plus counterexample; bilingual Summary/Detailed,one Chinese meeting entry and under20MBlocal ZIP. Full weights/h/preactivation or large null states remain execution-side with omission indexes; all key sparse rows, raw behavior and null statistic traces fit the package. Offline replay must work without model/weights and reproduce decisive values. ZIPCRC,new-directory extraction,per-fileSHA,all portable links and size verified. Local Anchor sync follows standing workflow; no commit/push/external publication.

R18 protected files and owning behavior Anchor/Focus must retain exact bytes. This new sibling owner15_27_11does not rewrite R18scientific state. Freeze Protocol/config/panel/code before smoke. Later changes append UTC,before/after,reason,already-visible data,affected scope,authorization and eligibility; keep original body and failed versions. Processing-agent self-review covers scientific identification,data/statistics and numerical implementation; no independent-human-review claim. Completion stops before functional intervention/training design, pending researcher review.
'''
(C/'protocol.md').write_text(protocol)
(C/'protocol_cn.md').write_text(f'''# R19协议中文阅读

当前用户已直接授权完整有界SAE组合分析及小于20MB结果包，完成后停止；精确合同为[英文Protocol](protocol.md)，冻结于{stamp}。科学接受Unknown，无训练／激活干预。

## 文本和划分

292前缀＝144旧主＋48旧相反近处搭配＋96新匹配中性／同向＋4smoke。每个正式家族12行：主d16/64/128×事实A/B，加匹配d128×目标A/B×近处不明/A/B。384干净配对：固定近处改目标、固定事实主距离、固定远事实只改近处词。旧主与旧竞争的填充不同、旧竞争A/B同步改两处，另列48条混杂审计。全长320、p319；远e190，d=p−e−1两端排除。R18全部文件和旧Anchor／Focus保存哈希，不改。

24家族每个旧4家族模板分层前2发现后2留出，各12；同家族所有条件同行。模板在两侧共享，故只是新家族检验。行为已接触，新的留出feature直到候选和联合方向哈希冻结才前向。

## 模型、字典、频率

复用原模型、tokenizer及两处独立30000／Top32 SAE，FP32、CPU2线程、固定2×328。Attention是block27.o_proj残差前输出，MLP输入是post-attention归一化后实际输入。保存真实前缀／端点token、完整Top32 ID和值、cutoff32/33、h和decoder范数；零坐标由稀疏表示精确重建。旧原生完整候选评分重放<2e−5、capture无操作差0、lane差<1e−5、native与手工编码一致。

频率直接沿用原D1各字典300自然发现文档／38400位置，命中≥20且覆盖≥5文档才分档。Attention计数边界35/70，MLP输入33/62；同计数不拆组。高／中／低／不足／零全部保存，从旧原生缓存核验计数与分组，不重分到有利结果。

## 成员和强弱

发现主6行中每feature统计“一个家族六行都活跃”的家族数，≥8/12才能进共同候选。按家族数、归一化事实响应RMS、ID排序；主要固定前6，前3敏感性；至少3才分析组合几何。另选最多6个响应候选，要求≥6家族任一主行出现。严格几何保留全C正值的家族；H1／H3看全部匹配6行，H2看近远4行。至少8/12资格；不合格与全零保留，不用敏感性救回失败主检验。

层1保存全部384配对的交集、换入换出、原值和Jaccard及频率组。层2固定列表分别看原始z与L2相对q。不同家族A/B只是不同物品词，不拟合跨家族共同语义方向。H1比较固定近处A、B时的目标差与近处不明时目标差的方向；H2比较同家族主16→128的A−B差余弦；H3看“1−相反对角差在中性目标差上的投影保留量”与正确候选边际损失的家族Spearman相关。

匹配析因T＝固定近处词的目标A−B差平均；N＝固定目标的近处A−B差平均；I＝两种近处词下目标差的差。相反对角差恒等于T−N，同向为T+N；恒等式只是实现核验。保留T投影但判断错是当前观测量与输出分离，不证明一般目标信息仍在；完整候选分数包含后续token／句号，不能全归于p319。

## 超出单成员边际的检验

U为固定共同与响应列表的并集≤12。仅发现侧各选最多4二值对和4幅值对：至少一个条件中共同出现≥4家族，至少两个条件有非退化零模型变化；按六条件平均残差绝对值排序，正负均可，方向冻结。留出投影到发现残差方向；没有合格对就证据不足，不扩池。

二值Curveball复用S09 C++，每个条件／划分24行上严格保持全30000列出现次数和每行32。4链，burn100、thin10、每链64；检查全部边际、锁定成员、混合Rhat≤1.10／ESS≥100，必要时仅一次预定burn500／thin50重试。强制边际的常数轨迹不是支持。幅值参照在实际支持不变时，逐成员独立重排该条件的正值多重集合；保留出现次数和每行成员数，但不保留每行总幅值。联合强度为两成员各除发现RMS后的乘积，不用行归一化制造依赖。保存256零模型轨迹及逐家族贡献。

## 判定与停止

H1/H2：家族95%区间下界>0、精确家族符号交换经Holm6通过且≥8资格，才支持有界复现。H3还需平均组合损失和行为损失均为正、相关区间正及Holm6通过；中性匹配行为低于80%或资格不足则不足。只有组合变化而行为联系不够，最多局部支持。联合4检验另Holm4，必须零模型／支持合格。4096次家族bootstrap，9999次相关标签置换；六模板整组区间与模板内置换单列。两SAE独立，不据一边显著另一边不显著推位置差。

交付原始配对／稀疏激活／完整评分、固定候选、频率组、所有图、F23预选完整例与反例、中英报告、一个中文组会入口、<20MB可复算ZIP；大权重／大缓存仅路径清单。离线复算、ZIP CRC、解压逐文件SHA与便携链接验证。完成后STOP，等待研究者共同审阅；不自动干预或训练。任何协议修改须追加时间、旧新值、原因、已见数据、范围、授权及资格，保留原正文。
''')
shutil.copy(C/'protocol.md',R/'protocol.md');shutil.copy(C/'protocol_cn.md',R/'protocol_cn.md')
dump(R/'evidence/pre_run_audits.json',dict(UTC=stamp,scientific=dict(status='SELF_REVIEW_PASS',rival='word/format/marginal response vs replicated target-associated geometry',causal_claim=False),data_statistics=dict(status='PASS',old_behavior_exposed=True,new_feature_split_sealed=True,matched_supplements=96,pairing=384,template_clusters=6),implementation=dict(status='AWAITING_SMOKE',training_parameters=0,asset_checks='PASS',reference_counts_replayed=True)))
dump(R/'evidence/freeze.json',dict(UTC=stamp,authorization='Current direct complete execution request',hashes={str(f):sha(f) for f in [A,Ac,F,C/'protocol.md',C/'protocol_cn.md',R/'config.json',R/'data/panel.jsonl',R/'data/text_pairing.csv',*sorted((R/'code').glob('*.py')),*sorted((R/'code').glob('*.cpp'))]}))
M=SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md';ms=M.read_text();M.write_text(re.sub(r'^Latest update at: .+$','Latest update at: '+stamp,ms,count=1,flags=re.M))
with M.open('a') as f:f.write(f'''\n\n## {stamp} -- 用户授权R19目标／竞争组合分析，设计先冻结

Processed by: Codex /root (harness: Codex desktop; model: GPT-6)

- Summary: 本轮用户明确授权两原生SAE、三个比较、成员／强弱／超边际联合统计、行为联系、图和<20MB包，完成后共同审阅再决定功能实验。此前“无SAE授权”的停止状态由当前请求在此有界范围内取代；训练／激活干预仍无授权。
- Current work: R18全部文件／旧Anchor与Focus已哈希保护，不编辑；新独立R19及15_27_11owner。发现12／留出12家庭同侧，行为已接触但新feature未读。补96前缀成匹配远目标A/B×近处不明/A/B，292总前向含4smoke，384干净比较。参考频率与原生SAE资产核实。尚未前向。
- Next action: smoke→发现前向／固定成员和联合方向→留出前向→完整统计、原文例／反例、图、报告和可复算小包→STOP。无新模型／字典训练，无功能干预。
- References: {A};{C/'protocol.md'};{R/'config.json'};{R/'data/text_pairing.csv'};{R/'evidence/R18_protected_snapshot.json'}。
''')
print('DESIGN_FROZEN',stamp)
