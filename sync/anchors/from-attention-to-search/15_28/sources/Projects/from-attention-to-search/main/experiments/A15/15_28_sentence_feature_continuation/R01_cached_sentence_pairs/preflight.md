# R01 preparation: sources, native caches, and old-graph eligibility

This record establishes feasibility for the requested design. It contains no new
H1/H2 estimates. The 2026-10-28 request first asks for an Anchor and Protocol,
then analysis; this delivery completes that first stage without claiming the
later three figures or sentence examples already exist.

## What was checked

The two named conversations were located and their decision-bearing content was
checked against current scientific owners. The [source audit](provenance/conversation_sources.md)
records the limited reading scope. The present question changes the observation
unit from fixed-target response to two positions in one sentence. It therefore
has independent owner A15_28; A15_27 has not been rewritten.

All eight required registered input IDs passed current strict access checks.
The [receipt](provenance/input_access_20261028.json) proves selected file access;
the [asset audit](provenance/asset_sources.md) separately records producer identity,
actual CSR checks and small-file hashes. It does not claim that large checkpoint
files were rehashed or new model forwards were executed.

| Object | Verified fact | Consequence |
|---|---|---|
| Existing math/biology data | 60 documents each; 120 independent canonical URL groups; 192 tokens each | Reuse 23,040 cached positions; sentence qualification will reduce this number |
| Native SAE | E16, block27 MLP input, F30000; positive FP32 Top32; all 120 token CSR caches readable | H1 feasible; no CrossCoder feature-ID reuse |
| Native CrossCoder | A22, F16384, joint 14-layer residual-post shared z with saved normalization/gate | H1 and compatible old-graph H2 feasible; not 14 independent layer observations |
| Activity count | SAE 32 throughout; CC 29–637, mean 295.4366 | Count matching and explicit target L0 are necessary |
| Independent frequency reference | 256 DCLM windows, 65,536 positions, 254 URL groups; zero observed URL/WARC/full-source-hash overlap with study texts | Reuse R05 frequency groups; unknown near-duplicates remain a limitation |
| Sentence boundaries | Not stored | Freeze complete-sentence annotations using text only before pair outcomes |
| Previous exposure | Per domain 30 discovery, 10 development, 20 heldout documents already analyzed in earlier rounds | No new untouched confirmation set |

R05 frequency groups use features with at least 20 DCLM activations, frequency
tertiles with ties kept together, and a separate low-support group. This is a
reused operational definition, not a newly power-justified cutoff. Exact cutpoints
and implementation are in the asset audit; they must not be re-estimated from
the math/biology panel.

## What the old graph actually means

The compatible CrossCoder graph has the full 16,384-coordinate universe. Use
`raw_edges.npz` fields `A -> u`, restricted to `passV=True`, as the proposed
fixed primary edge set: 206,136 edges. Isolated nodes remain in the universe;
not having an admitted edge differs from not being represented in the graph.

At a **single token**, the historical rule requires source and target counts at
least 200, joint count at least 20, P(target|source) at least 0.8,
P(source|target) at most 0.5, and target frequency at least twice source frequency.
DeltaP and lift are saved diagnostics, not acceptance requirements. Therefore a
common target can yield a strong-looking arrow through its base rate.

There are no self-loops or bidirectional edges. Every arrow increases positive
frequency by at least a factor of two, which mathematically precludes cycles.
No cycle was deleted in this audit. The graph has no independently defined
semantic hierarchy. The historical reduced graph's longest-path depth is a graph
statistic, not semantic level. Reduced and raw one-hop coverage are different;
switching between them after outcomes would change H2.

The maximum in-degree is 15,439 and maximum out-degree 91. The Protocol therefore
includes degree-preserving nulls. Null graphs are labeled random baselines and
do not replace the old graph. Same-token conditional probabilities are not
cross-token transfer probabilities.

## Branch-specific block and remaining preparation

The old E17 SAE graph uses BF16 encoding, FP16 output, norm-outlier filtering,
and selected-index counts that need not equal counts of positive values.
Its equality with the R04 native FP32 positive interface is unqualified, and
historical parent/source binding has gaps. **SAE H2 is
`INCOMPATIBLE_INTERFACE_UNQUALIFIED`.** SAE H1 and both eligible CrossCoder
readouts remain available. No replacement graph was built.

Next preparation is text-only sentence segmentation and an outcome-blind
coverage audit under fixed matching rules. This audit must distinguish genuine
lack of same-ID partners from losses caused by the proposed document blocking,
position bins and count calipers. Do not interpret a convenience threshold as
scientific power or silently relax matching after reading outcomes.

## Execution and delivery state

New model forwards: 0. Training: 0. New clustering: 0. New old-graph replacement: 0.
New sentence-pair H1/H2 estimates: NOT RUN. The [machine-readable audit](provenance/asset_preflight.json)
records the observed preparation facts. The complete statistical scripts, output
tables, three figure types, and selected real examples belong to the subsequent
analysis stage; they have not been represented as completed results here.

[One-page reading entry](one_page_cn.md) · [Protocol](protocol.md)
· [Paper methods](literature_methods.md).
