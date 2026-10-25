# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetRealization(models.Model):
    """Report the realized amount of each analytic budget.

    Read-only SQL view (``_auto = False``) that joins every analytic
    budget with the posted analytic lines of its analytic account,
    grouped by date, general account and product. Each row exposes the
    amount realized against the budget.
    """

    _name = "analytic_budget.realization"
    _description = "Analytic Budget Realization"
    _auto = False
    _order = "date"

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
    )
    date = fields.Date(
        string="Date",
    )
    analytic_account_id = fields.Many2one(
        string="Account",
        comodel_name="account.analytic.account",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    amount_realized = fields.Monetary(
        string="Amount Realized",
        currency_field="company_currency_id",
    )

    def _select(self):
        """Return the ``SELECT`` clause of the view query.

        Pick the budget, its analytic account, date, general account,
        product and the realized amount of each analytic line group.

        :return: SQL ``SELECT`` fragment
        """
        select_str = """
        SELECT  row_number() OVER() as id,
                a.id AS budget_id,
                a.company_currency_id,
                b.account_id AS analytic_account_id,
                b.date as date,
                b.general_account_id AS account_id,
                b.product_id AS product_id,
                b.amount AS amount_realized
        """
        return select_str

    def _from(self):
        """Return the ``FROM`` clause of the view query.

        The budget table is the driving source of the view.

        :return: SQL fragment naming the source table
        """
        from_str = """
        analytic_budget_budget AS a
        """
        return from_str

    def _where(self):
        """Return the ``WHERE`` clause of the view query.

        No extra criteria by default; override to restrict the rows.

        :return: SQL ``WHERE`` fragment
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Return the ``JOIN`` clause of the view query.

        Join each budget to its analytic lines that belong to a journal
        entry, summed by account, general account, product and date.

        :return: SQL ``JOIN`` fragment
        """
        join_str = """
        JOIN (
            SELECT  b1.account_id,
                    b1.general_account_id,
                    b1.product_id,
                    b1.date,
                    SUM(b1.amount) AS amount
            FROM account_analytic_line AS b1
            WHERE       b1.move_id IS NOT NULL
            GROUP BY    b1.account_id,
                        b1.general_account_id,
                        b1.product_id,
                        b1.date

        ) AS b ON   a.analytic_account_id = b.account_id

        """
        return join_str

    def _group_by(self):
        """Return the ``GROUP BY`` clause of the view query.

        Empty by default because the aggregation is done in the join.

        :return: SQL ``GROUP BY`` fragment
        """
        group_str = """
        """
        return group_str

    def init(self):
        """Recreate the SQL view when the module is installed or updated.

        Drop the view if it exists, then create it from the fragments
        returned by the ``_select``, ``_from``, ``_join``, ``_where``
        and ``_group_by`` methods.
        """
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
