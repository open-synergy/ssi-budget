# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class FinancialBudgetMoveLineSummary(models.Model):
    """Report the budgeted amount per budget and account.

    Read-only SQL view (``_auto = False``) that sums the amounts of
    ``financial_budget.move_line`` records grouped by budget and
    account.
    """

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
        """Build the ``SELECT`` clause of the view query.

        Returns a row id derived from the budget and account pair plus
        the budget, the account, the direction and the summed amount of
        the budget move lines.
        Extension point: override to add columns.

        :return: SQL ``SELECT`` fragment as a string
        """
        select_str = """
        SELECT
            (a.budget_id::bigint * 10000000000 + a.account_id::bigint) AS id,
            a.budget_id AS budget_id,
            a.account_id AS account_id,
            a.direction AS direction,
            SUM(a.amount) AS amount
        """
        return select_str

    def _from(self):
        """Build the ``FROM`` clause of the view query.

        The data source is the ``financial_budget_move_line`` table.
        Extension point: override to change the source relation.

        :return: SQL fragment naming the source table as a string
        """
        from_str = """
        financial_budget_move_line AS a
        """
        return from_str

    def _where(self):
        """Build the ``WHERE`` clause of the view query.

        Currently applies no filter, so every budget move line is
        included. Extension point: override to add criteria.

        :return: SQL ``WHERE`` fragment as a string
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Build the ``JOIN`` clauses of the view query.

        Currently empty because the view reads a single table.
        Extension point: override to join additional tables.

        :return: SQL ``JOIN`` fragment as a string
        """
        join_str = """
        """
        return join_str

    def _group_by(self):
        """Build the ``GROUP BY`` clause of the view query.

        Groups the amounts by budget, account and direction.
        Extension point: override together with ``_select``.

        :return: SQL ``GROUP BY`` fragment as a string
        """
        group_str = """
        GROUP BY    a.budget_id,
                    a.account_id,
                    a.direction
        """
        return group_str

    def init(self):
        """Recreate the SQL view backing this model.

        Drops the existing view if any, then creates it again from
        the fragments returned by ``_select``, ``_from``, ``_join``,
        ``_where`` and ``_group_by``.
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
