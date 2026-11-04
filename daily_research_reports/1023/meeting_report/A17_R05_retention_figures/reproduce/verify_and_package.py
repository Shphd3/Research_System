"""Verify presentation against saved per-answer results; no model loading."""
from pathlib import Path
import csv,json,math,hashlib,re,shutil,zipfile,datetime
from collections import defaultdict
import xml.etree.ElementTree as ET
from PIL import Image
F=Path(__file__).resolve().parent;E=F.parents[1];S=Path('/data/250010109/Research_System');M=S/'daily_research_reports/1023/meeting_report';D=M/'A17_R05_retention_figures';C=S/'Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023'
checks={};raw=[]
def mark(k,b):
 assert b,k
 checks[k]=True
def read(p):return json.load(open(p))
def rows(p):return list(csv.DictReader(open(p)))
def ev(p):return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def behavior(p):
 x=read(p);rr=x['records'];mark('records_'+str(p),len(rr)==len({r['record_id'] for r in rr})==1600)
 mark('correct_'+str(p),all(r['correct']==float(r['prediction_id']==r['target_id']) for r in rr))
 parts={m:[r for r in rr if r['mode']==m] for m in [1,2]};mark('denominators_'+str(p),all(len(v)==800 for v in parts.values()))
 old,new=[100*sum(r['correct'] for r in parts[m])/800 for m in [1,2]];cells=defaultdict(list)
 for r in parts[2]:cells[r['panel'],r['command']].append(r)
 mark('four_new_cells_'+str(p),len(cells)==4 and all(len(v)==200 for v in cells.values()))
 minimum=min(100*sum(r['correct'] for r in v)/200 for v in cells.values());raw.append(ev(p));return old,new,minimum
plan=read(D/'figure_plan_and_sources.json')
for x in plan['source_files']:mark('source_unchanged_'+x['role'],ev(Path(x['path']))['sha256']==x['sha256'])
t1=rows(D/'tables/table1_main_experiment_21.csv');mark('all7x3',len(t1)==21 and len({(r['training_order'],r['method']) for r in t1})==21)
for r in t1:
 p=E/f"runs/A/seed_{r['training_order']}/{r['method']}/eval_01200.json";a,b,c=behavior(p);mark('table1_raw_'+r['training_order']+r['method'],abs(a-float(r['old_accuracy_pct']))<1e-10 and abs(b-float(r['new_accuracy_pct']))<1e-10 and (c>=95)==(r['new_learning_qualified']=='True'))
 u=next(q for q in t1 if q['training_order']==r['training_order'] and q['method']=='U');mark('relativeU_'+r['training_order']+r['method'],abs(float(r['old_minus_U_pp'])-(a-float(u['old_accuracy_pct'])))<1e-10)
f1=rows(D/'plot_data/figure1_6.csv');mark('figure1_all6',len(f1)==6)
for r in f1:mark('Cnet_ratio_'+r['training_order']+r['method'],math.isclose(float(r['C_net_over_C0_pct']),100*float(r['C_endpoint_net_norm'])/float(r['C0_joint_frobenius_norm']),rel_tol=1e-12))
f2=rows(D/'plot_data/figure2_TS_21.csv');mark('figure2_all21',len(f2)==21 and all(r['arm']=='TS' for r in f2))
for r in f2:
 p=Path(r['reuse_source']) if r['reuse_source'] else E/f"analysis/A_residual_spectral_20261023/readouts/TS_{r['seed']}_{r['kind']}_{r['label']}.json";a,b,_=behavior(p);mark('figure2_raw_'+r['seed']+r['kind']+r['label'],abs(a-float(r['mode1_accuracy_pct']))<1e-10 and abs(b-float(r['mode2_accuracy_pct']))<1e-10)
t2=rows(D/'tables/table2_residual_interventions_9.csv');mark('table2_nine',len(t2)==9)
for r in t2:
 seed=r['training_order'];rr=[x for x in f2 if x['seed']==seed and (x['kind']==r['condition'] or r['condition']=='endpoint' and x['kind']=='dose')];base=next(x for x in f2 if x['seed']==seed and x['kind']=='dose');mark('table2_counts_'+seed+r['condition'],len(rr)==(5 if r['condition']=='random' else 1))
 for pre,field in [('old','mode1_accuracy_pct'),('new','mode2_accuracy_pct')]:
  vals=[float(x[field]) for x in rr];summary={'mean':math.fsum(vals)/len(vals),'min':min(vals),'max':max(vals)}
  for stat,v in summary.items():mark('table2_'+seed+r['condition']+pre+stat,abs(v-float(r[f'{pre}_accuracy_{stat}_pct']))<1e-10 and abs(v-float(base[field])-float(r[f'{pre}_change_{stat}_pp']))<1e-10)
aligned=rows(C/'A_residual_spectral_20261023/tables/aligned_spectra_behavior_216.csv');f3=rows(D/'plot_data/figure3_TS_27.csv');mark('backup27',len(f3)==27)
for r in f3:
 rr=[z for z in aligned if z['seed']==r['seed'] and z['arm']=='TS' and z['step']==r['step']];mark('backup_max_'+r['seed']+r['step'],len(rr)==4 and abs(max(abs(float(z['W_sigma1_relative_change'])) for z in rr)-float(r['max_matrix_sigma1_relative_change']))<1e-12 and abs(max(1-float(z[k]) for z in rr for k in ['W_left_mean_cos2','W_right_mean_cos2'])-float(r['max_top16_mean_cos2_loss']))<1e-12)
