from common import *
import numpy as np
summary=json.load(open(R/'results/summary.json'));panel=rows(R/'data/panel.jsonl');coverage=list(csv.DictReader(open(R/'results/pattern_coverage.csv')));inter=list(csv.DictReader(open(R/'results/common_intersections.csv')))
def mdtab(headers,rr):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(v) for v in row)+' |' for row in rr])+'\n'
def fmt(x):return 'NA' if x is None else f'{x:.6f}'
def countstr(site,group,sp):return ', '.join(f"#{r['atom']} {r['matches']}/3" for r in coverage if r['site']==site and r['group']==group and r['split']==sp) or '无候选 / no eligible candidates'
def readcsv(p):return list(csv.DictReader(open(p)))
texts=['# S03 24条文本、标签与取样位置\n','P只确定animal，cat/dog为未知；N为chair／非动物。cat/dog原文及完整前缀与S02逐字一致。所有末尾token为` a`，ID=264；索引从0计，括号内从1计。同家族四条件的绝对取样索引也完全一致。\n']
for p in panel:
 texts += [f"## {p['id']} · {p['split']}\n",f"标签：`{json.dumps(p['labels'])}`；cat={p['cat']}，dog={p['dog']}（None表示文本未给定，不是负例）。\n",'完整可见前文：\n\n```text\n'+p['prefix']+'\n```\n',f"目标：`{p['target_token_text']}`；token piece=`{p['target_token_piece']}`；ID={p['target_token_id']}；位置={p['target_index_zero_based']}（{p['target_index_one_based']}）。\n",f"完整token IDs：`{p['token_ids']}`\n"]
(C/'data_casebook_cn.md').write_text('\n'.join(texts))

for site,s in summary.items():
 sel=s['selected'];siteout=C/site;siteout.mkdir(exist_ok=True);parts=[np.load(R/f'cache/{sp}.npz') for sp in ['exploration','heldout_check']];z=np.concatenate([p[site+'__z'] for p in parts]).astype(float);pre=np.concatenate([p[site+'__pre'] for p in parts]).astype(float);dn=parts[0][site+'__decoder_norm'].astype(float);u=z*dn
 case=[f'# {site}：24条全文与逐成员数值\n','本文件按原家族顺序保留全部四条件；F01–03探索，F04–06保留。各表是四条活跃成员的并集，未列出的字典成员在本家族四条中均为0。0指原SAE的ReLU-Top32最终未激活，不意味着preactivation≤0。ID只属于本字典。\n',f"共同候选：{sel['H1_common']}；新增猫候选：{sel['H1_added']['cat']}；新增狗候选：{sel['H1_added']['dog']}；H2：{sel['H2']}。\n"]
 for fi in range(6):
  off=fi*4;fam=f'F{fi+1:02d}';case.append(f'## {fam} · {panel[off]["split"]}\n')
  for p in panel[off:off+4]:
   case.extend([f"### {p['condition']} · {p['labels']}\n",'```text\n'+p['prefix']+'\n```\n',f"token IDs `{p['token_ids']}`；目标` a`，ID264，0起位置{p['target_index_zero_based']}；完整可见前文止于此，没有答案。\n"])
  ids=np.flatnonzero((z[off:off+4]>0).any(0));case.append('### 全部实际成员：原始／加权响应\n')
  case.append(mdtab(['本字典ID','decoder范数','P z / u','cat z / u','dog z / u','N z / u'],[[i,fmt(dn[i])]+[fmt(z[off+j,i])+' / '+fmt(u[off+j,i]) for j in range(4)] for i in ids]))
  ids2=sel['H2'];w=u[off:off+4,ids2];norm=np.linalg.norm(w,axis=1);q=np.divide(w,norm[:,None],out=np.full_like(w,np.nan),where=norm[:,None]>0)
  case.append('### 固定H2成员的相对加权值\n')
  case.append(mdtab(['ID','P q','cat q','dog q','N q','cat−dog'],[[i]+[fmt(q[j,k]) for j in range(4)]+[fmt(q[1,k]-q[2,k])] for k,i in enumerate(ids2)]))
  case.append('此列表的weighted L2：'+', '.join(f'{c}={norm[j]:.6f}' for j,c in enumerate(CONDS))+'。未把这些原始总范数视为已相同。\n')
 failures=readcsv(R/f'results/{site}/pattern_failures.csv');held=[f for f in failures if f['split']=='heldout_check'];first=held[0] if held else failures[0] if failures else None
 case.append('## 不符合固定候选模式的例子\n')
 if first:
  fi=int(first['family'][1:])-1;i=int(first['atom']);case.extend([f"按原家族、原候选顺序取第一条检查失败：{first['family']}，{first['hypothesis']}，#{i}；{first['reason']}。不是从全部数据重新选一个方向。\n",mdtab(['条件','z','decoder范数','u','preactivation'],[[c,fmt(z[fi*4+j,i]),fmt(dn[i]),fmt(u[fi*4+j,i]),fmt(pre[fi*4+j,i])] for j,c in enumerate(CONDS)]),f"该家族全文见上文{first['family']}。所有失败均保留在[失败表](../results/{site}/pattern_failures.csv)。\n"])
 else:case.append('固定候选在本面板中没有失败例；不构造不存在的反例。这不建立总体复现。\n')
 (siteout/'casebook_cn.md').write_text('\n'.join(case))

