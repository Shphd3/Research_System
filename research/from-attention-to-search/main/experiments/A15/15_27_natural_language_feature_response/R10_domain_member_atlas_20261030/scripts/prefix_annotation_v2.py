"""Conservative, activation-blind annotation amendment; retain all v1 outputs."""
from pathlib import Path
import csv,json,re,hashlib
O=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030')
def read(n):return list(csv.DictReader((O/n).open()))
def write(n,rows):
    with (O/n).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
inputs={r['case_id']:r['already_read_window'] for r in read('prefix_annotation_blinded_inputs.csv')}
patterns=[r'\bfor example\b',r'\bin general\b',r'\bin other words\b',r'\bin this (?:article|section|chapter)\b',r'\bas (?:mentioned|noted|described)\b',r'\bon the other hand\b']
cfg={'revision':'prefix-proposal-v2','amendment_reason':'Absence of a finite terminology lexicon is not positive evidence of generic context. v1 had zero undetermined cases. Retain v1; downgrade unsupported generic labels without consulting activations.','input_fields':['case_id','already_read_window'],'generic_rule':'v1 generic label AND an explicit generic-discourse cue; otherwise undetermined','generic_patterns':patterns,'other_categories':'v1 rule proposals unchanged; domain terms and relation cues still require human verification','human_review_status':'PENDING','no_activation_or_future_text_in_annotation':True}
out=[]
for row in read('prefix_annotation_AI_proposals.csv'):
    r=dict(row);r['v1_category']=r['proposed_category'];text=inputs[r['case_id']];cue=next((m.group(0) for p in patterns if (m:=re.search(p,text,re.I))), '')
    if r['v1_category']=='general_narration' and not cue:r['proposed_category']='undetermined'
    r['generic_discourse_cue']=cue;r['review_status']='RULE_PROPOSAL_V2_UNREVIEWED';out.append(r)
write('prefix_annotation_v2_AI_proposals.csv',out)
(O/'prefix_annotation_v2_codebook.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
summary={'cases':len(out),'v1_counts':dict(Counter(r['v1_category'] for r in out)),'v2_counts':dict(Counter(r['proposed_category'] for r in out)),'human_review_status':'PENDING','interpretation':'No semantic prevalence estimate is certified; no noun-phrase/coreference labels have been supplied.'}
(O/'prefix_annotation_v2_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
