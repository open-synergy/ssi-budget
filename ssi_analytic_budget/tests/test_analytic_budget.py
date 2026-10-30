# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
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

    def test_analytic_budget_hierarchy(self):
        """Run the hierarchy view, action and parent to child scenarios."""
        self.run_yaml_scenario("test_data_analytic_budget_hierarchy.yaml")

    def test_analytic_budget_hierarchy_fields_view(self):
        """Return the hierarchy arch with its attributes and no total.

        Pure Python, triggers P1 (L-01) and P4 (L-08):
        ``fields_view_get`` returns a dict and ``action: call`` discards
        the returned value. The parent and child fixture feeds the
        roots and expand data of the view.
        """
        env = self.env(user=self.env.ref("base.user_admin"))
        budget_type = env["analytic_budget.type"].create(
            {"name": "AB HIER P1 TYPE", "code": "ABHP1"}
        )
        account_model = env["account.analytic.account"]
        parent_account = account_model.create({"name": "AB HIER P1 PARENT"})
        child_account = account_model.create(
            {"name": "AB HIER P1 CHILD", "parent_id": parent_account.id}
        )
        parent = env["analytic_budget.budget"].create(
            {
                "type_id": budget_type.id,
                "analytic_account_id": parent_account.id,
            }
        )
        child = env["analytic_budget.budget"].create(
            {
                "type_id": budget_type.id,
                "analytic_account_id": child_account.id,
                "parent_id": parent.id,
            }
        )
        self.assertFalse(parent.parent_id)
        self.assertEqual(parent.child_ids, child)
        self.assertEqual(child.parent_id, parent)
        result = env["analytic_budget.budget"].fields_view_get(view_type="hierarchy")
        arch = etree.fromstring(result["arch"])
        self.assertEqual(arch.tag, "hierarchy")
        self.assertEqual(arch.get("parent_field"), "parent_id")
        self.assertEqual(arch.get("child_field"), "child_ids")
        names = [node.get("name") for node in arch.findall("field")]
        self.assertEqual(
            names,
            [
                "name",
                "analytic_account_id",
                "state",
                "amount_planned_revenue",
                "amount_planned_cost",
                "amount_planned_pl",
                "amount_profit_realization",
            ],
        )
        for node in arch.iter():
            self.assertIsNone(node.get("sum"))
