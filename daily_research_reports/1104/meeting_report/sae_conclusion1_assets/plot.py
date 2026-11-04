from pathlib import Path
import argparse,json,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch,Patch
from matplotlib.colors import ListedColormap
from matplotlib.offsetbox import AnnotationBbox,HPacker,TextArea
P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--font',default='/data/250010109/Research_System/daily_research_reports/backup/2026/09/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf');args=parser.parse_args();font=Path(args.font)
if not font.exists():raise SystemExit('请用 --font 指定支持中文的字体；字体文件不随结果包分发。')
fp=lambda size:FontProperties(fname=str(font),size=size)
plt.rcParams.update({'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
colors=['#1479BD','#EF8A23','#8959C7'];mean=pd.read_csv(P/'data/figure1_means_and_family_CI.csv')
fig,axes=plt.subplots(1,2,figsize=(15.8,7.2),sharey=True)
for ax,site,title in zip(axes,['ATTN_SAE','MLPIN_SAE'],['Attention 输出 SAE','MLP 输入 SAE']):
 x=mean[mean.site==site];values=x['mean'].to_numpy();low=x.CI_lo.to_numpy();high=x.CI_hi.to_numpy();bars=ax.bar(np.arange(3),values,width=.62,color=colors,zorder=2);ax.errorbar(np.arange(3),values,yerr=[values-low,high-values],fmt='none',color='#26313E',elinewidth=1.7,capsize=6,zorder=4)
 for k,v in enumerate(values):ax.text(k,high[k]+.028,f'{v:.3f}',ha='center',va='bottom',fontproperties=fp(22),color='#18202A')
 ax.set_xticks(range(3),['动物类内','交通工具类内','跨大类'],fontproperties=fp(17));ax.set_yticks(np.arange(0,1.01,.2));ax.set_ylim(0,1);ax.set_xlim(-.55,2.55);ax.tick_params(axis='x',length=0,pad=12);ax.tick_params(axis='y',labelsize=15);ax.set_title(title,fontproperties=fp(21),pad=20);ax.spines['left'].set_color('#A1A8AF');ax.spines['bottom'].set_color('#A1A8AF');ax.grid(axis='y',alpha=.22,zorder=0)
 for label in ax.get_yticklabels():label.set_fontproperties(fp(15))
axes[0].set_ylabel('平均成员重叠度 Jaccard',fontproperties=fp(18),labelpad=13)
fig.suptitle('同一大类内部的 feature 激活组合更相似',fontproperties=fp(27),y=.972)
fig.text(.5,.885,'Qwen3-0.6B Base  ·  显式类别文本  ·  留出集：8 个配对文本家族',ha='center',fontproperties=fp(15),color='#414B56')
fig.text(.5,.075,'每个家族内：类内各 3 对（父类—子类、子类—子类）；跨大类 9 对。',ha='center',fontproperties=fp(13),color='#414B56')
fig.text(.5,.025,'误差线：根据原 8 个家族的单独均值重算的 95% 家族 bootstrap 区间；不是“类内减跨类”的区间。',ha='center',fontproperties=fp(12),color='#59636D')
fig.subplots_adjust(left=.083,right=.98,bottom=.19,top=.77,wspace=.16)
def save(fig,name):
 fig.savefig(P/'figures'/f'{name}.png',dpi=240)
 with plt.rc_context({'svg.fonttype':'none'}):fig.savefig(P/'figures'/f'{name}.svg')
 with plt.rc_context({'svg.fonttype':'path'}):fig.savefig(P/'figures'/f'{name}_outlined.svg')
 fig.savefig(P/'figures'/f'{name}.pdf');plt.close(fig)
save(fig,'figure1_category_overlap')
# Figure2: original two strings, same40coordinates and an adjacent ID mapping.
m=pd.read_csv(P/'data/figure2_F09_members.csv');meta=json.load(open(P/'data/figure2_F09_text_and_position.json'));shared='#15966F';lost='#EC8A24';gained='#1479BD';inactive='#E6E9ED';ink='#18202A';red='#CA3A41'
fig=plt.figure(figsize=(18,10));fig.text(.5,.976,'从动物到猫：部分 feature 保留，部分发生更替',ha='center',va='top',fontproperties=fp(27),color=ink)
fig.text(.5,.925,'显式留出实例 F09  ·  Attention 输出 SAE  ·  在两句末尾 Description: 的冒号处读取',ha='center',fontproperties=fp(15),color='#414B56')
for xx,key,name,col in [(.045,'animal','动物',lost),(.515,'cat','猫',gained)]:
 ax=fig.add_axes([xx,.69,.44,.19]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off');box=FancyBboxPatch((0,0),1,1,boxstyle='round,pad=0.015,rounding_size=.025',linewidth=1,edgecolor='#D5DBE1',facecolor='#F7F9FB',transform=ax.transAxes,clip_on=False);ax.add_patch(box);ax.text(.025,1.08,name,fontproperties=fp(18),color=col,va='bottom')
 ax.text(.03,.84,'Asked what the survey was about,',fontproperties=fp(15),va='top',color=ink)
 line=HPacker(children=[TextArea('the researcher replied that it concerned ',textprops={'fontproperties':fp(15),'color':ink}),TextArea(meta[key]['category_phrase'],textprops={'fontproperties':fp(16),'color':col,'bbox':dict(boxstyle='round,pad=.13',facecolor='#FFF0DC' if key=='animal' else '#E4F2FC',edgecolor='none')}),TextArea('.',textprops={'fontproperties':fp(15),'color':ink})],align='baseline',pad=0,sep=0)
 ax.add_artist(AnnotationBbox(line,(.03,.61),xycoords=ax.transAxes,box_alignment=(0,1),frameon=False,pad=0))
 ax.text(.03,.38,'The interview then ended.',fontproperties=fp(15),va='top',color=ink)
 read=HPacker(children=[TextArea('Description',textprops={'fontproperties':fp(15),'color':ink}),TextArea(':',textprops={'fontproperties':fp(19),'color':red}),TextArea('  ← 读取这里',textprops={'fontproperties':fp(14),'color':red})],align='baseline',pad=0,sep=0)
 ax.add_artist(AnnotationBbox(read,(.03,.15),xycoords=ax.transAxes,box_alignment=(0,1),frameon=False,pad=0))
fig.text(.5,.653,'原文：an animal → a cat，类别词与冠词同步变化；读取位置相同（第 23 个 token，0 起索引 22）。',ha='center',fontproperties=fp(14),color='#414B56')
parts=[('各激活 32 个',ink),('   |   ', '#9BA3AC'),('保留 24 个',shared),('   |   ','#9BA3AC'),('换出 8 个',lost),('   |   ','#9BA3AC'),('换入 8 个',gained)]
banner=HPacker(children=[TextArea(s,textprops={'fontproperties':fp(22),'color':c}) for s,c in parts],align='baseline',pad=0,sep=0);fig.add_artist(AnnotationBbox(banner,(.5,.602),xycoords=fig.transFigure,box_alignment=(.5,.5),frameon=False,pad=0))
arr=np.zeros((2,40),int)
for j,row in m.iterrows():
 if row.status=='shared':arr[:,j]=1
 elif row.status=='animal_only':arr[0,j]=2
 else:arr[1,j]=3
ax=fig.add_axes([.11,.385,.84,.13]);ax.imshow(arr,cmap=ListedColormap([inactive,shared,lost,gained]),vmin=0,vmax=3,aspect='auto',interpolation='nearest');ax.set_yticks([0,1],['动物','猫'],fontproperties=fp(19));ax.set_xticks([0,7,15,23,31,39],[1,8,16,24,32,40],fontproperties=fp(13));ax.tick_params(axis='both',length=0,pad=9);ax.set_xticks(np.arange(-.5,40,1),minor=True);ax.set_yticks([-.5,.5,1.5],minor=True);ax.grid(which='minor',color='white',linewidth=1);ax.tick_params(which='minor',bottom=False,left=False)
for p in ax.spines.values():p.set_visible(False)
for pos in [23.5,31.5]:ax.axvline(pos,color='white',linewidth=5)
for mid,lab,col in [(11.5,'共同保留 24',shared),(27.5,'动物独有 8（换出）',lost),(35.5,'猫独有 8（换入）',gained)]:ax.text(mid,-.82,lab,ha='center',va='center',fontproperties=fp(15),color=col,clip_on=False)
fig.text(.53,.332,'成员排列位置：同一列 = 同一个 feature；浅灰色 = 未激活',ha='center',fontproperties=fp(14),color='#414B56')
# Every featureID is explicit, keyed to the indicated column range.
for left,width,status,title,col,start,perline in [(.05,.52,'shared','列 1–24：保留',shared,1,8),(.59,.18,'animal_only','列 25–32：换出',lost,25,4),(.80,.18,'cat_only','列 33–40：换入',gained,33,4)]:
 ax=fig.add_axes([left,.11,width,.17]);ax.axis('off');ax.text(0,.98,title,fontproperties=fp(15),color=col,va='top');ids=m[m.status==status].feature_id.to_list()
 for q in range(0,len(ids),perline):
  label=f'{start+q}–{start+q+min(perline,len(ids)-q)-1}： '+ '  '.join(str(int(v)) for v in ids[q:q+perline]);ax.text(0,.69-(q//perline)*.24,label,fontproperties=fp(12.5),color='#26313E',va='top')
fig.text(.5,.060,'展示两句激活成员的并集，共 40 列；ID 对照表按图中从左到右的列次序排列。',ha='center',fontproperties=fp(13),color='#414B56')
fig.text(.5,.022,'Top-32 的固定名额使此例换出数与换入数相等；这是一个具体实例，需与图一的 8 家族总体统计配合解读。',ha='center',fontproperties=fp(12.5),color='#59636D')
save(fig,'figure2_F09_member_replacement')
print('PLOTS_READY')
