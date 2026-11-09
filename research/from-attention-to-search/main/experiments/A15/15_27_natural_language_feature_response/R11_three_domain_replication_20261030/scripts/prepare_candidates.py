"""Activation-blind R11 candidate inventory; does NOT qualify a450document panel."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import argparse
import json,re,io,hashlib,collections,datetime
from urllib.parse import urlsplit,unquote
import zstandard as zstd
from tokenizers import Tokenizer
ap=argparse.ArgumentParser();ap.add_argument('--broad',action='store_true');args=ap.parse_args()
S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response');O=S/'R11_three_domain_replication_20261030/preparation';O=O/'broader_topic_inventory_v2' if args.broad else O;O.mkdir(parents=True,exist_ok=True);P=Path('/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst')
TOK=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');T=Tokenizer.from_file(str(TOK))
patterns={
'math':r'\b(?:theorem|lemma|integer|polynomial|algebra|geometry|calculus|mathematical|mathematics|matrix|matrices|eigenvalue|prime number|proof|topology|differential|isomorphism|convex|manifold)\w*\b',
'biology':r'\b(?:cells?|genes?|proteins?|organisms?|evolution|species|biological|biology|enzymes?|chromosome|neurons?|bacteria|genome|genetic|membrane|renal|glial|tissue|immune|fibrillin|ubiquitin)\w*\b',
'physics':r'\b(?:physics|physicist|quantum|photon|electron|electromagnet|magnetic|thermodynam|entropy|relativity|gravitational|momentum|acceleration|velocity|wavelength|Maxwell|Hamiltonian|Schrodinger|Schrödinger|dielectric|superconduct|optical|diffraction|Planck|particle|mechanics|kinetic|turbulence|nuclear)\w*\b'}
if args.broad:
    # The first inventory undercovered two prespecified math topics;expand INPUT-only recall,not feature eligibility.
    patterns['math']=r'\b(?:theorem|lemma|integer|polynomial|algebra|geometry|calculus|mathematical|mathematics|matrix|matrices|eigenvalue|prime number|proof|topology|differential|isomorphism|convex|manifold|probability|statistical|statistics|stochastic|random variable|Bayesian|permutation|combinatorics|combinatorial|graph theory|Boolean|mathematical logic)\w*\b'
    patterns['biology']=r'\b(?:cells?|genes?|proteins?|organisms?|evolution|species|biological|biology|enzymes?|chromosome|neurons?|bacteria|genome|genetic|membrane|renal|glial|tissue|immune|fibrillin|ubiquitin|plants?|animals?|ecology|ecological|botanical|zoology)\w*\b'
patterns={k:re.compile(v,re.I) for k,v in patterns.items()}
topics={
'math':{'algebra':r'algebra|polynomial|matri[cex]|eigen|isomorph','geometry_topology':r'geometr|topolog|manifold|polygon|circle|curvature','analysis':r'calculus|differential|integral|analytic|convergen|derivative','probability_statistics':r'probabil|statistic|random|stochastic','number_theory':r'prime|integer|number theory|modular|Diophant','discrete_logic':r'combinator|graph theory|logic|Boolean|discrete|axiom'},
'biology':{'cell':r'cell|membrane|organel|mitochond','molecular_genetics':r'gene|genetic|genome|protein|DNA|RNA|chromosom','physiology_neuro':r'physiolog|neuron|neural|brain|renal|kidney|nerve|glial','ecology_evolution':r'evolut|ecolog|species|selection|fossil','microbiology_immunity':r'bacter|vir[ua]l|virus|immune|microb|infection','organismal':r'plant|animal|zoolog|botan|fung|reproduct|insect|flower'},
'physics':{'mechanics':r'mechanic|Newton|momentum|acceleration|velocity|gravit|relativ','electromagnetism':r'electric|magnetic|Maxwell|electromag|dielectric|charge','thermo_statistical':r'thermodynam|entropy|thermal|temperature|statistical mechanics','waves_optics':r'optical|optics|wave|diffraction|lens|photon|wavelength','quantum':r'quantum|Schrodinger|Schrödinger|Planck|uncertainty principle|wavefunction','materials_solid':r'solid.state|material|superconduct|crystal|lattice|semiconductor|band gap'}}
topics={g:{k:re.compile(v,re.I) for k,v in d.items()} for g,d in topics.items()}
def family(url):
    u=urlsplit(url);h=(u.hostname or '').lower();p=unquote(u.path).rstrip('/');q=re.search(r'/questions/(\d+)',p)
    if q:return h+':question:'+q.group(1)
    if '/book/' in p:p=p.split('/section/')[0]
    return h+p
def platform(h):
    h=h.removeprefix('www.')
    if h.endswith('stackexchange.com') or h.endswith('mathoverflow.net'):return 'stackexchange-family'
    if any(h.endswith(x) for x in ['wikipedia.org','wikibooks.org','wikimedia.org']):return 'wikimedia-family'
    a=h.split('.');cc=['co.uk','com.au','ac.uk']+(['net.au','org.au','org.uk','ac.jp','ac.cn'] if args.broad else []);return '.'.join(a[-3:]) if len(a)>=3 and '.'.join(a[-2:]) in cc else '.'.join(a[-2:])
old=[json.loads(x) for x in (S/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];ref=[json.loads(x) for x in (S/'R04_domain_usage_20261027/data/reference.jsonl').read_text().splitlines()];oldfam={family(x['url']) for x in old+ref};oldplatform={platform(x['host']) for x in old};oldsha={x.get('source_text_sha256',x.get('text_sha256')) for x in old+ref}
inverted=collections.defaultdict(set);oldgrams=[]
for k,r in enumerate(old+ref):
    a=r['token_ids'];ss={tuple(a[j:j+5]) for j in range(len(a)-4)};oldgrams.append(ss)
    for gram in ss:inverted[gram].add(k)
cfg={'revision':'R11-candidate-qualification-v1','stage':'prefilter ONLY,activation-blind,not final content review or selection','source_asset_id':'dclm_raw_holdout_global02','source':str(P),'domains':list(patterns),'term_patterns':{k:v.pattern for k,v in patterns.items()},'topics':{g:{k:v.pattern for k,v in d.items()} for g,d in topics.items()},'source_filter':'>=5matches and>=2distinct matched terms in first12000chars for any domain;allow interdisciplinary multiple domain labels','window_filter':'earliest of first40paragraph starts with192tokens,>=65English words,>=55%alphabetic chars,>=3matches for an eligible domain;paragraph-style QA/UI rules need independent review','one_candidate_per_family':True,'old_article_or_reference_family_quarantined':True,'old_5shingle_Jaccard_limit':.8,'newsource_platforms':'absent from old120platformfamilies;this alone does not qualify H','labels':'provisional lexical labels only;NO feature/model outputs used','new_model_forwards':0}
if args.broad:cfg.update(revision='R11-candidate-qualification-v2-input-only-recall-audit',amendment='Retain v1;expand missing probability/discrete/ecology/organism input lexicons,correct known ccTLDpublisher grouping,and add QAstructure flags. No new-model outputs exist;no selection/holdout quota is relaxed.')
cp=O/'candidate_config.json'
if cp.exists():assert json.loads(cp.read_text())==cfg
else:cp.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
out=O/'candidate_windows.jsonl'
if out.exists():raise RuntimeError('Existing candidate inventory;inspect it instead of overwriting.')
counts=collections.Counter();rows=[];seen=set();hosts=collections.defaultdict(collections.Counter);domain_platform=collections.defaultdict(set)
with P.open('rb') as src,zstd.ZstdDecompressor().stream_reader(src) as zr,out.open('x') as dest:
    for i,line in enumerate(io.TextIOWrapper(zr,encoding='utf8')):
        counts['raw_documents']+=1
        if i and i%10000==0:print('SCAN',i,'candidates',len(rows),flush=True)
        x=json.loads(line);s=x.get('text','');head=s[:12000];hits={g:patterns[g].findall(head) for g in patterns};eligible=[g for g in patterns if len(hits[g])>=5 and len(set(z.lower() for z in hits[g]))>=2]
        if not eligible:continue
        counts['lexical_prefilter_pass']+=1;url=x.get('url','');u=urlsplit(url);h=u.hostname or '';fam=family(url);digest=hashlib.sha256(s.encode()).hexdigest()
        if fam in oldfam or digest in oldsha:counts['old_family_or_text']+=1;continue
        if fam in seen:counts['duplicate_family']+=1;continue
        starts=sorted(set([0]+[m.end() for m in re.finditer(r'\n\s*\n',s[:14000])]))[:40];chosen=None
        for start in starts:
            chunk=s[start:start+5000];e=T.encode(chunk,add_special_tokens=False)
            if len(e.ids)<192:continue
            end=e.offsets[191][1];text=chunk[:end];ids=e.ids[:192]
            if T.encode(text,add_special_tokens=False).ids!=ids:continue
            if len(re.findall(r'[A-Za-z]+',text))<65 or sum(c.isalpha() for c in text)/max(len(text),1)<.55:continue
            if re.search(r'\b(?:void |std::|function\(|Log In|Sign In|Forgot your password|jump to:|Jump to:)',text):continue
            ww={g:patterns[g].findall(text) for g in eligible};possible=[g for g in eligible if len(ww[g])>=3 and len(set(z.lower() for z in ww[g]))>=2]
            if not possible:continue
            chosen=(start,start+end,text,ids,possible,ww);break
        if chosen is None:counts['no_clean_192window']+=1;continue
        start,end,text,ids,possible,wh=chosen;grams={tuple(ids[j:j+5]) for j in range(188)};ov=collections.Counter(k for gram in grams for k in inverted.get(gram,[]));near=any(v/(len(grams)+len(oldgrams[k])-v)>=.8 for k,v in ov.items())
        if near:counts['old_near_duplicate']+=1;continue
        seen.add(fam);plat=platform(h);qa_host=any(z in h for z in ['stackexchange','mathoverflow','physicsforums','quora','answers.','reddit']);qa_struct=args.broad and (bool(re.search(r'/(?:questions?|answers?|qanda|ask)/',u.path,re.I)) or (bool(re.search(r'\bQuestion\s*:',s[:5000],re.I)) and bool(re.search(r'\bAnswer\s*:',s[:5000],re.I))));genre='question_answer' if qa_host or qa_struct else 'expository';topic_scores={g:{k:len(p.findall(text)) for k,p in topics[g].items()} for g in possible};topic_guess={g:max(topic_scores[g],key=topic_scores[g].get) if max(topic_scores[g].values())>0 else 'unknown' for g in possible}
        row={'candidate_id':f'R11_RAW_{i:06d}','source_asset_id':'dclm_raw_holdout_global02','source_line':i,'url':url,'host':h,'platform_family':plat,'document_family':fam,'old_platform':plat in oldplatform,'possible_domains':possible,'provisional_topics':topic_guess,'provisional_topic_scores':topic_scores,'provisional_genre':genre,'term_evidence':{g:sorted(set(wh[g])) for g in possible},'char_start':start,'char_end':end,'text_sha256':digest,'window_sha256':hashlib.sha256(text.encode()).hexdigest(),'warc_record_id':x.get('metadata',{}).get('WARC-Record-ID'),'prefix':text,'token_ids':ids,'review_status':'PENDING_ACTIVATION_BLIND_CONTENT_REVIEW','new_model_forwards':0};dest.write(json.dumps(row,ensure_ascii=False)+'\n');rows.append(row)
        for g in possible:counts['candidate_'+g]+=1;hosts[g][plat]+=1;domain_platform[plat].add(g)
sharedplatforms={p for p,d in domain_platform.items() if len(d)>=2};upper=[]
for g in patterns:
    for topic in topics[g]:
        for genre in ['expository','question_answer']:
            rr=[r for r in rows if g in r['possible_domains'] and r['provisional_topics'][g]==topic and r['provisional_genre']==genre];ss=[r for r in rr if r['platform_family'] in sharedplatforms];nn=[r for r in ss if not r['old_platform']];upper.append({'domain':g,'topic':topic,'genre':genre,'all_provisional':len(rr),'shared_platform_candidates':len(ss),'newsource_shared_platform_candidates':len(nn),'newsource_platforms':len({r['platform_family'] for r in nn})})
summary={'stage':'SOURCE_INVENTORY_DONE_NOT_QUALIFIED','counts':dict(counts),'candidate_document_families':len(rows),'platforms_seen_in_ge2provisional_domains':len(sharedplatforms),'old_platform_families':sorted(oldplatform),'platform_counts':{g:dict(c) for g,c in hosts.items()},'optimistic_quota_inventory':upper,'scope_warning':'lexical prefilter/source inventory;counts are upper bounds before content review,not a built450-document dataset','new_model_forwards':0}
(O/'candidate_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print('COMPLETE',json.dumps({'counts':dict(counts),'candidate_families':len(rows),'shared_platforms':len(sharedplatforms)},ensure_ascii=False),flush=True)
