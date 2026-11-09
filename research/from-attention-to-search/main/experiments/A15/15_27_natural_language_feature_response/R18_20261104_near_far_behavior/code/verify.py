from common import *
import csv,math,re
from tokenizers import Tokenizer
t=Tokenizer.from_file(str(MODEL/'tokenizer.json'))
p=rows(R/'data/panel.jsonl');raw=rows(R/'results/smoke.jsonl')+rows(R/'results/heldout.jsonl');lookup={x['id']:x for x in raw};checks=[]
def check(name,ok,detail):
    checks.append(dict(check=name,passed=bool(ok),detail=detail));assert ok,(name,detail)
check('all actual records',len(raw)==len(p)==444 and len(lookup)==444,dict(prefixes=len(raw),families=len({x['family'] for x in p})))
for z in p:
    enc=t.encode(z['text'],add_special_tokens=False);check('fresh tokenizer identity',enc.ids==z['token_ids'],z['id'])
    check('fixed position',len(enc.ids)==320 and z['target_position']==319 and z['target_token_id']==enc.ids[319],z['id'])
    if z['gold'] is not None:
        l,r=z['evidence_char_span'];span=z['text'][l:r];ev=[i for i,(a,b) in enumerate(enc.offsets) if a<r and b>l]
        check('literal whole item span',span==z['evidence_item'] and re.fullmatch(r'\b'+re.escape(span)+r'\b',span) is not None,z['id'])
        check('last item token and exclusive gap',ev==z['evidence_token_positions'] and ev[-1]==z['evidence_last_position'] and 319-ev[-1]-1==z['actual_distance'],z['id'])
    x=lookup[z['id']]
    for c,sc in zip(z['candidates'],x['candidates']):
        check('full candidate chain tokenization',t.encode(z['text']+c['text'],add_special_tokens=False).ids==c['full_ids'] and c['full_ids'][320:]==sc['token_ids'],z['id']+c['label'])
        check('all token scores finite and exact sum',len(sc['token_logprobs'])==sc['token_count']==len(sc['token_ids']) and all(math.isfinite(q) and q<=0 for q in sc['token_logprobs']) and math.fsum(sc['token_logprobs'])==sc['total_logprob'],z['id']+c['label'])
    check('within-pair candidate lengths matched',x['candidates'][0]['token_count']==x['candidates'][1]['token_count'],z['id'])
for f in sorted({z['family'] for z in p}):
    for mode in ['main','paraphrase','lure']:
        a=[z for z in p if z['family']==f and z['mode']==mode]
        if not a:continue
        for d in sorted({z['planned_distance'] for z in a}):
            aa,bb=[z for z in a if z['planned_distance']==d]
            if mode!='lure':
                la,ra=aa['evidence_char_span'];lb,rb=bb['evidence_char_span']
                check('A/B only item differs',aa['text'][:la]==bb['text'][:lb] and aa['text'][ra:]==bb['text'][rb:] and aa['local_suffix']==bb['local_suffix'],f+mode+str(d))
        for label in 'AB':
            zz=[z for z in a if z['gold']==label]
            check('identical token multiset across gaps',len({tuple(sorted(z['token_ids'])) for z in zz})==1,f+mode+label)
        if mode!='lure':check('no leakage outside evidence',all(not z['outside_fact_answer_words'] for z in a),f+mode)
resolution=R/'evidence/frozen_owner_resolution.json'
archived=json.load(open(resolution))['files'] if resolution.exists() else {}
for file,h in json.load(open(R/'evidence/freeze.json'))['hashes'].items():
    source=archived[file]['archive'] if file in archived else file
    check('registered pre-run bytes preserved',sha(source)==h,dict(original=file,verified=source))
ac=json.load(open(R/'evidence/analysis_code_frozen.json'));check('analysis code frozen before heldout',sha(ac['file'])==ac['sha256'] and ac['UTC']<json.load(open(R/'evidence/heldout_started.json'))['UTC'],ac)
for path,h in json.load(open(R/'config.json'))['input_sha256'].items():check('input weights and tokenizer unchanged',sha(path)==h,path)
pairtable=list(csv.DictReader(open(R/'tables/family_pairs.csv')))
for row in pairtable:
    prefix=f"{row['family']}_{row['mode']}_{row['planned_distance']}_";a=lookup[prefix+'A'];b=lookup[prefix+'B']
    deltaa=a['candidates'][0]['total_logprob']-a['candidates'][1]['total_logprob'];deltab=b['candidates'][1]['total_logprob']-b['candidates'][0]['total_logprob']
    check('paired success independently recomputed',int(row['paired_success'])==int(deltaa>0 and deltab>0),prefix)
    check('both raw margins and mean independently recomputed',abs(float(row['margin_A'])-deltaa)<1e-12 and abs(float(row['margin_B'])-deltab)<1e-12 and abs(float(row['mean_margin'])-(deltaa+deltab)/2)<1e-12,prefix)
for row in csv.DictReader(open(R/'tables/distance_summary.csv')):
    q=[x for x in pairtable if all(x[k]==row[k] for k in ['split','mode','planned_distance'])];n=len(q);k=sum(int(x['paired_success']) for x in q)
    check('family count and switch summary',n==int(row['families']) and k==int(row['paired_success']) and abs(k/n-float(row['paired_rate']))<1e-12,row)
    check('family mean margin summary',abs(sum(float(x['mean_margin']) for x in q)/n-float(row['mean_margin']))<1e-12,row)
    z=1.959963984540054;den=1+z*z/n;center=(k/n+z*z/(2*n))/den;half=z*math.sqrt(k/n*(1-k/n)/n+z*z/(4*n*n))/den
    check('Wilson interval independent formula',abs(center-half-float(row['paired_wilson_lo']))<1e-12 and abs(center+half-float(row['paired_wilson_hi']))<1e-12,row['split']+row['mode']+row['planned_distance'])
check('template split disjoint',set(z['template'] for z in p if z['split']=='smoke').isdisjoint(set(z['template'] for z in p if z['split']=='heldout')),True)
check('no calibration or baseline truth labels',all(z['gold'] is None and lookup[z['id']]['correct'] is None for z in p if z['mode']=='baseline'),84)
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',checks=len(checks),details=checks,independent_human_review=False,meaning='independent reimplementation of arithmetic/token checks by same Codex agent; not independent scientific review'))
print('PASS',len(checks),'checks')
