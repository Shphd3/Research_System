from common import *
import shutil,zipfile,subprocess,tempfile,os,re
B=R/'discussion_package';assert not B.exists();B.mkdir();mapping={};origin={}
def copy(src,dest):
 src=Path(src);dest=B/dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);mapping[str(src)]=dest;mapping[str(src.resolve())]=dest;origin[str(dest.relative_to(B))]=dict(source=str(src),source_sha256=sha(src),transform='byte copy')
for f in C.rglob('*.md'):copy(f,Path('records')/f.relative_to(C))
for f in (R/'code').glob('*.py'):copy(f,Path('code')/f.name)
for f in (R/'data').iterdir():
 if f.is_file():copy(f,Path('data')/f.name)
for folder in ['tables','figures']:
 for f in (R/folder).iterdir():
  if f.is_file() and f.suffix in ['.csv','.json','.png']:copy(f,Path(folder)/f.name)
for f in (R/'results').rglob('*'):
 if f.is_file() and f.suffix in ['.json','.jsonl']:copy(f,Path('results')/f.relative_to(R/'results'))
for f in (R/'evidence').iterdir():
 if f.is_file() and f.suffix in ['.json','.jsonl'] and f.name!='package_verification.json':copy(f,Path('evidence')/f.name)
for f in (R/'versions').iterdir():
 if f.is_file() and f.suffix in ['.md','.py','.json']:copy(f,Path('versions')/f.name)
copy(R/'versions/preparation_attempt1/incident.json','versions/preparation_incident.json')
for f in (R/'cache').glob('*.npz'):copy(f,Path('cache')/f.name)
for f in (R/'cache/calibration').glob('*.npz'):copy(f,Path('cache/calibration')/f.name)
for f in [R/'config.json',R/'effective_config.json']:copy(f,f.name)
for f in [FOCUS,FOCUS.with_name(FOCUS.stem+'_cn.md')]:copy(f,Path('records')/f.name)
for name in ['membership_summary.csv','family_geometry.csv']:copy(OLD/'tables'/name,Path('reference/R19/tables')/name)
for f in [OLD_C/'summary.md',OLD_C/'protocol.md',OLD/'config.json']:copy(f,Path('reference/R19')/f.name)
for site,s in json.load(open(R/'config.json'))['sites'].items():copy(s['loader'],Path('native_loaders')/(site+'.py'))
brief=SYS/'daily_research_reports/1104/meeting_report/meeting_brief_R20_distance_composition_cn.md';copy(brief,'meeting_brief_cn.md')
# Canonical small evidence and execution files are one packet object, not duplicate payloads.
for f in C.rglob('*'):
 if f.is_file() and f.suffix!='.md':
  rel=f.relative_to(C);dest=B/rel
  if rel.parts[0]=='config':dest=B/'data'/f.name
  if dest.exists():mapping[str(f)]=dest;mapping[str(f.resolve())]=dest
external=set()
def rebase(match,doc):
 target=match.group(1);base,_,anchor=target.partition('#')
 if not base or base.startswith(('http:','https:','mailto:')):return match.group(0)
 source=Path(base) if base.startswith('/') else Path(origin[str(doc.relative_to(B))]['source']).parent/base
 dest=mapping.get(str(source)) or mapping.get(str(source.resolve()))
 if dest:return ']('+os.path.relpath(dest,doc.parent)+('#'+anchor if anchor else '')+')'
 if not base.startswith('/') and (doc.parent/base).exists():return match.group(0)
 external.add(str(source));return ']('+os.path.relpath(B/'external_sources.md',doc.parent)+')'
for f in B.rglob('*.md'):
 if 'versions' in f.relative_to(B).parts:continue
 text=f.read_text();new=re.sub(r'\]\(([^)]+)\)',lambda m:rebase(m,f),text)
 if new!=text:f.write_text(new);origin[str(f.relative_to(B))]['transform']='Markdown links rebased to exact included source copy; omitted dependencies use explicit external-source index.'
(B/'external_sources.md').write_text('# External source index\n\nThese source addresses are outside this bounded packet; redirected links do not imply an included payload.\n\n'+''.join('- `'+p+'`\n' for p in sorted(external)))
cfg=json.load(open(R/'config.json'));omitted=[]
paths=list(cfg['input_hashes'])+[s['path'] for s in cfg['sites'].values()]+sorted({s[k] for s in cfg['sites'].values() for k in ['reference_sparse_cache','reference_metadata']})
for p in paths:
 f=Path(p);omitted.append(dict(path=p,bytes=f.stat().st_size,sha256=sha(f),reason='External pretrained identity or independent natural-reference source; frozen groups and actual study arrays are included.'))
