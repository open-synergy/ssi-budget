odoo.define("ssi_analytic_budget.analytic_budget_budget_create_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/analytic_budget_budget/01-create.md
    tour.register(
        "ssi_analytic_budget_analytic_budget_budget_create",
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
                content: "Select the Analytic Budget Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR AB TYPE 1",
            },
            {
                content: "Pick the Analytic Budget Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AB TYPE 1)",
                in_modal: false,
            },
            {
                content: "Select the Analytic Account",
                trigger: ".o_field_many2one[name='analytic_account_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR AB CREATE",
            },
            {
                content: "Pick the Analytic Account from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AB CREATE)",
                in_modal: false,
            },
            // Flow 3 - Parent Budget is an optional header field; it stays empty.
            {
                content: "Parent Budget field is available and optional",
                trigger: ".o_field_many2one[name='parent_id']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // Flow 4 - The planned lines, including their optional
            // multiplier factors, are optional and not exercised here.
            // Flow 5 - Click Save.
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
