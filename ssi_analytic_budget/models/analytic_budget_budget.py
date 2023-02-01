# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


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

    @api.depends(
        "type_id",
    )
    def _compute_allowed_period_ids(self):
        obj_date_range = self.env["date.range"]
        for record in self:
            allowed_date_range_type_ids = record.type_id.allowed_date_range_type_ids.ids
            criteria = [("type_id", "in", allowed_date_range_type_ids)]
            date_range_ids = obj_date_range.search(criteria)
            record.allowed_period_ids = date_range_ids.ids

    allowed_period_ids = fields.Many2many(
        string="Allowed Periods",
        comodel_name="date.range",
        compute="_compute_allowed_period_ids",
        store=False,
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        required=True,
        readonly=True,
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

    all_realization_ids = fields.One2many(
        string="All Realization Lines",
        comodel_name="account.analytic.line",
        inverse_name="account_id",
    )

    @api.depends(
        "date_start",
        "date_end",
        "type_id",
        "analytic_account_id",
    )
    def _compute_realization(self):
        AL = self.env["account.analytic.line"]
        for record in self:
            criteria = [
                ("account_id", "=", record.analytic_account_id.id),
                ("date", ">=", record.date_start),
                ("date", "<=", record.date_end),
            ]
            realizations = AL.search(criteria)

            product_ids = (
                record.type_id.allowed_revenue_product_ids.ids
                + record.type_id.allowed_cost_product_ids.ids
            )

            criteria_budgeted = criteria + [("product_id", "in", product_ids)]
            budgeted_realizations = AL.search(criteria_budgeted)

            criteria_budgeted = criteria + [("product_id", "not in", product_ids)]
            unbudgeted_realizations = AL.search(criteria_budgeted)

            record.realization_ids = realizations.ids
            record.budgeted_realization_ids = budgeted_realizations.ids
            record.unbudgeted_realization_ids = unbudgeted_realizations.ids

    realization_ids = fields.Many2many(
        string="Realization Lines",
        comodel_name="account.analytic.line",
        compute="_compute_realization",
        store=True,
        relation="rel_budget_2_realization",
        column1="budget_id",
        column2="analytic_line_id",
    )
    budgeted_realization_ids = fields.Many2many(
        string="Budgeted Realization",
        comodel_name="account.analytic.line",
        compute="_compute_realization",
        store=False,
    )
    unbudgeted_realization_ids = fields.Many2many(
        string="Unbudgeted Realization",
        comodel_name="account.analytic.line",
        compute="_compute_realization",
        store=False,
    )

    @api.depends(
        "detail_ids",
        "detail_ids.product_id",
        "detail_ids.price_subtotal",
        "realization_ids",
        "realization_ids.amount",
        "realization_ids.unit_amount",
        "realization_ids.product_id",
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

            for detail in self.detail_ids:
                if detail.direction == "revenue":
                    amount_planned_revenue += detail.price_subtotal
                else:
                    amount_planned_cost -= detail.price_subtotal

            amount_planned_pl = amount_planned_revenue + amount_planned_cost

            for budgeted in document.budgeted_realization_ids:
                if budgeted.product_id.sale_ok and not budgeted.product_id.purchase_ok:
                    amount_budgeted_revenue_realization += budgeted.amount
                elif (
                    not budgeted.product_id.sale_ok and budgeted.product_id.purchase_ok
                ):
                    amount_budgeted_cost_realization += budgeted.amount
                elif budgeted.product_id.sale_ok and budgeted.product_id.purchase_ok:
                    if budgeted.amount > 0.0:
                        amount_budgeted_revenue_realization += budgeted.amount
                    elif budgeted.amount > 0.0:
                        amount_budgeted_cost_realization += budgeted.amount

            for unbudgeted in document.unbudgeted_realization_ids:
                if (
                    unbudgeted.product_id.sale_ok
                    and not unbudgeted.product_id.purchase_ok
                ):
                    amount_unbudgeted_revenue_realization += unbudgeted.amount
                elif (
                    not unbudgeted.product_id.sale_ok
                    and unbudgeted.product_id.purchase_ok
                ):
                    amount_unbudgeted_cost_realization += unbudgeted.amount
                elif (
                    unbudgeted.product_id.sale_ok and unbudgeted.product_id.purchase_ok
                ):
                    if unbudgeted.amount > 0.0:
                        amount_unbudgeted_revenue_realization += unbudgeted.amount
                    elif budgeted.amount > 0.0:
                        amount_unbudgeted_cost_realization += unbudgeted.amount

            amount_revenue_realization = (
                amount_unbudgeted_revenue_realization
                + amount_budgeted_revenue_realization
            )
            amount_cost_realization = (
                amount_unbudgeted_cost_realization + amount_budgeted_cost_realization
            )
            amount_profit_realization = (
                amount_revenue_realization + amount_cost_realization
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

    @api.model
    def create(self, values):
        _super = super(AnalyticBudgetBudget, self)
        result = _super.create(values)
        if not result.policy_template_id:
            template_id = result._get_template_policy()
            if template_id:
                result.write({"policy_template_id": template_id})
        return result

    def action_compute_realization(self):
        for record in self:
            record._compute_realization()
