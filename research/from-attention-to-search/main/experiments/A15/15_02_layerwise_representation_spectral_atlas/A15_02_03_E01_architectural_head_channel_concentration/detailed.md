# A15_02_03_E01 Detailed Evidence Ledger

## 1. Question And Registered Clauses

**Question.** In frozen Qwen3-8B, is coarse/fine semantic discriminability more concentrated in architectural attention heads before `o_proj` than in fixed contiguous groups of the actual MLP input, and does either partition exceed a matched random 32×128 channel partition?

The Protocol adjudicates four clauses independently:

1. **H1 attention concentration:** typical or maximum true-head concentration exceeds the attention-site random-partition null.
2. **H2 MLP-group concentration:** typical or maximum fixed contiguous-group concentration exceeds the MLP-site random-partition null.
3. **H3 cross-site difference:** after calibrating each site against its own random null, attention concentration exceeds MLP concentration.
4. **H4 within-unit spectral specificity:** a concentration-qualified unit contains a real 16-d covariance band that exceeds matched random 16-d orientations.

Typed closure: H1 sparse maximum Pass; H1 typical Fail; H2 Fail; H3 maximum Pass and typical Fail; H4 Fail.

## 2. Frozen Model And Exact Hook Sites

| Item | Frozen value |
| --- | --- |
| Model | `/data/share/Qwen3-8B` |
| Revision | local filesystem snapshot |
| Manifest hash | `3e33117aebc01710cf1011093bbf4c2700336fce4600788f15d80d69f165dc25` |
| Config hash | `deaa300e5384a480c2cafd0db33cba0da89db8eeeb8ddc2b584b89bd46d52ffb` |
| Architecture | 36 blocks; hidden 4096; 32 query heads; head dim 128 |
| Forward | frozen bfloat16; no model update |
| Attention object | direct input to every `self_attn.o_proj`, reshaped `[batch,seq,32,128]` |
| MLP object | post-attention RMSNorm output directly entering every block MLP |
| Readout | common final `Classification:` colon token |

The attention object is the actual architectural query-head boundary. The MLP object is not an attention-head tensor: G1--G32 are only fixed contiguous coordinate slices of its native 4096-d order.

## 3. Data And Provenance

The semantic data are reused exactly from A15_02_E01:

- 8 academic parent classes;
- 8 child concepts per parent;
- 4 templates and 2 disjoint fact bundles per child;
- 512 English descriptions with no answer label in the text;
- design templates 1--2 and sealed confirmation templates 3--4;
- common final-colon readout at absolute token position 57 after left padding;
- canonical semantic-record hash `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`;
- byte hash of the complete text ledger `60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1`.

The exact texts, token ids, labels, fact bundles, and split identities are in [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json).

Natural-background covariance is also reused exactly:

- 128 independent DCLM documents;
- 512 fixed Qwen tokens per document;
- 65,536 effective tokens;
- two fixed calibration halves of 32,768 tokens;
- canonical token-sequence hash `5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`;
- cached tensor byte hash `2d1aee93af592df45bdfbed668e755052c1fbe8544b05fc31211ae4eb31a62a1`;
- zero exact semantic-test-sentence leakage.

The document ledger is [calibration_manifest.json](provenance/calibration_manifest.json). Labels were used only after frozen extraction to compute statistics and never entered the Qwen prompt.

## 4. Metrics And Physical Interpretation

For granularity \(g\in\{coarse,fine\}\) and a 128-d unit \(u\):

\[
D_u^g=\frac{\operatorname{tr}(B_u^g)}{\operatorname{tr}(W_u^g)+\epsilon},
\qquad
C_u^g=\log\frac{D_u^g}{D_{full}^g}.
\]

\(B\) measures dispersion of semantic class centers; \(W\) measures template/fact dispersion within the same semantic class. \(D\) is therefore class separation per unit within-class nuisance, not probe accuracy, model loss, or causal use. \(C>0\) means a unit has higher discriminability than the complete state at the same site.

