# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAnalyticBudget(YamlTransactionCase):
    """Run the analytic budget YAML scenarios."""

    def test_analytic_budget(self):
        """Run the workflow, master data and onchange scenarios."""
        self.run_yaml_scenario("test_data_analytic_budget.yaml")
