# Create Analytic Budget

> **Module:** `ssi_analytic_budget_work_log`
>
> **Extends:** ssi_analytic_budget — model `analytic_budget.budget`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_analytic_budget_work_log` is installed.

## Additional Fields

The create form gains a **Work Log** tab. It is shown after the other tabs of the
analytic budget and holds the following fields:

- **Estimation**: The planned working time for the budget. Optional.
- **Total**: Read-only. The total working time logged against the budget.
- **Remaining**: Read-only. The part of the estimation that has not been logged yet.
- **Excess**: Read-only. The working time logged beyond the estimation.
- **Work Log Analytic Account**: Optional. The analytic account used when work is logged
  against the budget.
- **Work Logs**: The work log lines recorded against the budget. It is empty on a new
  budget.

The base Flow steps 1–5 apply unchanged, as documented in
`ssi_analytic_budget/docs/analytic_budget_budget/01-create.md`, and so does the base
Post-Condition.
