# A15_01_05 Thinking Card: Layerwise Variance And Spectral Atlas Of Coarse And Fine Semantics

Status: researcher judgment completed and approved for formalization on 2026-08-04.

## My Judgment

- **Concrete phenomenon:** Prior experiments showed that a compositional target can become more readable in deep full representations and that same-token parent/child roles have layer-specific spectral responses. They did not directly compare between-class variance for broad categories with within-parent between-class variance for fine categories.
- **Mechanism hypothesis:** Broad domains may already be separable in shallow layers. Fine subfields require resolving nearby meanings after conditioning on the parent domain, so fine discriminability relative to coarse discriminability may increase with depth.
- **Spectral hypothesis:** Both semantic granularities may place most per-direction actual semantic variance in the first covariance band. Fine semantics may nevertheless allocate a larger relative share to middle and tail bands; its absolute energy need not exceed coarse semantics there.
- **Strongest rival:** Any apparent depth or spectral difference may be explained by unequal label entropy, sample count, lexical leakage, token length, prompt template, readout position, residual scale, tiny eigenvalues, or arbitrary equal-dimensional subspaces.
- **Most uncertain link:** Whether frozen Qwen3-8B can distinguish the natural concepts after removing the correct label strings, and whether covariance rank is more specific than an equal-dimensional random orientation.
- **Evidence that would change the judgment:** Fine/coarse relative discriminability does not increase with depth after matching labels, samples, templates, positions, and readout object; or fine non-head enrichment fails to replicate across sealed templates, parents, calibration splits, and random-subspace controls.
- **One decision:** Build a static `layer x semantic granularity x 16 covariance bands` atlas in frozen Qwen3-8B. Only a stable atlas may nominate coordinates for a separately approved Router-function test.

## AI Audit

- **Undefined object or hidden assumption:** “Fine is stronger” must mean stable within-parent discriminability or relative band enrichment. It cannot be replaced by a single-token projection or total energy from bands of unequal width.
- **Minimal counterexample:** If both variables are readable from the full representation but the registered covariance bands do not outperform equal-dimensional random subspaces, semantic information exists but covariance rank is not its privileged coordinate.
- **AI recommendation:** pursue.

## My Confirmation

- **Retained judgment:** The semantic structure contains only two levels, parent and child. Composition steps, long/short dependencies, Router utility, and training benefit are outside this experiment.
- **Permission to formalize:** yes.

