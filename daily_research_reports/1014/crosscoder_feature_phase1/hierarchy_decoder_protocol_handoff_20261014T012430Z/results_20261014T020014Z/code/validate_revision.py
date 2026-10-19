"""Validate only revised artifacts against already frozen source tables."""
import os
os.environ.update(CUDA_VISIBLE_DEVICES='',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from pathlib import Path
import json,csv,hashlib,re,time,datetime,resource,shutil,collections
import numpy as np
R=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z')
V=R/'visual_revision_20261014T025700Z'
D=Path('/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z')
H=D.parent
t=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rows(p):
 with Path(p).open() as f:return list(csv.DictReader(f))
def put(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
rec=json.loads((V/'revision_record.json').read_text());checks={}
for x in rec['source_files']:assert sha(x['path'])==x['sha256']
checks['all_registered_primary_inputs_unchanged']=True
oldmanifest=json.loads((V/'before/payload_manifest.json').read_text());oldentries={x['relative_path']:x for x in oldmanifest['files']}
for x in oldmanifest['files']:
 rel=x['relative_path']
 if rel.startswith('tables/') or rel.startswith('provenance/') or rel.startswith('code/') or rel in ['completion_receipt.json','derived_geometry.npz','text_examples.jsonl','text_examples_cn.md']:
  assert sha(D/rel)==x['sha256'],rel
checks['all_original_tables_geometry_text_code_and_receipts_unchanged']=True
archive=H/'results_20261014T020014Z_portable.zip';assert sha(archive)=='2411367ff2f533e7e98bc7f64699db4a9dcac01cd898c28049a633033bfaca75'
checks['previously_pushed_zip_unchanged']=True
npz=np.load(R/'derived_geometry.npz');g={k:npz[k] for k in ['Q','h','layers','L','L_raw','p','p_raw']};npz.close();q=g['Q'];ids=np.flatnonzero(q);h=g['h'][1];layers=g['layers'];assert len(ids)==15537
comparison=rows(D/'tables/figure3_coordinate_comparison_source.csv');oldpoints=rows(R/'figure3_source.csv');assert len(comparison)==len(oldpoints)==15537
for a,b,f in zip(comparison,oldpoints,ids):
 assert int(a['feature'])==int(b['feature'])==f and int(a['h'])==int(b['h'])==h[f]
 assert float(a['x_for_plot'])==float(b['x_for_plot'])
 assert float(a['L_train'])==float(g['L'][f]) and float(a['L_raw'])==float(g['L_raw'][f])
checks['figure3_identical_15537_ids_h_jitter_both_coordinates']=True
means=rows(D/'tables/group_mean_p_source.csv');origmeans=rows(R/'hierarchy_mean_p.csv');assert len(means)==168
for a in means:
 k='V_train_normalized' if a['coordinate']=='train' else 'V_raw_coordinate';hh=int(a['h']);l=int(a['model_layer']);b=next(b for b in origmeans if b['condition']==k and int(b['h'])==hh);assert float(a['mean_p'])==float(b[f'mean_p_layer{l}'])
for key in ['train','raw']:
 for hh in range(6):assert np.isclose(sum(float(a['mean_p']) for a in means if a['coordinate']==key and int(a['h'])==hh),1)
checks['group_mean_p_all_168_cells_match_original_and_sum1']=True
features=rows(D/'tables/peak_feature_labels_posthoc.csv');comp=rows(D/'tables/peak_composition_posthoc.csv');assert len(features)==31074 and len(comp)==36
for key,member in [('train','p'),('raw','p_raw')]:
 p=g[member];assert np.allclose(p[:,q].sum(0),1)
 subset=[a for a in features if a['coordinate']==key];assert [int(a['feature']) for a in subset]==ids.tolist()
 for a,f in zip(subset,ids):
  peak=int(layers[p[:,f].argmax()]);assert int(a['maximum_model_layer'])==peak and int(a['exact_maximum_ties'])==1
 for hh in range(6):
  at=[a for a in subset if int(a['h'])==hh];n=len(at);counts=collections.Counter(a['peak_class'] for a in at)
  cc=[a for a in comp if a['coordinate']==key and int(a['h'])==hh]
  assert sum(int(a['feature_count']) for a in cc)==n
  assert np.isclose(sum(float(a['share']) for a in cc),1)
  for a in cc:assert int(a['n_features'])==n and int(a['feature_count'])==counts[a['peak_class']] and float(a['share'])==counts[a['peak_class']]/n and a['analysis_role']=='POST_HOC_DESCRIPTIVE'
checks['posthoc_peaks_unique_and_counts_proportions_exact']=True
zero=rows(D/'tables/h0_individual_source.csv');top=rows(D/'tables/h5_curves_source.csv');assert len(zero)==560 and len(top)==56
assert sorted({int(a['feature']) for a in zero})==np.flatnonzero(q&(h==0)).tolist()
assert sorted({int(a['feature']) for a in top})==[937,3461]
for rr in [zero,top]:
 for a in rr:
  p=g['p'] if a['coordinate']=='train' else g['p_raw'];j=np.flatnonzero(layers==int(a['model_layer']))[0];assert float(a['p'])==float(p[j,int(a['feature'])])
checks['h0_all20_h5_both_and_all_p_cells_exact']=True
freq=rows(D/'tables/frequency_comparison_25cells_source.csv');orig=[a for a in rows(R/'frequency_overlap_comparison.csv') if a['graph']=='V'];assert len(freq)==len(orig)==25
statuses=collections.Counter(a['status'] for a in freq);assert statuses=={'COMPARABLE_RANGE':11,'NO_GROUP':10,'NO_OVERLAP':1,'SMALL_N':3}
for a,b in zip(freq,orig):
 for k in b:assert a[k]==b[k]
 valid=a['status'] in ['COMPARABLE_RANGE','FIXED_FREQUENCY_LOCAL'];assert (a['display_valid']=='True')==valid
 assert a['display_delta_median_L']==(a['delta_median_L'] if valid else '')
checks['frequency_25_original_cells_invalid_not_displayed_as0']=True
# Verify source labels/units and absence of deprecated plot labels.
script=(V/'code/revise_figures.py').read_text();assert 'V 激活频率：' in script and 'pV' not in script
assert 'A→更常见的 u' in script
checks['unambiguous_chinese_frequency_p_and_arrow_labels']=True
# Literal local Markdown paths are checked; rendering was separately reviewed.
files=['summary_cn.md','detailed_cn.md','figures_cn.md','tables_cn.md','README_cn.md','provenance/visual_revision_scope_cn.md'];missing=[]
for rel in files:
 s=(D/rel).read_text()
 for target in re.findall(r'\]\(([^)]+)\)',s):
  if target.startswith('/'):p=Path(target.split('#')[0]);
  else:continue
  if not p.exists() and p not in [D/'provenance/visual_revision_record.json',D/'visual_revision_receipt.json']:missing.append((rel,target))
assert not missing,missing
summary=(D/'summary_cn.md').read_text();assert re.findall(r'^## (.+)$',summary,re.M)==['目的','方法','现象','解释','结论'];assert len(re.findall(r'^### 认识',summary,re.M))==2
checks['report_local_links_and_requested_structure']=True
figurefiles=[f for f in (D/'figures').iterdir() if f.suffix in ['.png','.pdf','.svg']];assert len(figurefiles)==36
for f in figurefiles:assert sha(f)==sha(V/'figures'/f.name)
checks['12_final_figures_in_three_formats_copied_exactly']=True
# All 12 final renders were viewed in the assistant turn; h0 was re-viewed after its layout repair.
rec['delivery_check_retry_note']='Initial delivery check found two completion artifacts not yet written; completion-artifact creation and final link checks reordered. No numeric/source check failed. First check runtime not individually retained; revision wall time includes it.'
rec.update(status='COMPLETE',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,visual_review={'status':'ALL_12_FINAL_PNGS_VIEWED','figure6':'Colorbar moved outside panels and final PNG reviewed; model28 unobscured','font_glyph_check':'all text supported by NotoSansCJKsc','changes':'layout and labels plus user-requested paired/full-cell plots; no scientific source edits'},reasoning_audit={'skill':'research-reasoning-auditor','boundary':'L is a weighted average only; h/frequency/model layer/p are distinct; frequency cells are not adjusted effects; peak categories post hoc not functional; no shared/expert benefit claim'},validation_seconds=time.monotonic()-t,validation_max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
rec['figure_hashes']=[{'relative_path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(figurefiles)]
put(V/'revision_record.json',rec);shutil.copy2(V/'revision_record.json',D/'provenance/visual_revision_record.json')
newbytes=sum(p.stat().st_size for p in V.rglob('*') if p.is_file() and 'before' not in p.parts)
start=datetime.datetime.fromisoformat(rec['created_utc']);end=datetime.datetime.fromisoformat(rec['completed_utc'])
receipt={'revision_id':rec['revision_id'],'status':'COMPLETE','kind':'user_authorized_visual_and_report_revision_with_posthoc_peak_description','primary_run_unchanged':str(R),'delivery_root':str(D),'completed_utc':rec['completed_utc'],'revision_wall_seconds_since_initial_record_including_writing_and_review':(end-start).total_seconds(),'render_and_posthoc_seconds':rec['render_seconds'],'layout_only_fix_seconds':rec['layout_only_fix']['seconds'],'validation_seconds':rec['validation_seconds'],'max_process_rss_bytes':max(rec['max_rss_bytes'],rec['layout_only_fix']['max_rss_bytes'],rec['validation_max_rss_bytes']),'execution_revision_bytes_including_font_excluding_before_backup':newbytes,'before_backup_bytes':sum(p.stat().st_size for p in (V/'before').rglob('*') if p.is_file()),'gpu_jobs':0,'cache_scans':0,'inference':False,'training':False,'primary_graph_or_frequency_recomputation':False,'posthoc_peak_classification':True,'all_checks':checks,'old_zip_sha256':sha(archive),'no_commit_push':True,'scientific_state_unchanged':True,'font_not_in_delivery':True,'stop':'图表和报告修订完成；不启动新实验'}
put(V/'visual_revision_receipt.json',receipt);shutil.copy2(V/'visual_revision_receipt.json',D/'visual_revision_receipt.json')
assert (D/'provenance/visual_revision_record.json').exists() and (D/'visual_revision_receipt.json').exists()
# Refresh delivery manifest with file-level origins, preserving unchanged origins.
newentries=[]
for p in sorted(D.rglob('*')):
 if not p.is_file() or p.name=='payload_manifest.json':continue
 rel=str(p.relative_to(D));digest=sha(p);old=oldentries.get(rel)
 if old and old['sha256']==digest:origin=old['origin']
 elif (V/rel).exists() and sha(V/rel)==digest:origin=str(V/rel)
 elif rel=='provenance/visual_revision_record.json':origin=str(V/'revision_record.json')
 elif rel=='provenance/visual_revision_scope_cn.md':origin=str(V/'visual_revision_scope_cn.md')
 else:raise AssertionError(('unknown origin',rel))
 assert not p.name.endswith('.otf')
 newentries.append({'relative_path':rel,'bytes':p.stat().st_size,'sha256':digest,'origin':origin,'scope':'derived reports/figures/tables/text/provenance; peak labels and proportions explicitly post hoc; no cache/checkpoint/font'})
put(D/'payload_manifest.json',{'revision_id':rec['revision_id'],'primary_run':str(R),'files':newentries,'prior_manifest':str(V/'before/payload_manifest.json'),'old_committed_zip_unchanged':True,'complete':True})
print(json.dumps(receipt,ensure_ascii=False,indent=2))
