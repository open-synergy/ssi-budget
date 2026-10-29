odoo.define(
    "ssi_analytic_budget.analytic_budget_budget_recompute_realization_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/analytic_budget_budget/15-recompute-realization.md
        tour.register(
            "ssi_analytic_budget_analytic_budget_budget_recompute_realization",
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
                    // The Analytic Budgets menu is the landing action of the app,
                    // so the click reloads an identical action. Mark the stale
                    // control panel so the gate below only passes after the
                    // remount.
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
                    trigger:
                        ".o_data_row:contains(TOUR AB RECOMPUTE) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Analytic budget form is displayed",
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
                    content: "Click Recompute Realization",
                    // Match the exact label so ":contains(Recompute)" never picks
                    // another menu item.
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $recompute = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return (
                                    $(this).text().trim() === "Recompute Realization"
                                );
                            }
                        );
                        $recompute[0].click();
                    },
                },
                // Post-Condition - the stored realization is rebuilt. The fixture
                // stores 0.00 on purpose, so 100.00 shows only after the action.
                {
                    content: "Revenue realization is recalculated",
                    trigger:
                        ".o_form_view .o_field_monetary[name='amount_revenue_realization']:contains(100.00)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
