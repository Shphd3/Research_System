"""Pooling helper. The caller MUST pass post-output-projection attention vectors.
content_mask selects text tokens only, not padding or automatically inserted specials.
This helper cannot establish the model's extraction site; see the audit plan.
"""
from __future__ import annotations
import torch


def pool_attention(a: torch.Tensor, content_mask: torch.Tensor) -> dict[str, torch.Tensor]:
    if a.ndim != 3:
        raise ValueError(f"Expected [batch, sequence, hidden], got {tuple(a.shape)}")
    if content_mask.shape != a.shape[:2]:
        raise ValueError("Mask and activation shapes differ")
    mask = content_mask.to(device=a.device, dtype=torch.bool)
    lengths = mask.sum(dim=1)
    if torch.any(lengths == 0):
        raise ValueError("An example has no selected text tokens")
    positions = torch.arange(a.shape[1], device=a.device).expand_as(mask)
    last_indices = positions.masked_fill(~mask, -1).max(dim=1).values
    x = a.float()
    selected = x.masked_fill(~mask.unsqueeze(-1), 0.0)
    mean = selected.sum(dim=1) / lengths.unsqueeze(-1)
    last = x[torch.arange(a.shape[0], device=a.device), last_indices]
    if not torch.isfinite(mean).all() or not torch.isfinite(last).all():
        raise FloatingPointError("Non-finite pooled representation")
    return {"mean": mean, "last": last, "last_index": last_indices, "n_content_tokens": lengths}


def _test() -> None:
    a = torch.tensor([[[100.], [2.], [4.], [999.]],
                      [[999.], [100.], [6.], [8.]]])
    mask = torch.tensor([[False, True, True, False], [False, False, True, True]])
    out = pool_attention(a, mask)
    torch.testing.assert_close(out["mean"], torch.tensor([[3.], [7.]]))
    torch.testing.assert_close(out["last"], torch.tensor([[4.], [8.]]))
    assert out["last_index"].tolist() == [2, 3]
    # Right- and left-padded views of the same content agree.
    x = torch.tensor([[[2.], [4.], [999.]], [[999.], [2.], [4.]]])
    m = torch.tensor([[True, True, False], [False, True, True]])
    p = pool_attention(x, m)
    torch.testing.assert_close(p["mean"][0], p["mean"][1])
    torch.testing.assert_close(p["last"][0], p["last"][1])
    try:
        pool_attention(x, torch.zeros_like(m))
    except ValueError:
        pass
    else:
        raise AssertionError("Empty content mask must fail")
    print("Pooling unit tests passed (synthetic tensors; no user model tested).")


if __name__ == "__main__":
    _test()
