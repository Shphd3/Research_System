from common import *
import shutil,zipfile,os,re,subprocess,tempfile
import numpy as np
B=R/'discussion_package';assert not B.exists(),'Keep old package; use a new version instead of overwrite.';B.mkdir();mapping={};provenance={}
def copy(source,dest):
 source=Path(source);dest=B/dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest);mapping[str(source)]=dest;mapping[str(source.resolve())]=dest;provenance[str(dest.relative_to(B))]=dict(source=str(source),source_sha256=sha(source),transform='byte copy')
for f in C.rglob('*'):
 if f.is_file() and f.suffix in ['.md','.csv','.png','.json','.py','.cpp'] and 'archive' not in f.parts:copy(f,Path('records')/f.relative_to(C))
for f in (R/'code').iterdir():
 if f.suffix in ['.py','.cpp']:copy(f,Path('code')/f.name)
for f in (R/'data').iterdir():
 if f.name=='panel.jsonl':continue
 copy(f,Path('data')/('panel.jsonl' if f.name=='panel_portable.jsonl' else f.name))
for folder in ['results','tables','figures']:
 for f in (R/folder).iterdir():
  if f.is_file() and f.suffix in ['.json','.jsonl','.csv','.png','.md']:copy(f,Path(folder)/f.name)
for f in (R/'evidence').iterdir():
 if f.is_file() and f.suffix in ['.json','.jsonl']:copy(f,Path('evidence')/f.name)
for folder in ['pre_result_owners','presentation_v1']:
 for f in (R/'evidence'/folder).iterdir():
  if f.is_file():copy(f,Path('evidence')/folder/f.name)
copy(R/'evidence/heldout_interrupted_20261104T0456/incident.json','evidence/heldout_interrupted_incident.json')
copy(R/'config.json','config.json')
for split in ['smoke','discovery','heldout']:
 f=R/f'cache/{split}.npz';a=np.load(f);dest=B/f'cache/{split}.npz';dest.parent.mkdir(exist_ok=True);np.savez_compressed(dest,**{k:a[k] for k in a.files if not k.endswith('__h')});provenance[str(dest.relative_to(B))]=dict(source=str(f),source_sha256=sha(f),transform='Omit __h only; IDs, Top32 values, cutoffs, decoder norms and other sparse diagnostics unchanged.')
for f in (R/'cache').glob('*_null.npz'):copy(f,Path('cache')/f.name)
focus=P/'main/focus/focus_remote_target_near_competitor_composition.md'
for f in [focus,focus.with_name(focus.stem+'_cn.md')]:copy(f,Path('records')/f.name)
brief=SYS/'daily_research_reports/1104/meeting_report/meeting_brief_R19_remote_target_competitor_cn.md';copy(brief,'meeting_brief_cn.md')
omitted=[];cfg=json.load(open(R/'config.json'))
for path in list(cfg['input_hashes'])+[s['path'] for s in cfg['sites'].values()]+sorted({s[k] for s in cfg['sites'].values() for k in ['reference_sparse_cache','reference_metadata']})+[str(R/f'cache/{s}.npz') for s in ['smoke','discovery','heldout']]:
 f=Path(path);omitted.append(dict(path=path,bytes=f.stat().st_size,sha256=sha(f),reason='External pretrained identity or full hook-input cache; sparse projections are included.'))
for site,s in cfg['sites'].items():copy(s['loader'],Path('native_loaders')/(site+'.py'))
dump(B/'omitted_assets.json',dict(payloads=omitted,not_saved=['Full pre-TopK activation vectors; full model logits; additional checkpoints'],weights_modified=False))
external={}
def relink(match,doc):
 target=match.group(2);anchor=''
 if '#' in target:target,anchor=target.split('#',1);anchor='#'+anchor
 if target.startswith('http') or target.startswith('mailto:') or target.startswith('#'):return match.group(0)
 raw=target.split(':')[0] if re.search(r':\d+$',target) else target
 source=Path(raw) if raw.startswith('/') else Path(provenance.get(str(doc.relative_to(B)),{}).get('source',doc)).parent/raw
 found=mapping.get(str(source)) or mapping.get(str(source.resolve()))
 if found:return ']('+os.path.relpath(found,doc.parent)+anchor+')'
 if (doc.parent/target).exists():return match.group(0)
 external[str(source)]=True
 return ']('+os.path.relpath(B/'external_sources.md',doc.parent)+')'
