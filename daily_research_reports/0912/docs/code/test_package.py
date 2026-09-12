import csv,json,subprocess,sys
from dataclasses import replace
from pathlib import Path
import numpy as np
import pytest
import torch
from torch.nn import functional as F
from model import Qwen3SAEConfig,Qwen3SAEForCausalLM,TopKSAE,normalized_objective
from analysis.collect_activations import collect
from analysis.feature_statistics import sparse_codes,coactivation_graph,group_scores
from analysis.feature_semantics import triplet_margins,block_bootstrap,patch_feature_group
from analysis.representation_evolution import relation_drift,variance_decomposition
from data.prepare_tokens import write_shards,split_for_text
from utils.distillation import coarsened_kl

torch.set_num_threads(1)

def cfg(**kwargs):
    base=Qwen3SAEConfig(vocab_size=47,hidden_size=24,intermediate_size=48,num_hidden_layers=2,
                      num_attention_heads=4,num_key_value_heads=2,head_dim=8,max_position_embeddings=32,
                      sae_width=64,sae_k=4,ce_chunk_tokens=3)
    return replace(base,**kwargs)

def sample():
    torch.manual_seed(4)
    return torch.randint(0,47,(2,8))

def test_invalid_config():
    with pytest.raises(ValueError):cfg(head_dim=7)
    with pytest.raises(ValueError):cfg(num_attention_heads=3)
    with pytest.raises(ValueError):Qwen3SAEConfig.from_dict({"unknown":True})

def test_sparse_reconstruction_shapes_norms():
    s=TopKSAE(24,64,4);x=torch.randn(7,24);o=s(x)
    assert o.indices.shape==(7,4) and o.reconstruction.shape==x.shape
    assert (o.values>=0).all()
    assert torch.allclose(s.dictionary().norm(dim=0),torch.ones(64),atol=1e-6)
    o.loss_sum.backward();assert s.encoder.weight.grad is not None
    assert s.tokens_observed.item()==0
    s.record_activity(o);assert s.tokens_observed.item()==7

def test_natural_backbone_gradient_parity():
    torch.manual_seed(17);a=Qwen3SAEForCausalLM(cfg(sae_mode="none"))
    torch.manual_seed(17);b=Qwen3SAEForCausalLM(cfg(sae_mode="observer"))
    x=sample();oa=a(x,labels=x);ob=b(x,labels=x)
    normalized_objective(oa).backward();normalized_objective(ob).backward()
    for name,p in a.named_parameters():
        q=dict(b.named_parameters())[name]
        assert torch.equal(p,q),name
        assert torch.allclose(p.grad,q.grad,atol=1e-7,rtol=1e-6),name
    assert b.sae.encoder.weight.grad.abs().sum()>0

def test_observer_sae_loss_cannot_move_backbone():
    m=Qwen3SAEForCausalLM(cfg());o=m(sample());o.sae_loss_sum.backward()
    assert m.embed.weight.grad is None

def test_auxiliary_sae_loss_reaches_backbone():
    m=Qwen3SAEForCausalLM(cfg(sae_mode="auxiliary"));o=m(sample());o.sae_loss_sum.backward()
    assert m.embed.weight.grad is not None and m.embed.weight.grad.abs().sum()>0

def test_future_token_does_not_change_prefix():
    m=Qwen3SAEForCausalLM(cfg(sae_mode="none")).eval();x=sample();y=x.clone();y[:,5:]=(y[:,5:]+1)%47
    a=m(x,return_logits=True).logits;b=m(y,return_logits=True).logits
    assert torch.allclose(a[:,:5],b[:,:5],atol=1e-6)
    assert not torch.allclose(a[:,5:],b[:,5:])

