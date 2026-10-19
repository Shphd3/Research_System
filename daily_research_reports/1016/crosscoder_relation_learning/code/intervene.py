"""Resettable one-step, zero-momentum/zero-decay SGD route intervention.

Donor route labels are exchanged only within fixed input-frequency bins. Each
bin AND the whole donor batch preserve expert token counts. Probe routing is
never modified. The intervention is never connected back to formal training.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
import train_adapters as trainer
from train_adapters import (ResidualExperts, FrozenHead, write_json, sha, tensor_hash,
                            gradients, tree_cpu, order_indices, validate_cache)


def row_frequency(data):
    p = data['discovery_frequency'].double().clamp_min(1e-12)
    ptr=data['feature_ptr'].long(); ids=data['feature_ids'].long()
    row=torch.repeat_interleave(torch.arange(len(ptr)-1),ptr[1:]-ptr[:-1])
    sums=torch.zeros(len(ptr)-1,dtype=torch.float64).scatter_add_(0,row,p[ids].log10())
    return sums/(ptr[1:]-ptr[:-1]).clamp_min(1)


def frequency_bins(data, cuts):
    return torch.bucketize(row_frequency(data),torch.tensor(cuts,dtype=torch.float64))


def permute_routes(route,bins,seed):
    gen=torch.Generator().manual_seed(seed)
    out=route.clone()
    for b in bins.unique():
        idx=torch.nonzero(bins==b,as_tuple=False).flatten()
        out[idx]=route[idx[torch.randperm(len(idx),generator=gen)]]
    if not torch.equal(torch.bincount(route,minlength=4),torch.bincount(out,minlength=4)):
        raise ValueError('Expert donor counts changed')
    for b in bins.unique():
        if not torch.equal(torch.bincount(route[bins==b],minlength=4),torch.bincount(out[bins==b],minlength=4)):
            raise ValueError('Within frequency-bin expert counts changed')
    return out


def low_probe_support(data,ids,min_eval_support):
    # Fix globally supported low features before any condition outcome is read.
    allids=data['feature_ids'].long()
    counts=torch.bincount(allids,minlength=16384)
    low=data['low_ids'].long();low=low[counts[low]>=min_eval_support]
    mask=torch.zeros(16384,dtype=torch.bool);mask[low]=True
    ptr=data['feature_ptr'].long()
    rows=[];features=[]
    for j,i in enumerate(ids.tolist()):
        f=allids[ptr[i]:ptr[i+1]];f=f[mask[f]]
        rows.append(torch.full((len(f),),j,dtype=torch.long));features.append(f)
    if not features: return torch.empty(0,dtype=torch.long),torch.empty(0,dtype=torch.long),low
    return torch.cat(rows),torch.cat(features),low


def probe_mean(losses,row,feature):
    if not len(feature): return None,0
    sums=torch.zeros(16384,dtype=torch.float64).scatter_add_(0,feature,losses.double()[row])
    counts=torch.bincount(feature,minlength=16384)
    present=counts>0
    return float((sums[present]/counts[present]).mean()),int(present.sum())


def parameter_gradients(model):
    return {k: p.grad.detach().clone() for k,p in model.named_parameters()}


def expert_norms(g):
    return torch.sqrt(sum(x.double().flatten(1).square().sum(-1) for x in g.values()))


@torch.no_grad()
def apply_step(model,state,g,lr):
    model.load_state_dict(state)
    for k,p in model.named_parameters(): p.add_(g[k],alpha=-lr)


@torch.no_grad()
def probe(model,head,data,indices,route,device,batch=256):
    result=[]
    for start in range(0,len(indices),batch):
        ids=indices[start:start+batch]
        h=data['hidden'][ids].to(device);y=data['target'][ids].to(device)
        r=route[start:start+batch].to(device)
        loss=F.cross_entropy(head(model(h,r)).float(),y,reduction='none')
        if not torch.isfinite(loss).all(): raise FloatingPointError('Nonfinite virtual-step probe')
        result.append(loss.cpu())
    return torch.cat(result)


def run(args):
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False
    torch.use_deterministic_algorithms(True)
    cfg=json.loads(Path(args.config).read_text());device=torch.device(args.device)
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    if (out/'completion.json').exists():raise ValueError('Refusing overwrite completed intervention')
    data=torch.load(cfg['train_cache'],map_location='cpu',weights_only=False)
    ev=torch.load(cfg['eval_cache'],map_location='cpu',weights_only=False)
    validate_cache(data);validate_cache(ev)
    checkpoint=torch.load(args.checkpoint,map_location='cpu',weights_only=False)
    if checkpoint['config_sha256']!=sha(args.config) or checkpoint['arm']!=args.arm or checkpoint['seed']!=args.seed:
        raise ValueError('Checkpoint contract mismatch')
    if checkpoint['source_sha256']!=sha(trainer.__file__):raise ValueError('Training source changed after checkpoint')
    if checkpoint['step']!=cfg['midpoint']:raise ValueError('Intervention requires frozen midpoint')
    model=ResidualExperts(seed=args.seed).to(device);model.load_state_dict(checkpoint['adapters'])
    state=tree_cpu(model.state_dict());head=FrozenHead.load(cfg['model_dir'],device)
    head_version={k:v._version for k,v in head.named_buffers()}
    dcfg=cfg['intervention'];batch=dcfg['donor_batch'];n=dcfg['batches'];lr=dcfg['lr']
    bins=frequency_bins(data,dcfg['frequency_cuts'])
    order=order_indices(len(data['target']),cfg['updates'],cfg['batch_size'],args.seed)
    if batch!=cfg['batch_size']:raise ValueError('Donor uses same fixed main training batch size')
    # Same evaluation probe positions across conditions and seeds. Stratification
    # uses only low-feature presence; neither target nor loss influences sampling.
    ptr=ev['feature_ptr'].long();fid=ev['feature_ids'].long()
    low=ev['low_ids'].long();counts=torch.bincount(fid,minlength=16384);low=low[counts[low]>=cfg['min_eval_support']]
    low_mask=torch.zeros(16384,dtype=torch.bool);low_mask[low]=True
    row=torch.repeat_interleave(torch.arange(len(ev['target'])),ptr[1:]-ptr[:-1])
    hits=torch.zeros(len(ev['target']),dtype=torch.long).scatter_add_(0,row,low_mask[fid].long())
    pool=torch.nonzero(hits>0,as_tuple=False).flatten()
    gen=torch.Generator().manual_seed(dcfg['probe_seed'])
    if len(pool)<dcfg['probe_batch']:raise ValueError('Insufficient low-feature probe positions')
    pool=pool[torch.randperm(len(pool),generator=gen)]
    selected=torch.cat([pool for _ in range(math.ceil(n*dcfg['probe_batch']/len(pool)))])[:n*dcfg['probe_batch']]
    records=[];norm_records=[];index_records=[]
    for j in range(n):
        # Donors are batches immediately after the frozen checkpoint; we reset
        # parameters on every batch, and never load Adam state for virtual SGD.
        did=order[(cfg['midpoint']+j)%len(order)]
        pid=selected[j*dcfg['probe_batch']:(j+1)*dcfg['probe_batch']]
        actual=data['routes'][args.arm][did].long()
        exchanged=permute_routes(actual,bins[did],dcfg['exchange_seed']+j)
        fraction=float((actual!=exchanged).float().mean())
        probe_route=ev['routes'][args.arm][pid].long()
        prow,pfeat,global_low=low_probe_support(ev,pid,cfg['min_eval_support'])
        model.load_state_dict(state)
        before=probe(model,head,ev,pid,probe_route,device,cfg['eval_batch_size'])
        pre_low,supported=probe_mean(before,prow,pfeat)
        if pre_low is None: raise ValueError('No low-feature support in fixed probe')
        h=data['hidden'][did].to(device);y=data['target'][did].to(device)
        model.load_state_dict(state);actual_loss,_,_=gradients(model,head,h,actual.to(device),y)
        ga=parameter_gradients(model);na=expert_norms(ga)
        model.load_state_dict(state);permuted_loss,_,_=gradients(model,head,h,exchanged.to(device),y)
        gp=parameter_gradients(model);np_=expert_norms(gp)
        valid_experts=(na>dcfg['norm_floor'])&(np_>dcfg['norm_floor'])
        all_match=bool(valid_experts.all())
        # Any zero expert is explicitly unmatched rather than dividing by zero.
        scale=torch.where(valid_experts,na/np_.clamp_min(dcfg['norm_floor']),torch.ones_like(na))
        matched={k:g*scale.to(g).view(-1,*([1]*(g.ndim-1))) for k,g in gp.items()}
        matched_norm=expert_norms(matched)
        relative_norm_error=float(((matched_norm-na).abs()/na.clamp_min(dcfg['norm_floor']))[valid_experts].max()) if valid_experts.any() else None
        if relative_norm_error is not None and relative_norm_error>1e-5:raise ValueError('Expert norm matching inaccurate')
        for version in ('raw','expert_norm_matched'):
            eligible=fraction>=dcfg['min_exchange_fraction'] and (all_match or version=='raw')
            for route_label,g in [('actual',ga),('exchanged',gp if version=='raw' else matched)]:
                apply_step(model,state,g,lr)
                after=probe(model,head,ev,pid,probe_route,device,cfg['eval_batch_size'])
                post_low,_=probe_mean(after,prow,pfeat)
                norm=expert_norms(g)*lr
                if not torch.isfinite(norm).all() or not all(torch.isfinite(p).all() for p in model.parameters()):
                    raise FloatingPointError('Invalid virtual parameter step')
                records.append({'arm':args.arm,'seed':args.seed,'batch':j,'version':version,'donor_route':route_label,
                    'lr':lr,'pre_low_loss':pre_low,'post_low_loss':post_low,'low_loss_decrease':pre_low-post_low,
                    'pre_position_loss':float(before.mean()),'post_position_loss':float(after.mean()),
                    'position_loss_decrease':float((before-after).mean()),'probe_tokens':len(pid),
                    'probe_low_features':supported,'global_supported_low_features':len(global_low),
                    'donor_tokens':len(did),'route_exchange_fraction':fraction,'eligible':eligible,
                    'matched_max_relative_norm_error':relative_norm_error,
                    'unmatched_experts':int((~valid_experts).sum()),'total_update_norm':float(norm.square().sum().sqrt())})
                for e in range(4):norm_records.append({'arm':args.arm,'seed':args.seed,'batch':j,'version':version,
                     'donor_route':route_label,'expert':e,'tokens':int((actual==e).sum()),'update_norm':float(norm[e]),
                     'actual_grad_norm':float(na[e]),'exchanged_grad_norm':float(np_[e]),'match_eligible':bool(valid_experts[e])})
        index_records.append({'batch':j,'donor_position_ids':data['position_id'][did].tolist(),
              'probe_position_ids':ev['position_id'][pid].tolist(),'actual_route':actual.tolist(),
              'exchanged_route':exchanged.tolist(),'donor_frequency_bins':bins[did].tolist()})
        print(json.dumps({'stage':'virtual_sgd','arm':args.arm,'seed':args.seed,'batch':j,
                         'exchange_fraction':fraction,'supported_probe_features':supported}),flush=True)
    model.load_state_dict(state)
    if tensor_hash(model.state_dict())!=tensor_hash(state):raise ValueError('Virtual update leaked into final parameter state')
    if any(x._version!=head_version[k] for k,x in head.named_buffers()):raise ValueError('Frozen head changed')
    for name,rows in [('effects.csv',records),('expert_norms.csv',norm_records)]:
        with (out/name).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_json(out/'fixed_indices.json',index_records)
    write_json(out/'completion.json',{'execution_status':'COMPLETE','arm':args.arm,'seed':args.seed,
        'checkpoint_sha256':sha(args.checkpoint),'config_sha256':sha(args.config),'source_sha256':sha(__file__),
        'virtual_optimizer':'SGD momentum=0 weight_decay=0','batches':n,'lr':lr,
        'frequency_cutpoints':dcfg['frequency_cuts'],'probe_route':'always original unchanged',
        'parameter_reset_each_donor':True,'formal_training_unchanged':True,
        'eligible_raw_batches':sum(r['eligible'] for r in records if r['version']=='raw' and r['donor_route']=='actual'),
        'eligible_matched_batches':sum(r['eligible'] for r in records if r['version']=='expert_norm_matched' and r['donor_route']=='actual')})


def selftest():
    route=torch.tensor([0,0,1,2,3,1,2,3,0,1,2,3]);bins=torch.arange(12)%3
    other=permute_routes(route,bins,42)
    assert torch.equal(torch.bincount(route,minlength=4),torch.bincount(other,minlength=4))
    ga={'down':torch.randn(4,3,7),'up':torch.randn(4,7,3)}
    gp={k:torch.randn_like(g) for k,g in ga.items()}
    scales=expert_norms(ga)/expert_norms(gp)
    gm={k:g*scales.to(g).view(4,1,1) for k,g in gp.items()}
    assert torch.allclose(expert_norms(ga),expert_norms(gm),atol=1e-6)
    a,n=probe_mean(torch.tensor([1.,3.,5.]),torch.tensor([0,1,2,2]),torch.tensor([0,0,1,2]))
    assert a==4.0 and n==3
    print(json.dumps({'status':'PASS','within_bin_exact_expert_counts':True,'per_expert_update_norm_matching':True,
                     'probe_feature_mean_handcheck':True}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config');p.add_argument('--checkpoint');p.add_argument('--output')
    p.add_argument('--arm',choices=['R','F','N']);p.add_argument('--seed',type=int,default=42)
    p.add_argument('--device',default='cuda:0');p.add_argument('--selftest',action='store_true');a=p.parse_args()
    if a.selftest:selftest()
    else:run(a)
