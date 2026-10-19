"""Read existing display CSV; layout changes only."""
import os
os.environ.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
from pathlib import Path
import json,csv,time,resource
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
from collections import Counter
V=Path(__file__).resolve().parents[1]
R=V.parent
source=(V/'code/draw_expanded_graph.py').read_text()
t=time.monotonic()
a=json.loads((V/'receipt.json').read_text());ns=a['checks']['full_Q_counts_exact']
nr=list(csv.DictReader((V/'tables/expanded_nodes.csv').open()));er=list(csv.DictReader((V/'tables/expanded_edges.csv').open()))
selected=[int(r['feature']) for r in nr];edgepairs=[(int(r['A']),int(r['u'])) for r in er]
h=np.zeros(16384,dtype=int);n=np.zeros((2,16384),dtype=int);x={};N_V=5247663
for r in nr:
 f=int(r['feature']);h[f]=int(r['h_full_V']);n[1,f]=int(r['n_V']);x[f]=float(r['layout_x'])
groups={j:sorted([f for f in selected if h[f]==j],key=lambda f:x[f]) for j in range(6)}
oldpairs={(int(r['A']),int(r['u'])) for r in er if r['in_old_30_node_branches']=='True'}
shown_in=Counter(u for f,u in edgepairs);shown_out=Counter(f for f,u in edgepairs)
font=R/'visual_revision_20261014T025700Z/font/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','pdf.fonttype':42})
colors=['#b76353','#4c8b61','#3f87b4','#9273ad','#c49b39','#b35a92'];figuremeta=[]
exec(source[source.index('def save(fig,name'):source.index('# Actual overall counts')])
exec(source[source.index('fig,ax=plt.subplots(figsize=(20,10))'):source.index('# Main expanded graph')])
exec(source[source.index('def graphfig('):source.index('# Multipage readable facets')])
a['layout_only_fix']={'seconds':time.monotonic()-t,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'changes':['Separate dot markers in overview','Increase ordinary edge visibility without changing any edges','Mark15 nodes with no induced edges but non-isolated in full graph'],'source_CSV_unchanged':True}
(V/'receipt.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print(a['layout_only_fix'])
