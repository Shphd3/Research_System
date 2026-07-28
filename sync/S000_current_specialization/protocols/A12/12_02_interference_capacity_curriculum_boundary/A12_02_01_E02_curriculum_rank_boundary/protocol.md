# Protocol: A12_02_01_E02 Curriculum Rank Boundary

Approved under the planned-anchor instruction. Reuse A12_04 data/model/optimizer/seeds. Compare static auxiliary weight 2 with a dose-matched schedule: weight 0 for steps 0--249 and 8/3 for steps 250--999. Primary decision is rank-1 Pareto improvement: standard loss decreases by more than 0.1 in 5/5 while auxiliary MSE increases by at most 0.02. Rank 2 is a sufficient-capacity guard. Cannot claim language-model curriculum behavior.
