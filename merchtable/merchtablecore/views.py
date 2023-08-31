from django.shortcuts import render, redirect, get_object_or_404

from django import forms
from django.forms.fields import IntegerField
from .forms import SellerForm, ItemForm
from .models import Seller, Item


def dashboard(request):
    sellers = {}
    for seller in Seller.objects.all():
        sellers[seller] = seller.items.all()
    if sellers == {}:
        return render(request, "dashboard.html", context={"home": True})
    if not Item.objects.all():
        return render(request, "dashboard.html", context={"home": True, "sellers": sellers})
    return render(request, "dashboard.html", context={"home": True, "sellers": sellers, "item": True})

def merch_form(request):
    if not Item.objects.all():
        return render(request, "merch_form.html", context={"error": "Cannot create form, no items exist."})
    sellers = {}
    for seller in Seller.objects.all():
        sellers[seller] = seller.items.all()
    if request.method == 'POST':
        #TODO
        print("Submitted")
        pass
    return render(request, "merch_form.html", context={"sellers": sellers})

def add_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add_seller.html',context={"form": SellerForm()})

def update_seller(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    if request.method == 'POST':
        form = SellerForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SellerForm(instance=seller)
    return render(request, 'update_seller.html', context={"form": form, "name": seller.name})

def delete_seller(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    seller.delete()
    return redirect("home")

def add_items(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add_item.html',context={"form": ItemForm()})

def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm(instance=item)
    return render(request, 'update_item.html', context={"form": form, "name": item.name})

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect("home")