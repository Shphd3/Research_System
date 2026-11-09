# A13_00_03_E01 Summary

## Direct Result

**Formal verdict: insufficient.** All six objective/path capability cells
passed, and the registered learning-curve effects were large and positive in
all eight paired seeds:

\[
\bar U_{\mathrm{relay}}=0.7127\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.4559,1.0492],
\]

\[
\bar\Delta_{\mathrm{relay}}=0.6333\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.3943,0.9443].
\]

However, the registered relay causal-use guard failed, so these effects remain
candidate evidence rather than a passed claim.

![Standard-head learning curves](figures/objective_learning_curves.png)

![Paired relay effects](figures/relay_interaction.png)

## Why the Guard Failed

The capability rule allowed one of eight seeds to be below 0.90 accuracy. NTP
seed 1401 was that permitted failure: intact accuracy was 0.7692 and donor
follow was 0.0769. The other seven NTP seeds each had donor follow 1.0.

The causal-use rule nevertheless averaged all eight seeds, producing
\((7+0.0769)/8=0.8846<0.90\). Thus the protocol asked an explicitly ineligible
model to demonstrate a learned causal interface.

Matched shared-aux and informative Next-2 each had donor follow 1.0 in all
eight seeds. The formal E01 verdict is not changed post hoc.

## Recognition Update

E01 exposes a gate-composition bug, not an identified mechanism failure. It
also supplies a strong preregistered pattern worth independent confirmation:
Next-2 improved the ordinary head in both paths, but its benefit was much
larger when the answer was structurally forced through the early relay.

## Next Decision

Run an independent eight-seed confirmation with the same task, objectives,
horizon, and numerical thresholds, but judge relay intervention only among
models that pass the already registered per-seed capability threshold.
