# Edit Financial Budget

> **Module:** `ssi_financial_analytic_budget`
>
> **Extends:** ssi_financial_budget — model `financial_budget.budget`, action `02-edit`

## Modified Validation

- Saving fails when a change of the amount, account or direction of a line, or the
  deletion of a line, leaves the financial budget amount of that account, direction and
  period below the total of the counted analytic budgets on top level analytic accounts.
  Cancelled and rejected analytic budgets are not counted.
