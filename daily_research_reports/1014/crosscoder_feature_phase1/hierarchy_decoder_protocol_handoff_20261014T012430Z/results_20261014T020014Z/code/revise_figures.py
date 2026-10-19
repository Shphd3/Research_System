"""User-requested visual revision; reuses saved geometry/counts; peak classes are post hoc."""
import os
os.environ.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
import sys,json,csv,time,hashlib,resource
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import TwoSlopeNorm

R=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z')
V=R/'visual_revision_20261014T025700Z'
LABELS={'train':'TRAIN 归一化坐标','raw':'恢复原始坐标'}
CLASSES=['layer_2','layer_28','other']
CLASS_LABELS=['第 2 层最大','第 28 层最大','其他层最大']
COLORS=['#3f82b0','#df8d41','#8a91a8']

def read(p):return json.loads(Path(p).read_text())
def rows(p):
 with Path(p).open() as f:return list(csv.DictReader(f))
def put(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def table(name,rr):
 rr=list(rr)
 with (V/'tables'/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 start=time.monotonic();os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:8])
 rec=read(V/'revision_record.json')
 for item in rec['source_files']:assert sha(item['path'])==item['sha256']
 font=V/'font/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));family=font_manager.FontProperties(fname=str(font)).get_name()
 plt.rcParams.update({'font.family':family,'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','pdf.fonttype':42})
 g=np.load(R/'derived_geometry.npz');Q=g['Q'];h=g['h'][1];layers=g['layers'];p={'train':g['p'],'raw':g['p_raw']};ll={'train':g['L'],'raw':g['L_raw']};ids=np.flatnonzero(Q);assert len(ids)==15537;ns=[int((Q&(h==i)).sum()) for i in range(6)];assert ns==[20,8896,5347,1209,63,2]
 assert np.array_equal(layers,np.arange(2,29,2));assert all(np.isfinite(a[:,Q]).all() and np.allclose(a[:,Q].sum(0),1) for a in p.values())
 stats=rows(R/'depth_vs_layer_summary.csv');means=rows(R/'hierarchy_mean_p.csv');result=read(R/'results.json');sel=read(R/'selection_frozen_before_geometry.json');nodeinfo={int(row['feature']):row for row in rows(R/'graph1_nodes.csv')};edges=rows(R/'graph1_edges.csv');meta=[]
 def save(fig,name,question,source,note=''):
  # Check every rendered text object is supported by the selected CJK font.
  from matplotlib.ft2font import FT2Font
  cmap=FT2Font(str(font)).get_charmap();missing=sorted({ord(c) for tx in fig.findobj(matplotlib.text.Text) for c in tx.get_text() if not c.isspace() and ord(c) not in cmap});assert not missing,missing
  for ext in ['png','pdf','svg']:fig.savefig(V/'figures'/f'{name}.{ext}',dpi=165,bbox_inches='tight')
  plt.close(fig);meta.append({'name':name,'question':question,'sources':source,'note':note,'n_Q':15537,'graph':'V full saved graph','no_independent_node_inference':True})
 def node_label(a):
  row=nodeinfo[a];return f"Feature {a}；h={h[a]}\nV 命中数：{int(row['n_V']):,}\nV 激活频率：{100*float(row['frequency_V']):.4g}%"
 table('figure1_nodes_display.csv',({'feature':a,'h':int(h[a]),'V_hits':int(row['n_V']),'V_activation_frequency_percent':100*float(row['frequency_V'])} for a,row in nodeinfo.items()))
 # Figure1: exact existing nodes/edges, with unambiguous frequency units.
 for anchor,subset in sel['subsets'].items():
  groups=defaultdict(list)
  for a in subset:groups[int(h[a])].append(a)
  pos={a:(float(x),depth) for depth,group in groups.items() for a,x in zip(sorted(group),np.linspace(.04,.96,len(group)) if len(group)>1 else [.5])}
  used=[row for row in edges if int(row['A']) in subset]
  fig,ax=plt.subplots(figsize=(27,13));ax.set(xlim=(-.03,1.03),ylim=(-.45,5.55),yticks=range(6),xticks=[],ylabel='统计图层级 h（无量纲；完整 V 图）',xlabel='横向位置仅用于排版；箭头 A→更常见的 u；边编号对应支持数源表')
  ax.grid(axis='y',alpha=.2);ax.spines[['top','right','bottom']].set_visible(False)
  for row in used:
   a,u=int(row['A']),int(row['u']);x1,y1=pos[a];x2,y2=pos[u];rad=((int(row['edge_id'])%5)-2)*.025
   ax.add_patch(FancyArrowPatch((x1,y1-.14),(x2,y2+.15),arrowstyle='-|>',mutation_scale=12,linewidth=.9,color='#526b82',alpha=.7,connectionstyle=f'arc3,rad={rad}',zorder=1))
   if h[a]!=1 or h[u]!=0:
    f=.32+.1*(int(row['edge_id'])%3);ax.text(x1+(x2-x1)*f,y1+(y2-y1)*f,row['edge_id'],fontsize=8,color='#334c64',ha='center',bbox=dict(facecolor='white',edgecolor='none',alpha=.8,pad=.3))
  for a,(x,y) in pos.items():ax.text(x,y,node_label(a),ha='center',va='center',fontsize=8.5,bbox=dict(boxstyle='round,pad=.35',facecolor='#cbdfee' if str(a)==anchor else '#e5eef6',edgecolor='#416781'),zorder=4)
  ax.set_title(f'图1｜Feature {anchor} 的完整出边可达子图：{len(subset)} 个节点、{len(used)} 条边\n统计图层级 h 不等于模型层号；激活频率以 V 的 5,247,663 个位置为分母；底部密集边见分面',pad=15)
  save(fig,f'figure1_anchor_{anchor}','固定节点的统计关联如何组织？',['graph1_nodes.csv','graph1_edges.csv'],'节点激活频率单位%；无传播／功能标签')
  parents=sorted(a for a in subset if h[a]==1);fig,axs=plt.subplots(len(parents),1,figsize=(27,4*len(parents)),squeeze=False)
  for ax,a in zip(axs[:,0],parents):
   ee=[row for row in used if int(row['A'])==a];children=sorted(int(row['u']) for row in ee);xx=np.linspace(.04,.96,len(children)) if len(children)>1 else [.5];positions=dict(zip(children,xx));ax.set(xlim=(-.03,1.03),ylim=(-.35,1.35),yticks=[0,1],xticks=[],ylabel='统计图层级 h');ax.grid(axis='y',alpha=.12);ax.spines[['top','right','bottom']].set_visible(False)
   for u,x in positions.items():
    row=next(row for row in ee if int(row['u'])==u);ax.add_patch(FancyArrowPatch((.5,.82),(x,.15),arrowstyle='-|>',mutation_scale=12,linewidth=1,color='#526b82'));ax.text(x,.43,f"边 e{row['edge_id']}\nD/V 共同命中：{row['c_D']}/{row['c_V']}\nV 条件概率 P(u|A)：{float(row['P_u_given_A_V']):.4f}",ha='center',va='center',fontsize=7.5,bbox=dict(facecolor='white',edgecolor='none',alpha=.95,pad=1))
   for u,x,y in [(a,.5,1)]+[(u,float(x),0) for u,x in positions.items()]:ax.text(x,y,node_label(u),ha='center',va='center',fontsize=8,bbox=dict(boxstyle='round,pad=.3',facecolor='#e5eef6',edgecolor='#416781'))
  fig.suptitle(f'图1分面｜Feature {anchor} 子图中的密集边；箭头 A→更常见的 u\n同一节点与同一边，统计图层级 h 保持完整图定义；V 激活频率单位为 %',y=1.005);fig.tight_layout();save(fig,f'figure1_anchor_{anchor}_details','密集边的支持与条件概率是多少？',['graph1_edges.csv','graph1_nodes.csv'])
 # Heatmap helper: common units, explicit sample count; pair uses one shared scale.
 def heatmap(ax,arr,ylabels,title,vmax,annotate=True):
  im=ax.imshow(100*arr,aspect='auto',interpolation='nearest',cmap='viridis',vmin=0,vmax=vmax);ax.set_xticks(range(14),layers);ax.set_yticks(range(len(ylabels)),ylabels);ax.set_xlabel('模型层号（一基）');ax.set_title(title,pad=13)
  if annotate:
   for i in range(len(ylabels)):
    for j in range(14):ax.text(j,i,f'{100*arr[i,j]:.1f}',ha='center',va='center',fontsize=8,color='black' if 100*arr[i,j]>.6*vmax else 'white')
  return im
 nodes=sorted(sel['nodes'],key=lambda a:(h[a],a));fig,ax=plt.subplots(figsize=(17,14));arr=p['train'][:,nodes].T;vmax=float(np.ceil(arr.max()*10)*10);im=heatmap(ax,arr,[f'Feature {a}；h={h[a]}' for a in nodes],'图2｜同一批 30 个 Feature 的跨层解码幅度占比 p\nTRAIN 归一化坐标；行按统计图层级 h、再按 ID 排序',vmax);ax.set_ylabel('Feature 与统计图层级 h');fig.colorbar(im,ax=ax,pad=.02,label='跨层解码幅度占比 p（%；每行合计 100%）');fig.tight_layout();save(fig,'figure2_decoder_distribution','同一节点的 14 层解码轮廓是否相同？',['figure2_source.csv'])
 # Figure3 same exact IDs/jitter/axes/aggregation, two coordinates.
 original=rows(R/'figure3_source.csv');table('figure3_coordinate_comparison_source.csv',({'feature':int(row['feature']),'h':int(row['h']),'x_for_plot':float(row['x_for_plot']),'L_train':float(ll['train'][int(row['feature'])]),'L_raw':float(ll['raw'][int(row['feature'])])} for row in original))
 xx=np.array([float(row['x_for_plot']) for row in original]);orderedids=np.array([int(row['feature']) for row in original]);assert np.array_equal(orderedids,ids)
 fig,axs=plt.subplots(1,2,figsize=(20,8),sharex=True,sharey=True)
 for ax,key,condition in zip(axs,['train','raw'],['V_train_normalized','V_raw_coordinate']):
  ax.scatter(xx,ll[key][ids],s=7,color='#346b91',alpha=.12,rasterized=True,label='每点一个 Feature；横向抖动仅排版')
  for depth in range(6):
   ax.text(depth,28.65,f'n={ns[depth]:,}',ha='center',fontsize=10)
   if depth<5:
    row=next(row for row in stats if row['condition']==condition and int(row['h'])==depth);med=float(row['median']);ax.errorbar(depth,med,yerr=np.array([[med-float(row['q25'])],[float(row['q75'])-med]]),fmt='o',color='#c95e2a',linewidth=2.5,capsize=6,label='中位数与四分位范围' if depth==0 else None)
   else:
    for a in [937,3461]:
     x=xx[np.flatnonzero(ids==a)[0]];ax.scatter(x,ll[key][a],s=65,facecolors='none',edgecolors='#a22c35',linewidths=1.6);ax.annotate(str(a),(x,ll[key][a]),xytext=(7,10 if a==937 else -17),textcoords='offset points',fontsize=9)
  ax.set(xlim=(-.4,5.45),ylim=(1.5,29.3),xticks=range(6),xlabel='统计图层级 h（无量纲）');ax.grid(alpha=.2);rho=result['correlations'][condition]['rho'];ax.set_title(f'{LABELS[key]}\n相同 15,537 个 Feature；描述性 Spearman={rho:.6f}',pad=14)
 axs[0].set_ylabel('幅度加权平均层号 L（模型层号；一基）');handles,labels=axs[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.01),ncol=2,frameon=False);fig.suptitle('图3｜统计图层级 h—幅度加权平均层号 L：两种坐标的同口径对照',y=1.01);fig.text(.5,.075,'相同坐标范围与绘图规则；四分位范围不是置信区间；h=5 单列两点；L 不代表整条分布移动',ha='center',fontsize=10);fig.subplots_adjust(bottom=.2,wspace=.1);save(fig,'figure3_all_features','方向是否保留、幅度差异有多依赖坐标？',['figure3_coordinate_comparison_source.csv','depth_vs_layer_summary.csv'])
 # Full 6x14 mean p in each coordinate, from the existing registered mean table.
 meanarrays={};meanrows=[]
 for key,condition in [('train','V_train_normalized'),('raw','V_raw_coordinate')]:
  arr=np.array([[float(next(row for row in means if row['condition']==condition and int(row['h'])==depth)[f'mean_p_layer{layer}']) for layer in layers] for depth in range(6)]);meanarrays[key]=arr
  for depth in range(6):
   for j,layer in enumerate(layers):meanrows.append({'coordinate':key,'h':depth,'n':ns[depth],'model_layer':int(layer),'mean_p':float(arr[depth,j])})
  fig,ax=plt.subplots(figsize=(16,6));im=heatmap(ax,arr,[f'h={depth}；n={ns[depth]:,}' for depth in range(6)],f'图4｜完整 6×14 组平均跨层解码幅度占比 p\n{LABELS[key]}；15,537 个 Feature 等权平均',40);ax.set_ylabel('统计图层级 h 与组内 Feature 数');fig.colorbar(im,ax=ax,pad=.02,label='平均跨层解码幅度占比 p（%；两图统一 0–40%）');fig.tight_layout();save(fig,f'figure4_mean_p_{key}','组平均轮廓在两种坐标下如何变化？',['hierarchy_mean_p.csv'],'两图共同色标；不是先加幅度再归一')
 table('group_mean_p_source.csv',meanrows);assert all(np.allclose(arr.sum(1),1) for arr in meanarrays.values())
 # Authorized additional post-hoc peak description, no formal hypothesis test.
 peakrows=[];composition=[]
 for key in ['train','raw']:
  arr=p[key][:,ids];ties=(arr==arr.max(0)).sum(0);assert (ties==1).all();peak=layers[arr.argmax(0)]
  for j,a in enumerate(ids):peakrows.append({'coordinate':key,'feature':int(a),'h':int(h[a]),'maximum_model_layer':int(peak[j]),'peak_class':'layer_2' if peak[j]==2 else 'layer_28' if peak[j]==28 else 'other','maximum_p':float(arr[:,j].max()),'exact_maximum_ties':int(ties[j]),'analysis_role':'POST_HOC_DESCRIPTIVE'})
  for depth in range(6):
   at=h[ids]==depth
   for cat in CLASSES:
    mask=peak==2 if cat=='layer_2' else peak==28 if cat=='layer_28' else (peak!=2)&(peak!=28);cnt=int((at&mask).sum());composition.append({'coordinate':key,'h':depth,'n_features':ns[depth],'peak_class':cat,'feature_count':cnt,'share':cnt/ns[depth],'analysis_role':'POST_HOC_DESCRIPTIVE'})
 table('peak_feature_labels_posthoc.csv',peakrows);table('peak_composition_posthoc.csv',composition)
 fig,axs=plt.subplots(1,2,figsize=(17,7),sharex=True,sharey=True)
 for ax,key in zip(axs,['train','raw']):
  bottom=np.zeros(6)
  for cat,label,color in zip(CLASSES,CLASS_LABELS,COLORS):
   shares=np.array([100*next(row for row in composition if row['coordinate']==key and row['h']==depth and row['peak_class']==cat)['share'] for depth in range(6)]);ax.bar(range(6),shares,bottom=bottom,color=color,label=label,width=.7)
   for depth,value in enumerate(shares):
    if value>=3:ax.text(depth,bottom[depth]+value/2,f'{value:.1f}%',ha='center',va='center',fontsize=10)
   bottom+=shares
  assert np.allclose(bottom,100)
  for depth in range(6):ax.text(depth,102,f'n={ns[depth]:,}',ha='center',fontsize=10)
  ax.set(xlim=(-.5,5.5),ylim=(0,108),xticks=range(6),xlabel='统计图层级 h（无量纲）',title=LABELS[key]);ax.grid(axis='y',alpha=.15)
 axs[0].set_ylabel('该峰值类别的 Feature 比例（%；每柱合计 100%）');handles,labels=axs[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,frameon=False);fig.suptitle('图5｜每个 h 内，最大解码分量落在哪层？【事后描述】',y=1.01);fig.text(.5,.07,'同一 15,537 个 Feature；类别只描述幅度峰值，不代表功能；小于 3% 的色段保留，精确值见源表',ha='center',fontsize=10);fig.subplots_adjust(bottom=.18,wspace=.1);save(fig,'figure5_peak_composition_posthoc','同级内不同峰值类别的比例如何、是否依赖坐标？',['peak_composition_posthoc.csv','peak_feature_labels_posthoc.csv'],'事后描述；无因果／功能／common-unique命名')
 # All 20 qualified h=0 nodes, both coordinates; no low-support isolates.
 zeroids=np.flatnonzero(Q&(h==0));assert len(zeroids)==20;vmax=float(np.ceil(max(p[key][:,zeroids].max() for key in p)*10)*10);fig,axs=plt.subplots(1,2,figsize=(25,11),sharey=True)
 for ax,key in zip(axs,['train','raw']):im=heatmap(ax,p[key][:,zeroids].T,[f'Feature {a}' for a in zeroids],f'{LABELS[key]}；h=0；n=20',vmax)
 axs[0].set_ylabel('Feature（全部 20 个合格非孤立叶节点）');fig.suptitle('图6｜h=0 的逐个跨层解码幅度占比 p：同级内部差异',y=1.01);fig.subplots_adjust(wspace=.1,right=.89);cax=fig.add_axes([.92,.15,.012,.70]);fig.colorbar(im,cax=cax,label='跨层解码幅度占比 p（%；两面板共用色标）');save(fig,'figure6_h0_individual','20个合格叶节点是否具有相同轮廓？',['h0_individual_source.csv'],'不包含847个孤立节点')
 table('h0_individual_source.csv',({'coordinate':key,'feature':int(a),'h':0,'model_layer':int(layer),'p':float(p[key][j,a])} for key in ['train','raw'] for a in zeroids for j,layer in enumerate(layers)))
 # h=5 two individual curves in each coordinate, no group inference.
 topids=np.flatnonzero(Q&(h==5));assert topids.tolist()==[937,3461];fig,axs=plt.subplots(1,2,figsize=(17,6),sharex=True,sharey=True)
 for ax,key in zip(axs,['train','raw']):
  for a,color in zip(topids,['#367aa4','#bf6046']):ax.plot(layers,100*p[key][:,a],marker='o',color=color,label=f'Feature {a}；L={ll[key][a]:.3f}')
  ax.set(xlim=(1,29),ylim=(0,100),xticks=layers,xlabel='模型层号（一基）',title=LABELS[key]);ax.grid(alpha=.2);ax.legend(loc='upper left',frameon=False,fontsize=10)
 axs[0].set_ylabel('跨层解码幅度占比 p（%；每条曲线合计 100%）');fig.suptitle('图7｜h=5 两个 Feature 的各自轮廓：n=2，不作最高级总体推断',y=1.01);fig.tight_layout();save(fig,'figure7_h5_individual_curves','同为最高统计图层级的两个Feature，轮廓是否相同？',['h5_curves_source.csv'])
 table('h5_curves_source.csv',({'coordinate':key,'feature':int(a),'h':5,'model_layer':int(layer),'p':float(p[key][j,a]),'L':float(ll[key][a])} for key in ['train','raw'] for a in topids for j,layer in enumerate(layers)))
 # All 25 predeclared V frequency cells. Invalid cells remain gray, never zero.
 freq=[row for row in rows(R/'frequency_overlap_comparison.csv') if row['graph']=='V'];assert len(freq)==25;arr=np.full((5,5),np.nan);fr=[]
 for row in freq:
  ok=row['status'] in ['COMPARABLE_RANGE','FIXED_FREQUENCY_LOCAL'];b=int(row['frequency_bin']);c=int(row['h_low'])
  if ok:arr[b,c]=float(row['delta_median_L'])
  fr.append(dict(row,display_valid=str(ok),display_delta_median_L=row['delta_median_L'] if ok else '',annotation_population='intersection' if row['status'] in ['COMPARABLE_RANGE','FIXED_FREQUENCY_LOCAL','SMALL_N','NO_ACTUAL_NODES'] else 'original_frequency_group'))
 table('frequency_comparison_25cells_source.csv',fr)
 cm=plt.get_cmap('RdBu_r').copy();cm.set_bad('#d9d9d9');fig,ax=plt.subplots(figsize=(15,10));im=ax.imshow(arr,cmap=cm,norm=TwoSlopeNorm(vmin=-10,vcenter=0,vmax=10),aspect='auto');ax.set_xticks(range(5),[f'{i}↔{i+1}' for i in range(5)]);ax.set_yticks(range(5),[f'频率组 {i+1}'+('（最低）' if i==0 else '（最高）' if i==4 else '') for i in range(5)]);ax.set_xlabel('统计图层级 h 的相邻对（差值＝高 h 减低 h）');ax.set_ylabel('D 激活频率分位组（固定 5 组）')
 for row in freq:
  b,c=int(row['frequency_bin']),int(row['h_low']);status=row['status'];nl,nh=row['n_low'],row['n_high'];color='black'
  if status in ['COMPARABLE_RANGE','FIXED_FREQUENCY_LOCAL']:
   val=float(row['delta_median_L']);s=f'差值 {val:+.3f}\n交集 n={nl}/{nh}';color='white' if abs(val)>5 else 'black'
  elif status=='SMALL_N':s=f'样本不足（各需 ≥20）\n交集 n={nl}/{nh}'
  elif status=='NO_GROUP':s=f"缺组\n组内 n={row['pre_n_low']}/{row['pre_n_high']}"
  elif status=='NO_OVERLAP':s=f"无共同范围\n组内 n={row['pre_n_low']}/{row['pre_n_high']}\n交集 n=0/0"
  else:s=f'无实际节点\n交集 n={nl}/{nh}'
  ax.text(c,b,s,ha='center',va='center',fontsize=10,color=color)
 ax.set_xticks(np.arange(-.5,5,1),minor=True);ax.set_yticks(np.arange(-.5,5,1),minor=True);ax.grid(which='minor',color='white',linewidth=2);ax.tick_params(which='minor',bottom=False,left=False);fig.colorbar(im,ax=ax,pad=.025,label='幅度加权平均层号 L 中位差（模型层号；高 h − 低 h）');ax.set_title('图8｜频率共同范围内比较：全部 25 个预定格\nTRAIN 归一化坐标；V 图；同一 Q（15,537 个 Feature）；11 格可比较',pad=15);fig.text(.5,.02,'灰格不是 0；n 顺序为低 h / 高 h。组内 n 为交集筛选前计数，交集 n 为比较所用计数。\n五分位与范围交集不等于严格频率匹配；没有共同范围或样本不足时不作该格比较。',ha='center',fontsize=10);fig.subplots_adjust(bottom=.15);save(fig,'figure8_frequency_all25','频率比较的效应大小、样本数和缺覆盖分别是什么？',['frequency_overlap_comparison.csv','frequency_comparison_25cells_source.csv'])
 # Current revision only: source checks and provenance, not a new experimental verdict.
 assert np.isfinite(arr).sum()==11
 for key in ['train','raw']:
  for depth in range(6):assert sum(row['feature_count'] for row in composition if row['coordinate']==key and row['h']==depth)==ns[depth]
 for item in rec['source_files']:assert sha(item['path'])==item['sha256']
 rec.update(status='RENDERED_PENDING_VISUAL_REVIEW',figure_manifest=meta,render_seconds=time.monotonic()-start,max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,font={'path':str(font),'sha256':sha(font),'source':'https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf','not_copied_to_git_or_delivery':True},source_files_unchanged=True,peak_exact_ties={'train':0,'raw':0},new_statistics='POST_HOC_DESCRIPTIVE_PEAK_COUNTS_ONLY');put(V/'revision_record.json',rec);put(V/'peak_composition_summary.json',composition);print(json.dumps({'status':rec['status'],'render_seconds':rec['render_seconds'],'figures':len(meta),'peak_composition':composition},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
