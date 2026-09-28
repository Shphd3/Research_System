# When does an effective A update help or harm B in a controlled shared parameter task?

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: shared_update_conditional_interference
focus_role: Unknown
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-27
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: daily_research_reports/0927/docs/shared_update_research_pack/documents/anchor.md
protocol: daily_research_reports/0927/docs/shared_update_research_pack/documents/protocol.md
source_meeting: Unknown
core_experiment_count: 1
```

## 1. Core question and boundary

At one fixed model state, A supplies an ordinary loss decreasing update to a shared parameter matrix. B is evaluated independently after that update. Which controlled relation between A and B makes B's loss fall or rise? The researcher confirmed the fixed S7 internal binary task as this cycle's independent question. Sparse autoencoder (SAE) analysis of every new direction family is required within this experiment.

This cycle tests a local update in an internal constructed task. It does not establish natural domain interference, long term joint training cost, parameter isolation benefit, or prospective SAE prediction.

## 2. Prediction and strongest rival

The proposed mechanism predicts that stronger coupling between the two task signal directions amplifies help when their answer rules agree and harm when they disagree. The strongest rival is that correction of the fixed model's common background error dominates, so all conditions may still help B. A change in the amount of help is distinct from net harm.

The researcher defines a representation common component as the **same SAE atom used by A and B with similar activation**, not atom identity alone. Similarity is measured on separate structure examples before outcome analysis, initially with a loose rule. Even similar common components may remain unchanged after A's update, change without affecting B's loss, or have a harmful local contribution offset by helpful changes elsewhere. The direction overlap intervention is not itself an intervention on SAE commonness.

Changing direction overlap changes both directions within a family. Their marginal distributions are unchanged by the randomized construction, but the experiment does not hold one exact A update fixed while changing only B. Results are conditional on this construction and fixed checkpoint.

## 3. Permitted information and separation

The source update may use only A's labels. Independent structure samples select SAE directions without B loss, gradients, or outcome information. B's labels enter evaluation and later signed diagnosis; they do not select source gradients, task directions, examples, SAE atoms, or step sizes. Development direction families check implementation and measurement. Unseen confirmation families determine the scientific result, with paired conditions kept within each family.

## 4. One core experiment: controlled directions, rules, and mandatory SAE diagnosis

- **Purpose:** Determine whether an effective A update has a reproducible helpful or harmful consequence for B under independently specified task relations, and whether the SAE observes the structure carrying that consequence.
- **Hypothesis:** Greater task direction coupling amplifies the contrast between agreeing and reversed answer rules. A common background correction may instead dominate. Even the same SAE atoms with similar activation may fail to represent the functional path if the loss contrast appears.
- **Analysis method:**

  1. Compare B's actual loss change across the crossed direction and rule conditions after ordinary A updates, while requiring improvement on independent A examples and retaining both update sizes.
  2. On every new direction family, select SAE directions used by both groups with similar activation frequency and strength from separate structure examples before viewing outcomes; measure whether B's update induced native representation change enters those directions, regardless of whether B was helped or harmed. Report an empty set rather than relaxing the rule after seeing outcomes.
  3. Combine B's loss sensitivity with representation changes to attribute signed first order effects to the selected directions and their complement. Check reconstruction of the task signal and a nonlinear remainder before interpreting SAE as a proxy.

- **Prospective conclusion branches:**
  - **Supporting:** Qualified loss readouts show the registered interaction and net help and harm. The result supports this controlled local relationship; SAE evidence is assessed separately and may support or fail the proposed proxy.
  - **Non supporting:** Qualified outcomes do not follow the predicted interaction, or the reversed rule merely reduces help. The strong claim is withdrawn for this carrier. SAE diagnosis is still reported for all new directions.
  - **Insufficient:** Source learning, joint feasibility, baseline comparability, numerical identity, or interval precision fails. Preserve the failed stage and diagnose that gate without selecting a favorable condition.

The exact construction, resource gates, thresholds, and verdict rules belong only to the [Protocol](docs/shared_update_research_pack/documents/protocol.md).

## 5. Rolling round summary

| Date (UTC) | Round question | Result | Knowledge update |
| --- | --- | --- | --- |
| 2026-09-28 | Does controlled direction overlap and rule change the consequence of an effective A update, and does SAE capture the relevant signal? | Registered analysis found modulation of B's benefit without net harm; common SAE activation was observed but its task-signal proxy guard failed. | Factual evidence available; researcher judgment and boundary confirmation pending. |

## 6. Current next decision

After the controlled loss result **and the mandatory SAE analysis on all new direction families**, decide whether SAE has enough evidence as a proxy to justify a separate prospective prediction test on untouched direction families. This is a decision about the next experiment; the present SAE analysis is not contingent on observing net harm.

## 7. Researcher result judgment

- **My knowledge update:** Unknown; the full S7 evidence is recorded in Summary/Detailed, awaiting the researcher's judgment.
- **Still cannot claim:** That SAE predicts harmful updates prospectively or that natural data should use separate parameters.
- **Result dependent next decision:** Pending the researcher's judgment after the result; Section 6 states the current evidence gathering decision.

## Paths

- [Candidate Anchor](docs/shared_update_research_pack/documents/anchor.md)
- [Protocol](docs/shared_update_research_pack/documents/protocol.md)
- [Summary](docs/shared_update_research_pack/summary.md), [Chinese Summary](docs/shared_update_research_pack/summary_cn.md), and [Detailed](docs/shared_update_research_pack/detailed.md): factual result records; human interpretation pending.
