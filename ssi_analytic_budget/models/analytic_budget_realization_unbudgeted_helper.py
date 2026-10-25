# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetRealizationUnbudgetedHelper(models.Model):
    """SQL view listing realized combinations that were never budgeted.

    Reports every budget, analytic account, account and product
    combination found in ``analytic_budget_realization`` that has no
    matching row in ``analytic_budget_realization_budgeted``. It is the
    helper used to isolate unbudgeted realization.
    """

    _name = "analytic_budget.realization_unbudgeted_helper"
    _description = "Analytic Budget Unbudgeted Realization Helper"
    _auto = False
    _order = "date"

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

    def _select_one(self):
        """Return the SELECT clause of the realized side.

        Selects the budget, analytic account, account and product
        columns of ``analytic_budget_realization``.

        :return: SQL ``SELECT`` fragment as a string
        """
        select_str = """
        SELECT  a.budget_id,
                a.analytic_account_id,
                a.account_id,
                a.product_id
        """
        return select_str

    def _from_one(self):
        """Return the FROM clause of the realized side.

        The source is the ``analytic_budget_realization`` view.

        :return: SQL table expression as a string
        """
        from_str = """
        analytic_budget_realization AS a
        """
        return from_str

    def _where_one(self):
        """Return the WHERE clause of the realized side.

        No filter is applied; extension point for glue modules.

        :return: SQL ``WHERE`` fragment as a string
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join_one(self):
        """Return the JOIN clause of the realized side.

        Empty by default; extension point for glue modules. It is not
        used by ``init``.

        :return: SQL join fragment as a string
        """
        join_str = """
        """
        return join_str

    def _group_by_one(self):
        """Return the GROUP BY clause of the realized side.

        Empty by default; extension point for glue modules. It is not
        used by ``init``.

        :return: SQL ``GROUP BY`` fragment as a string
        """
        group_str = """
        """
        return group_str

    def _select_two(self):
        """Return the SELECT clause of the budgeted side.

        Selects the budget, analytic account, account and product
        columns of ``analytic_budget_realization_budgeted``.

        :return: SQL ``SELECT`` fragment as a string
        """
        select_str = """
        SELECT  b.budget_id,
                b.analytic_account_id,
                b.account_id,
                b.product_id
        """
        return select_str

    def _from_two(self):
        """Return the FROM clause of the budgeted side.

        The source is the ``analytic_budget_realization_budgeted`` view.

        :return: SQL table expression as a string
        """
        from_str = """
        analytic_budget_realization_budgeted AS b
        """
        return from_str

    def _where_two(self):
        """Return the WHERE clause of the budgeted side.

        No filter is applied; extension point for glue modules.

        :return: SQL ``WHERE`` fragment as a string
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join_two(self):
        """Return the JOIN clause of the budgeted side.

        Empty by default; extension point for glue modules. It is not
        used by ``init``.

        :return: SQL join fragment as a string
        """
        join_str = """
        """
        return join_str

    def _group_by_two(self):
        """Return the GROUP BY clause of the budgeted side.

        Empty by default; extension point for glue modules. It is not
        used by ``init``.

        :return: SQL ``GROUP BY`` fragment as a string
        """
        group_str = """
        """
        return group_str

    def init(self):
        """(Re)create the SQL view backing this model.

        Drops the view if it exists, then recreates it as the realized
        rows (``_select_one``) minus the budgeted rows (``_select_two``)
        using ``EXCEPT``.
        """
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            EXCEPT
            %s
            FROM %s
            %s
        )"""
            % (
                self._table,
                self._select_one(),
                self._from_one(),
                self._where_one(),
                self._select_two(),
                self._from_two(),
                self._where_two(),
            )
        )
