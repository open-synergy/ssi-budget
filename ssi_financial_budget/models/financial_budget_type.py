# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class FinancialBudgetType(models.Model):
    _name = "financial_budget.type"
    _inherit = ["mixin.master_data"]
    _description = "Financial Budget Type"

    name = fields.Char(
        string="Financial Budget Type",
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        relation="rel_financial_budget_type_2_account",
        column1="type_id",
        column2="account_id",
    )
