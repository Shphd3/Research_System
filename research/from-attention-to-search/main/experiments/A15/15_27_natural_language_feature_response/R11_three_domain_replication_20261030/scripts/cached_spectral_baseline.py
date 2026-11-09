"""Spectral priority: unchanged R10discriminators vs strict16,NOT physics confirmation."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np
from scipy import sparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter
B=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response');S=B/'R10_domain_member_atlas_20261030';O=B/'R11_three_domain_replication_20261030/cached_spectral_baseline';O.mkdir(parents=True,exist_ok=True);F=O/'figures';F.mkdir(exist_ok=True);W=Path(__file__).resolve().parents[1]
def rows(p):return list(csv.DictReader(p.open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def table(n,rr):
 rr=list(rr)
 with (O/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
f=json.loads((S/'freeze.json').read_text())['sets'];lf=json.loads((S/'presentation_variants/pooled_simple_20261030/freeze.json').read_text())['sets'];groups={'discriminative':{g:np.array(f['main_'+g],int) for g in ['math','biology']},'strict16':{g:np.array(lf['all_cached_strict_'+g],int) for g in ['math','biology']}}
cfg={'revision':'cached-spectral-baseline-v1','scope':'EXPOSED MATH/BIOLOGY CACHES ONLY;not R11physics/independent validation','main_counts':[433,527],'strict_counts':[7,9],'main_freeze_sha256':sha(S/'freeze.json'),'strict_freeze_sha256':sha(S/'presentation_variants/pooled_simple_20261030/freeze.json'),'quantity':'unit block27decoder squared projection;equal members;no z/eigenvalue/norm weighting','basis':'unchanged full1024PC R04pooled60discoverydocs x160;R07SAMEbasis','background':'same A01half-octave hits x5-doc total/max support,eligible inclusive pool,exact sizes/strata,math/bio disjoint per draw','background_draws':1000,'seed':2026103008,'new_model_forwards':0,'training_updates':0}
if (O/'config.json').exists():assert json.loads((O/'config.json').read_text())==cfg
else:dump('config.json',cfg)
pr=np.load(S/'analysis/all_decoder_projection.npz');P=pr['per_pc'];bands=P.reshape(16384,16,64).sum(2);zero=pr['zero_norm'];met=np.load(S/'analysis/discovery_metrics.npz');pool=np.flatnonzero(met['support']&~zero);sm=met['support_math'];sb=met['support_biology'];screen=rows(S/'tables/all_dictionary_screen.csv');hits=np.rint(np.array([float(r['DCLM_feature_occurrence']) for r in screen])*65536).astype(int);keys=list(zip(np.where(hits>0,np.floor(2*np.log2(np.maximum(hits,1))).astype(int),-1),(sm+sb)//5,np.maximum(sm,sb)//5));lookup={k:i for i,k in enumerate(sorted(set(keys)))};stratum=np.array([lookup[k] for k in keys]);rng=np.random.default_rng(cfg['seed']);allstats={};memberrows=[];bandrows=[];overlaprows=[];stratarows=[]
for cohort,G in groups.items():
 ids=np.r_[G['math'],G['biology']];assert not zero[ids].any();ref={};refids={}
 if cohort=='discriminative':
  for g in G:
   z=np.load(S/'analysis'/f'{g}_fine_matched_background.npz');ref[g]=z['mean_per_pc'];refids[g]=z['feature_ids']
 else:
  draw={g:np.empty((1000,len(G[g])),int) for g in G}
  for st in np.unique(stratum[ids]):
   candidates=pool[stratum[pool]==st];loc={g:np.flatnonzero(stratum[G[g]]==st) for g in G};n0,n1=len(loc['math']),len(loc['biology']);assert n0+n1<=len(candidates)
   for b in range(1000):
    picked=rng.choice(candidates,n0+n1,replace=False);draw['math'][b,loc['math']]=picked[:n0];draw['biology'][b,loc['biology']]=picked[n0:]
   stratarows.append(dict(cohort=cohort,stratum=int(st),eligible_candidates=len(candidates),selected_math=n0,selected_biology=n1))
  for g in G:
   d=draw[g];weights=sparse.csr_matrix((np.full(d.size,1/len(G[g])),(np.repeat(np.arange(1000),len(G[g])),d.ravel())),shape=(1000,16384));ref[g]=weights@P;refids[g]=d;np.savez_compressed(O/f'{g}_matched_reference.npz',feature_ids=d,mean_per_pc=ref[g])
 # Independent numerical check of exact reference sizes and strata,including reused background.
 for b in range(1000):
  assert not set(refids['math'][b])&set(refids['biology'][b])
  for g in G:
   assert len(set(refids[g][b]))==len(G[g]);assert np.array_equal(np.bincount(stratum[refids[g][b]],minlength=len(lookup)),np.bincount(stratum[G[g]],minlength=len(lookup)))
 q={g:P[ii].mean(0) for g,ii in G.items()};qm=P[ids].mean(0);bgpooled=sum(len(G[g])*ref[g] for g in G)/len(ids);groupstats={}
 for label,ii,mean,bg in [(g,G[g],q[g],ref[g]) for g in G]+[('pooled',ids,qm,bgpooled)]:
  h=P[ii,:64].sum(1);pc1=P[ii,0];headref=bg[:,:64].sum(1);lo,hi=np.quantile(headref,[.025,.975]);groupstats[label]={'members':len(ii),'head_mean':float(h.mean()),'head_median':float(np.median(h)),'head_min_max':[float(h.min()),float(h.max())],'head_above_isotropic_dimension_fraction':int((h>64/1024).sum()),'PC1_mean':float(pc1.mean()),'PC2_64_mean':float(P[ii,1:64].sum(1).mean()),'first256_mean':float(P[ii,:256].sum(1).mean()),'head_matched_reference95':[float(lo),float(hi)],'head_above_matched95':bool(h.mean()>hi),'head_below_matched95':bool(h.mean()<lo)}
  meanband=mean.reshape(16,64).sum(1);medianband=np.median(bands[ii],axis=0);bb=bg.reshape(1000,16,64).sum(2);blo,bhi=np.quantile(bb,[.025,.975],axis=0)
  for k in range(16):bandrows.append(dict(cohort=cohort,group=label,members=len(ii),band=k+1,PC_start=64*k+1,PC_end=64*(k+1),mean=float(meanband[k]),median=float(medianband[k]),matched_low=float(blo[k]),matched_high=float(bhi[k]),dictionary_mean=float(bands[:,k].mean())))
 ov=float(np.minimum(q['math'],q['biology']).sum());ovb=float(np.minimum(q['math'].reshape(16,64).sum(1),q['biology'].reshape(16,64).sum(1)).sum());bgov=np.minimum(ref['math'],ref['biology']).sum(1);bgob=np.minimum(ref['math'].reshape(1000,16,64).sum(2),ref['biology'].reshape(1000,16,64).sum(2)).sum(1);cond=float(np.minimum(q['math'][1:64]/q['math'][1:64].sum(),q['biology'][1:64]/q['biology'][1:64].sum()).sum())
 for resolution,v,arr in [('per_PC',ov,bgov),('64PC_bands',ovb,bgob)]:
  lo,hi=np.quantile(arr,[.025,.975]);overlaprows.append(dict(cohort=cohort,math_members=len(G['math']),biology_members=len(G['biology']),resolution=resolution,observed=v,matched_median=float(np.median(arr)),matched_low=float(lo),matched_high=float(hi),below_matched95=bool(v<lo),above_matched95=bool(v>hi),physics_documents=0))
 allstats[cohort]={'groups':groupstats,'overlap_per_PC':ov,'overlap_64PC':ovb,'PC2_64_renormalized_overlap':cond,'reference_selected_fraction':{g:float(np.isin(refids[g],ids).mean()) for g in G}}
 for g,ii in G.items():
  for i in ii:memberrows.append(dict(cohort=cohort,domain_bias=g,feature_id=int(i),PC1=float(P[i,0]),PC2_64=float(P[i,1:64].sum()),first64=float(P[i,:64].sum()),first256=float(P[i,:256].sum()),**{f'band{k+1}':float(bands[i,k]) for k in range(16)}))
 assert np.isclose(qm.sum(),1) and ovb+1e-12>=ov
 if cohort=='strict16':np.savez_compressed(O/'strict16_distributions.npz',math=q['math'],biology=q['biology'],pooled=qm,math_background_overlap=bgov,band_background_overlap=bgob)
table('member_spectrum.csv',memberrows);table('band_profiles.csv',bandrows);table('overlap_comparison.csv',overlaprows);table('strict_background_strata.csv',stratarows)

# Direction signs and actual subspaces are separate from square-distribution overlap.
decpath=B/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz';dec=np.load(decpath)['decoder_model_scale'];u=dec/np.linalg.norm(dec,axis=1,keepdims=True);G=groups['strict16'];um,ub=u[G['math']],u[G['biology']];cos=np.abs(um@ub.T);qm,_=np.linalg.qr(um.T);qb,_=np.linalg.qr(ub.T);sing=np.linalg.svd(qm.T@qb,compute_uv=False);proj=np.load(S/'analysis/common_spectrum.npz')['PC_columns'];err=float(np.max(np.abs((u[np.r_[G['math'],G['biology']]]@proj)**2-P[np.r_[G['math'],G['biology']]])));assert err<1e-10
np.savez_compressed(O/'strict16_actual_directions.npz',absolute_pair_cosine=cos,principal_cosine=sing,math_ids=G['math'],biology_ids=G['biology']);allstats['strict16']['actual_directions']={'absolute_cosine_mean':float(cos.mean()),'absolute_cosine_max':float(cos.max()),'subspace_ranks':[len(G['math']),len(G['biology'])],'subspace_trace_over_minrank':float((sing**2).sum()/min(len(G['math']),len(G['biology']))),'projection_cache_max_error':err}
dump('summary.json',{'scope':cfg['scope'],'quantities':allstats,'physics_status':'NOT_RUN','new_model_forwards':0,'training_updates':0})
dump('audit.json',{'status':'PASS','group_reference_stratum_size_disjoint_checks':6000,'projection_direct_reconstruction_max_error':err,'all_selected_full_PC_sums_one':bool(np.allclose(P[np.unique([r['feature_id'] for r in memberrows])].sum(1),1)),'coarsened_overlap_nondecreasing':True,'new_model_forwards':0,'physics_not_claimed':True})

# Few words on figures;interpretation and denominators live in the report.
font=S/'presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':13,'axes.titlesize':17,'axes.labelsize':14,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
def save(fig,n):
 for ext in ['png','pdf']:fig.savefig(F/(n+'.'+ext),dpi=190,bbox_inches='tight',facecolor='white')
 plt.close(fig)
color={'discriminative':'#267a9e','strict16':'#c36a43'};titles={'discriminative':'领域区分成员（960名）','strict16':'严格单域成员（16名）'}
fig,axes=plt.subplots(1,2,figsize=(13,5.1),sharey=True);fig.subplots_adjust(left=.08,right=.98,top=.85,bottom=.18,wspace=.16)
for ax,cohort in zip(axes,groups):
 rr=[r for r in bandrows if r['cohort']==cohort and r['group']=='pooled'];x=np.arange(16);ax.fill_between(x,[r['matched_low'] for r in rr],[r['matched_high'] for r in rr],color='#d2d5d8',alpha=.8,label='匹配字典95%参照');ax.plot(x,[r['mean'] for r in rr],'-o',color=color[cohort],label='成员平均');ax.plot(x,[r['median'] for r in rr],'--',color=color[cohort],alpha=.8,label='成员中位数');ax.set_xticks([0,3,7,11,15],['1–64','193–256','449–512','705–768','961–1024']);ax.set_ylim(0,.30);ax.set_xlabel('共同PC谱段（每段64维）');ax.set_title(titles[cohort]);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.grid(axis='y',alpha=.16)
axes[0].set_ylabel('单位decoder平方投影份额');axes[0].legend(fontsize=10,frameon=False);save(fig,'figure1_spectral_location')
fig,axes=plt.subplots(1,2,figsize=(12.8,4.8),sharey=True);fig.subplots_adjust(left=.16,right=.98,bottom=.17,top=.82,wspace=.23)
for ax,res,title in zip(axes,['per_PC','64PC_bands'],['逐PC重合（主读数）','每64PC合并（较粗读数）']):
 for y,cohort in enumerate(['discriminative','strict16']):
  r=next(r for r in overlaprows if r['cohort']==cohort and r['resolution']==res);ax.plot([r['matched_low'],r['matched_high']],[1-y,1-y],color='#bfc5cb',lw=10,solid_capstyle='round');ax.plot(r['observed'],1-y,'o',color=color[cohort],ms=10);ax.text(r['observed'],1-y+.20,f"{r['observed']:.3f}",ha='center',color=color[cohort],fontsize=15)
 ax.set_xlim(.3,1);ax.set_ylim(-.5,1.6);ax.set_yticks([1,0],['领域区分433／527','严格单域7／9']);ax.set_xlabel('数学／生物谱分布重合');ax.set_title(title);ax.grid(axis='x',alpha=.16)
save(fig,'figure2_spectral_overlap')
G=groups['strict16'];ii=np.r_[G['math'],G['biology']];fig,ax=plt.subplots(figsize=(12,7.7));fig.subplots_adjust(left=.18,right=.94,bottom=.12,top=.91);im=ax.imshow(bands[ii],aspect='auto',vmin=0,vmax=float(bands[ii].max()),cmap='YlOrRd');ax.set_yticks(range(16),['数学 · f'+str(i) for i in G['math']]+['生物 · f'+str(i) for i in G['biology']]);ax.set_xticks([0,3,7,11,15],['1–64','193–256','449–512','705–768','961–1024']);ax.axhline(6.5,color='white',lw=2);ax.set_xlabel('共同PC谱段（每段64维）');ax.set_title('严格单域16名：逐成员谱位置');cb=fig.colorbar(im,ax=ax,pad=.025);cb.ax.yaxis.set_major_formatter(PercentFormatter(1));cb.set_label('单位decoder平方投影份额');save(fig,'appendix_strict16_members')
sources=[Path(__file__).resolve(),S/'freeze.json',S/'presentation_variants/pooled_simple_20261030/freeze.json',S/'analysis/all_decoder_projection.npz',S/'analysis/discovery_metrics.npz',S/'analysis/common_spectrum.npz',S/'tables/all_dictionary_screen.csv',decpath,S/'analysis/math_fine_matched_background.npz',S/'analysis/biology_fine_matched_background.npz'];dump('source_manifest.json',{'files':[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sources],'parent_asset_ids':['analysis_a15_27_04_r10_domain_member_atlas_20261030','analysis_a15_27_03_r09_domain_difference_decomposition_20261029'],'physics_documents':0,'new_model_forwards':0})
print(json.dumps({'statistics':allstats,'overlap_rows':overlaprows},ensure_ascii=False,indent=2),flush=True)
