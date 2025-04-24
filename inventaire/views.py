from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Commande, Rapport
from .forms import ProduitForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum

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
    search = request.GET.get('search', '')  # Récupère le paramètre 'search' de l'URL
    if search:
        produits = produits.filter(nom__icontains=search)  # Filtre par nom
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

# Vue pour modifier un produit
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'inventaire/modifier_produit.html', {'form': form})

# Vue pour supprimer un produit
def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'inventaire/supprimer_produit.html', {'produit': produit})

from .models import Commande

def liste_commandes(request):
    commandes = Commande.objects.all()  # Récupère toutes les commandes
    statut_filter = request.GET.get('statut', '')  # Récupère le paramètre 'statut' de l'URL
    if statut_filter:
        commandes = commandes.filter(statut=statut_filter)  # Filtre par statut
    return render(request, 'inventaire/liste_commandes.html', {'commandes': commandes})

# Vue pour enregistrer une commande
def enregistrer_commande(request):
    if request.method == 'POST':
        produit_id = request.POST['produit_id']
        type_transaction = request.POST['type_transaction']
        quantite = int(request.POST['quantite'])

        produit = Produit.objects.get(id=produit_id)

        # Mettre à jour la quantité du produit
        if type_transaction == 'vente':
            produit.quantite_stock -= quantite
        elif type_transaction == 'achat':
            produit.quantite_stock += quantite

        produit.save()

        # Enregistrer la commande
        commande = Commande.objects.create(
            produit=produit,
            type_transaction=type_transaction,
            quantite=quantite,
            utilisateur=request.user
        )

        return redirect('liste_commandes')
    return render(request, 'inventaire/enregistrer_commande.html')



# inventaire/views.py
from .models import Rapport


def rapport_ventes(request):
    produits_ventes = Commande.objects.filter(type_transaction='vente') \
        .values('produit__nom') \
        .annotate(total_ventes=Sum('quantite')) \
        .order_by('-total_ventes')

    return render(request, 'inventaire/rapport_ventes.html', {'produits_ventes': produits_ventes})