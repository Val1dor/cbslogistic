from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Article, Supplier, Detail, Orderbasket, Orders, Address
from django.shortcuts import render
from datetime import datetime
from django.views import generic
from .forms import AddArticleToSuppForm, AddArticleToBasket, AddArticle, AddSupplier, BucketToOrder, AddDetailPrice, AddAddress, Detailprice


class InqueryView(generic.TemplateView):
    template_name = 'inquery.html'

    def get_context_data(self, **kwargs):
        context = super(InqueryView, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        if 'cart' in request.POST:
            baskets = Orderbasket.objects.filter(detail__supplier__id=request.POST.get('cart'))
            #16.2.2019 alt brauche ich nicht
            suppliers = Supplier.objects.filter(id=request.POST.get('cart'))
            BucketOrder = BucketToOrder()

            return render(request, 'inquery.html', {'baskets': baskets,
                                                    'BucketOrder': BucketOrder,
                                                    'suppliers': suppliers})

        if 'printsave' in request.POST:

            basket_set = Orderbasket.objects.filter(detail__supplier__id=request.POST.get('printsave'), confirmed='True', ordered='False')
            for basket in basket_set:
                instance = Orders()
                instance.basket = basket
                instance.ordernumber = 'XX'
                instance.save()
                form = BucketToOrder(request.POST, instance=instance)

                if form.is_valid():
                    form.save()
                    baskets = Orderbasket.objects.filter(detail__supplier__id=request.POST.get('printsave'))
                    for basket1 in baskets:
                        basket1.ordered = 'True'
                        basket1.save()
            #return render(request, 'getstatus.html')#url bleibt alte, geht zu getstatus, wird nicht geladen
            return redirect('getstatus')

class ArticleView(generic.TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['empty_form'] = AddArticle()
        context['articles'] = Article.objects.all()
        return context

    def post(self, request):
        if 'save' in request.POST:
            form = AddArticle(request.POST, request.FILES)
            if form.is_valid():
                form.save()

            return HttpResponseRedirect(reverse('getstatus'))

class EditArticleView(generic.TemplateView):
    template_name = 'editarticle.html'

    def post(self, request):
        if 'edit' in request.POST:
            article_edit = Article.objects.get(id=request.POST['edit'])
            article_form = AddArticle(initial={'label': article_edit.label, 'sensor_no': article_edit.sensor_no, 'image': article_edit.image})

            return render(request, 'editarticle.html', {'article_edit': article_edit,
                                                        'article_form': article_form})

        if 'savechanges' in request.POST:
            instance = Article.objects.get(id=request.POST['savechanges'])
            form_edit = AddArticle(request.POST or None,request.FILES, instance=instance)
            if form_edit.is_valid():
                form_edit.save()

            return render(request, 'article.html')



class SupplierView(generic.TemplateView):
    template_name = 'supplier.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierView, self).get_context_data(**kwargs)
        context['empty_form'] = AddSupplier()
        context['suppliers'] = Supplier.objects.all()
        return context

    def post(self, request):
        if 'save' in request.POST:
            form = AddSupplier(request.POST)
            if form.is_valid():
                form.save()

            return HttpResponseRedirect(reverse('getstatus'))

class EditSupplierView(generic.TemplateView):
    template_name = 'editsupplier.html'

    def post(self, request):
        if 'edit' in request.POST:
            supplier_edit = Supplier.objects.get(id=request.POST['edit'])
            supplier_form = AddSupplier(initial={'name': supplier_edit.name,
                                                'shipment_cost': supplier_edit.shipment_cost,
                                                'order_min_value': supplier_edit.order_min_value})

            return render(request, 'editsupplier.html', {'supplier_edit': supplier_edit,
                                                        'supplier_form': supplier_form})

        if 'savechanges' in request.POST:
            instance = Supplier.objects.get(id=request.POST['savechanges'])
            form_edit = AddSupplier(request.POST or None,request.FILES, instance=instance)
            if form_edit.is_valid():
                form_edit.save()

            return render(request, 'article.html')

class OrderView(generic.TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['orders'] = Orders.objects.all()
        return context

    def post(self, request):
        if 'save' in request.POST:
            form = AddArticle(request.POST)
            if form.is_valid():
                form.save()

            return HttpResponseRedirect(reverse('getstatus'))




class ArticleListView(generic.ListView):
    template_name = 'getstatus.html'
    context_object_name = 'all_articles'
    queryset = Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['empty_articles'] = Article.objects.filter(sensor_status=True)
        context['all_supplier'] = Supplier.objects.all()
        context['details'] = Detail.objects.filter(article__sensor_status=True, status='True')
        context['baskets'] = Orderbasket.objects.filter(ordered='False').order_by('detail__supplier')

        return context
    def post(self, request):
        if 'detail' in request.POST:
        #if request.POST['detail']:
            #try:

            exist = Orderbasket.objects.filter(detail__id=request.POST['detail'], ordered='False') #Checkt op schon ein basket existiert und neu ob es noch nicht georder wurde
            if not exist:
                detail = Detail.objects.get(id=request.POST['detail'])
                basket = Orderbasket()
                basket.detail = (detail)
                basket.save()
                return HttpResponseRedirect(reverse('getstatus'))
            else:
                return HttpResponseRedirect(reverse('getstatus'))

        if 'remove' in request.POST:

            instance = Orderbasket.objects.get(id=request.POST['remove'])
            instance.delete()
            empty_articles = Article.objects.filter(sensor_status=True)
            all_supplier = Supplier.objects.all()
            details = Detail.objects.filter(article__sensor_status=True)
            #baskets = Orderbasket.objects.order_by('detail__supplier')
            baskets = Orderbasket.objects.filter(ordered='False').order_by('detail__supplier')

            return render(request, 'getstatus.html', {'empty_articles': empty_articles,
                                                      'all_supplier': all_supplier,
                                                      'details': details,
                                                      'baskets': baskets})


class AddressView(generic.TemplateView):
    template_name = 'address.html'

    def get_context_data(self, **kwargs):
        context = super(AddressView, self).get_context_data(**kwargs)
        context['empty_form'] = AddAddress()
        context['addresses'] = Address.objects.all()
        return context

    def post(self, request):
        if 'save' in request.POST:
            form = AddAddress(request.POST, request.FILES)
            if form.is_valid():
                form.save()

            return HttpResponseRedirect(reverse('getstatus'))


class MatrixListView(generic.ListView):
    template_name = 'getmatrix.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MatrixListView, self).get_context_data(**kwargs)
        context['details'] = Detail.objects.all()#filter(status='True')
        context['formy'] = AddArticleToSuppForm()
        context['formx'] = AddDetailPrice()
        return context

    def post(self, request):
        if 'sub' in request.POST:
            try:
                sub = Detail.objects.get(id=request.POST['sub'])
                sub.status = 'False'
                sub.save()
            except Detail.DoesNotExist:
                raise Http404("Gibts nicht1")
            return HttpResponseRedirect(reverse('getmatrix'))

        if 'activate' in request.POST:
            try:
                sub = Detail.objects.get(id=request.POST['activate'])
                sub.status = 'True'
                sub.save()
            except Detail.DoesNotExist:
                raise Http404("Gibts nicht1")
            return HttpResponseRedirect(reverse('getmatrix'))

        elif 'AddArticleToSupp' in request.POST:
            form1 = AddArticleToSuppForm(request.POST)#Detail aktuell nicht VALID
            form2 = AddDetailPrice(request.POST)       #Preis

            if form1.is_valid() and form2.is_valid():

                new_detail = form1.save(commit=False)
                new_price = form2.save()
                new_detail.price = (new_price)
                new_detail.save()

                formy = AddArticleToSuppForm()
                formx = AddDetailPrice()
                details = Detail.objects.all()
                articles = Article.objects.all()


                context = {'details': details,
                            'articles': articles,
                            'formy': formy,
                            'formx': formx,
                            'new_detail': new_detail,
                            'new_price': new_price}
                return render(request, self.template_name, context)

            else:
                raise Http404("Gibts nicht2ee")


class EditMatrixView(generic.TemplateView):
    template_name = 'editmatrix.html'

    def post(self, request):
        if 'edit' in request.POST:
            matrix_edit = Detail.objects.get(id=request.POST['edit'])
            #fields = ('article', 'supplier', 'shipment_cost', 'order_min')
            price_form = AddDetailPrice()#initial={'price': matrix_edit.price.price})#ICH HAB HIER FALSCHE SACHEN!!!
            matrix_form = AddArticleToSuppForm(initial={'article': matrix_edit.article.label,
                                                'supplier': matrix_edit.supplier.name,
                                                'shipment_cost': matrix_edit.shipment_cost,
                                                'order_min': matrix_edit.order_min})

            return render(request, 'editmatrix.html', {'matrix_edit': matrix_edit,
                                                        'price_form': price_form,
                                                        'matrix_form': matrix_form})

        if 'savechanges' in request.POST:
            instance1 = Detail.objects.get(id=request.POST['savechanges'])
            instance2 = Detailprice.objects.get(id=request.POST['detailprice']) #hier steht die richtige zahl

            #form_matrix = AddArticleToSuppForm(request.POST or None, instance=instance1) #request.FILES dazwischen
            form_price = AddDetailPrice(request.POST or None)#, instance=instance2)


            if form_price.is_valid():# and form_matrix.is_valid():
                new_price = form_price.save()
                instance1.price = (new_price)
                instance1.save()

                return render(request, 'test.html', {#'instance2': instance2,
                                                    'instance1': instance1,
                                                    #'new_detail': new_detail,
                                                    #'new_price': new_price
                                                     })

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

        if 'getbucket' in request.POST: #supplier.id
            formy = AddArticleToBasket()
            baskets = Orderbasket.objects.filter(detail__supplier__id=request.POST['getbucket']) #basket.detail.supplier.id
            baskets_saved = Orderbasket.objects.filter(detail__supplier__id=request.POST['getbucket']).filter(confirmed='True').filter(ordered=False)
            baskets_unsaved = Orderbasket.objects.filter(detail__supplier__id=request.POST['getbucket']).filter(confirmed='False').filter(ordered=False)
            supplier = Supplier.objects.get(id=request.POST['getbucket'])
            return render(request, 'getbucket.html', {'baskets_saved': baskets_saved,
                                                      'baskets_unsaved': baskets_unsaved,
                                                      'formy': formy,
                                                      'supplier': supplier})

        if 'savequantity' in request.POST:
            instance = Orderbasket.objects.get(id=request.POST['savequantity'])
            form = AddArticleToBasket(request.POST or None, instance=instance)

            if form.is_valid():
                form.save()
                #update table to true
                beforesave = Orderbasket.objects.get(id=request.POST['savequantity'])
                beforesave.confirmed = 'True'
                beforesave.save()
                formy = AddArticleToBasket()
                baskets_saved = Orderbasket.objects.filter(detail__supplier__id=request.POST['supplier'], confirmed='True', ordered='False')
                baskets_unsaved = Orderbasket.objects.filter(detail__supplier__id=request.POST['supplier'], confirmed='False', ordered='False')

                supplier = Supplier.objects.get(id=request.POST.get('supplier'))

                return render(request, 'getbucket.html', {'formy': formy,
                                                          'baskets_saved': baskets_saved,
                                                          'baskets_unsaved': baskets_unsaved,
                                                          'supplier': supplier})

            return render(request, '404.html')

        if 'delquantity' in request.POST:
            #instance = Orderbasket.objects.get(id=request.POST['delquantity'])
            #form = AddArticleToBasket(request.POST or None, instance=instance)
            beforesave = Orderbasket.objects.get(id=request.POST['delquantity'])
            beforesave.confirmed = 'False'
            beforesave.save()
            formy = AddArticleToBasket()
            baskets_saved = Orderbasket.objects.filter(detail__supplier__id=request.POST['supplier'], confirmed='True', ordered='False')
            baskets_unsaved = Orderbasket.objects.filter(detail__supplier__id=request.POST['supplier'], confirmed='False', ordered='False')
            supplier = Supplier.objects.get(id=request.POST.get('supplier'))

            return render(request, 'getbucket.html', {'formy': formy,
                                                      'baskets_saved': baskets_saved,
                                                      'baskets_unsaved': baskets_unsaved,
                                                      'supplier': supplier})


class TestView(generic.TemplateView):
    template_name = 'test.html'





















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
