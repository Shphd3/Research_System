"""Input-only document matching and activation-blind prefix-label proposals."""
import os
for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[key]='2'
from pathlib import Path
import argparse,collections,csv,hashlib,json,re,datetime
import numpy as np
from scipy import sparse
from scipy.optimize import linear_sum_assignment
from tokenizers import Tokenizer
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'));arg=ap.parse_args();S=arg.source;O=S/'presentation_variants/near_single_domain_20261030';T=S/'presentation_variants/token_context_audit_20261030'
def table(name,rr):
    rr=list(rr)
    if not rr:return
    with (O/name).open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def dump(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def safe(x):return float(x) if np.isfinite(x) else ''
freeze=json.loads((O/'freeze.json').read_text());groups={g:np.array(freeze['sets']['near95_'+g],int) for g in ['math','biology']};ids=np.r_[groups['math'],groups['biology']];sl={'math':slice(0,len(groups['math'])),'biology':slice(len(groups['math']),len(ids))}
docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];pk=np.load(S/'analysis/position_keys.npz');di=pk['document_index'];pos=pk['position'];token=pk['token_id'];held=np.flatnonzero(np.array([docs[d]['split']=='heldout' for d in di]));helddoc={g:[i for i,d in enumerate(docs) if d['split']=='heldout' and d['domain']==g] for g in groups};docrow={d:np.flatnonzero(di==d) for g in groups for d in helddoc[g]}
tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');tcfg=json.loads((T/'config.json').read_text());target=tcfg['primary_the_id'];predetermined=[int(groups['math'][0]),int(groups['biology'][0])]
math_patterns=[r'\bintegers?\b',r'\bpolynomial\w*',r'\bquadratic\b',r'\belliptic\b',r'\btheorems?\b',r'\blemma\b',r'\bcalculus\b',r'\balgebra\w*',r'\bgeometr\w*',r'\btopolog\w*',r'\bhomotop\w*',r'\bisoperim\w*',r'\bequations?\b',r'\bmatrices\b',r'\bmatrix\b',r'\bintegrals?\b',r'\bderivatives?\b',r'\bcoordinates?\b',r'\bcongruen\w*',r'\bPythagor\w*',r'\bsquare root\b',r'\bmathematic\w*',r'\baxioms?\b',r'\bprobabilit\w*',r'\beigen\w*']
bio_patterns=[r'\bcells?\b',r'\bproteins?\b',r'\bgenes?\b',r'\bgenetic\w*',r'\bDNA\b',r'\bRNA\b',r'\benzym\w*',r'\bmembran\w*',r'\bneuron\w*',r'\bdendrit\w*',r'\baxons?\b',r'\bsynap\w*',r'\borganisms?\b',r'\bspecies\b',r'\btrilobit\w*',r'\bcephalon\b',r'\bthorax\b',r'\bcranidium\b',r'\blibrigena\b',r'\bglabella\b',r'\bmitochond\w*',r'\bimmune\w*',r'\blungs?\b',r'\bkidney\w*',r'\brenal\b',r'\brespirat\w*',r'\bmacrophag\w*',r'\bblood\b',r'\bbacter\w*',r'\bviruses?\b',r'\bviral\b',r'\bfung\w*',r'\banimals?\b',r'\bplants?\b',r'\btissues?\b',r'\bhormon\w*',r'\breceptors?\b',r'\bnucle\w*',r'\bvascular\w*',r'\bchromosom\w*',r'\bevolut\w*',r'\bmutat\w*',r'\bamino acids?\b',r'\boblongata\b',r'\bmedulla\b',r'\bpapilla\w*']
relation_patterns=[r'\bif\b.+\bthen\b',r'\btherefore\b',r'\bimplies\b',r'\bbecause\b',r'\bcauses?\b',r'\bleads? to\b',r'\bdepends? on\b',r'\bincreases?\b',r'\bdecreases?\b',r'\bregulat\w*',r'\bencoded by\b',r'\bbinds?\b',r'\bproof\b',r'\bprove\w*',r'\bshow that\b',r'\bcalculat\w*',r'\bequations?\b',r'\bequal\w*',r'\bsum\b',r'\bproduct\b',r'\bratio\b',r'\bsquare root\b',r'\bderived\b',r'\bfunction of\b']
codebook={'window':'last40already-read tokens EXCLUDING target; no later text/source/domain/activation fields passed to proposal function','categories':['domain_terms_objects','domain_relations_reasoning','general_narration','format_quote','undetermined'],'primary_priority':'dominant format(last12tokens>=3markup markers or trailing citation/quote); domain cue+relation; domain cue; intelligible prose>=6English words without listed domain cue; otherwise undetermined','math_cue_patterns':math_patterns,'biology_cue_patterns':bio_patterns,'relation_patterns':relation_patterns,'secondary_flags':'math cue,bio cue,relation cue,format cue kept independently; mixed cues allowed','gold_status':'AI_RULE_PROPOSALS_ONLY; human verification blank/pending; lexical-cue coverage is incomplete and is not semantic ground truth','counterexamples_to_review':['low-response prefixes can contain domain terminology','biology-source text can contain mathematical equations','generic noun phrases can still refer to domain objects','quotation/markup is not automatically a semantic relation']}
cfg={'revision':'near-token-matching-and-prefix-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'near_freeze_sha256':hashlib.sha256((O/'freeze.json').read_bytes()).hexdigest(),'target_example_ID':target,'predetermined_example_members':predetermined,'broad_tokens':'all discovery-shared IDs with>=5heldoutdocs/domain','levels':['local','source_local'],'local_environment':['exact target ID','exact preceding tokenID','genre','40-position bin','sentence/paragraph boundary flag'],'source_local':'all local matches AND exact source host','matching':'maximum number of independent document pairs, then maximum shared occurrences; no activation in matching; within each doc pair and exact stratum, minimum absolute position-distance assignment without reuse','aggregation':'mean matched occurrence difference within each document pair, then equal document pairs; all fixed members including zeros','uncertainty':'1000document-pair bootstrap draws; each original doc used in at most1pair per token/level; >=5pairs for reported interval','response':'native z and fixed R10 high-response indicator both saved; group plot uses mean fraction high across all fixed group members','example_rule':'same fixed ID279 and first discovery-ranked near member/domain; highest preferred native-z matched occurrence and its assigned opposite-domain control; no member replacement if inactive; examples illustrate, full matching drives inference','prefix_annotation_codebook':codebook,'new_model_forwards':0,'new_training':0,'human_review_status':'PENDING'}
if (O/'matching_config.json').exists():old=json.loads((O/'matching_config.json').read_text());cfg['frozen_utc']=old['frozen_utc'];assert old==cfg
else:dump('matching_config.json',cfg)

# Prefix proposals are computed from text alone before any activation cache is opened.
prefix_input=[];proposals=[];annotation={};fullprefix={};localprefix={};boundary={}
def hits(patterns,text):
    result=[]
    for pattern in patterns:
        m=re.search(pattern,text,re.I)
        if m:result.append(m.group(0))
    return list(dict.fromkeys(result))
def propose(text,last12):
    mh=hits(math_patterns,text);bh=hits(bio_patterns,text);rh=hits(relation_patterns,text);markup=len(re.findall(r'\\[A-Za-z]+|[{}^_$]',last12));citation=bool(re.search(r'\[\d+(?:[,\-]\d+)*\]\s*$',last12));quote=bool(re.search(r'["“]\s*$',last12));ff=markup>=3 or citation or quote
    if ff:cat='format_quote'
    elif (mh or bh) and rh:cat='domain_relations_reasoning'
    elif mh or bh:cat='domain_terms_objects'
    elif len(re.findall(r'[A-Za-z]+',text))>=6 and '\ufffd' not in text:cat='general_narration'
    else:cat='undetermined'
    return {'proposed_category':cat,'math_cues':' | '.join(mh),'biology_cues':' | '.join(bh),'relation_cues':' | '.join(rh),'format_flag':ff,'proposed_domain':'mixed' if mh and bh else 'math' if mh else 'biology' if bh else 'undetermined','human_verified_category':'','review_status':'AI_RULE_PROPOSED_UNREVIEWED'}
for r in held:
    d=int(di[r]);p=int(pos[r]);ids0=docs[d]['token_ids'];pre=tok.decode(ids0[:p],skip_special_tokens=False);win=tok.decode(ids0[max(0,p-40):p],skip_special_tokens=False);last12=tok.decode(ids0[max(0,p-12):p],skip_special_tokens=False);case=hashlib.sha256(f'prefix-only:{d}:{p}'.encode()).hexdigest()[:14]
    prefix_input.append(dict(case_id=case,already_read_window=win));lab=propose(win,last12);proposals.append(dict(case_id=case,**lab));annotation[int(r)]=lab;fullprefix[int(r)]=pre;localprefix[int(r)]=win;boundary[int(r)]='paragraph' if '\n\n' in last12[-8:] else 'sentence' if re.search(r'[.!?]\s*$',pre) else 'other'
table('prefix_annotation_blinded_inputs.csv',sorted(prefix_input,key=lambda r:r['case_id']));table('prefix_annotation_AI_proposals.csv',sorted(proposals,key=lambda r:r['case_id']))
table('prefix_annotation_unblind_key.csv',(dict(case_id=hashlib.sha256(f'prefix-only:{int(di[r])}:{int(pos[r])}'.encode()).hexdigest()[:14],global_row=int(r),seq_id=docs[int(di[r])]['seq_id'],domain=docs[int(di[r])]['domain'],position=int(pos[r]),token_id=int(token[r])) for r in held))
assert len(proposals)==6400 and not any('activ' in k for row in prefix_input for k in row)

Z=sparse.load_npz(S/'analysis/native_positions_csr.npz')[:,ids].tocsr();tau=np.load(S/'analysis/token_thresholds.npz')['positive_z_p90'][ids];zc=Z.tocoo();ok=zc.data>tau[zc.col];H=sparse.csr_matrix((np.ones(ok.sum()),(zc.row[ok],zc.col[ok])),shape=Z.shape)
shared={int(r['token_id']) for r in csv.DictReader((O/'input_token_categories.csv').open()) if r['category']=='shared_both_domains'};target_ids=sorted(t for t in shared if min(sum(any(token[r]==t for r in docrow[d]) for d in helddoc[g]) for g in groups)>=5)
rng=np.random.default_rng(2026103011);member_results=[];group_results=[];allpairs=[];context_references={};main_examples=[]
def make_pairs(t,level):
    strata={d:collections.defaultdict(list) for g in groups for d in helddoc[g]}
    for d in strata:
        for r in docrow[d]:
            if token[r]!=t:continue
            p=int(pos[r]);key=(docs[d]['genre'],(p-32)//40,docs[d]['token_ids'][p-1],boundary[int(r)])
            if level=='source_local':key+=(docs[d]['host'],)
            strata[d][key].append(int(r))
    score=np.zeros((20,20),int)
    for i,m in enumerate(helddoc['math']):
        for j,b in enumerate(helddoc['biology']):score[i,j]=sum(min(len(strata[m][k]),len(strata[b][k])) for k in set(strata[m])&set(strata[b]))
    ii,jj=linear_sum_assignment(np.where(score>0,1000+score,0),maximize=True);pairs=[]
    for i,j in zip(ii,jj):
        if score[i,j]==0:continue
        m,b=helddoc['math'][i],helddoc['biology'][j];matched=[]
        for k in sorted(set(strata[m])&set(strata[b]),key=str):
            mr,br=strata[m][k],strata[b][k];cost=np.abs(pos[mr,None]-pos[None,br]);aa,bb=linear_sum_assignment(cost)
            matched.extend((mr[a],br[b0]) for a,b0 in zip(aa,bb))
        pairs.append((m,b,matched))
    assert len({a for a,b,rr in pairs})==len(pairs) and len({b for a,b,rr in pairs})==len(pairs)
    return pairs
for t in target_ids:
    for level in ['local','source_local']:
        pairs=make_pairs(t,level);n=len(pairs)
        if not n:
            for g in groups:
                group_results.append(dict(feature_group=g,target_token_id=t,target_string=tok.decode([t],skip_special_tokens=False),level=level,members=len(groups[g]),matched_document_pairs=0,matched_position_pairs=0,preferred_minus_other_high_fraction='',CI_low='',CI_high='',native_supported_members=0,high_supported_members=0,retained_math_positions=0.,retained_biology_positions=0.,math_source_hosts=0,biology_source_hosts=0,mean_position_distance='',interval_status='NO_MATCHED_OPPORTUNITY'))
            for j,f in enumerate(ids):
                g='math' if j<len(groups['math']) else 'biology'
                member_results.append(dict(feature_id=int(f),domain_bias=g,target_token_id=t,level=level,matched_document_pairs=0,matched_position_pairs=0,native_math_mean='',native_biology_mean='',native_math_minus_biology='',native_CI_low='',native_CI_high='',high_math_minus_biology='',high_CI_low='',high_CI_high='',preferred_native_active_docpairs=0,preferred_high_docpairs=0,coverage_status='NO_MATCHED_OPPORTUNITY'))
            continue
        zmath=[];zbio=[];hmath=[];hbio=[]
        for pairno,(m,b,rr) in enumerate(pairs):
            mr=np.array([a for a,b0 in rr]);br=np.array([b0 for a,b0 in rr]);zmath.append(np.asarray(Z[mr].mean(0)).ravel());zbio.append(np.asarray(Z[br].mean(0)).ravel());hmath.append(np.asarray(H[mr].mean(0)).ravel());hbio.append(np.asarray(H[br].mean(0)).ravel())
            for a,b0 in rr:
                assert token[a]==token[b0]==t and docs[m]['token_ids'][int(pos[a])-1]==docs[b]['token_ids'][int(pos[b0])-1]
                allpairs.append(dict(token_id=t,token_string=tok.decode([t],skip_special_tokens=False),level=level,document_pair=pairno,math_doc=docs[m]['seq_id'],biology_doc=docs[b]['seq_id'],math_host=docs[m]['host'],biology_host=docs[b]['host'],math_position=int(pos[a]),biology_position=int(pos[b0]),position_distance=int(abs(pos[a]-pos[b0])),preceding_token_id=docs[m]['token_ids'][int(pos[a])-1],math_global_row=a,biology_global_row=b0))
        zm=np.array(zmath);zb=np.array(zbio);hm=np.array(hmath);hb=np.array(hbio);wd=rng.multinomial(n,np.full(n,1/n),size=1000)/n;dh=hm-hb;dz=zm-zb;CIH=np.quantile(wd@dh,[.025,.975],axis=0) if n>=5 else np.full((2,len(ids)),np.nan);CIZ=np.quantile(wd@dz,[.025,.975],axis=0) if n>=5 else np.full((2,len(ids)),np.nan)
        for j,f in enumerate(ids):
            g='math' if j<len(groups['math']) else 'biology';pref=zm[:,j] if g=='math' else zb[:,j];h_pref=hm[:,j] if g=='math' else hb[:,j]
            member_results.append(dict(feature_id=int(f),domain_bias=g,target_token_id=t,level=level,matched_document_pairs=n,matched_position_pairs=sum(len(rr) for m,b,rr in pairs),native_math_mean=float(zm[:,j].mean()),native_biology_mean=float(zb[:,j].mean()),native_math_minus_biology=float(dz[:,j].mean()),native_CI_low=safe(CIZ[0,j]),native_CI_high=safe(CIZ[1,j]),high_math_minus_biology=float(dh[:,j].mean()),high_CI_low=safe(CIH[0,j]),high_CI_high=safe(CIH[1,j]),preferred_native_active_docpairs=int((pref>0).sum()),preferred_high_docpairs=int((h_pref>0).sum()),coverage_status='NO_NATIVE_SUPPORT' if not np.any(zm[:,j]>0) and not np.any(zb[:,j]>0) else 'LOW_SUPPORT' if (pref>0).sum()<3 else 'NATIVE_SUPPORT_GE3_DOC_PAIRS'))
        for g in groups:
            sign=1 if g=='math' else -1;v=sign*dh[:,sl[g]].mean(1);bc=wd@v;lo,hi=np.quantile(bc,[.025,.975]) if n>=5 else [np.nan,np.nan];opportunities={d:sum(token[r]==t for dd in helddoc[d] for r in docrow[dd]) for d in groups};countpos=sum(len(rr) for m,b,rr in pairs)
            group_results.append(dict(feature_group=g,target_token_id=t,target_string=tok.decode([t],skip_special_tokens=False),level=level,members=len(groups[g]),matched_document_pairs=n,matched_position_pairs=countpos,preferred_minus_other_high_fraction=float(v.mean()),CI_low=safe(lo),CI_high=safe(hi),native_supported_members=int(((zm[:,sl[g]]>0)|(zb[:,sl[g]]>0)).any(0).sum()),high_supported_members=int(((hm[:,sl[g]]>0)|(hb[:,sl[g]]>0)).any(0).sum()),retained_math_positions=countpos/opportunities['math'],retained_biology_positions=countpos/opportunities['biology'],math_source_hosts=len({docs[m]['host'] for m,b,rr in pairs}),biology_source_hosts=len({docs[b]['host'] for m,b,rr in pairs}),mean_position_distance=float(np.mean([abs(pos[a]-pos[b0]) for m,b,rr in pairs for a,b0 in rr])),interval_status='EXPLORATORY_DOC_PAIR_BOOTSTRAP' if n>=5 else 'INSUFFICIENT_DOCUMENT_PAIRS'))
        if t==target:
            context_references[level]=dict(pairs=pairs,zm=zm,zb=zb,hm=hm,hb=hb)
            np.savez_compressed(O/f'the_{level}_matched_document_means.npz',feature_ids=ids,native_math=zm,native_biology=zb,high_math=hm,high_biology=hb,bootstrap_docpair_weights=wd)
table('matched_token_position_pairs.csv',allpairs);table('matched_same_token_per_member.csv',member_results);table('matched_same_token_group_summary.csv',group_results)

# Exactly the first discovery-ranked member/domain; no substitute for an inactive member.
for g,f in zip(groups,predetermined):
    j=list(ids).index(f);reference=context_references.get('local');cases=[]
    if reference:
        for m,b,rr in reference['pairs']:
            for a,b0 in rr:
                pr=a if g=='math' else b0;cases.append((float(Z[pr,j]),hashlib.sha256(f'{f}:{a}:{b0}'.encode()).hexdigest(),a,b0))
    if not cases:main_examples.append(dict(feature_id=f,domain_bias=g,status='NO_MATCHED_OPPORTUNITY',math_position='',biology_position='',math_z='',biology_z='',threshold=float(tau[j]),math_prefix='',biology_prefix='',math_cues='',biology_cues='',math_AI_label='',biology_AI_label='',math_source='',biology_source='',target_token_id=target,target_string=tok.decode([target],skip_special_tokens=False)));continue
    cases.sort(key=lambda r:(-r[0],r[1]));_,_,a,b=cases[0];az=float(Z[a,j]);bz=float(Z[b,j]);labm=annotation[a];labb=annotation[b]
    main_examples.append(dict(feature_id=f,domain_bias=g,status='MATCHED_HIGH_EXAMPLE' if max(az,bz)>tau[j] else 'NO_MATCHED_HIGH_RESPONSE_SUPPORT',math_position=int(pos[a]),biology_position=int(pos[b]),math_z=az,biology_z=bz,threshold=float(tau[j]),math_prefix=localprefix[a],biology_prefix=localprefix[b],math_cues=' | '.join(x for x in [labm['math_cues'],labm['biology_cues']] if x),biology_cues=' | '.join(x for x in [labb['math_cues'],labb['biology_cues']] if x),math_AI_label=labm['proposed_category'],biology_AI_label=labb['proposed_category'],math_source=docs[int(di[a])]['host'],biology_source=docs[int(di[b])]['host'],target_token_id=target,target_string=tok.decode([target],skip_special_tokens=False),math_seq_id=docs[int(di[a])]['seq_id'],biology_seq_id=docs[int(di[b])]['seq_id']))
table('predetermined_member_matched_examples.csv',main_examples)

# Exploratory label proportions are separate from verified response counts.
categories=codebook['categories'];category_index=np.array([categories.index(annotation[int(r)]['proposed_category']) for r in held]);onehot=sparse.csr_matrix((np.ones(len(held)),(np.arange(len(held)),category_index)),shape=(len(held),len(categories)));HC=(H[held].T@onehot).toarray();NH=HC.sum(1);old={int(r['feature_id']):r for r in csv.DictReader((S/'tables/token_member_summary.csv').open())};labelstats=[]
for g in groups:
    select=np.array([j for j in np.arange(len(ids))[sl[g]] if old[int(ids[j])]['usable']=='True']);q=(HC[select]/NH[select,None]).mean(0)
    for k,cat in enumerate(categories):labelstats.append(dict(feature_group=g,proposed_category=cat,member_equal_high_share=float(q[k]),all_available_positions_share=float((category_index==k).mean()),composition_members=len(select),annotation_status='AI_RULE_PROPOSED_UNREVIEWED',human_review_completed=False))
table('exploratory_prefix_label_statistics.csv',labelstats)
the_rows=[r for r in group_results if r['target_token_id']==target];summary={'main_members':{g:len(v) for g,v in groups.items()},'broad_shared_token_IDs':len(target_ids),'the_summary':the_rows,'predetermined_members':predetermined,'prefix_proposals':len(proposals),'human_review_status':'PENDING','annotation_primary_counts':dict(collections.Counter(r['proposed_category'] for r in proposals)),'matching_levels':{lev:dict(tokens_with_any_pairs=len({r['target_token_id'] for r in group_results if r['level']==lev and r['matched_document_pairs']>0}),tokens_with_ge5_docpairs=len({r['target_token_id'] for r in group_results if r['level']==lev and r['matched_document_pairs']>=5})) for lev in cfg['levels']},'source_boundary':'source-controlled pool can have substantial coverage loss; local token/genre/position matching is not a full syntactic or semantic control','new_model_forwards':0,'new_training':0}
dump('matching_summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
