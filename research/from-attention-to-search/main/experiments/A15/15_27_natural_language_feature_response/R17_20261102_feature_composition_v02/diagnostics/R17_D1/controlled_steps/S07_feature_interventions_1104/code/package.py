from common import *
import zipfile,shutil,tempfile,subprocess,sys
assert json.load(open(R/'evidence/verification.json'))['status']=='PASS'
assert json.load(open(R/'evidence/completed.json'))['task_state']=='COMPLETED_BOUNDED_S07'
stage=R/'combined_package';stage.mkdir(exist_ok=False);shutil.copytree(MAIN/'discussion_package',stage/'main');(stage/'interventions').mkdir()
supp=stage/'interventions'
for folder in ['data','results','figures','code','versions']:
 (supp/folder).mkdir()
 for p in (R/folder).glob('*'):
  if p.is_file():shutil.copy2(p,supp/folder/p.name)
(supp/'evidence').mkdir()
for p in (R/'evidence').glob('*'):
 if p.is_file() and p.suffix in ['.json','.csv','.md']:shutil.copy2(p,supp/'evidence'/p.name)
(supp/'cache').mkdir();shutil.copy2(R/'cache/baseline_tail.npz',supp/'cache/baseline_tail.npz')
for p in R.glob('*'):
 if p.is_file() and p.suffix in ['.md','.json']:shutil.copy2(p,supp/p.name)
(stage/'anchors').mkdir();ar=SYS/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
for pattern in ['15_27_06*anchor*.md','15_27_07*anchor*.md']:
 for p in ar.glob(pattern):shutil.copy2(p,stage/'anchors'/p.name)
shutil.copy2(SYS/'daily_research_reports/1104/meeting_report/sae_feature_hierarchy_with_interventions_cn.md',stage/'daily_report_cn.md')
readme='''# 1104 SAE特征组合、语义层级与干预

先读[组会简报](daily_report_cn.md)，然后分别读[主实验认识更新](main/summary_cn.md)和[干预认识更新](interventions/summary_cn.md)。[主实验完整文本和反例](main/casebook_cn.md)；[干预原文、feature数值、候选分数、词语rank/top词分布与反例](interventions/casebook_cn.md)。详细过程和控制分别在main/detailed_cn.md与interventions/detailed_cn.md；各自协议在同目录protocol.md。

主实验384条、每域16家族(共享16模板簇)、固定8/8；两SAE。先完整保存主结果和独立3.96MB原包，再做补充96条原输入、14976临时干预条件。原主实验与S02–S05文件及权重保持。H1为条件下部分成员关联；H2更受字典/措辞/共同支持约束。干预中Attention动物仅小的同成员方向分数差；不意味着概念转换或MoE/router分工。科研接受与关闭Unknown。

main/保存独立主包的原文件；interventions/保存干预全部条件与其控制、实际旧新坐标、分数／四候选分布、全词表首词rank／概率、所有top20和剩余质量、统计表、6图、脚本及关键注入向量。全4候选概率与全词表概率分母不同。完整384×30000稀疏z包含隐式零，所有文本无删除。anchors/为只读当前Owner快照；main/anchors是主实验完成时快照。原始外部链接保持来源，本离线入口改用此目录结构。

不含：模型/SAE权重、完整大预激活/h缓存和14976条的全部1024维注入向量。执行路径、真实bytes及SHA在两目录large_files_index.json；关键F09注入向量和96条小型末层原状态已含。没有保存完整151936维概率向量，只保存所有条件的完整4候选分布、rank、top20+尾部质量及熵/KL；不把top20冒充全分布。

离线复算：Python+numpy/scipy，主与干预分开运行。

```bash
python main/code/reproduce_portable.py main
python interventions/code/reproduce_portable.py interventions
```

完整模型重跑还需冻结外部可信资产和既有依赖目录，见各自reproduce.md；脚本拒绝覆盖原响应。所有文件bytes/SHA见PACKAGE_MANIFEST.json；ZIP本身校验及原包SHA记录在旁边manifest。仅本地交付，无commit/push/外部发布。
'''
(stage/'README.md').write_text(readme)
day=SYS/'daily_research_reports/1104';dest=day/'20261104_SAE_hierarchy_with_interventions.zip';assert not dest.exists();candidates=R/'package_candidates';candidates.mkdir()
exclusions=[]
for attempt in range(2):
 files=[p for p in sorted(stage.rglob('*')) if p.is_file() and p.name!='PACKAGE_MANIFEST.json' and str(p.relative_to(stage)) not in exclusions]
 manifest=dict(UTC=now(),files=[dict(path=str(p.relative_to(stage)),bytes=p.stat().st_size,sha256=sha(p)) for p in files],excluded_redundant_tables=exclusions,main_prefixes=384,intervention_prefixes=96,intervention_conditions=14976,model_weights=False,full_dense_preactivation=False,full_all_injection_vectors=False,all_candidate_scores_and_rank_distributions=True)
 dump(stage/'PACKAGE_MANIFEST.json',manifest);candidate=candidates/f'candidate_{attempt+1}.zip'
 with zipfile.ZipFile(candidate,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files+[stage/'PACKAGE_MANIFEST.json']:z.write(p,str(p.relative_to(stage)))
 if candidate.stat().st_size<20_000_000:break
 # Exact duplicate derivation from full conditions; not removing scientific values or originals.
 exclusions=['interventions/results/candidate_ranks_and_probabilities.csv']
else:raise RuntimeError('Package still too large; preserve candidates and revise export without dropping conditions')
shutil.copy2(candidate,dest)
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='S07_combined_open_') as td:
  z.extractall(td)
  for p in manifest['files']:assert sha(Path(td)/p['path'])==p['sha256']
  replay={}
  for scope in ['main','interventions']:
   cp=subprocess.run([sys.executable,str(Path(td)/scope/'code/reproduce_portable.py'),str(Path(td)/scope)],capture_output=True,text=True);assert cp.returncode==0,cp.stdout+cp.stderr;replay[scope]=cp.stdout
