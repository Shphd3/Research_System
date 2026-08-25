# Theory And Proof Explanation Mode

Use this mode for equations, derivations, lemmas, theorem claims, proof audits,
counterexamples, or requested theoretical proof suggestions.

## Explain A Claim Before Its Proof

State in plain language:

1. the mathematical objects and their types;
2. the assumptions and quantifiers;
3. the exact conclusion;
4. why the conclusion matters to the document's research question;
5. the nearest stronger statement that it does not prove.

Then give a short proof roadmap. Expand only the step the reader needs or the
step whose validity is uncertain.

## Explain Each Proof Step

For every material step, state:

```text
starting statement
operation, lemma, or inequality used
why its assumptions hold here
resulting statement
what would break if the assumption failed
```

Give one boundary example or counterexample when it distinguishes a theorem
from a tempting overclaim.

## Proof Status

Classify every central theoretical statement as one of the following. In
Chinese output, use the Chinese status first; include the internal code only
when the exact code helps the reader:

| 中文状态 | Internal code | Meaning |
|---|---|---|
| 恒等式 | `IDENTITY` | Algebraic equality following from definitions. |
| 在所列假设下已证明 | `PROVED_UNDER_STATED_ASSUMPTIONS` | All needed assumptions and proof steps are available. |
| 只证明存在 | `EXISTENCE_ONLY` | Shows that an object exists, not how to construct or learn it. |
| 条件推导 | `CONDITIONAL_DERIVATION` | The conclusion follows only after assuming the key scaling or property. |
| 有缺口的证明思路 | `PROOF_SKETCH_WITH_GAPS` | Main route exists but one or more lemmas or conditions are missing. |
| 经验现象 | `EMPIRICAL_PATTERN` | Observed or fitted behavior, not a theorem. |
| 未知 | `UNKNOWN` | The claim cannot be checked from available material. |

Do not call a proof complete because the final formula looks plausible. Do not
transfer an existence result into algorithmic learnability, token-level
feasibility, optimization convergence, or model capability without a bridge.

## Construct A Candidate Proof

When the user asks for a new proof, place the whole construction under the
Chinese label `AI 建议` and call it `未经验证的候选证明` (internal proof status
`UNVERIFIED_PROOF`). This makes clear that the derivation was not contained in
the source and still needs an independent check. State the target and
assumptions first, derive each step using the proof-step contract above, then
try the closest counterexample and list every remaining gap. Do not relabel the
candidate as a source theorem even when no gap is found.

## Suggest A Proof Route

An `AI 建议` proof route marked `未经验证的候选证明` contains:

```text
target theorem
minimal assumptions
candidate lemma sequence
the hardest unresolved obligation
counterexample class to test
what empirical or architectural claim would still remain unproved
```

If a requested theorem is likely false, give the smallest counterexample or
weaker correct statement before proposing more machinery. Route broad theory
critique or literature positioning beyond the named document to `scholar-mode`.
