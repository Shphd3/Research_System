from common import *
import argparse,pickle,re,warnings
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.special import expit
from scipy.stats import spearmanr
warnings.filterwarnings('error',category=RuntimeWarning)
TASKS=['coarse','math_fine','bio_fine']; CSP=[.01,.1,1.,10.]

def task_rows(rr,task,strict=True):
 a=[r for r in rr if r['panel']=='the' and r.get('eligible',True)]
 if task!='coarse':a=[r for r in a if r['domain']==('math' if task=='math_fine' else 'biology') and (r.get('fine_eligible',False) if strict else True)]
 return a

def labels(rr,task):return np.array([int(r['domain']=='biology') if task=='coarse' else int(r['topic']==('analysis' if task=='math_fine' else 'ecology_evolution')) for r in rr])
def ba(y,p):return float(np.mean([np.mean(np.asarray(p)[y==c]==c) for c in [0,1] if np.any(y==c)]))
def choose(rr,task,n):
 y=labels(rr,task);out=[]
 for c in [0,1]:
  group=sorted([r for r,v in zip(rr,y) if v==c],key=order)
  if task=='coarse':
   leaves=LEAVES['math' if c==0 else 'biology'];g=[[r for r in group if r['topic']==t] for t in leaves];picked=[]
   for k in range(max(map(len,g))):
    for gg in g:
     if k<len(gg):picked.append(gg[k])
   group=picked
  out+=group[:n]
 return out

def coords(rr,V,mu):
 h,z,nm=selected_array(rr);return (h-mu)@V,h,z,nm

def train(X,y,Xv,yv,scale='standardized',Cfixed=None):
 mu=X.mean(0);sd=np.std(X,axis=0) if scale=='standardized' else np.ones(X.shape[1]);floor=max(float(sd.max())*1e-6,1e-8);sd=np.maximum(sd,floor)
 best=None
 for C in ([Cfixed] if Cfixed else CSP):
  m=LogisticRegression(C=C,class_weight='balanced',solver='liblinear',tol=1e-8,max_iter=5000,random_state=1031).fit((X-mu)/sd,y);v=ba(yv,m.predict((Xv-mu)/sd))
  if best is None or v>best['dev_ba']+1e-12:best={'model':m,'mean':mu,'std':sd,'C':C,'dev_ba':v,'parameters':int(X.shape[1]+1),'scale':scale,'iterations':int(m.n_iter_[0]),'std_floor':floor}
 return best

