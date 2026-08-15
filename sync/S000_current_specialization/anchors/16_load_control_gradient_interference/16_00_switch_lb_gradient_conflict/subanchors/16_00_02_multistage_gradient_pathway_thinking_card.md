# Thinking Card: Does Centering Reduce Load-Control Gradient Conflict Across Training?

Status: `HUMAN_CONFIRMED`; recorded from the researcher's 2026-08-09 instruction.

- **Parent direction:** explain whether load control slows useful Router and expert learning, before choosing a replacement controller.
- **Phenomenon:** Vanilla-Full and Centered-Full use the same Switch load-balance coefficient but develop very different hard expert usage.
- **Mechanism judgment:** subtracting the running center may reduce conflict between the language-model and load-balance objectives in the Router input path, reduce conflict between document updates inside experts, and lower the immediate held-out cost of the LB update.
- **Strongest rival:** centering may only change token assignment or regularize the model; lower raw-gradient conflict need not improve held-out learning, and expert parameters receive no direct LB gradient.
- **Evidence that changes the judgment:** paired early, middle, and late checkpoint measurements for Vanilla and Centered, with identical seeds and checkpoint states, must jointly measure Router-upstream representation gradients, Gate gradients, expert LM-update conflict, exact AdamW shadow-step NLL, and hard load.
- **Data judgment:** use the labeled Web of Science abstracts available in the local `river-martin` dataset for document-level and domain-level expert-update measurements; preserve an untouched split.
- **Current next decision:** execute the multistage gradient-pathway audit before starting a dynamic-expert-bias long training comparison.
