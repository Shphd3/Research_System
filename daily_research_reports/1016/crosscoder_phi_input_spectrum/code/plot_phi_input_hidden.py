#!/usr/bin/env python3
"""Plot saved phi-group-hit original-hidden spectra; never select a population.

Required input schema is documented in --help. Selection IDs are supplied by
the analysis owner, explicitly common to all R/F/N and original/residual views.
The script neither alters measurements nor silently excludes sparse/NA groups.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

ROOT=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/report_spectrum/20261016_phi_input_spectrum')
FONT=Path('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf')
COLORS={'R':'#3264A0','F':'#D78230','N':'#338C66'}
LABELS={'R':'关系','F':'频率','N':'匹配随机'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def plot_curves(data,stage,out,rank):
    title='归一化谱' if stage=='original' else '剩余归一化谱'
    name='figure7_phi_raw_spectrum' if stage=='original' else 'figure9_phi_residual_spectrum'
    fig,ax=plt.subplots(figsize=(8.8,6.6),layout='constrained');rows=[]
    for arm in ['R','F','N']:
        norm=data[arm][stage]
        assert np.isfinite(norm).all() and np.all(norm>=-1e-10)
        assert np.allclose(norm.sum(1),1,rtol=1e-7,atol=1e-7)
        mean=norm.mean(0)
        ax.plot(np.arange(1,rank+1),mean[:rank],color=COLORS[arm],lw=3.0,label=LABELS[arm])
        rows.extend({'stage':stage,'arm':arm,'direction_index':j+1,'equal_group_mean_variance_share':float(value),'groups':len(norm),'displayed':bool(j<rank)} for j,value in enumerate(mean))
    ax.set_title(title);ax.set_xlabel('方向序号');ax.set_ylabel('方差占比')
    ax.set_xlim(1,rank);ax.set_ylim(bottom=0)
    ticks=np.unique(np.array([1,round(rank/4),round(rank/2),round(3*rank/4),rank]))
    ax.set_xticks(ticks);ax.grid(axis='y',alpha=.15);ax.legend(frameon=False)
    outputs=[]
    for ext in ['png','pdf']:
        p=out/(name+'.'+ext);fig.savefig(p,dpi=240);outputs.append(p)
    plt.close(fig)
    return rows,outputs

def plot_first(data,stage,out,first_ylim):
    title='第一方向占比' if stage=='original' else '剩余第一方向占比'
    name='figure8_phi_raw_first_share' if stage=='original' else 'figure10_phi_residual_first_share'
    fig,ax=plt.subplots(figsize=(8.8,6.6),layout='constrained');rng=np.random.default_rng(2026101608)
    first=[data[arm][stage][:,0] for arm in ['R','F','N']]
    for k,(arm,value) in enumerate(zip(['R','F','N'],first),1):
        ax.scatter(k+rng.uniform(-.18,.18,len(value)),value,s=19,alpha=.26,color=COLORS[arm],edgecolors='none',zorder=1)
    bp=ax.boxplot(first,positions=[1,2,3],widths=.43,showfliers=False,patch_artist=True,medianprops={'color':'#202020','lw':2.},boxprops={'lw':1.8},whiskerprops={'lw':1.5},capprops={'lw':1.5})
    for patch,arm in zip(bp['boxes'],['R','F','N']):
        patch.set_facecolor('white');patch.set_edgecolor(COLORS[arm]);patch.set_alpha(.82)
    ax.scatter([1,2,3],[x.mean() for x in first],marker='D',s=75,color=[COLORS[x] for x in ['R','F','N']],edgecolors='white',linewidths=.8,zorder=4)
    ax.set_title(title);ax.set_xlabel('分组规则');ax.set_ylabel('第一方向占比');ax.set_xticks([1,2,3],[LABELS[x] for x in ['R','F','N']]);ax.set_xlim(.5,3.5);ax.set_ylim(0,first_ylim);ax.grid(axis='y',alpha=.15)
    outputs=[]
    for ext in ['png','pdf']:
        p=out/(name+'.'+ext);fig.savefig(p,dpi=240);outputs.append(p)
    plt.close(fig)
    return outputs

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--out',type=Path)
    ap.add_argument('--font',type=Path,default=FONT)
    ap.add_argument('--selection',type=Path,help='JSON: group_ids common across arms/stages; N_positions; original_plot_rank; residual_plot_rank; analysis_population_note. Required; no plot-derived filtering.')
    ap.add_argument('--data-pattern',default='{arm}_input_hidden_spectra.npz',help='NPZ per R/F/N: group_id, normalized_original, normalized_residual.')
    a=ap.parse_args();out=a.out or a.root/'figures';out.mkdir(parents=True,exist_ok=True)
    selection_path=a.selection or a.root/'plot_selection.json';selection=json.loads(selection_path.read_text())
    selected=np.array(selection['group_ids'],dtype=np.int64)
    assert len(selected)>0 and len(np.unique(selected))==len(selected)
    font_manager.fontManager.addfont(str(a.font));fp=font_manager.FontProperties(fname=str(a.font))
    plt.rcParams.update({'font.family':fp.get_name(),'font.size':18,'axes.titlesize':24,'axes.labelsize':21,'xtick.labelsize':16,'ytick.labelsize':16,'legend.fontsize':18,'figure.facecolor':'white','axes.facecolor':'white','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.titlepad':18,'savefig.facecolor':'white'})
    data={};inputs=[];first_rows=[]
    for arm in ['R','F','N']:
        p=a.root/a.data_pattern.format(arm=arm)
        with np.load(p) as z:
            ids=np.asarray(z['group_id'],np.int64)
            assert len(np.unique(ids))==len(ids)
            byid={int(x):i for i,x in enumerate(ids)};take=np.array([byid[int(x)] for x in selected])
            data[arm]={'original':z['normalized_original'][take].copy(),'residual':z['normalized_residual'][take].copy()}
        for stage in ['original','residual']:
            norm=data[arm][stage]
            if not np.isfinite(norm).all():raise ValueError(f'{arm}/{stage}: owner-selected population contains non-estimable values; no automatic omission')
            for group,value in zip(selected,norm[:,0]):first_rows.append({'group_id':int(group),'arm':arm,'stage':stage,'first_direction_share':float(value)})
        inputs.append({'path':str(p),'sha256':sha(p)})
    rows=[];outputs=[]
    first_max=max(float(data[arm][stage][:,0].max()) for arm in ['R','F','N'] for stage in ['original','residual'])
    first_ylim=min(1.02,max(.1,float(np.ceil(first_max*1.05/.05)*.05)))
    for stage in ['original','residual']:
        rank=int(selection[stage+'_plot_rank'])
        rr,pp=plot_curves(data,stage,out,rank);rows+=rr;outputs+=pp
        outputs+=plot_first(data,stage,out,first_ylim)
    for filename,values in [('phi_input_normalized_spectrum_plot_data.csv',rows),('phi_input_first_direction_plot_data.csv',first_rows)]:
        with (out/filename).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(values[0]));w.writeheader();w.writerows(values)
    receipt={'status':'COMPLETE','plot_script':str(Path(__file__).resolve()),'plot_script_sha256':sha(__file__),'font_path':str(a.font),'font_sha256':sha(a.font),'inputs':inputs,'selection_path':str(selection_path),'selection_sha256':sha(selection_path),'selection':selection,'groups_per_arm':len(selected),'aggregation':'First normalize every group covariance eigenvalue vector by its own nonzero total variance, then equal group arithmetic mean.','point_readout':'All selected group points shown; boxes median/IQR,1.5IQR whiskers; diamonds group-equal mean; no inferential error bars.','first_share_common_y_axis':[0,first_ylim],'colors':COLORS,'matrix_object':'Original cached model hidden at fixed phi-group-winning input positions. Residual subtracts each position-centered group PC1; not CrossCoder reconstructed group contribution or parameter spectrum.','source_covariance_data_unchanged':True,'outputs':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in outputs]}
    (out/'plot_phi_input_provenance.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':'COMPLETE','figures':len(outputs),'output':str(out)},ensure_ascii=False))

if __name__=='__main__':main()