head='''# S03：动物到猫／狗的共同成员、成员变化与相对强弱

本轮完成24条、两套冻结SAE的描述性探索，候选只来自F01–F03，F04–F06只作固定候选检查。原H1／H2的额外信息与功能作用尚未验证，科学接受及下一步决定等待共同审阅。

本次事实按三条路径阅读：①行为与条件：沿用S02的12/12猫狗续写结果，没有重测或筛掉文本；②表征组织：在同一末尾token分别观察两套原生SAE，下面报告共同／新增／相对强弱；③功能与质量：本轮没有功能干预或probe，原编码等价、hook不改模型及数据冻结检查见核验记录。

## 1. 目的

把“animal→cat/dog”缩成可逐条人工核对的6个家族，先确定现有SAE坐标里实际发生了哪些组合变化。原子只指字典坐标，不预设唯一语义。

## 2. 假设

H1原命题包括共同成员复用及新增成员提供额外细节信息。本轮只检验共同／新增的出现和复现。H2原命题要求成员身份和总幅值受控后的额外细类信息。本轮只描述固定列表上的比例方向，支持集与原始幅值另列。两种变化可以同时出现。

## 3. 实验

6家族×P／猫／狗／N四条件，共24条。P明确animal但猫狗未知；N明确chair。S02原12条前文和分数完整保留。P正文以object指代对象、以animal表类别；N末句用“The object is a”，其余沿用“The animal is a”。这是为保证语法语义自洽而保留的实际差异。没有只改类别词的严格P/N对照，后缀本身可以引起差异。

同一冻结Qwen3-0.6B Base/tokenizer；全体在最后可见token ` a`（ID264）处取样，不含答案；同家族四条件连绝对索引也相同。ATTN_SAE读取block27的o_proj输出、残差相加前；MLPIN_SAE读取block27实际MLP输入，已经过残差相加及post_attention_layernorm。两者分别用自己的30000维字典，原规则ReLU-Top32，无额外输入归一化或减decoder偏置。它们不是MLP输入输出的因果对照。

原始激活z、自己的decoder列范数d、加权响应u=z×d同时保存。u度量单个解码方向的幅值；方向非正交，不能把它当作对模型输出的语义贡献。相对值是在固定列表内分别做z或u的L2归一化，零范数不可定义。两套字典当前decoder范数都很接近1，原始与加权图接近是正常的。

候选规则在运行前写定，见[协议](protocol_cn.md)。探索覆盖至少2/3，最多每组6个。共同候选须P／猫／狗均正且相对N更强；新增候选须P为0、相应细类为正；H2按猫狗共同覆盖、共同强度排序，不按差异挑最漂亮的成员。候选和H2探索方向冻结后才读取保留家族。

## 4. 分析

表中的“3/3”是3个家族均出现，不是统计显著。每个ID在保留家族中的表现都报告，未据此重选。完整[24条文本与token](data_casebook_cn.md)、[成员转换数值](results/member_transition_values.csv)、[覆盖计数](results/pattern_coverage.csv)可核对。
'''
en='''# S03: animal-to-cat/dog membership and relative response

Completed bounded descriptive analysis of24rows and two independently encoded frozen SAEs. Scientific acceptance and next decision remain pending joint review. Behavior: S02's original12/12 continuation result is retained without rescoring. Representation: fixed exploration candidates are checked on three other families below. Function/quality: no intervention or probe was run; native-rule equivalence, hook no-op, immutable provenance and arithmetic are verified.

Purpose: inspect common members, genuine native-support transitions and relative responses for explicit animal/cat/dog content. H1's original incremental-information claim and H2's identity-and-scale-controlled extra-information claim remain unchanged and untested functionally.

Six families, P/cat/dog/N, 24texts. P gives animal, fine category unknown, not a cat/dog negative. N gives chair. Original12cat/dogtexts/prefixes/scores are untouched. P uses object as referent; N necessarily changes suffix animal to object. These lexical/suffix confounds remain. All rows observe the final visible ' a' token, ID264; within-family absolute positions also match. No generated token is used.

Same official frozen0.6BBase/tokenizer as S02. ATTN is block27 o_proj before residual addition; MLPIN is actual block27 mlp input after residual addition and post_attention_layernorm. Native linear+ReLU+Top32 rules, 30000atoms, no extra SAE input normalization or decoder-bias subtraction. The sites are separate dictionary observations, not an MLP input/output causal comparison. z is raw activation; u=z times own decoder-column norm. Selected-list L2 normalization yields q; zero norm is undefined. Decoder norms are near1 in both saved dictionaries, so raw/weighted values nearly coincide.

Freeze F01-03 exploration/F04-06 check, coverage threshold2/3 and maximum6 per group before responses. H1 common requires triple support and min_PCD> N in weighted response; H1 added is zeroP/positive fine, not necessarily unique to that fine category. H2 uses cat/dog coactivation coverage then common magnitude, not contrast. Exact candidates/directions freeze before any check response exists. All check outcomes, not just attractive examples, are retained.
'''
rowgroups=[]
for site,s in summary.items():
 sel=s['selected'];title='Attention输出SAE' if site=='ATTN_SAE' else 'MLP输入SAE';h1tab=[[str(i),next(r['ratio'] for r in coverage if r['site']==site and r['group']=='H1_common' and r['atom']==str(i) and r['split']=='exploration'),next(r['ratio'] for r in coverage if r['site']==site and r['group']=='H1_common' and r['atom']==str(i) and r['split']=='heldout_check')] for i in sel['H1_common']]
 h2tab=[[str(i),sel['H2_discovery_direction'][str(i)],next(r['ratio'] for r in coverage if r['site']==site and r['group']=='H2' and r['atom']==str(i) and r['split']=='exploration'),next(r['ratio'] for r in coverage if r['site']==site and r['group']=='H2' and r['atom']==str(i) and r['split']=='heldout_check')] for i in sel['H2']]
 head+=f'\n### {title}：H1\n\n共同候选的完整条件（共同为正且相对N更强）覆盖：\n\n'+mdtab(['本字典ID','探索','保留检查'],h1tab)
 head+='\n细类新增（P=0、细类>0）的逐候选覆盖：\n\n'+mdtab(['条件','探索','保留检查'],[[label,countstr(site,'H1_added_'+label,'exploration'),countstr(site,'H1_added_'+label,'heldout_check')] for label in ['cat','dog']])
 commonadded=set(sel['H1_added']['cat'])&set(sel['H1_added']['dog']);head+=f'\n猫狗新增列表相交{len(commonadded)}个：`{sorted(commonadded)}`。这些候选在探索中同时相对P新增，不能仅凭入选名称解释成猫／狗专属特征。\n'
 tt=readcsv(R/f'results/{site}/transitions.csv');head+='\n每家族的真实成员变化（保留／新增／消失，各自分母完整列在原表；每条原生支持数均32）：\n\n'+mdtab(['家族／分组','P／猫／狗共同 / P','P→猫 保留/新增/消失','P→狗 保留/新增/消失'],[[f'F{fi+1:02d} '+('探索' if fi<3 else '保留'),next(r['PCD_common_over_P'] for r in inter if r['site']==site and r['family']==f'F{fi+1:02d}')]+['/'.join(next(t[k] for t in tt if t['family']==f'F{fi+1:02d}' and t['source']=='P' and t['destination']==label) for k in ['retained','zero_to_positive','positive_to_zero']) for label in ['cat','dog']] for fi in range(6)])
 head+=f'\n![{site}成员转换](figures/{site}_H1_transitions.png)\n\n绿为P中已有并保留到细类的成员，黄为P中0→细类正，柱上标P中消失数；横轴前三为探索、后三为检查。新增数量不是新增辨别信息。\n\n![{site}共同候选热图](figures/{site}_H1_common.png)\n\n共同候选按探索顺序固定。四图依次给原始z、加权u和各自固定列表L2归一化值；数值写在格内，红线分开探索与保留，颜色尺度各图独立，灰色为不可定义。N后缀含object差异仍在。\n'
 head+=f'\n### {title}：H2\n\n探索平均相对加权差的正号指cat较强，负号指dog较强。下面是每个固定方向的逐家族一致数：\n\n'+mdtab(['本字典ID','冻结方向','探索同向','保留同向'],h2tab)
 pairs=s['same_support_pairs'];head+='\n成员身份和原幅值另列，不能用归一化替代这些事实：\n\n'+mdtab(['家族','全字典支持完全相同','固定6成员支持相同','猫/狗固定列表原加权L2','同向成员/有方向成员'],[[p['family'],p['full_support_equal'],p['H2_selected_support_equal'],f"{p['cat_selected_weighted_L2']:.5f} / {p['dog_selected_weighted_L2']:.5f}",f"{p['direction_matches']}/{p['direction_defined']}"] for p in pairs])
 head+=f'\n全字典支持完全相同{s["full_support_equal_pairs"]}/6对；选定列表内支持相同{s["selected_support_equal_pairs"]}/6对。只对后者可说观察的是同一固定列表内的比例，不能据此声称整套字典身份已受控。H2零范数样本{s["zero_norm_H2_samples"]}/24。\n\n![{site}H2共同成员热图](figures/{site}_H2_joint.png)\n\n四图与H1图使用相同读法。原始总幅度在上表保留，方向只取自探索，不因检查的反向结果修改。完整原始比例、cat/dog比值及每对方向见[H2逐对表](results/{site}/H2_directions.csv)。\n\n[F01完整四条全文、全部成员数值和每个保留家族]( {site}/casebook_cn.md) · [全部未复现模式](results/{site}/pattern_failures.csv)。\n'
 en+=f'\n## {site}\n\nH1 common check coverage: {countstr(site,"H1_common","heldout_check")}.\n\nH1 newly active cat check: {countstr(site,"H1_added_cat","heldout_check")}.\n\nH1 newly active dog check: {countstr(site,"H1_added_dog","heldout_check")}.\n\nH2 fixed weighted-relative direction check: {countstr(site,"H2","heldout_check")}.\n\nWhole-support identical pairs{s["full_support_equal_pairs"]}/6; selected-list identical support{s["selected_support_equal_pairs"]}/6. Selected norms are not equal; see all norms in H2_pairs.csv. Zero norms{s["zero_norm_H2_samples"]}/24. Every failure and all24full prefixes/member values appear in the Chinese casebook and machine-readable tables; these retain exact raw numbers.\n'
 rowgroups.append([site,len(sel['H1_common']),len(sel['H1_added']['cat']),len(sel['H1_added']['dog']),len(sel['H2']),s['full_support_equal_pairs'],s['selected_support_equal_pairs']])
