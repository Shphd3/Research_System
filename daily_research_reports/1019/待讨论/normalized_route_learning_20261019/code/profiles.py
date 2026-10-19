from common import *
import ast,argparse

def decoder():
 src=ast.parse((PREV/'scripts/visual_dispatch.py').read_text());node=next(n for n in src.body if isinstance(n,ast.ClassDef) and n.name=='FrozenByteLevelDecoder');ns={'Path':Path,'json':json};exec(compile(ast.Module(body=[node],type_ignores=[]),'<reused_frozen_decoder>','exec'),ns);return ns['FrozenByteLevelDecoder'](BASE)
def run(device):
 configure(device);t0=time.time();rec=json.load(open(OLD/'provenance/cache_preparation_receipt.json'));ck=torch.load(rec['inputs']['crosscoder_checkpoint'],map_location='cpu',mmap=True,weights_only=False);dec=ck['crosscoder']['decoder'][-1].float();bias=ck['crosscoder']['decoder_bias'][-1].float();norm=ck['normalization'];assert norm['rms_target']==1 and norm['centering'];rms=norm['rms'][-1].item();mean=norm['train_mean'][-1].float();norms=dec.norm(dim=-1).numpy();dd=dec.to(device);bb=bias.to(device);mm=mean.to(device);st=stats();p=st['p'];L=st['low'];top=st['top10'];lowset=set(L.tolist());topset=set(top.tolist());tok=decoder();profiles=[];rank=[];contrib=[];amplitudes=[];recons=[];windows=[];owners=np.load(PREV/'metrics/core/owners.npz');mu=json.load(open(ROOT/'provenance/denominators.json'))['groups']
 for split in ['train','eval']:
  c=loadcache(split);z=csr(c);pos=c['position_id'].numpy();blocks=c['block_id'].numpy();N=len(pos);source=rec['inputs']['sources'][0 if split=='train' else 1]['path'];tokens=np.memmap(source,dtype=np.uint32,mode='r');order=np.argsort(pos,kind='stable');chosen=None;fallback=None
  for a in range(len(order)-63):
   ix=order[a:a+64]
   if blocks[ix[0]]!=blocks[ix[-1]] or not np.array_equal(pos[ix],np.arange(pos[ix[0]],pos[ix[0]]+64)):continue
   if fallback is None:fallback=ix.copy()
   if (z[ix][:,L].getnnz(axis=0)>0).sum()>=2:chosen=ix.copy();break
  if chosen is None:chosen=fallback
  if chosen is None:raise ValueError('No complete contiguous64 window')
  ix=chosen;zw=z[ix].toarray();cw=zw*norms;categories=[('top10',top,4),('other',np.array([i for i in range(FCOUNT) if i not in topset and i not in lowset]),4),('low',L,8)];selected=[]
  for category,ids,limit in categories:
   eligible=[i for i in ids if zw[:,i].max()>0];pick=sorted(eligible,key=lambda i:(-float(cw[:,i].max()),int(i)))[:limit]
   selected.extend(pick)
  selected=sorted(selected,key=lambda i:(p[i],int(i)));rawids=np.asarray(tokens[pos[ix]],dtype=np.int64);off=int(pos[ix[0]]);window=dict(split=split,source=source,rows=ix.tolist(),feature_ids=[int(i) for i in selected],start=off,context=int(blocks[ix[0]]),token_ids=rawids.tolist(),raw_tokens=tok.convert_ids_to_tokens(rawids),text=tok.decode(rawids.tolist()),visible_prefix_before_window=tok.decode(np.asarray(tokens[off-off%1024:off],dtype=np.int64).tolist()),fallback_no_two_L=not((zw[:,L].max(0)>0).sum()>=2))
  windows.append(window);np.savez_compressed(ROOT/'cache'/f'profile_{split}.npz',rows=ix,feature_ids=selected,z=zw[:,selected],c=cw[:,selected],p=p[selected],position=pos[ix],token_ids=rawids)
  for k,row in enumerate(ix):
   for i in np.flatnonzero(zw[k]):
    profiles.append(dict(split=split,cache_row=int(row),context=int(blocks[row]),position=int(pos[row]),feature_id=int(i),train_p=p[i],z=float(zw[k,i]),c28=float(cw[k,i]),a_route=float(zw[k,i]*st['weights'][i]),selected_display=int(i in selected),token=tok.convert_ids_to_tokens([rawids[k]])[0]))
  for i in selected:
   if i not in lowset:continue
   ordering=sorted(range(64),key=lambda k:(-float(cw[k,i]),int(pos[ix[k]])))
   for j,k in enumerate(ordering):
    row=ix[k];po=int(pos[row]);start=po-po%1024
    rank.append(dict(split=split,feature_id=int(i),rank=j+1,position=po,train_p=p[i],z=float(zw[k,i]),c28=float(cw[k,i]),current=tok.decode([int(tokens[po])]),previous2=tok.decode(np.asarray(tokens[max(start,po-2):po],dtype=np.int64).tolist()),following2=tok.decode(np.asarray(tokens[po+1:min(start+1024,po+3)],dtype=np.int64).tolist()),following_posthoc_only=True))
  for group in ['T','R11']:
   labels=owners[group];sizes=np.bincount(labels[labels>=0],minlength=8)
   for s in range(4):
    saved=np.load(ROOT/'routes'/f'{split}_{group}_S{s}.npz');scores=saved['score'][ix];route=saved['route'][ix]
    for k,row in enumerate(ix):
     for e in range(8):
      ids=np.flatnonzero((labels==e)&(zw[k]>0));a=zw[k,ids]*st['weights'][ids]
      if s==1:a=a/max(mu[group]['mu'][e],mu[group]['floor']) if mu[group]['mu'][e]>0 else a*0
      elif s==2:a=a*st['invm'][ids]
      elif s==3:a=a*st['invpm'][ids]
      ordera=sorted(range(len(ids)),key=lambda j:(-a[j],int(ids[j])))[:5]
      contrib.append(dict(split=split,position=int(pos[row]),grouping=group,score=f'S{s}',expert=e,group_size=int(sizes[e]),group_score=float(scores[k,e]),selected=int(route[k]),top_feature_ids=';'.join(str(int(ids[j])) for j in ordera),top_score_terms=';'.join(str(float(a[j]/sizes[e])) for j in ordera),top_c28=';'.join(str(float(cw[k,ids[j]])) for j in ordera)))
  for group,ff in [('low',L),('high',st['high'])]:
   vals=z[:,ff].data;ids=z[:,ff].indices
   for quantity,mult in [('z',np.ones(len(ff))),('c28',norms[ff]),('a_route',st['weights'][ff])]:
    v=vals*mult[ids];q=np.quantile(v,[.25,.5,.75]) if len(v) else [None]*3;amplitudes.append(dict(split=split,group=group,quantity=quantity,unit='positive activation events, pooled',positive_event_N=len(v),feature_N=len(ff),q25=q[0],median=q[1],q75=q[2],zero_hit_features=int((z[:,ff].getnnz(axis=0)==0).sum())))
   cz=z[:,ff].tocsc()
   for j,i in enumerate(ff):
    vv=cz.data[cz.indptr[j]:cz.indptr[j+1]]
    if len(vv):
     q=np.quantile(vv,[.25,.5,.75]);amplitudes.append(dict(split=split,group=group,quantity=f'feature_z_{i}',unit='one feature conditional positives',positive_event_N=len(vv),feature_N=1,q25=q[0],median=q[1],q75=q[2],zero_hit_features=0))
    else:amplitudes.append(dict(split=split,group=group,quantity=f'feature_z_{i}',unit='one feature conditional positives',positive_event_N=0,feature_N=1,q25=None,median=None,q75=None,zero_hit_features=1))
  # Exact dictionary coordinates; dense batch only, original sparse cache reused.
  totals=dict(raw_error_sq=0.,raw_h_sq=0.,raw_hat_sq=0.,normalized_error_sq=0.,normalized_h_sq=0.)
  with torch.no_grad():
   for a in range(0,N,512):
    zz=torch.from_numpy(z[a:a+512].toarray()).to(device);hh=c['hidden'][a:a+512].to(device).float();hat=zz@dd+bb;hh_norm=(hh-mm)/rms;rawhat=hat*rms+mm
    vals=[(rawhat-hh).square().sum(),hh.square().sum(),rawhat.square().sum(),(hat-hh_norm).square().sum(),hh_norm.square().sum()]
    for key,v in zip(totals,vals):totals[key]+=float(v)
  recons.append(dict(split=split,N=N,decoder_layer='block28 residual-post',inverse='raw_hat=normalized_hat*rms28+TRAINmean28',rms28=rms,raw_relative_squared_error=totals['raw_error_sq']/totals['raw_h_sq'],centered_relative_squared_error=totals['normalized_error_sq']/totals['normalized_h_sq'],raw_h_L2_RMS=math.sqrt(totals['raw_h_sq']/N),raw_hat_L2_RMS=math.sqrt(totals['raw_hat_sq']/N),computation='FP32 sparse-cache densification batch512 @ FP32 D28, TF32 disabled',**totals));print('PROFILE',split,recons[-1],flush=True)
 csvwrite(ROOT/'tables/feature_text_profiles.csv',profiles);csvwrite(ROOT/'tables/low_window_rankings.csv',rank);csvwrite(ROOT/'tables/fixed_text_score_contributors.csv',contrib);csvwrite(ROOT/'tables/conditional_amplitudes.csv',amplitudes);csvwrite(ROOT/'tables/reconstruction28.csv',recons);write_json(ROOT/'texts/fixed_windows.json',windows);write_json(ROOT/'provenance/profiles_receipt.json',dict(status='COMPLETE',seconds=time.time()-t0,z_c_frozen=True,no_transformer_forward=True,reconstruction=recons,selected_windows=[{k:v for k,v in w.items() if k not in ['raw_tokens','token_ids','text','visible_prefix_before_window']} for w in windows]))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--device',default='cuda:0');a=ap.parse_args();run(a.device)
