"""Register actual derived outputs and manifests; never reclassify semantic evidence."""
from pathlib import Path
import json,datetime,hashlib,fcntl,os
R=Path('/data/250010109/Research_System');W=R/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030';S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');O=S/'presentation_variants/near_single_domain_20261030';T=S/'presentation_variants/token_context_audit_20261030'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def entry(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=[S/'freeze.json',S/'analysis/position_keys.npz',S/'analysis/native_positions_csr.npz',S/'analysis/token_thresholds.npz',S/'analysis/all_decoder_projection.npz',S/'tables/master_members.csv',S/'tables/token_member_summary.csv',S.parent/'R04_domain_usage_20261027/data/documents.jsonl',S.parent/'R04_domain_usage_20261027/data/reference.jsonl',S.parent/'R04_domain_usage_20261027/forward/documents_CC.npz',S.parent/'R04_domain_usage_20261027/forward/reference_CC.npz',Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')]
sources=[entry(p) for p in inputs];sources.extend(entry(W/'scripts'/n) for n in ['analyze_token_context.py','analyze_near_single_domain.py','token_word_readability.py','match_and_annotate_contexts.py','prefix_annotation_v2.py','near_token_details.py','plot_near_domain_evidence.py','audit_near_domain_evidence.py','package_near_domain_evidence.py','register_near_domain_evidence.py'])
for p in [O,T]:
    (p/'source_manifest.json').write_text(json.dumps({'recorded_utc':now,'parent_asset_id':'analysis_a15_27_04_r10_domain_member_atlas_20261030','files':sources,'checkpoint':'native A22 inherited from parent registration; no checkpoint loaded for this supplement','new_model_forwards':0},indent=2)+'\n')
    files=[entry(f) for f in sorted(p.rglob('*')) if f.is_file() and f.name not in ['artifact_manifest.json','registration_receipt.json','final_delivery_checks.json'] and 'fonts' not in f.relative_to(p).parts]
    (p/'artifact_manifest.json').write_text(json.dumps({'recorded_utc':now,'files':files,'fonts_excluded_nonresearch_dependency':True,'new_model_forwards':0,'human_semantic_review':'PENDING'},indent=2)+'\n')
entries=[]
for identifier,p,title,kind,probes in [
('analysis_a15_27_r10_token_context_audit_20261030',T,'R10完整领域区分名单的真实token与the前后文缓存审计','cache_only_token_identity_context_and_posthoc_audit',['config.json','summary.json','all_token_composition.csv','same_token_domain_comparison.csv','the_semantic_review_blinded.csv','source_manifest.json','artifact_manifest.json']),
('analysis_a15_27_r10_near_domain_token_context_20261030',O,'R10近单域55名成员的频率、真实token及同词面匹配','cache_only_near_domain_members_and_same_token_document_matching',['config.json','freeze.json','summary.json','near95_members.csv','per_member_token_top10.csv','matched_same_token_group_summary.csv','prefix_annotation_v2_codebook.json','near_the_all_occurrences.csv','audit.json','source_manifest.json','artifact_manifest.json'])]:
    identity={'parent_asset_ids':['analysis_a15_27_04_r10_domain_member_atlas_20261030','data_a15_27_r04_domain_native_dual_20261027','tokenizer_qwen3_0p6b_base_official_a5'],'dictionary':'unchanged A22 native shared-z, original gate, block27 residual-post decoder','config_sha256':sha(p/'config.json'),'source_manifest_sha256':sha(p/'source_manifest.json'),'artifact_manifest_sha256':sha(p/'artifact_manifest.json'),'new_model_forwards':0,'training_updates':0,'new_PCA_fit':0,'heldout':'previously exposed; exploratory','human_semantic_referent_review':'PENDING','scientific_acceptance':'Unknown'}
    if p==O:identity.update({'main_members':{'math':31,'biology':24},'strict_members':{'math':14,'biology':15},'freeze_sha256':sha(p/'freeze.json'),'composition_members':{'math':25,'biology':18},'audit_categories_passed':18,'matching_unit':'independent document pair; input-only local/source matching; all frozen members including zeros','coverage_boundary':'source matching on ID279 only6document pairs/10position pairs; no full syntactic or semantic isolation'})
    else:identity.update({'main_members':{'math':433,'biology':527},'composition_members':{'math':371,'biology':472},'the_ID279_heldout_positions':289,'the_family_heldout_positions':333})
    entries.append({'id':identifier,'category':'analysis','kind':kind,'title_cn':title,'projects':['from-attention-to-search'],'required_projects':[],'storage_owner':'MoE_Router execution','payload_status':'ARRAY_FILES_PRESENT','locations':[{'path':str(p),'expected':'directory','required':True,'probes':[{'path':f,'expected':'file','required':True} for f in probes]}],'identity':identity,'source_paths':[str(W/'supplement_near_domain_tokens.md'),str(W/'supplement_near_domain_tokens_cn.md'),str(p/'source_manifest.json'),str(p/'artifact_manifest.json')],'notes_cn':['发现名单冻结；旧留出复核不换人。','真实输入token与事后词形、对象标签分开；人工语义核查仍未完成。','统计与方向几何不证明领域专有知识、功能或因果。']})
catpath=R/'assets/catalog.json'
with (R/'assets/.near_domain_registration.lock').open('w') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX);cat=json.loads(catpath.read_text());oldids={r['id'] for r in cat['assets']};added=[]
    for e in entries:
        if e['id'] in oldids:raise RuntimeError('Refuse duplicate registration: '+e['id'])
        cat['assets'].append(e);added.append(e['id'])
    cat['catalog_amendments'].append({'recorded_at_utc':now,'reason':'Register actually saved cache-only R10 token-context and near-domain supplements; no new model experiment or scientific state transition.','added_asset_ids':added})
    tmp=catpath.with_name('catalog.near_domain.tmp');tmp.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,catpath)
receipt={'recorded_utc':now,'added_asset_ids':added,'catalog_entries_after':len(cat['assets']),'catalog_path':str(catpath),'human_review':'PENDING'}
for p in [O,T]:(p/'registration_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
