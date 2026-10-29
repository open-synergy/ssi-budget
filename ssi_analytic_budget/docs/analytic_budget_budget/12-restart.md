# Restart Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / Validator_ (`restart_ok` policy)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Record:** The budget has no child budget that is still active (Draft, Waiting for
  Approval, In Progress, Done or Terminated).
- **Record:** If the budget has a **Parent Budget**, its lines fit the parent budget
  again: the total of the child budgets, this budget included, stays inside the lines of
  the parent budget.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group.
- **Access:** User is in group _Analytic Budget / Validator_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
