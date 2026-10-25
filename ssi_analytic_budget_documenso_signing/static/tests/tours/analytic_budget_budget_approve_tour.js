// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_analytic_budget_documenso_signing.analytic_budget_budget_approve_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/analytic_budget_budget/05-approve.md (E2a delta -- Modified
        // Flow)
        // Navigation (open menu -> open record) is retraced from the base IK
        // ssi_analytic_budget/docs/analytic_budget_budget/05-approve.md Flow
        // steps 1-2. The delta assertion, anchored at base Flow step 2, verifies
        // the Signature Requests tab injected because
        // `_documenso_signing_create_page = True`, then stops. Base Flow steps 3-4
        // (Approve / OK) are covered by the base module tour and are not repeated
        // here; this module does not change them.
        tour.register(
            "ssi_analytic_budget_documenso_signing_analytic_budget_budget_approve",
            {
                test: true,
                url: "/web",
            },
            [
                // Base Flow 1 - Open the Cost Accounting > Budget > Analytic
                // Budgets menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Cost Accounting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
                },
                {
                    content: "Open the Budget menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_root_budget"]',
                },
                {
                    // The Analytic Budgets menu is the landing action of the app,
                    // so the click reloads an identical action. Mark the stale
                    // control panel so the gate below only passes after remount.
                    content: "Open the Analytic Budgets menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_analytic_budget.analytic_budget_budget_menu"]',
                    run: function (actions) {
                        $(".o_control_panel").addClass("oe_tour_stale");
                        actions.click();
                    },
                },
                {
                    content: "Analytic Budgets list is displayed",
                    trigger:
                        ".o_control_panel:not(.oe_tour_stale) " +
                        ".breadcrumb-item.active:contains(Analytic Budgets)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                // Base Flow 2 - Open the record to approve.
                {
                    content: "Open the analytic budget",
                    trigger:
                        ".o_data_row:contains(TOUR AB DS APPROVE) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Analytic budget form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                // Delta assertion (anchor: base Flow step 2) - the Signature
                // Requests tab is present on the form.
                {
                    content: "Open the Signature Requests tab",
                    trigger: ".o_notebook .nav-link:contains(Signature Requests)",
                },
                {
                    content:
                        "Signature Requests tab shows the New Signing Request button",
                    trigger:
                        ".o_notebook .tab-pane.active " +
                        "button[name='action_create_signing_request']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
