"""Portable <=10MB reading bundle of this step, not the entire historical R17."""
from common import *
import re,shutil,tempfile,zipfile,urllib.parse,os
day=S/'daily_research_reports/1103';dest=day/'20261103_S03_animal_H1_H2_discussion.zip'
assert not dest.exists(),'No overwrite'
# Record exact final figure sources and visual audit; no scientific selection changed.
dump(R/'evidence/figure_review.json',dict(UTC=now(),figures=[p.name for p in (R/'figures').glob('*.png')],inspection='All six initial renders inspected; margins/titles and legends repaired without changing inputs or selection. Final heatmaps show complete row labels and atom IDs; legends moved below bars. No claim of rendered mathematical proof.',data_sources=['cache/exploration.npz','cache/heldout_check.npz','results/selection.json','results/*/transitions.csv'],units='z raw; u decoder-direction weighted; q unit L2 on fixed list; member count native support',aggregation='one row is one text; independent descriptive unit is family',boundary='visual evidence of response/support only; no additional functional information or causal role'))
for n in ['output_access.json','figure_review.json']:
 shutil.copy2(R/'evidence'/n,C/'evidence'/n)
manifest=json.load(open(C/'payload_manifest.json'))
for n in ['evidence/output_access.json','evidence/figure_review.json','code/package.py']:
 p=R/n;d=C/n;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
 manifest['files'].append(dict(path=n,source=str(p),sha256=sha(p),bytes=p.stat().st_size,role='requested evidence reading copy'))
dump(C/'payload_manifest.json',manifest)

def checklinks(root):
 bad=[];checked=0
 for p in root.rglob('*.md'):
  for raw in re.findall(r'!?\[[^\]]*\]\(([^\n)]+)\)',p.read_text()):
   link=raw.strip().strip('<>')
   if link.startswith(('http:','https:','mailto:','#')):continue
   path=urllib.parse.unquote(link.split('#')[0]);target=(p.parent/path).resolve();checked+=1
   if not target.exists():bad.append(dict(file=str(p.relative_to(root)),link=raw))
 assert not bad,bad
 return checked
links=checklinks(C)
for item in manifest['files']:assert sha(C/item['path'])==item['sha256']==sha(item['source'])
dump(R/'evidence/delivery_checks.json',dict(UTC=now(),Markdown_links_checked=links,broken_links=0,byte_exact_generated_copies=len(manifest['files']),asset_strict_output='PASS',old_steps_unchanged=True,figure_layout='repaired and inspected',commit_push_publication='NOT_RUN'))
shutil.copy2(R/'evidence/delivery_checks.json',C/'evidence/delivery_checks.json')

with tempfile.TemporaryDirectory(prefix='s03_portable_') as tmp:
 root=Path(tmp)/'S03_animal_H1_H2_24';shutil.copytree(C,root)
 files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts];portable=dict(UTC=now(),source_root=str(C),scope='Only S03 requested scripts,24texts,old12texts/scores,full raw arrays/tables, six figures and bilingual reports; no weights, historical bulk or future experiments.',files=[dict(path=str(p.relative_to(root)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(files)])
 dump(root/'MANIFEST.json',portable)
 assert checklinks(root)==links
 with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(root.rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(root.parent))
 assert dest.stat().st_size<10_000_000,('Archive too large',dest.stat().st_size)
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  fresh=Path(tmp)/'verified_extract';z.extractall(fresh)
 rr=fresh/root.name;assert checklinks(rr)==links
 for f in portable['files']:assert sha(rr/f['path'])==f['sha256']
 receipt=dict(UTC=now(),archive=str(dest),bytes=dest.stat().st_size,MB_decimal=dest.stat().st_size/1_000_000,limit_bytes=10_000_000,sha256=sha(dest),payload_files=len(portable['files']),Markdown_links=links,source_hashes_verified=True,CRC='PASS',fresh_extract='PASS',scientific_acceptance='Unknown',next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW')
 dump(day/'20261103_S03_animal_H1_H2_discussion.manifest.json',dict(**receipt,source_manifest=portable))
 dump(R/'evidence/discussion_package_receipt.json',receipt)
# Append only the dated navigation entry; the project remains the sole scientific owner.
relative=os.path.relpath(C/'summary_cn.md',day)
for fn,body in [('README_cn.md',f'\n- [S03 动物猫狗H1/H2小例子]({relative})：24条、探索3家族／检查3家族、两套冻结SAE。部分共同／新增和比例方向复现，也保留失败。未验证额外信息或因果作用；已停止待审阅。[讨论包](20261103_S03_animal_H1_H2_discussion.zip)，{receipt["MB_decimal"]:.3f} MB（小于10MB）；含全部24条、原始数组、脚本、6图和逐例中文分析。[包核验](20261103_S03_animal_H1_H2_discussion.manifest.json)。\n'),('README.md',f'\n- [S03 animal/cat/dog H1/H2]({relative.replace("summary_cn.md","summary.md")})：24rows, 3exploration/3check families, two frozen nativeSAEs; descriptive observations and all failures, no incremental-information or causal test. Stopped for joint review. [Discussion archive](20261103_S03_animal_H1_H2_discussion.zip), {receipt["MB_decimal"]:.3f}MB (<10MB), full data/code/raw arrays/six figures; [verified manifest](20261103_S03_animal_H1_H2_discussion.manifest.json).\n')]:
 p=day/fn;assert '20261103_S03_animal_H1_H2_discussion.zip' not in p.read_text()
 with p.open('a') as f:f.write(body)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
