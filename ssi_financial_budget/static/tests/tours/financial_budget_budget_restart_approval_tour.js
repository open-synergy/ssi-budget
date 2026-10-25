odoo.define(
    "ssi_financial_budget.financial_budget_budget_restart_approval_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/financial_budget_budget/14-restart-approval.md
        tour.register(
            "ssi_financial_budget_financial_budget_budget_restart_approval",
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
                    content: "Open the financial budget",
                    trigger:
                        ".o_data_row:contains(TOUR FB RELOAD APPROVAL) .o_data_cell:first",
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
                    content: "Open the Approvals tab",
                    trigger: ".o_notebook .nav-link:contains(Approvals)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "The approval list is displayed",
                    trigger: ".o_field_widget[name='approval_ids'] .o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    // Mark the current approval rows: a restart removes them and builds
                    // new ones, so a row without the marker proves the restart ran.
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                    run: function (actions) {
                        $(".o_field_widget[name='approval_ids'] .o_data_row").addClass(
                            "oe_tour_stale"
                        );
                        actions.click();
                    },
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "The approval process has been rebuilt",
                    trigger:
                        ".o_field_widget[name='approval_ids'] .o_data_row:not(.oe_tour_stale)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
