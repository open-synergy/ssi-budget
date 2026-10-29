# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class FinancialBudgetMoveLine(models.Model):
    """Report journal entry lines that count toward a budget.

    SQL view (``_auto = False``) listing, for every budget, the posted
    journal items of the accounts mapped to its budget type, signed as
    budget amounts.
    """

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
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("revenue", "Revenue"),
            ("cost", "Cost"),
        ],
    )
    amount = fields.Float(
        string="Amount",
    )

    def _select(self):
        """Build the SELECT clause of the view.

        The effective direction is the direction of the budget detail of
        the same account, or revenue for income accounts and cost for the
        others when the account has no detail. The amount is credit minus
        debit for revenue and debit minus credit for cost. The id is
        derived from the budget and the journal item, so it is stable.

        :return: SQL SELECT fragment
        :rtype: str
        """
        select_str = """
        SELECT
            (a.id::bigint * 10000000000 + e.id::bigint) AS id,
            a.id AS budget_id,
            e.account_id AS account_id,
            e.move_id AS move_id,
            a.period_id AS period_id,
            e.journal_id AS journal_id,
            COALESCE(
                dd.direction,
                CASE
                    WHEN g.internal_group = 'income'
                    THEN 'revenue'
                    ELSE 'cost'
                END
            ) AS direction,
            CASE
                WHEN
                    COALESCE(
                        dd.direction,
                        CASE
                            WHEN g.internal_group = 'income'
                            THEN 'revenue'
                            ELSE 'cost'
                        END
                    ) = 'revenue'
                THEN
                    (e.credit - e.debit)
                ELSE
                    (e.debit - e.credit)
            END AS amount
        """
        return select_str

    def _from(self):
        """Build the FROM clause of the view.

        Budgets are the driving table of the query.

        :return: SQL table expression
        :rtype: str
        """
        from_str = """
        financial_budget_budget AS a
        """
        return from_str

    def _where(self):
        """Build the WHERE clause of the view.

        Keeps only journal items belonging to posted journal entries.

        :return: SQL WHERE fragment
        :rtype: str
        """
        where_str = """
        WHERE 1 = 1 AND
        f.state = 'posted'
        """
        return where_str

    def _join(self):
        """Build the JOIN clauses of the view.

        Links each budget to its type, the accounts mapped to that type,
        its period, and the journal items of the budget company dated
        within that period. Budget details are joined aggregated per
        budget and account so that a journal item is never duplicated.

        :return: SQL JOIN fragment
        :rtype: str
        """
        join_str = """
        JOIN financial_budget_type AS b ON a.type_id = b.id
        JOIN rel_financial_budget_type_2_account AS c ON b.id = c.type_id
        JOIN date_range AS d ON a.period_id = d.id
        JOIN account_move_line AS e ON  e.date >= d.date_start AND
                                        e.date <= d.date_end AND
                                        e.company_id = a.company_id AND
                                        c.account_id = e.account_id
        JOIN account_move AS f ON e.move_id = f.id
        JOIN account_account AS g ON e.account_id = g.id
        JOIN account_account_type AS h ON g.user_type_id = h.id
        LEFT JOIN (
            SELECT budget_id, account_id, MIN(direction) AS direction
            FROM financial_budget_detail
            GROUP BY budget_id, account_id
        ) AS dd ON dd.budget_id = a.id AND dd.account_id = e.account_id
        """
        return join_str

    def _group_by(self):
        """Build the GROUP BY clause of the view.

        The view is not aggregated, so the fragment is empty.

        :return: SQL GROUP BY fragment
        :rtype: str
        """
        group_str = """
        """
        return group_str

    def init(self):
        """Recreate the SQL view when the module is installed or updated.

        Drops the existing view, then creates it again from the select,
        from, join, where and group by fragments.
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