def test_chunked_ce_matches_full_and_gradients():
    m=Qwen3SAEForCausalLM(cfg(sae_mode="none"));x=sample();o=m(x,labels=x,return_logits=True)
    ref=F.cross_entropy(o.logits[:,:-1].reshape(-1,47),x[:,1:].reshape(-1),reduction="sum")
    assert o.lm_tokens.item()==14
    assert torch.allclose(o.lm_loss_sum,ref,atol=1e-5)
    g1=torch.autograd.grad(o.lm_loss_sum,m.embed.weight,retain_graph=True)[0]
    g2=torch.autograd.grad(ref,m.embed.weight)[0]
    assert torch.allclose(g1,g2,atol=1e-5,rtol=1e-5)

def test_padding_and_shift_mask():
    m=Qwen3SAEForCausalLM(cfg());x=sample();mask=torch.ones_like(x,dtype=torch.bool);mask[1,5:]=False
    o=m(x,attention_mask=mask,labels=x)
    assert o.lm_tokens.item()==11 and o.sae_tokens.item()==13
    assert torch.isfinite(normalized_objective(o))

def test_segment_mask_blocks_previous_document():
    m=Qwen3SAEForCausalLM(cfg(sae_mode="none")).eval();x=sample();y=x.clone();y[:,:4]=(y[:,:4]+3)%47
    seg=torch.tensor([[0]*4+[1]*4]*2)
    a=m(x,segment_ids=seg,return_logits=True,labels=x)
    b=m(y,segment_ids=seg,return_logits=True)
    assert torch.allclose(a.logits[:,4:],b.logits[:,4:],atol=1e-6)
    assert a.lm_tokens.item()==12

def test_zero_alpha_exact_parity():
    torch.manual_seed(3);a=Qwen3SAEForCausalLM(cfg(sae_mode="none"))
    torch.manual_seed(3);b=Qwen3SAEForCausalLM(cfg(sae_mode="bottleneck",bottleneck_alpha=0))
    x=sample()
    assert torch.equal(a(x,return_logits=True).logits,b(x,return_logits=True).logits)

def test_nonzero_bottleneck_and_checkpointed_blocks():
    m=Qwen3SAEForCausalLM(cfg(sae_mode="bottleneck",bottleneck_alpha=.2,gradient_checkpointing=True))
    x=sample();loss=normalized_objective(m(x,labels=x));loss.backward()
    assert torch.isfinite(loss) and m.sae.decoder.grad.abs().sum()>0

def test_model_checkpoint_roundtrip(tmp_path):
    m=Qwen3SAEForCausalLM(cfg()).eval();x=sample();m.save_checkpoint(tmp_path)
    n=Qwen3SAEForCausalLM.from_checkpoint(tmp_path).eval()
    assert torch.equal(m(x,return_logits=True).logits,n(x,return_logits=True).logits)

def test_collect_exact_position(tmp_path):
    m=Qwen3SAEForCausalLM(cfg());x=sample();data={"input_ids":x.numpy(),"attention_mask":np.ones((2,8)),
      "positions":np.array([3,6]),"sample_ids":np.array(["a","b"])}
    out=collect(m,data,batch_size=1)
    assert out["h"].shape==(2,24)
    with torch.no_grad():h=m.forward_features(x,torch.ones_like(x))[1]
    assert np.allclose(out["h"],h[torch.arange(2),torch.tensor([3,6])].numpy(),atol=1e-6)
    assert m.sae.tokens_observed.item()==0

def test_coactivation_and_missing_mass():
    z=sparse_codes(np.array([[0,1],[0,2]]),np.array([[1.,1.],[1.,1.]]),3)
    graph,counts=coactivation_graph(z)
    assert np.array_equal(counts,[2,1,1]) and graph[1,2]==0
    q,coverage=group_scores(z,np.array([0,-1,1]))
    assert np.allclose(q.sum(1),[.5,1.]) and np.allclose(coverage,[.5,1.])

def test_variance_identity_soft_and_hard():
    rng=np.random.default_rng(2);x=rng.normal(size=(20,5));q=rng.random((20,3));q/=q.sum(1,keepdims=True)
    r=variance_decomposition(x,q);assert abs(r["W"]+r["B"]-r["T"])<1e-10
    with pytest.raises(ValueError):variance_decomposition(x,q*.8)

