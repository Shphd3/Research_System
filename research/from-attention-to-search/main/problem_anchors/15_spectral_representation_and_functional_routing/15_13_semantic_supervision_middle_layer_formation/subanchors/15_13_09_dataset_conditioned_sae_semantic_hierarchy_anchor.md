# A15_13_09: Does the Replicated SAE Graph Encode the M2D2 Coarse--Fine Taxonomy?

## 1. Problem Definition

E17 established a small activation-containment graph but did not establish semantics. The present decision is whether its 24 DCLM-replicated composite groups and 53 retained nodes correspond to M2D2's known three-parent by three-child taxonomy. The graph is fixed before labels are opened. Task-mixture and M2D2-adapted graphs are secondary data-condition diagnostics; they cannot replace the frozen DCLM graph in the primary verdict.

## 2. Physical Priors

A semantic coarse feature should be selective for one parent domain while remaining broad across that parent's three children. A semantic fine feature should be selective for one child conditional on the same parent. Under the E17 edge orientation, a rarer proposed composite points to more frequent constituents; a semantic coarse-to-fine refinement therefore appears as a constituent with broad child coverage connected from a composite with stronger conditional-child selectivity. Frequency or topical words can imitate either node profile, so fixed activation supports are compared with label permutations that preserve both node coverage and the balanced taxonomy.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts at least one frozen DCLM graph edge whose constituent is parent-selective and child-broad on M2D2 development data, whose composite is more child-selective within the same parent, and whose frozen assignments reproduce above a family-wise 97.5% permutation bound on confirmation data. The strongest rival predicts isolated selectivity without graph-consistent refinement, reversed refinement, or no effect beyond the matched null. A graph constructed directly on unlabeled M2D2 activations is only a target-adapted sensitivity condition.

## 4. Mathematical Model

For M2D2 window \(w\), let \(A_f(w)=1\) when feature \(f\) has a positive SAE activation at least once in target positions 64--255. On development data, feature \(f\) is assigned parent

\[
\hat c_f=\arg\max_c P(Y_c=c\mid A_f=1)
\]

and child \(\hat j_f\) by the analogous maximization conditional on \(Y_c=\hat c_f\). Because both decisions have three balanced choices, normalized parent and child purity are

\[
S_c(f)=\frac{P(Y_c=\hat c_f\mid A_f=1)-1/3}{2/3},\qquad
S_f(f)=\frac{P(Y_f=\hat j_f\mid Y_c=\hat c_f,A_f=1)-1/3}{2/3}.
\]

Let \(B_f=1-\tfrac12\sum_j|P(Y_f=j\mid Y_c=\hat c_f,A_f=1)-1/3|\) measure breadth over the three children. A coarse-role score is \(R_c(f)=\max(0,S_c(f))B_f\) and a fine-role score is \(R_f(f)=\max(0,S_c(f))\max(0,S_f(f))\). For stored edge \(q\to u\), where \(q\) is the proposed composite and \(u\) the constituent, the semantic refinement score is

\[
R(q,u)=\min\{R_c(u),R_f(q)\}
\]

only when both nodes select the same parent, \(S_f(q)>S_f(u)\), and \(B_u>B_q\); otherwise it is zero. Labels are assigned on development data and frozen before confirmation.

## 5. Computational Realization

The base model, layer-27 MLP input, 30,000-feature ReLU Top-32 SAE, E17 checkpoint, and containment thresholds are unchanged. The exact senior SFT-mixture parquet is searched for but is not substituted silently. The available balanced eight-task answer-only mixture is explicitly named a proxy. DCLM E17 tables are reused; the proxy and M2D2 each receive disjoint unlabeled discovery and relation-replication samples. M2D2 development labels assign semantic roles, and its untouched confirmation labels evaluate the frozen assignments. Joint-label permutations preserve the exact 3-by-3 counts and each node's activation support.

## 6. Minimal Falsification Tests

The primary pass requires at least one DCLM-derived replicated edge to qualify on development and independently retain its parent identity, child identity, refinement direction, minimum support, and score above the confirmation family-wise 97.5% permutation bound. Significant nodes without a qualifying edge yield semantic selectivity without hierarchy. No significant nodes or edges yield no detected alignment. Missing exact identities do not invalidate M2D2, but the exact senior-data comparison remains insufficient. Cache mismatch, support below 30 active windows per node, label leakage, invalid split separation, or incomplete artifacts yields insufficient evidence.

## 7. Current Evidence

E16 trained the technically qualified SAE only on DCLM. E17 found 1,212 discovery groups but only 24 groups, 91 edges, and 53 nodes survived disjoint DCLM replication, with maximum activation depth two. E18 evaluated those frozen relations on the exactly balanced M2D2 taxonomy. Two edges pass the registered development and independent-confirmation family-wise bounds, so the typed verdict is `COARSE_FINE_GRAPH_CONFIRMED`. Both lie under `Culture and arts`, covering only `Mass media` and `Performing arts`: one of three parents and two of nine children. The broad endpoints have confirmation coarse normalized purities 0.02096 and 0.03853, below the node family-wise bound 0.20420. Four of 24 DCLM groups retain the unchanged activation-relation gates on M2D2, but neither semantically confirmed edge belongs to those four. The same SAE yields 24, 60, and 37 replicated groups on DCLM, the local task proxy, and M2D2 respectively, so graph form is strongly analysis-data-conditioned.

The researcher-approved post-hoc senior-alignment audit adds a graph-level trend result without changing the registered verdict. Among nodes with at least 30 active windows in both semantic splits, DCLM has 27/5/0 eligible nodes at depths zero/one/two. Its depth correlation is positive for coarse purity (\(\rho=0.484\), permutation \(p=0.0220\)) but not significant at 0.05 for parent-conditioned fine purity (\(\rho=0.359\), \(p=0.0649\)). The task-proxy and M2D2 graphs have positive correlations for both purities, but their coarse-role correlations are also positive rather than showing shallower coarse dominance. DCLM's 11 eligible edges have 9 positive fine-purity differences and 11 positive breadth differences, yet neither fraction separates from the dependency-preserving label null and neither median separates from support-exact endpoint re-pairing. The senior-alignment conclusion is therefore `PARTIAL_ALIGNMENT_NO_ROLE_TRANSITION`. The exact senior SFT parquet remains absent and is recorded as `NOT_RUN_MISSING_DATA`.

## 8. Claim Boundary And Next Decision

E18 establishes only two pairwise relative wide-to-narrow correspondences in one M2D2 parent. Its post-hoc trend evidence supports data-conditioned label specificity but rejects the stronger interpretation that shallow graph nodes preferentially carry coarse roles and deeper graph nodes replace them with fine roles. It does not establish a complete three-by-three teacher, a transported DCLM hierarchy, causal feature composition, a universal semantic hierarchy, Transformer-layer onset, online Router recovery, expert utility, or task gain. The frozen DCLM graph is therefore not approved as a unified coarse/fine teacher. The sole next decision is whether to obtain the exact senior SFT mixture and reconstruct the hierarchy under that task-conditioned corpus before any SAE-teacher layerwise recovery audit is authorized.
