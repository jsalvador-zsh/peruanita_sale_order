{
    'name': 'Personalización Módulo de Ventas - PERUANITA',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Personalización del módulo de ventas para formato de cotizaciones específico',
    'description': """
        Módulo de personalización para el sistema de ventas que incluye:
        - Campos personalizados en cotizaciones
        - Formato específico de numeración
        - Plantilla de PDF personalizada para cotizaciones
        - Campos adicionales para productos (marca, especificaciones)
        - Información comercial específica de la empresa
        - Cuentas bancarias y condiciones comerciales
    """,
    'author': 'Juan Salvador',
    'website': 'https://jsalvador.dev',
    'depends': [
        'base',
        'sale',
        'sale_management',
        'account',
        'peruanita_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/res_partner_bank_views.xml',
        'views/sale_order_views.xml',
        'views/res_company_views.xml',
        'reports/report_actions.xml',
        'reports/sale_order_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}