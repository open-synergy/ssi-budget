import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-budget",
    description="Meta package for open-synergy-ssi-budget Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_analytic_budget',
        'odoo14-addon-ssi_analytic_budget_work_log',
        'odoo14-addon-ssi_financial_budget',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
