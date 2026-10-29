# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAnalyticBudgetBudget(HttpSavepointCase):
    """UI tour test suite for ``analytic_budget.budget``."""

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
        cls.budget_type = cls.env["analytic_budget.type"].create(
            {"name": "TOUR AB TYPE 1", "code": "TOURABT1"}
        )
        # Second type, so the edit tour really changes the value.
        cls.env["analytic_budget.type"].create(
            {"name": "TOUR AB TYPE 2", "code": "TOURABT2"}
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {"name": "TOUR AB CANCEL REASON", "code": "TOURABCXL", "global_use": True}
        )
        cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR AB TERMINATE REASON",
                "code": "TOURABTRM",
                "global_use": True,
            }
        )

        # Analytic accounts picked through the UI by the create/edit tours.
        cls._prepare_analytic_account("TOUR AB CREATE")
        cls._prepare_analytic_account("TOUR AB NEWACC")

        # Records prepared in the starting state each tour begins from.
        cls._prepare_budget("TOUR AB EDIT")
        cls._prepare_budget("TOUR AB DELETE")
        cls._prepare_budget("TOUR AB CONFIRM")
        cls._prepare_budget("TOUR AB CANCEL")
        for name in ("TOUR AB APPROVE", "TOUR AB REJECT"):
            cls._prepare_budget(name).with_context(
                bypass_policy_check=True
            ).action_confirm()
        for name in ("TOUR AB DONE", "TOUR AB TERMINATE"):
            cls._prepare_open_budget(name)
        cls._prepare_budget("TOUR AB RESTART").with_context(
            bypass_policy_check=True
        ).action_cancel()

        # Recompute tour: a budget with one realized analytic line whose
        # stored realization is made stale on purpose.
        cls._prepare_recompute_budget("TOUR AB RECOMPUTE")

        # Restart-approval tour: the button is granted for any confirmed
        # record (the policy has no additional condition), so a plain
        # confirmed record is enough.
        cls._prepare_budget("TOUR AB RELOAD APPROVAL").with_context(
            bypass_policy_check=True
        ).action_confirm()

    @classmethod
    def _prepare_analytic_account(cls, name):
        """Create an analytic account whose name is the marker for a tour.

        :param name: analytic account name used by the tour to find the record
        :return: the new ``account.analytic.account`` record
        """
        return cls.env["account.analytic.account"].create({"name": name})

    @classmethod
    def _prepare_budget(cls, name):
        """Create a draft budget on a uniquely named analytic account.

        :param name: analytic account name used by the tour to find the record
        :return: the new ``analytic_budget.budget`` record
        """
        account = cls._prepare_analytic_account(name)
        return cls.env["analytic_budget.budget"].create(
            {
                "user_id": cls.admin.id,
                "type_id": cls.budget_type.id,
                "analytic_account_id": account.id,
            }
        )

    @classmethod
    def _prepare_open_budget(cls, name):
        """Create a budget and walk it through confirm and approve to open.

        The policy cache is invalidated between the two transitions, because
        ``_compute_policy`` caches every ``*_ok`` flag while still in draft.

        :param name: analytic account name used by the tour to find the record
        :return: the ``analytic_budget.budget`` record in state ``open``
        """
        budget = cls._prepare_budget(name)
        budget.with_context(bypass_policy_check=True).action_confirm()
        cls.env["analytic_budget.budget"].invalidate_cache()
        budget.with_user(cls.admin).action_approve_approval()
        return budget

    @classmethod
    def _prepare_recompute_budget(cls, name):
        """Create a draft budget with a realized line and stale totals.

        A posted entry puts 100.0 of revenue on the analytic account of
        the budget. The stored realization is then reset to zero in the
        database, so only the Recompute Realization action can bring the
        value back.

        :param name: analytic account name used by the tour to find the record
        :return: the new ``analytic_budget.budget`` record
        """
        account_type = cls.env.ref("account.data_account_type_expenses")
        revenue_account = cls.env["account.account"].create(
            {
                "name": "TOUR AB RC REVENUE",
                "code": "TOURABRC1",
                "user_type_id": account_type.id,
            }
        )
        counterpart_account = cls.env["account.account"].create(
            {
                "name": "TOUR AB RC COUNTER",
                "code": "TOURABRC2",
                "user_type_id": account_type.id,
            }
        )
        journal = cls.env["account.journal"].create(
            {"name": "TOUR AB RC JOURNAL", "code": "TOURABRC", "type": "general"}
        )
        account = cls._prepare_analytic_account(name)
        budget = cls.env["analytic_budget.budget"].create(
            {
                "user_id": cls.admin.id,
                "type_id": cls.budget_type.id,
                "analytic_account_id": account.id,
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "TOUR AB RC DETAIL",
                            "direction": "revenue",
                            "account_id": revenue_account.id,
                            "price_unit": 1000.0,
                            "uom_quantity": 1.0,
                        },
                    )
                ],
            }
        )
        move = cls.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": journal.id,
                "date": "2027-01-15",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Debit",
                            "account_id": counterpart_account.id,
                            "debit": 100.0,
                            "credit": 0.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Credit",
                            "account_id": revenue_account.id,
                            "debit": 0.0,
                            "credit": 100.0,
                            "analytic_account_id": account.id,
                        },
                    ),
                ],
            }
        )
        move.action_post()
        cls.env["analytic_budget.budget"].flush()
        cls.env.cr.execute(
            "UPDATE analytic_budget_budget SET amount_revenue_realization = 0.0 "
            "WHERE id = %s",
            (budget.id,),
        )
        cls.env.cr.execute(
            "UPDATE analytic_budget_detail SET amount_realized = 0.0 "
            "WHERE budget_id = %s",
            (budget.id,),
        )
        cls.env["analytic_budget.budget"].invalidate_cache()
        cls.env["analytic_budget.detail"].invalidate_cache()
        return budget

    def test_create(self):
        """Run the create tour.

        IK: docs/analytic_budget_budget/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour.

        IK: docs/analytic_budget_budget/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour.

        IK: docs/analytic_budget_budget/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour.

        IK: docs/analytic_budget_budget/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour.

        IK: docs/analytic_budget_budget/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour.

        IK: docs/analytic_budget_budget/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour.

        IK: docs/analytic_budget_budget/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour.

        IK: docs/analytic_budget_budget/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_cancel",
            login="admin",
        )

    def test_terminate(self):
        """Run the terminate tour.

        IK: docs/analytic_budget_budget/11-terminate.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_terminate",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour.

        IK: docs/analytic_budget_budget/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour.

        IK: docs/analytic_budget_budget/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_restart_approval",
            login="admin",
        )

    def test_recompute_realization(self):
        """Run the recompute realization tour.

        IK: docs/analytic_budget_budget/15-recompute-realization.md
        """
        self.start_tour(
            "/web",
            "ssi_analytic_budget_analytic_budget_budget_recompute_realization",
            login="admin",
        )
