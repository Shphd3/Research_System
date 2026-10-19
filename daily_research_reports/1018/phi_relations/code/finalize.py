#!/usr/bin/env python3
"""Qualify selected reading evidence and preserve an immutable delivery manifest."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, re, shutil, subprocess, sys
from PIL import Image
import numpy as np
S=Path('/data/250010109/Research_System')
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
O=E/'analysis/phi_relations_20261018'
C=E/'analysis_tools/phi_relations_20261018'
D=S/'daily_research_reports/1018/phi_relations'
def read(p):return json.loads(Path(p).read_text())
def rows(p):return list(csv.DictReader(Path(p).open()))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def main():
    for p in C.glob('*.py'):shutil.copy2(p,D/'code'/p.name)
    for p in C.glob('*.py'):compile(p.read_text(),str(p),'exec')
    captions=read(D/'provenance/figure_captions.json')
    assert len(captions)==32
    visible=read(D/'provenance/visual_review.json')
    for name in captions:
        assert len(captions[name]['sentences'])==4
        for ext in ['png','pdf','csv']:assert (D/'figures'/f'{name}.{ext}').stat().st_size>0
        with Image.open(D/'figures'/f'{name}.png') as im:
            im.load();assert min(im.size)>=600
        assert sha(D/'figures'/f'{name}.png')==visible['final_png_sha256'][name+'.png']
    assert len(list((D/'figures').glob('*.png')))==32
    members=rows(D/'data/all_members_frequency.csv')
    assert len(members)==13807
    assert len(rows(D/'data/all186_group_index.csv'))==186
    assert len({r['feature_id'] for r in members})==13807
    cases=read(D/'data/cases.json');chain=read(D/'data/chain_cases.json')
    for case in cases+chain:
        assert (D/case['prefix_file']).read_text()==case['visible_prefix']
        assert case['K_full']==len(case['active_members'])
    graphchecks=[]
    for gid in (68,34,14):
        g=f'G{gid:03d}';mm=[r for r in members if int(r['group_id'])==gid]
        memberids={int(r['feature_id']) for r in mm};freq={int(r['feature_id']):float(r['p_V']) for r in mm}
        geo=np.load(D/f'data/geometry_{g}.npz');display=geo['display_feature_id'].tolist()
        edges=rows(D/f'data/frozen_edges_{g}.csv')
        expected={tuple(sorted([int(r['u']),int(r['v'])])):float(r['phi']) for r in edges
                  if int(r['u']) in display and int(r['v']) in display}
        graphed={tuple(sorted([int(r['feature_i']),int(r['feature_j'])])):float(r['phi_D_frozen_edge'])
                 for r in rows(D/f'figures/figure1_{g}_graph.csv')}
        assert expected==graphed
        nodes=rows(D/f'figures/figure1_{g}_nodes.csv')
        assert {int(r['feature_id']) for r in nodes}==set(display)
        assert all(float(r['p_V_full'])==freq[int(r['feature_id'])] for r in nodes)
        casebypos={c['position_id']:c for c in cases if c['group_id']==gid}
        for r in rows(D/f'data/case_{g}_full_matrix.csv'):
            c=casebypos[int(r['position_id'])];active={a['feature_id'] for a in c['active_members']}
            assert sum(int(r[str(f)]) for f in memberids)==c['K_full']
            assert all(int(r[str(f)])==int(f in active) for f in memberids)
        for r in rows(D/f'figures/figure1_{g}_activation.csv'):
            c=casebypos[int(r['position_id'])];active={a['feature_id'] for a in c['active_members']}
            assert all(int(r[str(f)])==int(f in active) for f in display)
            assert int(r['K_full'])==c['K_full']
            assert int(r['K_display'])==len(active&set(display))
        graphchecks.append({'group':g,'full_members':len(memberids),'display_members':len(display),
                            'frozen_edges_full':len(edges),'displayed_original_edges':len(expected)})
    broken=[];linkcount=0
    for p in D.rglob('*.md'):
        for href in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
            if href.startswith(('http:','https:','thread:','app:','codex:','#')):continue
            target=href.split('#')[0]
            if not target:continue
            linkcount+=1
            if not (p.parent/target).exists():broken.append([str(p.relative_to(D)),href])
    assert not broken,broken
    mathcheck=subprocess.run([sys.executable,str(S/'tools/check_markdown_math.py'),
        *[str(p) for p in sorted(D.rglob('*.md'))]],capture_output=True,text=True)
    assert mathcheck.returncode==0,mathcheck.stdout+mathcheck.stderr
    numeric=read(O/'result_validation.json');assert numeric['status']=='PASS'
    assert numeric['additional_chain_case_checks']==12
    assert read(O/'estimator_qualification.json')['status']=='PASS'
    now=datetime.now(timezone.utc).isoformat()
    check={'created_utc':now,'status':'PASS','graphs_against_frozen_edge_source':graphchecks,
        'markdown_local_links':linkcount,'missing_links':broken,'figures_png_pdf_csv':32,
        'all_PNG_decoded_and_visually_reviewed':True,'PDF_independently_rendered':False,
        'members':13807,'groups':186,'case_positions':45,'additional_chain_positions':12,
        'binary_case_matrices_match_actual_same_position_active_members':True,
        'code_compile':'PASS','mathematical_source_check':mathcheck.stdout.strip(),
        'entrypoints_check':'2 pre-existing issues outside changed scope: ntp_learning_mechanisms README_cn missing; diffusion literature untracked',
        'numeric_validation':numeric['status'],'new_forward_calls':0,'training_updates':0,
        'graph_parameters_changed':False,'branch':'master','commit_push':'NOT_REQUESTED_THIS_ROUND',
        'scientific_approval':'Unknown'}
    dump(D/'delivery_checks.json',check)
    excluded={'payload_manifest.json','artifact_manifest.json'}
    files=[]
    for p in sorted(D.rglob('*')):
        if not p.is_file() or p.name in excluded:continue
        files.append({'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p),
            'origin':str(C/p.name) if p.parent.name=='code' and p.suffix=='.py' else
                     str(O/'figures'/p.name) if p.parent.name=='figures' else
                     'Selected derived evidence or reading synthesis; exact sources in input manifest and methods'})
    manifest={'created_utc':now,'owner':str(D),'execution_owner':str(O),
        'purpose':'Selected, auditable reading evidence for the current user-authorized relation-source analysis',
        'selected_payload_exception':True,'no_raw_cache_checkpoint_or_font_payload':True,
        'asset_id':'analysis_crosscoder_phi_relations_sources_20261018',
        'output_access_check':str(S/'assets/checks/2026-10-18_phi_relations_outputs_v2.json'),
        'files':files,'file_count':len(files),'total_bytes':sum(r['bytes'] for r in files)}
    dump(D/'payload_manifest.json',manifest)
    dump(O/'artifact_manifest.json',{'created_utc':now,'reader_owner':str(D),
        'reader_manifest':str(D/'payload_manifest.json'),'reader_manifest_sha256':sha(D/'payload_manifest.json'),
        'asset_id':manifest['asset_id'],'output_access_check':manifest['output_access_check'],
        'raw_saved_results':['panel.npz','conditional_sufficient_G068.npz','conditional_sufficient_G034.npz',
            'conditional_sufficient_G014.npz','activation_G068.npz','activation_G034.npz','activation_G014.npz','geometry_all_pairs.csv'],
        'raw_payload_git':'EXCLUDED','scientific_approval':'Unknown'})
    print('DELIVERY_PASS',len(files),'files',manifest['total_bytes'],'bytes',flush=True)
if __name__=='__main__':main()
