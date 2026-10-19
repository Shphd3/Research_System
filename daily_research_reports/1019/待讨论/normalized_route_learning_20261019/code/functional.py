from common import *
import argparse

def run(name,seed,device,spectra=False):
 configure(device,seed);out=ROOT/f'training/{name}/seed{seed}';dest=ROOT/f'functional/{name}/seed{seed}';dest.mkdir(parents=True,exist_ok=True)
 if not (out/'complete.json').exists():write_json(dest/'status.json',dict(status='NOT RUN',reason='endpoint not complete'));return
 marker=dest/('spectra_complete.json' if spectra else 'complete.json')
 if marker.exists():return
 t0=time.monotonic();co=condition(name);m=Branch(seed,co['router']=='learned').to(device);init=cpu_tree(m.experts.state_dict());m.load_state_dict(torch.load(out/'epoch3.pt',map_location='cpu',weights_only=False)['model']);c=loadcache('eval');ix=np.load(ROOT/'config/probe.npy');head=FrozenHead(device);h=c['hidden'][ix].to(device).float();y=c['target'][ix].to(device);low=c['mask_low'][ix].numpy();fixed=torch.as_tensor(routes('eval',name)[ix],device=device) if m.router is None else None
 with torch.no_grad():natural_r,natural_g,_=m.routing(h,fixed)
 if not spectra:
  nll=[];swap=[];responses=[];row=[];base,_,_=evaluate(None,head,c,device,indices=ix);natural,_,_=evaluate(m,head,c,device,name,indices=ix)
  for e in range(8):
   force,_,_=evaluate(m,head,c,device,name,indices=ix,force=e,gate_override=1.);ss,_,_=evaluate(m,head,c,device,name,indices=ix,force=e);nll.append(force);swap.append(ss)
   with torch.no_grad(),torch.autocast(device_type='cuda',dtype=torch.bfloat16):response=m.experts[e](h/m.scale).float()*m.scale
   responses.append(response.cpu().numpy());row.append(dict(condition=name,seed=seed,expert=e,probe_N=len(ix),probe_L_N=int(low.sum()),forced_gate=1.,force_NLL=float(force.mean()),force_L_NLL=float(force[low].mean()),forced_output_L2_mean=float(response.norm(dim=-1).mean()),swap_preserve_natural_gate_delta=float((ss-natural).mean()),swap_L_delta=float((ss[low]-natural[low]).mean()),zero_branch_delta=float((base-natural).mean()),zero_branch_L_delta=float((base[low]-natural[low]).mean())))
  rr=np.stack(responses);cos=np.empty((8,8));
  for a in range(8):
   for b in range(8):
    aa=rr[a];bb=rr[b];norm=np.linalg.norm(aa,axis=1)*np.linalg.norm(bb,axis=1);v=np.divide((aa*bb).sum(1),norm,out=np.full(len(ix),np.nan),where=norm>0);cos[a,b]=np.nanmean(v) if np.isfinite(v).any() else np.nan
  np.savez_compressed(dest/'probe.npz',rows=ix,natural_nll=natural,base_nll=base,forced_nll=nll,swap_nll=swap,responses=rr,cosine=cos,natural_route=natural_r.cpu().numpy(),natural_gate=natural_g.cpu().numpy(),low=low);csvwrite(dest/'expert_probe.csv',row)
 else:
  spectralrows=[];arrays={}
  for ei,e in enumerate(m.experts):
   for nm in ['gate','up','down']:
    W=getattr(e,nm).weight.detach().float();W0=init[f'{ei}.{nm}.weight'].to(device);delta=W-W0;data={}
    for kind,mat in [('initial',W0),('final',W),('delta',delta)]:
     energy=float(mat.square().sum())
     if energy==0:sv=np.zeros(D)
     elif nm=='down' and kind=='delta':sv=data['final']
     else:sv=torch.linalg.svdvals(mat,driver='gesvd').cpu().numpy().astype(np.float64)
     data[kind]=sv;arrays[f'e{ei}_{nm}_{kind}']=sv;share=sv**2/energy if energy>0 else np.full_like(sv,np.nan)
     spectralrows.append(dict(condition=name,seed=seed,expert=ei,matrix=f'W_{nm}',version=kind,full_singular_count=len(sv),frobenius=math.sqrt(energy),full_energy=energy,top16_energy_fraction=float(np.nansum(share[:16])) if energy>0 else None,top16_singular_values=';'.join(map(str,sv[:16])),normalization='sigma_squared / FULL Frobenius_squared; zero=NA'))
   with torch.no_grad(),torch.autocast(device_type='cuda',dtype=torch.bfloat16):rr=e(h/m.scale).float()*m.scale
   centered=rr.double()-rr.double().mean(0);cov=centered.T@centered/(len(ix)-1);eig=torch.linalg.eigvalsh(cov).flip(0).clamp_min(0).cpu().numpy();arrays[f'e{ei}_response_centered_covariance_eigenvalues']=eig;energy=float(eig.sum());spectralrows.append(dict(condition=name,seed=seed,expert=ei,matrix='response centered covariance, rows=fixed probe positions, uniform weights',version='final',full_singular_count=len(eig),frobenius=None,full_energy=energy,top16_energy_fraction=float(eig[:16].sum()/energy) if energy>0 else None,top16_singular_values=';'.join(map(str,eig[:16])),normalization='eigenvalue / FULL covariance trace, units=(raw residual amplitude)^2'))
  csvwrite(dest/'spectra.csv',spectralrows);np.savez_compressed(dest/'full_spectra.npz',**arrays)
 write_json(marker,dict(status='COMPLETE',condition=name,seed=seed,seconds=time.monotonic()-t0,probe_N=len(ix),paired_same_input=True,**memory(device)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('--seed',type=int,required=True);ap.add_argument('--device',default='cuda:0');ap.add_argument('--spectra',action='store_true');a=ap.parse_args();run(a.name,a.seed,a.device,a.spectra)
