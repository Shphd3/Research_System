
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def zipf_probs(n: int, alpha: float = 1.5) -> np.ndarray:
    ranks = np.arange(1, n + 1)
    q = 1.0 / (ranks ** alpha)
    q = q / q.sum()
    return q


class ToyData:
    def __init__(
        self,
        d_common: int = 4,
        k_tail: int = 12,
        p_tail_total: float = 0.15,
        alpha: float = 1.5,
        common_var: np.ndarray | None = None,
        seed: int = 0,
    ) -> None:
        set_seed(seed)
        self.d_common = d_common
        self.k_tail = k_tail
        self.d = d_common + k_tail
        if common_var is None:
            common_var = np.array([1.5, 1.0, 0.7, 0.5], dtype=np.float32)
        self.common_var = torch.tensor(common_var, dtype=torch.float32)
        q = zipf_probs(k_tail, alpha)
        self.q = torch.tensor(q, dtype=torch.float32)
        self.p_tail_total = p_tail_total

        beta_c_raw = torch.tensor(np.random.uniform(0.7, 1.3, size=d_common), dtype=torch.float32)
        beta_t_raw = torch.tensor(np.random.uniform(0.7, 1.3, size=k_tail), dtype=torch.float32)

        var_c_raw = torch.sum(beta_c_raw ** 2 * self.common_var).item()
        var_t_raw = torch.sum(beta_t_raw ** 2 * (self.p_tail_total * self.q)).item()

        scale_c = 1.0 / math.sqrt(var_c_raw)
        scale_t = 1.0 / math.sqrt(var_t_raw)
        self.beta_c = beta_c_raw * scale_c
        self.beta_t = beta_t_raw * scale_t
        self.beta = torch.cat([self.beta_c, self.beta_t])

    def sample(self, n: int):
        c = torch.randn(n, self.d_common) * torch.sqrt(self.common_var)[None, :]
        has_tail = (torch.rand(n) < self.p_tail_total)
        concept = torch.multinomial(self.q, n, replacement=True)
        amp = torch.randn(n)
        t = torch.zeros(n, self.k_tail)
        idx = torch.nonzero(has_tail).flatten()
        t[idx, concept[idx]] = amp[idx]

        y_c = c @ self.beta_c
        y_t = t @ self.beta_t
        y = y_c + y_t + 0.05 * torch.randn(n)
        x = torch.cat([c, t], dim=1)
        return x, y[:, None], y_c[:, None], y_t[:, None], has_tail, concept


def generate_batches(data: ToyData, steps: int, batch_size: int, test_n: int, seed: int):
    set_seed(seed)
    xs, ys, ycs, yts, has_tails, concepts = [], [], [], [], [], []
    for _ in range(steps):
        x, y, yc, yt, has_tail, concept = data.sample(batch_size)
        xs.append(x)
        ys.append(y)
        ycs.append(yc)
        yts.append(yt)
        has_tails.append(has_tail)
        concepts.append(concept)
    test = data.sample(test_n)
    return xs, ys, ycs, yts, has_tails, concepts, test


class FlatRegressor(torch.nn.Module):
    def __init__(self, d: int) -> None:
        super().__init__()
        self.linear = torch.nn.Linear(d, 1, bias=False)
        torch.nn.init.zeros_(self.linear.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)

    def split_weights(self, d_common: int):
        w = self.linear.weight.detach().clone().view(-1)
        return w[:d_common], w[d_common:]


