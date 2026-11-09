from common import *
from tokenizers import Tokenizer
import re, random, shutil
assert not (R/'data/panel.jsonl').exists()
for p in ['data','evidence','results','figures','versions']: (R/p).mkdir(exist_ok=True)
t=Tokenizer.from_file(str(MODEL/'tokenizer.json'))
def enc(s): return t.encode(s,add_special_tokens=False).ids
pairs=[('key','spoon'),('coin','ring'),('pen','pencil'),('fork','spoon'),('cup','mug'),('book','notebook'),('brush','comb'),('sock','glove'),('shirt','scarf'),('hat','cap'),('ball','die'),('apple','peach'),('lemon','lime'),('carrot','potato'),('cookie','cake'),('ribbon','string'),('button','bead'),('nail','screw'),('toy car','toy truck'),('tea cup','wine glass'),('postcard','greeting card'),('marble','stone'),('battery','magnet'),('towel','cloth'),('plate','bowl'),('rope','cord'),('map','chart'),('card','stamp')]
containers=['box','bag','basket','drawer','pouch','tin','suitcase','crate','bucket','chest','cabinet','basket','box','bag','tin','drawer','pouch','crate','chest','cabinet','box','bag','drawer','basket','crate','pouch','cabinet','tin']
facts=['The {c} contains the {x}.\n','Inside the {c} there is the {x}.\n','The item stored in the {c} is the {x}.\n','An inventory lists the {c} as holding the {x}.\n','The {c} was packed with the {x}.\n','According to the note, the {c} holds the {x}.\n']
questions=['What is in the {c}?\nAnswer:','What does the {c} contain?\nAnswer:','What item is inside the {c}?\nAnswer:','Name the contents of the {c}.\nAnswer:','What was stored in the {c}?\nAnswer:','Which item is in the {c}?\nAnswer:']
para=['The note says that the {x} is inside the {c}.\n','Someone placed the {x} in the {c}.\n','The {c} is where the {x} was stored.\n','The {x} was put away inside the {c}.\n','A record says the {x} was packed in the {c}.\n','The {x} is being kept in the {c}.\n']
bank=['Time passed.\n','It rained.\n','Morning came.\n','The weather was mild.\n']
bank += [f'The {day} was {adj}.\n' for day in ['morning','afternoon','evening','night','weekend','day','early morning','late afternoon'] for adj in ['quiet','calm','pleasant','warm','cool','cloudy','bright','peaceful']]
bank += ['Clouds drifted slowly overhead.\n','A breeze arrived after noon.\n','Sunlight faded near sunset.\n','The sky became clearer later.\n','Rain continued until dawn.\n','The temperature remained steady.\n','Shadows grew longer by evening.\n','The wind eased before midnight.\n']
assert len(bank)==len(set(bank))
def subset(pool,budget):
    dp={0:[]}
    for s in pool:
        n=len(enc(s))
        for k,v in list(dp.items())[::-1]:
            if k+n<=budget and k+n not in dp: dp[k+n]=v+[s]
    return dp.get(budget)
def select(pool,budget):
    z=subset(pool,budget)
    assert z is not None, ('unconstructible filler budget',budget)
    return z,[s for s in pool if s not in z]
