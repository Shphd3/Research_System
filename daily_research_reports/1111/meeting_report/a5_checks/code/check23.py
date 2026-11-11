from common import *
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch

def check2():
 rows=[]
 for metric,grid in [('train_CE',np.arange(50,2001,50)),('EVAL_NLL',np.arange(250,2001,250))]:
  arms={}
  for a in ['A0','A1','A5']:
   if metric=='train_CE':
    root=R4 if a=='A5' else R3;d={x['optimizer_step']:x['lm_loss'] for x in map(json.loads,(root/f'runs/{a}/metrics.jsonl').read_text().splitlines()) if x['optimizer_step']<=2000}
    s=pd.Series(d).sort_index().rolling(50,min_periods=1).mean();arms[a]={'overall':s.loc[grid].to_numpy()}
   else:
    e=erows(a);arms[a]={'overall':np.array([e[s]['lm_loss'] for s in grid]),**{f'bin{k}':np.array([e[s]['bins'][k]['nll'] for s in grid]) for k in range(10)}}
  for a in ['A0','A1']:
   for band,val5 in arms['A5'].items():
    raw=arms[a][band];mono=np.minimum.accumulate(raw)
    for t,loss in zip(grid,val5):
     hit=np.flatnonzero(mono<=loss)
     if not len(hit):tp=np.nan;lead=np.nan;censored=True;lb=2000-int(t)
     else:
      j=hit[0];tp=float(grid[j]) if j==0 else float(grid[j-1]+(mono[j-1]-loss)/(mono[j-1]-mono[j])*(grid[j]-grid[j-1]));lead=tp-t;censored=False;lb=np.nan
     rows.append(dict(metric=metric,comparison=a,band=band,step=int(t),A5_loss=loss,comparison_first_step=tp,lead_steps=lead,right_censored=censored,lead_lower_bound=lb))
 d=pd.DataFrame(rows);table(d,'check2_step_lead','等loss首次达到时间线性插值，比较曲线用累计最小值；2000步内未达到记右删失，下界不是观测领先量。')
 fits=[]
 for keys,z in d.groupby(['metric','comparison','band']):
  q=z[(z.step>=1000)&(~z.right_censored)];full=z[z.step>=1000];slope=zero=np.nan
  if len(q)>=2:
   slope,intercept=np.polyfit(q.step,q.lead_steps,1);zero=-intercept/slope if slope<0 else np.nan
  descending=len(q)>=2 and bool((np.diff(q.lead_steps)<0).all());nondescending=len(q)>=2 and bool((np.diff(q.lead_steps)>=0).all())
  rule='不足：1000–2000存在右删失；只对观测区间描述'
  if len(q)==len(full):rule='持续下降；给线性外推' if descending else '持平或上升，优势缩小不成立' if nondescending else '非单调，无法套用单一趋势分支'
  fits.append(dict(metric=keys[0],comparison=keys[1],band=keys[2],observed_late_points=len(q),late_points=len(full),lead_slope=slope,strictly_descending_observed=descending,zero_step_extrapolation_if_observed_descending=zero if descending else np.nan,rule=rule))
 f=pd.DataFrame(fits);table(f,'check2_lead_trend','OLS为描述性；外推仅对观测持续下降区间输出，2000步右删失使全区间判据不足。')
 for metric in d.metric.unique():
  fig,axs=plt.subplots(1,2,figsize=(12,4))
  for a in ['A0','A1']:
   z=d[(d.metric==metric)&(d.comparison==a)&(d.band=='overall')];v=z[~z.right_censored];c=z[z.right_censored]
   axs[0].plot(v.step,v.lead_steps,'-o',label=f'A5 versus {a}');axs[0].scatter(c.step,c.lead_lower_bound,marker='^',label=f'{a}: lower bound (censored)')
  axs[0].set_ylabel('comparison first reach step minus A5 step');axs[0].legend(fontsize=7)
  z=d[(d.metric==metric)&(d.comparison=='A0')]
  for b in z.band.unique():
   if b=='overall':continue
   q=z[(z.band==b)&(~z.right_censored)];axs[1].plot(q.step,q.lead_steps,'-o',ms=3,label=b)
  axs[1].set_ylabel('A5 lead versus A0 by frequency band');axs[1].legend(fontsize=7,ncol=2)
  for ax in axs:ax.set_xlabel('A5 optimizer step');ax.grid(alpha=.2)
  fig.tight_layout()
  for ext in ['png','pdf']:fig.savefig(R/f'results/check2_{metric}.{ext}',dpi=160)
  plt.close(fig)
 event('2','等loss步数领先已计算；终点比较臂未达到A5端点loss，1000–2000判据须保留右删失，不能仅凭nat差缩小断言追平。',0)

