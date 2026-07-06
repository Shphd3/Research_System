# Negative Result Policy

Negative results are expected and useful.

Examples:

- Equal mass succeeds but NMI remains low: means feature coherence is not solved.
- Expert weights do not help: means expert alignment assumption fails.
- Margin-aware update fails: means preservation method is insufficient.
- Discrete atoms prevent exact split: means deterministic feature-only uniform dispatch is impossible under that distribution.

Do not hide negative results. Map each negative result to a violated assumption.
