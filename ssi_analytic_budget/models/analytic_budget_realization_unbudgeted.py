# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetRealizationUnbudgeted(models.Model):
    """Report unbudgeted realizations of analytic budgets.

    Read-only SQL view listing the realized amounts of the analytic
    lines that do not match any detail line of their budget, inside the
    date range of the budget when it has one. Matching follows the rules
    of ``analytic_budget.realization_budgeted``: same account, the same
    product or no product, and a period holding the date.
    """

    _name = "analytic_budget.realization_unbudgeted"
    _description = "Analytic Budget Unbudgeted Realization"
    _auto = False
    _order = "date"

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
    )
    date = fields.Date(
        string="Date",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
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
    amount_realized = fields.Monetary(
        string="Amount Realized",
        currency_field="company_currency_id",
    )

    def _select(self):
        """Return the ``SELECT`` clause of the report view.

        Builds the view columns: a generated row id, the budget,
        analytic account, account, product, date, currency and
        realized amount of the realization rows.

        :return: SQL ``SELECT`` fragment as a string
        """
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.budget_id AS budget_id,
            a.analytic_account_id AS analytic_account_id,
            a.account_id AS account_id,
            a.product_id,
            a.date,
            a.company_currency_id,
            a.amount_realized AS amount_realized
        """
        return select_str

    def _from(self):
        """Return the ``FROM`` clause of the report view.

        The data source is the realization view, before any matching.

        :return: SQL table expression as a string
        """
        from_str = """
        analytic_budget_realization AS a
        """
        return from_str

    def _where(self):
        """Return the ``WHERE`` clause of the report view.

        Keeps the realization rows that match no detail line of the
        budget and that are dated inside the date range of the budget.

        :return: SQL ``WHERE`` fragment as a string
        """
        where_str = """
        WHERE 1 = 1 AND
            NOT EXISTS (
                SELECT  1
                FROM analytic_budget_detail AS d
                LEFT JOIN date_range AS p ON d.period_id = p.id
                WHERE   d.budget_id = a.budget_id AND
                        d.account_id = a.account_id AND
                        (d.product_id IS NULL OR d.product_id = a.product_id) AND
                        (
                            d.period_id IS NULL OR
                            (a.date >= p.date_start AND a.date <= p.date_end)
                        )
            ) AND
            (b.date_start IS NULL OR a.date >= b.date_start) AND
            (b.date_end IS NULL OR a.date <= b.date_end)
        """
        return where_str

    def _join(self):
        """Return the ``JOIN`` clause of the report view.

        Joins the budget header, whose date range limits the rows.

        :return: SQL ``JOIN`` fragment as a string
        """
        join_str = """
        JOIN analytic_budget_budget AS b ON a.budget_id = b.id
        """
        return join_str

    def _group_by(self):
        """Return the ``GROUP BY`` clause of the report view.

        The view is not aggregated, so the clause is empty.

        :return: SQL ``GROUP BY`` fragment as a string
        """
        group_str = """
        """
        return group_str

    def init(self):
        """Recreate the SQL view backing this report model.

        Drops the view if it exists, then creates it again from the
        ``_select``, ``_from``, ``_join``, ``_where`` and ``_group_by``
        fragments.
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
