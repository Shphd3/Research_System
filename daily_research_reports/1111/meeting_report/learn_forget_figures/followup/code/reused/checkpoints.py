from lf_common import *
DENSE=BASE/'20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z';MOE=BASE/'20261031_dense_order_aligned_moe_baseline/runs/formal'
sys.path[:0]=[str(BASE/'20260913_dense_baseline_pretraining'),str(BASE/'20261031_dense_order_aligned_moe_baseline')]
from dense_sae.model import Qwen3SAEConfig,Qwen3SAEForCausalLM
from moe_baseline.model import DenseAlignedMoE,MoeConfig
def inventory():
 rows=[]
 for label,root in [('Dense',DENSE),('MoE',MOE)]:
  for mp in sorted((root/'milestones').glob('*/manifest.json')):
   z=json.load(mp.open());t=z['tokens_seen']
   if t>10000000000 and not(label=='MoE' and t==33000000000):continue
   f=next(x for x in z['files'] if x['path']=='state.pt');p=mp.parent/'state.pt';rows.append(dict(model=label,tokens=t,step=z['optimizer_step'],path=str(p),config=str(root/'resolved_config.json'),manifest=str(mp),bytes=f['size_bytes'],sha256=f['sha256'],exists=p.exists(),purpose='reference' if t==33000000000 else 'trajectory'))
 dump(R/'evidence/checkpoint_inventory.json',rows);table(pd.DataFrame(rows),'checkpoint_inventory','Manifest SHA initially recorded; actual load and checksum receipts are saved one checkpoint at a time.')
 register('checkpoint_family_learn_forget_inputs_20261111',[Path(x['path']) for x in rows if x['exists']]+[R/'evidence/checkpoint_inventory.json'],dict(parent_assets=['checkpoint_family_moe_baseline_saved_20261104','model_s7_temporal_dense_1b_a24_20261013'],checkpoints=rows,training_updates=0),category='model_checkpoint')
 return rows
def load(row,grad=False):
 p=Path(row['path']);assert p.stat().st_size==row['bytes'];actual=sha(p);assert actual==row['sha256']
 cfg=json.load(open(row['config']));cfg=cfg.get('config',cfg)['model']
 m=Qwen3SAEForCausalLM(Qwen3SAEConfig(**cfg)) if row['model']=='Dense' else DenseAlignedMoE(MoeConfig.from_dict(cfg))
 s=torch.load(p,map_location='cpu',mmap=True,weights_only=False);assert s['tokens_seen']==row['tokens'];m.load_state_dict(s['model'],strict=True);del s
 m.cuda().eval().requires_grad_(grad);return m,dict(sha256_verified=actual,total_parameters=sum(p.numel() for p in m.parameters()))
if __name__=='__main__':inventory()
