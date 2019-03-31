from django import forms
from .models import Detail, Article, Supplier, Orderbasket, Orders, Detailprice, Address

class AddArticleToSuppForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ('article', 'supplier', 'shipment_cost', 'order_min', 'price')
        widgets = {'price': forms.HiddenInput()}

    #def save(self, commit=True, *args, **kwargs):
#
 #       article = self.cleaned_data.get('article')
  #      supplier = self.cleaned_data.get('supplier')

   #     try:
    #        query = Detail.objects.get(article__label=article, supplier__name=supplier)
     #   except Detail.DoesNotExist:
      #      m = super(AddArticleToSuppForm, self).save(commit=False, *args, **kwargs)
       #     if commit:
        #        m.save()
         #   return m

class AddDetailPrice(forms.ModelForm):
    class Meta:
        model = Detailprice
        fields = ('price',)


class AddArticleToBasket(forms.ModelForm):
    class Meta:
        model = Orderbasket
        fields = ('quantity', 'detail', 'address', 'discount_abs', 'discount_percent')
        widgets = {'detail': forms.HiddenInput()}

class AddArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('label', 'sensor_no', 'image')

class AddSupplier(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'shipment_cost', 'order_min_value')

class BucketToOrder(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('ordernumber',)# 'basket')

class AddAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('zip', 'town', 'street', 'housenumber', 'information')

