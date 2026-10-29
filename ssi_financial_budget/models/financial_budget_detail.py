# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class FinancialBudgetDetail(models.Model):
    """Planned line of a financial budget.

    Holds the planned amount for one account and direction (revenue
    or cost) of a financial budget.
    """

    _name = "financial_budget.detail"
    _description = "Financial Budget Detail"

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="financial_budget.budget",
        required=True,
        ondelete="cascade",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        related="budget_id.period_id",
        compute_sudo=True,
        store=True,
    )
    date_start = fields.Date(
        string="Date Start",
        related="budget_id.period_id.date_start",
        compute_sudo=True,
        store=True,
    )
    date_end = fields.Date(
        string="Date End",
        related="budget_id.period_id.date_end",
        compute_sudo=True,
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="financial_budget.type",
        related="budget_id.type_id",
        compute_sudo=True,
        store=False,
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        related="budget_id.type_id.allowed_account_ids",
        store=False,
        compute_sudo=True,
        help="Accounts permitted by the type of the budget.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("revenue", "Revenue"),
            ("cost", "Cost"),
        ],
        required=True,
        default="revenue",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="budget_id.company_currency_id",
        store=False,
        help="Currency of the budget company. Only supports the "
        "currency of the amount field.",
    )
    amount = fields.Monetary(
        string="Amount",
        required=True,
        default=0.0,
        currency_field="company_currency_id",
        help="Planned amount of this account and direction.",
    )

    @api.depends(
        "amount",
        "account_id",
        "budget_id.child_ids.state",
        "budget_id.child_ids.detail_ids.amount",
        "budget_id.child_ids.detail_ids.account_id",
    )
    def _compute_allocation(self):
        """Compute the allocated and unallocated amounts of the line.

        The allocated amount is the sum of the matching detail lines of
        the monthly budgets counted against this budget. Lines of a
        budget without monthly budgets have nothing allocated.
        """
        for record in self:
            allocated = 0.0
            if isinstance(record.id, int) and record.account_id:
                children = self.search(record._get_allocation_criteria())
                allocated = sum(children.mapped("amount"))
            record.amount_allocated = allocated
            record.amount_unallocated = record.amount - allocated

    amount_allocated = fields.Monetary(
        string="Allocated Amount",
        compute="_compute_allocation",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Sum of the same account in the monthly budgets counted "
        "against this budget.",
    )
    amount_unallocated = fields.Monetary(
        string="Unallocated Amount",
        compute="_compute_allocation",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Planned amount minus the allocated amount.",
    )

    def _get_allocation_criteria(self):
        """Build the criteria of the monthly lines counted against this line.

        Public extension point: called on a line of the parent budget.

        :return: domain matching the lines of the counted child budgets
        :rtype: list
        """
        self.ensure_one()
        states = self.env["financial_budget.budget"]._get_allocation_child_states()
        return [
            ("budget_id.parent_id", "=", self.budget_id.id),
            ("budget_id.state", "in", states),
            ("account_id", "=", self.account_id.id),
        ]

    @api.constrains("budget_id", "account_id", "direction", "amount")
    def _constrains_allocation(self):
        """Validate the lines of a monthly budget against its parent.

        The account must exist in the parent budget with the same
        direction, and the lines of all counted monthly budgets must not
        exceed the amount of the parent line.

        :raises ValidationError: if a rule is violated
        """
        states = self.env["financial_budget.budget"]._get_allocation_child_states()
        for record in self.filtered(lambda r: r.budget_id.parent_id and r.account_id):
            record._check_parent_detail()
            if record.budget_id.state in states:
                record._check_parent_allocation()

    def _get_parent_detail(self):
        """Find the line of the parent budget with the same account.

        :return: matching line of the parent budget, may be empty
        :rtype: recordset
        """
        self.ensure_one()
        return self.sudo().budget_id.parent_id.detail_ids.filtered(
            lambda r: r.account_id == self.account_id and r.direction == self.direction
        )

    def _check_parent_detail(self):
        """Check that the parent budget has the account and direction.

        :raises ValidationError: if the parent has no matching line
        """
        self.ensure_one()
        if not self._get_parent_detail():
            error_message = (
                _(
                    """
Context: Save budget detail line
Database ID: %s
Problem: Account and direction are not in the parent budget
Solution: Use an account and direction planned in the parent budget
"""
                )
                % (self.id)
            )
            raise ValidationError(error_message)

    def _check_parent_allocation(self):
        """Check the allocation limit of the parent line.

        The line itself is always counted, whatever the state of its
        budget, so the check also serves a budget about to be restarted.

        :raises ValidationError: if the total exceeds the parent line
        """
        self.ensure_one()
        parent_detail = self._get_parent_detail()
        if not parent_detail:
            return
        parent_detail.ensure_one()
        children = self.sudo().search(parent_detail._get_allocation_criteria())
        others = children.filtered(lambda r: r.budget_id != self.budget_id)
        total = sum(others.mapped("amount")) + self.amount
        rounding = self.company_currency_id.rounding
        if float_compare(total, parent_detail.amount, precision_rounding=rounding) > 0:
            error_message = (
                _(
                    """
Context: Save budget detail line
Database ID: %s
Problem: Monthly budgets exceed the amount of the parent budget
Solution: Reduce the amount so the monthly budgets of the account do not \
exceed the amount of the parent budget
"""
                )
                % (self.id)
            )
            raise ValidationError(error_message)

    @api.constrains("budget_id", "account_id")
    def _constrains_account_id(self):
        """Validate the account of the detail line.

        Runs the two-layer check: the account must be one of the
        accounts allowed by the budget type, and no other detail line
        of the same budget may use the same account.

        :raises ValidationError: if the account is not allowed or is
            used twice in the same budget
        """
        for record in self.filtered(lambda r: r.account_id):
            record._check_account_allowed()
            record._check_account_unique()

    def _check_account_allowed(self):
        """Check that the account belongs to the budget type.

        :raises ValidationError: if the account is not allowed
        """
        self.ensure_one()
        allowed = self.budget_id.type_id.allowed_account_ids
        if self.account_id not in allowed:
            error_message = (
                _(
                    """
Context: Save budget detail line
Database ID: %s
Problem: Account is not allowed by the budget type
Solution: Choose an account listed in the allowed accounts of the type
"""
                )
                % (self.id)
            )
            raise ValidationError(error_message)

    def _check_account_unique(self):
        """Check that the account is used once in the budget.

        :raises ValidationError: if another line uses the same account
        """
        self.ensure_one()
        criteria = self._get_duplicate_account_criteria()
        if self.search_count(criteria) > 0:
            error_message = (
                _(
                    """
Context: Save budget detail line
Database ID: %s
Problem: Account is used more than once in the same budget
Solution: Use one detail line per account in a budget
"""
                )
                % (self.id)
            )
            raise ValidationError(error_message)

    def _get_duplicate_account_criteria(self):
        """Build the search criteria of duplicate detail lines.

        :return: domain matching other lines with the same account
        :rtype: list
        """
        self.ensure_one()
        return [
            ("id", "!=", self.id),
            ("budget_id", "=", self.budget_id.id),
            ("account_id", "=", self.account_id.id),
        ]
