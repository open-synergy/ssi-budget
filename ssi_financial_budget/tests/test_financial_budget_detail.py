# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules import get_module_path
from odoo.tests import tagged

_MODULE = "ssi_financial_budget"
_VERSION_DIR = "14.0.2.0.0"
_MIXIN_COLUMNS = ["price_subtotal", "price_unit", "uom_quantity"]
_PRODUCT_FIELDS = [
    "product_id",
    "pricelist_id",
    "price_unit",
    "uom_quantity",
    "uom_id",
    "price_subtotal",
    "currency_id",
]


def _load_script(filename):
    """Load a migration script of this module from its file.

    :param filename: file name inside the versioned migrations directory
    :return: the loaded module object
    """
    path = os.path.join(get_module_path(_MODULE), "migrations", _VERSION_DIR, filename)
    spec = importlib.util.spec_from_file_location(
        "fb_" + filename.replace("-", "_").replace(".py", ""), path
    )
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    return script


@tagged("post_install", "-at_install")
class TestFinancialBudgetDetail(YamlTransactionCase):
    """Check the amount-only budget line and its migration scripts."""

    def test_fields_get_has_no_product_field(self):
        """Reject product and price fields on the budget line.

        Pure Python, trigger P1 (L-01): ``fields_get()`` is a method
        return value, which ``action: call`` drops.
        """
        fields_dict = self.env["financial_budget.detail"].fields_get()
        for name in _PRODUCT_FIELDS:
            self.assertNotIn(name, fields_dict)
        for name in ("account_id", "direction", "amount"):
            self.assertIn(name, fields_dict)

    def _create_detail(self):
        """Create a budget with one detail line through the ORM.

        :return: the created ``financial_budget.detail`` record
        """
        range_type = self.env["date.range.type"].create(
            {"name": "MIG FB RANGE TYPE", "fiscal_month": True}
        )
        period = self.env["date.range"].create(
            {
                "name": "MIG FB PERIOD",
                "type_id": range_type.id,
                "date_start": "2024-07-01",
                "date_end": "2024-07-31",
            }
        )
        budget_type = self.env["financial_budget.type"].create(
            {"name": "MIG FB TYPE", "code": "MIGFBT"}
        )
        budget = self.env["financial_budget.budget"].create(
            {"type_id": budget_type.id, "period_id": period.id}
        )
        account = self.env["account.account"].create(
            {
                "name": "MIG FB ACCOUNT",
                "code": "MIGFBA",
                "user_type_id": self.env.ref("account.data_account_type_revenue").id,
            }
        )
        return self.env["financial_budget.detail"].create(
            {
                "budget_id": budget.id,
                "account_id": account.id,
                "direction": "revenue",
                "amount": 0.0,
            }
        )

    def _columns(self):
        """Return the existing column names of the detail table.

        :return: set of column names
        """
        self.env.cr.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'financial_budget_detail'"
        )
        return {row[0] for row in self.env.cr.fetchall()}

    def test_migration_scripts(self):
        """Copy the old subtotal and drop the old columns, twice.

        Pure Python, trigger P10 (L-11): the scripts must be loaded from
        their files, which ``EVAL:`` cannot do. The legacy columns are
        recreated by hand, then both scripts are executed twice.
        """
        cr = self.env.cr
        detail = self._create_detail()
        cr.execute(
            "ALTER TABLE financial_budget_detail "
            "ADD COLUMN price_subtotal numeric, "
            "ADD COLUMN price_unit numeric, "
            "ADD COLUMN uom_quantity numeric"
        )
        cr.execute(
            "UPDATE financial_budget_detail SET price_subtotal = 777 " "WHERE id = %s",
            (detail.id,),
        )
        pre = _load_script("pre-migrate.py")
        post = _load_script("post-migrate.py")
        for _ in range(2):
            pre.migrate(cr, _VERSION_DIR)
        cr.execute(
            "SELECT amount FROM financial_budget_detail WHERE id = %s",
            (detail.id,),
        )
        self.assertEqual(cr.fetchone()[0], 777)
        for _ in range(2):
            post.migrate(cr, _VERSION_DIR)
        self.assertFalse(set(_MIXIN_COLUMNS) & self._columns())
        cr.execute(
            "SELECT amount FROM financial_budget_detail WHERE id = %s",
            (detail.id,),
        )
        self.assertEqual(cr.fetchone()[0], 777)
