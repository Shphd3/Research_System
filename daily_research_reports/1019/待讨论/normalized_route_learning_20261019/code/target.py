from common import *
from train import optimizer
import argparse
from torch.utils.tensorboard import SummaryWriter

def run(expert,device):
 configure(device,11);dest=ROOT/f'target/adapt/expert{expert}';dest.mkdir(parents=True,exist_ok=True)
 if (dest/'complete.json').exists():return
 t0=time.monotonic();writer=SummaryWriter(str(dest/'tensorboard'));target=json.load(open(ROOT/'config/target.json'));u=target['feature_id'];c=loadcache('train');e=loadcache('eval');Ct=np.flatnonzero(csr(c,True)[:,u].toarray().ravel()>0);Ce=np.flatnonzero(csr(e,True)[:,u].toarray().ravel()>0);Be=np.flatnonzero(csr(e,True)[:,u].toarray().ravel()==0);head=FrozenHead(device);m=Branch(11,False).to(device);m.load_state_dict(torch.load(ROOT/'target/background/epoch2.pt',map_location='cpu',weights_only=False)['model'])
 for ei,ex in enumerate(m.experts):
  for p in ex.parameters():p.requires_grad_(ei==expert)
 opt=torch.optim.AdamW(m.experts[expert].parameters(),lr=1e-4,betas=(.9,.95),eps=1e-8,weight_decay=.01);gen=np.random.default_rng(11);parts=[]
 while sum(map(len,parts))<32*64:parts.append(gen.permutation(Ct))
 order=np.concatenate(parts)[:32*64].reshape(32,64);np.save(dest/'adapt_order.npy',order);baseold,_,_=evaluate(m,head,e,device,'T_S1',indices=Be);rows=[]
 def assess(step):
  new,_,_=evaluate(m,head,e,device,'T_S1',indices=Ce,force=expert,gate_override=1.);old,_,_=evaluate(m,head,e,device,'T_S1',indices=Be);np.savez_compressed(dest/f'eval_step{step}.npz',new_nll=new,old_nll=old,C_eval=Ce,B_eval=Be);rows.append(dict(expert=expert,step=step,target_feature=u,C_train_N=len(Ct),C_eval_N=len(Ce),C_eval_contexts=len(np.unique(e['block_id'][Ce].numpy())),B_eval_N=len(Be),C_absolute_NLL=float(new.mean()),gain_before_minus_after=0 if step==0 else rows[0]['C_absolute_NLL']-float(new.mean()),B_old_cost=float((old-baseold).mean()),evidence_sufficient=bool(len(Ce)>=50 and len(np.unique(e['block_id'][Ce].numpy()))>=5)));csvwrite(dest/'new_input_assignment.csv',rows)
 assess(0)
 for step in range(32):
  ix=order[step];h=c['hidden'][ix].to(device);y=c['target'][ix].to(device);opt.zero_grad(set_to_none=True);ho,_=m(h,torch.as_tensor(routes('train','T_S1')[ix],device=device),force=expert,gate_override=1.);loss=F.cross_entropy(head(ho).float(),y);loss.backward();torch.nn.utils.clip_grad_norm_(m.experts[expert].parameters(),1.);opt.step();append(dest/'steps.jsonl',dict(step=step+1,nll=float(loss.detach()),seen=(step+1)*64))
  writer.add_scalar('tokens/train_lm_loss',float(loss.detach()),(step+1)*64);writer.add_scalar('updates/train_lm_loss',float(loss.detach()),step+1);writer.add_scalar('tokens/train_total_loss',float(loss.detach()),(step+1)*64);writer.add_scalar('updates/learning_rate',1e-4,step+1);writer.add_scalar('progress/tokens_seen',(step+1)*64,step+1);writer.add_scalar('progress/effective_tokens_per_update',64,step+1);writer.add_scalar('progress/optimizer_step',step+1,(step+1)*64)
  if step+1 in [8,32]:
   assess(step+1);save(dest/f'step{step+1}.pt',dict(model=cpu_tree(m.state_dict()),optimizer=cpu_tree(opt.state_dict()),rng=rng(),step=step+1,seen=(step+1)*64,data_order=order,next_batch=step+1,target=u,expert=expert));writer.flush()
 writer.close();save(dest/'final.pt',dict(model=cpu_tree(m.state_dict()),optimizer=cpu_tree(opt.state_dict()),rng=rng(),step=32,seen=2048,data_order=order,background_checkpoint=str(ROOT/'target/background/epoch2.pt'),target=u,expert=expert));write_json(dest/'complete.json',dict(status='COMPLETE',seconds=time.monotonic()-t0,steps=32,seen=2048,**memory(device)))
def recommend(device):
 configure(device);c=loadcache('train');u=json.load(open(ROOT/'config/target.json'))['feature_id'];ix=np.flatnonzero(csr(c,True)[:,u].toarray().ravel()>0);m=Branch(11,False).to(device);m.load_state_dict(torch.load(ROOT/'target/background/epoch2.pt',map_location='cpu',weights_only=False)['model']);head=FrozenHead(device);loss=[]
 for expert in range(8):
  n,_,_=evaluate(m,head,c,device,'T_S1',indices=ix,force=expert,gate_override=1.);loss.append(float(n.mean()))
 natural=routes('train','T_S1')[ix];load=np.bincount(natural,minlength=8);owner=np.load(PREV/'metrics/core/owners.npz')['T'][u];write_json(ROOT/'target/recommendations.json',dict(target_feature=u,list_recommendation=int(owner),actual_route_recommendation=int(load.argmax()),current_prediction_recommendation=int(np.argmin(loss)),TRAIN_forced_NLL=loss,TRAIN_natural_route_load=load,TRAIN_only=True,recorded_before_adapt=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--expert',type=int);ap.add_argument('--device',default='cuda:0');ap.add_argument('--recommend',action='store_true');a=ap.parse_args()
 if a.recommend:recommend(a.device)
 else:run(a.expert,a.device)
