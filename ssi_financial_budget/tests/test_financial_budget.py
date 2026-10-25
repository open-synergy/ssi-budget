# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestFinancialBudget(YamlTransactionCase):
    """Run the financial budget YAML scenarios."""

    def test_financial_budget(self):
        """Run the financial budget workflow scenarios.

        Covers the full workflow, master data creation and the
        reject transition, all defined in the YAML file.
        """
        self.run_yaml_scenario("test_data_financial_budget.yaml")
