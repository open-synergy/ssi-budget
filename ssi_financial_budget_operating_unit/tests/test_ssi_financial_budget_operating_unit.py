# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSsiFinancialBudgetOperatingUnit(YamlTransactionCase):
    """YAML scenario runner for the Financial Budget Operating Unit glue.

    Covers Operating Unit propagation on ``financial_budget.budget`` and the
    record rule that restricts access by operating unit.
    """

    def test_ssi_financial_budget_operating_unit(self):
        """Run the Operating Unit scenarios from the YAML file.

        The scenarios live in
        ``test_data_ssi_financial_budget_operating_unit.yaml``.
        """
        self.run_yaml_scenario("test_data_ssi_financial_budget_operating_unit.yaml")
