"""cbslogistic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from warehouse.views import getstatus
from warehouse.views import getbucket
from warehouse.views import getmatrix
from warehouse.views import ArticleListView
from warehouse.views import MatrixListView
from warehouse.views import BucketListView
from warehouse.views import ArticleView
from warehouse.views import SupplierView
from warehouse.views import InqueryView
from warehouse.views import OrderView
from warehouse.views import EditArticleView
from warehouse.views import EditSupplierView
from warehouse.views import EditMatrixView
from warehouse.views import AddressView
from warehouse.views import TestView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #path('getstatus/', getstatus, name='getstatus'),
    path('getstatus/', ArticleListView.as_view(), name='getstatus'),
    path('getmatrix/', MatrixListView.as_view(), name='getmatrix'),
    #path('getmatrix/', getmatrix, name='getmatrix'),
    #path('getbucket/', getbucket, name='getbucket'),
    path('getbucket/', BucketListView.as_view(), name='getbucket'),
    path('article/', ArticleView.as_view(), name='article'),
    path('supplier/', SupplierView.as_view(), name='supplier'),
    path('inquery/', InqueryView.as_view(), name='inquery'),
    path('order/', OrderView.as_view(), name='order'),
    path('editarticle/', EditArticleView.as_view(), name='editarticle'),
    path('editsupplier/', EditSupplierView.as_view(), name='editsupplier'),
    path('editmatrix/', EditMatrixView.as_view(), name='editsupplier'),
    path('address/', AddressView.as_view(), name='editsupplier'),
    path('test/', TestView.as_view(), name='test')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
