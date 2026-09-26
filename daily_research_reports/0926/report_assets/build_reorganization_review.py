"""Build derived maps after reviewed text revisions; never mutate source records."""
from pathlib import Path
import csv
import hashlib
import json
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs'
DATE = ROOT / 'daily_research_reports/0926'
ATLAS = DATE / 'report_assets/anchor_atlas_data.json'
rows = json.loads(ATLAS.read_text())['rows']
by_index = {r['index']: r for r in rows}
revision_path = DATE / 'report_assets/reasoning_anchor_revisions_20260926.json'
revisions = json.loads(revision_path.read_text())
revised_paths = {r['path']:r for r in revisions}

# Reading families, not a new scientific hierarchy or a selection of active workstreams.
lines = [
 (1, '共同性与功能分工的判定', '先定义：什么才算共同方向、专家不同且确实有用？', [11,0,1,2,15,16,14], 'A01_01–03；A06_00、03、04', '定义与判据'),
 (2, '路由锁定与分工形成', '为什么早期分路会被保留，什么过程阻碍功能分工？', [4,7,9,10,3,5,6,8,12,13,60,61,62], 'A02、A05；A01_04；A06_01–02；A15_01', '形成机制'),
 (3, '共享更新、优化与干扰', '一次更新何时帮助或伤害另一目标，哪些优化过程造成差异？', list(range(17,24))+[26,27,116,117,118,121,122,123], 'A07、A10、A16_00；0924/0925 三份草案', '更新机制'),
 (4, '监督信号与任务必要性', '更早的任务相关监督，何时真正改变后续答案计算？', list(range(28,48)), 'A11、A12、A13', '监督机制'),
 (5, '频率、复用与低维结构', '低维结构来自频率、函数复用，还是构造中的先验假设？', [24,25,48,49,50,53,54,55,51,52], 'A04、A09、A14', '结构解释'),
 (6, '表征结构与测量边界', '哪些层、谱位置、方向和长度差异可以稳定测到？', list(range(56,60))+list(range(63,72))+[92,93,109,115], 'A15_00、02、04、09、14；旧 03', '描述与测量'),
 (7, '信息增量、使用与迁移', '额外可读的信息有多少，能否被使用或迁移？', list(range(81,92))+[94,96,111], 'A15_07、08、10、12、16', '信息与功能'),
 (8, '稀疏自编码约束与表征变化', 'SAE 条件下，集中和复用变化伴随什么信息变化？', [112,113,114], 'A15_17 及两个子问题', '约束与表征'),
 (9, '表征坐标驱动的路由方法', '谱带、接力和增量坐标，是否有超出匹配对照的分流价值？', list(range(72,81))+[119,120], 'A15_05、06；A16_01', '方法比较'),
 (10, '语义与效用监督的路由方法', '指定分组的价值能否变成可学习的路由和专家结构？', [95]+list(range(97,109))+[110], 'A15_11、13、15', '方法比较'),
]

parent = {16:15,29:28,31:30,33:32,34:32,36:35,38:37,53:50,54:50,82:81,93:92,113:112,114:112,117:116,118:116,120:119}
for p, children in [(41,range(42,48)),(56,range(57,60)),(60,range(61,63)),(63,range(64,71)),(72,range(73,78)),(78,range(79,81)),(83,range(84,92)),(97,range(98,109))]:
    parent.update({c:p for c in children})
archived = {51,52,115}
drafts = {121,122,123}
mapped = []
numbers = {}
for number, title, question, indices, old, kind in lines:
    p_count = 0
    c_count = {}
    for idx in indices:
        r = by_index[idx]
        source = Path(r['anchor_path'])
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != r['anchor_sha256']:
            reviewed = revised_paths.get(str(source))
            if not reviewed or reviewed['before_sha256'] != r['anchor_sha256'] or reviewed['after_sha256'] != digest:
                raise RuntimeError(f'Unreviewed source change since reading: {source}')
        if idx in archived:
            new = None
            role = '已归档历史；保留原历史标识'
        elif idx in parent:
            p = parent[idx]
            c_count[p] = c_count.get(p,0)+1
            new = f'{numbers[p]}.{c_count[p]}'
            role = '原有子 Anchor；不因重编号升级为独立课题'
        else:
            p_count += 1
            new = f'{number}.{p_count}'
            role = '未归属日期草案；新归属和编号仍待研究者确认，不覆盖已有执行授权' if idx in drafts else '现存非归档父级/平铺 Anchor；不表示当前活跃'
        numbers[idx] = new
        mapped.append({
            'source_inventory_index':idx, 'proposed_line_number':number,
            'proposed_line_title':title, 'proposed_display_number':new,
            'proposed_id_prefix': '_'.join(f'{int(n):02}' for n in new.split('.')) if new else None,
            'legacy_id':r['id'], 'source_path':str(source), 'source_sha256':digest,
            'pre_revision_atlas_source_sha256':r['anchor_sha256'],
            'existing_parent_source_path':by_index[parent[idx]]['anchor_path'] if idx in parent else None,
            'role':role, 'question':r['question'],
            'evidence_reading_from_atlas':r['evidence'],
            'knowledge_update_AI_DRAFT':r['update_draft'],
            'human_decision':None,
        })

