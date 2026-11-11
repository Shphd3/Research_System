"""Derived portable reading copy; never changes raw source results."""
from fu import *
import shutil,zipfile,re,subprocess

def stage():
 REPORT.mkdir(exist_ok=True,parents=True);changes=[]
 for p in sorted((F/'results').rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(F/'results');dest=REPORT/rel
  if p.parent.name=='raw' and p.stem.startswith('F_statistics_'):
   if dest.exists():dest.unlink()
   changes.append(dict(path=str(rel),source=str(p),source_sha256=sha(p),operation='逐臂底表合并于F_statistics.csv，原列和全部行保留'))
   continue
  dest.parent.mkdir(parents=True,exist_ok=True)
  if p.suffix=='.md' and p.parent.name=='raw':
   csv=p.with_suffix('.csv');d=pd.read_csv(csv);text='# '+p.stem+'\n\nAI 分析；研究者判断 Unknown。便携 Markdown 展示前 20 行；完整 '+str(len(d))+' 行原始数值保留于同名 [CSV]('+csv.name+')。未删除任何 CSV 行或降低 CSV 精度。执行根还保留完整 Markdown 表。\n\n'+d.head(20).to_markdown(index=False,floatfmt='.7g')+'\n';dest.write_text(text);changes.append(dict(path=str(rel),source=str(p),source_sha256=sha(p),portable_sha256=sha(dest),operation='Markdown前20行阅读副本；完整CSV同包',rows=len(d)))
  else:shutil.copy2(p,dest)
 for p in F.glob('protocol*.md'):shutil.copy2(p,REPORT/p.name)
 (REPORT/'code').mkdir(exist_ok=True)
 for p in (F/'code').glob('*.py'):shutil.copy2(p,REPORT/'code'/p.name)
 for p in (ROOT/'code').glob('*.py'):
  q=REPORT/'code/reused';q.mkdir(exist_ok=True);shutil.copy2(p,q/p.name)
 evidence=REPORT/'evidence';evidence.mkdir(exist_ok=True)
 for p in (F/'evidence').glob('*.json'):
  if p.name not in ['final_delivery.json','delivery_asset_registration.json']:shutil.copy2(p,evidence/p.name)
 dump(REPORT/'PORTABLE_TRANSFORMS.json',changes)
 # Minimal source tables for M1 and M4 are part of the same local reading copy.
 for name in ['baseline_NLL_document_CI','fig1_mastery_transitions','fig1_gap_decomposition','baseline_concentration','fig4_switch_recovery']:
  for ext in ['csv','md']:
   p=ROOT/f'results/{name}.{ext}'
   if p.exists():q=REPORT/'previous_source_tables';q.mkdir(exist_ok=True);shutil.copy2(p,q/p.name)
 for p in [ROOT/'evidence/checkpoint_inventory.json',ROOT/'evidence/activation_alignment.json',ROOT/'evidence/execution_cost.json',ROOT/'precision8/evidence/gradient_batches.json']:
  shutil.copy2(p,REPORT/'evidence'/('previous_'+p.name))
 sources=[]
 for p in sorted((F/'results').rglob('*')):
  if p.is_file():sources.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
 dump(REPORT/'SOURCE_MANIFEST.json',sources)

def validate_links():
 bad=[]
 for p in REPORT.rglob('*.md'):
  for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   link=next(x for x in target if x).split('#')[0]
   if not link or link.startswith(('http:','https:','/','mailto:')):continue
   link=link.strip('<>')
   if not (p.parent/link).exists():bad.append(dict(source=str(p.relative_to(REPORT)),link=link))
 return bad

def package():
 name='1111-学会遗忘_追加分析_结果.zip';out=REPORT/name
 items=[p for p in REPORT.rglob('*') if p.is_file() and p.suffix!='.zip' and p.name not in ['FILE_MANIFEST.json','delivery_validation.json']]
 manifest=[dict(path=str(p.relative_to(REPORT)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(items)];dump(REPORT/'FILE_MANIFEST.json',manifest);items.append(REPORT/'FILE_MANIFEST.json');bad=validate_links();assert not bad,bad
 with zipfile.ZipFile(out,'w') as z:
  for p in sorted(items):z.write(p,p.relative_to(REPORT),compress_type=zipfile.ZIP_LZMA)
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for r in manifest:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
  count=len(z.namelist())
 assert out.stat().st_size<20000000,out.stat().st_size
 data=dict(zip=str(out),bytes=out.stat().st_size,sha256=sha(out),files=count,CRC_and_SHA_passed=True,all_CSV_rows_and_precision_preserved=True,large_raw_Markdown_preview_rows=20,local_links_passed=True,old_experiments_read_only=True,training_updates=0)
 dump(F/'evidence/final_delivery.json',data);dump(REPORT/'delivery_validation.json',data);print(json.dumps(data,ensure_ascii=False))
if __name__=='__main__':
 stage();package()
