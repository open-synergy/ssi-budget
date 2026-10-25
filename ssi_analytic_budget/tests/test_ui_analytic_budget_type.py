# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAnalyticBudgetType(HttpSavepointCase):
    """UI tour test suite for ``analytic_budget.type``."""

    @classmethod
    def setUpClass(cls):
        """Prepare one budget type per tour starting state.

        Admin holds the configurator group through the module data, so it can
        open the configuration menu.
        """
        super().setUpClass()
        obj_type = cls.env["analytic_budget.type"]
        for name, code in (
            ("TOUR ABT EDIT", "TOURABTE"),
            ("TOUR ABT DELETE", "TOURABTD"),
            ("TOUR ABT ARCHIVE", "TOURABTA"),
        ):
            obj_type.create({"name": name, "code": code})
        # Starting state of the activate tour: an archived record.
        obj_type.create(
            {"name": "TOUR ABT RESTORE", "code": "TOURABTR", "active": False}
        )

        # Accounts picked through the UI on the Revenue and Cost tabs.
        obj_account = cls.env["account.account"]
        obj_account.create(
            {
                "name": "TOUR AB REV ACC",
                "code": "TOURAB1",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        obj_account.create(
            {
                "name": "TOUR AB COST ACC",
                "code": "TOURAB2",
                "user_type_id": cls.env.ref("account.data_account_type_expenses").id,
            }
        )

    def test_create(self):
        """Run the create tour.

        IK: docs/analytic_budget_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_type_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour.

        IK: docs/analytic_budget_type/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_type_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour.

        IK: docs/analytic_budget_type/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_type_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour.

        IK: docs/analytic_budget_type/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_type_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour.

        IK: docs/analytic_budget_type/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_type_activate",
            login="admin",
        )
