"""Saved V graph visualization only; no new graph/statistical fitting/inference."""
import os
os.environ.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
from pathlib import Path
import json,csv,hashlib,time,resource,datetime
from collections import Counter,defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages

V=Path(__file__).resolve().parents[1]
R=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z')
O=R.parents[1]/'feature_relation_phase1/20261013T173130Z'
# R is .../analysis/hierarchy_decoder_distribution/run; sibling phase1 is analysis/feature_relation_phase1.
O=R.parent.parent/'feature_relation_phase1/20261013T173130Z'
start=time.monotonic();os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:8])
def read(p):return json.loads(Path(p).read_text())
def put(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=lambda a:a.item() if isinstance(a,np.generic) else a.tolist())+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def table(name,rr):
 rr=list(rr)
 with (V/'tables'/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
rules=read(V/'selection_rules_frozen.json')
required=[O/'graphs/reduced_V.json',O/'graphs/raw_edges.npz',O/'feature_frequency.npz',R/'selection_frozen_before_geometry.json',R/'derived_geometry.npz']
source=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in required]
# Verify saved parent identities, not file names alone.
original_manifest=read(R/'input_reuse_manifest.json')
oldhash={x['path']:x['sha256'] for x in original_manifest['files']}
for x in source:
 if x['path'] in oldhash:assert x['sha256']==oldhash[x['path']]
g=read(O/'graphs/reduced_V.json');h=np.asarray(g['depth']);out=g['lists'];F=len(h);assert F==16384
indeg=np.zeros(F,dtype=int)
for us in out:indeg[us]+=1
outdeg=np.array([len(us) for us in out]);fr=np.load(O/'feature_frequency.npz');n=fr['n'];Q=(n>=200).all(0)&((indeg+outdeg)>0);ids=np.flatnonzero(Q);ns=[int((Q&(h==j)).sum()) for j in range(6)];assert ns==[20,8896,5347,1209,63,2]
N_D=5238097;N_V=5247663
oldsel=read(R/'selection_frozen_before_geometry.json');oldnodes=set(oldsel['nodes']);assert len(oldnodes)==30
rng=np.random.Generator(np.random.PCG64(rules['seed']));selected=oldnodes|set(np.flatnonzero(Q&np.isin(h,[0,4,5])).tolist());reason=defaultdict(set)
for a in oldnodes:reason[a].add('old_anchor_union')
for a in selected:
 if h[a] in [0,4,5]:reason[a].add('all_h'+str(h[a]))
witness=[]
for root in sorted(np.flatnonzero(Q&(h==4)).tolist()):
 path=[root];a=root
 while h[a]>0:
  options=sorted(u for u in out[a] if h[u]==h[a]-1 and Q[u]);assert options
  reuse=[u for u in options if u in selected];pick=int(rng.choice(reuse or options));selected.add(pick);reason[pick].add('h4_longest_path_witness');path.append(pick);a=pick
 witness.append({'root_h4':root,'path':path})
strata={}
for depth in range(6):
 allh=sorted(np.flatnonzero(Q&(h==depth)).tolist(),key=lambda a:(int(n[0,a]),a))
 for b,chunk in enumerate(np.array_split(np.array(allh,dtype=int),4)):
  for a in chunk:strata[int(a)]=b
quota=rules['target_counts_h0_to_h5'];protectedcounts=[int(sum(h[a]==j for a in selected)) for j in range(6)]
for depth in [3,2,1]:
 while sum(h[a]==depth for a in selected)<quota[depth]:
  opts={b:sorted(a for a in ids.tolist() if h[a]==depth and strata[a]==b and a not in selected) for b in range(4)}
  available=[b for b in range(4) if opts[b]];assert available
  b=min(available,key=lambda b:(sum(h[a]==depth and strata[a]==b for a in selected),b))
  a=int(rng.choice(opts[b]));selected.add(a);reason[a].add('D_frequency_rank_stratum_fill')
