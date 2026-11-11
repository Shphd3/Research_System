from offline import balance,quantities,objective
from lf_common import *
from threadpoolctl import threadpool_limits
def main():
 F,d=features('DEV');ct=np.asarray(F.sum(0)).ravel();fb=artifact('A0',2000)['feature_bin'].numpy();g=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);A=np.zeros((30000,8),np.float32);A[np.arange(30000),g['group'].numpy()]=g['w'].numpy();ids,b,feasible,it=balance(F@A);M,q,u=quantities(F,ct,ids);low=fb<=2;omega=low/max(low.sum(),1);no_low=~((fb[d['indices'].numpy()]<=2)&(d['values'].numpy()>0)).any(1);share=float(no_low.mean());row=dict(DEV_positions=N,no_low_feature_share=share,deterministic_Top2_bias_load_lower_bound=4*share,required_load_cap=1.2,initial_binary_A5_feasible=feasible,initial_binary_A5_max_load=float(u.max()*8),initial_binary_A5_low_M=float(np.median(M[low])),initial_binary_A5_high_M=float(np.median(M[fb>=7])),initial_binary_A5_low_objective=objective(M,omega),interpretation='The specifiedlambda1update zeros all non-lowfeatures, so an updated iterate cannot satisfyloadcap withsinglebias/deterministicTop2. InitialA5can still be feasible: this is an update-map obstruction,not proof thatthe originaloptimizationproblem has nofeasible solution.')
 table(pd.DataFrame([row]),'fig3_feasibility_diagnostic');dump(R/'evidence/fig3_feasibility_diagnostic.json',row)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
