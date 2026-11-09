import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,csv,gzip,sys,time
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];O=E/'analysis'
def rows(p):return [json.loads(x) for x in Path(p).read_text().splitlines() if x]
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def main():
 t=time.time();cfg=json.load(open(E/'config.json'));prefix=rows(E/'data/prefixes.jsonl');pos=rows(E/'data/positions.jsonl');families=rows(E/'data/families.jsonl');conditions=json.load(open(E/'data/conditions.json'));bykey={r['prefix_id']:r for r in prefix};first=np.array([r['candidate_map']['U']['position_indices'][0] for r in prefix]);cands=[];prs=[];allrows=[]
 with gzip.open(O/'candidate_token_logprob.csv.gz','wt',newline='') as f:
  w=csv.writer(f);w.writerow(['condition','prefix_id','family_id','split','candidate','token_index','model_position','token_number','fragment','log_probability','first_prediction_from_prefix'])
  for c in conditions['unique']:
   name=c['condition'];x=np.load(O/f'condition_{name}.npz');lp=x['logp'];diag=x['first_diagnostics'];assert len(diag)==len(prefix)
   for ri,r in enumerate(prefix):
    d={'condition':name,'prefix_id':r['prefix_id'],'family_id':r['family_id'],'domain':r['domain'],'split':r['split'],'paraphrase_id':r['paraphrase_id'],'context_type':r['context_type'],'length_matched_AB':r['length_matched_AB'],'length_matched_UV':r['length_matched_UV'],'KL':diag[ri,1],'entropy':diag[ri,2],'expected_log_frequency':diag[ri,3],'common1_mass':diag[ri,4],'format_mass':diag[ri,5],'special_token_mass':diag[ri,6],'unassigned_vocabulary_mass':diag[ri,7],'perturbation_norm':float(x['perturbation_norm'][first[ri]]),'applied_perturbation_norm':float(x['applied_perturbation_norm'][first[ri]]),'applied_h_norm':float(x['applied_h_norm'][first[ri]]),'h_norm':float(x['h_norm'][first[ri]]),'energy_fraction':float(x['energy_fraction'][first[ri]])}
    for j,k in enumerate(['U','V','A','B']):
     a=r['candidate_map'][k];inds=a['position_indices'];values=[float(lp[ix,j if ti==0 else 0]) for ti,ix in enumerate(inds)];d['L_'+k]=sum(values);d['length_'+k]=len(values);d['mean_token_L_'+k]=np.mean(values)
     for ai,(ix,v,token,frag) in enumerate(zip(inds,values,a['token_ids'],a['token_fragments'])):w.writerow([name,r['prefix_id'],r['family_id'],r['split'],k,ai,pos[ix]['model_position'],token,frag,v,ai==0])
     cands.append({'condition':name,'prefix_id':r['prefix_id'],'family_id':r['family_id'],'domain':r['domain'],'split':r['split'],'paraphrase_id':r['paraphrase_id'],'context_type':r['context_type'],'candidate':k,'text':a['text'],'token_count':len(values),'log_probability':sum(values),'sequence_probability':float(np.exp(sum(values))),'per_token_log_probability':json.dumps(values),'token_numbers':json.dumps(a['token_ids'])})
    d['r']=d['L_A']-d['L_B'];d['upper_margin']=d['L_U']-d['L_V'];d['upper_correct']=float(d['upper_margin']>0);d['specific_correct']=float(d['r']>0) if r['context_type']=='A' else float(d['r']<0) if r['context_type']=='B' else np.nan
    d['correct_candidate_NLL']=-d['L_'+r['context_type']] if r['context_type'] in ['A','B'] else np.nan
    d['specific_vs_U']=d['L_'+r['context_type']]-d['L_U'] if r['context_type'] in ['A','B'] else np.nan
    allrows.append(d)
   print('Summarized',name,flush=True)
 pd.DataFrame(cands).to_csv(O/'candidate_sequence_scores.csv.gz',index=False,compression='gzip');D=pd.DataFrame(allrows);D.to_csv(O/'prefix_scores.csv.gz',index=False,compression='gzip')
 # Family/paraphrase metrics with both sides and broad preference explicit.
 for key,g in D.groupby(['condition','family_id','domain','split','paraphrase_id'],sort=False):
  a=g.set_index('context_type');r0=a.loc['broad','r'];ra=a.loc['A','r'];rb=a.loc['B','r'];m={'condition':key[0],'family_id':key[1],'domain':key[2],'split':key[3],'paraphrase_id':key[4],'r0':r0,'rA':ra,'rB':rb,'gA':ra-r0,'gB':r0-rb,'J':(ra-rb)/2,'specific_correct':(float(ra>0)+float(rb<0))/2,'both_correct':float(ra>0 and rb<0),'upper_correct':g['upper_correct'].mean(),'upper_both_cues':float(a.loc['A','upper_correct'] and a.loc['B','upper_correct']),'upper_margin':g['upper_margin'].mean(),'upper_broad':a.loc['broad','upper_margin'],'upper_A':a.loc['A','upper_margin'],'upper_B':a.loc['B','upper_margin'],'length_matched_AB':bool(g['length_matched_AB'].all()),'length_matched_UV':bool(g['length_matched_UV'].all()),'J_mean_token':((a.loc['A','mean_token_L_A']-a.loc['A','mean_token_L_B'])-(a.loc['B','mean_token_L_A']-a.loc['B','mean_token_L_B']))/2}
  for col in ['KL','entropy','expected_log_frequency','common1_mass','format_mass','special_token_mass','unassigned_vocabulary_mass','perturbation_norm','applied_perturbation_norm','applied_h_norm','h_norm','energy_fraction','correct_candidate_NLL','specific_vs_U']:m[col]=g[col].mean()
  prs.append(m)
 T=pd.DataFrame(prs);T.to_csv(O/'paraphrase_metrics.csv',index=False);metrics=['J','gA','gB','r0','rA','rB','specific_correct','both_correct','upper_correct','upper_both_cues','upper_margin','upper_broad','upper_A','upper_B','J_mean_token','KL','entropy','expected_log_frequency','common1_mass','format_mass','special_token_mass','unassigned_vocabulary_mass','perturbation_norm','applied_perturbation_norm','applied_h_norm','h_norm','energy_fraction','correct_candidate_NLL','specific_vs_U']
 F=T.groupby(['condition','family_id','domain','split'],sort=False)[metrics+['length_matched_AB','length_matched_UV']].mean().reset_index();F.to_csv(O/'family_metrics.csv',index=False)
 # Pair all intervention effects to unchanged full values, same family/paraphrase.
 fullT=T[T.condition=='full'].set_index(['family_id','paraphrase_id']);pair=T.copy();pair['J_loss']=pair.apply(lambda r:fullT.loc[(r.family_id,r.paraphrase_id),'J']-r.J,axis=1)
 pair['specific_correct_loss']=pair.apply(lambda r:fullT.loc[(r.family_id,r.paraphrase_id),'specific_correct']-r.specific_correct,axis=1);pair['upper_correct_loss']=pair.apply(lambda r:fullT.loc[(r.family_id,r.paraphrase_id),'upper_correct']-r.upper_correct,axis=1)
 pair['new_specific_error_upper_retained']=pair.apply(lambda r:float(fullT.loc[(r.family_id,r.paraphrase_id),'both_correct']==1 and r.both_correct<1 and fullT.loc[(r.family_id,r.paraphrase_id),'upper_both_cues']==1 and r.upper_both_cues==1),axis=1)
 pair['eligible_full_specific_and_upper']=pair.apply(lambda r:float(fullT.loc[(r.family_id,r.paraphrase_id),'both_correct']==1 and fullT.loc[(r.family_id,r.paraphrase_id),'upper_both_cues']==1),axis=1);pair.to_csv(O/'paired_paraphrase_changes.csv',index=False)
 PF=pair.groupby(['condition','family_id','domain','split'])[['J_loss','specific_correct_loss','upper_correct_loss','new_specific_error_upper_retained','eligible_full_specific_and_upper']].mean().reset_index();PF.to_csv(O/'paired_family_changes.csv',index=False)
 S=F[F.split=='evaluation'].copy();domains=['biology','mathematics','physics'];fids={d:sorted(S[S.domain==d].family_id.unique()) for d in domains};rng=np.random.default_rng(cfg['bootstrap_seed']);draws={d:rng.integers(0,12,(cfg['bootstrap_replicates'],12)) for d in domains};np.savez(O/'bootstrap_family_draws.npz',**draws)
 def interval(a):return float(np.mean(a)),float(np.quantile(a,.025)),float(np.quantile(a,.975))
 def boot_values(frame,col,domain):
  x=frame.set_index('family_id').loc[fids[domain],col].to_numpy();return x.mean(),x[draws[domain]].mean(1)
 sums=[]
 for name,g in S.groupby('condition',sort=False):
  bs={};means={}
  for domain in domains:
   z=g[g.domain==domain];row={'condition':name,'domain':domain,'families':12,'cue_positions':48,'upper_positions':72,'both_side_paraphrases':24}
   for m in metrics:
    mean,b=boot_values(z,m,domain);row[m]=mean;row[m+'_low']=np.quantile(b,.025);row[m+'_high']=np.quantile(b,.975);bs.setdefault(m,[]).append(b);means.setdefault(m,[]).append(mean)
   q=T[(T.condition==name)&(T.domain==domain)&(T.split=='evaluation')];row['specific_correct_count']=int(np.rint(q.specific_correct.sum()*2));row['both_correct_count']=int(q.both_correct.sum());row['upper_correct_count']=int(np.rint(q.upper_correct.sum()*3));row['family_all_four_specific_correct']=int((z.specific_correct==1).sum());sums.append(row)
  row={'condition':name,'domain':'overall_equal_domains','families':36,'cue_positions':144,'upper_positions':216,'both_side_paraphrases':72}
  for m in metrics:
   b=np.mean(bs[m],0);row[m]=np.mean(means[m]);row[m+'_low']=np.quantile(b,.025);row[m+'_high']=np.quantile(b,.975)
  q=T[(T.condition==name)&(T.split=='evaluation')];row['specific_correct_count']=int(np.rint(q.specific_correct.sum()*2));row['both_correct_count']=int(q.both_correct.sum());row['upper_correct_count']=int(np.rint(q.upper_correct.sum()*3));row['family_all_four_specific_correct']=int((g.specific_correct==1).sum());sums.append(row)
 summary=pd.DataFrame(sums);summary.to_csv(O/'summary.csv',index=False)
 def diff(a,b,col='J'):
  ga=S[S.condition==a].set_index('family_id');gb=S[S.condition==b].set_index('family_id');v=ga[col]-gb[col];return v
 # Complete family-paired contrasts: all conditions versus full and versus head16.
 contrasts=[]
 for name in S.condition.unique():
  for ref in ['full','keep_head16']:
   for col in ['J','upper_margin','specific_correct','upper_correct','KL','correct_candidate_NLL']:
    v=diff(name,ref,col);boot=[];mean=[]
    for domain in domains:
     a=v.loc[fids[domain]].to_numpy();b=a[draws[domain]].mean(1);boot.append(b);mean.append(a.mean());contrasts.append({'condition':name,'reference':ref,'metric':col,'domain':domain,'difference':a.mean(),'low95':np.quantile(b,.025),'high95':np.quantile(b,.975),'positive_families':int((a>0).sum()),'negative_families':int((a<0).sum()),'families':12})
    b=np.mean(boot,0);contrasts.append({'condition':name,'reference':ref,'metric':col,'domain':'overall_equal_domains','difference':np.mean(mean),'low95':np.quantile(b,.025),'high95':np.quantile(b,.975),'positive_families':int((v>0).sum()),'negative_families':int((v<0).sum()),'families':36})
 pd.DataFrame(contrasts).to_csv(O/'all_paired_contrasts.csv',index=False)
 primary=[];membercontrasts=[]
 for group in ['low','middle','high']:
  target=f'feature_delete_{group}';loss=diff('full',target)
  for typ in ['same_count','norm_matched']:
   controls=[f'feature_delete_random_{group}_{seed}' if typ=='same_count' else f'feature_normmatch_{group}_{seed}' for seed in cfg['random_seeds']]
   nulls=[diff('full',c) for c in controls];null=sum(nulls)/3;excess=loss-null
   for control,n in zip(controls,nulls):
    v=loss-n
    for domain in domains+['overall_equal_domains']:
     ds=domains if domain=='overall_equal_domains' else [domain];bs=[v.loc[fids[d]].to_numpy()[draws[d]].mean(1) for d in ds];b=np.mean(bs,0);membercontrasts.append({'group':group,'type':typ,'control':control,'domain':domain,'excess_loss':float(np.mean([v.loc[fids[d]].mean() for d in ds])),'low95':np.quantile(b,.025),'high95':np.quantile(b,.975)})
   for domain in domains+['overall_equal_domains']:
    ds=domains if domain=='overall_equal_domains' else [domain];b=np.mean([excess.loc[fids[d]].to_numpy()[draws[d]].mean(1) for d in ds],0);ids=sum([fids[d] for d in ds],[])
    primary.append({'group':group,'control_type':typ,'domain':domain,'target_J_loss':loss.loc[ids].mean(),'control_mean_J_loss':null.loc[ids].mean(),'excess_J_loss':excess.loc[ids].mean(),'low95':np.quantile(b,.025),'high95':np.quantile(b,.975),'low_simultaneous6':np.quantile(b,.05/12),'high_simultaneous6':np.quantile(b,1-.05/12),'positive_families':int((excess.loc[ids]>0).sum()),'families':len(ids)})
 pd.DataFrame(primary).to_csv(O/'primary_feature_contrasts.csv',index=False);pd.DataFrame(membercontrasts).to_csv(O/'individual_random_contrasts.csv',index=False)
 # Length sensitivity uses fixed, whole-family masks; no new fit, no selection of easier model successes.
 sensitivity=[]
 for name,g in S.groupby('condition'):
  for subset,col in [('AB_length_matched','length_matched_AB'),('UV_length_matched','length_matched_UV')]:
   for domain in domains:
    z=g[(g.domain==domain)&(g[col]==1)]
    if len(z):sensitivity.append({'condition':name,'subset':subset,'domain':domain,'families':len(z),**{m:z[m].mean() for m in ['J','J_mean_token','specific_correct','upper_margin','upper_correct']}})
 pd.DataFrame(sensitivity).to_csv(O/'length_sensitivity.csv',index=False)
 # Independent arithmetic audit, without calling the aggregation path above.
 checks={'all_conditions_present':len(summary.condition.unique())==167,'prefix_rows':len(D)==288*167,'candidate_rows':len(cands)==288*4*167,'family_rows':len(F)==48*167,'evaluation_families':len(S.family_id.unique())==36,'J_identity':float(abs(T.J-(T.gA+T.gB)/2).max())<1e-10,'mean_only_J_zero':float(abs(T[T.condition=='mean_only'].J).max())<1e-8}
 xa=np.load(O/'condition_full.npz');xb=np.load(O/'condition_keep_head1024.npz');checks['all_PC_exact_all_scored_positions']=bool(np.array_equal(xa['logp'],xb['logp']));checks['full_KL_zero']=float(abs(xa['first_diagnostics'][:,1]).max())<1e-6
 dump(E/'audit/result_validation.json',{'pass':all(checks.values()),'checks':checks,'elapsed_seconds':time.time()-t,'raw_candidate_rows':len(cands),'raw_prefix_rows':len(D),'bootstrap_seed':cfg['bootstrap_seed'],'bootstrap_replicates':cfg['bootstrap_replicates']});print(json.dumps(checks));assert all(checks.values())
 print(summary[(summary.domain=='overall_equal_domains')&summary.condition.isin(['full','mean_only','keep_head16','keep_head64','feature_delete_low','feature_delete_middle','feature_delete_high','crosscoder_reconstruction'])][['condition','J','specific_correct_count','upper_correct_count','KL']].to_string(index=False))
if __name__=='__main__':main()
