import os
os.environ['MPLBACKEND']='Agg'
from pathlib import Path
import json,hashlib,datetime
from zoneinfo import ZoneInfo
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager
P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding');E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')/P.name
O=P/'audit_review_20261101';O.mkdir(exist_ok=True)
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'font.size':11,'axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False})
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rr=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];records=[r for p in sorted((E/'analysis/chunks').glob('*.json')) for r in json.load(open(p))['records']];freq=np.load(E/'data/frequency.npz');base={};best={}
for r in records:
 t=sorted(r['top20'],key=lambda t:(-t['probability'],t['id']));assert t[9]['probability']>t[19]['probability'];best[r['index'],r['condition']]=t[0]['id']
for i in range(len(rr)):base[i]=best[i,'identity']
long=[]
for i,r in enumerate(rr):
 id=base[i];group='nonlexical' if not freq['valid'][id] else 'format' if freq['format_mask'][id] else 'nonformat_common' if freq['group'][id]==0 else 'nonformat_other'
 for k in [1,4,16,64,128,256,512,768,1024]:long.append({'index':i,'panel':r['panel'],'seq_id':r['seq_id'],'group':group,'k':k,'match':int(best[i,'k'+str(k)]==id)})
a=pd.DataFrame(long);stored=pd.read_csv(E/'analysis/recovery_by_full_top1_type.csv');s=stored[stored.metric=='top1_agreement'];errs=[]
for r in s.to_dict('records'):
 k=1024 if r['condition']=='identity' else int(r['condition'][1:]) if r['condition'].startswith('k') else None
 if k is None:continue
 q=a[(a.panel==r['panel'])&(a.group==r['group'])&(a.k==k)];actual=q.groupby('seq_id').match.mean().mean();errs.append(abs(actual-r['mean']))
assert max(errs)<1e-12
counts=a[a.k==64].groupby(['panel','group']).agg(positions=('index','size'),documents=('seq_id','nunique'),matched_positions=('match','sum')).reset_index();counts.to_csv(O/'figure1_raw_counts_k64.csv',index=False)
z=a[(a.panel=='natural')&(a.k==64)&a.group.isin(['nonformat_common','nonformat_other'])];wide=z.groupby(['seq_id','group']).match.mean().unstack().dropna();delta=wide.nonformat_common-wide.nonformat_other;rng=np.random.default_rng(20261101);draw=rng.integers(0,len(delta),(2000,len(delta)));ci=np.quantile(delta.to_numpy()[draw].mean(1),[.025,.975]);sensitivity={'kind':'posthoc_audit_sensitivity_not_replacing_primary_estimand','shared_documents':len(delta),'difference_common_minus_other':float(delta.mean()),'CI95':ci.tolist(),'retained_common_positions':int(z[z.seq_id.isin(wide.index)&(z.group=='nonformat_common')].shape[0]),'retained_other_positions':int(z[z.seq_id.isin(wide.index)&(z.group=='nonformat_other')].shape[0]),'remaining_limit':'same document, different positions/lexical roles; not a semantic/frequency intervention'};(O/'same_document_sensitivity.json').write_text(json.dumps(sensitivity,indent=2)+'\n')
ks=[1,4,16,64,128,256,512,768,1024];fig,axes=plt.subplots(1,2,figsize=(12,5.8));colors={'format':'#b47d24','nonformat_common':'#2177a5','nonformat_other':'#8e5f9a'};labels={'format':'空白／标点','nonformat_common':'参考常见ID，排除格式','nonformat_other':'其余ID，排除格式'}
for ax,panel,title in zip(axes,['the','natural'],['原主面板：37篇，读完 the','补充面板：175篇，700个自然位置']):
 for group in ['format','nonformat_common','nonformat_other']:
  d=s[(s.panel==panel)&(s.group==group)];n=int(d.iloc[0].documents);nposition=int(d.iloc[0].positions)
  if n<2:
   ax.text(.03,.94,'格式组仅1篇：不画推断曲线',transform=ax.transAxes,color='#777777',fontsize=10);continue
  q=d.set_index('condition').loc[['k'+str(k) for k in ks]];ax.plot(ks,q['mean']*100,'o-',c=colors[group],label=f'{labels[group]}\n{n}篇／{nposition}位置');ax.fill_between(ks,q.ci_low.to_numpy()*100,q.ci_high.to_numpy()*100,color=colors[group],alpha=.13)
 ax.axvline(64,ls=':',c='#888888',lw=1);ax.set_xscale('log',base=2);ax.set_xticks([1,4,16,64,256,1024],[1,4,16,64,256,1024]);ax.set_ylim(-2,103);ax.set_xlabel('累计保留前 k 个训练主成分（维）');ax.set_ylabel('恢复未投影原生头首选ID的文档均值（%）');ax.set_title(title);ax.grid(alpha=.15);ax.legend(fontsize=9,loc='upper left',bbox_to_anchor=(.02,.88 if panel=='the' else .98))
