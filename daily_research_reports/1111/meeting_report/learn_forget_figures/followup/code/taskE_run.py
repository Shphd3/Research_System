import os
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION','python')
from fu import *
from checkpoints import load
from gradients import parameter_blocks,maps,raw_T,summarize
from torch.nn import functional as NN
from torch.utils.checkpoint import checkpoint
from threadpoolctl import threadpool_limits
import gc
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
DIM=2**20
def one_gradient(m,blocks,mapping,inputs,targets,W,seqs,group):
 m.zero_grad(set_to_none=True);den=float(np.asarray(W).reshape(2048,2048,16)[seqs,:,group].astype(np.float64).sum());assert den>0;loss=0.
 for k in range(0,len(seqs),8):
  ix=seqs[k:k+8];x=torch.from_numpy(np.array(inputs[ix])).long().cuda();y=torch.from_numpy(np.array(targets[ix])).reshape(-1).long().cuda();ww=torch.from_numpy(np.asarray(W).reshape(2048,2048,16)[ix,:,group].copy()).reshape(-1).float().cuda()
  with torch.autocast('cuda',dtype=torch.bfloat16):
   _,h=m.forward_features(x);hs=h.reshape(-1,1024);num=hs.sum()*0
   for j in range(0,len(y),128):
    def ce(a,weight,t,w):return (NN.cross_entropy(NN.linear(a,weight).float(),t,reduction='none')*w).sum()
    num+=checkpoint(ce,hs[j:j+128],m.output_weight,y[j:j+128],ww[j:j+128],use_reentrant=False)
   part=num/den
  part.backward();loss+=float(part.detach());del x,y,ww,h,hs,num,part
 out={};norms={}
 for block,arr in blocks.items():
  v=torch.zeros(DIM,device='cuda');n=torch.zeros((),device='cuda',dtype=torch.float64)
  for name,p in arr:
   if p.grad is None:continue
   g=p.grad.detach().reshape(-1);n+=(g.double()*g.double()).sum();index,sign=mapping[name];v.index_add_(0,index.long(),g*sign)
  out[block]=v.cpu().numpy();norms[block]=float(n)
 return out,norms,loss
def main():
 assert (F/'evidence/E_preparation_complete.json').exists();folder=F/'data/E';inputs=np.load(folder/'inputs.npy',mmap_mode='r');targets=np.load(folder/'targets.npy',mmap_mode='r');W=np.load(folder/'group_weights.npy',mmap_mode='r');old=json.load(open(ROOT/'precision8/evidence/gradient_batches.json'))['sequence_ids'];batches={'32_extended':json.load(open(folder/'batches32.json')),'8_extended_control':json.load(open(folder/'batches8_extended.json')),'8_original':old};inventory=json.load(open(ROOT/'evidence/checkpoint_inventory.json'));co=pd.read_csv(ROOT/'results/fig2_transfer_coefficients.csv');lift=np.empty((16,16))
 for r in co.drop_duplicates(['group_a','group_b']).itertuples():lift[r.group_a,r.group_b]=r.cooccurrence_lift
 plans=[('32_extended',10000000000),('8_extended_control',10000000000),('8_original',3000000000),('8_original',5000000000),('8_original',500000000)];outdir=F/'data/E/sketches';outdir.mkdir(exist_ok=True);rows=pd.read_csv(F/'results/E_new_transfer_coefficients.csv').to_dict('records') if (F/'results/E_new_transfer_coefficients.csv').exists() else [];summaries=pd.read_csv(F/'results/E_new_statistics.csv').to_dict('records') if (F/'results/E_new_statistics.csv').exists() else [];normrows=[];tic=time.monotonic()
 for mode,t in plans:
  for kind in ['MoE','Dense']:
   receipt=F/f'evidence/E_{mode}_{kind}_{t}.json'
   if receipt.exists():continue
   row=next(z for z in inventory if z['model']==kind and z['tokens']==t);print('E_LOAD',mode,kind,t,flush=True);m,loadinfo=load(row,False);versions=[p._version for p in m.parameters()];bias=[b.moe.load_bias.clone() for b in m.blocks] if kind=='MoE' else [];blocks=parameter_blocks(m,kind);mapping=maps(blocks);Gs={b:[] for b in blocks};localnorm=[];start=time.monotonic()
   for g in range(16):
    bs={b:[] for b in blocks}
    for r,seqs in enumerate(batches[mode][str(g)]):
     out,nn,ll=one_gradient(m,blocks,mapping,inputs,targets,W,seqs,g)
     for b in blocks:bs[b].append(out[b]);localnorm.append(dict(mode=mode,model=kind,tokens=t,block=b,group=g,replicate=r,sequences=len(seqs),exact_gradient_norm2=nn[b],projected_norm2=float(np.sum(out[b].astype(np.float64)**2)),loss=ll))
    for b in blocks:Gs[b].append(np.stack(bs[b]))
    if g%4==3:print('E_GRAD',mode,kind,t,'group',g,'sec',round(time.monotonic()-start),flush=True)
   assert [p._version for p in m.parameters()]==versions;assert all(torch.equal(a,b.moe.load_bias) for a,b in zip(bias,m.blocks))
   for block,arr in Gs.items():
    G=np.stack(arr);np.save(outdir/f'{mode}_{kind}_{t}_{block}.npy',G);pp,ss,T=summarize(G,list(range(16)),lift,kind,t,block)
    for a in pp:a['mode']=mode
    ss['mode']=mode;rows+=pp;summaries.append(ss)
   normrows+=localnorm;table(pd.DataFrame(localnorm),f'E_norm_{mode}_{kind}_{t}');m.zero_grad(set_to_none=True);del m,mapping,Gs;gc.collect();torch.cuda.empty_cache();dump(receipt,dict(mode=mode,model=kind,tokens=t,seconds=time.monotonic()-start,model_and_bias_unchanged=True,training_updates=0,load=loadinfo))
   # Reconstruct from percondition files on resume; these are new followup-only outputs.
   table(pd.DataFrame(rows),'E_new_transfer_coefficients');table(pd.DataFrame(summaries),'E_new_statistics');event('E条件',f'{mode} {kind} {t/1e9:g}B完成',seconds=time.monotonic()-start)
 dump(F/'evidence/E_gradients_complete.json',dict(plans=plans,models=2,groups=16,R=4,seconds=time.monotonic()-tic,training_updates=0));event('E梯度','10B精度、扩展样本对照与新增3/5/0.5B全部只读梯度完成',seconds=time.monotonic()-tic)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
