from django.db import models
import uuid

class Facture(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    numero_facture = models.CharField(max_length=50, unique=True)
    nom_vendeur = models.CharField(max_length=255)
    adresse_vendeur = models.TextField()
    identifiant_fiscal_vendeur = models.CharField(max_length=50)
    iban_vendeur = models.CharField(max_length=50)
    nom_client = models.CharField(max_length=255)
    adresse_client = models.TextField()
    identifiant_fiscal_client = models.CharField(max_length=50)
    date_emission = models.CharField(max_length=20)  
    taux_tva = models.CharField(max_length=10)
    valeur_brute = models.CharField(max_length=50)  
    valeur_nette = models.CharField(max_length=50)  

    def __str__(self):
        return f"Facture {self.numero_facture}"


class Produit(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    facture = models.ForeignKey(Facture, related_name='produits', on_delete=models.CASCADE)
    description = models.TextField()
    prix_unitaire = models.CharField(max_length=50) 
    quantite = models.CharField(max_length=50)       
    unite = models.CharField(max_length=50)
    valeur_brute = models.CharField(max_length=50)   
    valeur_nette = models.CharField(max_length=50)   
    TVA = models.CharField(max_length=10)

    def __str__(self):
        return self.description[:50]
