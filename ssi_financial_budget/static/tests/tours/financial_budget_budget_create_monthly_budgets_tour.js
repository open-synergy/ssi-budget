odoo.define(
    "ssi_financial_budget.financial_budget_budget_create_monthly_budgets_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/financial_budget_budget/15-create-monthly-budgets.md
        tour.register(
            "ssi_financial_budget_financial_budget_budget_create_monthly_budgets",
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
                    // The Financial Budgets menu is the landing action of the app, so
                    // the click reloads an identical action. Mark the stale control
                    // panel so the gate below only passes after the remount.
                    content: "Open the Financial Budgets menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_financial_budget.financial_budget_budget_menu"]',
                    run: function (actions) {
                        $(".o_control_panel").addClass("oe_tour_stale");
                        actions.click();
                    },
                },
                {
                    content: "Financial Budgets list is displayed",
                    trigger:
                        ".o_control_panel:not(.oe_tour_stale) .breadcrumb-item.active:contains(Financial Budgets)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Open the yearly financial budget",
                    trigger: ".o_data_row:contains(TOUR FB YEAR) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Financial budget form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Open the Monthly Budgets tab",
                    trigger: ".o_notebook .nav-link:contains(Monthly Budgets)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Click the Create Monthly Budgets button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_create_monthly_budgets']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // The list is empty before the action runs, so a data row can
                    // only appear once the monthly budgets have been created.
                    content: "Monthly budgets are listed in Draft status",
                    trigger:
                        ".o_field_widget[name='child_ids'] .o_data_row:contains(Draft)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The yearly budget stays In Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    extra_trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
