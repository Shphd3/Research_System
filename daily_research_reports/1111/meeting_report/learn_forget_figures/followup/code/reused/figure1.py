from lf_common import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threadpoolctl import threadpool_limits

def bigram_and_masks():
 d=codes('EVAL');fb=artifact('A0',2000)['feature_bin'].numpy();idx=d['indices'].numpy();positive=d['values'].numpy()>0;fraction=((fb[idx]<=2)&positive).sum(1)/32;q25,q75=np.quantile(fraction,[.25,.75]);dev=np.load(R4/'data/DEV_tokens.npy',mmap_mode='r');ev=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');V=151936
 dx=np.asarray(dev[:N],dtype=np.int64);dy=np.asarray(dev[1:N+1],dtype=np.int64);unigram=np.bincount(dy,minlength=V);nx=np.bincount(dx,minlength=V);key=dx*V+dy;uk,ct=np.unique(key,return_counts=True);ex=np.asarray(ev[:N],dtype=np.int64);ey=np.asarray(ev[1:N+1],dtype=np.int64);ek=ex*V+ey;ix=np.searchsorted(uk,ek);hit=(ix<len(uk))&(uk[np.minimum(ix,len(uk)-1)]==ek);counts=np.zeros(N,np.float64);counts[hit]=ct[ix[hit]];p0=(unigram[ey]+.1)/(N+.1*V);prob=(counts+10*p0)/(nx[ex]+10)
 masks={'overall':np.ones(N,bool),'rare_high':fraction>=q75,'rare_low':fraction<=q25,'bigram_recognition':prob>=.5,'needs_context':prob<.5}
 np.savez(R/'data/strata.npz',rare_fraction=fraction,bigram_p=prob,**masks);dump(R/'evidence/strata.json',dict(q25=float(q25),q75=float(q75),counts={k:int(v.sum()) for k,v in masks.items()},rare_high_low_overlap=int((masks['rare_high']&masks['rare_low']).sum()),bigram='DEV only;(nxy+10*smoothedunigram)/(nx+10);unigramadditive0.1',fit_positions=N));return masks
def bootstrap_weights(D):
 rng=np.random.default_rng(20261111);return rng.multinomial(D,np.full(D,1/D),size=2000).astype(np.float64)
def stat_ci(num,den,W):
 value=num.sum()/max(den.sum(),1);bs=(W@num)/np.maximum(W@den,1);return float(value),np.quantile(bs,[.025,.975]),bs
def concentration():
 F,_=features('EVAL');ct=np.asarray(F.sum(0)).ravel();p=artifact('A0',2000)['p_dev'].numpy();rows=[]
 for row in json.load(open(R/'evidence/checkpoint_inventory.json')):
  if row['model']!='MoE':continue
  path=R/f'positions/MoE_{row["tokens"]:012d}.npz'
  if not path.exists():continue
  sel=np.load(path)['sel'];mm=[];me=[]
  for l in range(8):
   ids=sel[l];Y=np.zeros((N,8),np.float32);Y[np.arange(N)[:,None],ids]=1;u=Y.mean(0)/2;q=np.asarray(F.T@Y)/np.maximum(2*ct[:,None],1);M=2*(q**3/np.maximum(u[None,:],1e-30)).sum(1);me.append(M);mm.append(M*(ct/N)/np.maximum(p,1e-30))
  rows.append(dict(tokens=row['tokens'],M_DEV_median=float(np.nanmedian(np.mean(mm,0))),M_EVAL_median=float(np.nanmedian(np.mean(me,0)))))
 table(pd.DataFrame(rows),'baseline_concentration','ExactR04primaryfrequency denominator andEVAL variant, averaged across8layers peratom before atommedian.');return rows
