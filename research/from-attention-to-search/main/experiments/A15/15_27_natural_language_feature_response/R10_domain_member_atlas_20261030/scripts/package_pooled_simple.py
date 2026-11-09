"""Save concise bilingual interpretation and replace the speaking view, preserving history."""
from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/data/250010109/Research_System');W=Path(__file__).resolve().parents[1];S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');O=S/'presentation_variants/pooled_simple_20261030';D=W/'figure_variants/pooled_simple_20261030';M=R/'daily_research_reports/1031/meeting_report';H=M/'history';H.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
st=json.loads((O/'summary.json').read_text());native=st['token']['native_all'];high=st['token']['high_supported'];assert native['members']==16 and high['members']==12
amend={'revision':'presentation-P1-native-all-activation','original_config_sha256':sha(O/'config.json'),'reason':'User additionally requested activated-token low/middle/high composition and fewer words/bars. Native z>0 explicitly answers all activation; original frozen-p90 high-response results remain separate sensitivity figures.','main_figures':{'figure1':'pooled reference frequency; near55vs all-cached-strict16','figure2':'native-positive token types and member-equal positions; all16','figure3':'native-positive token within-panel frequency; all16'},'unchanged':['A22 dictionary/gate','near55 and discovery-strict29 lists','old per-member high-response thresholds','high-response support gate','original R10 frequency cuts'],'new_scope':'descriptive all120-document zero-opposite subset and all120-document token coverage categories; not independently heldout','new_model_forwards':0}
(O/'presentation_amendment.json').write_text(json.dumps(amend,indent=2)+'\n');shutil.copy2(O/'presentation_amendment.json',D/'presentation_amendment.json')
cn=f'''# 合并简图：单域使用、feature频率与激活token

[English](README.md) · [原R10完整结果]({W}/summary_cn.md) · [发现集冻结补充]({W}/supplement_near_domain_tokens_cn.md)

## 认识更新

**在原频率规则下，近单域和本批严格单域成员都以低中频为主；但单域使用不等于只响应单域词面。严格单域成员也响应两域共用token，而激活位置中的高频token占比与语料背景接近，尚不能称特殊偏好。**

目的：把用户截图第二条结论画成可直接读懂的比例图，并回答严格单域成员响应多少种共用或本批单域token、激活token有多常见。数学、生物合并后每名成员等权。所有图只用缓存；科研接受Unknown。

## 结果分析一：feature自身的发生率

![合并feature频率](figure1_pooled_feature_frequency.png)

横轴为独立DCLM参考激活频率组，纵轴为feature人数比例，柱顶同时标比例和人数。左图原近单域55名，频率可判定52名：低21（40.4%）、中28（53.8%）、高3（5.8%）。右图本批严格单域16名，频率可判定14名：低4（28.6%）、中9（64.3%）、高1（7.1%）。支持不足3/2名保留另表，不算低频。

参考频率=独立DCLM中原生z>0次数/65,536，至少20次；原切点0.259399414%和1.344299316%，相等归低一组。该规则下中频最多，不能把“中频”当所有分组规则下的不变标签；旧log敏感性仍保留。

三份名单必须分开：①近单域55（31数学+24生物），发现集偏向域≥5篇、另一域≤1篇、≥95%正激活位置来自偏向域；②发现集严格单域29（14+15），发现集另一域零激活，旧留出仍严格21名；③**本批严格单域16（7+9）**，从29名中要求全部120缓存文档的另一域60篇、9,600分析位置均零激活。16是本次追加的描述性子集，不替换55或29。

“全缓存严格”只指本批分析位置，不能称全语料领域专有。它用到了开发及旧留出，因此下面不是独立留出泛化证据。没有按频率或token图再挑成员。

## 结果分析二：响应多少种token，各占多少位置？

![token类别数量与激活位置](figure2_strict_token_categories.png)

两图均为严格16名，在旧留出40篇×160位置=6,400位置观察原生z>0。左图对不同token ID去重，纵轴为种类比例；右图先在每名feature内算位置比例，再对16名等权。两种百分比的分母不同，不能互换。

| token类别 | 不同ID数／1,182 | 种类占比 | 成员等权激活位置占比 |
|---|---:|---:|---:|
| 两域共用 | 108 | 9.1% | 33.1% |
| 本批单域 | 48 | 4.1% | 8.6% |
| 其他／支持不足 | 1,026 | 86.8% | 58.3% |

“常用”在此落实为可核对的“两域共用”，不是凭词义判断。**本次新描述分类**使用全部120篇输入：两域各≥5篇出现为共用；一域≥5篇且另一域0篇出现为本批单域；其余为其他／支持不足。单域类别会包含子词、数学符号和格式，不能自动称领域术语。精确ID、标点、大小写和空格均保留。[逐token表](token_ID_details.csv)可查看具体词形与两域文档覆盖。

这套全缓存分类与前版“发现集冻结、偏域允许另一域≤1篇”的分类不同，旧结果不重写、不直接拼接。它回答当前语料内的覆盖，不能作为独立语义验证。其他类别尚不能判断，也不能全部叫通用或领域专有。

同文档暴露量匹配背景，共用42.7%、本批单域5.2%、其他52.1%；全部可用位置背景为43.3%/5.2%/51.5%。共用位置有激活不等于对共用词富集；本批单域8.6%相对背景5.2%是描述性组成偏移，尚无语义或因果认定。

## 结果分析三：激活token的低中高频组成

![激活token词频](figure3_activated_token_frequency.png)

横轴为token语料内频率组，纵轴为成员等权激活位置比例。数学、生物合并；同一16名，原生z>0。低频14.1%、中频9.3%、高频76.6%。

词频计数沿用原R10：在全部120篇有效19,200位置上统计同一tokenizer的精确ID，按token类型计数分位点1、2分组，计数并列不拆分。低=出现1次，中=2次，高=至少3次。“高频”是本批类型分组，不是日常语言或全语料常用程度。类型数与位置数见[token频率表](token_frequency_composition.csv)，此图纵轴分母为激活位置，不是token类型数。

全部可用位置的高频token占77.1%，与激活位置76.6%接近。因此“激活大多发生在高频token上”成立，但“特别偏好高频token”尚未建立。feature的DCLM频率与这里的token词频是两个不同变量。

## 原高响应阈值对照、方法变化与复现

原发现集正激活p90阈值没有改变；作为单独[高响应词频图](appendix_high_token_frequency.png)及[高响应类别图](appendix_high_token_categories.png)保留。16名中12名满足原≥5高响应位置、≥2文档的构成支持，4名支持不足不换人。12名高响应对应243种ID：共用61种（25.1%）、本批单域15种（6.2%）、其他167种（68.7%）；成员等权高响应位置比例35.5%/14.1%/50.4%，低中高词频12.4%/7.9%/79.7%。原生激活与高响应不能混用分母。

本轮变化明确为：数学/生物合并；追加全缓存零异域16名描述子集；全缓存token覆盖分类；新增原生z>0的全激活视图。旧发现名单、分类、阈值与结果全部保留。presentation_amendment.json记录了新增全激活主视图与旧高响应附录的关系。没有新增模型前向、训练、PCA或领域。

原始绘图数据、16名名单、29/55映射、每成员组成、确切token ID及语料计数、输入与输出哈希均在本目录；原始缓存留执行侧。核查包括：16名均属于旧29、全部异域分析位置零激活、高响应计数与原表逐成员一致、ID去重以及比例合计1。脚本为`{W}/scripts/pooled_simple_figures.py`，再运行`package_pooled_simple.py`整理稿件；使用本地spectral-hier Python，零模型调用。

汇报追问：**为什么能区分“数量多”与“偏好”？** 比较激活位置和全部可用位置的组成，并保留同文档背景。**为什么不能说领域语义专有？** 单域只在本批中观察到，类别含格式/子词，大量token支持不足，且未进行对象语义人工确认或因果干预。缓存补统计与简图完成后停止。
'''
en=f'''# Pooled simple figures: single-domain use, feature frequency and activated tokens

[中文](README_cn.md) · [Parent R10]({W}/summary.md) · [Discovery-frozen supplement]({W}/supplement_near_domain_tokens.md)

## Belief update

**Under the original frequency bins, near-domain and panel-strict members concentrate in low/middle reference ranges. Single-domain use does not imply lexical exclusivity: members activate on shared token surfaces, while the high-frequency-token share is close to input composition and does not establish special preference.**

Pool math and biology with equal member weights. Three sets remain distinct: near55(31/24),discovery-strict29(14/15),and a new descriptive all-cached-strict16(7/9). The last requires zero native activation in every opposite-domain analysis position across all120documents,including development/oldheldout. It does not replace frozen discovery lists or establish independent heldout generalization. No frequency/token outcome determines membership; no global exclusive-knowledge claim.

## Analysis1: feature reference frequency

![Feature frequency](figure1_pooled_feature_frequency.png)

X:low/middle/high independent DCLM frequency.Y:classified-member count fraction.Near55has52classified:21/28/3(40.4/53.8/5.8%).Panel-strict16has14classified:4/9/1(28.6/64.3/7.1%).Three/two insufficient-reference members remain in tables.Frequency=z>0count/65,536;≥20hits;original lower-inclusive cuts.002593994140625/.0134429931640625.Majority-bin names depend on the binning rule;oldlog sensitivity is retained.

## Analysis2: distinct activated types versus activated positions

![Token categories](figure2_strict_token_categories.png)

Same16members,nativez>0,on6,400oldheldoutpositions.X:shared/panel-single-domain/other.LeftY:deduplicated exact-token-ID fraction;rightY:position fraction normalized within each member then averaged.1,182types comprise108shared(9.1%),48panel-single-domain(4.1%),1,026other/insufficient(86.8%).Member-equal activated-position shares33.1%/8.6%/58.3%.Do not confuse type and position denominators.

NEWdescriptive input categories use all120documents:shared appears in≥5documents in EACH domain;panel-single-domain in≥5of one and0of the other;remainingother/insufficient.This differs from the older discovery-frozen,≤1opposite-document associated category;old numbers are preserved rather than relabeled.It is a panel coverage description,not semantic ground truth;subwords,format and symbols remain.Shared surfaces operationalize the requested common-token comparison without assuming high frequency or generic meaning.Exact IDs/strings/document support are in token_ID_details.csv.

All-position background is43.3/5.2/51.5%;document-exposure-matched42.7/5.2/52.1%.Shared-token activation is not shared-token enrichment.Panel-single-domain8.6%versus5.2%is an observational composition shift,not semantic or causal evidence.

## Analysis3: frequency of activated tokens

![Token frequency](figure3_activated_token_frequency.png)

X:within-panel exact-ID type-count groups(low1,middle2,high≥3);Y:member-equal activated-position share.Native16gives14.1/9.3/76.6%.Groups preserve originalR10type-count quantiles1/2and ties over19,200validpositions.High here is panel-relative,not global everyday vocabulary.Type and position counts are separate in token_frequency_composition.csv.The all-available-position high-frequency share is77.1%,close to76.6%,so a high share alone does not demonstrate preference.Token frequency and DCLM FEATURE frequency remain distinct.

## Preserved high-response sensitivity and reproduction

Frozen discovery-positivep90thresholds are unchanged.12/16members meet original≥5high positions/2documents support;4remain insufficient.High-response243types split61shared/15single/167other,type fractions25.1/6.2/68.7%;member-equal high-position fractions35.5/14.1/50.4%;token-frequency fractions12.4/7.9/79.7%.See appendix_high_token_categories.png and appendix_high_token_frequency.png.Native and high-response denominators are not mixed.

presentation_amendment.json declares the new all-activation main view and preserved high-response appendix.Raw plotting/member/coverage tables and exact IDs,config/freeze/source/output hashes are saved.Old lists,thresholds,classification and findings remain unchanged.Checks verify parent-subset identity,all opposite counts zero,original high counts,equal-member weighting,deduplication and sum-to-one.No new forward/training/PCAfit/domain.Canonical raw caches remain execution-side.Reproduce with local spectral-hierPython scripts/pooled_simple_figures.py then scripts/package_pooled_simple.py.Scientific acceptance remains Unknown;no semantic referent labels or causal functional result were added.Stop after this cached supplement.
'''
for name,body in [('README_cn.md',cn),('README.md',en)]:
    (D/name).write_text(body);(O/name).write_text(body)
