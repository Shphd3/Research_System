"""Layout only: read already generated cells, do not recompute statistics."""
import os
os.environ.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
from pathlib import Path
import csv,time,json,resource
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
V=Path(__file__).resolve().parents[1]
t=time.monotonic()
font=V/'font/NotoSansCJKsc-Regular.otf'
font_manager.fontManager.addfont(str(font))
plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','pdf.fonttype':42})
with (V/'tables/h0_individual_source.csv').open() as f:rr=list(csv.DictReader(f))
ids=sorted({int(r['feature']) for r in rr});layers=list(range(2,29,2));assert len(ids)==20 and len(rr)==560
fig,axs=plt.subplots(1,2,figsize=(25,11),sharey=True)
for ax,key,label in zip(axs,['train','raw'],['TRAIN 归一化坐标','恢复原始坐标']):
 arr=np.array([[100*float(next(r['p'] for r in rr if r['coordinate']==key and int(r['feature'])==a and int(r['model_layer'])==l)) for l in layers] for a in ids])
 im=ax.imshow(arr,aspect='auto',interpolation='nearest',cmap='viridis',vmin=0,vmax=50)
 ax.set_xticks(range(14),layers);ax.set_yticks(range(20),[f'Feature {a}' for a in ids]);ax.set_xlabel('模型层号（一基）');ax.set_title(f'{label}；h=0；n=20',pad=13)
 for i in range(20):
  for j in range(14):ax.text(j,i,f'{arr[i,j]:.1f}',ha='center',va='center',fontsize=8,color='black' if arr[i,j]>30 else 'white')
axs[0].set_ylabel('Feature（全部 20 个合格非孤立叶节点）')
fig.suptitle('图6｜h=0 的逐个跨层解码幅度占比 p：同级内部差异',y=1.01)
fig.subplots_adjust(wspace=.1,right=.89)
cax=fig.add_axes([.92,.15,.012,.70]);fig.colorbar(im,cax=cax,label='跨层解码幅度占比 p（%；两面板共用色标）')
for ext in ['png','pdf','svg']:fig.savefig(V/'figures'/f'figure6_h0_individual.{ext}',dpi=165,bbox_inches='tight')
plt.close(fig)
p=V/'revision_record.json';rec=json.loads(p.read_text());rec['layout_only_fix']={'figure':'figure6_h0_individual','reason':'place colorbar outside panels without hiding model layer28','seconds':time.monotonic()-t,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'source_cells_unchanged':True};p.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
print(rec['layout_only_fix'])
