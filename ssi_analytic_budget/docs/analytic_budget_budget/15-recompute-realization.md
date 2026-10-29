# Recompute Realization of Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / User_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The budget exists, in any status.
- **Access:** User is in group _Analytic Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Find and open the record whose realization needs to be recomputed.
3. Click **Action** > **Recompute Realization**.

## Post-Condition

- The **Realized** amount of every line in the **Budget Details** tab and the
  realization amounts of the budget are recalculated from the analytic lines of the
  analytic account and of its descendant accounts, inside the periods of the lines.
- A value that was already correct does not change. The action is a safety net: the
  realization is normally refreshed by itself when an analytic line is created, changed
  or deleted, or when an analytic account is moved in the hierarchy.
