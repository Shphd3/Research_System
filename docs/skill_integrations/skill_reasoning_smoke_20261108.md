# Short reasoning smoke before publication

[中文与实际回答](skill_reasoning_smoke_20261108_cn.md)

The researcher authorized a short research reasoning test followed by commit
and push. One independent, read-only agent (`/root/skill_reasoning_smoke`, no
inherited conversation) answered three requests using the modified repository
skills. It was not given expected answers or the earlier review examples.
No model weights, training, GPU job or scientific experiment was used.

| Case | Observed behavior | Assessment |
|---|---|---|
| Qualitative batch/routing observations | Conditional explanation, live rival, bounded next comparison; no invented gradient measurements or long-run verdict | PASS on this short request |
| Equal scalar gradient SNR, fixed-learning-rate SGD | Correct moments, both SNRs equal to 1; expected final losses 5/16 and 1/4; requests a reference for batch equivalence | PASS; exact rational arithmetic independently agrees |
| Facts only | Two sentences reproducing only supplied observations | PASS |

The Chinese companion preserves the requests, actual answers and the exact
arithmetic check. The editing agent assessed the returned answers. This is one
independent answer sample, not a blinded old/new comparison, a full independent
R30–R32 evaluation or evidence of stable cross-domain generalization.

Publication checks: 15 skills/105 local links passed `check_skills.py`; all eight
affected skills passed skill-creator validation; 24 existing local unit tests
passed. Changed-scope links, Markdown math source, whitespace and Git payload
were checked before commit. Earlier review records describe their own earlier
NOT RUN states; this follow-up records the newly authorized bounded test.