def main():
 assert (R/'evidence/forward_complete.json').exists()
 masks=bigram_and_masks();tok=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');dd=np.cumsum((tok[:N]==151645).astype(np.int32));D=int(dd.max())+1;W=bootstrap_weights(D);inv=json.load(open(R/'evidence/checkpoint_inventory.json'));times=sorted(set(x['tokens'] for x in inv if x['purpose']=='trajectory'));rows=[];gaps=[];identity_errors=[];nll=[]
 loss={a:{t:np.load(R/f'positions/{a}_{t:012d}.npz')['loss'].astype(np.float64) for t in times} for a in ['Dense','MoE']}
 for t in times:
  dx=loss['Dense'][t]-loss['MoE'][t];num=np.bincount(dd,weights=dx,minlength=D);den=np.bincount(dd,minlength=D);value,ci,_=stat_ci(num,den,W);nll.append(dict(tokens=t,Dense_NLL=json.load(open(R/f'evidence/forward_Dense_{t:012d}.json'))['NLL'],MoE_NLL=json.load(open(R/f'evidence/forward_MoE_{t:012d}.json'))['NLL'],paired_fp16_difference=value,ci95_low=ci[0],ci95_high=ci[1]))
 table(pd.DataFrame(nll),'baseline_NLL_document_CI','Paired2000document bootstrap; intervals reflect EVAL sampling only.')
 latest=[x for x in inv if x['model']=='Dense' and x['tokens']>times[-1]]
 refs=[('MoE33B',np.load(R/'positions/MoE_033000000000.npz')['loss']),('Dense_latest10B',loss['Dense'][times[-1]])]
 if latest:
  latest=max(latest,key=lambda x:x['tokens']);refs.insert(1,('Dense_latest_available',np.load(R/f'positions/Dense_{latest["tokens"]:012d}.npz')['loss']))
 for reference,ref in refs:
  learnable=ref<=np.log(2)
  for stratum,base_mask in masks.items():
   mask=learnable&base_mask;den=np.bincount(dd,weights=mask.astype(float),minlength=D);states={a:np.zeros(N,bool) for a in ['Dense','MoE']};stats={};boots={};sumlearn={a:np.zeros(D) for a in states};sumforget={a:np.zeros(D) for a in states}
   for ti,t in enumerate(times):
    for a in states:
     prev=states[a].copy();ll=loss[a][t];states[a]=np.where(ll<=np.log(2),True,np.where(ll>=2*np.log(2),False,prev));known=np.bincount(dd,weights=(states[a]&mask).astype(float),minlength=D);K,kci,kboot=stat_ci(known,den,W)
     learned=np.bincount(dd,weights=((~prev)&states[a]&mask).astype(float),minlength=D);forgot=np.bincount(dd,weights=(prev&(~states[a])&mask).astype(float),minlength=D);old=np.bincount(dd,weights=(prev&mask).astype(float),minlength=D)
     newc=float(learned.sum()/max(den.sum(),1));fc=float(forgot.sum()/max(den.sum(),1));ap=float(learned.sum()/max((den-old).sum(),1));fp=float(forgot.sum()/max(old.sum(),1));err=abs(K-(float(old.sum()/max(den.sum(),1))+newc-fc));identity_errors.append(err)
     if ti>0:sumlearn[a]+=learned;sumforget[a]+=forgot
     stats[a]=(K,known);boots[a]=kboot
     rows.append(dict(reference=reference,stratum=stratum,model=a,tokens=t,previous_tokens=None if ti==0 else times[ti-1],positions=int(mask.sum()),K=K,K_ci95_low=kci[0],K_ci95_high=kci[1],a=ap,f=fp,new_learned_contribution=newc,forgotten_contribution=fc,identity_error=err,initial_point=ti==0))
    diff=stats['MoE'][0]-stats['Dense'][0];db=boots['MoE']-boots['Dense'];ci=np.quantile(db,[.025,.975])
    if ti==0:initial_gap=diff;initial_bs=db.copy()
    newnum=sumlearn['MoE']-sumlearn['Dense'];forgetnum=sumforget['Dense']-sumforget['MoE'];new,nci,nb=stat_ci(newnum,den,W);less,fci,ffb=stat_ci(forgetnum,den,W);assert abs(diff-initial_gap-new-less)<1e-12
    if ci[0]<=0:rule='分不出（MoE掌握率优势区间跨0或非正）'
    elif nci[0]<=0 and fci[0]<=0:rule='分不出（两项区间均跨0或非正）'
    elif diff-initial_gap<=0:rule='分不出（后续增长差非正）'
    elif less/(diff-initial_gap)>=.6 and fci[0]>0:rule='主要来自忘得少'
    elif new/(diff-initial_gap)>=.6 and nci[0]>0:rule='主要来自学得快'
    else:rule='两者都有'
    gaps.append(dict(reference=reference,stratum=stratum,tokens=t,K_MoE_minus_Dense=diff,gap_ci95_low=ci[0],gap_ci95_high=ci[1],initial_gap=initial_gap,cumulative_new_learned_difference=new,new_ci95_low=nci[0],new_ci95_high=nci[1],cumulative_less_forgotten=less,forgot_ci95_low=fci[0],forgot_ci95_high=fci[1],new_share_of_growth_gap=new/(diff-initial_gap) if diff!=initial_gap else np.nan,less_forgotten_share=less/(diff-initial_gap) if diff!=initial_gap else np.nan,rule_result=rule))
 table(pd.DataFrame(rows),'fig1_mastery_transitions','Hysteresis:<=ln2known,>=2ln2unknown,otherwiseprevious; initialband defaultsunknown. Rates conditional; contributions normalized by learnable stratum positions.')
 table(pd.DataFrame(gaps),'fig1_gap_decomposition','Kgap=initialgap+cumulative(newMoE-newDense)+cumulative(forgotDense-forgotMoE). Positive contributions favorMoE. Same document bootstrap across models.')
 d=pd.DataFrame(rows)
 for reference,_ in refs:
  fig,axs=plt.subplots(2,5,figsize=(20,7))
  for col,stratum in enumerate(masks):
   for a,c in [('Dense','#d97720'),('MoE','#2471a3')]:
    z=d[(d.reference==reference)&(d.stratum==stratum)&(d.model==a)];axs[0,col].plot(z.tokens/1e9,z.K,'o-',label=a,color=c);axs[0,col].fill_between(z.tokens.to_numpy()/1e9,z.K_ci95_low.to_numpy(),z.K_ci95_high.to_numpy(),color=c,alpha=.15);z=z[~z.initial_point];xx=np.arange(len(z));offset=-.19 if a=='Dense' else .19;axs[1,col].bar(xx+offset,z.new_learned_contribution,.35,color=c,label=a+'new');axs[1,col].bar(xx+offset,-z.forgotten_contribution,.35,color=c,alpha=.4,hatch='//',label=a+'forgot');axs[1,col].set_xticks(xx,[f'{v/1e9:g}' for v in z.tokens])
   axs[0,col].set(title=stratum,xlabel='billion training tokens',ylabel='mastery K');axs[1,col].set(xlabel='interval ending token(B)',ylabel='learned(+) /forgotten(-) contribution');axs[0,col].legend(fontsize=7);axs[1,col].legend(fontsize=6)
   for ax in axs[:,col]:ax.grid(alpha=.2)
  savefig(fig,'图1_'+reference,'上排可学位置的迟滞掌握率，阴影文档区间；下排为各区间新学会正项／忘掉负项。首列总体，后四列为独立分层，不是交叉分组。')
 concentration();dump(R/'evidence/fig1_complete.json',dict(identity_max_abs_error=max(identity_errors),checkpoints_per_model=len(times),references=len(refs),latest_Dense_reference_tokens=None if not latest else latest['tokens'],document_resamples=2000,training_updates=0));event('图1','掌握率恒等式、四分层、文档区间和Dense参照敏感性完成',identity_error=max(identity_errors))
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
