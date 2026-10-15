"""Source-only gradient SVD and frozen native finite-loss response audit.

This is an exploratory analysis of existing caches, not an LM/SAE update.
Raw arrays and logs stay in the execution workspace supplied by --out.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.stats import rankdata
from threadpoolctl import threadpool_limits

DOMAINS = ["computer_science", "mathematics", "physics", "biology"]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(16 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dump(path, obj):
    def encode(x):
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, np.generic):
            return x.item()
        raise TypeError(type(x))
    Path(path).write_text(json.dumps(obj, default=encode, ensure_ascii=False,
                                   allow_nan=False, indent=2) + "\n")


def write_csv(path, rows):
    with Path(path).open("w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def corr(x, y):
    x = x - np.mean(x)
    y = y - np.mean(y)
    return float(np.dot(x, y) / np.sqrt(np.dot(x, x) * np.dot(y, y)))


def corr_ci(x, y, boot):
    # The 16 positions stay attached to their record in every bootstrap draw.
    xx, yy = x.reshape(-1, 16), y.reshape(-1, 16)
    sums = np.column_stack([xx.sum(1), yy.sum(1), (xx * yy).sum(1),
                            (xx * xx).sum(1), (yy * yy).sum(1)])
    s = boot @ sums
    n = 16 * boot.sum(1)
    cov = s[:, 2] - s[:, 0] * s[:, 1] / n
    vx = s[:, 3] - s[:, 0] ** 2 / n
    vy = s[:, 4] - s[:, 1] ** 2 / n
    rr = cov / np.sqrt(np.maximum(vx * vy, 1e-300))
    return [float(v) for v in np.quantile(rr, [.025, .975])]


def decomposition(gram, scale):
    kg = gram / scale[:, None] / scale[None, :]
    eig, u = np.linalg.eigh(kg)
    ix = np.argsort(eig)[::-1]
    eig, u = eig[ix], u[:, ix]
    assert eig[-1] > eig[0] * 1e-12, "Four nondegenerate source directions expected"
    for k in range(4):
        if u[np.argmax(np.abs(u[:, k])), k] < 0:
            u[:, k] *= -1
    return eig, u


def self_check():
    rng = np.random.default_rng(1008)
    c, e = rng.normal(size=(41, 5)), rng.normal(size=(41, 3))
    g = np.einsum("ni,nj->nij", e, c).reshape(41, -1)
    m = rng.normal(size=(4, 15))
    h = -g @ m.T
    gram = m @ m.T
    for scale in [np.ones(4), np.sqrt(np.diag(gram))]:
        eig, u = decomposition(gram, scale)
        basis = (u.T @ (m / scale[:, None])) / np.sqrt(eig)[:, None]
        r = (h / scale[None, :]) @ u / np.sqrt(eig)[None, :]
        assert np.allclose(r, -g @ basis.T, atol=1e-12)
        components = r[:, None, :] * (scale[:, None] * u * np.sqrt(eig)[None, :])[None, :, :]
        assert np.allclose(components.sum(2), h, atol=1e-12)
        assert np.allclose(basis @ basis.T, np.eye(4), atol=1e-12)
        cg = np.cov(g, rowvar=False, bias=True)
        assert np.allclose(np.cov(r, rowvar=False, bias=True), basis @ cg @ basis.T, atol=1e-12)
    return {"explicit_outer_product_gradient": True,
            "raw_and_unit_source_basis": True,
            "orthonormal_parameter_basis": True,
            "component_response_closure": True,
            "receiver_covariance_identity": True}


def main(args):
    started = time.monotonic()
    out = Path(args.out)
    recipe_path = out / "recipe.json"
    assert recipe_path.exists(), "Freeze recipe before computation"
    assert not (out / "receipt.json").exists(), "Do not overwrite a completed audit"
    recipe = json.loads(recipe_path.read_text())
    for path, expected in recipe["inputs"].items():
        assert sha(path) == expected, path
    dump(out / "implementation_checks.json", self_check())

    old = Path(recipe["source_workspace"]) / "runs"
    m = np.load(old / "cache_audit_01/source_mean_gradients.npy").astype(np.float64)
    assert m.shape == (4, 1024, 2048)
    m = m.reshape(4, -1)
    gram = m @ m.T
    norms = np.sqrt(np.diag(gram))
    cz = np.load(old / "cache_audit_01/responses.npz")
    h, docs, positions = cz["readout"], cz["readout_docs"], cz["readout_positions"]
    domains = cz["readout_domains"]
    meta = np.load(old / "finite_panel_01/panel_metadata.npz")
    ix = np.flatnonzero(meta["part"] == 1)
    assert np.array_equal(meta["docs"][ix], docs)
    assert np.array_equal(meta["positions"][ix], positions)
    assert np.array_equal(meta["domains"][ix], domains)
    assert np.array_equal(positions, np.tile(np.arange(16), 1024))
    assert np.all(docs.reshape(-1, 16) == docs.reshape(-1, 16)[:, :1])
    assert len(np.unique(docs)) == 1024
    effects = np.load(old / "finite_panel_01/effects.npz")
    linear = np.load(old / "finite_panel_01/first_order.npz")
    eta = recipe["eta"]
    losses = {step: np.column_stack([effects[d + "__" + step][ix] for d in DOMAINS])
              for step in ["full_step", "half_step"]}
    closure = max(float(np.max(np.abs(linear[d + "__full_step"][ix] - eta * h[:, j])))
                  for j, d in enumerate(DOMAINS))
    assert closure < 1e-10

    records = [json.loads(s) for s in Path(recipe["record_manifest"]).open()]
    record_docs = docs.reshape(-1, 16)[:, 0]
    categories = np.array([records[int(d)]["category"] for d in record_docs])
    rng = np.random.default_rng(recipe["bootstrap_seed"])
    boot = np.zeros((recipe["bootstrap_draws"], 1024), dtype=np.int16)
    for cat in sorted(set(categories)):
        ids = np.flatnonzero(categories == cat)
        boot[:, ids] = rng.multinomial(len(ids), np.full(len(ids), 1 / len(ids)), size=len(boot))

    # Independent direct e^T M c check on one metadata-fixed record per domain.
    wanted = {int(record_docs[np.flatnonzero(domains.reshape(-1, 16)[:, 0] == d)[0]]) for d in range(4)}
    h_lookup = {(int(doc), int(pos)): i for i, (doc, pos) in enumerate(zip(docs, positions))}
    direct_max, checked = 0., 0
    feature_run = Path(recipe["feature_run"])
    matrices = m.reshape(4, 1024, 2048)
    for worker in range(4):
        z = np.load(feature_run / "readout" / f"shard_{worker}" / "features.npz")
        rows = z["row_indices"]
        selected = np.flatnonzero(np.isin(rows, list(wanted)))
        if len(selected) == 0:
            continue
        c, e = z["c"][selected].astype(float), z["e"][selected].astype(float)
        c, e = c.reshape(-1, 2048), e.reshape(-1, 1024)
        expected = np.array([h[h_lookup[(int(doc), p)]] for doc in rows[selected] for p in range(16)])
        actual = np.column_stack([-np.einsum("ni,ij,nj->n", e, matrix, c, optimize=True)
                                  for matrix in matrices])
        direct_max = max(direct_max, float(np.max(np.abs(actual - expected))))
        checked += len(c)
    assert checked == 64 and direct_max < 1e-9

    geometry = []
    correlations = []
    spectra = []
    loadings = []
    cumulative = []
    arrays = {"docs": docs, "positions": positions, "domains": domains, "H": h}
    for i, di in enumerate(DOMAINS):
        for j, dj in enumerate(DOMAINS):
            geometry.append({"source_i": di, "source_j": dj,
                             "gradient_cosine": gram[i, j] / norms[i] / norms[j],
                             "finite_response_pearson": corr(losses["full_step"][:, i], losses["full_step"][:, j]),
                             "first_order_response_pearson": corr(h[:, i], h[:, j]),
                             "scope": "same_1024_records_16384_events_fixed_sources"})
    write_csv(out / "gradient_geometry_vs_loss.csv", geometry)

    common = m.mean(0)
    for mode, scale in [("raw", np.ones(4)), ("unit_norm", norms)]:
        eig, u = decomposition(gram, scale)
        r = (h / scale[None, :]) @ u / np.sqrt(eig)[None, :]
        coef = scale[:, None] * u * np.sqrt(eig)[None, :]
        components = r[:, None, :] * coef[None, :, :]
        assert np.allclose(components.sum(2), h, atol=1e-10)
        arrays[mode + "__unit_direction_response"] = r
        arrays[mode + "__components"] = components
        for k in range(4):
            basis = (u[:, k] / scale) @ m / np.sqrt(eig[k])
            spectra.append({"basis": mode, "component": k + 1, "eigenvalue": eig[k],
                            "gradient_energy_fraction": eig[k] / eig.sum(),
                            "cumulative_gradient_energy_fraction": eig[:k + 1].sum() / eig.sum(),
                            "cosine_to_raw_mean_gradient": np.dot(basis, common) / np.linalg.norm(common),
                            "definition": "uncentered_SVD_of_four_source_mean_gradients"})
            for d, name in enumerate(DOMAINS):
                loadings.append({"basis": mode, "component": k + 1, "source": name,
                                 "source_eigenvector_loading": u[d, k],
                                 "raw_gradient_projection_coefficient": coef[d, k]})
            for l in range(4):
                correlations.append({"basis": mode, "component_i": k + 1, "component_j": l + 1,
                                     "parameter_inner_product": float(k == l),
                                     "receiver_response_pearson": corr(r[:, k], r[:, l])})
        for k in range(1, 5):
            hk = components[:, :, :k].sum(2)
            for step, step_eta in [("full_step", eta), ("half_step", eta / 2)]:
                for d, name in enumerate(DOMAINS):
                    x, y = step_eta * hk[:, d], losses[step][:, d]
                    ci = corr_ci(x, y, boot)
                    cumulative.append({"basis": mode, "k": k, "source": name, "step": step,
                                       "gradient_energy_fraction": eig[:k].sum() / eig.sum(),
                                       "finite_pearson": corr(x, y), "conditional_lo": ci[0], "conditional_hi": ci[1],
                                       "finite_spearman": corr(rankdata(x), rankdata(y)),
                                       "relative_signed_response_squared_error": np.sum((hk[:, d] - h[:, d]) ** 2) / np.sum(h[:, d] ** 2),
                                       "relative_absolute_finite_error": np.sum(np.abs(x - y)) / np.sum(np.abs(y)),
                                       "finite_mean_nat": y.mean(), "predicted_mean_nat": x.mean(),
                                       "sign_agreement_outside_1e_5": np.mean(np.sign(x[np.abs(y) > 1e-5]) == np.sign(y[np.abs(y) > 1e-5])),
                                       "events": len(y), "records": 1024})
    write_csv(out / "gradient_component_spectrum.csv", spectra)
    write_csv(out / "gradient_component_loadings.csv", loadings)
    write_csv(out / "gradient_component_response_correlations.csv", correlations)
    write_csv(out / "gradient_cumulative_vs_finite.csv", cumulative)
    np.savez_compressed(out / "component_arrays.npz", **arrays)
    dump(out / "summary.json", {"source_domains": DOMAINS, "records": 1024, "events": 16384,
                                "gradient_geometry_vs_loss": geometry, "spectrum": spectra,
                                "component_response_correlations": correlations,
                                "cumulative_vs_finite": cumulative,
                                "scope": "exposed_panel_post_hoc_fixed_source_association_not_semantic_causality",
                                "principal_basis_definition": "four_aggregated_domain_gradients_not_event_gradient_PCA",
                                "scientific_judgment": "Unknown"})
    for path, expected in recipe["inputs"].items():
        assert sha(path) == expected, "Input changed: " + path
    output_hashes = {p.name: sha(p) for p in sorted(out.iterdir()) if p.name not in ["receipt.json", "run.log"]}
    dump(out / "receipt.json", {"status": "COMPLETE_EXPLORATORY_COMPONENT_AUDIT",
                                "completed_at_utc": datetime.now(timezone.utc).isoformat(),
                                "elapsed_seconds": time.monotonic() - started,
                                "inputs_unchanged": True, "source_recipe_sha256": sha(recipe_path),
                                "implementation_sha256": sha(__file__), "output_sha256": output_hashes,
                                "direct_factorized_response_events": checked,
                                "direct_factorized_response_max_abs_error": direct_max,
                                "old_finite_linear_alignment_max_abs_error": closure,
                                "LM_forwards": 0, "LM_updates": 0, "SAE_updates": 0,
                                "GPU_used": False, "remote_jobs": 0,
                                "scientific_judgment": "Unknown"})
    print(json.dumps({"status": "COMPLETE_EXPLORATORY_COMPONENT_AUDIT",
                      "seconds": time.monotonic() - started, "out": str(out)}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    with threadpool_limits(limits=8):
        main(parser.parse_args())
