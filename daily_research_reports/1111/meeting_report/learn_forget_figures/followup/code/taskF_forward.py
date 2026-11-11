import os
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION','python')
from fu import *
sys.path[:0]=[str(ROOT.parent/'20260913_dense_baseline_pretraining'),str(R4),str(R4/'vendor')]
from routing import configure,set_scores,group_scores,random_scores
from moe_baseline.model import DenseAlignedMoE,MoeConfig
from dense_sae.model import Qwen3SAEForCausalLM,Qwen3SAEConfig
from torch.nn import functional as NN
import gc,fcntl,subprocess

def prepare():
 folder=F/'data/F';folder.mkdir(exist_ok=True);rng=np.random.default_rng(20261116);samples={split:sorted(map(int,rng.choice(1024,128,replace=False))) for split in ['DEV','EVAL']};dump(folder/'samples.json',samples);inv=json.load(open(ROOT/'evidence/checkpoint_inventory.json'));rows=[dict(next(z for z in inv if z['model']=='Dense' and z['tokens']==500000000),arm='Dense')]
 for a in ['A0','A5','A2']:
  root=R4 if a=='A5' else R3;mp=root/f'runs/{a}/milestones/token_000524288000/manifest.json';d=json.load(mp.open());z=next(x for x in d['files'] if x['path']=='state.pt');rows.append(dict(arm=a,model='MoE',step=2000,tokens=524288000,path=str(mp.parent/'state.pt'),config=str(root/f'arms/{a}.yaml'),manifest=str(mp),bytes=z['size_bytes'],sha256=z['sha256']))
 dump(F/'evidence/F_checkpoint_inventory.json',rows)
 aid='checkpoint_learn_forget_followup_spectra_inputs_20261111'
 with (REPO/'assets/.catalog.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);p=REPO/'assets/catalog.json';c=json.load(p.open())
  if not any(a['id']==aid for a in c['assets']):
   c['assets'].append(dict(id=aid,title_cn='FFN条件谱四臂输入状态',category='model_checkpoint',kind='learn_forget_followup_F',projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=z['path'],expected='file',required=True,probes=[]) for z in rows],identity=dict(inventory=str(F/'evidence/F_checkpoint_inventory.json')),source_paths=[str(F/'protocol_F_cn.md')]));tmp=p.with_suffix('.F.tmp');tmp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)
 subprocess.run([sys.executable,str(REPO/'tools/check_assets.py'),'--strict','--asset',aid,'--asset','dclm_pair_v1','--output',str(F/f'evidence/F_input_access_{time.time_ns()}.json')],stdout=subprocess.DEVNULL,check=True);return samples,rows

