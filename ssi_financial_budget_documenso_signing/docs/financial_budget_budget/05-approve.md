# Approve Financial Budget

> **Module:** `ssi_financial_budget_documenso_signing`
>
> **Extends:** ssi_financial_budget — model `financial_budget.budget`, action
> `05-approve`

## Additional Pre-Condition

- **Module:** `ssi_financial_budget_documenso_signing` is installed.

## Modified Flow

- Anchor: at Flow base step 2 (open the record to approve), the form additionally shows
  a **Signature Requests** tab, injected because
  `_documenso_signing_create_page = True`. The tab contains the **New Signing Request**
  and **Open Signature Requests** buttons and the list of signature requests linked to
  this financial budget. It is empty until a signature request is created for the
  record.
- This module only tracks signature requests on the record. It does not change how the
  budget is approved: base Flow steps 3–4 (click **Approve**, click **OK** on the
  confirmation dialog) apply unchanged, exactly as documented in
  `ssi_financial_budget/docs/financial_budget_budget/05-approve.md`, and so does the
  base Post-Condition.
