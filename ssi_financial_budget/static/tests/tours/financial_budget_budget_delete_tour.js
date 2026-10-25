odoo.define("ssi_financial_budget.financial_budget_budget_delete_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/financial_budget_budget/03-delete.md
    tour.register(
        "ssi_financial_budget_financial_budget_budget_delete",
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
                trigger: ".o_data_row:contains(TOUR FB DELETE) .o_data_cell:first",
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
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // Match the exact label so ":contains(Delete)" never picks
                // another menu item.
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Click the Financial Budgets breadcrumb",
                trigger: ".breadcrumb-item.o_back_button a:contains(Financial Budgets)",
                extra_trigger: "body:not(:has(.modal))",
            },
            {
                content: "Deleted budget no longer appears in the list",
                trigger: ".o_list_view:not(:has(.o_data_row:contains(TOUR FB DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
