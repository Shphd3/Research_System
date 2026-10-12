# A17_04: Conditional mapping transfer

## 1. Problem Definition

Does reversing a command-to-position mapping in a new, visibly different mode change the effect of shared learning on the old mode? The root question asks which conditional prediction requirements benefit from sharing updates and which incur a learning cost. Existing FIRST/LAST and update-component experiments show that correct-token cross-entropy can improve while answer competition and error repair differ. They do not manipulate the relation between two conditional mappings.

The researcher adopted one merged task: manipulate consistent versus reversed mappings, then use output comparisons to examine how the effect occurs. These are a task-relation comparison and its diagnostic readers, not two synonymous experiments. Support redirects attention to condition-specific prediction demands; non-support weakens reversal as a sufficient interference trigger in this carrier; insufficiency blocks that judgment. Architecture separation, SAE training and natural-text generalization are outside this question.

## 2. Physical Priors

These are testable modeling premises, not established internal functions. First, shared parameters may support a reusable command-to-position relation, so changing that relation in a new mode may alter old predictions. Second, a visible mode can in principle disambiguate the two rules; opposite mappings therefore need not be contradictory or harmful. Third, increasing probability for plausible answer words can reduce correct-token loss without improving rule-sensitive selection. Equal candidate exposure and relative answer readouts protect that distinction.

## 3. Falsifiable Hypotheses

Candidate H: compared with a consistent new mapping, a reversed new mapping reduces old correct-versus-opposite answer advantage after matched new-task exposure. The stronger claim that old learning is harmed requires an absolute decline from the common old endpoint, not merely a smaller improvement than the consistent branch.

The strongest live rival is that differences follow new-task difficulty, initial competence or optimization path rather than a specific failure to retain a common command-position relation. General candidate adaptation is another live rival. Matched inputs/answer marginals, comparable-level readers, equal-norm immediate updates and a joint feasibility control constrain these explanations; none alone removes every rival. Both old commands are trained, so this design cannot support a missing-position-completion interpretation.

## 4. Mathematical Model

The current implemented system is registered Qwen3-0.6B Base with exactly the final-layer q/k/v/o projection weights trainable (6,291,456 parameters); all other parameters, including q/k normalization, remain frozen. R02 begins from E03's actual AdamW main-update1200 adapter, which qualified all four old DEV cells. Both new worlds begin with identical weights and fresh zero-decay AdamW; the Protocol fixes optimization settings. Because Q/K/V change attention, the R01 fixed-projection-input relation does not apply: use the complete native forward \(p_\theta(y\mid x)\), automatic derivatives and actual finite interventions. The model total size is unchanged. Input \(x=(m,c,L)\) contains a visible mode, a neutral command and a three-word list. Mode one maps甲 to FIRST and乙 to LAST. Mode two preserves this mapping in the consistent world and swaps it in the reversed world. Each world remains independently label-consistent.

For an old-mode input, \(y\) is its correct endpoint word and \(o\) the opposite endpoint word. Define its answer advantage, in natural-log units, and the paired branch effect:

\[
M_A(\theta)=\mathbb E_{x\in\mathcal E_A}\left[\log p_\theta(y\mid x)-\log p_\theta(o\mid x)\right],\qquad
E=\Delta M_A^{\mathrm{reversed}}-\Delta M_A^{\mathrm{consistent}}.
\]

Here \(\mathcal E_A\) is the fixed heldout old-mode panel, and each change is relative to the identical old endpoint. Negative \(E\) means reversal gives less old answer advantage than consistency. It does not by itself establish old loss increase or accuracy decline.

Output coordinates examine the two commands on the same list. Let \(s_{m,c}=\log p(L_3\mid x)-\log p(L_1\mid x)\). Define \(a_m=(s_{m,乙}-s_{m,甲})/2\), \(q_m=(s_{m,乙}+s_{m,甲})/2\), \(C=(a_1+a_2)/2\), and \(K=(a_2-a_1)/2\). These exact output coordinates describe command response, endpoint bias and mode-response difference. They are not identifiable parameter modules. The teaching model \(D=a r+d c r\), with signed command \(r\) and a new-mode indicator \(c\), illustrates a reusable relation versus a conditional correction; it is not the implemented neural architecture or a proved mechanism.

## 5. Computational Realization

Construct balanced paired lists with single-token answers, visible modes and neutral commands. The two new-world inputs and every paired minibatch are identical; their labels alone implement the task-relation intervention. Reuse the same underlying training list content across modes intentionally, while keeping old full inputs out of primary new training. Separate unseen permutations of familiar unordered triples from entirely unseen unordered triples; retain the original split identity. R02 loads TRAIN/DEV only; the original TEST was exposed and is not reused as fresh confirmation.

