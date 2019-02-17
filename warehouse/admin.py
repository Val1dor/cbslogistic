from django.contrib import admin
from .models import Article, Orderbasket, Supplier, Detail, Suppliercontract, Orders

# Register your models here.
admin.site.register(Article)
admin.site.register(Orderbasket)
admin.site.register(Supplier)
admin.site.register(Detail)
admin.site.register(Suppliercontract)
admin.site.register(Orders)
