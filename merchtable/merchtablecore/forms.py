from django.forms import ModelForm
from .models import Seller, Item


class SellerForm(ModelForm):

    class Meta:
        model = Seller
        exclude = ['id']
        

class ItemForm(ModelForm):

    class Meta:
        model = Item
        exclude = ['id']