Fine-relative concentration is

\[
C_u^{rel}=\log\frac{D_u^{fine}/D_u^{coarse}}
{D_{full}^{fine}/D_{full}^{coarse}}.
\]

It asks whether a unit is unusually biased toward fine rather than coarse discrimination. It does not mean the unit has high absolute fine discriminability unless \(D^{fine}\) is also inspected.

Raw semantic energy is \(v_u^g=\operatorname{tr}(B_u^g)/128\). Its share is \(s_u^g=\operatorname{tr}(B_u^g)/\operatorname{tr}(B_{full}^g)\). These retain activation scale and answer where actual between-class variance is allocated; they do not remove within-class noise.

## 5. Selection And Null Controls

The maximum unit is not self-validating because \(D_{full}\) is a within-variance-weighted average of unit \(D\), and 36×32 cells create a large selection surface. The registered controls are:

- 1,024 random permutations of 4096 channels into 32 groups of 128;
- a global maximum over all registered layers and groups for every random draw;
- separate median and maximum verdicts;
- 2,000 nested bootstrap draws over the semantic hierarchy with the same resample indices at both sites;
- design templates for candidate selection and confirmation templates for verdicts;
- 5,000 label permutations for selected-unit semantic validity;
- 256 matched random eight-subspace orientation draws inside a unit;
- eigenvalue floors \(10^{-4},10^{-6},10^{-8}\) relative to the largest eigenvalue.

## 6. Smoke And Numerical Guards

| Guard | Attention | MLP | Status |
| --- | ---: | ---: | --- |
| Smoke shape | `[16,36,32,128]` | `[16,36,32,128]` | exact |
| Unit concatenation error | 0 | 0 | pass |
| Two-forward replay error | 0 | 0 | pass |
| Site identity relative error | \(2.20\times10^{-7}\) smoke; \(2.07\times10^{-7}\) full | 0 | pass |
| Max basis orthogonality error | \(2.08\times10^{-15}\) | \(2.01\times10^{-15}\) | pass |
| Calibration half counts | 32,768 / 32,768 | 32,768 / 32,768 | pass |
| Capability gate | pass | pass | pass |

The attention identity guard reconstructs the native `o_proj` input from its 32 reshaped heads and checks separately projected slices against the native output. The MLP identity guard compares the pre-hook tensor to the post-attention RMSNorm output.

## 7. H1 And H2: Fixed Units Versus Random Partitions

### 7.1 Attention heads

| Metric | Fixed maximum | Random maximum q95 | Bootstrap maximum lower bound | Sparse verdict | Fixed median | Random median q95 | Typical verdict |
| --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| Coarse | 3.2214 | 1.2155 | 2.8391 | Pass | -0.0221 | -0.0110 | Fail |
| Fine | 1.0454 | 0.5893 | 0.7527 | Pass | -0.0673 | -0.0006 | Fail |
| Fine relative | 2.5441 | 1.4082 | 1.8149 | Pass | -0.0261 | 0.0212 | Fail |

The pass is selection-corrected and stable, but sparse. It must not be summarized as “an average head is more discriminative than the complete attention state.”

![Attention unit advantage](figures/figure2a_attention_unit_advantage_heatmaps.png)

### 7.2 Fixed MLP-input groups

| Metric | Fixed maximum | Random maximum q95 | Bootstrap maximum lower bound | Sparse verdict | Fixed median | Random median q95 | Typical verdict |
| --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| Coarse | 0.8774 | 0.9645 | 0.6766 | Fail | -0.0031 | -0.0007 | Fail |
| Fine | 0.6236 | 0.7315 | 0.4070 | Fail | -0.0125 | -0.0060 | Fail |
| Fine relative | 0.9454 | 1.1057 | 0.7308 | Fail | -0.0070 | 0.0021 | Fail |

