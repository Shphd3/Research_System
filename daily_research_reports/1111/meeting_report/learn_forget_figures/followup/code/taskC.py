from fu import *
from torch.nn import functional as NN
from threadpoolctl import threadpool_limits
import gc
def forward_new(row,label):
 from checkpoints import load
 out=F/f'data/positions/{label}_{row["step"]:06d}.npz';out.parent.mkdir(exist_ok=True,parents=True);receipt=F/f'evidence/C_forward_{label}_{row["step"]}.json'
 if out.exists() and receipt.exists():return out
 tic=time.monotonic();m,info=load(row);versions=[p._version for p in m.parameters()];bias=[b.moe.load_bias.clone() for b in m.blocks] if row['model']=='MoE' else [];captures={};hooks=[]
 for l,b in enumerate(m.blocks):
  if row['model']=='MoE':hooks.append(b.moe.router.register_forward_hook(lambda mod,args,y,l=l,b=b:captures.__setitem__(l,(y.float().softmax(-1)+b.moe.load_bias).topk(2).indices)))
 tok=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');ll=np.empty(N,np.float16);ss=np.empty((8,N,2),np.uint8) if bias else None;total=0.
 with torch.inference_mode():
  for k in range(0,1024,2):
   sl=slice(k*2048,(k+2)*2048);x=torch.from_numpy(np.array(tok[sl])).reshape(2,2048).long().cuda();y=torch.from_numpy(np.array(tok[k*2048+1:(k+2)*2048+1])).long().cuda()
   with torch.autocast('cuda',dtype=torch.bfloat16):
    _,h=m.forward_features(x);ce=torch.cat([NN.cross_entropy(NN.linear(a,m.output_weight).float(),b,reduction='none') for a,b in zip(h.reshape(-1,1024).split(128),y.split(128))])
   ll[sl]=ce.cpu().numpy();total+=float(ce.double().sum())
   if ss is not None:
    for l in range(8):ss[l,sl]=captures[l].reshape(-1,2).cpu().numpy()
 assert versions==[p._version for p in m.parameters()];assert all(torch.equal(a,b.moe.load_bias) for a,b in zip(bias,m.blocks))
 for h in hooks:h.remove()
 np.savez(out,loss=ll,**({'sel':ss} if ss is not None else {}));dump(receipt,dict(row=row,NLL=total/N,positions=N,bias_unchanged=True,model_unchanged=True,seconds=time.monotonic()-tic,**info));del m;gc.collect();torch.cuda.empty_cache();return out
