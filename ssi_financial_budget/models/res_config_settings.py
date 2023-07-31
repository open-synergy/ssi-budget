# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = [
        "res.config.settings",
    ]

    module_ssi_financial_budget_related_attachment = fields.Boolean(
        "Financial Budget - Related Attachment",
    )
    module_ssi_financial_budget_custom_information = fields.Boolean(
        "Financial Budget - Custom Information",
    )
    module_ssi_financial_budget_status_check = fields.Boolean(
        "Financial Budget - Status Check",
    )
    module_ssi_financial_budget_state_change_constrains = fields.Boolean(
        "Financial Budget - State Change Constrains",
    )
    module_ssi_financial_budget_qrcode = fields.Boolean(
        "Financial Budget - QR Code",
    )
