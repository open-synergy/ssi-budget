# Terminate Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / Validator_ (`terminate_ok` policy)\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Config:** An active `policy.template` for this model grants `terminate_ok` for state
  `open` to the actor's group.
- **Data:** At least one termination reason is available for this model.
- **Access:** User is in group _Analytic Budget / Validator_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Termination Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Terminated**.
