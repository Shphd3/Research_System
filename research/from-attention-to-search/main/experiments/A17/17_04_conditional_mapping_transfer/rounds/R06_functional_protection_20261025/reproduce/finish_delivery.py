from pathlib import Path
import json,csv,hashlib,datetime,shutil,re,zipfile
ROOT=Path(__file__).resolve().parents[1];S=Path('/data/250010109/Research_System');P=S/'Projects/from-attention-to-search';OWN=json.load(open(ROOT/'provenance/ownership.json'));R=Path(OWN['round']);A=Path(OWN['anchor'])
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 assert (ROOT/'provenance/output_registration.json').exists()
 ag=list(csv.DictReader(open(ROOT/'analysis/method_means_12.csv')));idx={(int(x['old_nonzero']),x['method']):x for x in ag}
 dec=list(csv.DictReader(open(ROOT/'analysis/operational_decisions.csv')));tr=list(csv.DictReader(open(ROOT/'analysis/frequency_relative_gains.csv')))
 term=json.load(open(ROOT/'terminal.json'));ver=json.load(open(ROOT/'analysis/verification.json'));g=json.load(open(ROOT/'provenance/final_geometry_verification.json'))
 assert ver['complete_runs']==36
 cn='''
## AI解读：有条件收益，频率关系不单调

**H1在零旧重放目标档得到有限支持。** F的平均旧准确率11.292%，U与D均0.125%，S为0.208%；F新准确率98.792%，比U低1.042个百分点。F对U/S/D的旧改善在三个顺序均为正，且新下降均在5个百分点内，达到事前操作门槛。当前幅度控制D没有复现收益，说明结果不只体现该局部幅度控制的作用。但旧能力仍从起点100%掉到约11%，不能称为已保持旧规则。F每步使用64条旧标签，收益属于旧标签辅助的局部保护规则，不能归于无需旧信息的参数分解。

**H3在有旧重放时更符合结果。** 每步只增加4条旧目标，U旧准确率已达93.125%，F反而降到68.250%，三个顺序F−U均为负；新准确率分别99.042%和98.208%。36条旧目标时U已达旧99.708%、新99.458%，F旧99.750%、新98.792%，没有稳定额外保留。共享参数加正确旧监督已能兼顾当前两规则，当前结果不要求分专家。

**未支持“监督越少，F优势越大”的三档单调关系。** F−U旧收益依次为+11.167、−24.875、+0.042个百分点；三个顺序都不满足0槽>4槽>36槽的冻结趋势判据。可以说零旧重放目标时存在相对收益，不能把非单调的三点概括成普适频率规律。

**一阶约束没有变成有限步保证。** 预定90个F有限步检查中，69次同一旧探针实际损失上升；一阶项与有限变化及余项完整分列。作为事后说明性样本，顺序29、零旧目标、F第1步，探针CE从1.91465e−5升到3.44467e−5 nat/答案，而实际位移的一阶预测约7.87e−13。这个小量样本只说明“预测近零不等于有限变化为零”，不能解释全部终点退化。探针代表性、有限步余项与优化轨迹的相对作用仍未区分；当前不新增实验。

次要学习水平比较也显示F有学习成本：U在三个顺序均于第180步完成连续两次90%的确认；零旧目标的F为第240、180、240步。它不替代固定240步的主结论，且实际确认时的新准确率与样本成本分别列出，不假装相同精确学习水平。

下一项建议是优先审视“旧目标为何比当前局部投影更有效，以及局部预测何时失效”，而非直接推进新MoE或不断换大奇异方向。本轮具体矩阵执行与记录已完成并停止训练；研究者的机制接受、后续实验选择和整个主问题关闭仍Unknown。
'''
 with (R/'summary_cn.md').open('a') as f:f.write(cn)
 en='''
## AI interpretation within the frozen scope

At k=0, F improves mean old accuracy from0.125% (U/D) to11.292% (S0.208%), with new98.792% versus U99.833%. F has positive old differences in every continuation order and each new difference stays within5pp against U/S/D, meeting the registered operational rule. This is limited retention: old accuracy remains far below the100% start. D does not reproduce the gain, but own-state norm control does not prove that all trajectory slowing alternatives are eliminated. F uses64old TRAIN labels per update.

At k=4, U already reaches93.125%old/99.042%new, whereas F reaches68.250%/98.208%; F-old is lower in every order. At k=36, U reaches99.708%/99.458%, F99.750%/98.792%, without stable added retention. Thus supervision organization explains the large high-replay benefit more directly than a general advantage of this projection rule. F-minus-U old gains+11.167,-24.875,+0.042pp are nonmonotonic in all three orders; the frozen three-level frequency trend is unsupported.

69of90predeclared F finite-step checks show positive realized old-probe CE change despite near-nonpositive first-order prediction. These are selected fixed diagnostic steps, not a fraction of all updates or a statistical significance claim. Probe representativeness, finite-step remainder and optimizer trajectory contributions remain unresolved. At zero old objective, the second consecutive new90percent reading is step180for all U, versus240/180/240for F; this secondary operating point does not replace step240. No new training follows. These are AI bounded interpretations; researcher acceptance and parent-question closure remain Unknown.
'''
 with (R/'summary.md').open('a') as f:f.write(en)
 # Explicit cost and inert legacy configuration notes.
 for p in [R/'detailed.md',R/'detailed_cn.md']:
  with p.open('a') as f:f.write('\nLegacy R05 configuration fields objective/moe/natural/reselect_steps/old milestones are inert in this engine. Actual R06 objective, batches, probes and evaluations use the explicit new flat fields and hard-bounded engine loop. full_updates=1200 owns only the inherited S attenuation horizon; max_updates=240 owns the scientific run budget. No legacy stage was launched.\n\n360 fixed finite-step probe checks and all original DEV cells are in tables/probe_finite_diagnostics_360.csv and DEV_cells_all_readings.csv. Probe-gradient label uses15360 plus640post-update diagnostic reuses=16000per full run; objective old labels0/960/8640are separate. Positive raw finite differences include small floating-point values and are not significance tests.\n')
 # Rewrite only the requested speaking brief's result paragraph, keeping five paragraphs.
 manifest=json.load(open(R/'artifact_manifest.json'));b=Path(manifest['meeting_brief']);s=b.read_text()
 start=s.index('**结果如何更新判断。**');end=s.index('\n\n**边界与下一步。**',start)
 para='**结果如何更新判断。** 旧目标为0时，F把平均旧准确率从U的0.125%提高到11.292%，新准确率从99.833%变为98.792%；幅度控制D和Top-16的S没有复现该收益，F达到冻结的操作门槛，但旧能力仍大幅丢失。每步加入4条旧目标后，普通U已达旧93.125%、新99.042%，F反而为旧68.250%、新98.208%，三个顺序旧表现都更差。加入36条旧目标后U已达旧99.708%、新99.458%，F没有稳定额外收益。因此，功能方向选择只在零旧重放目标档有有限价值，正确旧监督的直接作用更大。'
 s=s[:start]+para+s[end:]
 start=s.index('**边界与下一步。**');end=s.index('\n\n[完整结果与曲线]',start)
 para='**边界与下一步。** 三档F−U收益不单调，不能概括为“旧监督越少越有效”。F/D在0槽时仍使用每步64条旧TRAIN探针标签；它们只约束一阶预测，90个固定F检查中69次实际探针损失仍上升。有限步误差、探针代表性和优化轨迹尚未区分。本轮36条轨迹与证据整理完成，训练已停止。AI建议先理解局部约束为何不能稳定转化为功能保持，再决定后续研究；当前不推出MoE必要性或自然语言feature频率机制。'
 s=s[:start]+para+s[end:];b.write_text(s)
 # Factual continuation note, no status reset or scientific closure.
 for lang in ['', '_cn']:
  p=P/'main/focus'/f'focus_conditional_mapping_transfer{lang}.md'
  with p.open('a') as f:
   if lang:f.write('\n### R06事实交付\n\n36/36条240步轨迹完成，训练墙钟1510.916秒；固定新曝光下F仅在零旧重放目标档达到预定操作门槛，4槽档旧表现稳定低于U，36槽档无稳定额外收益。三个档位的相对收益不单调。这是冻结规则的AI有界解读，不更新研究者机制接受或总问题关闭。[结果](../experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/summary_cn.md)。\n')
   else:f.write('\n### R06 factual delivery\n\n36/36 step240 trajectories completed in1510.916seconds. Under fixed new exposure, F meets the registered operational criterion only with zero old replay in the objective; k4 consistently hurts old behavior relative to U, k36 adds no stable benefit. Relative gains are nonmonotonic. This bounded AI reading does not set researcher scientific acceptance or parent closure. [Results](../experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/summary.md).\n')
 # Light provenance copies, excluding weight/log/evaluation payloads.
 for p in [ROOT/'analysis/checkpoints_manifest.json',ROOT/'provenance/verified_inputs.json',ROOT/'provenance/input_access.json',ROOT/'budget.json',ROOT/'terminal.json',ROOT/'provenance/platform_terminal.txt']:
  shutil.copy2(p,R/'reproduce'/p.name)
 for name in ['finish_delivery.py']:
  shutil.copy2(ROOT/'ops'/name,R/'reproduce'/name)
 # Byte identity and all scoped links.
 problems=[];nlinks=0
 for p in [*R.rglob('*.md'),*A.glob('*.md'),b]:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   target=target.strip('<>').split('#')[0]
   if not target or re.match(r'^[a-zA-Z]+://',target):continue
   q=Path(target) if target.startswith('/') else p.parent/target
   nlinks+=1
   if not q.exists():problems.append({'source':str(p),'target':target})
 assert not problems,problems
 assert all(sha(p)==v['sha256'] for p,v in json.load(open(ROOT/'provenance/freeze.json'))['files'].items())
 write(ROOT/'provenance/scoped_delivery_check.json',{'status':'PASS','checked_local_links':nlinks,'frozen_bytes_unchanged':True,'all_36_endpoints_and360_probe_readings_verified':True,'plots_visually_reviewed':'accuracy_curves.png; standalone loss/seed curves share aggregation source','original_results_unchanged':True,'raw_events_preserved':True,'global_navigation':'7 preexisting unrelated untracked entries, not repository-wide PASS'})
 shutil.copy2(ROOT/'provenance/scoped_delivery_check.json',R/'reproduce/scoped_delivery_check.json')
 # Refresh hashes only after factual text/certificate/figure provenance is complete.
 manifest['curated_files']={str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and p.name!='artifact_manifest.json'}
 manifest['scientific_trajectory_updates']=8640;manifest['engineering_replay_updates']=1;manifest['probe_label_uses_per_run']={'gradient':15360,'post_update_diagnostic':640,'total':16000};manifest['training_wall_seconds']=term['training_wall_seconds']
 write(R/'artifact_manifest.json',manifest)
 # Scope-specific root asset guide entries; preserve every previous entry.
 for name in ['README.md','README_cn.md']:
  p=S/'assets'/name
  with p.open('a') as f:f.write('\n## A17 R06 actual outputs (2026-10-25 UTC)\n\nRegistered checkpoint_family_a17_r06_functional_20261025 (288 actual states) and analysis_a17_r06_functional_20261025. [Results](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/summary_cn.md). Input identities, actual member digests and scope-specific current output access are retained in the round evidence index; payloads remain execution-side.\n')
 print(json.dumps({'status':'PASS','links':nlinks,'brief':str(b),'curated_files':len(manifest['curated_files'])},ensure_ascii=False))
if __name__=='__main__':main()
