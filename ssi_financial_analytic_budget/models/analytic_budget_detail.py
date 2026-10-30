# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools import config, float_compare


class AnalyticBudgetDetail(models.Model):
    _name = "analytic_budget.detail"
    _inherit = [
        "analytic_budget.detail",
    ]

    @api.model
    def _is_financial_ceiling_enabled(self):
        """Tell whether the financial ceiling check is active.

        While the test suite runs, every addon of the repository shares
        one database, so the check is active only for the tests that
        opt in with the ``test_financial_analytic_budget`` context key.

        :return: True when the ceiling must be checked
        :rtype: bool
        """
        if config["test_enable"]:
            return bool(self.env.context.get("test_financial_analytic_budget"))
        return True

    def _is_financial_ceiling_counted(self, extra_budget):
        """Tell whether the line is counted against a financial ceiling.

        A line is counted when it has a period, its budget belongs to a
        top level analytic account, and its budget is in an allocation
        state or is the budget given as extra.

        :param extra_budget: analytic budget counted whatever its state
        :return: True when the line is counted
        :rtype: bool
        """
        self.ensure_one()
        budget = self.budget_id
        states = budget._get_allocation_child_states()
        return bool(
            self.period_id
            and not budget.analytic_account_id.parent_id
            and (budget.state in states or budget in extra_budget)
        )

    def _get_financial_ceiling_periods(self):
        """Find the financial budget periods that cap the line.

        Every period of a counted financial budget of the same company
        that contains the whole period of the line is a ceiling period.

        :return: ceiling periods, may be empty
        :rtype: recordset of ``date.range``
        """
        self.ensure_one()
        obj_budget = self.env["financial_budget.budget"].sudo()
        budgets = obj_budget.search(
            [
                ("company_id", "=", self.budget_id.company_id.id),
                ("state", "in", obj_budget._get_allocation_child_states()),
                ("period_id.date_start", "<=", self.period_id.date_start),
                ("period_id.date_end", ">=", self.period_id.date_end),
            ]
        )
        return budgets.mapped("period_id")

    @api.model
    def _get_analytic_allocation_amount(
        self, company, account, direction, period, extra_budget=None
    ):
        """Sum the counted top level analytic lines inside a period.

        :param company: company of the budgets
        :param account: accounting account of the lines
        :param direction: ``revenue`` or ``cost``
        :param period: date range that must contain the lines
        :param extra_budget: analytic budget counted whatever its state
        :return: total of the line subtotals
        :rtype: float
        """
        states = self.env["analytic_budget.budget"]._get_allocation_child_states()
        criteria = [
            ("budget_id.company_id", "=", company.id),
            ("analytic_account_id.parent_id", "=", False),
            ("account_id", "=", account.id),
            ("direction", "=", direction),
            ("period_id.date_start", ">=", period.date_start),
            ("period_id.date_end", "<=", period.date_end),
        ]
        if extra_budget:
            criteria += [
                "|",
                ("budget_id.state", "in", states),
                ("budget_id", "in", extra_budget.ids),
            ]
        else:
            criteria.append(("budget_id.state", "in", states))
        return sum(self.sudo().search(criteria).mapped("price_subtotal"))

    @api.model
    def _get_financial_ceiling_amount(self, company, account, direction, period):
        """Sum the amounts of the counted financial budget lines.

        :param company: company of the budgets
        :param account: accounting account of the lines
        :param direction: ``revenue`` or ``cost``
        :param period: period of the financial budgets
        :return: total of the financial budget amounts
        :rtype: float
        """
        obj_budget = self.env["financial_budget.budget"]
        details = (
            self.env["financial_budget.detail"]
            .sudo()
            .search(
                [
                    ("budget_id.company_id", "=", company.id),
                    (
                        "budget_id.state",
                        "in",
                        obj_budget._get_allocation_child_states(),
                    ),
                    ("budget_id.period_id", "=", period.id),
                    ("account_id", "=", account.id),
                    ("direction", "=", direction),
                ]
            )
        )
        return sum(details.mapped("amount"))

    @api.model
    def _raise_financial_ceiling_error(self, context_name, record_id):
        """Raise the error of an exceeded financial ceiling.

        The environment is cleared first: the cache, the pending writes
        and the pending recomputes are shared by every environment of
        the thread, so another cursor of the same thread (e.g. a REST
        request log) would otherwise flush them onto rows locked by
        the failing transaction. The transaction is rolled back by the
        raised error anyway.

        :param context_name: action shown in the context of the message
        :param record_id: database id shown in the message
        :raises ValidationError: always
        """
        error_message = (
            _(
                """
Context: %s
Database ID: %s
Problem: Analytic budget allocation exceeds the financial budget amount
Solution: Reduce the analytic budget lines or raise the amount of the \
financial budget for the same account, direction and period
"""
            )
            % (context_name, record_id)
        )
        self.env.clear()
        raise ValidationError(error_message)

    @api.model
    def _check_financial_ceiling_total(
        self,
        company,
        account,
        direction,
        period,
        record_id,
        context_name,
        extra_budget=None,
    ):
        """Check the analytic total of one ceiling against its ceiling.

        :param company: company of the budgets
        :param account: accounting account of the lines
        :param direction: ``revenue`` or ``cost``
        :param period: ceiling period
        :param record_id: database id shown in the error message
        :param context_name: action shown in the error message
        :param extra_budget: analytic budget counted whatever its state
        :raises ValidationError: if the allocation exceeds the ceiling
        """
        allocated = self._get_analytic_allocation_amount(
            company, account, direction, period, extra_budget=extra_budget
        )
        ceiling = self._get_financial_ceiling_amount(
            company, account, direction, period
        )
        rounding = company.currency_id.rounding
        if float_compare(allocated, ceiling, precision_rounding=rounding) > 0:
            self._raise_financial_ceiling_error(context_name, record_id)

    def _check_financial_ceiling(self, extra_budget=None):
        """Check the counted lines against the financial budgets.

        A counted line without any ceiling period has a ceiling of zero.
        Every ceiling touched by the lines is checked once.

        :param extra_budget: analytic budget counted whatever its state
        :raises ValidationError: if an allocation exceeds its ceiling
        """
        if not self._is_financial_ceiling_enabled():
            return
        extra = extra_budget or self.env["analytic_budget.budget"]
        context_name = "Save analytic budget detail"
        keys = {}
        for record in self.sudo():
            if not record._is_financial_ceiling_counted(extra):
                continue
            company = record.budget_id.company_id
            periods = record._get_financial_ceiling_periods()
            if not periods:
                rounding = company.currency_id.rounding
                if (
                    float_compare(
                        record.price_subtotal, 0.0, precision_rounding=rounding
                    )
                    > 0
                ):
                    self._raise_financial_ceiling_error(context_name, record.id)
                continue
            for period in periods:
                key = (company, record.account_id, record.direction, period)
                keys.setdefault(key, record.id)
        for key, record_id in keys.items():
            company, account, direction, period = key
            self._check_financial_ceiling_total(
                company,
                account,
                direction,
                period,
                record_id,
                context_name,
                extra_budget=extra,
            )

    @api.constrains(
        "budget_id",
        "account_id",
        "direction",
        "period_id",
        "price_unit",
        "uom_quantity",
    )
    def _constrains_financial_ceiling(self):
        """Keep the top level analytic lines inside the financial budget.

        :raises ValidationError: if an allocation exceeds its ceiling
        """
        self._check_financial_ceiling()
