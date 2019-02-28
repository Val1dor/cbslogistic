from django.db import models
from django.db.models import CharField
from django.contrib import admin
from datetime import datetime


class Suppliercontract(models.Model):
    Suppliercontract_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    position = (
        ('SP', 'Support'),
        ('TC', 'Technican'),
        ('DP', 'Development'),
        ('CO', 'CEO'),
    )
    mail = models.EmailField()

    def __str__(self):
        return self.name

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField
    zip = models.IntegerField()
    town = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    housenumber = models.CharField(max_length=50)
    information = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.zip) + str(self.town)

#class Home(Address):


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    shipment_cost = models.IntegerField(default=0)
    order_min_value = models.IntegerField(default=0)
    #supplier = models.ForeignKey(Suppliercontract, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)
    sensor_no = models.IntegerField()
    sensor_status = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Supplier, through='Detail')
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.label

    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)

class Detail(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_min = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    shipment_cost = models.IntegerField(default=0)
    def __str__(self):
        return str(self.article) + str(': ____added to____: ') + str(self.supplier)

class Orderbasket(models.Model):
    id = models.AutoField(primary_key=True)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    quantity = models.IntegerField(default=1)
    confirmed = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    discount_abs = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    #place = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.detail.id)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    basket = models.ForeignKey(Orderbasket, on_delete=models.CASCADE)
    ordernumber = models.CharField(max_length=50) #unique wurde auskommentiert 12.2.2019
    date = models.DateTimeField(default=datetime.now)
    delivered = models.BooleanField(default=False)
    delivery_number = models.CharField(default='notset',max_length=50)


    def __str__(self):
        return str(self.ordernumber)

