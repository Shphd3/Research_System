#!/usr/bin/env python3
"""Post-observation A repair. Fixed cache, full-pipeline fixed-margin null.

The original empirical-log endpoint is retained separately. The bounded null
uses an explicitly exploratory Jeffreys-smoothed score to avoid undefined
log(0) without filtering groups or null draws. No model forward or training.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import resource
import time

import numpy as np
from numba import njit
from scipy import sparse

EXE = Path(os.environ.get('CROSSCODER_EXECUTION_ROOT', '/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder'))
OLD = EXE/'analysis/feature_frequency/20261015T143300Z'
PHASE1 = EXE/'analysis/feature_relation_phase1/20261013T173130Z'
DEFAULT = EXE/'analysis/relation_learning/20261015T164000Z/structure'


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


core = module('core_a', EXE/'analysis_tools/feature_frequency/core_analysis.py')
null = module('null_a', EXE/'analysis_tools/feature_frequency/null_analysis.py')


def save(path, value):
    core.write_json(path, value)


@njit(cache=True)
def heatbath(logd, logv, strictlogv, initial, ordered, tol, burn, space, draws, seed):
    """Exact random-scan single-slot conditional heat-bath, including self-loops.

    Slot order is a redundant ordered representation; every valid subset has
    exactly s! representations. The conditional Gibbs kernel is reversible
    for uniform valid subsets. Finite mixing is diagnosed, never assumed.
    """
    np.random.seed(seed)
    sample = initial.copy()
    s = len(sample)
    F = len(logd)
    occupied = np.zeros(F, np.bool_)
    original = np.zeros(F, np.bool_)
    occupied[sample] = True
    original[sample] = True
    sorted_logs = logd[ordered]
    total = np.sum(logd[sample])
    target = total/s
    vtotal = np.sum(logv[sample])
    vtotal2 = np.sum(logv[sample]**2)
    changed = 0
    original_count = s
    outcomes = np.empty((draws, 5), np.float64)
    unique_ids = np.zeros(F, np.bool_)
    at = 0
    for step in range(burn + space*draws):
        pos = np.random.randint(s)
        old = sample[pos]
        rest = total-logd[old]
        lo = np.searchsorted(sorted_logs, s*(target-tol)-rest-1e-12, side='left')
        hi = np.searchsorted(sorted_logs, s*(target+tol)-rest+1e-12, side='right')
        occupied[old] = False
        # Current value is always a valid conditional option. Rejection below
        # only samples the finite uniform eligible set; it is not a chain clock.
        new = ordered[np.random.randint(lo, hi)]
        while occupied[new]:
            new = ordered[np.random.randint(lo, hi)]
        occupied[new] = True
        if new != old:
            changed += 1
            original_count += int(original[new])-int(original[old])
            total += logd[new]-logd[old]
            vtotal += logv[new]-logv[old]
            vtotal2 += logv[new]*logv[new]-logv[old]*logv[old]
            sample[pos] = new
        if step+1 <= burn or (step+1-burn) % space:
            continue
        mean = vtotal/s
        outcomes[at, 0] = np.sqrt(max(0., vtotal2/s-mean*mean))
        bad = False
        sv = 0.
        sv2 = 0.
        for idx in sample:
            unique_ids[idx] = True
            if not np.isfinite(strictlogv[idx]):
                bad = True
            else:
                sv += strictlogv[idx]
                sv2 += strictlogv[idx]*strictlogv[idx]
        outcomes[at, 1] = np.nan if bad else np.sqrt(max(0., sv2/s-(sv/s)**2))
        outcomes[at, 2] = total/s-target
        outcomes[at, 3] = original_count/(2*s-original_count)
        outcomes[at, 4] = 1. if original_count == s else 0.
        at += 1
    return outcomes, changed, np.sum(unique_ids)


@njit(cache=True)
def _pair_count_le(values, start, threshold):
    lo, hi, count = start, len(values)-1, 0
    while lo < hi:
        if values[lo]+values[hi] <= threshold:
            count += hi-lo
            lo += 1
        else:
            hi -= 1
    return count


@njit(cache=True)
def _triple_cdf(values, lower, upper):
    cumulative = np.zeros(len(values), np.int64)
    count = 0
    for i in range(len(values)-2):
        if values[i]+values[-2]+values[-1] < lower:
            cumulative[i] = count
            continue
        if values[i]+values[i+1]+values[i+2] > upper:
            cumulative[i:] = count
            break
        # Lower bound is inclusive; nextafter makes the complementary count < lower.
        low = np.nextafter(lower-values[i], -np.inf)
        high = upper-values[i]
        count += _pair_count_le(values, i+1, high)-_pair_count_le(values, i+1, low)
        cumulative[i] = count
    cumulative[-2:] = count
    return cumulative


@njit(cache=True)
def exact_small(logd, logv, strictlogv, initial, ordered, tol, draws, ceiling, seed, triple_counting=False):
    """IID uniform feasible pairs (counting) or triples (uniform rejection)."""
    np.random.seed(seed)
    s = len(initial)
    F = len(logd)
    target = np.sum(logd[initial])/s
    original = np.zeros(F, np.bool_)
    original[initial] = True
    unique = np.zeros(F, np.bool_)
    outcome = np.full((draws, 5), np.nan)
    proposals = 0
    valid_pairs = 0
    lows = np.zeros(F, np.int64)
    cumulative = np.zeros(F, np.int64)
    if s == 2:
        vals = logd[ordered]
        for i in range(F):
            lo = max(i+1, np.searchsorted(vals, 2*(target-tol)-vals[i]-1e-12, side='left'))
            hi = np.searchsorted(vals, 2*(target+tol)-vals[i]+1e-12, side='right')
            lows[i] = lo
            valid_pairs += max(0, hi-lo)
            cumulative[i] = valid_pairs
    elif triple_counting:
        vals = logd[ordered]
        lower, upper = 3*(target-tol)-1e-12, 3*(target+tol)+1e-12
        cumulative = _triple_cdf(vals, lower, upper)
        valid_pairs = cumulative[-1]
    accepted = 0
    for draw in range(draws):
        sample = np.empty(s, np.int64)
        if s == 2:
            r = np.random.randint(valid_pairs)
            first = np.searchsorted(cumulative, r, side='right')
            previous = cumulative[first-1] if first else 0
            second = lows[first]+r-previous
            sample[0], sample[1] = ordered[first], ordered[second]
            proposals += 1
        elif triple_counting:
            r = np.random.randint(valid_pairs)
            first = np.searchsorted(cumulative, r, side='right')
            previous = cumulative[first-1] if first else 0
            rem = r-previous
            second, third = -1, -1
            for j in range(first+1, F-1):
                lo = max(j+1, np.searchsorted(vals, lower-vals[first]-vals[j], side='left'))
                hi = np.searchsorted(vals, upper-vals[first]-vals[j], side='right')
                size = max(0, hi-lo)
                if rem >= size:
                    rem -= size
                else:
                    second, third = j, lo+rem
                    break
            if second < 0 or third < 0:
                raise ValueError('Triple CDF/index inverse mismatch')
            sample[0], sample[1], sample[2] = ordered[first], ordered[second], ordered[third]
            proposals += 1
        else:
            success = False
            while proposals < ceiling:
                proposals += 1
                i, j, k = np.random.randint(F), np.random.randint(F), np.random.randint(F)
                if i==j or i==k or j==k:
                    continue
                if abs((logd[i]+logd[j]+logd[k])/3-target) > tol:
                    continue
                sample[0], sample[1], sample[2] = i, j, k
                success = True
                break
            if not success:
                break
        v, vv, sv, svv = 0., 0., 0., 0.
        bad = False
        ov = 0
        total = 0.
        for idx in sample:
            unique[idx] = True
            total += logd[idx]
            v += logv[idx]
            vv += logv[idx]**2
            sv += strictlogv[idx]
            svv += strictlogv[idx]**2
            if not np.isfinite(strictlogv[idx]):
                bad = True
            ov += int(original[idx])
        outcome[draw, 0] = np.sqrt(max(0., vv/s-(v/s)**2))
        outcome[draw, 1] = np.nan if bad else np.sqrt(max(0., svv/s-(sv/s)**2))
        outcome[draw, 2] = total/s-target
        outcome[draw, 3] = ov/(2*s-ov)
        outcome[draw, 4] = 1. if ov==s else 0.
        accepted += 1
    return outcome, proposals, np.sum(unique), accepted, valid_pairs


def rhat_ess(x):
    """Split Rhat and initial-positive-sequence ESS of a scalar chain readout."""
    x = np.asarray(x, float)
    if not np.isfinite(x).all():
        return math.inf, 0.
    m, n = x.shape
    half = n//2
    x = np.concatenate([x[:, :half], x[:, -half:]], 0)
    m, n = x.shape
    W = np.var(x, axis=1, ddof=1).mean()
    B = n*np.var(x.mean(1), ddof=1)
    if W < 1e-20:
        return (1., float(m*n)) if B < 1e-20 else (math.inf, 0.)
    var = (n-1)*W/n+B/n
    rhat = math.sqrt(max(var/W, 0.))
    xc = x-x.mean(1)[:, None]
    rhos = [1.]
    for lag in range(1, n):
        acov = np.mean(np.sum(xc[:, :-lag]*xc[:, lag:], 1)/(n-lag))
        rhos.append(1.-(W-acov)/var)
    tau = 1.
    for lag in range(1, n-1, 2):
        pair = rhos[lag]+rhos[lag+1]
        if pair <= 0:
            break
        tau += 2*pair
    return float(rhat), float(min(m*n, m*n/max(tau, 1.)))


def matched_controls(groups, nD, nV, ND, NV, config, seed, full=False):
    ld = np.log10(nD/ND)
    lv = np.log10((nV+.5)/(NV+1))
    ls = np.full(len(nV), np.nan)
    ok = (nV > 0)&(nV < NV)
    ls[ok] = np.log10(nV[ok]/NV)
    ordered = np.argsort(ld, kind='stable').astype(np.int64)
    reps = config['draws_per_chain_full' if full else 'draws_per_chain_null']
    spacing = config.get('spacing_updates_per_member_full', config['spacing_updates_per_member']) if full else config['spacing_updates_per_member']
    rows = []
    arrays = []
    for gid, g in enumerate(groups):
        if len(g) < 2:
            continue
        s = len(g)
        chains = []
        changes = []
        uniques = []
        proposal_counts = []
        sample_counts = []
        valid_pairs = 0
        for c in range(config['chains']):
            chainseed = (seed+7919*gid+104729*c) % (2**31-1)
            if s <= 3:
                a, proposed, unique, sampled, valid_pairs = exact_small(ld, lv, ls,
                    np.asarray(g, np.int64), ordered, config['tolerance_dex'], reps,
                    config['small_group_iid_proposal_ceiling'], chainseed,
                    bool(config.get('triple_counting', False)))
                changed = sampled
                proposal_counts.append(proposed)
                sample_counts.append(sampled)
            else:
                a, changed, unique = heatbath(ld, lv, ls, np.asarray(g, np.int64), ordered,
                    config['tolerance_dex'], config['burnin_updates_per_member']*s,
                    spacing*s, reps, chainseed)
                proposal_counts.append(s*(config['burnin_updates_per_member']+reps*spacing))
                sample_counts.append(reps)
            chains.append(a)
            changes.append(changed)
            uniques.append(unique)
        a = np.asarray(chains)
        rh, ess = rhat_ess(a[:, :, 0])
        rhmean, essmean = rhat_ess(a[:, :, 2])
        overlap = a[:, :, 3].mean(1)
        exact = a[:, :, 4].mean(1)
        qualified = bool(rh <= config['rhat_max'] and ess >= config['ess_min']
            and rhmean <= config['rhat_max'] and essmean >= config['ess_min']
            and max(overlap) <= config['mean_initial_jaccard_max']
            and max(exact) <= config['exact_initial_state_fraction_max'])
        if s <= 3:
            # These are mathematically IID conditional draws; empirical Rhat
            # variation is reported but cannot invalidate an exact sampler.
            qualified = bool(all(v==reps for v in sample_counts)
                             and np.isfinite(a[:, :, 0]).all())
        real = float(np.std(lv[g]))
        realstrict = float(np.std(ls[g])) if np.isfinite(ls[g]).all() else None
        strict_draws = a[:, :, 1].ravel()
        strict_mean = float(np.mean(strict_draws)) if np.isfinite(strict_draws).all() else None
        match = float(np.mean(a[:, :, 0]))
        row = {'group_id': gid, 'size': s, 'observed_smoothed_SD': real,
            'meanmatched_smoothed_SD': match, 'delta_smoothed': real-match,
            'observed_strict_SD': realstrict, 'meanmatched_strict_SD': strict_mean,
            'delta_strict': realstrict-strict_mean if realstrict is not None and strict_mean is not None else None,
            'qualified': qualified, 'strict_qualified': qualified and realstrict is not None and strict_mean is not None,
            'rhat_SD': rh, 'ess_SD': ess, 'rhat_mean': rhmean, 'ess_mean': essmean,
            'max_abs_D_mean_error': float(np.abs(a[:, :, 2]).max()),
            'mean_initial_jaccard_chain0': float(overlap[0]), 'mean_initial_jaccard_chain1': float(overlap[1]),
            'exact_initial_fraction_max': float(max(exact)),
            'changed_updates': int(sum(changes)), 'updates_per_chain': s*(config['burnin_updates_per_member']+reps*spacing),
            'distinct_ids_min': min(uniques), 'draws_total': reps*config['chains'],
            'sampler': 'exact_iid_pair_counting' if s==2 else (('exact_iid_triple_counting' if config.get('triple_counting', False) else 'exact_iid_triple_rejection') if s==3 else 'single_slot_heatbath'),
            'sampler_proposals': int(sum(proposal_counts)), 'valid_pair_states': valid_pairs if s==2 else None,
            'valid_triple_states': valid_pairs if s==3 and config.get('triple_counting',False) else None,
            'strict_valid_draws': int(np.isfinite(strict_draws).sum())}
        rows.append(row)
        arrays.append(a)
    def aggregate(field, eligible):
        rr = [r for r in rows if r[eligible] and r[field] is not None]
        if len(rr) != len(rows) or not rr:
            return None, None
        return (float(np.mean([r[field] for r in rr])),
                float(np.average([r[field] for r in rr], weights=[r['size'] for r in rr])))
    sm, smw = aggregate('delta_smoothed', 'qualified')
    st, stw = aggregate('delta_strict', 'strict_qualified')
    counts = {'groups': len(rows), 'members': sum(r['size'] for r in rows),
        'qualified_groups': sum(r['qualified'] for r in rows),
        'qualified_members': sum(r['size'] for r in rows if r['qualified']),
        'strict_qualified_groups': sum(r['strict_qualified'] for r in rows),
        'T_b_smoothed': sm, 'T_b_smoothed_memberweighted': smw,
        'T_b_original_strict': st, 'T_b_original_strict_memberweighted': stw}
    for field in ('observed_smoothed_SD','meanmatched_smoothed_SD','observed_strict_SD','meanmatched_strict_SD'):
        valid = [r for r in rows if r[field] is not None and np.isfinite(r[field])]
        counts[field+'_groupweighted'] = float(np.mean([r[field] for r in valid])) if len(valid)==len(rows) and rows else None
        counts[field+'_memberweighted'] = float(np.average([r[field] for r in valid],weights=[r['size'] for r in valid])) if len(valid)==len(rows) and rows else None
    for label, pred in [('small_size2_3', lambda s: s <= 3), ('medium_size4_19', lambda s: 4 <= s <= 19), ('large_size20plus', lambda s: s >= 20)]:
        rr = [r for r in rows if pred(r['size'])]
        qq = [r for r in rr if r['qualified']]
        counts[label] = {'groups': len(rr), 'qualified_groups': len(qq),
            'observed_groupweighted_SD': float(np.mean([r['observed_smoothed_SD'] for r in rr])) if rr else None,
            'control_groupweighted_SD': float(np.mean([r['meanmatched_smoothed_SD'] for r in qq])) if len(qq)==len(rr) and rr else None,
            'delta_groupweighted': float(np.mean([r['delta_smoothed'] for r in qq])) if len(qq)==len(rr) and rr else None,
            'delta_memberweighted': float(np.average([r['delta_smoothed'] for r in qq], weights=[r['size'] for r in qq])) if len(qq)==len(rr) and rr else None}
    return rows, counts, np.asarray(arrays)


def self_test(out):
    import itertools
    logs = np.array([-3., -2., -1., 0.])
    tol = .6
    states = [tuple(s) for s in itertools.combinations(range(4), 2)
              if abs(logs[list(s)].mean()+1.5) <= tol]
    P = np.zeros((len(states), len(states)))
    for i, state in enumerate(states):
        for slot in range(2):
            other = state[1-slot]
            options = [j for j in range(4) if j != other and abs((logs[j]+logs[other])/2+1.5) <= tol]
            for new in options:
                dest = tuple(sorted([other, new]))
                P[i, states.index(dest)] += 1/(2*len(options))
    assert np.allclose(P.sum(0), 1) and np.allclose(P, P.T)
    # Empirical moments against complete enumeration for a constrained set.
    nD = 10**(logs+3)
    nV = np.array([3., 9., 16., 7.])
    initial = np.array([0, 3])
    a, changed, uniques = heatbath(logs, np.log10(nV/100), np.log10(nV/100), initial,
        np.arange(4), tol, 1000, 10, 10000, 7)
    truth = np.mean([np.std(np.log10(nV[list(s)]/100)) for s in states])
    assert abs(a[:, 0].mean()-truth) < .01
    assert np.abs(a[:, 2]).max() <= tol+1e-10
    b, proposed, unique, accepted, pairs = exact_small(logs, np.log10(nV/100), np.log10(nV/100),
        initial, np.arange(4), tol, 20000, 1000000, 9)
    assert pairs==len(states) and accepted==20000
    assert abs(b[:,0].mean()-truth) < .005
    triples = [tuple(s) for s in itertools.combinations(range(4),3)
               if abs(logs[list(s)].mean()-logs[:3].mean())<=tol]
    c, proposed, unique, accepted, pairs = exact_small(logs, np.log10(nV/100), np.log10(nV/100),
        np.arange(3), np.arange(4), tol, 20000, 1000000, 11)
    truth3 = np.mean([np.std(np.log10(nV[list(s)]/100)) for s in triples])
    assert accepted==20000 and abs(c[:,0].mean()-truth3)<.005
    c2, proposed, unique, accepted, states3 = exact_small(logs, np.log10(nV/100), np.log10(nV/100),
        np.arange(3), np.arange(4), tol, 20000, 1000000, 11, True)
    assert accepted==20000 and states3==len(triples)
    assert abs(c2[:,0].mean()-truth3)<.005
    # Exhaustively verify the O(P^2) triple CDF and integer inverse on many
    # different targets. This catches rare-support states as well as ordinary ones.
    test_logs = np.array([-4.7,-3.2,-2.81,-2.0,-1.77,-1.1,-.73,-.1])
    for initial3 in itertools.combinations(range(8),3):
        target3 = np.mean(test_logs[list(initial3)])
        for tol3 in (.1,.6):
            legal = [s for s in itertools.combinations(range(8),3)
                     if abs(test_logs[list(s)].mean()-target3)<=tol3+1e-12]
            cdf = _triple_cdf(test_logs, 3*(target3-tol3)-1e-12, 3*(target3+tol3)+1e-12)
            assert cdf[-1]==len(legal)
            sampled, _, _, count, number = exact_small(test_logs, test_logs, test_logs,
                np.asarray(initial3), np.arange(8), tol3, 20, 1000000, 19, True)
            assert count==20 and number==len(legal) and np.abs(sampled[:,2]).max()<=tol3+1e-10
    rng = np.random.default_rng(42)
    rh, ess = rhat_ess(rng.normal(size=(2, 1000)))
    assert rh < 1.02 and ess > 500
    # Sparse projected counts are exactly the corresponding full submatrix.
    A = rng.random((41, 17)) < .25
    ids = np.array([1, 5, 8, 11])
    x = sparse.csr_matrix(A[:, ids], dtype=np.int32)
    assert np.array_equal((x.T@x).toarray(), (A.astype(int).T@A.astype(int))[np.ix_(ids, ids)])
    result = {'status': 'PASS_ENGINEERING_NOT_SCIENTIFIC', 'heatbath_detailed_balance_enumerated': True,
        'heatbath_empirical_moment': float(a[:, 0].mean()), 'enumerated_moment': float(truth),
        'fixed_step_schedule': True, 'no_draw_filtering': True,
        'exact_iid_pair_counting_verified': True, 'exact_iid_triple_rejection_verified': True,
        'exact_iid_triple_counting_verified': True, 'triple_cdf_exhaustive_targets': 112,
        'projected_counts_identity': True, 'Rhat_ESS_sanity': [rh, ess],
        'inherited_swap_selftest': null.self_test()}
    save(out/'self_test.json', result)
    return result


def full_repair(out, config):
    start = time.monotonic()
    z = np.load(PHASE1/'feature_frequency.npz')
    n = z['n'].astype(float)
    split = json.loads((PHASE1/'split_manifest.json').read_text())
    groups_original = json.loads((OLD/'main/groups_D.json').read_text())
    ids = np.load(OLD/'main/candidate_ids.npy')
    loc = np.full(n.shape[1], -1, int)
    loc[ids] = np.arange(len(ids))
    groups = [loc[g['members']].tolist() for g in groups_original]
    rows, summary, draws = matched_controls(groups, n[0, ids], n[1, ids], split['N_D'], split['N_V'], config, config['seed'], full=True)
    core.write_csv(out/'full_group_controls.csv', rows)
    np.savez_compressed(out/'full_matched_draws.npz', draws=draws)
    # Source old facts are rederived from owner tables, never new graph fits.
    old_metrics = list(csv.DictReader((OLD/'main/group_metrics.csv').open()))
    jaccard = list(csv.DictReader((OLD/'main/matches.csv').open()))
    summary.update({'seconds': time.monotonic()-start,
        'source_T_a_recomputed_from_matches': float(np.mean([float(r['jaccard']) for r in jaccard])),
        'source_186_groups': len(rows), 'source_size2_groups': sum(r['size']==2 for r in rows),
        'source_observed_SD_from_old_table': float(np.mean([float(r['logsd_V']) for r in old_metrics])),
        'source_q20_groups': sum(g['size']>1 for g in json.loads((OLD/'sensitivity_q20/groups_D.json').read_text())),
        'original_ids_sha256': hashlib.sha256(ids.tobytes()).hexdigest(),
        'sample_role': 'fixed full-cache groups; no reencoding, no independent-document claim',
        'strict_coverage_rule': 'every original nontrivial group, every scheduled matched draw; no V redraw'})
    save(out/'full_repair_summary.json', summary)
    print(json.dumps({'stage': 'full_repair', **core.json_safe(summary)}), flush=True)
    return summary


def projected_counts(A, ids):
    x = sparse.csr_matrix(A[:, ids], dtype=np.int32)
    return (x.T@x).toarray()


def evaluate_events(A_D, A_V, ctxD, config, seed, path=None):
    start = time.monotonic()
    ND, NV = len(A_D), len(A_V)
    nD = A_D.sum(0).astype(np.int64)
    nV = A_V.sum(0).astype(np.int64)
    coverage = null.context_coverage(A_D, ctxD)
    mask = (nD >= config['candidate_min_hits_sample'])&(nD < ND)&(coverage >= config['candidate_min_contexts_sample'])
    ids = np.flatnonzero(mask)
    CD, CV = projected_counts(A_D, ids), projected_counts(A_V, ids)
    method = {'q': 10, 'joint_min': config['joint_min_sample'], 'resolution': 1.0}
    t_graph = time.monotonic()
    d = core.construct_graph(CD, nD[ids], ND, np.ones(len(ids), bool), method)
    v = core.construct_graph(CV, nV[ids], NV, np.ones(len(ids), bool), method)
    Ta, matches, _ = core.match_groups(d['groups'], v['groups'], len(ids))
    graph_seconds = time.monotonic()-t_graph
    rows, controls, draws = matched_controls(d['groups'], nD[ids].astype(float), nV[ids].astype(float), ND, NV, config, seed)
    result = {'T_a': Ta, **controls, 'candidate_count': len(ids), 'D_groups': d['summary'], 'V_groups': v['summary'],
        'seconds': time.monotonic()-start, 'graph_seconds': graph_seconds,
        'candidate_ids_sha256': hashlib.sha256(ids.tobytes()).hexdigest(),
        'zero_V_candidate_count': int((nV[ids]==0).sum()),
        'score_scope': 'post-observation Jeffreys-smoothed sample-frequency endpoint; strict empirical score retained separately'}
    if path is not None:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        save(path/'summary.json', result)
        core.write_csv(path/'group_controls.csv', rows)
        save(path/'groups_D.json', [{'group_id': i, 'members': ids[g].tolist()} for i, g in enumerate(d['groups'])])
        save(path/'groups_V.json', [{'group_id': i, 'members': ids[g].tolist()} for i, g in enumerate(v['groups'])])
        np.savez_compressed(path/'matched_draws.npz', draws=draws)
    return result


def worker_evaluate(file, config, draw, cid, out):
    with np.load(file) as z:
        AD, AV, ctx = z['A_D'], z['A_V'], z['ctx_D']
    result = evaluate_events(AD, AV, ctx, config, config['seed']+1000000+draw,
                            Path(out)/f'draw_{draw:03d}')
    result.update(draw_id=draw, chain_id=cid)
    return result


def repair_one_controls(source_dir, target_dir, config, margins):
    """Recompute all controls from frozen graph memberships, never refit graphs."""
    oldsummary = json.loads((source_dir/'summary.json').read_text())
    original_groups = json.loads((source_dir/'groups_D.json').read_text())
    ids = np.array(sorted(i for g in original_groups for i in g['members']), np.int64)
    loc = np.full(len(margins['nD']), -1, np.int64)
    loc[ids] = np.arange(len(ids))
    groups = [loc[g['members']].tolist() for g in original_groups]
    if source_dir.name.startswith('draw_'):
        draw = int(source_dir.name.split('_')[1])
        seed = config['seed']+1000000+draw
    elif source_dir.name=='observed':
        draw = None
        seed = config['seed']+1
    else:
        draw = None
        cid = int(source_dir.name.split('chain')[1].split('_')[0])
        multiple = int(source_dir.name.split('step')[1])
        seed = config['seed']+cid*1000+multiple
    begin = time.monotonic()
    rows, controls, arrays = matched_controls(groups, margins['nD'][ids].astype(float),
        margins['nV'][ids].astype(float), int(margins['ND']), int(margins['NV']),config,seed)
    # The graph and Ta retain their original frozen identities. Only the
    # numerical conditional-control sampler is repaired under the same law.
    result = {**oldsummary, **controls, 'old_T_b_smoothed':oldsummary.get('T_b_smoothed'),
        'old_qualified_groups':oldsummary.get('qualified_groups'),
        'conditional_control_repair':'uniform exact IID triple counting replaces rare-event rejection for all size3 groups; other conditional target/settings unchanged',
        'repair_seconds':time.monotonic()-begin,
        'source_graph_summary_sha256':hashlib.sha256((source_dir/'summary.json').read_bytes()).hexdigest()}
    if draw is not None:
        result.update(draw_id=draw,chain_id=draw%2)
    target_dir.mkdir(parents=True,exist_ok=True)
    core.write_csv(target_dir/'group_controls.csv',rows)
    np.savez_compressed(target_dir/'matched_draws.npz',draws=arrays)
    save(target_dir/'summary.json',result)
    return result


def aggregate_repaired(input_dir, output_dir, config):
    source_result = input_dir/'null_results.json'
    if not source_result.exists() or not (output_dir/'observed/summary.json').exists():
        return None
    original = json.loads(source_result.read_text())
    observed = json.loads((output_dir/'observed/summary.json').read_text())
    draws = [json.loads(f.read_text()) for f in sorted((output_dir/'draws').glob('draw_*/summary.json'))] if (output_dir/'draws').exists() else []
    requested = config['null_B']
    result = {**original,'observed':observed,'draws':draws,'B_completed':len(draws),'approx_p':None,'holm_approx':None,
        'status':'IN_PROGRESS_EXACT_TRIPLE_NUMERICAL_REPAIR','original_sampling_result':str(source_result),
        'repair_scope':'Same uniform D-mean constrained control law for every observed/null graph. No V-based selection, no draw dropping, no graph refitting.',
        'original_confirmatory_p':None}
    for key in ('H1b_missing_reason','multiplicity','error'):
        if key in original:
            result['original_sampling_'+key] = original[key]
            result.pop(key,None)
    qpaths = [[output_dir/f'qualification_chain{cid}_step{step}/summary.json' for step in (16,32)] for cid in range(2)]
    failures = []
    if all(p.exists() for cp in qpaths for p in cp):
        q = [[json.loads(p.read_text()) for p in cp] for cp in qpaths]
        for cid, cp in enumerate(q):
            if not compatible(cp[0],cp[1],'T_b_smoothed',config['null_qualification_endpoint_floor']):
                failures.append(f'chain{cid}/Tb:drift_or_missing')
        if not compatible(q[0][-1],q[1][-1],'T_b_smoothed',config['null_qualification_endpoint_floor']):
            failures.append('between_chain/Tb:drift_or_missing')
        save(output_dir/'qualification_control_repair.json',{'failures':failures,'qualified':not failures,
            'same_thresholds':True,'original_fixed_margin_diagnostics':str(input_dir/'qualification.json'),
            'chains':q})
    else:
        failures.append('Missing qualification repaired controls')
    result['repair_qualification_failures']=failures
    if len(draws)==requested and original.get('B_completed')==requested:
        B = len(draws)
        pa = (1+sum(d['T_a']>=observed['T_a'] for d in draws))/(B+1)
        if failures or observed['T_b_smoothed'] is None or any(d['T_b_smoothed'] is None for d in draws):
            result.update(status='H1A_EXPLORATORY_CALIBRATED_H1B_INSUFFICIENT_AFTER_EXACT_TRIPLE_REPAIR',
                approx_p={'H1a':pa,'H1b_smoothed':None},holm_approx={'H1a':min(1.,2*pa),'H1b_smoothed':None},
                H1b_missing_reason='At least one complete group/control endpoint or unchanged qualification check remains unavailable; no valid-only filtering')
        else:
            pb = (1+sum(d['T_b_smoothed']<=observed['T_b_smoothed'] for d in draws))/(B+1)
            result.update(status='EXPLORATORY_APPROXIMATE_CONDITIONAL_CALIBRATION_AFTER_EXACT_TRIPLE_REPAIR',
                approx_p={'H1a':pa,'H1b_smoothed':pb},holm_approx=dict(zip(('H1a','H1b_smoothed'),null.holm_two([pa,pb]))))
            result['multiplicity']='Two-endpoint exploratory family, Holm arithmetic on both approximate conditional p values; serial MCMC implies no guaranteed nominal FWER.'
        result.update(p_resolution=1/(B+1),FWER_guarantee=False)
    save(output_dir/'null_results.json',result)
    fields = ['draw_id','chain_id','T_a','T_b_smoothed','T_b_smoothed_memberweighted','T_b_original_strict','qualified_groups','groups','members','repair_seconds']
    core.write_csv(output_dir/'null_metrics.csv',[{k:d.get(k) for k in fields} for d in draws],fields)
    return result


def repair_controls(input_dir, output_dir, config, watch=False):
    input_dir,output_dir = Path(input_dir),Path(output_dir)
    with np.load(input_dir/'repair_input_margins.npz') as z:
        margins = {k:z[k] for k in z.files}
    config = {**config,'triple_counting':True,'conditional_sampler_revision':'exact_triple_counting_all_observed_and_null_groups',
        'post_observation':True,'numerical_target_unchanged':True}
    save(output_dir/'registered_control_repair_config.json',config)
    started = time.monotonic()
    while True:
        sources = [input_dir/'observed']+[input_dir/f'qualification_chain{cid}_step{step}' for cid in range(2) for step in (16,32)]
        sources += sorted((input_dir/'draws').glob('draw_*')) if (input_dir/'draws').exists() else []
        for source in sources:
            if not (source/'groups_D.json').exists() or not (source/'summary.json').exists():
                continue
            target = output_dir/'draws'/source.name if source.name.startswith('draw_') else output_dir/source.name
            if (target/'summary.json').exists():
                continue
            result = repair_one_controls(source,target,config,margins)
            print(json.dumps({'stage':'exact_triple_controls','source':source.name,'seconds':result['repair_seconds'],
                'Ta':result['T_a'],'Tb':result['T_b_smoothed'],'qualified_groups':result['qualified_groups'],'groups':result['groups']}),flush=True)
            aggregate_repaired(input_dir,output_dir,config)
        result = aggregate_repaired(input_dir,output_dir,config)
        if not watch or (result is not None and result['B_completed']==config['null_B']
                         and not result['status'].startswith('IN_PROGRESS')):
            break
        if time.monotonic()-started>6*3600:
            print(json.dumps({'stage':'repair_watch_time_bound','seconds':time.monotonic()-started}),flush=True)
            break
        time.sleep(10)
    save(output_dir/'completion.json',{'seconds':time.monotonic()-started,'B_completed':result.get('B_completed') if result else 0,
        'status':result.get('status') if result else 'WAITING_FOR_INPUTS'})
    return result


def compatible(a, b, key, floor, relative=.1):
    if a.get(key) is None or b.get(key) is None:
        return False
    aa, bb = np.asarray(a[key]), np.asarray(b[key])
    return bool(np.all(np.abs(aa-bb) <= np.maximum(floor, relative*np.maximum(np.maximum(np.abs(aa), np.abs(bb)), .02))))


def run_null(out, config, formal=True):
    start = time.monotonic()
    deadline = start+config['wall_seconds_max']
    with np.load(OLD/'null/sample_events.npz') as z:
        data = {k: z[k] for k in z.files}
    observed = evaluate_events(data['A_D'], data['A_V'], data['ctx_D'], config, config['seed']+1, out/'observed')
    print(json.dumps({'stage': 'sample_observed', **core.json_safe(observed)}), flush=True)
    diagnostics = []
    rng = np.random.default_rng(config['seed'])
    pi, pj = rng.integers(0, data['A_D'].shape[1], (2, 10000))
    pj[pi==pj] = (pj[pi==pj]+1)%data['A_D'].shape[1]
    states = []
    for cid in range(2):
        chains = {s: null.SwapChain(data['A_'+s], config['seed']+10000*cid+1000*(s=='V'), deadline, 32) for s in ('D', 'V')}
        checkpoints = []
        previous = 0
        for multiple in config['qualification_checkpoints_proposals_per_nnz']:
            tm = time.monotonic()
            diag = {'chain_id': cid, 'proposal_multiple': multiple, 'sides': {}}
            for s in ('D', 'V'):
                ch = chains[s]
                ch.advance_proposals((multiple-previous)*len(ch.row))
                overlap = float(np.count_nonzero(ch.A&ch.original)/len(ch.row))
                ni, nj = ch.col_margin[pi], ch.col_margin[pj]
                joint = np.sum(ch.A[:, pi]&ch.A[:, pj], 0)
                phi = core.phi_values(joint, ni, nj, len(ch.A))
                diag['sides'][s] = {'original_edge_overlap': overlap, 'phi_quantiles': np.quantile(phi[np.isfinite(phi)], [.1,.5,.9,.99]).tolist(),
                    'acceptance': ch.accepted/ch.proposals, 'proposals': ch.proposals, 'accepted': ch.accepted,
                    'row_margins_equal': True, 'column_margins_equal': True}
            diag['endpoint'] = evaluate_events(chains['D'].A, chains['V'].A, data['ctx_D'], config,
                config['seed']+cid*1000+multiple, out/f'qualification_chain{cid}_step{multiple}')
            diag['seconds'] = time.monotonic()-tm
            checkpoints.append(diag)
            save(out/'qualification_progress.json', diagnostics+[checkpoints])
            print(json.dumps({'stage': 'null_qualification', 'chain': cid, 'multiple': multiple, 'seconds': diag['seconds'],
                'Ta': diag['endpoint']['T_a'], 'Tb': diag['endpoint']['T_b_smoothed'], 'qualified_groups': diag['endpoint']['qualified_groups'], 'groups': diag['endpoint']['groups']}), flush=True)
            previous = multiple
        diagnostics.append(checkpoints)
        states.append(chains)
    failures = []
    for cid, cp in enumerate(diagnostics):
        for s in ('D','V'):
            for key in ('original_edge_overlap','phi_quantiles'):
                if not compatible(cp[-2]['sides'][s],cp[-1]['sides'][s],key,config['null_qualification_diagnostic_floor']):
                    failures.append(f'chain{cid}/{s}/{key}:drift')
            if cp[-1]['sides'][s]['acceptance'] < config['null_min_acceptance']:
                failures.append(f'chain{cid}/{s}:low_acceptance')
        for key in ('T_a','T_b_smoothed'):
            if not compatible(cp[-2]['endpoint'],cp[-1]['endpoint'],key,config['null_qualification_endpoint_floor']):
                failures.append(f'chain{cid}/{key}:drift_or_missing')
    for s in ('D','V'):
        for key in ('original_edge_overlap','phi_quantiles'):
            if not compatible(diagnostics[0][-1]['sides'][s],diagnostics[1][-1]['sides'][s],key,config['null_qualification_diagnostic_floor']):
                failures.append(f'between_chain/{s}/{key}:drift')
    for key in ('T_a','T_b_smoothed'):
        if not compatible(diagnostics[0][-1]['endpoint'],diagnostics[1][-1]['endpoint'],key,config['null_qualification_endpoint_floor']):
            failures.append(f'between_chain/{key}:drift_or_missing')
    per = max(cp[-1]['endpoint']['seconds'] for cp in diagnostics)+5.
    estimate = per*config['null_B']/config['workers']*1.25
    report = {'status': 'DIAGNOSTICS_QUALIFIED' if not failures else 'NOT_QUALIFIED', 'failures': failures,
        'chains': diagnostics, 'seconds': time.monotonic()-start, 'B99_conservative_wall_seconds': estimate,
        'remaining_seconds': deadline-time.monotonic(), 'formal_B_requested': config['null_B'],
        'sampling': 'fixed proposal clock with rejected self-loops, same candidate/phi/graph/community/score operations for each draw',
        'uniform_mixing_proved': False, 'original_strict_Tb': observed['T_b_original_strict'],
        'exploratory_smoothed_Tb': observed['T_b_smoothed']}
    save(out/'qualification.json', report)
    result = {'status': 'NOT_STARTED', 'observed': observed, 'B_requested': config['null_B'], 'B_completed': 0,
        'draws': [], 'approx_p': None, 'original_confirmatory_p': None,
        'scope': 'post-observation bounded within-bin exploratory pipeline calibration; no full-cache or independent-document p value'}
    failures_a = [f for f in failures if 'T_b_smoothed' not in f]
    failures_b = [f for f in failures if 'T_a' not in f]
    report.update(failures_H1a=failures_a,failures_H1b=failures_b,
                  H1a_diagnostic_qualified=not failures_a,H1b_diagnostic_qualified=not failures_b)
    save(out/'qualification.json', report)
    if failures_a or not formal or estimate > deadline-time.monotonic():
        result.update(status='QUALIFICATION_FAILED_H1A' if failures_a else 'RESOURCE_BOUND_OR_QUALIFICATION_ONLY')
        save(out/'null_results.json', result)
        return result
    # The checkpoint at exactly 32M proposals is already the frozen burn-in.
    pending = []
    result['status']='RUNNING_FIXED_MARGIN_NULL'
    save(out/'null_results.json',result)
    pool = ProcessPoolExecutor(max_workers=config['workers'])
    try:
        for draw in range(config['null_B']):
            if time.monotonic() > deadline-60:
                raise TimeoutError('Local CPU wall budget reached; retain scheduled completed draws, no p value')
            cid = draw % 2
            chains = states[cid]
            for ch in chains.values():
                ch.advance_proposals(config['null_spacing_proposals_per_nnz']*len(ch.row))
            snapshot = out/f'events_draw_{draw:03d}.npz'
            np.savez(snapshot,A_D=chains['D'].A,A_V=chains['V'].A,ctx_D=data['ctx_D'])
            pending.append((draw, snapshot, pool.submit(worker_evaluate, str(snapshot), config, draw, cid, str(out/'draws'))))
            if len(pending) >= config['workers']:
                k, snap, future = pending.pop(0)
                scored = future.result()
                result['draws'].append(scored)
                result['B_completed'] += 1
                # Only the temporary event snapshot is removed. Tables/score traces persist.
                snap.unlink()
                save(out/'null_results.json', result)
                print(json.dumps({'stage':'formal_null','draw':k,'B_completed':result['B_completed'],'Ta':scored['T_a'],'Tb':scored['T_b_smoothed'],'seconds':scored['seconds']}),flush=True)
        for k, snap, future in pending:
            scored = future.result()
            result['draws'].append(scored)
            result['B_completed'] += 1
            snap.unlink()
        result['draws'].sort(key=lambda r:r['draw_id'])
        B = result['B_completed']
        pa = (1+sum(d['T_a'] >= observed['T_a'] for d in result['draws']))/(B+1)
        if failures_b or observed['T_b_smoothed'] is None or any(d['T_b_smoothed'] is None for d in result['draws']):
            result.update(status='H1A_EXPLORATORY_CALIBRATED_H1B_INSUFFICIENT',
                approx_p={'H1a':pa,'H1b_smoothed':None},holm_approx={'H1a':min(1.,2*pa),'H1b_smoothed':None},
                p_resolution=1/(B+1),FWER_guarantee=False,
                H1b_missing_reason='Observed/null endpoint missing or Tb diagnostic qualification failed; no valid-only filtering',
                multiplicity='Two-endpoint family retained; missing H1b treated conservatively as p=1 solely for H1a adjustment, not an estimated H1b p')
        else:
            pb = (1+sum(d['T_b_smoothed'] <= observed['T_b_smoothed'] for d in result['draws']))/(B+1)
            result.update(status='EXPLORATORY_APPROXIMATE_CONDITIONAL_CALIBRATION',approx_p={'H1a':pa,'H1b_smoothed':pb},
                holm_approx=dict(zip(('H1a','H1b_smoothed'),null.holm_two([pa,pb]))),p_resolution=1/(B+1),FWER_guarantee=False)
    except Exception as exc:
        result.update(status='INCOMPLETE_NO_P',error=type(exc).__name__+': '+str(exc))
    finally:
        pool.shutdown(wait=True)
    result['seconds'] = time.monotonic()-start
    save(out/'null_results.json',result)
    fields = ['draw_id','chain_id','T_a','T_b_smoothed','T_b_smoothed_memberweighted','T_b_original_strict','qualified_groups','groups','members','seconds']
    core.write_csv(out/'null_metrics.csv',[{k:d.get(k) for k in fields} for d in result['draws']],fields)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode',choices=['self-test','full','qualification','run','repair-controls'],required=True)
    p.add_argument('--output',default=str(DEFAULT))
    p.add_argument('--input',default=str(DEFAULT))
    p.add_argument('--watch',action='store_true')
    args = p.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True,exist_ok=True)
    config_path = Path(args.input)/'registered_structure_config.json' if args.mode=='repair-controls' else out/'registered_structure_config.json'
    config = json.loads(config_path.read_text())
    receipt = {'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'config_sha256':hashlib.sha256(config_path.read_bytes()).hexdigest(),'pid':os.getpid(),'mode':args.mode,
        'cpu_affinity':sorted(os.sched_getaffinity(0)),'post_observation':True}
    save(out/'source_receipt.json',receipt)
    save(out/f'source_receipt_{args.mode}.json',receipt)
    snapshots = out/'source_snapshots'
    snapshots.mkdir(exist_ok=True)
    (snapshots/(receipt['source_sha256']+'.py')).write_text(Path(__file__).read_text())
    if args.mode=='self-test':
        print(json.dumps(self_test(out)),flush=True)
    elif args.mode=='full':
        full_repair(out,config)
    elif args.mode=='repair-controls':
        repair_controls(args.input,out,config,args.watch)
    else:
        run_null(out,config,formal=args.mode=='run')


if __name__=='__main__':
    main()
