#!/usr/bin/env python3
"""Standalone figures for one-question-at-a-time group relation reading."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='2'
from pathlib import Path
import csv,json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager,colors

E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
O=E/'analysis/phi_relations_20261018';FIG=O/'figures'
OLD=E/'analysis/feature_frequency/20261015T143300Z'
S=Path('/data/250010109/Research_System')
FONT=S/'daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf'
CORE='#8B5CF6';OTHER='#607D8B';UNCOND='#64748B';COND='#009E73'
RFN={'R':'#3264A0','F':'#D78230','N':'#338C66'}
GROUP={68:'#007F86',34:'#8B5CF6',14:'#607D8B'}
def rows(p):return list(csv.DictReader(Path(p).open()))
def csvout(p,data):
    if not data:return
    with Path(p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
def save(fig,name,data=None):
    for ext in ('png','pdf'):fig.savefig(FIG/(name+'.'+ext),dpi=200,bbox_inches='tight')
    plt.close(fig)
    if data is not None:csvout(FIG/(name+'.csv'),data)
def setup():
    FIG.mkdir(exist_ok=True);font_manager.fontManager.addfont(str(FONT))
    plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(FONT)).get_name(),
        'font.size':14,'axes.titlesize':20,'axes.labelsize':16,'xtick.labelsize':12,'ytick.labelsize':12,
        'figure.facecolor':'white','axes.facecolor':'white','axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})

def main():
    setup();cases=json.loads((O/'cases.json').read_text());selection=json.loads((O/'selection_D.json').read_text())
    mem=rows(O/'all_members_frequency.csv');edges=rows(OLD/'main/edges_D.csv')
    conditions=rows(O/'conditional_metrics.csv');core=rows(O/'all186_core_decomposition.csv')
    for gid in (68,34,14):
        geo=np.load(O/f'geometry_G{gid:03d}.npz')
        members=geo['feature_id'];display=geo['display_feature_id'].tolist()
        local=[int(np.flatnonzero(members==f)[0]) for f in display]
        mm=[r for r in mem if int(r['group_id'])==gid];freq={int(r['feature_id']):float(r['p_V']) for r in mm}
        G=nx.Graph();G.add_nodes_from(display)
        ed=[]
        for e in edges:
            a,b=int(e['u']),int(e['v'])
            if a in G and b in G:
                weight=float(e.get('phi',e.get('weight',1)));G.add_edge(a,b,weight=weight)
                ed.append({'feature_i':a,'feature_j':b,'phi_D_frozen_edge':weight})
        # Circular coordinates are a display choice only; preserve every frozen edge.
        theta=np.arange(len(display))*2*np.pi/len(display)
        layout={f:np.array([np.cos(t),np.sin(t)]) for f,t in zip(display,theta)}
        fig,ax=plt.subplots(figsize=(10,9));mx=max(freq[f] for f in display)
        ns=[140+1850*freq[f]/mx for f in display]
        for a,b in G.edges:
            ax.plot([layout[a][0],layout[b][0]],[layout[a][1],layout[b][1]],color='#A0A7B0',alpha=.5,lw=1.1,zorder=1)
        xy=np.array([layout[f] for f in display])
        ax.scatter(xy[:,0],xy[:,1],s=ns,c=[CORE if f in selection['core_members'][str(gid)] else OTHER for f in display],edgecolors='white',zorder=2)
        for f,t in zip(display,theta):
            ax.text(1.15*np.cos(t),1.15*np.sin(t),str(f),ha='center',va='center',fontsize=12,zorder=3)
        ax.set_xlim(-1.4,1.4);ax.set_ylim(-1.4,1.4);ax.set_aspect('equal')
        ax.set_title(f'G{gid:03d} 关系图');ax.axis('off')
        save(fig,f'figure1_G{gid:03d}_graph',ed)
        csvout(FIG/f'figure1_G{gid:03d}_nodes.csv',[{'feature_id':f,'p_V_full':freq[f],'D_selected_core':f in selection['core_members'][str(gid)],'x':float(layout[f][0]),'y':float(layout[f][1]),'all_group_members':len(members),'display_members':len(display)} for f in display])
        cc=[c for c in cases if c['group_id']==gid]
        A=np.array([[int(any(a['feature_id']==f for a in c['active_members'])) for f in display] for c in cc])
        fig,ax=plt.subplots(figsize=(max(9,len(display)*.39),max(6,len(cc)*.46)))
        ax.imshow(A,aspect='auto',interpolation='nearest',cmap=colors.ListedColormap(['#FFFFFF','#1F4E79']),vmin=0,vmax=1)
        ax.set_xticks(np.arange(len(display)),display,rotation=90)
        kind={'random_hit':'随机','high_K':'高K','single_member':'单成员'}
        labels=[f"{c['position_id']} {'/'.join(kind[k] for k in c['categories'])} K={c['K_full']}/{c['K_display']}" for c in cc]
        ax.set_yticks(np.arange(len(cc)),labels);ax.set_xlabel('feature ID');ax.set_ylabel('位置／类别／K全组与展示')
        ax.set_title(f'G{gid:03d} 二元激活')
        ax.set_xticks(np.arange(-.5,len(display),1),minor=True);ax.set_yticks(np.arange(-.5,len(cc),1),minor=True)
        ax.grid(which='minor',color='#DDE2E7',linewidth=.45);ax.tick_params(which='minor',bottom=False,left=False)
        save(fig,f'figure1_G{gid:03d}_activation',[{'position_id':c['position_id'],'categories':'|'.join(c['categories']),'K_full':c['K_full'],'K_display':c['K_display'],**{str(f):int(v) for f,v in zip(display,A[i])}} for i,c in enumerate(cc)])
        # Input-token composition; top8 plus the complete complement.
        tr=[r for r in rows(O/'token_composition.csv') if int(r['group_id'])==gid][:8]
        pdata=[{'token_id':r['token_id'],'token':repr(r['token']),
                'group_fraction':float(r['group_token_fraction']),'V_full_fraction':float(r['V_full_token_fraction'])} for r in tr]
        pdata.append({'token_id':'OTHER','token':'其他','group_fraction':1-sum(x['group_fraction'] for x in pdata),
                      'V_full_fraction':1-sum(x['V_full_fraction'] for x in pdata)})
        fig,ax=plt.subplots(figsize=(10,6));xx=np.arange(len(pdata));w=.37
        ax.bar(xx-w/2,[r['group_fraction'] for r in pdata],w,color=GROUP[gid],label='组命中面板')
        ax.bar(xx+w/2,[r['V_full_fraction'] for r in pdata],w,color='#B5BDC7',label='完整V窗口')
        ax.set_xticks(xx,[r['token'] for r in pdata],rotation=45,ha='right');ax.set_xlabel('当前token');ax.set_ylabel('位置比例');ax.set_title(f'G{gid:03d} token构成');ax.legend(frameon=False)
        save(fig,f'figure2_G{gid:03d}_tokens',pdata)
        pr=[r for r in rows(O/'position_composition.csv') if int(r['group_id'])==gid]
        fig,ax=plt.subplots(figsize=(8,5.5));xx=np.arange(4)
        ax.bar(xx-.18,[float(r['group_fraction']) for r in pr],.36,color=GROUP[gid],label='组命中面板')
        ax.bar(xx+.18,[float(r['V_full_fraction']) for r in pr],.36,color='#B5BDC7',label='完整V窗口')
        ax.set_xticks(xx,['0–255','256–511','512–767','768–1023']);ax.set_xlabel('序列内位置');ax.set_ylabel('位置比例');ax.set_title(f'G{gid:03d} 位置构成');ax.legend(frameon=False)
        save(fig,f'figure2_G{gid:03d}_positions',pr)
        # Conditional relation on exactly the same supported panel positions.
        cr={r['metric']:r for r in conditions if int(r['group_id'])==gid}
        keys=['excess_unconditional','excess_conditional'];vals=[float(cr[k]['value']) for k in keys]
        fig,ax=plt.subplots(figsize=(7.5,6));ax.bar([0,1],vals,color=[UNCOND,COND],width=.58)
        for i,key in enumerate(keys):
            r=cr[key]
            if r['lo_coarse'] and r['hi_coarse']:
                lo,hi=float(r['lo_coarse']),float(r['hi_coarse'])
                ax.vlines(i,lo,hi,color='#222222',lw=1.8);ax.hlines([lo,hi],i-.09,i+.09,color='#222222',lw=1.8)
        ax.axhline(0,color='#444444',lw=.8);ax.set_xticks([0,1],['Q−Q0','Q−Q0_cond'])
        ax.set_ylabel('平均成对净共同激活');ax.set_xlabel('独立背景');ax.set_title(f'G{gid:03d} 条件关系')
        save(fig,f'figure3_G{gid:03d}_conditions',[cr[k] for k in keys])
        # Full-window covariance, original fixed denominator, both signs.
        r=next(r for r in core if int(r['group_id'])==gid and r['side']=='V');den=float(r['fixed_denominator'])
        fig,ax=plt.subplots(figsize=(7.5,6));data=[]
        for i,part in enumerate(['core','rest']):
            positive=float(r[part+'_positive'])/den;negative=float(r[part+'_negative'])/den
            color=CORE if part=='core' else OTHER
            ax.bar(i,positive,color=color,width=.58);ax.bar(i,negative,color=color,width=.58,hatch='///',alpha=.75)
            data.append({'part':part,'positive_raw':float(r[part+'_positive']),'negative_raw':float(r[part+'_negative']),
                         'original_fixed_denominator':den,'positive_normalized':positive,'negative_normalized':negative})
        ax.axhline(0,color='#444444',lw=.8);ax.set_xticks([0,1],['核心相关项','其余项'])
        ax.set_xlabel('互斥成员对集合');ax.set_ylabel('平均成对协方差');ax.set_title(f'G{gid:03d} 协方差分解')
        save(fig,f'figure4_G{gid:03d}_core',data)
        for kind,key,title in [('phi','phi_V_panel','二元激活相关'),('cosine','cosine_layer28','解码方向余弦')]:
            full=geo[key];matrix=full[np.ix_(local,local)]
            fig,ax=plt.subplots(figsize=(9,8));cmap=plt.get_cmap('coolwarm').copy();cmap.set_bad('#BDBDBD')
            im=ax.imshow(matrix,vmin=-1,vmax=1,cmap=cmap,interpolation='nearest')
            ax.set_xticks(np.arange(len(display)),display,rotation=90);ax.set_yticks(np.arange(len(display)),display)
            ax.set_xlabel('feature ID');ax.set_ylabel('feature ID');ax.set_title(f'G{gid:03d} {title}')
            fig.colorbar(im,ax=ax,fraction=.046,pad=.03)
            save(fig,f'figure5_G{gid:03d}_{kind}',[{'feature_i':a,'feature_j':b,'value':float(matrix[i,j])} for i,a in enumerate(display) for j,b in enumerate(display)])
    er=rows(O/'contribution_energy.csv')
    fig,ax=plt.subplots(figsize=(9,6));bar=.24;xx=np.arange(3);data=[]
    for j,(term,label,col) in enumerate([('self','自项','#64748B'),('cross_positive','正交叉项','#009E73'),('cross_negative','负交叉项','#CC6677')]):
        yy=[float(next(r[term] for r in er if int(r['group_id'])==g and int(r['layer'])==28)) for g in (68,34,14)]
        ax.bar(xx+(j-1)*bar,yy,bar,label=label,color=col)
    ax.set_xticks(xx,['G068','G034','G014']);ax.axhline(0,color='#444444',lw=.8)
    ax.set_xlabel('关系组');ax.set_ylabel('平均平方贡献');ax.set_title('贡献分解');ax.legend(frameon=False)
    save(fig,'figure5_contribution_energy',[r for r in er if int(r['layer'])==28])
    fig,ax=plt.subplots(figsize=(8,6))
    for g in (68,34,14):
        rr=sorted([r for r in er if int(r['group_id'])==g],key=lambda r:int(r['layer']))
        ax.plot([int(r['layer']) for r in rr],[float(r['cross_over_self']) for r in rr],marker='o',color=GROUP[g],label=f'G{g:03d}')
    ax.axhline(0,color='#444444',lw=.8);ax.set_xlabel('模型层');ax.set_ylabel('交叉项／自项');ax.set_xticks([2,14,28]);ax.set_title('跨层贡献组织');ax.legend(frameon=False)
    save(fig,'figure5_cross_layer',er)
    # Existing genuine-hidden spectra: primary paired differences and size strata.
    prior=S/'daily_research_reports/1016/crosscoder_phi_input_spectrum'
    selected=json.loads((prior/'provenance/plot_selection.json').read_text())['group_ids']
    rr={(r['condition'],int(r['group_id'])):r for r in rows(prior/'data/per_group_input_hidden_metrics.csv')}
    pdata=[]
    for stage,col in [('original','first_share_original'),('residual','first_share_residual')]:
        fig,ax=plt.subplots(figsize=(9,6));rng=np.random.default_rng(20261018)
        for c,delta in [('F',-.15),('N',.15)]:
            for stratum,x in [('small',0),('medium',1),('large',2)]:
                ids=[g for g in selected if rr['R',g]['stratum']==stratum]
                dif=[float(rr['R',g][col])-float(rr[c,g][col]) for g in ids]
                ax.scatter(x+delta+rng.uniform(-.08,.08,len(ids)),dif,s=19,alpha=.55,color=RFN[c],label=f'R−{c}' if x==0 else None)
                ax.scatter(x+delta,np.mean(dif),marker='D',s=60,color=RFN[c],edgecolors='white')
                pdata.extend({'stage':stage,'contrast':f'R-{c}','group_id':g,'size_stratum':stratum,
                              'group_size':rr['R',g]['group_size'],'difference':v} for g,v in zip(ids,dif))
        ax.axhline(0,color='#444444',lw=1);ax.set_xticks([0,1,2],['2–3','4–19','≥20'])
        ax.set_xlabel('组成员数');ax.set_ylabel('第一方向占比差');ax.set_title('原谱配对差异' if stage=='original' else '剩余谱配对差异');ax.legend(frameon=False)
        save(fig,f'appendix_spectrum_paired_{stage}',[r for r in pdata if r['stage']==stage])
    csvout(O/'old_spectrum_individual_paired.csv',pdata)
    curves=rows(prior/'data/phi_input_normalized_spectrum_plot_data.csv')
    for stage in ('original','residual'):
        fig,ax=plt.subplots(figsize=(9,6));data=[r for r in curves if r['stage']==stage and r['displayed']=='True']
        for arm in 'RFN':
            cc=[r for r in data if r['arm']==arm]
            ax.plot([int(r['direction_index']) for r in cc],[float(r['equal_group_mean_variance_share']) for r in cc],color=RFN[arm],lw=2,label=arm)
        ax.set_xlabel('方向序号');ax.set_ylabel('方差占比');ax.set_title('原始hidden谱' if stage=='original' else '原始hidden剩余谱');ax.legend(frameon=False);ax.set_ylim(bottom=0)
        save(fig,f'appendix_spectrum_mean_{stage}',data)
    print('FIGURES_COMPLETE',len(list(FIG.glob('*.png'))),flush=True)

if __name__=='__main__':main()
