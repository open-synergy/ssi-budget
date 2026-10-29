# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

from odoo.addons.ssi_decorator import ssi_decorator


class AnalyticBudgetBudget(models.Model):
    """Analytic budget document tied to one analytic account.

    Holds planned revenue and cost details, compares them with the
    analytic lines posted on the account and its descendant accounts,
    and follows the confirm, open, done, cancel and terminate
    workflow. A detail may be bound to a period, so one budget can
    cover several years, and a budget may be the child of the budget of
    the parent analytic account. The realized amounts are stored and
    refreshed by explicit triggers on the analytic lines.
    """

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
        compute_sudo=True,
        store=False,
    )
    exclude_analytic_line_ids = fields.Many2many(
        string="All Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_exclude_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        compute_sudo=True,
        store=False,
    )
    budgeted_analytic_line_ids = fields.Many2many(
        string="Budgeted Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_budgeted_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        compute_sudo=True,
        store=False,
    )
    unbudgeted_analytic_line_ids = fields.Many2many(
        string="Unbudgeted Analytic Lines",
        comodel_name="account.analytic.line",
        relation="rel_budget_analytic_2_unbudgeted_line",
        column1="budget_id",
        column2="analytic_line_id",
        compute="_compute_analytic_line",
        compute_sudo=True,
        store=False,
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
        "date_start",
        "date_end",
        "exclude_account_ids",
        "account_ids",
    )
    def _compute_analytic_line(self):
        """Compute the analytic lines related to the budget.

        Splits the lines of the analytic account and of its descendant
        accounts, inside the date range of the budget, into all,
        budgeted, unbudgeted and excluded lines, based on the selected
        accounts and the excluded accounts. The lines are for display
        only and are not stored.

        :return: None
        """
        AnalyticLine = self.env["account.analytic.line"]
        for record in self:
            all_lines = budgeted = unbudgeted = excluded = AnalyticLine
            if isinstance(record.id, int) and record.analytic_account_id:
                criteria = record._get_analytic_line_criteria()
                all_lines = AnalyticLine.search(criteria)
                budgeted = AnalyticLine.search(
                    criteria
                    + [
                        ("general_account_id", "in", record.account_ids.ids),
                        (
                            "general_account_id",
                            "not in",
                            record.exclude_account_ids.ids,
                        ),
                    ]
                )
                unbudgeted = AnalyticLine.search(
                    criteria
                    + [
                        ("general_account_id", "not in", record.account_ids.ids),
                        (
                            "general_account_id",
                            "not in",
                            record.exclude_account_ids.ids,
                        ),
                    ]
                )
                excluded = AnalyticLine.search(
                    criteria
                    + [
                        ("general_account_id", "in", record.exclude_account_ids.ids),
                    ]
                )
            record.analytic_line_ids = all_lines
            record.budgeted_analytic_line_ids = budgeted
            record.unbudgeted_analytic_line_ids = unbudgeted
            record.exclude_analytic_line_ids = excluded

    def _get_analytic_line_criteria(self):
        """Build the criteria of the analytic lines counted by the budget.

        The lines of the analytic account of the budget and of all its
        descendant accounts, limited to the date range of the budget
        when it has one.

        :return: search domain on ``account.analytic.line``
        :rtype: list
        """
        self.ensure_one()
        criteria = [("account_id", "child_of", self.analytic_account_id.id)]
        if self.date_start:
            criteria.append(("date", ">=", self.date_start))
        if self.date_end:
            criteria.append(("date", "<=", self.date_end))
        return criteria

    @api.depends(
        "detail_ids.period_id.date_start",
        "detail_ids.period_id.date_end",
    )
    def _compute_period(self):
        """Compute the date range covered by the periods of the details.

        Start is the earliest period start and end is the latest period
        end among the details. Both stay empty when no detail has a
        period.

        :return: None
        """
        for record in self:
            periods = record.detail_ids.mapped("period_id")
            result_start = result_end = False
            if periods:
                result_start = min(periods.mapped("date_start"))
                result_end = max(periods.mapped("date_end"))
            record.date_start = result_start
            record.date_end = result_end

    @api.depends(
        "detail_ids",
        "detail_ids.direction",
        "detail_ids.price_subtotal",
    )
    def _compute_amount_planned(self):
        """Compute the planned revenue, cost and profit or loss.

        Planned amounts come from the revenue and cost details of the
        budget itself.

        :return: None
        """
        for document in self:
            amount_planned_revenue = 0.0
            amount_planned_cost = 0.0
            for detail in document.detail_revenue_ids:
                amount_planned_revenue += detail.price_subtotal
            for detail in document.detail_cost_ids:
                amount_planned_cost += detail.price_subtotal
            document.amount_planned_revenue = amount_planned_revenue
            document.amount_planned_cost = amount_planned_cost
            document.amount_planned_pl = amount_planned_revenue - amount_planned_cost

    @api.depends(
        "analytic_account_id",
        "date_start",
        "date_end",
        "account_ids",
        "exclude_account_ids",
    )
    def _compute_amount_realization(self):
        """Compute the realization amounts of the budget.

        The sums come from one ``read_group`` on the analytic lines per
        sign, never from a loop on the lines. The lines are those of the
        analytic account and its descendants, inside the date range of
        the budget. Positive amounts are revenue and negative amounts
        are cost, each split into budgeted and unbudgeted by the
        accounts of the budget.

        :return: None
        """
        for document in self:
            revenue = document._get_realization_sums(positive=True)
            cost = document._get_realization_sums(positive=False)
            document.amount_budgeted_revenue_realization = revenue["budgeted"]
            document.amount_unbudgeted_revenue_realization = revenue["unbudgeted"]
            document.amount_revenue_realization = (
                revenue["budgeted"] + revenue["unbudgeted"]
            )
            document.amount_budgeted_cost_realization = cost["budgeted"]
            document.amount_unbudgeted_cost_realization = cost["unbudgeted"]
            document.amount_cost_realization = cost["budgeted"] + cost["unbudgeted"]
            document.amount_profit_realization = (
                document.amount_revenue_realization - document.amount_cost_realization
            )

    def _get_realization_sums(self, positive):
        """Sum the analytic lines of one sign, split by the budget accounts.

        :param positive: True for revenue lines, False for cost lines
        :return: dict with the ``budgeted`` and ``unbudgeted`` totals;
            cost totals are returned as positive numbers
        :rtype: dict
        """
        self.ensure_one()
        result = {"budgeted": 0.0, "unbudgeted": 0.0}
        if not isinstance(self.id, int) or not self.analytic_account_id:
            return result
        criteria = self._get_analytic_line_criteria()
        if positive:
            criteria.append(("amount", ">", 0.0))
        else:
            criteria.append(("amount", "<", 0.0))
        groups = (
            self.env["account.analytic.line"]
            .sudo()
            .read_group(
                criteria,
                ["amount"],
                ["general_account_id"],
                lazy=False,
            )
        )
        account_ids = self.account_ids.ids
        exclude_ids = self.exclude_account_ids.ids
        for group in groups:
            account_id = group["general_account_id"] and group["general_account_id"][0]
            if account_id in exclude_ids:
                continue
            key = "budgeted" if account_id in account_ids else "unbudgeted"
            result[key] += abs(group["amount"])
        return result

    @api.model
    def _get_realization_field_names(self):
        """Return the stored realization fields of the budget.

        Public extension point used by the recompute triggers.

        :return: names of the stored realization fields
        :rtype: list
        """
        return [
            "amount_unbudgeted_revenue_realization",
            "amount_budgeted_revenue_realization",
            "amount_revenue_realization",
            "amount_unbudgeted_cost_realization",
            "amount_budgeted_cost_realization",
            "amount_cost_realization",
            "amount_profit_realization",
        ]

    def _add_realization_to_compute(self):
        """Schedule the recomputation of the stored realization.

        Marks the stored realization fields of the budgets and the
        realized amount of all their details; the ORM batches the
        computation until the next flush.

        :return: None
        """
        budgets = self.sudo().exists()
        for field_name in self._get_realization_field_names():
            self.env.add_to_compute(self._fields[field_name], budgets)
        self.env.add_to_compute(
            self.env["analytic_budget.detail"]._fields["amount_realized"],
            budgets.mapped("detail_ids"),
        )

    def action_recompute_realization(self):
        """Recompute the stored realization of the selected budgets.

        Safety net for the automatic triggers: it recomputes the stored
        realization amounts of the budgets and of their details from
        the analytic lines.

        :return: None
        """
        self._add_realization_to_compute()
        self.flush()

    date_start = fields.Date(
        string="Date Start",
        compute="_compute_period",
        compute_sudo=True,
        store=True,
        help="Earliest start date of the periods of the details. Empty when "
        "no detail has a period.",
    )
    date_end = fields.Date(
        string="Date End",
        compute="_compute_period",
        compute_sudo=True,
        store=True,
        help="Latest end date of the periods of the details. Empty when "
        "no detail has a period.",
    )
    analytic_account_parent_id = fields.Many2one(
        string="Parent Analytic Account",
        comodel_name="account.analytic.account",
        related="analytic_account_id.parent_id",
        compute_sudo=True,
        store=False,
    )
    parent_id = fields.Many2one(
        string="Parent Budget",
        comodel_name="analytic_budget.budget",
        ondelete="restrict",
        domain="[('analytic_account_id', '=', analytic_account_parent_id)]",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Budget of the parent analytic account. The details of this "
        "budget may not exceed the matching details of the parent budget.",
    )
    child_ids = fields.One2many(
        string="Child Budgets",
        comodel_name="analytic_budget.budget",
        inverse_name="parent_id",
        readonly=True,
    )
    amount_planned_revenue = fields.Monetary(
        string="Planned Revenue",
        compute="_compute_amount_planned",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_planned_cost = fields.Monetary(
        string="Planned Cost",
        compute="_compute_amount_planned",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_planned_pl = fields.Monetary(
        string="Planned Profit/Loss",
        compute="_compute_amount_planned",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_unbudgeted_revenue_realization = fields.Monetary(
        string="Unbudgeted Revenue Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_budgeted_revenue_realization = fields.Monetary(
        string="Budgeted Revenue Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_revenue_realization = fields.Monetary(
        string="Revenue Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_unbudgeted_cost_realization = fields.Monetary(
        string="Unbudgeted Cost Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_budgeted_cost_realization = fields.Monetary(
        string="Budgeted Cost Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_cost_realization = fields.Monetary(
        string="Cost Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
        store=True,
        currency_field="company_currency_id",
    )
    amount_profit_realization = fields.Monetary(
        string="Profit/Loss Realization",
        compute="_compute_amount_realization",
        compute_sudo=True,
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
        "analytic_account_id",
    )
    def onchange_parent_id(self):
        """Clear the parent budget when the analytic account changes."""
        self.parent_id = False

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

    @api.model
    def _get_allocation_child_states(self):
        """Return the states of child budgets counted in an allocation.

        Public extension point: glue modules may extend the result.

        :return: states of child budgets counted against the parent
        :rtype: list
        """
        return ["draft", "confirm", "open", "done", "terminate"]

    def _get_counted_children(self):
        """Return the child budgets counted in the allocation.

        :return: child budgets whose state is an allocation state
        :rtype: recordset
        """
        self.ensure_one()
        states = self._get_allocation_child_states()
        return self.sudo().child_ids.filtered(lambda r: r.state in states)

    @api.constrains("parent_id", "analytic_account_id")
    def _constrains_parent_id(self):
        """Validate the link between a budget and its parent budget.

        The analytic account of the parent budget must be the parent of
        the analytic account of this budget, and the details must fit
        the parent details.

        :raises ValidationError: if the link is not valid
        """
        for record in self.filtered(lambda r: r.parent_id):
            parent_account = record.sudo().analytic_account_id.parent_id
            if record.sudo().parent_id.analytic_account_id != parent_account:
                error_message = (
                    _(
                        """
Context: Save analytic budget
Database ID: %s
Problem: The analytic account of the parent budget is not the parent \
of the analytic account of this budget
Solution: Choose the budget of the parent analytic account
"""
                    )
                    % (record.id)
                )
                raise ValidationError(error_message)
            record._check_parent_allocation()

    def _is_detail_within_parent(self, detail):
        """Tell whether a detail fits a detail group of the parent budget.

        :param detail: detail line of this budget
        :return: True when a parent line has the same account and holds
            the period of the detail
        :rtype: bool
        """
        self.ensure_one()
        parent_details = self.sudo().parent_id.detail_ids.filtered(
            lambda r: r.account_id == detail.account_id
        )
        return any(detail._is_period_within(x) for x in parent_details)

    def _check_parent_allocation(self, force=False):
        """Check the details of this budget against its parent budget.

        Every detail must fit a parent detail of the same account whose
        period holds the period of the detail. When the budget counts in
        the allocation, or when ``force`` is set, the total of the child
        details must also stay inside the parent details.

        :param force: count this budget in the allocation whatever its
            state, used when it is about to enter the allocation again
        :raises ValidationError: if a limit is exceeded
        """
        self.ensure_one()
        parent = self.sudo().parent_id
        if not parent:
            return
        for detail in self.sudo().detail_ids.filtered(lambda r: r.account_id):
            if not self._is_detail_within_parent(detail):
                error_message = (
                    _(
                        """
Context: Check analytic budget allocation
Database ID: %s
Problem: A detail is not inside any detail of the parent budget \
with the same account and a period holding its period
Solution: Plan the account in the parent budget, or use a period \
inside the period of the parent detail
"""
                    )
                    % (self.id)
                )
                raise ValidationError(error_message)
        if force or self.state in self._get_allocation_child_states():
            parent._check_children_allocation(extra_children=self)

    def _check_children_allocation(self, extra_children=None):
        """Check that the child details stay inside the details of this budget.

        The details of this budget are grouped by account and period;
        for every group, the total of the child details of the same
        account whose period fits the period of the group may not exceed
        the total of the group. The product is ignored.

        :param extra_children: child budgets counted whatever their state
        :raises ValidationError: if a group is exceeded
        """
        self.ensure_one()
        children = self._get_counted_children()
        if extra_children:
            children |= extra_children.sudo()
        if not children:
            return
        details = self.sudo().detail_ids.filtered(lambda r: r.account_id)
        rounding = self.company_currency_id.rounding
        groups = {(x.account_id.id, x.period_id.id): x for x in details}
        for key in groups:
            group_details = details.filtered(
                lambda r: (r.account_id.id, r.period_id.id) == key
            )
            reference = groups[key]
            limit = sum(group_details.mapped("price_subtotal"))
            child_details = children.mapped("detail_ids").filtered(
                lambda r: r.account_id == reference.account_id
                and r._is_period_within(reference)
            )
            total = sum(child_details.mapped("price_subtotal"))
            if float_compare(total, limit, precision_rounding=rounding) > 0:
                error_message = (
                    _(
                        """
Context: Check analytic budget allocation
Database ID: %s
Problem: The child budgets exceed the amount of the parent budget
Solution: Reduce the child details so the total of an account and period \
does not exceed the parent detail
"""
                    )
                    % (self.id)
                )
                raise ValidationError(error_message)

    def _check_no_counted_children(self, context):
        """Reject the action while counted child budgets exist.

        :param context: name of the action, used in the message
        :raises ValidationError: if a counted child budget exists
        """
        self.ensure_one()
        if self._get_counted_children():
            error_message = (
                _(
                    """
Context: %s analytic budget
Database ID: %s
Problem: The budget still has child budgets that are not cancelled or rejected
Solution: Cancel or reject the child budgets first
"""
                )
                % (context, self.id)
            )
            raise ValidationError(error_message)

    @ssi_decorator.pre_confirm_check()
    def _10_check_allocation_confirm(self):
        """Reject confirming a child budget that exceeds its parent.

        Runs on the ``pre_confirm_check`` slot.

        :raises ValidationError: if the allocation limit is exceeded
        """
        self.ensure_one()
        self._check_parent_allocation(force=True)

    @ssi_decorator.pre_cancel_check()
    def _10_check_children_cancel(self):
        """Reject cancelling a budget with counted child budgets.

        Runs on the ``pre_cancel_check`` slot.

        :raises ValidationError: if a counted child budget exists
        """
        self.ensure_one()
        self._check_no_counted_children("Cancel")

    @ssi_decorator.pre_restart_check()
    def _10_check_children_restart(self):
        """Reject restarting a budget with counted child budgets.

        Runs on the ``pre_restart_check`` slot.

        :raises ValidationError: if a counted child budget exists
        """
        self.ensure_one()
        self._check_no_counted_children("Restart")

    @ssi_decorator.pre_restart_check()
    def _20_check_allocation_restart(self):
        """Reject restarting a child budget that exceeds its parent.

        Runs on the ``pre_restart_check`` slot, counting this budget
        itself in the allocation it would join again.

        :raises ValidationError: if the allocation limit is exceeded
        """
        self.ensure_one()
        self._check_parent_allocation(force=True)
