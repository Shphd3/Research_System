from common import *
from tokenizers import Tokenizer
import copy,random,collections,re,shutil
assert not (R/'data/panel.jsonl').exists()
for folder in ['data','cache','results','tables','figures','evidence','versions']:(R/folder).mkdir(exist_ok=True)
C.mkdir(parents=True,exist_ok=True)
cfg=json.load(open(OLD/'config.json'));tok=Tokenizer.from_file(str(Path(cfg['model'])/'tokenizer.json'))
enc=lambda s:tok.encode(s,add_special_tokens=False).ids
old=[x for x in rows(OLD/'data/panel_portable.jsonl') if x['condition'].startswith('main')]
by={p['id']:p for p in old};families=json.load(open(OLD/'data/families.json'));fmeta={x['family']:x for x in families};held=cfg['heldout'];discovery=cfg['discovery'];selected=[next(f for f in held if fmeta[f]['template']=='H'+str(k)) for k in range(1,7)]
oldprotect={}
for root in [OLD,OLD_C]:
 for f in root.rglob('*'):
  if f.is_file() and '__pycache__' not in f.parts:oldprotect[str(f)]=sha(f)
for f in [(OLD_C/'anchor.md').resolve(),(OLD_C/'anchor_cn.md').resolve(),P/'main/focus/focus_remote_target_near_competitor_composition.md',P/'main/focus/focus_remote_target_near_competitor_composition_cn.md',SYS/'daily_research_reports/1104/20261104_R19_remote_target_competitor_composition.zip']:oldprotect[str(f)]=sha(f)
dump(R/'evidence/R19_protected_snapshot.json',dict(UTC=now(),files=oldprotect))
shutil.copyfile('/tmp/r20_inputs_20261104.json',R/'evidence/input_assets.json')
shutil.copyfile(OLD/'data/candidates.json',R/'data/R19_candidates.json');shutil.copyfile(OLD/'data/families.json',R/'data/families.json')
frequencies={}
for site in SITES:
 shutil.copyfile(OLD/f'data/{site}_reference_frequency.csv',R/f'data/{site}_reference_frequency.csv');shutil.copyfile(OLD/f'data/{site}_reference_bins.json',R/f'data/{site}_reference_bins.json')
 ff=list(csv.DictReader(open(R/f'data/{site}_reference_frequency.csv')));edges=[35,70] if site=='ATTN_SAE' else [33,62];counts=collections.Counter()
 for i,row in enumerate(ff):
  assert int(row['atom'])==i;cnt=int(row['positive_positions']);doc=int(row['document_coverage']);group='zero' if cnt==0 else 'insufficient' if cnt<20 or doc<5 else 'low' if cnt<edges[0] else 'middle' if cnt<edges[1] else 'high';assert group==row['group'];assert abs(float(row['frequency'])-cnt/38400)<1e-12;counts[group]+=1
 ss=cfg['sites'][site]
 for key in ['reference_frequency','reference_sparse','reference_metadata']:
  path=ss[key+'_csv'] if key=='reference_frequency' else ss[key+'_cache'] if key=='reference_sparse' else ss[key]
  assert sha(path)==ss[key+'_sha256']
 frequencies[site]=dict(reference_documents=300,reference_positions=38400,bins=edges,groups=dict(counts),copied_csv_sha256=sha(R/f'data/{site}_reference_frequency.csv'),source_hashes_current=True,source_count_and_doc_replay_receipts=[str(OLD/'evidence/reference_validation.json'),str(OLD/'evidence/reference_document_coverage_check.json')])
dump(R/'evidence/frequency_validation.json',dict(UTC=now(),sites=frequencies))
def split(p):
 t=p['text'];start,end=p['evidence_char_span'];a=t.rfind('\n',0,start)+1;b=t.index('\n',end)+1;q=fmeta[p['family']]['question_template'].format(c=fmeta[p['family']]['container']);assert t.endswith(q);before=t[:a];fact=t[a:b];after=t[b:len(t)-len(q)];assert before.startswith('Record:\n');return before,fact,after,q
bank=['Work continued.\n','People waited.\n','Everyone paused.\n','The meeting ended.\n','The work continued.\n','Everyone waited calmly.\n']
for noun in ['office','building','hallway','corridor','library','garden','classroom','street']:
 for adj in ['quiet','bright','warm','cool','clean','dim','empty','spacious']:
  bank.extend([f'The {noun} was {adj}.\n',f'The {noun} was very {adj}.\n',f'The {noun} was {adj} during lunch.\n',f'The {noun} was {adj} throughout the afternoon.\n'])
pool=collections.defaultdict(list)
for s in bank:pool[len(enc(s))].append(s)
blocked={x[k] for x in families for k in ['A','B','container']}
bank=[s for s in bank if not any(re.search(r'\b'+re.escape(w)+r'\b',s,re.I) for w in blocked)]
pool=collections.defaultdict(list)
for s in bank:pool[len(enc(s))].append(s)
def rewrite_line(line,f):
 n=len(enc(line));assert pool[n],(n,line)
 k=int(hashlib.sha256((f+'|'+line).encode()).hexdigest()[:12],16)%len(pool[n]);return pool[n][k]
