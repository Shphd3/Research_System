# Self-contained research writing

[中文](report_writing_cn.md)

Help the reader understand the question, reasoning, evidence and boundary on the
first reading. Use these rules when writing a report or explaining research;
they do not create another review stage or change scientific authority.

## Language

- Prefer short sentences with an explicit subject and a concrete verb. Separate
  an observation, its interpretation and its consequence when one sentence hides
  their relationship. Use active voice when the actor is known.
- Use one consistent term for each object. Define necessary technical terms and
  symbols where they first matter. Do not vary synonyms for stylistic effect.
- Put the main answer early. Each paragraph develops one point; a link supplies
  evidence rather than substituting for the explanation.
- Keep assumptions, quantifiers, uncertainty and scope. Simpler wording must not
  turn a local observation into a general claim, a hypothesis into a result, or
  a mathematical relation into a causal finding.
- Write natural Chinese and clear English. Do not enforce English word counts
  on Chinese, impose a controlled dictionary on scientific notation, or claim
  ASD-STE100 compliance without a separate compliance check.

## Objects, operations and first-use terms

Before naming a technical term, explain **what object it refers to, how it is
obtained, how it is used, and which question it answers**. A translation or another
abstract noun is not a definition. Put this explanation in the body at first use;
a glossary may help retrieval but cannot carry the argument alone.

Separate construction, selection and learning status. For example, averaging raw
domain gradients constructs a **common update**; selecting one update on fitting
data and using it everywhere is **fixed selection**; keeping all candidate updates
unchanged throughout evaluation defines a **frozen candidate library**. Neither
selection rule is a trained expert. Distinguish a parameter increment, its induced
activation displacement, an expert with learned weights and a shared module whose
weights continue to train. Reconstruct these operations from the owning Protocol
and implementation; do not transfer a step size or interface between experiments.

## Why a comparison is performed

For each experiment, make the following reasoning readable in this order, within
its existing artifact structure:

1. The concrete uncertainty and its relation to the root question.
2. The prior judgment or candidate hypothesis and a credible competing explanation.
3. What changes, what stays fixed and what is compared.
4. What each control rules out, and what it leaves unresolved.
5. Which outcomes would change the judgment, including non-support and insufficiency.
6. The observed outcome, supported claim, remaining boundary and resulting decision
   or explicitly labeled AI suggestion.

“Further analysis” or “validate effectiveness” is not a purpose. A proved identity
does not need an invented empirical rival. Keep Summary's four parts and Anchor's
eight sections; these requirements concern their content, not extra forms.

## Formula meaning and evidence scope

Near each equation, define the objects/symbols, dimensions or units, random variables,
expectation or averaging domain, necessary assumptions and intended use. State whether
the quantity is empirical training loss, heldout loss or population risk; total risk
or excess risk after subtracting irreducible randomness; squared or half-squared
loss; and an exact relation, local approximation or conjecture. Disambiguate symbols
reused by different models with a local correspondence, or rename in maintained
exposition without changing frozen evidence. A variance of group mean gradients is
not an estimator-noise covariance.

Name the random object behind “noise”: conditional variation of the true target
given the observed input, finite-sample error of an estimated mean, or minibatch
gradient fluctuation at a stated model state. “Denoising” requires an operation and
conditions; it does not mean deleting real group differences or correcting labels.

Distinguish model derivations, teaching examples, language-model measurements,
interpretations and unfinished work. One-step selection on a frozen model does not
establish continuing expert training. Winning a usage-matched random control does
not establish a win over a strong fixed baseline. An interval crossing zero does
not prove no effect. A failed implementation or unrun comparison is not an
architecture result. Keep values, uncertainty, versions and evidence identities.
Do not rewrite raw data, logs, receipts or frozen protocols as new history; clarify
their historical scope in the current report. Personal anxiety and assessments of
an advisor do not belong in research reports.

Each substantive section starts with the question it resolves and ends with the
judgment it changes and the uncertainty it leaves. Remove repeated exposition that
does not help understanding. These are meaning requirements, not mandatory repeated
labels or a requirement to lengthen every section.

## Content and depth

For a research-progress report, preserve this reasoning chain:

1. Purpose: which uncertainty matters, and what understanding an answer changes.
2. Observations: what is already seen, under which conditions; distinguish facts
   from the explanation being proposed.
3. Hypothesis: which explanation could account for the observations, its strongest
   rival, and what could distinguish them. Keep the named question's population,
   conditions and time horizon; a transfer limitation is not a new main hypothesis.
4. Model and staged derivation: define the objects, state, assumptions, mappings,
   update and observable needed for the scoped question. Each stage explains its
   input, relation, output and why it follows; connect adjacent stages. Mark exact,
   approximate, assumed and still-untested relations. Numerical models are valid;
   missing links stay visible instead of being invented to make a complete story.
