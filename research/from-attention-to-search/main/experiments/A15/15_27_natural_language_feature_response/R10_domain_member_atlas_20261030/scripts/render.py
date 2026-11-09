"""Standard static scientific plots; only reads R10 statistics."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,csv,textwrap,argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'));args=parser.parse_args()
O=args.output;A=O/'analysis';T=O/'tables'
R=json.loads((A/'results.json').read_text());freeze=json.loads((O/'freeze.json').read_text());sets={k:np.array(v) for k,v in freeze['sets'].items()};M=sets['main_math'];B=sets['main_biology'];main=np.r_[M,B]
G=R['geometry'];col={'math':'#2874A6','biology':'#C05B38','pool':'#7F8C8D'};groups=['math','biology'];n={'math':len(M),'biology':len(B)}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160})
def rows(name):return list(csv.DictReader((T/name).open()))
def save(fig,name,foot='',appendix=False):
 fig.text(.012,.012,foot,fontsize=8,va='bottom');fig.tight_layout(rect=(0,.065,1,.955));fig.savefig((O/('appendix' if appendix else 'figures')/name).with_suffix('.png'));plt.close(fig)
freq=rows('frequency_counts.csv')
def fdata(selection,rule='original'):
 r=[r for r in freq if r['selection']==selection and r['rule']==rule];valid=int(r[0]['plotted_denominator']);alln=int(r[0]['all_members']);return np.array([int(next(x['count'] for x in r if x['frequency']==lab)) for lab in ['low','middle','high']]),valid,alln

# 1: reference feature occurrence, not spectrum.
fig,ax=plt.subplots(figsize=(10,5.3));x=np.arange(3)
for i,(sel,label,c) in enumerate([('main_math','Math-biased',col['math']),('main_biology','Biology-biased',col['biology']),('eligible_pool','Eligible pool',col['pool'])]):
 counts,den,alln=fdata(sel);bars=ax.bar(x+(i-1)*.25,counts/den,.24,label=f'{label} ({den}/{alln} classified)',color=c)
 for bar,num in zip(bars,counts):ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.012,f'{num}\n{num/den:.1%}',ha='center',fontsize=9)
ax.set(xticks=x,xticklabels=['Low','Middle','High'],ylabel='Member proportion among frequency-classified members',ylim=(0,.83),title='1 | Domain discriminators are not concentrated in rare members');ax.yaxis.set_major_formatter(PercentFormatter(1));ax.legend(loc='upper left',fontsize=9)
save(fig,'figure1_frequency','Main: discovery AUC >= .75; math 433 / biology 527. Discovery: 30 docs/domain x160 positions.\nDCLM z>0 /65,536; original cuts .259399% /1.344299%, >=20 hits. Excluded from bars only: math1, biology2, pool101.')

# Small sensitivity: original and alternative grouping plus rank truncations.
fig,axs=plt.subplots(2,3,figsize=(13,7),sharey=True)
for ax,pre in zip(axs.flat,['top16','top64','top128','main','auc0.70','auc0.80']):
 for j,g in enumerate(groups):
  counts,den,total=fdata(pre+'_'+g);bottom=0
  for k,c in enumerate(['#C8D7E5','#7E9BB5','#234660']):ax.bar(j,counts[k]/den,bottom=bottom,color=c,label=['Low','Middle','High'][k] if j==0 else None);bottom+=counts[k]/den
  ax.text(j,1.015,f'{den}/{total}',ha='center',fontsize=9)
 ax.set(title=pre,xticks=[0,1],xticklabels=['Math','Bio'],ylim=(0,1.13));ax.yaxis.set_major_formatter(PercentFormatter(1))
axs[0,0].legend(fontsize=8);fig.suptitle('Appendix | Frozen frequency composition across list sizes / AUC thresholds')
save(fig,'frequency_selection_sensitivity','Numbers = classified / all members; all sets fixed on discovery documents. Same original frequency cuts; low-support exclusions remain outside bars.',True)
fig,axs=plt.subplots(1,2,figsize=(11,4.5))
for ax,rule in zip(axs,['original','log_width']):
 for j,sel in enumerate(['main_math','main_biology','eligible_pool']):
  cc,den,_=fdata(sel,rule);ax.bar(np.arange(3)+(j-1)*.25,cc/den,.24,color=[col['math'],col['biology'],col['pool']][j],label=['Math','Bio','Pool'][j])
 ax.set(title=rule,xticks=np.arange(3),xticklabels=['Low','Middle','High'],ylim=(0,.9));ax.yaxis.set_major_formatter(PercentFormatter(1));ax.legend(fontsize=8)
save(fig,'frequency_bin_sensitivity','Original cuts .259399% /1.344299%; log-width cuts .451726% /6.686506%. Frequency labels depend on the rule; low-bin depletion vs pool persists.',True)

P=np.load(A/'all_decoder_projection.npz')['per_pc'];bands=P.reshape(16384,16,64).sum(2);bg={g:np.load(A/f'{g}_fine_matched_background.npz')['mean_per_pc'] for g in groups}
pool=np.array([int(r['feature_id']) for r in rows('all_dictionary_screen.csv') if r['support_qualified']=='True']);x=np.arange(16)
fig=plt.figure(figsize=(13,9));grid=fig.add_gridspec(2,2,height_ratios=[1.3,1]);axes=[fig.add_subplot(grid[0,i]) for i in range(2)]
plotrng=np.random.default_rng(10)
for ax,g in zip(axes,groups):
 ids=sets['main_'+g];bm=bg[g].reshape(1000,16,64).sum(2);lo,hi=np.quantile(bm,[.025,.975],axis=0)
 for k in range(16):ax.scatter(k+plotrng.uniform(-.12,.12,len(ids)),bands[ids,k],s=2,color=col[g],alpha=.1,rasterized=True)
 ax.fill_between(x,lo,hi,color='gray',alpha=.25,label='Matched background 95% range');ax.plot(x,bands[ids].mean(0),'o-',color=col[g],lw=2,label='Member mean');ax.plot(x,np.median(bands[ids],axis=0),'--',color=col[g],label='Member median');ax.plot(x,bands.mean(0),':',color='black',label='Whole dictionary mean')
 ax.set(title=f'2A | {g.title()} ({len(ids)} members)',ylabel='Full unit-decoder squared-length fraction',xticks=x[::2],xticklabels=[f'{i*64+1}-{(i+1)*64}' for i in x[::2]],xlabel='PC range (64 directions per band)');ax.legend(fontsize=7)
ax=fig.add_subplot(grid[1,:]);xx=np.arange(3)
for i,g in enumerate(groups):
 ids=sets['main_'+g];tri=np.c_[P[ids,0],P[ids,1:64].sum(1),P[ids,64:].sum(1)];b=ax.bar(xx+(i-.5)*.27,tri.mean(0),.26,color=col[g],label=f'{g.title()} mean')
 ax.scatter(xx+(i-.5)*.27,np.median(tri,axis=0),color='black',marker='_',s=110,label='Member median' if i==0 else None)
 for bar,v in zip(b,tri.mean(0)):ax.text(bar.get_x()+bar.get_width()/2,v+.025,f'{v:.3%}',ha='center',fontsize=9)
ax.scatter(xx,[1/1024,63/1024,960/1024],marker='D',facecolors='none',edgecolors='black',label='Dimension fraction');ax.set(title='2B | The front bias remains after separating PC1',xticks=xx,xticklabels=['PC1 (1 dimension)','PC2-64 (63 dimensions)','PC65-1024 (960 dimensions)'],ylabel='Fraction of complete unit decoder',ylim=(0,1.08));ax.yaxis.set_major_formatter(PercentFormatter(1));ax.legend(fontsize=8,ncol=2)
fig.suptitle('2 | Unit decoder geometry in one pooled natural-document spectrum')
save(fig,'figure2_decoder_spectrum','Main math433 / biology527; same 60 discovery docs,9,600 true block27 residual-post positions. All1024-PC sums=1.\nBackground:1,000 fine occurrence/support-stratum draws, matching group sizes; eligible pool includes selected members. Dots are members, not tokens.')

# 3: same unit quantity vs actual summed contribution, clearly separated rows.
fig,axs=plt.subplots(2,2,figsize=(12,8.5));qm=P[M].mean(0);qb=P[B].mean(0);bm=qm.reshape(16,64).sum(1);bb=qb.reshape(16,64).sum(1)
ax=axs[0,0];ax.plot(x,bm,'o-',color=col['math'],label='Math');ax.plot(x,bb,'o-',color=col['biology'],label='Biology');ax.fill_between(x,0,np.minimum(bm,bb),color='#7C8C73',alpha=.35,label='Common minimum');ax.set(title=f'3A | Unit geometry: PC overlap={G["overlap_pc"]:.4f}\n64-PC-band overlap={G["overlap_band"]:.4f}',xticks=x[::3],xticklabels=[f'{i*64+1}-{(i+1)*64}' for i in x[::3]],ylabel='Group mean squared projection',xlabel='Common PC band');ax.legend(fontsize=8)
ax=axs[0,1];ax.plot(np.arange(2,65),qm[1:64],color=col['math']);ax.plot(np.arange(2,65),qb[1:64],color=col['biology']);ax.fill_between(np.arange(2,65),0,np.minimum(qm[1:64],qb[1:64]),color='#7C8C73',alpha=.3);ax.set(title=f'PC2-64 zoom | within-segment overlap={G["PC2_64_overlap_renormalized"]:.4f}',xlabel='PC number',ylabel='Original full-unit-decoder fraction');ax.text(.02,.96,f'Full-spectrum masses: math {qm[1:64].sum():.2%}, bio {qb[1:64].sum():.2%}\nPC overlap matched range: {G["overlap_pc_bg95"][0]:.4f}-{G["overlap_pc_bg95"][1]:.4f}',transform=ax.transAxes,va='top',fontsize=8)
energy=rows('group_reconstruction_energy.csv')
for ax,dom in zip(axs[1],groups):
 for g in groups:
  rr=[r for r in energy if r['member_group']==g and r['input_domain']==dom];y=[float(r['fraction']) for r in rr];total=float(rr[0]['total_mean_squared_norm']);ax.plot(x,y,'o-',color=col[g],label=f'{g.title()} group (norm^2={total:,.0f})')
 ax.set(title=f'3B | Actual reconstruction on {dom} inputs (20 docs)',xlabel='Same common PC band',ylabel='Summed-vector spectral energy fraction',xticks=x[::3],xticklabels=[f'{i*64+1}-{(i+1)*64}' for i in x[::3]],ylim=(0,.6));ax.legend(fontsize=8)
fig.suptitle('3 | Similar spectral positions coexist with input-dependent use')
save(fig,'figure3_overlap_and_use','Same main groups:433math /527bio. Top: member-equal unit geometry, no z/scale/eigenvalue factors. Bottom:40 exposed-heldout natural docs x160 positions.\nBottom sums z x restored decoder FIRST, retains cross terms, then squares and averages equally by doc; fractions are not full-representation explained variance.')

# 4: true input tokens and corpus counts.
tm=rows('token_member_summary.csv');fig=plt.figure(figsize=(12,9));gs=fig.add_gridspec(2,2,height_ratios=[1,1.1]);ax=fig.add_subplot(gs[0,0])
xx=np.arange(3)
for j,g in enumerate(groups):
 good=[r for r in tm if r['domain_bias']==g and r['usable']=='True'];props=np.array([[float(r[k]) for k in ['low','middle','high']] for r in good]);y=props.mean(0);b=ax.bar(xx+(j-1)*.25,y,.24,color=col[g],label=f'{g.title()} ({len(good)}/{n[g]} usable)')
 for bar,v in zip(b,y):ax.text(bar.get_x()+bar.get_width()/2,v+.02,f'{v:.1%}',ha='center',fontsize=8)
ax.bar(xx+.25,R['tokens']['baseline'],.24,color=col['pool'],label='All19,200 positions');ax.set(title='4A | High-response events: member-equal token-bin fractions',xticks=xx,xticklabels=['Low: count1','Middle: count2','High: count>=3'],ylim=(0,1),ylabel='High-response position proportion');ax.legend(fontsize=8);ax.yaxis.set_major_formatter(PercentFormatter(1))
ax=fig.add_subplot(gs[0,1]);master={int(r['feature_id']):r for r in rows('master_members.csv')}
for g in groups:
 good=[r for r in tm if r['domain_bias']==g and r['usable']=='True'];fx=np.array([float(master[int(r['feature_id'])]['DCLM_feature_occurrence']) for r in good]);yy=np.array([float(r['token_count_median'])/19200 for r in good]);ylo=np.array([float(r['token_count_p10'])/19200 for r in good]);yhi=np.array([float(r['token_count_p90'])/19200 for r in good]);ax.vlines(fx,ylo,yhi,color=col[g],alpha=.07,lw=.5);ax.scatter(fx,yy,s=9,alpha=.45,color=col[g],label=f'{g.title()} rho={R["tokens"]["groups"][g]["spearman_feature_rate_vs_panel_token_count"]:.3f}')
ax.set(xscale='log',yscale='log',xlabel='Feature DCLM reference occurrence (z>0 /65,536)',ylabel='Median panel token count /19,200',title='4B | Feature occurrence and token frequency differ');ax.legend(fontsize=8)
ax=fig.add_subplot(gs[1,:]);ax.axis('off');examples=rows('real_token_examples.csv');chosen=[]
for g in groups:
 for f in sets['main_'+g][:2]:
  rr=[r for r in examples if int(r['feature_id'])==f];high=next((r for r in rr if r['kind']=='high'),None)
  if not high:continue
  low=next((r for r in rr if r['kind']=='same_token_low' and r['token_id']==high['token_id']),None)
  prefix=' '.join(high['already_read_prefix'].split())[-150:]
  chosen.append([f'{g} f{f}',repr(high['token_string'])+f'\nID {high["token_id"]}',textwrap.fill('...'+prefix,65),f'{float(high["z"]):.3f}\n'+(f'{float(low["z"]):.3f}' if low else 'NA')])
tab=ax.table(cellText=chosen,colLabels=['Frozen rank1-2 members','Actual input token','Already-read prefix (cropped at left)','z high / same-ID low'],colWidths=[.16,.14,.57,.13],cellLoc='left',loc='center');tab.auto_set_font_size(False);tab.set_fontsize(8);tab.scale(1,3.1);ax.set_title('4C | Real heldout high-response examples; exact same-ID low examples in another document')
fig.suptitle('4 | High feature response is not restricted to rare input tokens')
save(fig,'figure4_real_tokens','Main433/527; usable371/472; insufficient62/55 retained. Panel120docs; high events on20heldout docs/domain x160 positions; discovery-positive-zp90 fixed.\nType-count quantiles with ties:2,782/888/1,203 types;2,782/1,776/14,642 positions. No special-token positions. Full contexts/IDs in tables.')

# 5: all member/family raw pairs, with exposed splits separated. No best-feature selection.
cats=rows('context_categories.csv');fig=plt.figure(figsize=(14,10.5));gs=fig.add_gridspec(3,4,height_ratios=[.75,1,1]);ax=fig.add_subplot(gs[0,:]);catnames=['context_response','target_suffix_sensitive','both_or_interaction','insufficient'];catcolors=['#2E8B70','#D79C38','#7A69A0','#CFD3D5'];bottom=np.zeros(2)
for k,c in zip(catnames,catcolors):
 v=np.array([sum(r['category']==k and r['domain_bias']==g for r in cats) for g in groups]);bars=ax.barh(np.arange(2),v/np.array([n[g] for g in groups]),left=bottom,color=c,label=k.replace('_',' ')+(f' (M{v[0]}/B{v[1]})' if k=='context_response' else ''))
 for j,val in enumerate(v):
  if val>=5:ax.text(bottom[j]+v[j]/n[groups[j]]/2,j,str(val),ha='center',va='center',fontsize=9)
 bottom+=v/np.array([n[g] for g in groups])
ax.set(yticks=[0,1],yticklabels=['Math n433','Biology n527'],xlim=(0,1));ax.xaxis.set_major_formatter(PercentFormatter(1));ax.legend(ncol=4,fontsize=8,loc='lower center',bbox_to_anchor=(.5,1.02));fig.suptitle('5 | Fixed-target context response and target-plus-suffix sensitivity can coexist',fontsize=14,y=.985)
for ri,split in enumerate(['discovery','heldout']):
 c=np.load(A/f'context_{split}.npz');arr=c['activation'];fw=c['bootstrap_family_weights'];Nf=arr.shape[0]
 for e in [0,1]:
  for w in [0,1]:
   ax=fig.add_subplot(gs[ri+1,e*2+w]);xj=np.array([0,1]);activecounts=[]
   for gi,g in enumerate(groups):
    off=0 if g=='math' else len(M);idslice=slice(off,off+n[g]);v=arr[:,:,w,e,idslice].transpose(0,2,1).reshape(-1,2);activecounts.append(int((arr[:,:,w,e,idslice]>0).any((0,1)).sum()))
    # Every member x family pair is present, including zeros; only nonzero segments need ink.
    nz=(v>0).any(1);a=v[nz];offset=(gi-.5)*.08
    for pair in a:ax.plot(xj+offset,pair,color=col[g],alpha=.022,lw=.45,rasterized=True)
    ax.scatter(np.full(len(a),offset),a[:,0],s=2,color=col[g],alpha=.08,rasterized=True);ax.scatter(np.full(len(a),1+offset),a[:,1],s=2,color=col[g],alpha=.08,rasterized=True)
    familymean=arr[:,:,w,e,idslice].mean(2);m=familymean.mean(0);bc=fw@familymean;lo,hi=np.quantile(bc,[.025,.975],axis=0);ax.errorbar(xj+offset,m,yerr=np.maximum(np.stack([m-lo,hi-m]),0),fmt='o-',color=col[g],lw=2,capsize=3,ms=4)
   ax.set(xticks=xj,xticklabels=['Math ctx','Bio ctx'],ylim=(-.00002,.15),ylabel='Native shared z' if e*2+w==0 else '')
   ax.set_yscale('symlog',linthresh=.001);ax.set_title(f'{split}: {"example" if e==0 else "explanation"}, W{w}\nactive M/B={activecounts[0]}/{activecounts[1]}; {Nf} families',fontsize=9)
save(fig,'figure5_context','Each faint pair = one main member x one family; zeros retained. Bold pairs/95% bars = equal-member mean, family bootstrap. Discovery24 / exposed heldout12 families.\nMain433/527; always-zero fixed-target coverage:318/471. Recurrent context at >=1 ending:33/21; both endings11/2. Ending contrasts change target AND suffix; pure identity test NOT RUN.')

# Bounded appendices: complete member distributions, allPC curves and cosine/subspace check.
fig,axs=plt.subplots(1,2,figsize=(12,7),gridspec_kw={'width_ratios':[1,1]})
for ax,g in zip(axs,groups):
 data=bands[sets['main_'+g]];im=ax.imshow(data,aspect='auto',interpolation='nearest',vmin=0,vmax=np.quantile(bands[main],.99),cmap='viridis');ax.set(title=f'{g.title()} {n[g]} ranked members',xlabel='64-PC band',ylabel='Frozen discovery rank')
fig.colorbar(im,ax=axs.ravel().tolist(),shrink=.6,label='Full unit-decoder fraction');fig.suptitle('Appendix | Every frozen member, no representative-feature substitution')
fig.subplots_adjust(top=.9,bottom=.12,wspace=.25);fig.savefig(O/'appendix/member_band_heatmap.png');plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(12,7));ax=axs[0,0];ax.plot(qm,color=col['math']);ax.plot(qb,color=col['biology']);ax.fill_between(np.arange(1024),0,np.minimum(qm,qb),alpha=.2);ax.set(title=f'All1024 PCs; overlap={G["overlap_pc"]:.4f}',xlabel='PC index (zero-based)',ylabel='Mean unit squared projection')
cos=np.load(A/'cross_group_absolute_cosine.npz')['absolute_cosine'];axs[0,1].hist(cos.ravel(),bins=60,color='gray');axs[0,1].set(title=f'All{cos.size:,} cross-member pairs',xlabel='Absolute decoder cosine',ylabel='Pair count')
pc=np.load(A/'actual_decoder_subspace.npz')['principal_cosine'];axs[1,0].plot(pc**2);axs[1,0].set(title=f'Decoder subspaces ranks433/527; trace/minrank={G["actual_subspace"]["trace_over_min_rank"]:.3f}',xlabel='Principal direction',ylabel='Squared principal cosine')
ov=np.minimum(bg['math'],bg['biology']).sum(1);axs[1,1].hist(ov,bins=35,color='gray');axs[1,1].axvline(G['overlap_pc'],color='red',label='Observed');axs[1,1].set(title='Matched dictionary reference',xlabel='PCwise overlap');axs[1,1].legend()
save(fig,'full_pc_and_direction_checks','Spectral-distribution overlap, pairwise direction similarity and decoder-subspace overlap measure different objects. High overlap never proves identical semantics.',True)

# Save the exact plotting source tables already present and render manifest.
manifest={'figures':[str(p.relative_to(O)) for p in sorted((O/'figures').glob('*.png'))],'appendix':[str(p.relative_to(O)) for p in sorted((O/'appendix').glob('*.png'))],'renderer':'matplotlib; measured tables only','visual_review':'PENDING'}
(O/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
