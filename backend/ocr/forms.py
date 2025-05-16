from django import forms
from .models import Vendeur, Client, Facture, Produit, Intermediaire

class VendeurForm(forms.ModelForm):
    class Meta:
        model = Vendeur
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = '__all__'
        widgets = {
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
        }

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'

class IntermediaireForm(forms.ModelForm):
    class Meta:
        model = Intermediaire
        fields = '__all__'
