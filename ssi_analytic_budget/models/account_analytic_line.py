# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # Extension of the core analytic line. The stored realization of the
    # analytic budgets of the line account and of all its ancestors is
    # scheduled for recomputation whenever a relevant line changes.

    @api.model
    def _get_budget_trigger_fields(self):
        """Return the fields whose change affects the budget realization.

        Public extension point used by ``write``.

        :return: names of the fields watched by the budget trigger
        :rtype: list
        """
        return [
            "amount",
            "account_id",
            "date",
            "general_account_id",
            "product_id",
            "unit_amount",
        ]

    @api.model
    def _get_ancestor_account_ids(self, accounts):
        """Return the ids of the accounts and of all their ancestors.

        The ancestors are read from ``parent_path`` of each account.

        :param accounts: analytic accounts
        :return: ids of the accounts and of their ancestors
        :rtype: set
        """
        result = set()
        for account in accounts.sudo():
            result.add(account.id)
            for path_id in (account.parent_path or "").split("/"):
                if path_id:
                    result.add(int(path_id))
        return result

    @api.model
    def _trigger_budget_realization(self, accounts):
        """Schedule the recomputation of the budgets of the accounts.

        Every budget whose analytic account is one of the given
        accounts or an ancestor of them gets its stored realization and
        the realized amount of its details recomputed.

        :param accounts: analytic accounts whose lines changed
        :return: None
        """
        account_ids = self._get_ancestor_account_ids(accounts)
        if not account_ids:
            return
        budgets = self.env["analytic_budget.budget"].sudo()
        budgets = budgets.search(
            self._get_budget_trigger_criteria(list(account_ids)),
        )
        budgets._add_realization_to_compute()

    @api.model
    def _get_budget_trigger_criteria(self, account_ids):
        """Build the criteria of the budgets to recompute.

        :param account_ids: ids of the analytic accounts and ancestors
        :return: search domain on ``analytic_budget.budget``
        :rtype: list
        """
        return [("analytic_account_id", "in", account_ids)]

    @api.model_create_multi
    def create(self, vals_list):
        """Create analytic lines and refresh the budget realization.

        :param vals_list: list of values of the lines to create
        :return: the new analytic lines
        """
        records = super().create(vals_list)
        self._trigger_budget_realization(records.mapped("account_id"))
        return records

    def write(self, vals):
        """Write analytic lines and refresh the budget realization.

        The refresh covers the old and the new account of the lines and
        happens only when a watched field is written.

        :param vals: values to write
        :return: result of the parent method
        """
        watched = bool(set(vals) & set(self._get_budget_trigger_fields()))
        accounts = self.mapped("account_id") if watched else self.browse()
        result = super().write(vals)
        if watched:
            self._trigger_budget_realization(accounts | self.mapped("account_id"))
        return result

    def unlink(self):
        """Delete analytic lines and refresh the budget realization.

        :return: result of the parent method
        """
        accounts = self.mapped("account_id")
        result = super().unlink()
        self._trigger_budget_realization(accounts)
        return result
