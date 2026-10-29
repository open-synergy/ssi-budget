# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetRealizationUnbudgetedHelper(models.Model):
    """SQL view listing realized combinations that were never budgeted.

    Reports every budget, analytic account, account and product
    combination found in ``analytic_budget_realization_unbudgeted``.
    It is no longer used to build the unbudgeted realization, which now
    matches the analytic lines to the details by date; the model is kept
    for compatibility.
    """

    _name = "analytic_budget.realization_unbudgeted_helper"
    _description = "Analytic Budget Unbudgeted Realization Helper"
    _auto = False
    _order = "budget_id"

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )

    def _select(self):
        """Return the SELECT clause of the view query.

        Selects the distinct budget, analytic account, account and
        product columns of the unbudgeted realization.

        :return: SQL ``SELECT`` fragment as a string
        """
        select_str = """
        SELECT DISTINCT
                a.budget_id,
                a.analytic_account_id,
                a.account_id,
                a.product_id
        """
        return select_str

    def _from(self):
        """Return the FROM clause of the view query.

        The source is the ``analytic_budget_realization_unbudgeted``
        view.

        :return: SQL table expression as a string
        """
        from_str = """
        analytic_budget_realization_unbudgeted AS a
        """
        return from_str

    def _where(self):
        """Return the WHERE clause of the view query.

        No filter is applied; extension point for glue modules.

        :return: SQL ``WHERE`` fragment as a string
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def init(self):
        """(Re)create the SQL view backing this model.

        Drops the view if it exists, then recreates it from the
        ``_select``, ``_from`` and ``_where`` fragments.
        """
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._where(),
            )
        )
