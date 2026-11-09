"""Meeting figures from saved near-domain statistics; no feature selection."""
from pathlib import Path
import csv,json,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter
S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030')
O=S/'presentation_variants/near_single_domain_20261030';T=S/'presentation_variants/token_context_audit_20261030';F=O/'figures';F.mkdir(exist_ok=True)
font=O/'fonts/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));family=font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams.update({'font.family':family,'font.size':11,'axes.titlesize':14,'axes.labelsize':11,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
C={'math':'#2378a3','biology':'#c25b3a'};cn={'math':'数学偏向','biology':'生物偏向'}
summary=json.loads((O/'summary.json').read_text())
def rows(p):return list(csv.DictReader(p.open()))
def save(fig,name):
    fig.savefig(F/(name+'.png'),dpi=190,facecolor='white');fig.savefig(F/(name+'.pdf'),facecolor='white');plt.close(fig)
def style(ax,y=True):
    ax.grid(axis='y' if y else 'x',alpha=.17);ax.set_axisbelow(True)
def foot(fig,text,y=.025):fig.text(.055,y,text,fontsize=9,color='#454545',va='bottom',linespacing=1.6)

# Frequency: denominators never substitute reference hits for member counts.
freq=rows(O/'frequency_composition.csv');fc={(r['cohort'],r['scheme'],r['frequency']):r for r in freq}
fig,axs=plt.subplots(1,2,figsize=(13.4,5.8),sharey=True);fig.subplots_adjust(left=.07,right=.98,bottom=.25,top=.82,wspace=.17)
fig.suptitle('近单域使用倾向，并不等于极罕见：数学以中频最多，生物以低频最多',fontsize=17,y=.96)
palette=['#88b5cd','#e5ba66','#8a78ac'];labs=['低频','中频','高频']
for ax,g in zip(axs,['math','biology']):
    cohorts=['parent_'+g,'near95_'+g,'strict_'+g,'eligible_pool'];names=['全部领域\n区分成员','近单域\n主集合','严格单域\n子集','支持合格\n候选池']
    bot=np.zeros(4)
    for c,label,col in zip(['low','middle','high'],labs,palette):
        vals=np.array([float(fc[k,'original',c]['proportion']) for k in cohorts]);counts=[int(fc[k,'original',c]['count']) for k in cohorts]
        ax.bar(range(4),vals,bottom=bot,color=col,label=label,width=.63)
        for x,v,b,n in zip(range(4),vals,bot,counts):
            if v>.08:ax.text(x,b+v/2,f'{v:.1%}\n(n={n:,})',ha='center',va='center',fontsize=10)
        bot+=vals
    for x,k in enumerate(cohorts):
        r=fc[k,'original','low'];ax.text(x,1.025,f"{r['classified_denominator']}/{r['total_members']}",ha='center',fontsize=10)
    ax.set_xticks(range(4),names);ax.set_ylim(0,1.12);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_title(cn[g]);style(ax)
axs[0].set_ylabel('频率可判定成员中的人数比例');axs[1].legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,1.16),frameon=False)
foot(fig,'柱顶为“频率可判定 / 冻结总人数”；近单域主集合 31 + 24，DCLM 支持不足 1 + 2，保留在名单中。\n频率 = 独立 DCLM 中原生 z>0 的位置数 / 65,536；至少 20 次。原阈值：低 ≤0.259399%，中 ≤1.344299%，其余高。\n近单域定义：发现集偏向域 ≥5 篇激活，另一域 ≤1/30 篇，且 ≥95% 正激活位置来自偏向域。发现集每域 30 篇。')
save(fig,'figure_frequency_near_domain')

