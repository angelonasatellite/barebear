# Capstone marking rubric

A 100-point rubric for marking the Lesson 13 capstone project. Designed
to be used as-is or adapted to your school's grading bands.

## Aspect 1 — Functionality (25 points)

Does the agent do what the README claims?

| Band | Points | Description |
|---|---|---|
| Excellent | 22–25 | Every claimed behaviour works on first run. The happy path is robust. |
| Good | 16–21 | The agent runs end-to-end. Most claimed behaviours work. One or two minor issues acknowledged in the write-up. |
| Adequate | 10–15 | The agent runs but is fragile. Several claimed behaviours don't work or only work in narrow conditions. |
| Limited | 0–9 | The agent fails to run end-to-end, or makes claims clearly contradicted by the report. |

**Look for:** the agent producing useful output, not just any output. A
homework-helper that gives nonsense answers in valid JSON is failing
this aspect even if it doesn't crash.

## Aspect 2 — Tool design (15 points)

Are the tools well-designed?

| Band | Points | Description |
|---|---|---|
| Excellent | 13–15 | At least three tools. Each has a clear, non-overlapping purpose. Names and descriptions match what they do. Type annotations correct. |
| Good | 9–12 | Three tools present. Names and descriptions reasonable. Some overlap or vagueness. |
| Adequate | 5–8 | Tools present but poorly distinguished, or descriptions are too vague for the model to choose between them reliably. |
| Limited | 0–4 | Fewer than three tools, or tools so similar the model can't tell them apart. |

**Look for:** can a fellow student, *without seeing the code*, guess
which tool the agent will pick for a given task? If not, the
descriptions need work.

## Aspect 3 — Policy and safety (20 points)

Are the right constraints chosen, and are they actually enforced?

| Band | Points | Description |
|---|---|---|
| Excellent | 18–20 | Policy reflects the actual risk profile of the tools. At least one budget set sensibly. At least one approval/block constraint that the agent could plausibly trigger. The submission includes a report showing the constraint firing. |
| Good | 13–17 | Policy is reasonable. Constraints exist. Evidence of enforcement is shown. |
| Adequate | 7–12 | Policy is present but generic — `max_steps=10, blocked_tools=[]`. No evidence the constraints ever fire. |
| Limited | 0–6 | No policy or one that doesn't match the agent's behaviour (e.g. `allow_external_side_effects=True` for an agent that handles emails). |

**Look for:** the student articulating *why* they chose those
constraints in the write-up. "I blocked X because Y" is the
deliverable.

## Aspect 4 — Reports and tests (15 points)

Is there behavioural evidence the agent does what's claimed?

| Band | Points | Description |
|---|---|---|
| Excellent | 13–15 | Two reports submitted: one happy-path, one failure-mode (budget exhaustion / policy block / checkpoint). Two pytest assertions present and meaningful. |
| Good | 9–12 | Two reports submitted, both showing relevant behaviour. Pytest assertions present. |
| Adequate | 5–8 | One report submitted. Pytest assertions present but trivial (e.g. `assert report.status == "completed"`). |
| Limited | 0–4 | No reports, or tests that don't actually test agent behaviour. |

**Look for:** assertions that pin down *behaviour*, not just *output*.
"The agent must call read_ticket before draft_email" is meaningful;
"the final output is a string" is not.

## Aspect 5 — Honest uncertainty (10 points)

Does the agent flag what it doesn't know?

| Band | Points | Description |
|---|---|---|
| Excellent | 9–10 | Agent system prompt explicitly invites uncertainty. Report shows `assumptions` and/or `uncertainties` populated in at least one run. Write-up reflects on what the agent surfaced. |
| Good | 6–8 | Agent acknowledges uncertainty in some way; some reflection in write-up. |
| Adequate | 3–5 | Mention of uncertainty in the README but no evidence the agent surfaces it. |
| Limited | 0–2 | No engagement with uncertainty; the agent always sounds confident. |

**Look for:** does the student treat hallucination as a property of
the system to be designed-against, or as something they hope won't
happen?

## Aspect 6 — Write-up (15 points)

Clarity, justification of design decisions, surfaced trade-offs.

| Band | Points | Description |
|---|---|---|
| Excellent | 13–15 | About 300 words, well-structured. Explains what, why, and what didn't work. Names the design trade-offs explicitly ("I considered X but chose Y because..."). |
| Good | 9–12 | Clear what the agent does and most key choices. Some trade-offs surfaced. |
| Adequate | 5–8 | Describes what the agent does. No real reflection on design choices. |
| Limited | 0–4 | Either too short to assess, or only re-states the code in prose. |

**Look for:** the strongest write-ups admit failure. *"I tried Z, the
agent kept ignoring the policy, so I switched to W"* shows engineering
judgement. *"Everything worked perfectly first time"* usually means the
student didn't try anything ambitious.

## Suggested marking process

1. **First read the README** before opening the code or running the
   agent. What is the student claiming?
2. **Run the agent yourself** following the README. Does it work?
3. **Look at the submitted reports.** Do they back up the README?
4. **Run the pytest tests.** Do they pass? Do they actually test
   behaviour?
5. **Read the code last.** By now you've formed a view of whether the
   submission is a working agent or a story about a working agent.
   The code either confirms or contradicts what you've seen.

This order — claim, behaviour, evidence, code — is the same way you'd
review a real-world agent in production. Students who've thought about
this order in their submission will mark well by default.

## Adapting to your grading scale

| Common scale | Suggested mapping |
|---|---|
| UK A*/A/B/C/D/E | A* = 85+, A = 70–84, B = 55–69, C = 40–54, D = 25–39, E = below |
| Percentage | Use the 100-point total directly |
| 4-point GPA | A = 80+, B = 65–79, C = 50–64, D = 35–49, F = below |
| Pass/Distinction/Merit | Pass ≥ 50, Merit ≥ 65, Distinction ≥ 80 |

Adjust to your context. The relative weighting of the six aspects
matters more than the bands.
