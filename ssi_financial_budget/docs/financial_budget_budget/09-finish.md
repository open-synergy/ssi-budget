# Finish Financial Budget

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** user in group _Financial Budget / User_ (`done_ok` policy)\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group.
- **Access:** User is in group _Financial Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