head+='''
## 5. 结论与认识更新

**H1：**本轮可以确认这些字典里存在P／细类共同激活、成员0→正、正→0及已有成员强弱变化；这些是不同的可观察事实，不能用“变强”替代“新增”。候选在保留家族的覆盖如上，失败候选均保留。较弱判断是部分响应组织可以随这批明确词语复现。新增是否提供额外细类信息仍未检验：没有同预算随机成员比较、固定读出或干预。共同对照受animal/object及后缀差异影响；cat/dog正文还有词面复述解释。

**H2：**在探索选出的固定列表上，可以直接检查同一成员的比例变化，并看哪些方向跨3个保留家族保持、哪些反向。选定列表身份相同的配对与全字典身份相同的配对是两件事。归一化去掉列表标量尺度，仍未控制其他成员、完整表征、所有总幅度或证明额外预测信息；也没有在概念不变时改变措辞的专门对照。

**认识更新：**当前可把“成员换入换出”和“固定列表内重新分配响应”拆成可逐条核对的现象，并用未参与选候选的家族看到各自的复现与失败；粗细概念是否通过这些变化获得额外信息，仍是下一次共同审阅要判断的问题。原H1／H2不作修订。

已排除的解释仅限记录范围：12条旧文本不是预测后筛选或改写，保留家族未用于选候选，单一家族的取样位置／目标token未变，hook未改变前向，SAE参数未训练。仍保留词面复制、固定后缀、object/animal指代差异、句式上下文、Top32竞争、字典局部坐标及重建误差。所有样本只覆盖6种短英文句式，N只有chair，不能概括非动物总体。字典重建相对L2误差见Detailed，较大误差进一步限制“完整概念”的解释。

**AI建议（未执行）：**先共同审阅完整F01与失败表，决定当前这些词面与后缀差异是否允许继续解释候选。保持概念的改写、同预算对照或受控干预都等待研究者决定。

本轮完成后停止。没有扩数据、H3／H4、CrossCoder、probe、消融、训练或后续实验。科学接受、机制判断及下一步决定为Unknown。

[协议](protocol_cn.md) · [完整24条与token](data_casebook_cn.md) · [Detailed](detailed_cn.md) · [原始数组](cache/) · [核验](evidence/verification.json)
'''
en+='''
## Bounded interpretation and stop

H1: actual native support transitions and recurring shared-response candidates are directly observed, with all check failures retained. Strengthening already active members is not new membership. Many additions can occur in both fine conditions. No budget-matched random-addition comparison or incremental functional information was tested. Common-response specificity is confounded by animal/object and suffix differences.

H2: fixed-list relative response directions can recur or reverse across check families. Selected-list support equality differs from whole-dictionary support equality. Normalizing selected vectors removes one scalar scale, not all amplitude or identity confounds, and does not establish extra predictive information. No concept-preserving paraphrase control or causal test was run.

Recognition update: membership recruitment/loss and redistribution within a fixed list are now separately auditable, including their cross-family failures. Whether they supply additional fine-concept information remains untested. Original hypotheses stay unchanged. Explicit word copying, suffix/referent differences, context, Top32 competition, dictionary dependence and reconstruction error remain competitors. Six short English families and one chair control do not establish population generality. AI suggestion, not run: review F01 and all failed patterns together before choosing any next step.

STOP_WAIT_FOR_JOINT_REVIEW. No H3/H4, training, probe, ablation, CrossCoder or automatic follow-up. Data/code/cache copies have execution ownership and payload hashes; no commit/push/publication.
'''
(C/'summary_cn.md').write_text(head.replace(']( ',']('));(C/'summary.md').write_text(en)
ver=json.load(open(R/'evidence/verification.json'));captures=[json.load(open(R/f'evidence/capture_{sp}.json')) for sp in ['exploration','heldout_check']]
dt=['# S03 执行、读法与核验\n','数据、筛选与止步规则见[冻结协议](protocol_cn.md)和[frozen_plan](frozen_plan.json)。H1/H2原命题及旧结果未修改；本轮直接用户指令是执行授权来源，运行完成不代表科学接受。\n',f"探索完成{captures[0]['UTC']}；候选冻结{json.load(open(R/'evidence/candidates_frozen_before_heldout.json'))['UTC']}；保留完成{captures[1]['UTC']}。CPU推理分别{captures[0]['elapsed_seconds']:.2f}/{captures[1]['elapsed_seconds']:.2f}秒，FP32两线程，固定物理4×192；每阶段额外一次无hook对照，最大差为0。没有生成答案或LM-head行为重测。\n",f"输入模型权重SHA `{captures[0]['input_model_SHA256'][str(Path(json.load(open(R/'frozen_plan.json'))['model'])/'model.safetensors')]}`；与S02一致。原生loader、SAE权重哈希和hook见两个capture收据。\n"]
for site,s in summary.items():
 err=np.array(s['reconstruction_relative_L2']);dt += [f'## {site}\n',f"重建相对L2误差定义||h-decoder(z)||2/||h||2，24条中最小／中位／最大={err.min():.6f}/{np.median(err):.6f}/{err.max():.6f}。这是该hook单点的近似误差，不作跨接口质量排名。\n",f"decoder范数范围{ver['sites'][site]['min_decoder_norm']:.9f}至{ver['sites'][site]['max_decoder_norm']:.9f}；最小Top32第32与33值差{ver['sites'][site]['min_Top32_positive_margin']:.9f}，边界精确并列{ver['sites'][site]['Top32_boundary_ties']}。原生激活都是32个，不是人为阈值筛成32。新成员可能来自Top32竞争；完整preactivation也保存。\n",f"[全部24条全文与全部活跃ID/数值]({site}/casebook_cn.md) · [全部候选值](results/{site}/candidate_values.csv) · [成员转换](results/{site}/transitions.csv) · [H2同支持配对](results/{site}/H2_pairs.csv)。\n"]
