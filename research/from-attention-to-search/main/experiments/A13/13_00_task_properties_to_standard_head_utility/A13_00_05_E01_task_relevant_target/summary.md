# A13_00_05_E01 Summary

## Direct Result

**Pass:** with vocabulary, target frequency, position, predictability,
auxiliary head, loss weight, data, and model matched, supervising the necessary
relay with answer variable \(A\) improved the ordinary next-token head more than
supervising it with causally irrelevant value \(B\).

\[
\bar R_{\mathrm{relay}}=0.2315\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.1792,0.2791],
\]

\[
\bar\Delta_R=0.2134\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.1646,0.2585].
\]

Both effects had the expected sign in 8/8 paired seeds. All four
objective/path cells reached final accuracy 1.0, and every relay model followed
a different-label donor state with accuracy 1.0.

![Task-relevance learning curves](figures/objective_learning_curves.png)

![Task-relevance paired effects](figures/relay_interaction.png)

## Plain-Language Reading

When the answer could only receive \(A\) through the relay, answer-aligned
supervision reached 90% held-out accuracy at a median 60 steps, versus 160
steps for equally predictable nuisance-\(B\) supervision. At step 100, mean
accuracy was 0.9928 versus 0.1635.

When the answer could read \(A\) directly, both conditions were already perfect
by step 100; their AULC difference was only 0.0181 nats. Thus the benefit is
not merely general auxiliary regularization.

## What Is Established

In this minimal carrier, earlier supervision has ordinary-head value when all
three conditions hold:

1. its target names a variable needed for the final answer;
2. the target is attached to an earlier state that must transport that
   variable;
3. the ordinary next-token head later consumes that state.

NTP still sees the answer one position later and can learn the task. The result
therefore identifies a finite-budget credit-assignment advantage, not an
information-visibility advantage.

## What Is Not Established

\(B\) is causally irrelevant under the answer rule, but the held-out-combination
split creates observational association between \(A\) and \(B\). The result does
not prove general MTP superiority, long-distance scaling, multi-evidence
composition, code or language transfer, planning value, or MoE routing value.

## Next Decision

Freeze this minimal sufficient condition. Next validate query-conditioned
binding as a separate NTP-only carrier property before asking whether the same
answer-aligned credit advantage survives composition.
