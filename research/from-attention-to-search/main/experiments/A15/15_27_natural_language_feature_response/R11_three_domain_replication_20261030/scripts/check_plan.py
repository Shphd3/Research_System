"""Read-only R11 design consistency checks; no model/data forwarding."""
from pathlib import Path
import json,re,hashlib
W=Path(__file__).resolve().parents[1];R=W.parents[5]
c=json.loads((W/'config.proposed.json').read_text());f=json.loads((W/'legacy16_frozen.json').read_text());checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)
n=sum(c['documents_per_domain'].values());check('150new documents per domain /450total',n==150 and len(c['domains'])*n==450==c['study_documents'])
for split,k in c['documents_per_domain'].items():
    check(split+' genre quota',sum(c['genre_per_domain'][split].values())==k)
    check(split+' topic quota',c['topics_per_domain']*c['topic_documents'][split]==k)
check('independent H source halves',sum(c['heldout_per_domain_source_strata'].values())==60)
length=c['analysis_stop_exclusive']-c['analysis_start'];check('native160position range',length==160 and c['input_positions']==192)
check('study72000observations and86400real inputs',450*length==72000==c['study_analysis_positions'] and 450*192==86400==c['study_real_input_positions'])
check('real vs padded model budget',450*256==115200==c['study_LM_padded_positions'] and 462*256==118272==c['all_calls_LM_padded_cap'] and 462*1024==473088==c['all_calls_CC_padded_cap'])
check('cap includes checks and retries',450+c['checks_at_most']==462==c['forward_sequence_cap_including_retries'])
check('original7math/9bio,all IDs distinct',len(f['math'])==7 and len(f['biology'])==9 and len(set(f['math']+f['biology']))==16)
old=Path(f['source']);check('legacy source freeze bytes unchanged',hashlib.sha256(old.read_bytes()).hexdigest()==f['source_sha256']);orig=json.loads(old.read_text())['sets'];check('IDs not reselected',f['math']==orig['all_cached_strict_math'] and f['biology']==orig['all_cached_strict_biology'])
check('minimum opponent does not hide weak comparison',min(.95,.55)<c['main_threshold'] and (.95+.55)/2>=c['main_threshold'])
check('near cap preserves5percent by document',int(.05*60)==3==c['near_max_opponent_documents_discovery_each'])
check('three-contrast planned interval',abs(c['primary_CI_coverage']-(1-.05/3))<1e-12 and c['primary_CI_quantiles']==[1/120,119/120])
check('reference-support coverage guard',c['min_reference_classified_fraction_each_group_and_pool']==.80 and c['min_classified_members_each_group_domain']==5)
upper=1-.05**(1/60);check('pointwise zero-of60 upper bound',.048<upper<.05)
for suffix in ['', '_cn']:
    p=W/('protocol'+suffix+'.md');t=p.read_text();heads=re.findall(r'^## (\d+)\. ',t,re.M);check(p.name+'18section ownership',heads==[str(i) for i in range(18)]);check(p.name+'not-executable', 'DRAFT_NOT_EXECUTABLE' in t)
root=W
while root.name!='Research_System':root=root.parent
anchor=root/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
for suffix in ['', '_cn']:
    p=anchor/('15_27_04_domain_member_atlas_anchor'+suffix+'.md');check(p.name+'eightsection ownership',re.findall(r'^## (\d+)\. ',p.read_text(),re.M)==[str(i) for i in range(1,9)])
check('no execution or training authorized/claimed',c['document_status']=='DRAFT_NOT_EXECUTABLE' and not c['execution_authorized'] and c['new_forwards_actual']==0 and c['training_updates_actual']==0)
paths=[W/'protocol.md',W/'protocol_cn.md',W/'README.md',W/'README_cn.md',W/'design_audit.md'];links=0
for p in paths:
    for dest in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if dest.startswith(('http','#')):continue
        q=Path(dest) if dest.startswith('/') else p.parent/dest;check('local link '+str(p.name)+':'+dest,q.exists());links+=1
result={'status':'PASS','scope':'design arithmetic/list/link/ownership checks ONLY,not empirical approval or runtime validation','checks':checks,'count':len(checks),'local_links':links,'planned_zero_of60_pointwise_upper95':upper,'planned_documents':450,'new_model_forwards_actual':0,'training_updates_actual':0,'new_dataset_status':'NOT_BUILT','runtime_replay':'NOT_RUN'}
(W/'provenance/planning_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','count','local_links','planned_documents','new_model_forwards_actual','new_dataset_status','runtime_replay']},indent=2))
