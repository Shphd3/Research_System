"""Read-only output contract checks; load each small npz array once."""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
import sys,csv,json,hashlib,time,resource
from pathlib import Path
import numpy as np

def main(r):
 r=Path(r);start=time.monotonic();g=np.load(r/'derived_geometry.npz');pp=g['p'];ll=g['L'];counts={}
 for path in r.glob('*.csv'):
  with path.open() as f:counts[path.name]=sum(1 for _ in csv.DictReader(f))
 assert counts['feature_layer_response.csv']==16384*14 and counts['hierarchy_members.csv']==16384
 assert counts['figure3_source.csv']==15537 and counts['figure2_source.csv']==420
 assert counts['graph1_nodes.csv']==30 and counts['graph1_edges.csv']==101 and counts['text_layer_amplitude.csv']==3360 and counts['hierarchy_mean_p.csv']==18
 with (r/'feature_layer_response.csv').open() as f:
  for k,row in enumerate(csv.DictReader(f)):
   a,li=divmod(k,14);assert int(row['feature'])==a and int(row['layer_one_based'])==2+2*li
   assert abs(float(row['p'])-pp[li,a])<1e-14 and abs(float(row['L'])-ll[a])<1e-12
 with (r/'hierarchy_mean_p.csv').open() as f:
  for row in csv.DictReader(f):assert abs(sum(float(row[f'mean_p_layer{i}']) for i in range(2,29,2))-1)<1e-12
 examples=[json.loads(x) for x in (r/'text_examples.jsonl').read_text().splitlines()];assert len(examples)==240
 nrandom=sum('random' in x['selection_labels'] for x in examples);nhigh=sum('high_activation' in x['selection_labels'] for x in examples);assert nrandom==150 and nhigh==90
 old=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z');norm=np.load(old/'decoder_geometry.npz')['norm'];data=old.parents[2]/'data/direct_dclm_bins_a15/index_val';m=json.loads((data/'manifest.json').read_text());records=np.load(data/'records.npy');prefix=np.load(data/'prefix.npy');maps={}
 for ex in examples:
  a=ex['feature'];pos=ex['eligible_position'];ctx=int(np.searchsorted(prefix,pos,side='right')-1);assert ctx==ex['context_index'];fi,starttok,nn,limit=map(int,records[ctx]);source=m['sources'][fi]
  if fi not in maps:maps[fi]=np.memmap(source['path'],dtype='<u4',mode='r')
  tokens=np.asarray(maps[fi][starttok:starttok+nn]);eligible=np.flatnonzero(~np.isin(tokens,m['excluded_ids']))[:limit];t=int(eligible[pos-int(prefix[ctx])]);assert t==ex['target_context_offset'] and starttok+t==ex['target_absolute_offset'] and int(tokens[t])==ex['target_token_id']
  assert len(ex['layer_amplitude'])==14 and np.allclose(ex['layer_amplitude'],ex['z']*norm[:,a].astype(float))
  assert ex['model_visible_prefix_includes_target'] and ex['original_document_id']=='UNKNOWN'
 manifest=json.loads((r/'input_reuse_manifest.json').read_text());unchanged=all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in manifest['files']);assert unchanged
 plan=json.loads((r/'execution_record.json').read_text());assert hashlib.sha256((r/'protocol_frozen.md').read_bytes()).hexdigest()==plan['protocol_sha256']
 review={'status':'PASS','CSV_row_counts':counts,'geometry_table_matches_derived_array':True,'mean_p_row_sums_one':True,'text_examples':240,'random_slots':nrandom,'high_slots':nhigh,'unique_contexts':len({e['context_index'] for e in examples}),'all_text_target_positions_match_original_index_and_bin':True,'all_amplitudes_match_shared_z_times_norm':True,'source_hashes_unchanged':unchanged,'frozen_protocol_unchanged':True,'validation_seconds':time.monotonic()-start,'validator_max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'visual_review':'All six final PNG panels viewed; Figure1 dense support labels separated into facets; Figure2/3 unchanged','scientific_review':'Codex self audit; not independent or researcher scientific approval'}
 (r/'delivery_checks.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');print(json.dumps(review,ensure_ascii=False,indent=2))
if __name__=='__main__':main(sys.argv[1])
