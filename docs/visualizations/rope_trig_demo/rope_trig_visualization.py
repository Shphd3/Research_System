"""Generate compact trigonometric and RoPE visualizations.

The script uses only NumPy and Matplotlib and writes two PNG files beside it
when run directly.
"""

from pathlib import Path

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def rope_frequencies(dimension: int) -> np.ndarray:
    """Return theta_i = 10000^(-2i/d) for each 2D dimension pair."""
    if dimension <= 0 or dimension % 2:
        raise ValueError("RoPE dimension must be a positive even integer")
    indices = np.arange(dimension // 2, dtype=float)
    return 10000.0 ** (-2.0 * indices / dimension)


def rotate_2d(vector, angle: float) -> np.ndarray:
    """Rotate a two-component vector counter-clockwise by ``angle`` radians."""
    values = np.asarray(vector, dtype=float)
    if values.shape != (2,):
        raise ValueError("vector must contain exactly two components")
    cosine, sine = np.cos(angle), np.sin(angle)
    return np.array(
        [cosine * values[0] - sine * values[1], sine * values[0] + cosine * values[1]]
    )


def _pi_tick_labels():
    locations = np.arange(-2.0, 2.1, 0.5) * np.pi
    labels = ["-2π", "-3π/2", "-π", "-π/2", "0", "π/2", "π", "3π/2", "2π"]
    return locations, labels


def _plot_trigonometric_functions(path: Path) -> None:
    x = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 3201)
    tangent = np.tan(x)
    tangent[np.abs(np.cos(x)) < 0.045] = np.nan

    figure, axis = plt.subplots(figsize=(12, 7), dpi=180)
    axis.plot(x, np.sin(x), label="sin(x)", linewidth=2.2, color="#2563eb")
    axis.plot(x, np.cos(x), label="cos(x)", linewidth=2.2, color="#16a34a")
    axis.plot(x, tangent, label="tan(x)", linewidth=1.8, color="#dc2626")
    for pole in (-1.5 * np.pi, -0.5 * np.pi, 0.5 * np.pi, 1.5 * np.pi):
        axis.axvline(pole, color="#dc2626", linestyle=":", linewidth=0.9, alpha=0.5)
    ticks, labels = _pi_tick_labels()
    axis.set_xticks(ticks, labels)
    axis.set_xlim(-2.0 * np.pi, 2.0 * np.pi)
    axis.set_ylim(-3.2, 3.2)
    axis.set_xlabel("x (radians)")
    axis.set_ylabel("function value")
    axis.set_title("Basic trigonometric functions")
    axis.axhline(0.0, color="black", linewidth=0.7, alpha=0.5)
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper left", ncol=3, frameon=True)
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def _plot_rope_positions(path: Path) -> None:
    dimension = 8
    frequencies = rope_frequencies(dimension)
    positions = np.arange(33)
    selected_positions = np.array([0, 4, 8, 16, 32])
    base_vector = np.array([1.0, 0.35])

    figure = plt.figure(figsize=(14, 10), dpi=180)
    grid = figure.add_gridspec(4, 2, width_ratios=(1.08, 1.0), wspace=0.28, hspace=0.62)
    vector_axis = figure.add_subplot(grid[:, 0])
    vector_axis.set_aspect("equal", adjustable="box")
    vector_axis.add_patch(Circle((0.0, 0.0), np.linalg.norm(base_vector), fill=False, linestyle="--", color="#94a3b8"))

    colors = plt.get_cmap("viridis")(np.linspace(0.08, 0.92, len(selected_positions)))
    for color, position in zip(colors, selected_positions):
        rotated = rotate_2d(base_vector, float(position) * frequencies[0])
        vector_axis.arrow(
            0.0,
            0.0,
            rotated[0],
            rotated[1],
            color=color,
            width=0.012,
            head_width=0.11,
            length_includes_head=True,
            alpha=0.95,
        )
        vector_axis.text(rotated[0] * 1.12, rotated[1] * 1.12, f"p={position}", color=color, fontsize=9, ha="center")
    vector_axis.scatter(*base_vector, color="#0f172a", s=24, zorder=5, label="base vector at p=0")
    vector_axis.scatter(0.0, 0.0, color="#0f172a", s=18, zorder=5)
    vector_axis.set_xlim(-1.65, 1.65)
    vector_axis.set_ylim(-1.65, 1.65)
    vector_axis.set_xlabel("dimension-pair component 1")
    vector_axis.set_ylabel("dimension-pair component 2")
    vector_axis.set_title("One 2D RoPE pair: same vector, different positions")
    vector_axis.text(
        0.02,
        0.02,
        "pair i=0, θ₀=1.000\nThis is one pair, not the full d-dimensional vector.",
        transform=vector_axis.transAxes,
        fontsize=9,
        va="bottom",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#cbd5e1", "alpha": 0.9},
    )
    vector_axis.grid(True, alpha=0.25)

    for index, frequency in enumerate(frequencies):
        axis = figure.add_subplot(grid[index, 1])
        angle = positions * frequency
        axis.plot(positions, np.cos(angle), color="#2563eb", linewidth=1.8, label="cos(p·θᵢ)")
        axis.plot(positions, np.sin(angle), color="#f97316", linewidth=1.8, label="sin(p·θᵢ)")
        axis.set_ylim(-1.12, 1.12)
        axis.set_xlim(0, 32)
        axis.set_ylabel("value")
        axis.set_title(f"i={index}, θᵢ={frequency:.3e}", loc="left", fontsize=10)
        axis.grid(True, alpha=0.22)
        if index == 0:
            axis.legend(loc="upper right", fontsize=8, ncol=2, frameon=True)
        if index == len(frequencies) - 1:
            axis.set_xlabel("position p")
        else:
            axis.set_xticklabels([])

    figure.suptitle(
        "Rotary Position Embedding (RoPE): θᵢ = 10000^(-2i/d), rotation angle = p·θᵢ (d=8)",
        fontsize=14,
        y=0.99,
    )
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def generate_figures(output_directory=Path(__file__).resolve().parent):
    """Generate both demonstration PNGs and return their paths."""
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    trig_path = output_directory / "trig_functions.png"
    rope_path = output_directory / "rope_positions.png"
    _plot_trigonometric_functions(trig_path)
    _plot_rope_positions(rope_path)
    return trig_path, rope_path


if __name__ == "__main__":
    for output in generate_figures():
        print(f"wrote {output}")