def test_relation_invariant_to_feature_permutation():
    x=np.random.default_rng(2).normal(size=(11,7))
    assert relation_drift(x,x[:,::-1])<1e-12

def test_semantic_margin_and_block_bootstrap():
    x=np.array([[1,0],[1,0],[0,1],[0,1.]])
    triplets=[dict(anchor_id="a",positive_id="b",negative_id="c",block_id="one"),
              dict(anchor_id="c",positive_id="d",negative_id="a",block_id="two")]
    v,c,b=triplet_margins(x,["a","b","c","d"],triplets)
    assert np.allclose(v,1) and c.all()
    assert block_bootstrap(v,b)["ci95"]==[1,1]

def test_residual_preserving_patch_noop():
    s=TopKSAE(24,64,4);h=torch.randn(5,24)
    assert torch.equal(patch_feature_group(h,s,[0,1],scale=1),h)
    assert torch.equal(patch_feature_group(h,s,[],scale=0),h)

def test_topk_tail_distillation_zero_at_same_distribution():
    logits=torch.randn(4,11);prob=logits.softmax(-1);vals,idx=prob.topk(3,dim=-1);tail=1-vals.sum(-1)
    loss=coarsened_kl(logits,idx,vals,tail)
    assert torch.allclose(loss,torch.zeros(4),atol=2e-7)
    with pytest.raises(ValueError):coarsened_kl(logits,idx,vals,tail+.1)

def test_tokenization_whole_document_dedup_and_uint32(tmp_path):
    info=write_shards([{"text":"hello  world"},{"text":"hello world"},{"text":"different"}],
                      lambda _: [151000,4],151643,tmp_path,shard_tokens=4)
    assert sum(info["document_counts"].values())==2
    assert sum(info["token_counts"].values())==6
    assert split_for_text("hello  world")==split_for_text("hello world")
    flat=np.concatenate([np.fromfile(tmp_path/v["file"],dtype="<u4") for v in info["shards"]])
    assert 151000 in flat and len(flat)==6

def test_distributed_count_normalization():
    m=Qwen3SAEForCausalLM(cfg(sae_mode="none"));x=sample();o=m(x,labels=x)
    a=normalized_objective(o,world_size=2,lm_global_count=o.lm_tokens*2)
    assert torch.allclose(a,normalized_objective(o))

def test_analysis_cli_end_to_end(tmp_path):
    root=Path(__file__).resolve().parents[1]
    m=Qwen3SAEForCausalLM(cfg());m.save_checkpoint(tmp_path/"model")
    x=sample().numpy();panel=tmp_path/"panel.npz"
    np.savez(panel,input_ids=x,attention_mask=np.ones_like(x),positions=np.array([3,6]),sample_ids=np.array(["a","b"]))
    subprocess.run([sys.executable,"-m","analysis.collect_activations","--checkpoint",str(tmp_path/"model"),
                    "--panel",str(panel),"--output",str(tmp_path/"acts.npz")],cwd=root,check=True,capture_output=True)
    subprocess.run([sys.executable,"-m","analysis.feature_statistics","--activations",str(tmp_path/"acts.npz"),
                    "--width","64","--output-dir",str(tmp_path/"stats")],cwd=root,check=True,capture_output=True)
    assert json.loads((tmp_path/"stats/statistics.json").read_text())["tokens"]==2

def test_probe_builder_no_future_answer():
    from data.build_probe_panel import build_panel
    rows=[dict(sample_id="a",prefix="AB",expected_continuation="C",relation_label="r",format_label="f",block_id="b",split="confirmation")]
    data=build_panel(rows,lambda text:[ord(c) for c in text],0,20)
    assert data["input_ids"].tolist()==[[65,66]]
    assert data["positions"].tolist()==[1] and data["expected_next_ids"].tolist()==[67]
    with pytest.raises(ValueError):build_panel(rows,lambda text:[ord(c) for c in text],0,1)
