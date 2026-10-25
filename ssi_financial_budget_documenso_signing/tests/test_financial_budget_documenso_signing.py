# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestFinancialBudgetDocumensoSigning(YamlTransactionCase):
    """Cover Documenso signing fields on ``financial_budget.budget``."""

    def test_financial_budget_documenso_signing(self):
        """Run the Documenso signing YAML scenarios.

        The scenarios live in
        ``test_data_financial_budget_documenso_signing.yaml``.
        """
        self.run_yaml_scenario("test_data_financial_budget_documenso_signing.yaml")
