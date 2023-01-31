# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AnalyticBudgetDetail(models.Model):
    _name = "analytic_budget.detail"
    _description = "Analytic Budget Detail"
    _inherit = [
        "mixin.product_line_price",
    ]

    @api.depends(
        "type_id",
        "direction",
    )
    def _compute_allowed_account(self):
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
        for record in self:
            result_product = []
            if record.direction == "revenue":
                result_product = record.type_id.allowed_revenue_product_ids.ids
            else:
                result_product = record.type_id.allowed_cost_product_ids.ids
            record.allowed_product_ids = result_product

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="analytic_budget.budget",
        required=True,
        ondelete="cascade",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        related="budget_id.period_id",
        store=True,
    )
    date_start = fields.Date(
        string="Date Start",
        related="budget_id.period_id.date_start",
        store=True,
    )
    date_end = fields.Date(
        string="Date End",
        related="budget_id.period_id.date_end",
        store=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        related="budget_id.analytic_account_id",
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="analytic_budget.type",
        related="budget_id.type_id",
        store=False,
    )
    product_required = fields.Boolean(
        string="Product Required",
        compute="_compute_allowed_product",
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        compute="_compute_allowed_product",
        store=False,
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_allowed_product",
        store=False,
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        compute="_compute_allowed_account",
        store=False,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=False,
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