def binweights():
 p=R/'data/EVAL_bin_weights.npy'
 if p.exists():return np.load(p,mmap_mode='r')
 d=torch.load(R4/'data/EVAL_codes.pt',map_location='cpu',weights_only=False);ii=d['indices'].numpy();v=d['values'].numpy()
 f=torch.load(erows('A0')[2000]['feature_artifact'],map_location='cpu',weights_only=False);fb=f['feature_bin'].numpy();w=np.empty((N,10),np.uint8)
 for k in range(10):w[:,k]=((fb[ii]==k)&(v>0)).sum(1).astype(np.uint8)
 np.save(p,w);return w

def check3():
 w=binweights();di=docs('EVAL');D=int(di.max())+1;den=np.stack([np.bincount(di,minlength=D)]+[np.bincount(di,weights=w[:,k],minlength=D) for k in range(10)],1);allnum=[];labels=[]
 for s in [1000,1500,2000]:
  for a,b in [('A5','A0'),('A5','A1'),('A6','A0')]:
   x=np.load(position(a,s))['loss'].astype(np.float64)-np.load(position(b,s))['loss'].astype(np.float64)
   arr=np.stack([np.bincount(di,weights=x,minlength=D)]+[np.bincount(di,weights=x*w[:,k],minlength=D) for k in range(10)],1)
   allnum.append(arr);labels.append((s,a,b))
 num=np.concatenate(allnum,1);den9=np.tile(den,(1,len(labels)));point=num.sum(0)/den9.sum(0);boots=[];rng=np.random.default_rng(SEED)
 for start in range(0,2000,50):
  counts=rng.multinomial(D,np.full(D,1/D),size=min(50,2000-start));boots.append(counts@num/(counts@den9))
 bs=np.concatenate(boots);lo,hi=np.quantile(bs,[.025,.975],axis=0);rows=[]
 for j,(s,a,b) in enumerate(labels):
  for k,band in enumerate(['overall']+[f'bin{k}' for k in range(10)]):
   z=j*11+k;rows.append(dict(step=s,pair=f'{a}-{b}',band=band,paired_difference=point[z],ci95_low=lo[z],ci95_high=hi[z],documents=D,nonempty_documents=int((den[:,0]>0).sum()),bootstrap_samples=2000,position_count=N,original_eval_difference=(erows(a)[s]['lm_loss']-erows(b)[s]['lm_loss']) if k==0 else (erows(a)[s]['bins'][k-1]['nll']-erows(b)[s]['bins'][k-1]['nll'])))
 d=pd.DataFrame(rows);table(d,'check3_document_bootstrap','配对文档块2000次重抽样，百分位95%区间；只反映固定模型的EVAL文档抽样，种子方差Unknown。使用原fp16位置loss，原未量化差另列。')
 np.savez_compressed(R/'data/bootstrap_draw_statistics.npz',draws=bs,point=point,document_denominators=den)
 fig,axs=plt.subplots(1,3,figsize=(14,4),sharey=True)
 for ax,pair in zip(axs,['A5-A0','A5-A1','A6-A0']):
  z=d[(d.pair==pair)&(d.band=='overall')];ax.errorbar(z.step,z.paired_difference,yerr=[z.paired_difference-z.ci95_low,z.ci95_high-z.paired_difference],fmt='o-',capsize=5);ax.axhline(0,color='grey',lw=1);ax.set_title(pair);ax.set_xlabel('optimizer step');ax.grid(alpha=.2)
 axs[0].set_ylabel('paired EVAL NLL difference (nat)');fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(R/f'results/check3_bootstrap.{ext}',dpi=160)
 plt.close(fig)
 z=d[(d.step==2000)&(d.band=='overall')];event('3','2000步配对文档区间：'+ '; '.join(f'{q.pair}={q.paired_difference:+.6f} [{q.ci95_low:+.6f},{q.ci95_high:+.6f}]' for q in z.itertuples())+'；仅评估集抽样，不是种子方差。',0)
 dump(R/'evidence/check23_complete.json',dict(status='COMPLETE',gpu_seconds=0,documents=D))
if __name__=='__main__':
 torch.set_num_threads(4);check2();check3()
