# Deactivate Analytic Budget Type

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.type`\
> **Menu:** Cost Accounting > Configuration > Budget > Analytic Budget Types\
> **Actor:** user in group _Analytic Budget Type_\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Analytic Budget Type_.

## Flow

1. Open the **Cost Accounting > Configuration > Budget > Analytic Budget Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected in new analytic budgets.
- Analytic budgets that already use this record can still be viewed.
