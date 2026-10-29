# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.6.4 -> 14.0.2.0.0
#
# Changes: ``financial_budget.detail`` no longer inherits
#          ``mixin.product_line_price``; the line holds an ``amount``.
#          The old ``price_subtotal`` is copied into ``amount``.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_TABLE = "financial_budget_detail"


@openupgrade.migrate()
def migrate(env, version):
    """Copy the line subtotal into the new ``amount`` column.

    Runs in the ``pre`` stage, before the ORM loads the new model
    definition. Does nothing when ``price_subtotal`` no longer exists,
    so running the script again is harmless.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; adds and fills the ``amount`` column
    """
    cr = env.cr
    if not openupgrade.column_exists(cr, _TABLE, "price_subtotal"):
        _logger.info("price_subtotal not found, nothing to copy.")
        return
    if not openupgrade.column_exists(cr, _TABLE, "amount"):
        openupgrade.logged_query(
            cr,
            "ALTER TABLE financial_budget_detail " "ADD COLUMN amount numeric",
        )
    openupgrade.logged_query(
        cr,
        "UPDATE financial_budget_detail " "SET amount = COALESCE(price_subtotal, 0)",
    )
