from lf_common import *
import shutil,zipfile,re
from urllib.parse import unquote,quote
import report
def main():
 for p in ['fig1_complete.json','fig2_complete.json','fig3_complete.json','gradient_refinement_complete.json','fig3_EVAL_load_calibration.json']:assert (R/'evidence'/p).exists(),p
 assert (R/'precision8/evidence/fig2_complete.json').exists()
 report.main()
 calibrated=pd.read_csv(R/'results/fig3_EVAL_load_calibration.csv');equal=calibrated[calibrated.label=='equal'].iloc[0]
 with (REPORT/'明早速报_cn.md').open('a') as f:
  f.write('\n\n## 图3的负载可行性补充（与冻结DEV偏置分开）\n\n![负载校准敏感性](图3_负载校准敏感性.png)\n\n固定DEV学出的A，只对EVAL边缘负载校准离线偏置，得到等权M中位数'+f'{equal.overall_M_median:.6f}'+'，负载比'+f'{equal.EVAL_max_load:.6f}'+'。这是使用EVAL边缘分布的转导校准可达值，不能称为冻结DEV偏置的泛化上界。原未校准1.775444、负载比1.257957保留；lambda1的指定更新依然无可行端点。\n\n'+calibrated.to_markdown(index=False,floatfmt='.6f')+'\n')
  f.write('\n\n## 给后续方案讨论的认识\n\nAI分析：当前低频高占比位置的掌握率优势主要来自新学会项，减少遗忘不是主要解释；容易由bigram识别的位置例外。梯度测量支持部分共现低高频内容在当前点借力，但批次噪声、训练阶段与参数块会改变冲突读数，尚不能据此永久隔离内容。离线表能提高集中度，但只优化低频时若丢掉背景分发信息，会先破坏负载可行性。下一架构仍需同时看获得速度、稳定的梯度信号、背景位置分发和真实训练收益；本轮未训练新架构。研究者判断Unknown。\n')
 coverage=[]
 def add(item,status,evidence,bound=''):coverage.append(dict(item=item,status=status,evidence=evidence,boundary=bound))
 add('0inventory_and_initial','DONE_VALID','checkpoint_inventory_final.csv;14forwardreceipts','12trajectory states plusMoE33B andDense34.076B references;allstrictloadedandSHAverified')
 add('0activation_alignment','DONE_VALID','evidence/activation_alignment.json','FFNactivebudgetequal;MoEadds65536routerparameters andhaslargertotalcapacity')
 add('0position_forward','DONE_VALID','positions/*.npz;forward_*.json','eval;modelandbiasunchanged;nooptimizer')
 add('0NLL_and_M','DONE_VALID','baseline_NLL_document_CI.csv;baseline_concentration.csv','Same2097152positions;docbootstrap2000')
 add('1mastery_acquisition_forgetting','DONE_VALID','fig1_mastery_transitions.csv;fig1_gap_decomposition.csv','MoE33Bprimary,Dense34.076Brequested sensitivity;Dense10Bextra;thresholdtiesandinitialstateexplicit')
 add('2gradient16groups','DONE_VALID','fig2_rules.csv;fig2_borrowing_by_A5_group.csv','All16groupsR4at1B/10Bforbothmodels;nonpositivesignalsmissing;localreadout')
 add('2precision8seq','DONE_EXPLORATORY','precision8/fig2_rules.csv;fig2_projection_norm_calibration.csv','One additionalbatchprecisioncheck;notreplacementofregistered1seq')
 add('3all_optimizer_conditions','DONE_EXPLORATORY','fig3_optimization_history.csv;fig3_frontier.csv','6objectives*4starts*30updatediterates;DEVselectiononly;notglobaloptimum')
 add('3lambda1_feasible_updated_endpoint','FAILED','fig3_feasibility_diagnostic.csv;fig3_frontier.csv','Specifiedupdatezerosbackground47.52%positions,loadlowerbound1.9008>1.2;initialA5canbefeasible,notglobalinfeasibility')
 add('3frozen_DEV_bias_EVAL_load_cap','FAILED','fig3_frontier.csv','AllfrozenDEVbiasoptimizedsolutions exceed1.2onEVAL;equal1.257957')
 add('3EVAL_load_calibrated_sensitivity','DONE_EXPLORATORY','fig3_EVAL_load_calibration.csv','FixedDEV A;transductiveEVALmarginalbiascalibration;no modelbiasupdate')
 add('4fit_and_switch','DONE_VALID','fig4_fixed_fit_residuals.csv;fig4_switch_recovery.csv','Fixed3armOLSdescriptive;gate/bias/routingjointswitch')
 add('4real_interval_forgetting','DONE_VALID','fig4_forgetting_all.csv','Originalledgerdefinitionsandactualsavedintervals')
 add('4all_old_arms_250grid','BLOCKED','fig4_forgetting_all.csv','OldA0only500-step,A4/A1deep1000-step positions;missingweightsnotretrained;countsnotinterpolated')
 table(pd.DataFrame(coverage),'coverage','FAILEDmeansconstraintorqualificationfailedafteractualmeasurement;BLOCKEDhistoricalgriddataismissing. No untrainedrequiredmodelremains.')
 for ext in ['csv','md']:shutil.copy2(R/f'results/coverage.{ext}',REPORT/f'coverage.{ext}')
 (REPORT/'README_cn.md').write_text('# 学会遗忘四张图\n\n先读[明早速报](明早速报_cn.md)，再按图号打开PNG/PDF、CSV/Markdown。\n\n[逐项完成／失败／缺口](coverage.md)；[冻结读法](protocol_cn.md)；[实际偏差和澄清](protocol_deviations_cn.md)。\n\n四张图指四个问题；每个问题可含多个面板、参照敏感性或参数块。包不含模型权重、逐位置大文件和完整梯度，保存的是原始统计表与固定梯度投影的来源索引。\n')
 projections=list((R/'gradient').glob('*.npy'))+list((R/'precision8/gradient').glob('*.npy'));position_files=list((R/'positions').glob('*.npz'));lookup=[]
 for p in projections+position_files:lookup.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
 dump(R/'evidence/large_output_manifest.json',lookup)
 register('representation_learn_forget_positions_20261111',position_files+[R/'evidence/large_output_manifest.json'],dict(positions_per_checkpoint=N,checkpoints=14,loss='fp16',MoE_Top2='uint8,8layers',model_updates=0),category='representation')
 register('analysis_learn_forget_gradient_sketches_20261111',projections+[R/'evidence/gradient_precision_sensitivity_plan.json'],dict(projection='fixedCountSketch2^20',models=['MoE','Dense'],nodes=[1000000000,10000000000],R=4,primary_sequences_per_batch=1,secondary=8,model_updates=0))
 small=list((R/'results').rglob('*'));small=[p for p in small if p.is_file()];manifest=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in small];dump(R/'evidence/result_manifest.json',manifest)
 register('analysis_learn_forget_four_figures_20261111',small+[R/'evidence/result_manifest.json',R/'protocol_cn.md',R/'protocol_deviations_cn.md'],dict(producer=str(Path(__file__).resolve()),researcher_judgment='Unknown',coverage=str(R/'results/coverage.csv')))
 primary=json.load(open(R/'evidence/fig2_complete.json'))['seconds'];secondary=json.load(open(R/'precision8/evidence/fig2_complete.json'))['seconds'];forward=sum(json.load(open(p)).get('GPU_seconds',0) for p in (R/'evidence').glob('forward_*.json'));cost=dict(primary_gradient_process_seconds=primary,secondary_gradient_process_seconds=secondary,failed_gradient_conservative_seconds=120,total_gradient_budget_charged_seconds=primary+secondary+120,gradient_limit_seconds=5400,forward_process_seconds=forward,local_device=str(torch.cuda.get_device_properties(0)),model_updates=0,note='Process wall spans includeCPUload/hash/IO,notCUDAkernel-onlytime;onlyalreadyallocatedlocalMIGused')
 assert cost['total_gradient_budget_charged_seconds']<=5400;dump(R/'evidence/execution_cost.json',cost)
 bundle=R/'delivery';bundle.mkdir(exist_ok=True)
 for p in REPORT.rglob('*'):
  if p.is_file() and p.suffix!='.zip':dst=bundle/p.relative_to(REPORT);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
 for folder,patterns in [('code',['*.py']),('evidence',['*.json']),('offline',['lambda*.npz','equal.npz'])]:
  for pat in patterns:
   for p in (R/folder).glob(pat):dst=bundle/folder/p.name;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,dst)
 for p in (R/'precision8/evidence').glob('*.json'):
  dst=bundle/'evidence/precision8'/p.name;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,dst)
 files=[dict(path=str(p.relative_to(bundle)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(bundle.rglob('*')) if p.is_file() and p.name!='FILE_MANIFEST.json'];dump(bundle/'FILE_MANIFEST.json',files)
 zip_path=REPORT/'1111-学会遗忘的四张图_结果.zip'
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(bundle.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(bundle)))
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None
  for row in files:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
 receipt=dict(time_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),path=str(zip_path),bytes=zip_path.stat().st_size,sha256=sha(zip_path),files=len(files)+1,CRC='PASS',manifest_hashes='PASS',researcher_judgment='Unknown');dump(R/'evidence/delivery.json',receipt)
 register('analysis_learn_forget_delivery_20261111',[zip_path,R/'evidence/delivery.json',bundle/'FILE_MANIFEST.json'],dict(sha256=receipt['sha256'],coverage=str(R/'results/coverage.csv'),researcher_judgment='Unknown'))
 event('交付','四图与全部可运行条件完成，失败约束和历史缺口已列明',zip_bytes=receipt['bytes'],gradient_budget_seconds=cost['total_gradient_budget_charged_seconds']);print(json.dumps(receipt,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
