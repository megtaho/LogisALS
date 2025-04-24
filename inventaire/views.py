from django.shortcuts import render


# Vue d'accueil
def accueil(request):
    return render(request, 'inventaire/accueil.html')

from .models import Produit

# Vue pour afficher tous les produits
def liste_produits(request):
    produits = Produit.objects.all()  # Récupère tous les produits
    return render(request, 'inventaire/liste_produits.html', {'produits': produits})


from .models import Commande

def liste_commandes(request):
    commandes = Commande.objects.all()  # Récupère toutes les commandes
    return render(request, 'inventaire/liste_commandes.html', {'commandes': commandes})

# inventaire/views.py
from .models import Rapport

def liste_rapports(request):
    rapports = Rapport.objects.all()  # Récupère tous les rapports
    return render(request, 'inventaire/liste_rapports.html', {'rapports': rapports})

