from engine import *
for site in SITES:
 x=np.load(R/'cache'/f'{site}__discovery__position.npz');features=x['features'];realq=x['realq'];real=realq.mean(1);null=x['qnull'].mean((0,1));res=real-null;norm=np.linalg.norm(res,axis=1);own=np.divide(res,norm[:,None],out=np.zeros_like(res),where=norm[:,None]>1e-12);deltas=np.array([res[a]-res[b] for a,b in DP]);dn=np.linalg.norm(deltas,axis=1);between=np.divide(deltas,dn[:,None],out=np.zeros_like(deltas),where=dn[:,None]>1e-12)
 # Example pair selection is discovery-only and does not alter full276primary scores.
 coactdocs=(realq>0).sum(1);eligible=np.max(coactdocs,axis=0)>=4;pooled=res.mean(0);spread=np.ptp(res,axis=0);good=np.where(eligible)[0];first=sorted(good,key=lambda j:(-pooled[j],j))[:6];second=sorted([j for j in good if j not in first],key=lambda j:(-spread[j],j))[:6];chosen=np.array(first+second,int)
 np.savez_compressed(R/'data'/f'{site}__discovery_directions.npz',own=own,between=between,residual=res,null_mean=null,norm=norm,between_norm=dn,selected_pair_indices=chosen,patterns=x['patterns'],features=features)
 table(R/'tables'/f'{site}__discovery_pair_selection.csv',[dict(pair_index=int(j),feature_i=int(features[FI[j]]),feature_j=int(features[FJ[j]]),reason='pooled-positive' if j in first else 'dataset residual range',discovery_pooled_excess=float(pooled[j]),discovery_residual_range=float(spread[j]),max_discovery_coactivating_docs=int(np.max(coactdocs[:,j]))) for j in chosen])
dump(R/'evidence/directions_freeze.json',dict(UTC=now(),source='discovery only',heldout_joint_read=False,hashes={str(R/'data'/f'{s}__discovery_directions.npz'):sha(R/'data'/f'{s}__discovery_directions.npz') for s in SITES}))
print('DIRECTIONS_FROZEN')
