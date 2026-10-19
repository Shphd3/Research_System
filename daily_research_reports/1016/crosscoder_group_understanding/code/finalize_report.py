"""Check the derived reading deliverable and record actual saved output identity."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,re,subprocess,shutil,collections
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
S=Path('/data/250010109/Research_System');R=E/'analysis/group_understanding'
D=S/'daily_research_reports/1016/crosscoder_group_understanding';OLD=E/'analysis/feature_frequency/20261015T143300Z'
CODE=E/'analysis_tools/group_understanding'
def read(p):return json.loads(p.read_text())
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main():
 shutil.copy2(Path(__file__),D/'code'/Path(__file__).name)
 audit='''# 解释审计与交付核对\n\n这是现有结果的逐组阅读，不是新增训练、模型推理或分组实验。审计由Codex /root、group_index_export、group_case_cache、group_case_figures完成，最终判断仍不代替研究者科学批准。\n\n## 第一轮：避免把算法产物解释成语义\n\n小组G87把六对共同次数和phi全部摊开：四对满足原互为前10邻居条件，两对虽phi为正却不满足，因而没有边。原图为三角加一条桥，四人构成独立连通分量；没有保存逐步合并日志，因此只说明已保存算法与结果，不编造合并先后。\n\n反驳“同组就是都很像”：G34未筛选全对phi中位仅0.00125，约42.1%为负；保留边却较强。互选前10名规则本来就使度≤10，故低密度本身不足以反驳相似性，必须同时看全对分布与桥。图的几何距离也不是新的相似度测量。\n\n## 第二轮：核对稳定性分母和图的覆盖\n\nG74有12/14原成员留在同一个98人V组，Jaccard=.12包含大量新成员；不能称为多数原成员消失。全局一对一匹配的J=0也不保证没有重叠，索引补充不受占位约束的最佳V组（含V单例），并保留原匹配，不替换注册统计。\n\nG34图明确只展示30/149人、85/310条原组内部边，基于D侧最大内度和固定广度优先规则选择，偏向高连接核心。显示的30人恰好全留在匹配V组，整组却只有86/149保留；正文同时呈现，不能外推。频率图和成员表包含全部149人。\n\n“容易变化”需要多次新划分或时间数据，本轮没有。当前只能报告谁在已有D/V和既有q20复核中没有留在匹配组，以及其实际去向；未测长期稳定性明确标注。\n\n## 第三轮：文本不能替代主题或机制证据\n\n18条均来自既有样本，不补采。随机是命中context哈希抽样而非token均匀；高分是活跃成员数占比而非z幅度，且同分优先较早位置。病例文本只显示可能共同点及反例：G87语境分散，G74的邮件字符段被非邮件ID例限制，G34跨话题共享当前of片段；不强命名主题。\n\n旧target_token字段实际是当前已见t，本报告分开当前t和预测位置t+1。下一token是真实语料标签，既不在模型可见前缀中，也不是模型argmax；实际模型预测未保存。18个完整前缀和全部非零z逐一复核，另有1002个含零成员值，无top-k截断。原文档ID与独立性仍未知。\n\n## 最后修正与实际检查\n\n修复了极低非零频率被三位小数显示成0.000%的问题，改用六位有效数字；区分命中次数和频率单位。数学公式只做来源/源码规范检查，不声称逐平台渲染验证。六张PNG逐张实际查看，统计与图覆盖交叉核对通过。\n\n完整检查见[delivery_checks.json](delivery_checks.json)，来源和字节哈希见[artifact_manifest.json](artifact_manifest.json)。这些检查证明当前派生表和解释一致，不证明语义、因果或共同学习相容。\n'''
 (D/'reasoning_audit_cn.md').write_text(audit)
 groups=[g for g in read(OLD/'main/groups_D.json') if g['size']>1]
 idx=rows(D/'tables/all_groups_index.csv');members=rows(D/'tables/all_group_members.csv')
 assert len(idx)==len(groups)==186 and len(members)==13807
 lookup={int(r['feature_id']):r for r in members};freq={int(r['feature_id']):r for r in rows(OLD/'frequency.csv')}
 assert len(lookup)==13807
 expected={g['group_id']:set(g['members']) for g in groups}
 for r in idx:
  gid=int(r['group_id']); local=rows(D/'tables'/r['members_csv'])
  assert set(int(x['feature_id']) for x in local)==expected[gid]
  assert len(local)==int(r['size'])
  assert len(rows(D/'tables'/r['edges_csv']))==int(r['internal_edges_D'])
  assert float(r['p_D_min'])>0 and float(r['p_V_min'])>0
 for row in members:
  f=freq[int(row['feature_id'])]
  for k in ['n_D','n_V','p_D','p_V']:
   assert float(row[k])==float(f[k])
 assert not any(v=='' for r in idx+members for v in r.values())
 for gid,n in [(87,4),(74,14),(34,149)]:
  pairs=rows(D/f'tables/cases/group_{gid:03d}_all_pairs.csv')
  assert len(pairs)==n*(n-1)//2
  for p in pairs:
   assert 0<=int(p['joint_D'])<=min(int(p['n_u_D']),int(p['n_v_D']))
   assert 0<=int(p['joint_V'])<=min(int(p['n_u_V']),int(p['n_v_V']))
  body=(D/f'cases/group_{gid:03d}_cn.md').read_text()
  assert body.count('### 随机')==3 and body.count('### 高分')==3
  member_lines=[line for line in body.splitlines() if re.match(r'^\| \d+ \|',line)]
  assert len(member_lines)==n
 cases=read(D/'text_evidence/selected_cases.json')['cases']
 assert len(cases)==18
 assert collections.Counter((e['group_id'],e['sample_type']) for e in cases)==collections.Counter({(g,t):3 for g in [87,74,34] for t in ['random','high_score']})
 old={(e['group_id'],e['sample_type'],e['eligible_position']):e for e in read(OLD/'inputs/examples.json')['examples']}
 for e in cases:
  original=old[e['group_id'],e['sample_type'],e['eligible_position']]
  assert e['model_visible_prefix']==original['model_visible_prefix']
  assert (D/'text_evidence'/e['model_visible_prefix_file']).read_text()==e['model_visible_prefix']
  assert e['prediction_position_context_offset_zero_based']==e['current_context_offset_zero_based']+1==e['visible_prefix_token_count']
  assert len(e['active_members_complete'])==e['active_member_count']
  assert len(e['all_members_gated_z'])==e['group_size']
  assert {x['feature_id']:x['z'] for x in e['active_members_complete']}=={x['feature_id']:x['z'] for x in original['feature_values']}
 allz=rows(D/'text_evidence/selected_case_all_member_z.csv');assert len(allz)==1002
 for gid in [87,74,34]:
  appendix=(D/f'cases/group_{gid:03d}_texts_cn.md').read_text()
  blocks=re.findall(r'```text\n(.*?)\n```',appendix,re.S)
  assert blocks==[e['model_visible_prefix'] for e in cases if e['group_id']==gid]
 coverage=rows(D/'figures/graph_coverage.csv')
 assert [(int(r['displayed_nodes']),int(r['frequency_plot_members'])) for r in coverage]==[(4,4),(14,14),(30,149)]
 assert len(list((D/'figures').glob('*.png')))==6
 assert len(list((D/'figures').glob('*.pdf')))==6 and len(list((D/'figures').glob('*.svg')))==6
 for p in (D/'source_tables').iterdir():
  source=OLD/p.name if p.name in ['frequency.csv','registered_config.json'] else OLD/'main'/p.name
  assert sha(p)==sha(source)
 excluded=[str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and (p.suffix in ['.pt','.pth','.bin','.safetensors','.npy','.npz','.jsonl','.log','.ttf','.otf'] or '__pycache__' in p.parts)]
 assert not excluded,excluded
 mathcheck=subprocess.run(['python',str(S/'tools/check_markdown_math.py'),str(D/'cases/group_087_cn.md')],capture_output=True,text=True)
 assert mathcheck.returncode==0,mathcheck.stdout+mathcheck.stderr
 manifest_path=D/'artifact_manifest.json';checks_path=D/'delivery_checks.json'
 # Both files are separately verifiable; the inventory excludes its own hash and the validation receipt.
 dump(manifest_path,{'status':'inventory_preparation'})
 dump(checks_path,{'status':'validation_preparation'})
 local_links=0
 for p in D.rglob('*.md'):
  for target in re.findall(r'!?\[[^\]\n]*\]\(([^\)\n]+)\)',p.read_text()):
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
   dest=(p.parent/target.split('#')[0]).resolve()
   assert dest.exists(),(p,target)
   assert dest.is_relative_to(D.resolve()),(p,target)
   local_links+=1
 files=[]
 for p in sorted(D.rglob('*')):
  if not p.is_file() or p in [manifest_path,checks_path]:continue
  rel=p.relative_to(D)
  part=rel.parts[0]
  origins={'tables':R/'20261016_tables','figures':R/'20261016_figures','text_evidence':R/'20261016_cases','code':CODE}
  source=origins[part]/Path(*rel.parts[1:]) if part in origins else None
  note='reading derivative; original fixed sources remain unedited'
  if part=='text_evidence' and p.name=='selected_cases.json':note='prefix file paths rebased; original absolute path retained separately'
  if part=='source_tables':source=OLD/p.name if p.name in ['frequency.csv','registered_config.json'] else OLD/'main'/p.name
  files.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p),'origin':str(source) if source else 'generated by code/build_report.py or code/finalize_report.py','purpose':note})
 manifest={'created_at_utc':datetime.now(timezone.utc).isoformat(),'processing_agent':'Codex /root','files':files,'inventory_excludes':['artifact_manifest.json','delivery_checks.json'],'source_hashes':['tables/source_manifest.json','figures/source_manifest.json','text_evidence/extraction_receipt.json'],'selected_evidence_exception':'only curated figures, count-derived CSV,18 existing text cases and provenance; no model/cache payload','training_updates':0,'model_forward_calls':0,'new_encoded_positions':0,'new_graph_fits':0,'graph_parameter_changes':0,'scientific_approval':'Unknown','question_closure':'Unknown'}
 dump(manifest_path,manifest)
 for x in files:assert sha(D/x['path'])==x['sha256']
 checks={'created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_DERIVED_READING_DELIVERABLE_NOT_SCIENTIFIC_APPROVAL','group_index_rows':186,'complete_member_rows':13807,'per_group_member_and_edge_files':186,'case_group_sizes':[4,14,149],'text_cases':18,'random_and_high_per_case_group':[3,3],'all_member_case_z_rows_including_zero':1002,'prefix_text_exact_checks':18,'complete_nonzero_z_exact_checks':18,'full_prefix_appendix_checks':3,'case_pair_table_rows':[6,91,11026],'figures':{'types':6,'formats':['png','pdf','svg'],'visual_checks':'figures/figure_audit.json','partial_large_graph':'30/149nodes;85/310edges;149member frequency/table'},'local_markdown_links_checked':local_links,'missing_links':[],'links_outside_deliverable':[],'math_source_check':mathcheck.stdout.strip(),'math_rendering_verified':False,'forbidden_payloads':excluded,'original_source_copies_byte_equal':True,'artifact_files_verified':len(files),'artifact_manifest_sha256':sha(manifest_path),'original_graph_config':{'q':10,'resolution':1,'min_D_hits':100,'min_D_blocks':10,'joint_min':10},'model_inference_training_new_graph_runs':0}
 dump(checks_path,checks)
 output={'created_at_utc':checks['created_at_utc'],'report_root':str(D),'report_manifest':str(manifest_path),'report_manifest_sha256':sha(manifest_path),'delivery_checks':str(checks_path),'source_table_root':str(R/'20261016_tables'),'source_case_root':str(R/'20261016_cases'),'source_figure_root':str(R/'20261016_figures'),'training_updates':0,'new_graph_fits':0,'groups':186,'members':13807,'cases':18,'figures':6,'scientific_approval':'Unknown'}
 dump(R/'20261016_delivery.json',output)
 print(json.dumps({'status':checks['status'],'report_root':str(D),'files':len(files),'links':local_links,'training':0,'graph_fits':0},ensure_ascii=False))
if __name__=='__main__':main()
