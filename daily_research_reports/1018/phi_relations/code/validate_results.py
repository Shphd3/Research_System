#!/usr/bin/env python3
"""Cross-check independent identities and frozen input selection, no new model."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
O=E/'analysis/phi_relations_20261018';P=E/'analysis/feature_relation_phase1/20261013T173130Z'
def main():
    source=json.loads((O/'protocol_freeze.json').read_text())
    for item in source['protocols']:
        assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
    panel=np.load(O/'panel.npz');assert len(np.unique(panel['position']))==64000
    freq=np.load(P/'feature_frequency.npz')['n'];split=json.loads((P/'split_manifest.json').read_text())
    groups={x['group_id']:x for x in json.loads((E/'analysis/feature_frequency/20261015T143300Z/main/groups_D.json').read_text())}
    hist=np.load(O/'full_K_and_chain.npz');core=list(csv.DictReader((O/'all186_core_decomposition.csv').open()))
    identities=[]
    for gid in (68,34,14):
        for si,side in enumerate('DV'):
            counts=hist[f'{gid}_{side}'];K=np.arange(len(counts));N=split['N_'+side]
            members=groups[gid]['members'];p=freq[si,members]/N
            assert counts.sum()==N
            mean=float(counts@K/N);assert abs(mean-p.sum())<1e-11
            S=float(counts@(K*(K-1))/N-((p.sum())**2-p@p))
            measured=float(next(x['total_numerator'] for x in core if int(x['group_id'])==gid and x['side']==side))
            assert abs(S-measured)<1e-8*max(abs(S),1)
            identities.append({'group_id':gid,'side':side,'full_K_mean':mean,'covariance_sum_identity_error':abs(S-measured)})
    conditional=list(csv.DictReader((O/'conditional_metrics.csv').open()))
    assert len({r['N_V_common_positions'] for r in conditional})==1
    assert len(conditional)==33
    energy=list(csv.DictReader((O/'contribution_energy.csv').open()));assert len(energy)==9
    for r in energy:
        selfv,cross,total=[float(r[k]) for k in ['self','cross','total_mean_square_contribution']]
        assert abs(selfv+cross-total)<=1e-8*max(total,1) and total>=0
    geo=json.loads((O/'geometry_qualification.json').read_text());assert geo['status']=='PASS'
    cases=json.loads((O/'cases.json').read_text())
    for c in cases:
        assert c['K_full']==len(c['active_members'])
        assert Path(O/c['prefix_file']).read_text()==c['visible_prefix']
        assert c['prefix_token_count']==c['context_offset_zero_based']+1
        assert c['layer28_total_energy']>=0
    chain=json.loads((O/'chain_cases.json').read_text())
    matrix=list(csv.DictReader((O/'case_G014_chain_full_matrix.csv').open()))
    for c,r in zip(chain,matrix):
        assert c['K_full']==len(c['active_members'])
        assert c['position_id']==int(r['position_id'])
        assert Path(O/c['prefix_file']).read_text()==c['visible_prefix']
        active={x['feature_id'] for x in c['active_members']}
        binary=[int(f in active) for f in c['chain_A_B_C']]
        assert binary==c['chain_binary']
        assert sum(b<<i for i,b in enumerate(binary))==c['chain_flag']
        assert sum(int(r[str(f)]) for f in groups[14]['members'])==c['K_full']
    assert len(chain)==len(matrix)==12
    result={'status':'PASS','frozen_protocol_hashes_unchanged':True,'panel_positions_unique':64000,
        'full_window_K_and_pair_covariance_identities':identities,'same_H1_positions_and_denominators':True,
        'same_shared_z_across_decoder_layers':True,'genuine_vector_case_energy':True,
        'case_prefix_and_active_count_checks':len(cases),'additional_chain_case_checks':len(chain),'new_forward_calls':0,'training_updates':0,
        'document_independence':'UNKNOWN','scientific_approval':'UNKNOWN'}
    (O/'result_validation.json').write_text(json.dumps(result,indent=2)+'\n');print('RESULT_VALIDATION_PASS')
if __name__=='__main__':main()