for doc in B.rglob('*.md'):
 old=doc.read_text();new=re.sub(r'(\])\(([^)]+)\)',lambda m:relink(m,doc),old)
 if new!=old:
  doc.write_text(new);provenance.setdefault(str(doc.relative_to(B)),{})['transform']='Markdown links rewritten to included relative copies; nonincluded sources point to explicit external-source index.'
(B/'external_sources.md').write_text('# External source index\n\nThese original sources are outside this bounded packet. A link redirected here does not mean its payload is included. The actual source addresses are preserved below.\n\n'+''.join('- `'+s+'`\n' for s in sorted(external)))
(B/'README_cn.md').write_text('''# R19 远处目标与近处竞争的 feature 组合

先读[组会入口](meeting_brief_cn.md)，再读[完整认识更新](records/summary_cn.md)、[完整原文与真实 feature](records/casebook_cn.md)和[执行及边界](records/detailed_cn.md)。所有科学接受与下一实验选择均待研究者审阅；已停止，无训练或激活干预。

包内包含292条真实全文/token、完整逐候选评分、两套字典全部正激活、固定成员与频率、逐家族差值、全联合统计参照轨迹、图、冻结协议及实际代码。原始模型/SAE权重与完整h缓存未纳入；[清单](omitted_assets.json)记录真实地址、字节与SHA。未保存的前TopK全量向量单列，不假称存在。

在此目录运行 `python code/offline_replay.py`，需要 Python、NumPy、SciPy，不需要模型、GPU或网络。复算从稀疏原始激活和逐token分数出发，检查成员、六项主要检验的点值/区间/校正p、四项联合检验和零假设投影；不只读取报告数值。重新做模型前向需要外部权重和原运行环境，参见[复现说明](records/reproduce_cn.md)。

`manifest.json`列出每个文件的实际大小、SHA与来源/转换。相对链接用于包内阅读；外部来源统一标记，不宣称可离线读取。已有 R18 原件未改。
''')
links=[]
for doc in B.rglob('*.md'):
 for m in re.finditer(r'\]\(([^)]+)\)',doc.read_text()):
  target=m.group(1).split('#')[0]
  if not target or target.startswith(('http:','https:','mailto:')):continue
  assert not target.startswith('/'),(doc,target)
  assert (doc.parent/target).resolve().is_relative_to(B.resolve()) and (doc.parent/target).exists(),(doc,target);links.append([str(doc.relative_to(B)),target])
manifest=dict(UTC=now(),scope='User-authorized R19 analysis packet; source scientific judgments unchanged',portable_links=len(links),entries=[])
for f in sorted(B.rglob('*')):
 if f.is_file():manifest['entries'].append(dict(path=str(f.relative_to(B)),bytes=f.stat().st_size,sha256=sha(f),**provenance.get(str(f.relative_to(B)),dict(source='R19 packaging derivation'))))
dump(B/'manifest.json',manifest)
dest=SYS/'daily_research_reports/1104/20261104_R19_remote_target_competitor_composition.zip';assert not dest.exists()
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(B.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(B)))
assert dest.stat().st_size<20_000_000
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='R19_extract_') as td:
  z.extractall(td);td=Path(td)
  for row in json.load(open(td/'manifest.json'))['entries']:assert sha(td/row['path'])==row['sha256']
  result=subprocess.run(['python','code/offline_replay.py'],cwd=td,capture_output=True,text=True);(R/'evidence/package_offline_replay.log').write_text(result.stdout+result.stderr);assert result.returncode==0,result.stderr
receipt=dict(UTC=now(),status='PASS',zip_path=str(dest),bytes=dest.stat().st_size,sha256=sha(dest),files=len(manifest['entries'])+1,portable_links=len(links),CRC='PASS',fresh_extraction_hashes='PASS',offline_replay='PASS',source_R18_unchanged=True)
dump(R/'evidence/package_verification.json',receipt);dump(dest.with_suffix('.manifest.json'),receipt);print(json.dumps(receipt,indent=2))