assert len(mapped)==124 and len({r['source_path'] for r in mapped})==124
assert {r['source_inventory_index'] for r in mapped}==set(range(124))
assert len({r['proposed_display_number'] for r in mapped if r['proposed_display_number']})==121

def rel_link(path, label, line=None):
    p = Path(path)
    relative = '../'+str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    return f'[{label}](<{relative}{":"+str(line) if line else ""}>)'

def anchor(idx):
    return rel_link(by_index[idx]['anchor_path'], by_index[idx]['id'])

def numbered(idx):
    return numbers[idx] or '历史'

E08 = ROOT/'Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation'
e01=E08/'A15_08_E01_layer25_conditional_innovation_matrix/summary.md'
e02=E08/'A15_08_E02_fresh_balanced_mismatch_repair/summary.md'
e03=E08/'A15_08_E03_fresh_confirmation_freeze_repair/summary.md'
e04=E08/'A15_08_E04_strict_conformance_repair/summary.md'

findings = [
 {'id':'L1','indices':[21],'kind':'逻辑命题过强；不是整条线无效',
  'problem':'把“共享有害”限定为必须存在负梯度夹角；同时用冲突降低与损失改善共同发生来支持因果中介。',
  'evidence':'Anchor 第 34–36、52–54、167 行。有限步长下，即使梯度同向，源目标更新也可能越过另一目标最优点而伤害它。',
  'rival':'有限步长、曲率、容量或其他优化变化造成代价；负夹角只是某些条件下的一阶指标。',
  'repair':'删去无条件 only when；把实际独立目标损失变化作为互害证据，将梯度指标限定为局部预测；已有结果保留。',
  'minimal_separator':'从同一状态做源目标更新，固定更新范数/步长规则并读取独立目标；要归因冲突还须让候选冲突过程相对对照单独改变。'},
 {'id':'L2','indices':[41,46],'kind':'必要条件与交互证据混用',
  'problem':'父 Anchor 说辅助监督仅在中继为必要路径时才有效；当前结果建立的是受控条件下更大的相对收益。',
  'evidence':'父 Anchor 第 27–29、41–43 行为 only when，第 204 行则称 controlled sufficient condition；中继 0.2315、绕过 0.0181、交互 0.2134。',
  'rival':'必要性放大收益，但非必要时仍可通过优化或其他学习路径带来小收益。',
  'repair':'把主张收窄为已测任务相关性×必要性条件下的收益差；不把交互为正当作普遍必要性。保留 A13_00_05 的有效实验。',
  'minimal_separator':'先用已有中继/绕过的匹配对照裁决交互；若继续主张必要性，必须明确非必要条件的收益界与反例判据。'},
 {'id':'L3','indices':[75],'kind':'机制比较同时改变两个关键因素',
  'problem':'用浅层接力与深层本地坐标的胜负区分“稳定性”与“新增信息”；两者在这组比较中一起变化。',
  'evidence':'Anchor 第 21、26、34–41 行；第 64 行还明确没有等维随机调度训练对照。',
  'rival':'信息来源、瓶颈或一般正则作用，而非稳定性本身解释方法差异。',
  'repair':'保留该实验的有界方法比较，删除从这组胜负单独确定稳定性机制的推断；停止原封不动重复头—中—尾排程。',
  'minimal_separator':'若仍有独立理由研究稳定性，固定信息来源和维数再比较坐标运动；先问能否构造这种独立操纵，不能就保留机制未知。'},
 {'id':'L4','indices':[78],'kind':'方法成败裁决了过多机制命题',
  'problem':'把接力方法最终损失不胜出写成全部物理先验为假；把胜出预先归因于跨层漂移减少。',
  'evidence':'Anchor 第 40–41、46–47 行；第 125–129 行却分别记录平滑追踪通过、接力终点收益不支持。',
  'rival':'追踪确实有效，但信息来源或瓶颈代价抵消其作用；也可能收益只来自中心化。',
  'repair':'删除一揽子先验否决与未经隔离的 because；分开追踪、谱身份、接力收益三条结论。保留随机匹配对照和负结果。',
  'minimal_separator':'优先采用已有运动匹配随机对照收束谱身份主张；工程追踪效果不能直接用终点质量反推真伪。'},
 {'id':'L5','indices':[86],'kind':'问题过载；不等于数据失效',
  'problem':'声称只有一个条件问题，却同时要求回答新增信息、参数谱位置、秩、层深和 token 几何。',
  'evidence':'Anchor 第 20–26 行。其注册对照与边界已有明确设计，不应笼统称为“无逻辑实验”。',
  'rival':'几何与坐标变化可能并无功能信息增加；多张图的一致外观不能代替决定性比较。',
  'repair':'从默认待办中移除独立的“再画一种几何图”；保留一个主裁决，其余作为该裁决所需的控制或历史证据。',
  'minimal_separator':'先选“稳定低维投影是否保留已合格增量”这一明确问题；其他读数仅在排除命名的对手时保留。'},
 {'id':'L6','indices':[83],'kind':'实质性的对照设计失效',
  'problem':'A15_08_E01 的循环标签替换仍保留全局可学习的一一映射，未构造出目标无关对照。',
  'evidence':'E01 Summary 明确 PRIMARY_H2_INELIGIBLE_CONTROL_DESIGN，不能裁决层增量假设。',
  'sources':[str(e01),str(e04)],
  'rival':'额外读出容量仍可以解码被重命名的目标，不能用该对照分离目标信息。',
  'repair':'从确认性支持证据中排除 E01，以已修复 E04 为该轮后续结果入口；保留 E01 作为失效设计记录。',
  'minimal_separator':'修复必须破坏目标对应关系而保持相关容量，且遵守冻结和独立确认；本线已有 E04，不因此再启动实验。'},
 {'id':'L7','indices':[83],'kind':'执行/证据资格失效；并非核心问题没有逻辑',
  'problem':'E02 在冻结前使用了协议不允许的确认标签；E03 未满足注册的身份标识、提取收据及清单要求。',
  'evidence':'E02 Summary 为 INELIGIBLE_PROTOCOL_CONFIRMATION_LABEL_PREUSE；E03 为 INELIGIBLE_GUARD。',
  'sources':[str(e02),str(e03),str(e04)],
  'rival':'协议与结果不一致使该轮不能承担确认性判断；不等于已证明效应不存在。',
  'repair':'从正向证据链排除 E02/E03 的假设判决；修复链折叠为历史记录，保留具体失败原因和原产物。',
  'minimal_separator':'使用已有合格 E04 的有界结果，不通过改旧协议或删除失败文件使旧数值重新合格。'},
]

