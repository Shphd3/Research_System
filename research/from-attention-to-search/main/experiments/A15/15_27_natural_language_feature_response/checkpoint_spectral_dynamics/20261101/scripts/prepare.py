"""Freeze inspected Dense states and paired existing text panels; no model forwards."""
from pathlib import Path
import json,hashlib,csv
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/data/250010109/MoE_Router/experiments')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
runs=[BASE/'20260913_dense_baseline_pretraining/runs'/s for s in ['full_10b_8x5090_20260913T102944Z','full_50b_continue_from_10b_8x5090_r2_20260915T131706Z']]+[BASE/'20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090']
rows=[];excluded=[]
for run in runs:
 cfg=json.load(open(run/'resolved_config.json'))
 if 'data' not in cfg:
  assert cfg['config']['tokenizer_name_or_path']==rows[0]['tokenizer']['path']
  cfg['data']={'tokenizer':rows[0]['tokenizer']}
 for p in sorted(list(run.glob('milestones/*/manifest.json'))+list(run.glob('checkpoints/*/manifest.json'))):
  m=json.load(open(p));t=m['tokens_seen']; f=next(f for f in m['files'] if f['path']=='state.pt');state=p.parent/'state.pt'
  row=dict(checkpoint=str(p.parent),state_path=str(state),tokens=t,step=m['optimizer_step'],kind=m['checkpoint_kind'],schema_version=m['schema_version'],complete=m['complete'],state_sha256=f['sha256'],state_bytes=f['size_bytes'],manifest_sha256=sha(p),config_path=str(run/'resolved_config.json'),config_sha256=sha(run/'resolved_config.json'),architecture=cfg['config']['model'],tokenizer=cfg['data']['tokenizer'],training_contract_sha256=cfg['training_contract_sha256'])
  if not 500_000_000<=t<=33_000_000_000:excluded.append(dict(checkpoint=row['checkpoint'],tokens=t,reason='outside_requested_window'));continue
  if not state.is_file():
   alternatives=list((BASE/'20260913_dense_baseline_pretraining/continuation_checkpoints').glob(f'*/target_*_actual_{t:012d}_step_*/state.pt'))
   alternatives=[a for a in alternatives if json.load(open(a.parent/'manifest.json'))['files'][0]['sha256']==f['sha256']]
   if alternatives:
    row['original_checkpoint']=row['checkpoint'];row['checkpoint']=str(alternatives[0].parent);state=alternatives[0];row['state_path']=str(state);row['manifest_sha256']=sha(state.parent/'manifest.json')
   else:
    excluded.append(dict(checkpoint=row['checkpoint'],tokens=t,reason='PAYLOAD_MISSING; manifest remains; searched original runs and continuation archives'));continue
  assert state.stat().st_size==f['size_bytes'] and m['complete']
  rows.append(row)
rows.sort(key=lambda r:r['tokens']);assert len({r['tokens'] for r in rows})==len(rows)
for r in rows:assert r['architecture']==rows[0]['architecture'] and r['tokenizer']['files_sha256']==rows[0]['tokenizer']['files_sha256']
manifest=dict(schema_version=1,anchor_id='15_27_05_01',date='2026-11-01',trajectory='native_dense_seed17_281431040_parameters',checkpoints=rows,excluded=excluded,missing_state_definition='Only source-manifested states with unavailable payloads count as missing. No nominal grid is assumed.',inventory_scope='all saved milestone/recovery states in the three inspected lineage runs; duplicate continuation archive aliases excluded by original identity',state_counter_verification='PENDING_AT_RUNTIME',architecture_compatibility='PASS',tokenizer_compatibility='PASS',main_interface='final_raw_h: blocks[7] residual-post before model.norm',source_code_root=str(BASE/'20260913_dense_baseline_pretraining'),smoke_and_semantic_tokens=[500000000,17000000000,33000000000])
write(ROOT/'manifest.json',manifest)
source=BASE/'20260930_ntp_statistics_local_compatibility/data/selected.jsonl';docs=[json.loads(l) for l in open(source)]
ids=np.array([d['input_ids'] for d in docs],np.int64);assert ids.shape==(2048,256)
for key in ['source_group_id','text_sha256','input_ids_sha256']:
 assert not {d[key] for d in docs if d['split']=='fit'}&{d[key] for d in docs if d['split']=='test'}
