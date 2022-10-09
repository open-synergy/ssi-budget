# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class FinancialBudgetBudget(models.Model):
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
        store=True,
    )
    date_end = fields.Date(
        string="Date End",
        related="period_id.date_end",
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

    def _compute_amount(self):
        for record in self:
            amount_planned = amount_realized = amount_diff = 0.0
            for detail in record.detail_ids:
                amount_planned += detail.price_subtotal

            for ml in record.move_line_ids:
                amount_realized += ml.amount

            amount_diff = amount_planned - amount_realized

            record.amount_planned = amount_planned
            record.amount_realized = amount_realized
            record.amount_diff = amount_diff

    amount_planned = fields.Monetary(
        string="Planned Amount",
        compute="_compute_amount",
        store=False,
        currency_field="company_currency_id",
    )
    amount_realized = fields.Monetary(
        string="Realized Amount",
        compute="_compute_amount",
        store=False,
        currency_field="company_currency_id",
    )
    amount_diff = fields.Monetary(
        string="Diff Amount",
        compute="_compute_amount",
        store=False,
        currency_field="company_currency_id",
    )
    state = fields.Selection(
        string="State",
        default="draft",
        required=True,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancel"),
            ("terminate", "Terminate"),
        ],
    )

    @api.model
    def _get_policy_field(self):
        res = super(FinancialBudgetBudget, self)._get_policy_field()
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