def make(source,text,frame,d,offset=0):
 p=copy.deepcopy(source);p['id']=cid(frame,p['family'],d,p['gold']);p['source_R19_id']=source['id'];p['condition']=frame;p['position_offset']=offset;p['text']=text;p['split']='heldout';p['provenance']='NEW_FORWARD';item=p['evidence_item'];where=text.index(item,text.index('Record:\n'));start,end=where,where+len(item);e=tok.encode(text,add_special_tokens=False);positions=[i for i,(a,b) in enumerate(e.offsets) if b>start and a<end];p.update(token_ids=e.ids,offsets=e.offsets,evidence_char_span=[start,end],evidence_token_positions=positions,evidence_token_ids=[e.ids[i] for i in positions],evidence_last_position=max(positions),target_position=len(e.ids)-1,target_token_id=e.ids[-1],actual_distance=len(e.ids)-max(positions)-2)
 assert p['actual_distance']==d and p['target_token_id']==25
 p['position_id_target']=p['target_position']+offset;p['position_id_evidence']=p['evidence_last_position']+offset
 for c in p['candidates']:
  full=enc(text+c['text']);assert full[:len(e.ids)]==e.ids and full[len(e.ids):]==c['token_ids'];c['full_ids']=full
 for c in p['candidates']:assert len(re.findall(r'\b'+re.escape(c['item'])+r'\b',text))==int(c['item']==item),(p['id'],c['item'])
 return p
base=[]
for p in old:
 p=copy.deepcopy(p);p.update(source_R19_id=p['id'],provenance='R19_REUSE',condition='baseline',position_offset=0,position_id_target=p['target_position'],position_id_evidence=p['evidence_last_position']);base.append(p)
new=[];construction=[]
for f in held:
 inventories=[]
 for d in DISTS:
  a=by[f'{f}_main{d}_A'];before,fact,after,q=split(a);inventories.append(collections.Counter(before.splitlines(True)[1:]+after.splitlines(True)))
 assert inventories[0]==inventories[1]==inventories[2]
 for g in 'AB':
  far=by[f'{f}_main128_{g}'];bf,ff,af,qf=split(far)
  for d in DISTS:
   source=by[f'{f}_main{d}_{g}'];before,fact,after,q=split(source)
   reverse='Record:\n'+''.join(before.splitlines(True)[1:][::-1])+fact+''.join(after.splitlines(True)[::-1])+q
   content='Record:\n'+''.join(rewrite_line(s,f) for s in before.splitlines(True)[1:])+fact+''.join(rewrite_line(s,f) for s in after.splitlines(True))+q
   for frame,text in [('reverse',reverse),('content',content)]:
    pp=make(source,text,frame,d);assert len(pp['token_ids'])==320 and pp['evidence_last_position']==source['evidence_last_position'];new.append(pp)
   if d<128:
    pp=make(source,bf+ff+after+q,'fixed_e',d);assert pp['evidence_last_position']==190 and pp['target_position']==190+d+1;new.append(pp)
   if f in selected:new.append(make(source,source['text'],'pos64',d,64))
 construction.append(dict(family=f,template=fmeta[f]['template'],main_filler_multiset_identical=True,main_answer_position=319,main_evidence_positions=[302,254,190],fixed_evidence=190,fixed_e_answer_positions=[207,255,319],question_fixed=True))
assert len(new)==228 and len(base)==144
panel=base+new;jsonl(R/'data/panel.jsonl',panel);jsonl(R/'data/new_panel.jsonl',new);table(R/'tables/construction_audit.csv',construction)
maps={}
for frame,fs in [('baseline',discovery+held),('reverse',held),('content',held),('fixed_e',held),('pos64',selected)]:maps[frame]={f:{str(d):{g:cid(frame,f,d,g) for g in 'AB'} for d in DISTS} for f in fs}
dump(R/'data/condition_mapping.json',maps)
smoke=[cid(frame,held[0],16,'A') for frame in ['reverse','content','fixed_e','pos64']];calibration=[f'{f}_main16_A' for f in selected]
cfg.update(experiment='R20_DISTANCE_COMPOSITION',UTC=now(),local_time=local_now(),seed=SEED,old_root=str(OLD),old_canonical=str(OLD_C),primary_heldout=held,discovery=discovery,supplemental_frames=['reverse','content','fixed_e','pos64'],position_shift_families=selected,new_forward_rows=228,old_main_rows=144,panel_rows=len(panel),smoke_ids=smoke,calibration_ids=calibration,primary=['H1_member_retention_ge_0p9','H2_relative_fact_norm_equivalent','H3_relative_fact_norm_decreases_20pct'],retention_threshold=.9,equivalence_bounds=[.8,1.25],primary_holm_family=6,bootstrap_draws=8192,opportunity_null_draws=512,task_frequency_prior=32,threshold_band=.25,wall_ceiling_per_stage=1800,training=False,intervention=False,scientific_acceptance='Unknown',authorization='Current user explicitly authorizes complete reanalysis, necessary bounded forward controls and result delivery without intermediate approval')
dump(R/'config.json',cfg);dump(R/'evidence/construction.json',dict(UTC=now(),status='PASS',rows=len(panel),old_main_rows=144,new_forward_rows=228,counts=dict(collections.Counter(x['condition'] for x in new)),alias_reused_far=24,smoke=smoke,position_shift_families=selected,all_role_token_checks=True,old_data_reexposed=True))
print('PREPARED',len(panel),dict(collections.Counter(x['condition'] for x in new)),local_now())
