// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_analytic_budget_operating_unit.analytic_budget_budget_create_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/analytic_budget_budget/01-create.md (E1 delta -- Additional
        // Fields). Navigation (open menu -> New) is taken from the base IK
        // ssi_analytic_budget/docs/analytic_budget_budget/01-create.md Flow steps
        // 1-2 (backing = base IK + delta IK). The delta assertion comes from this
        // module's own IK: the Operating Unit field is visible on the create form
        // for a user in the operating_unit.group_multi_operating_unit group. The
        // tour stops there; it does not fill or save (E1 delta-only).
        tour.register(
            "ssi_analytic_budget_operating_unit_analytic_budget_budget_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Base Flow 1 - Open the Cost Accounting > Budget > Analytic Budgets menu.
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
                    // The Analytic Budgets menu is the landing action of the app,
                    // so the click reloads an identical action. Mark the stale
                    // control panel so the gate below only passes after remount.
                    content: "Open the Analytic Budgets menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_analytic_budget.analytic_budget_budget_menu"]',
                    run: function (actions) {
                        $(".o_control_panel").addClass("oe_tour_stale");
                        actions.click();
                    },
                },
                {
                    content: "Analytic Budgets list is displayed",
                    trigger:
                        ".o_control_panel:not(.oe_tour_stale) " +
                        ".breadcrumb-item.active:contains(Analytic Budgets)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                // Base Flow 2 - Click the New button. (14.0: "Create")
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
                // Delta assertion - the Operating Unit field is visible on the
                // create form. The tour stops here (E1 delta-only).
                {
                    content: "Operating Unit field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable " +
                        ".o_field_widget[name='operating_unit_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