# Figure A: discovery categories, heldout member-equal fractions and BOTH input baselines.
tokens=rows(O/'near95_activated_tokens.csv');cats=rows(O/'input_token_categories.csv');catmap={int(r['token_id']):r['category'] for r in cats};pk=np.load(S/'analysis/position_keys.npz');docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];held=np.array([docs[int(d)]['split']=='heldout' for d in pk['document_index']]);heldtokens=pk['token_id'][held]
category=['shared_both_domains','math_associated','biology_associated','other_or_low_support'];clabels=['两域共用','本语料偏数学','本语料偏生物','其他／支持不足']
rawbg=np.array([np.mean([catmap[int(t)]==c for t in heldtokens]) for c in category]);rawtok={int(t):float(np.mean(heldtokens==t)) for t in np.unique(heldtokens)}
fig=plt.figure(figsize=(14.2,10.5));gs=fig.add_gridspec(2,2,height_ratios=[1,1.15],left=.085,right=.98,bottom=.16,top=.85,wspace=.27,hspace=.55)
fig.suptitle('图 A｜近单域成员也响应共用词面；大量 token 的偏域类别仍未确定',fontsize=18,y=.97)
fig.text(.5,.913,'类别仅由发现集输入中的文档覆盖冻结；在旧留出 40 篇、6,400 个位置评估。不是语义专属性标签。',ha='center',fontsize=11)
catstats=[]
for j,g in enumerate(['math','biology']):
    rr=[r for r in tokens if r['domain_bias']==g];sub=summary['token_summary'][g];q=np.array([sub['category_shares'][c] for c in category]);bg=np.array([sub['document_matched_category_shares'][c] for c in category]);ax=fig.add_subplot(gs[0,j]);x=np.arange(4)
    ax.bar(x-.18,q,width=.34,color=C[g],label='高响应位置：成员等权');ax.bar(x+.18,rawbg,width=.34,color='#d4d7da',label='全部可用位置背景');ax.scatter(x+.18,bg,color='black',marker='D',s=24,label='同文档暴露量匹配背景',zorder=5)
    for xx,v in zip(x,q):ax.text(xx-.18,v+.016,f'{v:.1%}',ha='center',fontsize=11,color=C[g],weight='bold')
    ax.set_title(f"{cn[g]}：25/31 名" if g=='math' else f"{cn[g]}：18/24 名");ax.set_xticks(x,clabels,fontsize=10);ax.set_ylim(0,.72);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_ylabel('各成员内占比，再对成员等权');style(ax)
    if j==0:ax.legend(fontsize=9,loc='upper left',frameon=False)
    for c,a,b,d in zip(category,q,rawbg,bg):catstats.append(dict(feature_group=g,token_category=c,member_equal_high_share=float(a),all_available_position_background=float(b),document_matched_background=float(d),frozen_members=sub['frozen_members'],composition_members=sub['composition_members'],excluded_for_composition_support=sub['excluded_composition_support']))
    ax=fig.add_subplot(gs[1,j]);top=sorted(rr,key=lambda r:int(r['rank']))[:8];y=np.arange(8);val=np.array([float(r['high_share']) for r in top]);base=np.array([float(r['document_matched_background']) for r in top]);ax.barh(y,val,color=C[g],alpha=.88);ax.scatter(base,y,marker='D',s=25,color='black',zorder=4)
    labels=[]
    for r in top:
        st=r['token_string'].replace('\n','\\n').replace('\t','\\t').strip();labels.append(f"{st or '[空白]'}  [ID {r['token_id']}]")
    ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(0,.066);ax.xaxis.set_major_formatter(PercentFormatter(1));ax.set_xlabel('高响应位置的成员等权份额；◆ 同文档背景');ax.set_title('实际 token：按高响应份额排名前 8，保留标点',fontsize=12);style(ax,False)
    for yy,v,r in zip(y,val,top):ax.text(max(v, float(r['document_matched_background']))+.001,yy,f"{v:.2%} · {r['high_response_members']} 名",va='center',fontsize=9)
