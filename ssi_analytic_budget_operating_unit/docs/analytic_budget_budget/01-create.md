# Create Analytic Budget

> **Module:** `ssi_analytic_budget_operating_unit`
>
> **Extends:** ssi_analytic_budget — model `analytic_budget.budget`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_analytic_budget_operating_unit` is installed.
- **Access:** User is in group _Multiple Operating Unit_
  (`operating_unit.group_multi_operating_unit`) to see and use the Operating Unit field
  described below. Users outside this group never see the field.

## Additional Fields

When this module is installed, the create form gains one field, placed after the
**Company** field and visible only to users in the **Multiple Operating Unit** group
(`operating_unit.group_multi_operating_unit`). The field is also available as an
optional column (hidden by default) in the list, as a search field, and as an
**Operating Unit** group-by filter:

- **Operating Unit**: the operating unit that owns this analytic budget. Not required.
  Defaults to the current user's default operating unit. Change if needed.

## Modified — Record Visibility

- The **Analytic Budgets** list is filtered by operating unit (record rule). A user only
  sees analytic budgets whose Operating Unit is one of the operating units assigned to
  them. This is not a Flow step.
