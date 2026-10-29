.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Financial Budget
================

Plan a financial budget per account. Each budget detail line only holds
an account, a direction (revenue or cost) and an amount. The account
must be one of the allowed accounts of the budget type and can be used
only once per budget.

The realization is the sum of the posted journal items of the budget
accounts, dated within the budget period and belonging to the budget
company. It is always live and does not depend on the state of the
budget. Each item is signed by the direction of the account: credit
minus debit for revenue, debit minus credit for cost. An account
without a detail line is revenue when it is an income account and cost
otherwise.

A budget is either *Yearly* or *Monthly*. A monthly budget uses a fiscal
month period. A yearly budget uses a period of the *Yearly Range Type*
configured per company in the Financial Budget settings. A yearly budget
can be broken down into monthly budgets, set as the *Parent Budget* of
each monthly budget. For each account and direction, the monthly budgets
that are not cancelled or rejected cannot exceed the amount of the
parent budget. The *Create Monthly Budgets* button of an open yearly
budget creates one draft monthly budget per fiscal month and divides
the amounts equally.

The budget header shows the planned, realized and difference amounts of
revenue and cost separately. The plain *Planned Amount*, *Realized
Amount* and *Diff Amount* are net: revenue minus cost.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-budget
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Financial Budget*
6.  Install the module

Work Instruction
================

* `Create Financial Budget Type <docs/financial_budget_type/01-create.html>`_
* `Edit Financial Budget Type <docs/financial_budget_type/02-edit.html>`_
* `Delete Financial Budget Type <docs/financial_budget_type/03-delete.html>`_
* `Deactivate Financial Budget Type <docs/financial_budget_type/04-deactivate.html>`_
* `Activate Financial Budget Type <docs/financial_budget_type/05-activate.html>`_
* `Create Financial Budget <docs/financial_budget_budget/01-create.html>`_
* `Edit Financial Budget <docs/financial_budget_budget/02-edit.html>`_
* `Delete Financial Budget <docs/financial_budget_budget/03-delete.html>`_
* `Confirm Financial Budget <docs/financial_budget_budget/04-confirm.html>`_
* `Approve Financial Budget <docs/financial_budget_budget/05-approve.html>`_
* `Reject Financial Budget <docs/financial_budget_budget/06-reject.html>`_
* `Finish Financial Budget <docs/financial_budget_budget/09-finish.html>`_
* `Cancel Financial Budget <docs/financial_budget_budget/10-cancel.html>`_
* `Terminate Financial Budget <docs/financial_budget_budget/11-terminate.html>`_
* `Restart Financial Budget <docs/financial_budget_budget/12-restart.html>`_
* `Restart Approval Process of Financial Budget <docs/financial_budget_budget/14-restart-approval.html>`_
* `Create Monthly Budgets of Financial Budget <docs/financial_budget_budget/15-create-monthly-budgets.html>`_

Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>


Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
