from fu import *
from threadpoolctl import threadpool_limits
import gc
folder=F/'data/F';DIM=1024;NS=128*2048

def labels():
 samples=json.load(open(folder/'samples.json'));d=codes('DEV');ids=np.concatenate([np.arange(s*2048,(s+1)*2048) for s in samples['DEV']]);ii=d['indices'].numpy()[ids];good=d['values'].numpy()[ids]>0;rr=np.broadcast_to(np.arange(NS,dtype=np.int32)[:,None],ii.shape)[good];Z=sparse.csr_matrix((np.ones(good.sum(),np.float64),(rr,ii[good])),shape=(NS,30000));counts=np.asarray(Z.sum(0)).ravel();fb,_,_=metadata();out={};rows=[]
 for name,mask in [('low',fb<=2),('high',fb>=7)]:
  js=np.flatnonzero(mask&(counts>=20));out[name]=Z[:,js].tocsr();p=counts[js]/NS
  for j in js:rows.append(dict(band=name,atom=int(j),bin=int(fb[j]),DEV_sample_support=int(counts[j])))
 table(pd.DataFrame(rows),'F_subspace_features','DEV固定所抽样本上支撑至少20；低/高频由原有teacher bins指定，不在EVAL挑方向。');return out

def basis(X,Z,null=False):
 if null:X=X[np.random.default_rng(20261118).permutation(NS)]
 counts=np.asarray(Z.sum(0)).ravel();p=counts/NS;B=np.asarray(Z.T@X,dtype=np.float64);B-=counts[:,None]*X.mean(0)[None,:];B/=NS*np.sqrt(p*(1-p))[:,None];b=torch.from_numpy(B).double().cuda();C=b.T@b;v,q=torch.linalg.eigh((C+C.T)/2);q=q[:,-128:].flip(1);return q,v[-128:].flip(0).cpu().numpy()

def statistics(C,mean,global_mean,ne,Q,identity):
 C=(C+C.T)/2;ev=torch.linalg.eigvalsh(C);minraw=float(ev[0]);ev=ev.clamp_min(0).flip(0);tr=float(ev.sum());p=ev/max(tr,1e-30);nonzero=p>0;rH=float(torch.exp(-(p[nonzero]*p[nonzero].log()).sum()));rPR=float(1/(p*p).sum());d90=int(torch.searchsorted(p.cumsum(0),torch.tensor(.9,device='cuda',dtype=torch.float64)))+1;row=dict(**identity,n=ne,trace=tr,effective_rank=rH,participation_rank=rPR,d90=d90,top1_variance_fraction=float(p[0]),bottom512_variance_fraction=float(p[-512:].sum()),normalized_entropy=float(np.log(rH)/np.log(DIM)),min_raw_eigenvalue=minraw)
 delta=mean-global_mean;row['mean_shift_norm2']=float((delta*delta).sum());Ct=C*((ne-1)/ne)+delta[:,None]*delta[None,:];trt=float(torch.trace(Ct))
 for name,q in Q.items():
  for k in ([64] if name=='null' else [32,64,128]):
   z=q[:,:k];row[f'{name}_mean_shift_energy_{k}']=float(((z.T@delta)**2).sum());row[f'{name}_variance_fraction_{k}']=float((z*(C@z)).sum())/max(tr,1e-30);row[f'{name}_second_moment_fraction_{k}']=float((z*(Ct@z)).sum())/max(trt,1e-30)
 return row,ev.cpu().numpy()

