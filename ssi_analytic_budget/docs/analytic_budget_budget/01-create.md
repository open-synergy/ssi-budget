# Create Analytic Budget

> **Module:** `ssi_analytic_budget`\
> **Model:** `analytic_budget.budget`\
> **Menu:** Cost Accounting > Budget > Analytic Budgets\
> **Actor:** user in group _Analytic Budget / User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** An analytic budget type exists (see
  `docs/analytic_budget_type/01-create.md`).
- **Data:** An analytic account exists.
- **Data:** Optional: to make the budget a child budget, the budget of the parent
  analytic account exists.
- **Data:** Optional: to plan a line for a period, a date range exists for it.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Analytic Budget / User_.

## Flow

1. Open the **Cost Accounting > Budget > Analytic Budgets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields in the header:
   - **Analytic Budget Type** _(required)_: Select the budget type. The **Accounts** and
     **Excluded** lists on the **Accounts** tab are filled from the type.
   - **Analytic Account** _(required)_: Select the analytic account that the budget
     applies to.
   - **Parent Budget**: Optionally select the budget of the parent analytic account of
     the selected **Analytic Account**. Only such budgets are offered. Leave it empty
     for a budget without parent.
   - **Responsible** _(required)_: Defaults to the current user.
4. Optionally, open the **Budget Details** tab and fill in the planned revenue and cost
   lines. In each line:
   - **Account** _(required)_: Select the account.
   - **Product**: Select the product. It is required when the account asks for a product
     in the budget type.
   - **Period**: Optionally select a date range. Only the analytic lines dated inside
     the range are realized against the line. Leave it empty for a line without date
     limit.
   - Fill in the price, quantity and unit of measure.
   - **Multipliers**: Optionally open the **Multipliers** tab of the line and add one
     row per factor (for example persons, days, times). In each row fill in the **Name**
     _(required)_, the **Factor** _(required, greater than zero)_ and optionally the
     **UoM**. When the line has at least one factor, the **Quantity** becomes read-only
     and shows the product of all factors; the **Subtotal** is the price times that
     quantity. Leave the tab empty to type the quantity manually.
5. Click **Save**.

## Post-Condition

- A new Analytic Budget record is created in **Draft** status.
- Document number is still **/** (not yet generated). It is generated when the budget
  becomes **In Progress**.
- **Date Start** and **Date End** show the earliest start and the latest end of the
  periods of the lines. They stay empty when no line has a period.
- The same account and product cannot be planned twice in overlapping periods of one
  budget; a line without period overlaps every other line of that account and product.
