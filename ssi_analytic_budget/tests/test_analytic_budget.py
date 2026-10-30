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

    def test_analytic_budget_period(self):
        """Run the period, remainder rule, hierarchy and realization scenarios."""
        self.run_yaml_scenario("test_data_analytic_budget_period.yaml")

    def test_analytic_budget_multiplier(self):
        """Run the multiplier factor and line quantity scenarios."""
        self.run_yaml_scenario("test_data_analytic_budget_multiplier.yaml")
