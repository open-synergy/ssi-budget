# Restart Approval Process of Financial Budget

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** user in group _Financial Budget / Validator_ (`restart_approval_ok` policy)\
> **State:** `confirm` → `confirm`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `policy.template` for this model grants `restart_approval_ok`
  for state `confirm` to the actor's group.
- **Access:** User is in group _Financial Budget / Validator_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Open the record whose approval process needs to be restarted.
3. Open the **Approvals** tab to see the current approval list.
4. Click the **Restart Approval Process** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- The existing approval records are removed and the **Approvals** tab shows the approval
  list newly formed from the approval template. Any approval already given is discarded.
