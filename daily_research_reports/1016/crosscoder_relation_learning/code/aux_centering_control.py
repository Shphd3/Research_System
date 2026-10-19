#!/usr/bin/env python3
"""Posthoc fixed-v control separating centering offset from projection.

Prediction is frozen in first_direction/centering_control/prediction.json before
this entrypoint runs. Original first-direction endpoints remain immutable.
"""
from data_routes import *


def run(device='cuda:0',root=ROOT):
    import csv
    import torch
    from crosscoder.bin_data_a15 import BinEvents
    root=Path(root)/'first_direction'
    out=root/'centering_control';out.mkdir(exist_ok=True)
    prediction=json.loads((out/'prediction.json').read_text())
    assert prediction['status']=='FROZEN_BEFORE_CONTROL_OUTCOMES'
    torch.set_num_threads(2)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    started=time.monotonic()
    _,ex,coder,stats=load_models(device)
    prior=np.load(root/'direction_data.npz')
    V=torch.from_numpy(prior['v'].copy()).to(device)
    prior_summary=json.loads((root/'summary.json').read_text())
    contexts=np.array(prior_summary['context_ids'])
    events=BinEvents(DATA,'VAL')
    ee=[events[int(i)] for i in contexts]
    tokens=torch.tensor([e['input_ids'] for e in ee],device=device,dtype=torch.long)
    valid=torch.tensor([e['valid_mask'] for e in ee],device=device,dtype=torch.bool)
    buffers={k:v.clone() for k,v in coder.named_buffers()}
    with torch.inference_mode():
        captured=ex.extract(tokens,torch.ones_like(tokens),valid)
        H=captured.activations[captured.position_indices[:,0]>=8].float()
        mu=stats.train_mean.to(device=device,dtype=torch.float32)[None]
        rms=stats.rms.to(device=device,dtype=torch.float32)[None,:,None]
        raw_removed=H-(H*V[None]).sum(-1,keepdim=True)*V[None]
        center_pres=H-((H-mu)*V[None]).sum(-1,keepdim=True)*V[None]
        normalized=stats.normalize(H)
        expected_center=normalized-(normalized*V[None]).sum(-1,keepdim=True)*V[None]
        identity_error=float((stats.normalize(center_pres)-expected_center).abs().max())
        shift=-(mu*V[None]).sum(-1,keepdim=True)*V[None]/rms
        shift_identity_error=float((stats.normalize(raw_removed)-stats.normalize(center_pres)-shift).abs().max())
        codes={name:encode(X,coder,stats) for name,X in [('original',H),('raw_removed',raw_removed),('center_preserved',center_pres)]}
        # Reproduce prior primary endpoints before interpreting new control.
        assert np.array_equal((codes['original']>0).sum(0).cpu().numpy(),prior['n_original'])
        assert np.array_equal((codes['raw_removed']>0).sum(0).cpu().numpy(),prior['n_removed'])
        old_heat=np.load(root/'heatmap_data.npz')
        assert np.array_equal(codes['original'][:256,old_heat['feature_ids']].float().cpu().numpy().T,old_heat['z_original'])
        errors={}
        for name,X in [('original',H),('raw_removed',raw_removed),('center_preserved',center_pres)]:
            raw_sse=torch.zeros(14,device=device,dtype=torch.float64)
            norm_sse=torch.zeros_like(raw_sse)
            for part in X.split(1024):
                normed=stats.normalize(part)
                rec=coder(normed,use_threshold=True).reconstruction
                norm_sse+=(rec.double()-normed.double()).square().sum((0,2))
                raw_sse+=(stats.inverse(rec).double()-part.double()).square().sum((0,2))
            errors[name]={'raw_SSE_by_layer':raw_sse.cpu().tolist(),
                          'normalized_mean_squared_vector_error_by_layer':(norm_sse/len(H)).cpu().tolist()}
    binary={k:(z>0).cpu().numpy() for k,z in codes.items()}
    counts={k:v.sum(0) for k,v in binary.items()}
    N=len(H)
    with (OLD/'main/edges_D.csv').open() as f:edges=list(csv.DictReader(f))
    uv=np.array([(int(x['u']),int(x['v'])) for x in edges],np.int32)
    phi={}
    for name,B in binary.items():
        n=counts[name]
        joint=np.concatenate([(B[:,u]&B[:,v]).sum(0) for u,v in [(x[:,0],x[:,1]) for x in np.array_split(uv,max(1,len(uv)//128))]])
        den=np.sqrt(n[uv[:,0]].astype(float)*(N-n[uv[:,0]])*n[uv[:,1]]*(N-n[uv[:,1]]))
        phi[name]=np.divide(N*joint-n[uv[:,0]]*n[uv[:,1]],den,out=np.full(len(uv),np.nan),where=den>0)
    common=np.isfinite(np.stack(list(phi.values()))).all(0)
    with (out/'fixed_edges.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['u','v','phi_original','phi_raw_removed','phi_center_preserved','estimable_all_three'])
        for i,(u,v) in enumerate(uv):w.writerow([u,v,*[phi[k][i] if np.isfinite(phi[k][i]) else '' for k in codes],bool(common[i])])
    with (out/'feature_frequency.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['feature_id','original_count','raw_removed_count','center_preserved_count','N'])
        for i in range(F):w.writerow([i,*[int(counts[k][i]) for k in codes],N])
    selected=old_heat['feature_ids']
    np.savez(out/'control_data.npz',feature_ids=selected,
             z_original=codes['original'][:256,selected].float().cpu().numpy().T,
             z_raw_removed=codes['raw_removed'][:256,selected].float().cpu().numpy().T,
             z_center_preserved=codes['center_preserved'][:256,selected].float().cpu().numpy().T,
             n_original=counts['original'],n_raw_removed=counts['raw_removed'],n_center_preserved=counts['center_preserved'])
    jaccard={}
    for a,b in [('original','raw_removed'),('original','center_preserved'),('raw_removed','center_preserved')]:
        jaccard[a+'_'+b]=float((binary[a]&binary[b]).sum()/(binary[a]|binary[b]).sum())
    means={k:float(n.sum()/N) for k,n in counts.items()}
    summary={'status':'COMPLETE','posthoc':True,'fixed_v_no_new_SVD':True,'no_training':True,
             'measurement_positions':N,'same_contexts_and_original_raw_encoding_reproduced':True,
             'prior_raw_removed_frequency_exact':True,'prior_selected_heatmap_exact':True,
             'center_preservation_identity_max_abs_error':identity_error,
             'constant_shift_identity_max_abs_error':shift_identity_error,
             'mean_l0':means,'event_jaccard':jaccard,
             'raw_removal_L0_excess':means['raw_removed']-means['original'],
             'center_preserved_L0_excess':means['center_preserved']-means['original'],
             'L0_excess_reduction_fraction':1-(means['center_preserved']-means['original'])/(means['raw_removed']-means['original']),
             'fixed_edges_common_estimable':int(common.sum()),'fixed_edges_total':len(uv),
             'mean_fixed_phi_on_same_common_edges':{k:float(v[common].mean()) for k,v in phi.items()},
             'reconstruction':errors,'elapsed_seconds':time.monotonic()-started,
             'boundary':'separates affine centering shift from centered-direction projection under fixed encoder; does not identify semantic common or learning benefit'}
    for k,v in coder.named_buffers():assert torch.equal(v,buffers[k])
    ex.assert_frozen()
    write_json(out/'summary.json',summary)
    log('centering_control_complete',**summary)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0');p.add_argument('--root',type=Path,default=ROOT)
    a=p.parse_args();run(a.device,a.root)
