# Cancel Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / Validator_ (`cancel_ok` policy)\
> **State:** `draft` | `confirm` | `open` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **In Progress**, or
  **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group.
- **Record:** The budget has no child budget that is still active (Draft, Waiting for
  Approval, In Progress, Done or Terminated). Cancel or reject the child budgets first.
- **Data:** At least one cancellation reason is available for this model.
- **Access:** User is in group _Analytic Budget / Validator_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
