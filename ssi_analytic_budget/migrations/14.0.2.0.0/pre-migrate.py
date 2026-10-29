# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.7.11 -> 14.0.2.0.0
#
# Changes: ``analytic_budget.detail`` gets the stored computed field
#          ``amount_realized``, read from the ``realization_budgeted`` SQL
#          view. Odoo computes a new stored field while it creates the
#          column, which happens before the new SQL view exists and is
#          slow on a big database. The empty column is created here so
#          that Odoo skips that computation; the post migration fills it.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Create the empty ``amount_realized`` column of the budget details.

    Runs in the ``pre`` stage, before the models are loaded, so Odoo
    finds the column and does not compute it while the SQL views of the
    module are still the old ones.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; adds the column when it is missing
    """
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE analytic_budget_detail
        ADD COLUMN IF NOT EXISTS amount_realized numeric
        """,
    )
    _logger.info("Prepared the empty amount_realized column of budget details.")
