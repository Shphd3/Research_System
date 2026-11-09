"""R06: frozen paired continuation; native final block, actual Adam displacement."""
import argparse,datetime,hashlib,importlib.util,json,math,os,random,subprocess,sys,time,traceback
from pathlib import Path
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r05',ROOT/'source/retention_r05_v1.py')
r05=importlib.util.module_from_spec(spec);spec.loader.exec_module(r05)
NAMES=r05.NAMES
CFG=json.loads((ROOT/'config/frozen.json').read_text())
DEVICE='cuda:0'

def write(p,x):r05.write(p,x)
def append(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:f.write(json.dumps(x,ensure_ascii=False,allow_nan=False)+'\n');f.flush()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def squares(xs):return sum(x.detach().double().square().sum() for x in xs)
def dot(xs,ys):return sum((x.detach().double()*y.detach().double()).sum() for x,y in zip(xs,ys))
def length(xs):return float(squares(xs).sqrt())

def filter_step(d,g,method,projs,t):
    z=dot(g,g);q=dot(g,d);floor=float(z)<=CFG['gradient_norm_squared_floor']
    active=float(q)>0 and not floor
    f=[x-y*(q/z).to(x) for x,y in zip(d,g)] if active else [x.clone() for x in d]
    dn=length(d);fn=length(f)
    if method=='U':actual=d
    elif method=='F':actual=f
    elif method=='D':actual=[x*(fn/dn) for x in d] if dn else [torch.zeros_like(x) for x in d]
    elif method=='S':
        a=r05.attenuation(CFG,t)
        actual=[x+(a-1)*p(x) for x,p in zip(d,projs)]
    else:raise ValueError(method)
    return actual,{'probe_g2':float(z),'g_dot_candidate':float(q),'projection_needed':active,'gradient_floor':floor,
                  'zero_candidate':dn==0,'candidate_norm':dn,'functional_norm':fn,'desired_norm':length(actual),'g_dot_desired':float(dot(g,actual)),
                  'S_attenuation':r05.attenuation(CFG,t) if method=='S' else 1.}

def numeric_tests():
    g=[torch.tensor([1.,0.,0.])];d=[torch.tensor([1.,2.,0.])]
    f,m=filter_step(d,g,'F',[],0);v,_=filter_step(d,g,'D',[],0)
    assert abs(float(dot(g,f)))<1e-10 and abs(length(v)-length(f))<1e-6
    assert torch.allclose(v[0],d[0]*(length(f)/length(d)))
    for gg,dd in [([torch.zeros(3)],d),(g,[-d[0]]),(g,[torch.zeros(3)])]:
        f,_=filter_step(dd,gg,'F',[],0);assert torch.equal(f[0],dd[0])
    u=torch.eye(3)[:,:2];p=r05.Projector(u,u)
    x=torch.tensor([[1.,2.,0.],[0.,3.,4.],[0.,0.,5.]])
    assert torch.equal(p(x),torch.diag(torch.tensor([1.,3.,0.])))
    xx=torch.tensor([1.,2.],requires_grad=True);o=torch.optim.AdamW([xx],lr=1e-4,weight_decay=0,foreach=False,fused=False)
    xx.grad=torch.tensor([3.,4.]);o.step();before=r05.cpu_tree(o.state_dict())
    with torch.no_grad():xx.add_(.001)
    assert r05.exact_tree(before,o.state_dict())
    return {'status':'PASS','F_harmful_dot':float(dot(g,filter_step(d,g,'F',[],0)[0])),
            'D_matches_F_norm':True,'D_direction_preserved':True,'zero_and_beneficial_unchanged':True,'rank_one_atom_not_full_subspace':True,'moments_unchanged_by_parameter_filter':True}

def build_orders(records):
    groups={1:{},2:{}}
    for i,r in enumerate(records):groups[r['mode']].setdefault(r['list_id'],{})[r['command']]=i
    assert set(groups[1])==set(groups[2])
    keys=sorted(groups[1]);assert len(keys)==1200
    def stream(seed,count):
        rg=random.Random(seed);out=[]
        while len(out)<count:
            ep=list(keys);rg.shuffle(ep);out.extend(ep)
        return out[:count]
    all_orders={}
    for seed in CFG['seeds']:
        nk=stream(seed,240*18);ok=stream(seed+100000,240*18);pk=stream(seed+200000,240*32)
        maskrng=random.Random(seed+300000);slot_order=list(range(18));steps=[]
        for t in range(240):
            if t%9==0:maskrng.shuffle(slot_order)
            activepairs=set(slot_order[2*(t%9):2*(t%9)+2])
            new=[groups[2][k][c] for k in nk[t*18:(t+1)*18] for c in ('甲','乙')]
            old=[groups[1][k][c] for k in ok[t*18:(t+1)*18] for c in ('甲','乙')]
            probes=[groups[1][k][c] for k in pk[t*32:(t+1)*32] for c in ('甲','乙')]
            mask=[int(j//2 in activepairs) for j in range(36)]
            assert len(new)==36 and len(old)==36 and len(probes)==64 and sum(mask)==4
            steps.append({'new':new,'old':old,'probe':probes,'mask4':mask})
        all_orders[str(seed)]=steps
    write(ROOT/'provenance/orders.json',{'seeds':all_orders,'record_ids':[r['record_id'] for r in records],
            'sampling':'independent shuffled full-list streams, paired commands; active old4 slots rotated through18 pair positions every9steps'})
    return all_orders

def fingerprint(p):
    p=Path(p);s=p.stat();return {'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'sha256':r05.sha(p)}

def verify_inputs_once():
    receipts={}
    for name,want in CFG['data_file_sha256'].items():
        p=Path(CFG['data'])/name;receipts[str(p)]=fingerprint(p);assert receipts[str(p)]['sha256']==want
    p=Path(CFG['data'])/'manifest.json';receipts[str(p)]=fingerprint(p);assert receipts[str(p)]['sha256']==CFG['data_manifest_sha256']
    p=Path(CFG['old_checkpoint_path']);receipts[str(p)]=fingerprint(p);assert receipts[str(p)]['sha256']==CFG['old_checkpoint_sha256']
    trainrows=[json.loads(s) for s in (Path(CFG['data'])/'train.jsonl').read_text().splitlines()]
    devrows=[json.loads(s) for s in (Path(CFG['data'])/'dev.jsonl').read_text().splitlines()]
    rows={'train':[r for r in trainrows if r['world'] in ('old','reversed')],
          'dev':[r for r in devrows if r['world'] in ('old','reversed')]}
    assert len(rows['train'])==4800 and len(rows['dev'])==1600
    assert not set(r['list_id'] for r in rows['train'])&set(r['list_id'] for r in rows['dev'])
    caches={};cr=json.loads((Path(CFG['cache_dir'])/'cache_receipt.json').read_text())
    for split in ['train','dev']:
        p=Path(CFG['cache_dir'])/(split+'.pt');receipts[str(p)]=fingerprint(p)
        assert receipts[str(p)]['sha256']==cr[split]['sha256']
        ca=torch.load(p,map_location='cpu',weights_only=False)
        assert ca['records']==rows[split]
        assert ca['hidden'].dtype==torch.float32 and torch.isfinite(ca['hidden']).all()
        for k in ['model','old_checkpoint_sha256','data_manifest_sha256']:assert ca['identity'][k]==CFG[k]
        caches[split]=ca
    p=Path(CFG['basis_path']);receipts[str(p)]=fingerprint(p)
    write(ROOT/'provenance/verified_inputs.json',{'checked_utc':utc(),'files':receipts,'TRAIN':4800,'DEV':1600,'TEST_opened':False,'checks':'one current full hash per required endpoint/data/cache/basis'})
    return caches

def model_load():
    # Content hash is performed once by verify_inputs_once; later replay loads
    # use its identity receipt and stat checks rather than repeated whole-file hashing.
    receipt=json.loads((ROOT/'provenance/verified_inputs.json').read_text())
    p=Path(CFG['old_checkpoint_path']);st=p.stat();fr=receipt['files'][str(p)]
    assert st.st_size==fr['bytes'] and st.st_mtime_ns==fr['mtime_ns']
    saved=torch.load(p,map_location='cpu',weights_only=False)
    assert saved['optimizer_step']==1200 and saved['tokens_seen']==24000
    assert set(saved['trainable_weights'])==set(NAMES)
    assert saved['parent_asset_id']==CFG['parent_model_asset_id']
    carrier=r05.QwenCarrier(CFG['model'],DEVICE)
    assert carrier.parent_identity==saved['base_disk_identity']
    named=dict(carrier.model.named_parameters())
    with torch.no_grad():
        for n in NAMES:named[n].copy_(saved['trainable_weights'][n].to(DEVICE))
    assert r05.frozen_hash(carrier.model,set(NAMES))==saved['frozen_sha256']
    for n in NAMES:named[n].requires_grad_(True)
    assert {n for n,p in carrier.model.named_parameters() if p.requires_grad}==set(NAMES)
    params=[named[n] for n in NAMES]
    assert sum(p.numel() for p in params)==6291456
    w0=[p.detach().clone() for p in params]
    bs=torch.load(CFG['basis_path'],map_location='cpu',weights_only=False)
    projs=[r05.Projector(bs[n]['u'].to(DEVICE),bs[n]['v'].to(DEVICE)) for n in NAMES]
    return carrier,r05.CachedAnswerLM(carrier.model),params,w0,projs,saved['frozen_sha256']

def optimizer(params):
    c=CFG['optimizer'];return torch.optim.AdamW(params,lr=c['lr'],betas=tuple(c['betas']),eps=c['eps'],weight_decay=0,foreach=False,fused=False)

def new_counters():return {'new_targets':0,'old_active_targets':0,'old_input_slots':0,'old_probe_targets':0,'input_tokens':0,'old_probe_input_tokens':0,'optimizer_steps':0,'all_input_slots':0,'valid_objective_targets':0}

def take_grad(model,params,cache,indices,mb):
    for p in params:p.grad=None
    total=0.
    for j in range(0,len(indices),mb):
        vals=r05.cache_batch(cache,indices[j:j+mb],DEVICE)
        v,_,_=model(*vals);(v/len(indices)).backward();total+=float(v.detach())
    g=[p.grad.detach().clone() for p in params]
    for p in params:p.grad=None
    return g,total/len(indices)

@torch.no_grad()
def probe_loss(model,cache,indices):
    total=0.
    for j in range(0,len(indices),CFG['probe_microbatch']):
        v,_,_=model(*r05.cache_batch(cache,indices[j:j+CFG['probe_microbatch']],DEVICE));total+=float(v)
    return total/len(indices)

def update(model,params,opt,projs,cache,order,method,k,t,counters):
    times={};start=time.monotonic()
    g,loss_probe=take_grad(model,params,cache,order['probe'],CFG['probe_microbatch'])
    times['probe_grad_seconds']=time.monotonic()-start
    assert all(torch.isfinite(x).all() for x in g)
    ix=order['new']+order['old'];mask=[1.]*36+([1.]*36 if k==36 else order['mask4'] if k==4 else [0.]*36)
    opt.zero_grad(set_to_none=True);new_sum=old_sum=0.
    phase=time.monotonic()
    for j in range(0,72,CFG['microbatch']):
        inds=ix[j:j+CFG['microbatch']];h,ma,le,y,mo=r05.cache_batch(cache,inds,DEVICE)
        weights=torch.tensor(mask[j:j+len(inds)],device=DEVICE)
        y=torch.where(weights.bool(),y,torch.zeros_like(y))
        _,_,losses=model(h,ma,le,y,mo)
        ((losses*weights).sum()/72).backward()
        vals=(losses.detach()*weights)
        if j<36:new_sum+=float(vals.sum())
        else:old_sum+=float(vals.sum())
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in params)
    grad_raw=length([p.grad for p in params]);torch.nn.utils.clip_grad_norm_(params,1.,foreach=False)
    grad_clipped=length([p.grad for p in params]);before=[p.detach().clone() for p in params]
    opt.step();times['objective_and_adam_seconds']=time.monotonic()-phase;phase=time.monotonic()
    with torch.no_grad():
        d=[p-w for p,w in zip(params,before)];desired,metrics=filter_step(d,g,method,projs,t)
        for p,w,dd in zip(params,before,desired):p.copy_(w+dd)
        actual=[p-w for p,w in zip(params,before)]
        err=length([a-b for a,b in zip(actual,desired)])
        projected=[pr(x) for x,pr in zip(actual,projs)]
        a2=float(squares(actual));c2=float(squares(projected))
        metrics.update(actual_norm=math.sqrt(a2),actual_C_norm=math.sqrt(c2),actual_C_energy_fraction=c2/a2 if a2 else 0.,g_dot_actual=float(dot(g,actual)),filter_roundoff_norm=err)
    assert all(torch.isfinite(p).all() for p in params)
    times['filter_seconds']=time.monotonic()-phase
    if t+1 in CFG['real_probe_loss_steps']:
        phase=time.monotonic();after=probe_loss(model,cache,order['probe'])
        metrics.update(probe_loss_before=loss_probe,probe_loss_after=after,probe_loss_change=after-loss_probe,first_order_remainder=after-loss_probe-metrics['g_dot_actual'])
        times['probe_after_forward_seconds']=time.monotonic()-phase
    counters['new_targets']+=36;counters['old_active_targets']+=k;counters['old_input_slots']+=36;counters['old_probe_targets']+=64
    counters['input_tokens']+=int(cache['lengths'][ix].sum());counters['old_probe_input_tokens']+=int(cache['lengths'][order['probe']].sum())
    counters['optimizer_steps']+=1;counters['all_input_slots']+=72;counters['valid_objective_targets']+=36+k
    metrics.update(step=t+1,probe_loss=loss_probe,new_train_ce=new_sum/36,old_active_train_ce=old_sum/k if k else 0.,old_active_count=k,
        train_lm_loss=(new_sum+old_sum)/(36+k),objective=(new_sum+old_sum)/72,new_weighted=new_sum/72,old_weighted=old_sum/72,
        objective_grad_raw_norm=grad_raw,objective_grad_clipped_norm=grad_clipped,clip_triggered=grad_raw>1.,
        counters=dict(counters),times=times,update_seconds=time.monotonic()-start)
    return metrics

@torch.no_grad()
def evaluate(model,cache):
    rows=[]
    for j in range(0,len(cache['records']),CFG['eval_microbatch']):
        ix=list(range(j,min(j+CFG['eval_microbatch'],len(cache['records']))))
        _,logits,losses=model(*r05.cache_batch(cache,ix,DEVICE));pred=logits.argmax(-1).cpu().tolist();ls=losses.cpu().tolist()
        for n,i in enumerate(ix):
            r=cache['records'][i];rows.append({'record_id':r['record_id'],'mode':r['mode'],'panel':r['panel'],'command':r['command'],'list_id':r['list_id'],
                    'prediction_id':pred[n],'target_id':r['target_id'],'correct':int(pred[n]==r['target_id']),'ce':ls[n]})
    ag={}
    for mode in [1,2]:
        for panel in ['combined']+sorted({r['panel'] for r in rows}):
            for cmd in ['both','甲','乙']:
                rr=[r for r in rows if r['mode']==mode and (panel=='combined' or r['panel']==panel) and (cmd=='both' or r['command']==cmd)]
                assert rr
                ag[f'mode{mode}/{cmd}/{panel}']={'n':len(rr),'accuracy':sum(r['correct'] for r in rr)/len(rr),'ce':sum(r['ce'] for r in rr)/len(rr)}
    assert ag['mode1/both/combined']['n']==800 and ag['mode2/both/combined']['n']==800
    return {'records':rows,'aggregates':ag,'scope':'exposed DEV; full151936-vocabulary argmax; answer CE in nat/answer; TEST not read'}

def telemetry(tb,m):
    t=m['step'];n=m['counters']['valid_objective_targets']
    for tag,val in [('train_lm_loss',m['train_lm_loss']),('train_total_loss',m['objective']),('loss_component/new_raw',m['new_train_ce']),('loss_component/new_weighted',m['new_weighted']),('loss_component/old_active_raw',m['old_active_train_ce']),('loss_component/old_active_weighted',m['old_weighted'])]:
        tb.add_scalar('tokens/'+tag,val,n);tb.add_scalar('updates/'+tag,val,t)
    tb.add_scalar('updates/learning_rate',1e-4,t)
    for tag,val in [('tokens_seen',n),('optimizer_step',t),('effective_tokens_per_update',36+m['old_active_count']),('new_targets',m['counters']['new_targets']),('probe_label_accesses',m['counters']['old_probe_targets'])]:tb.add_scalar('progress/'+tag,val,t)
    tb.add_scalar('progress/optimizer_step',t,n)
    for tag in ['candidate_norm','actual_norm','g_dot_candidate','g_dot_actual','probe_loss','actual_C_energy_fraction','objective_grad_raw_norm']:
        tb.add_scalar('diagnostics/'+tag,m[tag],t)
    tb.flush()

def save(case,params,opt,step,counters,seed,k,method,frozen,ordersha):
    state={'trainable_weights':{n:r05.cpu_tree(p) for n,p in zip(NAMES,params)},'optimizer':r05.cpu_tree(opt.state_dict()),
        'optimizer_step':step,'tokens_seen':counters['valid_objective_targets'],'counters':dict(counters),'data_cursor':step,
        'rng':r05.rng_state(DEVICE),'seed':seed,'old_nonzero':k,'method':method,'scheduler':{'kind':'R05_cosine','horizon':1200,'next_update':step},
        'old_checkpoint_sha256':CFG['old_checkpoint_sha256'],'config_sha256':r05.sha(ROOT/'config/frozen.json'),'orders_sha256':ordersha,
        'frozen_sha256':frozen,'projector_sha256':json.loads((ROOT/'provenance/verified_inputs.json').read_text())['files'][CFG['basis_path']]['sha256'],
        'base_model_asset':CFG['parent_model_asset_id'],'full_base_saved':False,'source_freeze_sha256':r05.sha(ROOT/'provenance/freeze.json')}
    p=case/'checkpoints'/f'step_{step:06}.pt';r05.atomic_save(p,state)
    write(p.with_suffix('.json'),{'path':str(p),'sha256':r05.sha(p),'bytes':p.stat().st_size,'step':step,'counters':counters,'full_base_saved':False})
    return p

def replay(statepath,expectedpath):
    r05.configure(29,DEVICE)
    data=torch.load(Path(CFG['cache_dir'])/'train.pt',map_location='cpu',weights_only=False)
    carrier,model,params,w0,projs,frozen=model_load();opt=optimizer(params)
    s=torch.load(statepath,map_location='cpu',weights_only=False);e=torch.load(expectedpath,map_location='cpu',weights_only=False)
    with torch.no_grad():
        for n,p in zip(NAMES,params):p.copy_(s['trainable_weights'][n].to(DEVICE))
    opt.load_state_dict(s['optimizer']);r05.restore_rng(s['rng'],DEVICE)
    orders=json.loads((ROOT/'provenance/orders.json').read_text())['seeds'];cnt=s['counters']
    update(model,params,opt,projs,data,orders[str(s['seed'])][s['optimizer_step']],s['method'],s['old_nonzero'],s['optimizer_step'],cnt)
    weights=all(torch.equal(p.cpu(),e['trainable_weights'][n]) for n,p in zip(NAMES,params));moments=r05.exact_tree(r05.cpu_tree(opt.state_dict()),e['optimizer'])
    rng=r05.exact_tree(r05.rng_state(DEVICE),e['rng']);counters=cnt==e['counters']
    ok=weights and moments and rng and counters
    write(ROOT/'provenance/external_process_replay.json',{'status':'PASS' if ok else 'FAIL','weights_bitwise':weights,'optimizer_bitwise':moments,'rng_exact':rng,'counters_exact':counters,'from':str(statepath),'to':str(expectedpath),'fresh_process':True,'time':utc()})
    assert ok,'external process replay'


def main():
    r05.configure(29,DEVICE)
    if (ROOT/'terminal.json').exists():raise ValueError('terminal exists, do not restart silently')
    ntests=numeric_tests();write(ROOT/'provenance/numeric_tests.json',ntests)
    caches=verify_inputs_once();train,dev=caches['train'],caches['dev'];orders=build_orders(train['records']);ordersha=r05.sha(ROOT/'provenance/orders.json')
    fs=[ROOT/'config/frozen.json',*sorted((ROOT/'source').glob('*.py')),ROOT/'provenance/orders.json']
    own=json.loads((ROOT/'provenance/ownership.json').read_text())
    fs += [Path(own['anchor'])/f for f in ['anchor.md','anchor_cn.md']]+[Path(own['round'])/f for f in ['protocol.md','protocol_cn.md']]
    write(ROOT/'provenance/freeze.json',{'frozen_utc':utc(),'before_new_DEV_and_training':True,'files':{str(p):fingerprint(p) for p in fs},'protocol_status':'APPROVED_FOR_BOUNDED_FULL','operator':'Codex gpt-6.1-sol','scientific_judgment':'Unknown'})
    carrier,model,params,w0,projs,frozen=model_load()
    frozen_versions=[(n,p,p._version) for n,p in carrier.model.named_parameters() if n not in NAMES]
    env={'utc':utc(),'python':sys.version,'torch':torch.__version__,'cuda':torch.version.cuda,'GPU':str(torch.cuda.get_device_properties(0)),
        'profile':os.getenv('RESOURCE_PROFILE'),'image':os.getenv('IMAGE_URL'),'host':os.uname().nodename,'gpu_used':True,'new_resource_quota_requested':False}
    write(ROOT/'provenance/environment.json',env)
    # One actual old/new DEV start replay, reused for every run's step0.
    baseline=evaluate(model,dev);write(ROOT/'provenance/start_DEV_replay.json',baseline)
    assert baseline['aggregates']['mode1/both/combined']['accuracy']==1.,'old start not qualified'
    # Current12/16 training shape replays vs complete native stack on an old TRAIN prefix.
    audit_indices=orders['29'][0]['old'][:12];records=[train['records'][i] for i in audit_indices]
    x,ma,le,y=r05.token_batch(records,DEVICE)
    with torch.no_grad():
        direct=carrier.model(input_ids=x,attention_mask=ma,use_cache=False).logits[torch.arange(len(le),device=DEVICE),le-1]
        cached=model(*r05.cache_batch(train,audit_indices,DEVICE))[1]
        err=float((direct-cached).abs().max());same=torch.equal(direct.argmax(-1),cached.argmax(-1))
    write(ROOT/'provenance/current_shape_cache_check.json',{'count':12,'logits_maxabs':err,'argmax_equal':same,'threshold':2e-4,'prior_shapes':'R05 saved native/cache exact replay cited'})
    assert same and err<=2e-4
    oldstart={n:{'shape':list(p.shape),'dtype':str(p.dtype)} for n,p in zip(NAMES,params)}
    write(ROOT/'provenance/trainable_scope.json',{'names':oldstart,'parameters':sum(p.numel() for p in params),'frozen_sha256':frozen,'old_optimizer_carried':False})
    started=time.time();deadline=started+CFG['wallclock_seconds'];cutoff=started+CFG['training_cutoff_seconds']
    write(ROOT/'budget.json',{'training_start_epoch':started,'training_start_utc':utc(),'deadline_epoch':deadline,'training_cutoff_epoch':cutoff,'wallclock_seconds':14400,'report_reserve_seconds':600})
    first=True;coverage=[];budget_hit=False
    for seed in CFG['seeds']:
        for k in CFG['old_slots_nonzero']:
            for method in CFG['methods']:
                if time.time()>=cutoff:budget_hit=True;coverage.append({'seed':seed,'old_nonzero':k,'method':method,'status':'MISSING_BUDGET'});continue
                case=ROOT/'runs'/f'seed_{seed}'/f'old_{k:02}'/method;case.mkdir(parents=True,exist_ok=True)
                r05.configure(seed,DEVICE)
                with torch.no_grad():
                    for p,w in zip(params,w0):p.copy_(w)
                opt=optimizer(params);assert len(opt.state)==0
                cnt=new_counters();tb=SummaryWriter(str(case/'tensorboard'));runstart=time.monotonic();step=0
                write(case/'scope.json',{'seed':seed,'old_nonzero':k,'method':method,'orders_sha256':ordersha,'same_acquired_old':True,'optimizer_state_empty':True,'configuration':str(ROOT/'config/frozen.json')})
                write(case/'eval_000000.json',{'step':0,'shared_source':str(ROOT/'provenance/start_DEV_replay.json'),'aggregates':baseline['aggregates'],'counters':cnt,'elapsed_seconds':0})
                save(case,params,opt,0,cnt,seed,k,method,frozen,ordersha)
                status='DONE_EXPLORATORY';error=None
                print(json.dumps({'event':'run_start','seed':seed,'old_nonzero':k,'method':method,'utc':utc()}),flush=True)
                try:
                    for t in range(240):
                        if time.time()>=cutoff:status='PARTIAL_BUDGET';budget_hit=True;break
                        m=update(model,params,opt,projs,train,orders[str(seed)][t],method,k,t,cnt);step=t+1
                        if any(p._version!=v for n,p,v in frozen_versions):raise RuntimeError('frozen tensor version drift')
                        telemetry(tb,m);append(case/'metrics.jsonl',m)
                        if step in CFG['save_steps']:save(case,params,opt,step,cnt,seed,k,method,frozen,ordersha)
                        if step in CFG['eval_steps']:
                            ev=evaluate(model,dev);ev.update(step=step,counters=dict(cnt),elapsed_seconds=time.monotonic()-runstart);write(case/f'eval_{step:06}.json',ev)
                        if first and step==2:
                            from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
                            ea=EventAccumulator(str(case/'tensorboard')).Reload();tags=ea.Tags()['scalars']
                            required=['tokens/train_lm_loss','updates/train_lm_loss','tokens/train_total_loss','progress/tokens_seen','tokens/loss_component/new_raw','tokens/loss_component/old_active_weighted']
                            assert all(tag in tags for tag in required)
                            assert ea.Scalars('progress/tokens_seen')[-1].value==2*(36+k)
                            write(ROOT/'provenance/telemetry_smoke.json',{'status':'PASS','tags':tags,'first_two_target_count':2*(36+k)})
                            proc=subprocess.run([sys.executable,str(ROOT/'source/entry.py'),str(ROOT/'source/engine.py'),'--replay',str(case/'checkpoints/step_000001.pt'),str(case/'checkpoints/step_000002.pt')],stdout=open(ROOT/'provenance/replay_stdout.log','w'),stderr=subprocess.STDOUT)
                            assert proc.returncode==0,'external replay failed; see replay_stdout.log'
                            first=False
                        if step in [2,64,120,240]:print(json.dumps({'event':'progress','seed':seed,'old_nonzero':k,'method':method,'step':step,'elapsed_run_seconds':time.monotonic()-runstart}),flush=True)
                    if step<240 and status=='DONE_EXPLORATORY':status='PARTIAL_BUDGET'
                except Exception:
                    status='FAILED';error=traceback.format_exc();append(ROOT/'errors.jsonl',{'seed':seed,'old_nonzero':k,'method':method,'step':step,'error':error,'utc':utc()})
                    if first:raise
                finally:
                    tb.close()
                if status!='DONE_EXPLORATORY':save(case,params,opt,step,cnt,seed,k,method,frozen,ordersha)
                row={'seed':seed,'old_nonzero':k,'method':method,'status':status,'steps':step,'counters':cnt,'elapsed_seconds':time.monotonic()-runstart,'error':error}
                write(case/'completion.json',row);coverage.append(row);write(ROOT/'coverage.json',coverage)
                print(json.dumps({'event':'run_complete',**{a:b for a,b in row.items() if a not in ['error','counters']}}),flush=True)
                del opt
    assert r05.frozen_hash(carrier.model,set(NAMES))==frozen
    freeze=json.loads((ROOT/'provenance/freeze.json').read_text())
    for p,r in freeze['files'].items():assert r05.sha(p)==r['sha256'],'source/config/contract changed during run'
    terminal={'status':'BUDGET_EXHAUSTED' if budget_hit else 'COMPLETED','utc':utc(),'training_wall_seconds':time.time()-started,'coverage':coverage,'frozen_final_match':True,'TEST_opened':False}
    write(ROOT/'terminal.json',terminal)
    print(json.dumps({'event':'terminal','status':terminal['status'],'completed':sum(r['status']=='DONE_EXPLORATORY' for r in coverage),'wall_seconds':time.time()-started}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',nargs=2);a=p.parse_args()
    if a.replay:replay(*map(Path,a.replay))
    else:
        try:main()
        except Exception:
            write(ROOT/'fatal.json',{'utc':utc(),'error':traceback.format_exc()});raise
