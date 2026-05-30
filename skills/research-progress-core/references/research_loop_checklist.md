# Research Loop Checklist

Use this checklist when planning or reviewing a research step.

## Claim

- Is the claim one sentence?
- Is it falsifiable?
- Does it name the assumed prior?
- Does it avoid claiming more than the test can show?

## Operational Definitions

- Are key terms measurable?
- Are ambiguous and missing evidence separated?
- Is success defined before running the test?
- Is failure defined before running the test?
- Is insufficient evidence defined before running the test?
- Is failure allowed to teach something specific?

## Benchmark

- Does the benchmark isolate one question?
- Is ground truth or a trusted reference available for the exact thing being evaluated?
- Can a human inspect the setup?
- Does the setup contain enough variation to expose the prior?
- Are important variations intentionally designed?

## Metrics

- Does each metric answer a specific question?
- Are thresholds and units stated?
- Are top-line metrics supported by examples?
- Are false positives and false negatives shown separately when relevant?
- Are false-positive and false-negative costs stated when asymmetric?
- Does the metric match the downstream decision?

## Evidence Types

- Is single-observation evidence separated from change evidence?
- Is change evidence shown for training trajectories, seed stability, or before/after comparisons?
- Is summary evidence clearly marked as aggregate evidence?
- Is any single-observation proxy justified if used instead of change evidence?

## Known Cases

- Are known good cases selected before interpretation?
- Are known bad cases selected before interpretation?
- Are known confusing cases selected before interpretation?
- Does each known case explain what failure mode it can reveal?

## Stage Contract

- Are input assumptions stated before implementation?
- Is the local objective narrow enough to falsify?
- Is the expected intermediate output defined?
- Is there a pass/fail criterion?
- Is there a debug artifact?
- Are representative success and failure cases saved or named?
- Is the next-stage handoff explicit?

## Failure Decomposition

- Is the broad failure decomposed into local causes?
- Does each candidate cause have a test?
- Are negative answers recorded as evidence?
- Is the verified bottleneck stated?
- Were algorithm changes delayed until the bottleneck was local?

## Interpretation

- What is validated?
- What failed?
- What remains uncertain?
- Did the result falsify the prior, model, operationalization, implementation, or metric?
- What changed in the current-state document?
- What is the next smallest test?
