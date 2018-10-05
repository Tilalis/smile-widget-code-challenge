from django.db import models


def _is_date_in_range(self, date):
    if self.date_end is not None:
        return self.date_start <= date <= self.date_end

    return self.date_start <= date


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Default price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(help_text='Price of product in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    is_valid = _is_date_in_range


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    is_valid = _is_date_in_range

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)
    
    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)
