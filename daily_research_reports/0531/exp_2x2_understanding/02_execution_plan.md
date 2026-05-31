# Execution Plan: 2x2 Top-1 Router Lock-In

Anchor: `anchor.md`
Approved protocol: `01_protocol_for_approval.md`

## Run Goal

Audit whether final route collapse follows early top-1 assignment.

## Data Construction

```text
h_A = e1, target A_next
h_B = e2, target B_next
```

## Model / Algorithm

```text
router: Linear(2,2)
experts: two Linear(2,2)
lm_head: Linear(2,2)
routing: selected top-1 expert output only
router gradient: selected softmax gate
```

## Stage Audit

| stage | local question | input evidence | pass/fail rule | debug artifact | handoff |
|---|---|---|---|---|---|
| initial router | do A/B start split or collapsed? | router logits, delta signs | opposite sign = split | `initial_router.csv` | detailed |
| early lock-in | does collapse exist by step 0/10? | NMI, top1, gate | same expert + rising gate = lock-in | lock-in figure | summary |
| success dynamics | does initial split stay stable? | logit margin, CE gap | stable NMI=1 + negative CE gap | success figure | summary |
| bias diagnostic | does removing bias improve split? | 10 seed comparison | higher split rate = partial support | bias table/figure | summary |

## Metrics And Artifacts

Primary:

```text
top1_A/top1_B trajectory
NMI trajectory
```

Secondary:

```text
selected gate
counterfactual CE selected - unselected
expert usage/update norm
token accuracy sanity check
```

## Result Location

```text
03_summary.md
04_detailed.md
05_report_card_for_advisor.md
figures/
tables/
notes/
```
