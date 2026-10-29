# Create Financial Budget

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** user in group _Financial Budget / User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A financial budget type exists (see
  `docs/financial_budget_type/01-create.md`).
- **Data:** A fiscal month period (date range of a date range type marked as fiscal
  month) exists, for a monthly budget.
- **Config:** For a yearly budget, the **Yearly Range Type** is set in the Financial
  Budget settings of the company and a period (date range) of that type exists.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Financial Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields in the header:
   - **Financial Budget Type** _(required)_: Select the budget type.
   - **Periodicity** _(required)_: Defaults to **Monthly**. Select **Yearly** for a
     yearly budget.
   - **Period** _(required)_: Select the period that the budget applies to. A monthly
     budget accepts a fiscal month period; a yearly budget accepts a period of the
     company **Yearly Range Type**. **Date Start** and **Date End** are filled from the
     period.
   - **Parent Budget**: For a monthly budget only. Select an open yearly budget of the
     same type and company whose period contains the period of this budget. The amounts
     of the monthly budget are then limited by the parent budget.
   - **Responsible** _(required)_: Defaults to the current user.
4. Optionally, open the **Budget Details** tab and fill in the planned budget detail
   lines. For a monthly budget with a parent budget, use only accounts and directions
   planned in the parent budget; the amounts of all monthly budgets of an account cannot
   exceed the amount of the parent budget.
5. Click **Save**.

## Post-Condition

- A new Financial Budget record is created in **Draft** status.
- Document number is still **/** (not yet generated). It is generated when the budget
  becomes **In Progress**.
