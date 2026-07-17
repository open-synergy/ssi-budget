# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Financial Budget + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_financial_budget",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/financial_budget_budget.xml",
        "security/ir_rule/financial_budget_budget.xml",
        "view/financial_budget_budget.xml",
    ],
}
