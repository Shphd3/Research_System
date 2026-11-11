from common import *
import torch,pandas as pd
from scipy import sparse
from scipy.stats import spearmanr
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cache_forward import PAIRS,PAIRMAP

def feature_matrix():
 d=torch.load(R4/'data/EVAL_codes.pt',map_location='cpu',weights_only=False);ii=d['indices'].numpy().astype(np.int32);vv=d['values'].numpy();good=vv>0
 # Same binary positive teacher Top32 support; duplicate feature indices do not occur.
 rr=np.broadcast_to(np.arange(N,dtype=np.int32)[:,None],ii.shape)[good];cc=ii[good]
 return sparse.csr_matrix((np.ones(len(cc),np.float32),(rr,cc)),shape=(N,30000))
def mcalc(F,weights,p,k=2,weighted=False):
 ct=np.asarray(F.sum(0)).ravel().astype(np.float64);J=np.asarray(F.T@weights,dtype=np.float64);ec=weights.sum(0);c=J/np.maximum(ct[:,None],1);pur=J/np.maximum(ec[None,:],1);m=(c*c*pur/np.maximum(p[:,None],1e-30)).sum(1)*(2 if weighted else 1/k);m[ct==0]=np.nan;return m

def bvalues(arm):
 st=torch.load(model_path(arm,2000),map_location='cpu',mmap=True,weights_only=False);return np.stack([st['model'][f'blocks.{l}.moe.load_bias'].numpy() for l in range(8)])
def pair_selection(s,b):return torch.topk(torch.from_numpy(np.asarray(s).copy())+torch.from_numpy(np.array(b)),2,dim=1).indices.numpy()
def hardweights(sel,k=2):
 w=np.zeros((N,8),np.float64);np.put_along_axis(w,sel[:,:k],1,axis=1);return w

