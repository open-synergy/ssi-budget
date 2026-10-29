# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class FinancialBudgetDetailSummary(models.Model):
    """Report the budget amount grouped by budget and account.

    SQL view model (``_auto = False``) that sums the amount of the
    ``financial_budget.detail`` lines per budget and per account.
    """

    _name = "financial_budget.detail_summary"
    _description = "Financial Budget Detail Summary"
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
        """Return the ``SELECT`` clause of the report view.

        Selects the budget, the account, and the summed line amount.

        :return: SQL ``SELECT`` fragment
        """
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.budget_id AS budget_id,
            a.account_id AS account_id,
            SUM(a.amount) AS amount
        """
        return select_str

    def _from(self):
        """Return the source table of the report view.

        The data source is the ``financial_budget_detail`` table.

        :return: SQL table fragment placed after ``FROM``
        """
        from_str = """
        financial_budget_detail AS a
        """
        return from_str

    def _where(self):
        """Return the ``WHERE`` clause of the report view.

        No filtering criteria are applied; every detail line is included.

        :return: SQL ``WHERE`` fragment
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Return the ``JOIN`` clauses of the report view.

        Extension point: no table is joined by default.

        :return: SQL ``JOIN`` fragment
        """
        join_str = """
        """
        return join_str

    def _group_by(self):
        """Return the ``GROUP BY`` clause of the report view.

        Groups the detail lines per budget and per account.

        :return: SQL ``GROUP BY`` fragment
        """
        group_str = """
        GROUP BY    a.budget_id,
                    a.account_id
        """
        return group_str

    def init(self):
        """Recreate the SQL view backing this model.

        Drop the view if it exists, then create it again from the
        ``_select``, ``_from``, ``_join``, ``_where`` and ``_group_by``
        fragments.
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