positions=np.arange(7,256,8,dtype=np.int64)
np.savez(ROOT/'data/geometry.npz',input_ids=ids,attention_mask=np.ones_like(ids,dtype=bool),positions=positions,split=np.array([d['split'] for d in docs]),sample_ids=np.array([d['sample_id'] for d in docs]),family=np.array([d['source_group_id'] for d in docs]),category=np.array([d['category'] for d in docs]))
geom_meta=[{k:d[k] for k in ['sample_id','split','category','source_group_id','source_group_scope','text_sha256','input_ids_sha256']} for d in docs]
write(ROOT/'data/geometry_metadata.json',geom_meta)
r12=BASE/'20261026_natural_language_feature_response/R12_spectral_semantic_granularity_20261031';r11=BASE/'20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02/data/documents.jsonl'
bridge=[json.loads(l) for l in open(r12/'data/selected_metadata.jsonl')];bridge=[d for d in bridge if d['panel']=='the']
hreview={(r['seq_id'],r['panel']):r for r in json.load(open(r12/'data/H_label_review.json'))['records']}
lookup={d['seq_id']:d for d in map(json.loads,open(r11))}
for d in bridge:
 if (d['seq_id'],'the') in hreview:d['fine_eligible']=hreview[d['seq_id'],'the']['fine_eligible']
 assert lookup[d['seq_id']]['token_ids'][d['position']]==279
bids=np.array([lookup[d['seq_id']]['token_ids'] for d in bridge],np.int64); assert bids.shape==(96,192)
np.savez(ROOT/'data/bridge.npz',input_ids=bids,attention_mask=np.ones_like(bids,dtype=bool),positions=np.array([d['position'] for d in bridge]),sample_ids=np.array([d['seq_id'] for d in bridge]))
write(ROOT/'data/bridge_metadata.json',bridge)
fitids=list(csv.DictReader(open(r12/'data/fitted_document_ids.csv')));write(ROOT/'data/bridge_fitted_ids.json',fitids)
config=dict(seed=1101,precision='float32 weights and forwards; TF32 off; no dropout; eval mode; math SDPA',covariance_precision='float64',positions=positions.tolist(),geometry_context=256,geometry_records=2048,reference_records=1024,evaluation_records=1024,positions_per_record=32,reference_N=32768,evaluation_N=32768,document_weight='equal 32 positions per record; each position weight1',independence='record group only; paper-level IDs unavailable',nested=[16,64,128,256],bands={'head':[0,64],'middle':[480,544],'tail':[960,1024]},explained_fractions=[0.5,0.8,0.9,0.95,0.99],semantic_tokens=manifest['smoke_and_semantic_tokens'],supplement_layers=[0,3],C_grid=[0.01,0.1,1.,10.],readout='binary logistic,balanced class weight,TRAIN-only per-feature standardization,C selected by DEV balanced accuracy;smallest C on ties',readout_sets={'head':list(range(64)),'middle':list(range(480,544)),'tail':list(range(960,1024)),'head128':list(range(128)),'head_middle':list(range(64))+list(range(480,544)),'head_tail':list(range(64))+list(range(960,1024)),'full':list(range(1024))},readout_bootstrap=2000,reference_split_replicates=8,reference_split_rule='eight deterministic paired 512/512 doc halves, same indices across checkpoints; descriptive 2.5/97.5% range, not calibrated population CI',key_turn_rule='largest absolute successive log normalized-spectrum-rate change, ties earliest; add its right endpoint to uncertainty set if not early/mid/late',stability_onset='NOT_ESTIMATED; no universal tolerance justified;show consecutive rates and ratio to split reference with thresholds 0.5,1,2 as descriptive sensitivity',single_direction='only if adjacent relative eigengaps >=0.05;otherwise UNIDENTIFIABLE;all bands retain gap diagnostics',max_gpus=2,resource_profile='5090-2-spot',image='shphd-lite-0911',wall_hours=6,storage_gib=20,checkpoint_load='sequential; release model after each;state mmap;read-only',resume='per checkpoint atomic cache with key and payload hashes',geometry_source_asset='ntp_statistics_panel_2048',bridge_source_asset='analysis_a15_27_05_r12_spectral_semantic_granularity_20261031',inputs_sha256={str(p):sha(p) for p in [source,r11,r12/'data/selected_metadata.jsonl',r12/'data/H_label_review.json',r12/'data/fitted_document_ids.csv']},panel_sha256={p.name:sha(p) for p in (ROOT/'data').glob('*')})
write(ROOT/'config.json',config)
print(json.dumps(dict(checkpoints=len(rows),tokens=[r['tokens']/1e9 for r in rows],geometry=ids.shape,bridge=bids.shape)))
