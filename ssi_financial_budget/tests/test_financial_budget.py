# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestFinancialBudget(YamlTransactionCase):
    """Run the financial budget YAML scenarios."""

    def test_financial_budget(self):
        """Run the financial budget workflow scenarios.

        Covers the full workflow, master data creation and the
        reject transition, all defined in the YAML file.
        """
        self.run_yaml_scenario("test_data_financial_budget.yaml")

    def test_financial_budget_yearly(self):
        """Run the yearly budget and monthly breakdown scenarios.

        Covers periodicity, parent limits, guards, allocation amounts,
        and the Create Monthly Budgets action.
        """
        self.run_yaml_scenario("test_data_financial_budget_yearly.yaml")

    def test_create_monthly_budgets_remainder(self):
        """Give the rounding remainder to the last monthly budget.

        Pure Python, trigger P2 (L-04): the amounts are floats and the
        YAML ``equals`` operator compares them bit-exact without any
        tolerance.
        """
        env = self.env(user=self.env.ref("base.user_admin"))
        company = env.user.company_id
        fiscal_type = env["date.range.type"].create(
            {"name": "REM FB FISCAL", "fiscal_month": True}
        )
        yearly_type = env["date.range.type"].create({"name": "REM FB YEARLY"})
        company.sudo().financial_budget_yearly_range_type_id = yearly_type
        year = env["date.range"].create(
            {
                "name": "REM FB YEAR",
                "type_id": yearly_type.id,
                "date_start": "2041-01-01",
                "date_end": "2041-12-31",
            }
        )
        for month in range(1, 13):
            env["date.range"].create(
                {
                    "name": "REM FB M%02d" % month,
                    "type_id": fiscal_type.id,
                    "date_start": "2041-%02d-01" % month,
                    "date_end": "2041-%02d-28" % month,
                }
            )
        account = env["account.account"].create(
            {
                "name": "REM FB REVENUE",
                "code": "REMFBR",
                "user_type_id": env.ref("account.data_account_type_revenue").id,
            }
        )
        budget_type = env["financial_budget.type"].create(
            {
                "name": "REM FB TYPE",
                "code": "REMFBT",
                "allowed_account_ids": [(6, 0, [account.id])],
            }
        )
        parent = env["financial_budget.budget"].create(
            {
                "type_id": budget_type.id,
                "periodicity": "yearly",
                "period_id": year.id,
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": account.id,
                            "direction": "revenue",
                            "amount": 1000000.0,
                        },
                    )
                ],
            }
        )
        parent.action_confirm()
        parent.invalidate_cache()
        parent.action_approve_approval()
        self.assertEqual(parent.state, "open")
        parent.action_create_monthly_budgets()
        children = parent.child_ids.sorted("date_start")
        self.assertEqual(len(children), 12)
        currency = parent.company_currency_id
        share = currency.round(1000000.0 / 12)
        amounts = [child.detail_ids.amount for child in children]
        self.assertEqual(amounts[:-1], [share] * 11)
        self.assertEqual(amounts[-1], currency.round(1000000.0 - share * 11))
        self.assertEqual(
            currency.compare_amounts(sum(amounts), 1000000.0),
            0,
        )

    def test_settings_yearly_range_type(self):
        """Save the yearly range type from the Financial Budget settings.

        Pure Python, trigger P12 (L-20): the field lives only in the
        ``ssi_cost_accounting.cost_accounting_settings_view_form`` view,
        which ``action: form`` cannot select because it has no ``view``
        key. Opens the form, sets the field, executes the settings and
        checks the value landed on the company.
        """
        env = self.env
        range_type = env["date.range.type"].create({"name": "SET FB YEARLY"})
        env.company.financial_budget_yearly_range_type_id = False
        form = Form(
            env["res.config.settings"],
            view="ssi_cost_accounting.cost_accounting_settings_view_form",
        )
        form.financial_budget_yearly_range_type_id = range_type
        settings = form.save()
        settings.execute()
        self.assertEqual(
            env.company.financial_budget_yearly_range_type_id,
            range_type,
        )

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
