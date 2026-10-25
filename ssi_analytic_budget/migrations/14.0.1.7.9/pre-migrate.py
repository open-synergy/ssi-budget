# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.7.8 -> 14.0.1.7.9
#
# Changes: the workflow groups of ``analytic_budget.budget`` were renamed
#          to follow the ``<model>_viewer/user/validator_group`` naming
#          pattern. Only the XML IDs change; the ``res.groups`` rows,
#          their users and implied groups stay untouched.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_XMLID_RENAMES = [
    (
        "ssi_analytic_budget.analytic_budget_viewer_group",
        "ssi_analytic_budget.analytic_budget_budget_viewer_group",
    ),
    (
        "ssi_analytic_budget.analytic_budget_user_group",
        "ssi_analytic_budget.analytic_budget_budget_user_group",
    ),
    (
        "ssi_analytic_budget.analytic_budget_validator_group",
        "ssi_analytic_budget.analytic_budget_budget_validator_group",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    """Rename the workflow group XML IDs of ``analytic_budget.budget``.

    Runs in the ``pre`` stage, before the data files are loaded, so the
    existing ``res.groups`` rows are adopted under their new XML IDs
    instead of being recreated as duplicate groups.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``ir_model_data`` rows
    """
    openupgrade.rename_xmlids(env.cr, _XMLID_RENAMES)
    _logger.info(
        "Renamed %s workflow group XML ID(s) of analytic_budget.budget.",
        len(_XMLID_RENAMES),
    )
