from engine import *
import re
out=[]
for site in SITES:
 for split in ['discovery','heldout']:
  p,z,a=load_stage(split,site);directions=json.load(open(R/f'data/{site}_joint_directions.json'))['kinds']
  for kind,info in directions.items():
   for pair in info['pair_ids']:
    for co,rr in per_condition(p).items():
     active=sorted({p[i]['family'] for i in rr if z[i,pair[0]]>0 and z[i,pair[1]]>0});positions=sum(z[i,pair[0]]>0 and z[i,pair[1]]>0 for i in rr);allf=sorted({x['family'] for x in p});out.append(dict(site=site,split=split,kind=kind,condition=co,atom_a=pair[0],atom_b=pair[1],coactive_positions=int(positions),position_denominator=24,coactive_families=len(active),family_denominator=12,active_families=active,missing_families=sorted(set(allf)-set(active))))
table(R/'tables/joint_pair_family_coverage.csv',out)
issues=[]
for p in rows(R/'data/panel.jsonl'):
 for c in p['candidates']:
  word=c['item'];expected=int(p['evidence_item']==word)+int(p['near_item']==word);actual=len(re.findall(r'\b'+re.escape(word)+r'\b',p['text']))
  if actual!=expected:issues.append(dict(id=p['id'],word=word,expected=expected,actual=actual))
assert not issues,issues
dump(R/'evidence/leak_audit.json',dict(UTC=now(),status='PASS',prefixes=292,answer_occurrences='Exactly intended remote/near roles; none elsewhere in filler/question',unexpected=issues))
