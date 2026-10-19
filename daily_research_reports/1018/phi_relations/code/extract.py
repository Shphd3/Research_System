#!/usr/bin/env python3
"""One immutable-cache pass: frozen group panel, full K and chain counts."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[key]='2'
from pathlib import Path
import csv, datetime, hashlib, importlib.util, json, time
import numpy as np
from numba import njit

E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
P=E/'analysis/feature_relation_phase1/20261013T173130Z'
OLD=E/'analysis/feature_frequency/20261015T143300Z'
OUT=E/'analysis/phi_relations_20261018'
GIDS=[68,34,14]
def load(p):return json.loads(Path(p).read_text())
def dump(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def csvout(p,rows):
    if not rows:return
    with Path(p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(**kw):print(json.dumps(kw,ensure_ascii=False),flush=True)
def h64(*a):return int.from_bytes(hashlib.sha256(':'.join(map(str,a)).encode()).digest()[:8],'little')
def phi(C,n,N):
    p=n/N;cov=C/N-np.outer(p,p);den=np.sqrt(np.outer(p*(1-p),p*(1-p)))
    return np.divide(cov,den,out=np.full_like(cov,np.nan),where=den>0)

@njit
def group_counts(ptr,ids,lookup,bits):
    nr=len(ptr)-1;counts=np.zeros((nr,3),np.uint16);flags=np.zeros(nr,np.uint8)
    for r in range(nr):
        for k in range(ptr[r],ptr[r+1]):
            f=ids[k];g=lookup[f]
            if g>=0:counts[r,g]+=1
            flags[r]|=bits[f]
    return counts,flags

def main():
    t0=time.monotonic();OUT.mkdir(parents=True,exist_ok=True)
    assert (OUT/'protocol_freeze.json').exists()
    assert not (OUT/'panel.npz').exists(),'Do not overwrite completed/partial panel'
    groups={g['group_id']:g for g in load(OLD/'main/groups_D.json') if g['size']>1}
    freq=np.load(P/'feature_frequency.npz');nD,nV=freq['n'];split=load(P/'split_manifest.json')
    ND,NV=split['N_D'],split['N_V'];CD=np.load(P/'counts/total0.npy',mmap_mode='r')
    cores={};core_scores={}
    for gid,g in groups.items():
        members=np.array(g['members']);p=nD[members]/ND
        cov=np.asarray(CD[np.ix_(members,members)],float)/ND-np.outer(p,p)
        np.fill_diagonal(cov,0);score=np.maximum(cov,0).sum(1)
        order=np.lexsort((members,-score));cores[str(gid)]=members[order[:3]].tolist()
        core_scores[str(gid)]={str(int(members[i])):float(score[i]) for i in order[:3]}
    edges=list(csv.DictReader((OLD/'main/edges_D.csv').open()))
    adj={i:set() for i in groups[14]['members']}
    for row in edges:
        u,v=int(row['u']),int(row['v'])
        if u in adj and v in adj:adj[u].add(v);adj[v].add(u)
    members=np.array(groups[14]['members']);ph=phi(np.asarray(CD[np.ix_(members,members)],float),nD[members],ND)
    loc={int(f):i for i,f in enumerate(members)};best=None
    for b in members:
        nb=sorted(adj[int(b)])
        for ai,a in enumerate(nb):
            for c in nb[ai+1:]:
                if c in adj[a]:continue
                score=min(ph[loc[a],loc[int(b)]],ph[loc[int(b)],loc[c]])-ph[loc[a],loc[c]]
                candidate=(float(score),-a,-int(b),-c)
                if best is None or candidate>best:best=candidate
    chain=[-int(x) for x in best[1:]]
    selection={'core_rule':'NEW same-source recheck: full D all-pair positive covariance row sum; top3 IDties; historical E/F rule unavailable',
               'core_members':cores,'core_scores':core_scores,'chain_G014':chain,
               'chain_rule':'D frozen edges AB,BC; AC not edge; max min(phiAB,phiBC)-phiAC then smallerID',
               'selected_before_V_statistics':True}
    dump(OUT/'selection_D.json',selection)
    features=np.array(sorted(set(sum([groups[g]['members'] for g in GIDS],[]))),np.int32)
    look=np.full(16384,-1,np.int32);look[features]=np.arange(len(features))
    group_lookup=np.full(16384,-1,np.int32)
    for j,g in enumerate(GIDS):group_lookup[groups[g]['members']]=j
    bits=np.zeros(16384,np.uint8)
    for i,f in enumerate(chain):bits[f]=1<<i
    chunks=[]
    for rank in load(P/'feature_cache/manifest.json')['ranks']:chunks.extend(load(rank)['chunks'])
    chunks.sort(key=lambda x:x['start'])
    assert len(chunks)==640
    ends=np.array([b['position_end'] for b in split['blocks']])
    block_sides=np.array([b['side']=='V' for b in split['blocks']])
    rng=np.random.default_rng(20261017)
    Z=np.zeros((len(chunks)*100,len(features)),np.float32)
    pos=np.empty(len(Z),np.int64);block=np.empty(len(Z),np.int32)
    hist={f'{g}_{side}':np.zeros(groups[g]['size']+1,np.int64) for g in GIDS for side in 'DV'}
    flaghist=np.zeros((2,8),np.int64);chain_first={};checks=[]
    for ci,meta in enumerate(chunks):
        lo,hi=meta['start'],meta['end'];nr=hi-lo
        rr=np.sort(rng.choice(nr,100,replace=False));pp=lo+rr
        pos[ci*100:(ci+1)*100]=pp;block[ci*100:(ci+1)*100]=np.searchsorted(ends,pp,side='right')
        with np.load(meta['file']) as cache:
            ptr,ids=cache['ptr'],cache['ids']
            k,flag=group_counts(ptr,ids,group_lookup,bits)
            bb=np.searchsorted(ends,np.arange(lo,hi),side='right');ss=block_sides[bb]
            for s in (0,1):
                mask=ss==s;flaghist[s]+=np.bincount(flag[mask],minlength=8)
                for j,g in enumerate(GIDS):
                    hist[f'{g}_{"DV"[s]}']+=np.bincount(k[mask,j],minlength=groups[g]['size']+1)
                if s==1:
                    for f in (3,5,6,7):
                        key=str(f);found=np.flatnonzero(mask&(flag==f))
                        chain_first.setdefault(key,[]).extend((lo+found).tolist()[:3])
                        chain_first[key]=chain_first[key][:3]
            values=cache['z']
            for outrow,row in enumerate(rr,ci*100):
                aa,zz=cache['ids'][int(ptr[row]):int(ptr[row+1])],values[int(ptr[row]):int(ptr[row+1])]
                col=look[aa];keep=col>=0;Z[outrow,col[keep]]=zz[keep]
            if ci in (0,160,320,480):
                digest=sha(meta['file']);assert digest==meta['sha256'];checks.append({'path':meta['file'],'sha256':digest})
        if ci%32==0:log(stage='cache_scan',chunk=ci,total=640,seconds=round(time.monotonic()-t0,1))
        if time.monotonic()-t0>1800:raise RuntimeError('30 minute scan boundary; no automatic retry')
    index=E/'data/direct_dclm_bins_a15/index_val';manifest=load(index/'manifest.json')
    prefix=np.load(index/'prefix.npy');records=np.load(index/'records.npy')
    bins=[np.memmap(s['path'],dtype='<u4',mode='r') for s in manifest['sources']]
    context=np.searchsorted(prefix,pos,side='right')-1
    token=np.empty(len(pos),np.int32);offset=np.empty(len(pos),np.int16);absolute=np.empty(len(pos),np.int64)
    window_counts=np.zeros((2,151936,4),np.int64)
    for ctx,record in enumerate(records):
        fi,start,length,limit=map(int,record);tokens=np.asarray(bins[fi][start:start+length])
        eligible=np.flatnonzero(~np.isin(tokens,manifest['excluded_ids']))[:limit]
        side=int(block_sides[min(ctx//128,len(block_sides)-1)])
        np.add.at(window_counts[side],(tokens[eligible],eligible//256),1)
        rows=np.flatnonzero(context==ctx)
        if len(rows):
            tt=eligible[pos[rows]-prefix[ctx]];token[rows]=tokens[tt];offset[rows]=tt;absolute[rows]=start+tt
    assert tuple(window_counts.sum((1,2)))==(ND,NV)
    np.savez_compressed(OUT/'panel.npz',z=Z,feature_id=features,position=pos,block=block,
                        side=block_sides[block],context=context,token_id=token,offset=offset,absolute=absolute)
    np.savez_compressed(OUT/'full_K_and_chain.npz',**hist,chain_flag_hist=flaghist)
    np.savez_compressed(OUT/'window_token_counts.npz',counts=window_counts)
    dump(OUT/'full_chain_counts.json',{'members':chain,'flag_definition':'bits A=1 B=2 C=4; full D/V allpositions',
        'D_hist':flaghist[0].tolist(),'V_hist':flaghist[1].tolist(),'V_first_positions_by_exact_flag':chain_first})
    dump(OUT/'extraction_receipt.json',{'status':'COMPLETE','positions':len(pos),
        'D_positions':int((~block_sides[block]).sum()),'V_positions':int(block_sides[block].sum()),
        'D_full_positions':ND,'V_full_positions':NV,'full_shared_z_features':len(features),
        'selected_groups':GIDS,'cache_chunks':640,'spot_hash_checks':checks,
        'panel_sha256':sha(OUT/'panel.npz'),'panel_seed':20261017,'seconds':time.monotonic()-t0,
        'inference_calls':0,'training_updates':0,'raw_hidden_same_structure_rows':'NOT_AVAILABLE',
        'old_1017_report_paths':'MISSING_ON_THIS_HOST; old source and pause receipts read',
        'cache_source':str(P/'feature_cache/manifest.json'),'index_source':str(index/'manifest.json')})
    log(stage='COMPLETE',seconds=time.monotonic()-t0,chain=chain)

if __name__=='__main__':main()
