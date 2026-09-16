"""Small CPU checks, NOT evidence from an actual trained language model.
Run: python verify_sae_identity.py --output identity_checks.json
Requires Python 3.10+ and PyTorch. Uses float64 and fixed random seeds.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import torch


def topk_codes(x: torch.Tensor, encoder: torch.Tensor, bias: torch.Tensor, k: int) -> torch.Tensor:
    scores = torch.relu(x @ encoder.T + bias)
    values, indices = torch.topk(scores, k, dim=-1)
    return torch.zeros_like(scores).scatter(-1, indices, values)


def check_identity() -> dict:
    torch.manual_seed(17)
    dtype = torch.float64
    x = torch.randn(23, 4, dtype=dtype)
    encoder = torch.randn(7, 4, dtype=dtype)
    bias = torch.randn(7, dtype=dtype)
    decoder = torch.nn.functional.normalize(torch.randn(4, 7, dtype=dtype), dim=0)
    permutation = torch.tensor([4, 2, 6, 0, 5, 1, 3])
    z = topk_codes(x, encoder, bias, 3)
    zp = topk_codes(x, encoder[permutation], bias[permutation], 3)
    recon = z @ decoder.T
    recon_p = zp @ decoder[:, permutation].T
    err = float((recon - recon_p).abs().max())
    gram_err = float((z @ z.T - zp @ zp.T).abs().max())
    mse = float((recon - x).square().mean())
    mse_p = float((recon_p - x).square().mean())
    assert err < 1e-12 and gram_err < 1e-12
    assert torch.equal((z != 0).sum(-1), (zp != 0).sum(-1))
    assert torch.allclose(zp, z[:, permutation], atol=1e-12, rtol=0)

    # Two artificial input classes A and B. These labels are not real semantic data.
    examples = torch.eye(2, dtype=dtype)
    start = examples @ torch.eye(2, dtype=dtype).T
    swapped = examples @ torch.eye(2, dtype=dtype).flip(0).T
    assert start[:, 0].tolist() == [1.0, 0.0]
    assert swapped[:, 0].tolist() == [0.0, 1.0]

    # Continuous parameter path: slot 0 moves from e_1 to e_2 without relabeling.
    angles = torch.linspace(0, torch.pi / 2, 5, dtype=dtype)
    slot_path = torch.stack([torch.cos(angles), torch.sin(angles)], dim=1)
    responses = (examples @ slot_path.T).T

    def aux_gradient(detach_input: bool, detach_target: bool) -> tuple[float, list]:
        theta = torch.tensor([[1.0, 0.2], [0.3, 0.8]], dtype=dtype, requires_grad=True)
        readout = torch.diag(torch.tensor([0.5, 0.25], dtype=dtype)).requires_grad_()
        h = examples @ theta.T
        source = h.detach() if detach_input else h
        target = h.detach() if detach_target else h
        scale = h.detach().square().mean(-1).clamp_min(1e-4)
        loss = ((source @ readout.T - target).square().mean(-1) / scale).mean()
        grad = torch.autograd.grad(loss, theta, allow_unused=True)[0]
        if grad is None:
            return 0.0, [[0.0, 0.0], [0.0, 0.0]]
        return float(grad.norm()), grad.tolist()

    observer_norm, _ = aux_gradient(True, True)
    live_norm, live_grad = aux_gradient(False, True)
    full_norm, full_grad = aux_gradient(False, False)
    assert observer_norm == 0.0 and live_norm > 0.0
    assert not torch.allclose(torch.tensor(live_grad), torch.tensor(full_grad))
    return {
        "scope": "Synthetic mathematical / automatic-differentiation checks only; not LM experimental results.",
        "seed": 17,
        "dtype": "float64",
        "permutation": {
            "maximum_reconstruction_difference": err,
            "maximum_sample_gram_difference": gram_err,
            "reconstruction_mse_before": mse,
            "reconstruction_mse_after": mse_p,
            "activation_count_unchanged": True,
            "original_slot_0_response_on_A_B": start[:, 0].tolist(),
            "permuted_slot_0_response_on_A_B": swapped[:, 0].tolist(),
        },
        "continuous_slot": {"responses_on_A_B_along_path": responses.tolist()},
        "gradient": {
            "observer_auxiliary_backbone_gradient_norm": observer_norm,
            "live_encoder_detached_target_gradient_norm": live_norm,
            "live_encoder_live_target_gradient_norm": full_norm,
            "detaching_target_changes_the_objective_gradient": True,
        },
        "all_checks_passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("identity_checks.json"))
    args = parser.parse_args()
    result = check_identity()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