def main():
 roots={'Dense':Path(json.load(open(ROOT/'evidence/checkpoint_inventory.json'))[0]['config']).parent,'MoE':R4.parent/'20261031_dense_order_aligned_moe_baseline/runs/formal','A0':R3/'runs/A0'};rows=[]
 for model,root in roots.items():
  for mp in sorted(root.glob('*/*/manifest.json')):
   z=json.load(mp.open());t=z.get('tokens_seen',0)
   if t>1000000000:continue
   f=next((a for a in z.get('files',[]) if a['path']=='state.pt'),None)
   if f is None:continue
   p=mp.parent/f['path'];rows.append(dict(model=model,tokens=t,step=z['optimizer_step'],path=str(p),exists=p.exists(),manifest=str(mp),bytes=f['size_bytes'],sha256=f['sha256'],config=str(R3/'arms/A0.yaml') if model=='A0' else str(root/'resolved_config.json')))
 inventory=pd.DataFrame(rows);table(inventory,'C_checkpoint_inventory','Boundedactualformalroots;missingstatepayloadnotassumedavailablefrommanifest. Smokesanddifferent-orderfamiliesexcluded.')
 interval_rows=[]
 for m in ['Dense','MoE']:
  for lo,hi in [(0,500000000),(500000000,1000000000)]:
   q=inventory[(inventory.model==m)&inventory.exists&(inventory.tokens>lo)&(inventory.tokens<hi)];interval_rows.append(dict(model=m,interval=f'{lo}-{hi}',interior_saved_states=len(q),status='存在可前向密点' if len(q) else '缺失：没有真实保存的更密正式状态'))
 table(pd.DataFrame(interval_rows),'C_dense_early_gaps')
 # New payloads, if actually present, are evaluated only after A/B. A0@200 is
 # a genuine saved nativeprefix, not an invented250-update checkpoint.
 new=[]
 for z in rows:
  if not z['exists']:continue
  if z['model'] in ['Dense','MoE'] and 0<z['tokens']<1000000000 and z['tokens']!=500000000:new.append(z)
  if z['model']=='A0' and z['step'] not in [0,500,1000,1500,2000]:new.append(z)
 dump(F/'evidence/C_new_forward_plan.json',new)
 if new:
  import fcntl,subprocess
  aid='checkpoint_learn_forget_followup_early_inputs_20261111'
  with (REPO/'assets/.catalog.lock').open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);p=REPO/'assets/catalog.json';c=json.load(p.open())
   if not any(a['id']==aid for a in c['assets']):
    c['assets'].append(dict(id=aid,title_cn='追加分析实际可见早期状态',category='model_checkpoint',kind='learn_forget_followup',projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=z['path'],expected='file',required=True,probes=[]) for z in new],identity=dict(manifest=str(F/'evidence/C_new_forward_plan.json')),source_paths=[str(F/'protocol_cn.md')]));q=p.with_suffix('.followup.tmp');q.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');q.replace(p)
  subprocess.run([sys.executable,str(REPO/'tools/check_assets.py'),'--strict','--asset',aid,'--output',str(F/f'evidence/C_input_access_{time.time_ns()}.json')],stdout=subprocess.DEVNULL,check=True)
 paths={}
 for row in new:
  label=row['model'];rr=dict(row,model='MoE' if label=='A0' else label);paths[label,row['step']]=forward_new(rr,label)
 e=evals('A0');target=1908;w=(np.log(target)-np.log(1750))/(np.log(2000)-np.log(1750));a0=(1-w)*e[1750]['lm_loss']+w*e[2000]['lm_loss'];baseline=json.load(open(ROOT/'evidence/forward_MoE_000500000000.json'))['NLL'];difference=a0-baseline;compatible=bool(abs(difference)<=.01)
 table(pd.DataFrame([dict(baseline_tokens=500000000,baseline_step=1908,baseline_NLL=baseline,A0_logstep_interpolated_NLL=a0,difference=difference,tolerance=.01,nearby_compatible=compatible,exact_same_token_checkpoint=False)]),'C_A0_baseline_check','Nearbyinterpolationonly;exact0.5B A0weightsabsent. Compatibilityisnotbitwiseequivalence,checkpointboundarytruncationdiffers.')
 learn={r:refmask(r) for r in REFS};state=np.zeros(N,bool);records=[];support=[]
 for step in sorted(s for s in e if s<=2000):
  p=paths.get(('A0',step),R4/f'analysis/positions/A0/step{step:06d}.npz');exists=p.exists();support.append(dict(step=step,tokens=e[step]['tokens_seen'],position_path=str(p),position_available=exists,aggregate_NLL=e[step]['lm_loss']))
  if not exists:continue
  ll=np.load(p)['loss'].astype(np.float64);state=np.where(ll<=np.log(2),True,np.where(ll>=2*np.log(2),False,state))
  for ref,mask in learn.items():records.append(dict(model='A0早期近似',tokens=e[step]['tokens_seen'],step=step,reference=ref,K=float(state[mask].mean()),NLL=e[step]['lm_loss'],nearby_compatible=compatible,source=str(p),hysteresis_checkpoint_grid='available200/500/1000/1500/2000only'))
 table(pd.DataFrame(support),'C_A0_position_availability','User-described250gridpositioncacheisnotfullypresent;aggregatesareavailablebutmasterycannotbeinferredwithoutpositions.')
 table(pd.DataFrame(records),'C_A0_early_mastery')
 plt=plotting();fig,axs=plt.subplots(1,2,figsize=(11,4.5));n=pd.read_csv(ROOT/'results/baseline_NLL_document_CI.csv');k=pd.read_csv(ROOT/'results/fig1_mastery_transitions.csv');k=k[(k.reference=='MoE33B')&(k.stratum=='overall')&(k.tokens<=1000000000)]
 for m in ['Dense','MoE']:
  z=n[n.tokens<=1000000000];axs[0].scatter(z.tokens/1e9,z[m+'_NLL'],c=COLORS[m],label=m+'实测');q=k[k.model==m];axs[1].scatter(q.tokens/1e9,q.K,c=COLORS[m],label=m+'实测')
 if compatible:
  z=pd.DataFrame(records);z=z[z.reference=='MoE33B'];axs[0].plot(z.tokens/1e9,z.NLL,'o--',color=COLORS['A0'],alpha=.65,label='A0单侧早期近似');axs[1].plot(z.tokens/1e9,z.K,'o--',color=COLORS['A0'],alpha=.65,label='A0单侧早期近似')
 for ax,y in zip(axs,['EVAL NLL（nat）','掌握率K']):ax.set(xlabel='累计训练token（B）',ylabel=y);ax.grid(alpha=.2);ax.legend(fontsize=8)
 savefig(fig,'C_早期轨迹核查','Dense没有0–0.5B内部真实保存点；A0只是单侧近似，不能制造同期Dense−MoE差。A0位置数据实际不全，迟滞使用其可见网格。')
 dump(F/'evidence/C_complete.json',dict(new_forward_states=len(new),nearby_A0_NLL_difference=difference,compatible_at_frozen_tolerance=compatible,Dense_dense_early_checkpoint_missing=not any(z['model']=='Dense' for z in new),all_no_training=True));event('C','更密正式状态核查、实际可用A0早期前向和近邻一致性核验完成',new_forward_states=len(new),A0_difference=difference)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
