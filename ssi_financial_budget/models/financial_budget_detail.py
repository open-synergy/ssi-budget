# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        related="budget_id.type_id.allowed_account_ids",
        store=False,
        compute_sudo=True,
        help="Accounts permitted by the type of the budget.",
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

    @api.constrains("budget_id", "account_id")
    def _constrains_account_id(self):
        """Validate the account of the detail line.

        Runs the two-layer check: the account must be one of the
        accounts allowed by the budget type, and no other detail line
        of the same budget may use the same account.

        :raises ValidationError: if the account is not allowed or is
            used twice in the same budget
        """
        for record in self.filtered(lambda r: r.account_id):
            record._check_account_allowed()
            record._check_account_unique()

    def _check_account_allowed(self):
        """Check that the account belongs to the budget type.

        :raises ValidationError: if the account is not allowed
        """
        self.ensure_one()
        allowed = self.budget_id.type_id.allowed_account_ids
        if self.account_id not in allowed:
            error_message = (
                _(
                    """
Context: Save budget detail line
Database ID: %s
Problem: Account is not allowed by the budget type
Solution: Choose an account listed in the allowed accounts of the type
"""
                )
                % (self.id)
            )
            raise ValidationError(error_message)

    def _check_account_unique(self):
        """Check that the account is used once in the budget.

        :raises ValidationError: if another line uses the same account
        """
        self.ensure_one()
        criteria = self._get_duplicate_account_criteria()
        if self.search_count(criteria) > 0:
            error_message = (
                _(
                    """
Context: Save budget detail line
Database ID: %s
Problem: Account is used more than once in the same budget
Solution: Use one detail line per account in a budget
"""
                )
                % (self.id)
            )
            raise ValidationError(error_message)

    def _get_duplicate_account_criteria(self):
        """Build the search criteria of duplicate detail lines.

        :return: domain matching other lines with the same account
        :rtype: list
        """
        self.ensure_one()
        return [
            ("id", "!=", self.id),
            ("budget_id", "=", self.budget_id.id),
            ("account_id", "=", self.account_id.id),
        ]