The MLP groups contain real semantic signal: the selected G21 late coarse and fine \(D\) values exceed label-permutation global q95. The failure means only that native contiguous grouping is not more special than random grouping.

![MLP unit advantage](figures/figure2b_mlp_unit_advantage_heatmaps.png)

## 8. H3: Cross-Site Comparison

Each site is first calibrated against its own random-partition q95. Positive paired attention-minus-MLP difference means greater attention concentration beyond its site-specific null.

| Metric | Statistic | Attention-minus-MLP | 95% paired interval | Winner |
| --- | --- | ---: | ---: | --- |
| Coarse | maximum | 2.0930 | [1.6485, 2.4371] | attention |
| Fine | maximum | 0.5640 | [0.2787, 0.8933] | attention |
| Fine relative | maximum | 1.2962 | [0.1867, 1.5740] | attention |
| Coarse | median | -0.0086 | [-0.0386, 0.0129] | indistinguishable |
| Fine | median | -0.0602 | [-0.0664, -0.0274] | MLP higher |
| Fine relative | median | -0.0382 | [-0.0481, 0.0151] | indistinguishable |

The MLP median result does not constitute positive concentration: both MLP fixed medians fail their own null. It only states that typical attention heads are more heterogeneous and often worse than the complete state, while typical MLP groups remain closer to the full-state average.

![Cross-site null-calibrated concentration](figures/figure6_cross_site_null_calibrated_concentration.png)

## 9. Raw Semantic-Energy Allocation

Across blocks 1--35:

| Site | Coarse/Fine median Gini | Coarse/Fine median effective units | Coarse/Fine median max share |
| --- | ---: | ---: | ---: |
| Attention | 0.6044 / 0.6115 | 12.51 / 12.26 | 0.171 / 0.169 |
| MLP | 0.0735 / 0.0666 | 31.38 / 31.46 | 0.0418 / 0.0440 |

The largest observed attention-head energy share is block 31 H18: 0.6315 coarse and 0.7900 fine. The largest MLP shares are 0.1225 coarse and 0.2177 fine. This demonstrates uneven pre-`o_proj` allocation but cannot measure causal output contribution because `o_proj` may compensate head scale.

![Attention raw energy](figures/figure1a_attention_raw_variance_heatmaps.png)

![MLP raw energy](figures/figure1b_mlp_raw_variance_heatmaps.png)

## 10. H4: Within-Unit Eight-Band Audit

Each 128-d unit covariance was estimated from independent natural text and split into eight 16-d bands: F1=head, F2--F5=middle, F6--F8=tail. Only concentration-qualified cells can pass H4.

| Attention candidate | Real stable-band maximum | Random eight-subspace max q95 | H4 |
| --- | ---: | ---: | --- |
| Coarse, block 28 H28 | 1.2626 | 1.6877 | Fail |
| Fine, block 33 H31 | 0.5839 | 0.6245 | Fail |
| Fine-relative, block 1 H10 | 1.9005 | 2.0498 | Fail |

The MLP site is concentration-ineligible. Its descriptive band peaks cannot rescue H2 and are not interpreted as fixed spectral coordinates.

![Attention layer-band atlas](figures/figure3a_attention_layer_band_heatmaps.png)

![MLP layer-band atlas](figures/figure3b_mlp_layer_band_heatmaps.png)

An earlier audit using 16 bands ×8 dimensions found one narrow F1 pass at L32H27. The current test uses the researcher-approved 8 bands ×16 dimensions plus an explicit concentration-eligibility gate and metric-specific design selection. The different resolution and selection surface mean the results are not direct replications. Their conservative intersection is that no broad, reusable within-head middle/tail rank identity has been established.

## 11. Label And Numerical Robustness

For the design-selected attention H25, late maximum semantic \(D\) values exceed the 5,000-label-permutation q95:

- coarse: 1.4015 versus 0.0606;
- fine: 1.0650 versus 0.3408.

