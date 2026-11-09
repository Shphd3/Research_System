from core import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyArrowPatch
import textwrap
FIG=R/'figures';FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160})

def cases():
 base=np.load(R/'data/base_pairs.npz')['pairs'];records={}
 for k in ['SAE','CC']:
  pk=np.load(R/f'results/matched_{k}.npz');bi=pk['base_indices'];ba=base[bi];mt=np.load(R/f'data/matches_{k}.npz')['matches'][bi];v=pk['values'];mask=(mt[:,1]==1)&(ba[:,8]==0)&(ba[:,9]==0)
  for sid in np.unique(ba[mask,3]):
   z=mask&(ba[:,3]==sid);r=records.setdefault(int(sid),dict(sid=int(sid),doc=SENTS[sid]['doc'],domain=SENTS[sid]['domain'],source_hash=DOCS[SENTS[sid]['doc']]['source_text_sha256'],start=SENTS[sid]['start']))
   for mi in range(1 if k=='SAE' else 3):
    ok=z&np.isfinite(v[:,4,mi,:]).all(1);real=v[ok,4,mi,0];ctrl=v[ok,4,mi,1]
    r[k+'_'+METRICS[mi]]=dict(real=float(real.mean()) if len(real) else None,control=float(ctrl.mean()) if len(ctrl) else None,delta=float((real-ctrl).mean()) if len(ctrl) else None,pairs=int(len(real)))
 allr=list(records.values());dump(R/'results/all_case_scores.json',allr)
 def score(r,k):return r.get(k,{}).get('delta')
 math=sorted([r for r in allr if r['domain']=='math' and score(r,'SAE_identity') is not None],key=lambda r:(-score(r,'SAE_identity'),r['source_hash'],r['start']))[0]
 bio=sorted([r for r in allr if r['domain']=='biology' and score(r,'CC_forward') is not None],key=lambda r:(-score(r,'CC_forward'),r['source_hash'],r['start']))[0]
 eligible=[r for r in allr if r['doc'] not in [math['doc'],bio['doc']] and all(score(r,'CC_'+m) is not None for m in ['identity','forward','reverse'])]
 counter=sorted(eligible,key=lambda r:(max(score(r,'CC_'+m) for m in ['identity','forward','reverse']),r['source_hash'],r['start']))[0]
 selected=[]
 for name,r in [('math',math),('biology',bio),('counterexample',counter)]:
  s=SENTS[r['sid']];r=dict(r);r.update(name=name,text=s['text'],seq_id=s['seq_id'],url=DOCS[s['doc']]['url'],positions=s['positions']);r['label']='selected illustration' if name!='counterexample' else ('nonpositive excess case' if max(score(r,'CC_'+m) for m in ['identity','forward','reverse'])<=0 else 'weakest available; no nonpositive counterexample')
  r['features']={}
  fig,axes=plt.subplots(2,1,figsize=(max(13,.24*len(s['positions'])),12),layout='constrained')
  for ax,k in zip(axes,['SAE','CC']):
   x=np.load(SRC/'forward/documents'/f"{s['seq_id']}.npz");ptr=x[k+'_ptr'];ids=x[k+'_ids'];zs=x[k+'_z'];F=30000 if k=='SAE' else 16384;mat=np.zeros((F,len(s['positions'])));act={}
   for col,pos in enumerate(s['positions']):mat[ids[ptr[pos]:ptr[pos+1]],col]=zs[ptr[pos]:ptr[pos+1]]
   union=np.flatnonzero((mat>0).any(1));selected_features=sorted(union,key=lambda f:(-int((mat[f]>0).sum()),-float(mat[f].sum()),int(f)))[:24];selected_features=np.array(selected_features,int)
   omitted=(mat>0).sum(0)-(mat[selected_features]>0).sum(0)
   r['features'][k]=dict(selected=selected_features.tolist(),union=len(union),omitted=len(union)-len(selected_features),omitted_active_per_token=omitted.tolist(),total_active_per_token=(mat>0).sum(0).tolist(),active_positions={str(f):[int(s['positions'][p]) for p in np.flatnonzero(mat[f]>0)] for f in selected_features})
   ax.imshow(mat[selected_features]>0,aspect='auto',interpolation='nearest',cmap=ListedColormap(['#f1f5f9','#155e75']),vmin=0,vmax=1)
   ax.set_yticks(np.arange(len(selected_features)),[f'f{f}' for f in selected_features],fontsize=8)
   labels=[str(pos)+': '+DOCS[s['doc']]['token_surfaces'][pos].replace('\n','↵').replace(' ','·') for pos in s['positions']]
   ax.set_xticks(np.arange(len(labels)),labels,rotation=90,fontsize=8);ax.set_xlabel('All sentence tokens in original order (cached position: decoded token)')
   ax.set_title(f'{k}: active / inactive; shown {len(selected_features)} of {len(union)} features; omitted {len(union)-len(selected_features)}',loc='left')
  display_name='weakest available (not a triple-negative counterexample)' if name=='counterexample' else name
  fig.suptitle(f'Figure 1 | {display_name}: {s["seq_id"]}, sentence {s["sid"]}\n'+textwrap.fill(s['text'].replace('\n',' '),125),fontsize=12)
  fig.savefig(FIG/f'figure1_{name}.png');plt.close(fig);selected.append(r)
 dump(R/'results/selected_cases.json',selected);return selected