retire = [
 {'id':'P1','indices':[75,77], 'scope':'固定谱带及头—中—尾排程作为默认方法路线', 'reason':'已有固定带比较和排程结果未建立可重复的整体功能收益；不能从层/谱外观继续推出方法必然有效。', 'action':'从默认待做中移除该原方案；保留其方法比较和停止边界。', 'reopen':'新的独立功能证据显示坐标相对等维随机或错误层控制有额外价值。'},
 {'id':'P2','indices':[78,79,80], 'scope':'在线接力必然因谱身份改善质量的原方法主张', 'reason':'接力收益不支持，运动匹配随机对照后谱身份优势不跨种子稳定；平滑追踪成功单独成立。', 'action':'不再默认扩大原接力训练；将方法结果与可复用工程组件分开记录。', 'reopen':'新问题明确改变了哪个已失败前提，并提供可分离对照；不能只增加预算。'},
 {'id':'P3','indices':[83], 'scope':'A15_08 E01–E03 修复链作为多个并行项目或确认性支持', 'reason':'E01 对照失效、E02/E03 资格失效，已有 E04 合格修复。', 'action':'当前入口只保留 E04 及一条修复历史索引；旧协议和结果不删除。', 'reopen':'只在复核资格或复现来源时展开，不自动重新执行。'},
 {'id':'P4','indices':[35,36,40,42,43,47], 'scope':'未合格或饱和载体上继续作训练目标优劣比较', 'reason':'A12 的可学性/捷径问题与 A13 的旧查询载体、软中继天花板会阻断目标裁决；合格单值载体与后续有效结果应保留。', 'action':'把载体资格及修复收回第 4 线的支持证据，不作为一串当前独立项目。此建议不是宣布整个 MTP 方向停止。', 'reopen':'先有可学、无绕过、未饱和的对照载体，再决定目标比较。'},
 {'id':'P5','indices':[51,52,115], 'scope':'已归档的三个历史 Anchor', 'reason':'它们分别是已关闭反例、执行前停止草案和执行前归档提案；科学含义不同。', 'action':'维持历史身份，从新编号的当前目录中分离；不重复归档，不把未运行改成负结果。', 'reopen':'保留各自原有条件；本方案不主动重新激活。'},
]

