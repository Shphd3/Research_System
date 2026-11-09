# A11_13 Sample Sheet

These ten examples expose the rendered cue and decision suffix. The intervening history is omitted here only for readability; its audited word count and hash are retained.

## availability_morning_evening / state 0

- relation family: `availability`
- cue: My current schedule leaves the early part of the day free while evenings are occupied.
- local decision: Current request: User: Please enroll me in one weekly class. Which time should you select? Candidate A: Select the Wednesday class at ten in the morning. Candidate B: Select the Wednesday class at eight in the evening. Choose the better action. Answer with A or B.
- answer: `A`
- cue-to-answer distance: `302` whitespace tokens
- filler hash: `a388dcf2ad3dcd2f522571a8163182a4ae79750704e8ee7b5dd0c49c63bb70f9`

## availability_morning_evening / state 1

- relation family: `availability`
- cue: My current schedule leaves the later part of the day free while mornings are occupied.
- local decision: Current request: User: Please enroll me in one weekly class. Which time should you select? Candidate A: Select the Wednesday class at ten in the morning. Candidate B: Select the Wednesday class at eight in the evening. Choose the better action. Answer with A or B.
- answer: `B`
- cue-to-answer distance: `302` whitespace tokens
- filler hash: `a388dcf2ad3dcd2f522571a8163182a4ae79750704e8ee7b5dd0c49c63bb70f9`

## goal_cost_speed / state 0

- relation family: `goal`
- cue: I set a strict spending limit, so I am willing to wait whenever that reduces the price.
- local decision: Current request: User: I need to send project samples to the other office. Which plan should you arrange? Candidate A: Use the standard courier for twelve dollars; delivery takes three days. Candidate B: Use the same-day courier for thirty-five dollars; delivery arrives tonight. Choose the better action. Answer with A or B.
- answer: `A`
- cue-to-answer distance: `308` whitespace tokens
- filler hash: `01de0369a1669792f18437a0386b279c68ccda6970f33f8d6568fbb4b8090537`

## goal_cost_speed / state 1

- relation family: `goal`
- cue: I have very little spare time, and I would rather pay an extra fee than wait around.
- local decision: Current request: User: I need to send project samples to the other office. Which plan should you arrange? Candidate A: Use the standard courier for twelve dollars; delivery takes three days. Candidate B: Use the same-day courier for thirty-five dollars; delivery arrives tonight. Choose the better action. Answer with A or B.
- answer: `B`
- cue-to-answer distance: `308` whitespace tokens
- filler hash: `01de0369a1669792f18437a0386b279c68ccda6970f33f8d6568fbb4b8090537`

## preference_quiet_social / state 0

- relation family: `preference`
- cue: Background chatter breaks my concentration, so I am seeking a quiet working environment.
- local decision: Current request: User: I need a place for planning next week. Which option should you book? Candidate A: Book the single-person focus booth. Candidate B: Book a seat beside the working group. Choose the better action. Answer with A or B.
- answer: `A`
- cue-to-answer distance: `297` whitespace tokens
- filler hash: `4940fa2185f6f9f62b243809a9bf52a75fcfd445dfde06f54bfa01c16152a6bc`

## preference_quiet_social / state 1

- relation family: `preference`
- cue: Working alone makes me stall, so I am seeking a collaborative environment.
- local decision: Current request: User: I need a place for planning next week. Which option should you book? Candidate A: Book the single-person focus booth. Candidate B: Book a seat beside the working group. Choose the better action. Answer with A or B.
- answer: `B`
- cue-to-answer distance: `297` whitespace tokens
- filler hash: `4940fa2185f6f9f62b243809a9bf52a75fcfd445dfde06f54bfa01c16152a6bc`

## state_energy / state 0

- relation family: `state`
- cue: I feel worn down at the moment and want my free time to be genuinely restorative.
- local decision: Current request: User: I have a long break on Friday. Which activity should you schedule? Candidate A: Schedule a calm visit to the botanical conservatory. Candidate B: Schedule a fast-paced dance class. Choose the better action. Answer with A or B.
- answer: `A`
- cue-to-answer distance: `297` whitespace tokens
- filler hash: `14b1b0f22bfa11836ffe2fc2fd2f27fe0dafd20aa9ad6e9208a1a43259e04c7d`

## state_energy / state 1

- relation family: `state`
- cue: I feel restless in a good way at the moment and want an active use of my free time.
- local decision: Current request: User: I have a long break on Friday. Which activity should you schedule? Candidate A: Schedule a calm visit to the botanical conservatory. Candidate B: Schedule a fast-paced dance class. Choose the better action. Answer with A or B.
- answer: `B`
- cue-to-answer distance: `297` whitespace tokens
- filler hash: `14b1b0f22bfa11836ffe2fc2fd2f27fe0dafd20aa9ad6e9208a1a43259e04c7d`

## value_privacy_sharing / state 0

- relation family: `value`
- cue: I would rather accept extra steps than place personal material somewhere broadly accessible.
- local decision: Current request: User: I need to publish the project calendar. Which setting should you apply? Candidate A: Keep it invitation-only and approve each viewer. Candidate B: Make it available to the whole team through a common link. Choose the better action. Answer with A or B.
- answer: `A`
- cue-to-answer distance: `302` whitespace tokens
- filler hash: `01bd1837eee176cd3fb0aed4b91b223aff4d57bf8103f95cab43cdb82b2861e2`

## value_privacy_sharing / state 1

- relation family: `value`
- cue: I would rather make access simple for the group than add restrictive sharing steps.
- local decision: Current request: User: I need to publish the project calendar. Which setting should you apply? Candidate A: Keep it invitation-only and approve each viewer. Candidate B: Make it available to the whole team through a common link. Choose the better action. Answer with A or B.
- answer: `B`
- cue-to-answer distance: `302` whitespace tokens
- filler hash: `01bd1837eee176cd3fb0aed4b91b223aff4d57bf8103f95cab43cdb82b2861e2`
