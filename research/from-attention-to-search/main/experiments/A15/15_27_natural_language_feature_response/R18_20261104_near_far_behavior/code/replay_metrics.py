"""Read-only replay of all behavioral point estimates from raw per-token scores."""
from pathlib import Path
import json,csv,math,argparse
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();root=args.root
raw=[json.loads(s) for name in ['smoke','heldout'] for s in (root/f'results/{name}.jsonl').read_text().splitlines() if s];groups={}
for row in raw:
    if row['gold'] is None:continue
    totals={c['label']:math.fsum(c['token_logprobs']) for c in row['candidates']}
    delta=totals['A']-totals['B'];margin=delta if row['gold']=='A' else -delta
    key=(row['split'],row['mode'],row['planned_distance']);groups.setdefault(key,{}).setdefault(row['family'],{})[row['gold']]=margin
out=[]
for row in csv.DictReader(open(root/'tables/distance_summary.csv')):
    key=(row['split'],row['mode'],int(row['planned_distance']));families=groups[key];assert all(set(v)=={'A','B'} for v in families.values())
    n=len(families);k=sum(v['A']>0 and v['B']>0 for v in families.values());acc=sum(int(v['A']>0)+int(v['B']>0) for v in families.values())/(2*n);margin=math.fsum((v['A']+v['B'])/2 for v in families.values())/n
    assert n==int(row['families']) and k==int(row['paired_success']) and abs(acc-float(row['accuracy']))<1e-12 and abs(margin-float(row['mean_margin']))<1e-12
    out.append(dict(split=key[0],mode=key[1],planned_gap=key[2],families=n,paired_success=k,accuracy=acc,mean_margin=margin))
print(json.dumps(dict(status='PASS',raw_prefixes=len(raw),cells=len(out),results=out),indent=2))
