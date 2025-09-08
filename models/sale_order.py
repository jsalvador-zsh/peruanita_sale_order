from odoo import models, fields, api
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Campo para el formato de numeración personalizado
    custom_quotation_number = fields.Char(
        string='Número de Cotización',
        help='Formato: COTIZACIÓN XXXX/YYYY-PE',
        readonly=True,
        copy=False
    )
    
    # Información del cliente específica
    client_ruc = fields.Char(
        string='RUC del Cliente',
        help='RUC de la entidad o empresa cliente'
    )
    
    client_address_detail = fields.Text(
        string='Dirección Detallada del Cliente',
        help='Dirección completa y detallada del cliente'
    )
    
    # Asunto de la cotización
    quotation_subject = fields.Text(
        string='Asunto',
        help='Asunto específico de la cotización'
    )
    
    # Mejoras a especificaciones técnicas
    technical_improvements = fields.Html(
        string='Mejoras a las Especificaciones Técnicas',
        help='Factores de evaluación y mejoras técnicas'
    )
    
    # Condiciones comerciales
    delivery_place = fields.Char(
        string='Lugar de Entrega',
        default='Puesto en almacén del cliente'
    )
    
    warranty_terms = fields.Text(
        string='Términos de Garantía',
        default='Tiempo de vida útil del producto'
    )
    
    # Override del método create para generar numeración personalizada y configurar validity_date
    @api.model
    def create(self, vals):
        if vals.get('custom_quotation_number', '/') == '/':
            vals['custom_quotation_number'] = self._generate_custom_quotation_number()
        
        # Configurar validity_date si no está definida (usar campo nativo)
        if not vals.get('validity_date'):
            days = self.env.company.quotation_validity_days if hasattr(self.env.company, 'quotation_validity_days') else 30
            vals['validity_date'] = fields.Date.today() + timedelta(days=days)
        
        return super(SaleOrder, self).create(vals)
    
    def _generate_custom_quotation_number(self):
        """Genera el número de cotización en formato COTIZACIÓN XXXX/YYYY-PE"""
        current_year = datetime.now().year
        
        # Buscar el último número de cotización del año actual
        last_quotation = self.search([
            ('custom_quotation_number', 'like', f'COTIZACIÓN %/{current_year}-PE')
        ], order='custom_quotation_number desc', limit=1)
        
        if last_quotation and last_quotation.custom_quotation_number:
            # Extraer el número secuencial
            try:
                number_part = last_quotation.custom_quotation_number.split('/')[0].split(' ')[-1]
                next_number = int(number_part) + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        return f'COTIZACIÓN {next_number:04d}/{current_year}-PE'
    
    # Método para obtener la fecha formateada en español
    def get_formatted_date(self):
        """Retorna la fecha en formato español: 'Arequipa, DD de Mes del YYYY'"""
        if self.date_order:
            months_spanish = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }
            
            date = fields.Datetime.from_string(self.date_order)
            month_name = months_spanish.get(date.month, '')
            
            return f"Arequipa, {date.day} de {month_name} del {date.year}"
        return ""
    
    # Método para obtener días de vigencia de la cotización
    def get_quotation_validity_days(self):
        """Retorna los días de vigencia basado en validity_date"""
        if self.validity_date:
            today = fields.Date.today()
            delta = self.validity_date - today
            return max(0, delta.days)
        return 0
    
    # Método para obtener información de contacto del partner
    def get_contact_info(self):
        """Retorna información de contacto del cliente"""
        contact_info = {}
        if self.partner_id:
            # Teléfonos
            phones = []
            if self.partner_id.phone:
                phones.append(self.partner_id.phone)
            if self.partner_id.mobile:
                phones.append(self.partner_id.mobile)
            contact_info['phones'] = ' - '.join(phones) if phones else ''
            
            # Email
            contact_info['email'] = self.partner_id.email or ''
            
        return contact_info
    
    # Método para obtener cuentas bancarias de la empresa
    def get_company_bank_accounts(self):
        """Retorna las cuentas bancarias de la empresa organizadas por tipo"""
        bank_accounts = []
        
        # Obtener cuentas bancarias de la empresa
        company_banks = self.env['res.partner.bank'].search([
            ('partner_id', '=', self.company_id.partner_id.id)
        ])
        
        for bank in company_banks:
            bank_name = bank.bank_id.name if bank.bank_id else 'Banco'
            
            # Usar el campo entity_type personalizado
            if bank.entity_type == 'public':
                bank_type = 'Entidades Públicas'
            elif bank.entity_type == 'private':
                bank_type = 'Entidades Privadas'
            else:
                bank_type = 'General'
            
            bank_accounts.append({
                'type': bank_type,
                'bank': bank_name,
                'account': bank.acc_number,
                'cci': bank.cci_number or ''
            })
        
        return bank_accounts
    
    # Método para obtener el total en palabras (opcional)
    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for record in self:

            record.amount_total_words = f"SON: {record.amount_total} SOLES"
    
    amount_total_words = fields.Char(
        string='Monto Total en Palabras',
        compute='_compute_amount_total_words',
        store=True
    )