from common import *
from load_data import *
from stats import *
from tokenizers import Tokenizer
import pandas as pd,math,sys
stage=sys.argv[1] if len(sys.argv)>1 else 'baseline';allnew=stage=='all';tok=Tokenizer.from_file(str(Path(CFG['model'])/'tokenizer.json'));checks=0
for p in PANEL:
 e=tok.encode(p['text'],add_special_tokens=False);assert e.ids==p['token_ids'];assert p['actual_distance']==p['target_position']-p['evidence_last_position']-1;assert p['target_position']==len(e.ids)-1 and e.ids[-1]==25;a,b=p['evidence_char_span'];where=[i for i,(l,r) in enumerate(e.offsets) if r>a and l<b];assert where==p['evidence_token_positions'] and [e.ids[i] for i in where]==p['evidence_token_ids'];assert max(where)==p['evidence_last_position'];checks+=1
 for c in p['candidates']:
  assert tok.encode(p['text']+c['text'],add_special_tokens=False).ids==c['full_ids'];assert c['full_ids'][:len(e.ids)]==e.ids
 if p['condition'] in ['reverse','content']:assert len(e.ids)==320 and p['target_position']==319 and p['evidence_last_position']=={16:302,64:254,128:190}[p['actual_distance']]
 if p['condition']=='fixed_e':assert p['evidence_last_position']==190 and p['target_position'] in [207,255]
 if p['condition']=='pos64':assert p['text']==META[p['source_R19_id']]['text'] and p['token_ids']==META[p['source_R19_id']]['token_ids'] and p['position_offset']==64
b=behavior(allnew)
for row in b.values():
 for c in row['candidates']:assert abs(math.fsum(c['token_logprobs'])-c['total_logprob'])<1e-12;checks+=1
 assert abs((row['candidates'][0]['total_logprob']-row['candidates'][1]['total_logprob'])*(1 if row['gold']=='A' else -1)-row['correct_margin'])<1e-12
for site in SITES:
 data,dn=load_site(site,allnew)
 for pid,a in data.items():
  assert len(set(a['indices']))==32 and np.all(a['values']>0);assert np.all(a['pre_relu'][a['indices']]==a['values']);cut=np.partition(a['pre_relu'],-33)[-33:];assert abs(a['cutoff32']-np.partition(cut,-32)[-32])<1e-10 and abs(a['cutoff33']-np.min(cut))<1e-10;assert np.all(np.isfinite(a['h']));checks+=1
 for name in ['baseline']+(['controls'] if allnew else []):
  m=pd.read_csv(R/f'tables/{name}_pair_metrics.csv');f=pd.read_csv(R/f'tables/{name}_fact_contrasts.csv')
  for _,row in m[m.site==site].iterrows():
   x=data[row.left_id]['z'];y=data[row.right_id]['z'];sx=set(np.flatnonzero(x));sy=set(np.flatnonzero(y));assert row.shared==len(sx&sy) and row.entered==len(sy-sx) and row.exited==len(sx-sy);assert row.entered==row.exited;assert abs(row.Jaccard-len(sx&sy)/len(sx|sy))<1e-12;checks+=1
  for _,row in f[(f.site==site)&(f.view=='native')].iterrows():
   fam=row.family;frame=row.frame
   def values(d):
    xa=data[cid(frame,fam,int(d),'A')]['z'];xb=data[cid(frame,fam,int(d),'B')]['z'];de=xa-xb;return de,np.linalg.norm(de),np.sqrt((xa@xa+xb@xb)/2)
   dl,nl,sl=values(row.distance_left);dr,nr,sr=values(row.distance_right);assert abs(np.log((nr/sr)/(nl/sl))-row.log_relative_ratio)<1e-10;assert abs(cosine(dl,dr)-row.raw_contrast_cosine)<1e-10;checks+=1
for path,h in json.load(open(R/'evidence/R19_protected_snapshot.json'))['files'].items():assert sha(path)==h,path
for path,h in json.load(open(R/'evidence/analysis_implementation_frozen.json'))['hashes'].items():assert sha(path)==h,path
dump(R/f'evidence/verification_{stage}.json',dict(UTC=now(),local_time=local_now(),status='PASS',checks=checks,retokenized_prefixes=len(PANEL),available_scores=len(b),all_old_files_unchanged=True,analysis_hashes_unchanged=True,all_new_rows=allnew,model_updates=0,interventions=0))
print('VERIFY',stage,checks)
