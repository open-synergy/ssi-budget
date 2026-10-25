# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAnalyticBudgetBudgetDocumenso(HttpSavepointCase):
    """Tour test for the ``analytic_budget.budget`` Documenso delta."""

    @classmethod
    def setUpClass(cls):
        """Create one analytic budget already Waiting for Approval.

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
        budget_type = cls.env["analytic_budget.type"].create(
            {"name": "TOUR AB DS TYPE", "code": "TOURABDST"}
        )
        analytic_account = cls.env["account.analytic.account"].create(
            {"name": "TOUR AB DS APPROVE"}
        )
        cls.budget = cls.env["analytic_budget.budget"].create(
            {
                "type_id": budget_type.id,
                "analytic_account_id": analytic_account.id,
                "user_id": cls.admin.id,
            }
        )
        cls.budget.with_context(bypass_policy_check=True).action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/analytic_budget_budget/05-approve.md (E2a delta --
        Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_documenso_signing_analytic_budget_budget_approve",
            login="admin",
        )
