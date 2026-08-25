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

Classify every central theoretical statement as one of:

| Status | Meaning |
|---|---|
| `IDENTITY` | Algebraic equality following from definitions. |
| `PROVED_UNDER_STATED_ASSUMPTIONS` | All needed assumptions and proof steps are available. |
| `EXISTENCE_ONLY` | Shows that an object exists, not how to construct or learn it. |
| `CONDITIONAL_DERIVATION` | The conclusion follows only after assuming the key scaling or property. |
| `PROOF_SKETCH_WITH_GAPS` | Main route exists but one or more lemmas or conditions are missing. |
| `EMPIRICAL_PATTERN` | Observed or fitted behavior, not a theorem. |
| `UNKNOWN` | The claim cannot be checked from available material. |

Do not call a proof complete because the final formula looks plausible. Do not
transfer an existence result into algorithmic learnability, token-level
feasibility, optimization convergence, or model capability without a bridge.

## Construct A Candidate Proof

When the user asks for a new proof, place the whole construction under the
top-level label `AI_PROPOSAL` and give it the internal proof status
`UNVERIFIED_PROOF`. This makes clear that the derivation was not contained in
the source and still needs an independent check. State the target and
assumptions first, derive each step using the proof-step contract above, then
try the closest counterexample and list every remaining gap. Do not relabel the
candidate as a source theorem even when no gap is found.

## Suggest A Proof Route

An `AI_PROPOSAL` proof route with status `UNVERIFIED_PROOF` contains:

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
