# Notes for Codex

Do not treat V2.1 as a direct numerical continuation of V2. V2.1 changes the target.

V2 target:

```text
equal-mass dispatch
```

V2.1 target:

```text
equal mass + feature coherence + preservation
```

Implementation priorities:

1. Correctness before speed.
2. Separate calibration from holdout.
3. Keep labels evaluation-only.
4. Report failure modes explicitly.
5. Never silently force counts in GA-SPR methods.

Important: if an experiment fails, do not hide it. Tie it to the violated assumption.
