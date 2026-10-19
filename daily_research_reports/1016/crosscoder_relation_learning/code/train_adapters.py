"""Frozen Qwen3 final-residual adapter experiment. No model/router training.

Cache contract: hidden[N,d] is final decoder block output BEFORE final RMSNorm;
target[N] is the actual next token; routes is a dict R/F/N[N]. CSR feature_ptr
and feature_ids contain ALL positive gated features, never a top-k truncation.
Every condition receives identical complete representations and targets.
"""
from __future__ import annotations
import argparse
import contextlib
import copy
import csv
import hashlib
import json
import math
import os
import random
import resource
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('w') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False); f.write('\n')
        f.flush(); os.fsync(f.fileno())
    tmp.replace(path)


def atomic_save(path, state):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    with tmp.open('wb') as f:
        torch.save(state, f); f.flush(); os.fsync(f.fileno())
    tmp.replace(path)


def tree_cpu(x):
    if torch.is_tensor(x): return x.detach().cpu().clone()
    if isinstance(x, dict): return {k: tree_cpu(v) for k, v in x.items()}
    if isinstance(x, list): return [tree_cpu(v) for v in x]
    if isinstance(x, tuple): return tuple(tree_cpu(v) for v in x)
    return x


def tensor_hash(state):
    h = hashlib.sha256()
    for k, x in sorted(state.items()):
        x = x.detach().cpu().contiguous()
        h.update(k.encode()); h.update(str(x.dtype).encode()); h.update(x.view(torch.uint8).numpy().tobytes())
    return h.hexdigest()


def tree_equal(a,b):
    if torch.is_tensor(a):return torch.equal(a,b)
    if isinstance(a,dict):return a.keys()==b.keys() and all(tree_equal(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)):return len(a)==len(b) and all(tree_equal(x,y) for x,y in zip(a,b))
    return a==b


class ResidualExperts(nn.Module):
    """Four bias-free linear bottlenecks, rank 32, top-1; paired initialization."""
    def __init__(self, d=1024, rank=32, k=4, seed=42):
        super().__init__()
        gen = torch.Generator(device='cpu').manual_seed(seed)
        self.down = nn.Parameter(torch.randn(k, rank, d, generator=gen) / math.sqrt(d))
        self.up = nn.Parameter(torch.zeros(k, d, rank))
        self.d, self.rank, self.k = d, rank, k

    def forward(self, hidden, route):
        h = hidden.float()
        # Small matrices stay fp32; final frozen vocabulary projection may use bf16.
        out = torch.zeros_like(h)
        for e in range(self.k):
            ids = torch.nonzero(route == e, as_tuple=False).flatten()
            if ids.numel(): out[ids] = F.linear(F.linear(h[ids], self.down[e]), self.up[e])
        return h + out


class FrozenHead(nn.Module):
    def __init__(self, norm, weight, eps=1e-6, output_dtype=torch.bfloat16):
        super().__init__()
        self.register_buffer('norm_weight', norm.detach().to(output_dtype))
        self.register_buffer('head_weight', weight.detach().to(output_dtype))
        self.eps = eps
        self.output_dtype = output_dtype

    def forward(self, h):
        # Preserve native Qwen3 BF16 residual/RMSNorm semantics exactly:
        # input BF16 -> variance FP32 -> normalized BF16 -> norm weight BF16.
        h = h.to(self.output_dtype).float()
        h = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + self.eps)
        h = h.to(self.output_dtype) * self.norm_weight
        return F.linear(h, self.head_weight)

    @classmethod
    def load(cls, model_dir, device):
        from safetensors import safe_open
        model_dir = Path(model_dir)
        cfg = json.loads((model_dir/'config.json').read_text())
        with safe_open(str(model_dir/'model.safetensors'), framework='pt', device='cpu') as f:
            norm = f.get_tensor('model.norm.weight')
            key = 'lm_head.weight'
            if key not in f.keys():
                if not cfg.get('tie_word_embeddings', False): raise ValueError('Missing untied LM head')
                key = 'model.embed_tokens.weight'
            head = f.get_tensor(key)
        if tuple(head.shape) != (151936, 1024): raise ValueError('Unexpected real Qwen vocabulary/head')
        out = cls(norm, head, cfg['rms_norm_eps']).to(device).eval()
        for p in out.parameters(): p.requires_grad_(False)
        return out


