# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, tools


class FinancialBudgetMoveLine(models.Model):
    _name = "financial_budget.move_line"
    _description = "Financial Budget Move Line"
    _auto = False

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="financial_budget.budget",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    move_id = fields.Many2one(
        string="# Move",
        comodel_name="account.move",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
    )
    amount = fields.Float(
        string="Amount",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.id AS budget_id,
            e.account_id AS account_id,
            e.move_id AS move_id,
            a.period_id AS period_id,
            e.journal_id AS journal_id,
            CASE
                WHEN
                    g.internal_type = 'asset' OR g.internal_type = 'expense'
                THEN
                    (e.debit - e.credit)
                ELSE
                    (e.credit - e.debit)
            END AS amount
        """
        return select_str

    def _from(self):
        from_str = """
        financial_budget_budget AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1 AND
        f.state = 'posted'
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN financial_budget_type AS b ON a.type_id = b.id
        JOIN rel_financial_budget_type_2_account AS c ON b.id = c.type_id
        JOIN date_range AS d ON a.period_id = d.id
        JOIN account_move_line AS e ON  d.date_start >= e.date AND
                                        d.date_end <= e.date AND
                                        c.account_id = e.account_id
        JOIN account_move AS f ON e.move_id = f.id
        JOIN account_account AS g ON e.account_id = g.id
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
