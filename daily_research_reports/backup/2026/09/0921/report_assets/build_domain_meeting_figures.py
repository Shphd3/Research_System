"""Domain meeting figures: existing PASS outputs and fixed observer caches only.

No model loading, probe fitting, new hypothesis test, or remote execution.
Rank bands are token distribution quantiles, NOT confidence intervals.
"""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'figures'
BASE = Path('/data/250010109/MoE_Router/experiments')
R21 = BASE / '20260920_sae_representation_21b_audit/runs/full_4x5090_retry2_20260921T0200Z'
R15 = BASE / '20260920_sae_representation_15b_early_audit/runs/full_15b_4x5090_20260920_wave1'
R08 = BASE / '20260920_sae_representation_15b_early_audit/runs/full_early_4x5090_20260920_wave1'
COLORS = {'dense':'#27272a', 'sall_original':'#00856a', 's7_reweighted':'#1676b8'}
NAMES = {'dense':'Dense', 'sall_original':'SALL', 's7_reweighted':'S7'}
sources = {}
outputs = []

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read(p):
    sources[str(p)] = sha(p)
    obj = json.loads(Path(p).read_text())
    assert obj.get('status') == 'PASS', p
    return obj

def save(fig, name):
    for ext in ('png', 'pdf'):
        p = OUT / (name + '.' + ext)
        fig.savefig(p, dpi=180, bbox_inches='tight', facecolor='white')
        outputs.append(str(p))
    plt.close(fig)

