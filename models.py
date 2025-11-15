from django.db import models

# Create your models here.

class TypeProducts(models.Model):
    name = models.CharField(max_length=100)
    ratio_product = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    type_product = models.ForeignKey(TypeProducts, on_delete=models.CASCADE)
    article = models.CharField(max_length=7)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class TypePartners(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Streets(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Cities(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Address(models.Model):
    street = models.ForeignKey(Streets, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    home = models.IntegerField()
    postal_code = models.IntegerField()

    def __str__(self):
        return self.home

class Partners(models.Model):
    type_partner = models.ForeignKey(TypePartners, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    email = models.EmailField()
    phone_num = models.CharField(max_length=11)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    inn = models.CharField()
    rating = models.IntegerField()

    def total_quantity(self):
        """Общее количество продуктов партнера"""
        return self.partnersproducts_set.aggregate(
            total=models.Sum('quantity_product')
        )['total'] or 0

    def discount(self):
        """Скидка на основе общего количества продуктов"""
        total_qty = self.total_quantity()
        if total_qty <= 10000:
            return 0
        elif total_qty <= 50000:
            return 5
        elif total_qty <= 300000:
            return 10
        else:
            return 15

    def __str__(self):
        return self.name



class PartnersProducts(models.Model):
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity_product = models.IntegerField()
    date_sale = models.DateField()

    def __str__(self):
        return self.partner.name



