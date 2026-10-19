#!/usr/bin/env python3
"""Build a reader copy from qualified, frozen cached-analysis results."""
from pathlib import Path
import csv, json, shutil, hashlib, math
import numpy as np

S=Path('/data/250010109/Research_System')
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
O=E/'analysis/phi_relations_20261018'
C=E/'analysis_tools/phi_relations_20261018'
D=S/'daily_research_reports/1018/phi_relations'
OLD=E/'analysis/feature_frequency/20261015T143300Z'
def read(p):return json.loads(Path(p).read_text())
def rows(p):return list(csv.DictReader(Path(p).open()))
def write(p,s):Path(p).write_text(s.rstrip()+'\n')
def csvout(p,data):
    with Path(p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
def table(header,data):
    def clean(v):return str(v).replace('|','\\|').replace('\n','\\n').replace('\r','\\r')
    return '| '+' | '.join(map(clean,header))+' |\n| '+' | '.join(['---']*len(header))+' |\n'+''.join('| '+' | '.join(map(clean,r))+' |\n' for r in data)
def pct(x):return f'{float(x)*100:.2f}%'
def freq(x):return f'{float(x)*100:.5g}%'
def num(x):return f'{float(x):.6g}'
def cp(src,rel):shutil.copy2(src,D/rel)

def main():
    for sub in ['data','figures','prefixes','provenance','code','cases','members']:(D/sub).mkdir(parents=True,exist_ok=True)
    assert read(O/'result_validation.json')['status']=='PASS'
    mem=rows(O/'all_members_frequency.csv');core=rows(O/'all186_core_decomposition.csv')
    cond=read(O/'conditional_summary.json');energy=rows(O/'contribution_energy.csv')
    cases=read(O/'cases.json');selection=read(O/'selection_D.json')
    hist=np.load(O/'full_K_and_chain.npz');sample=read(O/'case_sampling_summary.json')
    metrics={int(r['group_id']):r for r in rows(OLD/'main/group_metrics.csv')}
    matches={int(r['group_D']):r for r in rows(OLD/'main/matches.csv')}
    vgroups={r['group_id']:set(r['members']) for r in read(OLD/'main/groups_V.json')}
    original_edges=rows(OLD/'main/edges_D.csv')
    for p in (O/'figures').iterdir():
        if p.suffix in ('.png','.pdf','.csv'):cp(p,'figures/'+p.name)
    for p in (O/'prefixes').glob('*.txt'):cp(p,'prefixes/'+p.name)
    data_files=['all_members_frequency.csv','all186_core_decomposition.csv','conditional_metrics.csv',
        'condition_support.csv','contribution_energy.csv','case_all_member_values.csv','case_positions.csv',
        'case_G068_full_matrix.csv','case_G034_full_matrix.csv','case_G014_full_matrix.csv',
        'case_G014_chain_full_matrix.csv','chain_pair_summary.csv','token_composition.csv',
        'position_composition.csv','old_spectrum_paired_strata.csv','old_spectrum_individual_paired.csv']
    for name in data_files:cp(O/name,'data/'+name)
    for gid in (68,34,14):cp(O/f'geometry_G{gid:03d}.npz',f'data/geometry_G{gid:03d}.npz')
    for name in ['cases.json','chain_cases.json','case_sampling_summary.json']:
        cp(O/name,'data/'+name)
    provenance=['input_manifest.json','asset_inventory.csv','selection_D.json','conditional_summary.json',
        'protocol_freeze.json','amendment_receipt.json','geometry_qualification.json','estimator_qualification.json',
        'result_validation.json','completion.json','extraction_receipt.json','full_chain_counts.json']
    for name in provenance:cp(O/name,'provenance/'+name)
    cp(O/'minimal_sync_needed_cn.md','provenance/minimal_sync_needed_cn.md')
    cp(OLD/'main/matches.csv','data/original_D_V_matches.csv')
    cp(OLD/'main/group_metrics.csv','data/original_group_metrics.csv')
    # Full 186-group index, with the already-saved D/V matching separated from new tests.
    idx=[]
    for gid in range(186):
        mm=[r for r in mem if int(r['group_id'])==gid];pD=[float(r['p_D']) for r in mm];pV=[float(r['p_V']) for r in mm]
        v=next(r for r in core if int(r['group_id'])==gid and r['side']=='V')
        mt=matches.get(gid,{})
        idx.append({'group_id':f'G{gid:03d}','members':len(mm),'p_D_min':min(pD),'p_D_max':max(pD),
            'p_V_min':min(pV),'p_V_max':max(pV),'D_V_matched_group':mt.get('group_V','MISSING'),
            'D_V_jaccard_saved':mt.get('jaccard','MISSING'),'D_V_intersection_saved':mt.get('intersection','MISSING'),
            'V_mean_phi_saved':metrics[gid].get('mean_phi_V_frozen_D_group','MISSING'),
            'new_D_core':v['core_members'],'V_core_out_signed_fraction':v['rest_fraction'],
            'H1_status':'COMPLETE_CASE_ONLY' if gid in (68,34,14) else 'NOT_RUN',
            'H2_status':'COMPLETE_CASE_ONLY' if gid in (68,34,14) else 'NOT_RUN',
            'members_source':str(OLD/'main/groups_D.json'),'frequency_source':str(E/'analysis/feature_relation_phase1/20261013T173130Z/feature_frequency.npz'),
            'stability_source':str(OLD/'main/matches.csv')})
    csvout(D/'data/all186_group_index.csv',idx)
    write(D/'data/README.md','''# Table guide and limits

all186_group_index.csv contains all 186 frozen nonsingleton groups. all_members_frequency.csv contains all 13,807 members, exact binary hit counts n_D/n_V, full position denominators N_D/N_V and proportions p_D/p_V. Per-member percentages in reading tables are rounded; CSV values retain precision. Group IDs remain original D IDs.

Saved D/V matching stability is copied from original matches.csv and groups_V.json. Jaccard is intersection divided by union of those member sets; it measures community reconstruction agreement, not document independence, semantic stability, or learning compatibility. membership_review_G*.csv lists retained, departing and arriving members in each saved matched pair.

The new core decomposition uses min(3,m) D-selected nodes. For groups of size 2 or 3 the core therefore covers every member: a zero outside-core sum is a set identity and cannot count as evidence that a few exceptional nodes explain the group. rest_fraction is a signed covariance-sum ratio, not a nonnegative variance attribution. Positive and negative terms and the original denominator are retained in all186_core_decomposition.csv.

The 45 illustrative positions, 12 chain positions, 32,000-position decoder panel, 30,014-position conditional support, complete V and historical winner-selected hidden spectra have different populations. They must not be joined by row number or combined by multiplying fractions. Cases use any-member hits; old spectra use the original winner rule.

Each CSV is either copied from the named execution owner or deterministically derived by code/build_report.py. Exact input paths/digests, raw-cache boundaries and full definitions are in ../methods_cn.md and ../provenance/input_manifest.json. NA or undefined quantities remain missing, never zero.
''')
    # Full-window hit stats, not inferred from an illustration or high-K subset.
    stats={}
    krows=[]
    for gid in (68,34,14):
        hh=hist[f'{gid}_V'];m=len(hh)-1;hits=int(hh[1:].sum())
        stats[gid]={'m':m,'hits':hits,'mean_hit_K':float(np.arange(len(hh))@hh/hits),
            'max_K':int(np.flatnonzero(hh)[-1]),'all_K':int(hh[-1])}
        for k,n in enumerate(hh):krows.append({'group_id':gid,'side':'V','K':k,'positions':int(n),'N':5247663})
    csvout(D/'data/full_V_K_histogram.csv',krows)
    # Each figure receives four explanations outside the plot.
    captions={}
    for gid in (68,34,14):
        g=f'G{gid:03d}';st=stats[gid];m=st['m'];nshow=21 if gid==68 else 24
        cv=next(r for r in core if int(r['group_id'])==gid and r['side']=='V')
        cm=cond[str(gid)];att=cm['attenuation']/cm['excess_unconditional']
        ee=next(r for r in energy if int(r['group_id'])==gid and int(r['layer'])==28)
        geo=np.load(O/f'geometry_{g}.npz');ph=geo['phi_V_panel'];up=ph[np.triu_indices(m,1)]
        token=next(r for r in rows(O/'token_composition.csv') if int(r['group_id'])==gid)
        pr=[r for r in rows(O/'position_composition.csv') if int(r['group_id'])==gid]
        posdelta=max(abs(float(r['group_fraction'])-float(r['V_full_fraction'])) for r in pr)
        mm=[r for r in mem if int(r['group_id'])==gid]
        def cap(suffix,title,sentences,scope):
            captions[f'figure{suffix}']={'title':title,'sentences':sentences,'scope':scope}
        cap(f'1_{g}_graph',g+' 冻结关系图',[
            f'节点为feature ID，面积按完整V命中频率设置并加可见下限，紫色是本轮D侧选定核心，线只来自冻结D图；环形位置没有距离含义。',
            f'完整组有{m}成员，本图展示{nshow}个；'+('这里展示全组。' if gid==68 else '其余成员及其边未画，展示的是D核心3个加其余D频率最高21个的诱导子图。'),
            '这说明原图保留了哪些局部联系，社区归属不要求两两连边，更不要求全组同时激活。',
            '可用它寻找候选子集合，但不能由图形距离、核心颜色或社区标签决定专家共享。'],
            f'D建图；V节点频率N=5,247,663；成员{nshow}/{m}；跨层共享z')
        cap(f'1_{g}_activation',g+' 同位置激活',[
            '每行是可回查的真实预测位置，每列是展示成员，深色仅表示z>0；右侧K依次为完整组与展示列的激活数。',
            f'随机6行、高K6行及单成员3行分开标记；完整V中组命中{st["hits"]:,}次，命中条件下平均K={st["mean_hit_K"]:.2f}，全员同激活{st["all_K"]:,}次。',
            '成员可以作为不同子集合出现；高K行特意富集共同激活，不能代表随机命中分布。',
            '这能限制“社区总作为整体出现”的想象，不能证明应当共享或应当分离学习。'],
            f'V面板32,000位置中选15例；显示{nshow}/{m}成员；完整矩阵另附')
        cap(f'2_{g}_tokens',g+' 当前token构成',[
            '比较V面板中任一组员激活的位置与完整V窗口，显示组内最常见8个当前token及全部其余token；引号内保留空格和换行转义。',
            f'最常见显示token为{repr(token["token"])}，组命中占{pct(token["group_token_fraction"])}，完整V占{pct(token["V_full_token_fraction"])}。',
            '这种富集与输入词片或格式条件参与关联一致，但单个token不能命名整个组的语义。',
            '它给出应纳入分组基线的可观测条件，不能单凭富集量判断φ是否提供额外信息。'],
            f'组命中分母：32,000 V面板的K>0；参考分母：完整V 5,247,663')
        cap(f'2_{g}_positions',g+' 序列位置构成',[
            '每根柱是序列内四个固定位置区间之一，比较组命中面板和完整V的比例。',
            f'四档中最大绝对比例差为{pct(posdelta)}，具体原值在逐图CSV中。',
            '该图检查粗位置组成是否相同，接近也不能排除更细的位置或上下文条件。',
            '因此条件分析同时保留token与位置区间，不能用这张单变量图宣布输入条件已控制。'],
            'V面板K>0对完整V；区间0–255、256–511、512–767、768–1023')
        cap(f'3_{g}_conditions',g+' 条件背景后的关系',[
            '两柱在完全相同的位置和完整成员对上，分别是Q−Q0与Q−Q0_cond，细线为500次粗block重采样95%范围。',
            f'净共同激活由{num(cm["excess_unconditional"])}降至{num(cm["excess_conditional"])}，统计衰减{pct(att)}，粗块范围仍在零以上。',
            '跨原block的独立背景诊断也给出衰减，与已测条件解释部分统计关联一致；剩余仍可能来自未控制上下文。',
            '下一分组比较应保留token与位置基线；衰减不是因果中介比例，残余不是语义组合或学习相容证明。'],
            f'同一V面板支持30,014/32,000=93.79%；{m}完整成员；41原块/11粗块')
        cap(f'4_{g}_core',g+' 核心与其余项',[
            '柱按至少一个D核心端点或两端都非核心分为互斥集合，斜纹为负项，原始分子均除以原m(m−1)。',
            f'核心为{cv["core_members"]}，核心外带符号协方差和为{num(cv["rest_numerator"])}，占全组净和{pct(cv["rest_fraction"])}；最强10对中{cv["top10_pairs_overlap_core_count"]}对也涉及核心。',
            '许多较弱项累加后仍可能占重要部分，因此最强边集中于核心不等于全组关系仅来自核心。',
            '这削弱“只需看这几个核心”的解释，不能排除token或位置解释；这是固定激活表分解，没有删除模型feature。'],
            f'新D正协方差行和top3；完整V 5,247,663；固定分母{m*(m-1):,}；旧E/F未可读')
        cap(f'5_{g}_phi',g+' 二元φ矩阵',[
            '按固定成员顺序读取二元激活相关系数，色标−1到1；灰色代表φ未定义，不是零。',
            f'完整成员对的有限φ范围为{num(np.nanmin(up))}至{num(np.nanmax(up))}，未定义{int(np.isnan(up).sum())}对；图仅显示{nshow}成员。',
            '这测量同位置额外共同出现，不能由正φ推出decoder方向相近。',
            '它为候选关联提供统计证据；频率0或1的面板缺口必须保留，不能补零或静默删员。'],
            f'同一V面板32,000位置；{nshow}/{m}成员；跨层共享z')
        cap(f'5_{g}_cosine',g+' decoder方向矩阵',[
            '成员顺序与φ图完全相同，显示第28层真实decoder单位向量余弦，色标同为−1到1。',
            f'全组非对角成员对中{pct(ee["negative_cosine_fraction"])}余弦为负；平均余弦{num(ee["cosine_mean"])}，具体贡献还取决于同位置z及方向范数。',
            '共同出现与方向相近是不同关系，负余弦也不自动代表功能或梯度冲突。',
            '可将贡献几何作为φ之外的候选分组信息，不能由角度判断学习收益或原模型全部表征。'],
            f'模型block28（零起始27），decoder源索引13；{nshow}/{m}成员')
    captions['figure5_contribution_energy']={'title':'同位置重建贡献分解','scope':'block28；相同32,000 V面板位置，含未命中零贡献；三个完整组',
        'sentences':['每组三柱是自项、正交叉项与负交叉项的平均值，按真实模型坐标和TRAIN层尺度还原decoder。',
        'G068自项603.63、净交叉项612.46；G034为120.44与36.73；G014为2833.27与66.25，净值可同时掩盖正负项。',
        '实际贡献由幅度与几何共同决定，不能把所有成员贡献平方直接相加。',
        '这只解释CrossCoder重建分量的未中心化平均平方量，不是原hidden方差、重建保真度、容量或学习收益。']}
    captions['figure5_cross_layer']={'title':'同一共享z的跨层贡献','scope':'block2/14/28；同一32,000 V位置和完整组；绝对量另附CSV',
        'sentences':['横轴为预先固定模型层，纵轴是净交叉项除以本层自项和；该量可有符号，不是解释率。',
        'G068为0.639/0.362/1.015，G034为0.205/0.433/0.305，G014为0.144/0.176/0.023，未出现统一单调排序。',
        '同一共享z在不同层decoder上具有不同贡献组织；该比值消去本层统一尺度，但仍受各feature相对范数影响。',
        '候选共享需要指定层与贡献对象，不能把这些差别称为各层独立激活或推广成深层更适合共享。']}
    for stage,label,vals in [('original','原谱','R12.53%、F13.14%、N14.05%'),('residual','各组去PC1后','R8.57%、F9.09%、N9.34%')]:
        residual=stage=='residual'
        captions[f'appendix_spectrum_mean_{stage}']={'title':label+'均值谱','scope':'复用1016结果；真实block28 hidden；128位置/组；共同145组；成员覆盖63.84%',
            'sentences':['每条线先将每组中心化协方差特征值归一化，再对相同145个组ID等权平均；R为φ组、F为频率组、N为频率档内匹配随机组。',
            f'第一显示方向的占比均值为{vals}，曲线接近且不是逐方向一致排序。',
            ('这里删除每组自身中心化PC1并按剩余总方差重归一化，差异不只局限于各组最大方向。' if residual else '原谱反映规则选出输入的总方差集中程度，均值排序不等于所有组有同样性质。'),
            '各规则选择的输入不同且原学习EVAL来自TRAIN来源；这不是固定输入的学习干预，不能归因为频率、容量或逐步分离机制。']}
        captions[f'appendix_spectrum_paired_{stage}']={'title':label+'逐组配对差异','scope':'同一145组：小69、中22、大54；block28、128位置/组；复用原谱',
            'sentences':['点为同一组ID的R−F或R−N第一方向占比差，按成员数2–3、4–19、≥20分层；菱形为该层均值，负值表示R较低。',
            ('R−F负值74/145，R−N负值90/145；中组R−F仍为正，大组R−F接近零。' if residual else 'R−F负值78/145，R−N负值85/145；中组R−F平均为正，和整体均值不同。'),
            '组大小分层与逐组反例削弱统一的“关系组都更平”的解释，未改变冻结主样本。',
            '应把谱作为输入分布诊断，不能用整体平均直接绑定专家；缺少共同支持的41组仍未测成同一比较。']}
    captions['figure1_G014_chain_graph']={'title':'G014中的链式子集','scope':'G014完整340成员中的D预选3节点；AB/BC原冻结边；未重新建图',
        'sentences':['仅显示A7146—B9168—C15405两条冻结D边，A–C不在原图；节点间距只为阅读。',
        'D侧φ_AB=0.7444、φ_BC=0.3824、φ_AC=0.0277，说明连边规则保留局部强关系而非所有正相关。',
        '同属社区并不要求两两连边；该子集不能代替340成员全组。',
        '它适合检查链式候选关系，不代表A与C从不共同激活，也不复刻缺少ID的历史案例。']}
    captions['figure1_G014_chain_matrix']={'title':'链中真实同位置激活','scope':'完整V 5,247,663位置；12个源顺序示例；完整340成员矩阵另附',
        'sentences':['三列按A/B/C显示0或1，每类AB非C、BC非A、AC非B和ABC各取源顺序最前3例，标签K为完整340成员计数。',
        '完整V中AB共同8905次、BC2637次、AC182次、ABC177次；没有AC边也存在AC同位置命中。',
        '链式图和激活事件是两个不同对象；历史旧链的成员ID及样本窗口缺失，不能说复现或推翻历史零次观察。',
        '该图修正“没边就没共同出现”的推断，对专家共享仍需贡献与学习证据。']}
    def figure(name,prefix=''):
        x=captions[name];p=prefix+'figures/'
        return f'\n![{x["title"]}]({p}{name}.png)\n\n口径：{x["scope"]}。\n\n'+''.join(f'**{tag}：** {s}\n\n' for tag,s in zip(['怎么读','观察','解释检验','分组意义与未知'],x['sentences']))+f'[PDF]({p}{name}.pdf) · [逐图CSV]({p}{name}.csv)\n'
    write(D/'figures_cn.md','# 逐图解释\n\n每图分别给出对象、实际观察、竞争解释与决策边界。PNG已逐张检查；PDF生成但未单独渲染。\n'+''.join(f'\n## {i+1}. {captions[n]["title"]}\n'+figure(n) for i,n in enumerate(captions)))
    write(D/'provenance/figure_captions.json',json.dumps(captions,ensure_ascii=False,indent=2))
    # Text pages give the exact same prediction positions as the binary matrices.
    kind={'random_hit':'随机命中','high_K':'高K','single_member':'单成员'}
    for gid in (68,34,14):
        g=f'G{gid:03d}';cc=[c for c in cases if c['group_id']==gid];mm=[r for r in mem if int(r['group_id'])==gid]
        csvout(D/f'data/members_{g}.csv',mm)
        memberids={int(r['feature_id']) for r in mm}
        ee=[r for r in original_edges if int(r['u']) in memberids and int(r['v']) in memberids]
        csvout(D/f'data/frozen_edges_{g}.csv',ee)
        mt=matches[gid];vg=vgroups[int(mt['group_V'])]
        retained=memberids&vg
        csvout(D/f'data/membership_review_{g}.csv',[
            {'feature_id':f,'in_frozen_D_group':f in memberids,'in_saved_matched_V_group':f in vg,
             'matched_V_group_id':mt['group_V'],'source':str(OLD/'main/groups_V.json')}
             for f in sorted(memberids|vg)])
        membertable=table(['feature ID','D命中次数','D比例','V命中次数','V比例','本轮D核心'],
            [[r['feature_id'],r['n_D'],freq(r['p_D']),r['n_V'],freq(r['p_V']),'是' if r['D_core']=='True' else ''] for r in mm])
        write(D/f'members/{g}_cn.md',f'# {g} 完整成员表\n\n完整D={5238097:,}，完整V={5247663:,}。次数为原缓存二元命中，不是decoder贡献次数。[来源与定义](../methods_cn.md)。\n\n'+membertable)
        text=f'# {g}：同一预测位置的输入与激活\n\n类别是选择方法，不是语义标签。随机6例来自固定V面板命中位置的哈希抽样；高K6例按激活成员数选取，不代表随机命中；另取K=1三例。各例均保留完整组激活值，未激活成员为0，可回查完整矩阵。下文前缀摘录只展示末320字符，完整前缀文件从当前context起点到位置t，**包含当前token，不包含预测目标t+1**。context起点不保证原文档起点，原文档ID未知。\n'
        for c in cc:
            active=', '.join(f'{a["feature_id"]}:{a["z"]:.7g}' for a in c['active_members'])
            suffix=c['visible_prefix'][-320:].replace('~~~','～')
            text+=f'\n## p{c["position_id"]} · '+ '/'.join(kind[k] for k in c['categories'])+f'\n\n当前token：{chr(96)*2}{repr(c["token"])}{chr(96)*2}；token ID={c["token_id"]}；context={c["context_id"]}；序列位置t={c["context_offset_zero_based"]}（零起始）；原block={c["block_id"]}。K全组={c["K_full"]}，K展示={c["K_display"]}。\n\n~~~text\n{suffix}\n~~~\n\n[完整可见前缀](../{c["prefix_file"]})；原bin绝对token偏移={c["absolute_source_token_offset"]}。\n\n同位置激活成员与z：{active}。\n'
        if gid==68:text+='\n这些例子包含参考文献、新闻、软件提交、评论等来源。高K六例当前token都是句点，随机例还包含转折词、连接符和换行；目前更可靠的共同点是词片或格式条件富集，不是一个统一主题。\n'
        elif gid==34:text+='\n当前token构成富集“ of”“ the”等词片，不能把不同位置的这些例子合成一次共同激活或命名为统一知识主题。读者应同时查看单成员与高K行的反例。\n'
        else:text+='\n该组任一命中几乎覆盖V面板，零散高激活文本容易给出宽泛主题错觉；必须用具体同位置子集合和条件统计，而不是强行命名340成员的主题。\n'
        write(D/f'cases/{g}_texts_cn.md',text)
        st=stats[gid];cv=next(r for r in core if int(r['group_id'])==gid and r['side']=='V');cm=cond[str(gid)]
        intro=f'# {g} 案例卡\n\n本组有{st["m"]}成员；冻结D社区归属未改。[完整成员频率](members/{g}_cn.md) · [成员CSV](data/members_{g}.csv) · [15位置的完整成员矩阵](data/case_{g}_full_matrix.csv) · [全部文本与z](cases/{g}_texts_cn.md)。\n\n'
        lo=min(float(r['p_V']) for r in mm);hi=max(float(r['p_V']) for r in mm)
        intro+=f'完整V成员频率范围为{freq(lo)}至{freq(hi)}。原D组内有{len(ee)}条冻结边；[完整边表及D共同次数/φ](data/frozen_edges_{g}.csv)。原保存D/V匹配中，对应V组{mt["group_V"]}，交集{len(retained)}/{len(memberids)}成员，Jaccard={float(mt["jaccard"]):.4f}；[保留与迁出/迁入成员](data/membership_review_{g}.csv)。这是原有社区重建匹配，不是本轮修改成员，也不证明独立文档稳定。\n\n'
        if gid==68:
            intro+='先把对象说清：feature是固定字典的一个共享系数坐标；在某一实际预测位置，它的z>0才算命中。组是D侧局部φ边经社区算法形成的21成员集合，不是一个总一起激活的“超feature”。\n\n'
            intro+=f'完整V中命中{st["hits"]:,}次，命中时平均{st["mean_hit_K"]:.2f}个成员；全21同激活113次，只占命中约0.0188%。下面固定同一批真实位置，先看谁和谁出现，再看输入、条件背景、核心与贡献。\n\n'+membertable
            intro+='\n例如1273–13292在完整D共同命中56,239次，φ_D=0.572545，是原冻结图中的一条边；它通过原共同命中≥10、正φ和互为top10筛选。社区算法依据全图加权关系将这些节点归为一组，并非要求21成员两两都连边；21成员共有210个无序对，实际只保留62条原边。\n\n'
        elif gid==34:intro+='该组有149成员。主图只展示D预选24成员，完整149列矩阵与成员频率已经另存；截取后没连上的节点不能解释成原社区断开。\n\n'
        else:intro+='该组有340成员，**不是一个三成员组**。主图24成员之外另给三节点链，只为区分图上的连接与真实激活事件；完整340列矩阵保留。\n\n'
        page=intro
        for prefix in ['1_graph','1_activation','2_tokens','2_positions','3_conditions','4_core','5_phi','5_cosine']:
            k,suffix=prefix.split('_',1);page+=figure(f'figure{k}_{g}_{suffix}')
        if gid==14:
            page+=figure('figure1_G014_chain_graph')+figure('figure1_G014_chain_matrix')
            page+='\n[链的完整D/V次数与φ](data/chain_pair_summary.csv) · [12位置完整340成员矩阵](data/case_G014_chain_full_matrix.csv) · [链文本与激活值](data/chain_cases.json)。这次按D规则新选的链出现AC和三者同时命中，不复刻未可读的历史链。\n'
        page+=f'\n## 这个组改变了什么判断\n\n在完整V命中时平均只出现{st["mean_hit_K"]:.2f}/{st["m"]}成员，不能把社区当成逐次全体激活。条件背景调整后净共同激活统计衰减{pct(cm["attenuation"]/cm["excess_unconditional"])}，但残余仍为正；完整V核心外净协方差占全组{pct(cv["rest_fraction"])}。两者窗口与统计量不同，不能将这两个比例相乘。\n\n'
        if gid==68:page+='同一32000位置面板中，1273–13292的φ=0.564676，而block28余弦=−0.141109。G068的全部210对φ都正，仍有68对decoder余弦为负。这使“共现强→同种贡献→应共享”的链条停在第一步；共同出现和幅度加权贡献需要分别看，负方向也不等于学习冲突。\n'
        page+='本轮能据此构造带有输入条件、子集合和贡献几何信息的候选组，不能决定将整个社区绑定一个expert。学习收益未检验，研究者判断保持Unknown。\n'
        write(D/f'case_{g}_cn.md',page)
    # Three-way evidence state is explicit, not hidden in a success flag.
    evidence=[
        ['H1：已测输入条件参与关系','三组同支持30014位置；统计衰减G068 74.90%、G034 79.27%、G014 26.93%；跨块背景同方向','三组粗块范围内仍有正残余；未测上下文可解释','支持部分统计解释；不是因果比例','条件分析仅三例，不外推186组'],
        ['仅少数核心造成全组关系','最强10对中G068/G034全涉及新D核心','完整V核心外净和仍为63.13%/73.36%；G014 85.63%','削弱“仅这三个核心”的解释','未排除token/位置；旧E/F定义缺失'],
        ['H2的竞争解释：φ足以决定贡献方向','G068全部210对φ为正','其中68对block28余弦负；1273–13292为具体反例','支持统计关系与贡献几何分开','负余弦不是学习冲突'],
        ['社区每次作为整体出现','G068全员同激活113例，存在整组事件','命中均K5.07/21；G034/G014从未全员命中','削弱普遍整体激活想象','子集合出现不证明应分开学习'],
        ['R原谱更平可推广到每组','145共同组的R平均第一占比低于F/N','中组R−F方向反转；去PC1后R−F仅74/145为负','平均输入分布差异，存在异质性','不同规则选输入不同，覆盖仅63.84%成员'],
        ['适合共享学习／改善低频学习','本轮没有对应学习干预','方向、共现或谱均不足以填补学习桥梁','Unknown／未执行','无新训练，无因果干预']]
    csvout(D/'data/evidence_rivals.csv',[dict(zip(['claim','support','opposition_or_rival','interpretation','boundary'],r)) for r in evidence])
    write(D/'evidence_cn.md','# 支持与反对解释的证据\n\n'+table(['待判断解释','支持侧观察','反对证据或竞争解释','当前解读','边界'],evidence)+'''

本轮没有任何模型feature删除或学习干预。核心分解是在固定二元激活表上分拆协方差项，条件背景改变的是统计参照，decoder交叉项是既有表示的代数分解。这些都是关系来源分析，不是已经找到低频学习困难的根因。
''')
    write(D/'status_cn.md','''# 执行与缺口

| 状态 | 本轮内容 |
| --- | --- |
| 已完成 | 简明Protocol冻结、自审与修订；严格输入访问；640chunk复用扫描；186组完整成员/频率/原有匹配稳定性索引；186组D/V新核心分解；G068/G034/G014实际位置案例；三例token×位置条件关系与块重采样；真实decoder方向与同位置z贡献、2/14/28层对照；旧145组原始hidden谱复用与分层配对图；32张PNG/PDF/CSV与脚本 |
| 支持不足 | 条件面板1986/32000位置未满足冻结支持，覆盖93.79%只针对面板；G014面板feature3461零命中，339对φ未定义；旧谱41/186组没有共同128位置支持，成员覆盖63.84%；原文档身份/独立性未知；1017两个指定报告与旧E/F核心规则、历史链ID未同步 |
| 未执行 | 其余183组条件与贡献分析；结构V同位置真实hidden保真度（所查owner未定位）；旧E/F精确历史复现；新模型前向；重新建图/分组；CrossCoder或MoE训练；学习收益或因果干预；问题科学关闭 |

没有为了补齐缺失而换数据、降共同谱样本数、修改图规则或重训。缺少结构V同行hidden只阻塞“对原模型表征的保真度”判断，没有阻塞已有z、decoder与文本分析。指定1017报告没有读取；执行侧同名目录的已读范围与最小同步需求见provenance/minimal_sync_needed_cn.md。

没有新Work或分支；当前master。没有commit或push。原始缓存、模型与大表保留执行侧，阅读副本只收选定证据。
''')
    write(D/'overview_cn.md','''# φ关系组：一页导读

长期目的是在固定参数预算下，为专家共享与分离找到依据，改善低频内容学习。本轮只问：φ社区组织了什么关系，它能提供哪些候选分组信息，还缺什么？**先读G068，不要先由组数或谱均值猜语义。**

1. **关系组组织了同位置共同激活的网络，不是一个总一起出现的单元。** G068有21成员，完整V命中时平均5.07个激活，全员同时113次。G034有149成员，命中平均2.79个；G014有340成员，命中平均9.04个。新选G014链有AB/BC边却无AC边，但V中AC仍共同182次，不能把没边说成没共现。
2. **已测输入条件解释了不同程度的统计关联，关系也不只依赖几个最强核心。** 三例同一30014个V面板支持位置中，token×位置背景调整后的净共同激活统计衰减约75%/79%/27%，仍有正残余；完整V的核心外带符号协方差和分别占全组63%/73%/86%。这两套比例不能相乘；条件不是因果干预，核心也不是删除模型feature。
3. **φ没有给出贡献几何与学习共享的答案。** G068中1273–13292的φ约0.565，block28 decoder余弦却约−0.141。同一共享z在不同层解码的交叉项组织也不同。旧真实hidden谱的平均差依组大小而变，不能把更平叫容量更大。

**当前可用信息：** 固定成员与局部边、实际输入条件、子集合命中、D选核心之外的关联、指定层的z幅度与decoder贡献。**仍缺信息：** 结构V同位置真实hidden与重建保真度，以及参数预算固定后的实际学习响应。

**唯一下一优先问题（AI建议，未自动执行）：** 在输入与feature预算固定、保留token/位置基线时，加入实际贡献几何，是否比只用φ更好预测独立位置上、相对真实hidden的重建误差（固定其余重建基线）？先补结构V同行hidden的最小资产，再考虑学习实验；负余弦或正交叉项都不直接决定共享。

[先看完整G068故事](report_cn.md) · [G068案例卡](case_G068_cn.md) · [G034](case_G034_cn.md) · [G014与链](case_G014_cn.md) · [186组索引](data/all186_group_index.csv) · [证据与竞争解释](evidence_cn.md) · [已完成/不足/未执行](status_cn.md)
''')
    write(D/'report_cn.md','''# φ特征关系分析：先真正看懂一个组

## 从G068走完整条分析

G068有21个feature。feature是固定CrossCoder的共享系数坐标；每个实际预测位置都产生一份z，z_i>0记该成员激活。原D侧先按共同命中、正φ与互为top10保留局部边，再通过社区算法形成组。因此，它是一个固定关系网络，不是“21个成员总在同一个输入上一起出现”的新feature。

先看实际出现方式：完整V的5,247,663位置中，G068命中600,157次；命中时平均激活5.07个，全21同激活仅113次。图中的随机行和高K行分开，避免全员案例造成典型性错觉。[完整21成员的D/V次数](members/G068_cn.md)可以回查，不把decoder范数写成各层独立激活。

![G068同位置激活](figures/figure1_G068_activation.png)

怎么读：行是同一实际预测位置，列为全部21成员，深色表示z>0，K是该位置的完整激活数。

观察：随机命中含K=1、2、3、4、10，高K选择有K=20、21；高K行不是随机分布。

解释检验：成员确实共同出现，但具体子集合会变化，社区不等于普遍全员同激活。

分组意义与未知：这使“将整个社区直接当作单一输入单元”需要额外论证，仍不能判定应该共享或分离学习。

再看这些行实际在读什么。例如p5443250位于参考文献前缀末尾“Hasan, S. Badrul (1982).”，当前token为“).”，同位置只有5451、13292、15730激活，z分别0.0546801、0.0925170、0.0127587；这三项才能算这一次共同激活，不能从别的位置拼出共同主题。随机例还包括新闻、软件提交和评论；高K六例当前token全是句点。[全部15例的完整可见前缀及激活值](cases/G068_texts_cn.md)保留实际预测位置t，前缀含当前token，不含预测目标t+1。

在V面板的组命中位置中，当前句点占21.42%，完整V窗口只占2.59%。这让“相同token或格式条件造成共现”成为可检验的解释，而不是将组强行命名为一个语义主题。我们用D面板定义token类别和四段序列位置，在V冻结应用；三个组采用完全相同的30,014个支持位置与完整成员对。

G068的实际平均成对共同激活Q=0.0130384，无条件独立背景Q0=0.000747839，token×位置条件背景Q0_cond=0.00995300。净额由0.0122905减为0.00308536，统计衰减74.90%；跨block背景也给出同方向。它与已测条件解释部分关联一致，但不是“75%因果来自token”；剩余仍可能来自更细的上下文。粗块重采样的剩余净额95%范围为[0.00271161,0.00342674]，只刻画该固定来源的块不确定性，不是独立文档复现。

接着问“是否只是三个核心节点把其他节点串起来”。旧E/F具体核心规则未可读，因此本轮在看V前冻结新的D侧正协方差行和top3规则，选出15730、5451、13292。完整V的全组非对角协方差和为5.08493，涉及核心为1.87504，其余为3.20989；核心外仍占63.13%。最强10对全部涉及核心，但大量较弱对累计并不小。这里分拆的是固定激活表，没有删除模型feature；也不能把63%与前面的25%残余相乘，两者窗口和统计量不同。

最后看“共现是否代表同一种贡献”。同一32,000位置V面板中，1273–13292的φ=0.564676，但第28层真实decoder余弦=−0.141109；全组210对φ都正，仍有68对方向余弦负。同一输入上的贡献还依赖z与方向范数；本层全组自项均值603.63、净交叉项612.46，存在正负交叉项相抵。负余弦不代表学习冲突，净正交叉项不代表共享收益；它们都只说明CrossCoder重建分量的几何与幅度组织。

这条链改变的判断是：**φ组不是语义组合的现成标签，也不是专家共享的直接答案；它提供候选统计联系，输入条件和实际贡献会进一步区分这些联系。** 完整图、同位置矩阵、条件关系与贡献比较见[G068案例卡](case_G068_cn.md)。

## 其他组给出的反例与总体认识

G034有149成员，完整V命中时平均2.79个；token×位置调整后净共同激活统计衰减79.27%，核心外净协方差和仍占73.36%。G014有340成员，命中时平均9.04个；条件衰减26.93%，核心外占85.63%。这些差异说明不能只根据组名、大小或均值给所有社区同一个解释。[G034完整案例](case_G034_cn.md)与[G014完整案例及链](case_G014_cn.md)分别保留全部成员和真实文本。

本轮D预选的G014三节点链为7146—9168—15405。完整V中AB共同8905次、BC2637次，AC虽无冻结边仍共同182次，三者共同177次；这是边阈值与实际事件不同的例子。历史“AC及ABC为零”的链缺少成员ID与窗口，本轮没有声称复现或推翻那个旧观察。

旧R/F/N真实第28层hidden谱只作补充：相同145组ID、128位置/组，R是φ组，F为同池频率排序组，N为D频率10档内交换标签且逐组保留大小和档构成。R均值首方向较低，但中等组相对F方向相反；各组去自己的中心化PC1后也没有统一逐组优势。输入由不同规则选择，来源还是原学习TRAIN来源EVAL512，不能与结构V拼行，不能把更平推成容量或学习收益。[逐组配对与分层图](figures_cn.md)保留反例和覆盖缺口。

目前只有三条认识更新：社区是多数命中只涉及部分成员的统计网络；已测输入条件能解释不同程度的关联而少数核心不足以概括总和；φ不足以决定实际贡献几何。它们能改进候选分组信息，尚不能支持专家共享的科学决定。

## 下一步唯一优先问题与交付

AI建议先固定输入、feature预算和其余重建基线，检验“φ加实际贡献几何”是否比“仅φ”更好预测独立位置上相对真实hidden的重建误差，同时保留token/位置基线；目标不是直接由z和decoder定义的交叉项。本轮结构V同位置真实hidden未定位，因此这个问题尚未执行；它比直接再上MoE训练更贴近当前缺失的证据桥梁。

本轮没有因果干预，是关系来源分析；没有CrossCoder重训、MoE训练、模型前向、重新建图或新Work。研究者对机制、共享决策和问题关闭的判断保持Unknown。

[一页导读](overview_cn.md) · [计算与来源](methods_cn.md) · [全部186组索引](data/all186_group_index.csv) · [13,807条成员频率](data/all_members_frequency.csv) · [45位置表](data/case_positions.csv) · [支持与反对证据](evidence_cn.md) · [执行状态与缺口](status_cn.md) · [全部32图与四句解释](figures_cn.md) · [推理审计](reasoning_audit_cn.md)
''')
    write(D/'methods_cn.md',r'''# 计算对象、来源与限制

## 资产口径

| 对象 | 实际可用口径 |
| --- | --- |
| 字典 | final14/F16384；999,997,440训练位置检查点；14个源层为block2,4,…,28；检查点SHA沿用registry与缓存绑定，本轮没有重新完整哈希GB检查点 |
| 组成员与图 | 20261015T143300Z/main/groups_D.json与edges_D.csv；186非单例组、13,807成员；原q10规则冻结 |
| D/V与样本量 | 结构缓存完整D=5,238,097、V=5,247,663；81个原128-context块，D40/V41；不是已核实的独立文档 |
| 激活 | 跨层共享z，经原TRAIN门控；a_i(x)=1[z_i(x)>0]；各层decoder范数不是独立激活 |
| 新面板 | 复用1017既定seed20261017，每640chunk各100位置，总64,000；D/V各32,000；不重新编码 |
| 条件窗口 | D确定token类别、位置区间与支持规则；V冻结使用；共同支持30,014/32,000=93.79%，缺1986位置，不补零 |
| 文本映射 | 原VAL bin→1024 context→eligible token offset；位置t对应当前可见token，前缀0..t，预测目标t+1不作为可见输入；原文档ID未知 |
| decoder | 真实检查点decoder；主block28，浅block2、中block14；保存方向乘各层TRAIN centered-vector RMS还原模型坐标；bias和TRAIN均值不重复加给每组 |
| 结构V原始hidden | 在已检查结构缓存owner内未定位；不能把不同行学习EVAL hidden替代 |
| 旧原始hidden谱 | 复用1016已核查结果；原学习TRAIN来源EVAL512，512contexts/523136位置；block28 residual-post、最终RMSNorm之前；每组128位置、共同145组 |
| 指定1017报告 | 本机两个Research_System路径缺失，未声称读取；同源执行目录已读但不含E/F完成结果 |

[逐资产路径](provenance/asset_inventory.csv) · [输入SHA与定义](provenance/input_manifest.json) · [最小同步清单](provenance/minimal_sync_needed_cn.md)。原始缓存和检查点保持执行侧。

## 二元关系、同分母与核心分解

先定义对象：每个实际预测位置有一组共享系数，feature命中是二元事件。指定窗口上\(p_i=E[a_i]\)、\(p_{ij}=E[a_i a_j]\)。二元相关为

\[
\phi_{ij}=\frac{p_{ij}-p_i p_j}{\sqrt{p_i(1-p_i)p_j(1-p_j)}}.
\]

频率0或1时未定义，不能补零。组内图保留D侧共同命中≥10、正φ、互为top10的边，再作加权贪心社区；同社区不等于全连接或全员同激活。G014为340成员，链只是子集。所有例子保留实际位置，不从不同文本拼出共同激活。

同一支持位置集T、完整m成员中，K为每位置激活数：

\[
Q=\frac{E_T[K(K-1)]}{m(m-1)},\quad
Q_0=\frac{(\sum_i p_i)^2-\sum_i p_i^2}{m(m-1)}.
\]

按D定义的token×位置条件s，以V支持位置比例\(w_s\)加权：

\[
Q_{0,\mathrm{cond}}=\sum_s w_s
\frac{(\sum_i p_{i|s})^2-\sum_i p_{i|s}^2}{m(m-1)}.
\]

三种值的feature对、位置和分母完全一致。主图显示Q−Q0与Q−Q0_cond；衰减为两者之差。百分比只在原净额正时报告，表示统计参照改变，不是因果贡献率。

D面板精确token需≥50行/5原D块，否则归OTHER；四个固定位置档；D与V每格支持均≥20行/3块。D决定类别，V只按样本支持应用，不看关系挑条件。面板支持表保留D/V所有条件，条件定义与全部支持位置ID保留执行侧condition_selection.json。

经验条件均值可能随细分层机械性降低净关联，因此另用同条件不同原block之间的边际乘积。每条件的分子为\(\sum_{i\ne j}[c_{is}c_{js}-\sum_b c_{isb}c_{jsb}]\)，分母为\(m(m-1)[N_s^2-\sum_b N_{sb}^2]\)，再按\(N_s/N\)加权；无条件背景也采用相同跨块规则。这个诊断减轻局部拟合担忧，仍不能排除块间上下文差异。

500次固定seed20261018块重采样同时给原41V块与11个较粗连续区间结果；重采样不重选D类别、V支持集、面板或核心。图用较粗范围，二者均附CSV。这些块不是原始文档，不能把大量相邻token当独立重复。

核心规则因旧E/F资产缺失而显式新定：完整D非对角正协方差行和最高3成员，同分按ID。完整V所有有序非对角项分为至少一端核心与两端都非核心，分别累计正负；全部除原m(m−1)，并保留未除分子。最强10对与核心有重叠，不能作为另一互斥部分相加。它不是删除模型节点的干预；核心外比例也不能与不同条件窗口的衰减比例相乘。

## 实际贡献对象

真实模型层l的方向为\(d_{i,l}=r_l W_{i,l}\)，r为该层TRAIN centered-vector RMS。组贡献\(h_G(x)=\sum_{i\in G}z_i(x)d_{i,l}\)，不重复加入bias或均值。对同一32,000个V面板位置（含未命中零值）：

\[
E\|h_G\|^2=
\underbrace{\sum_i E[z_i^2]\|d_{i,l}\|^2}_{\text{自项}}
+\underbrace{2\sum_{i<j}E[z_i z_j]\langle d_{i,l},d_{j,l}\rangle}_{\text{交叉项}}.
\]

这是未中心化的平均平方重建贡献，不是协方差、方差或对真实hidden的保真度。余弦只测单位方向角度；实际交叉项保留幅度与范数，负项可参与重建抵消。跨层cross/self消去本层统一尺度但保留相对范数影响，不是解释率。直接向量重建与Gram计算9单元核对通过，误差在浮点范围内。

G014在此V面板feature3461零命中，339个成员对φ未定义；仍保留该成员和可测方向。没有同行真实hidden及残差，不能声称解释原模型全部表征。

## 旧谱及选择差异

R为原φ组；F将同一13,807池按D频率排序填入原组大小序列；N在D频率10等人数档内随机交换R标签，逐组保留成员数与频率档构成。N没有控制全部连续频率、幅度或输入组成，F组平均频率分布也与R不同。

输入沿旧学习评分：组命中比例按D均值/标准差标准化，只有命中组竞争，原固定并列顺序选胜组；每组固定128位置。本轮案例/条件用任一成员命中或全V面板，**不与旧谱胜组口径混用**。旧谱各组centered hidden的\(\lambda_1/\sum\lambda\)是第一方向方差占比；若来自SVD应为\(\sigma_1^2/\sum\sigma^2\)。删除每组自身中心化PC1后，剩余首占比为\(\lambda_2/\sum_{k\ge2}\lambda_k\)，不是删除全局未中心化第一奇异方向，也不把PC1叫common feature。

145共同组、8,814/13,807=63.84%成员；小69/中22/大54。R/F/N原首均值12.53/13.14/14.05%，余首8.57/9.09/9.34%，不是普遍逐组结论。旧来源里每组最大单context比例曾达R32.03%，各规则输入不同；后验10%上限诊断未消除全部文本重复。旧完整支持、位置、context诊断见1016/crosscoder_phi_input_spectrum，不为本轮另选样本或重求谱。
''')
    write(D/'reasoning_audit_cn.md','''# 科研推理审计

采用research-reasoning-auditor，对Protocol冻结前、估计式实现后、结果解释与交付前重复审计。实际文件、CPU执行和数值资格由主agent完成；两个辅助agent只审阅主agent提供的公式/数值与措辞，没有文件工具，不能算独立来源复核。

| 审计阶段 | 自我反驳 | 修正与证据 |
| --- | --- | --- |
| 冻结前 | 同社区是否被偷换成全员同激活？ | 保留完整K分布、随机/高K/单成员行与全组矩阵；G014明确340成员 |
| 估计前 | 条件细分会机械提高条件背景吗？ | 增加不同原block边际乘积；无条件和条件均用相同跨块规则；协议amendment保留 |
| 数值后 | Q三项是否偷换位置、成员或分母？ | 共同30014位置、完整成员对；显式枚举cross-block与纯条件合成例PASS；冻结哈希未变 |
| 核心解释 | 核心外百分比是否受删节点分母变小影响？ | 原分子与固定原m(m−1)并报；正负项分开；核心与top10重叠不能相加 |
| 贡献解释 | 平均平方量是否被叫协方差或解释率？ | 改为未中心化平均平方重建贡献；9单元直接向量/Gram核对PASS；cross/self不称解释率 |
| 文本解释 | 不同位置例子能否被拼成同一共同激活？ | 每例保留position/context/t/token/完整前缀及同位置z；不强制语义命名 |
| 历史与来源 | 同源新结果是否冒充旧E/F或G014复现？ | 缺失资产单列；新D核心规则与新链ID显式标注；旧谱TRAIN来源与结构VAL分开 |
| 最终推断 | 条件后残余、正交叉项、更平谱能否决定学习？ | 仍有未测上下文、幅度与源选择；本轮无学习/因果干预，科学判断Unknown |

实质修正：将“解释75%”改为“条件独立背景调整后统计衰减约75%”；将“核心外保留关系”精确为“核心外带符号协方差和占全组净和”；明确面板覆盖不是完整V覆盖；禁止将条件残余与核心外比例相乘；负余弦不是梯度冲突；跨层是同一共享z的decoder组织差别。

科学结论只落在三例的关系来源与贡献组织；186组只完成成员频率、原有匹配索引和新核心分解。没有用三例代表全部组，没有将现象、已削弱解释、仍存竞争解释和实际干预合并。
''')
    write(D/'summary.md','''# Phi feature groups: relation sources and reconstruction contributions

The long-term aim is to inform expert sharing under a fixed parameter budget. This round asks what the frozen phi communities organize, without treating co-activation, input conditions, contribution geometry, and learning compatibility as interchangeable.

G068 has 21 members but averages 5.07 active members conditional on a full-V hit; all 21 occur together only 113 times. Across the same 30,014 supported V-panel positions, token-by-position background adjustment attenuates excess pairwise co-activation by 74.90% for G068, 79.27% for G034, and 26.93% for G014. Positive residual association remains under block resampling and cross-block background diagnostics. These are statistical attenuation estimates, not causal mediation.

A newly frozen D-only positive-covariance core rule leaves 63.13%, 73.36%, and 85.63% of the signed full-V covariance sum outside the three cores. This is fixed-table decomposition, not feature deletion. Strong binary association also does not determine decoder geometry: G068 features 1273 and 13292 have panel phi 0.564676 but layer-28 decoder cosine -0.141109.

All analysis reuses saved activations, actual decoder vectors, token mappings, and prior raw-hidden spectra. No model forward, training, regrouping, new Work, commit, or push occurred. Same-position structural-V raw hidden and historical E/F outputs remain unavailable in the inspected owners. Learning compatibility and scientific closure remain Unknown.

[Chinese reader entry](overview_cn.md) · [Detailed methods](detailed.md) · [All 186 groups](data/all186_group_index.csv) · [Evidence and rivals](evidence_cn.md)
''')
    write(D/'detailed.md','''# Detailed execution record

The exact contract is in protocol.md, with explicit amendments. Chinese computation definitions, layer interfaces, source boundaries, and uncertainty are in methods_cn.md. The execution owner is /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/phi_relations_20261018. Scripts originate from the sibling analysis_tools/phi_relations_20261018 directory and are copied under code/.

The saved 640-chunk activation cache was scanned once. A fixed 100-position sample per chunk yielded 64,000 positions, split evenly into discovery D and review V. New conditional and geometry analyses concern three case groups, not all 186. Core decomposition and member/frequency export cover all 186 frozen nonsingleton groups. All conditional comparisons share 30,014 positions; decoder analyses share all 32,000 V-panel positions; complete-window covariance uses 5,247,663 V positions. These populations must not be conflated.

Estimator examples, brute cross-block enumeration, full-window K/covariance identities, direct decoder-vector energy, frozen protocol digests, actual text prefixes, and same-denominator checks passed. Provenance and qualification receipts are preserved. PNGs were decoded and visually checked; generated PDFs were not independently rendered. No independent-document confirmation or causal intervention is claimed.

Selected figures, small sufficient results, case activation matrices, texts, and manifests are reading evidence. Raw z panels, full activation caches, conditional block statistics, checkpoint tensors, and the large all-pairs table stay execution-side. The payload manifest records every selected file. No historical scientific state was promoted.

[Chinese detailed methods](methods_cn.md) · [Completed / insufficient / not run](status_cn.md) · [Audit](reasoning_audit_cn.md)
''')
    write(D/'summary_cn.md','# 本轮总结\n\n[一页中文概要](overview_cn.md)给出目的、三条认识更新及唯一下一优先问题；[完整报告](report_cn.md)先用G068解释整条分析；详细方法与来源在[计算记录](methods_cn.md)。\n')
    write(D/'detailed_cn.md','# 详细记录入口\n\n[精确计算、窗口与来源](methods_cn.md) · [推理审计与修正](reasoning_audit_cn.md) · [已完成/支持不足/未执行](status_cn.md) · [逐图解释](figures_cn.md) · [执行英文记录](detailed.md)。数值资格与协议哈希见provenance目录；大缓存保留执行侧。\n')
    write(D/'README.md','''# 11109 — phi feature relation analysis

[一页导读](overview_cn.md) → [先看一个真实组的完整分析](report_cn.md)

- Cases: [G068](case_G068_cn.md), [G034](case_G034_cn.md), [G014 and its chain](case_G014_cn.md).
- Data: [186 groups](data/all186_group_index.csv), [all members and frequencies](data/all_members_frequency.csv), [same-position text cases](data/case_positions.csv).
- Interpretation: [evidence/rivals](evidence_cn.md), [methods](methods_cn.md), [status](status_cn.md), [reasoning audit](reasoning_audit_cn.md).
- Figures: [32 figures, four explanations each](figures_cn.md), with PNG, PDF and CSV under figures/.
- Contract: [English protocol](protocol.md), [Chinese protocol](protocol_cn.md), [amendments](protocol_amendments_cn.md).

Existing master workspace; no new Work, training, model forward or graph change. Scientific judgment and learning utility remain Unknown. Execution data stays in MoE_Router; this folder contains selected reading evidence.
''')
    # Copy reproducible code last; payload hash is produced by the finalizer after viewing.
    for p in C.glob('*.py'):cp(p,'code/'+p.name)
    print('REPORT_BUILT',len(captions),'figures',len(idx),'groups',flush=True)

if __name__=='__main__':main()
