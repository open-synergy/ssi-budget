# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class FinancialBudgetBudget(models.Model):
    """Financial budget document for one fiscal period.

    Plans revenue and cost amounts per account through its detail
    lines and compares them with the realized journal items. The
    document follows the confirm, approval, open, done, cancel and
    terminate workflow.
    """

    _name = "financial_budget.budget"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.company_currency",
    ]
    _description = "Financial Budget"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_open_policy_fields = True
    _automatically_insert_open_button = True

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "open_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    type_id = fields.Many2one(
        string="Financial Budget Type",
        comodel_name="financial_budget.type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        required=True,
        readonly=True,
        domain=[
            ("type_id.fiscal_month", "=", True),
        ],
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Date Start",
        related="period_id.date_start",
        compute_sudo=True,
        store=True,
    )
    date_end = fields.Date(
        string="Date End",
        related="period_id.date_end",
        compute_sudo=True,
        store=True,
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="financial_budget.detail",
        inverse_name="budget_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_account_ids = fields.One2many(
        string="Detail Accounts",
        comodel_name="financial_budget.account",
        inverse_name="budget_id",
        readonly=True,
    )
    detail_summary_ids = fields.One2many(
        string="Detail Summary",
        comodel_name="financial_budget.detail_summary",
        inverse_name="budget_id",
        readonly=True,
    )
    move_line_ids = fields.One2many(
        string="Move Lines",
        comodel_name="financial_budget.move_line",
        inverse_name="budget_id",
        readonly=True,
    )
    move_line_summary_ids = fields.One2many(
        string="Move Line Summary",
        comodel_name="financial_budget.move_line_summary",
        inverse_name="budget_id",
        readonly=True,
    )
    summary_ids = fields.One2many(
        string="Budget Summary",
        comodel_name="financial_budget.summary",
        inverse_name="budget_id",
        readonly=True,
    )

    @api.depends(
        "detail_ids.amount",
        "detail_ids.account_id",
        "detail_ids.direction",
    )
    def _compute_amount(self):
        """Compute the planned, realized and difference amounts.

        Reads the live ``financial_budget.summary`` view once, grouped by
        budget and direction. Revenue and cost are exposed separately and
        the plain amounts are net: revenue minus cost. The difference of
        each pair is planned minus realized. The realization is live and
        does not depend on the state of the budget.
        """
        fields_amount = ["amount_planned", "amount_realized"]
        data = {}
        budget_ids = [rec.id for rec in self if isinstance(rec.id, int)]
        if budget_ids:
            groups = (
                self.env["financial_budget.summary"]
                .sudo()
                .read_group(
                    [("budget_id", "in", budget_ids)],
                    fields_amount,
                    ["budget_id", "direction"],
                    lazy=False,
                )
            )
            for group in groups:
                key = (group["budget_id"][0], group["direction"])
                data[key] = (group["amount_planned"], group["amount_realized"])
        for record in self:
            planned_revenue, realized_revenue = data.get((record.id, "revenue"), (0, 0))
            planned_cost, realized_cost = data.get((record.id, "cost"), (0, 0))
            planned = planned_revenue - planned_cost
            realized = realized_revenue - realized_cost
            values = {
                "amount_planned_revenue": planned_revenue,
                "amount_realized_revenue": realized_revenue,
                "amount_diff_revenue": planned_revenue - realized_revenue,
                "amount_planned_cost": planned_cost,
                "amount_realized_cost": realized_cost,
                "amount_diff_cost": planned_cost - realized_cost,
                "amount_planned": planned,
                "amount_realized": realized,
                "amount_diff": planned - realized,
            }
            record.update(values)

    amount_planned = fields.Monetary(
        string="Planned Amount",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Net planned amount: planned revenue minus planned cost.",
    )
    amount_realized = fields.Monetary(
        string="Realized Amount",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Net realized amount: realized revenue minus realized cost.",
    )
    amount_diff = fields.Monetary(
        string="Diff Amount",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Net planned amount minus net realized amount.",
    )
    amount_planned_revenue = fields.Monetary(
        string="Planned Revenue",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Sum of the planned amount of revenue accounts.",
    )
    amount_realized_revenue = fields.Monetary(
        string="Realized Revenue",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Posted journal items of revenue accounts in the period.",
    )
    amount_diff_revenue = fields.Monetary(
        string="Diff Revenue",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Planned revenue minus realized revenue.",
    )
    amount_planned_cost = fields.Monetary(
        string="Planned Cost",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Sum of the planned amount of cost accounts.",
    )
    amount_realized_cost = fields.Monetary(
        string="Realized Cost",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Posted journal items of cost accounts in the period.",
    )
    amount_diff_cost = fields.Monetary(
        string="Diff Cost",
        compute="_compute_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Planned cost minus realized cost.",
    )
    state = fields.Selection(
        string="State",
        default="draft",
        required=True,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("reject", "Rejected"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancel"),
            ("terminate", "Terminate"),
        ],
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "open_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res
