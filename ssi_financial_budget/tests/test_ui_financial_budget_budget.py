# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiFinancialBudgetBudget(HttpSavepointCase):
    """UI tour test suite for ``financial_budget.budget``."""

    @classmethod
    def setUpClass(cls):
        """Prepare the master data and one budget per tour starting state.

        The validator group is granted to ``base.user_admin`` by the module
        data, so admin can open the menu, act as the approver, cancel,
        terminate and restart.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition master data, not the focus of the tours.
        cls.budget_type = cls.env["financial_budget.type"].create(
            {"name": "TOUR FB TYPE 1", "code": "TOURFBT1"}
        )
        # Second type, so the edit tour really changes the value.
        cls.env["financial_budget.type"].create(
            {"name": "TOUR FB TYPE 2", "code": "TOURFBT2"}
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {"name": "TOUR FB CANCEL REASON", "code": "TOURFBCXL", "global_use": True}
        )
        cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR FB TERMINATE REASON",
                "code": "TOURFBTRM",
                "global_use": True,
            }
        )

        # Fiscal month type of the periods; the periods of the tours never
        # overlap in the same month, but overlap is allowed anyway.
        cls.period_type = cls.env["date.range.type"].create(
            {
                "name": "TOUR FB PERIOD TYPE",
                "fiscal_month": True,
                "allow_overlap": True,
            }
        )
        cls._period_index = 0

        # Period picked through the UI by the create tour.
        cls._prepare_period("TOUR FB CREATE")

        # Records prepared in the starting state each tour begins from.
        cls._prepare_budget("TOUR FB EDIT")
        cls._prepare_budget("TOUR FB DELETE")
        cls._prepare_budget("TOUR FB CONFIRM")
        cls._prepare_budget("TOUR FB CANCEL")
        for name in ("TOUR FB APPROVE", "TOUR FB REJECT"):
            cls._prepare_budget(name).with_context(
                bypass_policy_check=True
            ).action_confirm()
        for name in ("TOUR FB DONE", "TOUR FB TERMINATE"):
            cls._prepare_open_budget(name)
        cls._prepare_budget("TOUR FB RESTART").with_context(
            bypass_policy_check=True
        ).action_cancel()

        # Restart-approval tour: the button is granted for any confirmed
        # record (the policy has no additional condition), so a plain
        # confirmed record is enough.
        cls._prepare_budget("TOUR FB RELOAD APPROVAL").with_context(
            bypass_policy_check=True
        ).action_confirm()

    @classmethod
    def _prepare_period(cls, name):
        """Create a fiscal month period whose name is the marker for a tour.

        :param name: period name used by the tour to find the record
        :return: the new ``date.range`` record
        """
        cls._period_index += 1
        month = (cls._period_index - 1) % 12 + 1
        year = 2040 + (cls._period_index - 1) // 12
        return cls.env["date.range"].create(
            {
                "name": name,
                "type_id": cls.period_type.id,
                "date_start": "%04d-%02d-01" % (year, month),
                "date_end": "%04d-%02d-28" % (year, month),
            }
        )

    @classmethod
    def _prepare_budget(cls, name):
        """Create a draft budget on a uniquely named period.

        :param name: period name used by the tour to find the record
        :return: the new ``financial_budget.budget`` record
        """
        period = cls._prepare_period(name)
        return cls.env["financial_budget.budget"].create(
            {
                "user_id": cls.admin.id,
                "type_id": cls.budget_type.id,
                "period_id": period.id,
            }
        )

    @classmethod
    def _prepare_open_budget(cls, name):
        """Create a budget and walk it through confirm and approve to open.

        The policy cache is invalidated between the two transitions, because
        ``_compute_policy`` caches every ``*_ok`` flag while still in draft.

        :param name: period name used by the tour to find the record
        :return: the ``financial_budget.budget`` record in state ``open``
        """
        budget = cls._prepare_budget(name)
        budget.with_context(bypass_policy_check=True).action_confirm()
        cls.env["financial_budget.budget"].invalidate_cache()
        budget.with_user(cls.admin).action_approve_approval()
        return budget

    def test_create(self):
        """Run the create tour.

        IK: docs/financial_budget_budget/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour.

        IK: docs/financial_budget_budget/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour.

        IK: docs/financial_budget_budget/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour.

        IK: docs/financial_budget_budget/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour.

        IK: docs/financial_budget_budget/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour.

        IK: docs/financial_budget_budget/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour.

        IK: docs/financial_budget_budget/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour.

        IK: docs/financial_budget_budget/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_cancel",
            login="admin",
        )

    def test_terminate(self):
        """Run the terminate tour.

        IK: docs/financial_budget_budget/11-terminate.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_terminate",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour.

        IK: docs/financial_budget_budget/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour.

        IK: docs/financial_budget_budget/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_financial_budget_financial_budget_budget_restart_approval",
            login="admin",
        )