foot(fig,'高响应：z 严格超过该成员发现集正激活第90百分位；不重新调阈值。构成统计需 ≥5 次高响应且覆盖 ≥2 篇留出文档。\n数学 6/31、生物 6/24 名构成支持不足，仍保留；同一位置可响应多个成员，不能把成员–位置事件当成独立 token 样本。\n共用：发现集两域各 ≥5 篇出现；偏域：该域 ≥5 篇且另一域 ≤1 篇；其余另列。词形省略前导空格，精确 token ID 保留。\n灰柱以两域各 20 篇全部 6,400 位置为分母；◆ 按各成员高响应所在文档的暴露量匹配。图示是构成差异，不是语义偏好证明。',y=.022)
with (O/'figureA_plot_data.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(catstats[0]));w.writeheader();w.writerows(catstats)
save(fig,'figureA_token_categories_and_names')

# Figure B: same exact token with input-only matching; all frozen members retained.
matched=rows(O/'matched_same_token_group_summary.csv');the=[r for r in matched if int(r['target_token_id'])==279];ex=rows(O/'predetermined_member_matched_examples.csv')
fig=plt.figure(figsize=(15.1,12));gs=fig.add_gridspec(3,2,height_ratios=[1,.94,.94],left=.10,right=.985,top=.85,bottom=.12,wspace=.37,hspace=.57)
fig.suptitle('图 B｜同一个 “ the” 在不同前文下仍有响应差异；来源与覆盖限制保留',fontsize=18,y=.97)
fig.text(.5,.917,'上方使用全部冻结 31 / 24 名（包括零）；下方固定展示两组发现排名首位成员，不因缺响应换案例。',ha='center',fontsize=11)
for j,level in enumerate(['local','source_local']):
    ax=fig.add_subplot(gs[0,j]);ax.axvline(0,color='#777',lw=1)
    for i,g in enumerate(['math','biology']):
        r=next(r for r in the if r['level']==level and r['feature_group']==g);v,lo,hi=[100*float(r[k]) for k in ['preferred_minus_other_high_fraction','CI_low','CI_high']];ax.errorbar(v,1-i,xerr=[[v-lo],[hi-v]],fmt='o',color=C[g],capsize=5,ms=9);ax.text(4.75,1-i,f"{v:+.2f} pp\n[{lo:.2f}, {hi:.2f}]\n高响应 {r['high_supported_members']}/{r['members']} 名",ha='right',va='center',fontsize=10,color=C[g])
    ax.set_yticks([1,0],['数学偏向 31 名','生物偏向 24 名']);ax.set_ylim(-.6,1.65);ax.set_xlim(-.35,4.9);ax.set_xlabel('偏向领域 − 另一领域：高响应成员比例差（百分点）');style(ax,False)
    title='相同 token + 前一 token + 位置/格式代理\n15 对文档 / 24 对位置' if j==0 else '再要求相同来源网站\n6 对文档 / 10 对位置（仅 1 个共用网站）'
    ax.set_title(title,fontsize=12);ret='保留 math/bio 的 the 位置：20.3% / 14.0%' if j==0 else '保留 math/bio 的 the 位置：8.5% / 5.8%'
    ax.text(.01,-.29,ret,transform=ax.transAxes,fontsize=10,color='#555')
for i,r in enumerate(ex):
    ax=fig.add_subplot(gs[1+i,:]);ax.axis('off');g=r['domain_bias'];fid=r['feature_id'];status='有高／低响应对照' if r['status']=='MATCHED_HIGH_EXAMPLE' else '两侧均未激活：测试覆盖不足，保留原成员'
    ax.text(.012,1.03,f"固定排名成员 f{fid}（{cn[g]}）｜{status}",fontsize=13,color=C[g],weight='bold',transform=ax.transAxes)
    for j,d in enumerate(['math','biology']):
        x=.014+j*.51;prefix=r[d+'_prefix'];prefix=prefix.replace('\ufffd','')
        if fid=='16271' and d=='math':prefix='... The main use of σ-algebras is in'
        else:prefix='... '+prefix[-205:].strip()
        txt='\n'.join(textwrap.wrap(prefix,width=69,replace_whitespace=True));ax.text(x,.79,('数学前文' if d=='math' else '生物前文')+f"｜{r[d+'_seq_id']} · 位置 {r[d+'_position']}",fontsize=10,transform=ax.transAxes)
        ax.text(x,.63,txt,fontsize=10,va='top',linespacing=1.45,transform=ax.transAxes)
        ax.text(x,.16,f"目标 [ the ]  ID 279     z = {float(r[d+'_z']):.4f}     高响应阈值 {float(r['threshold']):.4f}",fontsize=11,color=C[d],transform=ax.transAxes)
        cue=r[d+'_cues'] or '词表未检出（不等于无领域信息）';ax.text(x,-.02,f"已读线索提议：{cue}；来源 {r[d+'_source']}",fontsize=9,color='#555',transform=ax.transAxes)
foot(fig,'响应差：每个位置先对全部冻结成员取高响应比例；位置对在文档对内平均，再对文档对等权。区间为 1,000 次文档对重采样的探索性95%区间。\n匹配只使用输入：精确目标/前一 token ID、40位置区间、段句边界和体裁；不使用激活。它是局部句法代理，未完整控制语法、语义或主题。\n“高响应 n/N名”指至少一次匹配高响应；“ the”在两域分别出现118 /171次、各20篇。例子不能代表全组；前文标签待人工核查。',y=.018)
save(fig,'figureB_same_token_context')

# Appendix: token frequency, distinguish token types from positions.
fr=rows(O/'high_token_frequency_composition.csv');fig,axs=plt.subplots(1,2,figsize=(12.8,5.6),sharey=True);fig.subplots_adjust(left=.075,right=.98,bottom=.25,top=.82,wspace=.18);fig.suptitle('附录｜高响应 token 在本批语料里多常见？先与所有可用位置比较',fontsize=17,y=.96)
for ax,g in zip(axs,['math','biology']):
    rr=[r for r in fr if r['feature_group']==g];x=np.arange(3);h=np.array([float(r['member_equal_high_share']) for r in rr]);b=np.array([float(r['all_available_position_share']) for r in rr]);db=np.array([float(r['document_matched_share']) for r in rr]);ax.bar(x-.18,h,.34,color=C[g],label='高响应位置（成员等权）');ax.bar(x+.18,b,.34,color='#d4d7da',label='所有可用位置');ax.scatter(x+.18,db,color='black',marker='D',label='同文档匹配背景');ax.set_xticks(x,['低：出现1次','中：出现2次','高：出现≥3次']);ax.set_ylim(0,1);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_title(cn[g]);style(ax)
    for xx,v in zip(x,h):ax.text(xx-.18,v+.015,f'{v:.1%}',ha='center')
axs[0].set_ylabel('高响应位置的成员等权比例');axs[0].legend(loc='upper left',fontsize=10,frameon=False)
allcounts=np.unique(pk['token_id'],return_counts=True)[1];nb=[int((allcounts==1).sum()),int((allcounts==2).sum()),int((allcounts>=3).sum())];np0=[int(allcounts[allcounts==1].sum()),int(allcounts[allcounts==2].sum()),int(allcounts[allcounts>=3].sum())]
foot(fig,f'分组沿用 R10 全部分析位置的 token 类型计数分位点（1、2），相同计数不拆组。4,873种 token，19,200位置。\n三组类型数 {nb}；三组全批位置数 {np0}。柱的评估分母为留出6,400位置，不是类型数。\n数学25/31、生物18/24名；这说明词在本批语料里常见程度，不能据此判断领域语义。')
save(fig,'appendix_token_frequency')

# Appendix: unit geometry for this exact 31/24 subset and matching sizes.
freeze=json.loads((O/'freeze.json').read_text());P=np.load(S/'analysis/all_decoder_projection.npz')['per_pc'];means={g:P[freeze['sets']['near95_'+g]].mean(0) for g in C};bands={g:v.reshape(16,64).sum(1) for g,v in means.items()};fig,axs=plt.subplots(1,2,figsize=(13.4,5.5));fig.subplots_adjust(left=.07,right=.98,bottom=.23,top=.8,wspace=.25);fig.suptitle('附录｜近单域使用倾向仍可与相近谱位置并存',fontsize=18,y=.96)
x=np.arange(16)
for g in C:axs[0].plot(x,bands[g],'-o',color=C[g],label=cn[g])
axs[0].fill_between(x,0,np.minimum(bands['math'],bands['biology']),color='#aca9c2',alpha=.45,label='较小份额：分段共同覆盖');axs[0].set_xticks([0,3,7,11,15],['1–64','193–256','449–512','705–768','961–1024']);axs[0].set_xlabel('共同 PCA 谱段（每段64方向）');axs[0].set_ylabel('单位 decoder 全平方长度的份额');axs[0].yaxis.set_major_formatter(PercentFormatter(1));axs[0].legend(frameon=False,fontsize=10);style(axs[0]);axs[0].set_title('方向几何：不是实际文本贡献能量',fontsize=13)
bg1=np.load(O/'math_matched_reference.npz')['mean_per_pc'];bg2=np.load(O/'biology_matched_reference.npz')['mean_per_pc'];ov=np.minimum(bg1,bg2).sum(1);axs[1].hist(ov,bins=30,color='#d5d8dc');obs=summary['geometry']['near95']['overlap_pc'];axs[1].axvline(obs,color='#574879',lw=2,label=f'实测逐PC重合 {obs:.3f}');axs[1].set_xlabel('同规模、频率与支持量匹配的逐PC重合');axs[1].set_ylabel('1,000次字典匹配抽样数');axs[1].legend(frameon=False,fontsize=10);axs[1].set_title('实测重合落在匹配背景范围内',fontsize=13)
foot(fig,'固定数学31、生物24名；共同发现谱9,600位置；每个decoder先单位化，平方投影全谱合计1，不乘激活或特征值。\n逐PC重合0.8303；64PC分段重合0.9562。背景逐PC95%范围0.8203–0.8459；不能用较高的分段重合遮盖段内差异。\n组规模改变会影响平均分布，不直接与960名的0.9493比较；这里不推断方向相同、功能重合或实际激活贡献。')
save(fig,'appendix_near_geometry')

# Appendix: broad original 433/527 list, never substitute for 31/24 subgroup.
br=rows(T/'all_token_composition.csv');fig,axs=plt.subplots(1,2,figsize=(12.8,6.3));fig.subplots_adjust(left=.13,right=.98,bottom=.2,top=.81,wspace=.42);fig.suptitle('附录｜完整领域区分名单的实际 token（不与近单域55名混用）',fontsize=17,y=.96)
for ax,g in zip(axs,C):
    rr=sorted([r for r in br if r['domain_bias']==g],key=lambda r:int(r['rank']))[:10];v=[float(r['member_equal_high_share']) for r in rr];b=[float(r['document_matched_background_share']) for r in rr];y=np.arange(len(rr));ax.barh(y,v,color=C[g]);ax.scatter(b,y,color='black',marker='D',s=23);ax.set_yticks(y,[r['token_string'].replace('\n','\\n').strip()+f" [{r['token_id']}]" for r in rr]);ax.invert_yaxis();ax.set_xlim(0,.061);ax.xaxis.set_major_formatter(PercentFormatter(1));ax.set_xlabel('成员等权份额；◆ 同文档匹配背景');ax.set_title(cn[g]+(' 371/433名' if g=='math' else ' 472/527名'));style(ax,False)
foot(fig,'原R10高响应阈值与构成支持门槛不变。旧留出40篇×160位置。这里展示可读 token 身份，不等于输出词或功能标签。\n例如生物偏向组的 “the” 本身常见，其高响应份额低于同文档输入背景；不能把常见词数量解释为特殊偏好。\n完整词形仅作事后拼写描述。子词 ot/oper 可来自 homotopy、neoteny / isoperimetry，不能按成员偏向直接给词贴领域语义。')
save(fig,'appendix_all_discriminators_actual_tokens')
print('SAVED',len(list(F.glob('*.png'))),'figures',str(F))
