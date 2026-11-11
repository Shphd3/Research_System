from common import *
import shutil,zipfile,os
import pandas as pd

def main():
 from write_status import main as status
 from write_analysis import main as analysis
 from figures import main as figs
 status();analysis()
 audit=json.load(open(R/'evidence/final_audit.json'))
 # New task artifacts only; no writes under R04.
 for name in ['code','evidence','training_metrics']:(REPORT/name).mkdir(exist_ok=True)
 for p in (R/'code').glob('*.py'):shutil.copy2(p,REPORT/'code'/p.name)
 for p in (R/'evidence').glob('*.json'):
  if p.name.startswith('access_'):continue
  shutil.copy2(p,REPORT/'evidence'/p.name)
 shutil.copy2(R/'evidence/events.jsonl',REPORT/'evidence/events.jsonl')
 for p in (R/'probes').glob('*_metrics.csv'):shutil.copy2(p,REPORT/'training_metrics'/p.name)
 for p in (R/'dictionaries').glob('*_metrics.csv'):shutil.copy2(p,REPORT/'training_metrics'/('dictionary_'+p.name))
 shutil.copy2(R/'protocol_frozen_cn.md',REPORT/'protocol_original_frozen_cn.md')
 gpu={}
 for l in (R/'evidence/events.jsonl').read_text().splitlines():
  x=json.loads(l);gpu[x['check']]=x['gpu_seconds']
 gpu['1_total']=gpu.get('1',0)+gpu.get('1前向',0)
 pd.DataFrame([dict(stage=k,gpu_process_wall_seconds=v,boundary='Measured GPU-stage wall includes in-stage I/O; some initialization excluded; not kernel time or exact billing') for k,v in gpu.items()]).to_csv(REPORT/'gpu_time.csv',index=False)
 (REPORT/'delivery_readme_cn.md').write_text('''# 包内阅读顺序\n\n1. README_cn.md：一页6项结论及规则套用。\n2. analysis_cn.md：各项原始摘要表、边界及为什么；各CSV保留全部精度。\n3. protocol_original_frozen_cn.md：跑前不可变规则和超参数；protocol_cn.md尾部追加实际偏差与用户接受A1微差的记录。\n4. evidence/final_audit.json：完成矩阵、源文件SHA及小模型存档清单。\n\n所有结论为AI分析，研究者判断Unknown。图为实测数据PNG/PDF。表中NaN表示未观测／不适用，不是0。小探针、字典权重和大型隐藏态缓存不进入下载包，仍在执行根；其来源和SHA可定位。部分绝对路径引用原始工作区，离线阅读请用同名CSV及相对链接。主模型未更新，原R04产物未改。\n\nZIP完整性与文件清单见DELIVERY_MANIFEST.json。\n''')
 manifest=dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_root=str(R),files=[dict(path=str(p.relative_to(REPORT)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(REPORT.rglob('*')) if p.is_file() and p.suffix!='.zip' and p.name not in ['DELIVERY_MANIFEST.json','1110-A5增益来源检查_结果.zip.sha256']])
 dump(REPORT/'DELIVERY_MANIFEST.json',manifest)
 target=REPORT/'1110-A5增益来源检查_结果.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for q in manifest['files']:z.write(REPORT/q['path'],q['path'])
  z.write(REPORT/'DELIVERY_MANIFEST.json','DELIVERY_MANIFEST.json')
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for q in manifest['files']:assert hashlib.sha256(z.read(q['path'])).hexdigest()==q['sha256']
 assert target.stat().st_size<20_000_000,target.stat().st_size
 target.with_suffix('.zip.sha256').write_text(sha(target)+'  '+target.name+'\n')
 dump(R/'evidence/delivery_receipt.json',dict(zip=str(target),bytes=target.stat().st_size,sha256=sha(target),crc='PASS',manifest_hashes='PASS',files=len(manifest['files']),scientific_judgment='Unknown'))
 event('交付','本轮结果ZIP已完成，包体小于20MB，CRC及逐文件SHA校验通过。',0,zip=str(target),bytes=target.stat().st_size)
 print(target,flush=True)
if __name__=='__main__':main()
