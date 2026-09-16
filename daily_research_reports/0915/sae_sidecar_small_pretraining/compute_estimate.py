#!/usr/bin/env python3
"""CPU-only budget arithmetic; never launches training or imports torch.

Default reproduces the planning estimate. --throughput accepts the measured
single-GPU valid-target throughput after Smoke, replacing planning scenarios.
"""
import argparse
import json
from pathlib import Path


def flops(c, serial_sae=False):
    h, f, layers = c['hidden_size'], c['intermediate_size'], c['num_hidden_layers']
    q = c['num_attention_heads'] * c['head_dim']
    kv = c['num_key_value_heads'] * c['head_dim']
    body = layers * (2*h*q + 2*h*kv + 3*h*f)
    # Approximate dense training operations. CE rematerializes the output matmul.
    output = 8 * c['vocab_size'] * h
    attention = 12 * layers * c['max_position_embeddings'] * q
    # Dense reference encoder/decoder; no sparse-kernel speedup assumed.
    sae = 0 if c.get('sae_mode') == 'none' else 12 * h * c['sae_width'] * (0.125 + int(serial_sae))
    return {'body_dense': 6*body, 'output_with_ce_rematerialization': output,
            'attention_full_square_upper_approximation': attention,
            'sae_main_paths': sae, 'total': 6*body + output + attention + sae}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--throughput', type=float)
    parser.add_argument('--gpus-per-condition', type=int, choices=[1, 2], default=1,
                        help='for measured throughput: aggregate rate across this many GPUs')
    parser.add_argument('--extra-fraction', type=float, default=0.15)
    parser.add_argument('--lost-compute-fraction', type=float, default=0.0)
    parser.add_argument('--queue-hours', type=float, default=0.0)
    args = parser.parse_args()
    if args.throughput is not None and args.throughput <= 0:
        parser.error('throughput must be positive')
    if args.extra_fraction < 0 or not 0 <= args.lost_compute_fraction < 1 or args.queue_hours < 0:
        parser.error('invalid overhead, lost-compute fraction, or queue hours')
    base = Path(__file__).resolve().parent
    cfg = json.loads((base/'candidate_pair.json').read_text())
    source = json.loads((base/'source_audit.json').read_text())
    old = source['reference_model']
    new = cfg['model']
    old_cost, new_cost = flops(old, True), flops(new)
    reference_rate = source['throughput_reference']['median_valid_targets_per_second']
    idealized_rate = reference_rate / 4 * old_cost['total'] / new_cost['total']
    old_5090 = source['reference_5090_model']
    old_5090_cost = flops(old_5090)
    rate_5090 = source['throughput_reference_5090']['median_valid_targets_per_second']
    idealized_5090 = rate_5090 / 8 * old_5090_cost['total'] / new_cost['total']
    specs = [('measured',args.throughput,args.gpus_per_condition,None)] if args.throughput else (
        [('H100_1gpu',r,1,None) for r in [60000,90000,120000]] +
        [('RTX5090_1gpu_reference_scenario',r,1,None) for r in [50000,70000,90000]] +
        [('RTX5090_2gpu_per_condition',r*2*eff,2,eff) for r,eff in [(50000,.75),(70000,.85),(90000,.9)]])
    scenarios = []
    for platform,rate,gpus,eff in specs:
        pure = 5_000_000_000/rate/3600
        budgeted = pure*(1+args.extra_fraction)
        elapsed = budgeted/(1-args.lost_compute_fraction)+args.queue_hours
        scenarios.append(dict(platform=platform,gpus_per_condition=gpus,assumed_ddp_efficiency=eff,
            valid_targets_per_second=rate, pure_training_hours=pure,
            with_eval_checkpoint_hours=budgeted, with_spot_scenario_hours=elapsed,
            two_conditions_serial_hours=2*elapsed,
            two_conditions_parallel_hours=elapsed,
            total_pair_gpu_hours_excluding_queue=2*gpus*budgeted/(1-args.lost_compute_fraction),
            one_B_pure_hours=1_000_000_000/rate/3600,
            development_1024_pure_hours=268435456/rate/3600))
    result = dict(status='ESTIMATE_NOT_MEASURED_FOR_NEW_MODEL' if args.throughput is None else 'USER_SUPPLIED_THROUGHPUT',
        tokens_per_condition=5_000_000_000, tokens_pair=10_000_000_000,
        approximate_flops_per_token_old=old_cost, approximate_flops_per_token_new=new_cost,
        reference_four_h100_rate=reference_rate,
        idealized_same_efficiency_single_h100_rate=idealized_rate,
        reference_eight_5090_rate=rate_5090,
        approximate_flops_per_token_old_5090=old_5090_cost,
        idealized_same_efficiency_single_5090_rate=idealized_5090,
        assumptions={'extra_fraction':args.extra_fraction,'lost_compute_fraction':args.lost_compute_fraction,
            'queue_hours_per_condition':args.queue_hours,
            'rate_scenarios_are_not_confidence_interval':True,
            'excluded':'offline reader training, unexpected kernel inefficiency, changing workload, unmodeled queue and preemption'},
        limitations=['FLOPs omit softmax/TopK/normalization/memory traffic/optimizer/AuxK and do not model utilization.',
          'Reference has 4-GPU DDP; dividing by four and scaling arithmetic is only a planning heuristic.',
          'Vocabulary projection remains large despite shallower backbone. No claim of measured acceleration.',
          'Checkpoint/validation 15% is an assumption; replace with measured inclusive wall time.'],
        scenarios=scenarios)
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
