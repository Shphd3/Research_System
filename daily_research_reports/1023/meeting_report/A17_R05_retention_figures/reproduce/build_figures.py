"""Presentation-only extraction and static figures from existing A evidence.
No torch import, model loading, new forward, training, or checkpoint selection.
"""
from pathlib import Path
import csv,json,hashlib,shutil,math
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter
from matplotlib.patches import Rectangle
F=Path(__file__).resolve().parent;E=F.parents[1];S=Path('/data/250010109/Research_System')
C=S/'Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023'
D=S/'daily_research_reports/1023/meeting_report/A17_R05_retention_figures'
for d in [D/'figures',D/'tables',D/'plot_data']:d.mkdir(parents=True,exist_ok=True)
fm.fontManager.addfont(str(F/'fonts/NotoSansCJKsc-Regular.otf'));FONT=fm.FontProperties(fname=F/'fonts/NotoSansCJKsc-Regular.otf').get_name()
plt.rcParams.update({'font.family':FONT,'font.size':11.5,'axes.titlesize':13,'axes.labelsize':12,'xtick.labelsize':11,'ytick.labelsize':11,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white','figure.facecolor':'white'})
BLUE='#0072B2';GRAY='#737373';ORANGE='#D55E00';BLACK='#171717'
def readcsv(p):return list(csv.DictReader(open(p)))
def writecsv(p,r):
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(r[0]));w.writeheader();w.writerows(r)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def savefig(fig,folder,name):
 for ext in ['svg','pdf','png']:
  p=folder/f'{name}.{ext}';fig.savefig(p,dpi=320,bbox_inches='tight',pad_inches=.13)
  if ext=='svg':p.write_text(p.read_text().replace("'Noto Sans CJK SC'","'Noto Sans CJK SC', 'Microsoft YaHei', 'PingFang SC', sans-serif"))
 plt.close(fig)
def main():
 src={'endpoints':C/'a_stage_audit_tables/endpoint_21.csv','C_coordinates':C/'A_localization_20261023/tables/C_coordinate_stability_48.csv','candidate_probe':C/'A_localization_20261023/tables/probe_pooled_2.csv','interventions':C/'A_residual_spectral_20261023/tables/intervention_behavior_66.csv','spectral_screen':C/'A_residual_spectral_20261023/tables/saved_point_screen_54.csv','intervention_geometry':C/'A_residual_spectral_20261023/tables/intervention_geometry_264.csv','actual_rank_norm':C/'A_residual_spectral_20261023/tables/actual_norm_rank_matches_120.csv','fixed_old_input_outputs':C/'A_residual_spectral_20261023/tables/fixed_inputs_432.csv'}
 endpoints=readcsv(src['endpoints']);coords=readcsv(src['C_coordinates']);inter=readcsv(src['interventions']);screen=readcsv(src['spectral_screen']);probe=readcsv(src['candidate_probe']);rank=readcsv(src['actual_rank_norm']);geometry=readcsv(src['intervention_geometry'])
 assert len(endpoints)==21 and all(int(r['step'])==1200 and r['primary_endpoint']=='True' and r['n_old']==r['n_new']=='800' for r in endpoints)
 names={'U':'统一更新','UL':'整体固定减速','US':'整体调度减速','TC':'前16固定衰减','TS':'前16调度衰减','RS':'随机方向调度衰减','LS':'小奇异方向调度衰减'}
 index={(int(r['seed']),r['arm']):r for r in endpoints};table1=[];fig1=[]
 for seed in [29,43,71]:
  u=index[seed,'U']
  for arm in ['U','UL','US','TC','TS','RS','LS']:
   r=index[seed,arm];ok=float(r['new_min_cell_pct'])>=95;assert ok==(r['new_qualified']=='True')
   table1.append({'training_order':seed,'method':arm,'method_name_cn':names[arm],'old_accuracy_pct':float(r['old_accuracy_pct']),'new_accuracy_pct':float(r['new_accuracy_pct']),'new_learning_qualified':ok,'old_minus_U_pp':float(r['old_accuracy_pct'])-float(u['old_accuracy_pct']),'new_min_cell_pct':float(r['new_min_cell_pct']),'n_old':800,'n_new':800,'update':1200})
  for arm in ['U','TS']:
   q=next(r for r in coords if int(r['seed'])==seed and r['arm']==arm and int(r['step'])==1200);r=index[seed,arm]
   assert math.isclose(float(q['C_net_over_C0']),float(q['C_net_displacement'])/float(q['C0_joint_norm']),rel_tol=1e-12)
   fig1.append({'training_order':seed,'method':arm,'C_endpoint_net_norm':float(q['C_net_displacement']),'C0_joint_frobenius_norm':float(q['C0_joint_norm']),'C_net_over_C0_pct':100*float(q['C_net_over_C0']),'old_accuracy_pct':float(r['old_accuracy_pct']),'new_accuracy_pct':float(r['new_accuracy_pct']),'n_old':800,'n_new':800,'update':1200})
 writecsv(D/'tables/table1_main_experiment_21.csv',table1);writecsv(D/'plot_data/figure1_6.csv',fig1)
 fig,ax=plt.subplots(1,4,figsize=(13.8,3.9),gridspec_kw={'width_ratios':[1.25,1,1,1]});x=np.arange(3);width=.29
 for arm,color,marker,offset in [('U',GRAY,'o',-.16),('TS',BLUE,'s',.16)]:
  rr=[r for r in fig1 if r['method']==arm];yy=[r['C_net_over_C0_pct'] for r in rr]
  bars=ax[0].bar(x+offset,yy,width,color='white' if arm=='U' else color,edgecolor=color,hatch='' if arm=='U' else '///',linewidth=1.4)
  for xx,y in zip(x+offset,yy):ax[0].text(xx,y+.008,f'{y:.4f}',ha='center',va='bottom',fontsize=9.5,color=BLACK)
  for j,key in [(1,'old_accuracy_pct'),(2,'old_accuracy_pct'),(3,'new_accuracy_pct')]:ax[j].scatter(x+offset,[r[key] for r in rr],s=60,c=color,marker=marker,edgecolor='white',linewidth=.5,zorder=4)
 ax[0].set_ylabel('C终点净位移 / 初始C长度（%）');ax[0].set_title('C净位移');ax[0].set_ylim(0,.57);ax[0].set_yticks([0,.1,.2,.3,.4,.5])
 for j,title in [(1,'旧任务：全范围'),(2,'旧任务：局部放大'),(3,'新任务：全范围')]:
  ax[j].set_title(title);ax[j].set_ylabel('准确率（%）')
  if j==2:ax[j].set_ylim(-.035,1.04);ax[j].set_yticks([0,.25,.5,.75,1])
  else:ax[j].set_ylim(-3,103);ax[j].set_yticks([0,25,50,75,100])
 for a in ax:a.set_xticks(x,['29','43','71']);a.set_xlabel('训练顺序');a.grid(axis='y',alpha=.18,zorder=0);a.set_axisbelow(True)
 handles=[Line2D([],[],marker='o',color=GRAY,ls='',label='U'),Line2D([],[],marker='s',color=BLUE,ls='',label='TS')]
 fig.legend(handles=handles,loc='upper center',ncol=2,frameon=False,bbox_to_anchor=(.51,1.04));fig.subplots_adjust(wspace=.48,top=.82,bottom=.21,left=.07,right=.99)
 savefig(fig,D/'figures','figure1_protection_and_retention')
 # TS, all three orders: only contrasts needed by the revised conclusion.
 fig2=[r for r in inter if r['arm']=='TS' and (r['kind']!='dose' or float(r['beta'])==1)];assert len(fig2)==21
 writecsv(D/'plot_data/figure2_TS_21.csv',fig2)
 fig,axs=plt.subplots(1,3,figsize=(14,5.5),sharex=True,sharey=True)
 for a,seed in zip(axs,[29,43,71]):
  rr=[r for r in fig2 if int(r['seed'])==seed];tar=next(r for r in rr if r['kind']=='target');rnd=[r for r in rr if r['kind']=='random'];base=next(r for r in rr if r['kind']=='dose')
  tx,ty=float(tar['mode2_accuracy_pct']),float(tar['mode1_accuracy_pct']);a.scatter(tx,ty,marker='D',color=ORANGE,s=85,zorder=5)
  a.annotate('靶向削弱',(tx,ty),xytext=(-25,16),textcoords='offset points',fontsize=11,color=ORANGE)
  bx,by=float(base['mode2_accuracy_pct']),float(base['mode1_accuracy_pct']);a.scatter(bx,by,marker='s',s=70,facecolors='none',edgecolors=BLACK,lw=1.2,zorder=6)
  a.annotate('原终点',(bx,by),xytext=(75,12),textcoords='data',fontsize=10,color=BLACK,arrowprops={'arrowstyle':'-','color':BLACK,'lw':.7})
  for r in rnd:a.scatter(float(r['mode2_accuracy_pct']),float(r['mode1_accuracy_pct']),marker='x',s=33,color=GRAY,lw=1.1,zorder=4)
  a.set_title(f'顺序 {seed}');a.set_xlim(-3,103);a.set_ylim(-3,103);a.set_aspect('equal');a.set_xticks([0,25,50,75,100]);a.set_yticks([0,25,50,75,100]);a.grid(alpha=.13);a.set_xlabel('新任务准确率（%）');a.set_ylabel('旧任务准确率（%）' if seed==29 else '')
  ins=a.inset_axes([.12,.11,.45,.29]);ins.set_facecolor('white');groups=defaultdict(list)
  for r in rnd:groups[float(r['mode2_accuracy_pct']),float(r['mode1_accuracy_pct'])].append(int(r['label'])-2700)
  slots=([(.48,.08),(.44,.90),(.68,.54)] if seed==71 else [(.08,.74),(.50,.90),(.52,.14),(.06,.17),(.08,.48)])
  for z,((xx,yy),ids) in enumerate(sorted(groups.items(),key=lambda kv:(kv[0][1],kv[0][0]))):
   ins.scatter(xx,yy,marker='x',s=29,color=GRAY,lw=1.1,zorder=5)
   label='R1–R5' if ids==[1,2,3,4,5] else 'R'+','.join(map(str,ids))
   ins.annotate(label,(xx,yy),xytext=slots[z],textcoords='axes fraction',fontsize=8.4,color=GRAY,arrowprops={'arrowstyle':'-','color':GRAY,'lw':.55})
  ins.scatter(bx,by,marker='s',s=35,facecolors='none',edgecolors=BLACK,lw=1,zorder=6)
  ins.set_xlim(98.35,100.2);ins.set_ylim(-.10,.85);ins.set_xticks([98.5,100]);ins.set_yticks([0,.5]);ins.tick_params(labelsize=8,length=2);ins.set_title('随机对照（局部）',fontsize=9,pad=3);ins.set_xlabel('新准确率（%）',fontsize=8,labelpad=1);ins.set_ylabel('旧准确率（%）',fontsize=8,labelpad=1);ins.grid(alpha=.13)
 fig.subplots_adjust(wspace=.18,left=.055,right=.99,bottom=.14,top=.90);savefig(fig,D/'figures','figure2_residual_tradeoff')
 # Backup: independent y axes on separate aligned panels; same scale within each row.
 backup=[r for r in screen if r['arm']=='TS'];assert len(backup)==27;writecsv(D/'plot_data/figure3_TS_27.csv',backup)
 fig,ax=plt.subplots(3,3,figsize=(12.8,8),sharex=True,sharey='row')
 metrics=[('mode1_accuracy_pct',1,'旧任务准确率（%）',[-3,103],[0,50,100]),('max_matrix_sigma1_relative_change',100,'最大谱范数\n相对变化（%）',[-.08,3],[0,1,2,3]),('max_top16_mean_cos2_loss',100,'最大前16子空间\n重合下降（%）',[-.2,11],[0,5,10])]
 for col,seed in enumerate([29,43,71]):
  rr=[r for r in backup if int(r['seed'])==seed];t=[int(r['step']) for r in rr]
  for row,(key,mul,label,yl,yt) in enumerate(metrics):
   a=ax[row,col];a.plot(t,[float(r[key])*mul for r in rr],color=BLUE,lw=1.6,marker='o',ms=3.5);a.axvline(16,color=ORANGE,ls='--',lw=1);a.set_xscale('symlog',linthresh=2);a.set_ylim(*yl);a.set_yticks(yt);a.grid(alpha=.14);a.set_xticks([0,2,16,120,1200],['0','2','16','120','1200'])
   if col==0:a.set_ylabel(label)
   if row==0:a.set_title(f'顺序 {seed}')
   if row==2:a.set_xlabel('已保存的训练步数')
  for a in ax[:,col]:
   for tick in a.get_xticklabels():
    if tick.get_text()=='16':tick.set_color(ORANGE);tick.set_fontweight('bold')
 fig.subplots_adjust(hspace=.17,wspace=.16,left=.11,right=.99,top=.94,bottom=.09);savefig(fig,D/'figures','figure3_backup_spectral_timing')
 # Two presentation tables; random ranges retain all5draws without adding another table.
 table2=[]
 for seed in [29,43,71]:
  rr=[r for r in fig2 if int(r['seed'])==seed];base=next(r for r in rr if r['kind']=='dose' and float(r['beta'])==1)
  for kind,source in [('endpoint',[base]),('target',[next(r for r in rr if r['kind']=='target')]),('random',[r for r in rr if r['kind']=='random'])]:
   a=np.array([float(r['mode1_accuracy_pct']) for r in source]);b=np.array([float(r['mode2_accuracy_pct']) for r in source]);ba=float(base['mode1_accuracy_pct']);bb=float(base['mode2_accuracy_pct'])
   table2.append({'training_order':seed,'condition':kind,'n_conditions':len(source),'old_accuracy_mean_pct':float(a.mean()),'old_accuracy_min_pct':float(a.min()),'old_accuracy_max_pct':float(a.max()),'new_accuracy_mean_pct':float(b.mean()),'new_accuracy_min_pct':float(b.min()),'new_accuracy_max_pct':float(b.max()),'old_change_mean_pp':float(a.mean()-ba),'old_change_min_pp':float(a.min()-ba),'old_change_max_pp':float(a.max()-ba),'new_change_mean_pp':float(b.mean()-bb),'new_change_min_pp':float(b.min()-bb),'new_change_max_pp':float(b.max()-bb),'n_old_per_condition':800,'n_new_per_condition':800})
 writecsv(D/'tables/table2_residual_interventions_9.csv',table2)
 selection={'primary_endpoint':1200,'figure1':'all3orders,U/TS;Cnet/C0andold/newaccuracy;fulloldscalepluszoom','figure2_and_table2':'revised user conclusions: TS, all3orders; original endpoint,target,andall5randoms;dose series remains in canonical results, not main presentation','backup':'TSall3orders,all9savedpoints;maxsigma1andmaxsubspacelossnot sumofsingularvalues','table1':'all7methods x3orders;failedgatesretained','candidate_probe':'read for boundary only: localprobabilitysensitivity doesnotidentifycross-taskreuse; notneeded asathirdmainfigure','random_aggregation':'table2meanandminmaxof5fixeddraws;figure2groupsexactcoordinateoverlapsandlabelsallRindices;noartificialpointjitter','uncertainty':'nopopulationerrorbars;threeordersshareoneacquiredparent;minmaxarenotconfidenceintervals','original_results_changed':False,'new_training_or_forward':False}
 provenance={'source_files':[{ 'role':k,'path':str(p),'sha256':sha(p)} for k,p in src.items()],'selection':selection,'font':json.load(open(F/'fonts/provenance.json')),'reproduce_source_sha256':sha(Path(__file__))}
 (F/'figure_plan_and_sources.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n');shutil.copy2(F/'figure_plan_and_sources.json',D/'figure_plan_and_sources.json')
 print(json.dumps({'directory':str(D),'main_figures':2,'backup_figures':1,'tables':2,'formats':['plots:SVG editable text,PDF embedded font,PNG320dpi','tables:Markdown text andCSV only'],'table1_rows':len(table1),'table2_rows':len(table2),'figure2_points':len(fig2)}))
if __name__=='__main__':main()