panel=[];families=[]
for fi,(a,b) in enumerate(pairs):
    family=f'F{fi+1:02d}';split='smoke' if fi<4 else 'heldout';group=(fi-4)//4 if fi>=4 else fi//2
    c=containers[fi]
    if split=='smoke':
        fact=('Stored in the {c}: the {x}.\n' if group==0 else 'The recorded contents of the {c} are the {x}.\n')
        question=('Inventory entry for the {c}:' if group==0 else 'The item inside the {c} is')
    else: fact=facts[group];question=questions[group]
    candidates=[{'label':k,'text':' '+x+'.','item':x,'token_ids':enc(' '+x+'.')} for k,x in zip('AB',[a,b])]
    # All predeclared pairs are retained; equality is a construction check, not outcome selection.
    assert len(candidates[0]['token_ids'])==len(candidates[1]['token_ids']), (family,candidates)
    familyrec=dict(family=family,split=split,template=('S' if split=='smoke' else 'H')+str(group+1),container=c,A=a,B=b,candidates=candidates,fact_template=fact,question_template=question)
    families.append(familyrec)
    modes=['main','baseline']+(['paraphrase','lure'] if split=='heldout' else [])
    for mode in modes:
        ff=para[group] if mode=='paraphrase' else fact
        suffix=question.format(c=c)
        if mode=='lure': suffix='The other container holds the {wrong}.\n'+suffix
        neutral='small object' if len(candidates[0]['token_ids'])==3 else 'object'
        # Filler inventory is built before responses; its order and bytes are identical at all distances.
        pool=bank.copy();random.Random(20261104+fi).shuffle(pool)
        xa=neutral if mode=='baseline' else a
        facta=ff.format(c=c,x=xa)
        suffixa=suffix.format(wrong=b)
        header='Record:\n'
        bare=header+facta+suffixa
        oe=len(header)+re.search(r'\b'+re.escape(xa)+r'\b',facta).start();end=oe+len(xa)
        encoded=t.encode(bare,add_special_tokens=False)
        ei=[i for i,(l,r) in enumerate(encoded.offsets) if l<end and r>oe][-1]
        d0=len(encoded.ids)-2-ei
        ds=[128] if mode=='lure' else [16,64,128]
        actual_near=next(d for d in range(max(16,d0),32) if subset(pool,d-d0) is not None)
        near,pool=select(pool,actual_near-d0)
        mid,pool=select(pool,64-actual_near)
        far,pool=select(pool,64)
        front,pool=select(pool,320-len(enc(bare))-sum(map(lambda x:len(enc(x)),near+mid+far)))
        chunks=[front,far,mid,near]
        inventory=[s for ch in chunks for s in ch]
        for planned in ds:
            cut={16:3,64:2,128:1}[planned]
            before=[s for ch in chunks[:cut] for s in ch];after=[s for ch in chunks[cut:] for s in ch]
            for label,x in ([('N',neutral)] if mode=='baseline' else [('A',a),('B',b)]):
                ftext=ff.format(c=c,x=x);sx=suffix.format(wrong=(b if label=='A' else a))
                text=header+''.join(before)+ftext+''.join(after)+sx
                ee=t.encode(text,add_special_tokens=False);ids=ee.ids
                charstart=len(header+''.join(before))+re.search(r'\b'+re.escape(x)+r'\b',ftext).start();charend=charstart+len(x)
                ev=[j for j,(l,r) in enumerate(ee.offsets) if l<charend and r>charstart]
                e=ev[-1];p=len(ids)-1;d=p-e-1
                assert len(ids)==320,(family,mode,planned,len(ids))
                assert d==({16:actual_near,64:64,128:128}[planned]),(family,mode,planned,d,d0)
                cc=[]
                for cand in candidates:
                    full=enc(text+cand['text']);assert full[:len(ids)]==ids
                    assert full[len(ids):]==cand['token_ids']
                    cc.append(dict(cand,full_ids=full))
                # Outside explicitly marked lure, only the evidence fact can contain either answer noun phrase.
                outside=text[:len(header+''.join(before))]+text[len(header+''.join(before))+len(ftext):]
                leaks=[x for x in [a,b] if re.search(r'\b'+re.escape(x)+r'\b',outside,re.I)]
                assert not leaks or mode=='lure',(family,mode,leaks)
                panel.append(dict(id=f'{family}_{mode}_{planned}_{label}',family=family,template=familyrec['template'],split=split,mode=mode,planned_distance=planned,actual_distance=None if mode=='baseline' else d,nominal_slot_distance=d,gold=None if mode=='baseline' else label,text=text,token_ids=ids,offsets=ee.offsets,evidence_item=x if mode!='baseline' else None,evidence_char_span=[charstart,charend] if mode!='baseline' else None,evidence_token_positions=ev if mode!='baseline' else [],evidence_token_ids=[ids[j] for j in ev] if mode!='baseline' else [],evidence_last_position=e if mode!='baseline' else None,target_position=p,target_token_id=ids[p],local_suffix=sx,candidates=cc,filler_inventory=inventory,intentional_lure=mode=='lure',outside_fact_answer_words=leaks))
