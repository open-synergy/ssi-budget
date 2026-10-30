# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestFinancialAnalyticBudget(YamlTransactionCase):
    """Run the financial ceiling scenarios of the analytic budget."""

    def test_financial_analytic_budget(self):
        """Run the ceiling, period selection and restart scenarios."""
        self.run_yaml_scenario("test_data_financial_analytic_budget.yaml")