dt += ['## 完成范围与原始记录\n',mdtab(['接口','共同候选','猫新增','狗新增','H2候选','全支持相同/6','列表支持相同/6'],rowgroups),f"保留旧S01/S02文件{ver['old_files_unchanged']}个，哈希全部相同。24条输入token重放，{ver['replayed_transition_rows']}条转换计数、{ver['replayed_H2_differences']}条H2差值、{ver['replayed_candidate_values']}个候选加权数值独立复核通过。数据标签、目标token与位置、候选门控和编码规则均通过；这些是实现有效性，不是原H1/H2的科学确认。\n",'data为24条加旧12条及原分数；cache的两个NPZ含ID、h、最终z、完整preactivation、32/33阈值、decoder范数和重建误差；results含共同/新增/消失逐原子事件、探索排序、固定候选四条件值、归一化、全部失败与分组覆盖；figures含两接口各3幅。code保留实际脚本；evidence保存冻结、捕获、检查和交付收据。归一化是候选向量内的计算；总幅度及原始值始终可取回。\n','## 覆盖台账\n','| 项目 | 状态 | 边界 |\n|---|---|---|\n| 数据和旧结果保留 | DONE_VALID | 24条，旧12条不变 |\n| 两套原生SAE与位置 | DONE_VALID | 冻结，CPU，无后续token |\n| H1共同/新增/强度与检查 | DONE_EXPLORATORY | 6家族，未测额外信息 |\n| H2比例/同支持/方向与检查 | DONE_EXPLORATORY | 未测额外预测信息 |\n| 图、完整例、失败例、核验 | DONE_VALID | 仅当前受控数据 |\n| H3/H4/训练/probe/干预 | NOT_RUN_BY_SCOPE | 用户要求停止 |\n| 科学接受、下一步决定 | Unknown | 等待共同审阅 |\n']
(C/'detailed_cn.md').write_text('\n'.join(dt))
(C/'detailed.md').write_text('# S03 execution record\n\nTwo sequential12-row captures, exploration then heldout only after candidate/direction freeze. CPU FP32, two threads,4x192physical shape; one no-hook forward per stage had exact zero difference. Native original loaders agree with raw linear/ReLU/Top32 implementation. All parameters frozen. No generated answers, learning, extra prompts or H3/H4.\n\n[Exact machine-readable checks](evidence/verification.json), [exploration receipt](evidence/capture_exploration.json), [heldout receipt](evidence/capture_heldout_check.json), [full numeric execution explanation](detailed_cn.md), [frozen plan](frozen_plan.json) and [Summary](summary.md) retain setup, hashes, per-site decoder norms, reconstruction errors, every failure and claim limits. Original S01/S02 files are hash-unchanged. Scientific acceptance and next decision remain Unknown.\n')
(C/'README.md').write_text('''# S03 · animal / cat / dog · H1 / H2

[中文小结](summary_cn.md) · [English Summary](summary.md) · [24条全文/token](data_casebook_cn.md) · [Attention全部成员与失败例](ATTN_SAE/casebook_cn.md) · [MLP输入全部成员与失败例](MLPIN_SAE/casebook_cn.md) · [冻结协议](protocol_cn.md) · [执行和核验](detailed_cn.md)

Read Summary first, then F01 and every check failure. All scripts, texts, arrays, tables and figures are included as requested. The execution directory is the sole source for generated payloads; copies here are byte-verified reading material. Payload_manifest records exact provenance. No model/SAE checkpoint is included.

Only this24-row descriptive step is complete. Original H1/H2 additional-information claims are not functionally tested; scientific acceptance/next decision remain Unknown. STOP_WAIT_FOR_JOINT_REVIEW.
''')
print('REPORTS_WRITTEN',flush=True)
