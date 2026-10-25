# Create Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** An analytic budget type exists (see
  `docs/analytic_budget_type/01-create.md`).
- **Data:** An analytic account exists.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Analytic Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields in the header:
   - **Analytic Budget Type** _(required)_: Select the budget type. The **Accounts** and
     **Excluded** lists on the **Accounts** tab are filled from the type.
   - **Analytic Account** _(required)_: Select the analytic account that the budget
     applies to.
   - **Responsible** _(required)_: Defaults to the current user.
4. Optionally, open the **Budget Details** tab and fill in the planned revenue and cost
   lines.
5. Click **Save**.

## Post-Condition

- A new Analytic Budget record is created in **Draft** status.
- Document number is still **/** (not yet generated). It is generated when the budget
  becomes **In Progress**.
