# Data and statistics audit

Registered at 2026-10-24T15:57:22.723159+00:00 before formal testing.

Protocol §§5/9/10 fixes canonical split units, unique-versus-rendered counts, exact 144-example marginals, all three seeds, fixed endpoints and paired family-level uncertainty. Actual data manifest/access hashes must bind before full execution. The finite p,q support explicitly prevents pretending 2048 unique training cases exist per family.

## Pre-run distribution limitations supplied by the coordinator

The CPU data audit reports that BOTH's 512 rendered test records contain only 32 independent numerical pairs. The never-add-shipping shortcut scores 93.945% there, with only 31 below-threshold records. S2b's always-free-shipping shortcut scores 481/512=93.945% on test and 234/256=91.4% on validation. These are generator/distribution facts observed before model qualification, not evidence that any model learned or failed. Retain the original task and thresholds; explicitly report rule-switching cases, enriched boundary pressure sets and canonical-(p,q)-clustered intervals. Do not describe 512 template records as 512 independent numerical cases. Actual manifest and baseline output paths will be bound in the runtime/data provenance receipt.