def curves(typ):
 cs=pd.read_csv(R/'results/all_cells.csv');cs=cs[(cs.tier==1)&(cs.pair_class=='lexical')&(cs.same_id==0)]
 panels=[('SAE','math','identity'),('SAE','biology','identity'),('CC','math','identity'),('CC','biology','identity')] if typ==2 else [('CC','math','forward'),('CC','math','reverse'),('CC','biology','forward'),('CC','biology','reverse')]
 fig=plt.figure(figsize=(15,17),layout='constrained');outer=fig.add_gridspec(4,3)
 for row,(k,dom,m) in enumerate(panels):
  for col,g in enumerate(GROUPS[:3]):
   axes=outer[row,col].subgridspec(2,1,height_ratios=[1.5,1]);a=fig.add_subplot(axes[0]);b=fig.add_subplot(axes[1]);df=cs[(cs.dictionary==k)&(cs.domain==dom)&(cs.metric==m)&(cs.frequency==g)].set_index('distance_bin').reindex(range(7));xx=np.arange(7)
   for nm,color,label in [('real','#0e7490','Same sentence'),('control','#d97706','Matched other document')]:
    a.plot(xx,100*df[nm],'.-',color=color,label=label,ms=6)
    a.fill_between(xx,100*df[nm+'_point_lo'],100*df[nm+'_point_hi'],color=color,alpha=.15)
   a.set_ylim(-2,102);a.set_ylabel('Coverage (%)' if typ==3 else 'Persistence (%)');a.set_xticks(xx,[]);a.set_title(f'{k} | {dom} | {g}'+(f' | {m}' if typ==3 else ''),loc='left',fontsize=10);a.grid(alpha=.15)
   b.axhline(0,color='#64748b',lw=1);b.plot(xx,100*df.delta,'.-',color='#6d28d9',ms=6)
   b.fill_between(xx,100*df.simultaneous_lo,100*df.simultaneous_hi,color='#6d28d9',alpha=.16)
   b.set_xticks(xx,DIST,fontsize=8);b.set_ylabel('Real - control (pp)',fontsize=9);b.grid(alpha=.15)
   txt='Blocks: '+', '.join('-' if pd.isna(n) else str(int(n)) for n in df.blocks)
   b.text(0,-.34,txt,transform=b.transAxes,fontsize=8)
   if row==0 and col==0:a.legend(fontsize=8,loc='upper right')
 title='Same-coordinate persistence (H1)' if typ==2 else 'Old-graph association among lost source coordinates (H2)'
 fig.suptitle(f'Figure {typ} | {title}\nLexical, different token IDs; exact target-ID controls. Top bands: pointwise 95%; bottom bands: simultaneous 95% across primary family.\nDistance = j - i in tokens (categorical bins). Missing bands mean unavailable uncertainty. Matching applies to a restricted population.'+('\nSAE graph branch unavailable: historical activation interface not qualified.' if typ==3 else ''),fontsize=11)
 fig.savefig(FIG/f'figure{typ}_distance.png');plt.close(fig)
 cs.to_csv(FIG/f'figure{typ}_plot_source.csv',index=False)

def diagram(case):
 s=SENTS[case['sid']];features=case['features']['CC']['selected'];pos=s['positions'];x=np.load(SRC/'forward/documents'/f"{s['seq_id']}.npz");ptr=x['CC_ptr'];ids=x['CC_ids'];A={p:set(ids[ptr[p]:ptr[p+1]].tolist()) for p in pos};a,b=graph();E=set(zip(a.tolist(),b.tolist()));found=[]
 for i in pos:
  for j in pos:
   if j<=i:continue
   for f in sorted((A[i]-A[j])&set(features)):
    for g in sorted(A[j]&set(features)):
     if (f,g) in E:found.append((i,j,f,g,'forward'))
     if (g,f) in E:found.append((i,j,f,g,'reverse'))
 edges=found[:8];used=sorted(set([e[2] for e in edges]+[e[3] for e in edges]));fig,ax=plt.subplots(figsize=(max(13,.24*len(pos)),5),layout='constrained')
 for y,f in enumerate(used):
  act=[v for v,p in enumerate(pos) if f in A[p]];ax.scatter(act,[y]*len(act),s=25,color='#155e75',zorder=3)
 for i,j,f,g,dr in edges:
  start=(pos.index(i),used.index(f));end=(pos.index(j),used.index(g))
  if dr=='reverse':start,end=end,start
  ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=11,color='#d97706' if dr=='forward' else '#7c3aed',alpha=.75,connectionstyle='arc3,rad=.10'))
 ax.set_yticks(range(len(used)),['f'+str(f) for f in used]);ax.set_xticks(range(len(pos)),[str(p)+':'+DOCS[s['doc']]['token_surfaces'][p].replace(' ','·').replace('\n','↵') for p in pos],rotation=90,fontsize=8);ax.set_xlim(-1,len(pos));ax.set_ylim(-1,max(1,len(used)));ax.set_xlabel('All tokens; dots are measured positive native CC activations')
 ax.set_title(f'Figure 3 detail | actual old edges in {s["seq_id"]}\nShown first {len(edges)} of {len(found)} qualifying cross-position edge instances among the 24 displayed features.\nArrow = historical same-token asymmetric coactivation, not information flow. Other features are omitted.',loc='left',fontsize=10)
 fig.savefig(FIG/'figure3_sentence_edges.png');plt.close(fig);dump(R/'results/diagram_edges.json',dict(sid=s['sid'],edges=edges,qualifying_displayed_feature_instances=len(found),omitted_instances=len(found)-len(edges),feature_union=case['features']['CC']['union'],features_displayed_in_heatmap=24,diagram_features=used,selection='lexicographic positions/features, first8; source absent at later position; directions separately marked'))
if __name__=='__main__':selected=cases();curves(2);curves(3);diagram(selected[1]);print('Figures rendered')
