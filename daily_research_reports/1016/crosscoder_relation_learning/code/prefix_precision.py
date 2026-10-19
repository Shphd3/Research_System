#!/usr/bin/env python3
"""Separate diagnostic for sequence-shape rounding versus future dependence."""
from data_routes import *


def diagnose(device='cuda:0',out=ROOT):
    import torch
    from crosscoder.bin_data_a15 import BinEvents
    torch.set_num_threads(2)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    model,ex,coder,stats=load_models(device)
    maps=np.load(Path(out)/'route_maps.npz')
    event=BinEvents(DATA,'TRAIN')[4096]
    original=torch.tensor(event['input_ids'][:128],device=device,dtype=torch.long)[None]
    result={'scope':'numeric sequence-shape diagnostic, no learning or routing reselection',
            'original_low_precision_failure_preserved':True,'cases':[]}
    with torch.inference_mode():
        for precision in ['bfloat16','float32']:
            if precision=='float32':
                model.float()
            for t in [7,31,63]:
                changed=original.clone()
                changed[:,t+1:]=(changed[:,t+1:]+12345)%151643
                padded=original.clone()
                padded[:,t+1:]=0
                rr=[]
                for tokens in [original,changed,original[:,:t+1],padded]:
                    valid=torch.zeros_like(tokens,dtype=torch.bool);valid[:,t]=True
                    rr.append(ex.extract(tokens,torch.ones_like(tokens),valid).activations)
                zz=[encode(x,coder,stats) for x in rr]
                routes=[]
                for z in zz:
                    ids=torch.nonzero(z[0]>0,as_tuple=True)[0].cpu().numpy().astype(np.int32)
                    row=[]
                    for c in ['R','F','N']:
                        win,_,_=scores_and_winner(np.array([0,len(ids)]),ids,maps[f'labels_{c}'],maps['sizes'],maps[f'means_{c}'],maps[f'stds_{c}'],maps[f'tie_order_{c}'])
                        row.append(int(apply_routes(win,maps[f'mapping_{c}'],np.array([int(event['position_ids'][t])]))[0]))
                    routes.append(row)
                base=rr[0].double()
                item={'precision':precision,'position':t,
                      'future_change_raw_max':float((rr[0]-rr[1]).abs().max()),
                      'future_zero_pad_raw_max':float((rr[0]-rr[3]).abs().max()),
                      'truncation_raw_max':float((rr[0]-rr[2]).abs().max()),
                      'truncation_per_layer_relative_L2':(torch.linalg.vector_norm(rr[0].double()-rr[2].double(),dim=-1)/torch.linalg.vector_norm(base,dim=-1)).cpu().tolist(),
                      'future_gate_differences':int(((zz[0]>0)!=(zz[1]>0)).sum()),
                      'zero_pad_gate_differences':int(((zz[0]>0)!=(zz[3]>0)).sum()),
                      'truncation_gate_differences':int(((zz[0]>0)!=(zz[2]>0)).sum()),
                      'truncation_z_max_abs':float((zz[0]-zz[2]).abs().max()),
                      'routes_original_future_changed_truncated_zero_padded':routes}
                result['cases'].append(item)
                log('prefix_precision_case',**item)
    result['fixed_shape_future_invariance']=all(x['future_change_raw_max']==0 and x['future_zero_pad_raw_max']==0 and x['future_gate_differences']==0 and x['zero_pad_gate_differences']==0 for x in result['cases'])
    result['all_tested_routes_invariant']=all(x['routes_original_future_changed_truncated_zero_padded'].count(x['routes_original_future_changed_truncated_zero_padded'][0])==4 for x in result['cases'])
    result['boundary']='BF16 variable-length raw and thresholded events may differ through matrix-shape rounding; fixed-shape arbitrary future changes directly test future dependence'
    write_json(Path(out)/'prefix_precision.json',result)
    if not result['fixed_shape_future_invariance'] or not result['all_tested_routes_invariant']:
        raise RuntimeError('future-invariance or operational-route prefix diagnostic failed')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0');p.add_argument('--out',type=Path,default=ROOT)
    a=p.parse_args();diagnose(a.device,a.out)