rank=rows(C/'A_residual_spectral_20261023/tables/actual_norm_rank_matches_120.csv');sel=[r for r in rank if r['arm']=='TS'];mark('all60_TS_rank_norm_matches',len(sel)==60 and all(r['matched']=='True' and r['target_rank']==r['random_rank']=='32' and float(r['relative_mismatch'])<.001 for r in sel))
# Additional text-only local-effect evidence used by the revised conclusion.
local=rows(C/'A_residual_spectral_20261023/tables/fixed_inputs_432.csv')
old16=[r for r in local if r['arm']=='TS' and r['mode']=='1' and r['step']=='16']
r=[100*float(x['delta_R_over_W0_output']) for x in old16];c=[100*float(x['delta_C_over_W0_output']) for x in old16]
mark('fixed_old_input_text_values',len(old16)==12 and round(min(r),2)==9.53 and round(max(r),2)==22.04 and round(min(c),4)==.0040 and round(max(c),4)==.0436)
# No hidden jitter: retain exact coordinate groups and all five control labels.
groups=[]
for seed in ['29','43','71']:
 g=defaultdict(list)
 for r in f2:
  if r['seed']==seed and r['kind']=='random':g[float(r['mode2_accuracy_pct']),float(r['mode1_accuracy_pct'])].append(int(r['label'])-2700)
 mark('five_randoms_visible_'+seed,sorted(i for v in g.values() for i in v)==[1,2,3,4,5]);groups.append({'seed':seed,'coordinate_groups':[{'new_accuracy_pct':k[0],'old_accuracy_pct':k[1],'R_indices':v} for k,v in g.items()]})
# Format and rendering accounting; rendered plots were also visually opened.
for p in (D/'figures').glob('*.svg'):
 root=ET.parse(p).getroot();texts=[e for e in root.iter() if e.tag.endswith('text')];mark('editable_text_'+p.name,len(texts)>15)
for p in (D/'figures').glob('*.png'):
 im=Image.open(p);mark('high_resolution_'+p.name,im.width>=3800 and abs(im.info.get('dpi',[0])[0]-320)<1)
mark('no_table_images',not any(p.suffix in ['.png','.pdf','.svg'] for p in (D/'tables').iterdir()))
mark('only_three_plot_variants',len(list((D/'figures').glob('*.png')))==3)
# Curated sources and scripts only; no font binary/model/readout payload in delivery.
R=D/'reproduce';R.mkdir(exist_ok=True)
for n in ['build_figures.py','write_brief.py','verify_and_package.py']:shutil.copy2(F/n,R/n)
shutil.copy2(F/'fonts/provenance.json',R/'font_provenance.json');shutil.copy2(F/'input_access.json',D/'input_access.json')
verification={'status':'PASS','checks_count':len(checks),'checks':checks,'raw_record_sources':raw,'random_coordinate_groups':groups,'visual_review':'All three final PNGs opened;axes,units,labels,overlapping controls andtable-free delivery inspected.','scope':'savedresults only; no checkpoint/modelload,newforward,training,or endpointselection','global_navigation':'two preexisting unrelated findings remain; no global PASS claimed'}
(D/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
manifest={'created_at_beijing':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'scope':'revised user conclusion presentation: two main figures,one optional backup,two Markdown/CSV result tables','speaking_entries':[ev(M/'meeting_brief_A17_R05_retention_cn.md'),ev(M/'meeting_brief_A17_R05_retention.md')],'sources':plan,'verification':ev(D/'verification.json'),'files':[ev(p) for p in sorted(D.rglob('*')) if p.is_file() and p.name not in ['manifest.json','delivery_check.json']],'source_mutation':False,'training_or_forward':False,'publication':'local delivery only; no commit/push'}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Check local link targets after manifest creation. Resolve optional line suffixes.
allmd=[*D.rglob('*.md'),M/'meeting_brief_A17_R05_retention_cn.md',M/'meeting_brief_A17_R05_retention.md'];missing=[]
for p in allmd:
 for t in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if t.startswith(('http://','https://','#')):continue
  t=re.sub(r':\d+$','',t.split('#')[0])
  if t and not (p.parent/t).exists():missing.append([str(p),t])
assert not missing,missing
(D/'delivery_check.json').write_text(json.dumps({'status':'PASS','all_local_markdown_link_targets_exist':True,'three_final_plots_visually_checked':True,'two_tables_text_only':True,'raw_checks':len(checks),'no_new_training_or_forward':True},indent=2)+'\n')
zip_path=E/'exports/A17_R05_conclusion_figures_20261023.zip';zip_path.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in [M/'meeting_brief_A17_R05_retention_cn.md',M/'meeting_brief_A17_R05_retention.md']+sorted(p for p in D.rglob('*') if p.is_file()):z.write(p,p.relative_to(M))
# Verify archive entries match delivered bytes, without changing original results.
with zipfile.ZipFile(zip_path) as z:
 for n in z.namelist():assert z.read(n)==(M/n).read_bytes(),n
(F/'delivery_receipt.json').write_text(json.dumps({'archive':ev(zip_path),'checks_count':len(checks),'canonical_brief':str(M/'meeting_brief_A17_R05_retention_cn.md'),'files_in_archive':len(zipfile.ZipFile(zip_path).namelist()),'status':'PASS'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(read(F/'delivery_receipt.json'),ensure_ascii=False))
