/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_analytic_budget_work_log.analytic_budget_budget_create_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/analytic_budget_budget/01-create.md
        // Delta tour: the navigation is retraced from the base work instruction
        // (Flow steps 1-2); the only assertion is that the Work Log tab added by
        // this module is displayed on the create form.
        tour.register(
            "ssi_analytic_budget_work_log_analytic_budget_budget_create",
            {
                test: true,
                url: "/web",
            },
            [
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
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Open the Work Log tab",
                    trigger: ".o_notebook .nav-link:contains(Work Log)",
                },
                {
                    content: "Estimation is displayed",
                    trigger:
                        ".o_notebook .tab-pane.active .o_form_label:contains(Estimation)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Total is displayed",
                    trigger:
                        ".o_notebook .tab-pane.active .o_form_label:contains(Total)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Remaining is displayed",
                    trigger:
                        ".o_notebook .tab-pane.active .o_form_label:contains(Remaining)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Excess is displayed",
                    trigger:
                        ".o_notebook .tab-pane.active .o_form_label:contains(Excess)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