def style(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.grid(alpha=.2)

def select(rows, model, layer, pool):
    return next(r for r in rows if r['case'].endswith('_'+model) and r['layer']==layer and r['pooling']==pool)

for root in (R21,R15,R08):
    for f in ('terminal_receipt.json','stages/COLLECTION_PASS.json','stages/ANALYSIS_PASS.json'):
        read(root/f)
p21 = read(R21/'analysis/primary/primary_metrics.json')
g21 = read(R21/'analysis/geometry/geometry_cka.json')
o21 = read(R21/'analysis/observer/observer_metrics.json')
ng = [r for r in g21['geometry'] if r['panel']=='N8_v1']

# Same dataset, native read site, checkpoint, layer and pooling.
fig, axs = plt.subplots(2,2,figsize=(11,7),layout='constrained')
for col,pool in enumerate(('mean','last')):
    for model in COLORS:
        for row,key,data,scale in ((0,'test_accuracy',p21['N8_v1'],100),(1,'B_over_W',ng,1)):
            vals=[scale*select(data,model,l,pool)[key] for l in (4,8)]
            axs[row,col].plot([4,8],vals,'o-',color=COLORS[model],label=NAMES[model])
            for l,v in zip((4,8),vals):
                if l != 8:
                    continue
                axs[row,col].annotate(f'{v:.2f}' if row==0 else f'{v:.3f}',(l,v),xytext=(5,5),textcoords='offset points',fontsize=8,color=COLORS[model])
    axs[0,col].set_title(f'N8 domain readout | {pool} pooling')
    axs[0,col].set_ylabel('8-category test accuracy (%)')
    axs[1,col].set_title(f'Between / within dispersion | {pool} pooling')
    axs[1,col].set_ylabel('B / W (relative centroid separation)')
    for ax in axs[:,col]:
        ax.set_xticks([4,8]);ax.set_xlabel('Human layer');style(ax)
axs[0,0].legend(frameon=False)
fig.suptitle('21B native attention writes: readability and geometric separation disagree\nN8 test: 1,600 records; descriptive estimates, paired uncertainty not yet available',fontsize=12)
save(fig,'domain_01_readability_vs_separation')

# Domain timecourse, never substitute P relation trajectory.
times=[0,.5,1,3,5,10,15,21]
primary=[]; geometry=[]
for t in times:
    root=R08/f'analysis/time_{int(t*1e9)}' if t<=10 else (R15/'analysis/15b' if t==15 else R21/'analysis')
    primary.append(read(root/'primary/primary_metrics.json')['N8_v1'])
    geometry.append([r for r in read(root/'geometry/geometry_cka.json')['geometry'] if r['panel']=='N8_v1'])
fig,axs=plt.subplots(2,2,figsize=(12,7),layout='constrained')
trajectory=[]
for model in ('dense','sall_original'):
    for ax,key,data,scale in ((axs[0,0],'test_accuracy',primary,100),(axs[1,0],'B_over_W',geometry,1)):
        ys=[scale*select(rows,model,8,'mean')[key] for rows in data]
        ax.plot(times,ys,'o-',label=NAMES[model],color=COLORS[model])
for layer,ls in ((4,'--'),(8,'-')):
    for ax,key,data,scale in ((axs[0,1],'test_accuracy',primary,100),(axs[1,1],'B_over_W',geometry,1)):
        ys=[scale*(select(rows,'sall_original',layer,'mean')[key]-select(rows,'dense',layer,'mean')[key]) for rows in data]
        ax.plot(times,ys,'o'+ls,label=f'Layer {layer}',color='#8b5cb5' if layer==4 else '#00856a')
        if layer==8 and key=='test_accuracy':
            for t,v in zip(times,ys):trajectory.append({'tokens_B':t,'L8_mean_accuracy_delta_pp':v})
        ax.axhline(0,color='#555',lw=.7)
titles=['Layer 8: domain readability','SALL - Dense: readability','Layer 8: geometric separation','SALL - Dense: geometric separation']
ylabels=['Test accuracy (%)','Accuracy difference (pp)','B / W','Difference in B / W']
for ax,title,ylabel in zip(axs.flat,titles,ylabels):
    ax.set_title(title);ax.set_ylabel(ylabel);ax.set_xlabel('Cumulative training tokens (billions)')
    ax.axvline(9.174381056,color='#888',ls=':',lw=1);style(ax);ax.legend(frameon=False,fontsize=9)
fig.suptitle('N8 native writes, mean pooling: training gains are shared; the SAE advantage is not monotonic\nDots are actual checkpoints, lines guide the eye; dotted line = SALL continuation branch. No across-seed inference.',fontsize=11)
save(fig,'domain_02_training_trajectory')

# Rank traces: verify cache hashes and exact per-token identity before comparison.
traces=[]; identities=[]; rank_summary=[]
for model,layer,worker in [('sall_original',4,1),('sall_original',8,1),('s7_reweighted',8,2)]:
    manifest=read(R21/f'workers/worker_{worker}/observer/observer_manifest.json')
    arrays=[];masses=[];keys=[]
    for c in manifest['chunks']:
        if c['panel']!='N8_v1' or c['human_layer']!=layer:continue
        path=Path(c['npz']);actual=sha(path);assert actual==c['sha256'];sources[str(path)]=actual
        with np.load(path,allow_pickle=False) as a:
            arrays.append(a['rank_scores_1_to_128']);masses.append(a['top32_positive_mass_fraction'])
            for row,pos in zip(a['token_local_row'],a['token_position']):
                keys.append((str(a['sequence_ids'][row]),str(a['input_hashes'][row]),int(pos)))
    ranks=np.concatenate(arrays).astype(np.float64);mass=np.concatenate(masses)
    assert ranks.shape==(49152,128) and np.isfinite(ranks).all()
    assert np.all(np.diff(ranks,axis=1)<=0)
    assert np.all(ranks[:,31]>0) and np.all(mass>0)
    identities.append(keys)
    total=ranks[:,:32].sum(axis=1)/mass
    curves=[ranks,ranks/ranks[:,0,None],ranks/ranks[:,31,None],np.cumsum(ranks,axis=1)/total[:,None]]
    qs=[np.quantile(v,[.1,.5,.9],axis=0) for v in curves]
    label=f'{NAMES[model]} L{layer}'
    traces.append((label,COLORS[model], '--' if layer==4 else '-',qs))
    rank_summary.append({'condition':label,'n_tokens':len(keys),'rank32_median':float(np.median(ranks[:,31])),
                         'rank33_median':float(np.median(ranks[:,32])), 'top32_mass_median':float(np.median(mass))})
assert identities[0]==identities[1]==identities[2]
fig,axs=plt.subplots(2,2,figsize=(12,7.5),layout='constrained')
rank=np.arange(1,129)
for label,color,ls,qs in traces:
    for j,ax in enumerate(axs.flat):
        q=qs[j];use=(rank>=24)&(rank<=40) if j==2 else np.ones(128,dtype=bool)
        ax.plot(rank[use],q[1,use],ls,color=color,label=label)
        if j in (1,2):ax.fill_between(rank[use],q[0,use],q[2,use],color=color,alpha=.1)
for ax,title,ylabel in zip(axs.flat,['Raw positive encoder scores','Shape after per-token rank-1 normalization','Does rank 32 have a cliff?','Cumulative positive score mass'],['Median score (log scale)','Score / rank-1 score','Score / rank-32 score','Median fraction of ALL positive scores']):
    ax.set_title(title);ax.set_ylabel(ylabel);ax.set_xlabel('Rank before Top-K truncation')
    ax.axvline(32,color='#555',ls=':',lw=1);style(ax);ax.legend(frameon=False,fontsize=8)
axs[0,0].set_yscale('log');axs[1,0].set_xticks([24,28,32,33,36,40]);axs[1,1].set_ylim(0,1.02)
fig.suptitle('21B online SAE, N8: S7 is more concentrated, but K=32 is not a natural cutoff\nSame 192 records / 49,152 tokens; bands = token 10th-90th percentiles, NOT confidence intervals',fontsize=12)
save(fig,'domain_03_rank_activation_lines')

# Conceptual subspace illustration with an explicit empirical scorecard.
fig,axs=plt.subplots(1,3,figsize=(14,4.9),gridspec_kw={'width_ratios':[1,1,1.35]},layout='constrained')
rng=np.random.default_rng(21)
for ax,angles,title in [(axs[0],[30,46,61],'Rival illustration: overlapping directions'),(axs[1],[5,60,120],'Hypothesis: domain-related subspaces')]:
    for i,angle in enumerate(angles):
        u=np.array([np.cos(np.deg2rad(angle)),np.sin(np.deg2rad(angle))]);v=np.array([-u[1],u[0]])
        ts=np.linspace(-1,1,25);points=ts[:,None]*u+rng.normal(0,.055,(25,1))*v
        ax.plot([-u[0],u[0]],[-u[1],u[1]],color=['#00856a','#1676b8','#cc7733'][i],alpha=.8)
        ax.scatter(points[:,0],points[:,1],s=10,color=['#00856a','#1676b8','#cc7733'][i])
    ax.set_title(title,fontsize=10);ax.set_aspect('equal');ax.set_xlim(-1.2,1.2);ax.set_ylim(-1.2,1.2);ax.set_xticks([]);ax.set_yticks([])
    ax.text(.5,-.08,'SCHEMATIC ONLY - not a data projection',transform=ax.transAxes,ha='center',fontsize=8,color='#a33')
axs[2].axis('off')
axs[2].text(0,1,'What the actual N8 evidence says',fontsize=12,weight='bold',va='top')
axs[2].text(0,.87,'21B / layer 8 / mean pooling\n\nDense -> SALL\n  Readout: 87.06% -> 87.81%\n  Separation B/W: 0.469 -> 0.430\n\nDense -> S7\n  Readout: 87.06% -> 74.94%\n  Separation B/W: 0.469 -> 0.179\n\nDomain subspaces and their SAE alignment:\n  NOT TESTED directly\n\nSmall readout gain does not establish\nmore separated domain subspaces.',fontsize=11,va='top',linespacing=1.4)
fig.suptitle('Intuition versus evidence: a union of local subspaces remains a hypothesis',fontsize=14)
save(fig,'domain_04_intuition_vs_evidence')

manifest={'status':'PASS','scope':'N8 meeting replot; existing metrics plus descriptive aggregation of saved ranks; no new inference or hypothesis tests',
          'script':str(Path(__file__).resolve()),'script_sha256':sha(__file__), 'sources':sources,'outputs':outputs,
          'rank_identity_check':'PASS: same sample_id, input hash, token position across all three conditions',
          'rank_summary':rank_summary,'L8_mean_trajectory':trajectory,
          'limitations':['N8 labels are source categories, not verified semantic labels.','No paired N8 accuracy interval is present in existing primary metrics.',
                         'Observer sample is 192 fixed records, pooled over fit/dev/test for descriptive ranks only.',
                         'Cumulative score mass is not reconstruction energy; rank bands are not confidence intervals.',
                         'Conceptual points are synthetic illustrations, not model embeddings.']}
(OUT/'domain_figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'outputs':outputs,'rank_summary':rank_summary,'L8_mean_trajectory':trajectory},indent=2))
