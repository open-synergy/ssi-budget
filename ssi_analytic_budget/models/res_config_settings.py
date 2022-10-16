# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = [
        "res.config.settings",
    ]

    module_ssi_analytic_budget_related_attachment = fields.Boolean(
        "Analytic Budget - Related Attachment",
    )
    module_ssi_analytic_budget_custom_information = fields.Boolean(
        "Analytic Budget - Custom Information",
    )
    module_ssi_analytic_budget_status_check = fields.Boolean(
        "Analytic Budget - Status Check",
    )
    module_ssi_analytic_budget_state_change_constrains = fields.Boolean(
        "Analytic Budget - State Change Constrains",
    )
    module_ssi_analytic_budget_qrcode = fields.Boolean(
        "Analytic Budget - QR Code",
    )
