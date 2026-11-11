from common import *
import pandas as pd,shutil

def main():
 lines=['# A5增益来源检查（AI分析）','','研究者判断：Unknown。接续R04；主模型冻结，原结果只读。启动A1缓存微差9.91e-6 nat已追溯至既有重算记录，用户明确接受后继续。','', '|检查|问题／一句话结论|预登记规则套用|原始表|','|---|---|---|---|']
 status=[]
 for n in [1,2,3,4,5,6]:
  file=R/f'evidence/check{n}_complete.json';done=file.exists()
  if n in [2,3]:done=(R/'evidence/check23_complete.json').exists()
  txt='尚未完成；按优先顺序执行';rule='NOT_RUN / IN_PROGRESS';tables=[]
  if n==1 and done:
   z=json.load(open(file));txt=f'A0宿主A5提示量{z["delta_A5"]:.6f} nat';rule=z['rule'];tables=['check1_hint_probes.csv','check1a_route_information.csv']
  elif n==2 and done:
   d=pd.read_csv(R/'results/check2_lead_trend.csv');q=d[(d.metric=='EVAL_NLL')&(d.band=='overall')];txt='可观测晚期领先量总体斜率为正；末点仍右删失，不能由nat差缩小断言追平';rule='可见区间未支持持续缩小；完整1000–2000判定不足';tables=['check2_step_lead.csv','check2_lead_trend.csv']
  elif n==3 and done:
   d=pd.read_csv(R/'results/check3_document_bootstrap.csv');z=d[(d.step==2000)&(d.band=='overall')&(d.pair=='A5-A0')].iloc[0];txt=f'A5−A0={z.paired_difference:.6f}，文档95%区间[{z.ci95_low:.6f},{z.ci95_high:.6f}]不跨0';rule='仅固定模型EVAL文档抽样；种子方差Unknown';tables=['check3_document_bootstrap.csv']
  elif n==4 and done:
   z=json.load(open(file));v=z['rows'];txt=f'bias使A5/A1集中度相对改变{v[0]["relative_change"]:.2%}/{v[1]["relative_change"]:.2%}';rule='10% bias干扰分支'+('触发' if z['rule_bias_interference'] else '未触发');tables=['check4_score_bias.csv','check4_concentration_variants.csv','check4_atom_groups.csv','check4_group_top_atoms.csv','check4_group_contexts.csv','check4_A5_A0_spearman.csv']
  elif n==5 and done:
   z=json.load(open(file));c=z['collapsed_group'];txt=f'塌缩层bias改变Top2 {c["bias_changes_top2"]:.2%}，maxgate中位数{c["max_gate_median"]:.5f}';rule='联合阈值'+('满足：soft目标偏离硬路由' if z['rule_soft_hard_bias_driven'] else '未同时满足');tables=['check5_layer_gates.csv','check5_layer_groups.csv','check5_seven_arm_scatter.csv']
  elif n==6 and done:
   z=json.load(open(file));aa=pd.read_csv(R/'results/check6a_readability.csv');bb=pd.read_csv(R/'results/check6b_bootstrap_atoms.csv');l7=aa[(aa.layer==7)&(aa.probe=='mlp_topk64')];txt=f'L7 MLP一致率{l7.exact_set_accuracy.min():.1%}–{l7.exact_set_accuracy.max():.1%}；自举M中位数{bb.Mbar_median.min():.3f}–{bb.Mbar_median.max():.3f}';rule=f'L7>60%配置{int((l7.exact_set_accuracy>.6).sum())}/3；自举M≥1.08配置{int((bb.Mbar_median>=1.08).sum())}/6，<1.01配置{int((bb.Mbar_median<1.01).sum())}/6；10pp规则见check6a_rules.csv';tables=['check6a_readability.csv','check6a_rules.csv','check6b_bootstrap_atoms.csv']
  if n==6 and not done and (R/'evidence/check6a_complete.json').exists():
   aa=pd.read_csv(R/'results/check6a_readability.csv');l7=aa[(aa.layer==7)&(aa.probe=='mlp_topk64')];txt=f'6a完成：L7 MLP一致率{l7.exact_set_accuracy.min():.1%}–{l7.exact_set_accuracy.max():.1%}；6b字典仍在运行';rule='6a阈值见表；6b尚未完成，不代填';tables=['check6a_readability.csv','check6a_rules.csv']
  links='；'.join(f'[{x}]({x})' for x in tables) or '待生成';lines.append(f'|{n}|{txt}|{rule}|{links}|');status.append(dict(check=n,status='COMPLETE' if done else 'PENDING',conclusion=txt,rule=rule,judgment='Unknown'))
 lines+=['','原始CSV保留精度；Markdown表、PNG/PDF图同目录。协议：[protocol_cn.md](protocol_cn.md)；输入微差：[input_gate_trace.csv](input_gate_trace.csv)。','', '探针阴性不等于任何解码器都不能取得提示；观察到的提示量按原阈值判断，仍不单独隔离训练中的因果增益。检查6为时间允许项；未完成项目按状态表保留。所有新训练只更新小探针或小字典，未训练／续训主模型。']
 REPORT.mkdir(parents=True,exist_ok=True)
 for p in (R/'results').iterdir():
  if p.is_file():shutil.copy2(p,REPORT/p.name)
 (REPORT/'README_cn.md').write_text('\n'.join(lines)+'\n');dump(R/'evidence/status.json',status)
if __name__=='__main__':main()
