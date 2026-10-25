# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAnalyticBudgetBudget(HttpSavepointCase):
    """Tour test for the Operating Unit field on ``analytic_budget.budget``.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    """

    @classmethod
    def setUpClass(cls):
        """Grant ``admin`` the multi operating unit group.

        Pre-Condition IK: the Operating Unit field is gated by
        ``groups="operating_unit.group_multi_operating_unit"`` in the
        form view, so without membership the field is never rendered.
        ``admin`` already belongs to the validator group of the base
        module, so the Analytic Budgets menu is visible without a grant.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        operating_unit_partner = cls.env["res.partner"].create(
            {"name": "Tour Analytic Budget OU Partner"}
        )
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Tour Analytic Budget Operating Unit",
                "code": "TABOU",
                "partner_id": operating_unit_partner.id,
            }
        )
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.admin.id)]}
        )
        cls.admin.sudo().write(
            {
                "assigned_operating_unit_ids": [(4, cls.operating_unit.id)],
                "default_operating_unit_id": cls.operating_unit.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``analytic_budget.budget``.

        IK: docs/analytic_budget_budget/01-create.md (E1 delta --
        Additional Fields)
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_operating_unit_analytic_budget_budget_create",
            login="admin",
        )
