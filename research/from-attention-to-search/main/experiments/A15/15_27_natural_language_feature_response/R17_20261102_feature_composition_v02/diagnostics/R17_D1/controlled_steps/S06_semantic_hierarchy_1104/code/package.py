from common import *
import zipfile,tempfile,shutil,subprocess,sys
assert json.load(open(R/'evidence/verification.json'))['status']=='PASS'
day=SYS/'daily_research_reports/1104';zip_path=day/'20261104_SAE_hierarchy_analysis.zip';assert not zip_path.exists()
stage=R/'discussion_package';stage.mkdir(exist_ok=False)
# Copy all compact raw evidence and selected preactivations. Exclude full caches, weights, logs and private memory.
for folder in ['data','results','figures','code','versions']:
 (stage/folder).mkdir(exist_ok=True)
 for p in (R/folder).glob('*'):
  if p.is_file():shutil.copy2(p,stage/folder/p.name)
(stage/'evidence').mkdir()
for p in (R/'evidence').glob('*'):
 if p.is_file() and p.suffix in ['.json','.csv','.md'] and p.name!='referenced_threads.json':shutil.copy2(p,stage/'evidence'/p.name)
for p in R.glob('*'):
 if p.is_file() and p.suffix in ['.md','.json']:shutil.copy2(p,stage/p.name)
(stage/'anchors').mkdir()
ar=SYS/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
for pattern in ['15_27_06*anchor*.md','15_27_07*anchor*.md']:
 for p in ar.glob(pattern):shutil.copy2(p,stage/'anchors'/p.name)
shutil.copy2(day/'meeting_report/sae_feature_hierarchy_cn.md',stage/'daily_report_cn.md')
readme='''# 1104 SAE特征组合与语义层级

阅读顺序：[中文认识更新](summary_cn.md) → [F09完整家族与反例](casebook_cn.md) → [详细做法、竞争解释和边界](detailed_cn.md)。[English Summary](summary.md)。

本包包含384条完整文本／标签／模板／划分／token位置、所有四候选逐token分数、两字典所有384×30000的完整稀疏激活、全部统计CSV、选中成员对所有样本的预激活、图、冻结配置／协议、脚本及原始版本。CSR隐式零值是完整激活，不是只挑样本。数据/特征IDs及文件SHA在PACKAGE_MANIFEST.json。

不在包内：模型／SAE权重、所有未选中坐标的完整预激活矩阵和h。其执行侧绝对路径、真实大小和SHA见large_files_index.json，未复制大型缓存。anchors/是已存在科学owner的只读快照；其中外部链接保留原路径，不代表离线拥有原项目。daily_report_cn.md也保留原项目入口；离线以本README和同名本地Summary为准。完整原始源报告仍在研究项目中。

离线复算（Python + numpy/scipy）：

```bash
python code/reproduce_portable.py .
```

原模型重推理需要外部可信权重／loader和已有依赖路径；见reproduce.md。原代码拒绝覆盖已完成响应。H1/H2为有界AI操作判断；科研接受、机制解释和关闭Unknown。H3/H4及真实router训练未运行。未commit/push或外部发布。
'''
(stage/'README.md').write_text(readme)
manifest=[dict(path=str(p.relative_to(stage)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(stage.rglob('*')) if p.is_file()]
dump(stage/'PACKAGE_MANIFEST.json',dict(UTC=now(),files=manifest,all384_prefixes=True,full_sparse_z_both_SAE=True,full_dense_preactivation=False,weights=False))
with zipfile.ZipFile(zip_path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
 for p in sorted(stage.rglob('*')):
  if p.is_file():zz.write(p,str(p.relative_to(stage)))
assert zip_path.stat().st_size<20_000_000
with zipfile.ZipFile(zip_path) as zz:
 assert zz.testzip() is None
 for n in ['README.md','summary_cn.md','detailed_cn.md','protocol.md','data/panel.jsonl','data/ATTN_SAE_all_z_csr.npz','data/MLPIN_SAE_all_z_csr.npz','PACKAGE_MANIFEST.json']:assert n in zz.namelist()
 with tempfile.TemporaryDirectory(prefix='S06_zip_open_') as td:
  zz.extractall(td)
  for r in manifest:assert sha(Path(td)/r['path'])==r['sha256']
  proc=subprocess.run([sys.executable,str(Path(td)/'code/reproduce_portable.py'),td],capture_output=True,text=True);assert proc.returncode==0,proc.stdout+proc.stderr
receipt=dict(UTC=now(),path=str(zip_path),bytes=zip_path.stat().st_size,MB_decimal=zip_path.stat().st_size/1e6,sha256=sha(zip_path),CRC='PASS',extract_and_source_SHA='PASS',files=len(manifest)+1,offline_numeric_replay=proc.stdout,large_cache_index=str(R/'large_files_index.json'),published=False)
dump(R/'evidence/final_delivery.json',receipt);dump(zip_path.with_suffix('.manifest.json'),receipt);shutil.copy2(R/'evidence/final_delivery.json',C/'evidence/final_delivery.json')
manifest_out=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'discussion_package' not in p.parts and p.name!='output_manifest.json']
dump(R/'output_manifest.json',dict(UTC=now(),files=manifest_out,scientific_acceptance='Unknown'))
mp=SYS/'.research/memory/conversations/1104-sae特征组合与语义层级/memory.md'
with mp.open('a') as f:f.write(f'''\n## {now()} -- 完整S06本地交付\n\nProcessed by: Codex (harness: Codex desktop; model: unknown)\n\n- Summary: 384条、两大类各16家族(共享16模板簇)、固定8/8、两nativeSAE的H1/H2、行为、改写/属性/负类、随机/打乱/配对参照、反例、图和独立数值复核完成；旧S02–S05哈希保持。无GPU/云job，无训练/干预/SVD/probe，H3/H4/router未运行。认识和AI判定由Summary拥有，科研接受/机制/关闭Unknown。\n- Current work: 本地报告和小于20MB包完成，ZIP {receipt['bytes']}bytes，CRC、解压逐文件SHA和离线复算通过。Anchor本地阅读副本同步状态见sync记录；未commit/push/外部发布。\n- Known boundary: 字面/属性提示、变长位置、字典重构和小样本仍限制推广；H2不适用点保留。主输出完整稀疏z进包，完整未选中pre/h大缓存外留索引，不能说全pre在包内。\n- Next action: 用户阅读Summary/完整F09/反例并决定是否启动下一有界问题；本轮停止，无自动后续。\n- References: {C}/summary_cn.md；{C}/detailed_cn.md；{R}/evidence/verification.json；{zip_path}；{R}/large_files_index.json。\n''')
# Header timestamp is the sole contract-permitted metadata update; prior entries untouched.
t=mp.read_text().splitlines();t=[('Latest update at: '+receipt['UTC']) if l.startswith('Latest update at:') else l for l in t];mp.write_text('\n'.join(t)+'\n')
print('DELIVERY',json.dumps(receipt),flush=True)
