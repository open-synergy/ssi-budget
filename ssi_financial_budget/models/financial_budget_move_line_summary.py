# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class FinancialBudgetMoveLineSummary(models.Model):
    _name = "financial_budget.move_line_summary"
    _description = "Financiak Budget Move Line Summary"
    _auto = False

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="financial_budget.budget",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    amount = fields.Float(
        string="Amount",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.budget_id AS budget_id,
            a.account_id AS account_id,
            SUM(a.amount) AS amount
        """
        return select_str

    def _from(self):
        from_str = """
        financial_budget_move_line AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY    a.budget_id,
                    a.account_id
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
