from pathlib import Path
import csv,hashlib,json,re,shutil,zipfile,datetime
X=Path(__file__).resolve().parents[1]; E=X/'evidence'
R=Path('/data/250010109/Research_System/daily_research_reports/1111/meeting_report')
O=R/'learn_forget_figures/followup2'
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    title='# 1111 组会前补图\n\nAI 分析；研究者判断 Unknown。只用本地 MIG 和 CPU，没有更新参数。[跑前协议](protocol_cn.md)。\n\n'
    sections=[]
    for i in range(1,5):
        p=O/f'{i:02d}_读图.md'
        sections.append(p.read_text() if p.exists() else f'## {i}｜未完成\n\n截至打包没有可交付结果。')
    p=O/'组会前速报_cn.md'
    p.write_text(title+'\n'.join(sections))
    links=re.findall(r'\]\(([^)]+)\)',p.read_text())
    assert all((O/x).is_file() for x in links)
    ev=O/'evidence';ev.mkdir(exist_ok=True)
    for n in ['protocol.sha256','access_before.json','teacher_code_access.json','checkpoints.json','run03.log','run03_retry.log','run04.log']:
        if (E/n).exists():shutil.copy2(E/n,ev/n)
    for src in E.glob('*.json'):
        if src.stem.startswith(('A0_','A5_','MoE_','Dense_')):shutil.copy2(src,ev/src.name)
    f=X.parent/'followup/data/F/samples.json'
    shutil.copy2(f,ev/'F_DEV_EVAL_samples.json')
    c=O/'code';c.mkdir(exist_ok=True)
    for f in (X/'code').glob('*.py'):shutil.copy2(f,c/f.name)
    (c/'README_cn.md').write_text('这些脚本记录生成步骤。前向、缓存与原表仍在服务器原路径；结果包本身不含训练数据、权重或激活。\n')
    audit={'time_Beijing':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'checkpoints_finished':sum(1 for p in ev.glob('*.json') if p.stem.startswith(('A0_','A5_','MoE_','Dense_'))),'sections_finished':[i for i in range(1,5) if (O/f'{i:02d}_读图.md').exists()],'training_updates':0}
    (ev/'delivery_status.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    manifest=O/'文件清单.csv'
    fs=sorted(p for p in O.rglob('*') if p.is_file() and p.suffix not in ('.zip','.tmp','.sha256') and p!=manifest)
    with manifest.open('w') as fp:
        w=csv.writer(fp);w.writerow(['file','bytes','sha256'])
        w.writerows((str(p.relative_to(O)),p.stat().st_size,digest(p)) for p in fs)
    z=O/'1111-组会前补图_结果.zip';tmp=z.with_suffix('.tmp')
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as fp:
        for p in fs+[manifest]:fp.write(p,p.relative_to(O))
    with zipfile.ZipFile(tmp) as fp:
        assert fp.testzip() is None
        for p in fs+[manifest]: assert hashlib.sha256(fp.read(str(p.relative_to(O)))).hexdigest()==digest(p)
    tmp.replace(z); z.with_suffix('.zip.sha256').write_text(digest(z)+'  '+z.name+'\n')
    print(z,z.stat().st_size,json.dumps(audit,ensure_ascii=False))
if __name__=='__main__':main()