class DecoupledRegressor(torch.nn.Module):
    def __init__(self, d_common: int, k_tail: int) -> None:
        super().__init__()
        self.common = torch.nn.Linear(d_common, 1, bias=False)
        self.tail = torch.nn.Linear(k_tail, 1, bias=False)
        torch.nn.init.zeros_(self.common.weight)
        torch.nn.init.zeros_(self.tail.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dc = self.common.in_features
        return self.common(x[:, :dc]) + self.tail(x[:, dc:])

    def split_weights(self):
        wc = self.common.weight.detach().clone().view(-1)
        wt = self.tail.weight.detach().clone().view(-1)
        return wc, wt


def cosine_lr(step: int, total_steps: int, lr0: float) -> float:
    return 0.5 * lr0 * (1.0 + math.cos(math.pi * step / total_steps))


def hold_then_cosine(step: int, total_steps: int, lr0: float, hold_ratio: float) -> float:
    hold_steps = int(total_steps * hold_ratio)
    if step < hold_steps:
        return lr0
    rem = max(1, total_steps - hold_steps)
    s = step - hold_steps
    return 0.5 * lr0 * (1.0 + math.cos(math.pi * s / rem))


def survival(weight: torch.Tensor, teacher: torch.Tensor) -> float:
    return float((weight * teacher).sum() / ((teacher * teacher).sum() + 1e-12))


def mse(pred: torch.Tensor, target: torch.Tensor) -> float:
    return float(torch.mean((pred - target) ** 2))


def train_config(
    config_name: str,
    data: ToyData,
    batches,
    test_data,
    *,
    steps: int,
    lr0: float,
    wd_common: float,
    wd_tail: float,
    hold_ratio: float,
    seed: int,
):
    set_seed(seed)
    d_common = data.d_common
    k_tail = data.k_tail
    d_total = data.d
    loss_fn = torch.nn.MSELoss()
    beta_c = data.beta_c
    beta_t = data.beta_t
    rare_idx = torch.arange(k_tail)[-max(1, k_tail // 3):]

    if config_name == "flat":
        model = FlatRegressor(d_total)
        opt = torch.optim.SGD(model.parameters(), lr=lr0, weight_decay=wd_common)
    else:
        model = DecoupledRegressor(d_common, k_tail)
        common_wd = wd_common
        tail_wd = wd_tail if config_name in {"decoupled_wd", "decoupled_full"} else wd_common
        opt_c = torch.optim.SGD(model.common.parameters(), lr=lr0, weight_decay=common_wd)
        opt_t = torch.optim.SGD(model.tail.parameters(), lr=lr0, weight_decay=tail_wd)

    metrics = {
        "step": [],
        "common_survival": [],
        "tail_survival": [],
        "rare_tail_survival": [],
        "train_loss": [],
        "lr_common": [],
        "lr_tail": [],
    }

    for step, (x, y) in enumerate(zip(batches[0], batches[1])):
        if config_name == "flat":
            lr = cosine_lr(step, steps, lr0)
            opt.param_groups[0]["lr"] = lr
            opt.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            opt.step()
            wc, wt = model.split_weights(d_common)
            lr_c = lr_t = lr
        else:
            lr_c = cosine_lr(step, steps, lr0)
            if config_name in {"decoupled_lr", "decoupled_full"}:
                lr_t = hold_then_cosine(step, steps, lr0, hold_ratio)
            else:
                lr_t = cosine_lr(step, steps, lr0)
            opt_c.param_groups[0]["lr"] = lr_c
            opt_t.param_groups[0]["lr"] = lr_t
            opt_c.zero_grad()
            opt_t.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            opt_c.step()
            opt_t.step()
            wc, wt = model.split_weights()

        metrics["step"].append(step)
        metrics["common_survival"].append(survival(wc, beta_c))
        metrics["tail_survival"].append(survival(wt, beta_t))
        metrics["rare_tail_survival"].append(survival(wt[rare_idx], beta_t[rare_idx]))
        metrics["train_loss"].append(float(loss.detach()))
        metrics["lr_common"].append(lr_c)
        metrics["lr_tail"].append(lr_t)

    x_test, y_test, yc_test, yt_test, _, _ = test_data
    with torch.no_grad():
        pred = model(x_test)
        if config_name == "flat":
            w = model.linear.weight.view(-1)
            pred_c = x_test[:, :d_common] @ w[:d_common][:, None]
            pred_t = x_test[:, d_common:] @ w[d_common:][:, None]
            wc, wt = w[:d_common], w[d_common:]
        else:
            pred_c = model.common(x_test[:, :d_common])
            pred_t = model.tail(x_test[:, d_common:])
            wc, wt = model.split_weights()

    results = {
        "overall_mse": mse(pred, y_test),
        "common_mse": mse(pred_c, yc_test),
        "tail_mse": mse(pred_t, yt_test),
        "common_survival_final": survival(wc, beta_c),
        "tail_survival_final": survival(wt, beta_t),
        "rare_tail_survival_final": survival(wt[rare_idx], beta_t[rare_idx]),
    }
    return metrics, results


def aggregate_curves(curve_dfs: list[pd.DataFrame]) -> pd.DataFrame:
    out = curve_dfs[0][["step"]].copy()
    metric_cols = [c for c in curve_dfs[0].columns if c != "step"]
    for col in metric_cols:
        stacked = np.stack([df[col].to_numpy() for df in curve_dfs], axis=0)
        out[f"{col}_mean"] = stacked.mean(axis=0)
        out[f"{col}_std"] = stacked.std(axis=0)
    return out


def plot_mean_curve(mean_curve: pd.DataFrame, configs: list[str], metric: str, title: str, out_path: Path) -> None:
    plt.figure(figsize=(7, 4.5))
    for cfg in configs:
        plt.plot(mean_curve[cfg]["step"], mean_curve[cfg][f"{metric}_mean"], label=cfg)
    plt.xlabel("training step")
    plt.ylabel(metric.replace("_", " "))
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def main():
    out_dir = Path(__file__).resolve().parent.parent
    (out_dir / "results").mkdir(exist_ok=True)
    (out_dir / "figures").mkdir(exist_ok=True)

    # Main experiment setting
    steps = 1500
    batch_size = 64
    test_n = 12000
    lr0 = 0.20
    wd_common = 5e-3
    wd_tail = 2e-4
    hold_ratio = 0.80
    seeds = [0, 1, 2]
    configs = ["flat", "decoupled_wd", "decoupled_lr", "decoupled_full"]

    all_final_rows = []
    mean_curve_dict = {}

    for cfg in configs:
        curve_dfs = []
        for seed in seeds:
            data = ToyData(seed=seed, p_tail_total=0.15, alpha=1.5, k_tail=12)
            batches = generate_batches(data, steps=steps, batch_size=batch_size, test_n=test_n, seed=100 + seed)
            metrics, results = train_config(
                cfg,
                data,
                batches,
                batches[-1],
                steps=steps,
                lr0=lr0,
                wd_common=wd_common,
                wd_tail=wd_tail,
                hold_ratio=hold_ratio,
                seed=seed,
            )
            curve_df = pd.DataFrame(metrics)
            curve_df.to_csv(out_dir / "results" / f"curves_{cfg}_seed{seed}.csv", index=False)
            curve_dfs.append(curve_df)

            row = {
                "config": cfg,
                "seed": seed,
                "overall_mse": results["overall_mse"],
                "common_mse": results["common_mse"],
                "tail_mse": results["tail_mse"],
                "common_survival_final": results["common_survival_final"],
                "tail_survival_final": results["tail_survival_final"],
                "rare_tail_survival_final": results["rare_tail_survival_final"],
            }
            all_final_rows.append(row)

        mean_curve = aggregate_curves(curve_dfs)
        mean_curve.to_csv(out_dir / "results" / f"mean_curve_{cfg}.csv", index=False)
        mean_curve_dict[cfg] = mean_curve

    final_df = pd.DataFrame(all_final_rows)
    final_df.to_csv(out_dir / "results" / "per_seed_results.csv", index=False)

    summary = (
        final_df.groupby("config")
        .agg(["mean", "std"])
        .reset_index()
    )
    summary.to_csv(out_dir / "results" / "final_results_mean_std.csv", index=False)

    plot_mean_curve(mean_curve_dict, configs, "common_survival", "Common coefficient survival", out_dir / "figures" / "common_survival_curve.png")
    plot_mean_curve(mean_curve_dict, configs, "tail_survival", "Tail coefficient survival", out_dir / "figures" / "tail_survival_curve.png")
    plot_mean_curve(mean_curve_dict, configs, "rare_tail_survival", "Rare-tail coefficient survival", out_dir / "figures" / "rare_tail_survival_curve.png")
    plot_mean_curve(mean_curve_dict, configs, "lr_common", "Common learning-rate schedule", out_dir / "figures" / "lr_common_curve.png")
    plot_mean_curve(mean_curve_dict, configs, "lr_tail", "Tail learning-rate schedule", out_dir / "figures" / "lr_tail_curve.png")
    plot_mean_curve(mean_curve_dict, configs, "train_loss", "Training loss", out_dir / "figures" / "train_loss_curve.png")


if __name__ == "__main__":
    main()