5. Experimental check: map the derived predictions or unresolved assumptions to
   actual comparisons and evidence. An implementation check of an identity is not
   independent empirical support for a mechanism.
6. Stage update: explain what is now understood, which hypothesis/assumption is
   strengthened, weakened or unresolved, and why the remaining question matters.

Use this logic in replies too, at the depth needed for the question. A short
reply gives the answer, decisive reason and boundary; a complex reply retains the
necessary model, derivation and evidence. Do not expand every reply into a report.

The chain is not six compulsory headings or a required new experiment. Reuse
existing derivations; theory uses proof/counterexamples and observations must not
invent a mechanism. Put the meeting's speaking core first and detail/Q&A later.
A long requested report starts with a brief route through its sections.

Use headings suited to the research. Formal arguments, observational studies,
interventions and engineering comparisons need different evidence; none requires
an invented experiment or model to fill a template. The existing eight-section
Anchor and four-part Summary keep their owning contracts. Full reports use the
advisor research-exploration method already integrated in the
[final-report skill](../.agents/skills/research-final-report/SKILL.md): explain
priors, model, computation, checks and what was learned to a reader who knows
basic mathematics and ML but has not seen the conversation.

## Results analysis and scientific conclusion

Results analysis explains measurements, comparisons, uncertainty, validity and
alternative explanations. A scientific conclusion answers the original purpose
and states the resulting change in understanding. Cite the smallest decisive
evidence; do not substitute a metric list or a pass/fail label for that answer.
Detailed analyses remain in Detailed, with only the necessary support in Summary.
If the evidence changes no scientific judgment yet, name the unresolved issue.
Do not create a deeper mechanism or broaden the question to make a conclusion
sound meaningful. Missing researcher judgment stays Unknown; AI interpretations
and next-step suggestions remain labeled proposals.

## Complete Markdown delivery

Use Markdown/text for research delivery. Do not generate or require a webpage,
interactive viewer or video as part of this workflow. Static figures may supplement
the text, but the question, decisive findings, reasoning and boundary must remain
understandable without opening an image, clicking a link or expanding hidden content.

- **Reading order:** give the question, bounded answer and evidence status early.
  Then explain the objects, reasoning/comparison and decisive evidence in dependency
  order. Put optional derivations and audit detail later under descriptive headings.
  A long document may start with a short reading route naming its sections/files;
  short replies need no contents table or fixed section count.
- **Formulas:** name the quantity and purpose before the equation; define symbols,
  types/units and conditions at first use. Explain the operation and implication in
  words, keeping exact relations, approximations and hypotheses distinct. Use the
  existing [math syntax](markdown_math.md); the explanation must still make sense
  when a reader sees literal TeX rather than rendered notation.
- **Numbers and comparisons:** state the compared objects, baseline, metric/unit,
  sample or aggregation basis, decisive value and uncertainty or its absence.
  Use a compact table when it makes comparison easier, and state the takeaway in
  prose. Avoid wide tables when a short list is clearer.
- **Figures:** state what is plotted, the compared conditions, visible result and
  limitation in the text. Keep the source/data link. A schematic illustrates a
  relation; it is not measured evidence. Do not invent a plot to satisfy a format.
- **Evidence and navigation:** put a descriptive source link near each decisive
  claim. Include enough setup and explanation to assess the claim without opening
  it; complete logs, settings and lineage stay with their owner. At a reading entry,
  give the project-relative file path as well as its role so a reader can locate it
  even when links do not open. State missing sources and unknown decisions explicitly.

These are content requirements, not additional mandatory headings. Reuse one
explanation for claims with the same conditions and limits; do not repeat the
whole result at every level. A portable Markdown bundle is a derived reading copy;
edit the owning sources. External distribution retains its requested scope.

## Check the text itself

Read the delivered Markdown sequentially with figures, link targets and rich
rendering unavailable. Can a new reader state the question, why the argument or
comparison answers it, the decisive finding and what remains unresolved? Check
symbol definitions, conditions, evidence links and agreement with the source.
Check whether the body alone lets a mathematically trained new reader identify
the research object, actual steps, rationale, meaningful controls, change in
judgment and unanswered questions. Record which sources could not be accessed.
Without an independent reader, call this self-review. Path and source checks do
not establish scientific correctness or independently measured comprehension.

This adapts the clear-language ideas in
[Karpathy's post](https://x.com/karpathy/status/2105819303471976479), while choosing text-only delivery locally. It does not impose a new report template. The [STE maintenance group's FAQ](https://asd-ste100.org/STE_faq.html)
supports applying short sentences, clear terms and active voice beyond maintenance
documents. The post's informal "80%" is not a compliance level.
