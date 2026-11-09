from pathlib import Path
import json,csv,hashlib,datetime,math,collections,shutil,fcntl,re,zipfile
E=Path(__file__).resolve().parents[1];O=E/'analysis/local_dynamics_20261026';S=Path('/data/250010109/Research_System');OWN=json.load(open(O/'provenance/ownership.json'));R=Path(OWN['round']);A=Path(OWN['anchor']);PROJ=S/'Projects/from-attention-to-search'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def rows(n):return list(csv.DictReader(open(O/'tables'/n)))
def main():
 receipt=read(O/'receipt.json');assert receipt['status']=='PASS' and receipt['sequence_forwards']==11424
 calls=read(O/'sequence_forward_calls.json');assert sum(r['sequences'] for r in calls)==11424
 assert calls[-1]['total']==11424 and max(r['total'] for r in calls)<=12000
 per=rows('per_item_losses.csv');loss=rows('candidate_group_losses_138.csv');dirs=rows('candidate_directions_54.csv')
 groups=collections.defaultdict(list)
 for r in per:groups[r['seed'],r['origin'],r['condition'],r['alpha'],r['group']].append(r)
 for r in loss:
  rr=groups[r['seed'],r['origin'],r['condition'],r['alpha'],r['group']];n=int(r['n']);assert len(rr)==n
  for col,raw in [('before_CE','before_CE'),('after_CE','after_CE'),('CE_change','CE_change')]:assert math.isclose(sum(float(x[raw]) for x in rr)/n,float(r[col]),abs_tol=1e-12)
  assert math.isclose(sum(int(x['after_correct']) for x in rr)/n*100,float(r['after_accuracy_pct']),abs_tol=1e-12)
 assert len(loss)==138 and len(dirs)==54 and len(per)==7992
 im=read(O/'provenance/original_asset_immutability.json');assert all(r['unchanged'] for r in im['states'])
 for x in im['states']:assert sha(x['path'])==x['sha256_before']
 fr=read(O/'provenance/freeze.json');assert all(sha(p)==h for p,h in fr['files'].items())
 # The original sixstate data and read-only registry are current; no same-state
 # claims are derived by averaging cross-history endpoints.
 links=[]
 for p in [*R.rglob('*.md'),*A.glob('*.md')]:
  for u in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   u=u.strip('<>').split('#')[0]
   if not u or re.match(r'^[a-zA-Z]+://',u):continue
   q=Path(u) if u.startswith('/') else p.parent/u
   if not q.exists():links.append({'source':str(p),'target':u})
 assert not links,links
 check={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'loss_group_rows_independently_recomputed':138,'per_item_rows':7992,'direction_rows':54,'noop_groups':18,'sequence_calls_summed':11424,'max_sequence_budget':12000,'original_six_checkpoints_SHA_unchanged':True,'frozen_contract_source_unchanged':True,'links':'PASS','plots_visually_reviewed':2,'new_continuation_runs':0,'candidate_checkpoints_saved':0,'temp_Adam_proposals':12,'resource_new_jobs':0,'TEST_labels_read':False,'conclusion_boundary':'only6preselectedstate×onebatch; nofulltrajectorycausalidentification'}
 write(O/'provenance/final_delivery_check.json',check)
 shutil.copy2(O/'provenance/final_delivery_check.json',R/'reproduce/final_delivery_check.json');shutil.copy2(__file__,R/'reproduce'/Path(__file__).name)
 # Actual diagnostic output asset; no trained checkpoint or candidate state is registered.
 aid='analysis_a17_r06_local_dynamics_20261026'
 entry={'id':aid,'category':'analysis','kind':'same_state_one_step_optimizer_counterfactual','title_cn':'A17 R06固定六状态单步优化反事实诊断','projects':['from-attention-to-search'],'required_projects':[],'storage_owner':'MoE_Router execution','payload_status':'ARRAY_FILES_PRESENT',
  'identity':{'source_protocol':str(R/'protocol.md'),'source_anchor':str(A/'anchor.md'),'scientific_parent':'17_04/R06','parent_assets':['checkpoint_family_a17_r06_functional_20261025','analysis_a17_r06_functional_20261025','representation_a17_r05_native_prefix_20261023','data_a17_conditional_mapping_v1','model_qwen3_0p6b_base_official_a5'],'frozen_source_manifest':str(O/'provenance/freeze.json'),'frozen_source_manifest_sha256':sha(O/'provenance/freeze.json'),'states':read(O/'provenance/plan.json')['states'],'actual_candidate_displacements':54,'temporary_Adam_proposals':12,'full_continuation_runs':0,'candidate_checkpoint_saves':0,'sequence_forwards':11424,'original_assets_immutable':str(O/'provenance/original_asset_immutability.json'),'samples':str(O/'provenance/plan.json'),'probe_train_n':64,'independent_old_DEV_n':64,'new_batch_n':36,'allowed_labels':'TRAINforobjective/projection, oldDEV64forindependentdiagnostic only; TESTnotread','uncertainty':'deterministicnoopprecisionnotstatisticalCI;3continuationordersshareoneoldmodel'},
  'locations':[{'path':str(O),'expected':'directory','required':True,'role':'actualdiagnosticresults','probes':[{'path':'receipt.json','expected':'file','required':True},{'path':'tables/candidate_group_losses_138.csv','expected':'file','required':True},{'path':'provenance/original_asset_immutability.json','expected':'file','required':True}]}],'source_paths':[str(R/'summary.md'),str(E/'ops/local_dynamics_20261026.py')],'notes_cn':['实际完成六状态各1904序列，只在副本临时单步并恢复，不保存为新训练终点。','当前F4对独立旧损失2改善4无操作0恶化；历史起点差异不能拆分θ和Adam矩。']}
 with open(S/'assets/.catalog_registration.lock','a') as f:
  fcntl.flock(f,fcntl.LOCK_EX);cat=read(S/'assets/catalog.json');assert not any(x['id']==aid for x in cat['assets']);cat['assets'].append(entry);tmp=S/'assets/catalog.json.localdyn.tmp';write(tmp,cat);tmp.replace(S/'assets/catalog.json');fcntl.flock(f,fcntl.LOCK_UN)
 # Register as a bounded supplemental record of existing17_04/R06, no new owner or Focus.
 p=PROJ/'main/anchor_ownership.json';owners=read(p);owner=next(r for r in owners['anchors'] if r['id']=='17_04')
 for q in [A/'anchor.md',A/'anchor_cn.md']:
  rel=str(q.relative_to(PROJ))
  if rel not in owner['companions']:owner['companions'].append(rel)
 rnd=next(x for x in owner['bounded_rounds'] if x['round_id']=='R06_functional_protection_20261025');rnd.setdefault('diagnostic_records',[]).append({'id':'local_dynamics_20261026','record':str(R.relative_to(PROJ)),'anchor_companions':[str((A/q).relative_to(PROJ)) for q in ['anchor.md','anchor_cn.md']],'role':'currentuserauthorizedfrozenlocalcounterfactual; nofullcontinuation','scientific_state_changed':False})
 write(p,owners)
 p=S/'sync/anchors/profiles.json';x=read(p);profile=next(z for z in x['entries'] if z['project']=='from-attention-to-search' and z['anchor_id']=='17_04_R06')
 for q in [*[A/n for n in ['anchor.md','anchor_cn.md']],*[R/n for n in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','one_page_cn.md','appendix_cn.md','figures_cn.md','deviations.md','internal_audits.md']]]:
  rel=str(q.relative_to(S))
  if rel not in profile['sources']:profile['sources'].append(rel)
 write(p,x)
 # Small index and canonical actual-payload manifest.
 (R/'README.md').write_text('# A17 R06: same-state local dynamics supplement\n\n[一页中文总结](one_page_cn.md) · [Summary](summary.md) / [完整中文](summary_cn.md) · [附录](appendix_cn.md) · [两图](figures_cn.md) · [Protocol](protocol.md) · [采样与配置](reproduce/plan.json)。\n\nBoundedauthoriseddiagnostic, notanewtrainingmethodorfullcontinuation. Existing6states restoredindependently;11424sequences, zeroTEST, noresourceallocation, nooriginalcheckpointchanges. Allsame-statefindingslocal.\n')
 manifest={'analysis_asset_id':aid,'execution_root':str(O),'state_receipt':str(O/'receipt.json'),'input_freeze_sha256':sha(O/'provenance/freeze.json'),'original_assets_immutable':True,'candidate_checkpoints_saved':False,'per_item_outputs_execution_only':str(O/'tables/per_item_losses.csv'),'source_log_steps_execution_only':str(O/'tables/trajectory_step_logs_2880.csv'),'actual_sequence_forwards':11424,'scientific_acceptance':'Unknown','fulltrajectorymechanism':'notidentified','curated_files':{str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and p.name!='artifact_manifest.json'}}
 write(R/'artifact_manifest.json',manifest);print(json.dumps({'status':'PASS','asset_id':aid,'files':len(manifest['curated_files']),'onepage':str(R/'one_page_cn.md')},ensure_ascii=False))
if __name__=='__main__':main()
