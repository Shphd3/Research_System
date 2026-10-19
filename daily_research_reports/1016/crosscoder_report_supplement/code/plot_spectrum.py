#!/usr/bin/env python3
"""Replot fixed representation spectra from saved small result tables only."""
import argparse,csv,json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/report_spectrum/20261016_spectrum'));ap.add_argument('--font',type=Path,default=Path('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf'));ap.add_argument('--out',type=Path);a=ap.parse_args();out=a.out or a.root/'figures';out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':18,'axes.titlesize':24,'axes.labelsize':21,'xtick.labelsize':16,'ytick.labelsize':16,'legend.fontsize':18,'figure.facecolor':'white','axes.facecolor':'white','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.titlepad':18,'savefig.facecolor':'white'})
    fp=FontProperties(fname=str(a.font));plt.rcParams['font.family']=fp.get_name()
    from matplotlib import font_manager
    font_manager.fontManager.addfont(str(a.font))
    colors=['#3572B0','#D98928'];labels=['同频','混频'];rules=['same_frequency','mixed_frequency']
    curves=[];outputs=[]
    for state,prefix in [('original',''),('column_shuffled','appendix_shuffled_')]:
        fig,ax=plt.subplots(figsize=(8.4,6.6),layout='constrained')
        first=[]
        for rule,color,label in zip(rules,colors,labels):
            p=a.root/f'{state}_{rule}_spectra.npz'
            with np.load(p) as z:
                shares=z['variance_shares'];valid=z['estimable'];mean=shares[valid].mean(0);first.append(shares[valid,0].copy())
            ax.plot(np.arange(1,15),mean,color=color,label=label,lw=3.0,marker='o',ms=5)
            curves.extend({'state':state,'rule':rule,'direction_index':j+1,'group_equal_variance_share_mean':float(x),'estimable_groups':int(valid.sum())} for j,x in enumerate(mean))
        ax.set_title('归一化谱');ax.set_xlabel('方向序号');ax.set_ylabel('方差占比');ax.set_xlim(.7,14.3);ax.set_ylim(bottom=0);ax.set_xticks([1,2,4,6,8,10,12,14]);ax.grid(axis='y',alpha=.15);ax.legend(frameon=False)
        base=out/(prefix+'figure3_normalized_spectrum')
        for ext in ['png','pdf']:fig.savefig(base.with_suffix('.'+ext),dpi=220);outputs.append(base.with_suffix('.'+ext))
        plt.close(fig)
        fig,ax=plt.subplots(figsize=(8.4,6.6),layout='constrained');rng=np.random.default_rng(2026101604)
        for k,(v,color) in enumerate(zip(first,colors),1):
            jitter=rng.uniform(-.19,.19,len(v));ax.scatter(k+jitter,v,color=color,alpha=.16,s=12,edgecolors='none',rasterized=False,zorder=1)
        bp=ax.boxplot(first,positions=[1,2],widths=.42,showfliers=False,patch_artist=True,medianprops={'color':'#202020','lw':2.0},boxprops={'lw':1.8},whiskerprops={'lw':1.5},capprops={'lw':1.5})
        for patch,color in zip(bp['boxes'],colors):patch.set_facecolor('white');patch.set_edgecolor(color);patch.set_alpha(.85)
        ax.scatter([1,2],[v.mean() for v in first],color=colors,marker='D',s=70,edgecolors='white',linewidths=.8,zorder=4)
        ax.set_title('第一方向占比');ax.set_xlabel('分组规则');ax.set_ylabel('第一方向占比');ax.set_xticks([1,2],labels);ax.set_xlim(.5,2.5);ax.set_ylim(0,1.03);ax.grid(axis='y',alpha=.15)
        base=out/(prefix+'figure4_first_direction_share')
        for ext in ['png','pdf']:fig.savefig(base.with_suffix('.'+ext),dpi=220);outputs.append(base.with_suffix('.'+ext))
        plt.close(fig)
    with (out/'normalized_spectrum_plot_data.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(curves[0]));w.writeheader();w.writerows(curves)
    (out/'plot_provenance.json').write_text(json.dumps({'plot_script':str(Path(__file__).resolve()),'plot_script_sha256':sha(__file__),'font_path':str(a.font),'font_sha256':sha(a.font),'source_config_sha256':sha(a.root/'frozen_config.json'),'source_summary_sha256':sha(a.root/'spectrum_summary.json'),'all_group_points':'All estimable groups shown; boxes median/IQR and1.5IQR whiskers; diamonds group-equal means; no inferential error bars.','colors':dict(zip(labels,colors)),'outputs':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in outputs]},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'COMPLETE','figures':len(outputs),'output':str(out)},ensure_ascii=False))
if __name__=='__main__':main()
