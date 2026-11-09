from pathlib import Path
import json,shutil
import pandas as pd
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements')/P.name;O=E.parents[1]
M=json.load(open(E/'manifest.json'));S=pd.read_csv(E/'analysis/summary_metrics.csv');C=pd.read_csv(E/'analysis/context_controls.csv');D=pd.read_csv(E/'analysis/band_definitions.csv');counts=pd.read_csv(E/'analysis/output_top1_counts.csv',keep_default_na=False);contexts={r['position_uid']:r for r in [json.loads(l) for l in (E/'analysis/contexts.jsonl').read_text().splitlines()]};raw=[json.loads(l) for l in (E/'analysis/raw_outputs.jsonl').read_text().splitlines()];lookup={(r['index'],r['condition']):r for r in raw};bands=M['bands'];main=bands[:8];names={b['condition']:f"PC{b['PC_start_one_based']}–{b['PC_stop_exclusive_one_based']-1}" for b in bands}
def probstr(p):return f'{100*p:.2e}%' if p<1e-5 else f'{100*p:.5f}%'
def v(co,metric):return S[(S.condition==co)&(S.metric==metric)].iloc[0]
def control(co):return C[(C.condition==co)&(C.target_group=='all')].iloc[0]
def table(conf):
 ls=['|单独保留区间|维数|训练参考方差|目标NLL↓|与原模型KL↓|原首选一致率|真实系数相对同token异文档的NLL增益 [95%区间]|','|---|---:|---:|---:|---:|---:|---:|']
 for b in conf:
  co=b['condition'];c=control(co);dd=D[D.condition==co].iloc[0];ls.append(f"|{names[co]}|{b['dimensions']}|{dd.reference_variance_fraction:.2%}|{v(co,'NLL')['mean']:.3f}|{v(co,'KL_full')['mean']:.3f}|{v(co,'top1_agreement')['mean']:.2%}|{c.mean_NLL_gain_real_vs_same_token_other_document:.3f} [{c.ci_low:.3f}, {c.ci_high:.3f}]|")
 return '\n'.join(ls)
text=['# 分段与尾部单独解码：完整语境、实际输出及语境核查','\n本轮关注三条线：行为和因素对照（只换谱段）、表征的谱位置（同一训练基底）、原生输出干预及可信度（恒等／旧条件重放）。所有指定区间及尾部已完成，不训练新模型、分类器或谱基。科学机制与语义层级判断仍Unknown。','\n## 先定义本轮究竟解码什么','175篇自然文档、700个固定位置。在0基位置t，模型已经读到x_t，解码预测x_(t+1)。这里比较的是同一可见前文下的下一token分布，不是把各位置首选拼成一段生成文本。PCA区间独立保留，不加入头部；每个条件加回同一训练均值，再接原生最终RMSNorm与冻结输出头。模型仍为原Qwen3-0.6B-Base、block27 residual-post（norm前）。','PC编号从1开始，区间采用左闭右开：用户的16到32对应PC16–31；其余依次32–63、64–127、128–255、256–511。另看512–767、768–959和960–1024。宽度分别16／32／64／128／256／256／192／65，不把维数差异冒称谱位置或语义差异；另有三个等64维尾段作参照。','所有完整可见输入已逐一用原token IDs重解码核对，700/700与原窗口前缀一致。当前句子是截至所选token已见部分，常常未结束；“原文整句／后续”标为参考，不能用来解释模型当时看到了什么。原语料已暴露，结果为探索性。','\n## 实际输出图：每段倾向解码什么','![自然面板实际输出](figures/02_actual_output_IDs.png)','\n图中是700个位置各自的首选ID频数；每段列5个最常见输出，**不代表正确率或语义相似度**。完整逐位置概率和目标排名见casebook与原始表。片段中的前导空格、子词和符号保留原样。','\n'+table(main),'\n原模型目标NLL为'+f"{v('identity','NLL')['mean']:.3f}"+' nat；仅训练均值为'+f"{v('mean_only','NLL')['mean']:.3f}"+' nat。NLL越低越支持真实后继；KL越低越接近原模型，两者分开。高熵只表示分布更分散，不直接定义“混乱”。','\n## 是否随上下文变化，而不是只输出背景','在相同当前tokenID内，将另一篇文档的该段系数替换过来，保留原位置目标。输出前固定一组置换，312位置／158篇可匹配；不匹配的位置仍保留在700主面板。正NLL增益表示真实系数比异文档系数更支持真实后继。误差区间按文档重采样2000次，条件于这一次固定置换，不是独立重复或多重比较校正后的确认。','\n![语境核查与等维参照](figures/01_band_context_checks.png)','\n'+table([bands[2]]+bands[8:]),'\n对照排除了当前token词面完全不同这一解释，并在匹配位置集合上保持系数／能量边际。它仍可能反映来源、格式、句法或词频信息，不能单凭NLL差命名对象／关系语义。区间跨0是不确定，不证明尾部没有信息。','\n## 三个固定例子：完整输入、当前位置和解码','三例在本轮输出前固定，来自原先输出无关挑选的12篇自然文本，没有按新结果挑案例。红色目标概率另报，原模型自己的首选也未必等于原文后继。']
for key in M['main_cases']:
 c=contexts[key];sid=c['seq_id'][-3:];text += ['\n### '+c['seq_id'],f"当前位置：**0基{c['position_zero_based']}，即第{c['position_one_based']}个token**；当前ID{c['input_id']}，片段 `{repr(c['input_fragment'])}`。真实后继ID{c['target_id']}，片段 `{repr(c['target_fragment'])}`。",'已经可见的当前句子／段落：\n\n> '+c['current_visible_sentence_or_paragraph'],'此前全部可见输入：\n\n```text\n'+c['visible_prefix']+'\n```',f'![同一前文各区间输出](figures/04_case_{sid}_compact.png)','\n下表把真实后继在各段中的变化单独列出，避免仅凭前三候选是否“像词”来判断：','|谱段|真实后继概率|排名|NLL相对仅均值的改善，nat|','|---|---:|---:|---:|']
 for b in main:
  co=b['condition'];x=lookup[c['index'],co];text.append(f"|{names[co]}|{probstr(x['target_probability'])}|{x['target_rank']}|{x['target_NLL_improvement_vs_mean']:.3f}|")
 text.append('\n**语境阅读：**见本轮逐例人工核查补充；此处完整保留原始候选及概率。')
