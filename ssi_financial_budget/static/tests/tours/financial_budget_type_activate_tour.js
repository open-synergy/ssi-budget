odoo.define("ssi_financial_budget.financial_budget_type_activate_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/financial_budget_type/05-activate.md
    tour.register(
        "ssi_financial_budget_financial_budget_type_activate",
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
                content: "Open the Financial Budget Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_financial_budget.financial_budget_type_menu"]',
            },
            {
                content: "Financial Budget Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Financial Budget Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Open the Filters menu",
                trigger: ".o_search_options .o_filter_menu button",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Enable the Archived filter",
                trigger: ".o_filter_menu .dropdown-item:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Archived filter is applied and the record is listed",
                trigger: ".o_searchview_facet:contains(Archived)",
                extra_trigger: ".o_data_row:contains(TOUR FBT RESTORE)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // The Action menu only renders once a row is selected.
            {
                content: "Select the row",
                trigger:
                    ".o_data_row:contains(TOUR FBT RESTORE) .o_list_record_selector input",
                run: "click",
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Unarchive",
                // Match the exact label so a substring never picks another item.
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $item = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Unarchive";
                        }
                    );
                    $item[0].click();
                },
            },
            // Unarchive has no confirmation dialog.
            {
                content: "Unarchived record leaves the Archived list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR FBT RESTORE)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
