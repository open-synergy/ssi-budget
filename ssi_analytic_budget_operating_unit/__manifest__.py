# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Analytic Budget + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_analytic_budget",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/analytic_budget_budget.xml",
        "security/ir_rule/analytic_budget_budget.xml",
        "view/analytic_budget_budget.xml",
    ],
}
