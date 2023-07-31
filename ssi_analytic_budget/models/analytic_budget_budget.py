# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class AnalyticBudgetBudget(models.Model):
    _name = "analytic_budget.budget"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.company_currency",
    ]
    _description = "Analytic Budget"

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
        string="Analytic Budget Type",
        comodel_name="analytic_budget.type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_ids = fields.Many2many(
        string="Accounts",
        comodel_name="account.account",
        relation="rel_budget_analytic_2_account",
        column1="budget_id",
        column2="account_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    exclude_account_ids = fields.Many2many(
        string="Exclude Accounts",
        comodel_name="account.account",
        relation="rel_budget_analytic_2_exclude_account",
        column1="budget_id",
        column2="account_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_line_ids = fields.Many2many(
        string="All Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_all_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        store=True,
    )
    exclude_analytic_line_ids = fields.Many2many(
        string="All Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_exclude_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        store=True,
    )
    budgeted_analytic_line_ids = fields.Many2many(
        string="Budgeted Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_budgeted_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        store=True,
    )
    unbudgeted_analytic_line_ids = fields.Many2many(
        string="Unbudgeted Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_unbudgeted_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        store=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="analytic_budget.detail",
        inverse_name="budget_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_revenue_ids = fields.One2many(
        string="Detail Revenue",
        comodel_name="analytic_budget.detail",
        inverse_name="budget_id",
        domain=[
            ("direction", "=", "revenue"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_cost_ids = fields.One2many(
        string="Detail Cost",
        comodel_name="analytic_budget.detail",
        inverse_name="budget_id",
        domain=[
            ("direction", "=", "cost"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    summary_cost_ids = fields.One2many(
        string="Cost Summary",
        comodel_name="analytic_budget.cost_summary_account",
        inverse_name="budget_id",
    )
    realization_ids = fields.One2many(
        string="Realization Lines",
        comodel_name="analytic_budget.realization",
        inverse_name="budget_id",
        readonly=True,
    )
    budgeted_realization_ids = fields.One2many(
        string="Budgeted Realization",
        comodel_name="analytic_budget.realization_budgeted",
        inverse_name="budget_id",
        readonly=True,
    )
    unbudgeted_realization_ids = fields.One2many(
        string="Unbudgeted Realization",
        comodel_name="analytic_budget.realization_unbudgeted",
        inverse_name="budget_id",
        readonly=True,
    )

    @api.depends(
        "analytic_account_id",
        "analytic_account_id.line_ids",
        "analytic_account_id.line_ids.account_id",
        "analytic_account_id.line_ids.general_account_id",
        "analytic_account_id.line_ids.product_id",
        "exclude_account_ids",
        "account_ids",
    )
    def _compute_analytic_line(self):
        AnalyticLine = self.env["account.analytic.line"]
        for record in self:
            record.analytic_line_ids = record.analytic_account_id.line_ids
            criteria = [
                ("account_id", "=", record.analytic_account_id.id),
                ("general_account_id", "in", record.account_ids.ids),
                ("general_account_id", "not in", record.exclude_account_ids.ids),
            ]
            record.budgeted_analytic_line_ids = AnalyticLine.search(criteria)
            criteria = [
                ("account_id", "=", record.analytic_account_id.id),
                ("general_account_id", "not in", record.account_ids.ids),
                ("general_account_id", "not in", record.exclude_account_ids.ids),
            ]
            record.unbudgeted_analytic_line_ids = AnalyticLine.search(criteria)
            criteria = [
                ("account_id", "=", record.analytic_account_id.id),
                ("general_account_id", "in", record.exclude_account_ids.ids),
            ]
            record.exclude_analytic_line_ids = AnalyticLine.search(criteria)

    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
        "analytic_line_ids",
        "analytic_line_ids.amount",
        "analytic_line_ids.unit_amount",
        "analytic_line_ids.account_id",
        "analytic_line_ids.product_uom_id",
        "analytic_line_ids.general_account_id",
        "analytic_line_ids.move_id",
    )
    def _compute_amount(self):
        for document in self:
            amount_planned_revenue = (
                amount_planned_cost
            ) = (
                amount_planned_pl
            ) = (
                amount_unbudgeted_revenue_realization
            ) = (
                amount_budgeted_revenue_realization
            ) = (
                amount_revenue_realization
            ) = (
                amount_unbudgeted_cost_realization
            ) = (
                amount_budgeted_cost_realization
            ) = amount_cost_realization = amount_profit_realization = 0.0

            # Planned Computation
            for detail in document.detail_revenue_ids:
                amount_planned_revenue += detail.price_subtotal

            for detail in document.detail_cost_ids:
                amount_planned_cost += detail.price_subtotal

            amount_planned_pl = amount_planned_revenue - amount_planned_cost

            # Realization Computation
            for detail in document.budgeted_analytic_line_ids.filtered(
                lambda r: r.amount > 0.0
            ):
                amount_budgeted_revenue_realization += detail.amount

            for detail in document.unbudgeted_analytic_line_ids.filtered(
                lambda r: r.amount > 0.0
            ):
                amount_unbudgeted_revenue_realization += detail.amount

            amount_revenue_realization = (
                amount_unbudgeted_revenue_realization
                + amount_budgeted_revenue_realization
            )

            for detail in document.budgeted_analytic_line_ids.filtered(
                lambda r: r.amount < 0.0
            ):
                amount_budgeted_cost_realization += abs(detail.amount)

            for detail in document.unbudgeted_analytic_line_ids.filtered(
                lambda r: r.amount < 0.0
            ):
                amount_unbudgeted_cost_realization += abs(detail.amount)

            amount_cost_realization = (
                amount_unbudgeted_cost_realization + amount_budgeted_cost_realization
            )

            amount_profit_realization = (
                amount_revenue_realization - amount_cost_realization
            )

            document.amount_planned_revenue = amount_planned_revenue
            document.amount_planned_cost = amount_planned_cost
            document.amount_planned_pl = amount_planned_pl
            document.amount_unbudgeted_revenue_realization = (
                amount_unbudgeted_revenue_realization
            )
            document.amount_budgeted_revenue_realization = (
                amount_budgeted_revenue_realization
            )
            document.amount_revenue_realization = amount_revenue_realization
            document.amount_unbudgeted_cost_realization = (
                amount_unbudgeted_cost_realization
            )
            document.amount_budgeted_cost_realization = amount_budgeted_cost_realization
            document.amount_cost_realization = amount_cost_realization
            document.amount_profit_realization = amount_profit_realization

    amount_planned_revenue = fields.Monetary(
        string="Planned Revenue",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_planned_cost = fields.Monetary(
        string="Planned Cost",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_planned_pl = fields.Monetary(
        string="Planned Profit/Loss",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_unbudgeted_revenue_realization = fields.Monetary(
        string="Unbudgeted Revenue Realization",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_budgeted_revenue_realization = fields.Monetary(
        string="Budgeted Revenue Realization",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_revenue_realization = fields.Monetary(
        string="Revenue Realization",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_unbudgeted_cost_realization = fields.Monetary(
        string="Unbudgeted Cost Realization",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_budgeted_cost_realization = fields.Monetary(
        string="Budgeted Cost Realization",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_cost_realization = fields.Monetary(
        string="Cost Realization",
        compute="_compute_amount",
        store=True,
        currency_field="company_currency_id",
    )
    amount_profit_realization = fields.Monetary(
        string="Profit/Loss Realization",
        compute="_compute_amount",
        store=True,
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
        res = super(AnalyticBudgetBudget, self)._get_policy_field()
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

    @api.onchange(
        "type_id",
    )
    def onchange_exclude_account_ids(self):
        self.exclude_account_ids = False
        if self.type_id:
            self.exclude_account_ids = self.type_id.exclude_account_ids

    @api.onchange(
        "type_id",
    )
    def onchange_account_ids(self):
        self.account_ids = False
        if self.type_id:
            self.account_ids = (
                self.type_id.all_allowed_revenue_account_ids
                + self.type_id.all_allowed_cost_account_ids
            )
