from common import *
import pickle,textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter
from validate import exact_bounds
from analyze import score
font=ROOT/'R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':12,'axes.titlesize':15,'axes.labelsize':12,'axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
A=OUT/'analysis';F=OUT/'figures';COL={'head':'#247b9b','middle':'#da913d','tail':'#9a629d','full':'#333e48','random1031':'#9b9b9b'};TN={'coarse':'数学／生物','math_fine':'数学内：代数／分析','bio_fine':'生物内：细胞／生态进化'};CL={'coarse':['数学','生物'],'math_fine':['代数','分析'],'bio_fine':['细胞','生态进化']}
def readcsv(name):return list(csv.DictReader((A/(name+'.csv')).open()))
def save(fig,name):
 fig.savefig(F/(name+'.png'),dpi=170,bbox_inches='tight',facecolor='white');fig.savefig(F/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
metrics=readcsv('readout_metrics');bounds=readcsv('finite_sample_bounds');contr=readcsv('contrasts');recon=readcsv('reconstruction');extra=readcsv('feature_and_residual_readouts');cover={r['task']:r for r in readcsv('coverage')};B=np.load(A/'bases.npz');ev=B['eigenvalues'];tasks=list(TN)
fig,ax=plt.subplots(1,2,figsize=(13.8,4.8));x=np.arange(1,1025)
ax[0].plot(x,ev,color='#31495b',lw=1.7)
for lo,hi,name in [(1,64,'head'),(481,544,'middle'),(961,1024,'tail')]:ax[0].axvspan(lo,hi,color=COL[name],alpha=.24,label={'head':'头部 1–64','middle':'中部 481–544','tail':'尾部 961–1024'}[name])
ax[0].set_yscale('log');ax[0].set_xlabel('主成分序号（奇异值递减）');ax[0].set_ylabel('协方差特征值（表征平方单位）');ax[0].legend(frameon=False);ax[0].set_title('固定旧谱：9600个真实表征向量')
ax[1].plot(x,np.cumsum(ev)/ev.sum(),color='#31495b');ax[1].yaxis.set_major_formatter(PercentFormatter(1));ax[1].set_ylim(0,1.03);ax[1].set_xlabel('前k个主成分');ax[1].set_ylabel('累计方差份额');ax[1].set_title('方差排序不定义语义粒度')
for name,ix in [('head',slice(0,64)),('middle',slice(480,544)),('tail',slice(960,1024))]:ax[1].text(.53,.33-.09*list(['head','middle','tail']).index(name),f'{dict(head="头",middle="中",tail="尾")[name]}64维：{ev[ix].sum()/ev.sum():.2%} 方差',transform=ax[1].transAxes,color=COL[name])
fig.suptitle('图1｜同一自然文本谱，固定三个等维分析区间',fontsize=18);fig.tight_layout();save(fig,'figure1_spectrum')
fig,axs=plt.subplots(1,3,figsize=(15.8,5.2),sharey=True);names=['head','middle','tail','random1031','full'];labs=['头64','中64','尾64','随机64','全1024']
for ax,t in zip(axs,tasks):
 for i,n in enumerate(names):
  r=next(r for r in metrics if r['task']==t and r['condition']=='standardized__'+n);b=next(r for r in bounds if r['task']==t and r['condition']=='standardized__'+n);y=float(r['balanced_accuracy']);lo=float(b['exact_ci_low']);hi=float(b['exact_ci_high']);ax.errorbar(i,y,yerr=[[y-lo],[hi-y]],fmt='o',capsize=4,color=COL[n],ms=8);ax.text(i,y+.035,f'{y:.1%}',ha='center',fontsize=11)
 ax.axhline(.5,color='#777',ls='--',lw=1);ax.set_xticks(range(5),labs,rotation=20);ax.set_ylim(.1,1.08);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_title(f'{TN[t]}\n留出{cover[t]["H_documents"]}篇，每篇一个the');ax.grid(axis='y',alpha=.15)
axs[0].set_ylabel('类别均衡正确率');fig.suptitle('图2｜谱头也能区分细类；谱段表现依任务而异',fontsize=19);fig.text(.5,-.015,'误差线：按文档、分类别的保守95%二项界；随机种子1031，其他种子见附录。旧留出已暴露，均为探索性结果。',ha='center',fontsize=11);fig.tight_layout();save(fig,'figure2_band_readability')
fig,axs=plt.subplots(1,3,figsize=(15.8,4.9),sharey=True);ns=['head_next','head_middle','head_tail','head_random'];ls=['头延长64','头＋中64','头＋尾64','头＋随机64']
for ax,t in zip(axs,tasks):
 for i,n in enumerate(ns):
  r=next(r for r in contr if r['task']==t and r['comparison']==n+'__minus__head');v=float(r['difference'])*100;lo=float(r['ci_low'])*100;hi=float(r['ci_high'])*100;ax.errorbar(i,v,yerr=[[max(0,v-lo)],[max(0,hi-v)]],fmt='o',color=['#496a8a',COL['middle'],COL['tail'],'#888'][i],capsize=4,ms=8);ax.text(i,v+2,f'{v:+.1f}',ha='center')
 ax.axhline(0,color='#666',ls='--');ax.set_xticks(range(4),ls,rotation=25,ha='right');ax.set_title(TN[t]);ax.grid(axis='y',alpha=.15)
axs[0].set_ylabel('相对头64维的正确率变化（百分点）');fig.suptitle('图3｜新增维数相同：中尾未显示稳定的专属增量',fontsize=19);fig.text(.5,-.035,'所有新增模型均128维；误差线为配对文档bootstrap。零宽经验区间不意味着总体等价。',ha='center',fontsize=11);fig.tight_layout();save(fig,'figure3_increment')
fig,axs=plt.subplots(2,3,figsize=(15.8,8.8));
with open(A/'evaluation_state.pkl','rb') as f:states=pickle.load(f)
with open(OUT/'models/frozen.pkl','rb') as f:models=pickle.load(f)
for j,t in enumerate(tasks):
 r=next(r for r in recon if r['task']==t and r['space']=='full');d=states[t];y=d['y'];S=(d['h']-B['mean'])@B['V'];D0=np.load(ROOT/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz');rh=d['z']@D0['decoder_model_scale']+D0['decoder_bias_model'];Sr=(rh-B['mean'])@B['V'];Se=(d['h']-rh)@B['V'];vals=[('真实h',d['scores']['standardized__full']),('重构：固定读出',score(models[t]['models']['standardized__full'],Sr)),('残差：另拟合',score(models[t]['residual_model'],Se))]
 ax=axs[0,j]
 for k,(lab,s) in enumerate(vals):
  v=.5*sum(np.mean((s[y==c]>=0)==bool(c)) for c in [0,1]);b=exact_bounds(y,s);ax.errorbar(k,v,yerr=[[v-b['exact_ci_low']],[b['exact_ci_high']-v]],fmt='o',capsize=4,ms=8,color=['#333e48','#318882','#b86c3b'][k]);ax.text(k,v+.035,f'{v:.1%}',ha='center')
 ax.set_xticks(range(3),[a for a,_ in vals],rotation=15);ax.set_ylim(.15,1.1);ax.axhline(.5,color='#999',ls='--');ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_title(TN[t]);ax.grid(axis='y',alpha=.12)
 ax=axs[1,j];f=float(r['reconstructed_fraction_of_score_difference']);ax.barh(0,f,color='#318882',label='重构');ax.barh(0,1-f,left=f,color='#b86c3b',label='残差');ax.text(f/2,0,f'{f:.1%}',ha='center',va='center',color='white',fontsize=14);ax.text(f+(1-f)/2,0,f'{1-f:.1%}',ha='center',va='center',color='white',fontsize=12);ax.set_xlim(0,1);ax.set_ylim(-.7,.7);ax.set_yticks([]);ax.xaxis.set_major_formatter(PercentFormatter(1));ax.set_xlabel('原固定读出：两类平均分数差的有符号账目');ax.set_title(f'总体重构NMSE={float(r["mean_normalized_squared_error"]):.1%}',fontsize=13)
axs[0,0].set_ylabel('类别均衡正确率');axs[1,0].legend(frameon=False,loc='upper left',bbox_to_anchor=(0,-.45),ncol=2);fig.suptitle('图4｜重构保留多数判别分数，残差仍携带可读区别',fontsize=19);fig.text(.5,.015,'下排不是信息解释率；上排残差重新拟合，与固定原读出的重构保留测试分开。',ha='center',fontsize=11);fig.tight_layout(rect=(0,.04,1,.96));save(fig,'figure4_reconstruction_residual')
feat=readcsv('features_top12');examples=json.load(open(A/'text_examples.json'));fig,axs=plt.subplots(3,2,figsize=(15.8,11.8),gridspec_kw={'width_ratios':[1,1.25]})
for row,t in enumerate(tasks):
 d=states[t];z=d['z'];y=d['y'];ids=models[t]['features'][:2];ax=axs[row,0]
 for k,f in enumerate(ids):
  for c in [0,1]:
   vals=z[y==c,f];rng=np.random.default_rng(100+k+c);ax.scatter(k+(c-.5)*.25+rng.uniform(-.06,.06,len(vals)),vals,s=27,color=['#287aa0','#cc7c34'][c],alpha=.7,label=CL[t][c] if k==0 else None)
  rr=next(q for q in feat if q['task']==t and q['feature_id']==str(f));ax.text(k,.97,f'激活文档 {rr["H_support0"]}/{cover[t]["H_class0"]} : {rr["H_support1"]}/{cover[t]["H_class1"]}',transform=ax.get_xaxis_transform(),ha='center',fontsize=10)
 ax.set_yscale('symlog',linthresh=.001);ax.set_ylabel('原生共享响应z（含零）');ax.set_xticks(range(2),[f'f{f}\nDCLM率 {float(next(q for q in feat if q["task"]==t and q["feature_id"]==str(f))["reference_rate"]):.3%}' for f in ids]);ax.set_title(TN[t]);ax.legend(frameon=False,fontsize=11,loc='upper right');ax.grid(axis='y',alpha=.12)
 ax=axs[row,1];ax.axis('off');f=ids[0];cases=[next(q for q in examples if q['task']==t and q['kind']==f'feature_{f}_{k}') for k in ['high','low']]
 ax.text(0,1,f'同一个the：冻结首位成员 f{f} 的真实高／低响应',transform=ax.transAxes,fontsize=14,va='top')
 for y0,c,name in zip([.82,.39],cases,['高','低']):
  text=c['prefix'][-230:];text='… '+text.split(' ',1)[-1] if len(c['prefix'])>230 else text
  title=f'{name}响应 z={c["z"]:.4f}｜{c["seq_id"]}｜{c["topic"]}'
  ax.text(0,y0,title,transform=ax.transAxes,va='top',fontsize=11,color='#375d75');ax.text(0,y0-.09,'\n'.join(textwrap.wrap(text.replace('\n',' '),width=73)),transform=ax.transAxes,va='top',fontsize=10.5,linespacing=1.3)
fig.suptitle('图5｜出现有无与强弱共同变化；高响应例子之外保留零响应反例',fontsize=19);fig.text(.5,.01,'全部位置目标token相同；只展示已读前文。DCLM率是独立参考出现率，不是当前响应幅值。完整实例与成员表见Detailed。',ha='center',fontsize=11);fig.tight_layout(rect=(0,.04,1,.96));save(fig,'figure5_features_text')
# Compact sensitivity appendix: all predefined conditions are retained.
rob=readcsv('training_subset_sensitivity');fig,axs=plt.subplots(1,3,figsize=(15,4.8),sharey=True)
for ax,t in zip(axs,tasks):
 for k,n in enumerate(['head','middle','tail']):
  vv=[float(r['balanced_accuracy']) for r in rob if r['task']==t and r['band']==n];ax.scatter(np.full(len(vv),k)+np.linspace(-.12,.12,len(vv)),vv,color=COL[n],s=30,alpha=.6);ax.plot([k-.2,k+.2],[np.median(vv)]*2,color=COL[n],lw=2)
  v=float(next(r for r in metrics if r['task']==t and r['condition']=='raw__'+n)['balanced_accuracy']);ax.scatter(k,v,marker='D',facecolors='white',edgecolors='black',s=65,zorder=4)
 ax.set_xticks(range(3),['头64','中64','尾64']);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_ylim(.3,1.06);ax.axhline(.5,color='#999',ls='--');ax.set_title(TN[t]);ax.grid(axis='y',alpha=.15)
axs[0].set_ylabel('类别均衡正确率');fig.suptitle('附图｜10个固定训练子集种子（点）及不标准化结果（空心菱形）',fontsize=17);fig.tight_layout();save(fig,'appendix_scale_training_subsets')
dump(F/'figure_manifest.json',{'source_tables':[str(A/(x+'.csv')) for x in ['readout_metrics','finite_sample_bounds','contrasts','reconstruction','features_top12','training_subset_sensitivity']],'font_external_path':str(font),'figures':{p.name:sha(p) for p in sorted(F.glob('*')) if p.suffix in ['.png','.pdf']},'font_not_copied_to_repository':True})
print('RENDERED',len(list(F.glob('*.png'))),'PNG/PDF pairs',flush=True)