for f in findings+retire:
    f['anchor_sources']=[{'path':by_index[i]['anchor_path'],'sha256':hashlib.sha256(Path(by_index[i]['anchor_path']).read_bytes()).hexdigest(),'proposed_number':numbers[i]} for i in f['indices']]
    f['human_scientific_confirmation']=None
    f['wording_revision_applied']=f['id'] in ['L1','L2','L3','L4']
    f['scientific_state_transition_executed']=False

copy_manifest=json.loads((OUT/'reasoning_audit_20260926_copy_manifest.json').read_text())
deletions=[]
for g in copy_manifest['groups']:
    if g['review_action_id'] not in ['D01','D02']:
        continue
    candidate=ROOT/g['proposed_delete_path']; retained=ROOT/g['retained_path_if_approved']
    a=hashlib.sha256(candidate.read_bytes()).hexdigest(); b=hashlib.sha256(retained.read_bytes()).hexdigest()
    assert a==b==g['sha256']
    deletions.append({'id':g['review_action_id'],'candidate':str(candidate),'retain':str(retained),'sha256':a,'bytes':candidate.stat().st_size,'basis':g['reason'],'human_approval':None,'executed':False,'precondition':'Recheck hashes and incoming references immediately before an explicitly approved deletion; preserve the retained source and update review/navigation references.'})

stamp=datetime.now(timezone.utc).isoformat()
payload={'status':'AI_REORGANIZATION_PROPOSAL_NOT_CANONICAL','created_utc':stamp,
 'scope':'121 unique project Anchors (118 nonarchived, 3 archived) plus 3 unassigned dated drafts. Companion translations are not independent questions.',
 'canonical_files_modified':True,'physical_renames':0,'actual_deletions':0,
 'applied_anchor_wording_revisions':revisions,
 'revision_boundary':'L1-L4 wording revised under the user request. Scientific candidates remain AI_PROPOSAL; protocols, result values, approvals and IDs unchanged. Numbering remains a proposal.',
 'default_analysis':'Explain a bounded observed learning consequence, including help or harm, before evaluating a feature predictor or routing method. Existing structure plots and same-panel update checks are complete.',
 'default_sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [ROOT/'PROJECTS.md',DATE/'docs/structure_update/summary_cn.md',DATE/'focus_meeting_structure_update_cn.md',DATE/'01_思路纠偏与聊天计划_cn.md']],
 'numbering_meaning':'Reading-family.question.local-child. Numbers do not confer activation, approval, priority, causality, or evidence strength. Existing explicit parent/child relationships preserved; archived identifiers retained.',
 'source_atlas_sha256':hashlib.sha256(ATLAS.read_bytes()).hexdigest(),
 'lines':[{'number':n,'title':t,'question':q,'kind':k,'legacy_families':o,'inventory_count':len(ix),'numbered_count':sum(i not in archived for i in ix)} for n,t,q,ix,o,k in lines],
 'mapping':mapped,'logic_findings':findings,'remove_from_default_route_proposals':retire,
 'physical_deletion_candidates':deletions,
 'duplicate_boundary':'42 groups and 43 extra copies identified in earlier scoped scan. Only the two named files are first-batch deletion candidates; four cross-date copies remain conditional; other 36 groups require responsibility review.',
 'source_records':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [e01,e02,e03,e04]],
}
(OUT/'research_reorganization_20260926_manifest.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')

header=['新编号（拟）','旧编号','身份','研究问题','原始来源']
md=['# 全量 Anchor 新旧编号对照（审阅稿）','',
 '这是问题检索与编号提案，不是默认推进顺序。共 124 项：118 份非归档项目 Anchor、3 份未归属日期草案、3 份已归档历史。英语与中文伴随稿共享一个编号；本表不改变编号路径、归档状态或研究者判断。L1–L4 的文字修订已另行完成并记录来源哈希。', '',
 '编号：主线.父问题.已有局部子问题。3 份历史不取得新的当前编号；日期草案仅分配待确认的候选号。缺号补齐和旧编号碰撞只在新表中消解，历史引用仍以完整路径识别。', '',
 '“保留”只表示保留问题与证据，不表示应继续运行。L 是推理修订项，P 是移出默认推进的提案；具体边界见[整理方案](research_reorganization_20260926_cn.md)。', '']
for n,t,q,ix,o,k in lines:
    md += [f'## {n}. {t}', '', q, '', '| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |', '|---|---|---|---|']
    for r in mapped:
        if r['proposed_line_number']!=n: continue
        idx=r['source_inventory_index']; tags=[f['id'] for f in findings+retire if idx in f['indices']]
        role='历史保留' if idx in archived else '草案，归属待确认' if idx in drafts else '子问题' if idx in parent else '父级/平铺问题'
        if tags: role+='；'+', '.join(tags)
        md += [f"| {r['proposed_display_number'] or '不重编号'} | {rel_link(r['source_path'],r['legacy_id'])} | {role} | {r['question']} |"]
    md.append('')
