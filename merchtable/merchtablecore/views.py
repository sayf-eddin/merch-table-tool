from django.shortcuts import render, redirect, get_object_or_404

from django import forms
from django.forms.fields import IntegerField
from .forms import SellerForm, ItemForm
from .models import Seller, Item


def dashboard(request):
    sellers = {}
    for seller in Seller.objects.all():
        sellers[str(seller)] = seller.items.all()
    return render(request, "dashboard.html", context={"sellers": sellers})

def merch_form(request):
    if request.method == 'POST':
        #TODO
        pass
    fields = {}
    for seller in Seller.objects.all():
        for item in seller.items.all():
            fields[str(item)] = IntegerField()
    form = type('MerchForm', (forms.Form), fields)
    return render(request, "merch_form.html", context={"form": form})

def add_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add_seller.html',context={"form": SellerForm()})

def add_items(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add_item.html',context={"form": ItemForm()})

def update_seller(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    if request.method == 'POST':
        form = SellerForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SellerForm(instance=seller)
    return render(request, 'update_seller.html', context={"form": form})

def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm(instance=item)
    return render(request, 'update_item.html', context={"form": form})

def delete_seller(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    seller.delete()
    return redirect("home")

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect("home")