def main():
 assert (F/'evidence/E_complete.json').exists();tic=time.monotonic();samples,rows=prepare();folder=F/'data/F';group=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);group={k:group[k].cuda() for k in ['group','w']};torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 for row in rows:
  arm=row['arm'];receipt=F/f'evidence/F_forward_{arm}.json'
  if receipt.exists():continue
  print('F_LOAD',arm,flush=True);p=Path(row['path']);actual=sha(p);assert actual==row['sha256'];cfg=json.load(open(row['config']));mc=cfg.get('config',cfg)['model'];m=Qwen3SAEForCausalLM(Qwen3SAEConfig(**mc)) if arm=='Dense' else DenseAlignedMoE(MoeConfig.from_dict(mc));s=torch.load(p,map_location='cpu',mmap=True,weights_only=False);assert s['tokens_seen']==row['tokens'];m.load_state_dict(s['model'],strict=True);del s;m.cuda().eval().requires_grad_(False)
  if arm!='Dense':configure(m,cfg)
  versions=[p._version for p in m.parameters()];bias=[] if arm=='Dense' else [b.moe.load_bias.clone() for b in m.blocks];captures={};hooks=[b.norm2.register_forward_hook(lambda mod,args,y,l=l:captures.__setitem__(l,y.detach())) for l,b in enumerate(m.blocks)];start=time.monotonic();checks=[];rounderr=[]
  for split,ids in samples.items():
   tok=np.load(R4/f'data/{split}_tokens.npy',mmap_mode='r');out=np.lib.format.open_memmap(folder/f'h_{arm}_{split}.npy',mode='w+',dtype=np.float16,shape=(8,128*2048,1024));sel=np.lib.format.open_memmap(folder/f'sel_{arm}_{split}.npy',mode='w+',dtype=np.uint8,shape=(8,128*2048,2)) if arm!='Dense' else None
   dc=torch.load(R4/f'data/{"DEV_bf16" if split=="DEV" and arm=="A5" else split}_codes.pt',map_location='cpu',weights_only=False) if arm=='A5' else None
   reference=None
   if split=='EVAL':reference=np.load(ROOT/'positions/Dense_000500000000.npz' if arm=='Dense' else R4/f'analysis/positions/{arm}/step002000.npz')['loss'];total=0.
   with torch.inference_mode():
    for k in range(0,128,2):
     ss=ids[k:k+2];x=torch.stack([torch.from_numpy(np.array(tok[j*2048:(j+1)*2048])) for j in ss]).long().cuda()
     if arm=='A5':
      ii=torch.cat([dc['indices'][j*2048:(j+1)*2048] for j in ss]).long().cuda();vv=torch.cat([dc['values'][j*2048:(j+1)*2048] for j in ss]).float().cuda();set_scores(m,group_scores(ii,vv,group['group'],group['w']))
     elif arm=='A2':set_scores(m,torch.cat([random_scores((1,2048,8),-1,j%4,j//4,'cuda') for j in ss]).reshape(-1,8))
     with torch.autocast('cuda',dtype=torch.bfloat16):
      _,h=m.forward_features(x)
      if split=='EVAL':
       y=torch.cat([torch.from_numpy(np.array(tok[j*2048+1:(j+1)*2048+1])) for j in ss]).long().cuda();ce=torch.cat([NN.cross_entropy(NN.linear(z,m.output_weight).float(),t,reduction='none') for z,t in zip(h.reshape(-1,1024).split(128),y.split(128))]);total+=float(ce.double().sum())
     sl=slice(k*2048,(k+2)*2048)
     for l in range(8):
      z=captures[l].reshape(-1,1024).float().cpu().numpy();v=z.astype(np.float16);out[l,sl]=v
      if k==0:rounderr.append(dict(split=split,layer=l,max_abs_hidden_rounding=float(np.max(abs(z-v.astype(np.float32)))),mean_square_rounding_fraction=float(np.mean((z-v.astype(np.float32))**2)/max(np.mean(z*z),1e-30))))
      if sel is not None:sel[l,sl]=m.blocks[l].moe.last_selected.reshape(-1,2).cpu().numpy()
     del x,h
   out.flush();del out
   if sel is not None:sel.flush();del sel
   if split=='EVAL':
    ix=np.concatenate([np.arange(j*2048,(j+1)*2048) for j in ids]);ref=float(reference[ix].astype(np.float64).mean());delta=total/(128*2048)-ref;checks.append(dict(split=split,NLL_subset=total/(128*2048),cached_fp16_NLL_subset=ref,difference=delta));assert abs(delta)<1e-4,(arm,delta)
    if arm!='Dense':
     orig=np.load(R4/f'analysis/positions/{arm}/step002000.npz')['sel'][:,ix];new=np.load(folder/f'sel_{arm}_{split}.npy',mmap_mode='r');assert np.array_equal(np.sort(orig,axis=-1),np.sort(new,axis=-1)),arm
   del dc;print('F_FORWARD',arm,split,'seconds',round(time.monotonic()-start),flush=True)
  assert versions==[p._version for p in m.parameters()];assert all(torch.equal(a,b.moe.load_bias) for a,b in zip(bias,m.blocks))
  for hook in hooks:hook.remove()
  dump(receipt,dict(arm=arm,row=row,sha256_verified=actual,seconds=time.monotonic()-start,all_parameters_and_bias_unchanged=True,NLL_and_selection_checks=checks,hidden_capture_dtype='float16; float64 statistics',rounding=rounderr,training_updates=0));event('F前向',arm+' 两split8层FFN输入完成，EVAL loss和Top2回放核验',seconds=time.monotonic()-start);del m;gc.collect();torch.cuda.empty_cache()
 dump(F/'evidence/F_forward_complete.json',dict(seconds=time.monotonic()-tic,arms=4,splits=2,layers=8,positions_per_split=262144,training_updates=0))
if __name__=='__main__':main()
