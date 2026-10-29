# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class FinancialBudgetAccount(models.Model):
    """SQL view of the accounts allowed for each budget.

    Report model (``_auto = False``) backed by a database view. Each
    row links a budget to one account permitted by the budget type.
    """

    _name = "financial_budget.account"
    _description = "Budget Account"
    _auto = False

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="financial_budget.budget",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )

    def _select(self):
        """Return the SELECT clause of the view query.

        Builds one row per budget and account pair; the record id is
        derived from the pair, so it is stable between queries.

        :return: SQL ``SELECT`` fragment
        """
        select_str = """
        SELECT
            (a.id::bigint * 10000000000 + c.account_id::bigint) AS id,
            a.id AS budget_id,
            c.account_id AS account_id
        """
        return select_str

    def _from(self):
        """Return the FROM clause of the view query.

        The source of data is the budget table.

        :return: SQL table expression
        """
        from_str = """
        financial_budget_budget AS a
        """
        return from_str

    def _where(self):
        """Return the WHERE clause of the view query.

        No filtering criteria are applied; every budget is included.

        :return: SQL ``WHERE`` fragment
        """
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        """Return the JOIN clauses of the view query.

        Joins each budget to its type and to the accounts allowed
        for that type.

        :return: SQL ``JOIN`` fragment
        """
        join_str = """
        JOIN financial_budget_type AS b ON a.type_id = b.id
        JOIN rel_financial_budget_type_2_account AS c ON b.id = c.type_id
        """
        return join_str

    def _group_by(self):
        """Return the GROUP BY clause of the view query.

        No grouping is applied; the fragment is empty.

        :return: SQL ``GROUP BY`` fragment
        """
        group_str = """
        """
        return group_str

    def init(self):
        """Recreate the database view for this model.

        Drops the view if it exists, then creates it from the
        fragments returned by the ``_select``, ``_from``, ``_join``,
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