def score(m,X):return (X-m['mean'])/m['std']@m['model'].coef_[0]+m['model'].intercept_[0]
def nuis(r):
 t=r['prefix'];return {'platform='+str(r['platform_family']):1.,'genre='+str(r['genre']):1.,'position_bin='+str(r['position']//32):1.,'position':r['position']/192,'newline':t.count('\n')/max(len(t),1),'math':sum(t.count(a) for a in ['\\','$','{','}','='])/max(len(t),1),'punct':sum(t.count(a) for a in ',;:.!?')/max(len(t),1),'heading':float(bool(r.get('heading_present'))),'words':len(t.split())/192}
def contrast_boot(y,s0,s1,seed=1031,B=2000):
 rng=np.random.default_rng(seed);ii=np.array([np.concatenate([rng.choice(np.flatnonzero(y==c),sum(y==c),replace=True) for c in [0,1]]) for _ in range(B)])
 d=(s1>=0).astype(int)==y;v=(s0>=0).astype(int)==y;diff=(d[ii]-v[ii].astype(int)).mean(1);return diff

def bootstrap_scores(y,s,seed=1031,B=2000):
 rng=np.random.default_rng(seed);ii=np.array([np.concatenate([rng.choice(np.flatnonzero(y==c),sum(y==c),replace=True) for c in [0,1]]) for _ in range(B)])
 a=((s>=0).astype(int)==y)[ii].mean(1);return a

def fit():
 t0=time.time();rr=rows(OUT/'data/selected_metadata.jsonl');assert all(r.get('fine_eligible') is not None for r in rr if r['split']!='heldout')
 basis=np.load(ROOT/'R10_domain_member_atlas_20261030/analysis/common_spectrum.npz');V=basis['PC_columns'];mu=basis['mean'];ev=basis['eigenvalues'];assert np.max(np.abs(V.T@V-np.eye(1024)))<1e-10
 bands={'head':np.eye(1024)[:,:64],'middle':np.eye(1024)[:,480:544],'tail':np.eye(1024)[:,960:],'full':np.eye(1024),'head_middle':np.eye(1024)[:,np.r_[0:64,480:544]],'head_tail':np.eye(1024)[:,np.r_[0:64,960:1024]],'head_next':np.eye(1024)[:,:128]}
 for s in [1031,1032,1033]:bands['random'+str(s)]=np.linalg.qr(np.random.default_rng(s).normal(size=(1024,64)))[0]
 q=np.linalg.qr(np.random.default_rng(1034).normal(size=(960,64)))[0];b=np.zeros((1024,128));b[:64,:64]=np.eye(64);b[64:,64:]=q;bands['head_random']=b
 np.savez_compressed(OUT/'analysis/bases.npz',V=V,mean=mu,eigenvalues=ev,**bands)
 budgets={}
 for split in ['discovery','development']:
  counts=[]
  for task in TASKS:
   a=task_rows([r for r in rr if r['split']==split],task);counts.extend(np.bincount(labels(a,task),minlength=2).tolist())
  budgets[split]=int(min(counts));assert budgets[split]>=3
 # Verify the saved decoder is in the same model units, before any H metric.
 dd=np.load(ROOT/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz');D=dd['decoder_model_scale'];bias=dd['decoder_bias_model'];smoke_rows=task_rows([r for r in rr if r['split']=='discovery'],'coarse')[:6];_,hh,zz,nm=coords(smoke_rows,V,mu);rec=zz@D+bias;calc=((hh-rec)**2).sum(1)/(hh**2).sum(1);err=float(np.max(np.abs(calc-nm)))
 smoke={'decoder_cpu_FP64_vs_cached_native_BF16_nmse_max_abs':err,'mean_abs':float(np.mean(np.abs(calc-nm))),'limit_max_abs':.02,'limit_mean_abs':.005,'n':len(hh),'native_z_unmodified':True,'bias_includes_TRAIN_mean':True,'H_numeric_accessed':False}
 dump(OUT/'audits/smoke.json',smoke);assert err<.02 and np.mean(np.abs(calc-nm))<.005
 state={};frozen=[];fit_rows=[];docrows=[];textprobes=[]
 for task in TASKS:
  d_all=task_rows([r for r in rr if r['split']=='discovery'],task);v_all=task_rows([r for r in rr if r['split']=='development'],task)
  d=choose(d_all,task,budgets['discovery']);v=choose(v_all,task,budgets['development']);y=labels(d,task);yv=labels(v,task);S,h,z,nm=coords(d,V,mu);Sv,hv,zv,nmv=coords(v,V,mu)
  sd={'D':d,'V':v,'models':{},'features':[]};
  for scale in ['standardized','raw']:
   for name,B in bands.items():
    m=train(S@B,y,Sv@B,yv,scale);sd['models'][scale+'__'+name]=m;fit_rows.append(dict(task=task,scale=scale,space=name,C=m['C'],D=len(d),V=len(v),parameters=m['parameters'],dev_ba=m['dev_ba'],iterations=m['iterations']))
  # All available D sensitivity: same frozen V; not used for main conclusions.
  Sa,ha,za,nma=coords(d_all,V,mu);ya=labels(d_all,task)
  for name in ['full','head','middle','tail']:
   sd['models']['allD__'+name]=train(Sa@bands[name],ya,Sv@bands[name],yv)
  dv=DictVectorizer(sparse=False);NX=dv.fit_transform([nuis(r) for r in d]);NV=dv.transform([nuis(r) for r in v]);sd['nuisance_vectorizer']=dv;sd['nuisance_model']=train(NX,y,NV,yv,'raw')
  tv=TfidfVectorizer(max_features=3000,min_df=1,ngram_range=(1,2),sublinear_tf=True);TX=tv.fit_transform([r['prefix'] for r in d]).toarray();TV=tv.transform([r['prefix'] for r in v]).toarray();sd['tfidf_vectorizer']=tv;sd['tfidf_model']=train(TX,y,TV,yv,'raw')
  m=sd['models']['standardized__full'];wpc=m['model'].coef_[0]/m['std'];w=V@wpc;df=D@w;delta=z[y==1].mean(0)-z[y==0].mean(0);sup=(z>0).sum(0);valid=np.flatnonzero(sup>=3);rank=sorted(valid.tolist(),key=lambda f:(-abs(delta[f]*df[f]),f));selected=rank[:18];sd['features']=selected;sd['feature_coeff']=df;sd['raw_wpc']=wpc
  for i in selected[:12]:frozen.append(dict(task=task,feature_id=i,D_support=int(sup[i]),D_mean_z_class0=float(z[y==0,i].mean()),D_mean_z_class1=float(z[y==1,i].mean()),D_signed_score_contrast=float(delta[i]*df[i]),frozen_rank=selected.index(i)+1))
  rec=z@D+bias;recv=zv@D+bias;se=S-(rec-mu)@V;sev=Sv-(recv-mu)@V
  sd['residual_model']=train(se,y,sev,yv)
  sd['reconstruction_model']=train((rec-mu)@V,y,(recv-mu)@V,yv)
  for name,X,Xv in [('feature_presence',(z[:,selected[:12]]>0).astype(float),(zv[:,selected[:12]]>0).astype(float)),('feature_amplitude',z[:,selected[:12]],zv[:,selected[:12]]),('feature_unit_amplitude',z[:,selected[:12]]/np.maximum(np.linalg.norm(z[:,selected[:12]],axis=1,keepdims=True),1e-12),zv[:,selected[:12]]/np.maximum(np.linalg.norm(zv[:,selected[:12]],axis=1,keepdims=True),1e-12))]:sd[name]=train(X,y,Xv,yv)
  # Candidate response relations chosen on D, not H; no causal interpretation.
  pair=[]
  for i,f in enumerate(selected[:12]):
   for g in selected[i+1:12]:
    a=(z[:,f]>0).astype(float);b=(z[:,g]>0).astype(float)
    if a.std()==0 or b.std()==0:continue
    ph=float(np.corrcoef(a,b)[0,1]);joint=[float(np.mean(a[y==c]*b[y==c])-np.mean(a[y==c])*np.mean(b[y==c])) for c in [0,1]];pair.append((abs(joint[1]-joint[0])+abs(ph)*.1,f,g,ph,joint[1]-joint[0]))
  pair=sorted(pair,reverse=True)[:6];sd['pairs']=pair
  def fx(Z,pairs):return np.stack([(Z[:,f]>0)*(Z[:,g]>0) for _,f,g,_,_ in pairs],1).astype(float) if pairs else np.empty((len(Z),0))
  pairX=fx(z,pair);pairV=fx(zv,pair);base=z[:,selected[:12]];basev=zv[:,selected[:12]]
  sd['pair_aug']=train(np.c_[base,pairX],y,np.c_[basev,pairV],yv);sd['single_aug']=train(z[:,selected[:12+len(pair)]],y,zv[:,selected[:12+len(pair)]],yv)
  # Train-only marginal propensity models for frequency/source-adjusted pair tests.
  PX=np.c_[NX,y];PV=np.c_[NV,yv];prop={}
  for f in sorted({x for p in pair for x in p[1:3]}):
   a=(z[:,f]>0).astype(int)
   if len(np.unique(a))==2:prop[f]=train(PX,a,PV,(zv[:,f]>0).astype(int),'raw',Cfixed=.1)
   else:prop[f]={'constant':float(a.mean())}
  sd['propensity']=prop
  # Frozen hypotheses for text interpretation: D-learned signed linear band axes.
  for name in ['head','middle','tail']:
   bm=sd['models']['standardized__'+name];axis=score(bm,S@bands[name]);idx=np.argsort(axis);lo=idx[:max(3,len(idx)//4)];hi=idx[-max(3,len(idx)//4):];vec=TfidfVectorizer(max_features=2000,ngram_range=(1,1),stop_words='english');A=vec.fit_transform([r['prefix'] for r in d]).toarray();deltaT=A[hi].mean(0)-A[lo].mean(0);terms=vec.get_feature_names_out();positive=terms[np.argsort(deltaT)[-5:][::-1]].tolist();negative=terms[np.argsort(deltaT)[:5]].tolist()
   textprobes.append(dict(task=task,band=name,positive_terms=positive,negative_terms=negative,selection='D high/low quartiles;H not seen'))
  for r in d+v:docrows.append(dict(task=task,role=r['split'],seq_id=r['seq_id'],topic=r['topic'],position=r['position'],token_id=r['token_id']))
  state[task]=sd;print('FIT',task,'D/V',len(d),len(v),'features',selected[:4],flush=True)
 with (OUT/'models/frozen.pkl').open('wb') as f:pickle.dump(state,f)
 dump(OUT/'analysis/text_hypotheses.json',textprobes);table(OUT/'analysis/D_feature_freeze.csv',frozen);table(OUT/'analysis/fit_ledger.csv',fit_rows);table(OUT/'data/fitted_document_ids.csv',docrows)
 config={'bands':{'head':[1,64],'middle':[481,544],'tail':[961,1024]},'D_V_matched_per_class':budgets,'tasks':TASKS,'C_grid':CSP,'bootstrap':2000,'permutation':99,'seed':1031,'label_pairs':LEAVES,'primary_token':279,'position_rule':'last in96..191','model_training_updates':0,'new_model_forwards':0,'source_basis':'R10/R04 pooled9600 old discovery vectors;same as R07','H_exposed_before_round':True,'text_hypotheses':'D-only terms and signed readout axes','precision':'canonical FP64 decoder product with cached native z;compare saved BF16decode NMSE','fit_seconds':time.time()-t0}
 dump(OUT/'config.json',config)
 paths=[OUT/'config.json',OUT/'models/frozen.pkl',OUT/'analysis/bases.npz',OUT/'analysis/text_hypotheses.json',OUT/'data/label_rubric.json',OUT/'data/selected_metadata.jsonl']+list((PROJECT/'scripts').glob('*.py'))+[PROJECT/'protocol.md',PROJECT/'protocol_cn.md']
 dump(OUT/'freeze.json',{'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'numeric_H_accessed':False,'sha256':{str(p):sha(p) for p in paths},'status':'FROZEN_BEFORE_R12_H_NUMERIC_ACCESS'})
 print('FROZEN',time.time()-t0,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['fit']);a=p.parse_args();fit()
