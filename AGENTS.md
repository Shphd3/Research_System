# Research System — core rules

Layout: `research/<project>/` = research history (explore logs, Anchors,
Protocols, results, map); `Projects/<project>/` = code + question summary;
`/data/250010109/MoE_Router/` = raw outputs and checkpoints; `daily_research_reports/`
= meetings.

Goal (Nov–Dec 2026): understand the MoE representation space, find root causes,
and design better routing / architecture from them. Use Chinese with the researcher.

## 以终为始，积累 know-how
先说最终想改善什么、怎样算改善，再倒推眼前的实验能检验哪条假设。导师指定的测量要回答原问题，也要说明它改变了推导中的哪一步。用得到的认识指导选择：在什么条件下值得采取哪种做法，为什么，什么结果会让我们换做法。
AI 应主动给出自己最看好的机制猜想，指出研究者推理中关键的一跳，用能区分两种做法的预测带着讨论往前走。把精力花在会改变解释、方法选择或结论可信度的细节上。

## Authority
- The researcher owns questions, priorities, mechanism judgment, approval and
  state transitions. AI proposes explanations, rivals, counterexamples and
  distinguishing experiments, and does authorized work. Proposals are `AI 建议`;
  missing judgment stays `Unknown`.
- Preserve frozen measurements and their original interpretation. Date new
  interpretations separately and identify the evidence behind the change.
- Keep four evidence kinds apart: observation (geometry/similarity), readout,
  intervention, training benefit. A local effect is not a training benefit.

## Experiment standard (both lanes)
Every experiment states the uncertainty, the strongest credible rival, the
comparison that separates them, and the next step for each outcome:
support / non-support / insufficient. Write the prediction before running.

## Exploration lane (default)
One working question = one folder `research/<project>/main/explore/MMDD_<slug>/`
with `log.md` (Chinese, append-only); the runnable script or config lives in the
project repo `Projects/<project>/code/` or the execution workspace.
Template: `templates/explore_log_cn.md`. Each entry has:
1. 假设; 2. 先验→模型→计算: the falsifiable prior about the model/data
   structure → the mathematical quantity or objective it implies → the exact
   computation this step runs (may say `沿用上条`; never choose a metric first);
3. 跑前预测 (结果 A → 做什么; 结果 B → 做什么); 4. 结果 with raw numbers or a
   figure path; 5. 研究者决定 (`Unknown` until given);
6. 链条位置: 表征现象 → 机制 → 干预验证 → routing/架构含义 → loss/训练效果,
   or `纯理解` when no routing/architecture decision changes.
End each day's entries with one line `今日认识更新：…`.
No Anchor, Protocol, Summary, `_cn`, sync or hashes are required here. Code,
raw outputs and checkpoints live execution-side; the log links them.
Promote to the formal lane only for meeting conclusions, papers or the long-term
map: load `docs/formal_lane.md` then.

## Question budget
At most 3 active questions per project (listed in `PROJECTS.md`); others are
frozen, keeping identity and evidence. Before opening a new question, ask which
active question it replaces or sits under.

## Iteration
Follow `docs/iteration_protocol_cn.md`. The researcher sets the objective and
resources. AI can originate hypotheses, derive predictions and recommend the
smallest comparison that changes the next decision. After a run, apply the
pre-written prediction and identify any new conjecture it inspires.
One conversation, one question; memory log
`.research/memory/conversations/MMDD-<name>/memory.md` via `research-memory`
(append-only, non-canonical).

## Training and assets (not relaxed, both lanes)
- New training or code reuse: read `docs/training_reuse_index.md` and the
  source; state reuse/adapt/reject. Training follows
  `docs/training_observability_contract.md`.
- Before using checkpoints, representations or datasets: check IDs in
  `assets/` with `python tools/check_assets.py --strict`; register saved
  training outputs and reusable analysis outputs; the explore log cites the asset IDs.

## Execution boundaries
Proceed with reads, in-scope edits, local tests and approved runs. Pause for
missing researcher judgment, scope growth, destructive or external actions, and
unapproved expensive remote runs (remote: `remote-experiment-workflow`,
`docs/execution_envelope.md`). Commit, push, sync and publication only on
explicit request. Keep concurrent write scopes disjoint; never revert others'
changes. Check navigation with `python tools/check_current_entrypoints.py`.
