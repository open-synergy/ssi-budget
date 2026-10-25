# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAnalyticBudgetWorkLog(YamlTransactionCase):
    """Cover the work log fields on ``analytic_budget.budget``."""

    def test_analytic_budget_work_log(self):
        """Run the work log YAML scenarios.

        The scenarios live in ``test_data_analytic_budget_work_log.yaml``.
        """
        self.run_yaml_scenario("test_data_analytic_budget_work_log.yaml")
