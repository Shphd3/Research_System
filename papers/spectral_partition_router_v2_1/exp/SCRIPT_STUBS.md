# Script Stubs to Create

Codex should create these scripts:

```text
exp/src/ga_spr.py
exp/src/data.py
exp/src/metrics.py
exp/src/training.py
exp/run_equal_mass.py
exp/run_assumption_ladder.py
exp/run_expert_guided.py
exp/run_margin_update.py
exp/run_controlled_training.py
exp/run_failures.py
exp/make_paper_tables.py
```

Each runner should support:

```bash
python <runner>.py --quick
python <runner>.py --full
python <runner>.py --describe
```
