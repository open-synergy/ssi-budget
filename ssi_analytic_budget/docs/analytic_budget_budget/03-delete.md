# Delete Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / User_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _Analytic Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Find and open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The record is permanently removed and no longer appears in the list.
