# Functional dependence of context-related computation on a common candidate

## 1. Problem Definition

The parent goal is evidence for retaining shared computation while allowing differential computation to specialize. Existing A15_25 joint-feature geometry does not establish this dependency; A17 is motivation for functional testing, not evidence about natural-language dependence.

Here C and R are activation-response candidates; R is neither the A17 parameter complement nor activation minus C.

For the same token in different contexts, does reducing stable candidate C at block14 specifically affect predefined context-related R readouts at block28 and corresponding prediction, beyond matched perturbations? A qualified positive result motivates later shared-path tests; a resolved negative weakens this precise dependency; failed measurement yields insufficient evidence.

## 2. Physical Priors

Block14 residual-post precedes block28 residual-post before final normalization. The frozen dictionary jointly encodes blocks2,4,...,28 into one z. Decoder directions are nonorthogonal; global z is not a causal layer-local feature measurement. Stable cross-context response is a candidate property, not a frequency-defined function.

## 3. Falsifiable Hypotheses

H1: selected context computation depends on C; C suppression produces larger R discrimination loss and predefined contextual-prediction damage than actual-norm matched random and other-candidate interventions. H2: coactivation without detectable specific dependency; effects resemble controls or remain stable. H3: generic damage, reconstruction error, or readout cross-talk; matched controls are similarly harmed or only coordinate scores change. Outcomes map to the companion decision table, not a forced unique story.

## 4. Mathematical Model

With frozen TRAIN mean mu_l and vector RMS s_l, x_l=(h_l-mu_l)/s_l. The joint encoder gives z from all14layers; reconstruction is b_l+sum_f z_f d_lf. At one token t edit the native block14 activation by

\[
h'_{14,t}=h_{14,t}-\alpha s_{14}\sum_{f\in C}z_f^{(0)}d_{14,f},\qquad\alpha\in\{0.05,0.10\}.
\]

Keep bias, other contributions and original reconstruction residual. Match actual BF16 displacement, not intended count or norm. Joint baseline z supplies offline dose only; never re-encode intervened multi-layer activations for the downstream readout.

R is a fixed nuisance-residualized local decoder-direction score of actual block28 activation, not an independently identified feature activation. Check direct residual-stream carry separately. Functional outcome is the true context's next-token log-probability advantage over a prespecified alternative-context token; also measure generic subsequent CE.

## 5. Computational Realization

Reuse frozen Qwen3-0.6B Base, final A22 14layer/F16384 dictionary, and existing Tulu caches. Discover at most2tokens,1–2Cfeatures and1Rfeature each, controlling token identity, position and provenance. Define candidates before recording their frequency. Fix14→28 structurally before outcomes.

After explicit future authorization, qualify readouts on discovery and freeze candidates/targets before held-out intervention outcomes. Each context receives baseline, no-op repeat,2C doses,5random directions×2doses,3other-candidate sets×2doses independently. This is offline intervention, not online routing. Current work is metadata-only; no forward or discovery was run.

## 6. Minimal Falsification Tests

Primary0.10dose must beat both matched-control families on R discrimination loss≥0.10discoverySD and prediction-margin damage≥0.02nat, with corrected intervals supporting positive effects and passed measurement/carry/generic-damage guards.0.05is secondary. Thresholds are proposed operational choices, not natural constants. Cluster by document; at most2candidates cannot establish model-wide laws. Joint readout/function effects do not establish R mediation without separate R intervention or rescue.

## 7. Current Evidence

Current selected asset access passes. Weight files were not deserialized or fully rehashed; saved hashes are retained. Historical DCLM block14/28 FVE is99.471%/86.472%; historical final-layer reconstruction replacement adds~0.306nat CE. This is not current Tulu measurement qualification.

Existing Tulu stores only raw last-layer activation plus joint z; source activation and independent layer-local encoder are absent from these selected caches. Existing exposed EVAL is exploratory, near-duplicate independence unknown. A local directional readout is constructible but unqualified; failure stops, no dictionary training.

## 8. Claim Boundary And Next Decision

Result NOT RUN. Current approval covers read-only assets/design only. The user's later “继续执行本协议” is required before bounded discovery/qualification/intervention on existing resources. No new training, allocation, router or broader search. Decide only whether the selected dependence has qualified support warranting a future shared-path test; expert benefit, independent modules, training order and full C→R→prediction mediation remain unestablished.
