# Restart Analytic Budget

> **Module:** `ssi_financial_analytic_budget`
>
> **Extends:** ssi_analytic_budget — model `analytic_budget.budget`, action `12-restart`

## Modified Validation

- Restart fails when the budget, counted again together with the other counted analytic
  budgets of the same company, would exceed the financial budget amount of the same
  account, direction and period. Budgets in the Cancel or Reject state are not counted
  until they are restarted.
