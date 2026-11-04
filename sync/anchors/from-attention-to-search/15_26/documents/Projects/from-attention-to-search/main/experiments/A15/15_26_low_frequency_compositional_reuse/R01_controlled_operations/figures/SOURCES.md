派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/figures/SOURCES.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/figures/SOURCES.md)；研究修改仍回到原件。

---

# R01 figure sources and reading rules

Producer: execution `source/aggregate.py::figures`, Matplotlib Agg,160dpi; exact originals in `analysis/aggregate/`. Curated hashes/bytes are in the project `main/curated_evidence.json`.

`learning_help.png`: Anchor asks learning help, Protocol compares relevant P, Base B, alternate C under matched composition supervision. Left: answer-target count versus VAL accuracy (%), one line per parent seed; no across-seed smoothing or uncertainty band. Right: fixed-final TEST accuracy (%), all3 seeds,96 rows each. Sources `learning_curves.csv` and `help.csv`. Registered helpfulness predicts≥5pp P advantages over both controls with consistent signs. Observed held-out scores remain low, while atomic-format qualification fails. Permitted conclusion: these measured preparations did not yield qualified composition. No internal mechanism, independent task-world replication or equivalence is shown.

`freezing_and_transfer.png`: left compares balanced primary U/F/J TEST accuracy by seed; source `all_runs.csv`. Right shows every revision's affected new-answer edit−sham difference (pp),F/G roles with distinct markers; source `revisions.csv`. Each revision has24 affected TEST rows; all9 cases/role shown. Marker index is case order, not training time. No error bars in the plot; conditional intervals remain in tables. Registered success additionally requires atomic, native and preservation guards, all baseline-ineligible here. Local gains cannot certify reuse, and small F/J gaps cannot establish2pp equivalence. The current evidence invites a separately labeled prerequisite/interface conjecture, without promoting the current Anchor's scientific state.
