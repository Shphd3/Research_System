# A06_00 Functional Specialization Contract

Status: completed parent anchor.

Thinking Card source: [06_00_functional_specialization_contract_thinking_card.md](06_00_functional_specialization_contract_thinking_card.md)

## 1. Complete Problem

**Decision question:** What minimum evidence is sufficient to call a learned
partition feature-level expert specialization?

### Terminology / Definitions

| Term | Plain meaning | Concrete computation | Cannot prove |
|---|---|---|---|
| Operational condition $z$ | A controlled or registered input group | synthetic task, proxy group, or workload stratum | Natural semantic meaning |
| Route identity | Which expert the Router selects | $r(h)=\arg\max_e w_e^\top h$ | Expert usefulness |
| Counterfactual expert utility | Same state evaluated with alternative experts | forced-expert loss $L_{z,e}^{cf}$ | Learnable routing |
| Functional specialization | Different conditions prefer different expert functions and routing captures value under cost | utility gap, route regret, activated cost | General LLM transfer |

## 2. Physical Priors

1. Expert labels are exchangeable; function is not.
2. Balanced load prevents collapse but does not identify useful computation.
3. Human feature labels may stratify evaluation but may not define the correct
   expert.
4. A useful partition must improve held-out task loss relative to matched
   routing controls at comparable activated cost.

## 3. Falsifiable Hypotheses

**H1: route-purity sufficiency.** High route-label agreement implies useful
specialization. Rejected if matched-NMI conditions have different
forced-expert losses.

**H2: functional contract.** A specialization claim requires a stable useful
expert identity, positive held-out utility gap, and lower route regret than
matched controls.

## 4. Core Mathematical Model

For condition $z$,

$$
a(z)=\arg\min_e L_{z,e}^{cf},
\qquad
G_z=\min_{b\ne a(z)}
\left[L_{z,b}^{cf}-L_{z,a(z)}^{cf}\right].
$$

The learned Router is judged by

$$
R_{route}=L_{learned}-L_{oracle},
$$

and the fraction of available functional value it captures is

$$
\rho_{capture}
=\frac{L_{shared}-L_{learned}}
{L_{shared}-L_{oracle}}.
$$

## 5. Evidence Chain

1. Slot/context experiments show that visible feature information and
   non-collapse do not guarantee useful binding.
2. Hierarchical and interference controls show that route-function value must
   be measured independently of route labels.
3. Correct and load-matched shuffled exposure can both retain route NMI 1.0,
   while only correct exposure creates strong held-out specialist utility.
4. Therefore the terminal Router objective is conditional expert value under
   cost, not a visually clean partition.

### Subanchor Registry

| Subanchor | Local decision | Experiment group |
|---|---|---|
| [`A06_00_01`](subanchors/06_00_01_operational_definition_and_failure_evidence_anchor.md) | Separate observable route failure from functional specialization. | [`A06_00_01_E01`--`E03`](/Projects/from-attention-to-search/main/experiments/A06/06_00_functional_specialization_contract) |
| [`A06_00_02`](subanchors/06_00_02_hierarchy_and_utility_diagnostics_anchor.md) | Require expert utility even when hierarchical route labels are recoverable. | [`A06_00_02_E01`](/Projects/from-attention-to-search/main/experiments/A06/06_00_functional_specialization_contract/A06_00_02_E01_hierarchical_route_utility) |
| [`A06_00_03`](subanchors/06_00_03_real_data_definition_boundary_anchor.md) | Treat real-text partitions as proxies until held-out expert value is established. | Definition guard; no standalone run. |

## 6. Minimal Adjudication Contract

A candidate specialization result must report:

1. route identity and load;
2. held-out forced-expert loss matrix;
3. useful-expert stability across calibration and evaluation splits;
4. learned-route loss, oracle-route loss, and route regret;
5. activated computation and communication cost;
6. a causal expert replacement or removal control.

Failure of items 2--4 blocks a functional specialization claim even when NMI
is perfect.

## 7. Current Verdict

**Supported:** specialization is a functional, held-out, cost-aware relation.
Route NMI, purity, load entropy, and active-expert count are necessary guards
only when relevant to the tested failure.

**Rejected:** balanced load or route-label agreement alone proves expert
specialization.

## 8. Claim Boundary And Next Decision

**Cannot claim:** natural semantic experts, real-workload utility, or a
deployable Router.

**Next decision:** determine whether hidden-state geometry can supply a
route-relevant initial partition without privileged feature labels (`A06_01`).
