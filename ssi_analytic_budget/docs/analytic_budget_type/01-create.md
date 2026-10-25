# Create Analytic Budget Type

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.type`\
> **Menu:** Cost Accounting > Configuration > Budget > Analytic Budget Types\
> **Actor:** user in group _Analytic Budget Type_

## Pre-Condition

- **Access:** User is in group _Analytic Budget Type_.

## Flow

1. Open the **Cost Accounting > Configuration > Budget > Analytic Budget Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Analytic Budget Type** _(required)_: Enter a short name.
   - **Code** _(required)_: Enter a unique code. Enter **/** to leave the code to be
     generated later with the **Generate Code** button.
   - **Excluded Accounts**: Select the accounts that budgets of this type must exclude.
4. Open the **Revenue Settings** tab. Optionally select **Allowed Revenue Accounts
   Without Product**, then add lines as many times as needed:
   - Click **Add a line**.
   - Fill in the line with:
     - **Account** _(required)_: Select a revenue account. Optionally restrict it with
       **Allowed Products** or **Allowed Product Categories**.
5. Open the **Cost Settings** tab. Optionally select **Allowed Cost Accounts Without
   Product**, then add lines as many times as needed:
   - Click **Add a line**.
   - Fill in the line with:
     - **Account** _(required)_: Select a cost account. Optionally restrict it with
       **Allowed Products** or **Allowed Product Categories**.
6. Click **Save**.

## Post-Condition

- A new analytic budget type record is created and can be selected on **Analytic
  Budget**.
