# Create Monthly Budgets

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.budget`\
> **Menu:** Cost Accounting > Budget > Financial Budgets\
> **Actor:** user in group _Financial Budget / User_\
> **State:** `open` → `open`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** The budget is **Yearly** and its status is **In Progress**.
- **Record:** The yearly budget has no monthly budget in status **Draft**, **Waiting for
  Approval**, **In Progress**, **Done**, or **Terminated**.
- **Data:** At least one fiscal month period exists inside the period of the yearly
  budget, and these fiscal month periods do not overlap each other.
- **Access:** User is in group _Financial Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Financial Budgets** menu.
2. Open the yearly budget in progress.
3. Click the **Create Monthly Budgets** button.

## Post-Condition

- One monthly budget in **Draft** status is created for each fiscal month inside the
  period of the yearly budget. Each one has the yearly budget as its **Parent Budget**.
- Every monthly budget has one detail line for each account and direction of the yearly
  budget. The amount is the yearly amount divided equally by the number of months; the
  last month takes the rounding remainder, so the total equals the yearly amount.
- The status of the yearly budget does not change.
- The **Monthly Budgets** tab of the yearly budget lists the new monthly budgets.
