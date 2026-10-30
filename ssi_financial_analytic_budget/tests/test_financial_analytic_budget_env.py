# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestFinancialAnalyticBudgetEnv(YamlTransactionCase):
    """Check the environment is empty after a ceiling error."""

    def setUp(self):
        """Create an analytic budget above its financial ceiling.

        The budget is created without the opt-in context, so the
        ceiling check is skipped and the over-ceiling line exists.
        """
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")
        account = env["account.account"].create(
            {
                "name": "FAB 10 Account X",
                "code": "FAB10X",
                "user_type_id": env.ref("account.data_account_type_expenses").id,
            }
        )
        fin_type = env["financial_budget.type"].create(
            {
                "name": "FAB 10 Financial Type",
                "code": "FABF10",
                "allowed_account_ids": [(6, 0, [account.id])],
            }
        )
        self.an_type = env["analytic_budget.type"].create(
            {"name": "FAB 10 Analytic Type", "code": "FABA10"}
        )
        self.an_acc = env["account.analytic.account"].create(
            {"name": "FAB 10 Analytic Account"}
        )
        yr_type = env["date.range.type"].create({"name": "FAB 10 Yearly"})
        env.company.financial_budget_yearly_range_type_id = yr_type.id
        year = env["date.range"].create(
            {
                "name": "FAB 10 Year",
                "type_id": yr_type.id,
                "date_start": "2050-01-01",
                "date_end": "2050-12-31",
            }
        )
        an_drt = env["date.range.type"].create(
            {"name": "FAB 10 Analytic Periods", "allow_overlap": True}
        )
        jan = env["date.range"].create(
            {
                "name": "FAB 10 jan",
                "type_id": an_drt.id,
                "date_start": "2050-01-01",
                "date_end": "2050-01-31",
            }
        )
        env["financial_budget.budget"].with_user(admin).create(
            {
                "type_id": fin_type.id,
                "periodicity": "yearly",
                "period_id": year.id,
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": account.id,
                            "direction": "cost",
                            "amount": 1000000.0,
                        },
                    )
                ],
            }
        )
        self.budget = (
            env["analytic_budget.budget"]
            .with_user(admin)
            .create(
                {
                    "type_id": self.an_type.id,
                    "analytic_account_id": self.an_acc.id,
                    "detail_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "Jan",
                                "direction": "cost",
                                "account_id": account.id,
                                "price_unit": 5000000.0,
                                "uom_quantity": 1.0,
                                "period_id": jan.id,
                            },
                        )
                    ],
                }
            )
        )
        self.env["analytic_budget.detail"].flush()
        self.env.cache.invalidate()

    def test_write_over_ceiling_clears_pending_environment(self):
        """Clear pending writes after a ceiling error on write.

        Pure Python -- trigger P13 (L-26: YAML's ``expect_error`` runs
        the call in a savepoint that flushes on entry and empties the
        environment on failure, so it cannot tell whether the code
        under test cleared the environment itself). The write runs
        here with no savepoint around it.
        """
        detail = self.budget.detail_ids
        with self.assertRaises(ValidationError) as caught:
            detail.with_context(test_financial_analytic_budget=True).write(
                {"price_unit": 5000000.0}
            )
        self.assertIn("exceeds the financial budget amount", str(caught.exception))
        self.assertFalse(self.env.all.towrite)
        self.assertFalse(self.env.all.tocompute)

    def test_confirm_over_ceiling_clears_pending_environment(self):
        """Clear pending writes after a ceiling error on confirm.

        Pure Python -- trigger P13 (L-26: same reason as the write
        test). ``action_confirm`` runs the ceiling hook on the
        ``pre_confirm_check`` slot, with no savepoint around it.
        """
        budget = self.budget.with_context(
            test_financial_analytic_budget=True,
            bypass_policy_check=True,
        )
        with self.assertRaises(ValidationError) as caught:
            budget.action_confirm()
        self.assertIn("exceeds the financial budget amount", str(caught.exception))
        self.assertFalse(self.env.all.towrite)
        self.assertFalse(self.env.all.tocompute)
