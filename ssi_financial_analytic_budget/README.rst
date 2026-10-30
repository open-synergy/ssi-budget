.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Financial Budget - Analytic Budget
==================================

Glue module that keeps the analytic budgets of top level analytic accounts inside the
financial budget. It is installed automatically when both ``ssi_financial_budget`` and
``ssi_analytic_budget`` are installed, and neither module depends on the other.

For each company, account, direction and financial budget period, the total of the
counted analytic budget lines of top level analytic accounts must not exceed the
financial budget amount. The check runs when an analytic budget line is saved, when an
analytic budget is confirmed or restarted, and when a financial budget line is changed
or deleted. Analytic budgets of child analytic accounts are limited by their parent
budget and are not checked here.

Work Instruction
================

* `Analytic Budget <docs/analytic_budget_budget/index.html>`_
* `Financial Budget <docs/financial_budget_budget/index.html>`_

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-budget/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


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
