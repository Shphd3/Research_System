"""Native final-attention retention, cached frozen prefix, and dense controls.

Reuse: inspected A17 native answer-only CE, four-projection adapter restore,
fresh AdamW, exact recovery, and training observability contract. Adaptation:
cache only the frozen first 27 blocks, then execute native final attention/MLP.
No finite 576-coordinate bank is reused. TEST is never opened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import sys
import time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

OLD_SOURCE = Path('/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/source')
sys.path.insert(0, str(OLD_SOURCE))
from carriers import QwenCarrier

NAMES = [f'model.layers.27.self_attn.{q}_proj.weight' for q in ('q', 'k', 'v', 'o')]
ARMS_A = ('U', 'UL', 'US', 'TC', 'TS', 'RS', 'LS')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(8 << 20), b''):
            h.update(block)
    return h.hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n')
    tmp.replace(path)


def atomic_save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    torch.save(value, tmp)
    tmp.replace(path)


def cpu_tree(value):
    if isinstance(value, torch.Tensor): return value.detach().cpu().clone()
    if isinstance(value, dict): return {k: cpu_tree(v) for k, v in value.items()}
    if isinstance(value, tuple): return tuple(cpu_tree(v) for v in value)
    if isinstance(value, list): return [cpu_tree(v) for v in value]
    return value


def exact_tree(a, b):
    if isinstance(a, torch.Tensor): return isinstance(b, torch.Tensor) and torch.equal(a.cpu(), b.cpu())
    if isinstance(a, np.ndarray): return isinstance(b, np.ndarray) and np.array_equal(a, b)
    if isinstance(a, dict): return isinstance(b, dict) and a.keys() == b.keys() and all(exact_tree(a[k], b[k]) for k in a)
    if isinstance(a, (tuple, list)): return type(a) == type(b) and len(a) == len(b) and all(exact_tree(x, y) for x, y in zip(a, b))
    return a == b


def configure(seed, device):
    os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
    torch.set_num_threads(4)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if str(device).startswith('cuda'): torch.cuda.set_device(device)


def load_parent(cfg, device):
    """Exact official Base plus all FOUR acquired projection weights."""
    path = cfg['old_checkpoint_path']
    if sha(path) != cfg['old_checkpoint_sha256']: raise ValueError('acquired checkpoint hash')
    state = torch.load(path, map_location='cpu', weights_only=False)
    if state['optimizer_step'] != 1200 or state['tokens_seen'] != 24000: raise ValueError('acquired endpoint counters')
    if set(state['trainable_weights']) != set(NAMES): raise ValueError('four native projection adapter required')
    if state['parent_asset_id'] != cfg['parent_model_asset_id']: raise ValueError('adapter Base identity')
    carrier = QwenCarrier(cfg['model'], device)
    if state['base_disk_identity'] != carrier.parent_identity: raise ValueError('exact disk Base mismatch')
    named = dict(carrier.model.named_parameters())
    with torch.no_grad():
        for name in NAMES:
            w = state['trainable_weights'][name]
            if w.dtype != torch.float32 or w.shape != named[name].shape or not torch.isfinite(w).all(): raise ValueError(name)
            named[name].copy_(w.to(device))
    carrier.model.eval().requires_grad_(False)
    if frozen_hash(carrier.model, set(NAMES)) != state['frozen_sha256']: raise ValueError('acquired frozen Base bytes')
    return carrier


def load_data(cfg):
    root = Path(cfg['data'])
    if sha(root / 'manifest.json') != cfg['data_manifest_sha256']: raise ValueError('data manifest mismatch')
    output = {}
    for split in ('train', 'dev'):
        name = split + '.jsonl'
        if sha(root / name) != cfg['data_file_sha256'][name]: raise ValueError('data payload mismatch')
        all_rows = [json.loads(l) for l in (root / name).read_text().splitlines() if l]
        part = [r for r in all_rows if r['world'] in ('old', 'reversed')]
        if any(r['split'] != split for r in part): raise ValueError('split mismatch')
        if len({r['record_id'] for r in part}) != len(part): raise ValueError('duplicate records')
        if any(r['mode'] != (1 if r['world'] == 'old' else 2) for r in part): raise ValueError('world/mode mismatch')
        output[split] = part
    if {r['list_id'] for r in output['train']} & {r['list_id'] for r in output['dev']}: raise ValueError('list leakage')
    return output


def token_batch(records, device):
    lengths = torch.tensor([len(r['input_ids']) for r in records], device=device)
    x = torch.zeros(len(records), int(lengths.max()), device=device, dtype=torch.long)
    for i, r in enumerate(records): x[i, :lengths[i]] = torch.tensor(r['input_ids'], device=device)
    mask = torch.arange(x.shape[1], device=device)[None] < lengths[:, None]
    targets = torch.tensor([r['target_id'] for r in records], device=device)
    return x, mask, lengths, targets


class CachedAnswerLM(nn.Module):
    """Direct native final block. Frozen MLP still carries gradients to attention."""
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.layer = base.model.layers[27]
        self.modes = None

    def hidden(self, h, mask, lengths):
        pos = (mask.long().cumsum(-1) - 1).clamp_min(0)
        n = h.shape[1]
        allowed = torch.ones(n, n, dtype=torch.bool, device=h.device).tril()[None, None] & mask[:, None, None, :]
        attention_mask = torch.zeros(allowed.shape, device=h.device, dtype=h.dtype).masked_fill(~allowed, torch.finfo(h.dtype).min)
        rotary = self.base.model.rotary_emb(h, pos)
        out = self.layer(h, attention_mask=attention_mask, position_ids=pos,
                         cache_position=torch.arange(n, device=h.device),
                         position_embeddings=rotary, use_cache=False)
        out = out[0] if isinstance(out, tuple) else out
        return self.base.model.norm(out)

    def forward(self, h, mask, lengths, targets, modes=None):
        self.modes = modes
        z = self.hidden(h, mask, lengths)
        logits = self.base.lm_head(z[torch.arange(len(z), device=z.device), lengths - 1])
        losses = F.cross_entropy(logits.float(), targets, reduction='none')
        return losses.sum(), logits, losses


def cache_batch(cache, indices, device):
    lengths = cache['lengths'][indices].to(device)
    n = int(lengths.max())
    h = cache['hidden'][indices, :n].to(device)
    mask = torch.arange(n, device=device)[None] < lengths[:, None]
    records = [cache['records'][i] for i in indices]
    targets = torch.tensor([r['target_id'] for r in records], device=device)
    modes = torch.tensor([r['mode'] for r in records], device=device)
    return h, mask, lengths, targets, modes


def prepare(cfg, device, root):
    """Cache schema: records, hidden[N,Lmax,1024] FP32, lengths, identity, audit."""
    carrier = load_parent(cfg, device)
    base, model = carrier.model, CachedAnswerLM(carrier.model)
    data = load_data(cfg)
    cache_dir = Path(cfg.get('cache_dir', root / 'cache'))
    cache_dir.mkdir(parents=True, exist_ok=True)
    identity = {k: cfg[k] for k in ('model', 'old_checkpoint_sha256', 'data_manifest_sha256')}
    identity['base_disk_identity'] = carrier.parent_identity
    receipts = {}
    for split, records in data.items():
        target = cache_dir / (split + '.pt')
        if target.exists():
            old = torch.load(target, map_location='cpu', weights_only=False)
            if old['identity'] != identity or old['records'] != records: raise ValueError('stale cache identity')
            receipts[split] = {'path': str(target), 'sha256': sha(target), 'reused_verified': True, 'audit': old['audit']}
            continue
        lengths = torch.tensor([len(r['input_ids']) for r in records])
        hidden = torch.zeros(len(records), int(lengths.max()), base.config.hidden_size, dtype=torch.float32)
        captured = []
        def capture(module, args, kwargs): captured.append(args[0].detach())
        handle = base.model.layers[27].register_forward_pre_hook(capture, with_kwargs=True)
        errors, started = [], time.monotonic()
        try:
            with torch.no_grad():
                for start in range(0, len(records), cfg.get('cache_microbatch', 20)):
                    batch = records[start:start + cfg.get('cache_microbatch', 20)]
                    x, mask, lens, y = token_batch(batch, device)
                    captured.clear()
                    pos = (mask.long().cumsum(-1) - 1).clamp_min(0)
                    out = base.model(input_ids=x, attention_mask=mask, position_ids=pos, use_cache=False).last_hidden_state
                    native_logits = base.lm_head(out[torch.arange(len(x), device=device), lens - 1])
                    h = captured[0].clone()
                    # Remove hook recursion capture produced by direct final-block replay.
                    _, replay, _ = model(h, mask, lens, y)
                    err = float((native_logits - replay).abs().max())
                    if err > cfg.get('cache_logits_atol', 2e-4): raise ValueError(f'cache no-op logits maxabs {err}')
                    if not torch.equal(native_logits.argmax(-1), replay.argmax(-1)): raise ValueError('cache argmax changed')
                    errors.append(err)
                    hidden[start:start + len(batch), :h.shape[1]] = h.cpu()
                    if start == 0 or start % 400 == 0:
                        print(json.dumps({'event': 'cache_progress', 'split': split, 'records': start + len(batch), 'elapsed_seconds': time.monotonic() - started}), flush=True)
        finally: handle.remove()
        audit = {'native_vs_cached_logits_maxabs': max(errors), 'argmax_equal': True,
                 'comparison_count': len(records), 'elapsed_seconds': time.monotonic() - started,
                 'dtype': 'float32', 'frozen_prefix_blocks': 27, 'cache_hook': 'layers.27 input',
                 'scope': 'same-shape native final-block replay; batch-trim replay separately checked in worker'}
        atomic_save(target, {'records': records, 'hidden': hidden, 'lengths': lengths,
                             'identity': identity, 'audit': audit})
        receipts[split] = {'path': str(target), 'sha256': sha(target), 'audit': audit}
    write(root / 'cache_preparation.json', receipts)
    write(cache_dir / 'cache_receipt.json', receipts)
    return receipts


def load_cache(cfg, split):
    path = Path(cfg['cache_dir']) / (split + '.pt')
    receipt = json.loads((path.parent / 'cache_receipt.json').read_text())
    if sha(path) != receipt[split]['sha256']: raise ValueError('cached payload bytes changed')
    cache = torch.load(path, map_location='cpu', weights_only=False)
    for k in ('model', 'old_checkpoint_sha256', 'data_manifest_sha256'):
        if cache['identity'][k] != cfg[k]: raise ValueError('cache identity ' + k)
    if cache['hidden'].dtype != torch.float32 or not torch.isfinite(cache['hidden']).all(): raise ValueError('cache dtype/finite')
    return cache


class Projector:
    """Frobenius projection onto paired, orthonormal rank-one matrix atoms."""
    def __init__(self, u, v):
        self.u, self.v = u, v

    def coordinates(self, w):
        return (self.u * (w @ self.v)).sum(0)

    def synthesize(self, c):
        return (self.u * c[None]) @ self.v.T

    def __call__(self, w):
        return self.synthesize(self.coordinates(w))

    def state(self): return {'u': self.u.detach().cpu(), 'v': self.v.detach().cpu()}


def make_projector(w, rank, kind='top', seed=29):
    if rank > min(w.shape): raise ValueError('rank exceeds matrix shape')
    if kind == 'random':
        gen = torch.Generator(device='cpu').manual_seed(seed)
        u = torch.linalg.qr(torch.randn(w.shape[0], rank, dtype=torch.float64, generator=gen), mode='reduced')[0]
        v = torch.linalg.qr(torch.randn(w.shape[1], rank, dtype=torch.float64, generator=gen), mode='reduced')[0]
        return Projector(u.to(w), v.to(w)), {'selector': kind, 'rank': rank, 'seed': seed}
    u, s, vh = torch.linalg.svd(w.detach().double(), full_matrices=False)
    indices = slice(0, rank) if kind == 'top' else slice(-rank, None)
    boundary = rank if kind == 'top' else len(s) - rank
    gap = float((s[boundary - 1] - s[boundary]).abs() / s[0]) if 0 < boundary < len(s) else None
    # Deterministic numerical SVD order is retained even at a near tie; explicitly
    # mark unstable boundaries, never expand/reduce rank after observing behavior.
    meta = {'selector': kind, 'rank': rank, 'singular_values': s.cpu().tolist(),
            'relative_boundary_gap': gap, 'near_tie': gap is not None and gap < 1e-8,
            'tie_policy': 'retain deterministic library ordering, mark near ties as selector instability'}
    return Projector(u[:, indices].float(), vh[indices].T.float()), meta


def attenuation(cfg, step):
    n = cfg.get('full_updates', 1200)
    start, end = cfg.get('attenuation_start', .1), cfg.get('attenuation_end', .01)
    return end + (start - end) * (1 + math.cos(math.pi * min(step / n, 1))) / 2


def norm(values): return math.sqrt(sum(float(x.detach().double().square().sum()) for x in values))


def frozen_hash(model, excluded):
    h = hashlib.sha256()
    for name, p in model.named_parameters():
        name = name.replace('.original.weight', '.weight').replace('.original.bias', '.bias')
        if name in excluded or p.requires_grad: continue
        h.update(name.encode()); h.update(p.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


class ResidualProjection(nn.Module):
    """Shared candidate coefficients; native full complementary residuals.

    split-full matches per-mode available capacity but increases total capacity.
    row variants exactly match *effective* total degrees of freedom: constrain
    each row-half residual against restricted candidate atoms. The shared variant
    exposes both halves; split exposes one half per mode. This additional
    constraint is explicit and is not equivalent to the full complement family.
    """
    def __init__(self, original, projector, context, split=False, rows=False):
        super().__init__()
        self.original = original.requires_grad_(False)
        # Context is a non-owning reference; registering the parent Module here
        # would create a recursive module graph.
        object.__setattr__(self, 'context', context)
        self.split, self.rows = split, rows
        self.register_buffer('u', projector.u)
        self.register_buffer('v', projector.v)
        k = self.u.shape[1]
        self.common = nn.Parameter(torch.zeros(k, device=self.u.device))
        shape = tuple(original.weight.shape)
        self.residual = nn.Parameter(torch.zeros((2 if split and not rows else 1,) + shape, device=self.u.device))
        if rows:
            # Inverse Gram for the non-normalized atoms restricted to each half.
            inverses = []
            for lo, hi in self.row_slices():
                a = self.u[lo:hi].double()
                gram = (a.T @ a) * (self.v.double().T @ self.v.double())
                if int(torch.linalg.matrix_rank(gram)) != k: raise ValueError('row atom Gram rank failure')
                inverses.append(torch.linalg.inv(gram).float())
            self.register_buffer('row_gram_inverse', torch.stack(inverses))

    @property
    def weight(self): return self.original.weight

    @property
    def bias(self): return self.original.bias

    def row_slices(self):
        m = self.original.weight.shape[0]
        return ((0, m // 2), (m // 2, m))

    def project(self, w): return (self.u * (self.u * (w @ self.v)).sum(0)[None]) @ self.v.T

    def complement(self, mode):
        if not self.rows:
            w = self.residual[mode - 1 if self.split else 0]
            return w - self.project(w)
        w = self.residual[0]
        blocks = []
        for index, (lo, hi) in enumerate(self.row_slices()):
            block, u = w[lo:hi], self.u[lo:hi]
            c = self.row_gram_inverse[index] @ (u * (block @ self.v)).sum(0)
            block = block - (u * c[None]) @ self.v.T
            blocks.append(block if not self.split or mode == index + 1 else block * 0)
        return torch.cat(blocks)

    def effective(self, mode):
        return self.original.weight + (self.u * self.common[None]) @ self.v.T + self.complement(mode)

    def forward(self, h):
        if self.context.modes is None: raise ValueError('visible mode context required')
        if not self.split: return F.linear(h, self.effective(1), self.original.bias)
        out = torch.zeros(*h.shape[:-1], self.original.out_features, device=h.device, dtype=h.dtype)
        for mode in (1, 2):
            selected = self.context.modes == mode
            if selected.any(): out[selected] = F.linear(h[selected], self.effective(mode), self.original.bias)
        return out

    def effective_dof(self):
        n, k = self.original.weight.numel(), len(self.common)
        return n - k if self.rows else (2 * (n - k) + k if self.split else n)


def make_batches(cache, seed, count, joint):
    grouped = {1: {}, 2: {}}
    for i, r in enumerate(cache['records']):
        grouped[r['mode']].setdefault(r['list_id'], {})[r['command']] = i
    if grouped[1].keys() != grouped[2].keys(): raise ValueError('paired mode list mismatch')
    if any(set(d) != {'甲', '乙'} for g in grouped.values() for d in g.values()): raise ValueError('incomplete pairs')
    keys = sorted(grouped[1]); order = []; gen = random.Random(seed + 2000)
    per = 5 if joint else 10
    while len(order) < count * per:
        ep = list(keys); gen.shuffle(ep); order.extend(ep)
    out = []
    for start in range(0, count * per, per):
        window = order[start:start + per]
        out.append([grouped[m][key][cmd] for m in ((1, 2) if joint else (2,)) for key in window for cmd in ('甲', '乙')])
    if any(len(x) != 20 for x in out): raise ValueError('twenty valid answers required')
    return out


@torch.no_grad()
def evaluate(model, cache, cfg, device, indices=None):
    indices = list(range(len(cache['records']))) if indices is None else list(indices)
    output = []
    pool = torch.tensor(cfg['answer_ids'], device=device)
    for start in range(0, len(indices), cfg.get('eval_microbatch', 20)):
        ix = indices[start:start + cfg.get('eval_microbatch', 20)]
        _, logits, losses = model(*cache_batch(cache, ix, device))
        lp = logits.log_softmax(-1)
        top = logits.topk(2, dim=-1)
        for j, index in enumerate(ix):
            r = cache['records'][index]
            y = r['target_id']; pred = int(top.indices[j, 0])
            # Pair targets are first/last list words, whose registered token IDs
            # can be recovered without hidden labels from the answer vocabulary.
            wordmap = dict(zip(cfg['answer_words'], cfg['answer_ids']))
            pair = [wordmap[r['words'][0]], wordmap[r['words'][-1]]]
            p3 = torch.tensor([wordmap[w] for w in r['words']], device=device)
            pair_mass = torch.logsumexp(lp[j, pair], 0)
            list_mass = torch.logsumexp(lp[j, p3], 0)
            pool_mass = torch.logsumexp(lp[j, pool], 0)
            other = pair[1] if y == pair[0] else pair[0]
            full_other = top.values[j, 1] if pred == y else top.values[j, 0]
            output.append({**{k: r[k] for k in ('record_id', 'list_id', 'split', 'panel', 'world', 'mode', 'command')},
                **{k: r[k] for k in ('unordered_group_id', 'orbit_id') if k in r},
                'target_id': y, 'prediction_id': pred, 'correct': float(pred == y),
                'ce': float(losses[j]), 'gold_log_probability': float(lp[j, y]),
                'gold_pair_margin': float(logits[j, y] - logits[j, other]),
                'full_margin': float(logits[j, y] - full_other),
                'pair_mass': float(pair_mass.exp()), 'pair_selection_ce': float(-lp[j, y] + pair_mass),
                'list3_mass': float(list_mass.exp()), 'list3_conditional_ce': float(-lp[j, y] + list_mass),
                'pool20_mass': float(pool_mass.exp()), 'pool20_conditional_ce': float(-lp[j, y] + pool_mass)})
    aggregates = {}
    for mode in (1, 2):
        for panel in sorted({r['panel'] for r in output}) + ['combined']:
            for command in ('甲', '乙', 'both'):
                part = [r for r in output if r['mode'] == mode and (panel == 'combined' or r['panel'] == panel) and (command == 'both' or r['command'] == command)]
                if part:
                    aggregates[f'mode{mode}/{command}/{panel}'] = {'n': len(part), **{k: float(np.mean([r[k] for r in part])) for k in ('correct', 'ce', 'gold_pair_margin', 'full_margin', 'pair_mass', 'pair_selection_ce', 'list3_mass', 'list3_conditional_ce', 'pool20_mass', 'pool20_conditional_ce')}}
    cells = {k: v['correct'] for k, v in aggregates.items() if '/both/' not in k and not k.endswith('/combined')}
    return {'records': output, 'aggregates': aggregates, 'qualification_cells': cells,
            'qualified_both': all(x >= cfg.get('qualification_accuracy', .95) for x in cells.values()),
            'scope': 'exposed DEV, full vocabulary argmax, answer-only one target per example'}


def rng_state(device):
    result = {'python': random.getstate(), 'numpy': np.random.get_state(), 'cpu': torch.get_rng_state()}
    if str(device).startswith('cuda'): result['cuda'] = torch.cuda.get_rng_state(device)
    return cpu_tree(result)


def restore_rng(state, device):
    random.setstate(state['python']); np.random.set_state(state['numpy']); torch.set_rng_state(state['cpu'])
    if 'cuda' in state: torch.cuda.set_rng_state(state['cuda'], device)


def verify_telemetry(root, expected_steps):
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
    acc = EventAccumulator(str(root / 'tensorboard'), size_guidance={'scalars': 0}); acc.Reload()
    token_tags = ('tokens/train_lm_loss', 'tokens/train_total_loss', 'progress/optimizer_step')
    update_tags = ('updates/train_lm_loss', 'updates/learning_rate', 'progress/tokens_seen', 'progress/effective_tokens_per_update')
    for tag in token_tags + update_tags:
        values = acc.Scalars(tag)
        expected = [20 * x if tag in token_tags else x for x in expected_steps]
        if [v.step for v in values] != expected or any(not math.isfinite(v.value) for v in values): raise ValueError('telemetry ' + tag)
    write(root / 'telemetry_verification.json', {'status': 'PASS', 'optimizer_steps': expected_steps, 'valid_answers': 20 * max(expected_steps), 'required_tags': token_tags + update_tags})


def run(cfg, root, stage, arm, seed, device, steps=None, resume=None):
    """Independent single-GPU lane. No DDP replication or exposure multiplication."""
    from torch.utils.tensorboard import SummaryWriter
    started = time.monotonic()
    microbatch = cfg.get('microbatch', cfg.get('objective', {}).get('microbatch', 5))
    if 20 % microbatch: raise ValueError('microbatch must divide the registered twenty-answer window')
    steps = cfg.get('full_updates', 1200) if steps is None else steps
    if stage == 'resume_verify':
        return verify_resume(cfg, root, seed, device, arm, resume)
    if stage == 'interference': return interference(cfg, root, seed, device)
    if stage == 'functional': return functional(cfg, root, seed, device, resume)
    stage = '0' if stage == 'zero' else stage
    if stage not in ('0', 'A', 'B', 'C'): raise ValueError('stage must be 0/A/B/C')
    if str(device).startswith('cuda'): torch.cuda.reset_peak_memory_stats(device)
    if stage == 'A' and arm not in ARMS_A: raise ValueError('unregistered A arm')
    if stage == 'C' and arm not in ('fixed', 'sham', 'dynamic'): raise ValueError('unregistered C arm')
    joint = stage in ('0', 'B')
    train, dev = load_cache(cfg, 'train'), load_cache(cfg, 'dev')
    carrier = load_parent(cfg, device); base = carrier.model
    write(root / f'environment_{stage}_{arm}_{seed}.json', {'torch': torch.__version__,
        'cuda_runtime': torch.version.cuda, 'device': str(device),
        'gpu': torch.cuda.get_device_name(device) if str(device).startswith('cuda') else 'CPU',
        'gpu_total_memory_bytes': torch.cuda.get_device_properties(device).total_memory if str(device).startswith('cuda') else 0,
        'dtype': 'float32', 'deterministic_algorithms': torch.are_deterministic_algorithms_enabled(),
        'matmul_allow_tf32': torch.backends.cuda.matmul.allow_tf32, 'cudnn_allow_tf32': torch.backends.cudnn.allow_tf32,
        'native_attention': 'sdpa', 'independent_lane_not_DDP': True,
        'resource_profile': os.environ.get('RESOURCE_PROFILE'), 'image_url': os.environ.get('IMAGE_URL'),
        'source_sha256': sha(__file__), 'config_sha256': cfg['_hash']})
    model = CachedAnswerLM(base)
    native = {name: dict(base.named_parameters())[name] for name in NAMES}
    before_native = {name: p.detach().clone() for name, p in native.items()}
    frozen_initial = frozen_hash(base, set(NAMES))
    saved_old = torch.load(cfg['old_checkpoint_path'], map_location='cpu', weights_only=False)
    if frozen_initial != saved_old['frozen_sha256']: raise ValueError('frozen Base bytes differ from acquired checkpoint')
    del saved_old
    frozen = [(n, p, p._version) for n, p in base.named_parameters() if n not in NAMES]
    def check_frozen():
        if any(p._version != version for _, p, version in frozen): raise ValueError('frozen tensor version drift')
    projs, metadata = {}, {}
    rank = cfg.get('rank', 16)
    kind = {'RS': 'random', 'LS': 'tail'}.get(arm, 'top')
    for index, (name, p) in enumerate(native.items()):
        projs[name], metadata[name] = make_projector(p, rank, kind, seed + index * 100)
    case = root / stage / f'seed_{seed}' / arm
    case.mkdir(parents=True, exist_ok=True)
    if (case / 'completion.json').exists() and not resume: raise ValueError('completed case exists; explicit resume required')
    atomic_save(case / 'basis_initial.pt', {n: p.state() for n, p in projs.items()})
    write(case / 'basis_metadata.json', metadata)
    modules = {}
    audit_ix = batches_probe = make_batches(train, seed, 1, joint)[0][:microbatch]
    with torch.no_grad():
        original_logits = model(*cache_batch(train, audit_ix, device))[1].detach().clone()
    if stage == 'B' and arm != 'Full':
        split = arm in ('DN', 'DP', 'RN', 'RP')
        rows = arm in ('RN', 'RP', 'SRN', 'SRP')
        if arm not in ('SN', 'SP', 'DN', 'DP', 'RN', 'RP', 'SRN', 'SRP'): raise ValueError('B arm')
        for name in NAMES:
            short = name.split('.')[-2]
            old = getattr(model.layer.self_attn, short)
            module = ResidualProjection(old, projs[name], model, split, rows)
            setattr(model.layer.self_attn, short, module); modules[name] = module
        params = [p for module in modules.values() for p in (module.common, module.residual)]
        parameter_names = [f'{n}.{suffix}' for n in NAMES for suffix in ('common', 'residual')]
        effective_dof = sum(m.effective_dof() for m in modules.values())
    else:
        params = list(native.values()); parameter_names = list(native)
        for p in params: p.requires_grad_(True)
        effective_dof = sum(p.numel() for p in params)
    with torch.no_grad():
        installed_logits = model(*cache_batch(train, audit_ix, device))[1].detach()
        installation_error = float((installed_logits - original_logits).abs().max())
        if installation_error > cfg.get('cache_logits_atol', 2e-4) or not torch.equal(installed_logits.argmax(-1), original_logits.argmax(-1)):
            raise ValueError('zero-increment parameterization function changed')
        write(case / 'installation_noop.json', {'logits_maxabs': installation_error, 'argmax_equal': True})
    batches = make_batches(train, seed, max(steps, cfg.get('full_updates', 1200)), joint)
    ac = cfg['optimizer']
    if ac.get('weight_decay', 0) != 0: raise ValueError('only zero weight decay')
    opt = torch.optim.AdamW(params, lr=ac['lr'], betas=tuple(ac['betas']), eps=ac['eps'], weight_decay=0, foreach=False, fused=False)
    def opt_new():
        return torch.optim.AdamW(params, lr=ac['lr'], betas=tuple(ac['betas']), eps=ac['eps'], weight_decay=0, foreach=False, fused=False)
    write(case / 'scope.json', {'stage': stage, 'arm': arm, 'seed': seed,
        'trainable_parameter_names': parameter_names, 'stored_trainable_parameters': sum(p.numel() for p in params),
        'effective_degrees_of_freedom': effective_dof, 'frozen_sha256': frozen_initial,
        'counter_scope': 'completed answer prediction tokens only, excludes common old acquisition',
        'old_optimizer_moments_carried': False, 'batch': 20, 'joint': joint,
        'capacity_boundary': 'DN/DP increase total DOF; RN/RP vs SRN/SRP match total effective DOF with changed per-mode row space',
        'B_optimizer_boundary': 'Adam on shared candidate coefficients and raw projected residual coordinates; not identical to A dense Adam'})
    write(case / 'frozen_order.json', {'batch_record_ids': [[train['records'][i]['record_id'] for i in b] for b in batches]})

    def snapshot(step, metric=None):
        return {'trainable_weights': {n: cpu_tree(p) for n, p in zip(parameter_names, params)},
                'optimizer': cpu_tree(opt.state_dict()), 'optimizer_step': step, 'tokens_seen': 20 * step,
                'data_cursor': step, 'rng': rng_state(device), 'seed': seed, 'arm': arm, 'stage': stage,
                'projectors': {n: p.state() for n, p in projs.items()}, 'config_sha256': cfg['_hash'],
                'old_checkpoint_sha256': cfg['old_checkpoint_sha256'], 'frozen_sha256': frozen_initial,
                'batch_order': batches, 'metric': metric, 'reselection_events': reselection_events,
                'scheduler': {'kind': 'candidate_cosine', 'before_update_step': step, 'total_steps': cfg.get('full_updates', 1200)},
                'effective_degrees_of_freedom': effective_dof, 'trainable_parameter_names': parameter_names,
                'full_base_saved': False, 'requires_exact_registered_Base_and_acquired_adapter': True}

    def save(step, metric=None):
        path = case / 'checkpoints' / f'update_{step:05d}' / 'state.pt'
        atomic_save(path, snapshot(step, metric))
        write(path.parent / 'manifest.json', {'complete': True, 'sha256': sha(path), 'bytes': path.stat().st_size,
              'optimizer_step': step, 'tokens_seen': step * 20, 'stage': stage, 'arm': arm, 'seed': seed,
              'old_checkpoint_sha256': cfg['old_checkpoint_sha256'], 'full_base_saved': False})

    def update(step):
        batch = batches[step]
        opt.zero_grad(set_to_none=True)
        loss_sum = 0.
        for start in range(0, 20, microbatch):
            ix = batch[start:start + microbatch]
            total, _, _ = model(*cache_batch(train, ix, device))
            (total / 20).backward(); loss_sum += float(total.detach())
        if any(p.grad is None or not torch.isfinite(p.grad).all() for p in params): raise ValueError('missing/nonfinite gradient')
        raw_norm = norm([p.grad for p in params])
        torch.nn.utils.clip_grad_norm_(params, cfg.get('clip', 1.), foreach=False)
        clipped = norm([p.grad for p in params])
        old = [p.detach().clone() for p in params]
        effective_before = {}
        if modules:
            with torch.no_grad():
                for name, module in modules.items():
                    for mode in ((1, 2) if module.split else (1,)):
                        effective_before[(name, mode)] = module.effective(mode).detach().clone()
        opt.step()
        a = attenuation(cfg, step)
        if stage == 'A':
            a = 1. if arm == 'U' else .1 if arm in ('UL', 'TC') else a
        elif stage in ('0', 'B'):
            a = a if arm in ('SP', 'DP', 'RP', 'SRP') else 1.
        desired, roundoff, projected, remaining, cand_norm = [], [], [], [], []
        with torch.no_grad():
            if modules:
                effective_candidate = {key: modules[key[0]].effective(key[1]).detach() - old_w
                                       for key, old_w in effective_before.items()}
                for index, (name, module) in enumerate(modules.items()):
                    ci, ri = index * 2, index * 2 + 1
                    d = params[ci] - old[ci]
                    params[ci].copy_(old[ci] + a * d)
                    cand_norm.extend((d, params[ri] - old[ri]))
                # Report realized effective matrix displacements, since raw
                # residual coordinates contain redundant/null directions.
                effective_actual = {key: modules[key[0]].effective(key[1]).detach() - old_w
                                    for key, old_w in effective_before.items()}
                projected = [projs[name](d) for (name, mode), d in effective_actual.items()]
                remaining = [d - projs[name](d) for (name, mode), d in effective_actual.items()]
            else:
                for index, (name, p) in enumerate(native.items()):
                    d = p - old[index]; pd = projs[name](d)
                    filtered = a * d if stage == 'A' and arm in ('UL', 'US') else d + (a - 1) * pd
                    # Correct actual Adam displacement filtering: moments were
                    # advanced once above, and only the candidate displacement
                    # is filtered. No gradient attenuation is substituted.
                    p.copy_(old[index] + filtered)
                    realized = p - old[index]
                    desired.append(filtered); roundoff.append(realized - filtered)
                    projected.append(projs[name](realized)); remaining.append(realized - projs[name](realized)); cand_norm.append(d)
        actual = [p - q for p, q in zip(params, old)]
        if not math.isfinite(loss_sum) or any(not torch.isfinite(p).all() for p in params): raise ValueError('nonfinite model/update')
        check_frozen()
        rows = [train['records'][i] for i in batch]
        if modules and {r['mode'] for r in rows} != {1, 2}: raise ValueError('B requires both modes active every completed optimizer window; idle-moment semantics not qualified')
        return {'loss': loss_sum / 20, 'total_loss': loss_sum / 20, 'attenuation': a,
                'raw_gradient_norm': raw_norm, 'clipped_gradient_norm': clipped,
                'candidate_step_norm': norm(list(effective_candidate.values())) if modules else norm(cand_norm),
                'actual_step_norm': norm(list(effective_actual.values())) if modules else norm(actual),
                'coordinate_step_norm': norm(actual),
                'per_mode_effective_step_norm': {f'{n}/mode{m}': norm([d]) for (n, m), d in effective_actual.items()} if modules else {},
                'projected_step_norm': norm(projected), 'complement_step_norm': norm(remaining),
                'rounding_error_norm': norm(roundoff), 'valid_answers': 20,
                'old_valid_answers': sum(r['mode'] == 1 for r in rows), 'new_valid_answers': sum(r['mode'] == 2 for r in rows),
                'input_tokens': sum(len(r['input_ids']) for r in rows), 'batch_record_ids': [r['record_id'] for r in rows]}

    reselection_events = []
    first = 0
    if resume:
        state = torch.load(resume, map_location='cpu', weights_only=False)
        for name, value in [('config_sha256', cfg['_hash']), ('stage', stage), ('arm', arm), ('seed', seed), ('frozen_sha256', frozen_initial)]:
            if state[name] != value: raise ValueError('resume identity ' + name)
        with torch.no_grad():
            for name, p in zip(parameter_names, params): p.copy_(state['trainable_weights'][name].to(device))
        for n, p in state['projectors'].items(): projs[n] = Projector(p['u'].to(device), p['v'].to(device))
        opt.load_state_dict(state['optimizer']); restore_rng(state['rng'], device)
        first = state['optimizer_step']; reselection_events = state['reselection_events']
        if state['tokens_seen'] != 20 * first or state['data_cursor'] != first or state['batch_order'] != batches: raise ValueError('resume counter/order mismatch')
    else:
        baseline = evaluate(model, dev, cfg, device)
        write(case / 'eval_00000.json', baseline)
        save(0)
    # Native vs cache check with the SAME actual microbatch shape used in training.
    if not modules and not resume:
        audit_ix = batches[0][:microbatch]
        native_rows = [train['records'][i] for i in audit_ix]
        with torch.no_grad():
            x, mask, lens, y = token_batch(native_rows, device)
            pos = (mask.long().cumsum(-1) - 1).clamp_min(0)
            h = base.model(input_ids=x, attention_mask=mask, position_ids=pos, use_cache=False).last_hidden_state
            real = base.lm_head(h[torch.arange(len(h), device=device), lens - 1])
            _, cached, _ = model(*cache_batch(train, audit_ix, device))
            error = float((real - cached).abs().max())
            if error > cfg.get('cache_logits_atol', 2e-4) or not torch.equal(real.argmax(-1), cached.argmax(-1)): raise ValueError('training-shape cache replay error')
            write(case / 'cache_training_shape_audit.json', {'maxabs': error, 'argmax_equal': True, 'microbatch': len(audit_ix)})
    writer = SummaryWriter(str(case / 'tensorboard' if first == 0 else case / f'tensorboard_resume_{first:05d}'))
    milestones = {1, steps} | set(cfg.get('milestones', [16, 50, 120, 240, 600, 1200]))
    update_seconds = []
    for step in range(first, steps):
        if stage == 'C' and step in cfg.get('reselect_steps', [400, 800]):
            probe = batches[step][:5]
            old_eval = model(*cache_batch(train, probe, device))[1].detach()
            before_weights = [p.detach().clone() for p in params]
            event = {'before_step': step, 'rule': 'top singular atoms of current TRAIN-fitted weights', 'uses_dev_labels': False, 'arm': arm}
            selection_started = time.monotonic()
            proposed = {n: make_projector(p, rank, 'top', seed)[0] for n, p in native.items()}
            event['selector_compute_seconds'] = time.monotonic() - selection_started
            event['same_svd_computation_all_C_arms'] = True
            if arm == 'dynamic': projs = proposed
            if arm in ('dynamic', 'sham'): opt = opt_new(); event['optimizer_reset'] = True
            else: event['optimizer_reset'] = False
            new_eval = model(*cache_batch(train, probe, device))[1].detach()
            event['weight_bytes_equal'] = all(torch.equal(p, q) for p, q in zip(params, before_weights))
            event['logits_maxabs'] = float((old_eval - new_eval).abs().max())
            if not event['weight_bytes_equal'] or event['logits_maxabs'] != 0: raise ValueError('reselection changes immediate function')
            reselection_events.append(event); write(case / 'reselection_events.json', reselection_events)
        tick = time.monotonic(); metric = update(step); seconds = time.monotonic() - tick
        update_seconds.append(seconds)
        completed = step + 1
        metric.update(optimizer_step=completed, step=completed, tokens_seen=20 * completed,
                      learning_rate=ac['lr'], seed=seed, arm=arm, stage=stage,
                      update_compute_seconds=seconds, cumulative_old_answers=(10 * completed if joint else 0),
                      cumulative_new_answers=(10 if joint else 20) * completed)
        with (case / 'metrics.jsonl').open('a') as f: f.write(json.dumps(metric, ensure_ascii=False) + '\n')
        values = [('tokens/train_lm_loss', metric['loss'], 20 * completed), ('updates/train_lm_loss', metric['loss'], completed),
                  ('tokens/train_total_loss', metric['total_loss'], 20 * completed), ('updates/learning_rate', ac['lr'], completed),
                  ('progress/tokens_seen', 20 * completed, completed), ('progress/optimizer_step', completed, 20 * completed),
                  ('progress/effective_tokens_per_update', 20, completed)]
        for name in ('attenuation', 'projected_step_norm', 'complement_step_norm', 'candidate_step_norm', 'actual_step_norm', 'rounding_error_norm'):
            values.append(('updates/' + name, metric[name], completed))
        for tag, value, coordinate in values: writer.add_scalar(tag, value, coordinate)
        writer.flush()
        if completed in milestones:
            save(completed, metric)
            write(case / f'eval_{completed:05d}.json', evaluate(model, dev, cfg, device))
        if completed == 2: atomic_save(case / 'external_reference.pt', snapshot(2, metric))
        if completed == 1 or completed % 50 == 0 or completed == steps:
            print(json.dumps({'stage': stage, 'arm': arm, 'seed': seed, 'step': completed, 'loss': metric['loss'], 'seconds': seconds, 'elapsed_seconds': time.monotonic() - started}), flush=True)
    writer.close()
    if first == 0: verify_telemetry(case, list(range(1, steps + 1)))
    check_frozen()
    if frozen_hash(base, set(NAMES)) != frozen_initial:
        raise ValueError('frozen bytes changed')
    write(case / 'completion.json', {'status': 'PASS', 'stage': stage, 'arm': arm, 'seed': seed, 'updates': steps,
        'tokens_seen': steps * 20, 'old_answers': steps * 10 if joint else 0, 'new_answers': steps * (10 if joint else 20),
        'elapsed_seconds': time.monotonic() - started, 'frozen_sha256': frozen_initial, 'effective_degrees_of_freedom': effective_dof,
        'checkpoint_saved': str(case / 'checkpoints' / f'update_{steps:05d}' / 'state.pt'),
        'gpu_peak_allocated_bytes': torch.cuda.max_memory_allocated(device) if str(device).startswith('cuda') else 0,
        'gpu_peak_reserved_bytes': torch.cuda.max_memory_reserved(device) if str(device).startswith('cuda') else 0,
        'update_compute_seconds': {'count': len(update_seconds), 'sum': sum(update_seconds),
            'mean': float(np.mean(update_seconds)) if update_seconds else None,
            'median': float(np.median(update_seconds)) if update_seconds else None,
            'p90': float(np.quantile(update_seconds, .9)) if update_seconds else None,
            'first': update_seconds[0] if update_seconds else None},
        'engineering_pass_not_scientific_support': True})


def verify_resume(cfg, root, seed, device, arm, checkpoint=None):
    """Call in a new process after a two-update smoke, replay update 2 exactly."""
    if checkpoint:
        case = Path(checkpoint).resolve().parents[2]
        saved = torch.load(checkpoint, map_location='cpu', weights_only=False)
        seed, arm = saved['seed'], saved['arm']
        if saved['optimizer_step'] != 1: raise ValueError('external verifier expects update1 checkpoint')
    else:
        candidates = [root / stage / f'seed_{seed}' / arm for stage in ('0', 'A', 'B', 'C')]
        cases = [c for c in candidates if (c / 'external_reference.pt').exists()]
        if len(cases) != 1: raise ValueError('resume needs exactly one stage case for this arm at this root')
        case = cases[0]
    reference = torch.load(case / 'external_reference.pt', map_location='cpu', weights_only=False)
    stage = reference['stage']
    replay_root = root / 'external_process_replay'
    run(cfg, replay_root, stage, arm, seed, device, 2, checkpoint or str(case / 'checkpoints/update_00001/state.pt'))
    replay = torch.load(replay_root / stage / f'seed_{seed}' / arm / 'external_reference.pt', map_location='cpu', weights_only=False)
    fields = ('trainable_weights', 'optimizer', 'rng', 'optimizer_step', 'tokens_seen', 'data_cursor', 'batch_order', 'projectors')
    matches = {field: exact_tree(reference[field], replay[field]) for field in fields}
    ignored = {'update_compute_seconds'}
    matches['deterministic_metrics'] = exact_tree({k: v for k, v in reference['metric'].items() if k not in ignored},
                                                {k: v for k, v in replay['metric'].items() if k not in ignored})
    receipt = {'status': 'PASS' if all(matches.values()) else 'FAIL', 'matches': matches,
               'external_process': True, 'loaded_step': 1, 'next_step': 2,
               'wall_time_excluded_from_exact_comparison': True}
    write(root / f'resume_verification_{stage}_{arm}_{seed}.json', receipt)
    if not all(matches.values()): raise ValueError('external resume exactness failure: ' + str(matches))


def interference(cfg, root, seed, device):
    """One actual finite matched-norm Adam displacement, both mode directions.

    This intervention is local and conditional on a shared acquired-old state;
    it cannot identify the sole cause of a 1200-update training trajectory.
    """
    carrier = load_parent(cfg, device); model = CachedAnswerLM(carrier.model)
    train, dev = load_cache(cfg, 'train'), load_cache(cfg, 'dev')
    params = [dict(carrier.model.named_parameters())[name] for name in NAMES]
    for p in params: p.requires_grad_(True)
    initial = [p.detach().clone() for p in params]
    projectors = [make_projector(p, cfg.get('rank', 16), 'top', seed)[0] for p in params]
    baselines = evaluate(model, dev, cfg, device)
    write(root / 'interference' / 'baseline.json', baselines)
    ac = cfg['optimizer']; receipts = []
    # Same first ten underlying lists across source modes, complete command pairs.
    keys = sorted({r['list_id'] for r in train['records']})[:10]
    for mode in (1, 2):
        ix = [i for i, r in enumerate(train['records']) if r['mode'] == mode and r['list_id'] in keys]
        if len(ix) != 20: raise ValueError('local diagnostic needs twenty paired answers')
        with torch.no_grad():
            for p, old in zip(params, initial): p.copy_(old)
        opt = torch.optim.AdamW(params, lr=ac['lr'], betas=tuple(ac['betas']), eps=ac['eps'], weight_decay=0, foreach=False, fused=False)
        opt.zero_grad(set_to_none=True)
        for start in range(0, 20, 5): (model(*cache_batch(train, ix[start:start + 5], device))[0] / 20).backward()
        torch.nn.utils.clip_grad_norm_(params, cfg.get('clip', 1.), foreach=False); opt.step()
        candidate = [p.detach().clone() - old for p, old in zip(params, initial)]
        target_norm = norm(candidate)
        for component in ('full', 'candidate', 'complement', 'random'):
            if component == 'full': delta = candidate
            elif component == 'candidate': delta = [proj(d) for proj, d in zip(projectors, candidate)]
            elif component == 'complement': delta = [d - proj(d) for proj, d in zip(projectors, candidate)]
            else:
                gen = torch.Generator(device='cpu').manual_seed(seed + mode)
                delta = [torch.randn(d.shape, generator=gen).to(d) for d in candidate]
            raw_norm = norm(delta)
            scale = target_norm / max(raw_norm, 1e-30)
            with torch.no_grad():
                for p, old, d in zip(params, initial, delta): p.copy_(old + d * scale)
            actual_norm = norm([p - old for p, old in zip(params, initial)])
            readout = evaluate(model, dev, cfg, device)
            write(root / 'interference' / f'mode{mode}_{component}.json', readout)
            changes = {}
            for target in (1, 2):
                key = f'mode{target}/both/combined'
                changes[f'mode{target}_ce_change'] = readout['aggregates'][key]['ce'] - baselines['aggregates'][key]['ce']
                changes[f'mode{target}_accuracy_change'] = readout['aggregates'][key]['correct'] - baselines['aggregates'][key]['correct']
            receipts.append({'source_mode': mode, 'component': component, 'source_train_answers': 20,
                'candidate_unscaled_norm': raw_norm, 'target_update_norm': target_norm, 'actual_update_norm': actual_norm,
                'amplitude_scale': scale, **changes})
    write(root / 'interference' / 'summary.json', {'records': receipts,
        'boundary': 'finite local intervention with matched actual parameter norm, not a global trajectory mechanism proof'})


def functional(cfg, root, seed, device, checkpoint):
    """Frozen endpoint C/R restoration with bidirectional and random controls."""
    if not checkpoint: raise ValueError('functional requires --resume exact endpoint state.pt')
    state = torch.load(checkpoint, map_location='cpu', weights_only=False)
    if state['old_checkpoint_sha256'] != cfg['old_checkpoint_sha256'] or set(state['trainable_weights']) != set(NAMES):
        raise ValueError('functional needs matching dense four-matrix state')
    carrier = load_parent(cfg, device); model = CachedAnswerLM(carrier.model)
    params = [dict(carrier.model.named_parameters())[n] for n in NAMES]
    initial = [p.detach().clone() for p in params]
    endpoint = [state['trainable_weights'][n].to(device) for n in NAMES]
    projs = [Projector(state['projectors'][n]['u'].to(device), state['projectors'][n]['v'].to(device)) for n in NAMES]
    dev = load_cache(cfg, 'dev')
    output = root / 'functional' / f"{state['stage']}_{state['arm']}_{seed}"
    output.mkdir(parents=True, exist_ok=True)
    cdelta = [p(w - w0) for p, w, w0 in zip(projs, endpoint, initial)]
    rdelta = [w - w0 - dc for w, w0, dc in zip(endpoint, initial, cdelta)]
    baseline = None; receipts = []
    for kind in ('endpoint', 'restore_C', 'amplify_C', 'restore_R', 'amplify_R', 'random_C', 'random_R'):
        if kind == 'endpoint': delta = [torch.zeros_like(w) for w in endpoint]
        elif kind.endswith('_C'): delta = cdelta
        else: delta = rdelta
        multiplier = -1. if kind.startswith('restore') else 1.
        if kind.startswith('random'):
            gen = torch.Generator(device='cpu').manual_seed(seed + (1 if kind.endswith('_C') else 2))
            raw = [torch.randn(d.shape, generator=gen).to(d) for d in delta]
            scale = norm(delta) / max(norm(raw), 1e-30)
            delta = [d * scale for d in raw]
        with torch.no_grad():
            for p, w, d in zip(params, endpoint, delta): p.copy_(w + multiplier * d)
        actual_norm = norm([p - w for p, w in zip(params, endpoint)])
        ev = evaluate(model, dev, cfg, device); write(output / (kind + '.json'), ev)
        if baseline is None: baseline = ev
        row = {'intervention': kind, 'actual_perturbation_norm': actual_norm}
        for mode in (1, 2):
            key = f'mode{mode}/both/combined'
            row[f'mode{mode}_accuracy'] = ev['aggregates'][key]['correct']
            row[f'mode{mode}_ce_change'] = ev['aggregates'][key]['ce'] - baseline['aggregates'][key]['ce']
        receipts.append(row)
    write(output / 'summary.json', {'checkpoint': checkpoint, 'checkpoint_sha256': sha(checkpoint), 'records': receipts,
          'boundary': 'off-trajectory conditional restoration/amplification sensitivity, not unique mediation or shared semantics'})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--arm', default='U')
    parser.add_argument('--seed', type=int, default=29)
    parser.add_argument('--device', default='cuda:0')
    parser.add_argument('--steps', type=int)
    parser.add_argument('--resume')
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    cfg['_hash'] = sha(args.config)
    configure(args.seed, args.device)
    root = Path(args.run)
    root.mkdir(parents=True, exist_ok=True)
    if args.stage == 'prepare': prepare(cfg, args.device, root)
    else: run(cfg, root, args.stage, args.arm, args.seed, args.device, args.steps, args.resume)


if __name__ == '__main__': main()
