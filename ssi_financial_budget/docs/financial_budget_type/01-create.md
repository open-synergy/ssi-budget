# Create Financial Budget Type

> **Module:** `ssi_financial_budget`\
> **Model:** `financial_budget.type`\
> **Menu:** Cost Accounting > Configuration > Budget > Financial Budget Types\
> **Actor:** user in group _Financial Budget Type_

## Pre-Condition

- **Access:** User is in group _Financial Budget Type_.

## Flow

1. Open the **Cost Accounting > Configuration > Budget > Financial Budget Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Financial Budget Type** _(required)_: Enter a short name.
   - **Code** _(required)_: Enter a unique code. Enter **/** to leave the code to be
     generated later with the **Generate Code** button.
   - **Allowed Accounts**: Select the accounts that budgets of this type may use.
4. Click **Save**.

## Post-Condition

- A new financial budget type record is created and can be selected on **Financial
  Budget**.
