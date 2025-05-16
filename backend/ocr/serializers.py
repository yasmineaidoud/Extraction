from rest_framework import serializers
from .models import Facture, Produit

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class FactureSerializer(serializers.ModelSerializer):
    produits = ProduitSerializer(many=True, read_only=True)

    class Meta:
        model = Facture
        fields = '__all__'
