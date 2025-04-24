from django.shortcuts import render, redirect
from .models import Produit
from .forms import ProduitForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Vue pour l'inscription des utilisateurs
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('login')  # Redirige l'utilisateur vers la page de connexion
    else:
        form = UserCreationForm()
    return render(request, 'inventaire/inscription.html', {'form': form})

# Vue pour la page de profil
def profile(request):
    return render(request, 'inventaire/profile.html')

# Vue d'accueil
def accueil(request):
    return render(request, 'inventaire/accueil.html')

from .models import Produit

# Vue pour afficher tous les produits
def liste_produits(request):
    produits = Produit.objects.all()  # Récupère tous les produits
    return render(request, 'inventaire/liste_produits.html', {'produits': produits})


def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  # Redirige vers la liste des produits
    else:
        form = ProduitForm()
    return render(request, 'inventaire/ajouter_produit.html', {'form': form})

from .models import Commande

def liste_commandes(request):
    commandes = Commande.objects.all()  # Récupère toutes les commandes
    return render(request, 'inventaire/liste_commandes.html', {'commandes': commandes})

# inventaire/views.py
from .models import Rapport

def liste_rapports(request):
    rapports = Rapport.objects.all()  # Récupère tous les rapports
    return render(request, 'inventaire/liste_rapports.html', {'rapports': rapports})

