# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.6.4 -> 14.0.2.0.0
#
# Changes: drop the columns and the field metadata left by
#          ``mixin.product_line_price`` on ``financial_budget.detail``.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_TABLE = "financial_budget_detail"
_MODEL = "financial_budget.detail"
_OLD_FIELDS = [
    "name",
    "sequence",
    "note",
    "product_id",
    "product_category_id",
    "pricelist_id",
    "price_unit",
    "uom_quantity",
    "uom_id",
    "quantity",
    "price_subtotal",
    "standard_price_unit",
    "standard_price_subtotal",
    "currency_id",
]


@openupgrade.migrate()
def migrate(env, version):
    """Drop the old mixin columns and field metadata.

    Runs in the ``post`` stage, after the SQL views that read the old
    columns were recreated on the new definition. Every step checks the
    current state first, so running the script again is harmless.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; removes columns and ``ir.model.fields`` rows
    """
    cr = env.cr
    columns = [
        column
        for column in _OLD_FIELDS
        if openupgrade.column_exists(cr, _TABLE, column)
    ]
    if columns:
        openupgrade.drop_columns(cr, [(_TABLE, column) for column in columns])
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_fields_selection
        WHERE field_id IN (
            SELECT id FROM ir_model_fields
            WHERE model = %s AND name IN %s
        )
        """,
        (_MODEL, tuple(_OLD_FIELDS)),
    )
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_data
        WHERE model = 'ir.model.fields' AND res_id IN (
            SELECT id FROM ir_model_fields
            WHERE model = %s AND name IN %s
        )
        """,
        (_MODEL, tuple(_OLD_FIELDS)),
    )
    openupgrade.logged_query(
        cr,
        "DELETE FROM ir_model_fields WHERE model = %s AND name IN %s",
        (_MODEL, tuple(_OLD_FIELDS)),
    )
    _logger.info("Dropped %s old column(s) of %s.", len(columns), _TABLE)
