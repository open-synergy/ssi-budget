# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=C8101
{
    "name": "Financial Budget - Analytic Budget Integration",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "ssi_financial_budget",
        "ssi_analytic_budget",
    ],
    "data": [
        "views/financial_budget_budget_views.xml",
    ],
    "demo": [],
    "images": [],
}
