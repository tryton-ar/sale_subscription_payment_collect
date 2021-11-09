# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import PoolMeta, Pool
from trytond.modules.company.model import CompanyValueMixin

__all__ = ['Configuration', 'ConfigurationPaymentCollect']


class Configuration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'
    invoice_description = fields.MultiValue(fields.Char('Invoice description'))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'invoice_description':
            return pool.get('sale.configuration.payment_collect')
        return super().multivalue_model(field)

    @classmethod
    def default_invoice_description(cls, **pattern):
        return cls.multivalue_model(
            'invoice_description').default_invoice_description()


class ConfigurationPaymentCollect(ModelSQL, CompanyValueMixin):
    "Sale Configuration PaymentCollect"
    __name__ = 'sale.configuration.payment_collect'
    invoice_description = fields.Char('Invoice description')

    @classmethod
    def default_invoice_description(cls):
        return ''