selected=sorted(selected);selectedset=set(selected);sc=[int(sum(h[a]==j for a in selected)) for j in range(6)];assert 200<=len(selected)<=400
edgepairs=sorted((a,int(u)) for a in selected for u in out[a] if u in selectedset)
assert all(h[a]>h[u] for a,u in edgepairs)
# Freeze selected IDs before reading p/L, no decoder-based selection.
freeze={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rule_sha256':sha(V/'selection_rules_frozen.json'),'selected_ids':selected,'counts_h0_to_h5':sc,'protected_counts_before_frequency_fill':protectedcounts,'old_anchor_ids_all_present':oldnodes.issubset(selectedset),'h4_witness_paths':witness,'selected_direct_edges':len(edgepairs),'full_Q_counts':ns,'no_geometry_read_before_this_freeze':True}
if (V/'selection_frozen_before_p.json').exists():
 previous=read(V/'selection_frozen_before_p.json');assert previous['selected_ids']==selected and previous['counts_h0_to_h5']==sc and previous['h4_witness_paths']==witness
else:put(V/'selection_frozen_before_p.json',freeze)
print(json.dumps({'stage':'SELECTION_FROZEN','counts':sc,'nodes':len(selected),'edges':len(edgepairs),'protected_counts':protectedcounts}),flush=True)
# Saved direct edge supports, no recount or reconstruction.
raw=np.load(O/'graphs/raw_edges.npz');raw={k:raw[k] for k in raw.files};lookup={(int(a),int(u)):i for i,(a,u) in enumerate(zip(raw['A'],raw['u'])) if a in selectedset and u in selectedset};oldedge={(int(a['A']),int(a['u'])):a for a in csv.DictReader((R/'graph1_edges.csv').open())}
for a,u in edgepairs:assert (a,u) in lookup and raw['passV'][lookup[a,u]]
# IDs within each layer are ordered by barycenter for layout only.
groups={j:sorted(a for a in selected if h[a]==j) for j in range(6)}
adj=defaultdict(list)
for a,u in edgepairs:adj[a].append(u);adj[u].append(a)
def xpos():return {a:(i+.5)/len(group) for j,group in groups.items() for i,a in enumerate(group)}
for sweep in range(16):
 for j in (range(6) if sweep%2==0 else range(5,-1,-1)):
  x=xpos();groups[j]=sorted(groups[j],key=lambda a:(float(np.median([x[b] for b in adj[a]])) if adj[a] else x[a],a))
x=xpos();order=[a for depth in range(5,-1,-1) for a in groups[depth]]
# Explicit omitted neighbor counts from saved full graph.
shown_in=Counter(u for a,u in edgepairs);shown_out=Counter(a for a,u in edgepairs)
noderows=[]
for idx,a in enumerate(order):
 noderows.append({'feature':a,'h_full_V':int(h[a]),'n_D':int(n[0,a]),'n_V':int(n[1,a]),'D_activation_frequency':float(n[0,a]/N_D),'V_activation_frequency':float(n[1,a]/N_V),'D_frequency_rank_stratum_within_h':strata[a]+1,'selection_reasons':'|'.join(sorted(reason[a])),'full_in_degree':int(indeg[a]),'shown_in_degree':shown_in[a],'omitted_in_neighbors':int(indeg[a]-shown_in[a]),'full_out_degree':int(outdeg[a]),'shown_out_degree':shown_out[a],'omitted_out_neighbors':int(outdeg[a]-shown_out[a]),'layout_x':x[a],'layout_order':idx})
table('expanded_nodes.csv',noderows)
# Highlight old branches only for reading continuity; all other edges still drawn.
oldpairs=set(oldedge);edgerows=[]
for ei,(a,u) in enumerate(edgepairs):
 k=lookup[a,u];cd=int(raw['cD'][k]);cv=int(raw['cV'][k]);row={'edge_id':ei,'A':a,'u':u,'h_A_full_V':int(h[a]),'h_u_full_V':int(h[u]),'h_skip':int(h[a]-h[u]),'n_A_D':int(n[0,a]),'n_u_D':int(n[0,u]),'joint_D':cd,'n_A_V':int(n[1,a]),'n_u_V':int(n[1,u]),'joint_V':cv,'P_u_given_A_D':cd/int(n[0,a]),'P_u_given_A_V':cv/int(n[1,a]),'P_A_given_u_V':cv/int(n[1,u]),'V_activation_frequency_u':int(n[1,u])/N_V,'lift_V':cv*N_V/(int(n[1,a])*int(n[1,u])),'in_old_30_node_branches':(a,u) in oldpairs,'edge_semantics':'saved_reduced_V_direct_association'}
 assert row['P_u_given_A_V']>=.8 and row['P_A_given_u_V']<=.5 and row['n_u_V']>=2*row['n_A_V']
 if (a,u) in oldedge:assert cv==int(oldedge[a,u]['c_V']) and cd==int(oldedge[a,u]['c_D'])
 edgerows.append(row)
table('expanded_edges.csv',edgerows)
table('overview_counts.csv',({'h':j,'Q_nodes':ns[j],'display_nodes':sc[j],'other_Q_nodes_not_displayed':ns[j]-sc[j]} for j in range(5,-1,-1)))
table('display_frequency_coverage.csv',({'h':j,'rank_stratum':b+1,'full_Q_n':sum(h[a]==j and strata[a]==b for a in ids),'display_n':sum(h[a]==j and strata[a]==b for a in selected),'D_frequency_min':float(min(n[0,a]/N_D for a in ids if h[a]==j and strata[a]==b)) if any(h[a]==j and strata[a]==b for a in ids) else '', 'D_frequency_max':float(max(n[0,a]/N_D for a in ids if h[a]==j and strata[a]==b)) if any(h[a]==j and strata[a]==b for a in ids) else ''} for j in range(6) for b in range(4)))
geom=np.load(R/'derived_geometry.npz');pp={key:geom[name] for key,name in [('train','p'),('raw','p_raw')]};assert np.array_equal(geom['h'][1],h) and np.array_equal(geom['Q'],Q);layers=geom['layers']
table('expanded_decoder_p.csv',({'coordinate':key,'feature':a,'h_full_V':int(h[a]),'row_order':idx,'model_layer':int(l),'p':float(pp[key][j,a])} for key in ['train','raw'] for idx,a in enumerate(order) for j,l in enumerate(layers)))
font=R/'visual_revision_20261014T025700Z/font/NotoSansCJKsc-Regular.otf';assert font.exists();font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','pdf.fonttype':42})
colors=['#b76353','#4c8b61','#3f87b4','#9273ad','#c49b39','#b35a92']
figuremeta=[]
def save(fig,name,dpi=200):
 for ext in ['png','svg','pdf']:fig.savefig(V/'figures'/f'{name}.{ext}',dpi=dpi,bbox_inches='tight')
 plt.close(fig);figuremeta.append(name);print('RENDERED',name,flush=True)
# Actual overall counts, not representative nodes or a fabricated pyramid.
fig,ax=plt.subplots(figsize=(20,10))
for depth in range(6):
 count=ns[depth];k=np.arange(count);xx=(k%200)/200;yy=depth+.32-(k//200)*(.64/45)
 ax.scatter(xx,yy,s=.35,color=colors[depth],marker='s',linewidths=0)
 ax.text(-.03,depth,f'h={depth}',ha='right',va='center',fontsize=15);ax.text(1.03,depth,f'n={count:,}',ha='left',va='center',fontsize=15)
 ax.axhline(depth-.46,color='#dedede',lw=.7)
ax.set(xlim=(-.08,1.18),ylim=(-.5,5.55),xticks=[],yticks=[]);ax.spines[:].set_visible(False);ax.set_title('整体概览｜完整纳入分析的 15,537 个 Feature；统计图层级 h=5 在上、h=0 在下\n每个小方点＝1 个真实 Feature；每层级带内固定 200 列点阵，点的位置仅用于排版',pad=20)
fig.text(.5,.02,'这是纳入分析的非孤立特征集合；h=0 的 20 个节点不代表全部 16,384 个特征中的所有终点。\n点阵不表示模型深度、相似度或边；完整字典 h=0 共 867 个，其中 847 个孤立节点不在本集合。',ha='center',fontsize=12);fig.subplots_adjust(bottom=.15);save(fig,'figure1_full_hierarchy_overview',300)
# Main expanded graph, all selected direct edges, no pruning by supports/decoder.
def graphfig(visible,ee,title,large=True):
 fig,ax=plt.subplots(figsize=(42,16) if large else (32,13));visible=set(visible)
 for depth in range(6):
  ax.axhline(depth,color=colors[depth],alpha=.2,lw=1);shown=sum(h[a]==depth for a in visible)
  ax.text(-.018,depth,f'h={depth}\n本页 {shown}\n全Q {ns[depth]:,}',ha='right',va='center',fontsize=10)
 for a,u in ee:
  highlight=(a,u) in oldpairs;ax.add_patch(FancyArrowPatch((x[a],h[a]-.06),(x[u],h[u]+.06),arrowstyle='-|>',mutation_scale=5 if large else 7,color='#925d40' if highlight else '#607487',alpha=.55 if highlight else (.26 if large else .32),linewidth=.85 if highlight else (.6 if large else .48),connectionstyle='arc3,rad=0',zorder=1))
 for depth in range(6):
  aa=[a for a in groups[depth] if a in visible];ax.scatter([x[a] for a in aa],[depth]*len(aa),s=62,color=colors[depth],edgecolors='white',linewidths=.5,zorder=3)
  for a in aa:
   ax.annotate(str(a)+('†' if shown_in[a]+shown_out[a]==0 else ''),(x[a],depth),xytext=(0,10),textcoords='offset points',ha='center',va='bottom',fontsize=7.5,zorder=5,bbox=dict(facecolor='white',edgecolor='none',alpha=.90,pad=.4))
   ax.annotate(f'{100*n[1,a]/N_V:.3g}%',(x[a],depth),xytext=(0,-13),textcoords='offset points',ha='center',va='top',fontsize=6.2,zorder=5,bbox=dict(facecolor='white',edgecolor='none',alpha=.90,pad=.3))
 ax.set(xlim=(-.06,1.025),ylim=(-.42,5.5),xticks=[],yticks=[]);ax.spines[:].set_visible(False);ax.set_title(title+'\n节点上方为稳定 Feature ID；下方为 V 激活频率（%）；统一节点大小，不同颜色表示统计图层级 h',pad=22)
 fig.text(.5,.035,'箭头 A→更常见的 u；展示所有选中端点之间已有的 V 约简直接边，包含跨 h 的边。棕色为原两个锚点分支内的边。\n未显示邻居不等于没有关系，逐节点完整／展示／遗漏入出度见 CSV；左右位置只为减少交叉，不代表相似度。\n本图是分层选取的展示子图，不按总体比例抽样；† 表示该节点仅在此子图没有连线，完整图中并非孤立。\n统计图层级不表示模型深度，边不表示已确认的因果关系或语义组合。',ha='center',fontsize=12);fig.subplots_adjust(bottom=.14);return fig
main=graphfig(selected,edgepairs,f'大型层级关联图｜{len(selected)} 个 Feature，{len(edgepairs):,} 条真实直接边；h 沿用完整 V 图')
save(main,'figure1_expanded_connections',210)
# Multipage readable facets: each shown edge appears exactly once by source node batch.
pages=[];faceted=0
with PdfPages(V/'figures/figure1_expanded_connections_facets.pdf') as pdf:
 for depth in range(5,0,-1):
  parents=groups[depth]
  for i in range(0,len(parents),20):
   batch=set(parents[i:i+20]);ee=[(a,u) for a,u in edgepairs if a in batch]
   visible=batch|{u for a,u in ee};fig=graphfig(visible,ee,f'直接边分面｜起点 h={depth}，第 {i//20+1} 批；{len(batch)} 个起点，{len(ee)} 条边',large=False);pdf.savefig(fig,bbox_inches='tight');plt.close(fig);faceted+=len(ee);pages.append({'page':len(pages)+1,'source_h':depth,'source_ids':sorted(batch),'shown_nodes':len(visible),'shown_edges':len(ee)})
assert faceted==len(edgepairs);put(V/'facets_index.json',pages)
print('RENDERED_FACETS',len(pages),flush=True)
# Same IDs, same stable within-h order, h5 first; geometry never overlays graph depth.
for key,label in [('train','TRAIN 归一化坐标'),('raw','恢复原始坐标')]:
 arr=pp[key][:,order].T;assert np.allclose(arr.sum(1),1)
 fig,ax=plt.subplots(figsize=(13,56));im=ax.imshow(100*arr,aspect='auto',interpolation='nearest',cmap='viridis',vmin=0,vmax=100);ax.set_xticks(range(14),layers);ax.set_yticks(range(len(order)),[f'h={h[a]} | {a}' for a in order],fontsize=6.8);ax.tick_params(axis='x',top=True,labeltop=True);ax.set_xlabel('模型层号（一基）：2、4、…、28');ax.set_ylabel('统计图层级 h 与稳定 Feature ID；与连接图相同的节点及行内顺序')
 cuts=np.cumsum([sc[d] for d in range(5,-1,-1)])
 for cut in cuts[:-1]:ax.axhline(cut-.5,color='white',lw=1.8)
 ax.set_title(f'同批 {len(order)} 个 Feature × 14 模型层｜跨层解码幅度占比 p\n{label}；按 h=5 至 h=0 分组；每行合计 100%；不是激活频率',pad=20)
 fig.subplots_adjust(left=.17,right=.85,top=.975,bottom=.025);cax=fig.add_axes([.89,.83,.025,.12]);fig.colorbar(im,cax=cax,label='跨层解码幅度占比 p（%）');save(fig,f'figure2_expanded_decoder_{key}',180)
# Compact group facets for on-screen reading; source CSV is the exact same data.
fig,axs=plt.subplots(2,3,figsize=(23,24))
for ax,depth in zip(axs.ravel(),range(5,-1,-1)):
 aa=groups[depth];arr=pp['train'][:,aa].T;im=ax.imshow(100*arr,aspect='auto',interpolation='nearest',cmap='viridis',vmin=0,vmax=100);ax.set_xticks(range(14),layers,fontsize=8);ax.set_yticks(range(len(aa)),[str(a) for a in aa],fontsize=7 if len(aa)<80 else 6);ax.set_xlabel('模型层号（一基）');ax.set_title(f'h={depth}；展示 n={len(aa)} / 全Q n={ns[depth]:,}');ax.set_ylabel('Feature ID')
fig.suptitle('同批节点的跨层解码幅度占比 p｜按统计图层级分面，仅用于阅读\nTRAIN 归一化坐标；共享 0–100% 色标；各面板高度相同不表示样本数相同',y=.995);fig.subplots_adjust(top=.95,bottom=.05,left=.06,right=.92,wspace=.28,hspace=.16);cax=fig.add_axes([.94,.15,.012,.7]);fig.colorbar(im,cax=cax,label='跨层解码幅度占比 p（%）');save(fig,'figure2_expanded_decoder_facets',180)
# Final checks: input identities and exact edge set preserved.
for z in source:assert sha(z['path'])==z['sha256']
assert set(edgepairs)=={(a,int(u)) for a in selected for u in out[a] if u in selectedset}
assert set(selected)=={int(r['feature']) for r in noderows}
checks={'all_primary_hashes_unchanged':True,'full_Q_counts_exact':ns,'selected_counts':sc,'original_h_preserved':True,'all_induced_saved_direct_edges':True,'all_old_30_nodes_and101_edges_retained':oldnodes.issubset(selectedset) and oldpairs.issubset(set(edgepairs)),'skipping_edges':sum(h[a]-h[u]>1 for a,u in edgepairs),'full_h4_branches':63,'selected_frequency_strata_coverage':'tables/display_frequency_coverage.csv','facets_each_edge_once':faceted==len(edgepairs),'same_ids_heatmap':True,'p_row_sum1':True,'selected_view_isolated_nodes':sum(shown_in[a]+shown_out[a]==0 for a in selected),'omitted_in_neighbor_incidences':sum(int(r['omitted_in_neighbors']) for r in noderows),'omitted_out_neighbor_incidences':sum(int(r['omitted_out_neighbors']) for r in noderows),'no_training_inference_count_or_graph_rebuild':True}
receipt={'status':'RENDERED_PENDING_VISUAL_REVIEW','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':source,'selection_rule_sha256':sha(V/'selection_rules_frozen.json'),'selection_sha256':sha(V/'selection_frozen_before_p.json'),'nodes':len(selected),'edges':len(edgepairs),'figures':figuremeta,'facet_pages':len(pages),'checks':checks,'CPU_seconds_wall':time.monotonic()-start,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'gpu_jobs':0,'cache_scans':0,'no_commit_push':True}
put(V/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2,default=lambda a:a.item() if isinstance(a,np.generic) else a.tolist()),flush=True)
