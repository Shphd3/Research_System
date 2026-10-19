#!/usr/bin/env python3
"""Validate and inventory the completed frozen-group input-spectrum supplement."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import re
import shutil
import subprocess
import numpy as np

S = Path('/data/250010109/Research_System')
E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
B = E/'analysis/report_spectrum/20261016_phi_input_spectrum'
D = S/'daily_research_reports/1016/crosscoder_phi_input_spectrum'
OLD = S/'daily_research_reports/1016/crosscoder_report_supplement'
ASSET = 'analysis_crosscoder_phi_group_input_spectrum_20261016'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    shutil.copy2(Path(__file__),D/'code'/Path(__file__).name)
    for p in (B/'audit').iterdir():
        if p.is_file():
            shutil.copy2(p,D/'provenance'/('audit_'+p.name))
    body = (D/'report_cn.md').read_text()
    for caption in ('统计对象：','计算方法：','实际观察：','推断边界：'):
        assert body.count(caption) == 4
    assert '33个真实位置×3条件的99次' in body and '99个真实位置' not in body
    assert 'phi_context_diagnostic.py' in (D/'data_dictionary_cn.md').read_text()
    assert '原/余共同人口mask' not in (D/'data_dictionary_cn.md').read_text()
    resolution = {
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS_ALL_THREE_TEXT_CORRECTIONS',
        'audit':'audit_delivery_text_audit_cn.md',
        'corrections':['33 actual positions x 3 arms, not 99 distinct positions',
                       'separate main, plotting, and posthoc producers',
                       'per-arm flags in NPZ, common lists in plot_selection.json'],
        'no_recomputation_or_frozen_definition_change':True,
    }
    (D/'provenance/delivery_text_audit_resolution.json').write_text(json.dumps(resolution,indent=2)+'\n')
    selection = json.loads((D/'provenance/plot_selection.json').read_text())
    selected = np.array(selection['group_ids'])
    assert len(selected)==145
    metrics = list(csv.DictReader((D/'data/per_group_input_hidden_metrics.csv').open()))
    assert len(metrics)==558 and len({(r['condition'],r['group_id']) for r in metrics})==558
    sizes = []
    for arm, sufficient in zip('RFN',(176,168,171)):
        with np.load(D/'data'/f'{arm}_input_hidden_spectra.npz') as z:
            assert z['normalized_original'].shape == z['normalized_residual'].shape == (186,1024)
            assert z['support_qualified'].sum() == sufficient
            for field in ('normalized_original','normalized_residual'):
                assert np.isfinite(z[field][selected]).all()
                assert np.allclose(z[field][selected].sum(1),1)
            assert (z['sampled_cache_row'][selected]>=0).all()
            assert all(len(np.unique(x))==128 for x in z['sampled_cache_row'][selected])
            sizes.append(z['group_size'][selected])
    assert all(np.array_equal(sizes[0],other) for other in sizes[1:])
    assert sizes[0].sum()==8814
    assert len(list((D/'figures').glob('*.png')))==len(list((D/'figures').glob('*.pdf')))==4
    for p in (D/'figures').iterdir():
        assert sha(p)==sha(B/'figures'/p.name)
    assert json.loads((D/'provenance/audit_result_audit.json').read_text())['status']=='PASS_RESULT_IDENTITY_AND_BOUNDED_INTERPRETATION'
    replay = json.loads((D/'provenance/replot_verification.json').read_text())
    assert replay['status']=='PASS'
    files = [str(p) for p in D.rglob('*.md')]
    math = subprocess.run(['python',str(S/'tools/check_markdown_math.py')]+files,capture_output=True,text=True)
    assert math.returncode==0,math.stdout+math.stderr
    links=0
    for p in D.rglob('*.md'):
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^\)\n]+)\)',p.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):
                continue
            assert (p.parent/target.split('#')[0]).resolve().exists(),(p,target)
            links+=1
    # The previous report must remain an exact prefix, including all its paragraphs.
    prior = json.loads((OLD/'artifact_manifest.json').read_text())
    prior_report = next(r for r in prior['files'] if r['path']=='report_cn.md')
    prefix = (OLD/'report_cn.md').read_text().split('\n**追加：原φ关系组对应输入的原始表征谱。**')[0]
    prefix_sha=hashlib.sha256(prefix.encode()).hexdigest()
    preservation = {
        'status':'PASS_EXACT_PRIOR_REPORT_PREFIX',
        'prior_manifest_sha256':sha(OLD/'artifact_manifest.json'),
        'prior_report_sha256':prior_report['sha256'],
        'current_prefix_sha256':prefix_sha,
        'original_report_file':str(OLD/'report_cn.md'),
        'scope':'only append one reading paragraph; no edits to previous report body',
    }
    if prefix_sha != prior_report['sha256']:
        # Re-running after the old bundle has been re-inventoried retains the
        # first completed prefix receipt rather than inventing a new before hash.
        previous=D/'provenance/original_report_append_preservation.json'
        assert previous.exists()
        kept=json.loads(previous.read_text())
        assert kept['current_prefix_sha256']==prefix_sha
        preservation=kept
    (D/'provenance/original_report_append_preservation.json').write_text(json.dumps(preservation,indent=2)+'\n')
    forbidden=[str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and
               (p.suffix in ('.pt','.pth','.bin','.safetensors','.npy','.log','.otf','.ttf','.pyc') or '__pycache__' in p.parts)]
    assert not forbidden,forbidden
    inventory=[{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)}
               for p in sorted(D.rglob('*')) if p.is_file() and p.name not in ('artifact_manifest.json','delivery_checks.json')]
    manifest={
        'created_utc':datetime.now(timezone.utc).isoformat(),'files':inventory,
        'inventory_excludes':['artifact_manifest.json','delivery_checks.json'],
        'asset_id':ASSET,
        'input_asset_ids':['representation_crosscoder_relation_learning_eval512_20261015t164000z',
                           'representation_crosscoder_relation_learning_20261015t164000z',
                           'analysis_crosscoder_feature_frequency_20261015t143300z',
                           'analysis_crosscoder_relation_learning_20261015t164000z'],
        'selected_evidence_exceptions':['four PNG/PDF pairs','three small derived spectra/sampling-ID NPZ','CSV summaries and provenance'],
        'execution_root':str(B),'source_manifest':'provenance/source_manifest.json',
        'scope':'Frozen186 phi R/F/N group-winning raw input spectra and per-group-centered-PC1 residual spectra',
        'scientific_approval':'Unknown','question_closure':'Unknown',
    }
    (D/'artifact_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for item in inventory:
        assert sha(D/item['path'])==item['sha256']
    checks={
        'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_EXECUTION_AND_DELIVERY_NOT_SCIENTIFIC_APPROVAL',
        'asset_id':ASSET,'all_condition_group_rows':558,'supported_group_arms':515,
        'main_common_groups':145,'main_member_fraction':8814/13807,'sample_N_per_group':128,
        'figures_png_pdf':4,'PNG_all_visually_inspected':True,'PDF_independently_rendered':False,
        'independent_replot':replay,'math_source_check':math.stdout.strip(),
        'math_rendering_verified':False,'local_links_verified':links,
        'artifact_files_verified':len(inventory),'manifest_sha256':sha(D/'artifact_manifest.json'),
        'new_training_updates':0,'new_model_forwards':0,'graph_parameter_changes':0,'new_branches':0,
        'prior_report_exact_prefix_preserved':True,'forbidden_payloads':forbidden,
    }
    (D/'delivery_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    (B/'delivery_receipt.json').write_text(json.dumps({
        'report_root':str(D),'manifest_sha256':checks['manifest_sha256'],
        'checks':str(D/'delivery_checks.json'),'asset_id':ASSET,
        'summary':str(B/'phi_input_hidden_summary.json'),'scientific_approval':'Unknown',
    },indent=2)+'\n')
    print(json.dumps({k:checks[k] for k in ('status','main_common_groups','artifact_files_verified','local_links_verified')},ensure_ascii=False))

if __name__ == '__main__':
    main()
