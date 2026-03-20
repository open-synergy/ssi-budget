# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class FinancialBudgetBudget(models.Model):
    _name = "financial_budget.budget"
    _inherit = [
        "financial_budget.budget",
        "mixin.documenso_signing",
    ]

    _documenso_signing_create_page = True