def check4():
 tic=time.monotonic();F=feature_matrix();a0=torch.load(erows('A0')[2000]['feature_artifact'],weights_only=False);p=a0['p_dev'].numpy();fb=a0['feature_bin'].numpy();frozen=torch.load(R4/'data/frozen.pt',map_location='cpu',weights_only=False);tau=float(frozen['distill_tau']);rows=[];mrows=[];combo=[];decisions=[];binvalid=p>0
 for arm in ['A5','A1']:
  scores=np.load(R/f'data/EVAL_scores_{arm}.npy',mmap_mode='r');bias=bvalues(arm);fixed_col=0 if arm=='A5' else 1;s0=np.array(PAIRS)[np.load(R/'data/EVAL_labels_fixed.npy')[:,fixed_col]];ref=PAIRMAP[s0[:,0],s0[:,1]];m0=mcalc(F,hardweights(s0),p);variants={'b0_top2':m0};allms=[]
  for l,b in enumerate(bias):
   sel=pair_selection(scores,b);ids=PAIRMAP[sel[:,0],sel[:,1]];br=float(np.ptp(b));sorted_scores=np.sort(scores,axis=1);gap=sorted_scores[:,-2]-sorted_scores[:,-3];ratio=gap/br if br>0 else np.full(N,np.nan)
   counts=np.bincount(ids,minlength=28);freq=counts/N;H=float(-(freq[freq>0]*np.log(freq[freq>0])).sum());allms.append(mcalc(F,hardweights(sel),p))
   rows.append(dict(arm=arm,layer=l,bias_range=br,bias_changes_top2_fraction=float((ref!=ids).mean()),score_gap_q10=float(np.quantile(gap,.1)),score_gap_median=float(np.median(gap)),score_gap_q90=float(np.quantile(gap,.9)),gap_over_bias_q10=float(np.nanquantile(ratio,.1)),gap_over_bias_median=float(np.nanmedian(ratio)),gap_over_bias_q90=float(np.nanquantile(ratio,.9)),effective_combinations=float(np.exp(H))))
   for k,(e1,e2) in enumerate(PAIRS):combo.append(dict(arm=arm,layer=l,expert1=e1,expert2=e2,positions=int(counts[k]),fraction=freq[k]))
  variants['actual_top2']=np.mean(allms,0)
  sel=pair_selection(scores,bias[0]);top1=np.argmax(np.asarray(scores)+bias[0],1)[:,None];variants['actual_top1']=mcalc(F,hardweights(top1,1),p,k=1)
  top10=np.argmax(scores,1)[:,None];variants['b0_top1']=mcalc(F,hardweights(top10,1),p,k=1)
  sp=np.take_along_axis(scores,sel,1)/tau;ww=np.exp(sp-sp.max(1,keepdims=True));ww/=ww.sum(1,keepdims=True);W=np.zeros((N,8),np.float64);np.put_along_axis(W,sel,ww,1);variants['softmax_score_weighted_D2']=mcalc(F,W,p,weighted=True)
  for name,m in variants.items():
   for k in range(-1,10):
    z=binvalid&np.isfinite(m)&((fb==k) if k>=0 else True);mrows.append(dict(arm=arm,variant=name,band='overall' if k<0 else f'bin{k}',median=float(np.median(m[z])),atoms=int(z.sum()),tau=tau if 'weighted' in name else np.nan))
  delta=float(abs(np.nanmedian(variants['actual_top2'])-np.nanmedian(m0))/np.nanmedian(m0));decisions.append(dict(arm=arm,b0_median=float(np.nanmedian(m0)),actual_median=float(np.nanmedian(variants['actual_top2'])),relative_change=delta))
  # Histograms retain all positions in modest bins for plotting/source.
  hist,edges=np.histogram(ratio[np.isfinite(ratio)],bins=np.r_[-np.inf,np.linspace(0,5,101),np.inf]);table(pd.DataFrame({'left':edges[:-1],'right':edges[1:],'positions':hist}),f'check4_gap_hist_{arm}')
 table(pd.DataFrame(rows),'check4_score_bias','固定FP32离线teacher分数；bias为实际2000状态。实际R04训练时teacher为bf16，offline与原训练硬映射可有微差；不是修改R04。')
 table(pd.DataFrame(combo),'check4_combinations');table(pd.DataFrame(mrows),'check4_concentration_variants','同R04 D2：top1同时给b0／actual；weighted在实际Top2中softmax(s/tau)，tau沿用冻结distill_tau。')
 dec=pd.DataFrame(decisions);rule=bool(dec.set_index('arm').relative_change['A5']<.1 and dec.set_index('arm').relative_change['A1']>.1);table(dec,'check4_bias_rule','规则：A5<10%且A1>10%则单列A1受bias干扰的证据；不独立量化其NLL贡献。')
 # Missing A5 versus A0 Spearman, all atoms and each frozen frequency band.
 rr=[]
 for step in [500,1000,1500,2000]:
  x=torch.load(erows('A5')[step]['feature_artifact'],map_location='cpu',weights_only=False);y=torch.load(erows('A0')[step]['feature_artifact'],map_location='cpu',weights_only=False);mx=x['concentration'].numpy().mean(0);my=y['concentration'].numpy().mean(0);G=y['feature_nll'].numpy()-x['feature_nll'].numpy();delta=np.log(np.maximum(mx,1e-30))-np.log(np.maximum(my,1e-30));base=(mx>0)&(my>0)&np.isfinite(G)
  for k in range(-1,10):
   z=base&((fb==k) if k>=0 else True);rho=float(spearmanr(G[z],delta[z]).statistic);rr.append(dict(step=step,band='overall' if k<0 else f'bin{k}',atoms=int(z.sum()),rho_gain_delta_logM=rho))
 table(pd.DataFrame(rr),'check4_A5_A0_spearman')
 # Recompute correct global atom IDs and enrichment; do not reuse R04 subgroup-local top-ID labels.
 g=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);groups=g['group'].numpy();d=torch.load(R4/'data/DEV_codes.pt',map_location='cpu',weights_only=False);ii=d['indices'].numpy().astype(np.int32);vv=d['values'].numpy();s=np.load(R/'data/DEV_scores_A5.npy',mmap_mode='r');ss=np.array(PAIRS)[np.load(R/'data/DEV_labels_fixed.npy')[:,0]];W=hardweights(ss);good=vv>0;flat=ii[good];rrr=np.broadcast_to(np.arange(N,dtype=np.int32)[:,None],ii.shape)[good];FD=sparse.csr_matrix((np.ones(len(flat),np.float32),(rrr,flat)),shape=(N,30000));ct=np.asarray(FD.sum(0)).ravel();J=FD.T@W;mass=np.bincount(flat,weights=vv[good],minlength=30000);lift=(J/np.maximum(ct[:,None],1))/(W.mean(0)[None,:]);grow=[];toprows=[]
 for e in range(8):
  z=groups==e;pp=p[z];grow.append(dict(group=e,atoms=int(z.sum()),token_mass_fraction=float(mass[z].sum()/mass.sum()),p_q10=float(np.quantile(pp,.1)),p_median=float(np.median(pp)),p_q90=float(np.quantile(pp,.9)),**{f'bin{k}_atoms':int((z&(fb==k)).sum()) for k in range(10)}))
  candidates=np.flatnonzero(z&(ct>=20));top=candidates[np.argsort(lift[candidates,e])[-10:][::-1]]
  for j in top:toprows.append(dict(group=e,atom=int(j),count=int(ct[j]),enrichment_lift=float(lift[j,e]),p_dev=float(p[j])))
 table(pd.DataFrame(grow),'check4_atom_groups');table(pd.DataFrame(toprows),'check4_group_top_atoms')
 # Context decoding at three highest DEV activations for each selected atom.
 sys.path.insert(0,str(R4/'analysis_deps'));from tokenizers import Tokenizer
 tok=Tokenizer.from_file('/data/share/Qwen3-0.6B-Base/tokenizer.json');tt=tokens('DEV');contexts=[]
 for row in toprows:
  j=row['atom'];pos,slot=np.nonzero((ii==j)&good);vals=vv[pos,slot];take=np.argsort(vals)[-3:][::-1]
  for idx in take:
   q=int(pos[idx]);lo=max(q-q%2048,q-20);hi=min(q-q%2048+2048,q+21);text=tok.decode(list(map(int,tt[lo:q])))+'⟦'+tok.decode([int(tt[q])])+'⟧'+tok.decode(list(map(int,tt[q+1:hi])));contexts.append(dict(**row,position=q,activation=float(vals[idx]),text=text))
 table(pd.DataFrame(contexts),'check4_group_contexts','每个组富集最高10个全局atom ID，各给DEV激活最高3例，窗口不跨2048上下文；富集定义见协议。')
 fig,axs=plt.subplots(1,2,figsize=(12,4))
 for a in ['A5','A1']:
  dd=pd.DataFrame(combo);z=dd[(dd.arm==a)&(dd.layer==0)];axs[0].plot(range(28),z.fraction,'o-',label=a);h=pd.read_csv(R/f'results/check4_gap_hist_{a}.csv');axs[1].plot(h.left.iloc[1:-1],h.positions.iloc[1:-1]/N,label=a)
 axs[0].set_xlabel('unordered expert pair (lexicographic)');axs[0].set_ylabel('position fraction');axs[1].set_xlabel('(score2-score3)/bias range');axs[1].set_ylabel('histogram position fraction')
 for ax in axs:ax.legend();ax.grid(alpha=.2)
 fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(R/f'results/check4_score_combinations.{ext}',dpi=160)
 plt.close(fig)
 dump(R/'evidence/check4_complete.json',dict(rule_bias_interference=rule,rows=decisions,gpu_seconds=0,cpu_seconds=time.monotonic()-tic));event('4',f'A5/A1的bias相对集中度变化为{decisions[0]["relative_change"]:.2%}/{decisions[1]["relative_change"]:.2%}，原10%规则'+('触发' if rule else '未触发')+'；分数尺度、组合多样性和bias须单列。',0)

