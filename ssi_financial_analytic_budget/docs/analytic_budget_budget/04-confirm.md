# Confirm Analytic Budget

> **Module:** `ssi_financial_analytic_budget`
>
> **Extends:** ssi_analytic_budget — model `analytic_budget.budget`, action `04-confirm`

## Modified Validation

- Confirm fails when the lines of the budget, together with the other counted analytic
  budgets of the same company, exceed the financial budget amount of the same account,
  direction and period. The check applies to a budget on a top level analytic account
  and ignores lines without a period.
