# Edit Analytic Budget

> **Module:** `ssi_financial_analytic_budget`
>
> **Extends:** ssi_analytic_budget — model `analytic_budget.budget`, action `02-edit`

## Modified Validation

- When both `ssi_financial_budget` and `ssi_analytic_budget` are installed, saving fails
  if the budget is on a top level analytic account (an analytic account without a
  parent) and the lines of the budget, together with the other counted analytic budgets
  of the same company, exceed the amount of the financial budgets for the same account,
  direction and period. A line is checked against every counted financial budget whose
  period contains the whole period of the line. Lines without a period, and budgets of
  child analytic accounts, are not checked.
- Changing the account, direction, period, unit price or quantity of a line is checked
  again.
