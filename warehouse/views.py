from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Article, Supplier, Detail, Orderbasket, Suppliercontract
from django.shortcuts import render
from datetime import datetime
from django.views import generic
from .forms import SearchForm, AddArticleToSuppForm, AddArticleToBasket



class ArticleListView(generic.ListView):
    template_name = 'getstatus.html'
    context_object_name = 'all_articles'
    queryset = Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['empty_articles'] = Article.objects.filter(sensor_status=True)
        context['all_supplier'] = Supplier.objects.all()
        context['details'] = Detail.objects.filter(article__sensor_status=True)
        context['baskets'] = Orderbasket.objects.order_by('detail__supplier')
        return context

    def post(self, request):
        if request.POST['detail']:# == 'detail':
            try:
                detail = Detail.objects.get(id=request.POST['detail'])
                basket = Orderbasket()
                basket.detail=(detail)
                basket.save()
            except Detail.DoesNotExist:
                raise Http404("Gibts nicht")
            return HttpResponseRedirect(reverse('getstatus'))

class MatrixListView(generic.ListView):
    template_name = 'getmatrix.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MatrixListView, self).get_context_data(**kwargs)
        context['details'] = Detail.objects.all()
        context['formx'] = SearchForm()
        context['formy'] = AddArticleToSuppForm()
        #context['formy'] = AddArticleToSuppFormRaw()
        return context

    def post(self, request):
        if 'sub' in request.POST:
            try:
                sub = Detail.objects.get(id=request.POST['sub'])
                sub.delete()
            except Detail.DoesNotExist:
                raise Http404("Gibts nicht1")
            return HttpResponseRedirect(reverse('getmatrix'))

        elif 'search_term' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                searchfield = form.cleaned_data.get('search_term')
                formx = SearchForm()
                matches = Supplier.objects.get(name__icontains=searchfield)
                details = Detail.objects.all()
                articles = Article.objects.all()

                context = {'details': details,
                          'searchfield': searchfield,
                          'articles': articles,
                           'matches': matches,
                           'formx': formx}
                return render(request, self.template_name, context)
            else:
                raise Http404("Gibts nicht2")

        elif 'AddArticleToSupp' in request.POST:
            form = AddArticleToSuppForm(request.POST)
            #form = AddArticleToSuppFormRaw(request.POST)
            if form.is_valid():
                form.save()
                formy = AddArticleToSuppForm()
                details = Detail.objects.all()
                articles = Article.objects.all()

                context = {'details': details,
                           'articles': articles,
                           'formy': formy}
                return render(request, self.template_name, context)
            else:
                raise Http404("Gibts nicht2ee")

class BucketListView(generic.ListView):
    template_name = 'getbucket.html'

    def get_context_data(self, **kwargs):
        context = super(BucketListView, self).get_context_data(**kwargs)
        try:
            context['details'] = Detail.objects.filter(supplier__id=request.POST['getbucket'])
            context['supplier'] = Supplier.objects.get(id=request.POST['getbucket'])
            context['formy'] = AddArticleToBasket()
        except:
            return context

    def post(self, request, *args, **kwargs):
        if 'getbucket' in request.POST:
            formy = AddArticleToBasket()

            details = Orderbasket.objects.filter(detail__supplier__id=request.POST['getbucket']) #basket.detail.supplier.id
            return render(request, 'getbucket.html', {'details': details,
                                                  'formy': formy})
        if 'savequantity' in request.POST:
            form = AddArticleToBasket(request.POST)

            if form.is_valid():
                form.save()
                formy = AddArticleToBasket()
                orders = Orderbasket.objects.all()

                return render(request, 'getbucket.html',{'formy': formy,
                                                         'orders': orders})








def getbucket(request):
    #if request.method == 'POST':
        try:
            supplier = Supplier.objects.get(id=request.POST['getbucket'])
            details = Detail.objects.filter(supplier__id=request.POST['getbucket'])

        except Supplier.DoesNotExist:
            raise Http404("Gibts nicht")
        return render(request, 'getbucket.html',
                      {'supplier': supplier,
                       'details': details})

def getmatrix(request):
    try:
        articles = Article.objects.all()
        details = Detail.objects.all()
    except Article.DoesNotExist:
        raise Http404("Gibts nicht")
    return render(request, 'getmatrix.html',
              {'articles': articles,
               'details': details})


def getstatus(request):
    if request.method == 'POST':
        try:
            detail = Detail.objects.get(id=request.POST['detail'])
            basket = Orderbasket()
            basket.detail=(detail)
            basket.save()

        except Order.DoesNotExist:
            raise Http404("Gibts nicht")
        return HttpResponseRedirect(reverse('getstatus'))
    else:
        try:
            all_articles = Article.objects.all()
            empty_articles = Article.objects.filter(sensor_status=True)
            all_supplier = Supplier.objects.all()
            details = Detail.objects.filter(article__sensor_status=True)
            baskets = Orderbasket.objects.order_by('detail__supplier')

        except Article.DoesNotExist:
            raise Http404("Gibts nicht")
        return render(request, 'getstatus.html',
                  {'all_articles': all_articles,
                   'empty_articles': empty_articles,
                   'all_supplier': all_supplier,
                   'details': details,
                   'baskets': baskets})