jsonl(R/'data/panel.jsonl',panel);dump(R/'data/families.json',families)
dump(R/'data/templates.json',dict(main_facts=facts,main_questions=questions,paraphrases=para,filler_bank=bank))
checks=[]
for f in families:
    for mode in ['main']+(['paraphrase','lure'] if f['split']=='heldout' else []):
        ps=[p for p in panel if p['family']==f['family'] and p['mode']==mode]
        for distance in sorted({p['planned_distance'] for p in ps}):
            a,b=[p for p in ps if p['planned_distance']==distance]
            if mode!='lure':
                assert a['local_suffix']==b['local_suffix']
                la,ra=a['evidence_char_span'];lb,rb=b['evidence_char_span']
                assert a['text'][:la]==b['text'][:lb] and a['text'][ra:]==b['text'][rb:]
        for gold in 'AB':
            qs=[p for p in ps if p['gold']==gold]
            assert len({tuple(p['filler_inventory']) for p in qs})==1
            assert len({tuple(sorted(p['token_ids'])) for p in qs})==1
        checks.append(dict(family=f['family'],mode=mode,rows=len(ps),PASS=True))
dump(R/'evidence/construction.json',dict(UTC=now(),rows=len(panel),families=len(families),heldout=24,smoke=4,checks=checks,all_prefix_lengths=[320],actual_distances=sorted({p['actual_distance'] for p in panel if p['actual_distance'] is not None}),candidate_lengths=sorted({len(c['token_ids']) for p in panel for c in p['candidates']}),unmatched_pairs=0))
cfg=dict(experiment='R18_NEAR_FAR_OBJECT_FACT_USE_20261104',created_utc=now(),model=str(MODEL),model_asset='model_qwen3_0p6b_base_official_a5',tokenizer_asset='tokenizer_qwen3_0p6b_base_official_a5',input_sha256={str(MODEL/x):sha(MODEL/x) for x in ['config.json','tokenizer.json','model.safetensors']},panel_sha256=sha(R/'data/panel.jsonl'),family_sha256=sha(R/'data/families.json'),seed=20261104,prefix_length=320,scoring_shape=[2,328],dtype='float32',device='cpu',threads=2,max_wall_seconds=3600,planned_distances=[16,64,128],gap_definition='p - e - 1; excludes evidence-last-token e and prefix-last-token p',training_updates=0,SAE_loaded=False,intervention=False,scientific_acceptance='Unknown',execution_authorization='Current user explicitly requests full bounded behavior experiment and stop before SAE; local CPU execution authorized.',primary='main heldout per-family both A and B correct, ties fail',point_gate=.8,adequacy_description='24 heldout families, 24 distinct item pairs, six template strata; report uncertainty and near-threshold cases as insufficient',uncertainty='95% Wilson over families; paired family bootstrap for margins; template-cluster bootstrap sensitivity; 10000 replicates',gate_interpretation='point rate >=.80 is numerical gate only; if interval overlaps .80, evidence for stable main condition is insufficient; no scientific approval inferred',baseline='No identifiable item: object / small object; no correctness label; nominal slot only',secondary='heldout paraphrase at all distances; heldout nearest wrong-item lure at128 only; never rescue primary failure')
dump(R/'config.json',cfg)
shutil.copy('/tmp/longshort_1104_assets.json',R/'evidence/input_access.json')
print(json.dumps(dict(rows=len(panel),families=len(families),actual_distances=sorted({p['actual_distance'] for p in panel if p['actual_distance'] is not None}))))
