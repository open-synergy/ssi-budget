# Cancel Financial Budget

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** user in group _Financial Budget / Validator_ (`cancel_ok` policy)\
> **State:** `draft` | `confirm` | `open` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **In Progress**, or
  **Done**.
- **Record:** For a yearly budget, none of its monthly budgets is in status **Draft**,
  **Waiting for Approval**, **In Progress**, **Done**, or **Terminated**. Cancelled and
  rejected monthly budgets do not count.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group.
- **Data:** At least one cancellation reason is available for this model.
- **Access:** User is in group _Financial Budget / Validator_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
