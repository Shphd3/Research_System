#!/usr/bin/env python3
"""Describe frozen q10 groups. Never fit a graph, encode text, or train a model."""
import argparse
import csv
import hashlib
import itertools
import json
import math
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx
import numpy as np

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
OLD = E/'analysis/feature_frequency/20261015T143300Z'
PHASE = E/'analysis/feature_relation_phase1/20261013T173130Z'
STRUCT = E/'analysis/relation_learning/20261015T164000Z/structure'


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def csv_out(path, rows):
    assert rows, str(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def label_map(groups):
    return {f: g['group_id'] for g in groups for f in g['members']}


def jaccard(a, b):
    return len(a & b)/len(a | b)


def phi(nij, ni, nj, N):
    # Count formula is algebraically identical to Bernoulli Pearson correlation.
    return (N*int(nij)-int(ni)*int(nj))/math.sqrt(int(ni)*int(nj)*(N-int(ni))*(N-int(nj)))


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    groups_all = json.loads((OLD/'main/groups_D.json').read_text())
    groups = [g for g in groups_all if g['size'] > 1]
    vg = json.loads((OLD/'main/groups_V.json').read_text())
    qg = json.loads((OLD/'sensitivity_q20/groups_D.json').read_text())
    freq = {int(r['feature_id']): r for r in read_csv(OLD/'frequency.csv')}
    matches = {int(r['group_D']): r for r in read_csv(OLD/'main/matches.csv')}
    qreview = {int(r['group_q10']): r for r in read_csv(STRUCT/'q10_q20_member_stability.csv')}
    controls = {int(r['group_id']): r for r in read_csv(STRUCT/'full_group_controls.csv')}
    sm = json.loads((OLD/'main/summary.json').read_text())
    ND, NV = sm['N_D'], sm['N_V']
    vsets = {g['group_id']: set(g['members']) for g in vg}
    qsets = {g['group_id']: set(g['members']) for g in qg}
    vlabels, qlabels = label_map(vg), label_map(qg)
    G = nx.Graph()
    G.add_nodes_from(freq)
    d_edges = read_csv(OLD/'main/edges_D.csv')
    v_edges = read_csv(OLD/'main/edges_V.csv')
    G.add_edges_from((int(r['u']), int(r['v']), {'phi': float(r['phi']), 'joint': int(r['joint'])}) for r in d_edges)
    v_edge_set = {tuple(sorted((int(r['u']), int(r['v'])))) for r in v_edges}
    v_weights = {tuple(sorted((int(r['u']), int(r['v'])))): r for r in v_edges}
    d_lookup = {tuple(sorted((int(r['u']), int(r['v'])))): r for r in d_edges}
    pd = np.load(OLD/'main/phi_D.npy', mmap_mode='r')
    pv = np.load(OLD/'main/phi_V.npy', mmap_mode='r')
    all_index, all_members, edge_rows, detail_rows = [], [], [], []
    for g in groups:
        gid, ids, n = g['group_id'], g['members'], g['size']
        S, sub = set(ids), G.subgraph(ids)
        m = matches[gid]
        mg = int(m['group_V']) if m['group_V'] not in ('', 'None') else None
        M = vsets[mg] if mg is not None else set()
        assert len(S & M) == int(m['intersection'])
        if mg is not None:
            assert abs(jaccard(S, M)-float(m['jaccard'])) < 1e-12
        best_v = min(vsets, key=lambda v: (-jaccard(S, vsets[v]), v))
        B = vsets[best_v]
        qr = qreview[gid]
        qid = int(qr['best_group_q20'])
        Q = qsets[qid]
        assert len(S & Q) == int(qr['intersection'])
        assert abs(jaccard(S, Q)-float(qr['best_jaccard'])) < 1e-12
        bridges = {tuple(sorted(e)) for e in nx.bridges(sub)}
        arts = set(nx.articulation_points(sub))
        components = list(nx.connected_components(sub))
        local_edges = sorted(tuple(sorted(e)) for e in sub.edges())
        retained_edges = sum(e in v_edge_set for e in local_edges)
        upper = np.triu_indices(n, 1)
        pair_d = np.asarray(pd[np.ix_(ids, ids)])[upper].astype(float)
        pair_v = np.asarray(pv[np.ix_(ids, ids)])[upper].astype(float)
        fd = np.array([int(freq[i]['n_D']) for i in ids])
        fv = np.array([int(freq[i]['n_V']) for i in ids])
        fdr = fd/ND
        fvr = fv/NV
        vc = Counter(vlabels[i] for i in ids)
        qc = Counter(qlabels[i] for i in ids)
        row = {
            'group_id': gid, 'size': n, 'members_csv': f'groups/group_{gid:03d}_members.csv',
            'edges_csv': f'groups/group_{gid:03d}_edges.csv',
            'members_json': json.dumps(ids),
            'n_D_min': int(fd.min()), 'n_D_max': int(fd.max()),
            'p_D_min': float(fdr.min()), 'p_D_max': float(fdr.max()),
            'frequency_max_min_ratio_D': float(fd.max()/fd.min()),
            'n_V_min': int(fv.min()), 'n_V_max': int(fv.max()),
            'p_V_min': float(fvr.min()), 'p_V_max': float(fvr.max()),
            'frequency_max_min_ratio_V': float(fv.max()/fv.min()) if fv.min() else 'NA',
            'log10_frequency_sd_D': float(np.std(np.log10(fdr))),
            'log10_frequency_sd_V': float(np.std(np.log10(fvr))) if fv.min() else 'NA',
            'internal_edges_D': len(local_edges), 'possible_pairs': n*(n-1)//2,
            'edge_density_D': nx.density(sub), 'connected_components_D': len(components),
            'largest_component_size_D': max(map(len, components)),
            'bridge_count_D': len(bridges), 'articulation_count_D': len(arts),
            'articulation_ids_json': json.dumps(sorted(arts)),
            'degree_min_D': min(dict(sub.degree()).values()), 'degree_max_D': max(dict(sub.degree()).values()),
            'all_pair_phi_D_min': float(np.nanmin(pair_d)), 'all_pair_phi_D_median': float(np.nanmedian(pair_d)),
            'all_pair_phi_D_mean': float(np.nanmean(pair_d)), 'all_pair_phi_D_positive_fraction': float(np.mean(pair_d > 0)),
            'all_pair_phi_V_mean': float(np.nanmean(pair_v)),
            'D_internal_edges_retained_in_V': retained_edges,
            'D_internal_edge_retention_V': retained_edges/len(local_edges) if local_edges else 'NA',
            'matched_V_group_id': mg if mg is not None else 'NA',
            'matched_V_group_size': len(M) if mg is not None else 'NA',
            'matched_V_jaccard': float(m['jaccard']), 'matched_V_intersection': len(S & M),
            'matched_V_member_retention': len(S & M)/n, 'matched_V_left_count': len(S-M),
            'matched_V_added_count': len(M-S), 'matched_V_retained_ids_json': json.dumps(sorted(S & M)),
            'matched_V_left_ids_json': json.dumps(sorted(S-M)), 'matched_V_added_ids_json': json.dumps(sorted(M-S)),
            'unconstrained_best_V_group_id': best_v, 'unconstrained_best_V_group_size': len(B),
            'unconstrained_best_V_jaccard': jaccard(S, B), 'unconstrained_best_V_intersection': len(S & B),
            'actual_V_groups_touched': len(vc), 'actual_V_member_flow_json': json.dumps(dict(sorted(vc.items()))),
            'q20_best_group_id_existing': qid, 'q20_best_group_size_existing': len(Q),
            'q20_member_retention_existing': float(qr['member_retention_q10']),
            'q20_best_jaccard_existing': float(qr['best_jaccard']),
            'q20_groups_touched_existing': int(qr['q20_groups_touched']),
            'q20_same_pair_fraction_existing': float(qr['same_pair_fraction']),
            'q20_member_flow_json': json.dumps(dict(sorted(qc.items()))),
            'repaired_control_qualified': controls[gid]['qualified'],
            'repaired_V_log_frequency_sd_delta': float(controls[gid]['delta_strict']),
            'frequency_source_id': 'frequency', 'group_source_id': 'groups_D_q10',
            'match_source_id': 'matches_DV_q10', 'q20_review_source_id': 'q10_q20_review',
            'control_source_id': 'full_group_controls_repaired',
            'missing_longitudinal_or_multi_split_stability': 'NOT_MEASURED',
            'semantic_theme': 'NOT_ASSIGNED', 'learning_compatibility_from_these_tables': 'NOT_ESTABLISHED',
        }
        all_index.append(row)
        members = []
        for i in ids:
            f = freq[i]
            mr = {'group_id': gid, 'group_size': n, 'feature_id': i,
                  'n_D': int(f['n_D']), 'n_V': int(f['n_V']),
                  'p_D': float(f['p_D']), 'p_V': float(f['p_V']),
                  'rank_D': int(f['rank_D']), 'blocks_D': int(f['blocks_D']), 'blocks_V': int(f['blocks_V']),
                  'ci_low_D': float(f['ci_low_D']), 'ci_high_D': float(f['ci_high_D']),
                  'ci_low_V': float(f['ci_low_V']), 'ci_high_V': float(f['ci_high_V']),
                  'internal_degree_D': sub.degree(i), 'internal_neighbors_D_json': json.dumps(sorted(sub.neighbors(i))),
                  'is_articulation_D': i in arts,
                  'incident_bridge_count_D': sum(i in edge for edge in bridges),
                  'actual_V_group_id': vlabels[i], 'actual_V_group_size': len(vsets[vlabels[i]]),
                  'retained_in_matched_V_group': i in M if mg is not None else 'NA',
                  'retained_in_unconstrained_best_V_group': i in B,
                  'actual_q20_D_group_id': qlabels[i], 'retained_in_existing_best_q20_group': i in Q,
                  'frequency_source_row_1based_including_header': i+2,
                  'frequency_source_id': 'frequency', 'stability_scope': 'one_D_V_partition_comparison_not_longitudinal'}
            members.append(mr)
        local_edge_rows = []
        for u, v in local_edges:
            de = d_lookup[(u, v)]
            ve = v_weights.get((u, v))
            er = {'group_id': gid, 'u': u, 'v': v, 'phi_D': float(de['phi']), 'joint_D': int(de['joint']),
                  'log2lift_D': float(de['log2lift']), 'is_bridge_in_D_group': (u, v) in bridges,
                  'edge_retained_in_V': ve is not None,
                  'phi_V_all_pair': float(pv[u, v]),
                  'phi_V_edge_file_float64': float(ve['phi']) if ve else 'NA',
                  'joint_V_edge_file': int(ve['joint']) if ve else 'NA',
                  'source_id_D': 'edges_D_q10', 'source_id_V': 'edges_V_q10'}
            local_edge_rows.append(er)
        csv_out(out/row['members_csv'], members)
        csv_out(out/row['edges_csv'], local_edge_rows)
        all_members.extend(members)
        edge_rows.extend(local_edge_rows)
        detail_rows.append({'group_id': gid, 'members': ids, 'matched_V_members': sorted(M),
                            'actual_V_member_groups': {str(k): [i for i in ids if vlabels[i] == k] for k in sorted(vc)},
                            'q20_member_groups': {str(k): [i for i in ids if qlabels[i] == k] for k in sorted(qc)},
                            'bridges_D': sorted(bridges), 'articulation_D': sorted(arts)})
    csv_out(out/'all_groups_index.csv', all_index)
    csv_out(out/'all_group_members.csv', all_members)
    csv_out(out/'all_internal_edges_D.csv', edge_rows)
    dump(out/'group_details.json', detail_rows)
    # Exact pair counts and double-precision phi for the three fixed teaching cases.
    cd = np.load(PHASE/'counts/total0.npy', mmap_mode='r')
    cv = np.load(PHASE/'counts/total1.npy', mmap_mode='r')
    candidates = np.array([i for i in sorted(freq) if freq[i]['candidate'] == 'True'])
    rank_cache = {}

    def existing_rule_rank(side, u, v):
        """Explain a frozen edge by the original rule; no graph/community fit."""
        key = (side, u)
        if key not in rank_cache:
            mat, N = (cd, ND) if side == 'D' else (cv, NV)
            counts = np.asarray(mat[u, candidates], dtype=float)
            marg = np.array([int(freq[i][f'n_{side}']) for i in candidates], dtype=float)
            marginal_u = int(freq[u][f'n_{side}'])
            p = marg/N
            pu = marginal_u/N
            with np.errstate(divide='ignore', invalid='ignore'):
                scores = (counts/N-pu*p)/np.sqrt(pu*(1-pu)*p*(1-p))
            eligible = (counts >= 10) & np.isfinite(scores) & (scores > 0) & (candidates != u) & (p > 0) & (p < 1)
            j = np.flatnonzero(eligible)
            j = j[np.lexsort((candidates[j], -scores[j]))]
            rank_cache[key] = {int(candidates[k]): rank+1 for rank, k in enumerate(j)}
        return rank_cache[key].get(v, 'NA')

    for gid in (87, 74, 34):
        ids = groups_all[gid]['members']
        rows = []
        for u, v in itertools.combinations(ids, 2):
            niD, njD, niV, njV = (int(freq[k][f'n_{side}']) for side, k in [('D',u),('D',v),('V',u),('V',v)])
            nijD, nijV = int(cd[u,v]), int(cv[u,v])
            row = {'group_id': gid, 'u': u, 'v': v, 'n_u_D': niD, 'n_v_D': njD,
                   'joint_D': nijD, 'phi_D': phi(nijD, niD, njD, ND),
                   'n_u_V': niV, 'n_v_V': njV, 'joint_V': nijV,
                   'phi_V': phi(nijV, niV, njV, NV),
                   'edge_D': (u,v) in d_lookup, 'edge_V': (u,v) in v_edge_set,
                   'eligible_positive_phi_rank_u_to_v_D': existing_rule_rank('D', u, v),
                   'eligible_positive_phi_rank_v_to_u_D': existing_rule_rank('D', v, u),
                   'eligible_positive_phi_rank_u_to_v_V': existing_rule_rank('V', u, v),
                   'eligible_positive_phi_rank_v_to_u_V': existing_rule_rank('V', v, u),
                   'counts_source_D': 'total_counts_D', 'counts_source_V': 'total_counts_V',
                   'edge_source_D': 'edges_D_q10', 'edge_source_V': 'edges_V_q10'}
            if (u,v) in d_lookup:
                assert abs(row['phi_D']-float(d_lookup[(u,v)]['phi'])) < 1e-12
            for side in ('D', 'V'):
                ranks = [row[f'eligible_positive_phi_rank_u_to_v_{side}'], row[f'eligible_positive_phi_rank_v_to_u_{side}']]
                assert row[f'edge_{side}'] == all(isinstance(r, int) and r <= 10 for r in ranks)
            rows.append(row)
        csv_out(out/f'cases/group_{gid:03d}_all_pairs.csv', rows)
        dump(out/f'cases/group_{gid:03d}_summary.json', all_index[gid])
    # All reused sources are hashed now. Large binary owners stay execution-side.
    sources = {
        'frequency': OLD/'frequency.csv', 'groups_D_q10': OLD/'main/groups_D.json',
        'groups_V_q10': OLD/'main/groups_V.json', 'groups_D_q20': OLD/'sensitivity_q20/groups_D.json',
        'edges_D_q10': OLD/'main/edges_D.csv', 'edges_V_q10': OLD/'main/edges_V.csv',
        'matches_DV_q10': OLD/'main/matches.csv', 'q10_q20_review': STRUCT/'q10_q20_member_stability.csv',
        'full_group_controls_repaired': STRUCT/'full_group_controls.csv',
        'phi_D_float32': OLD/'main/phi_D.npy', 'phi_V_float32': OLD/'main/phi_V.npy',
        'total_counts_D': PHASE/'counts/total0.npy', 'total_counts_V': PHASE/'counts/total1.npy',
        'original_config': OLD/'registered_config.json', 'original_graph_source': E/'analysis_tools/feature_frequency/core_analysis.py',
        'export_code': Path(__file__).resolve(),
    }
    manifest = {key: {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)} for key, path in sources.items()}
    dump(out/'source_manifest.json', {'checked_utc': datetime.now(timezone.utc).isoformat(),
         'sources': manifest, 'N_D': ND, 'N_V': NV,
         'source_roles': {'D': 'original_discovery_side', 'V': 'original_validation_side_not_verified_independent_documents'},
         'no_training': True, 'new_encoded_positions': 0, 'new_graph_fits': 0})
    assert len(all_index) == 186 and len(all_members) == 13807
    assert len({m['feature_id'] for m in all_members}) == 13807
    assert len(groups_all) == 2045 and sum(g['size'] == 1 for g in groups_all) == 1859
    checks = {
        'status': 'PASS_DERIVED_TABLE_CONSISTENCY_NOT_SCIENTIFIC_APPROVAL',
        'groups_exported': len(all_index), 'members_exported': len(all_members),
        'original_all_groups_including_singletons': len(groups_all), 'excluded_singletons': 1859,
        'within_group_D_edges': len(edge_rows),
        'source_config_unchanged': {'q':10,'sensitivity_q':20,'resolution':1.0,'min_D_hits':100,'min_D_blocks':10,'min_joint':10},
        'matches_recomputed_for_consistency_only': 186,
        'q20_existing_row_intersections_and_jaccards_verified': 186,
        'case_exact_counts_vs_existing_edge_phi': 'PASS_WITHIN_1e-12',
        'missing_fields': {'repeated_split_stability':'NOT_MEASURED','document_independence':'UNKNOWN','semantic_theme':'NOT_ASSIGNED'},
        'inference_boundary': 'within-group positive association or graph connection is not a semantic composition or evidence of joint-learning compatibility',
    }
    dump(out/'validation.json', checks)
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=E/'analysis/group_understanding/20261016_tables')
    main(ap.parse_args().output)
