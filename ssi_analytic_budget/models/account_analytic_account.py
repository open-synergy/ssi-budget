# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    # Extension of the core analytic account. Moving an account in the
    # hierarchy changes which analytic lines the budgets of its old and
    # new ancestors consolidate, so their stored realization is refreshed.

    def write(self, vals):
        """Write analytic accounts and refresh the budget realization.

        When ``parent_id`` changes, the budgets of the ancestors before
        and after the move are scheduled for recomputation.

        :param vals: values to write
        :return: result of the parent method
        """
        watched = "parent_id" in vals
        Line = self.env["account.analytic.line"]
        old_ids = Line._get_ancestor_account_ids(self) if watched else set()
        result = super().write(vals)
        if watched:
            new_ids = Line._get_ancestor_account_ids(self)
            accounts = self.browse(list(old_ids | new_ids))
            Line._trigger_budget_realization(accounts)
        return result
