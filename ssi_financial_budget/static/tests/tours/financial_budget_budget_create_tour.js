odoo.define("ssi_financial_budget.financial_budget_budget_create_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/financial_budget_budget/01-create.md
    tour.register(
        "ssi_financial_budget_financial_budget_budget_create",
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
            // Flow 2 - Click the New button. (14.0: "Create")
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
                content: "Select the Financial Budget Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR FB TYPE 1",
            },
            {
                content: "Pick the Financial Budget Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FB TYPE 1)",
                in_modal: false,
            },
            {
                content: "Select the Period",
                trigger: ".o_field_many2one[name='period_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR FB CREATE",
            },
            {
                content: "Pick the Period from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FB CREATE)",
                in_modal: false,
            },
            // Flow 4 - Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            // Post-Condition - A new budget is created in Draft.
            {
                content: "Budget is saved and in Draft status",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
