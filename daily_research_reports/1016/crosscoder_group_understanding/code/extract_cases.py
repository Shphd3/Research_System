#!/usr/bin/env python3
"""Recover selected existing text cases from immutable sparse cache; no inference.

Original examples named the current, already-visible token ``target_token``.
This derivative uses current_token at t and label-only next_token at t+1.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


EXPERIMENT = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
OLD = EXPERIMENT / 'analysis/feature_frequency/20261015T143300Z'
INDEX = EXPERIMENT / 'data/direct_dclm_bins_a15/index_val'
DEFAULT_OUT = EXPERIMENT / 'analysis/group_understanding/20261016_cases'
SELECTED_GROUPS = [87, 74, 34]


def load(path):
    return json.loads(Path(path).read_text())


def dump(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def h64(*xs):
    return int.from_bytes(hashlib.sha256(':'.join(map(str, xs)).encode()).digest()[:8], 'little')


def byte_decoder():
    bs = list(range(ord('!'), ord('~') + 1)) + list(range(ord('¡'), ord('¬') + 1)) + list(range(ord('®'), ord('ÿ') + 1))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return {chr(c): b for b, c in zip(bs, cs)}


class FrozenDecoder:
    def __init__(self, path):
        tok = load(path)
        assert tok['decoder']['type'] == 'ByteLevel'
        self.vocab = {int(v): k for k, v in tok['model']['vocab'].items()}
        self.special = {int(y['id']): y['content'] for y in tok['added_tokens']}
        self.bd = byte_decoder()

    def decode(self, seq):
        out, buff = [], bytearray()
        for k in seq:
            k = int(k)
            if k in self.special:
                if buff:
                    out.append(buff.decode('utf-8', errors='replace'))
                    buff = bytearray()
                out.append(self.special[k])
            else:
                for c in self.vocab[k]:
                    if c in self.bd:
                        buff.append(self.bd[c])
                    else:
                        buff.extend(c.encode('utf-8'))
        if buff:
            out.append(buff.decode('utf-8', errors='replace'))
        return ''.join(out)


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    prefix_out = out / 'prefixes'
    prefix_out.mkdir(exist_ok=True)
    config = load(OLD / 'registered_config.json')
    prior = Path(config['prior_root'])
    old_examples = load(OLD / 'inputs/examples.json')['examples']
    assert all(e['model_visible_prefix'].endswith(e['left_text'] + e['target_token']) for e in old_examples)
    group_payload = load(OLD / 'main/groups_D.json')
    groups = group_payload['groups'] if isinstance(group_payload, dict) else group_payload
    by_group = {int(g['group_id']): g for g in groups}
    chosen = []
    selection = []
    for gid in SELECTED_GROUPS:
        candidates = [e for e in old_examples if e['group_id'] == gid]
        random = sorted((e for e in candidates if e['sample_type'] == 'random'),
                        key=lambda e: h64(config['seed'], 'context', gid, e['context_index']))[:3]
        high = sorted((e for e in candidates if e['sample_type'] == 'high_score'),
                      key=lambda e: (-e['group_score'], e['eligible_position']))[:3]
        for kind, rows in [('random', random), ('high_score', high)]:
            assert len({e['context_index'] for e in rows}) == len(rows)
            selection.append({'group_id': gid, 'sample_type': kind,
                              'old_available': sum(e['sample_type'] == kind for e in candidates),
                              'selected_count': len(rows), 'required_count': 3,
                              'positions': [e['eligible_position'] for e in rows]})
            for rank, e in enumerate(rows, 1):
                chosen.append({**e, 'selection_rank': rank})

    manifest = load(prior / 'feature_cache/manifest.json')
    chunks = []
    for rank in manifest['ranks']:
        chunks.extend(load(rank)['chunks'])
    chunks.sort(key=lambda x: x['start'])
    ends = np.array([x['end'] for x in chunks])
    split = load(prior / 'split_manifest.json')
    split_ends = np.array([b['position_end'] for b in split['blocks']])
    data_manifest = load(INDEX / 'manifest.json')
    context_starts = np.load(INDEX / 'prefix.npy')
    records = np.load(INDEX / 'records.npy')
    tokenizer_path = Path('/data/share/Qwen3-0.6B-Base/tokenizer.json')
    decoder = FrozenDecoder(tokenizer_path)
    bins = [np.memmap(s['path'], dtype=np.uint32, mode='r') for s in data_manifest['sources']]
    per_chunk = defaultdict(list)
    for e in chosen:
        per_chunk[int(np.searchsorted(ends, e['eligible_position'], side='right'))].append(e)
    output = []
    verified_chunks = []
    for chunk_index, selected in sorted(per_chunk.items()):
        chunk = chunks[chunk_index]
        observed_hash = sha(chunk['file'])
        assert observed_hash == chunk['sha256'], chunk['file']
        verified_chunks.append({'path': chunk['file'], 'sha256': observed_hash,
                                'start': chunk['start'], 'end': chunk['end'],
                                'rows_selected': len(selected)})
        with np.load(chunk['file']) as cache:
            for e in selected:
                gid = e['group_id']
                members = by_group[gid]['members']
                position = e['eligible_position']
                assert split['blocks'][int(np.searchsorted(split_ends, position, side='right'))]['side'] == 'V'
                row = position - chunk['start']
                a, b = map(int, cache['ptr'][row:row + 2])
                ids, z = cache['ids'][a:b], cache['z'][a:b]
                mask = np.isin(ids, members)
                active = [{'feature_id': int(f), 'z': float(v)} for f, v in zip(ids[mask], z[mask])]
                assert active == e['feature_values'], (gid, position, 'feature values differ')
                assert len(active) == e['active_members']
                assert len(np.unique(ids)) == len(ids)
                assert np.all(z > 0)
                ctx = e['context_index']
                source, offset, length, _ = map(int, records[ctx])
                tokens = np.asarray(bins[source][offset:offset + length])
                eligible_offsets = np.flatnonzero(~np.isin(tokens, data_manifest['excluded_ids']))
                t = int(eligible_offsets[position - int(context_starts[ctx])])
                assert t == e['target_context_offset']
                assert int(tokens[t]) == e['target_token_id']
                prefix = decoder.decode(tokens[:t + 1])
                assert prefix == e['model_visible_prefix'] == e['context']
                assert decoder.decode([tokens[t]]) == e['target_token']
                assert prefix.endswith(e['left_text'] + e['target_token'])
                assert e['position_key'] == f"{data_manifest['sources'][source]['sha256']}:{offset+t}"
                key = f"G{gid:03d}_{e['sample_type']}_{e['selection_rank']}_p{position}"
                prefix_rel = f'prefixes/{key}.txt'
                (out / prefix_rel).write_text(prefix)
                z_map = {x['feature_id']: x['z'] for x in active}
                has_next = t + 1 < len(tokens)
                output.append({
                    'case_id': key, 'group_id': gid, 'group_size': len(members),
                    'sample_type': e['sample_type'], 'selection_rank': e['selection_rank'],
                    'group_score': e['group_score'], 'score_definition': 'positive gated member count / group size',
                    'group_threshold': e['group_threshold'], 'active_member_count': len(active),
                    'active_members_complete': active,
                    'all_members_gated_z': [{'feature_id': int(f), 'z': z_map.get(int(f), 0.0),
                                             'active': int(f) in z_map} for f in members],
                    'eligible_position': position, 'context_index': ctx,
                    'current_context_offset_zero_based': t, 'visible_prefix_token_count': t + 1,
                    'current_token_id': int(tokens[t]), 'current_token': decoder.decode([tokens[t]]),
                    'prediction_position_context_offset_zero_based': t + 1 if has_next else None,
                    'next_target_token_id_label_only': int(tokens[t + 1]) if has_next else None,
                    'next_target_token_label_only': decoder.decode([tokens[t + 1]]) if has_next else None,
                    'next_target_source': 'actual corpus next token; not an argmax/model prediction',
                    'next_token_excluded_special': bool(int(tokens[t + 1]) in data_manifest['excluded_ids']) if has_next else None,
                    'prediction_label_missing_reason': None if has_next else 'context boundary; model was not supplied next context',
                    'visible_prefix_tokens': [int(v) for v in tokens[:t + 1]],
                    'model_visible_prefix': prefix, 'model_visible_prefix_file': prefix_rel,
                    'display_suffix_current_marked': e['display_context'],
                    'current_position_key': e['position_key'],
                    'source_bin': data_manifest['sources'][source]['path'],
                    'source_bin_sha256_from_owner_manifest': data_manifest['sources'][source]['sha256'],
                    'context_source_token_offset': offset, 'current_source_token_offset': offset + t,
                    'context_source_token_count': length, 'cache_chunk': chunk['file'],
                    'cache_chunk_sha256': observed_hash, 'cache_row_within_chunk': row,
                    'source_examples_json': str(OLD / 'inputs/examples.json'),
                    'original_document_id': 'UNKNOWN',
                    'future_visibility': 'tokens after current t were not visible to hidden state h_t; next token is an outcome label only',
                })
    output.sort(key=lambda e: (SELECTED_GROUPS.index(e['group_id']), e['sample_type'] != 'random', e['selection_rank']))
    dump(out / 'selected_cases.json', {'cases': output, 'selection': selection,
         'selection_rule': {'groups': {'small': '2-5 members; nearest size to4, non-clique, smallest group ID',
                                       'medium': '6-19 members; nearest size to layer median14, smallest group ID',
                                       'large': '>=20 members; nearest size to layer median149, smallest group ID'},
                            'random': 'first3 old hit contexts by original seeded SHA256 context rank; saved position unchanged',
                            'high_score': 'first3 old cases by descending active fraction then ascending eligible position; saved positions unchanged',
                            'text_selection': 'no theme, wording or stability selection'},
         'position_contract': 'h_t and z_t see tokens0..t inclusive, predict token t+1; original target_token was current token t',
         'activation_contract': 'all selected group positive gated cache entries retained; absent member z=0 after saved gate, not raw encoder preactivation',
         'inference_calls': 0, 'training_updates': 0, 'new_graph_or_group_computations': 0})
    flat = []
    values = []
    for e in output:
        flat.append({k: v for k, v in e.items() if k not in ['active_members_complete', 'all_members_gated_z', 'visible_prefix_tokens', 'model_visible_prefix']})
        for a in e['all_members_gated_z']:
            values.append({'case_id': e['case_id'], 'group_id': e['group_id'], **a})
    for filename, rows in [('selected_cases_index.csv', flat), ('selected_case_all_member_z.csv', values)]:
        with (out / filename).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    sources = [OLD / 'inputs/examples.json', OLD / 'main/groups_D.json', OLD / 'registered_config.json',
               prior / 'feature_cache/manifest.json', prior / 'split_manifest.json', INDEX / 'manifest.json',
               INDEX / 'records.npy', INDEX / 'prefix.npy', tokenizer_path, Path(__file__)]
    dump(out / 'extraction_receipt.json', {
        'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'selected_groups': SELECTED_GROUPS,
        'case_count': len(output), 'per_group_count': {str(g): sum(e['group_id'] == g for e in output) for g in SELECTED_GROUPS},
        'all_old_prefix_suffix_checks': len(old_examples), 'all_selected_z_exact_cache_checks': len(output),
        'all_selected_prefix_exact_original_checks': len(output), 'all_selected_context_position_join_checks': len(output),
        'all_selected_side_V_checks': len(output), 'full_active_values_retained_no_top_k_truncation': True,
        'verified_chunks': verified_chunks,
        'sources': [{'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in sources],
        'model_forward_calls': 0, 'training_updates': 0, 'graph_parameter_changes': 0,
        'reasoning_audit': {
            'position': 'The original target field described the current already-visible token; derivative labels current t and next t+1 separately.',
            'future': 'Full prefix contains tokens0..t only. Next token is separately marked label-only and is not used to explain activation.',
            'representation': 'Cache contains frozen joint CrossCoder z; nonzero counts are coordinates, not automatically concepts or independent features.',
            'selection': 'Three saved hash-random cases and three saved high active-fraction cases per group, with no selection by semantic content.',
            'scope': 'Case similarities and counterexamples are descriptive. Coactivation does not identify semantic composition or learning compatibility.'}})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    run(args.output)
