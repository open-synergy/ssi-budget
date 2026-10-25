odoo.define("ssi_analytic_budget.analytic_budget_budget_terminate_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/analytic_budget_budget/11-terminate.md
    tour.register(
        "ssi_analytic_budget_analytic_budget_budget_terminate",
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
                // The Analytic Budgets menu is the landing action of the app, so
                // the click reloads an identical action. Mark the stale control
                // panel so the gate below only passes after the remount.
                content: "Open the Analytic Budgets menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_analytic_budget.analytic_budget_budget_menu"]',
                run: function (actions) {
                    $(".o_control_panel").addClass("oe_tour_stale");
                    actions.click();
                },
            },
            {
                content: "Analytic Budgets list is displayed",
                trigger:
                    ".o_control_panel:not(.oe_tour_stale) .breadcrumb-item.active:contains(Analytic Budgets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Open the analytic budget",
                trigger: ".o_data_row:contains(TOUR AB TERMINATE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Analytic budget form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // It is an action button whose DOM name is a numeric action id,
            // so it is targeted by its label.
            {
                content: "Click the Terminate button",
                trigger: ".o_statusbar_buttons button:enabled:contains(Terminate)",
                extra_trigger: ".o_form_view",
            },
            // When a modal is open the tour scopes triggers INSIDE it.
            {
                content: "The reason wizard is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Select the reason",
                trigger:
                    ".o_field_widget[name='terminate_reason_id'] .o_radio_item label:contains(TOUR AB TERMINATE REASON)",
            },
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
            },
            {
                content: "Status is Terminated",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='terminate'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
