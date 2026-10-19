#!/usr/bin/env python3
"""Independent first-direction sensitivity; no model training."""
from data_routes import *

def auxiliary_first_direction(out=ROOT,device='cuda:0'):
    """Independent original-H, uncentered, per-layer first-direction sensitivity."""
    import csv
    import torch
    from crosscoder.bin_data_a15 import BinEvents
    out=Path(out)/'first_direction';out.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    torch.set_num_threads(2)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    _,ex,coder,stats=load_models(device)
    events=BinEvents(DATA,'VAL')
    split=json.loads((PHASE/'split_manifest.json').read_text())
    first=next(b for b in split['blocks'] if b['side']=='D')
    contexts=np.arange(first['context_begin'],first['context_begin']+16)
    ee=[events[int(i)] for i in contexts]
    tokens=torch.tensor([e['input_ids'] for e in ee],device=device,dtype=torch.long)
    valid=torch.tensor([e['valid_mask'] for e in ee],device=device,dtype=torch.bool)
    buffers={k:v.clone() for k,v in coder.named_buffers()}
    with torch.inference_mode():
        result=ex.extract(tokens,torch.ones_like(tokens),valid)
        raw=result.activations
        fit_mask=result.position_indices[:,0]<8
        fit=raw[fit_mask].float()
        measure=raw[~fit_mask].float()
        vectors=[];energies=[];residuals=[];spectra=[]
        for layer in range(14):
            H=fit[:,layer,:]
            gram=H.T@H
            eigenvalues,eigenvectors=torch.linalg.eigh(gram)
            v=eigenvectors[:,-1]
            if v[v.abs().argmax()]<0:v=-v
            vectors.append(v)
            residuals.append(float(torch.linalg.vector_norm(gram@v-eigenvalues[-1]*v)/eigenvalues[-1].abs()))
            spectra.append(eigenvalues[-4:].cpu().numpy())
            energies.append(float(eigenvalues[-1]/eigenvalues.clamp_min(0).sum()))
        V=torch.stack(vectors)
        projected=measure-(measure*V[None]).sum(-1,keepdim=True)*V[None]
        no_op=measure-(measure*V[None]).sum(-1,keepdim=True)*V[None]*0
        z0=encode(measure,coder,stats)
        z_noop=encode(no_op,coder,stats)
        assert torch.equal(z0,z_noop),'zero removal must exactly reproduce same encoding'
        z1=encode(projected,coder,stats)
        assert torch.equal(z0[:1024],coder(stats.normalize(measure[:1024]),use_threshold=True).z)
        errors=[]
        for X in [measure,projected]:
            sse=torch.zeros(14,device=device,dtype=torch.float64)
            for part in X.split(1024):
                rec=coder(stats.normalize(part),use_threshold=True).reconstruction
                rec=stats.inverse(rec)
                sse+=(rec.double()-part.double()).square().sum((0,2))
            errors.append(sse.cpu().numpy())
        actual_removed=(measure-projected).square().sum((0,2))/measure.square().sum((0,2))
    b0=(z0>0).cpu().numpy();b1=(z1>0).cpu().numpy()
    n0=b0.sum(0);n1=b1.sum(0);N=len(b0)
    maps=np.load(Path(out).parent/'route_maps.npz')
    d_order=np.lexsort((np.arange(F),maps['nD']))
    reliable=d_order[maps['nD'][d_order]>=100]
    quarter=len(reliable)//4
    # Selection uses D only, fixed before viewing sensitivity outcomes.
    selected=np.r_[reliable[-16:],reliable[quarter-16:quarter]].astype(np.int32)
    measurement_positions=result.position_indices[~fit_mask].cpu().numpy()
    np.savez(out/'heatmap_data.npz',feature_ids=selected,
             z_original=z0[:256,selected].float().cpu().numpy().T,
             z_removed=z1[:256,selected].float().cpu().numpy().T,
             z_difference=(z1[:256,selected]-z0[:256,selected]).float().cpu().numpy().T,
             context_id=contexts[measurement_positions[:256,0]],
             within_context_position=measurement_positions[:256,1],
             token_ids=tokens[measurement_positions[:256,0],measurement_positions[:256,1]].cpu().numpy())
    np.savez(out/'direction_data.npz',v=V.cpu().numpy(),fit_top4_eigenvalues=np.stack(spectra),
             fit_first_energy_share=np.array(energies),measurement_removed_energy_share=actual_removed.cpu().numpy(),
             original_reconstruction_sse=errors[0],removed_reconstruction_sse=errors[1],
             n_original=n0,n_removed=n1,measurement_contexts=contexts[8:])
    with (out/'feature_frequency.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['feature_id','D_count','measurement_N','original_count','removed_count','original_frequency','removed_frequency','frequency_delta'])
        for i in range(F):w.writerow([i,int(maps['nD'][i]),N,int(n0[i]),int(n1[i]),n0[i]/N,n1[i]/N,(int(n1[i])-int(n0[i]))/N])
    with (OLD/'main/edges_D.csv').open() as f:edges=list(csv.DictReader(f))
    uv=np.array([(int(e['u']),int(e['v'])) for e in edges],np.int32)
    def phi_on_edges(B,n):
        joint=np.concatenate([(B[:,u]&B[:,v]).sum(0) for u,v in [(x[:,0],x[:,1]) for x in np.array_split(uv,max(1,len(uv)//128))]])
        den=np.sqrt(n[uv[:,0]].astype(float)*(N-n[uv[:,0]])*n[uv[:,1]]*(N-n[uv[:,1]]))
        return np.divide(N*joint-n[uv[:,0]]*n[uv[:,1]],den,out=np.full(len(uv),np.nan),where=den>0)
    phi0=phi_on_edges(b0,n0);phi1=phi_on_edges(b1,n1)
    with (out/'fixed_edges.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['u','v','phi_original','phi_removed','phi_delta'])
        for (u,v),p0,p1 in zip(uv,phi0,phi1):w.writerow([u,v,p0 if np.isfinite(p0) else '',p1 if np.isfinite(p1) else '',p1-p0 if np.isfinite(p0+p1) else ''])
    original_groups=json.loads((OLD/'main/groups_D.json').read_text())
    with (out/'fixed_groups.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['group_id','size','original_dispersion_dex','removed_dispersion_dex','original_mean_activation_density','removed_mean_activation_density'])
        for g in original_groups:
            if g['size']<2:continue
            members=np.array(g['members'])
            disp=[]
            for n in [n0,n1]:
                disp.append(float(np.std(np.log10(n[members]/N))) if np.all(n[members]>0) else '')
            w.writerow([g['group_id'],g['size'],*disp,float(n0[members].sum()/(N*len(members))),float(n1[members].sum()/(N*len(members)))])
    for k,v in coder.named_buffers():assert torch.equal(v,buffers[k])
    ex.assert_frozen()
    finite=np.isfinite(phi0)&np.isfinite(phi1)
    summary={'status':'COMPLETE','source':'first16source-ordered contexts in first discovery block; first8fit, following8measure',
             'context_ids':contexts.tolist(),'fit_positions':len(fit),'measurement_positions':N,
             'fit_matrix':'original raw H_l [N,1024], no mean subtraction; independent first right singular vector each layer',
             'normalization':'original frozen TRAIN CenteredRMSStats after removal; fixed saved threshold',
             'zero_removal_exact_reproduction':True,'encoder_only_equals_original_forward':True,
             'first_direction_eigen_residual':residuals,'fit_energy_share':energies,
             'measurement_removed_energy_share':actual_removed.cpu().tolist(),
             'original_mean_l0':float(n0.sum()/N),'removed_mean_l0':float(n1.sum()/N),
             'binary_event_jaccard':float((b0&b1).sum()/(b0|b1).sum()),
             'fixed_edges_estimable_both':int(finite.sum()),'fixed_edges_total':len(uv),
             'fixed_edge_mean_phi_original':float(phi0[finite].mean()),'fixed_edge_mean_phi_removed':float(phi1[finite].mean()),
             'seconds':time.monotonic()-started,'no_training':True,
             'boundary':'first-direction sensitivity; no semantic common identification and no random-direction control'}
    write_json(out/'summary.json',summary)
    log('auxiliary_complete',**summary)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=ROOT)
    p.add_argument("--device",default="cuda:0")
    a=p.parse_args()
    auxiliary_first_direction(a.out,a.device)
