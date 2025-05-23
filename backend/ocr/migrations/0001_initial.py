# Generated by Django 5.2.1 on 2025-05-15 23:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('numero_facture', models.CharField(max_length=50, unique=True)),
                ('nom_vendeur', models.CharField(max_length=255)),
                ('adresse_vendeur', models.TextField()),
                ('identifiant_fiscal_vendeur', models.CharField(max_length=50)),
                ('iban_vendeur', models.CharField(max_length=50)),
                ('nom_client', models.CharField(max_length=255)),
                ('adresse_client', models.TextField()),
                ('identifiant_fiscal_client', models.CharField(max_length=50)),
                ('date_emission', models.CharField(max_length=20)),
                ('taux_tva', models.CharField(max_length=10)),
                ('valeur_brute', models.CharField(max_length=50)),
                ('valeur_nette', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField()),
                ('prix_unitaire', models.CharField(max_length=50)),
                ('quantite', models.CharField(max_length=50)),
                ('unite', models.CharField(max_length=50)),
                ('valeur_brute', models.CharField(max_length=50)),
                ('valeur_nette', models.CharField(max_length=50)),
                ('TVA', models.CharField(max_length=10)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='ocr.facture')),
            ],
        ),
    ]
