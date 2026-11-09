"""Portable reading/data package; no scientific recomputation."""
from pathlib import Path
import json,hashlib,zipfile,datetime,re,shutil
O=Path(__file__).resolve().parent;R=O.parent;C=json.loads((O/'config.json').read_text());P=Path(C['owner_root']);D=O/'delivery';D.mkdir(exist_ok=True)

def digest(b):return hashlib.sha256(b).hexdigest()

def main():
    # Refresh small code/provenance copies after final engineering edits.
    for q in O.glob('*.py'):shutil.copy2(q,P/'code'/q.name)
    for q in ['audit.json','engineering_notes.json','decoder_and_token_provenance.json']:shutil.copy2(O/q,P/q)
    manifest={'owner':str(P),'execution':str(O),'output_asset_id':(O/'output_asset_id.txt').read_text().strip(),'scope':'cache-only exploratory; real-spectrum blocked; no new forwards','files':[{'path':str(q.relative_to(P)),'bytes':q.stat().st_size,'sha256':digest(q.read_bytes())} for q in sorted(P.rglob('*')) if q.is_file() and q.name not in ['artifact_manifest.json','delivery_receipt.json']],'parent_records_modified':False,'excluded_self_referential_receipt':'delivery_receipt.json'}
    (P/'artifact_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    start='''# 先读这里：R04领域区分性与频率

1. [一页中文结论](summary_cn.md)：只列两条认识更新和一个必要下一步。
2. [图1、图2及图3缺项卡逐轴说明](figures_cn.md)：图3不是谱测量结果。
3. [真实feature算例和反例](examples_cn.md)。
4. [完整数据、公式、匹配不足与范围](detailed_cn.md)。

本包新增模型前向0、拟合分类器0、字典训练0、聚类0、干预0。没有新建Work/Codex任务或资源。旧留出已看过，新增统计全部标为探索性。

`analysis/*_expanded_math64_metrics.csv`和`*_expanded_bio64_metrics.csv`是四个扩大后的固定名单，按发现排序列出；`*_display16_metrics.csv`是主图名单；`*_all_feature_metrics.csv`保留完整字典、资格及失败读数。`selected_token_examples.csv`提供真实token位置/可见前文；`selected_token_hit_summary.csv`是命中次数，不是词选择性。

`source_R04/`保存原始分割/全文/参考窗、四份全坐标汇总、40篇留出逐token缓存、旧候选与旧统计。未包含模型权重或不存在的真实h。`source_manifest.json`和`PACKAGE_MANIFEST.json`给出来源/成员哈希。

复算已有统计可在解压根目录设置环境变量R04_SOURCE_ROOT为source_R04绝对路径后运行analyze.py，再运行render.py；需要numpy/scipy/sklearn/matplotlib，无模型、torch或GPU。候选freeze会逐项核对，不接受新方向替换。读取原decoder和重新提取token例子另需已有原字典与匹配tokenizer及spectral-hier环境，源码见extract_provenance_examples.py。不要自动运行任何新前向；PCA部分等待真实h的单独授权。

图3共同谱缺失：补取完整发现/开发/留出需120篇重放，另最多4检查，FP32两hook约150MiB。没有用重构h或旧语料PCA替代。
'''
    payload={'先读这里.md':start.encode()}
    for p in sorted(O.iterdir()):
        if p.is_file() and p.suffix in ['.py','.md','.json','.txt'] and p.name!='delivery_receipt.json':payload[p.name]=p.read_bytes()
    for sub in ['analysis','figures']:
        for p in sorted((O/sub).iterdir()):
            if p.is_file():payload[str(p.relative_to(O))]=p.read_bytes()
    for f in ['documents.jsonl','context_panel.jsonl','reference.jsonl','source_manifest.json']:
        p=R/'data'/f
        if p.exists():payload['source_R04/data/'+f]=p.read_bytes()
    for d in ['SAE','CC']:
        for phase in ['documents','reference']:
            p=R/f'forward/{phase}_{d}.npz';payload['source_R04/forward/'+p.name]=p.read_bytes()
        for f in [f'{d}_candidate_freeze.json',f'{d}_candidate_document_usage.npz']:
            payload['source_R04/analysis/'+f]=(R/'analysis'/f).read_bytes()
    payload['source_R04/analysis/results.json']=(R/'analysis/results.json').read_bytes()
    docs=[json.loads(s) for s in (R/'data/documents.jsonl').read_text().splitlines()]
    first_discovery=next(x['seq_id'] for x in docs if x['split']=='discovery')
    for row in docs:
        if row['split']=='heldout' or row['seq_id']==first_discovery:
            p=R/'forward/documents'/f"{row['seq_id']}.npz";payload['source_R04/forward/documents/'+p.name]=p.read_bytes()
    for f in ['run_dual_forward.py','pre_forward_freeze.json','amendment_A01.json','forward_ledger.jsonl']:
        payload['source_R04/'+f]=(R/f).read_bytes()
    pm={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{n:{'bytes':len(b),'sha256':digest(b)} for n,b in payload.items()},'PCA':'NOT_RUN_REAL_H_MISSING','new_forwards':0,'new_classifier_fits':0}
    payload['PACKAGE_MANIFEST.json']=json.dumps(pm,ensure_ascii=False,indent=2).encode()
    zpath=D/'R04_领域区分性与频率_64候选_20261028_v1.zip'
    with zipfile.ZipFile(zpath,'w') as z:
        for name,b in payload.items():z.writestr(name,b,compress_type=zipfile.ZIP_STORED if name.endswith(('.npz','.png','.pdf')) else zipfile.ZIP_DEFLATED,compresslevel=6)
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None
        for n,m in pm['files'].items():assert digest(z.read(n))==m['sha256']
        # Internal links in the delivered reading pages. Fragment semantics remain headings, not remote links.
        links=[]
        for name in ['先读这里.md','summary_cn.md','figures_cn.md','examples_cn.md','detailed_cn.md','README.md']:
            s=z.read(name).decode()
            for link in re.findall(r'\]\(([^)]+)\)',s):
                target=link.split('#')[0]
                if target and not target.startswith(('http:','https:')):links.append(target);assert target in z.namelist(),(name,target)
    receipt={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'zip':str(zpath),'bytes':zpath.stat().st_size,'sha256':digest(zpath.read_bytes()),'verified_members':len(pm['files']),'verified_internal_links':len(links),'owner':str(P),'new_forwards':0,'completion':'ALL_CACHE_AVAILABLE_PARTS_DONE; REAL_SPECTRAL_BRANCH_BLOCKED','audit_checks':json.loads((O/'audit.json').read_text())['check_count'],'PCA':'NOT_RUN'}
    (O/'delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(P/'delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False))

if __name__=='__main__':main()
