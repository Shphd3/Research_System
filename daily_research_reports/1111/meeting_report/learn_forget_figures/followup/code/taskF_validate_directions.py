from fu import *
from threadpoolctl import threadpool_limits
folder=F/'data/F';NS=262144

def main():
 tic=time.monotonic();sample=json.load(open(folder/'samples.json'))['EVAL'];positions=np.concatenate([np.arange(s*2048,(s+1)*2048) for s in sample]);dc=codes('EVAL');ii=dc['indices'].numpy()[positions];good=dc['values'].numpy()[positions]>0;rr=np.broadcast_to(np.arange(NS,dtype=np.int32)[:,None],ii.shape)[good];Z=sparse.csr_matrix((np.ones(good.sum(),np.float64),(rr,ii[good])),shape=(NS,30000));features=pd.read_csv(F/'results/F_subspace_features.csv');rows=[]
 for arm in ['Dense','A0','A5','A2']:
  h=np.load(folder/f'h_{arm}_EVAL.npy',mmap_mode='r')
  for layer in range(8):
   X=np.asarray(h[layer],dtype=np.float64);ss=features[features.band=='low'];z=Z[:,ss.atom];cnt=np.asarray(z.sum(0)).ravel();p=ss.DEV_sample_support.to_numpy()/NS;B=np.asarray(z.T@X);B-=cnt[:,None]*X.mean(0);B/=NS*np.sqrt(p*(1-p))[:,None];total=float(np.sum(B*B));q=np.load(folder/f'Q_{arm}_{layer}_low.npy')[:,:64];qn=np.load(folder/f'Q_{arm}_{layer}_null.npy')[:,:64];e=float(np.sum((B@q)**2))/max(total,1e-30);en=float(np.sum((B@qn)**2))/max(total,1e-30);over=float(np.sum((q.T@qn)**2)/64);rows.append(dict(arm=arm,layer=layer,low_features=len(ss),heldout_low_crosscov_energy_fraction_Qlow=e,heldout_low_crosscov_energy_fraction_Qnull=en,heldout_energy_ratio=e/max(en,1e-30),subspace_overlap_fraction=over));del X,B
  print('F_HELDOUT',arm,flush=True)
 table(pd.DataFrame(rows),'F_direction_heldout_validation','Q固定由DEV定义；EVAL交叉协方差沿同一DEV标签方差归一化，比较低频方向与DEV标签打乱方向。能量占比接近不能当作低频专属方向证据。');dump(F/'evidence/F_direction_validation_complete.json',dict(seconds=time.monotonic()-tic,arms=4,layers=8,training_updates=0))
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
