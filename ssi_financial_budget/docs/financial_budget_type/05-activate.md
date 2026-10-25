# Activate Financial Budget Type

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.type`\
> **Menu:** Cost Accounting > Configuration > Budget > Financial Budget Types\
> **Actor:** user in group _Financial Budget Type_\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Financial Budget Type_.

## Flow

1. Open the **Cost Accounting > Configuration > Budget > Financial Budget Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected in new financial budgets.
