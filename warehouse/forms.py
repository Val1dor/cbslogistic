from django import forms
from .models import Detail, Article, Supplier

class SearchForm(forms.Form):
    search_term = forms.CharField(label='search_term', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))

class AddArticleToSuppForm(forms.ModelForm):
    query_article = Article.objects.all()
    query_supplier = Supplier.objects.all()
    article = forms.ModelChoiceField(queryset=query_article, widget=forms.RadioSelect())             #label='Article',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))
    supplier = forms.ModelChoiceField(queryset=query_supplier, widget=forms.RadioSelect())                  #(label='Supplier',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))


    class Meta:
        model = Detail
        fields = ('article', 'supplier')

