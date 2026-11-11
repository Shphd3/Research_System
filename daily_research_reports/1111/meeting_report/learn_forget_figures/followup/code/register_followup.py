from fu import *
import fcntl,subprocess

def add(aid,paths,identity,category='analysis'):
 paths=list(map(Path,paths));assert paths and all(p.exists() for p in paths)
 with (REPO/'assets/.catalog.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);p=REPO/'assets/catalog.json';c=json.load(p.open())
  if not any(a['id']==aid for a in c['assets']):
   c['assets'].append(dict(id=aid,title_cn=aid,category=category,kind='learn_forget_followup_20261111',projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',payload_status='ARRAY_FILES_PRESENT' if category in ['representation','dataset'] else 'SOURCE_FILES_PRESENT',locations=[dict(path=str(p),expected='directory' if p.is_dir() else 'file',required=True,probes=[]) for p in paths],identity=identity,source_paths=[str(F/'protocol_cn.md'),str(F/'protocol_E_cn.md'),str(F/'protocol_F_cn.md')]));tmp=p.with_suffix('.followup-register.tmp');tmp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)
 subprocess.run([sys.executable,str(REPO/'tools/check_assets.py'),'--strict','--asset',aid,'--output',str(F/f'evidence/access_{aid}_{time.time_ns()}.json')],check=True,stdout=subprocess.DEVNULL)

def main():
 assert (F/'evidence/all_analysis_complete.json').exists();add('representation_learn_forget_followup_early_positions_20261111',[F/'data/positions/A0_000200.npz',F/'evidence/C_forward_A0_200.json'],dict(checkpoint='A0@200',positions=N,loss_dtype='float16',selection_dtype='uint8',split='R04 EVAL',updates=0),'representation')
 add('dataset_learn_forget_extended_DEV_20261111',[F/'data/E/inputs.npy',F/'data/E/targets.npy',F/'data/E/group_weights.npy',F/'data/E/batches32.json',F/'data/E/batches8_extended.json',F/'evidence/E_extension_source.json'],dict(rows=2048,sequence_length=2048,old_panel=1024,new_panel=1024,teacher_labels='FP32 TopK32 SAE 33B, A5 groups frozen',source_asset='dclm_pair_v1',user_authorized=True,eval_document_overlap=False),'dataset')
 add('analysis_learn_forget_followup_gradient_sketches_20261111',list((F/'data/E/sketches').glob('*.npy'))+[F/'results/E_pair_signs_and_values.csv',F/'evidence/E_gradients_complete.json'],dict(DIM=1048576,groups=16,replicates=4,original8_nodes_B=[.5,3,5],precision_nodes_B=[10],updates=0))
 add('representation_learn_forget_followup_FFN_inputs_20261111',list((F/'data/F').glob('h_*.npy'))+list((F/'data/F').glob('sel_*.npy'))+[F/'data/F/samples.json',F/'evidence/F_checkpoint_inventory.json'],dict(hook='block.norm2 output',hidden_dim=1024,layers=8,positions=262144,splits=['DEV','EVAL'],arms=['Dense','A0','A5','A2'],capture='float16, measuredrounding receipt',updates=0),'representation')
 add('analysis_learn_forget_followup_spectra_20261111',list((F/'data/F').glob('Q_*.npy'))+list((F/'data/F').glob('eigenvalues_*.npz'))+[F/'results/F_statistics.csv',F/'results/F_direction_heldout_validation.csv'],dict(direction_fit='DEV Cov(h,binaryFeature)/feature_std, top64, 32/128 sensitivity',lowbins=[0,1,2],evaluation='heldoutEVAL',coordinates='each model/layer own',updates=0))
 add('analysis_learn_forget_followup_tables_20261111',[F/'results',F/'evidence/all_analysis_complete.json',REPORT/'明早速报_追加_cn.md'],dict(tasks=['A','B','C','D','E','F'],researcher_judgment='Unknown',updates=0))
 dump(F/'evidence/asset_registration_complete.json',dict(new_output_assets=6,strict_passed=True,updates=0))
if __name__=='__main__':main()
