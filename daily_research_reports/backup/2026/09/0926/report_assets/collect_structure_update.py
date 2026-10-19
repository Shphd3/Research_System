"""Bounded, exploratory native-structure and same-panel virtual-update readout.

No optimizer, training trajectory, checkpoint write, or confirmation unsealing.
All four sources and both prespecified step sizes are reported.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '4')
import sys, json, hashlib, time, datetime
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F

ROOT = Path('/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge')
PRIOR = Path('/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation')
LOADER = Path('/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/scripts')
ASSETS = Path('/data/250010109/MoE_Router/experiments/20260923_sae_n8_21b_four_model_audit/manifests/resolved_assets.json')
sys.path.insert(0, str(LOADER))
from smoke_sites import load_model, make_batch, forward_with_capture, sample_state

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(16 << 20), b''): h.update(b)
    return h.hexdigest()

def write(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    if (ROOT / 'complete.json').exists(): raise RuntimeError('Completed output already exists')
    start = time.monotonic()
    rows = [json.loads(l) for l in (PRIOR / 'selected.jsonl').open()]
    entry = json.loads(ASSETS.read_text())['models']['21b_s7_fresh']
    domains = ['computer_science', 'mathematics', 'physics', 'biology']
    # 16 prediction positions, all with a next token inside each 256-token record.
    positions = np.arange(14, 255, 16)
    assert len(positions) == 16 and positions[-1] == 254
    assert len(rows) == 1024 and len({r['input_ids_sha256'] for r in rows}) == 1024
    contract = dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status='EXPLORATORY_SCOPE_FIXED_BEFORE_READOUT',
        authorization='User requested advisor figures and completion/analysis of the reasoning chain, without another approval; bounded local diagnostic only.',
        parent_sources=['Projects/from-attention-to-search/main/experiments/shared_updates/sae_domain_activation/20260925/summary.md',
                        'Projects/from-attention-to-search/main/problem_anchors/shared_updates/human_semantic_updates/anchor_cn.md'],
        checkpoint=entry['checkpoint'], checkpoint_sha256=entry['checkpoint_state_sha256_manifest_claim'],
        source_selected=str(PRIOR/'selected.jsonl'), selected_sha256=sha(PRIOR/'selected.jsonl'),
        domains=domains, records=1024, records_per_domain_per_split=128,
        structure=dict(layer_code_index=7, objects=['attention_output_after_o_before_residual', 'down_projection_input'],
                       primary_pool='mean_of_all_256_body_positions', sensitivity_pool='last_body_position',
                       axes='one pooled, domain-balanced fit-only centered PCA per object/pool; test never chooses axes',
                       energy='centered variance spectrum and uncentered second-moment energy separately'),
        diagnostic=dict(object='final down full weight, functional additive delta; all other weights frozen',
                        loss='next-token cross entropy over 16 fixed positions per record; natural text, no answer prompt',
                        positions=positions.tolist(), source='128 fit records per domain', readout='128 test records per domain',
                        update='delta=-rho*FrobeniusNorm(W)*G/FrobeniusNorm(G)', rho=[1e-4, 5e-5],
                        numeric_path='frozen BF16 upstream; FP32 down, residual, final norm and output head; TF32 disabled',
                        control='exact zero delta and repeated baseline; independent delta reset, no optimizer/momentum',
                        quantity='help = baseline loss - updated loss, nats/predicted token; positive helps',
                        uncertainty='2000 paired record bootstrap, stratified by subfield, conditional on fixed fit gradient; descriptive marginal intervals',
                        source_gate='source heldout improvement must be positive in both sizes; report intervals and all cells, no multiplicity-adjusted population claim'),
        boundaries=['previously inspected source splits, not new confirmatory evidence', 'no paper IDs, records not guaranteed independent papers',
                    'one checkpoint, no training seeds', 'four sources do not establish a general interference predictor',
                    'full-weight virtual gradient step is not LoRA/Adam training or isolation benefit',
                    'directions, norm and separability do not alone establish semantic or functional specialization'],
        wall_limit_s=1800, script_sha256=sha(__file__), source_loader_sha256=sha(LOADER/'smoke_sites.py'))
    write('analysis_contract.json', contract)
    assert sha(Path(entry['checkpoint'])/'state.pt') == contract['checkpoint_sha256']
    torch.set_num_threads(4)
    torch.manual_seed(20260926)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True)
    device = torch.device('cuda:0')
    model = load_model(entry, device).requires_grad_(False).eval()
    before = sample_state(model)
    counts0 = model.sae.firing_counts.clone(); tokens0 = model.sae.tokens_observed.clone()
    W = model.blocks[7].down.weight
    Wcopy = W.detach().clone()
    native_means=[]; native_last=[]; down_means=[]; down_last=[]
    cache_u=[]; cache_r=[]; native_rms=[]; smoke={}
    pp = torch.tensor(positions, device=device)
    print('MODEL_READY', torch.cuda.get_device_name(), flush=True)
    for offset in range(0, len(rows), 8):
        part = rows[offset:offset+8]
        ids, mask = make_batch([r['input_ids'] for r in part], device)
        box = []
        hook = model.blocks[7].down.register_forward_pre_hook(lambda m, inp: box.append(inp[0].detach()))
        try: cap, feat = forward_with_capture(model, ids, mask)
        finally: hook.remove()
        assert len(box)==1
        a=cap[7]['a'][0]; u=box[0]; r=feat['post_attention_residual']
        assert torch.equal(a,feat['sae_input'])
        for x in (a,u,r): assert torch.isfinite(x).all()
        native_means.append(a.float().mean(1).cpu().numpy()); native_last.append(a[:,-1].float().cpu().numpy())
        down_means.append(u.float().mean(1).cpu().numpy()); down_last.append(u[:,-1].float().cpu().numpy())
        native_rms.extend(a.float().square().mean((1,2)).sqrt().cpu().tolist())
        cache_u.append(u[:,pp].cpu()); cache_r.append(r[:,pp].float().cpu())
        if offset==0:
            # Native BF16 tail replay must match the actual full model before
            # adopting an explicit FP32 tail for sub-BF16-resolution steps.
            with torch.inference_mode(), torch.autocast('cuda',dtype=torch.bfloat16):
                replay = model.norm(r + F.linear(u,W))
            err=float((replay-feat['final_h']).abs().max()); assert err==0
            # Validate the FP32 tail against a complete forward with only down
            # output overridden to FP32. This is the diagnostic numeric model.
            def fp32_down(m, inp, output):
                with torch.autocast('cuda',enabled=False): return F.linear(inp[0].float(),W.float())
            hh=model.blocks[7].down.register_forward_hook(fp32_down)
            try:
                with torch.inference_mode(), torch.autocast('cuda',dtype=torch.bfloat16):
                    full_fp32tail=model.forward_intermediates(ids,mask)['final_h']
            finally: hh.remove()
            with torch.inference_mode(): tail=model.norm(r.float()+F.linear(u.float(),W.float()))
            err32=float((tail-full_fp32tail).abs().max()); assert err32==0
            smoke=dict(native_tail_replay_max_abs=err,fp32_tail_full_forward_max_abs=err32,hook_equals_sae_input=True)
            write('smoke_receipt.json',dict(status='PASS',**smoke))
        if (offset+8)%128==0: print('EXTRACTED',offset+8,flush=True)
    old=np.load(PRIOR/'activations.npz')
    rms_error=float(np.max(np.abs(np.array(native_rms)-old['native_rms'])))
    assert np.array_equal(old['sample_ids'],np.array([r['sample_id'] for r in rows]))
    assert rms_error<1e-6, rms_error
    np.savez_compressed(ROOT/'representations.npz',
        a_mean=np.concatenate(native_means), a_last=np.concatenate(native_last),
        u_mean=np.concatenate(down_means),u_last=np.concatenate(down_last),
        sample_ids=np.array([r['sample_id'] for r in rows]),native_rms=np.array(native_rms))
    u=torch.cat(cache_u).float().to(device); residual=torch.cat(cache_r).to(device)
    targets=torch.tensor([[r['input_ids'][i+1] for i in positions] for r in rows],device=device)
    torch.save(dict(u=u.cpu(),residual=residual.cpu(),targets=targets.cpu(),positions=positions),ROOT/'fixed_tail_cache.pt')
    del cache_u,cache_r,cap,feat,old
    torch.cuda.empty_cache()
    fit={d:np.array([i for i,r in enumerate(rows) if r['domain']==d and r['split']=='fit']) for d in domains}
    test=np.array([i for i,r in enumerate(rows) if r['split']=='test'])
    assert len(test)==512 and all(len(fit[d])==128 for d in domains)
    delta=torch.zeros_like(W,requires_grad=True)
    def chunks(ix):
        # 4 records x 16 positions. Backprop independently to keep the full
        # vocabulary logits out of the autograd graph after each chunk.
        for start_i in range(0,len(ix),4): yield ix[start_i:start_i+4]
    def losses(ix):
        h=model.norm(residual[ix]+F.linear(u[ix],W+delta))
        logits=F.linear(h.reshape(-1,h.shape[-1]),model.output_weight)
        return F.cross_entropy(logits,targets[ix].reshape(-1),reduction='none').reshape(len(ix),16).mean(1)
    def evaluate(ix):
        with torch.no_grad(): return np.concatenate([losses(j).cpu().numpy() for j in chunks(ix)])
    baseline=evaluate(test); repeat=evaluate(test)
    noop=float(np.max(np.abs(baseline-repeat))); assert noop==0
    write('diagnostic_progress.json',dict(phase='BASELINE',noop_max_abs=noop))
    gradients=[]; source_fit_losses=[]
    for d in domains:
        delta.grad=None; total=0.
        for ix in chunks(fit[d]):
            ll=losses(ix); (ll.sum()/len(fit[d])).backward(); total+=float(ll.detach().sum())
        g=delta.grad.detach().clone(); assert torch.isfinite(g).all() and g.norm()>1e-8
        gradients.append(g); source_fit_losses.append(total/128)
        print('GRADIENT',d,float(g.norm()),flush=True)
    gg=torch.stack([g.flatten().double() for g in gradients]); gram=gg@gg.T
    cosine=(gram/gram.diag().sqrt()[:,None]/gram.diag().sqrt()[None,:]).cpu().numpy()
    np.savez_compressed(ROOT/'gradient_geometry.npz',gram=gram.cpu().numpy(),cosine=cosine)
    torch.save({d:g.cpu() for d,g in zip(domains,gradients)},ROOT/'source_gradients.pt')
    outcomes=[]; branch_ids=[]
    for d,g in zip(domains,gradients):
        for rho in (1e-4,5e-5):
            with torch.no_grad(): delta.copy_(-rho*W.norm()*g/g.norm())
            vals=evaluate(test)
            outcomes.append(vals); branch_ids.append(dict(source=d,rho=rho,gradient_norm=float(g.norm()),delta_norm=float(delta.norm())))
            with torch.no_grad(): delta.zero_()
            assert torch.count_nonzero(delta)==0
            print('BRANCH',d,rho,'help',float((baseline-vals).mean()),flush=True)
            write('diagnostic_progress.json',dict(phase='BRANCHES',completed=len(outcomes),expected=8))
    final=evaluate(test); assert np.array_equal(final,baseline)
    assert torch.equal(W,Wcopy) and sample_state(model)==before
    assert torch.equal(counts0,model.sae.firing_counts) and torch.equal(tokens0,model.sae.tokens_observed)
    np.savez_compressed(ROOT/'update_losses.npz',baseline=baseline,after=np.stack(outcomes),test_indices=test)
    write('branches.json',branch_ids)
    complete=dict(status='COMPLETE',elapsed_s=time.monotonic()-start,records=1024,
        representation_tokens=1024*256,update_tokens_per_source=128*16,readout_tokens_per_group=128*16,
        virtual_branches=8,optimizer_updates=0,checkpoint_writes=0,noop_max_abs=noop,
        state_sample_unchanged=True,down_weight_bitwise_unchanged=True,activity_buffers_unchanged=True,
        old_cache_native_rms_max_abs=rms_error,numeric_smoke=smoke,source_fit_losses=source_fit_losses,
        W_norm=float(W.norm()),gpu=torch.cuda.get_device_name(),torch=str(torch.__version__),
        max_allocated_bytes=torch.cuda.max_memory_allocated(),max_reserved_bytes=torch.cuda.max_memory_reserved(),
        source_model_sha256=sha(Path(entry['source_root'])/'dense_sae/model/modeling_qwen3_sae.py'),
        source_sae_sha256=sha(Path(entry['source_root'])/'dense_sae/model/sae.py'),
        contract_sha256=sha(ROOT/'analysis_contract.json'))
    write('complete.json',complete)
    write('raw_manifest.json',{str(p):sha(p) for p in ROOT.iterdir() if p.is_file() and p.name not in ['raw_manifest.json','run.log']})
    print(json.dumps(complete),flush=True)

if __name__=='__main__': main()
