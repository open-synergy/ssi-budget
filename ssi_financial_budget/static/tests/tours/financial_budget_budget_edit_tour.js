odoo.define("ssi_financial_budget.financial_budget_budget_edit_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/financial_budget_budget/02-edit.md
    tour.register(
        "ssi_financial_budget_financial_budget_budget_edit",
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
                trigger: ".o_data_row:contains(TOUR FB EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Financial budget form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // 14.0: an already-existing record opens readonly; Edit is
            // required before any field can be changed.
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Select the Financial Budget Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR FB TYPE 2",
            },
            {
                content: "Pick the Financial Budget Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FB TYPE 2)",
                in_modal: false,
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Type shows the new value",
                trigger:
                    ".o_form_view.o_form_readonly .o_field_widget[name='type_id']:contains(TOUR FB TYPE 2)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
