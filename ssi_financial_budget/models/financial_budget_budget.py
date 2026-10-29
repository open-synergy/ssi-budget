# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

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
    periodicity = fields.Selection(
        string="Periodicity",
        selection=[
            ("yearly", "Yearly"),
            ("monthly", "Monthly"),
        ],
        required=True,
        default="monthly",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Yearly budgets use the yearly range type configured on the "
        "company. Monthly budgets use fiscal month periods and can be "
        "limited by a yearly parent budget.",
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
    allowed_period_ids = fields.Many2many(
        string="Allowed Periods",
        comodel_name="date.range",
        compute="_compute_allowed_period_ids",
        compute_sudo=True,
        store=False,
        help="Periods that match the periodicity of the budget.",
    )
    parent_id = fields.Many2one(
        string="Parent Budget",
        comodel_name="financial_budget.budget",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Yearly budget that limits the amount of this monthly budget "
        "per account.",
    )
    child_ids = fields.One2many(
        string="Monthly Budgets",
        comodel_name="financial_budget.budget",
        inverse_name="parent_id",
        readonly=True,
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

    @api.depends(
        "periodicity",
        "company_id",
        "company_id.financial_budget_yearly_range_type_id",
    )
    def _compute_allowed_period_ids(self):
        """Compute the periods that match the periodicity of the budget.

        Used to restrict the ``period_id`` selection on the form view.
        """
        for record in self:
            record.allowed_period_ids = self.env["date.range"].search(
                record._get_period_domain()
            )

    def _get_period_domain(self):
        """Build the domain of the periods allowed for the budget.

        Monthly budgets accept fiscal month periods. Yearly budgets
        accept the periods of the yearly range type of the company,
        and none when the company has not configured one.

        :return: domain on ``date.range``
        :rtype: list
        """
        self.ensure_one()
        if self.periodicity == "yearly":
            range_type = self.company_id.financial_budget_yearly_range_type_id
            if not range_type:
                return [("id", "=", False)]
            return [("type_id", "=", range_type.id)]
        return [("type_id.fiscal_month", "=", True)]

    @api.model
    def _get_allocation_child_states(self):
        """Return the states of monthly budgets counted in an allocation.

        Public extension point: glue modules may extend the result.

        :return: states of child budgets counted against the parent
        :rtype: list
        """
        return ["draft", "confirm", "open", "done", "terminate"]

    @api.onchange("periodicity")
    def onchange_period_id(self):
        """Clear the period when the periodicity changes."""
        self.period_id = False

    @api.onchange("periodicity")
    def onchange_parent_id(self):
        """Clear the parent when the periodicity changes."""
        self.parent_id = False

    @api.constrains("periodicity", "period_id", "company_id")
    def _check_period_periodicity(self):
        """Validate that the period matches the periodicity.

        :raises ValidationError: if the period does not match the rule
            of the periodicity, including a yearly budget while the
            company has no yearly range type configured
        """
        for record in self.filtered(lambda r: r.period_id):
            domain = record._get_period_domain() + [
                ("id", "=", record.period_id.id),
            ]
            if not self.env["date.range"].sudo().search_count(domain):
                error_message = (
                    _(
                        """
Context: Save financial budget
Database ID: %s
Problem: Period does not match the periodicity of the budget
Solution: Choose a fiscal month period for a monthly budget, or a period \
of the company yearly range type for a yearly budget
"""
                    )
                    % (record.id)
                )
                raise ValidationError(error_message)

    @api.constrains("parent_id", "periodicity", "type_id", "company_id", "period_id")
    def _check_parent_consistency(self):
        """Validate the link between a monthly budget and its parent.

        The parent must be yearly with the same type and company, and
        the period of the monthly budget must lie inside the period of
        the parent. Then the amounts of the details must respect the
        allocation limit of the parent.

        :raises ValidationError: if the parent is not consistent
        """
        for record in self:
            if record.periodicity == "yearly" and record.parent_id:
                record._raise_parent_error("A yearly budget cannot have a parent")
            if not record.parent_id:
                continue
            parent = record.parent_id
            if parent.periodicity != "yearly":
                record._raise_parent_error("The parent budget must be yearly")
            if parent.type_id != record.type_id:
                record._raise_parent_error("The parent has a different type")
            if parent.company_id != record.company_id:
                record._raise_parent_error("The parent has a different company")
            if (
                not record.period_id
                or record.date_start < parent.date_start
                or record.date_end > parent.date_end
            ):
                record._raise_parent_error("The period is outside the parent period")
            for detail in record.detail_ids:
                detail._check_parent_detail()
                if record.state in self._get_allocation_child_states():
                    detail._check_parent_allocation()

    def _raise_parent_error(self, problem):
        """Raise the structured error of an invalid parent link.

        :param problem: description of the problem
        :raises ValidationError: always
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: Save financial budget
Database ID: %s
Problem: %s
Solution: Choose an open yearly budget of the same type and company \
whose period contains the period of this budget
"""
            )
            % (self.id, problem)
        )
        raise ValidationError(error_message)

    def _get_counted_children(self):
        """Return the child budgets counted in the allocation.

        :return: child budgets whose state is an allocation state
        :rtype: recordset
        """
        self.ensure_one()
        states = self._get_allocation_child_states()
        return self.sudo().child_ids.filtered(lambda r: r.state in states)

    def _check_no_counted_children(self, context):
        """Reject the action while counted monthly budgets exist.

        :param context: name of the action, used in the message
        :raises ValidationError: if a counted child budget exists
        """
        self.ensure_one()
        if self.periodicity == "yearly" and self._get_counted_children():
            error_message = (
                _(
                    """
Context: %s financial budget
Database ID: %s
Problem: The yearly budget still has monthly budgets in progress
Solution: Cancel or reject the monthly budgets first
"""
                )
                % (context, self.id)
            )
            raise ValidationError(error_message)

    @ssi_decorator.pre_restart_check()
    def _10_check_children_restart(self):
        """Reject restarting a yearly budget with counted children.

        Runs on the ``pre_restart_check`` slot.

        :raises ValidationError: if a counted child budget exists
        """
        self.ensure_one()
        self._check_no_counted_children("Restart")

    @ssi_decorator.pre_restart_check()
    def _20_check_allocation_restart(self):
        """Reject restarting a monthly budget that exceeds its parent.

        Runs on the ``pre_restart_check`` slot, counting this budget
        itself in the allocation it would join again.

        :raises ValidationError: if the allocation limit is exceeded
        """
        self.ensure_one()
        if self.parent_id:
            for detail in self.detail_ids:
                detail._check_parent_allocation()

    @ssi_decorator.pre_cancel_check()
    def _10_check_children_cancel(self):
        """Reject cancelling a yearly budget with counted children.

        Runs on the ``pre_cancel_check`` slot.

        :raises ValidationError: if a counted child budget exists
        """
        self.ensure_one()
        self._check_no_counted_children("Cancel")

    def action_create_monthly_budgets(self):
        """Create one draft monthly budget per fiscal month of the year.

        Every fiscal month range inside the period of this yearly open
        budget gets a monthly budget linked to it. The amount of each
        account is divided equally and the last month takes the
        rounding remainder so that the total equals the yearly amount.

        :raises UserError: if the budget is not yearly and open, already
            has counted monthly budgets, or has no usable fiscal months
        """
        self.ensure_one()
        if self.periodicity != "yearly" or self.state != "open":
            self._raise_create_error("The budget must be yearly and in progress")
        if self._get_counted_children():
            self._raise_create_error("The budget already has monthly budgets")
        ranges = self._get_monthly_ranges()
        if not ranges:
            self._raise_create_error("There is no fiscal month in the period")
        for previous, current in zip(ranges, ranges[1:]):
            if current.date_start <= previous.date_end:
                self._raise_create_error("The fiscal months overlap")
        for date_range in ranges:
            self.create(self._prepare_monthly_budget(date_range, ranges))

    def _raise_create_error(self, problem):
        """Raise the structured error of the monthly budget generation.

        :param problem: description of the problem
        :raises UserError: always
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: Create monthly budgets
Database ID: %s
Problem: %s
Solution: Use a yearly budget in progress without monthly budgets, whose \
period contains separate fiscal month ranges
"""
            )
            % (self.id, problem)
        )
        raise UserError(error_message)

    def _get_monthly_ranges(self):
        """Find the fiscal month ranges inside the period of the budget.

        :return: fiscal month ranges ordered by start date
        :rtype: recordset
        """
        self.ensure_one()
        return self.env["date.range"].search(
            [
                ("type_id.fiscal_month", "=", True),
                ("company_id", "in", [self.company_id.id, False]),
                ("date_start", ">=", self.date_start),
                ("date_end", "<=", self.date_end),
            ],
            order="date_start",
        )

    def _prepare_monthly_budget(self, date_range, ranges):
        """Prepare the values of one monthly budget.

        :param date_range: fiscal month range of the monthly budget
        :param ranges: all ranges that receive a monthly budget
        :return: values for ``create``
        :rtype: dict
        """
        self.ensure_one()
        count = len(ranges)
        is_last = date_range == ranges[-1]
        currency = self.company_currency_id
        details = []
        for detail in self.detail_ids:
            share = currency.round(detail.amount / count)
            amount = share
            if is_last:
                amount = currency.round(detail.amount - share * (count - 1))
            details.append(
                (
                    0,
                    0,
                    {
                        "account_id": detail.account_id.id,
                        "direction": detail.direction,
                        "amount": amount,
                    },
                )
            )
        return {
            "type_id": self.type_id.id,
            "company_id": self.company_id.id,
            "periodicity": "monthly",
            "period_id": date_range.id,
            "parent_id": self.id,
            "detail_ids": details,
        }

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
