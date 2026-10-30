# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models

from odoo.addons.ssi_decorator import ssi_decorator


class AnalyticBudgetBudget(models.Model):
    _name = "analytic_budget.budget"
    _inherit = [
        "analytic_budget.budget",
    ]

    @ssi_decorator.pre_confirm_check()
    def _30_check_financial_ceiling_confirm(self):
        """Reject confirming a budget above the financial budget.

        Runs on the ``pre_confirm_check`` slot.

        :raises ValidationError: if an allocation exceeds its ceiling
        """
        self.ensure_one()
        self.detail_ids._check_financial_ceiling(extra_budget=self)

    @ssi_decorator.pre_restart_check()
    def _30_check_financial_ceiling_restart(self):
        """Reject restarting a budget above the financial budget.

        Runs on the ``pre_restart_check`` slot, counting this budget
        itself in the allocation it would join again.

        :raises ValidationError: if an allocation exceeds its ceiling
        """
        self.ensure_one()
        self.detail_ids._check_financial_ceiling(extra_budget=self)
