from pathlib import Path
import json,csv,hashlib,datetime,shutil,re,time
import numpy as np
V=Path(Path('/tmp/expanded_graph_current_path').read_text());R=V.parent
D=Path('/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z');B=D/V.name
receipt=json.loads((V/'receipt.json').read_text());rule=json.loads((V/'selection_rules_frozen.json').read_text());sel=json.loads((V/'selection_frozen_before_p.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def link(label,p):return f'[{label}]({p})'
def fig(label,name):return f'![{label}]({B}/figures/{name}.png)'
def rr(name):
 with (V/'tables'/name).open() as f:return list(csv.DictReader(f))
t=time.monotonic();nodes=rr('expanded_nodes.csv');edges=rr('expanded_edges.csv');prows=rr('expanded_decoder_p.csv');idset={int(r['feature']) for r in nodes}
assert len(nodes)==320 and len(idset)==320 and {937,3461}.issubset(idset) and len(edges)==1250
oldnodes=set(json.loads((R/'selection_frozen_before_geometry.json').read_text())['nodes']);assert oldnodes.issubset(idset)
full=json.loads(Path(receipt['sources'][0]['path']).read_text());expected={(a,u) for a in idset for u in full['lists'][a] if u in idset};assert expected=={(int(e['A']),int(e['u'])) for e in edges}
for node in nodes:
 a=int(node['feature']);assert int(node['h_full_V'])==full['depth'][a]
 assert int(node['full_in_degree'])==int(node['shown_in_degree'])+int(node['omitted_in_neighbors'])
 assert int(node['full_out_degree'])==int(node['shown_out_degree'])+int(node['omitted_out_neighbors'])
assert len(prows)==8960
geo=np.load(R/'derived_geometry.npz');ps={key:geo[name] for key,name in [('train','p'),('raw','p_raw')]};layers=geo['layers'];porder=[]
for co in ['train','raw']:
 s=[row for row in prows if row['coordinate']==co];assert {int(x['feature']) for x in s}==idset
 for row in s:assert float(row['p'])==float(ps[co][int(np.flatnonzero(layers==int(row['model_layer']))[0]),int(row['feature'])])
 for a in idset:assert np.isclose(sum(float(row['p']) for row in s if int(row['feature'])==a),1)
for src in receipt['sources']:assert sha(src['path'])==src['sha256']
assert hashlib.sha256((D.parent/'results_20261014T020014Z_portable.zip').read_bytes()).hexdigest()=='2411367ff2f533e7e98bc7f64699db4a9dcac01cd898c28049a633033bfaca75'
# Verify SVG/PDF containers and all PNG dimensions; independent client PDF rendering remains unverified.
from PIL import Image
import xml.etree.ElementTree as ET
image_sizes={}
for p in (V/'figures').iterdir():
 if p.suffix=='.png':
  with Image.open(p) as im:im.verify()
  with Image.open(p) as im:image_sizes[p.name]=im.size
 elif p.suffix=='.svg':ET.parse(p)
 elif p.suffix=='.pdf':
  data=p.read_bytes();assert data.startswith(b'%PDF-') and b'%%EOF' in data[-100:]
receipt.update(status='COMPLETE',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),visual_review={'final_overview_and_main_graph':'Actual final PNGs viewed; markers separated, ordinary lines visible, dagger shown','heatmaps':'TRAIN/raw tall plots reviewed via top/bottom PNG crops; grouped TRAIN plot viewed','PDF_SVG':'PDF headers/endings and SVG XML checked; same figure source as PNG. Independent PDF client rendering not available; do not claim client display issue resolved.'},validation={'selected_graph_exact_induced_edge_set':True,'original_h_all320':True,'same320_ids_all8960_decoder_cells_exact':True,'p_each_row_sum1':True,'omitted_counts_match_full_minus_shown':True,'all_source_hashes_unchanged':True,'old_zip_unchanged':True,'image_sizes':image_sizes,'seconds':time.monotonic()-t},reasoning_audit={'skill':'research-reasoning-auditor','bounded_conclusion':'Visualization of existing associations; not a model depth, causal or semantic combination claim; no new trend comparison or learning conclusion.'})
(V/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
readme=f'''# 大范围特征层级关联图：整体概览与320节点连接图

**本次补图展示现有 V 统计图；不改变建图规则，也不产生新的学习结论。** 主图含 320 个 Feature、1,250 条已有约简直接边，其中 261 条跨越多个 h。原 30 个节点和 101 条边全部保留，新增更多分支。

## 先看总体，再看展示子图

| 统计图层级 h | 完整分析集合 Q 的真实节点数 | 本次连接图节点数 |
|---|---:|---:|
| 5 | 2 | 2 |
| 4 | 63 | 63 |
| 3 | 1,209 | 75 |
| 2 | 5,347 | 80 |
| 1 | 8,896 | 80 |
| 0 | 20 | 20 |
| 合计 | 15,537 | 320 |

{fig('完整15537个非孤立合格节点的统计图层级概览','figure1_full_hierarchy_overview')}

每个小方点代表一个真实 Feature，在每个 h 带内按固定 200 列点阵排版；缩小时会呈密度纹理，放大 SVG/PDF 可看点阵。h=5 在上，h=0 在下。点阵没有连线，内部位置只为容纳数量，不表示模型层号或相似度。

Q 是两侧支持 ≥200 且 V 图非孤立的集合。**h=0 的20个节点不代表完整16,384字典中的所有终点。** 完整字典 h=0 为867个，其中847个孤立节点不纳入 Q。原19／22节点分支不是总体分布；本图纠正这一展示范围歧义，而不是人为改变节点数。

{link('概览SVG',B/'figures/figure1_full_hierarchy_overview.svg')} · {link('概览PDF',B/'figures/figure1_full_hierarchy_overview.pdf')}。

## 大型连接图：谁与谁相连

{fig('320个节点与1250条真实直接边','figure1_expanded_connections')}

节点上方为稳定 Feature ID，下方是 **V 激活频率（%）**，统一节点大小，不同颜色仅标统计图层级 h。h 沿用完整 V 图，不在展示子图重算。左右排布只用于减少交叉，不表示相似度。

箭头 **A→更常见的 u**，是保存的 V 约简图中原有的直接统计边，不是已确认的因果或语义组合。选中端点之间的全部 1,250 条边都画出，包括跨 h 边；没有按解码分布、边是否漂亮或是否符合假设过滤。棕色仅帮助认出原两个锚点分支，其他边仍完整保留。这里的“直接”指约简图中的出邻接边，不是将原始图传递边重新加回。

本图是分层展示选择，**不按完整 Q 的数量比例抽样**。图旁同时标出本页节点数与全 Q 数。h=0、h=4、h=5 全部纳入；中间层部分展示，不能用子图密度替代全体结论。

{link('可放大SVG',B/'figures/figure1_expanded_connections.svg')} · {link('可放大PDF',B/'figures/figure1_expanded_connections.pdf')} · {link('高分辨率PNG（6877×3031）',B/'figures/figure1_expanded_connections.png')}。

### 密集连接如何读

{link('17页直接边分面PDF',B/'figures/figure1_expanded_connections_facets.pdf')}每页最多20个起点，按起点的 h 和行内顺序分批；起点及其选中直接邻居保留完整图 h 和主图横坐标。**每条展示边在分面文件中恰好出现一次**，总计仍为1,250，不因分面添加／删除。{link('分面页码与起点清单',B/'facets_index.json')}给每页 ID 范围。

15个节点在所选320节点间没有边，但在完整图中非孤立，主图用 **†** 标记；这来自邻居在展示范围之外，不能判作完整图中无关系。每个节点的完整／展示／遗漏入出度都在CSV中。合计遗漏入邻接条目102,824、出邻接条目1,693，属于逐节点条目数，不是不同外部Feature的数量。

## 与连接图分开的解码占比热图

热图使用**完全相同的320个ID**，按h=5到h=0分组，组内顺序与连接图从左到右一致。横轴才是实际模型层号2、4、…、28；颜色为跨层解码幅度占比 p，单位%，每个Feature的一行合计100%。它不是激活频率，也不把图中的上下位置变成模型深度。

{link('TRAIN归一化坐标：完整320×14热图PDF',B/'figures/figure2_expanded_decoder_train.pdf')} · {link('SVG',B/'figures/figure2_expanded_decoder_train.svg')} · {link('PNG',B/'figures/figure2_expanded_decoder_train.png')}。

{link('恢复原始坐标：完整320×14热图PDF',B/'figures/figure2_expanded_decoder_raw.pdf')} · {link('SVG',B/'figures/figure2_expanded_decoder_raw.svg')} · {link('PNG',B/'figures/figure2_expanded_decoder_raw.png')}。两坐标使用相同0–100%色标。

{fig('同320节点TRAIN归一化坐标解码占比，按h分面方便阅读','figure2_expanded_decoder_facets')}

分面只是完整热图的阅读版本；各面板画布等高不表示样本数相同，标题写明展示数／总体数。{link('分面PDF',B/'figures/figure2_expanded_decoder_facets.pdf')} · {link('分面SVG',B/'figures/figure2_expanded_decoder_facets.svg')}。

## 预先固定的选择规则

规则在读取本次展示用 p 之前保存：{link('完整冻结规则JSON',B/'selection_rules_frozen.json')}；{link('冻结节点与63条分支路径',B/'selection_frozen_before_p.json')}。

1. 保留937、3461原完整出边可达并集30个节点。
2. 纳入全部合格 h=0、h=4、h=5 节点，数量为20、63、2。
3. 按 h=4 根节点 ID 升序，为每个根选一条到 h=0 的最长路径见证：每步只从已有直接出邻居中选择 h 低一级者，优先复用已选邻居；候选按ID排序，以固定种子20261014的PCG64抽取。全部63个h=4分支都有路径，不只重复两个h=5小分支。并未保留这些根的全部后代，所以范围外邻居另行说明。
4. 依次补充 h=3、h=2、h=1 到75、80、80个。每个完整 h 组按 D 激活频率及ID排序，按秩分四组；从当前选中数最少且仍有候选的秩组补取，数量并列时按低组优先，组内固定种子抽取。频率并列用ID打破，秩组不是严格不相交的频率区间。种子、分组和配额不看 p、L、文本或深层假设结果。
5. 保留选中ID之间的全部已有直接边，不重约简。若路径保护节点超配额则保留并报告，不删除路径；本次未超配额。选择冻结时保护节点数 h=0至5为20、20、18、33、63、2，之后按规则补齐320个。

本选择覆盖分支和激活频率范围，目的是看连接。它不是概率代表样本，也不重新计算／替代全体15,537节点的趋势。

## CSV与来源

| 文件 | 行数 | 内容 |
|---|---:|---|
| {link('expanded_nodes.csv',B/'tables/expanded_nodes.csv')} | 320 | ID、原h、D/V支持与激活频率、选择原因、频率秩组、完整／展示／遗漏入出度、排版坐标 |
| {link('expanded_edges.csv',B/'tables/expanded_edges.csv')} | 1,250 | A/u、原h、D/V共同支持、条件概率、背景频率、lift、跨h幅度、原分支标记 |
| {link('expanded_decoder_p.csv',B/'tables/expanded_decoder_p.csv')} | 8,960 | 320×14×2坐标的p，数值保持0—1，图中乘100 |
| {link('overview_counts.csv',B/'tables/overview_counts.csv')} | 6 | 各h总体与展示数量 |
| {link('display_frequency_coverage.csv',B/'tables/display_frequency_coverage.csv')} | 24 | 每h各频率秩组完整／展示人数与D频率范围 |

原关系图：`{receipt['sources'][0]['path']}`。边支持从同run的raw_edges.npz按(A,u)查已有D/V计数；没有新计数。p直接复用`{R}/derived_geometry.npz`。父checkpoint是既有最终14选定层、16,384特征CrossCoder；阈值、归一化、数据划分不变。精确来源路径和hash见 {link('完成回执',B/'receipt.json')}。

CPU作图及来源核对约63.91秒；仅点阵／主图可读性修正另18.27秒；峰值进程RSS约1.13GiB。本次没有GPU任务、推理、训练、激活缓存扫描、关系计数或重新构图。JSON序列化的两次启动错误已修复，未改变选择规则或结果；记录见engineering_note.json。PNG已实际查看；PDF/SVG容器和来源一致性已检查，但未独立验证用户客户端PDF渲染。客户端“不显示”的具体原因尚未确定，不能宣称已修复客户端。

整体统计结论仍以原15,537特征结果为依据；本次只补充可读性与展示范围，不修改科学状态，不commit/push。完成后停止。
'''
(V/'README_cn.md').write_text(readme)
# Copy dedicated visualization package without overwriting prior figures or results.
B.mkdir(exist_ok=False)
for p in V.rglob('*'):
 if p.is_file():
  dest=B/p.relative_to(V);dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,dest)
# Add a short navigation entry; original figures stay available.
append=f'''\n## 大范围补图：整体概览、320节点连接与同ID热图\n\n{link('完整阅读入口及冻结选择规则',B/'README_cn.md')}。总体概览用全部15,537个节点；连接图含320个节点与1,250条已有直接边（261条跨h）。h=0至5展示数为20、80、80、75、63、2，主图同时标总体数；这是分层展示子图，不是总体比例。\n\n{link('主图PDF',B/'figures/figure1_expanded_connections.pdf')} · {link('主图SVG',B/'figures/figure1_expanded_connections.svg')} · {link('17页直接边分面',B/'figures/figure1_expanded_connections_facets.pdf')} · {link('同ID解码占比热图',B/'figures/figure2_expanded_decoder_train.pdf')}。原19／22节点图仅代表各自可达分支，保留为局部图，不代表整体层级数量。\n'''
for name in ['README_cn.md','figures_cn.md']:
 p=D/name;before=p.read_text();(V/f'parent_{name}_before.txt').write_text(before);p.write_text(before.rstrip()+'\n'+append)
# Validate all Markdown links in new package and current two navigation entries.
for p in [B/'README_cn.md',D/'README_cn.md',D/'figures_cn.md']:
 for x in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if x.startswith('/'):assert Path(x.split('#')[0]).exists(),(p,x)
# Add this revision to current full delivery manifest, leaving old entries' origins intact.
mp=D/'payload_manifest.json';manifest=json.loads(mp.read_text());(V/'parent_payload_manifest_before.json').write_text(mp.read_text());prev={e['relative_path']:e for e in manifest['files']};files=[]
for p in sorted(D.rglob('*')):
 if not p.is_file() or p==mp:continue
 rel=str(p.relative_to(D));digest=sha(p)
 if rel in prev and prev[rel]['sha256']==digest:entry=prev[rel]
 elif p.is_relative_to(B):entry={'relative_path':rel,'bytes':p.stat().st_size,'sha256':digest,'origin':str(V/p.relative_to(B)),'scope':'saved-V-graph visualization; frozen320-node selection; no graph/threshold change'}
 elif p in [D/'README_cn.md',D/'figures_cn.md']:
  origin=V/f'parent_{p.name}_after.md';origin.write_text(p.read_text());entry={'relative_path':rel,'bytes':p.stat().st_size,'sha256':digest,'origin':str(origin),'scope':'navigation only: link expanded graph package'}
 else:raise AssertionError(('unexpected change',rel))
 files.append(entry)
manifest['files']=files;manifest['supplementary_expanded_graph']=str(B);manifest['complete']=True;mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
assert all(sha(D/x['relative_path'])==x['sha256'] for x in files)
print(json.dumps({'delivery':str(B),'nodes':320,'edges':1250,'skip_edges':261,'files':len(list(B.rglob('*'))),'package_bytes':sum(p.stat().st_size for p in B.rglob('*') if p.is_file()),'validation_seconds':receipt['validation']['seconds'],'total_delivery_manifest_files':len(files)},ensure_ascii=False,indent=2))
