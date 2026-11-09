"""Read native saved decoders and cached token examples, without model construction."""
from pathlib import Path
import json,hashlib,csv,collections,os
import numpy as np
O=Path(__file__).resolve().parent;R=Path(os.environ.get('R04_SOURCE_ROOT',str(O.parent)));A=O/'analysis'

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(8<<20),b''):h.update(b)
    return h.hexdigest()

def main():
    from tokenizers import Tokenizer
    import torch
    torch.set_num_threads(2)
    paths={'SAE':Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt'),
           'CC':Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt')}
    expected={'SAE':'e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65','CC':'09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628'}
    meta={}; groups=json.loads((A/'candidate_freeze.json').read_text())['dictionaries']
    for name in ['SAE','CC']:
        path=paths[name];digest=sha(path);assert digest==expected[name]
        p=torch.load(path,map_location='cpu',mmap=True,weights_only=False)
        ids=np.unique(np.concatenate([np.array(v,dtype=int) for v in groups[name]['groups'].values()]))
        if name=='SAE':
            w=p['state_dict']['decoder.weight'].detach().numpy();assert w.shape==(1024,30000);vectors=w[:,ids].T.astype(float);scale=1.; original_shape=list(w.shape)
        else:
            w=p['crosscoder']['decoder'];assert tuple(w.shape)==(14,16384,1024);scale=float(p['normalization']['rms'][-1]);vectors=w[-1,ids].detach().numpy().astype(float)*scale;original_shape=list(w.shape)
        norms=np.linalg.norm(vectors,axis=1);unit=vectors/norms[:,None];old=np.load(R/f'forward/documents_{name}.npz')['decoder_norm'][ids]
        assert np.allclose(norms,old,rtol=2e-6,atol=1e-5)
        assert np.max(abs(np.linalg.norm(unit,axis=1)-1))<1e-12
        np.savez_compressed(A/f'{name}_selected_native_decoder.npz',feature_ids=ids,native_decoder=vectors,unit_native_decoder=unit,native_norm=norms,layer_zero_based=27)
        meta[name]={'path':str(path),'sha256_fresh':digest,'checkpoint_decoder_shape':original_shape,'selected_count':len(ids),'space':'block27 MLP input after native post-attention layernorm' if name=='SAE' else 'block27 residual-post before final global norm','native_scale':scale,'native_norm_matches_R04':True,'unit_norm_max_abs_error':float(np.max(abs(np.linalg.norm(unit,axis=1)-1))),'spectral_projection':'NOT_RUN_MISSING_TRUE_H','model_constructed':False}
        del p,w
    tokpath=Path('/data/share/Qwen3-0.6B-Base/tokenizer.json');tsha=sha(tokpath)
    assert tsha=='c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539'
    tok=Tokenizer.from_file(str(tokpath));docs=[json.loads(s) for s in (R/'data/documents.jsonl').read_text().splitlines()];held=[x for x in docs if x['split']=='heldout']
    best=collections.defaultdict(list);tokens=collections.defaultdict(collections.Counter)
    for row in held:
        q=np.load(R/'forward/documents'/f"{row['seq_id']}.npz"); assert q['token_ids'].tolist()==row['token_ids']
        for name in ['SAE','CC']:
            allowed=set(int(i) for i in np.load(A/f'{name}_selected_native_decoder.npz')['feature_ids']);norms=np.load(R/f'forward/documents_{name}.npz')['decoder_norm'];seen={}
            for pos in range(32,192):
                lo,hi=int(q[name+'_ptr'][pos]),int(q[name+'_ptr'][pos+1])
                for feature,z in zip(q[name+'_ids'][lo:hi],q[name+'_z'][lo:hi]):
                    f=int(feature)
                    if f not in allowed:continue
                    text=tok.decode([row['token_ids'][pos]]);tokens[name,f][text]+=1;val=float(z)*float(norms[f])
                    if f not in seen or val>seen[f]['native_contribution']:
                        seen[f]={'dictionary':name,'feature':f,'domain':row['domain'],'seq_id':row['seq_id'],'position':pos,'token_id':row['token_ids'][pos],'token':text,'raw_z':float(z),'native_contribution':val,'visible_prefix_excerpt':tok.decode(row['token_ids'][:pos+1])[-220:],'document_url':row['url']}
            for f,v in seen.items():best[name,f,row['domain']].append(v)
    rows=[]
    for key,v in sorted(best.items()):rows.extend(sorted(v,key=lambda x:(-x['native_contribution'],x['seq_id'],x['position']))[:3])
    with (A/'selected_token_examples.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    tt=[{'dictionary':d,'feature':f,'top5_token_hit_counts':json.dumps(sorted(c.items(),key=lambda x:(-x[1],x[0]))[:5],ensure_ascii=False),'heldout_total_hits':sum(c.values())} for (d,f),c in sorted(tokens.items())]
    with (A/'selected_token_hit_summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(tt[0]));w.writeheader();w.writerows(tt)
    # A direct arithmetic example for one known shared member and one newly displayed member.
    arithmetic=[]
    for name,f in [('SAE',16240),('SAE',11667),('SAE',693),('SAE',5662),('CC',11710)]:
        ag=np.load(R/f'forward/documents_{name}.npz');seq=ag['seq_id'].tolist()
        for domain in ['math','biology']:
            vals=best.get((name,f,domain),[])
            if not vals:continue
            v=sorted(vals,key=lambda x:(-x['native_contribution'],x['seq_id'],x['position']))[0];j=seq.index(v['seq_id']);n=float(ag['counts'][j,f]);s=float(ag['sum_z'][j,f])*float(ag['decoder_norm'][f]);arithmetic.append({**v,'active_positions':int(n),'positions':160,'hit_fraction':n/160,'active_mean_native':s/n,'zero_inclusive_mean_native':s/160,'whole_document_prefix':next(x['prefix'] for x in docs if x['seq_id']==v['seq_id'])})
    (A/'arithmetic_examples.json').write_text(json.dumps(arithmetic,ensure_ascii=False,indent=2)+'\n')
    (O/'decoder_and_token_provenance.json').write_text(json.dumps({'decoders':meta,'tokenizer_sha256_fresh':tsha,'example_rows':len(rows),'selection':'all frozen expanded and old cohorts; highest3 contributions per domain in distinct heldout docs, descriptive only; one source-token at a time, never future text','token_counts':'raw hit counts, not token-conditional preference','new_forwards':0,'model_constructed':False},ensure_ascii=False,indent=2)+'\n')
    print('DECODER_AND_EXAMPLES_DONE',len(rows),json.dumps(meta))

if __name__=='__main__':main()
