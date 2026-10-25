odoo.define("ssi_analytic_budget.analytic_budget_type_edit_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/analytic_budget_type/02-edit.md
    tour.register(
        "ssi_analytic_budget_analytic_budget_type_edit",
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
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR ABT EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
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
                content: "Change the name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR ABT EDITED",
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Name shows the new value",
                trigger:
                    ".o_form_view.o_form_readonly .o_field_widget[name='name']:contains(TOUR ABT EDITED)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
