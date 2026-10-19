"""Post-observation frozen-response intervention; no training or route changes.

For each expert e, TRAIN-only mu_e gives the algebraic split
U_e D_e h = U_e D_e mu_e + U_e D_e (h - mu_e).
The ORIGINAL complete h still traverses the base residual in every condition.
The split concerns a learned adapter response, not a semantic common feature.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from train_adapters import ResidualExperts,FrozenHead,atomic_save,write_json,sha,tensor_hash


class ResponseExperts(ResidualExperts):
    def set_component(self,component,means):
        self.component=component;self.means=means.to(self.down)
    def forward(self,hidden,route):
        if self.component=='full':return super().forward(hidden,route)
        h=hidden.float();out=torch.zeros_like(h)
        if self.component=='zero':return h+out
        for e in range(4):
            idx=torch.nonzero(route==e,as_tuple=False).flatten()
            if not idx.numel():continue
            if self.component=='constant_only':
                value=F.linear(F.linear(self.means[e],self.down[e]),self.up[e])
                out[idx]=value.expand(len(idx),-1)
            elif self.component=='centered_only':
                out[idx]=F.linear(F.linear(h[idx]-self.means[e],self.down[e]),self.up[e])
            else:raise ValueError('Unknown response component')
        return h+out


def position_weights(data,label,minimum):
    """Exact fixed-feature equal mean as a fixed linear weight on token losses."""
    ptr=data['feature_ptr'].numpy();fid=data['feature_ids'].numpy()
    counts=np.bincount(fid,minlength=16384)
    selected=data[label+'_ids'].numpy();selected=selected[counts[selected]>=minimum]
    if not len(selected):raise ValueError('No eligible fixed '+label+' features')
    lookup=np.zeros(16384,dtype=np.float64);lookup[selected]=1/(len(selected)*counts[selected])
    weight=np.zeros(len(ptr)-1,dtype=np.float64)
    for start in range(0,len(weight),32768):
        end=min(start+32768,len(weight));ids=fid[ptr[start]:ptr[end]]
        rows=np.repeat(np.arange(end-start),np.diff(ptr[start:end+1]))
        weight[start:end]=np.bincount(rows,weights=lookup[ids],minlength=end-start)
    if not np.isclose(weight.sum(),1,atol=1e-12):raise ValueError('Conditional feature weight normalization')
    return torch.from_numpy(weight),torch.from_numpy(selected.copy()).long()


def prepare(args):
    torch.set_num_threads(4)
    root=Path(args.root);out=root/'response_decomposition';out.mkdir(parents=True,exist_ok=True)
    if (out/'precomputed.pt').exists():raise ValueError('Preserve existing prepared response intervention')
    cfg=json.loads(Path(args.config).read_text())
    prediction={'registered_at_utc':datetime.now(timezone.utc).isoformat(),
       'role':'post-observation intervention prompted by completed R damage; not a new training comparison or original confirmation',
       'fixed_scope':{'arms':['R','F','N'],'seeds':cfg['paired_seeds'],'checkpoint':'final frozen adapter',
                      'input':'complete original final-block residual','routes':'original unchanged',
                      'mu':'expert-specific mean original TRAIN hidden, no target/loss/EVAL fitting',
                      'eval':'same complete EVAL and fixed supported low/high cohorts as C'},
       'operation':'delta_full(h)=U D h; delta_constant=U D mu; delta_centered(h)=U D(h-mu)',
       'four_states':['zero','full','constant_only','centered_only'],
       'predictions':{
          'constant_response_dominates':'constant-only reproduces most full damage; removing it (centered-only) restores performance toward zero; small residual loss interaction',
          'input_dependent_response_dominates':'centered-only reproduces most full damage; constant-only stays near zero; small residual loss interaction',
          'nonlinear_interaction_dominates':'neither component alone reproduces full damage; Lfull-Lconstant-Lcentered+Lzero is large; or components cancel strongly',
          'mixed_or_unidentified':'components and interaction are comparable or seed/metric patterns conflict; no single-cause conclusion'},
       'registered_primary_readout':'overall loss damage relative to zero; fixed low-feature conditional result is also reported',
       'interaction':'Lfull-Lconstant-Lcentered+Lzero, separately for overall/low/high loss',
       'guards':['original zero/full per-position loss arrays reproduced exactly','linear response decomposition residual measured',
                 'same target, route, head, normalization, eval membership and loss reduction in all four states'],
       'boundary':'identifies functional response components at this frozen checkpoint; no common semantics, no optimizer history or full training root-cause proof'}
    write_json(out/'prediction.json',prediction)
    train=torch.load(cfg['train_cache'],map_location='cpu',weights_only=False)
    means={};loads={}
    for arm in ['R','F','N']:
        route=train['routes'][arm].long();counts=torch.bincount(route,minlength=4)
        if (counts==0).any():raise ValueError('Missing TRAIN expert')
        sums=torch.zeros(4,1024,dtype=torch.float64)
        for start in range(0,len(route),8192):
            end=min(start+8192,len(route))
            sums.index_add_(0,route[start:end],train['hidden'][start:end].double())
        means[arm]=(sums/counts[:,None]).float();loads[arm]=counts.tolist()
    del train
    ev=torch.load(cfg['eval_cache'],map_location='cpu',weights_only=False)
    weights={};eligible={}
    for label in ['low','high']:weights[label],eligible[label]=position_weights(ev,label,cfg['min_eval_support'])
    prepared={'config_sha256':sha(args.config),'source_sha256':sha(__file__),'means':means,'weights':weights,
              'eligible_features':eligible,'eval_positions':len(ev['target']),'TRAIN_expert_counts':loads,
              'eval_blocks':ev['block_id'],'eval_position_ids':ev['position_id'],'min_eval_support':cfg['min_eval_support']}
    atomic_save(out/'precomputed.pt',prepared)
    write_json(out/'preparation.json',{'status':'COMPLETE','config_sha256':sha(args.config),'source_sha256':sha(__file__),
           'eval_positions':len(ev['target']),'eligible_low_features':len(eligible['low']),'eligible_high_features':len(eligible['high']),
           'conditional_position_weights_sum':{k:float(v.sum()) for k,v in weights.items()},'TRAIN_expert_counts':loads,
           'mu_fitted_without_EVAL_or_targets':True,'precomputed_sha256':sha(out/'precomputed.pt')})
    print(json.dumps({'stage':'response_prepare','status':'COMPLETE','positions':len(ev['target'])}),flush=True)


@torch.no_grad()
def response_error(model,data,arm,means,device,batch):
    # Source-ordered fixed first 4096 EVAL positions; no outcome-based selection.
    maximum=0.;squared_error=0.;squared_response=0.
    for start in range(0,min(4096,len(data['target'])),batch):
        end=min(start+batch,min(4096,len(data['target'])))
        h=data['hidden'][start:end].to(device).float();route=data['routes'][arm][start:end].to(device)
        for e in range(4):
            selected=h[route==e]
            if not len(selected):continue
            full=F.linear(F.linear(selected,model.down[e]),model.up[e])
            const=F.linear(F.linear(means[e],model.down[e]),model.up[e])
            center=F.linear(F.linear(selected-means[e],model.down[e]),model.up[e])
            err=full-const-center
            maximum=max(maximum,float(err.abs().max()))
            squared_error+=float(err.double().square().sum());squared_response+=float(full.double().square().sum())
    relative=math.sqrt(squared_error/max(squared_response,1e-30))
    if relative>1e-5:raise ValueError('Linear response reconstruction error too large')
    return {'sample_positions':min(4096,len(data['target'])),'max_abs_response_error':maximum,
            'relative_response_L2_error':relative,'check':'U D h versus U D mu + U D(h-mu), before final norm/head',
            'loss_additivity_not_assumed':True}


@torch.no_grad()
def worker(args):
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.use_deterministic_algorithms(True)
    root=Path(args.root);shared=root/'response_decomposition';out=shared/f'seed_{args.seed}'/args.arm
    out.mkdir(parents=True,exist_ok=True)
    if (out/'completion.json').exists():raise ValueError('Preserve completed response intervention')
    started=time.monotonic();cfg=json.loads(Path(args.config).read_text());device=torch.device(args.device)
    if 'H100' not in torch.cuda.get_device_name(device):raise ValueError('Reserved H100 required')
    prepared=torch.load(shared/'precomputed.pt',map_location='cpu',weights_only=False)
    if prepared['config_sha256']!=sha(args.config) or prepared['source_sha256']!=sha(__file__):raise ValueError('Prepared intervention contract drift')
    case=root/'learning'/f'seed_{args.seed}'/args.arm
    checkpoint=case/'checkpoints'/f"update_{cfg['updates']:05d}.pt"
    state=torch.load(checkpoint,map_location='cpu',weights_only=False)
    if state['config_sha256']!=sha(args.config) or state['step']!=cfg['updates'] or state['arm']!=args.arm or state['seed']!=args.seed:
        raise ValueError('Wrong final checkpoint')
    model=ResponseExperts(seed=args.seed).to(device);model.load_state_dict(state['adapters'])
    initial_hash=tensor_hash(model.state_dict());head=FrozenHead.load(cfg['model_dir'],device)
    versions={k:x._version for k,x in head.named_buffers()}
    data=torch.load(cfg['eval_cache'],map_location='cpu',weights_only=False)
    if len(data['target'])!=prepared['eval_positions']:raise ValueError('EVAL size changed')
    means=prepared['means'][args.arm].to(device)
    error=response_error(model,data,args.arm,means,device,cfg['eval_batch_size'])
    records=[];loss_arrays={};guards={}
    for component in ['zero','full','constant_only','centered_only']:
        model.set_component(component,means);losses=np.empty(len(data['target']),dtype=np.float32)
        for start in range(0,len(losses),cfg['eval_batch_size']):
            end=min(start+cfg['eval_batch_size'],len(losses))
            h=data['hidden'][start:end].to(device);r=data['routes'][args.arm][start:end].to(device)
            y=data['target'][start:end].to(device)
            ell=F.cross_entropy(head(model(h,r)).float(),y,reduction='none')
            if not torch.isfinite(ell).all():raise FloatingPointError('Nonfinite response intervention loss')
            losses[start:end]=ell.cpu().numpy()
        if component in ['zero','full']:
            ref=np.load(case/f"eval_losses_{0 if component=='zero' else cfg['updates']:05d}.npy")
            exact=np.array_equal(losses,ref);max_error=float(np.abs(losses.astype(float)-ref).max())
            guards[component]={'per_position_loss_exact':exact,'max_absolute_loss_error':max_error}
            if not exact:raise ValueError('Original '+component+' loss arrays not reproduced exactly')
        np.save(out/f'{component}_losses.npy',losses);loss_arrays[component]=losses.astype(np.float64)
        values={'overall':float(losses.astype(np.float64).mean())}
        values.update({k:float(np.dot(v.numpy(),losses.astype(np.float64))) for k,v in prepared['weights'].items()})
        for metric,value in values.items():records.append({'arm':args.arm,'seed':args.seed,'state':component,
                 'metric':metric,'loss_nat':value,'eval_positions':len(losses),
                 'eligible_features':len(prepared['eligible_features'][metric]) if metric!='overall' else ''})
        print(json.dumps({'stage':'response_decomposition','arm':args.arm,'seed':args.seed,'state':component,'loss':values}),flush=True)
    effects=[]
    for metric in ['overall','low','high']:
        v={r['state']:r['loss_nat'] for r in records if r['metric']==metric}
        effects.append({'arm':args.arm,'seed':args.seed,'metric':metric,'zero_loss':v['zero'],'full_loss':v['full'],
             'constant_only_loss':v['constant_only'],'centered_only_loss':v['centered_only'],
             'full_damage_nat':v['full']-v['zero'],'constant_only_damage_nat':v['constant_only']-v['zero'],
             'centered_only_damage_nat':v['centered_only']-v['zero'],
             'loss_interaction_nat':v['full']-v['constant_only']-v['centered_only']+v['zero']})
    for name,rows in [('losses.csv',records),('effects.csv',effects)]:
        with (out/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    if tensor_hash(model.state_dict())!=initial_hash:raise ValueError('Frozen adapter changed')
    if any(x._version!=versions[k] for k,x in head.named_buffers()):raise ValueError('Frozen head changed')
    write_json(out/'completion.json',{'status':'COMPLETE','arm':args.arm,'seed':args.seed,'config_sha256':sha(args.config),
        'source_sha256':sha(__file__),'checkpoint_sha256':sha(checkpoint),'prepared_sha256':sha(shared/'precomputed.pt'),
        'zero_full_guards':guards,'linear_response_decomposition':error,'no_training':True,'original_routes_fixed':True,
        'complete_input_preserved':True,'means_from_TRAIN_only':True,'elapsed_seconds':time.monotonic()-started,
        'boundary':'functional adapter-response components at this checkpoint, not semantic common or complete training cause'})


def selftest():
    torch.manual_seed(2);h=torch.randn(19,12);r=torch.arange(19)%4
    mu=torch.stack([h[r==e].double().mean(0).float() for e in range(4)])
    m=ResponseExperts(d=12,rank=3,k=4);m.up.data.normal_()
    outs={}
    for state in ['zero','full','constant_only','centered_only']:
        m.set_component(state,mu);outs[state]=m(h,r)
    assert torch.equal(outs['zero'],h)
    assert torch.allclose(outs['full']-h,outs['constant_only']+outs['centered_only']-2*h,atol=2e-6)
    toy={'feature_ptr':torch.tensor([0,2,3,5]),'feature_ids':torch.tensor([0,1,0,1,2],dtype=torch.int32),'low_ids':torch.tensor([0,1])}
    w,sel=position_weights(toy,'low',1)
    assert np.isclose(np.dot(w.numpy(),[1.,3.,5.]),2.5)
    print(json.dumps({'status':'PASS','linear_response_decomposition':True,'complete_base_input_preserved':True,
                     'fixed_feature_equal_mean_position_weights':True}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root');p.add_argument('--config');p.add_argument('--arm',choices=['R','F','N'])
    p.add_argument('--seed',type=int,default=20261016);p.add_argument('--device',default='cuda:0')
    p.add_argument('--prepare',action='store_true');p.add_argument('--selftest',action='store_true');a=p.parse_args()
    if a.selftest:selftest()
    elif a.prepare:prepare(a)
    else:worker(a)