(OUT/'research_reorganization_20260926_mapping_cn.md').write_text('\n'.join(md)+'\n')
with (OUT/'research_reorganization_20260926_mapping.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.writer(f);writer.writerow(header)
    for r in mapped: writer.writerow([r['proposed_display_number'] or '历史保留',r['legacy_id'],r['role'],r['question'],r['source_path']])

report=['# 从 1 开始的编号与项目清理方案（待研究者审阅）','',
 '**当前默认推进已经重构为机制分析：先选定实际发生的学习后果，区分可能解释，再判断表征信号或分配方法是否有依据。十条编号保留为问题检索目录，不再充当默认执行路线。**','',
 '本次应用 `research-reasoning-auditor`、`research-mainline` 和相关写作技能，已改 PROJECTS/roadmap 的默认入口及四组 Anchor 的推理文字；新增科学候选保持 AI_PROPOSAL。编号迁移、科学状态确认、实验合同和原始结果没有因整理而改变；未运行实验或删除文件。', '',
 '## 当前默认推进：从已经交付的证据出发', '',
 '研究者要求结合[0926-思维分析-推进](chatgpt-conversation://6ab67be9-ed5c-83e8-bc73-25e9153f8de9)改写。完整可见对话已读；两份上传附件与生成文档的正文未返回。本地[0926结果摘要](../daily_research_reports/0926/docs/structure_update/summary_cn.md)已核实图和同数据更新完成，不能把旧聊天中的“下一步”当作今天仍未做。', '',
 '| 默认任务 | 现在的证据位置 | 完成或停止条件 |', '|---|---|---|',
 '| 明确学习后果及比较口径 | 本面板观察到局部平均帮助；长期共享落后、隔离收益属不同比较 | 写明模型、状态、数据、更新和预算，不预设必须有伤害 |',
 '| 读共同坐标结构及实际参数输入 | 结构图、原始能量谱、中心化方差谱已完成 | 能解释每个点与取点位置；不以可分性代替互害 |',
 '| 读同状态更新的独立后果 | 两步长各12个跨组均值为帮助；一个来源自改善仍不足 | 保留结果及局部范围，不事后挑负值 |',
 '| 选择后果与竞争解释 | 当前讨论任务；具体科学选择仍待研究者确认 | 两种解释产生不同预测；支持、未支持、不足会改变决定 |',
 '| 评价 SAE 信号或路由方法 | 独立预测价值与分配收益尚未建立 | 另行问题/合同，不由几何图自动开启 |', '',
 '最短入口：[结果摘要](../daily_research_reports/0926/docs/structure_update/summary_cn.md) → [图与参数连接](../daily_research_reports/0926/focus_meeting_structure_update_cn.md) → [思路与讨论计划](../daily_research_reports/0926/01_思路纠偏与聊天计划_cn.md)。[当前路线图](../daily_research_reports/0926/figures/default_mechanism_route_20260926.png)与下面的十类目录承担不同职责。', '',
 '**术语解释：**Anchor 是一个研究问题及其可裁决设计；Focus 是研究者当前推进的问题和下一决定；稀疏自编码器（SAE）用少量激活特征重建表征；多词预测（MTP）指同时监督后续多个位置；机制研究要区分现象为何发生，方法比较要判断一种做法在约定条件下是否更有效。','',
 '## 1. 编号的逻辑','',
 '先定义研究对象，再分别理解形成过程、结构和信息后果，最后把方法比较单独列出。第 2–8 线是相关但独立的解释/测量分支，数字相邻不表示存在已证明的因果链，也不表示必须逐线完成后才能研究方法。第 9–10 线明确承认自己在比较方法；方法效果本身不能替代第 2–8 线的机制判断。','',
 '1. **主线用 1–10。** 同一大类下可有数个独立父问题，不能把一个大类强装成一个当前 Anchor。','2. **父问题用 1.1、1.2……；已有局部子问题用 1.1.1、1.1.2……。** 文件前缀可对应 `01_01`、`01_01_01`。每一层都从 1 开始，本轮拟编号无跳号。','3. **每个问题只归一个主目录。** 跨线关系用链接；不复制一份 Anchor，也不因依赖关系把一个独立问题变成另一个的子问题。当前已有的明确父子关系在对照表中保留。','4. **编号表示归属，不表示重要性、通过、完成或活跃。** 当前推进由已有 Focus/研究者决定。历史归档保留旧标识；日期草案的拟归属不等于正式激活。','5. **实验、种子、图和修复轮次不自动取得新的问题编号。** 能改变独立研究决定才需要独立父问题；否则放回对应实验或局部子问题。','6. **这次批准后统一迁移，之后不随删一项反复洗牌。** 旧号保留在映射中；远程作业、原始产物和冻结协议/收据中的历史标识保留原值，不能把审计用的历史字符串全局替换。','',
 '| 新主线 | 核心问题 | 主要旧来源 | 清理方向 |','|---|---|---|---|']
for n,t,q,ix,o,k in lines:
    report.append(f'| **{n}. {t}** | {q} | {o} | {k} |')
report += ['',
 '完整[新旧编号表](research_reorganization_20260926_mapping_cn.md)覆盖全部 124 项；[CSV](research_reorganization_20260926_mapping.csv)便于筛选；[机器清单](research_reorganization_20260926_manifest.json)记录源文件哈希、处置范围及尚未批准的状态。121 项获得候选编号，其中 3 项是未归属草案；另外 3 项保留归档身份。[编号总览图](../daily_research_reports/0926/figures/research_lines_renumbered_20260926.png)给出十条线及其旧来源。', '',
 f'具体例子：旧 A06_00 → **{numbered(11)}**；旧 A15_17 → **{numbered(112)}**，其复用与领域读出子问题 → **{numbered(113)}、{numbered(114)}**。两个同名旧 A15_08_06 分别成为 **{numbered(89)}（8B 几何复现）**和 **{numbered(90)}（语义条件功能子空间）**，不再靠旧短编号猜来源。','',
 '## 2. 可以明确指出的逻辑/设计问题','',
 '以下保存审计发现和处理状态。L1–L4 所述旧句已经修订；“依据”中的行号指修订前审计位置，原判断见[上一版推理审计](reasoning_audit_20260926_research_logic_cn.md)，前后哈希见[修订清单](../daily_research_reports/0926/report_assets/reasoning_anchor_revisions_20260926.json)。L5 是问题过载，L6 是对照设计实质失效，L7 是执行与证据资格失败；这些边界不因改写而成为支持证据。','']
for f in findings:
    links='、'.join(anchor(i) for i in f['indices'])
    if f.get('sources'): links+='；'+'、'.join(rel_link(p,Path(p).parent.name+' Summary') for p in f['sources'])
    state='文字已修订；科学候选待研究者确认' if f['wording_revision_applied'] else '保留审计边界；未更改实验或科学状态'
    report += [f"### {f['id']}：{f['kind']}", '',f'**处理状态：**{state}。','',f"**来源：**{links}。",'',f"**审计发现：**{f['problem']}",'',f"**依据：**{f['evidence']}",'',f"**最强竞争解释：**{f['rival']}",'',f"**处置：**{f['repair']}",'',f"**区分办法：**{f['minimal_separator']}",'']
report += ['L1 的一个可复核反例：令 $L_A(x)=(x-1)^2/2$，$L_B(x)=(x-0.1)^2/2$，在 $x=0$ 两梯度分别为 $-1$、$-0.1$，方向相同。以步长 1 对 A 更新到 $x=1$ 后，A 损失从 0.5 降为 0，B 从 0.005 升为 0.405。它只反驳“不加条件的必要性”，不否定小步长下的一阶梯度分析。','',
 '相反，A15_15 关于可读性最高层的预测可以被结果否定，这本身是合法研究。三个位置都表现出功能价值、唯一最优未定，应该保留这种认识限制，不能仅因预测未成就把实验判为混乱。A15_17_02 的结果不足以及 0925 筛选停止也必须保留；不足和负结果不是删除证据的理由。','',
 '## 3. 建议退出默认推进的具体分支','',
 '这是待确认的阅读/议程收缩建议，不是已经修改科学状态。若某分支本来已经关闭，只纠正旧入口，不再次宣告关闭。P1–P4 的收益是减少自动延续的工作；P5 是维护历史边界。','',
 '| 编号 | 范围与直接来源 | 为何应收束 | 执行后保留什么 / 何时可重开 |','|---|---|---|---|']
for f in retire:
    links='、'.join(anchor(i) for i in f['indices'])
    report.append(f"| {f['id']} | {f['scope']}：{links} | {f['reason']} | {f['action']} 重开条件：{f['reopen']} |")
report += ['',
 '**A15_13 的额外整理要求：**第 10 线可以容纳语义监督、教师资格、结构路由、增量学习，但这些不能在同一 Focus 被当成一个已经获准自动展开的大计划。已完成的教师、层级图、静态读出及失败控制归回各自证据；研究者选定下一决定之前，不把每项技术产物都升级为新的当前项目。本表保留现有来源的父子关系，正式拆并需确认具体问题。','',
 '**与近期主问题的关系：**第 8 线的表征变化、第 3 线的更新互害、第 9/10 线的分配价值可以互相提供证据，但没有一条自动成立的“更集中 → 更语义 → 梯度更兼容 → 路由更好”链。先选择其中一个未知，再决定哪个实验能让两种解释产生不同预测。','',
 '## 4. 本轮可提交审批的实体文件删除','',
 '此前扫描发现 42 组完全相同正文、43 份额外副本；“相同”不等于没有独立职责。当前只建议第一批删除下列两份孤立/别名正文，已再次核对哈希。其他 4 份跨日副本仍需确认逐日自包含的用途；其余 36 组没有加入删除名单。','',
 '| 编号 | 拟删除 | 必须保留 | 字节数 |','|---|---|---|---|']
for d in deletions:
    report.append(f"| {d['id']} | {rel_link(d['candidate'],Path(d['candidate']).name)} | {rel_link(d['retain'],Path(d['retain']).name)} | {d['bytes']:,} |")
report += ['',
 '删除执行前必须再查引用与哈希，因为本审阅材料也新增了候选路径引用。本清单只授权范围提案，不授权删除其他同名或相邻文件。唯一 Protocol、Summary、Detailed、失败记录、已归档原设计、新增未版本化证据，以及运行目录/检查点均不在删除范围。','',
 '## 5. 整理后的最小工作方式','',
 '每个当前问题先写六句：看到了什么；还不知道什么；我的解释；最强竞争解释；两者在哪个结果上不同；三类结果分别改变什么决定。第 5 句写不出来，先澄清问题；三类结果都只是继续调参，就将其明确归为方法迭代，或重新设计机制比较。','',
 '本方案不把 10 条目录设成 10 条活跃线，也不要求立即重写 121 份文档。先选一个当前问题，处理该问题的断点；其余按已有状态收回证据导航。旧 A11/A12/A13 和 A14 等线包含可用的机制分解、反例与有效结果，不应为了目录简洁而整线抹掉。','',
 '## 6. 审阅和实施范围','',
 '- **默认入口已改：**PROJECTS、roadmap、项目 AGENTS 及现有讨论稿按机制问题和按需读取对齐。','- **编号方案仍待审：**确认 10 条线及全量归属后才迁移路径；当前只保留检索映射。','- **推理文字已修：**L1–L4 共六份 Anchor 已收窄；L5–L7 保留审计/资格边界，不改实验。正式认识更新仍由研究者确认。','- **默认推进已收缩：**方法分支不自动进入本轮；P1–P5 的原科学状态和历史记录保持，未整线归档或删除。','- **实体删除仍待认可：**仅 D01、D02 共 70,797 字节列入候选；未执行。','',
 '按研究者先前“我认可以后需要删除”的要求，未实施实体删除。当前改写请求已用于修订默认入口与逻辑措辞，不推定为批准编号迁移或新的实验。编号提案没有替代 PROJECTS/Focus；本轮不声称已完成全仓迁移验收。','',
 '当前入口检查结果：33 项中 5 项文件存在但尚未版本化，均属于 A15_17_02 的新 Anchor/实验记录。保留这些文件；本轮无提交授权，未做 git add/commit。','']
(OUT/'research_reorganization_20260926_cn.md').write_text('\n'.join(report)+'\n')

print(json.dumps({'inventory':len(mapped),'numbered':121,'archived':3,'lines':len(lines),'findings':len(findings),'route_cleanup_groups':len(retire),'delete_candidates':len(deletions),'physical_renames':0,'actual_deletions':0,'line_counts':[(n,len(ix)) for n,t,q,ix,o,k in lines]},ensure_ascii=False))

# Exact, data-driven navigation figure; no generative illustration or causal arrows.
from PIL import Image, ImageDraw, ImageFont
font_path=ROOT/'daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf'
font=lambda size:ImageFont.truetype(str(font_path),size)
im=Image.new('RGB',(1800,1710),'#F4F6F9')
draw=ImageDraw.Draw(im)
draw.text((70,45),'研究问题目录 · 编号审阅方案',font=font(55),fill='#16233B')
draw.text((72,128),'十类历史与独立问题｜当前默认推进另见机制分析路线',font=font(28),fill='#52627A')
colors={'定义与判据':'#4A5975','形成机制':'#246B63','更新机制':'#246B63','监督机制':'#246B63','结构解释':'#4B5EA1','描述与测量':'#4B5EA1','信息与功能':'#4B5EA1','约束与表征':'#4B5EA1','方法比较':'#986026'}
for row,(n,t,q,ix,o,k) in enumerate(lines):
    y=208+row*132
    color=colors[k]
    draw.rounded_rectangle((60,y,1740,y+118),radius=16,fill='white')
    draw.rounded_rectangle((78,y+20,158,y+98),radius=12,fill=color)
    num=str(n); box=draw.textbbox((0,0),num,font=font(39))
    draw.text((118-(box[2]-box[0])/2,y+29),num,font=font(39),fill='white')
    draw.text((185,y+9),t,font=font(34),fill='#18263D')
    draw.text((185,y+54),q,font=font(25),fill='#35435B')
    draw.text((185,y+86),f'旧来源：{o}',font=font(19),fill='#66728A')
    draw.text((1500,y+15),k,font=font(22),fill=color)
draw.text((73,1547),'编号方式：8 → 8.1 → 8.1.1，分别表示主线、父问题、局部子问题。',font=font(27),fill='#263952')
draw.text((73,1595),'124 项均有归属；3 项已归档仅保留历史。目录与文件尚未迁移或删除。',font=font(25),fill='#52627A')
draw.text((73,1640),'来源：124 项 Anchor 清单与新旧编号映射；AI 提案，等待研究者审阅。',font=font(22),fill='#66728A')
fig=DATE/'figures/research_lines_renumbered_20260926.png'
im.save(fig)
digest=hashlib.sha256(fig.read_bytes()).hexdigest()
sources=DATE/'figures/SOURCES.md'
entry=f'| `{fig.name}` | generated | `../report_assets/build_reorganization_review.py` from `../../../docs/research_reorganization_20260926_manifest.json` and `../report_assets/anchor_atlas_data.json` | `{digest}` | 10 proposed reading families; no canonical state transition or causal arrows. |'
old=sources.read_text() if sources.exists() else '# Figure Sources\n\n| File | Origin | Source | SHA256 | Note |\n|---|---|---|---|---|\n'
old='\n'.join(l for l in old.splitlines() if f'`{fig.name}`' not in l)
sources.write_text(old.rstrip()+'\n'+entry+'\n')

route=Image.new('RGB',(1800,1310),'#F4F6F9')
rd=ImageDraw.Draw(route)
rd.text((70,48),'当前默认推进：解释实际学习后果',font=font(51),fill='#16233B')
rd.text((73,124),'结构与一步检查已完成；下一步由证据改变解释，不以找到伤害为目标',font=font(28),fill='#52627A')
stages=[
 ('界定后果','区分局部更新、长期共享落后和隔离收益；固定模型、状态与预算。','当前观测：局部帮助','#246B63'),
 ('结构图与参数对象','共同坐标中的实际样本、两种能量谱、被更新矩阵的真实输入。','已完成','#246B63'),
 ('同状态更新的独立后果','两步长各 12 个跨组均值均为帮助；一个来源的自改善仍不足。','已完成，范围有限','#246B63'),
 ('选择待解释后果与竞争解释','写出双方不同预测及支持／未支持／不足分支，再决定区分检验。','当前讨论；判断待确认','#986026'),
 ('信号预测与分配价值','SAE 只作候选分析工具；独立预测和方法价值分别需要证据。','有依据后另行决定','#66728A'),
]
for i,(title,body,state,color) in enumerate(stages):
    y=220+i*180
    rd.rounded_rectangle((60,y,1740,y+148),radius=18,fill='white')
    rd.rounded_rectangle((82,y+31,160,y+110),radius=12,fill=color)
    rd.text((106,y+41),str(i+1),font=font(40),fill='white')
    rd.text((191,y+17),title,font=font(37),fill='#18263D')
    rd.text((191,y+83),body,font=font(27),fill='#35435B')
    rd.text((1340,y+27),state,font=font(24),fill=color)
rd.text((73,1150),'十条编号是问题检索目录，不是十条并行待办。',font=font(30),fill='#263952')
rd.text((73,1202),'依据：0926 结果摘要、现有图稿与 PROJECTS 默认入口；未启动新实验。',font=font(26),fill='#52627A')
route_path=DATE/'figures/default_mechanism_route_20260926.png'
route.save(route_path)
route_hash=hashlib.sha256(route_path.read_bytes()).hexdigest()
route_entry=f'| `{route_path.name}` | generated | `../report_assets/build_reorganization_review.py` from `../docs/structure_update/summary_cn.md`, `../focus_meeting_structure_update_cn.md` and `../../../PROJECTS.md` | `{route_hash}` | Current reading/analysis route; no scientific approval or execution authorization. |'
existing='\n'.join(l for l in sources.read_text().splitlines() if f'`{route_path.name}`' not in l)
sources.write_text(existing.rstrip()+'\n'+route_entry+'\n')
