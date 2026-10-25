# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAnalyticBudgetBudget(HttpSavepointCase):
    """Tour test for the ``analytic_budget.budget`` work log delta."""

    def test_create(self):
        """Run the create tour for the work log delta.

        IK: docs/analytic_budget_budget/01-create.md (delta -- Additional
        Fields)
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_work_log_analytic_budget_budget_create",
            login="admin",
        )
