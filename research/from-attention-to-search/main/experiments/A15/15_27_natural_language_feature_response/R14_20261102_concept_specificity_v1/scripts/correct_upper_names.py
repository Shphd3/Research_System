from pathlib import Path
import json,hashlib,datetime,shutil,re
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response')/E.name
assert (E/'terminal_receipt.json').exists();assert len(list((E/'analysis').glob('condition_*.npz')))==167
V=E/'versions/data_v1p2';V.mkdir(parents=True,exist_ok=False)
for n in ['data','scripts','audit']:shutil.copytree(E/n,V/n,ignore=shutil.ignore_patterns('*.pyc','__pycache__'))
for n in ['freeze.json','manifest.json','terminal_receipt.json','forward_cpu.log']:shutil.copy2(E/n,V/n)
shutil.move(E/'analysis',V/'analysis');(E/'analysis').mkdir();(V/'cache').mkdir()
for n in ['merged.npz','vectors.npz','full_first_logp.npy']:shutil.move(E/'cache'/n,V/'cache'/n)
(E/'terminal_receipt.json').unlink()
changes={
 'A cellular structure performs a biochemical function.':'A specialized part inside a cell performs a biochemical task.',
 'This mature human blood cell lacks a nucleus and carries oxygen using hemoglobin.':'This mature human cell lacks a nucleus and carries oxygen using hemoglobin.',
 'This blood cell has a nucleus and participates in defense against infectious agents.':'This nucleated cell circulates in vertebrates and participates in defense against infectious agents.',
 'An enzyme builds a nucleic acid strand from a template.':'A molecule accelerates the assembly of a nucleic acid strand along a template without being consumed.',
 'This enzyme extends a new genome copy using deoxyribonucleotides during replication.':'This molecule extends a new genome copy using deoxyribonucleotides during replication.',
 'This enzyme makes a ribonucleotide transcript from a genomic template.':'This molecule makes a ribonucleotide transcript from a genomic template.',
 'A real function relates a positive quantity to another number.':'An input value is assigned exactly one output value according to a fixed mathematical rule.',
 'A number lies on the real number line.':'A numerical quantity can be located as a point on a continuous number line.',
 'A nonconstant expression is a polynomial in one variable.':'A nonconstant expression in one variable is a finite sum of terms whose powers are nonnegative integers.',
 'An interaction exerts a mechanical force on an object.':'An interaction pushes or pulls on an object and can change its motion.',
 'At a sliding contact, this force opposes relative tangential motion of the surfaces.':'At a sliding contact, this tangential interaction opposes relative motion of the surfaces.',
 'A pressure difference in a fluid exerts this upward force equal to the weight of displaced fluid.':'A pressure difference in a fluid produces an upward push equal to the weight of the displaced fluid.',
 'Two solid surfaces rub, producing a tangential force that resists their sliding.':'Two solid surfaces rub, producing a tangential resistance to sliding.',
 'An immersed object experiences a resultant force because fluid pressure is greater at its bottom.':'An immersed object experiences a net upward push because fluid pressure is greater at its bottom.'}
f=E/'scripts/families.py';source=f.read_text()
for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
f.write_text(source)
load=lambda n:[json.loads(l) for l in (E/'data'/n).read_text().splitlines()];rr=load('prefixes.jsonl');pp=load('positions.jsonl');ss=load('sequences.jsonl');tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');affected=[];indices=set();seqs=[];ledger=[]
for r in rr:
 old=r['prefix'];new=old
 for a,b in changes.items():new=new.replace(a,b)
 if old==new:continue
 affected.append(r['prefix_id']);r['prefix']=new;pre=tok.encode(new,add_special_tokens=False).ids;r['prefix_token_ids']=pre;r['prefix_length']=len(pre)
 ledger.append({'prefix_id':r['prefix_id'],'family_id':r['family_id'],'before':old,'after':new,'reason':'literal U name, identified by exhaustive pre-outcome text scan;A/B candidates unchanged'})
 for key,c in r['candidate_map'].items():
  ids=tok.encode(new+c['answer'],add_special_tokens=False).ids;assert ids[:len(pre)]==pre and ids[len(pre):]==c['token_ids'];sq=next(x for x in ss if x['sequence_id']==c['sequence_id']);sq['token_ids']=ids;sq['selected']=[(len(pre)-1+i,ix) for i,ix in enumerate(c['position_indices']) if key=='U' or i!=0];seqs.append(sq['sequence_id'])
  oldcache=E/'cache'/(sq['sequence_id']+'.npz');assert oldcache.exists();shutil.move(oldcache,V/'cache'/oldcache.name)
  for ai,ix in enumerate(c['position_indices']):
   indices.add(ix)
   if ai==0 and key!='U':continue
   pp[ix]['model_position']=len(pre)-1+ai;pp[ix]['visible_token_ids']=pre+c['token_ids'][:ai]
assert len(affected)==20
for r in rr:
 for k in ['U','V','A','B']:assert not re.search(r'(?<!\w)'+re.escape(r[k])+r'(?!\w)',r['prefix'],re.I),(r['prefix_id'],k)
for n,rs in [('prefixes.jsonl',rr),('positions.jsonl',pp),('sequences.jsonl',ss)]: (E/'data'/n).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rs))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
patch={'version':'1.3','parent_version':'1.2','parent_root':str(V),'parent_freeze_sha256':sha(V/'freeze.json'),'affected_prefixes':affected,'affected_position_indices':sorted(indices),'affected_sequences':seqs,'edits':ledger,'selection':'all literal candidate-name matches from text,not model outcomes','old_results_available':True,'old_numeric_scores_used_to_select_correction':False,'original_unique_conditions':167}
(E/'audit/upper_name_correction_patch.json').write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n')
p=E/'amendments.md';p.write_text(p.read_text()+'\n## A10 — complete all-candidate name guard; data1.3\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\nThe original audit prohibited literal A/B names but omitted U/V. Exhaustive text-only scan found20prefixes in7evaluation families with literal U; no A/B or V match. v1.2 had completed167conditions, but no numerical scores were read to select edits. Preserve all original data, source, raw167conditions, affected caches and terminal receipt under versions/data_v1p2. Replace ALL20literal-name prefixes by operational descriptions; same48families,288prefixes,U/V/A/B answers,2640positions,source definitions,split,frequency groups,basis,conditions and metrics. Regenerate only80affected model sequences and their coefficients; qualify reuse of1072unchanged sequence caches by exact input IDs/indices, original frozen CPU model and parent manifest. Re-encode joint coefficients with same1024padding and require unaffected z and h bit equality. Recompute all167interventions at affected scoring positions, reuse unchanged per-position raw scores only after untouched native replay matches exactly. Reaggregate all family metrics. Old raw outputs remain identifiable v1.2, not mixed into current names/coordinates. No dataset selection based on full-model success, no additional family or classifier. This is a data-contract implementation repair, not positive-result search.\n')
fr=json.load(open(E/'freeze.json'));fr['sha256']={p:sha(p) for p in fr['sha256']};(E/'freeze.json').write_text(json.dumps(fr,indent=2)+'\n');m=json.load(open(E/'manifest.json'));m['data_version']='1.3';m['sha256']=fr['sha256'];m['parent_v1p2']=str(V);m['patch']='audit/upper_name_correction_patch.json';(E/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('CORRECTION',len(affected),'prefixes',len(indices),'positions',len(seqs),'sequences;all4namesnowabsent')