history=[]
for name,body in [('meeting_brief_crosscoder_domain_members_cn.md',cn),('meeting_brief_crosscoder_domain_members.md',en)]:
    p=M/name;old=H/(p.stem+'_pre_pooled_simple_20261030.md')
    if not old.exists():shutil.copy2(p,old)
    # Absolute figure/data paths keep one stable speaking entry across folders.
    import re
    body=re.sub(r'\]\(([^)]+)\)',lambda m:']('+str(D/m.group(1))+')' if not m.group(1).startswith(('/', 'http','#')) else m.group(0),body)
    body+='\n\n'+('此前上下文对照与完整三项认识保留在[历史稿](' if name.endswith('_cn.md') else 'Prior context controls and full discussion are preserved in[history](')+str(old)+').\n'
    p.write_text(body);history.append(dict(path=str(old),sha256=sha(old)))
(O/'meeting_history_receipt.json').write_text(json.dumps(history,indent=2)+'\n');shutil.copy2(O/'meeting_history_receipt.json',D/'meeting_history_receipt.json')
for name,link,text in [('supplement_near_domain_tokens_cn.md','README_cn.md','最新合并简图：追加全缓存严格16名与原生激活token统计；这是另列描述性口径，不替换本页发现集冻结结果。'),('supplement_near_domain_tokens.md','README.md','Latest pooled simple figures add an all-cached-strict16descriptive subset and native-positive token views;they do not replace this page\'s discovery-frozen results.')]:
    p=W/name;mark='\n\n['+text+'](figure_variants/pooled_simple_20261030/'+link+')\n'
    if mark.strip() not in p.read_text():p.write_text(p.read_text()+mark)
pro=json.loads((O/'provenance.json').read_text());pro['sources'].append(dict(path=str(Path(__file__).resolve()),bytes=Path(__file__).stat().st_size,sha256=sha(Path(__file__).resolve())));(O/'provenance.json').write_text(json.dumps(pro,indent=2)+'\n');shutil.copy2(O/'provenance.json',D/'provenance.json')
manifest=json.loads((D/'payload_manifest.json').read_text());names={r['path'] for r in manifest['files']}|{'README.md','README_cn.md','presentation_amendment.json','meeting_history_receipt.json'};manifest['files']=[dict(path=n,origin=str(O/n),bytes=(D/n).stat().st_size,sha256=sha(D/n)) for n in sorted(names)];(D/'payload_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(O/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PACKAGED SIMPLE THREE-FIGURE SPEAKING VIEW',str(D))
