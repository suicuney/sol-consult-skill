# Sol High Plan Review Packet

Use this packet only for executable-plan review before implementation.

````markdown
SOL_HIGH_PLAN_REVIEW_V1

```json
{
  "task_id": "sol-high-plan-review-YYYYMMDD-HHMMSS",
  "sentinel": "SOL_HIGH_PLAN_REVIEW_RESULT_YYYYMMDD_HHMMSS",
  "review_round": 1,
  "max_review_rounds": 3,
  "credential_status": "no_executable_credentials"
}
```

## USER REQUIREMENT

## REPOSITORY FACTS

## RESOLVED DECISIONS

## EXECUTABLE PLAN

## ACCEPTANCE CRITERIA

## EXECUTION SLICES

## VERIFICATION STRATEGY

## RISKS / ONE-WAY DECISIONS

## CODEX LOCAL JUDGMENT

## ASK

Review this executable plan as a strict independent plan critic.

Rules:
- Find blocking flaws first.
- Do not expand product scope.
- Do not take ownership of the plan.
- Distinguish real blockers from optional polish.
- If a real product/architecture trade-off requires the user, say so explicitly.
- Do not reveal hidden chain-of-thought; provide concise reasons and evidence instead.

## RETURN FORMAT

First line must be:

SOL_HIGH_PLAN_REVIEW_RESULT_YYYYMMDD-HHMMSS

Then return exactly these sections:

1. Verdict: `PASS | REVISE | USER_DECISION_REQUIRED`
2. Blocking Findings
3. Non-blocking Suggestions
4. Missing Evidence
5. User Decisions Required
6. Recommendation
````
