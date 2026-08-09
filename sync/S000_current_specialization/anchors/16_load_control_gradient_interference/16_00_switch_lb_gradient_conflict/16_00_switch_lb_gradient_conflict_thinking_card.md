# Thinking Card: Does load balancing slow useful Router learning through gradient conflict?

Source status: `HUMAN_CONFIRMED`; this card records the researcher's approved 2026-08-09 direction and metrics. Exact run settings remain outside this card.

- **Parent research direction:** Separate load control from the A15 spectral-routing line and determine how to prevent expert collapse without slowing language-model learning or expert formation.
- **Phenomenon:** All compared Router arms used the same Switch-style load-balancing coefficient, yet Vanilla collapsed while Centered did not; the frozen DC audit identified an immediate common-component dependency but not the training update that formed it.
- **Mechanism judgment:** A differentiable load-balancing objective may inject a gradient that opposes the language-model gradient on Gate and upstream Router parameters. Raw global-batch gradient cosine is the approved mechanism measurement.
- **Strongest rival:** Local gradient opposition may be beneficial regularization, or the real failure may be that a soft-probability objective cannot change saturated hard top-1 winners. Negative cosine alone therefore does not establish harmful training interference.
- **Evidence that would change the judgment:** From one identical parameter and AdamW state, compare an LM-only shadow step with an LM-plus-LB shadow step. The primary metric is the paired held-out NLL difference; harmful conflict additionally requires improved hard load and negative raw global-batch LM/LB gradient cosine.
- **Most uncertain point:** Does Switch LB pay a measurable held-out learning cost for the load correction it actually achieves during the first 100M tokens?
- **Current blocking uncertainty:** Without this measurement, increasing the LB coefficient, projecting its gradient, or replacing it with a dynamic expert bias cannot be assigned a mechanism.
- **Why this decision is needed now:** The previous line observed collapse and large centering gains, but selecting another Router or running a long comparison before identifying the update conflict would conflate load correction, regularization, representation geometry, and systems effects.
- **Current next decision:** Formalize and approve the paired early-gradient/shadow-update Protocol.
- **Researcher-selected intervention after the audit:** Dynamic expert bias is the first candidate if A16_00 supports harmful gradient interference or hard/soft load-control mismatch. It is not yet a validated solution.
- **Known source material:** A15 matched training, the migrated DC sustainer audit, the verified Switch-style objective, immutable paired initialization/data machinery, and primary literature on auxiliary-loss and loss-free load control.

