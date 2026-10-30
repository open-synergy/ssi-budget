# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AnalyticBudgetDetailMultiplier(models.Model):
    """One multiplier factor of an analytic budget detail line.

    The product of all factors of a line becomes the quantity of the
    line, for example persons times days times occurrences. The
    sequence, name, factor and unit of measure come from the
    multiplier factor mixin.
    """

    _name = "analytic_budget.detail_multiplier"
    _description = "Analytic Budget Detail Multiplier"
    _inherit = [
        "mixin.product_line_multiplier_factor",
    ]

    line_id = fields.Many2one(
        string="# Budget Detail",
        comodel_name="analytic_budget.detail",
        required=True,
        ondelete="cascade",
        help="Budget detail line that owns this factor.",
    )
