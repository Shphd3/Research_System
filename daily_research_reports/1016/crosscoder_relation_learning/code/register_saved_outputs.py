"""Register actual saved adapter states and analysis, preserving existing assets."""
from pathlib import Path
import json, hashlib, datetime, argparse


def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(8<<20),b''):h.update(b)
    return h.hexdigest()


def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');t.replace(p)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--catalog',required=True)
    a=ap.parse_args();r=Path(a.root);cfg=json.load(open(r/'config/formal_R1_8.json'))
    members=[];runs=[]
    for seed in cfg['paired_seeds']:
        for arm in ('R','F','N'):
            p=r/'learning'/f'seed_{seed}'/arm
            complete=json.load(open(p/'completion.json'));contract=json.load(open(p/'run_contract.json'))
            assert complete['execution_status']=='COMPLETE'
            assert complete['updates']==cfg['updates'] and complete['tokens_seen']==cfg['updates']*cfg['batch_size']
            runs.append({'arm':arm,'seed':seed,'completion':complete,'contract_path':str(p/'run_contract.json')})
            for q in sorted((p/'checkpoints').glob('update_*.json')):
                x=json.load(open(q));state=Path(x['path'])
                if not state.is_absolute():state=(r.parents[2]/state).resolve()
                assert state==q.with_suffix('.pt').resolve(),'Checkpoint sidecar path mismatch'
                digest=sha(state);assert digest==x['sha256']
                members.append({'member_id':f'{arm}_seed{seed}_update{x["step"]}',
                    'path':str(state),'sha256':digest,'bytes':state.stat().st_size,
                    'step':x['step'],'tokens_seen':x['tokens_seen'],'seed':seed,'arm':arm,
                    'selected_final':x['step']==cfg['updates'],'config_sha256':x['config_sha256'],
                    'source_sha256':x['source_sha256'],'digest_evidence':'freshly_rehashed_at_registration'})
    assert sum(m['selected_final'] for m in members)==9
    manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'producer_job_id':'pt-szeffn72',
        'runs':runs,'members':members,'selected_final_count':9,'saved_member_count':len(members),
        'resume_state':'adapters, Adam, RNG, order hash, data cursor, optimizer steps, valid target counters',
        'resume_qualification':'CPU exact Adam test and GPU serialized next-update weights+optimizer exact; external-process resume NOT_QUALIFIED'}
    write(r/'checkpoint_manifest.json',manifest)
    common={'storage_owner':'MoE_Router','projects':['from-attention-to-search','moe-router-execution'],
        'required_projects':[],'notes_cn':['仅登记真实保存与可访问状态，不授予科学批准或问题关闭。']}
    parents=['model_qwen3_0p6b_base','tokenizer_qwen3_0p6b_base',cfg['cache_asset_id'],
        'crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013']
    family={**common,'id':'checkpoint_family_crosscoder_relation_learning_20261015t164000z',
        'category':'checkpoint_family','kind':'frozen_base_terminal_k4_rank32_adapter_complete_states',
        'title_cn':'冻结Qwen3末端K4/r32：R/F/N三种子实际保存状态', 'payload_status':'SOURCE_PRESENT',
        'identity':{'parent_asset_ids':parents,'producer_job_id':'pt-szeffn72','protocol_path':cfg['protocol'],
            'protocol_revision':'R1.8','configuration_sha256':sha(r/'config/formal_R1_8.json'),
            'member_manifest':str(r/'checkpoint_manifest.json'),'member_manifest_sha256':sha(r/'checkpoint_manifest.json'),
            'saved_members':[{'member_id':m['member_id'],'path':m['path'],'sha256':m['sha256'],'step':m['step'],'tokens_seen':m['tokens_seen']} for m in members],
            'interface':{'insertion':'raw last decoder block residual-post, before frozen native final RMSNorm/head',
                'hidden':1024,'experts':4,'rank':32,'trainable_parameters':262144,'active_parameters':65536,
                'adapter_dtype':'FP32','head_projection_dtype':'BF16','zero_up_nonzero_down':True},
            'loss':'real next-token cross entropy over all valid targets; no extra losses',
            'actual_final_updates_each':cfg['updates'],'actual_valid_targets_each':cfg['updates']*cfg['batch_size'],
            'base_frozen':True,'CrossCoder_frozen':True,'head_frozen':True,
            'resume_state':manifest['resume_state'],'resume_qualification':manifest['resume_qualification'],
            'scientific_approval':'UNKNOWN','scientific_question_answered':False},
        'locations':[{'path':str(r/'learning'),'expected':'directory','required':True,'role':'actual complete adapter states',
            'probes':[{'path':m['path'],'expected':'file'} for m in members if m['selected_final']]}],
        'source_paths':[str(r/'checkpoint_manifest.json'),str(r/'config/formal_R1_8.json')]}
    smoke={**common,'id':'checkpoint_crosscoder_relation_learning_smoke_20261015t164000z',
        'category':'model_checkpoint','kind':'adapter_numeric_smoke_complete_state','title_cn':'末端适配器数值Smoke实际step5状态',
        'payload_status':'SOURCE_PRESENT','identity':{'parent_asset_ids':[x if x!=cfg['cache_asset_id'] else 'representation_crosscoder_relation_learning_20261015t164000z' for x in parents],'producer_job_id':'pt-szeffn72',
            'purpose':'engineering smoke only','saved_updates':5,'saved_valid_targets':1280,
            'configuration_path':str(r/'config/smoke.json'),'configuration_sha256':sha(r/'config/smoke.json'),
            'sha256':sha(r/'learning/smoke/resume_smoke.pt'),'resume_state':'adapters, optimizer, RNG, counters/cursor',
            'scientific_question_answered':False},
        'locations':[{'path':str(r/'learning/smoke/resume_smoke.pt'),'expected':'file','required':True,'role':'actual saved engineering smoke state','probes':[]}],
        'source_paths':[str(r/'learning/smoke/smoke.json')]}
    catalog=Path(a.catalog);raw=catalog.read_bytes();x=json.loads(raw)
    for entry in (family,smoke):
        previous=[z for z in x['assets'] if z.get('id')==entry['id']]
        if previous:
            assert previous[0]==entry,'Refusing to change existing asset identity'
        else:x['assets'].append(entry)
    assert catalog.read_bytes()==raw,'Concurrent registry modification; retry from fresh catalog'
    write(catalog,x)
    print(json.dumps({'status':'REGISTERED_ACTUAL_SAVED_STATES','members':len(members),'finals':9,
        'ids':[family['id'],smoke['id']]}))


if __name__=='__main__':main()
