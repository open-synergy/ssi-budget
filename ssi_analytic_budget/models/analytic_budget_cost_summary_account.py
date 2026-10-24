# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetCostSummaryAccount(models.Model):
    """Report budgeted cost per analytic account and account.

    SQL view (``_auto = False``) that sums the subtotal of cost
    direction budget details grouped by budget, analytic account and
    accounting account.
    """

    _name = "analytic_budget.cost_summary_account"
    _description = "Analytic Budget Cost Summary By Account"
    _auto = False

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
    )
    analytic_account_id = fields.Many2one(
        string="Account",
        comodel_name="account.analytic.account",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    amount_budgeted = fields.Monetary(
        string="Amount Budgeted",
        currency_field="company_currency_id",
    )

    def _select(self):
        """Build the SELECT clause of the view query.

        Selects the budget, company currency, account and analytic
        account, plus the summed budgeted amount of the details.

        :return: SQL SELECT fragment
        :rtype: str
        """
        select_str = """
        SELECT  row_number() OVER() as id,
                a.id AS budget_id,
                a.company_currency_id AS company_currency_id,
                b.account_id AS account_id,
                a.analytic_account_id AS analytic_account_id,
                SUM(b.price_subtotal) AS amount_budgeted
        """
        return select_str

    def _from(self):
        """Build the FROM clause of the view query.

        The data source is the budget table, aliased as ``a``.

        :return: SQL FROM fragment
        :rtype: str
        """
        from_str = """
        analytic_budget_budget AS a
        """
        return from_str

    def _where(self):
        """Build the WHERE clause of the view query.

        Restricts the budget details to the cost direction.

        :return: SQL WHERE fragment
        :rtype: str
        """
        where_str = """
        WHERE   1 = 1 AND
                b.direction = 'cost'
        """
        return where_str

    def _join(self):
        """Build the JOIN clause of the view query.

        Joins the budget detail table, aliased as ``b``, to its budget.

        :return: SQL JOIN fragment
        :rtype: str
        """
        join_str = """
        JOIN analytic_budget_detail AS b ON a.id = b.budget_id

        """
        return join_str

    def _group_by(self):
        """Build the GROUP BY clause of the view query.

        Groups by budget, company currency, account and analytic
        account so the amounts are summed per combination.

        :return: SQL GROUP BY fragment
        :rtype: str
        """
        group_str = """
        GROUP BY    a.id,
                    a.company_currency_id,
                    b.account_id,
                    a.analytic_account_id
        """
        return group_str

    def init(self):
        """Recreate the SQL view of the cost summary report.

        Drops the view if it exists, then creates it again from the
        query parts built by the ``_select``, ``_from``, ``_join``,
        ``_where`` and ``_group_by`` methods.
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
