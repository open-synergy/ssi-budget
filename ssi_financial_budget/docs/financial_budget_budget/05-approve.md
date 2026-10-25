# Approve Financial Budget

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** approver on the pending approval level (group _Financial Budget / Validator_)\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `approve_ok` for state
  `confirm`.
- **Access:** User is registered as an approver on the approval level that is currently
  pending. When the template uses sequential approval, only the first unapproved level
  is pending.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, the budget starts automatically: status changes
  to **In Progress** and the document number is generated.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
