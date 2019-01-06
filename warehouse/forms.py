from django import forms
from .models import Detail, Article, Supplier, Orderbasket

class SearchForm(forms.Form):
    search_term = forms.CharField(label='search_term', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))

class AddArticleToSuppForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ('article', 'supplier','shipment_cost', 'order_min', 'price')
        widgets = {
            #'article': forms.TextInput(attrs={'cols': 80, 'rows': 20}),
            #'supplier': forms.TextInput(attrs={'cols': 80, 'rows': 20})
        }

class AddArticleToBasket(forms.ModelForm):
    class Meta:
        model = Orderbasket
        fields = ('quantity', 'detail')
        widgets = {'detail': forms.HiddenInput()}


class AddArticleToSuppFormRaw(forms.Form):
    article = forms.CharField()
    supplier = forms.CharField()

