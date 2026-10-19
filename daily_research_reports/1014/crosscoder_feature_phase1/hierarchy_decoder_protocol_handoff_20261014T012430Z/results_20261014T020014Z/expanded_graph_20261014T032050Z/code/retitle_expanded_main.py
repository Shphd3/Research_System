"""Redraw one saved graph only; preserve IDs, edges, x/h, colors, sizes."""
import os
os.environ.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
from pathlib import Path
import json,csv,time,resource,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
from collections import Counter
V=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/expanded_graph_20261014T032050Z');R=V.parent
REV=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/expanded_graph_20261014T032050Z/title_revision_20261014T033332Z');t=time.monotonic()
nr=list(csv.DictReader((V/'tables/expanded_nodes.csv').open()));er=list(csv.DictReader((V/'tables/expanded_edges.csv').open()));assert len(nr)==320 and len(er)==1250
selected=[int(r['feature']) for r in nr];edgepairs=[(int(r['A']),int(r['u'])) for r in er]
h=np.zeros(16384,dtype=int);n=np.zeros((2,16384),dtype=int);x={};N_V=5247663;ns=[20,8896,5347,1209,63,2]
for row in nr:
 a=int(row['feature']);h[a]=int(row['h_full_V']);n[1,a]=int(row['n_V']);x[a]=float(row['layout_x'])
groups={j:sorted([f for f in selected if h[f]==j],key=lambda f:x[f]) for j in range(6)}
oldpairs={(int(r['A']),int(r['u'])) for r in er if r['in_old_30_node_branches']=='True'};shown_in=Counter(u for a,u in edgepairs);shown_out=Counter(a for a,u in edgepairs)
font=R/'visual_revision_20261014T025700Z/font/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','pdf.fonttype':42})
colors=['#b76353','#4c8b61','#3f87b4','#9273ad','#c49b39','#b35a92']
source=(V/'code/draw_expanded_graph.py').read_text();exec(source[source.index('def graphfig('):source.index('main=graphfig(')])
fig=graphfig(selected,edgepairs,'')
for text in list(fig.texts):text.remove()
ax=fig.axes[0];ax.set_title('')
fig.suptitle('CrossCoder 特征层级关联图',fontsize=25,y=.972,fontweight='medium')
fig.text(.5,.935,'验证侧 V｜展示 320 个特征、1,250 条关联边｜节点层级沿用完整统计图',ha='center',va='center',fontsize=16)
for text in ax.texts:
 if text.get_text().startswith('h='):text.set_text(text.get_text().replace('本页','展示').replace('全Q','总体'))
fig.subplots_adjust(top=.885,bottom=.045)
assert len(ax.patches)==1250
assert sum(len(c.get_offsets()) for c in ax.collections)==320
assert len(fig.texts)==2
assert all('箭头' not in tx.get_text() and '未显示邻居' not in tx.get_text() for tx in fig.texts)
for ext in ['png','pdf','svg']:fig.savefig(V/'figures'/f'figure1_expanded_connections.{ext}',dpi=210,bbox_inches='tight')
plt.close(fig)
r=json.loads((REV/'record.json').read_text())
for a in r['inputs']:assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
r.update(render_seconds=time.monotonic()-t,max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,status='RENDERED_PENDING_VISUAL_CHECK',checks={'same320_nodes1250_edges':True,'same_source_x_h_colors_and_sizes':True,'no_footer_text':True,'left_count_labels_display_total':True,'node_edge_CSV_hashes_unchanged':True})
(REV/'record.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
