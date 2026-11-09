# A06_03_04_E02 Utility-Certified Audition Stop Protocol

Approval status: approved under the active long-run research instruction.

Purpose: test whether expert utility already observed during continuous pair
audition can certify a safe switch to selected-only top-1 without feature labels.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`.

## Fixed Setup

- Reconstruct A06_03_04_E01 learned specialists with useful expert at rank 4.
- Freeze representation and experts; router-only SGD `0.001`; full LM loss.
- Total horizon: 800 updates. Pair audition is allowed through step 600; after a
  branch stops, all remaining updates use weighted top-1.
- 32 seeds and four tasks; identical initial tensors across stopping branches.

## Utility Certificate

An audition already executes incumbent \(e\) and challenger \(c\). Reuse these
outputs to compute forced path losses at every next-token position:

\[
U_{e,c}=\operatorname{EMA}
\left[\ell(E_c(h)) - \ell(E_e(h))\right].
\]

Positive \(U_{e,c}\) means the incumbent is functionally better on its current
routed population. The deployable `utility_all` rule stops only when:

1. every directed incumbent/challenger pair has an observed finite EMA;
2. \(\min_{e\ne c}U_{e,c}>0\) for nine consecutive updates;
3. all-position route assignments change on at most 1% of tokens for the same
   nine-update window.

EMA decay is `0.9`. The certificate reads targets and losses already available
during LM training, but no feature label, task mask, or useful-expert identity.

## Conditions

- `fixed600`: continuous audition for 600 updates, then top-1.
- `oracle_route`: stop after true useful-route accuracy is at least `0.95` for
  five consecutive updates; non-deployable compute lower bound.
- `score_only`: stop when every routed incumbent has mean top1-minus-runner-up
  score gap above `1.0` and assignment stability passes for nine updates.
- `utility_all`: proposed all-position utility certificate.
- `utility_task_oracle`: same utility rule using only task-dependent positions;
  non-deployable positive control for semantic-credit contamination.
- `generalist_utility_all`: false-certificate guard with interchangeable experts.

If a rule does not trigger by step 600, it is censored at 600 and switches to
top-1, matching the fixed branch's maximum audition compute.

## Metrics And Decision

Primary method criteria for `utility_all`:

- final sustained correction at least `0.90`;
- final retention among corrected cells at least `0.90`;
- premature-stop rate at most `0.05`, where stop occurs before oracle sustained
  correction;
- median audition saving at least `0.30` relative to 600;
- generalist certificate-trigger rate below `0.10`.

Hypotheses:

- **H1 utility-certified stop succeeds:** all primary criteria pass.
- **H2 score confidence is sufficient:** score-only correction/false-stop are
  within five percentage points of utility-all and median audition count within
  10% of utility-all.
- **H3 semantic-position credit is required:** utility-all fails, while
  utility-task-oracle passes the H1 criteria.
- **H4 certificate is not identifiable:** both utility rules fail or generalist
  false-certificate rate is at least 10%.

## Validity Guards

- A06_03_04_E01 specialist/generalist utility, rank, gap, load, finite-value, and
  state-pairing guards pass;
- fixed600 reproduces continuous audition correction and retention within five
  percentage points;
- oracle stop never precedes its own five-step route criterion;
- forced incumbent/challenger utility losses use only already executed pair
  outputs and add no expert forward;
- pair branches activate exactly two experts before stop and one after stop.

## Claim Boundary

Passing can establish a controlled label-free training-time phase switch. It
cannot establish joint-training robustness, pretrained-LLM transfer, scalable
per-token state, MTP re-triggering, or systems throughput.
