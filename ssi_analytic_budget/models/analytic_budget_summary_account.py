# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetCostSummaryAccount(models.Model):
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
        from_str = """
        analytic_budget_budget AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE   1 = 1 AND
                b.direction = 'cost'
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN analytic_budget_detail AS b ON a.id = b.budget_id

        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY    a.id,
                    a.company_currency_id,
                    b.account_id,
                    a.analytic_account_id
        """
        return group_str

    def init(self):
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
