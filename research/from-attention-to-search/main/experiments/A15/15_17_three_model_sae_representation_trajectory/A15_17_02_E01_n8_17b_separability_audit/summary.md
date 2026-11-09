# Summary: A15_17_02_E01 Exact-17B N8 Native Separability Audit

Primary Anchor: [A15_17_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md), Amendment A2  
Detailed record: [detailed.md](detailed.md)  
Document status: `DRAFT_AWAITING_RESEARCHER_JUDGMENT`  
Result status / eligibility: measurement `COMPLETE / ELIGIBLE`; mechanism judgment `AWAITING_RESEARCHER`

## 1. Purpose

Test whether SAE-associated concentration of the native layer-8 attention write
is accompanied by stronger held-out readability of eight N8 academic-source
domains at the same exact-17B training coordinate.

## 2. Hypothesis

The registered primary hypothesis predicts that fresh coefficient-0.1 S7 has
higher native body-mean N8 test accuracy than Dense. The strongest rival is that
SAE history changes concentration, scale, or shared directions without improving
domain distinctions; the reweighted 1→0.1 versus fresh 0.1 contrast tests this
history-associated alternative without treating it as an isolated coefficient
intervention.

## 3. Analysis Method

- Compare exact-17B Dense, fresh S7 0.1, and reweighted S7 1→0.1 on identical
  frozen N8 fit/dev/test records and the same native layer-8 body-mean write.
- Fit an L2 multiclass linear reader on fit, choose `C` on dev, and evaluate
  1,600 test records; use two class-stratified paired 2,000-draw bootstrap
  contrasts and the registered 97.5% directional intervals.
- Report effective dimension, top-16 variance share, between/within scatter,
  and five-seed fit-only K-means ARI as explanatory structure diagnostics;
  they cannot replace the primary accuracy rule.

## 4. Conclusion

Registered measurement verdict:

1. `fresh S7 − Dense = +1.4375` percentage points, but its registered 97.5%
   interval is `[−0.1250,+2.9375]`; therefore the primary direction is
   `INSUFFICIENT`, not a confirmed gain and not equivalence.
2. `reweighted S7 − fresh S7 = −14.9375` points with 97.5% interval
   `[−17.5000,−12.5000]`; therefore the history contrast is
   `REWEIGHTED_LOWER_THAN_FRESH`.
3. The reweighted condition is also the most concentrated
   (`d_eff=7.4958`, Q16 `0.7929`) but has the weakest B/W (`0.1324`) and
   five-seed mean ARI (`0.1220`). This is eligible evidence that concentration
   is not a monotonic proxy for N8 domain separability in this comparison.

| Registered rule | Observed value | Guard / eligibility | Typed verdict | Evidence source |
|---|---|---|---|---|
| Fresh−Dense 97.5% interval wholly above zero | `+1.4375` pp; `[−0.1250,+2.9375]` | eligible; same 1,600 test records | `INSUFFICIENT` | [paired contrasts](tables/paired_contrasts.csv) |
| Reweighted−fresh 97.5% interval excludes zero | `−14.9375` pp; `[−17.5000,−12.5000]` | eligible; same 1,600 test records | `REWEIGHTED_LOWER_THAN_FRESH` | [paired contrasts](tables/paired_contrasts.csv) |

![Exact-17B N8 primary accuracy and registered intervals](figures/n8_17b_separability_primary.png)

How to read: the left panel shows absolute test accuracy; the right panel shows
the two pre-registered paired differences. Crossing zero leaves the fresh
direction unresolved, while the reweighted interval is wholly negative.

### Claim Boundary

Can claim: for these exact checkpoints and N8 panel, fresh S7 is not
directionally established above Dense by the registered rule; the more
concentrated reweighted S7 is substantially less readable than fresh and has
weaker distance-based domain organization.  
Cannot claim: coefficient causality, broad semantic improvement or damage,
actual language-model use, language-model quality, training efficiency, or
generalization across training seeds and tasks.

### Researcher Judgment Required Before Finalization

```text
Question: Does SAE-associated concentration strengthen exact-17B N8 domain separability?
Direct result: fresh-minus-Dense is unresolved; reweighted is markedly below fresh while more concentrated.
Confirmed: AWAITING_RESEARCHER
Weakened or rejected: AWAITING_RESEARCHER
Current mechanism and reason: AI DRAFT — concentration is not a monotonic readability proxy; the reweighted history may emphasize non-domain or shared directions.
Cannot claim: causal coefficient effect, broad semantics, model use, LM quality, training efficiency, or cross-seed generality.
Exactly one next decision: AWAITING_RESEARCHER; AI suggestion is to distinguish reversible scale/conditioning change from loss of domain-discriminative directions.
```

The Summary remains a draft until the researcher confirms or corrects the
judgment fields above.
