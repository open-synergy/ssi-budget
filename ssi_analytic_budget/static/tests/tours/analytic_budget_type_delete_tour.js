odoo.define("ssi_analytic_budget.analytic_budget_type_delete_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/analytic_budget_type/03-delete.md
    tour.register(
        "ssi_analytic_budget_analytic_budget_type_delete",
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
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            // "Budget" (level 3) has children, so it renders as a non-clickable
            // dropdown header and is skipped; only the leaf item gets a step.
            {
                content: "Open the Analytic Budget Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_analytic_budget.analytic_budget_type_menu"]',
            },
            {
                content: "Analytic Budget Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Analytic Budget Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // The Action menu only renders once a row is selected.
            {
                content: "Select the row",
                trigger:
                    ".o_data_row:contains(TOUR ABT DELETE) .o_list_record_selector input",
                run: "click",
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // Match the exact label so ":contains(Delete)" never picks another
                // menu item.
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
                content: "Deleted record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR ABT DELETE)))",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