dump(B/'omitted_assets.json',dict(payloads=omitted,original_per_row_caches='All228original files remain execution-side; cache/new_all.npzcontains every original field/value with exact repeateddecoder_normdeduplication. Seeevidence/cache_consolidation.jsonfor all228sourceaddresses,SHAsandlosslessarrayverification.',not_saved=['Full LM logits','A new model/SAE checkpoint'],no_training=True))
(B/'README_cn.md').write_text('''# R20 距离与SAE组合：可复核结果包

先读[10秒/30秒组会入口](meeting_brief_cn.md)、[认识更新](records/summary_cn.md)，再看[四案例全文与反例](records/casebook_cn.md)、[数值附录](records/numeric_evidence.md)和[方法/质量](records/detailed_cn.md)。科学接受待研究者审阅，已停止，无训练/干预。

包中包含372条件完整文本/token、两字典全部原生Top32、完整截断前ReLU/h/重构、逐token候选分数、全家族与机会表、图、协议/配置/实际代码。228新条件的每条原缓存都仍在执行侧；包内cache/new_all.npz逐数组无损合并，只去重相同decoder_norm，未删除任何观察数值。原评分cache_sha指源NPZ字节；包内manifest负责当前容器SHA。cache_consolidation.json列出全部源路径/哈希和一致性验证。外部权重/原参考大缓存见omitted_assets.json。

在解压根目录运行`python code/offline_replay.py`，只需Python/NumPy，无模型、网络或GPU。它从真实稀疏值复算所有评分总和、全部成对成员/范数及六项主要结果的点值/区间/p/Holm。

若要重算全部统计表，运行`python code/portable_reanalysis.py`，另需Pandas。它先从无损合并缓存恢复每条数组，在当前解压目录重算主要/对照/频率/支持表并复核；不读取外部权重、不做前向。原ZIP保留。原始模型前向另需外部资产和原环境，见records/reproduce_cn.md；本轮审阅无需重跑模型。

versions目录保留原冻结版本的精确字节和历史绝对源链接；请用records阅读副本阅读。manifest.json逐文件记录SHA/大小/源版本。冻结配置残留旧R19字段已在effective_config.json隔离，实际R20为372条件/228新前向，协议A1保留澄清。包内相对链接可独立阅读；外部源明确单列。

当前ZIP自身的大小/SHA与解压核验回执保存在ZIP旁的同名.manifest.json，避免在包内误放前一版包的回执。包内full_offline_reanalysis_verification.json记录最终元数据整理前的完整统计复算；交付回执另核实两版的所有数值输入、统计代码和结果逐字节相同。复算只产生新的运行UTC；35项统计输出中34项字节相同，模板敏感性JSON除UTC外完全相同。
''')
links=[]
for doc in B.rglob('*.md'):
 if 'versions' in doc.relative_to(B).parts:continue
 for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=target.split('#')[0]
  if not target or target.startswith(('http:','https:','mailto:')):continue
  assert not target.startswith('/') and (doc.parent/target).exists(),(doc,target);assert (doc.parent/target).resolve().is_relative_to(B.resolve());links.append([str(doc.relative_to(B)),target])
manifest=dict(UTC=now(),local_time=local_now(),scope='R20 user-authorized distance-only study; no new scientific acceptance',portable_links=len(links),entries=[])
for f in sorted(B.rglob('*')):
 if f.is_file():manifest['entries'].append(dict(path=str(f.relative_to(B)),bytes=f.stat().st_size,sha256=sha(f),**origin.get(str(f.relative_to(B)),dict(source='R20 packaging derivation'))))
dump(B/'manifest.json',manifest)
dest=SYS/'daily_research_reports/1104/20261104_R20_distance_composition.zip';assert not dest.exists()
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(B.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(B)))
assert dest.stat().st_size<20_000_000,dest.stat().st_size
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='R20_packet_') as td:
  td=Path(td);z.extractall(td)
  for f in json.load(open(td/'manifest.json'))['entries']:assert sha(td/f['path'])==f['sha256']
  r=subprocess.run(['python','code/offline_replay.py'],cwd=td,capture_output=True,text=True);(R/'evidence/package_replay.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
receipt=dict(UTC=now(),local_time=local_now(),status='PASS',zip_path=str(dest),bytes=dest.stat().st_size,sha256=sha(dest),files=len(manifest['entries'])+1,portable_links=len(links),CRC='PASS',all_file_SHA='PASS',fresh_extraction_replay='PASS')
dump(R/'evidence/package_verification.json',receipt);dump(dest.with_suffix('.manifest.json'),receipt);print(json.dumps(receipt,indent=2))
