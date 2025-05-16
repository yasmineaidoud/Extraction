from .models import Facture, Produit
from datetime import datetime
from decimal import Decimal
from PIL import Image
import cv2
from .main_process import extract_facture_data, extract_produits_data

image = cv2.imread("batch_1/invoice_94.pdf0.jpg")

def image_to_database(image):
    facture_data = extract_facture_data(image)  # check its type
    products = extract_produits_data(image)

    print(facture_data)
    facture = Facture.objects.create(**facture_data)

    for p in products:
        Produit.objects.create(
            facture=facture,
            TVA=p['TVA'],
            description=p['description'],
            prix_unitaire=p['prix_unitaire'].replace(',', '.'),
            quantite=p['quantite'].replace(',', '.'),
            unite=p['unite'],
            valeur_brute=p['valeur_brute'].replace(',', '.'),
            valeur_nette=p['valeur_nette'].replace(',', '.'),
        )

    return facture_data, products
