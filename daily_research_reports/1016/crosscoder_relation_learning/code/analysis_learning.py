"""Read-only analysis of frozen structure, learning and virtual-update outputs.

Evaluation CIs use paired CONTEXT clusters, preserving feature overlap. The
feature-conditional ratio estimand is linearized at the frozen eligible feature
set. These CIs condition on each trained seed; they are not seed uncertainty.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from train_adapters import write_json, order_indices

COLORS={'R':'#3264a0','F':'#d88335','N':'#438968'}


def read_json(path):return json.loads(Path(path).read_text())
def read_csv(path):
    with open(path) as f:return list(csv.DictReader(f))
def csv_out(path,rows):
    if not rows:return
    with open(path,'w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def save(fig,root,name,manifest,metadata):
    root.mkdir(parents=True,exist_ok=True)
    for ext in ('png','pdf','svg'):fig.savefig(root/f'{name}.{ext}',dpi=180,bbox_inches='tight')
    plt.close(fig);manifest[name]=metadata


def unavailable(ax,label):
    ax.text(.5,.5,label,ha='center',va='center',transform=ax.transAxes,wrap=True,color='#666666')
    ax.set_xticks([]);ax.set_yticks([])


class FixedFeatureView:
    def __init__(self,data,label,minimum,blocks):
        ptr=data['feature_ptr'].numpy();ids=data['feature_ids'].numpy()
        counts=np.bincount(ids,minlength=16384)
        sel=data[label+'_ids'].numpy();self.defined=len(sel);self.selected=sel[counts[sel]>=minimum]
        mapping=np.full(16384,-1,np.int32);mapping[self.selected]=np.arange(len(self.selected))
        eligible=mapping[ids]>=0
        # Rows of the complete gated CSR are retained, including overlap.
        rows=np.repeat(np.arange(len(ptr)-1),np.diff(ptr))
        self.row=rows[eligible];self.feature=mapping[ids[eligible]]
        self.counts=counts[self.selected].astype(float)
        self.nblocks=int(blocks.max())+1
        self.key=blocks[self.row]*len(self.selected)+self.feature
        self.block_counts=(np.bincount(self.key,minlength=self.nblocks*len(self.selected)).reshape(self.nblocks,-1)
                           if len(self.selected) else np.zeros((self.nblocks,0)))
    def difference(self,delta):
        if not len(self.selected):return None,None
        totals=np.bincount(self.feature,weights=delta[self.row],minlength=len(self.selected))
        means=totals/self.counts;point=float(means.mean())
        bsum=np.bincount(self.key,weights=delta[self.row],minlength=self.nblocks*len(self.selected)).reshape(self.nblocks,-1)
        influence=((bsum-self.block_counts*means)/self.counts).mean(1)
        if not np.isclose(influence.sum(),0,atol=1e-8):raise ValueError('Context influence failed centering')
        return point,influence


def bootstrap_interval(point,influence,draws):
    values=point+draws@influence
    return float(np.quantile(values,.025)),float(np.quantile(values,.975)),float(values.std(ddof=1))


def analyze_learning(root,cfg):
    output=root/'analysis_outputs';output.mkdir(parents=True,exist_ok=True)
    rows=[];endpoints=[];checkpoints=[];loads=[];run_index={};missing=[]
    for seed in cfg['paired_seeds']:
        for arm in ('R','F','N'):
            path=root/'learning'/f'seed_{seed}'/arm
            if not (path/'completion.json').exists():missing.append(f'{seed}/{arm}');continue
            complete=read_json(path/'completion.json')
            if complete['execution_status']!='COMPLETE':missing.append(f'{seed}/{arm}');continue
            if complete['config_sha256']!=cfg['_config_sha256']:
                raise ValueError('Mixed training contract')
            run_index[seed,arm]=path
            for evfile in sorted(path.glob('eval_*.json')):
                ev=read_json(evfile)
                rows.append({k:ev[k] for k in ('arm','seed','step','tokens_seen','overall','low_loss','high_loss',
                            'low_eligible_features','low_defined_features','low_coverage','high_eligible_features','high_coverage')})
            metrics=[json.loads(x) for x in (path/'metrics.jsonl').read_text().splitlines()]
            for expert in range(4):
                exposure=sum(m['expert_tokens'][expert] for m in metrics)
                active=sum(m.get('expert_nonzero_gradient',[True]*4)[expert] for m in metrics)
                loads.append({'arm':arm,'seed':seed,'expert':expert,'tokens':exposure,
                              'fraction':exposure/complete['tokens_seen'],'nonzero_gradient_updates':active,
                              'total_updates':complete['updates']})
    csv_out(output/'learning_metrics.csv',rows);csv_out(output/'expert_exposure.csv',loads)
    baseline_changes=[]
    for seed,arm in run_index:
        rr=[r for r in rows if r['seed']==seed and r['arm']==arm]
        initial=next(r for r in rr if r['step']==0);final=next(r for r in rr if r['step']==cfg['updates'])
        for metric,key in [('low','low_loss'),('overall','overall'),('high','high_loss')]:
            if initial[key] is None or final[key] is None:continue
            baseline_changes.append({'seed':seed,'arm':arm,'metric':metric,'initial_loss_nat':initial[key],
                 'final_loss_nat':final[key],'initial_minus_final_nat':initial[key]-final[key],
                 'final_minus_initial_nat':final[key]-initial[key],
                 'sign':'positive means improvement from original frozen zero-adapter reference'})
    csv_out(output/'zero_reference_changes.csv',baseline_changes)
    summary={'completed_runs':len(run_index),'missing_runs':missing,'expected_runs':len(cfg['paired_seeds'])*3}
    summary['zero_reference_changes']=baseline_changes
    if run_index:
        data=torch.load(cfg['eval_cache'],map_location='cpu',weights_only=False)
        context_ids,context_index=np.unique(data['block_id'].numpy(),return_inverse=True)
        # Freeze four consecutive eval contexts as the primary cluster before
        # reading outcomes. Adjacent packed contexts may share a document.
        blocks=context_index//4;cluster_count=int(blocks.max())+1
        rng=np.random.default_rng(20261016)
        bootstrap=rng.multinomial(cluster_count,np.full(cluster_count,1/cluster_count),size=2000)
        views={label:FixedFeatureView(data,label,cfg['min_eval_support'],blocks) for label in ('low','high')}
        summary.update(eval_positions=len(blocks),eval_contexts=len(context_ids),eval_cluster_blocks=cluster_count,contexts_per_cluster=4,
            coverage={k:{'defined':v.defined,'eligible':len(v.selected),'fraction':len(v.selected)/v.defined} for k,v in views.items()},
            interval_method='approximate paired four-consecutive-context block bootstrap of linearized fixed-feature conditional mean; 2000 draws; seed-conditioned; not document independent')
        first_path=next(iter(run_index.values()));initial=np.load(first_path/'eval_losses_00000.npy').astype(float)
        variability=[]
        for metric in ('low','overall','high'):
            if metric=='overall':
                point=float(initial.mean());influence=np.bincount(blocks,weights=initial-point,minlength=cluster_count)/len(initial)
            else:point,influence=views[metric].difference(initial)
            if point is None:continue
            se=float(np.sqrt(cluster_count/(cluster_count-1)*np.square(influence).sum()))
            variability.append({'metric':metric,'baseline_loss_nat':point,'baseline_block_robust_se':se,
                                'eval_contexts':len(context_ids),'eval_blocks':cluster_count,'contexts_per_block':4,
                                'fixed_practical_threshold_nat':cfg['practical_low_gain_nat'],
                                'threshold_over_baseline_se':cfg['practical_low_gain_nat']/se if se>0 else None,
                                'threshold_selection':'fixed beforehand; variability is descriptive, not used to choose threshold'})
        csv_out(output/'baseline_variability.csv',variability);summary['baseline_variability']=variability
        for seed in cfg['paired_seeds']:
            for control in ('F','N'):
                if (seed,'R') not in run_index or (seed,control) not in run_index:continue
                rp=run_index[seed,'R'];cp=run_index[seed,control]
                rcomplete=read_json(rp/'completion.json');ccomplete=read_json(cp/'completion.json')
                if rcomplete['initialization_hash']!=ccomplete['initialization_hash']:raise ValueError('Unpaired expert initialization')
                if read_json(rp/'run_contract.json')['order_hash']!=read_json(cp/'run_contract.json')['order_hash']:
                    raise ValueError('Unpaired position exposure/order')
                r0=np.load(rp/'eval_losses_00000.npy');c0=np.load(cp/'eval_losses_00000.npy')
                if not np.array_equal(r0,c0):raise ValueError('Conditions differ before training')
                for step in sorted(set([0,cfg['updates']]+cfg['eval_steps'])):
                    r=np.load(rp/f'eval_losses_{step:05d}.npy');c=np.load(cp/f'eval_losses_{step:05d}.npy')
                    delta=r.astype(float)-c.astype(float)
                    for metric in ('low','overall','high'):
                        if metric=='overall':
                            point=float(delta.mean());infl=np.bincount(blocks,weights=delta-point,minlength=cluster_count)/len(delta)
                            eligible=None
                        else:
                            point,infl=views[metric].difference(delta);eligible=len(views[metric].selected)
                        if point is None:continue
                        lo,hi,se=bootstrap_interval(point,infl,bootstrap)
                        row={'seed':seed,'contrast':'R-'+control,'metric':metric,'difference_nat':point,
                             'ci025':lo,'ci975':hi,'context_bootstrap_se':se,'eval_contexts':len(context_ids),
                             'eval_cluster_blocks':cluster_count,'contexts_per_cluster':4,
                             'eval_tokens':len(delta),'eligible_features':eligible,'train_tokens':step*cfg['batch_size'],
                             'step':step,'uncertainty_scope':'approximate 4-context block interval conditional on this trained seed; not document independent'}
                        checkpoints.append(row)
                        if step==cfg['updates']:endpoints.append(row)
        # Same feature-conditional coefficients are reused for all routes.
        summary['initial_logits_and_losses_exact_across_conditions']=True
    csv_out(output/'paired_endpoints.csv',endpoints)
    csv_out(output/'paired_checkpoints.csv',checkpoints)
    if endpoints:
        summary['paired_differences']={m:{c:[r['difference_nat'] for r in endpoints if r['metric']==m and r['contrast']==c]
                                         for c in ('R-F','R-N')} for m in ('low','overall','high')}
        summary['paired_trajectory_mean']={m:{c:[{'step':s,'train_tokens':s*cfg['batch_size'],
           'mean_difference_nat':float(np.mean([r['difference_nat'] for r in checkpoints if r['metric']==m and r['contrast']==c and r['step']==s]))}
           for s in sorted({r['step'] for r in checkpoints if r['metric']==m and r['contrast']==c})]
           for c in ('R-F','R-N')} for m in ('low','overall','high')}
    if run_index:
        train=torch.load(cfg['train_cache'],map_location='cpu',weights_only=False)
        ptr=train['feature_ptr'].numpy();fid=train['feature_ids'].numpy()
        source_row=np.repeat(np.arange(len(train['target'])),np.diff(ptr))
        hit_counts={label:np.bincount(source_row[np.isin(fid,train[label+'_ids'].numpy())],minlength=len(train['target']))
                    for label in ('low','high')}
        del source_row
        exposure=[]
        for seed in cfg['paired_seeds']:
            ix=order_indices(len(train['target']),cfg['updates'],cfg['batch_size'],seed).numpy().reshape(-1)
            for arm in ('R','F','N'):
                if (seed,arm) not in run_index:continue
                route=train['routes'][arm].numpy()[ix]
                for expert in [-1,0,1,2,3]:
                    selected=np.ones(len(ix),dtype=bool) if expert==-1 else route==expert
                    exposure.append({'seed':seed,'arm':arm,'expert':'ALL' if expert==-1 else expert,
                        'training_tokens':int(selected.sum()),'low_position_exposures':int((hit_counts['low'][ix][selected]>0).sum()),
                        'high_position_exposures':int((hit_counts['high'][ix][selected]>0).sum()),
                        'low_feature_hit_exposures':int(hit_counts['low'][ix][selected].sum()),
                        'high_feature_hit_exposures':int(hit_counts['high'][ix][selected].sum()),
                        'low_term_coefficient':1.0,'loss_denominator':'entire fixed batch256, no low-feature reweighting'})
        csv_out(output/'feature_exposure.csv',exposure)
        summary['feature_exposure_csv']=str(output/'feature_exposure.csv')
        # A global equal-exposure check allows expert composition to differ,
        # since that difference is exactly the treatment under study.
        for seed in cfg['paired_seeds']:
            rr=[r for r in exposure if r['seed']==seed and r['expert']=='ALL']
            for key in ['training_tokens','low_position_exposures','high_position_exposures','low_feature_hit_exposures','high_feature_hit_exposures']:
                if len({r[key] for r in rr})>1:raise ValueError('Paired feature exposure differs: '+key)
        summary['same_total_low_and_high_position_exposure']=True
    write_json(output/'learning_summary.json',summary)
    return rows,endpoints,loads,summary


def analyze_intervention(root,cfg):
    output=root/'analysis_outputs';allrows=[];effects=[]
    for seed in cfg['paired_seeds']:
        for arm in ('R','F','N'):
            path=root/'intervention'/f'seed_{seed}'/arm
            if not (path/'completion.json').exists():continue
            rows=read_csv(path/'effects.csv');allrows.extend(rows)
            for version in ('raw','expert_norm_matched'):
                eligible=[];actual_changes=[];exchange_changes=[];bad=0
                for batch in sorted({int(r['batch']) for r in rows}):
                    pair={r['donor_route']:r for r in rows if int(r['batch'])==batch and r['version']==version}
                    if len(pair)!=2:raise ValueError('Missing paired virtual update')
                    if any(r['eligible']!='True' for r in pair.values()):bad+=1;continue
                    eligible.append(float(pair['actual']['low_loss_decrease'])-float(pair['exchanged']['low_loss_decrease']))
                    actual_changes.append(float(pair['actual']['low_loss_decrease']))
                    exchange_changes.append(float(pair['exchanged']['low_loss_decrease']))
                if eligible:
                    rng=np.random.default_rng(20261017)
                    boot=rng.choice(eligible,size=(2000,len(eligible)),replace=True).mean(1)
                    effects.append({'arm':arm,'seed':seed,'version':version,'actual_minus_exchanged_low_decrease':float(np.mean(eligible)),
                                    'actual_mean_low_decrease':float(np.mean(actual_changes)),
                                    'exchanged_mean_low_decrease':float(np.mean(exchange_changes)),
                                    'ci025':float(np.quantile(boot,.025)),'ci975':float(np.quantile(boot,.975)),
                                    'eligible_batches':len(eligible),'ineligible_batches':bad,
                                    'uncertainty_scope':'paired donor/probe batch resampling; seed-conditioned'})
    csv_out(output/'intervention_all_effects.csv',allrows);csv_out(output/'intervention_paired_effects.csv',effects)
    write_json(output/'intervention_summary.json',{'completed_runs':len({(r['arm'],r['seed']) for r in effects}),
                 'effects':effects,'positive_sign':'actual donor route causes greater one-step low-feature probe loss decrease',
                 'boundary':'SGD zero momentum/weight decay at frozen midpoint; not the Adam trajectory; expert norm matching isolates direction locally'})
    return effects


def structure_figure(root,figdir,manifest):
    s=root/'structure';fig,ax=plt.subplots(2,2,figsize=(11,8.5));meta={}
    controls=s/'full_group_controls.csv';summary=s/'full_repair_summary.json'
    if controls.exists() and summary.exists():
        rows=read_csv(controls);sizes=np.array([int(r['size']) for r in rows]);real=np.array([float(r['observed_strict_SD']) for r in rows]);
        ctrl=np.array([float(r['meanmatched_strict_SD']) for r in rows]);weights=[np.ones(len(rows))/len(rows),sizes/sizes.sum()]
        for j,w in enumerate(weights):
            ax[0,0].bar([j*3,j*3+1],[w@real,w@ctrl],color=['#3264a0','#888888'],width=.8)
            for x,y in [(j*3,w@real),(j*3+1,w@ctrl)]:ax[0,0].text(x,y+.012,f'{y:.3f}',ha='center',fontsize=9)
        ax[0,0].set_xticks([.5,3.5],['Group equal','Member weighted']);ax[0,0].set_ylabel('Within-group SD of log10 frequency (dex)')
        ax[0,0].set_title('Full cache: actual / mean-matched control\n186/186 groups qualified')
        from matplotlib.patches import Patch
        ax[0,0].legend(handles=[Patch(color='#3264a0',label='Actual'),Patch(color='#888888',label='Mean-matched control')],fontsize=8)
        sm=read_json(summary);keys=['small_size2_3','medium_size4_19','large_size20plus'];x=np.arange(3)
        ax[0,1].bar(x-.18,[sm[k]['delta_groupweighted'] for k in keys],.36,label='Group equal',color='#3264a0')
        ax[0,1].bar(x+.18,[sm[k]['delta_memberweighted'] for k in keys],.36,label='Member weighted',color='#7daccb')
        ax[0,1].axhline(0,color='#333333',lw=.8);ax[0,1].set_xticks(x,['2-3 members','4-19 members','20+ members'])
        ax[0,1].set_ylabel('Actual minus matched SD (dex)');ax[0,1].set_title('Effect by group size; lower = more similar');ax[0,1].legend(fontsize=8)
        meta['full_cache_summary']=str(summary)
    else:
        unavailable(ax[0,0],'Full-cache controls NOT COMPLETED');unavailable(ax[0,1],'Size strata NOT COMPLETED')
    repaired=s/'triple_counting_repair'/'null_results.json'
    nullfile=repaired if repaired.exists() else s/'null_results.json'
    if nullfile.exists():
        null=read_json(nullfile);draws=null.get('draws',[]);obs=null.get('observed',{});status=null.get('status','UNKNOWN')
        for axis,key,label in [(ax[1,0],'T_a','Matched-community member Jaccard\n(group-equal mean)'),(ax[1,1],'T_b_smoothed','SD difference (Jeffreys-smoothed dex)')]:
            values=[r[key] for r in draws if isinstance(r,dict) and r.get(key) is not None]
            missing=len(draws)-len(values)
            if missing:
                unavailable(axis,f'{key}: NA in {missing}/{len(draws)} null draws\nNo valid-only reference distribution')
            elif values and obs.get(key) is not None:
                axis.hist(values,bins=min(15,len(values)),color='#999999',alpha=.8,label=f'Null B={len(values)}')
                axis.axvline(obs[key],color='#3264a0',lw=2,label=f'Actual {obs[key]:.3f}')
                axis.set_xlabel(label);axis.set_ylabel('Randomization draws');axis.legend(fontsize=8)
                complete=null.get('B_completed',len(draws))==null.get('B_requested',99)
                axis.set_title('4096 positions/side: bounded pipeline null'+('' if complete else '\nPARTIAL snapshot'))
            else:unavailable(axis,f'Bounded null: {status}\nNo eligible reference distribution')
        meta['bounded_null_summary']=str(nullfile);meta['bounded_scope']='4096 positions/side; cannot calibrate full-cache score'
    else:
        unavailable(ax[1,0],'Bounded null NOT COMPLETED');unavailable(ax[1,1],'Bounded null NOT COMPLETED')
    fig.tight_layout();save(fig,figdir,'figure1_structure',manifest,meta)


def direction_figure(root,figdir,manifest):
    auxroot=root/'data'/'first_direction'
    if not (auxroot/'heatmap_data.npz').exists():auxroot=root/'first_direction'
    path=auxroot/'heatmap_data.npz'
    if not path.exists():return {'status':'NOT_COMPLETED','expected':str(path)}
    d=np.load(path);summary=read_json(auxroot/'summary.json')
    provenance_file=auxroot/'figures/provenance.json'
    provenance=read_json(provenance_file) if provenance_file.exists() else {}
    fig,axes=plt.subplots(3,1,figsize=(12,10),sharex=True)
    maximum=max(d['z_original'].max(),d['z_removed'].max());diff=max(abs(d['z_difference'].min()),abs(d['z_difference'].max()))
    for ax,key,title in zip(axes,['z_original','z_removed','z_difference'],['Original gated shared latent','After removing per-layer first direction','Removed minus original']):
        im=ax.imshow(d[key],aspect='auto',interpolation='nearest',cmap='RdBu_r' if key=='z_difference' else 'viridis',
                     vmin=-diff if key=='z_difference' else 0,vmax=diff if key=='z_difference' else maximum)
        ticks=np.arange(len(d['feature_ids']));ax.set_yticks(ticks,[str(i) for i in d['feature_ids'][ticks]],fontsize=6)
        ax.set_ylabel('Fixed feature ID');ax.set_title(title);fig.colorbar(im,ax=ax,label='Gated activation z')
    axes[-1].set_xlabel('Same ordered text prediction position t (first 256 measured positions)')
    fig.suptitle(f"Fixed 32 shared-latent features, 256 plotted positions; full measurement N={summary['measurement_positions']:,}",fontsize=11)
    fig.tight_layout();save(fig,figdir,'figure2_direction_sensitivity',manifest,{'heatmap_source':str(path),'summary':str(auxroot/'summary.json'),
                            'feature_selection':provenance.get('feature_selection','see source aux_direction.py'),
                            'feature_selection_provenance':str(provenance_file),'fixed_feature_ids':d['feature_ids'].tolist(),
                            'measurement_positions':summary['measurement_positions'],'plotted_positions':d['z_original'].shape[1],
                            'no_random_direction_control':True})
    return {'status':'COMPLETE'}


def learning_figures(root,figdir,manifest,rows,endpoints,loads,cfg):
    if not rows:return
    fig,axes=plt.subplots(1,2,figsize=(12,4.6))
    for ax,key,title in zip(axes,['low_loss','overall'],['Fixed low-feature conditional loss','Overall next-token loss']):
        initial=next(r[key] for r in rows if r['step']==0)
        ax.axhline(initial,color='#666666',ls='--',lw=1.3,label='Frozen base (zero adapter)')
        for arm in ('R','F','N'):
            rr=[r for r in rows if r['arm']==arm];steps=sorted({int(r['tokens_seen']) for r in rr})
            for seed in cfg['paired_seeds']:
                per=sorted([r for r in rr if r['seed']==seed],key=lambda r:r['tokens_seen'])
                ax.plot([r['tokens_seen'] for r in per],[r[key] for r in per],color=COLORS[arm],lw=.8,alpha=.35)
            means=[np.mean([r[key] for r in rr if r['tokens_seen']==s]) for s in steps]
            ax.plot(steps,means,color=COLORS[arm],lw=2.3,label=arm)
        ax.set_title(title);ax.set_xlabel('Cumulative valid training prediction tokens');ax.set_ylabel('NTP loss (nat)');ax.legend()
        ax.grid(alpha=.15)
    fig.tight_layout();save(fig,figdir,'figure3_learning_curves',manifest,{'source':str(root/'analysis_outputs/learning_metrics.csv'),
              'thin_lines':'individual trained seeds','thick_lines':'arithmetic seed mean','frozen_baseline':'initial zero-adapter loss, identical all routes/seeds',
              'evaluation_set':'fixed across checkpoints and conditions'})
    changes=read_csv(root/'analysis_outputs/zero_reference_changes.csv')
    fig,axes=plt.subplots(1,3,figsize=(13,4.5))
    for ax,metric,title in zip(axes,['low','overall','high'],['Low-feature conditional','Overall NTP','High-feature conditional']):
        for j,arm in enumerate(('R','F','N')):
            rr=[r for r in changes if r['metric']==metric and r['arm']==arm]
            values=[float(r['final_minus_initial_nat']) for r in rr]
            if values:
                ax.bar(j,np.mean(values),color=COLORS[arm],alpha=.3,width=.65)
                ax.scatter(j+np.linspace(-.12,.12,len(values)),values,color=COLORS[arm],s=30)
        ax.axhline(0,color='#333333',lw=.9);ax.set_xticks(range(3),['R','F','N']);ax.set_xlabel('Route condition');ax.set_title(title)
        ax.grid(axis='y',alpha=.15)
    axes[0].set_ylabel('Final minus frozen-base loss (nat)\nPositive = damage relative to zero adapter')
    fig.tight_layout();save(fig,figdir,'supplement_zero_reference',manifest,{'source':str(root/'analysis_outputs/zero_reference_changes.csv'),
                 'quantity':'final_minus_initial_nat; positive is worse than frozen base','points':'individual paired seeds','bars':'seed means'})
    if endpoints:
        fig,axes=plt.subplots(1,2,figsize=(11,4.7),sharey=True)
        for ax,metric in zip(axes,['low','overall']):
            for j,seed in enumerate(cfg['paired_seeds']):
                for c,offset,color in [('R-F',-.13,COLORS['F']),('R-N',.13,COLORS['N'])]:
                    r=next((r for r in endpoints if r['metric']==metric and r['contrast']==c and r['seed']==seed),None)
                    if r:
                        ax.errorbar(r['difference_nat'],j+offset,xerr=[[max(0,r['difference_nat']-r['ci025'])],[max(0,r['ci975']-r['difference_nat'])]],
                                    fmt='o',color=color,label=c if j==0 else None,capsize=3)
            ax.axvline(0,color='#333333',lw=.9);ax.set_xlabel('Endpoint loss difference (nat); negative favors R')
            ax.set_title('Low-feature conditional' if metric=='low' else 'Overall NTP');ax.grid(axis='x',alpha=.15);ax.legend()
        axes[0].set_yticks(range(len(cfg['paired_seeds'])),[str(x) for x in cfg['paired_seeds']]);axes[0].set_ylabel('Paired training seed')
        fig.tight_layout();save(fig,figdir,'figure4_paired_endpoints',manifest,{'source':str(root/'analysis_outputs/paired_endpoints.csv'),
                   'interval':'approximate 95% paired 4-consecutive-context block bootstrap, linearized fixed-feature mean; conditional on each seed; not document independent','no_seed_mean_ci':True})
    if loads:
        fig,axes=plt.subplots(1,2,figsize=(11,4.5))
        for j,arm in enumerate(('R','F','N')):
            for e in range(4):
                rr=[r for r in loads if r['arm']==arm and r['expert']==e]
                axes[0].bar(e+(j-1)*.24,np.mean([r['fraction'] for r in rr]),.24,color=COLORS[arm],label=arm if e==0 else None)
                axes[1].bar(e+(j-1)*.24,np.mean([r['nonzero_gradient_updates'] for r in rr]),.24,color=COLORS[arm],label=arm if e==0 else None)
        axes[0].axhline(.25,color='#333333',ls='--',lw=.8);axes[0].set_ylabel('Fraction of training tokens')
        axes[1].set_ylabel('Updates with nonzero expert gradient')
        for ax in axes:ax.set_xlabel('Expert ID');ax.set_xticks(range(4));ax.legend();ax.grid(axis='y',alpha=.15)
        fig.tight_layout();save(fig,figdir,'supplement_expert_load',manifest,{'source':str(root/'analysis_outputs/expert_exposure.csv'),
                                           'averaging':'mean over paired seeds; raw per-seed values retained'})


def intervention_figure(root,figdir,manifest,effects,cfg):
    if not effects:return
    fig,axes=plt.subplots(2,2,figsize=(11,8),sharex=True,sharey='row')
    for column,version in enumerate(['raw','expert_norm_matched']):
        top=axes[0,column];ax=axes[1,column]
        for j,arm in enumerate(('R','F','N')):
            rr=[r for r in effects if r['arm']==arm and r['version']==version]
            for k,r in enumerate(rr):
                x=j+(k-(len(rr)-1)/2)*.16;y=r['actual_minus_exchanged_low_decrease']
                top.scatter(x-.025,r['actual_mean_low_decrease'],marker='o',color=COLORS[arm],s=35)
                top.scatter(x+.025,r['exchanged_mean_low_decrease'],marker='x',color=COLORS[arm],s=40)
                ax.errorbar(x,y,yerr=[[max(0,y-r['ci025'])],[max(0,r['ci975']-y)]],fmt='o',color=COLORS[arm],capsize=3)
        for axis in [top,ax]:axis.axhline(0,color='#333333',lw=.9);axis.set_xticks(range(3),['R','F','N']);axis.grid(axis='y',alpha=.15)
        ax.set_xlabel('Training route condition')
        top.set_title('Same SGD step size' if version=='raw' else 'Per-expert update norms matched')
        from matplotlib.lines import Line2D
        top.legend(handles=[Line2D([0],[0],marker='o',color='black',ls='',label='Actual donor route'),
                            Line2D([0],[0],marker='x',color='black',ls='',label='Frequency-matched exchange')],fontsize=8)
    axes[0,0].set_ylabel('One-step low-feature probe loss decrease (nat)\nPositive = improvement; each point a seed mean')
    axes[1,0].set_ylabel('Actual minus exchanged loss decrease (nat)\nPositive = actual causes greater decrease')
    fig.suptitle('Three paired seeds left to right: '+', '.join(str(s) for s in cfg['paired_seeds']),fontsize=10)
    fig.tight_layout();save(fig,figdir,'figure5_local_update',manifest,{'source':str(root/'analysis_outputs/intervention_paired_effects.csv'),
        'interval':'95% paired donor/probe batch bootstrap, conditional on each trained seed',
        'donor':'frequency-bin route-label exchange preserves each expert token count','probe':'original routing always fixed'})


def response_figure(root,figdir,manifest):
    source=root/'response_decomposition';rows=[];guards=[]
    for path in sorted(source.glob('seed_*/*/completion.json')):
        receipt=read_json(path)
        if receipt['status']!='COMPLETE':continue
        if not all(v['per_position_loss_exact'] for v in receipt['zero_full_guards'].values()):
            raise ValueError('Response zero/full reproduction failed')
        original=root/'learning'/f"seed_{receipt['seed']}"/receipt['arm']
        resolved=read_json(original/'run_contract.json')['config'];loss_rows=read_csv(path.with_name('losses.csv'))
        for state,step in [('zero',0),('full',resolved['updates'])]:
            native=read_json(original/f'eval_{step:05d}.json')
            for metric,key in [('overall','overall'),('low','low_loss'),('high','high_loss')]:
                got=float(next(r['loss_nat'] for r in loss_rows if r['state']==state and r['metric']==metric))
                if not np.isclose(got,native[key],rtol=0,atol=1e-8):
                    raise ValueError('Response changed C metric/cohort: '+metric)
        rows.extend(read_csv(path.with_name('effects.csv')));guards.append(receipt)
    if not rows:return {'status':'NOT_COMPLETED'}
    output=root/'analysis_outputs';csv_out(output/'response_decomposition_effects.csv',rows)
    summary={'status':'COMPLETE' if len(guards)==9 else 'PARTIAL','completed_runs':len(guards),
       'prediction':str(source/'prediction.json'),'no_new_training':True,'original_complete_h_and_routes_fixed':True,
       'zero_and_full_original_arrays_exact':True,
       'fixed_low_high_metric_reproduction_within_1e_minus_8_nat':True,
       'max_linear_response_relative_L2_error':max(g['linear_response_decomposition']['relative_response_L2_error'] for g in guards),
       'effects':{}}
    for arm in ['R','F','N']:
        summary['effects'][arm]={}
        for metric in ['overall','low','high']:
            rr=[r for r in rows if r['arm']==arm and r['metric']==metric]
            if not rr:continue
            summary['effects'][arm][metric]={k:{'seed_values':[float(r[k]) for r in rr],
               'mean':float(np.mean([float(r[k]) for r in rr]))}
               for k in ['full_damage_nat','constant_only_damage_nat','centered_only_damage_nat','loss_interaction_nat']}
    write_json(output/'response_decomposition_summary.json',summary)
    fig,axes=plt.subplots(1,2,figsize=(13,5))
    fields=['full_damage_nat','constant_only_damage_nat','centered_only_damage_nat','loss_interaction_nat']
    labels=['Full response','Constant only','Centered only','Loss interaction']
    for ax,metric,title in zip(axes,['overall','low'],['Overall next-token loss','Fixed low-feature conditional loss']):
        for j,arm in enumerate(['R','F','N']):
            rr=[r for r in rows if r['arm']==arm and r['metric']==metric]
            for k,field in enumerate(fields):
                values=[float(r[field]) for r in rr];x=k+(j-1)*.24
                if not values:continue
                ax.bar(x,np.mean(values),width=.22,color=COLORS[arm],alpha=.35,label=arm if k==0 else None)
                ax.scatter(x+np.linspace(-.045,.045,len(values)),values,color=COLORS[arm],s=22)
        ax.axhline(0,color='#333333',lw=.9);ax.set_xticks(range(4),labels,rotation=15,ha='right')
        ax.set_title(title);ax.legend();ax.grid(axis='y',alpha=.15)
    axes[0].set_ylabel('Loss damage or interaction (nat)\nPositive = damage or super-additive damage')
    fig.suptitle('Frozen final adapter: TRAIN-only expert mean response decomposition; individual seed points',fontsize=11)
    fig.tight_layout();save(fig,figdir,'supplement_response_decomposition',manifest,{'source':str(output/'response_decomposition_effects.csv'),
        'prediction':str(source/'prediction.json'),'states':'original complete h plus full / constant-only / centered-only adapter response',
        'means':'TRAIN original-route expert means; no targets or EVAL fitting',
        'interaction':'Lfull-Lconstant-Lcentered+Lzero; effects are not assumed additive',
        'boundary':'functional response components at this fixed checkpoint; not common semantics or complete training root cause'})
    return summary


def main(args):
    torch.set_num_threads(4)
    root=Path(args.root);figdir=root/'figures'
    old_manifest=root/'analysis_outputs/figure_manifest.json'
    manifest=read_json(old_manifest) if old_manifest.exists() else {}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'pdf.fonttype':42,'svg.fonttype':'none'})
    if args.structure_only:
        structure_figure(root,figdir,manifest);write_json(old_manifest,manifest)
        print(json.dumps({'refreshed':'figure1_structure','no_learning_reaggregation':True}),flush=True);return
    if args.response_only:
        summary=response_figure(root,figdir,manifest);write_json(old_manifest,manifest)
        print(json.dumps({'response_decomposition':summary.get('status'),'completed_runs':summary.get('completed_runs',0),
                          'no_learning_reaggregation':True}),flush=True);return
    config=Path(args.config) if args.config else root/'config/formal.json'
    cfg=read_json(config);cfg['_config_sha256']=__import__('hashlib').sha256(config.read_bytes()).hexdigest()
    rows,endpoints,loads,summary=analyze_learning(root,cfg);effects=analyze_intervention(root,cfg)
    if not args.skip_structure:structure_figure(root,figdir,manifest)
    aux=direction_figure(root,figdir,manifest)
    learning_figures(root,figdir,manifest,rows,endpoints,loads,cfg);intervention_figure(root,figdir,manifest,effects,cfg)
    write_json(root/'analysis_outputs/figure_manifest.json',manifest)
    write_json(root/'analysis_outputs/analysis_status.json',{'learning':summary,'direction':aux,
               'intervention_completed_runs':len({(r['arm'],r['seed']) for r in effects}),
               'scientific_judgment':'UNASSIGNED','all_intervals_seed_conditioned':True})
    print(json.dumps({'figures':list(manifest),'completed_learning_runs':summary['completed_runs'],
                      'completed_intervention_runs':len({(r['arm'],r['seed']) for r in effects})}),flush=True)


def selftest():
    data={'feature_ptr':torch.tensor([0,1,3,4,4]),'feature_ids':torch.tensor([0,0,1,1]),
          'low_ids':torch.tensor([0,1])}
    blocks=np.array([0,0,1,1]);view=FixedFeatureView(data,'low',1,blocks)
    delta=np.array([1.,2.,3.,4.]);point,inf=view.difference(delta)
    assert point==2. and np.allclose(inf,[-.125,.125])
    # Check the linearized ratio derivative against the exact weighted ratio.
    direction=np.array([.7,-.4]);eps=1e-5;weights=1+eps*direction
    r=view.row;f=view.feature;w=weights[blocks[r]]
    exact=(np.bincount(f,weights=w*delta[r])/np.bincount(f,weights=w)).mean()
    assert np.isclose((exact-point)/eps,direction@inf,atol=1e-6)
    p,i=view.difference(np.ones(4));assert p==1. and np.allclose(i,0)
    print(json.dumps({'status':'PASS','overlapping_feature_mean':True,'paired_context_ratio_influence_derivative':True,
                       'constant_difference_zero_uncertainty':True}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root');p.add_argument('--config');p.add_argument('--selftest',action='store_true')
    p.add_argument('--structure-only',action='store_true');p.add_argument('--skip-structure',action='store_true')
    p.add_argument('--response-only',action='store_true');a=p.parse_args()
    if a.selftest:selftest()
    else:main(a)
