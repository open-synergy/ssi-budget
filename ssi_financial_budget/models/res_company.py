# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = [
        "res.company",
    ]

    # Adds the date range type used by yearly financial budgets.
    financial_budget_yearly_range_type_id = fields.Many2one(
        string="Financial Budget Yearly Range Type",
        comodel_name="date.range.type",
        help="Date range type whose ranges are the periods of yearly "
        "financial budgets of this company.",
    )
