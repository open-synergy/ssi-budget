# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalyticBudgetDetail(models.Model):
    """Planned revenue or cost line of an analytic budget.

    Each line is priced through the product line price multiplier
    mixin, so its quantity may be the product of several factors,
    and is restricted to the accounts and products allowed by the
    budget type. A line may be bound to a date range, so one budget
    can cover several periods. The realized amount of a line is
    stored and read from the ``realization_budgeted`` SQL view, which
    is the single source of the matching rules.
    """

    _name = "analytic_budget.detail"
    _description = "Analytic Budget Detail"
    _inherit = [
        "mixin.product_line_price_multiplier",
    ]

    @api.depends(
        "type_id",
        "direction",
    )
    def _compute_allowed_account(self):
        """Compute the accounts allowed for the line.

        The allowed revenue or cost accounts of the budget type are
        used, depending on the direction of the line.

        :return: None
        """
        for record in self:
            result = []
            if record.direction == "revenue":
                result = record.type_id.all_allowed_revenue_account_ids.ids
            elif record.direction == "cost":
                result = record.type_id.all_allowed_cost_account_ids.ids
            record.allowed_account_ids = result

    @api.depends(
        "type_id",
        "direction",
        "account_id",
    )
    def _compute_allowed_product(self):
        """Compute the products allowed for the line.

        Looks up the budget type account matching the selected
        account, then sets the allowed products, the allowed product
        categories and whether a product is required.

        :return: None
        """
        obj_allowed = self.env["analytic_budget.type_account"]
        for record in self:
            result_product = []
            result_categ = []
            product_required = False
            if record.account_id and record.type_id:
                criteria = [
                    ("type_id", "=", record.type_id.id),
                    ("account_id", "=", record.account_id.id),
                ]
                alloweds = obj_allowed.search(criteria)
                if len(alloweds) > 0:
                    allowed = alloweds[0]
                    product_required = True
                    result_product = allowed.allowed_product_ids.ids
                    result_categ = allowed.allowed_product_categ_ids.ids
            record.allowed_product_ids = result_product
            record.allowed_product_categ_ids = result_categ
            record.product_required = product_required

    @api.depends(
        "budget_id",
        "budget_id.analytic_account_id",
        "account_id",
        "product_id",
        "period_id",
        "direction",
        "budget_id.detail_ids.account_id",
        "budget_id.detail_ids.product_id",
        "budget_id.detail_ids.period_id",
    )
    def _compute_amount_realized(self):
        """Compute the amount realized against the line.

        Reads the ``amount_realized`` column of the
        ``analytic_budget.realization_budgeted`` SQL view, which holds
        the matching rules of analytic lines to budget lines. The
        tables read by the view are flushed first, because the view is
        queried directly in SQL.

        :return: None
        """
        self._flush_realization_source()
        View = self.env["analytic_budget.realization_budgeted"].sudo()
        ids = [x for x in self.ids if isinstance(x, int)]
        amounts = {}
        if ids:
            rows = View.search_read(
                self._get_realization_view_criteria(ids), ["id", "amount_realized"]
            )
            amounts = {row["id"]: row["amount_realized"] for row in rows}
        for record in self:
            result = 0.0
            if isinstance(record.id, int):
                result = amounts.get(record.id, 0.0)
            record.amount_realized = result

    @api.model
    def _get_realization_view_criteria(self, ids):
        """Build the criteria selecting the view rows of the given lines.

        :param ids: database ids of the budget detail lines
        :return: search domain on ``analytic_budget.realization_budgeted``
        """
        return [("id", "in", ids)]

    @api.model
    def _flush_realization_source(self):
        """Flush the data read by the realization SQL views.

        The SQL views read the tables directly, so pending writes of
        the analytic lines, the budget lines, the budgets and the
        analytic account tree must reach the database first.

        :return: None
        """
        self.env["account.analytic.line"].flush(
            [
                "amount",
                "account_id",
                "date",
                "general_account_id",
                "product_id",
                "move_id",
            ]
        )
        self.env["analytic_budget.detail"].flush(
            [
                "budget_id",
                "account_id",
                "product_id",
                "period_id",
                "direction",
            ]
        )
        self.env["analytic_budget.budget"].flush(
            [
                "date_start",
                "date_end",
                "analytic_account_id",
            ]
        )
        self.env["account.analytic.account"].flush(["parent_id", "parent_path"])

    def _is_period_overlap(self, other):
        """Tell whether the period of this line overlaps another line.

        A line without period overlaps every other line.

        :param other: another budget detail line
        :return: True when the two date ranges intersect
        :rtype: bool
        """
        self.ensure_one()
        result = True
        if self.period_id and other.period_id:
            result = (
                self.period_id.date_start <= other.period_id.date_end
                and other.period_id.date_start <= self.period_id.date_end
            )
        return result

    def _is_period_within(self, parent_detail):
        """Tell whether the period of this line fits the parent period.

        A parent line without period holds every period, and a line
        without period fits only a parent line without period.

        :param parent_detail: line of the parent budget
        :return: True when the date range is inside the parent range
        :rtype: bool
        """
        self.ensure_one()
        result = True
        if parent_detail.period_id:
            result = bool(
                self.period_id
                and self.period_id.date_start >= parent_detail.period_id.date_start
                and self.period_id.date_end <= parent_detail.period_id.date_end
            )
        return result

    @api.constrains("budget_id", "account_id", "product_id", "period_id")
    def _constrains_period_overlap(self):
        """Forbid duplicate and overlapping lines inside one budget.

        For the same account and product, an empty product counted as
        one value, the date ranges of the lines must not intersect. A
        line without period intersects every line, and an exact
        duplicate is covered as well.

        :raises ValidationError: if two lines overlap
        """
        for record in self.filtered(lambda r: r.account_id and r.budget_id):
            siblings = record.sudo().budget_id.detail_ids - record
            for other in siblings.filtered(
                lambda r: r.account_id == record.account_id
                and r.product_id == record.product_id
            ):
                if record._is_period_overlap(other):
                    error_message = (
                        _(
                            """
Context: Save analytic budget detail
Database ID: %s
Problem: Account and product are already planned in an overlapping period
Solution: Use another period, or remove the overlapping line of the budget
"""
                        )
                        % (record.id)
                    )
                    raise ValidationError(error_message)

    @api.constrains("product_id", "account_id", "budget_id")
    def _constrains_product_required(self):
        """Require a product on the lines whose account asks for it.

        :raises ValidationError: if the product is required but empty
        """
        for record in self.filtered(lambda r: r.product_required):
            if not record.product_id:
                error_message = (
                    _(
                        """
Context: Save analytic budget detail
Database ID: %s
Problem: Product is required for this account
Solution: Select a product on the line
"""
                    )
                    % (record.id)
                )
                raise ValidationError(error_message)

    @api.constrains(
        "budget_id",
        "account_id",
        "period_id",
        "price_unit",
        "uom_quantity",
    )
    def _constrains_allocation(self):
        """Check the lines against the parent and the child budgets.

        A line of a child budget must fit a line of the parent budget,
        and the total of the child lines must stay inside the parent
        lines. A line of a parent budget must keep covering the lines
        of its child budgets.

        :raises ValidationError: if the allocation limit is exceeded
        """
        for budget in self.sudo().mapped("budget_id"):
            if budget.parent_id:
                budget._check_parent_allocation()
            if budget.child_ids:
                budget._check_children_allocation()

    def unlink(self):
        """Delete the lines then recheck the allocation of their parents.

        :return: result of the parent method
        """
        budgets = self.sudo().mapped("budget_id").filtered(lambda r: r.child_ids)
        result = super().unlink()
        for budget in budgets.exists():
            budget._check_children_allocation()
        return result

    multiplier_ids = fields.One2many(
        string="Multipliers",
        comodel_name="analytic_budget.detail_multiplier",
        inverse_name="line_id",
        copy=True,
        help="Factors whose product is the quantity of the line. "
        "Without factors the quantity is typed manually.",
    )
    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
        required=True,
        ondelete="cascade",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        related="budget_id.analytic_account_id",
        compute_sudo=True,
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="analytic_budget.type",
        related="budget_id.type_id",
        compute_sudo=True,
        store=False,
    )
    product_required = fields.Boolean(
        string="Product Required",
        compute="_compute_allowed_product",
        compute_sudo=True,
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        compute="_compute_allowed_product",
        compute_sudo=True,
        store=False,
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_allowed_product",
        compute_sudo=True,
        store=False,
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        compute="_compute_allowed_account",
        compute_sudo=True,
        store=False,
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
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        ondelete="restrict",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Date range of the line. Only the analytic lines dated inside "
        "the range are realized against this line. Empty means no date limit.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="budget_id.company_id",
        compute_sudo=True,
        store=False,
    )
    amount_realized = fields.Monetary(
        string="Realized",
        compute="_compute_amount_realized",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Revenue or cost realized against this line. Revenue is the "
        "sum of the matching analytic lines, cost is the opposite of that "
        "sum, so a normal realization is positive.",
    )
