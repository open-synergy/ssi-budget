# Restart Financial Budget

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** user in group _Financial Budget / Validator_ (`restart_ok` policy)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Record:** For a yearly budget, none of its monthly budgets is in status **Draft**,
  **Waiting for Approval**, **In Progress**, **Done**, or **Terminated**.
- **Record:** For a monthly budget with a parent budget, restarting does not make the
  monthly budgets of an account exceed the amount of the parent budget.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group.
- **Access:** User is in group _Financial Budget / Validator_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
