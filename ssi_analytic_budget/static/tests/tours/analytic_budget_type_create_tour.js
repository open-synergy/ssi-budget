odoo.define("ssi_analytic_budget.analytic_budget_type_create_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/analytic_budget_type/01-create.md
    tour.register(
        "ssi_analytic_budget_analytic_budget_type_create",
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
                content: "Fill in the name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR ABT CREATE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            {
                content: "Open the Revenue Settings tab",
                trigger: ".o_notebook .nav-link:contains(Revenue Settings)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Click Add a line on the Revenue Settings tab",
                trigger: ".tab-pane.active .o_field_x2many_list_row_add a",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Select the Account",
                trigger:
                    ".tab-pane.active .o_selected_row .o_field_many2one[name='account_id'] input",
                run: "text TOUR AB REV ACC",
            },
            {
                content: "Pick the Account from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AB REV ACC)",
                in_modal: false,
            },
            {
                content: "Open the Cost Settings tab",
                trigger: ".o_notebook .nav-link:contains(Cost Settings)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Click Add a line on the Cost Settings tab",
                trigger: ".tab-pane.active .o_field_x2many_list_row_add a",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Select the Account",
                trigger:
                    ".tab-pane.active .o_selected_row .o_field_many2one[name='account_id'] input",
                run: "text TOUR AB COST ACC",
            },
            {
                content: "Pick the Account from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AB COST ACC)",
                in_modal: false,
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
