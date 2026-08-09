# Thinking Card: Why does the same load-balancing loss fail for Vanilla?

Source status: `HUMAN_CONFIRMED`; this card is a structured transcription of the researcher's explicit judgments in the 2026-08-09 review.

- **Parent research direction:** A16 asks how to keep hard expert load usable without slowing language-model learning or blocking expert differentiation. This card migrated from the A15-discovered phenomenon without changing the researcher's original judgment.
- **Phenomenon:** All six arms optimize the same Switch-style load-balancing loss with coefficient $0.01$, yet Vanilla-Full sends almost every deep-layer token to one expert while Centered-Full and the centered band arms remain much less concentrated.
- **Mechanism guess:** The uncentered Router input contains a token-shared mean component.  Its expert-dependent logit offset can create a large early winner margin; after hard top-1 routing saturates, the soft-probability load loss may remain numerically large while having little leverage to change the winner.
- **Strongest rival:** The mean is only correlated with collapse.  Learned Gate rows, upstream representation drift, or Router--expert feedback already encode the imbalance, so subtracting the true mean from a frozen Vanilla Router will not restore expert use.
- **Most uncertain point:** Is the common mean term necessary and sufficient for the observed frozen Router imbalance, or does centering help only through the earlier training trajectory?
- **Evidence that would change the judgment:** On fixed tokens and frozen parameters, subtracting the independently estimated mean must rescue Vanilla more than matched random or wrong-layer shifts; adding the checkpoint center back to Centered must recreate concentration.  Failure of either direction narrows or rejects the mechanism.
- **Current blocking uncertainty:** We do not yet know why the same load-loss coefficient produces very different hard expert use across arms.
- **Why this decision is needed now:** The 30B extension is being interpreted through load, loss, and routing dynamics.  Without this audit, changing the LB coefficient or Router form would be an ungrounded repair.
- **Current next decision:** The bidirectional frozen counterfactual is complete with a `necessary_only` verdict. Parent Anchor A16_00 now measures complete-global-batch LM/LB gradients and held-out shadow-step NLL before deciding whether to enter dynamic expert bias.
- **Known source material:** A15_06 E01/E02 results, the approved E03 continuation, immutable checkpoints, frozen statistics/validation tokens, and the verified Router/LB implementation.
