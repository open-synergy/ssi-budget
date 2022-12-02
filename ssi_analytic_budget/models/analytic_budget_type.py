# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class AnalyticBudgetType(models.Model):
    _name = "analytic_budget.type"
    _inherit = ["mixin.master_data"]
    _description = "Analytic Budget Type"

    name = fields.Char(
        string="Analytic Budget Type",
    )

    @api.multi
    def _compute_allowed_revenue_account(self):
        for record in self:
            result = []
            result += record.allowed_revenue_account_ids.ids
            for product in record.revenue_account_ids:
                result.append(product.account_id.id)
            record.all_allowed_revenue_account_ids = result

    @api.multi
    def _compute_allowed_cost_account(self):
        for record in self:
            result = []
            result += record.allowed_cost_account_ids.ids
            for product in record.cost_account_ids:
                result.append(product.account_id.id)
            record.all_allowed_cost_account_ids = result

    allowed_revenue_account_ids = fields.Many2many(
        string="Allowed Revenue Accounts Without Product",
        comodel_name="account.account",
        relation="rel_budget_analytic_type_2_revenue_account",
        column1="type_id",
        column2="account_id",
    )
    allowed_cost_account_ids = fields.Many2many(
        string="Allowed Cost Accounts Without Product",
        comodel_name="account.account",
        relation="rel_budget_analytic_type_2_cost_account",
        column1="type_id",
        column2="account_id",
    )
    allowed_date_range_type_ids = fields.Many2many(
        string="Allowed Date Range Types",
        comodel_name="date.range.type",
        relation="rel_budget_analytic_type_2_date_range_type",
        column1="type_id",
        column2="date_range_type_id",
    )
    account_ids = fields.One2many(
        string="Allowed Account",
        comodel_name="analytic_budget.type_account",
        inverse_name="type_id",
    )
    revenue_account_ids = fields.One2many(
        string="Revenue Accounts",
        comodel_name="analytic_budget.type_account",
        inverse_name="type_id",
        domain=[
            ("direction", "=", "revenue"),
        ],
    )
    cost_account_ids = fields.One2many(
        string="Cost Accounts",
        comodel_name="analytic_budget.type_account",
        inverse_name="type_id",
        domain=[
            ("direction", "=", "cost"),
        ],
    )
    all_allowed_revenue_account_ids = fields.Many2many(
        string="All Allowed Revenue Account",
        comodel_name="account.account",
        compute="_compute_allowed_revenue_account",
        store=False,
    )
    all_allowed_cost_account_ids = fields.Many2many(
        string="All Allowed Cost Account",
        comodel_name="account.account",
        compute="_compute_allowed_cost_account",
        store=False,
    )