For the MLP selected G21, the corresponding real semantic signals also exceed label null. Therefore H2 failure is not “no semantic information”; it is “fixed contiguous groups are not special relative to random groups.”

Changing the eigenvalue floor from \(10^{-6}\) to \(10^{-4}\) changes maximum band log scores by at most 0.0130 for attention and 0.0036 for MLP; correlations exceed 0.99999999. Tail numerical amplification is not a decision-changing explanation.

## 12. Execution And Repair Ledger

| Branch | ACP job | Resource | Platform state | Scientific artifact |
| --- | --- | --- | --- | --- |
| Attention | `om-y32ahxua` | one 8×5090 SPOT node | FAILED after one retry | full extraction and statistics complete |
| MLP | `om-vjowli0r` | one 8×5090 SPOT node | FAILED after one retry | full extraction and statistics complete |

Both jobs exited after statistical outputs were already available because a plotting function used a NumPy `.median` bound method instead of `np.median(..., axis=1)`. The correction was analysis-only. `full_analysis_repaired` was generated on a local H100 from the exact extracted tensors; model inference, data, units, partitions, seeds, bootstrap, orientation nulls, and thresholds were unchanged.

The remote CLI could not be re-queried during final documentation because the installed client rejected a newly added workspace API field. This does not alter the preserved job ids, cached outputs, or prior observed terminal states.

## 13. Visualization Audit

All thirteen curated figures were opened and inspected. Presentation-only checks confirmed:

- block axes use 1--36 rather than 0--35;
- attention columns are H1--H32 and MLP columns are G1--G32;
- raw-variance panels state activation²/direction;
- energy-share panels state the log ratio to uniform \(1/32\);
- \(C\) panels use zero as the complete-state reference;
- F1--F8 and their head/middle/tail grouping are visible;
- Figure 6 states that positive cross-site values favor attention after null calibration;
- no descriptive band cell is marked as a spectral Pass.

## 14. Claim Ledger

| Claim | Verdict | Boundary |
| --- | --- | --- |
| Sparse true attention heads concentrate coarse semantics beyond random partition | Pass | one model and taxonomy |
| Sparse true attention heads concentrate fine semantics beyond random partition | Pass | one model and taxonomy |
| Most attention heads outperform the full state | Fail | median clause |
| Fixed contiguous MLP-input groups are special | Fail | random partition falsifier |
| MLP groups contain no semantic information | Not supported | label-null signals exist |
| A fixed F1--F8 band is specific inside qualified heads | Fail | random-orientation falsifier |
| Attention heads causally compute the semantics | Not tested | frozen association |
| Candidate heads improve Router/expert training | Not tested | no intervention |

## 15. Artifact Map

- Protocols: [protocol.md](protocol.md), [protocol_cn.md](protocol_cn.md)
- Reading path: [summary.md](summary.md), [summary_cn.md](summary_cn.md)
- Exact semantic texts: [provenance/actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json)
- Natural calibration ledger: [provenance/calibration_manifest.json](provenance/calibration_manifest.json)
- Model identity: [provenance/model_manifest.json](provenance/model_manifest.json)
- Full extraction manifests: [attention](provenance/extraction_manifests/attention), [MLP](provenance/extraction_manifests/mlp)
- Site verdicts: [attention](provenance/attention_verdict.json), [MLP](provenance/mlp_verdict.json), [cross-site](provenance/posthoc_verdict.json)
- Full statistics: [tables](tables)
- Curated plots: [figures](figures)
- Worker code and raw outputs: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_06_e01_qwen3_mlp_group_vs_attention_head_semantic_concentration/`

## 16. One Next Decision

Approve or reject an independent-taxonomy replication of the selection-corrected attention-head maximum, with layer/head-identity stability as the additional criterion. Candidate coordinates should enter expert-counterfactual or Router-training experiments only if the sparse concentration and identity stability replicate without changing the null or selection surface.
