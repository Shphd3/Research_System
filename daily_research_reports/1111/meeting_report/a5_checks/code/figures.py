from common import *
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt

def save(fig,name):
 fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(R/f'results/{name}.{ext}',dpi=160)
 plt.close(fig)
def main():
 lead=pd.read_csv(R/'results/check2_step_lead.csv')
 fig,axs=plt.subplots(1,2,figsize=(12,4))
 for ax,metric in zip(axs,['train_CE','EVAL_NLL']):
  for a in ['A0','A1']:
   z=lead[(lead.metric==metric)&(lead.comparison==a)&(lead.band=='overall')];u=z[~z.right_censored];c=z[z.right_censored];ax.plot(u.step,u.lead_steps,'o-',ms=3,label=f'versus {a}');ax.scatter(c.step,c.lead_lower_bound,marker='^',facecolors='none',edgecolors='C0' if a=='A0' else 'C1',label=f'{a}: lower bound, NOT estimate')
   for q in c.itertuples():ax.annotate('',xy=(q.step,q.lead_lower_bound+45),xytext=(q.step,q.lead_lower_bound),arrowprops=dict(arrowstyle='->',color='C0' if a=='A0' else 'C1',lw=1))
  ax.set_title(metric);ax.set_xlabel('A5 optimizer step');ax.set_ylabel('equal-loss lead (updates)');ax.grid(alpha=.2);ax.legend(fontsize=7)
 save(fig,'check2_overall_lead')
 fig,axs=plt.subplots(1,2,figsize=(12,4))
 for ax,a in zip(axs,['A0','A1']):
  for k in range(10):
   z=lead[(lead.metric=='EVAL_NLL')&(lead.comparison==a)&(lead.band==f'bin{k}')&(~lead.right_censored)];ax.plot(z.step,z.lead_steps,'o-',ms=3,label=f'bin{k}')
  ax.set_title('A5 versus '+a);ax.set_xlabel('A5 optimizer step');ax.set_ylabel('EVAL equal-loss lead');ax.grid(alpha=.2);ax.legend(fontsize=7,ncol=2)
 save(fig,'check2_frequency_lead')
 p=R/'results/check1_hint_probes.csv'
 if p.exists():
  d=pd.read_csv(p);fig,axs=plt.subplots(1,2,figsize=(11,4))
  for ax,h in zip(axs,['A0','A1']):
   for x in ['A5','A1','A2','A0-L7']:
    z=d[(d.host==h)&(d.distribution==x)&(d.band!='overall')].copy();z['bin']=z.band.str[3:].astype(int);z=z.sort_values('bin');ax.plot(z.bin,z.delta_hint,'o-',label=x)
   ax.axhline(.010,color='grey',ls=':',label='0.010 threshold');ax.axhline(.044,color='black',ls='--',label='0.044 threshold');ax.axhline(0,color='grey',lw=.5);ax.set_title('Frozen host '+h);ax.set_xlabel('frequency bin (0 rarest)');ax.set_ylabel('shuffled minus real probe NLL');ax.legend(fontsize=7);ax.grid(alpha=.2)
  save(fig,'check1_hint_by_frequency')
 p=R/'results/check6a_readability.csv'
 if p.exists():
  d=pd.read_csv(p);fig,axs=plt.subplots(1,3,figsize=(13,4))
  for ax,s in zip(axs,[500,1000,2000]):
   for k in ['linear','mlp_topk64']:
    z=d[(d.step==s)&(d.probe==k)];ax.plot(z.layer,z.exact_set_accuracy,'o-',label=k)
   ax.axhline(.6,color='grey',ls='--');ax.set_title(f'A0 step{s}');ax.set_xlabel('FFN input layer');ax.set_ylabel('A5 exact pair accuracy');ax.legend(fontsize=7);ax.grid(alpha=.2)
  save(fig,'check6a_readability')
 p=R/'results/check6b_bootstrap_atoms.csv'
 if p.exists():
  d=pd.read_csv(p);fig,axs=plt.subplots(1,2,figsize=(11,4))
  for l in [4,7]:
   z=d[d.layer==l];axs[0].plot(z.step,z.Mbar_median,'o-',label=f'L{l}');axs[1].plot(z.step,z.top2_overlap_fraction,'o-',label=f'L{l}')
  axs[0].axhline(1.08,color='black',ls='--',label='1.08');axs[0].axhline(1.01,color='grey',ls=':',label='1.01');axs[0].set_ylabel('teacher-atom coordinate median M');axs[1].set_ylabel('A5 overlap fraction after Hungarian')
  for ax in axs:ax.set_xlabel('A0 checkpoint step');ax.legend();ax.grid(alpha=.2)
  save(fig,'check6b_bootstrap')
if __name__=='__main__':main()
