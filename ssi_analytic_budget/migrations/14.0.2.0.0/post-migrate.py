# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.7.11 -> 14.0.2.0.0
#
# Changes: the realization of the analytic budgets now consolidates the
#          descendant analytic accounts and is limited to the periods of
#          the details, so the stored compute logic changed. The stored
#          values of the existing records still hold the old logic.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute the stored realization of all analytic budgets.

    Runs in the ``post`` stage, once the new SQL views exist. The
    realized amount of every detail and the stored realization amounts
    of every budget are rebuilt with ``add_to_compute`` and ``flush``.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; refreshes the stored realization
    """
    Budget = env["analytic_budget.budget"]
    Detail = env["analytic_budget.detail"]
    budgets = Budget.with_context(active_test=False).search([])
    details = Detail.with_context(active_test=False).search([])
    budget_fields = Budget._get_realization_field_names()
    for field_name in budget_fields:
        env.add_to_compute(Budget._fields[field_name], budgets)
    env.add_to_compute(Detail._fields["amount_realized"], details)
    details.flush(["amount_realized"])
    budgets.flush(budget_fields)
    _logger.info(
        "Recomputed the realization of %s budget(s) and %s detail(s).",
        len(budgets),
        len(details),
    )
