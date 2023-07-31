# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetRealizationBudgeted(models.Model):
    _name = "analytic_budget.realization_budgeted"
    _description = "Analytic Budget Budgeted Realization"
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
    amount_budgeted = fields.Monetary(
        string="Amount Budgeted",
        currency_field="company_currency_id",
    )
    amount_realized = fields.Monetary(
        string="Amount Realized",
        currency_field="company_currency_id",
    )

    def _select(self):
        select_str = """
        SELECT
            a.id as id,
            a.budget_id AS budget_id,
            b.analytic_account_id AS analytic_account_id,
            a.account_id AS account_id,
            a.product_id AS product_id,
            c.date as date,
            b.company_currency_id,
            CASE
                WHEN a.direction = 'revenue' THEN
                    a.price_subtotal
                WHEN a.direction = 'cost' THEN
                    -1.0 * a.price_subtotal
            END AS amount_budgeted,
            COALESCE(c.amount_realized, 0.0) AS amount_realized
        """
        return select_str

    def _from(self):
        from_str = """
        analytic_budget_detail AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN analytic_budget_budget AS b ON a.budget_id = b.id
        RIGHT JOIN analytic_budget_realization AS c ON
            b.analytic_account_id = c.analytic_account_id AND
            a.account_id = c.account_id AND
            COALESCE(a.product_id, 0) = COALESCE(c.product_id, 0)
        """
        return join_str

    def _group_by(self):
        group_str = """
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
