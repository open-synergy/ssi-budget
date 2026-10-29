# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FinancialBudgetDetail(models.Model):
    """Planned line of a financial budget.

    Holds the planned amount for one account and direction (revenue
    or cost) of a financial budget.
    """

    _name = "financial_budget.detail"
    _description = "Financial Budget Detail"

    budget_id = fields.Many2one(
        string="# Budget",
        comodel_name="financial_budget.budget",
        required=True,
        ondelete="cascade",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        related="budget_id.period_id",
        compute_sudo=True,
        store=True,
    )
    date_start = fields.Date(
        string="Date Start",
        related="budget_id.period_id.date_start",
        compute_sudo=True,
        store=True,
    )
    date_end = fields.Date(
        string="Date End",
        related="budget_id.period_id.date_end",
        compute_sudo=True,
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="financial_budget.type",
        related="budget_id.type_id",
        compute_sudo=True,
        store=False,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("revenue", "Revenue"),
            ("cost", "Cost"),
        ],
        required=True,
        default="revenue",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="budget_id.company_currency_id",
        store=False,
        help="Currency of the budget company. Only supports the "
        "currency of the amount field.",
    )
    amount = fields.Monetary(
        string="Amount",
        required=True,
        default=0.0,
        currency_field="company_currency_id",
        help="Planned amount of this account and direction.",
    )
