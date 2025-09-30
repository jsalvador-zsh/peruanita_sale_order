from odoo import models, fields, api


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    # Campo para CCI
    cci_number = fields.Char(
        string='CCI',
        help='Código de Cuenta Interbancaria'
    )
    
    # Campo para indicar el tipo de entidad
    entity_type = fields.Selection([
        ('public', 'Entidades Públicas'),
        ('private', 'Entidades Privadas'),
        ('general', 'General')
    ], string='Tipo de Entidad', default='general',
       help='Indica si esta cuenta es para entidades públicas, privadas o de uso general')
    
    # Campo para indicar a qué empresa pertenece la cuenta
    company_type = fields.Selection([
        ('peruanita', 'PERUANITA'),
        ('gibbor', 'GIBBOR'),
        ('corpealim', 'CORPEALIM')
    ], string='Empresa', default='peruanita', required=True,
       help='Indica a qué empresa corresponde esta cuenta bancaria')
    
    # Campo computado para mostrar el nombre completo
    @api.depends('bank_id', 'acc_number', 'entity_type', 'company_type')
    def _compute_display_name(self):
        for bank in self:
            parts = []
            if bank.company_type:
                type_label = dict(bank._fields['company_type'].selection)[bank.company_type]
                parts.append(f"[{type_label}]")
            if bank.bank_id:
                parts.append(bank.bank_id.name)
            if bank.acc_number:
                parts.append(f"({bank.acc_number})")
            if bank.entity_type and bank.entity_type != 'general':
                entity_label = dict(bank._fields['entity_type'].selection)[bank.entity_type]
                parts.append(f"- {entity_label}")
            
            bank.display_name = ' '.join(parts) if parts else bank.acc_number or ''