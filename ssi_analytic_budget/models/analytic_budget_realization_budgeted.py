# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class AnalyticBudgetRealizationBudgeted(models.Model):
    """Report on budgeted amount versus realization per budget detail.

    SQL view model (``_auto = False``) with one row per budget detail
    line, whose ``id`` is the id of the line. Each analytic line of the
    budget and of its descendant analytic accounts is matched to at most
    one line of the same budget: first the line with the same account
    and product, then the line with the same account and no product,
    in both cases when its period holds the date of the analytic line
    or when it has no period. The view is the single source of these
    matching rules; the stored realized amount of the lines reads it.
    """

    _name = "analytic_budget.realization_budgeted"
    _description = "Analytic Budget Budgeted Realization"
    _auto = False
    _order = "budget_id, id"

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
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
        """Build the SELECT clause of the report view.

        Budgeted amount is positive for revenue and negative for cost
        lines. Realized amount follows the direction of the line, so it
        is the sum of the matching analytic lines for revenue and the
        opposite of that sum for cost; it defaults to zero when absent.

        :return: SQL SELECT fragment.
        :rtype: str
        """
        select_str = """
        SELECT
            a.id as id,
            a.budget_id AS budget_id,
            b.analytic_account_id AS analytic_account_id,
            a.account_id AS account_id,
            a.product_id AS product_id,
            a.period_id AS period_id,
            b.company_currency_id,
            CASE
                WHEN a.direction = 'revenue' THEN
                    a.price_subtotal
                WHEN a.direction = 'cost' THEN
                    -1.0 * a.price_subtotal
            END AS amount_budgeted,
            CASE
                WHEN a.direction = 'cost' THEN
                    -1.0 * COALESCE(c.amount, 0.0)
                ELSE
                    COALESCE(c.amount, 0.0)
            END AS amount_realized
        """
        return select_str

    def _from(self):
        """Build the FROM clause of the report view.

        The data source is the budget detail table.

        :return: SQL FROM fragment.
        :rtype: str
        """
        from_str = """
        analytic_budget_detail AS a
        """
        return from_str

    def _where(self):
        """Build the WHERE clause of the report view.

        No filtering criteria are applied.

        :return: SQL WHERE fragment.
        :rtype: str
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Build the JOIN clauses of the report view.

        Joins the budget header and the total of the analytic lines
        matched to each line by the rules in the class docstring.

        :return: SQL JOIN fragment.
        :rtype: str
        """
        join_str = """
        JOIN analytic_budget_budget AS b ON a.budget_id = b.id
        LEFT JOIN (
            SELECT  m.detail_id,
                    SUM(m.amount) AS amount
            FROM (
                SELECT  COALESCE(s1.id, s2.id) AS detail_id,
                        l.amount AS amount
                FROM analytic_budget_budget AS mb
                JOIN account_analytic_account AS mab ON
                    mb.analytic_account_id = mab.id
                JOIN account_analytic_account AS mal ON
                    mal.id = mab.id OR
                    mal.parent_path LIKE mab.parent_path || '%'
                JOIN account_analytic_line AS l ON
                    l.account_id = mal.id AND
                    l.move_id IS NOT NULL
                LEFT JOIN LATERAL (
                    SELECT  d.id
                    FROM analytic_budget_detail AS d
                    LEFT JOIN date_range AS p ON d.period_id = p.id
                    WHERE   d.budget_id = mb.id AND
                            d.account_id = l.general_account_id AND
                            d.product_id = l.product_id AND
                            (
                                d.period_id IS NULL OR
                                (l.date >= p.date_start AND l.date <= p.date_end)
                            )
                    ORDER BY d.id
                    LIMIT 1
                ) AS s1 ON TRUE
                LEFT JOIN LATERAL (
                    SELECT  d.id
                    FROM analytic_budget_detail AS d
                    LEFT JOIN date_range AS p ON d.period_id = p.id
                    WHERE   d.budget_id = mb.id AND
                            d.account_id = l.general_account_id AND
                            d.product_id IS NULL AND
                            (
                                d.period_id IS NULL OR
                                (l.date >= p.date_start AND l.date <= p.date_end)
                            )
                    ORDER BY d.id
                    LIMIT 1
                ) AS s2 ON TRUE
            ) AS m
            WHERE m.detail_id IS NOT NULL
            GROUP BY m.detail_id
        ) AS c ON c.detail_id = a.id
        """
        return join_str

    def _group_by(self):
        """Build the GROUP BY clause of the report view.

        No grouping is applied.

        :return: SQL GROUP BY fragment.
        :rtype: str
        """
        group_str = """
        """
        return group_str

    def init(self):
        """Recreate the SQL view backing this model.

        Drops the existing view and creates it again from the SQL
        fragments built by the ``_select``, ``_from``, ``_join``,
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
