# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, tools


class FinancialBudgetSummary(models.Model):
    _name = "financial_budget.summary"
    _description = "Financial Budget Summary"
    _auto = False

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="financial_budget.budget",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    amount_planned = fields.Monetary(
        string="Planned Amount",
        currency_field="currency_id",
    )
    amount_realized = fields.Monetary(
        string="Realized Amount",
        currency_field="currency_id",
    )
    amount_diff = fields.Monetary(
        string="Diff. Amount",
        currency_field="currency_id",
    )

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            a.budget_id AS budget_id,
            a.account_id AS account_id,
            d.company_currency_id AS currency_id,
            CASE
                WHEN
                    b.amount IS NOT NULL
                THEN
                    b.amount
                ELSE 0.0 END AS amount_planned,
            CASE
                WHEN
                    c.amount IS NOT NULL
                THEN
                    c.amount
                ELSE 0.0 END AS amount_realized,
            (
            CASE
                WHEN
                    b.amount IS NOT NULL
                THEN
                    b.amount ELSE 0.0 END -
            CASE
                WHEN
                c.amount IS NOT NULL
            THEN
                c.amount ELSE 0.0 END
            ) AS amount_diff
        """
        return select_str

    def _from(self):
        from_str = """
        financial_budget_account AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        LEFT JOIN financial_budget_detail_summary AS b ON  a.budget_id = b.budget_id AND
                                            a.account_id = b.account_id
        LEFT JOIN financial_budget_move_line_summary AS c ON
            a.budget_id = c.budget_id AND
            a.account_id = c.account_id
        JOIN financial_budget_budget AS d ON a.budget_id = d.id
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
