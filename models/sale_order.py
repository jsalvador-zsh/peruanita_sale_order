from odoo import models, fields, api
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Selector de empresa para la cotización
    quotation_company_type = fields.Selection([
        ('peruanita', 'PERUANITA'),
        ('gibbor', 'GIBBOR'),
        ('corpealim', 'CORPEALIM')
    ], string='Tipo de Empresa', default='peruanita', required=True,
       help='Seleccione la empresa para esta cotización')
    
    # Campo para el formato de numeración personalizado
    custom_quotation_number = fields.Char(
        string='Número de Cotización',
        help='Formato: COTIZACIÓN XXXX/YYYY-PE',
        readonly=True,
        copy=False
    )
    
    distributor_id = fields.Many2one('res.partner', string='Distribuidor', tracking=True, help='Seleccione el distribuidior relacionado a la cotización')

    # ============ CAMPOS COMUNES ============
    client_ruc = fields.Char(
        string='RUC del Cliente',
        help='RUC de la entidad o empresa cliente'
    )
    
    client_address_detail = fields.Text(
        string='Dirección Detallada del Cliente',
        help='Dirección completa y detallada del cliente'
    )
    
    quotation_subject = fields.Text(
        string='Asunto',
        help='Asunto específico de la cotización'
    )
    
    delivery_place = fields.Char(
        string='Lugar de Entrega',
        default='Puesto en almacén del cliente'
    )
    
    warranty_terms = fields.Text(
        string='Términos de Garantía',
        default='Tiempo de vida útil del producto'
    )
    
    # ============ CAMPOS ESPECÍFICOS PERUANITA ============
    technical_improvements_peruanita = fields.Html(
        string='Mejoras a las Especificaciones Técnicas (Peruanita)',
        help='Factores de evaluación y mejoras técnicas para Peruanita'
    )
    
    # ============ CAMPOS ESPECÍFICOS GIBBOR ============
    technical_improvements_gibbor = fields.Html(
        string='Mejoras a las Especificaciones Técnicas (Gibbor)',
        help='Factores de evaluación para Gibbor'
    )
    
    gibbor_attention = fields.Char(
        string='Atención',
        help='Persona de atención en Gibbor'
    )
    
    # ============ CAMPOS ESPECÍFICOS CORPEALIM ============
    technical_improvements_corpealim = fields.Html(
        string='Mejoras a las Especificaciones Técnicas (Corpealim)',
        help='Factores de evaluación para Corpealim'
    )

    corpealim_attention = fields.Char(
        string='Atención',
        help='Persona de atención en Corpealim'
    )

    # ============ CONTROL DE VISUALIZACIÓN ============
    show_default_technical_table = fields.Boolean(
        string='Mostrar Tabla de Mejoras Técnicas por Defecto',
        default=True,
        help='Si está activado, muestra la tabla de mejoras técnicas estándar (DIGESA, HACCP). Si está desactivado, muestra el contenido del campo de condiciones generales.'
    )
    
    # Override del método create
    @api.model
    def create(self, vals):
        if vals.get('custom_quotation_number', '/') == '/':
            company_type = vals.get('quotation_company_type', 'peruanita')
            vals['custom_quotation_number'] = self._generate_custom_quotation_number(company_type)
        
        if not vals.get('validity_date'):
            days = self.env.company.quotation_validity_days if hasattr(self.env.company, 'quotation_validity_days') else 30
            vals['validity_date'] = fields.Date.today() + timedelta(days=days)
        
        return super(SaleOrder, self).create(vals)
    
    def _generate_custom_quotation_number(self, company_type='peruanita'):
        """Genera el número de cotización según el tipo de empresa"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Definir sufijos por empresa
        suffixes = {
            'peruanita': 'PE',
            'gibbor': 'GIBBOR',
            'corpealim': 'CORPEALIM'
        }
        
        suffix = suffixes.get(company_type, 'PE')
        
        # Buscar el último número según el tipo de empresa
        if company_type == 'corpealim':
            # CORPEALIM usa formato: COTIZACIÓN 0025-2025-05/CORPEALIM
            search_pattern = f'%-{current_year}-{current_month:02d}/{suffix}'
        elif company_type == 'gibbor':
            # GIBBOR usa formato: COTIZACIÓN 0006-2024-08/GIBBOR
            search_pattern = f'%-{current_year}-{current_month:02d}/{suffix}'
        else:
            # PERUANITA usa formato: COTIZACIÓN 0001/2025-PE
            search_pattern = f'%/{current_year}-{suffix}'
        
        last_quotation = self.search([
            ('quotation_company_type', '=', company_type),
            ('custom_quotation_number', 'like', search_pattern)
        ], order='custom_quotation_number desc', limit=1)
        
        if last_quotation and last_quotation.custom_quotation_number:
            try:
                # Extraer el número secuencial
                if company_type in ['gibbor', 'corpealim']:
                    # Formato: COTIZACIÓN 0025-2025-05/CORPEALIM
                    number_part = last_quotation.custom_quotation_number.split('-')[0].split(' ')[-1]
                else:
                    # Formato: COTIZACIÓN 0001/2025-PE
                    number_part = last_quotation.custom_quotation_number.split('/')[0].split(' ')[-1]
                next_number = int(number_part) + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Generar el número según el formato de cada empresa
        if company_type == 'corpealim':
            return f'COTIZACIÓN {next_number:04d}-{current_year}-{current_month:02d}/{suffix}'
        elif company_type == 'gibbor':
            return f'COTIZACIÓN {next_number:04d}-{current_year}-{current_month:02d}/{suffix}'
        else:
            return f'COTIZACIÓN {next_number:04d}/{current_year}-{suffix}'
    
    def get_formatted_date(self):
        """Retorna la fecha en formato español"""
        if self.date_order:
            months_spanish = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }
            
            date = fields.Datetime.from_string(self.date_order)
            month_name = months_spanish.get(date.month, '')
            
            return f"Arequipa, {date.day:02d} de {month_name} del {date.year}"
        return ""
    
    def get_quotation_validity_days(self):
        """Retorna los días de vigencia basado en validity_date"""
        if self.validity_date:
            today = fields.Date.today()
            delta = self.validity_date - today
            return max(0, delta.days)
        return 0
    
    def get_contact_info(self):
        """Retorna información de contacto del cliente"""
        contact_info = {}
        if self.partner_id:
            phones = []
            if self.partner_id.phone:
                phones.append(self.partner_id.phone)
            if self.partner_id.mobile:
                phones.append(self.partner_id.mobile)
            contact_info['phones'] = ' - '.join(phones) if phones else ''
            contact_info['email'] = self.partner_id.email or ''
        return contact_info
    
    def get_company_bank_accounts(self):
        """Retorna las cuentas bancarias de la compañía desde res.partner.bank"""
        bank_accounts_list = []

        # Buscar las cuentas bancarias de la compañía actual
        company = self.company_id or self.env.company

        # Obtener solo las cuentas bancarias de tipo público y privado
        bank_accounts = self.env['res.partner.bank'].search([
            ('partner_id', '=', company.partner_id.id),
            ('entity_type', 'in', ['public', 'private'])
        ], order='entity_type, bank_id')

        # Mapeo de tipos de entidad
        entity_type_labels = {
            'public': 'Entidades Públicas',
            'private': 'Entidades Privadas'
        }

        for account in bank_accounts:
            bank_data = {
                'bank': account.bank_id.name if account.bank_id else 'N/A',
                'type': entity_type_labels.get(account.entity_type, ''),
                'account': account.acc_number or 'N/A',
                'cci': account.cci_number or 'N/A'
            }
            bank_accounts_list.append(bank_data)

        return bank_accounts_list
    
    def get_company_info_by_type(self):
        """Retorna la información de la empresa según el tipo seleccionado"""
        company_info = {
            'peruanita': {
                'name': 'PERUANITA',
                'ruc': '20455005869',
                'address': 'Calle Francia Mza. A Lote. 9 Asoc. APTASA Parque Industrial, Cerro Colorado',
                'email': 'ventas@peruanita.com'
            },
            'gibbor': {
                'name': 'GIBBOR ALIMENTOS S.A.C',
                'ruc': '20612492639',
                'address': 'Cal. Mariano Melgar nro. 621 dpto. 101 urb. La Libertad Cerro Colorado- Arequipa',
                'email': 'administracion@gibboralimentos.com'
            },
            'corpealim': {
                'name': 'CORPEALIM EIRL',
                'ruc': '2045557928',
                'address': 'Urbanización Challapampa Mza. LL Lt. 2, Dpto. 802, Cerro Colorado, Departamento y Provincia de Arequipa',
                'email': 'corpealim@gmail.com'
            }
        }
        return company_info.get(self.quotation_company_type, company_info['peruanita'])
    
    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for record in self:
            record.amount_total_words = f"SON: {record.amount_total} SOLES"
    
    amount_total_words = fields.Char(
        string='Monto Total en Palabras',
        compute='_compute_amount_total_words',
        store=True
    )
    
    @api.onchange('quotation_company_type')
    def _onchange_quotation_company_type(self):
        """Actualiza el número de cotización cuando cambia el tipo de empresa"""
        if self.quotation_company_type:
            self.custom_quotation_number = self._generate_custom_quotation_number(self.quotation_company_type)