fig.suptitle('主图1：哪类首选预测较早恢复？',fontsize=16);fig.text(.5,.065,'每篇先在该组的位置内平均，再对含该组的文档等权平均；同篇可出现在多个组，组内文档数不能相加。',ha='center',fontsize=10);fig.text(.5,.025,'阴影：组内文档重采样2000次的逐点95%区间。固定Qwen3-0.6B block27 norm前；随后原生RMSNorm＋冻结输出头。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.12,1,.93]);fig.savefig(O/'main1_recovery_audited.png',dpi=150,bbox_inches='tight');plt.close(fig)
# Second figure prepared only, not shown until feedback.
d=pd.read_csv(E/'analysis/document_metrics.csv');contrasts=pd.read_csv(E/'analysis/paired_contrasts.csv');spec=[('k128','前部下一64'),('head_middle','中64'),('head_tail','尾64'),('head_random1034','正交随机1'),('head_random1035','正交随机2'),('head_random1036','正交随机3')];fig,axes=plt.subplots(1,2,figsize=(12,5.5));pc=[]
for ax,panel,title in zip(axes,['the','natural'],['37篇 the 面板','175篇自然位置面板']):
 for j,(cond,label) in enumerate(spec):
  r=contrasts[(contrasts.panel==panel)&(contrasts.condition==cond)&(contrasts.baseline=='k64')&(contrasts.metric=='NLL')].iloc[0];q=d[d.panel==panel].pivot(index='seq_id',columns='condition',values='NLL');v=q.k64-q[cond];gain=float(v.mean());assert abs(gain+r.difference_condition_minus_baseline)<1e-12;lo=-r.ci_high;hi=-r.ci_low;ax.errorbar(gain,j,xerr=[[gain-lo],[hi-gain]],fmt='o',capsize=4,color='#2478a4' if j<3 else '#888888');pc.append({'panel':panel,'addition':cond,'documents':len(v),'improved':int((v>1e-8).sum()),'worsened':int((v<-1e-8).sum()),'equal':int((abs(v)<=1e-8).sum()),'gain':gain,'ci_low':lo,'ci_high':hi})
 ax.set_yticks(range(len(spec)),[x[1] for x in spec]);ax.invert_yaxis();ax.axvline(0,c='black',lw=.8);ax.grid(axis='x',alpha=.15);ax.set_xlabel('相对头64的真实后继NLL改善（nat；正为好）');ax.set_title(title)
fig.suptitle('主图2：中尾新增是否超过同维数参照？',fontsize=16);fig.text(.5,.025,'全部文档配对，未筛漂亮案例；误差条为配对文档bootstrap95%区间。维数相同，保留能量并未匹配。',ha='center',fontsize=10);fig.tight_layout(rect=[0,.08,1,.93]);fig.savefig(O/'main2_addition_controls_audited.png',dpi=150,bbox_inches='tight');plt.close(fig);pd.DataFrame(pc).to_csv(O/'figure2_all_document_changes.csv',index=False)
# Material issues classified; no original protocol/Anchor overwritten.
issues=[{'id':'I1','grade':'实现错误，既有修复已核实','evidence':'scripts/analyze.py:14-24;provenance/topk_tie_fix.json','issue':'原始GPUchunk的top1/top10字段使用不同topk并列排序，不能直接复用','impact':'旧chunk一致率字段；NLL/KL/概率不受影响，当前更正CSV和主图有效','minimum_fix':'保留原chunk；必须经当前CPU canonical tie reader计算，本审计已从原概率重建核对','recompute':'无需GPU；CPU更正已完成'}, {'id':'G1','grade':'证据缺口','evidence':'protocol.md:56-57;scripts/recovery_groups.py:1-19','issue':'恢复类型分层为输出后描述性分析；没有外部粗细语义标注与语义最小对照','impact':'主图1只能支持本面板内频率相关恢复差异，不能裁决粗细语义','minimum_fix':'显式标探索性并收窄文字；语义确认另列协议由研究者决定','recompute':'文字不需；新语义检验需另议'}, {'id':'G2','grade':'证据缺口','evidence':'data/bases.npz;analysis/summary_metrics.csv;analysis/addition_control_contrasts.csv','issue':'等维控制完整，逐位置保留能量未匹配','impact':'主图2不能将额外收益直接命名为独有细语义信息','minimum_fix':'保留能量解释；若要裁决，先制定等能量敏感性协议','recompute':'收窄不需；新条件需先讨论'}, {'id':'E1','grade':'表达问题，读图版已修复','evidence':'scripts/recovery_groups.py:16-19;figure1_raw_counts_k64.csv','issue':'恢复率是组内文档均值，不是简单命中位置数/全部位置数','impact':'百分数与原始计数可能被误读，但原统计没有算错','minimum_fix':'新图标明分母并附全部原始计数；不替换旧结果','recompute':'仅已有表重绘，已完成'}, {'id':'G3','grade':'证据缺口／基准精度边界','evidence':'scripts/run_gpu.py:67-74,83;provenance/03_implementation_numerics.json','issue':'p_full是相同batch16的未投影原生头重解码，三篇与整模型返回logits存在0.0625最大BF16差；未全量验证两者首选完全相同','impact':'不影响相同解码参照下的投影对比，不能声称逐位复现整模型分布','minimum_fix':'图中明确称未投影原生头参照；全量整模型首选一致性若必需再议','recompute':'当前文字不需；全量额外对照未运行'}, {'id':'P1','grade':'解释过度，已限制','evidence':'analysis/recovery_group_members.csv;data/frequency.npz','issue':'常见/其余token ID不等于粗/细语义；平均原模型置信度相近不等于已匹配置信度','impact':'主图1的语义层级和因果词频解释不可用','minimum_fix':'只保留频率相关预测恢复这一观察；不因一个局部缺口否定全部输出','recompute':'无需重算'}]
(O/'issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2)+'\n')
manifest={'created_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'type':'interactive audit reading,not new experiment','original_owner':'15_27_05','original_protocol_unchanged':True,'anchor_update':'pending discussion','GPU_calls':0,'first_curve_raw_rebuild_max_abs_error':max(errs),'source_sha256':{str(x):sha(x) for x in [E/'freeze.json',P/'provenance/protocol_executed_A4.md',E/'scripts/run_gpu.py',E/'analysis/recovery_by_full_top1_type.csv',E/'analysis/position_metrics.csv',E/'analysis/paired_contrasts.csv',E/'data/frequency.npz']},'figures':['main1_recovery_audited.png','main2_addition_controls_audited.png'],'figure1_denominator':'within-group average per doc,then mean over eligible docs; reference groups fixed by unprojected head argmax','figure1_CI':'stored2000 within-group doc bootstrap,not simultaneous','sensitivity':sensitivity,'raw_support':counts.to_dict('records')};(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
text='''# 原生谱解码：交互精读审计（未改变原Anchor）

只审计R13_20261101_native_spectral_decoding；另外两个实验不在此清单。先对原始prompt、初始冻结protocol前缀、A4执行版本、代码生产者哈希、运行回执和原始chunk/CSV核对，不以Summary自证。

## 实际执行清单

|原计划|实际|状态与影响|
|---|---|---|
|固定R12模型、tokenizer与末层测点，原生解码，不训分类器|官方Qwen3-0.6B，block27 residual-post→原生最终RMSNorm→绑定lm_head；参数冻结|完整执行；生产代码哈希匹配新缓存manifest|
|复用匹配R12缓存|旧缓存NLL重放越过0.05阈值，改为同权重同测点在5090重缓存180篇|替代执行；旧缓存不作主输入，不能说原样复现旧运行时|
|固定训练侧谱|继续用R04发现侧60篇×160位置的mu/V，1024秩；不重新拟合|旧拟合复用，不是独立复现|
|37篇the及未经本轮输出筛选的自然位置|37篇/37位置；175篇/700自然位置；共享32篇，总180物理文档；两个面板分报|完整执行；旧H已暴露，探索性，不是新确认集|
|嵌套k、头中尾64、128维新增、随机与均值/恒等|21去重条件×737位置=15477行|完整执行；等能量不在已执行控制中|
|NLL/KL/熵、词频、排名、top1/top10、真实文本、文档区间|当前概率/原表及文档聚合已核对；并列错误在CPU更正|完整执行，原chunk一致率字段有已知错误，不得绕开更正reader|
|自然词频/格式恢复顺序|分组规则基于输出前冻结掩码，但恢复分层与控制差是输出后加入|探索性补充，不是原始确认检验|
|可选贪心生成／条件触发范数匹配|两者未运行；只审计解析/数值尺度上界|未执行；不得说实测验证了范数匹配敏感性|

初始protocol正文前缀已与第一次freeze校验相同；实际A4协议快照与运行freeze哈希相同。当前protocol的A5/A6是显式事后追加，不能当预注册。197项执行artifact哈希当前匹配；新图1所有曲线点由原始GPUchunk的ID/概率重建，最大误差小于1e-16。图片只是已有数据的单问题读图版，不改原图、不启动模型。

## 审计问题与最小修复

'''
for x in issues:text+=f"### {x['id']} · {x['grade']}\n\n证据：{x['evidence']}。\n\n问题：{x['issue']}。影响：{x['impact']}。\n\n最小修复：{x['minimum_fix']}。重算：{x['recompute']}。\n\n"
text+='## 首图关键计数与敏感性\n\n64维自然面板：常见非格式118/386位置命中，其余非格式3/206，格式40/108。文档等权均值分别30.3%/2.0%/38.3%，与简单位置比例不是同一分母。原主the面板为3/16与1/20；格式仅1篇。\n\n同篇同时有常见/其余非格式位置的113篇，64维差为27.58个百分点，文档配对95%区间20.65–34.81；这是本次审计的事后稳健性检查，不替代主图，也未控制同文档内位置/词面/任务差别。\n\n## 待读顺序\n\n先读主图1“哪类首选预测较早恢复”；等研究者反馈后再读主图2“中尾新增是否超过同维参照”。认识更新卡和Anchor的科学边界更新留待讨论确认。本轮不启动新实验。\n'
(O/'audit_cn.md').write_text(text);(O/'audit.md').write_text('# Interactive native-spectral audit\n\nNo new model calls. Original Protocol/Anchor preserved; interpretation updates pending discussion. See [full Chinese audit](audit_cn.md) and [machine-readable findings](issues.json). Two reading figures use unchanged canonical metrics. Figure1 points were independently rebuilt from raw GPU top20 probabilities and frozen frequency masks; maximum error<1e-16. Legacy-cache refresh, reused TRAIN PCA, exposed panel status, post-output strata, tie correction, actual denominator and native-head batch-reference precision are explicitly distinguished.\n')
print(O);print('points max error',max(errs));print('same-doc',sensitivity)
