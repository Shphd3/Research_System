#!/usr/bin/env python3
"""Source-conditioned binary relations and genuine decoder contribution moments."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='2'
from pathlib import Path
import csv, hashlib, importlib.util, json, time
import numpy as np
import torch
from scipy import sparse

E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
P=E/'analysis/feature_relation_phase1/20261013T173130Z'
OLD=E/'analysis/feature_frequency/20261015T143300Z'
OUT=E/'analysis/phi_relations_20261018'
GIDS=[68,34,14]
def load(p):return json.loads(Path(p).read_text())
def clean(x):
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    if isinstance(x,np.ndarray):return clean(x.tolist())
    if isinstance(x,np.generic):return clean(x.item())
    if isinstance(x,float) and not np.isfinite(x):return None
    return x
def dump(p,x):Path(p).write_text(json.dumps(clean(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def csvout(p,rows):
    if not rows:return
    with Path(p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(clean(rows))
def h64(*xs):return int.from_bytes(hashlib.sha256(':'.join(map(str,xs)).encode()).digest()[:8],'little')
def phi(C,n,N):
    p=n/N;cov=C/N-np.outer(p,p);den=np.sqrt(np.outer(p*(1-p),p*(1-p)))
    return np.divide(cov,den,out=np.full_like(cov,np.nan),where=den>0)

def conditional_stats(weights,cbs,nbs,num_b,m):
    n_s=weights@nbs;N=n_s.sum();D=m*(m-1)
    cs=np.tensordot(weights,cbs,axes=(0,0))
    total=cs.sum(0)
    Q=float(weights@num_b/N/D)
    pair_s=cs.sum(1)**2-(cs*cs).sum(1)
    Q0=float((total.sum()**2-total@total)/N**2/D)
    Qcond=float(np.divide(pair_s,n_s,out=np.zeros_like(n_s),where=n_s>0).sum()/N/D)
    same_b=(cbs.sum(2)**2-(cbs*cbs).sum(2))
    numerator=pair_s-weights@same_b
    denom=n_s*n_s-weights@(nbs*nbs)
    active=n_s>0
    Qcross=float(np.sum((n_s[active]/N)*np.divide(numerator[active],denom[active]))/D) if np.all(denom[active]>0) else np.nan
    cb=cbs.sum(1);nb=nbs.sum(1)
    d0=N*N-weights@(nb*nb)
    u0=(total.sum()**2-total@total)-weights@(cb.sum(1)**2-(cb*cb).sum(1))
    Q0cross=float(u0/d0/D) if d0>0 else np.nan
    return np.array([Q,Q0,Qcond,Q-Q0,Q-Qcond,Qcond-Q0,Q0cross,Qcross,
                     Q-Q0cross,Q-Qcross,Qcross-Q0cross])

METRICS=['Q','Q0','Q0_cond','excess_unconditional','excess_conditional','attenuation',
         'Q0_crossblock','Q0_cond_crossblock','excess_cross_unconditional',
         'excess_cross_conditional','attenuation_crossblock']

def bootstrap(cbs,nbs,num_b,m,reps=500):
    rng=np.random.default_rng(20261018);B=len(nbs)
    draws=np.empty((reps,len(METRICS)))
    for j in range(reps):
        w=rng.multinomial(B,np.full(B,1/B)).astype(float)
        draws[j]=conditional_stats(w,cbs,nbs,num_b,m)
    return {metric:{'lo':float(np.nanquantile(draws[:,i],.025)) if np.isfinite(draws[:,i]).any() else None,
                    'hi':float(np.nanquantile(draws[:,i],.975)) if np.isfinite(draws[:,i]).any() else None,
                    'valid_draws':int(np.isfinite(draws[:,i]).sum())}
            for i,metric in enumerate(METRICS)}

def main():
    t0=time.monotonic();assert (OUT/'panel.npz').exists()
    z=np.load(OUT/'panel.npz');Z=z['z'];features=z['feature_id'];side=z['side']
    pos=z['position'];token=z['token_id'];offset=z['offset'];block=z['block'];context=z['context']
    groups={g['group_id']:g for g in load(OLD/'main/groups_D.json') if g['size']>1}
    selected=load(OUT/'selection_D.json');cores=selected['core_members']
    cols={int(f):i for i,f in enumerate(features)}
    split=load(P/'split_manifest.json');Ns=[split['N_D'],split['N_V']]
    freq=np.load(P/'feature_frequency.npz')['n']
    CD=np.load(P/'counts/total0.npy',mmap_mode='r');CV=np.load(P/'counts/total1.npy',mmap_mode='r')
    # Full-window core partition. Positive/negative and raw/fixed-denominator are all retained.
    core_rows=[];pair_rows=[];member_rows=[]
    for gid,g in groups.items():
        fs=np.array(g['members']);m=len(fs);core=np.isin(fs,cores[str(gid)])
        cu=core[:,None]|core[None,:];tri=np.triu(np.ones((m,m),bool),1)
        for si,label,C in [(0,'D',CD),(1,'V',CV)]:
            p=freq[si,fs]/Ns[si];joint=np.asarray(C[np.ix_(fs,fs)],float)/Ns[si]
            cov=joint-np.outer(p,p)
            parts={}
            for name,mask in [('core',tri&cu),('rest',tri&~cu)]:
                a=cov[mask];parts[name+'_positive']=float(2*a[a>0].sum())
                parts[name+'_negative']=float(2*a[a<0].sum())
            total=sum(parts.values());remaining=parts['rest_positive']+parts['rest_negative']
            edgeval=cov[tri];top10=np.flatnonzero(tri)[np.argsort(-edgeval,kind='stable')[:10]]
            row={'group_id':gid,'side':label,'size':m,'core_members':cores[str(gid)],
                 'N_positions':Ns[si],'total_numerator':total,'rest_numerator':remaining,
                 'rest_fraction':remaining/total if abs(total)>1e-15 else None,
                 'fixed_denominator':m*(m-1),'total_fixed_normalized':total/(m*(m-1)),
                 'rest_fixed_normalized':remaining/(m*(m-1)),
                 'top10_pairs_overlap_core_count':int(cu.ravel()[top10].sum()),**parts}
            core_rows.append(row)
        for f in fs:
            member_rows.append({'group_id':gid,'group_size':m,'feature_id':int(f),'n_D':int(freq[0,f]),'N_D':Ns[0],
                               'p_D':float(freq[0,f]/Ns[0]),'n_V':int(freq[1,f]),'N_V':Ns[1],
                               'p_V':float(freq[1,f]/Ns[1]),'D_core':int(f) in cores[str(gid)]})
    csvout(OUT/'all186_core_decomposition.csv',core_rows);csvout(OUT/'all_members_frequency.csv',member_rows)
    # Conditions are chosen by D support only; V support is subsequently frozen.
    tokD,ctD=np.unique(token[~side],return_counts=True)
    exact=[int(t) for t,n in zip(tokD,ctD) if n>=50 and len(np.unique(block[(~side)&(token==t)]))>=5]
    exact=np.array(exact,np.int32);cat=np.full(len(token),len(exact),np.int32)
    for i,t in enumerate(exact):cat[token==t]=i
    cell=cat*4+offset//256;S0=(len(exact)+1)*4
    counts={};block_counts={}
    for si,label in [(False,'D'),(True,'V')]:
        counts[label]=np.bincount(cell[side==si],minlength=S0)
        unique=np.unique(cell[side==si]*81+block[side==si])
        block_counts[label]=np.bincount(unique//81,minlength=S0)
    eligible=(counts['D']>=20)&(block_counts['D']>=3)
    supported=eligible&(counts['V']>=20)&(block_counts['V']>=3)
    use=side&supported[cell];keepcells=np.flatnonzero(supported);lookup=np.full(S0,-1,np.int32);lookup[keepcells]=np.arange(len(keepcells))
    bs,bi=np.unique(block[use],return_inverse=True);cs=lookup[cell[use]]
    B,S=len(bs),len(keepcells)
    nbs=np.bincount(bi*S+cs,minlength=B*S).reshape(B,S).astype(float)
    condition_rows=[{'cell_id':i,'token_id':int(exact[i//4]) if i//4<len(exact) else 'OTHER',
                     'position_bin':int(i%4),'D_rows':int(counts['D'][i]),'D_blocks':int(block_counts['D'][i]),
                     'V_rows':int(counts['V'][i]),'V_blocks':int(block_counts['V'][i]),
                     'D_eligible':bool(eligible[i]),'V_common_supported':bool(supported[i])} for i in range(S0)]
    csvout(OUT/'condition_support.csv',condition_rows)
    dump(OUT/'condition_selection.json',{'D_exact_token_ids':exact,'position_bins':[0,256,512,768,1024],
        'D_eligible_cells':np.flatnonzero(eligible),'V_supported_cells':keepcells,
        'V_panel_rows':int(side.sum()),'V_used_rows':int(use.sum()),'coverage':float(use.sum()/side.sum()),
        'V_original_blocks':B,'V_coarse_intervals':len(np.unique(bs//8)),
        'primary_position_ids':pos[use],'selection_only_counts_no_outcome':True})
    conditional_rows=[];conditions_summary={}
    for gid in GIDS:
        fs=np.array(groups[gid]['members']);A=(Z[:,[cols[int(f)] for f in fs]]>0).astype(float)
        AU=A[use];K=AU.sum(1);m=len(fs)
        cbs=(sparse.csr_matrix((np.ones(len(bi)),(bi*S+cs,np.arange(len(bi)))),shape=(B*S,len(bi)))@AU).reshape(B,S,m)
        num_b=np.bincount(bi,weights=K*(K-1),minlength=B)
        values=conditional_stats(np.ones(B),cbs,nbs,num_b,m)
        ci=bootstrap(cbs,nbs,num_b,m) if B>=20 else {}
        coarse,cc=np.unique(bs//8,return_inverse=True)
        cco=np.array([cbs[cc==i].sum(0) for i in range(len(coarse))])
        nco=np.array([nbs[cc==i].sum(0) for i in range(len(coarse))])
        qco=np.array([num_b[cc==i].sum() for i in range(len(coarse))])
        coarseci=bootstrap(cco,nco,qco,m) if len(coarse)>=8 else {}
        for i,key in enumerate(METRICS):
            conditional_rows.append({'group_id':gid,'metric':key,'value':float(values[i]),'N_V_common_positions':int(use.sum()),
                'V_blocks':B,'coarse_intervals':len(coarse),'lo_block':ci.get(key,{}).get('lo'),
                'hi_block':ci.get(key,{}).get('hi'),'valid_block_draws':ci.get(key,{}).get('valid_draws'),
                'lo_coarse':coarseci.get(key,{}).get('lo'),'hi_coarse':coarseci.get(key,{}).get('hi')})
        conditions_summary[str(gid)]={key:float(values[i]) for i,key in enumerate(METRICS)}
        np.savez_compressed(OUT/f'conditional_sufficient_G{gid:03d}.npz',cbs=cbs,nbs=nbs,num_b=num_b,block_ids=bs)
        print('conditional',gid,flush=True)
    csvout(OUT/'conditional_metrics.csv',conditional_rows);dump(OUT/'conditional_summary.json',conditions_summary)
    # Actual decoder vectors, saved TRAIN scales, shared Z, uncentered contribution energy.
    torch.set_num_threads(2)
    payload=torch.load(E/'runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt',map_location='cpu',mmap=True,weights_only=False)
    decoder=payload['crosscoder']['decoder'];rms=payload['normalization']['rms'].numpy()
    geometry_rows=[];energy_rows=[];qual=[];directions28={}
    for gid in GIDS:
        fs=np.array(groups[gid]['members']);m=len(fs);cols_g=[cols[int(f)] for f in fs]
        zg=Z[side][:,cols_g].astype(float);A=(zg>0).astype(float);n=A.sum(0);N=len(zg)
        C=A.T@A;ph=phi(C,n,N);z2=zg.T@zg/N
        display=list(cores[str(gid)])
        for f in sorted(fs,key=lambda f:(-freq[0,f],int(f))):
            if int(f) not in display:display.append(int(f))
            if len(display)>=min(24,m):break
        if m<=24:display=fs.tolist()
        local=np.array([int(np.flatnonzero(fs==f)[0]) for f in display])
        pack={'feature_id':fs,'phi_V_panel':ph,'panel_V_n':n,'panel_V_N':np.array(N),
              'display_feature_id':np.array(display),'z_second_moment':z2}
        for layer,source in [(28,13),(2,0),(14,6)]:
            d=decoder[source,fs,:].detach().numpy().astype(float)*rms[source]
            if layer==28:directions28[gid]=d.copy()
            gram=d@d.T;norm=np.sqrt(np.diag(gram));cos=np.divide(gram,np.outer(norm,norm),out=np.full_like(gram,np.nan),where=np.outer(norm,norm)>0)
            selfv=float(np.dot(np.diag(z2),np.diag(gram)))
            crossmat=2*z2*gram;tri=np.triu(np.ones((m,m),bool),1);pairs=crossmat[tri]
            cross=float(pairs.sum());total=selfv+cross
            assert total>=-1e-6*max(selfv,1)
            sample=zg[:128];direct=np.square(sample@d).sum()/len(sample)
            algebra=float(((sample.T@sample/len(sample))*gram).sum())
            err=abs(direct-algebra)/max(abs(direct),1);assert err<1e-10
            qual.append({'group_id':gid,'layer':layer,'direct128_relative_error':err})
            energy_rows.append({'group_id':gid,'layer':layer,'source_index':source,'TRAIN_rms':float(rms[source]),
                'N_V_panel':N,'hit_positions':int((A.sum(1)>0).sum()),'self':selfv,'cross':cross,
                'cross_positive':float(pairs[pairs>0].sum()),'cross_negative':float(pairs[pairs<0].sum()),
                'total_mean_square_contribution':total,'cross_over_self':cross/selfv if selfv>0 else None,
                'positive_z_pair_count':int(np.count_nonzero(z2[tri]>0)),
                'undefined_phi_pairs':int(np.count_nonzero(~np.isfinite(ph[tri]))),
                'cosine_mean':float(np.nanmean(cos[tri])),'negative_cosine_fraction':float(np.mean(cos[tri]<0))})
            pack[f'cosine_layer{layer}']=cos;pack[f'cross_energy_layer{layer}']=crossmat
            for i in range(m):
                for j in range(i+1,m):
                    geometry_rows.append({'group_id':gid,'layer':layer,'feature_i':int(fs[i]),'feature_j':int(fs[j]),
                        'phi_V_panel':float(ph[i,j]),'decoder_cosine':float(cos[i,j]),
                        'E_zi_zj':float(z2[i,j]),'cross_mean_square_contribution':float(crossmat[i,j])})
        np.savez_compressed(OUT/f'geometry_G{gid:03d}.npz',**pack)
        np.savez_compressed(OUT/f'activation_G{gid:03d}.npz',feature_id=fs,position=pos[side],
             packed_binary=np.packbits((zg>0).astype(np.uint8),axis=1),shape=np.array(zg.shape))
    csvout(OUT/'geometry_all_pairs.csv',geometry_rows);csvout(OUT/'contribution_energy.csv',energy_rows)
    dump(OUT/'geometry_qualification.json',{'status':'PASS','checks':qual,'quantity':'uncentered mean square reconstruction contribution, not covariance or raw hidden fidelity'})
    # Case positions and full visible prefixes; avoid textual/theme selection.
    spec=importlib.util.spec_from_file_location('old_cases',E/'analysis_tools/group_understanding/extract_cases.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    tokenizer=old.FrozenDecoder('/data/share/Qwen3-0.6B-Base/tokenizer.json')
    index=E/'data/direct_dclm_bins_a15/index_val';meta=load(index/'manifest.json')
    records=np.load(index/'records.npy');bins=[np.memmap(x['path'],dtype='<u4',mode='r') for x in meta['sources']]
    cases=[];case_cells=[];sampling=[];case_dir=OUT/'prefixes';case_dir.mkdir(exist_ok=True)
    for gid in GIDS:
        fs=np.array(groups[gid]['members']);zg=Z[:,[cols[int(f)] for f in fs]];K=(zg>0).sum(1)
        hits=np.flatnonzero(side&(K>0));sing=np.flatnonzero(side&(K==1))
        random=sorted(hits,key=lambda r:(h64(20261018,gid,int(pos[r])),int(pos[r])))[:6]
        high=sorted(hits,key=lambda r:(-int(K[r]),h64(20261018,'high',gid,int(pos[r]))))[:6]
        single=sorted(sing,key=lambda r:(h64(20261018,'single',gid,int(pos[r])),int(pos[r])))[:3]
        choose={}
        for kind,rr in [('random_hit',random),('high_K',high),('single_member',single)]:
            for row in rr:choose.setdefault(int(row),[]).append(kind)
        sampling.append({'group_id':gid,'V_panel_positions':int(side.sum()),'available_hit_positions':len(hits),
                         'available_single_member_positions':len(sing),'random_selected':len(random),
                         'highK_selected':len(high),'single_selected':len(single),'unique_positions':len(choose),
                         'maximum_K_panel_V':int(K[side].max()),'all_members':len(fs)})
        for order,(row,kinds) in enumerate(choose.items()):
            ctx=int(context[row]);fi,start,length,limit=map(int,records[ctx]);tt=int(offset[row])
            tokens=np.asarray(bins[fi][start:start+length]);assert int(tokens[tt])==int(token[row])
            visible=tokenizer.decode(tokens[:tt+1]);name=f'G{gid:03d}_p{int(pos[row])}'
            (case_dir/(name+'.txt')).write_text(visible)
            display=np.load(OUT/f'geometry_G{gid:03d}.npz')['display_feature_id']
            active=[{'feature_id':int(f),'z':float(v)} for f,v in zip(fs,zg[row]) if v>0]
            v=zg[row].astype(float);d=directions28[gid]
            self_energy=float(np.dot(v*v,np.square(d).sum(1)))
            actual_vector=v@d;total_energy=float(actual_vector@actual_vector)
            item={'case_id':name,'group_id':gid,'group_size':len(fs),'categories':kinds,
                'panel_row':row,'position_id':int(pos[row]),'block_id':int(block[row]),'context_id':ctx,
                'context_offset_zero_based':tt,'token_id':int(token[row]),'token':tokenizer.decode([token[row]]),
                'K_full':int(K[row]),'K_display':sum(a['feature_id'] in display for a in active),
                'active_members':active,'prefix_file':'prefixes/'+name+'.txt',
                'layer28_self_energy':self_energy,'layer28_cross_energy':total_energy-self_energy,
                'layer28_total_energy':total_energy,
                'visible_prefix':visible,'prefix_token_count':tt+1,'display_suffix':visible[-350:],
                'source_path':meta['sources'][fi]['path'],'source_sha256_from_manifest':meta['sources'][fi]['sha256'],
                'absolute_source_token_offset':start+tt,'actual_next_token_id_label_only':int(tokens[tt+1]) if tt+1<len(tokens) else None,
                'original_document_id':'UNKNOWN'}
            cases.append(item)
            for f,v in zip(fs,zg[row]):case_cells.append({'case_id':name,'group_id':gid,'position_id':int(pos[row]),'feature_id':int(f),'active':int(v>0),'z':float(v)})
        csvout(OUT/f'case_G{gid:03d}_full_matrix.csv',[{'position_id':int(pos[r]),'categories':'|'.join(kinds),'K_full':int(K[r]),**{str(int(f)):int(v>0) for f,v in zip(fs,zg[r])}} for r,kinds in choose.items()])
    dump(OUT/'cases.json',cases);dump(OUT/'case_sampling_summary.json',sampling);csvout(OUT/'case_all_member_values.csv',case_cells)
    flat=[{k:v for k,v in x.items() if k not in ('active_members','visible_prefix')} for x in cases]
    csvout(OUT/'case_positions.csv',flat)
    # Token and sequence-position composition on panel and full evaluation.
    composition=[];position_rows=[];window=np.load(OUT/'window_token_counts.npz')['counts'][1]
    for gid in GIDS:
        fs=groups[gid]['members'];K=(Z[:,[cols[int(f)] for f in fs]]>0).sum(1);hit=side&(K>0)
        ct=np.bincount(token[hit],minlength=len(window))
        positive=np.flatnonzero(ct>0)
        for tid in positive[np.argsort(-ct[positive],kind='stable')[:15]]:
            composition.append({'group_id':gid,'token_id':int(tid),'token':tokenizer.decode([tid]),'group_hit_count_panel':int(ct[tid]),
                'group_hit_positions_panel':int(hit.sum()),'group_token_fraction':float(ct[tid]/hit.sum()) if hit.sum() else None,
                'V_panel_token_fraction':float(np.mean(token[side]==tid)),
                'V_full_token_count':int(window[tid].sum()),'V_full_positions':Ns[1],
                'V_full_token_fraction':float(window[tid].sum()/Ns[1])})
        for q in range(4):
            position_rows.append({'group_id':gid,'position_bin':q,'group_fraction':float(np.mean(offset[hit]//256==q)),
                                 'V_panel_fraction':float(np.mean(offset[side]//256==q)),
                                 'V_full_fraction':float(window[:,q].sum()/Ns[1])})
    csvout(OUT/'token_composition.csv',composition);csvout(OUT/'position_composition.csv',position_rows)
    # Bounded old raw-hidden results: copy data only, never recompute eigenvalues.
    oldspec=Path('/data/250010109/Research_System/daily_research_reports/1016/crosscoder_phi_input_spectrum')
    spectrum=[]
    for r in csv.DictReader((oldspec/'data/paired_group_contrasts.csv').open()):
        if r['population']=='main_RFN':spectrum.append(r)
    csvout(OUT/'old_spectrum_paired_strata.csv',spectrum)
    dump(OUT/'completion.json',{'status':'COMPLETE','seconds':time.monotonic()-t0,'case_groups':GIDS,
        'conditional_groups':3,'core_groups':186,'geometry_layers':[28,2,14],
        'cases':len(cases),'H1_support_positions':int(use.sum()),'H1_coverage':float(use.sum()/side.sum()),
        'old_spectrum_reused_not_recomputed':True,'new_forward_calls':0,'training_updates':0})
    print('COMPLETE',time.monotonic()-t0,flush=True)

if __name__=='__main__':main()
