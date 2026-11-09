"""Full v2reading package, preserving cache-only v1 and original R04."""
from pathlib import Path
import json,zipfile,hashlib,shutil,re,datetime
O=Path(__file__).resolve().parent;S=O.parent;P=Path(json.loads((S/'config.json').read_text())['owner_root']);D=S/'delivery'

def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    for q in O.glob('*.py'):shutil.copy2(q,P/'code/real_spectrum_A01'/q.name)
    current_manifest={'scope':'fullmeasuredA01result;figures1/2unchanged,figure3truePCA','execution':str(S),'raw_and_spectrum':str(O),'output_asset_id':(S/'current_output_asset_id.txt').read_text().strip(),'new_forwards':124,'files':[{'path':str(q.relative_to(P)),'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())} for q in sorted(P.rglob('*')) if q.is_file() and q.name!='artifact_manifest.json' and 'delivery_receipt' not in q.name]}
    (P/'artifact_manifest.json').write_text(json.dumps(current_manifest,ensure_ascii=False,indent=2)+'\n')
    v1=D/'R04_领域区分性与频率_64候选_20261028_v1.zip';v1sha=sha(v1.read_bytes())
    payload={}
    with zipfile.ZipFile(v1) as z:
        for n in z.namelist():
            if n not in ['PACKAGE_MANIFEST.json','先读这里.md']:payload[n]=z.read(n)
    # Replace reading pages/code with current complete records; source_R04/old metrics stay unchanged.
    for q in S.iterdir():
        if q.is_file() and q.suffix in ['.py','.md','.json','.txt'] and 'delivery_receipt' not in q.name:payload[q.name]=q.read_bytes()
    for q in (S/'figures').iterdir():
        if q.is_file():payload['figures/'+q.name]=q.read_bytes()
    for q in O.rglob('*'):
        if q.is_file() and '__pycache__' not in q.parts:payload['real_spectrum_A01/'+str(q.relative_to(O))]=q.read_bytes()
    start='''# 先读这里：R04领域区分性、频率与真实共同谱（完整v2）

1. [一页中文结论](summary_cn.md)：两条认识更新、一个必要下一步。
2. [三图逐轴解释](figures_cn.md)：图1使用次数/强度/含零平均；图2独立频率对文档排序；图3真实共同谱。
3. [真实feature算例与反例](examples_cn.md)。
4. [完整方法、全部集合与边界](detailed_cn.md)。

新增120篇同文档重放+4检查=124/124；两套字典的原激活逐token完全一致。完成两个真实hookPCA和所有可估统计；模型/字典训练、聚类、干预、新资源/任务、TEST均0。原456次不改记，合计580。新64集合按单坐标区分排序，不是旧率比定义直接扩容。

当前谱文件在real_spectrum_A01/analysis。原缓存阶段analysis/results.json中的缺项状态、NOT_MEASURED卡及cache_only_before_amendment目录是历史记录；当前状态看combined_results.json和真实谱结果，不能当成三图之外另一轮独立实验。

查看名单：analysis/*_expanded_math64_metrics.csv、*_expanded_bio64_metrics.csv按发现顺序列出，*_display16_metrics.csv是主图固定16；*_all_feature_metrics.csv保留所有坐标、资格和失败。selected_token_examples.csv给真实token/可见前文。

真实谱：每hook60发现文档×160位置、完整1024维基，16个各64方向排名段。每坐标各PC平方投影/累计量、匹配随机谱、真实方差、域均值差及辅助平方贡献都在real_spectrum_A01/analysis。辅助量不含feature交叉项，不是总解释方差、不归一化到100%。均值差比例的bootstrap范围只描述条件重采样，存在高维非线性偏移，不当成总体覆盖保证。

source_R04保存原文本、分割、四份全坐标汇总、40篇留出及1篇固定发现复放缓存、原名单与旧读数；real_spectrum_A01/raw_documents保存本次全部120篇两个真实hook。没有模型/字典完整权重。重画图不需前向；从真实h复算PCA不需训练；完整decoder重投影还需已登记原字典。所有来源与成员hash见清单，当前统计脚本和图源都已包含。

全部新留出读数是对已讨论数据的探索性再分析。部分旧整组随机匹配池不足仍NA，未强留候选或放宽。图3表明几何位置，不能替代语义真值、因果作用或模型必需性。
'''
    payload['先读这里.md']=start.encode();payload['historical_v1_reference.json']=json.dumps({'path':str(v1),'sha256':v1sha,'status':'cache-onlyhistorical;notcurrentmeasuredstate'},ensure_ascii=False,indent=2).encode()
    pm={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_forwards':124,'original_R04_forwards':456,'PCA_fits':2,'LM_dictionary_training':0,'status':'COMPLETE_ALL_ESTIMABLE_STATISTICS','matching_NA':'original insufficient pools retained','files':{n:{'bytes':len(b),'sha256':sha(b)} for n,b in payload.items()}}
    payload['PACKAGE_MANIFEST.json']=json.dumps(pm,ensure_ascii=False,indent=2).encode()
    path=D/'R04_领域区分性_64候选_含真实共同谱_v2.zip'
    with zipfile.ZipFile(path,'w') as z:
        for n,b in payload.items():z.writestr(n,b,compress_type=zipfile.ZIP_STORED if n.endswith(('.npz','.png','.pdf')) else zipfile.ZIP_DEFLATED,compresslevel=6)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        for n,m in pm['files'].items():assert sha(z.read(n))==m['sha256']
        linkcount=0
        for n in ['先读这里.md','summary_cn.md','figures_cn.md','examples_cn.md','README.md']:
            for target in re.findall(r'\]\(([^)]+)\)',z.read(n).decode()):
                target=target.split('#')[0]
                if target and not target.startswith(('http:','https:')):assert target in z.namelist(),(n,target);linkcount+=1
    assert sha(v1.read_bytes())==v1sha
    receipt={'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'zip':str(path),'bytes':path.stat().st_size,'sha256':sha(path.read_bytes()),'verified_members':len(pm['files']),'verified_internal_links':linkcount,'new_forwards':124,'cap':124,'statistical_PCA_fits':2,'training':0,'model_or_dictionary_parameter_updates':0,'status':'COMPLETE_ALL_ESTIMABLE_STATISTICS','retained_matching_NA':True,'cache_numerical_audit':106,'new_true_spectrum_audit':34,'v1_preserved_sha256':v1sha,'original_R04_manifest_files_unchanged':563}
    (S/'delivery_receipt_v2.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(P/'current_delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False))

if __name__=='__main__':main()
