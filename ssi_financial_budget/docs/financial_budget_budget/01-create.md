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
  month) exists.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Financial Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields in the header:
   - **Financial Budget Type** _(required)_: Select the budget type.
   - **Period** _(required)_: Select the fiscal month period that the budget applies to.
     **Date Start** and **Date End** are filled from the period.
   - **Responsible** _(required)_: Defaults to the current user.
4. Optionally, open the **Budget Details** tab and fill in the planned budget detail
   lines.
5. Click **Save**.

## Post-Condition

- A new Financial Budget record is created in **Draft** status.
- Document number is still **/** (not yet generated). It is generated when the budget
  becomes **In Progress**.
