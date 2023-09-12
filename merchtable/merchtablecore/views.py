from django.shortcuts import render, redirect, get_object_or_404

from .forms import SellerForm, ItemForm
from .models import Seller, Item

from django.conf import settings
import os
import pandas as pd


def dashboard(request):
    sellers = {}
    for seller in Seller.objects.all():
        sellers[seller] = seller.items.all()
        
    # If database is empty
    if sellers == {}:
        return render(request, "dashboard.html", context={"home": True})
    
    # If no seller has an item
    if not Item.objects.all():
        return render(request, "dashboard.html", context={"home": True, "sellers": sellers})
    
    return render(request, "dashboard.html", context={"home": True, "sellers": sellers, "item": True})

def merch_form(request):
    # If accessing the form incorrectly
    if not Item.objects.all():
        return render(request, "merch_form.html", context={"error": "Cannot create form, no items exist."})
    
    sellers = {}
    for seller in Seller.objects.all():
        sellers[seller] = seller.items.all()
    
    if request.method == 'POST':
        sales_file = "merch.xlsx"
        dfs = {}
        total_qty = 0
        total_amt = 0
        
        # If file has not been created and no sales were recorded
        if (not os.path.exists(settings.BASE_DIR / sales_file)):
            
            # Create dataframes for each seller
            for seller, items in sellers.items():
                seller_qty = 0
                seller_amt = 0
                df = pd.DataFrame(columns=["Item Name", "Price", "Qty", "Amount"])
                
                # Add row in dataframe for each item
                for item in items:
                    qty = int(request.POST[str(item)])
                    
                    # Validate form
                    if qty < 0:
                        context = {"sellers": sellers, "message": "Error processing form."}
                        return render(request, "merch_form.html", context=context)
                    
                    # Create and add row
                    amount = qty * item.price
                    row = {"Item Name": item.name, "Price": item.price, "Qty": qty, "Amount": amount}
                    df = df.append(row, ignore_index=True)
                    
                    # Update totals
                    seller_qty += qty
                    seller_amt += amount
                    total_qty += qty
                    total_amt += amount
                    
                # Add row for total for seller
                row = {"Item Name": "Total", "Price": "", "Qty": seller_qty, "Amount": seller_amt}
                df = df.append(row, ignore_index=True)
                
                # Save dataframe
                dfs[seller.name] = df
                
            # Create Excel file with sheet with totals across sellers
            df_total = pd.DataFrame(columns=["Total Qty", "Total Amount"])
            row = {"Total Qty": total_qty, "Total Amount": total_amt}
            df_total = df_total.append(row, ignore_index=True)
            df_total.to_excel(sales_file, sheet_name="Totals", index=False)

            # Add saved seller dataframes as sheets
            with pd.ExcelWriter(sales_file, engine='openpyxl', mode='a') as writer: 
                for seller, df in dfs.items():
                    df.to_excel(writer, sheet_name=seller, index=False)
               
        # If file has been created and sales are recorded
        else:
            # Get seller sheets and update dataframe
            for seller, items in sellers.items():
                seller_qty = 0
                seller_amt = 0
                df = pd.read_excel(sales_file, sheet_name=seller.name, index_col=0, engine='openpyxl')
                
                # Check for update for each item
                for item in items:
                    qty = int(request.POST[str(item)])
                    
                    # Validate form
                    if qty < 0:
                        context = {"sellers": sellers, "message": "Error processing form."}
                        return render(request, "merch_form.html", context=context)
                    
                    # Update if needed
                    if qty > 0:
                        amount = qty * item.price
                        df.at[item.name, "Qty"] += qty
                        df.at[item.name, "Amount"] += float(amount)
                        
                        # Update totals
                        seller_qty += qty
                        seller_amt += amount  
                        total_qty += qty
                        total_amt += amount
                
                # Update seller totals
                df.at["Total", "Qty"] += seller_qty
                df.at["Total", "Amount"] += float(seller_amt)
                
                # Save dataframe
                dfs[seller.name] = df
                
            # Update totals across sellers
            df_total = pd.read_excel(sales_file, sheet_name="Totals", engine='openpyxl')
            df_total.at[0, "Total Qty"] += total_qty
            df_total.at[0, "Total Amount"] += float(total_amt)
            
            # Overwrite Excel sheets with updated data
            with pd.ExcelWriter(sales_file, engine='openpyxl', mode='w') as writer: 
                for seller, df in dfs.items():
                    df.to_excel(writer, sheet_name=seller)
                
                df_total.to_excel(writer, sheet_name="Totals", index=False)
            
        message = "Transaction recorded in " + sales_file + "!"
        return render(request, "merch_form.html", context={"sellers": sellers, "message": message})
    
    # If GET request
    return render(request, "merch_form.html", context={"sellers": sellers})

# Seller CRUD
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

# Item CRUD
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