Reuse the qualified E03 old endpoint; train consistent and reversed branches at matched new-answer exposure, input order, four-weight scope and fresh AdamW. Three continuation orders share one trained old endpoint, rather than replicating old acquisition. Measure old/new loss, accuracy, paired advantage and full-vocabulary competition. Split correct-answer CE into probability assigned to the three list words and conditional selection within that set. The latter distinguishes general candidate access from selecting the correct candidate.

Use comparable new-learning levels as a secondary reader, not a replacement primary result. The separately specified same-state, norm-matched optimizer diagnostic constrains immediate update-scale explanations; it does not replace the task-relation comparison. Joint old/new supervision is a feasibility witness if it succeeds; because it receives extra old labels, it is not a primary equal-supervision performance comparison, and failure does not prove insufficient capacity.


A bounded optimizer diagnostic distinguishes the source gradient \(g_t=\nabla L_{\mathrm{source}}(\theta_t)\) from the actually applied displacement \(d_t=\theta_{t+1}-\theta_t\). Plain clipped SGD applies \(-\eta\widetilde g_t\); AdamW with zero decay uses historical moments and coordinate scaling, so its displacement need not be a scalar multiple of the current gradient. For a recipient loss, define the first-order term and finite-change remainder:

\[
\Delta L_{\mathrm{rec}}=L_{\mathrm{rec}}(\theta+d)-L_{\mathrm{rec}}(\theta),\qquad
T_1=\nabla L_{\mathrm{rec}}(\theta)^\top d,\qquad R=\Delta L_{\mathrm{rec}}-T_1.
\]

These are measurement/derivation definitions, not a mechanism discovery. Same-state, same-batch SGD/Adam directions at both native update norms constrain overall step-scale versus directional effects. Separate fresh versus carried Adam moments only where actual history is saved. All matched interventions use the measured FP32 displacement and check rounding. Such local effects cannot explain a1200-step trajectory without a bridge.

AI candidate optimizer hypothesis: actual step scale and coordinate/history-dependent direction jointly contribute to the observed SGD/Adam acquisition difference. A surviving equal-norm difference supports a local directional contribution; disappearance weakens it at that state. Opposite or mixed effects remain state-dependent. This diagnostic does not assert which factor caused the long training outcome.

## 6. Minimal Falsification Tests

The decisive test is the seed-paired reversed-minus-consistent old advantage at the registered equal-exposure endpoint, reported separately by unseen type and with equal panel weight. Record each continuation seed and its dispersion; all share one trained old state. The delegated operational report convention calls an effect descriptively stable only when all three seed effects have the expected sign and their combined mean magnitude is at least 0.01 nat. This convention is not a significance test or researcher mechanism verdict.

Support requires qualified old acquisition, useful new learning and a stable negative primary effect. No stable negative effect weakens H locally; opposite effects are retained. Missing acquisition, ineffective new learning, invalid data or failed freeze/resume/numerical checks are insufficient or ineligible rather than hypothesis refutation. Loss and accuracy can disagree; report both instead of using a secondary metric to rescue H.

## 7. Current Evidence

R01 completed but did not acquire the old mapping, so its transfer result was insufficient. [R01 Summary](../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary.md) preserves that result. E03 then demonstrated a qualified single-layer AdamW route: both unseen DEV panels and both commands reached100%; the tested SGD configuration did not qualify. [E03 Summary](../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary.md) owns the measurements. R02 is NOT_RUN at this amendment; those acquisition results do not establish transfer or optimizer mechanism.

R02 factual completion: nine bounded branches and 34 local optimizer conditions completed; 72 actual saved states were verified and registered. Final old DEV accuracy was 100% under consistent continuation and 0% under reversed continuation, whose new DEV accuracy was 97.75%–100%. Joint old/new supervision achieved 99.25%–100% across the two modes. This establishes a mapping-relation-dependent cost in this diagnostic setting and a conditional-compatibility witness within the same trainable scope, not the utility of separate parameters or a unique optimizer mechanism. [R02 Summary](../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md) owns the complete bounded readings. Original R01 results remain unchanged; mechanism acceptance and question closure remain Unknown.

## 8. Claim Boundary And Next Decision

The researcher explicitly approved final-layer Q/K/V/O plus AdamW consistent/reversed transfer and a smaller optimizer diagnostic after E03. This supersedes the earlier hold for this scope. [R02 Protocol](../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol.md) owns execution; original frozen records remain unchanged. Completion includes primary branches, guards, actual-asset registration and bilingual results even for negative/insufficient findings.

The one next researcher decision is whether qualified mapping-dependent transfer costs justify a sharing-versus-separation comparison. No separate-parameter, expert or SAE experiment is included. TRAIN/DEV are exposed diagnosis, and continuation orders share one old state. Local optimizer effects do not close a training-trajectory mechanism. Scientific mechanism acceptance and question closure remain Unknown.
