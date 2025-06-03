from django import forms
from .models import Produit

# Formulaire pour ajouter/modifier un produit
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit  # Spécifie le modèle associé au formulaire
        fields = ['nom', 'description', 'prix', 'quantite_stock', 'vendeur']  # Les champs à inclure dans le formulaire
        