text+=['\n## 完整材料与界限','[固定12例完整前文、token邻域及所有谱段](casebook_cn.md)；[全部700自然位置入口](all_contexts_cn.md)；[位置与token索引](evidence/input_position_index.csv)；[总体指标](evidence/summary_metrics.csv)；[同token异文档对照及后继类型分层](evidence/context_controls.csv)。全量原始top20和每个位置指标在执行目录analysis中，未截断或筛掉失败位置。','尾部原始参考特征值仍为正，最小4.21，不是由样本不足形成的数值零空间。复用同一谱不是独立复现；大部分单根相邻谱间隙很小，不给单根命名语义。','孤立谱段经原生头的输出可能离开训练时的全表征分布。单独解码不贴切，只说明在此原生读出口径下未直接恢复上下文预测，不等于没有可读信息、没有与其他方向组合的作用，或模型储存了随机噪声。反之，出现一个具体词也不能自动当成它对应语义的证据。','本轮没有继续扩展模型、层或训练任务。']
(P/'summary_cn.md').write_text('\n\n'.join(text)+'\n')
en='''# Isolated spectral bands and tail: native decoding with full contexts

Same qualified frozenQwen3-0.6B-Base block27pre-finalnorm vectors/TRAINmean/PCA/nativeRMSNorm+tiedhead.175documents700naturalpositions,exploratory;37auxiliaryrows preserveR13batchshape butareexcludedfromprimaryanalysis. No training/newPCA/classifier/newtext/transformerforward.

One-basedhalf-openPCintervals:16–31,32–63,64–127,128–255,256–511,512–767,768–959,960–1024. IsolatedbandplusTRAINmean,notcumulativehead. Widthsdiffer;matched64d512–575,768–831,961–1024comparewith64–127. Literalindices/dimensionsandallstatisticsinthelinkedtables. Fullvisibleprefix,currentinputID/fragment,zero-basedtandone-basedt+1andtruesuccessorareexplicit. All700prefixescheckedagainstoriginaltokenwindows;futureoriginalsentence/referenceisclearlynotvisibleinput. Threeprespecifiedcases134:144,242:78,434:160and12oldoutput-blindcasespreventshowcaseselectionbynewoutputs.

NLLmeasuresactualsuccessorprobability,KL(full||band)fidelity,entropyuncertainty,top1/top10recoveryreferenceagreement. Mean-only/full/head64arefixedreferences. Top20recordsincludeactualprobabilitiesandlog-probabilityliftvsmean. Highentropy,rareforeignfragment,orasinglesemantic-lookingworddoesnotbyitselfidentifychaosorsemantics.

Boundedcontextcontrol:onefixedseed20261103derangescoefficientsacrossdifferentdocumentsWITHINexactcurrenttokenIDon312positions/158documents,keepingoriginaltargetandreference. Marginalsarepreservedonmatchedpositions. PositivepairedNLLgainshowscontext-linkedpredictiveassociationbeyondcurrentID/marginals,notcausalsemantics;source/style/syntax/frequencyremainrivals. Pointwise95%document-bootstrapintervals(2000draws,seed20261104)conditiononthisonepermutation;notmultiplicity-correctedconfirmation. Unmatchedpositionsremaininthe700primarypanel. No-gain/wideintervalisnotabsenceofinformation.

TheChineseSummarypreserveseverymaincontextandliteraldecodertable;theseareoriginalEnglishprefixes. Allnaturalpositioncasebooksandrawoutputsremainexecution-side,withselected12-casebookinproject. Nativeisolatedbandfailuredoesnotprovefullmodelstoresnoiseorwhatthebandcancontributewhencombined. Tailreferenceeigenvaluesarenonzero;basisreuseisnotindependentreplication. MechanismandsemantichierarchyacceptanceUnknown.

'''+table(main)+'\n\n[Chinese complete figures/contexts and bounded reading](summary_cn.md) · [fixed12casebook](casebook_cn.md) · [all700contexts](all_contexts_cn.md) · [protocol](protocol.md) · [rawstatisticstable](evidence/summary_metrics.csv).\n'
(P/'summary.md').write_text(en)
(P/'casebook.md').write_text('# Fixed English prefixes and literal decoding outputs\n\n[Complete12-case table](casebook_cn.md) retainsfullEnglishvisibleprefix,currenttokenID,zero/one-basedpositions,neighborswithvisibilityflags,andcandidateIDs/probabilities/ranksforall11isolatedbandsplusmean/full. ChineseheadingsexplainoriginalEnglishdata;post-positiontextisreferenceonly.\n')
for name in ['summary.md','summary_cn.md','casebook_cn.md','casebook.md','all_contexts_cn.md']:shutil.copy2(P/name,E/name)
print('full-contextbilingualreadingdraftwritten;manualcaseanalysispending')
