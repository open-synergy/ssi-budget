# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestFinancialBudget(YamlTransactionCase):
    """Run the financial budget YAML scenarios."""

    def test_financial_budget(self):
        """Run the financial budget workflow scenarios.

        Covers the full workflow, master data creation and the
        reject transition, all defined in the YAML file.
        """
        self.run_yaml_scenario("test_data_financial_budget.yaml")

    def test_sql_view_ids_are_stable(self):
        """Return identical ids on two consecutive reads of the views.

        Pure Python, trigger P1 (L-01): comparing the id lists of two
        consecutive ``search()`` calls is not expressible with
        ``action: search``, which only saves the result.
        """
        env = self.env
        range_type = env["date.range.type"].create(
            {"name": "STABLE FB RANGE TYPE", "fiscal_month": True}
        )
        period = env["date.range"].create(
            {
                "name": "STABLE FB PERIOD",
                "type_id": range_type.id,
                "date_start": "2024-01-01",
                "date_end": "2024-01-28",
            }
        )
        revenue = env["account.account"].create(
            {
                "name": "STABLE FB REVENUE",
                "code": "STBFBR",
                "user_type_id": env.ref("account.data_account_type_revenue").id,
            }
        )
        balancing = env["account.account"].create(
            {
                "name": "STABLE FB BALANCING",
                "code": "STBFBB",
                "user_type_id": env.ref("account.data_account_type_current_assets").id,
            }
        )
        journal = env["account.journal"].create(
            {"name": "STABLE FB JOURNAL", "code": "STBFB", "type": "general"}
        )
        budget_type = env["financial_budget.type"].create(
            {
                "name": "STABLE FB TYPE",
                "code": "STBFBT",
                "allowed_account_ids": [(6, 0, [revenue.id])],
            }
        )
        budget = env["financial_budget.budget"].create(
            {"type_id": budget_type.id, "period_id": period.id}
        )
        env["financial_budget.detail"].create(
            {
                "budget_id": budget.id,
                "account_id": revenue.id,
                "direction": "revenue",
                "amount": 100.0,
            }
        )
        move = env["account.move"].create(
            {
                "journal_id": journal.id,
                "date": "2024-01-10",
                "line_ids": [
                    (0, 0, {"account_id": revenue.id, "debit": 0.0, "credit": 50.0}),
                    (0, 0, {"account_id": balancing.id, "debit": 50.0, "credit": 0.0}),
                ],
            }
        )
        move.action_post()
        criteria = [("budget_id", "=", budget.id)]
        for model in (
            "financial_budget.move_line",
            "financial_budget.summary",
            "financial_budget.account",
            "financial_budget.detail_summary",
            "financial_budget.move_line_summary",
        ):
            first = env[model].search(criteria, order="id").ids
            second = env[model].search(criteria, order="id").ids
            self.assertTrue(first, model)
            self.assertEqual(first, second, model)
