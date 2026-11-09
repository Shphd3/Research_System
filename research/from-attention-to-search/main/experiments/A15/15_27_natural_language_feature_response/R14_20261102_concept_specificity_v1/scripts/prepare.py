import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import numpy as np,json,hashlib,datetime,csv,sys
from tokenizers import Tokenizer
from families import BIO,MATH,PHYS
E=Path(__file__).resolve().parents[1]; BASE=E.parent
P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response')/E.name
M=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 assert not (E/'freeze.json').exists(),'Frozen: use append-only amendments, not prepare rerun'
 tok=Tokenizer.from_file(str(M/'tokenizer.json'));families=[];rows=[];positions=[];sequences=[]
 overrides={('mathematics',3):['https://mathworld.wolfram.com/GeometricMean.html'],('mathematics',8):['https://mathworld.wolfram.com/SymmetricMatrix.html','https://mathworld.wolfram.com/AntisymmetricMatrix.html'],('mathematics',9):['https://mathworld.wolfram.com/Injection.html','https://mathworld.wolfram.com/Surjection.html'],('mathematics',13):['https://mathworld.wolfram.com/PrimeNumber.html'],('mathematics',14):['https://mathworld.wolfram.com/Rotation.html','https://mathworld.wolfram.com/Reflection.html']}
 for domain,fs in [('biology',BIO),('mathematics',MATH),('physics',PHYS)]:
  assert len(fs)==16
  for fi,f in enumerate(fs):
   U,V,A,B,broad,a1,b1,a2,b2,source=f;fid=f'{domain}_{fi+1:02d}';split='development' if fi<4 else 'evaluation'
   src=([] if domain=='mathematics' and fi in [8,9,13,14] else ['https://openstax.org/books/'+source.replace('/', '/pages/',1)])+overrides.get((domain,fi),[])
   # Audit which additional sources are needed; no claim a citation URL by itself proves semantic correctness.
   fam={'domain':domain,'family_id':fid,'split':split,'U':U,'V':V,'A':A,'B':B,'sources':src,'review_agent':'/root, model-independent semantic review','review':'A and B share the named upper concept; supplied contrasts distinguish them under stated conditions. V is from a different category. Not a human blind annotation.','remaining_matching':'V and U can differ in length/frequency; all lengths/frequencies retained. Two global wording templates are shared, not independent source replications.'}
   families.append(fam)
   for pi,(aa,bb) in enumerate([(a1,b1),(a2,b2)]):
    for ct,text in [('broad',broad),('A',aa),('B',bb)]:
     for term in [A,B]:assert term.casefold() not in text.casefold(),(fid,ct,term)
     prefix=('Identify the scientific concept from the description.\nDescription: '+text+'\nAnswer:') if pi==0 else ('Name the concept that best fits this account.\nAccount: '+text+'\nAnswer:')
     pre=tok.encode(prefix,add_special_tokens=False).ids; rid=f'{fid}_p{pi}_{ct}'
     row={**fam,'prefix_id':rid,'paraphrase_id':pi,'context_type':ct,'prefix':prefix,'prefix_token_ids':pre,'prefix_length':len(pre),'candidate_map':{}}
     for key,term in [('U',U),('V',V),('A',A),('B',B)]:
      answer=' '+term+'.';allids=tok.encode(prefix+answer,add_special_tokens=False).ids
      assert allids[:len(pre)]==pre,(rid,key,'boundary merge')
      ans=allids[len(pre):];assert len(ans)>0
      sid=f'{rid}_{key}';pidx=[]
      for ai,target in enumerate(ans):
       # Reuse the first prediction for the four candidates, since the visible prefix is exactly identical.
       uid=rid+'_first' if ai==0 else f'{sid}_{ai}'
       if ai==0 and key!='U':ix=next(j for j in range(len(positions)-1,-1,-1) if positions[j]['position_uid']==uid)
       else:
        ix=len(positions);positions.append({'index':ix,'position_uid':uid,'sequence_id':sid,'prefix_id':rid,'family_id':fid,'domain':domain,'split':split,'candidate':key,'candidate_token_index':ai,'model_position':len(pre)-1+ai,'target_id':target,'first':ai==0,'visible_token_ids':allids[:len(pre)+ai]})
       pidx.append(ix)
      row['candidate_map'][key]={'text':term,'answer':answer,'token_ids':ans,'token_fragments':[tok.decode([i],skip_special_tokens=False) for i in ans],'length':len(ans),'position_indices':pidx,'end_boundary':'includes terminal period; no EOS','sequence_id':sid}
      sequences.append({'sequence_id':sid,'prefix_id':rid,'split':split,'token_ids':allids,'selected':[(j,ix) for j,ix in zip(range(len(pre)-1,len(allids)-1),pidx) if key=='U' or j!=len(pre)-1]})
     row['length_matched_AB']=row['candidate_map']['A']['length']==row['candidate_map']['B']['length'];row['length_matched_UV']=row['candidate_map']['U']['length']==row['candidate_map']['V']['length']
     row['AB_prefix_token_length_difference']=len(tok.encode(aa).ids)-len(tok.encode(bb).ids)
     rows.append(row)
 assert len(rows)==288 and len(families)==48 and sum(r['split']=='evaluation' for r in rows)==216
 for name,rr in [('families',families),('prefixes',rows),('positions',positions),('sequences',sequences)]:
  (E/'data'/f'{name}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rr))
 # Preserve R13's qualified frequency groups exactly; no reselecting based on concept-task response.
 ref=np.load(BASE/'R13_feature_presence_amplitude_20261101/data/reference_frequency.npz');np.savez(E/'data/reference_frequency.npz',**{k:ref[k] for k in ref.files})
 groups={n:np.flatnonzero(ref['group']==i).tolist() for n,i in [('low',0),('middle',1),('high',2)]}
 groups['insufficient_positive']=np.flatnonzero((ref['group']<0)&(ref['hits']>0)).tolist();groups['zero_reference']=np.flatnonzero(ref['hits']==0).tolist()
 pool=np.flatnonzero(ref['group']>=0)
 for name in ['low','middle','high']:
  other=np.setdiff1d(pool,np.array(groups[name]))
  for s in [11021,11022,11023]:groups[f'random_{name}_{s}']=np.random.default_rng(s).choice(other,len(groups[name]),replace=False).tolist()
 dump(E/'data/feature_groups.json',groups)
 old=np.load(BASE/'R13_20261101_native_spectral_decoding/data/bases.npz');V=old['V'];mu=old['mean'];ev=old['eigenvalues'];basis={'V':V,'mean':mu,'eigenvalues':ev}
 specs=[];aliases={};keys={}
 def add(name,kind,**kw):
  key=json.dumps([kind,kw],sort_keys=True)
  if key in keys:aliases[name]=keys[key];return keys[key]
  keys[key]=name;specs.append({'condition':name,'kind':kind,**kw});return name
 add('full','identity');add('identity','identity');add('mean_only','keep',pc=[])
 ends=[1,16,64,128,256,512,768,1024];bounds=[0,1,16,64,128,256,512,768,1024]
 for k in ends:add(f'keep_head{k}','keep',pc=list(range(k)))
 for j,(l,h) in enumerate(zip(bounds[:-1],bounds[1:]),1):
  add(f'keep_B{j}','keep',pc=list(range(l,h)));add(f'delete_B{j}','delete',pc=list(range(l,h)))
 add('keep_H','keep',pc=list(range(16)));add('delete_H','delete',pc=list(range(16)))
 for j in range(3,9):
  l,h=bounds[j-1:j+1];add(f'append_B{j}','keep',pc=list(range(16))+list(range(l,h)));add(f'head_extension_B{j}','keep',pc=list(range(16+h-l)))
 ranks=sorted({len(c['pc']) for c in specs if 'pc' in c and 0<len(c['pc'])<1024});Q={}
 for seed in [11021,11022,11023]:
  rng=np.random.default_rng(seed);R=np.linalg.qr(rng.standard_normal((1024,1024)))[0];basis[f'random_{seed}']=R
  Q0=V[:,:16];X=rng.standard_normal((1024,1008));X-=Q0@(Q0.T@X);Rorth=np.linalg.qr(X)[0];basis[f'orthogonal_{seed}']=Rorth
  assert np.max(abs(Q0.T@Rorth))<1e-10
  for rank in ranks:
   add(f'random_keep_r{rank}_s{seed}','random_keep',seed=seed,rank=rank);add(f'random_delete_r{rank}_s{seed}','random_delete',seed=seed,rank=rank)
  for j in range(3,9):
   l,h=bounds[j-1:j+1];add(f'random_append_B{j}_s{seed}','random_append',seed=seed,rank=h-l)
  for c in list(specs):
   if c['kind']=='delete':add(f'normmatch_{c["condition"]}_s{seed}','spectral_normmatch',target=c['condition'],seed=seed,rank=len(c['pc']))
 # Feature deletion preserves residual, mean and decoder bias. Random groups use the complement, same cardinality.
 add('crosscoder_reconstruction','reconstruct')
 for name in ['low','middle','high']:
  add(f'feature_delete_{name}','feature_delete',group=name)
  for seed in [11021,11022,11023]:
   gn=f'random_{name}_{seed}';add(f'feature_delete_{gn}','feature_delete',group=gn)
   add(f'feature_normmatch_{name}_{seed}','feature_normmatch',group=gn,target_group=name)
 
 for seed in [11021,11022,11023]:aliases[f'random_keep_r1024_s{seed}']='full';aliases[f'random_delete_r1024_s{seed}']='mean_only'
 np.savez(E/'data/bases.npz',**basis);dump(E/'data/conditions.json',{'unique':specs,'aliases':aliases,'random_ranks':ranks})
 cfg={'run':E.name,'seed':1102,'bootstrap_seed':21102,'bootstrap_replicates':4000,'random_seeds':[11021,11022,11023],'model':str(M),'crosscoder_checkpoint':'/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt','layers':list(range(1,28,2)),'LM_dtype':'BF16','projection_dtype':'FP64','head':'native RMSNorm once then tied BF16 lm_head; fixed evaluation row batch64','family_counts':{'development_per_domain':4,'evaluation_per_domain':12},'token_scoring':'all answer tokens including period, no EOS, full answer sequence summed, first token from prefix last position','CC_gate':'u=post_relu(normalize(h14));z=u*(u*sum_layer_decoder_norm>checkpoint_threshold);1024 position pad;eval frozen','frequency_reference_positions':65536,'frequency_reference_independent_documents':'UNKNOWN: packed DCLM reference positions, no recovered document map','frequency_cuts_hits':[20,170,881],'frequency_zero_and_insufficient':'separate, retained in full/reconstruction and residual; not target group','fixed_families':[f'{d}_{n:02d}' for d in ['biology','mathematics','physics'] for n in [5,6]],'estimate':{'cache_GB_max':2,'GPU_used':1,'max_concurrent_GPU':2,'wall_minutes_initial_estimate':[10,35]},'semantic_acceptance':'Unknown','resources':'5090-2-spot; embedded smoke before scoring; second allocated device unused; no H100'}
 dump(E/'config.json',cfg)
 dump(E/'audit/01_scientific_identification.json',{'status':'PRE_OUTPUT_FROZEN','primary':'full J minus feature-deleted J; excess over same-count random deletion and per-position norm-matched random perturbations','three_evidence_layers':'prior readout accessibility; current frozen-output intervention; current externally defined concept/line evidence','rivals':['general output corruption','unequal perturbation magnitude','redundant contribution','insufficient whole-model concept ability','answer length/frequency and wording effects'],'selectivity':'requires excess effect, clear cue, independent family consistency; upper judgement and prediction distortion separately reported; no subtracting task accuracies','scope':'task-specific contribution, not unique encoding, global ranking, presence-vs-amplitude mechanism or free generation'})
 dump(E/'audit/02_data_statistics.json',{'status':'PRE_OUTPUT_FROZEN','families':48,'prefixes':288,'evaluation_independence_units':36,'development_independence_units':12,'semantic_review':'AI-authored and AI-reviewed with independent reference definitions, not human-rated','length_matched_eval_prefixes':sum(r['length_matched_AB'] and r['split']=='evaluation' for r in rows),'template':'two shared templates; not independent template generalization','splits':'first4 specified families per domain develop; subsequent12 eval; no exact A/B concepts shared across splits','uncertainty':'4000 paired family draws stratified by domain; domain equal overall; all conditions paired same draws; pointwise95%; primary6 group-v-control-mean contrasts additionally Bonferroni99.1667%; no p-values','source_review':'sources recorded, see source_audit.json for current retrieval; no model answers used to swap data','family_members':{d:[f['family_id'] for f in families if f['domain']==d and f['split']=='evaluation'] for d in ['biology','mathematics','physics']}})
 print(json.dumps({'prefixes':len(rows),'positions':len(positions),'sequences':len(sequences),'conditions':len(specs),'aliases':len(aliases),'feature_counts':{n:len(v) for n,v in groups.items() if not n.startswith('random')}}))
if __name__=='__main__':main()
