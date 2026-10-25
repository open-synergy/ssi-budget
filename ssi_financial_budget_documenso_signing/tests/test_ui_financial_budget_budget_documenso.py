# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiFinancialBudgetBudgetDocumenso(HttpSavepointCase):
    """Tour test for the ``financial_budget.budget`` Documenso delta."""

    @classmethod
    def setUpClass(cls):
        """Create one financial budget already Waiting for Approval.

        ``base.user_admin`` is a member of the validator group of the base
        module, so it can open the menu without extra group setup. The
        record is moved to ``confirm`` here in Python, not via UI clicks.

        The budget owner (``user_id``) is set to ``admin`` explicitly:
        ``setUpClass`` runs as SUPERUSER, so the default owner would be
        OdooBot and the internal user record rule would hide the record
        from the tour session.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        budget_type = cls.env["financial_budget.type"].create(
            {"name": "TOUR FBDS TYPE", "code": "TOURFBDST"}
        )
        period_type = cls.env["date.range.type"].create(
            {
                "name": "TOUR FBDS PERIOD TYPE",
                "fiscal_month": True,
                "allow_overlap": True,
            }
        )
        period = cls.env["date.range"].create(
            {
                "name": "TOUR FBDS APPROVE",
                "type_id": period_type.id,
                "date_start": "2041-01-01",
                "date_end": "2041-01-28",
            }
        )
        cls.budget = cls.env["financial_budget.budget"].create(
            {
                "user_id": cls.admin.id,
                "type_id": budget_type.id,
                "period_id": period.id,
            }
        )
        cls.budget.with_context(bypass_policy_check=True).action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/financial_budget_budget/05-approve.md (E2a delta --
        Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_documenso_signing_financial_budget_budget_approve",
            login="admin",
        )
