# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class FinancialBudgetSummary(models.Model):
    """SQL view reporting planned vs realized amount per budget account.

    Each row is one account of one financial budget, showing the planned
    amount, the realized amount and the difference between them.
    """

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
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("revenue", "Revenue"),
            ("cost", "Cost"),
        ],
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
        """Build the SELECT clause of the report view.

        Planned and realized amounts default to zero when the account
        has no matching detail or move line summary. The direction is the
        direction of the budget detail of the account, or revenue for
        income accounts and cost for the others when there is no detail.
        The realized amount is signed by that direction.

        :return: SQL SELECT fragment
        :rtype: str
        """
        select_str = """
        SELECT
            a.id AS id,
            a.budget_id AS budget_id,
            a.account_id AS account_id,
            d.company_currency_id AS currency_id,
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
        """Build the FROM clause, using budget accounts as data source.

        :return: SQL FROM fragment
        :rtype: str
        """
        from_str = """
        financial_budget_account AS a
        """
        return from_str

    def _where(self):
        """Build the WHERE clause, which applies no extra criteria.

        :return: SQL WHERE fragment
        :rtype: str
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Build the JOIN clauses for amounts and budget currency.

        Planned and realized summaries are joined by budget and account,
        the budget provides the company currency and the account its
        group, used to derive the direction when there is no detail.

        :return: SQL JOIN fragment
        :rtype: str
        """
        join_str = """
        LEFT JOIN financial_budget_detail_summary AS b ON  a.budget_id = b.budget_id AND
                                            a.account_id = b.account_id
        LEFT JOIN financial_budget_move_line_summary AS c ON
            a.budget_id = c.budget_id AND
            a.account_id = c.account_id
        JOIN financial_budget_budget AS d ON a.budget_id = d.id
        JOIN account_account AS g ON a.account_id = g.id
        LEFT JOIN (
            SELECT budget_id, account_id, MIN(direction) AS direction
            FROM financial_budget_detail
            GROUP BY budget_id, account_id
        ) AS dd ON dd.budget_id = a.budget_id AND dd.account_id = a.account_id
        """
        return join_str

    def _group_by(self):
        """Build the GROUP BY clause, which is empty for this view.

        :return: SQL GROUP BY fragment
        :rtype: str
        """
        group_str = """
        """
        return group_str

    def init(self):
        """Drop and recreate the SQL view from the query fragments."""
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