def validate_cache(data, vocab=151936):
    n = len(data['target'])
    if data['hidden'].shape != (n, 1024): raise ValueError('Wrong cached final-residual shape')
    if not torch.isfinite(data['hidden']).all(): raise ValueError('Nonfinite residual')
    if not ((data['target'] >= 0) & (data['target'] < vocab)).all(): raise ValueError('Invalid next token')
    for arm in ('R', 'F', 'N'):
        r = data['routes'][arm]
        if r.shape != (n,) or not ((r >= 0) & (r < 4)).all(): raise ValueError('Invalid fixed route')
    ptr, ids = data['feature_ptr'], data['feature_ids']
    if len(ptr) != n+1 or ptr[0] != 0 or ptr[-1] != len(ids) or not (ptr[1:] >= ptr[:-1]).all():
        raise ValueError('Malformed complete feature CSR')
    if not ((ids >= 0) & (ids < 16384)).all(): raise ValueError('Invalid feature IDs')
    if data['position_id'].unique().numel() != n: raise ValueError('Duplicate source positions')


def order_indices(n, updates, batch, seed):
    if n < batch: raise ValueError('Training cache smaller than one fixed batch')
    gen = torch.Generator().manual_seed(seed + 91217)
    chunks = []
    while sum(len(x) for x in chunks) < updates * batch:
        chunks.append(torch.randperm(n, generator=gen)[:(n//batch)*batch])
    return torch.cat(chunks)[:updates*batch].view(updates, batch)


def feature_reduce(data, losses, min_support=5):
    ptr, ids = data['feature_ptr'].long(), data['feature_ids'].long()
    row = torch.repeat_interleave(torch.arange(len(losses)), ptr[1:] - ptr[:-1])
    counts = torch.bincount(ids, minlength=16384)
    sums = torch.zeros(16384, dtype=torch.float64).scatter_add_(0, ids, losses.double()[row])
    means = sums / counts.clamp_min(1)
    out = {'overall': float(losses.double().mean()), 'n_tokens': len(losses), 'min_eval_support': min_support}
    for label in ('low', 'high'):
        sel = data[label + '_ids'].long()
        eligible = sel[counts[sel] >= min_support]
        out[label + '_loss'] = float(means[eligible].mean()) if len(eligible) else None
        out[label + '_eligible_features'] = len(eligible)
        out[label + '_defined_features'] = len(sel)
        out[label + '_coverage'] = len(eligible)/len(sel) if len(sel) else 0.
        hit=torch.zeros(len(losses),dtype=torch.long).scatter_add_(0,row,torch.isin(ids,eligible).long())
        out[label + '_position_union'] = int((hit>0).sum())
    return out, counts, means


@torch.no_grad()
def predict_losses(model, head, data, arm, batch, device):
    losses = torch.empty(len(data['target']), dtype=torch.float32)
    for start in range(0, len(losses), batch):
        end = min(start+batch, len(losses))
        h = data['hidden'][start:end].to(device)
        route = data['routes'][arm][start:end].to(device)
        target = data['target'][start:end].to(device)
        logits = head(model(h, route))
        loss = F.cross_entropy(logits.float(), target, reduction='none')
        if not torch.isfinite(loss).all(): raise FloatingPointError('Nonfinite eval loss')
        losses[start:end] = loss.cpu()
    return losses


def gradients(model, head, hidden, route, targets, timing=None):
    model.zero_grad(set_to_none=True)
    if timing is not None and hidden.is_cuda:torch.cuda.synchronize(hidden.device)
    t=time.monotonic()
    losses = F.cross_entropy(head(model(hidden, route)).float(), targets, reduction='none')
    loss = losses.mean()
    if not torch.isfinite(loss): raise FloatingPointError('Nonfinite NTP')
    if timing is not None:
        if hidden.is_cuda:torch.cuda.synchronize(hidden.device)
        timing['forward_seconds']=time.monotonic()-t
    t=time.monotonic()
    loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
    if not torch.isfinite(norm): raise FloatingPointError('Nonfinite gradients')
    if timing is not None:
        if hidden.is_cuda:torch.cuda.synchronize(hidden.device)
        timing['backward_seconds']=time.monotonic()-t
    return float(loss.detach()), float(norm), losses.detach()


def rng_state():
    return {'python': random.getstate(), 'numpy': np.random.get_state(), 'torch': torch.get_rng_state(),
            'cuda': torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None}


def restore_rng(state):
    random.setstate(state['python']); np.random.set_state(state['numpy']); torch.set_rng_state(state['torch'])
    if state['cuda'] is not None: torch.cuda.set_rng_state_all(state['cuda'])


def train(args):
    from torch.utils.tensorboard import SummaryWriter
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True)
    cfg = json.loads(Path(args.config).read_text())
    device = torch.device(args.device)
    if device.type != 'cuda' or 'H100' not in torch.cuda.get_device_name(device): raise RuntimeError('Allocated H100 required')
    cfg_hash = sha(args.config)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    lock = out/'.run.lock'
    try: fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError: raise RuntimeError('Existing run lock; do not duplicate a live run')
    os.write(fd, str(os.getpid()).encode()); os.close(fd)
    started = time.monotonic()
    try:
        train_data = torch.load(cfg['train_cache'], map_location='cpu', weights_only=False)
        eval_data = torch.load(cfg['eval_cache'], map_location='cpu', weights_only=False)
        validate_cache(train_data); validate_cache(eval_data)
        # Offsets are local to each source file; equal integers in two different
        # files are different positions. Validate the source-qualified split.
        tm=json.loads(Path(cfg['train_cache']).with_name('train_manifest.json').read_text())
        em=json.loads(Path(cfg['eval_cache']).with_name('eval_manifest.json').read_text())
        if set(tm['source_paths']) & set(em['source_paths']):raise ValueError('Learning/eval source-file overlap')
        if torch.isin(train_data['block_id'].unique(),eval_data['block_id'].unique()).any():
            raise ValueError('Learning/eval globally indexed context overlap')
        expected_hashes = cfg.get('cache_sha256', {})
        for label in ('train', 'eval'):
            if label in expected_hashes and sha(cfg[label+'_cache']) != expected_hashes[label]: raise ValueError('Cache hash drift')
        model = ResidualExperts(seed=args.seed).to(device)
        head = FrozenHead.load(cfg['model_dir'], device)
        frozen_versions = {k: x._version for k, x in head.named_buffers()}
        initial_hash = tensor_hash(model.state_dict())
        if sum(p.numel() for p in model.parameters()) != 262144: raise ValueError('Parameter count')
        opt_cfg = cfg['optimizer']
        opt = torch.optim.AdamW(model.parameters(), lr=opt_cfg['lr'], betas=tuple(opt_cfg['betas']),
                                eps=opt_cfg['eps'], weight_decay=opt_cfg['weight_decay'], foreach=False, fused=False)
        batch, total = cfg['batch_size'], cfg['updates']
        order = order_indices(len(train_data['target']), total, batch, args.seed)
        order_hash = hashlib.sha256(order.numpy().tobytes()).hexdigest()
        eval_steps = sorted(set([0, total]+cfg['eval_steps']))
        if cfg['midpoint'] not in eval_steps: raise ValueError('Midpoint must be saved/evaluated')
        step, tokens = 0, 0
        source_hash = sha(__file__)
        def stage_timing(label,at,seconds):
            with (out/'stage_timings.jsonl').open('a') as f:
                f.write(json.dumps({'stage':label,'optimizer_step':at,'tokens_seen':at*batch,
                        'seconds':seconds,'arm':args.arm,'seed':args.seed})+'\n')
        def checkpoint(step, tokens):
            tc=time.monotonic()
            state = {'adapters': tree_cpu(model.state_dict()), 'optimizer': tree_cpu(opt.state_dict()),
                     'step': step, 'tokens_seen': tokens, 'data_cursor': step*batch, 'order_hash': order_hash,
                     'config_sha256': cfg_hash, 'source_sha256': source_hash, 'initialization_hash': initial_hash,
                     'seed': args.seed, 'arm': args.arm, 'rng': rng_state(), 'head_frozen': True,
                     'trainable_parameters': 262144, 'active_parameters': 65536}
            path = out/'checkpoints'/f'update_{step:05d}.pt'; atomic_save(path, state)
            write_json(path.with_suffix('.json'), {'complete': True, 'path': str(path), 'sha256': sha(path),
                       'step': step, 'tokens_seen': tokens, 'config_sha256': cfg_hash, 'source_sha256': source_hash})
            stage_timing('checkpoint',step,time.monotonic()-tc)
        if args.resume:
            state = torch.load(args.resume, map_location='cpu', weights_only=False)
            for key, value in [('config_sha256', cfg_hash), ('source_sha256', source_hash), ('order_hash', order_hash),
                               ('arm', args.arm), ('seed', args.seed), ('initialization_hash', initial_hash)]:
                if state[key] != value: raise ValueError('Resume identity failed: '+key)
            model.load_state_dict(state['adapters']); opt.load_state_dict(state['optimizer']); restore_rng(state['rng'])
            step, tokens = state['step'], state['tokens_seen']
            if tokens != step*batch or state['data_cursor'] != tokens: raise ValueError('Resume counter mismatch')
        elif (out/'completion.json').exists() or (out/'metrics.jsonl').exists():
            raise ValueError('Existing run requires explicit resume')
        # Resume writes a named segment: TensorBoard purge_step cannot safely
        # purge both optimizer-index and token-index tags with one coordinate.
        tbdir=out/'tensorboard'/(f'resume_from_update_{step:05d}' if args.resume else 'initial')
        writer = SummaryWriter(str(tbdir))
        write_json(out/'run_contract.json', {'config': cfg, 'config_sha256': cfg_hash, 'source_sha256': source_hash,
                   'arm': args.arm, 'seed': args.seed, 'initialization_hash': initial_hash, 'order_hash': order_hash,
                   'total_trainable_parameters': 262144, 'active_parameters_per_position': 65536,
                   'gpu': torch.cuda.get_device_name(device), 'torch': torch.__version__,
                   'head_vocab': 151936, 'head_projection_dtype': 'bf16', 'adapter_and_ce_dtype': 'fp32',
                   'components': {}, 'loss_denominator': 'all valid prediction tokens in fixed batch',
                   'no_skipped_updates': True, 'data_order': 'paired seeded permutation, repeated full epochs',
                   'estimated_flops_per_training_token_head_only': 4*151936*1024})
        def evaluate(at):
            te=time.monotonic()
            losses = predict_losses(model, head, eval_data, args.arm, cfg['eval_batch_size'], device)
            metrics, counts, means = feature_reduce(eval_data, losses, cfg['min_eval_support'])
            metrics.update(step=at, tokens_seen=at*batch, arm=args.arm, seed=args.seed)
            np.save(out/f'eval_losses_{at:05d}.npy', losses.numpy())
            write_json(out/f'eval_{at:05d}.json', metrics)
            if at in (0, total):
                with (out/f'feature_metrics_{at:05d}.csv').open('w') as f:
                    w=csv.writer(f); w.writerow(['feature_id','support','mean_ntp_loss','eligible'])
                    for i in range(16384): w.writerow([i,int(counts[i]),float(means[i]) if counts[i] else '',int(counts[i]>=cfg['min_eval_support'])])
            for name in ('overall','low_loss','high_loss'):
                if metrics[name] is not None: writer.add_scalar('tokens/eval_'+name, metrics[name], at*batch)
            writer.flush()
            stage_timing('evaluation',at,time.monotonic()-te)
            return metrics
        if not args.resume:
            # Exact zero adapter output and route invariance at initialization.
            h = train_data['hidden'][:batch].to(device)
            with torch.no_grad():
                ref = head(h); got = head(model(h, train_data['routes'][args.arm][:batch].to(device)))
                zero_error = float((ref.float()-got.float()).abs().max())
            if zero_error != 0: raise ValueError('Zero adapter failed exact no-op')
            checkpoint(0,0); initial_eval = evaluate(0)
            write_json(out/'zero_guard.json', {'max_logit_error': zero_error, 'status':'PASS',
                       'reference':'cached final residual through identical frozen native norm/head',
                       'native_end_to_end_cache_guard':'owned by cache extraction receipt'})
        for index in range(step, total):
            t0 = time.monotonic(); ids = order[index]
            h = train_data['hidden'][ids].to(device); target=train_data['target'][ids].to(device)
            route = train_data['routes'][args.arm][ids].to(device)
            torch.cuda.synchronize(device);data_seconds=time.monotonic()-t0
            timing={}
            loss, raw_grad, _ = gradients(model, head, h, route, target,timing=timing)
            if index == 0 and float(model.up.grad.norm()) <= 0: raise ValueError('Zero-up initialization has no effective gradient')
            topt=time.monotonic()
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg['gradient_clip'], foreach=False)
            opt.step()
            torch.cuda.synchronize(device);optimizer_seconds=time.monotonic()-topt
            if not all(torch.isfinite(p).all() for p in model.parameters()): raise FloatingPointError('Nonfinite adapters')
            if any(x._version != frozen_versions[k] for k,x in head.named_buffers()): raise ValueError('Frozen head modified')
            step=index+1; tokens=step*batch
            torch.cuda.synchronize(device); seconds=time.monotonic()-t0
            loads=torch.bincount(route,minlength=4).cpu().tolist()
            expert_grad=torch.sqrt(model.down.grad.double().flatten(1).square().sum(-1)+
                                   model.up.grad.double().flatten(1).square().sum(-1)).cpu().tolist()
            metrics={'optimizer_step':step,'tokens_seen':tokens,'loss':loss,'total_loss':loss,'raw_gradient_norm':raw_grad,
                     'learning_rate':opt_cfg['lr'],'effective_tokens':batch,'expert_tokens':loads,
                     'expert_gradient_norm':expert_grad,'expert_nonzero_gradient':[x>0 for x in expert_grad],
                     'data_seconds':data_seconds,'forward_seconds':timing['forward_seconds'],
                     'backward_seconds':timing['backward_seconds'],'optimizer_seconds':optimizer_seconds,
                     'rss_peak_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                     'gpu_allocated_bytes':torch.cuda.memory_allocated(device),
                     'gpu_reserved_bytes':torch.cuda.memory_reserved(device),
                     'gpu_peak_allocated_bytes':torch.cuda.max_memory_allocated(device),
                     'step_seconds':seconds,'arm':args.arm,'seed':args.seed,'skipped':False}
            with (out/'metrics.jsonl').open('a') as f: f.write(json.dumps(metrics)+'\n')
            for tag,value,x in [('tokens/train_lm_loss',loss,tokens),('updates/train_lm_loss',loss,step),
                                ('tokens/train_total_loss',loss,tokens),('updates/learning_rate',opt_cfg['lr'],step),
                                ('progress/tokens_seen',tokens,step),('progress/optimizer_step',step,tokens),
                                ('progress/effective_tokens_per_update',batch,step)]: writer.add_scalar(tag,value,x)
            for e,n in enumerate(loads): writer.add_scalar(f'updates/expert_{e}_tokens',n,step)
            for name in ('data_seconds','forward_seconds','backward_seconds','optimizer_seconds','step_seconds'):
                writer.add_scalar('updates/timing/'+name,metrics[name],step)
            for name in ('rss_peak_bytes','gpu_allocated_bytes','gpu_reserved_bytes','gpu_peak_allocated_bytes'):
                writer.add_scalar('updates/memory/'+name,metrics[name],step)
            writer.flush()
            if step in eval_steps:
                checkpoint(step,tokens); ev=evaluate(step)
                print(json.dumps({'arm':args.arm,'seed':args.seed,'step':step,'tokens_seen':tokens,
                       'train_loss':loss,'eval':ev,'elapsed_seconds':time.monotonic()-started}),flush=True)
            elif step == 1 or step%32==0:
                print(json.dumps({'arm':args.arm,'seed':args.seed,'step':step,'tokens_seen':tokens,
                                 'loss':loss,'elapsed_seconds':time.monotonic()-started}),flush=True)
        writer.close()
        # Verify actual persisted event tags and coordinate mapping, not just writer calls.
        from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
        events=EventAccumulator(str(tbdir),size_guidance={'scalars':0}).Reload()
        required=['tokens/train_lm_loss','updates/train_lm_loss','tokens/train_total_loss','updates/learning_rate',
                  'progress/tokens_seen','progress/optimizer_step','progress/effective_tokens_per_update']
        if any(t not in events.Tags()['scalars'] for t in required): raise ValueError('Missing TensorBoard tags')
        points=events.Scalars('tokens/train_lm_loss')
        if any(not math.isfinite(p.value) for p in points) or any(b.step<=a.step for a,b in zip(points,points[1:])):
            raise ValueError('Invalid persisted token-coordinate losses')
        if points[-1].step != tokens: raise ValueError('Persisted token counter mismatch')
        write_json(out/'telemetry_verification.json',{'status':'PASS','required_tags':required,
                   'monotonic_tokens':True,'final_tokens':tokens,'batch_valid_target_count':batch,'skipped_updates':0})
        write_json(out/'completion.json',{'execution_status':'COMPLETE','scientific_verdict':'UNASSIGNED',
                   'arm':args.arm,'seed':args.seed,'updates':step,'tokens_seen':tokens,
                   'initialization_hash':initial_hash,'final_adapter_hash':tensor_hash(model.state_dict()),
                   'elapsed_seconds':time.monotonic()-started,'config_sha256':cfg_hash,'source_sha256':source_hash})
    finally:
        lock.unlink(missing_ok=True)


def smoke(args):
    """One fixed R pilot for numerical/throughput qualification only."""
    from torch.utils.tensorboard import SummaryWriter
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False
    torch.use_deterministic_algorithms(True)
    cfg=json.loads(Path(args.config).read_text());out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    device=torch.device(args.device)
    if device.type!='cuda' or 'H100' not in torch.cuda.get_device_name(device):raise RuntimeError('H100 required')
    data=torch.load(cfg['train_cache'],map_location='cpu',weights_only=False);validate_cache(data)
    model=ResidualExperts(seed=args.seed).to(device);head=FrozenHead.load(cfg['model_dir'],device)
    batch=cfg['batch_size'];indices=order_indices(len(data['target']),12,batch,args.seed)
    oc=cfg['optimizer'];opt=torch.optim.AdamW(model.parameters(),lr=oc['lr'],betas=tuple(oc['betas']),
                 eps=oc['eps'],weight_decay=oc['weight_decay'],foreach=False,fused=False)
    h=data['hidden'][indices[0]].to(device);route=data['routes']['R'][indices[0]].to(device);y=data['target'][indices[0]].to(device)
    with torch.no_grad():error=float((head(h).float()-head(model(h,route)).float()).abs().max())
    if error!=0:raise ValueError('Zero-adapter no-op')
    writer=SummaryWriter(str(out/'tensorboard'));times=[];phase_times=[];saved=None;expected=None
    for step in range(1,13):
        i=indices[step-1];h=data['hidden'][i].to(device);route=data['routes']['R'][i].to(device);y=data['target'][i].to(device)
        torch.cuda.synchronize(device);t=time.monotonic()
        timing={};loss,norm,_=gradients(model,head,h,route,y,timing=timing)
        if step==1 and model.up.grad.norm()<=0:raise ValueError('Dead low-rank initialization')
        topt=time.monotonic()
        torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip'],foreach=False);opt.step()
        torch.cuda.synchronize(device);timing['optimizer_seconds']=time.monotonic()-topt
        times.append(time.monotonic()-t);phase_times.append(timing)
        if step==5:
            saved=tree_cpu({'adapters':model.state_dict(),'optimizer':opt.state_dict(),'rng':rng_state(),
                           'step':step,'tokens_seen':step*batch,'data_cursor':step*batch})
            atomic_save(out/'resume_smoke.pt',saved)
        if step==6:expected=tree_cpu({'adapters':model.state_dict(),'optimizer':opt.state_dict()})
        for tag,value,x in [('tokens/train_lm_loss',loss,step*batch),('updates/train_lm_loss',loss,step),
                           ('tokens/train_total_loss',loss,step*batch),('updates/learning_rate',oc['lr'],step),
                           ('progress/tokens_seen',step*batch,step),('progress/optimizer_step',step,step*batch),
                           ('progress/effective_tokens_per_update',batch,step)]:writer.add_scalar(tag,value,x)
    writer.close()
    restored=torch.load(out/'resume_smoke.pt',map_location='cpu',weights_only=False)
    replay=ResidualExperts(seed=args.seed).to(device);replay.load_state_dict(restored['adapters'])
    opt2=torch.optim.AdamW(replay.parameters(),lr=oc['lr'],betas=tuple(oc['betas']),eps=oc['eps'],
                          weight_decay=oc['weight_decay'],foreach=False,fused=False)
    opt2.load_state_dict(restored['optimizer']);restore_rng(restored['rng'])
    i=indices[5];h=data['hidden'][i].to(device);route=data['routes']['R'][i].to(device);y=data['target'][i].to(device)
    gradients(replay,head,h,route,y);torch.nn.utils.clip_grad_norm_(replay.parameters(),cfg['gradient_clip'],foreach=False);opt2.step()
    exact=tree_equal(expected,tree_cpu({'adapters':replay.state_dict(),'optimizer':opt2.state_dict()}))
    if not exact:raise ValueError('Serialized checkpoint replay changed exact next update')
    events=EventAccumulator(str(out/'tensorboard'),size_guidance={'scalars':0}).Reload()
    tags=['tokens/train_lm_loss','updates/train_lm_loss','tokens/train_total_loss','updates/learning_rate',
          'progress/tokens_seen','progress/optimizer_step','progress/effective_tokens_per_update']
    if any(k not in events.Tags()['scalars'] for k in tags):raise ValueError('Smoke telemetry missing')
    seq=events.Scalars(tags[0]);assert [p.step for p in seq]==list(range(batch,13*batch,batch))
    # Fixed candidate virtual step; qualify its size without choosing by probe benefit.
    gradients(model,head,h,route,y)
    grad_norms=torch.sqrt(model.down.grad.double().flatten(1).square().sum(-1)+model.up.grad.double().flatten(1).square().sum(-1))
    param_norms=torch.sqrt(model.down.double().flatten(1).square().sum(-1)+model.up.double().flatten(1).square().sum(-1))
    candidate=0.1
    if float((candidate*grad_norms/param_norms.clamp_min(1e-12)).max())>0.05:candidate=0.01
    with torch.no_grad():
        for p in model.parameters():p.add_(p.grad,alpha=-candidate)
        virtual=F.cross_entropy(head(model(h,route)).float(),y)
    if not torch.isfinite(virtual):raise FloatingPointError('Virtual SGD numeric failure')
    result={'status':'PASS','gpu':torch.cuda.get_device_name(device),'torch':torch.__version__,
       'zero_adapter_max_logit_error':error,'serialized_next_update_replay_exact':exact,'external_process_resume':'NOT_QUALIFIED',
       'valid_tokens_per_update':batch,'required_tb_tags':tags,'median_update_seconds':float(np.median(times[2:])),
       'observed_update_seconds':times,'estimated_train_tokens_per_second':batch/float(np.median(times[2:])),
       'phase_timings':phase_times,
       'virtual_sgd_lr_fixed':candidate,'virtual_sgd_max_relative_expert_step':float((candidate*grad_norms/param_norms.clamp_min(1e-12)).max()),
       'virtual_sgd_finite':True,'selection_rule':'0.1 unless expert relative parameter step exceeds 0.05; else 0.01',
       'config_sha256':sha(args.config),'source_sha256':sha(__file__),'comparison_outcomes_inspected':False}
    write_json(out/'smoke.json',result);print(json.dumps(result),flush=True)


def selftest():
    torch.set_num_threads(2)
    model=ResidualExperts(d=12,rank=3,k=4,seed=42)
    head=FrozenHead(torch.ones(12),torch.randn(31,12),output_dtype=torch.float32)
    h=torch.randn(16,12); route=torch.arange(16)%4; target=torch.arange(16)%31
    assert torch.equal(model(h,route),h)
    assert torch.equal(head(model(h,route)),head(h))
    optimizer=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=0,foreach=False)
    loss,_,_=gradients(model,head,h,route,target)
    assert model.up.grad.norm()>0 and model.down.grad.norm()==0
    optimizer.step()
    saved=tree_cpu({'model':model.state_dict(),'opt':optimizer.state_dict()})
    gradients(model,head,h,route,target);optimizer.step(); expected=tree_cpu(model.state_dict())
    resumed=ResidualExperts(d=12,rank=3,k=4,seed=42); resumed.load_state_dict(saved['model'])
    opt2=torch.optim.AdamW(resumed.parameters(),lr=1e-3,weight_decay=0,foreach=False);opt2.load_state_dict(saved['opt'])
    gradients(resumed,head,h,route,target);opt2.step()
    assert all(torch.equal(expected[k],resumed.state_dict()[k]) for k in expected)
    order=order_indices(23,12,8,42);assert torch.equal(order,order_indices(23,12,8,42))
    toy={'feature_ptr':torch.tensor([0,2,3,5]),'feature_ids':torch.tensor([0,1,0,1,2]),
         'low_ids':torch.tensor([0,1]),'high_ids':torch.tensor([2])}
    m,c,f=feature_reduce(toy,torch.tensor([1.,3.,5.]),1)
    assert m['low_loss']==2.5 and m['high_loss']==5. and m['overall']==3.
    print(json.dumps({'status':'PASS','zero_adapter_exact':True,'nonzero_up_gradient':True,
                     'paired_order':True,'exact_optimizer_resume':True,'feature_equal_mean_handcheck':True}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config');p.add_argument('--output');p.add_argument('--arm',choices=['R','F','N'])
    p.add_argument('--seed',type=int,default=42);p.add_argument('--device',default='cuda:0');p.add_argument('--resume')
    p.add_argument('--selftest',action='store_true');p.add_argument('--smoke',action='store_true');a=p.parse_args()
    if a.selftest:selftest()
    elif a.smoke:smoke(a)
    else:train(a)