original=json.load(open(MAIN/'evidence/final_delivery.json'));assert sha(original['path'])==original['sha256']
for p,h in json.load(open(R/'evidence/main_immutable_before.json')).items():assert sha(p)==h
receipt=dict(UTC=now(),path=str(dest),bytes=dest.stat().st_size,MB_decimal=dest.stat().st_size/1e6,sha256=sha(dest),files=len(manifest['files'])+1,CRC='PASS',fresh_extraction_and_all_hashes='PASS',offline_replays=replay,original_main_zip_unchanged=True,original_main_zip_sha256=original['sha256'],excluded_redundant_tables=exclusions,full_conditions_and_top20_included=True,main_scientific_acceptance='Unknown',intervention_scientific_acceptance='Unknown',published=False)
dump(R/'evidence/final_delivery.json',receipt);dump(dest.with_suffix('.manifest.json'),receipt);shutil.copy2(R/'evidence/final_delivery.json',C/'evidence/final_delivery.json')
dump(R/'output_manifest.json',dict(UTC=now(),files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'combined_package' not in p.parts and 'package_candidates' not in p.parts and p.name!='output_manifest.json']))
mp=SYS/'.research/memory/conversations/1104-sae特征组合与语义层级/memory.md';old=mp.read_text()
with mp.open('a') as f:f.write(f'''\n## {now()} -- 按追加授权完成S07干预与合并交付\n\nProcessed by: Codex (harness: Codex desktop; model: unknown)\n\n- Summary: 先完成并保存S06，再按本thread追加用户请求执行96原留出前缀、14976临时组合干预。删除/相对强弱、多剂量、同成员打乱/同侧/其他成员、计数/频率/幅值/范数和跨域检查均完成。原S06全部文件、原包和权重哈希保持；无训练/GPU/云job。\n- Current work: 数值/完整前向等价、分布和源文件复核通过；13图(主7+干预6)、中英报告、组会简报和合并ZIP完成。包{receipt['bytes']}bytes，CRC、解压全部SHA及主/干预离线复算通过。完整14976注入向量45MB留执行侧并索引，关键例进包；所有分数、4候选rank/概率、top20和尾部质量进包，未保存完整词表概率向量。\n- Recognition routing: Attention动物强弱相对同成员等范数打乱仅小的局部分数差；共同大组删除常提高正确边际并影响无关分布，不能解释为类别必要机制。其他域/SAE的未支持、身份/匹配不足保留。具体判断由Summary拥有，科研接受/机制唯一性/关闭Unknown。\n- Next action: 本轮停止；研究者阅读组会/两份Summary及具体rank/反例决定下一问题，不自动扩展训练或router。\n- References: {C}/summary_cn.md；{C}/detailed_cn.md；{C}/casebook_cn.md；{R}/evidence/verification.json；{dest}；{R}/large_files_index.json；两Owner15_27_06/07及其本地阅读副本。\n''')
t=mp.read_text().splitlines();t=[('Latest update at: '+receipt['UTC']) if a.startswith('Latest update at:') else a for a in t];mp.write_text('\n'.join(t)+'\n')
# A direct downloadable entry and owner/protocol/memory navigation; one combined speaking surface.
entry=day/'sae_hierarchy_delivery.md';entry.write_text(f'''# 1104阅读与下载

[合并结果包，{receipt['MB_decimal']:.3f}MB]({dest.name})；[原主包，3.961MB，保持原SHA](20261104_SAE_hierarchy_analysis.zip)。包CRC/解压SHA/主与干预复算均通过。

[组会简报](meeting_report/sae_feature_hierarchy_with_interventions_cn.md)；[主Summary]({C.parent/MAIN.name}/summary_cn.md)；[干预Summary]({C}/summary_cn.md)；[干预完整排名与分布]({C}/casebook_cn.md)。

[H1 Anchor]({ar}/15_27_06_common_members_extra_responses_anchor.md)；[H2 Anchor]({ar}/15_27_07_conditional_relative_strength_anchor.md)；[主Protocol]({C.parent/MAIN.name}/protocol.md)；[干预Protocol]({C}/protocol.md)；[本对话memory]({mp})；[主图]({C.parent/MAIN.name}/figures)；[干预图]({C}/figures)。科学接受Unknown，本地副本未发布。
''')
print('S07_DELIVERY',json.dumps(receipt),flush=True)
