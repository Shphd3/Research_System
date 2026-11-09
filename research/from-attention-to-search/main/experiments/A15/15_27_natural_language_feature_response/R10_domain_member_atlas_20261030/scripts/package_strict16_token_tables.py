"""Readable bilingual tables from the unchanged per-member native-positive inventory."""
from pathlib import Path
import csv,json,hashlib,shutil,re
W=Path(__file__).resolve().parents[1];R=Path('/data/250010109/Research_System');S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');O=S/'presentation_variants/strict16_per_member_tokens_20261030';D=W/'figure_variants/strict16_per_member_tokens_20261030';M=R/'daily_research_reports/1031/meeting_report'
def read(n):return list(csv.DictReader((O/n).open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=read('member_summary.csv');top=read('member_token_top10.csv')
def pct(x):return f'{100*float(x):.1f}%'
def piece(t):
    t=t.replace('\\','\\\\').replace('\n',r'\n').replace('\t',r'\t').replace('|',r'\|');return t.lstrip(' ') or '[space]'
def topcell(r,cn=True):
    token=piece(r['token_string']);count=r['native_positive_positions'];docs=r['active_documents'];return f"`{token}` [{r['token_id']}]：{count}次／{docs}篇" if cn else f"`{token}` [{r['token_id']}]: {count}positions / {docs}docs"
metrics_cn=['| Feature | 领域 | 激活次数 | 覆盖篇数/20 | token种类 | 共用位置占比 | 本批单域位置占比 | 其他位置占比 |','|---|---|---:|---:|---:|---:|---:|---:|']
metrics_en=['| Feature | Bias | Positive positions | Active docs/20 | Token types | Shared positions | Single-domain positions | Other positions |','|---|---|---:|---:|---:|---:|---:|---:|']
type_cn=['| Feature | 共用种类数／占比 | 本批单域种类数／占比 | 其他种类数／占比 |','|---|---:|---:|---:|'];type_en=['| Feature | Shared types / fraction | Single-domain types / fraction | Other types / fraction |','|---|---:|---:|---:|'];type_rows=[]
for r in rows:
    vals=[r['feature_id'],r['domain_bias'],r['positive_positions'],r['active_documents'],r['distinct_token_IDs'],pct(r['shared_share']),pct(r['observed_single_domain_share']),pct(r['other_or_insufficient_share'])]
    metrics_en.append('| '+' | '.join(vals)+' |');vals[1]='数学' if r['domain_bias']=='math' else '生物';metrics_cn.append('| '+' | '.join(vals)+' |');N=int(r['distinct_token_IDs']);out={'feature_id':r['feature_id'],'domain_bias':r['domain_bias'],'total_token_types':N};types=[]
    for c in ['shared','observed_single_domain','other_or_insufficient']:
        n=int(r[c+'_token_types']);v=n/N;types.append(f'{n}／{v:.1%}');out[c+'_types']=n;out[c+'_type_fraction']=v
    label_cn=('数学' if r['domain_bias']=='math' else '生物')+' · f'+r['feature_id'];label_en=('Math' if r['domain_bias']=='math' else 'Biology')+' · f'+r['feature_id']
    type_cn.append('| '+label_cn+' | '+' | '.join(types)+' |');type_en.append('| '+label_en+' | '+' | '.join(types)+' |');type_rows.append(out)
with (O/'member_type_composition.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(type_rows[0]));w.writeheader();w.writerows(type_rows)
tops_cn=['| Feature | 第1位：token [ID]，次数／篇数 | 第2位 | 第3位 |','|---|---|---|---|'];tops_en=['| Feature | Rank1: token [ID], positions/docs | Rank2 | Rank3 |','|---|---|---|---|']
for r in rows:
    label_cn=('数学' if r['domain_bias']=='math' else '生物')+' · f'+r['feature_id'];label_en=('Math' if r['domain_bias']=='math' else 'Biology')+' · f'+r['feature_id']
    tt=[x for x in top if x['feature_id']==r['feature_id']][:3];tops_cn.append('| '+label_cn+' | '+' | '.join(topcell(x) for x in tt)+' |');tops_en.append('| '+label_en+' | '+' | '.join(topcell(x,False) for x in tt)+' |')
cn='''# 严格单域16名：逐成员真实token表

[English](README.md) · [上轮合并简图](../pooled_simple_20261030/README_cn.md)

## 认识更新

**这16名的词面响应形式并不一致：有的激活主要落在共用词面和标点上，有的更多落在细胞相关词或子词上。严格单域使用不能直接等同于识别领域专有词；“其他／支持不足”也不能理解为没有领域含义。**

以下是已核验的描述性结果，不赋予因果、语义功能或身份编码结论。逐成员列表与计数先供研究者核查，机制判断仍Unknown。

## 统计口径

- 同一A22原生共享z、同一门控，沿用全缓存严格单域16名（7数学、9生物），不换成员。
- 本表只统计旧留出40篇（每域20篇），每篇token索引32–191的160位置，共6,400位置。激活是z>0，没有改用p90或强度加权。
- 同一token在不同位置出现分别计数；文档覆盖按不同原文档去重。16名合计4,675个“成员×位置”激活事件，对应2,898个不同输入位置。不同成员可在同一位置激活，不能把4,675当独立token数。
- 每个成员的共用／单域／其他占比，分母为该成员自己的激活位置数；不同token ID去重后的“种类占比”另表列出。
- 类别沿用上一轮全120篇输入覆盖：两域各≥5篇出现为共用；某域≥5篇且另一域0篇为本批单域；其余是其他／支持不足。它不是凭词义标注的语义专属性。16名筛选和类别均已使用全缓存，因此本表不是独立留出验证。

## 表1：每名成员的激活量、覆盖与位置组成

'''+ '\n'.join(metrics_cn)+'''

百分比四舍五入后可能相差0.1个百分点。所有16名保留，11960仅覆盖4篇、32位置，尤其需要保留支持有限的边界。

## 表2：按激活次数排序的前三token

每格是“token [精确ID]：激活次数／覆盖篇数”。为阅读省略前导空格，换行以反斜杠记号显示，完整原字符串在CSV中。次数并列按tokenID升序；没有为展示换词。前三名不表示覆盖多数激活；各成员Top3/Top10覆盖率保存在member_summary.csv。

'''+ '\n'.join(tops_cn)+'''

## 怎样理解这些具体token

1. 数学七名的前三位大多包含`the`、逗号、`is/in/of`；5234还突出`$`与`_{`，说明数学格式也是可见响应对象，不能只按术语解释。
2. 生物2635的共用位置占90.3%，前三位是句点、句点加换段、右方括号；这只是响应位置构成，尚不能称它只编码标点或边界。6270也有标点和数字token。
3. 生物15401更集中在细胞词面：` cell`14次、6篇，` cells`10次、4篇；两者合计24/45=53.3%的激活位置。本批单域类别合计55.6%，不等于全语料语义专有。
4. 13691的`il/gl/pred`、7238的`ial/illin/itin`都是子词，完整拼写可出现在trilobite/glial/predation、glial/fibrillin/ubiquitin中。完整词形是事后可读性说明，不用于解释当时已读信息；即便token显示`the`，也可能是theorems的前缀，精确ID不能直接当完整词。
5. 10395的前三token都仅覆盖一篇，7238的前三token也各仅一篇；不能凭这些主要词面将其推广到所有肾脏或蛋白质语境。11960的bamboo有3次但仅一篇，整体支持有限。
6. `renal`等词虽然词义上容易辨认为生物相关，在本批却可能不足5篇覆盖，依规则仍归其他。高“其他”比例不代表通用语义，更不证明缺少领域信息。

表中原始次数未扣除词本来出现的频率，不单独建立token偏好。完整表还提供同域可用token次数与文档数、条件激活比例，便于继续核查，但它们仍不是配对干预。

## 表3：按不同token ID计数的种类组成

本表分母是各成员激活过的不同ID数，与表1的位置分母不同。

'''+ '\n'.join(type_cn)+'''

## 可下载数据与复现

[逐成员总表](member_summary.csv) · [逐成员类型占比](member_type_composition.csv) · [每成员Top10](member_token_top10.csv) · [每成员全部token](member_token_all.csv) · [定义](config.json) · [核查](audit.json)。全部列表来自同一原始位置缓存。生物与数学在这里是成员偏向标签，不能直接转成词义标签。

复现：本轮`strict16_per_member_tokens.py`生成原始表，`package_strict16_token_tables.py`生成阅读表；均在所属R10的scripts目录，使用本地spectral-hier Python。逐成员次数、文档覆盖和三类位置份额与前版逐成员表一致，16名均零异域激活，4675事件与1182不同ID完全复现。没有新增模型前向、训练、谱拟合或成员筛选。
'''
en='''# Native-positive token inventory for every strict16member

[中文](README_cn.md) · [Previous pooled figures](../pooled_simple_20261030/README.md)

## Belief update

**The16members have heterogeneous surface responses: some occur largely on shared tokens/punctuation, others more on cell-related surfaces or subwords. Panel-single-domain use does not establish exclusive domain-word recognition. Other/insufficient coverage does not mean absent domain meaning.**

These are verified descriptive measurements. Mechanism/identity/causal interpretation remains Unknown.

## Units and definitions

Unchanged native A22shared-z/gate and16all-cached-strict members(7math/9biology).Observe oldheldout40documents,20/domain,160positions/doc(indices32..191),6,400positions.Nativez>0only;no p90or intensity weighting.Positive counts are positions;document coverage deduplicates original documents.The total4,675member-position events cover2,898distinct input positions,not4,675independent samples.

Per-member position fractions divide by that member's positive positions.Type fractions below divide by its distinct exact IDs.Categories preserve the previous all120input-document rule:shared≥5documents/domain;panel-single-domain≥5in one and0in the other;remainingother/insufficient.These are coverage categories,not semantic labels.Selection and category definition inspect all cached documents;oldheldout is exploratory rather than independent generalization.

## Table1: every member's support and position composition

'''+ '\n'.join(metrics_en)+'''

Rounding can produce0.1ppdiscrepancies.All16remain;11960has only4active heldout documents/32positions.

## Table2: first three tokens by native positive count

Display omits leading spaces but preserves IDs/case/newline notation.Raw strings remain inCSV.Rank by descending count,ascendingIDfor ties.No example substitutions.Top3need not cover a majority;Top3/Top10coverage is saved.

'''+ '\n'.join(tops_en)+'''

Math top ranks often include shared words and punctuation;5234also hasmath markup.Biology2635has90.3%shared positions and punctuation at top,but this does not establish a pure punctuation feature.15401hascell14times/6docsandcells10times/4docs,together24/45=53.3%of positive positions.Subwordsil/gl/predandial/illin/itinare not complete words;posthoc spelling aids include trilobite/glial/predationandglial/fibrillin/ubiquitin,never causal explanations of unseen suffixes.EvenID279can prefix theorems rather than a full article.All three leading10395tokens occur in one document each;7238also has one-document leading-token coverage.11960is especially sparse.Recognizable domain words such asrenalcan remainotherdue to inadequate document support.Highotherdoes not mean generic semantics or no domain information.

Raw counts alone do not establish token preference.Full tables include same-domain available occurrences/documents and conditional activation fractions for audit;these are observational quantities.

## Table3: distinct-token-type composition

'''+ '\n'.join(type_en)+'''

## Data and reproduction

[Member summary](member_summary.csv) · [Type fractions](member_type_composition.csv) · [Top10per member](member_token_top10.csv) · [All tokens per member](member_token_all.csv) · [Definitions](config.json) · [Audit](audit.json).

Run R10scripts/strict16_per_member_tokens.pythenpackage_strict16_token_tables.pywith local spectral-hierPython.Counts/document coverage/category fractions independently reproduce the existing native-positive summaries;4,675events/1,182unionIDsand all16members retained.No new model forward,training,PCAor selection.
'''
for name,body in [('README_cn.md',cn),('README.md',en)]:
    (O/name).write_text(body);(D/name).write_text(body)
shutil.copy2(O/'member_type_composition.csv',D/'member_type_composition.csv')
pro=json.loads((O/'provenance.json').read_text());pro['sources']=[r for r in pro['sources'] if r['path']!=str(Path(__file__).resolve())];pro['sources'].append(dict(path=str(Path(__file__).resolve()),bytes=Path(__file__).stat().st_size,sha256=sha(Path(__file__).resolve())));(O/'provenance.json').write_text(json.dumps(pro,indent=2)+'\n');shutil.copy2(O/'provenance.json',D/'provenance.json')
names=['config.json','member_summary.csv','member_token_all.csv','member_token_top10.csv','member_type_composition.csv','provenance.json','audit.json','README.md','README_cn.md'];manifest={'parent_asset_id':'analysis_a15_27_r10_near_domain_token_context_20261030','scope':'derived native-positive per-member token counts on unchanged16members','files':[dict(path=n,origin=str(O/n),bytes=(D/n).stat().st_size,sha256=sha(D/n)) for n in names],'new_model_forwards':0};(D/'payload_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(O/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for filename,text in [('meeting_brief_crosscoder_domain_members_cn.md',f'\n\n## 逐成员token核查表\n\n严格16名的z>0逐成员总量、前三token及完整Top10现已[单独整理]({D}/README_cn.md)，含每token次数与文档覆盖、各成员的三类位置/种类比例。沿用旧留出40篇、6,400位置，不改变正文三张简图；原始次数不直接证明token偏好。\n'),('meeting_brief_crosscoder_domain_members.md',f'\n\n## Per-member token inventory\n\n[Native-positive inventory for every strict16member]({D}/README.md)adds top3/top10and all exact IDs,positive counts,document coverage,and separate position/type category fractions.Same40oldheldoutdocuments/6,400positions;the three main figures remain unchanged.Raw counts do not alone establish token preference.\n')]:
    p=M/filename
    if text.strip() not in p.read_text():p.write_text(p.read_text()+text)
print('READABLE TABLES',str(D))
