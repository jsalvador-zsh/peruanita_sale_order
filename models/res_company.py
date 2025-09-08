from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    # Información específica de la empresa para cotizaciones
    company_ruc = fields.Char(
        string='RUC',
        help='Registro Único de Contribuyentes de la empresa'
    )
    
    detailed_address = fields.Text(
        string='Dirección Detallada',
        help='Dirección completa y detallada para cotizaciones'
    )
    
    # Términos y condiciones estándar
    standard_delivery_terms = fields.Text(
        string='Términos de Entrega Estándar',
        default='Puesto en almacén del cliente',
        help='Términos de entrega que aparecen por defecto en cotizaciones'
    )
    
    standard_payment_terms = fields.Text(
        string='Términos de Pago Estándar',
        default='De acuerdo a lo indicado en las Especificaciones Técnicas y/o bases de licitación.',
        help='Términos de pago estándar para cotizaciones'
    )
    
    standard_warranty_terms = fields.Text(
        string='Términos de Garantía Estándar',
        default='Tiempo de vida útil del producto.',
        help='Términos de garantía que aparecen por defecto'
    )
    
    # Texto de disclaimer para pagos
    payment_disclaimer = fields.Html(
        string='Disclaimer de Pagos',
        default='''<p>Todo pago debe ser realizado únicamente a través de depósitos y/o transferencias en nuestras cuentas bancarias a nombre de la empresa.</p>''',
        help='Texto que aparece en las cotizaciones sobre métodos de pago'
    )
    
    # Texto de introducción para cotizaciones
    quotation_intro_text = fields.Html(
        string='Texto de Introducción',
        default='''<p>Nos es grato dirigirnos a Usted, para saludarlo cordialmente a nombre de la Empresa, y por medio de la presente hacemos llegar nuestra cotización de acuerdo a la información remitida según el siguiente detalle:</p>''',
        help='Texto de introducción que aparece en las cotizaciones'
    )
    
    # Texto de condiciones generales
    general_conditions_text = fields.Html(
        string='Condiciones Generales',
        default='''<p>Dicha cotización es a todo costo, incluye todos los tributos, seguros, transportes, inspecciones, pruebas y de ser el caso, los costos laborales respectivos, conforme a la legislación vigente, así como cualquier otro concepto que sea aplicable y que pueda incidir sobre el valor del servicio a contratar.</p>
        <p>Asimismo, confirmamos que la presente cotización cumple con todos los requerimientos establecidos en las Especificaciones técnicas remitidos.</p>''',
        help='Condiciones generales que aparecen en las cotizaciones'
    )
    
    # Método para obtener el saludo personalizado
    def get_greeting_text(self):
        """Retorna el texto de saludo personalizado con datos de la empresa"""
        company_name = self.name or "LA EMPRESA"
        ruc = f"RUC: {self.company_ruc}" if self.company_ruc else ""
        address = f"con domicilio: {self.detailed_address}" if self.detailed_address else ""
        
        return f"Nos es grato dirigirnos a Usted, para saludarlo cordialmente a nombre de la Empresa {company_name}, {ruc}, {address}"