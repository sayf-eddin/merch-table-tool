"""merchtable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url
from merchtablecore import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('form/', views.merch_form, name="form"),
    path('vendor/add/', views.add_seller, name="add_seller"),
    path('vendor/<uuid:seller_id>.UUID/', views.update_seller, name="update_seller"),
    path('vendor/<uuid:seller_id>.UUID/delete/', views.delete_seller, name="delete_seller"),
    path('item/add/', views.add_items, name="add_item"),
    path('item/<uuid:item_id>.UUID/', views.update_item, name="update_item"),
    path('item/<uuid:item_id>.UUID/delete/', views.delete_item, name="delete_item"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [url(r'^', RedirectView.as_view(url='/'))]
