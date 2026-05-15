import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-ssi-budget",
    description="Meta package for open-synergy-ssi-budget Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-ssi_analytic_budget',
        'odoo11-addon-ssi_financial_budget',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
