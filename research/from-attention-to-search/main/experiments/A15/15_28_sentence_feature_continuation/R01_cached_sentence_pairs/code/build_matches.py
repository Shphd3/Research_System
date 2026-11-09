from core import *
from datetime import datetime,timezone
from collections import Counter
(R/'results').mkdir(exist_ok=True)
rows=[]
for s in SENTS:
 for r,p in enumerate(s['positions']):
  d=DOCS[s['doc']];surf=d['token_surfaces'][p]
  rows.append([s['doc'],p,s['sid'],r,len(s['positions']),min(9,10*r//len(s['positions'])),p//48,d['token_ids'][p],d['token_class'][p],int(any(c.isnumeric() for c in surf)),int(d['domain']=='biology')])
t=np.array(rows,np.int32);names=['doc','pos','sid','relative','length','decile','quartile','id','class','numeric','domain'];np.savez_compressed(R/'data/tokens.npz',**dict(zip(names,t.T)))
rng=np.random.default_rng(20261028);partners={};blocks={};blocklist=[]
for dom in ['math','biology']:
 ds=sorted([i for i,d in enumerate(DOCS) if d['domain']==dom],key=lambda i:(DOCS[i]['source_text_sha256'],DOCS[i]['seq_id']));rng.shuffle(ds)
 for bi in range(30):
  a,b=ds[2*bi:2*bi+2];partners[a]=b;partners[b]=a;blocks[a]=bi;blocks[b]=bi;blocklist.append(dict(domain=dom,block=bi,docs=[a,b]))
dump(R/'data/document_blocks.json',blocklist)
ps=[]
for s in SENTS:
 rr=np.flatnonzero(t[:,2]==s['sid'])
 for v,i in enumerate(rr):
  for j in rr[v+1:]:
   cl=max(t[i,8],t[j,8]);cl=1 if 1 in (t[i,8],t[j,8]) else (2 if 2 in (t[i,8],t[j,8]) else cl)
   dist=t[j,1]-t[i,1];db=np.searchsorted([1,3,7,15,31,63],dist,side='left')
   ps.append([i,j,s['doc'],s['sid'],blocks[s['doc']],int(s['domain']=='biology'),dist,db,cl,int(t[i,7]==t[j,7])])
base=np.array(ps,np.int32);np.savez_compressed(R/'data/base_pairs.npz',pairs=base)
receipts={}
for k in ['SAE','CC']:
 B,ptr,ids,g=load_data(k);l0=B.sum(1);out=np.full((len(base),6),-1,np.int32);diagnostics=Counter();dr={i:np.flatnonzero(t[:,0]==i) for i in range(120)}
 allid={dom:set(t[t[:,10]==dom,7]) for dom in (0,1)}
 for q,row in enumerate(base):
  i,j,di,si,bi,dom,dist,db,cl,eq=row;donor=partners[di];rr=dr[donor]
  global_other=(t[:,10]==dom)&(t[:,0]!=di)&(t[:,7]==t[j,7]);hasglobal=global_other.any();haspartner=(t[rr,7]==t[j,7]).any()
  samepos=rr[(t[rr,5]==t[j,5])&(t[rr,6]==t[j,6])]
  good=samepos[(l0[samepos]>=.8*l0[j])&(l0[samepos]<=1.25*l0[j])]
  exact=good[t[good,7]==t[j,7]];tier=1
  if not len(exact):
   reason='global_no_ID' if not hasglobal else ('partner_no_ID' if not haspartner else ('position_loss' if not (t[samepos,7]==t[j,7]).any() else 'L0_loss'))
   diagnostics[reason]+=1;tier=2;exact=good[(t[good,8]==t[j,8])&((t[good,7]==t[i,7])==bool(eq))]
  else:reason='T1'
  if len(exact):
   def key(c):return (abs(int(l0[c])-int(l0[j])),abs(t[c,3]/t[c,4]-t[j,3]/t[j,4]),abs(int(t[c,1])-int(t[j,1])),hashlib.sha256(f'{k}/{DOCS[di]["seq_id"]}/{t[i,1]}/{t[j,1]}/{DOCS[donor]["seq_id"]}/{t[c,1]}/20261029'.encode()).hexdigest())
   c=min(exact,key=key);narrow=int(.9*l0[j]<=l0[c]<=1.1*l0[j]);out[q]=[c,tier,narrow,hasglobal,haspartner,len(exact)];diagnostics['T'+str(tier)]+=1
  else:out[q,3:5]=[hasglobal,haspartner];diagnostics['no_match']+=1
 np.savez_compressed(R/f'data/matches_{k}.npz',matches=out,l0=l0,frequency_group=g)
 receipts[k]=dict(counts=dict(diagnostics),eligible_pairs=len(base),T1_lexical_different=int(((out[:,1]==1)&(base[:,8]==0)&(base[:,9]==0)).sum()),unique_donors_T1=len(set(out[out[:,1]==1,0].tolist())),group_counts=np.bincount(g,minlength=4).tolist())
 print(k,receipts[k],flush=True);del B
frozen=dict(seed=20261028,seeds={'pairing':20261028,'ties':20261029,'bootstrap':20261030,'incidence':20261031,'graph':20261032},null_chains=2,null_draws_per_chain=199,burnin_factor=5,spacing_factor=.1,bootstrap=5000,threads=4,ram_gib=16,wall_hours=4,output_gib=5,dicts=['SAE','CC'],groups=GROUPS,metrics=METRICS,distances=DIST,pair_columns=['i','j','doc','sid','block','domain','distance','distance_bin','class','same_id'],match_columns=['control','tier','narrow','global_id','partner_id','candidate_count'],token_columns=names,primary_family_cells=336,text_sha256=sha(R/'data/sentence_manifest.jsonl'),frozen_at=datetime.now(timezone.utc).isoformat(),outcomes_opened=False)
dump(R/'config.json',frozen);dump(R/'provenance/matching.json',receipts)
print('Preparation frozen',len(t),'tokens',len(base),'pairs')
