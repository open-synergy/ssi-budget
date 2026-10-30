# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class FinancialBudgetDetail(models.Model):
    _name = "financial_budget.detail"
    _inherit = [
        "financial_budget.detail",
    ]

    @api.depends(
        "amount",
        "account_id",
        "direction",
        "budget_id.period_id",
        "budget_id.company_id",
    )
    def _compute_amount_allocated_analytic(self):
        """Compute the analytic budget amount allocated to the line.

        The allocation is the total of the counted top level analytic
        budget lines with the same account and direction inside the
        period of the budget.

        :return: None
        """
        obj_detail = self.env["analytic_budget.detail"]
        for record in self:
            result = 0.0
            budget = record.budget_id
            if budget.period_id and record.account_id:
                result = obj_detail._get_analytic_allocation_amount(
                    budget.company_id,
                    record.account_id,
                    record.direction,
                    budget.period_id,
                )
            record.amount_allocated_analytic = result

    amount_allocated_analytic = fields.Monetary(
        string="Allocated Analytic Amount",
        compute="_compute_amount_allocated_analytic",
        compute_sudo=True,
        store=False,
        readonly=True,
        currency_field="company_currency_id",
        help="Total of the analytic budget lines of top level analytic "
        "accounts with the same account and direction inside the period "
        "of this budget.",
    )

    def _get_analytic_ceiling_keys(self):
        """Collect the ceilings that the lines give to analytic budgets.

        Only lines of a counted financial budget with a period give a
        ceiling.

        :return: database id of one line for each ceiling key
        :rtype: dict
        """
        obj_budget = self.env["financial_budget.budget"]
        states = obj_budget._get_allocation_child_states()
        keys = {}
        for record in self.sudo():
            budget = record.budget_id
            if budget.state not in states or not budget.period_id:
                continue
            if not record.account_id:
                continue
            key = (
                budget.company_id,
                record.account_id,
                record.direction,
                budget.period_id,
            )
            keys.setdefault(key, record.id)
        return keys

    def _check_analytic_ceiling(self, keys):
        """Check the analytic allocation of the given ceilings.

        :param keys: result of ``_get_analytic_ceiling_keys``
        :raises ValidationError: if an allocation exceeds its ceiling
        """
        obj_detail = self.env["analytic_budget.detail"]
        if not obj_detail._is_financial_ceiling_enabled():
            return
        for key, record_id in keys.items():
            company, account, direction, period = key
            obj_detail._check_financial_ceiling_total(
                company,
                account,
                direction,
                period,
                record_id,
                "Save financial budget detail",
            )

    @api.constrains("budget_id", "account_id", "direction", "amount")
    def _constrains_analytic_ceiling(self):
        """Keep the financial budget above the analytic allocation.

        :raises ValidationError: if an allocation exceeds its ceiling
        """
        self._check_analytic_ceiling(self._get_analytic_ceiling_keys())

    def write(self, vals):
        """Write the lines then recheck the ceilings they left.

        A change of account, direction or amount lowers the ceiling of
        the previous values, which the constraint does not see.

        :param vals: values to write
        :return: result of the parent method
        """
        watched = {"budget_id", "account_id", "direction", "amount"}
        old_keys = {}
        if watched & set(vals):
            old_keys = self._get_analytic_ceiling_keys()
        result = super().write(vals)
        if old_keys:
            self._check_analytic_ceiling(old_keys)
        return result

    def unlink(self):
        """Delete the lines then recheck the ceilings they gave.

        :return: result of the parent method
        """
        keys = self._get_analytic_ceiling_keys()
        result = super().unlink()
        self._check_analytic_ceiling(keys)
        return result
