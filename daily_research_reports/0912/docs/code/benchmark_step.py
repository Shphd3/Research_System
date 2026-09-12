"""CUDA/DDP step microbenchmark ONLY. Random tokens are NOT a scientific training run.
Example: torchrun --standalone --nproc_per_node=4 -m scripts.benchmark_step --steps 30
"""
import argparse,json,os,time
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from model import Qwen3SAEConfig,Qwen3SAEForCausalLM,normalized_objective

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--steps",type=int,default=30);p.add_argument("--warmup",type=int,default=10)
    p.add_argument("--microbatch",type=int,default=2);p.add_argument("--sequence",type=int,default=2048)
    p.add_argument("--mode",choices=["none","observer","auxiliary"],default="observer")
    p.add_argument("--sae-stride",type=int,default=8);p.add_argument("--output",default="benchmark.json")
    a=p.parse_args()
    if not torch.cuda.is_available():raise RuntimeError("No CUDA device; refusing to fabricate an H100 timing")
    if min(a.steps,a.warmup,a.microbatch,a.sequence,a.sae_stride)<=0:raise ValueError("Positive benchmark sizes required")
    world=int(os.environ.get("WORLD_SIZE","1"));rank=int(os.environ.get("RANK","0"));local=int(os.environ.get("LOCAL_RANK","0"))
    torch.cuda.set_device(local);device=torch.device("cuda",local)
    if world>1:dist.init_process_group("nccl")
    torch.manual_seed(17)
    c=Qwen3SAEConfig(sae_mode=a.mode,max_position_embeddings=a.sequence)
    net=Qwen3SAEForCausalLM(c).to(device)
    model=DDP(net,device_ids=[local],broadcast_buffers=False) if world>1 else net
    optimizer=torch.optim.AdamW(model.parameters(),lr=3e-4,fused=True)
    x=torch.randint(0,c.vocab_size,(a.microbatch,a.sequence),device=device)
    mask=torch.zeros_like(x,dtype=torch.bool);mask[:,::a.sae_stride]=True
    torch.cuda.reset_peak_memory_stats();start=None
    for step in range(a.warmup+a.steps):
        if step==a.warmup:
            torch.cuda.synchronize()
            if world>1:dist.barrier()
            start=time.perf_counter()
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast("cuda",dtype=torch.bfloat16):
            out=model(x,labels=x,sae_mask=mask)
            loss=normalized_objective(out) # equal shapes/counts on every rank in this benchmark
        loss.backward();optimizer.step()
    torch.cuda.synchronize();duration=torch.tensor(time.perf_counter()-start,device=device)
    memory=torch.tensor(torch.cuda.max_memory_allocated(),device=device)
    if world>1:
        dist.all_reduce(duration,op=dist.ReduceOp.MAX);dist.all_reduce(memory,op=dist.ReduceOp.MAX)
    if rank==0:
        report={"gpu":torch.cuda.get_device_name(),"world_size":world,"mode":a.mode,
                "seconds":duration.item(),"valid_prediction_tokens_per_second":world*a.steps*a.microbatch*(a.sequence-1)/duration.item(),
                "max_allocated_bytes_per_rank":memory.item(),"includes":"forward, CE recompute, SAE, backward, optimizer, DDP",
                "excludes":"real data I/O, checkpoint I/O, validation, cluster queue, source compilation startup",
                "status":"SYSTEMS_MICROBENCHMARK_NOT_A_RESEARCH_RESULT"}
        open(a.output,"w",encoding="utf-8").write(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if world>1:dist.destroy_process_group()
if __name__=="__main__":main()
