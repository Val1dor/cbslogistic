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

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    #supplier = models.ForeignKey(Suppliercontract, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)
    sensor_no = models.IntegerField()
    sensor_status = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Supplier, through='Detail')

    def __str__(self):
        return self.label

class Detail(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    shipment_cost = models.IntegerField(default=0)
    order_min = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.article) + str(': ____added to____: ') + str(self.supplier)

class Orderbasket(models.Model):
    id = models.AutoField(primary_key=True)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    #article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    #number = models.CharField(max_length=200, default="XXX")
    #date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        #return str(self.article) + str(': ____ordered from____: ') + str(self.supplier)
        return str(self.detail.id)
        #return str('test')
