from pathlib import Path
import json,csv,hashlib,datetime,math,collections,re,shutil,zipfile,fcntl
E=Path(__file__).resolve().parents[1];O=E/'analysis/meeting_20261026';S=Path('/data/250010109/Research_System');D=Path(json.load(open(O/'provenance/delivery_paths.json'))['owner']);B=Path(json.load(open(O/'provenance/delivery_paths.json'))['brief'])
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for buf in iter(lambda:f.read(8<<20),b''):h.update(buf)
 return h.hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def read(p):return json.loads(Path(p).read_text())
def rows(n):return list(csv.DictReader(open(O/'tables'/n)))
def main():
 checks={};ep=rows('01_endpoints_36.csv');assert len(ep)==36;checks['runs']=36;index={(int(r['seed']),int(r['old_slots']),r['method']):r for r in ep}
 for m in rows('01_method_means_12.csv'):
  r=[index[s,int(m['old_slots']),m['method']] for s in [29,43,71]]
  for task in ['old','new']:
   val=sum(round(float(x[task+'_accuracy_pct'])*8) for x in r)/24
   assert math.isclose(val,float(m[task+'_accuracy_pct']),abs_tol=1e-10)
 for r in rows('01_all_vs_U_seed_27.csv'):
  s,k,m=int(r['seed']),int(r['old_slots']),r['comparison'][0]
  for task in ['old','new']:
   assert math.isclose(float(index[s,k,m][task+'_accuracy_pct'])-float(index[s,k,'U'][task+'_accuracy_pct']),float(r[task+'_accuracy_pct']),abs_tol=1e-10)
 stats=rows('02_rule_mode_stats_all.csv');checks['behavior_group_rows']=len(stats)
 for r in stats:
  n=int(r['pair_n']);excluded=int(r['same_target_excluded_n']);nn=int(r['rule_confusion_denominator']);assert n-excluded==nn
  assert sum(int(r[x+'_n']) for x in ['old_rule_correct','new_rule_endpoint','other_list_item','other_output_or_invalid'])==nn
  for x in ['old_rule_correct','new_rule_endpoint','other_list_item','other_output_or_invalid']:assert math.isclose(float(r[x+'_pct']),int(r[x+'_n'])/nn*100,abs_tol=1e-10)
 for s in [29,43,71]:
  for m,k in [('U',0),('F',0),('U',4),('F',4)]:
   for step in [0,1,2,4,8,16,32,64,120,180,240]:
    both=next(r for r in stats if r['seed']==str(s) and r['method']==m and r['old_slots']==str(k) and r['step']==str(step) and r['panel']=='combined' and r['command']=='both')
    panels=[r for r in stats if r['seed']==str(s) and r['method']==m and r['old_slots']==str(k) and r['step']==str(step) and r['panel']!='combined' and r['command']=='both'];assert len(panels)==2
    for n in ['old_rule_correct_n','new_rule_endpoint_n','other_list_item_n','other_output_or_invalid_n','both_correct_n','same_prediction_n']:assert sum(int(r[n]) for r in panels)==int(both[n])
 nr=rows('03_F_finite_checks_90.csv');assert len(nr)==90;checks['raw_F_loss_increases']=sum(float(r['actual_loss_change'])>0 for r in nr);assert checks['raw_F_loss_increases']==69
 checks['raw_F_positive_final_dot']=sum(float(r['g_dot_final_actual'])>0 for r in nr);assert checks['raw_F_positive_final_dot']==48
 checks['F_positive_beyond_rounding_tolerance']=sum(float(r['g_dot_final_actual'])>float(r['final_actual_tolerance']) for r in nr);assert checks['F_positive_beyond_rounding_tolerance']==0
 for r in nr:
  assert math.isclose(float(r['finite_remainder']),float(r['actual_loss_change'])-float(r['g_dot_final_actual']),abs_tol=1e-12)
 rep=read(O/'provenance/representation_receipt.json');assert rep['checkpoint_count']==9 and rep['sequence_forwards']==1152 and rep['optimizer_updates']==0
 assert all(r['all_predictions_equal'] for r in rep['states']);checks['representation_prediction_match_sequences']=1152
 checks['checkpoint_readout_max_CE_error']=max(r['replay_max_CE_error'] for r in rep['states'])
 # Reconfirm original freeze only, no repeated checkpoint qualification.
 freeze=read(E/'provenance/freeze.json');assert all(sha(p)==v['sha256'] for p,v in freeze['files'].items());checks['original_frozen_bytes_unchanged']=True
 # Plot-data source agreement, full precision not rounded prose.
 assert read(O/'results.json')['F_final_positive_beyond_tolerance']==0
 for a,b in [('01_method_means_12.csv','figure1_data.csv'),('02_rule_mode_endpoint_mean4.csv','figure2_data.csv'),('03_F_finite_checks_90.csv','figure3_data.csv')]:assert rows(a)==rows(b)
 checks['all_three_plot_data_sources_equal']=True
 links=[]
 for p in [*D.rglob('*.md'),B]:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   target=target.strip('<>').split('#')[0]
   if not target or re.match(r'^[a-zA-Z]+://',target):continue
   q=Path(target) if target.startswith('/') else p.parent/target
   if not q.exists():links.append({'source':str(p),'target':str(q)})
 assert not links,links;checks['scoped_links']='PASS'
 # Register actually saved analysis/readout output, under the existing R06 owner.
 assetid='analysis_a17_r06_meeting_20261026'
 with open(S/'assets/.catalog_registration.lock','a') as lk:
  fcntl.flock(lk,fcntl.LOCK_EX);cat=read(S/'assets/catalog.json');assert not any(x['id']==assetid for x in cat['assets'])
  entry={'id':assetid,'category':'analysis','kind':'frozen_endpoint_mode_readout_and_behavior_audit','title_cn':'A17 R06组会已有结果分析与有限模式读出','projects':['from-attention-to-search'],'required_projects':[],'storage_owner':'MoE_Router execution','payload_status':'ARRAY_FILES_PRESENT',
    'identity':{'producer_authorization':'user26Oct2026existing-results meeting analysis; no training/noTEST/noadditionalresource','owning_round':str(D),'source_protocol':str(Path(read(E/'provenance/ownership.json'))['round']) if False else str(Path(read(E/'provenance/ownership.json')['round'])/'protocol.md'),'input_assets':['analysis_a17_r06_functional_20261025','checkpoint_family_a17_r06_functional_20261025','representation_a17_r05_native_prefix_20261023','data_a17_conditional_mapping_v1','model_qwen3_0p6b_base_official_a5'],'existing_trajectory_count':36,'checkpoint_readout_count':9,'forward_sequences':1152,'new_training_updates':0,'representation_sites':['layer27.q_proj input','layer27.o_proj rawoutput'],'position':'lastprefix token beforeanswer','dtype':'float32','sampling_lock_path':str(O/'provenance/representation_sampling_lock.json'),'sampling_lock_sha256':sha(O/'provenance/representation_sampling_lock.json'),'readout_receipt':str(O/'provenance/representation_receipt.json'),'sample_boundary':'64modepairs correctnessstratified after behavior, before representationresults; notunbiasedfullDEVestimate','raw_representation_npz_sha256':sha(O/'representation_raw.npz'),'TEST_opened':False,'source_manifest':str(O/'provenance/source_manifest.json')},
    'locations':[{'path':str(O),'expected':'directory','required':True,'role':'existing_run_analysis','probes':[{'path':'results.json','expected':'file','required':True},{'path':'representation_raw.npz','expected':'file','required':True},{'path':'tables/03_F_finite_checks_90.csv','expected':'file','required':True},{'path':'provenance/representation_receipt.json','expected':'file','required':True}]}],'source_paths':[str(D/'summary.md'),str(E/'ops/meeting_analysis_20261026.py'),str(E/'ops/meeting_mode_readout_20261026.py')],'notes_cn':['实际保存分析/表示读出，非新训练；共享一个旧模型的3续训顺序。只读9检查点1152序列，未新增资源。所有性能结论仍以完整DEV而非分层小样本为准。']}
  cat['assets'].append(entry);tmp=S/'assets/catalog.json.meeting.tmp';write(tmp,cat);tmp.replace(S/'assets/catalog.json');fcntl.flock(lk,fcntl.LOCK_UN)
 checks['registered_output_asset']=assetid
 # Mark expansion stopped now; only organization/copy/hash can follow.
 finished=datetime.datetime.now(datetime.timezone.utc);cutoff=datetime.datetime(2026,10,26,1,40,tzinfo=datetime.timezone.utc)
 assert finished<cutoff
 checks.update(status='PASS',analysis_expansion_stopped_utc=finished.isoformat(),analysis_expansion_stopped_BJT=finished.astimezone(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S'),before_0940=True,new_training_updates=0,new_forward_sequences=1152,new_checkpoint_readouts=9,TEST_opened=False,new_external_job=False,visual_reviewed=['figure1','figure2','figure3'],report_target_BJT='2026-10-26 10:00')
 write(O/'provenance/final_analysis_verification.json',checks);shutil.copy2(O/'provenance/final_analysis_verification.json',D/'reproduce/final_analysis_verification.json');shutil.copy2(__file__,D/'reproduce'/Path(__file__).name)
 with (D/'coverage_cn.md').open('a') as f:f.write('\n实际停止追加分析：北京时间'+checks['analysis_expansion_stopped_BJT']+'，早于09:40；之后仅整理、同步与打包。新读出9检查点1152序列、零训练更新，严格资源/TEST边界未变。\n')
 # Input hashes verify existing originals; current small-output manifests kept separately.
 manifest={'owner':str(D),'analysis_root':str(O),'brief':str(B),'asset_id':assetid,'verification':checks,'input_manifest_sha256':sha(O/'provenance/source_manifest.json'),'raw_modepair_table_execution_only':str(O/'tables/02_rule_mode_pairs_105600.csv'),'raw_vectors_execution_only':str(O/'representation_raw.npz'),'curated_files':{str(p.relative_to(D)):sha(p) for p in D.rglob('*') if p.is_file() and p.name!='artifact_manifest.json'}}
 write(D/'artifact_manifest.json',manifest)
 assert all(sha(D/p)==h for p,h in manifest['curated_files'].items())
 print(json.dumps({'status':'PASS','analysis_stop_BJT':checks['analysis_expansion_stopped_BJT'],'asset_id':assetid,'curated_files':len(manifest['curated_files'])},ensure_ascii=False))
if __name__=='__main__':main()
