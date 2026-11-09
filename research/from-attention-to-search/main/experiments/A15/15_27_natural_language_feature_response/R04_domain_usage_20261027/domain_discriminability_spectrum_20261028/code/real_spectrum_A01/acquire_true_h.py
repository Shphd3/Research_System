"""Authorized <=124 existing-resource forwards: original native Runner, true hooks only saved."""
from pathlib import Path
import json,importlib.util,hashlib,time,os
import numpy as np
O=Path(__file__).resolve().parent;S=O.parent;R=S.parent

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(8<<20),b''):h.update(b)
    return h.hexdigest()

def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def old_z(row,name):
    q=np.load(R/'forward/documents'/f"{row['seq_id']}.npz");F=30000 if name=='SAE' else 16384
    z=np.zeros((len(row['token_ids']),F),dtype=np.float32)
    for t in range(len(z)):
        a,b=q[name+'_ptr'][t:t+2];z[t,q[name+'_ids'][a:b]]=q[name+'_z'][a:b]
    return z

def main():
    spec=json.loads((O/'amendment.json').read_text());assert sha(S/'config.json')==spec['parent_config_sha256'];assert sha(S/'analysis/candidate_freeze.json')==spec['candidate_freeze_sha256'];src=Path(spec['source_forward_loader']);assert sha(src)==spec['source_forward_loader_sha256']
    modspec=importlib.util.spec_from_file_location('r04_frozen_native',src);m=importlib.util.module_from_spec(modspec);modspec.loader.exec_module(m)
    # Only output/ledger addresses are rebound. Native model/normalization/encoding implementation is unchanged.
    m.R=O;m.O=O/'forward';m.O.mkdir(exist_ok=True)
    docs=[json.loads(s) for s in (R/'data/documents.jsonl').read_text().splitlines()];assert len(docs)==120
    ledger=O/'forward_ledger.jsonl'
    def charged(row,purpose,cut=None):
        n=len(ledger.read_text().splitlines()) if ledger.exists() else 0
        assert n<spec['new_forward_cap'],(n,'CAP')
        return runner.call(row,purpose,cut=cut)
    t=time.time();dump(O/'started.json',{'started_at_utc':m.now(),'pid':os.getpid(),'script_sha256':sha(__file__),'amendment_sha256':sha(O/'amendment.json'),'original_loader_sha256':sha(src),'scope':'120sameR04docs+4checks;no new tasks/resources/training','transformers':m.__import__('transformers').__version__ if hasattr(m,'__import__') else __import__('transformers').__version__})
    runner=m.Runner();comparisons=[]
    for i,row in enumerate(docs):
        p=O/'raw_documents'/f"{row['seq_id']}.npz"
        if p.exists():raise RuntimeError('Existing true-h output: explicit resume required, no duplicate forward')
        res=charged(row,'A01_true_h_documents')
        for name in ['SAE','CC']:
            old=old_z(row,name);c=m.cmp(res[name],old);comparisons.append({'seq_id':row['seq_id'],'dictionary':name,**c});assert c['pass'],comparisons[-1]
        assert res['SAE_h'].shape==res['CC_h'].shape==(192,1024)
        assert np.isfinite(res['SAE_h']).all() and np.isfinite(res['CC_h']).all()
        np.savez_compressed(p,token_ids=np.array(row['token_ids'],dtype=np.int32),SAE_h=res['SAE_h'],CC_h=res['CC_h'],SAE_nmse=res['SAE_nmse'],CC_nmse=res['CC_nmse'])
        if i==0 or (i+1)%12==0:
            dump(O/'progress.json',{'documents_done':i+1,'total_documents':120,'charged':len(ledger.read_text().splitlines()),'elapsed_seconds':time.time()-t,'all_z_comparisons_pass':all(v['pass'] for v in comparisons)})
            print(json.dumps({'documents_done':i+1,'seconds':round(time.time()-t,1),'latest_z_checks':comparisons[-2:]}),flush=True)
        del res,old
    checks=[]
    math=next(x for x in docs if x['split']=='discovery' and x['label']==1);bio=next(x for x in docs if x['split']=='discovery' and x['label']==0)
    for kind,row,cut in [('repeat',math,None),('repeat',bio,None),('visible_prefix',math,128),('visible_prefix',bio,128)]:
        res=charged(row,'A01_check_'+kind,cut=cut);saved=np.load(O/'raw_documents'/f"{row['seq_id']}.npz");n=192 if cut is None else cut
        for name in ['SAE','CC']:
            a=res[name+'_h'];b=saved[name+'_h'][:n];rel=float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-12));assert rel<=.02
            z=m.cmp(res[name],old_z(row,name)[:n]);assert z['pass']
            checks.append({'kind':kind,'seq_id':row['seq_id'],'dictionary':name,'relative_h_error':rel,'z':z,'pass':True})
        del res
    assert runner.unchanged()
    charged_n=len(ledger.read_text().splitlines());assert charged_n==124
    result={'completed_at_utc':m.now(),'documents':120,'checks_forwards':4,'charged_forwards':charged_n,'cap':124,'remaining':0,'old_R04_forwards':456,'R04_plus_supplement_forwards':456+charged_n,'original_budget_not_rewritten':True,'raw_arrays_per_hook':[120,192,1024],'measured_arrays_per_hook':[120,160,1024],'old_z_comparisons':comparisons,'checks':checks,'all_checks_pass':True,'max_original_z_relative_error':max(v['relative_z_error'] for v in comparisons),'min_original_z_support_jaccard':min(v['support_jaccard'] for v in comparisons),'buffers_unchanged':True,'parameters_updated':0,'new_tasks_resources':0,'elapsed_seconds':time.time()-t,'peak_GPU_bytes':m.torch.cuda.max_memory_allocated(),'torch':m.torch.__version__,'transformers':__import__('transformers').__version__,'GPU':str(m.torch.cuda.get_device_properties(0)),'training':0,'TEST':False}
    dump(O/'completed.json',result);print('ACQUISITION_COMPLETE',charged_n,'seconds',round(time.time()-t,1),flush=True)

if __name__=='__main__':main()
