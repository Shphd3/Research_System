from pathlib import Path
import json,pandas as pd,numpy as np
E=Path(__file__).resolve().parents[1];P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response')/E.name
TR={
'biology_05':('细胞结构：核糖体／溶酶体','细胞内一个专门部分执行一项生化任务。',[
('这个结构读取信使核苷酸序列，把氨基酸连接成蛋白质。','这个膜包围的区室用酸性消化酶分解衰老的细胞材料。'),
('转运分子将氨基酸运来，通过肽键延长蛋白链。','受损的细胞组分进入这个酸性区室，被水解酶拆解。')],'读取信使、连接氨基酸指向核糖体；酸性区室、水解旧材料指向溶酶体。两者同属细胞结构，与错误上位“动物组织”不同。'),
'biology_06':('血细胞：红细胞／白细胞','一种细胞在脊椎动物血液中循环。',[
('这种成熟的人类细胞没有细胞核，靠血红蛋白携氧。','这种有核细胞在脊椎动物体内循环，参与防御感染因子。'),
('双凹外形和大量血红蛋白有助于向组织输送氧气。','它能离开小血管，作为免疫防御的一部分对付入侵微生物。')],'无核、血红蛋白携氧与有核、免疫防御构成辨别线索；不能仅根据“血液”一词完成同层区别。'),
'mathematics_05':('圆锥曲线：椭圆／双曲线','一个平面与圆锥相交形成曲线。',[
('闭合曲线上每一点到两个固定焦点的距离之和不变。','双分支曲线上每一点到两焦点的距离差的绝对值不变。'),
('点围绕两个焦点分布，并保持到两焦点的总距离固定。','两条不相连的分支逼近直线渐近线，且焦距差固定。')],'距离和固定指椭圆，距离差绝对值固定指双曲线；闭合／双分支是额外相容线索，不能断言模型只用了距离关系。'),
'mathematics_06':('函数：指数函数／对数函数','一个固定数学规则为每个输入恰好指定一个输出。',[
('输入位于固定正底数的指数位置，底数不等于一。','输出给出固定底数需要取多大指数才能得到正输入。'),
('输入等量增加时，输出总被同一个正因子相乘。','它是固定正底数的变指数幂运算的反函数。')],'输入作为指数与输出返回指数是不同关系；第二措辞也使用乘法增长与反函数定义。不能由两个答案的词频或片段长度替代这条关系。'),
'physics_05':('力：摩擦力／浮力','某种相互作用推或拉物体，并能改变其运动。',[
('滑动接触时，这种切向相互作用反抗表面的相对运动。','流体压差造成向上推动，其大小等于排开流体的重量。'),
('两个固体表面相互摩擦，产生阻碍滑动的切向作用。','浸入的物体因底部流体压强更大而受到净向上推动。')],'接触、切向阻力指摩擦力；流体上下压差、排开流体重量指浮力。不是任意两个术语的标签匹配。'),
'physics_06':('传热方式：热传导／热对流','热能从较热区域移向较冷区域。',[
('能量通过静止固体中的微观相互作用传递，没有材料整体流动。','能量由冷热流体的整体循环携带。'),
('金属棒的材料留在原位，热能却沿棒传播。','热液上升、冷液下沉，将热能带遍容器。')],'无宏观物质流动与有流体整体运动构成辨别关系。金属／液体也是相关线索，当前没有干预或词面控制将它们彼此分开。')}
def md(df):return df.to_markdown(index=False,floatfmt='.5f')
def main():
 R=[json.loads(l) for l in (E/'data/prefixes.jsonl').read_text().splitlines()];F=pd.read_csv(E/'analysis/family_metrics.csv');D=pd.read_csv(E/'analysis/prefix_scores.csv.gz');C=pd.read_csv(E/'analysis/candidate_sequence_scores.csv.gz');T=pd.read_csv(E/'analysis/paraphrase_metrics.csv');M=pd.read_csv(E/'analysis/representative_member_responses.csv');cfg=json.load(open(E/'config.json'));evalF=F[(F.condition=='full')&(F.split=='evaluation')].set_index('family_id');high=F[(F.condition=='feature_delete_high')&(F.split=='evaluation')].set_index('family_id');loss=(evalF.J-high.J).sort_index();chosen=[('最大恶化',loss.idxmax()),('最大改善／最小损失',loss.idxmin()),('最接近无变化',loss.abs().idxmin())];out=['# R14：完整自然语言与原始评分精读','\n固定展示家族为每域05、06，共六家族，结果之前指定。后面的三例明确按高频删除的家族平均区分量变化选择，不是代表性样本。所有句号均参与候选评分，未评分结束符；概率是完整带空格答案加句号的序列概率。','\n`文字片段编号`是词表编号，不是频率、重要性或排名。候选由多个片段组成时，必须合并全部片段分数。模型在每个位置只读可见前文与之前已给出的候选片段。','\n对数概率越大表示该完整候选更受偏好。r为第一个具体概念减第二个；指向第一个的前文期望r>0，指向第二个期望r<0。上位差为正确上位减错误上位；与r不是同一个任务，不比较绝对降幅。']
 def append_case(fid,selection):
  rr=[r for r in R if r['family_id']==fid];base=rr[0];out.extend([f'\n## {fid}：{TR[fid][0] if fid in TR else base["A"]+" / "+base["B"]}',f'\n选择方式：{selection}。上位概念：{base["U"]}；错误上位：{base["V"]}。具体概念：{base["A"]}／{base["B"]}。','\n来源：'+', '.join(f'[{u.split("/")[-1]}]({u})' for u in base['sources'])])
  if fid in TR:out.append('\n辨别关系与边界：'+TR[fid][3])
  for pi in [0,1]:
   out.append(f'\n### 措辞{pi+1}：完整模型前文')
   for ct in ['broad','A','B']:
    r=next(x for x in rr if x['paraphrase_id']==pi and x['context_type']==ct);out.append(f'\n**{ct}前文**\n\n```text\n{r["prefix"]}\n```')
    if fid in TR:out.append('\n中文释义：'+(TR[fid][1] if ct=='broad' else TR[fid][2][pi][0 if ct=='A' else 1]))
   names=['full','keep_head16','feature_delete_low','feature_delete_middle','feature_delete_high','feature_normmatch_high_11021'] if pi==0 else ['full','feature_delete_high']
   q=D[(D.family_id==fid)&(D.paraphrase_id==pi)&D.condition.isin(names)][['condition','context_type','L_A','L_B','L_U','L_V','r','upper_margin']].copy();out.extend(['\n### 原始完整候选分数（自然对数单位）',md(q)])
   q=T[(T.family_id==fid)&(T.paraphrase_id==pi)&T.condition.isin(names)][['condition','r0','rA','rB','gA','gB','J','specific_correct','both_correct','upper_both_cues']];out.extend(['\n宽泛偏好与双侧线索增益：',md(q)])
  out.append('\n### 完整候选及分词边界')
  for k,a in base['candidate_map'].items():out.append(f'- {k}：`{a["answer"]}`，文字片段编号{a["token_ids"]}；片段{a["token_fragments"]}；共{a["length"]}片段（包括句号）。')
  out.append('\n### 第一措辞的关键逐片段概率：完整模型与高频删除')
  for ct in ['broad','A','B']:
   r=next(x for x in rr if x['paraphrase_id']==0 and x['context_type']==ct);q=C[(C.prefix_id==r['prefix_id'])&C.condition.isin(['full','feature_delete_high'])&C.candidate.isin(['A','B'])]
   for _,a in q.iterrows():
    lp=json.loads(a.per_token_log_probability);fr=r['candidate_map'][a.candidate]['token_fragments'];out.append(f'\n{ct}前文／{a.condition}／`{a.text}`：完整候选概率={a.sequence_probability:.8g}；逐片段'+', '.join(f'`{f}`:{v:.6f}（概率{np.exp(v):.6g}）' for f,v in zip(fr,lp))+f'；求和={sum(lp):.6f}。')
  if fid in set(M.family_id):
   out.append('\n### 对应成员的出现、响应强弱与独立参考频率')
   out.append('\n成员在本家族按预先规则选：每组跨两措辞的|A线索响应−B线索响应|×最后层解码向量范数最大两名，另附符合原规则且确有非零响应的低差异成员；找不到则记为未找到，不拿全零成员冒充高响应反例。它是响应诊断，不是成员功能命名，也没有单成员删除。零响应反例保留。')
   q=M[M.family_id==fid];entries=[]
   for (g,j),a in q.groupby(['group','feature_number']):
    p=a.pivot(index='paraphrase_id',columns='context_type',values='coefficient');entries.append({'频率组':g,'成员编号':j,'参考出现次数/65536':int(a.reference_hits.iloc[0]),'宽泛响应1':p.loc[0,'broad'],'A线索响应1':p.loc[0,'A'],'B线索响应1':p.loc[0,'B'],'A线索响应2':p.loc[1,'A'],'B线索响应2':p.loc[1,'B'],'选择规则':a.selection.iloc[0]})
   out.append(md(pd.DataFrame(entries)))
 for fid in cfg['fixed_families']:append_case(fid,'结果前固定')
 for typ,fid in chosen:append_case(fid,'结果后诊断选择：'+typ+f'，完整减高频删除的家族平均区分量={loss.loc[fid]:.6f}')
 out.append('\n## 所有概念家族的结果与失败\n')
 q=evalF[['domain','J','specific_correct','both_correct','upper_correct']].copy();q['高频删除后的J']=high.J;q['高频删除损失']=loss;q=q.reset_index();out.append(md(q));out.append('\n全部288条前文、四候选、所有条件的逐片段分数在执行目录 data/prefixes.jsonl 与 analysis/candidate_token_logprob.csv.gz；本页没有替换或筛除任何完整模型失败家族。')
 text='\n'.join(out)+'\n';(E/'casebook_cn.md').write_text(text);(P/'casebook_cn.md').write_text(text)
 selections={'fixed_families':cfg['fixed_families'],'diagnostic_metric':'fullJ minus high_frequency_deletedJ;family averaged','diagnostic_cases':chosen};(E/'analysis/case_selection.json').write_text(json.dumps(selections,ensure_ascii=False,indent=2)+'\n');print('CASEBOOK',len(text),'characters')
if __name__=='__main__':main()