def analyse_arm(arm,Z):
 receipt=F/f'evidence/F_analysis_{arm}.json'
 if receipt.exists():return
 tic=time.monotonic();hd=np.load(folder/f'h_{arm}_DEV.npy',mmap_mode='r');he=np.load(folder/f'h_{arm}_EVAL.npy',mmap_mode='r');rows=[];evals={};basisvals=[];selection={a:np.load(folder/f'sel_{a}_EVAL.npy',mmap_mode='r') for a in ['A0','A5','A2']};perm=np.random.default_rng(20261117).permutation(NS)
 for layer in range(8):
  X=np.asarray(hd[layer],dtype=np.float64);Q={}
  for name,z in [('low',Z['low']),('high',Z['high']),('null',Z['low'])]:
   Q[name],vv=basis(X,z,null=name=='null');np.save(folder/f'Q_{arm}_{layer}_{name}.npy',Q[name].cpu().numpy());basisvals +=[dict(arm=arm,layer=layer,band=name,rank=k+1,DEV_cross_cov_eigenvalue=float(v)) for k,v in enumerate(vv)]
  del X;xx=torch.from_numpy(np.array(he[layer])).double().cuda();mu=xx.mean(0);xc=xx-mu;cg=xc.T@xc/(NS-1);globalrow,e=statistics(cg,mu,mu,NS,Q,dict(arm=arm,layer=layer,route='global',condition='global',expert=-1,view='own'));globalrow['spectrum_L1_to_own_global']=0.;globalrow['spectrum_L1_to_Dense_global']=float(np.abs(e/e.sum()-np.load(folder/'eigenvalues_Dense.npz')[f'Dense_L{layer}_global']/np.load(folder/'eigenvalues_Dense.npz')[f'Dense_L{layer}_global'].sum()).sum()) if arm!='Dense' else 0.;rows.append(globalrow);evals[f'{arm}_L{layer}_global']=e;del xc
  if arm!='Dense':
   routes=['A0','A5','A2'] if arm=='A0' else [arm]
   for route in routes:
    ss=np.asarray(selection[route][layer]);view='own' if route==arm else 'common_A0'
    for mode in ['actual','shuffled']:
     labels=ss if mode=='actual' else ss[perm]
     for expert in range(8):
      mask=np.any(labels==expert,axis=1);ne=int(mask.sum());yy=xx[torch.from_numpy(mask).cuda()];me=yy.mean(0);yy-=me;cc=yy.T@yy/(ne-1);r,ee=statistics(cc,me,mu,ne,Q,dict(arm=arm,layer=layer,route=route,condition=mode,expert=expert,view=view));r['spectrum_L1_to_own_global']=float(np.abs(ee/ee.sum()-e/e.sum()).sum());denseev=np.load(folder/'eigenvalues_Dense.npz')[f'Dense_L{layer}_global'];r['spectrum_L1_to_Dense_global']=float(np.abs(ee/ee.sum()-denseev/denseev.sum()).sum());rows.append(r)
      if mode=='actual' and view=='own':evals[f'{arm}_L{layer}_e{expert}']=ee
      del yy,cc
  print('F_SPECTRUM',arm,layer,'seconds',round(time.monotonic()-tic),flush=True);del xx,cg,Q;gc.collect();torch.cuda.empty_cache()
 table(pd.DataFrame(rows),f'raw/F_statistics_{arm}');table(pd.DataFrame(basisvals),f'F_DEV_basis_{arm}');np.savez(folder/f'eigenvalues_{arm}.npz',**evals);dump(receipt,dict(arm=arm,seconds=time.monotonic()-tic,layers=8,statistics=len(rows),training_updates=0));event('F谱统计',arm+' 完成全部层/条件谱与低频方向',seconds=time.monotonic()-tic)

