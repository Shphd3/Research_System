from common import *
import torch,importlib.util,sys
def load_saes():
 cfg=json.load(open(R/'config.json'));out={}
 for site,s in cfg['sites'].items():
  assert sha(s['path'])==s['sha256'] and sha(s['loader'])==s['loader_sha256'];spec=importlib.util.spec_from_file_location('r20_native_'+site,s['loader']);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);sae=mod.TopKSAE.from_pretrained(s['path'],map_location='cpu').eval().requires_grad_(False);assert (sae.d_model,sae.n_latents,sae.k)==(1024,30000,32);out[site]=sae
 return out
def assert_freeze():
 for path,h in json.load(open(R/'evidence/freeze.json'))['hashes'].items():assert sha(path)==h,path
def encode_one(sae,x):
 with torch.inference_mode():
  values,indices,z,pre=sae.encode_topk(x);vv,ii=torch.nn.functional.linear(x,sae.encoder.weight,sae.encoder.bias).relu().topk(32,sorted=False);assert torch.equal(z,torch.zeros_like(z).scatter(-1,ii,vv));cut=pre.relu().topk(33,sorted=True).values;rec=sae.decoder(z);assert int(torch.count_nonzero(z))==32
  return dict(h=x.numpy(),indices=indices.numpy(),values=values.numpy(),pre_relu=pre.relu().numpy(),cutoff32=cut[:,31].numpy(),cutoff33=cut[:,32].numpy(),reconstruction=rec.numpy(),relative_reconstruction_error=np.array([float((rec-x).norm()/x.norm())]))
