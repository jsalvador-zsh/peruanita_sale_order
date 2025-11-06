from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    # ============ CONFIGURACIÓN PERUANITA ============
    peruanita_ruc = fields.Char(
        string='RUC Peruanita',
        help='RUC de la empresa Peruanita'
    )
    
    peruanita_address = fields.Text(
        string='Dirección Peruanita',
        help='Dirección completa de Peruanita'
    )
    
    peruanita_email = fields.Char(
        string='Email Peruanita',
        help='Email de contacto Peruanita'
    )
    
    peruanita_phone = fields.Char(
        string='Teléfono Peruanita',
        help='Teléfono de contacto Peruanita'
    )
    
    peruanita_intro_text = fields.Html(
        string='Texto Introducción Peruanita',
        default='''<p>Nos es grato dirigirnos a Usted, para saludarlo cordialmente a nombre de la Empresa PERUANITA, y por medio de la presente hacemos llegar nuestra cotización.</p>'''
    )
    
    peruanita_conditions_text = fields.Html(
        string='Condiciones Generales Peruanita',
        default='''<p>Dicha cotización es a todo costo, incluye todos los tributos, seguros, transportes, inspecciones y pruebas.</p>'''
    )

    # ============ CONFIGURACIÓN GIBBOR ============
    gibbor_logo = fields.Binary(
        string='Logo Gibbor',
        help='Logo de la empresa Gibbor para cotizaciones'
    )
    
    gibbor_ruc = fields.Char(
        string='RUC Gibbor',
        default='20612492639',
        help='RUC de la empresa Gibbor'
    )
    
    gibbor_address = fields.Text(
        string='Dirección Gibbor',
        default='Cal. Mariano Melgar nro. 621 dpto. 101 urb. La Libertad Cerro Colorado- Arequipa',
        help='Dirección completa de Gibbor'
    )
    
    gibbor_email = fields.Char(
        string='Email Gibbor',
        default='administracion@gibboralimentos.com',
        help='Email de contacto Gibbor'
    )
    
    gibbor_phone = fields.Char(
        string='Teléfono Gibbor',
        help='Teléfono de contacto Gibbor'
    )
    
    gibbor_manager_name = fields.Char(
        string='Gerente Gibbor',
        default='Charo Yohany Huamán Bacón',
        help='Nombre del gerente general de Gibbor'
    )
    
    gibbor_intro_text = fields.Html(
        string='Texto Introducción Gibbor',
        default='''<p>lo saluda y a la vez hacerles llegar nuestra cotización referente a nuestro producto:</p>'''
    )
    
    # ============ CONFIGURACIÓN CORPEALIM ============
    corpealim_logo = fields.Binary(
        string='Logo Corpealim',
        help='Logo de la empresa Corpealim para cotizaciones'
    )
    
    corpealim_ruc = fields.Char(
        string='RUC Corpealim',
        default='2045557928',
        help='RUC de la empresa Corpealim'
    )
    
    corpealim_address = fields.Text(
        string='Dirección Corpealim',
        default='Urbanización Challapampa Mza. LL Lt. 2, Dpto. 802, Cerro Colorado, Departamento y Provincia de Arequipa',
        help='Dirección completa de Corpealim'
    )
    
    corpealim_email = fields.Char(
        string='Email Corpealim',
        default='corpealim@gmail.com',
        help='Email de contacto Corpealim'
    )
    
    corpealim_phone = fields.Char(
        string='Teléfono Corpealim',
        help='Teléfono de contacto Corpealim'
    )
    
    corpealim_manager_name = fields.Char(
        string='Gerente Corpealim',
        default='ROBERTO SCOCCO',
        help='Nombre del gerente general de Corpealim'
    )
    
    corpealim_intro_text = fields.Html(
        string='Texto Introducción Corpealim',
        default='''<p>lo saluda y a la vez hacerles llegar nuestra cotización referente a nuestro producto:</p>'''
    )
    
    corpealim_bank_info = fields.Text(
        string='Información Bancaria Corpealim',
        default='Banco BBVA Continental 0011-0778-0100018684-89, cuenta CCI: 011-778-000100018684-89',
        help='Información de cuenta bancaria para Corpealim'
    )