def finish():
 tables=[pd.read_csv(F/f'results/raw/F_statistics_{arm}.csv') for arm in ['Dense','A0','A5','A2']];D=pd.concat(tables,ignore_index=True);globalmap=D[D.condition=='global'].set_index(['arm','layer']);cols=[c for c in D.columns if c.endswith('_variance_fraction_64') or c.endswith('_second_moment_fraction_64')];D['rank_ratio_to_global']=[r.effective_rank/globalmap.loc[(r.arm,r.layer),'effective_rank'] for r in D.itertuples()]
 for col in cols:D[col.replace('_fraction_','_amplification_')]=[r/globalmap.loc[(a,l),col] for r,a,l in zip(D[col],D.arm,D.layer)]
 table(D,'F_statistics','全局和逐expert条件统计；shuffle保留所选EVAL样本中每层硬负载/Top2集合分布。放大量对该模型本层全局基线。');combined={}
 for a in ['Dense','A0','A5','A2']:
  d=np.load(folder/f'eigenvalues_{a}.npz');combined.update({k:d[k] for k in d.files})
 table(pd.DataFrame(dict(eigenvalue_rank=np.arange(1,1025),**combined)),'raw/F_eigenvalues','逐层完整1024维特征值；列名含臂/层/expert或global。控制条件完整指标见F_statistics，控制全谱不作大表重复。')
 rows=[]
 for keys,z in D[D.condition!='global'].groupby(['arm','layer','route','condition','view']):
  arm,layer,route,condition,view=keys;r=dict(arm=arm,layer=layer,route=route,condition=condition,view=view,experts=len(z),min_n=int(z.n.min()),max_n=int(z.n.max()))
  for col in ['effective_rank','rank_ratio_to_global','low_variance_amplification_64','high_variance_amplification_64','null_variance_amplification_64','top1_variance_fraction','normalized_entropy','spectrum_L1_to_own_global','spectrum_L1_to_Dense_global']:
   r[col+'_median']=float(z[col].median());r[col+'_weighted']=float(np.average(z[col],weights=z.n))
  rows.append(r)
 S=pd.DataFrame(rows);table(S,'F_layer_summary');decomp=[]
 for keys,z in D[D.condition!='global'].groupby(['arm','layer','route','condition','view']):
  arm,layer,route,condition,view=keys;g=globalmap.loc[(arm,layer)];ww=z.n.to_numpy()/(2*NS);within=float(np.sum(ww*(z.n-1)/z.n*z.trace));between=float(np.sum(ww*z.mean_shift_norm2));glob=float(g.trace*(NS-1)/NS);decomp.append(dict(arm=arm,layer=layer,route=route,condition=condition,view=view,within_trace_fraction=within/glob,between_trace_fraction=between/glob,covariance_trace_identity_relative_error=abs(within+between-glob)/glob))
 table(pd.DataFrame(decomp),'F_total_covariance_decomposition','每位置Top2计两次，expert混合权重n_e/(2N)；以总体形式协方差验证全局=条件内+条件均值间。并非训练因果。');rules=[]
 for view in ['own','common_A0']:
  for l in range(8):
   rr={}
   for route in ['A0','A5','A2']:
    z=S[(S.layer==l)&(S.route==route)&(S.condition=='actual')&((S.arm==route) if view=='own' else (S.arm=='A0'))];rr[route]=z.iloc[0]
   rank={a:float(r.rank_ratio_to_global_median) for a,r in rr.items()};amp={a:float(r.low_variance_amplification_64_median) for a,r in rr.items()};rankok=rank['A5']<rank['A0']<rank['A2'];ampok=amp['A5']>amp['A0'] and amp['A5']>amp['A2'];rules.append(dict(view=view,layer=l,rank_order_A5_native_A2=bool(rankok),low_amplification_A5_greatest=bool(ampok),joint_order=bool(rankok and ampok),**{a+'_rank_ratio':rank[a] for a in rank},**{a+'_low_amplification':amp[a] for a in amp}))
 table(pd.DataFrame(rules),'F_prediction_rules','逐层按跑前顺序检查；原生即A0。是否超过其标签shuffle噪声基线另读F_layer_summary；不能从跨臂谱直接推出训练因果。')
 plt=plotting();fig,axs=plt.subplots(1,3,figsize=(16,4.8))
 for ax,l in zip(axs,[0,4,7]):
  for arm in ['Dense','A0','A5','A2']:
   if arm=='Dense':arr=np.array([combined[f'{arm}_L{l}_global']])
   else:arr=np.stack([combined[f'{arm}_L{l}_e{e}'] for e in range(8)])
   arr=arr/arr.sum(1,keepdims=True);med=np.median(arr,axis=0);x=np.arange(1,1025);ax.plot(x,med,label=arm+('全局' if arm=='Dense' else '条件中位'),color=COLORS[arm]);ax.fill_between(x,np.quantile(arr,.1,axis=0),np.quantile(arr,.9,axis=0),color=COLORS[arm],alpha=.1)
  ax.set(xscale='log',yscale='log',xlabel='特征值序号',ylabel='特征值 / 总方差',title=f'第{l}层 FFN输入');ax.grid(alpha=.2);ax.legend(fontsize=8)
 savefig(fig,'F_条件协方差谱','Dense为0.5B实测，各MoE臂为2000步0.524288B；全局/逐expert条件分别扣均值。阴影是8个expert的10–90分位，不是种子CI。归一化谱越平，熵有效秩越高，不能同时解释成低秩。')
 fig,axs=plt.subplots(2,2,figsize=(12,9))
 for row,view in enumerate(['own','common_A0']):
  for arm in ['A0','A5','A2']:
   z=S[(S.route==arm)&(S.condition=='actual')&((S.arm==arm) if view=='own' else (S.arm=='A0'))].sort_values('layer');axs[row,0].plot(z.layer,z.rank_ratio_to_global_median,'o-',label=arm,color=COLORS[arm]);axs[row,1].plot(z.layer,z.low_variance_amplification_64_median,'o-',label=arm,color=COLORS[arm])
  for ax in axs[row]:ax.axhline(1,color='gray',ls='--');ax.grid(alpha=.2);ax.legend();ax.set_xlabel('FFN层编号')
  axs[row,0].set(title=('各自训练表征' if view=='own' else '共同A0表征')+'：条件有效秩 / 全局秩',ylabel='8个expert的中位数');axs[row,1].set(title=('各自训练表征' if view=='own' else '共同A0表征')+'：低频方向方差占比放大',ylabel='64维低频子空间占比 / 全局占比')
 savefig(fig,'F_有效秩与低频方向放大','低频方向在各自DEV表征中拟合，再在EVAL测；共同A0控制使用同一坐标和同一低频子空间，仅按既有标签切片，不改模型前向。有效秩下降表示条件方差更集中，不等同谱更平。')
 dump(F/'evidence/F_complete.json',dict(arms=4,layers=8,primary_rank=64,positions_per_split=NS,joint_order_layers_own=sum(r['joint_order'] for r in rules if r['view']=='own'),joint_order_layers_common=sum(r['joint_order'] for r in rules if r['view']=='common_A0'),training_updates=0));event('F完成','条件协方差谱、低频/高频/打乱方向与共同表征对照均完成',GPU_seconds='见逐臂占用墙钟回执')

def main():
 assert (F/'evidence/F_forward_complete.json').exists();Z=labels()
 for arm in ['Dense','A0','A5','A2']:analyse_arm(arm,Z)
 finish()
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
