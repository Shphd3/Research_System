from pathlib import Path
import csv,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parents[1]/'analysis/meeting_20261026';rs=list(csv.DictReader(open(O/'tables/03_F_finite_checks_90.csv')))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
fig,axs=plt.subplots(1,2,figsize=(9,3.8));co={'0':'#D55E00','4':'#0072B2','36':'#009E73'}
for k in ['0','4','36']:
 a=[r for r in rs if r['old_slots']==k]
 axs[0].scatter([float(r['g_dot_final_actual']) for r in a],[float(r['actual_loss_change']) for r in a],s=25,c=co[k],alpha=.75,label=f'Old slots {k}')
axs[0].axhline(0,c='grey',lw=.7);axs[0].axvline(0,c='grey',lw=.7);axs[0].set_xlim(-.075,.005);axs[0].set_ylim(-.075,.06);axs[0].set_xlabel('Final first-order prediction (nat/answer)');axs[0].set_ylabel('Actual old-probe loss change (nat/answer)');axs[0].legend(fontsize=8,frameon=False,loc='upper left')
raw=[r for r in rs if r['final_raw_positive']=='True'];rat=[float(r['g_dot_final_actual'])/float(r['final_actual_tolerance']) for r in raw]
axs[1].scatter(range(1,len(raw)+1),rat,c=[co[r['old_slots']] for r in raw],s=25);axs[1].axhline(1,c='black',lw=1,ls='--');axs[1].axhline(0,c='grey',lw=.7);axs[1].set_ylim(-.02,1.08);axs[1].set_xlabel(f'Raw-positive predictions ({len(raw)} / 90 checks)');axs[1].set_ylabel('Final prediction / numerical tolerance')
for ax in axs:ax.grid(alpha=.16)
fig.tight_layout()
for ext in ['png','svg','pdf']:fig.savefig(O/'figures'/('figure3_first_order_finite_loss.'+ext),dpi=280,bbox_inches='tight')
print({'raw_positive_checks':len(raw),'max_ratio':max(rat),'all90_kept_in_left_panel':True})