def check5():
 rows=[];allstats=[]
 for arm in ['A6','A0']:
  d=np.load(R/f'data/route_{arm}_2000_EVAL.npy',mmap_mode='r');a=torch.load(erows(arm)[2000]['feature_artifact'],map_location='cpu',weights_only=False);current=np.load(position(arm,2000))['sel'];prior=np.load(position(arm,1000))['sel'];same=(np.sort(current,-1)==np.sort(prior,-1)).all(-1);m=erows(arm)
  root=R4 if arm=='A6' else R3;metrics={x['optimizer_step']:x for x in map(json.loads,(root/f'runs/{arm}/metrics.jsonl').read_text().splitlines())};raw=metrics[2000]['layers']
  collapsed=[]
  for l in range(8):
   c=max(raw[l]['raw_probability_mean'])>.995;collapsed.append(c);v=np.asarray(d[l],np.float32);rows.append(dict(arm=arm,layer=l,collapsed_from_R04=bool(c),max_gate_q10=float(np.quantile(v[:,0],.1)),max_gate_median=float(np.median(v[:,0])),max_gate_q90=float(np.quantile(v[:,0],.9)),selected_raw_mass_q10=float(np.quantile(v[:,1],.1)),selected_raw_mass_median=float(np.median(v[:,1])),selected_raw_mass_q90=float(np.quantile(v[:,1],.9)),bias_changes_top2=float(v[:,2].mean()),hard_M_median=float(np.nanmedian(a['concentration'][l].numpy())),flip_1000_2000=float((~same[l]).mean()),gate_degenerate=float(np.median(v[:,0]))>=.95))
  for name,ls in [('all',list(range(8))),('collapsed6',[1,3,4,5,6,7]),('uncollapsed2',[0,2])]:
   if not ls:continue
   vals=np.asarray(d[ls],np.float32);allstats.append(dict(arm=arm,group=name,layers=','.join(map(str,ls)),layer_count=len(ls),max_gate_median=float(np.median(vals[:,:,0])),bias_changes_top2=float(vals[:,:,2].mean()),selected_raw_mass_median=float(np.median(vals[:,:,1])),hard_M_median=float(np.nanmedian(np.nanmean(a['concentration'][ls].numpy(),axis=0))),flip_1000_2000=float((~same[ls]).mean()),all_layer_bias_above80=all(float(np.asarray(d[l,:,2],np.float32).mean())>.8 for l in ls),all_layer_gate_median_above95=all(float(np.median(np.asarray(d[l,:,0],np.float32)))>=.95 for l in ls)))
 table(pd.DataFrame(rows),'check5_layer_gates');table(pd.DataFrame(allstats),'check5_layer_groups','gate退化预定义median(maxgate)>=0.95，bias影响>0.80；collapse按原训练step2000的raw marginal max>0.995划分。')
 stats=pd.read_csv(R4/'analysis/out/B3_Mbar_distribution.csv');nl=pd.read_csv(R4/'analysis/out/A1_eval_nll_by_step.csv');fl=pd.read_csv(R4/'analysis/out/C8_matched_1000_2000.csv');df=stats[stats.step==2000][['arm','median']].merge(nl[nl.step==2000][['arm','eval_nll']],on='arm').merge(fl[['arm','position_flip_rate']],on='arm');table(df,'check5_seven_arm_scatter')
 fig,axs=plt.subplots(1,2,figsize=(11,4))
 for q in df.itertuples():
  axs[0].scatter(q.median,q.eval_nll);axs[0].annotate(q.arm,(q.median,q.eval_nll),xytext=(4,4),textcoords='offset points');axs[1].scatter(q.position_flip_rate,q.eval_nll);axs[1].annotate(q.arm,(q.position_flip_rate,q.eval_nll),xytext=(4,4),textcoords='offset points')
 axs[0].set_xlabel('median atom concentration @2000');axs[1].set_xlabel('position route-flip fraction 1000 to2000')
 for ax in axs:ax.set_ylabel('EVAL NLL @2000');ax.grid(alpha=.2)
 fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(R/f'results/check5_scatter.{ext}',dpi=160)
 plt.close(fig)
 forward_gpu=json.load(open(R/'evidence/cache_A6_2000_EVAL.json'))['gpu_seconds'];c=[z for z in allstats if z['arm']=='A6' and z['group']=='collapsed6'][0];rule=bool(c['bias_changes_top2']>.8 and c['max_gate_median']>=.95);dump(R/'evidence/check5_complete.json',dict(rule_soft_hard_bias_driven=rule,collapsed_group=c,gpu_seconds=forward_gpu));event('5',f'A6塌缩层bias影响率{c["bias_changes_top2"]:.2%}，最大gate中位数{c["max_gate_median"]:.6f}；联合判读'+('满足：soft目标推离硬路由，实际bias驱动' if rule else '未同时满足，不强判bias驱动')+'。',forward_gpu)

if __name__=='__main__':
 import argparse;a=argparse.ArgumentParser();a.add_argument('check');x=a.parse_args();torch.set_num_threads(4)
 if x.check=='4':check4()
 else:check5()
