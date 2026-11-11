from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager,ticker
import matplotlib.pyplot as plt
X=Path(__file__).resolve().parents[1]; ROOT=X.parent; BASE=ROOT.parent
R4=BASE/'20261109_atom_concentration_regularizer'
R=Path('/data/250010109/Research_System/daily_research_reports/1111/meeting_report')
O=R/'learn_forget_figures/followup2'; F=O.parent/'followup'
font=ROOT/'followup/data/NotoSansCJKsc-Regular.otf'
font_manager.fontManager.addfont(str(font))
plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':15,'axes.unicode_minus':False,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelsize':16,'xtick.labelsize':14,'ytick.labelsize':14})
names={'A0':'原生 MoE','A5':'按 feature 共现分组（A5）','A2':'随机分发（A2）','Dense':'Dense'}
colors={'A0':'#2471a3','A5':'#7254a3','A2':'#777777','Dense':'#d97720'}
def save(fig,name):
    for ext in ('png','pdf'): fig.savefig(O/f'{name}.{ext}',dpi=175,bbox_inches='tight',facecolor='white')
    plt.close(fig)
def one():
    old=pd.read_csv(R/'a5_checks/check3_document_bootstrap.csv')
    bas=pd.read_csv(O.parent/'baseline_NLL_document_CI.csv')
    last=pd.read_csv(R/'a5_to_1B/endpoint_CI.csv').query('pair=="A5-MoE_baseline" and band=="overall"').iloc[0]
    rows=[]
    for x in bas.query('tokens>0').itertuples(): rows.append(('dense',x.tokens,'正式原生 baseline',x.paired_fp16_difference,x.ci95_low,x.ci95_high,'baseline_NLL_document_CI.csv'))
    for s in (500,1000,1500,2000):
        y=old.query('step==@s and pair=="A5-A0" and band=="overall"')
        if len(y):
            y=y.iloc[0]; mid,lo,hi=-y.paired_difference,-y.ci95_high,-y.ci95_low; src='R04 配对结果（check3_document_bootstrap.csv）'
        else:
            n=2097152
            docs=np.cumsum(np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r')[:n]==151645)
            data=[np.load(R4/f'analysis/positions/{a}/step{s:06d}.npz')['loss'].astype('float64') for a in ('A0','A5')]
            z=data[0]-data[1]; sums=np.bincount(docs,weights=z); cnt=np.bincount(docs); m=len(cnt)
            rng=np.random.default_rng(20261111); boot=[]
            for j in range(20):
                k=rng.integers(m,size=(100,m)); boot.extend(sums[k].sum(1)/cnt[k].sum(1))
            mid=z.mean();lo,hi=np.quantile(boot,[.025,.975]);src=f'既有 R04 逐位置损失，新做配对文档 bootstrap（{m} 文档/2000 重抽）'
        rows.append(('a5',s*262144,f'原生 MoE（A0），{s} 步',mid,lo,hi,src))
    rows.append(('a5',1000000000,'正式原生 baseline；A5 实际 1.000341504B',-last.difference,-last.ci95_high,-last.ci95_low,'R06 endpoint_CI.csv'))
    d=pd.DataFrame(rows,columns=['series','tokens','reference','difference_nat','ci95_low','ci95_high','source'])
    d.to_csv(O/'01_损失差.csv',index=False)
    for zoom,fn in [(False,'01_两种损失差_0到10B'),(True,'01_两种损失差_0到1B放大')]:
        fig,ax=plt.subplots(figsize=(12,5.8),layout='constrained')
        for k,lab,c in [('dense','Dense − 原生 MoE',colors['A0']),('a5','原生 MoE − 按 feature 共现分组（A5）',colors['A5'])]:
            x=d[(d.series==k)&(d.tokens<=(1e9 if zoom else 1e10))];ts=x.tokens.to_numpy()/1e9; y=x.difference_nat.to_numpy()
            ax.errorbar(ts,y,yerr=[y-x.ci95_low,x.ci95_high-y],fmt='o',ms=7,capsize=5,elinewidth=1.7,color=c,label=lab,zorder=3)
            ax.plot(ts if k=='dense' else ts[:-1],y if k=='dense' else y[:-1],color=c,lw=2.2)
            if k=='a5': ax.plot(ts[-2:],y[-2:],'--',lw=2,color=c)
        ax.set_title('两种损失差：架构差距大体维持，分发优势缩小',loc='left',fontsize=19,pad=13)
        ax.set_xlabel('累计训练 token（B）');ax.set_ylabel('损失差（nat）')
        ax.axhline(0,c='#aaa',lw=1)
        if zoom: ax.set_xlim(0,1.035)
        else:
            ax.set_xscale('symlog',linthresh=.09);ax.set_xlim(0,11);ax.set_xticks([0,.13,.26,.52,1,3,5,10]);ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
        ax.grid(alpha=.22);ax.legend(loc='upper right',fontsize=13,frameon=True)
        save(fig,fn)
    a=d[d.series=='a5'].difference_nat.tolist()
    (O/'01_读图.md').write_text(f"""## 1｜两种差距放在一起

![0–10B 损失差](01_两种损失差_0到10B.png)

[主图 PDF](01_两种损失差_0到10B.pdf) · [0–1B 线性放大 PNG](01_两种损失差_0到1B放大.png) / [PDF](01_两种损失差_0到1B放大.pdf) · [点值与区间](01_损失差.csv)

**读图：** 蓝线（Dense − 原生 MoE）从 0.5B 到 10B 一直约为 0.09 nat；紫线（原生 MoE − A5）到约 1B 仍为正，但优势由 500/1000/1500/2000 步的 {a[0]:.3f}/{a[1]:.3f}/{a[2]:.3f}/{a[3]:.3f} 降到 **{a[4]:.3f} nat**。误差棒是配对文档 95% 区间。紫色虚线提醒：1B 改用正式原生 baseline；A5 实际 1.000341504B。500 步用既有逐位置 loss 补算区间。
""")
def two():
    f=pd.read_csv(F/'F_statistics.csv').query('condition=="actual" and view=="own"')
    d=f.groupby(['arm','layer']).rank_ratio_to_global.agg(median='median',q10=lambda x:x.quantile(.1),q90=lambda x:x.quantile(.9)).reset_index()
    assert len(d)==24
    d.assign(model=d.arm.map(names)).to_csv(O/'02_逐层有效秩比.csv',index=False)
    pivot=d.pivot(index='layer',columns='arm',values='median')[['A0','A5','A2']]
    fig,(ax,tb)=plt.subplots(1,2,figsize=(14,6.25),gridspec_kw={'width_ratios':[2.1,1]},layout='constrained')
    for a in ('A0','A5','A2'):
        z=d[d.arm==a];ax.plot(z.layer,z['median'],'o-',color=colors[a],label=names[a],lw=2.3,ms=6)
        ax.fill_between(z.layer.to_numpy(),z.q10.to_numpy(),z.q90.to_numpy(),color=colors[a],alpha=.17)
    ax.axhline(1,c='#444',ls='--',lw=1.5,label='Dense：所有输入进同一个 FFN')
    ax.set(xlabel='FFN 层号',ylabel='每个 expert 的输入有效秩 ÷ 全部输入的有效秩',xticks=range(8))
    ax.grid(alpha=.22);ax.legend(fontsize=12,loc='lower right')
    tb.axis('off'); tb.set_title('逐层中位数',pad=5,fontsize=15)
    t=tb.table(cellText=[[str(i),*(f'{y:.3f}' for y in v)] for i,v in pivot.iterrows()],colLabels=['层号','原生 MoE','按 feature\n共现分组（A5）','随机分发\n（A2）'],colWidths=[.14,.24,.34,.28],bbox=(0,.055,1,.87),cellLoc='center')
    t.auto_set_font_size(False);t.set_fontsize(12)
    for (i,j),c in t.get_celld().items():
        c.set_edgecolor('#e2e4e8')
        if i==0: c.set_facecolor('#edf1f4');c.set_height(c.get_height()*1.5)
        elif i%2==0: c.set_facecolor('#f7f8fb')
    fig.suptitle('按专家分组后，输入方差分布在多少个有效方向？',fontsize=19,fontweight='bold')
    save(fig,'02_专家输入有效秩')
    (O/'02_读图.md').write_text("""## 2｜专家输入谱：只留条件有效秩

![每层条件有效秩比](02_专家输入有效秩.png)

[投屏 PDF](02_专家输入有效秩.pdf) · [逐层中位数和分位数](02_逐层有效秩比.csv)

**读图：** 横轴是层号，纵轴是每个 expert 输入的有效秩除以该层全体输入的有效秩；点为 8 个 expert 的中位数，阴影为专家间 10%–90% 分位。原生 MoE 和 A5 多数层低于随机分发，A5 并非逐层低于原生。三臂均为各自 2000 步训练表征，沿用 F 的既有 EVAL 面板；Dense 虚线 1 是所有输入进入同一个 FFN 时的定义参照。
""")
if __name__=='__main__': one();two()
