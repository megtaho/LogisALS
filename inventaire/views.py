from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Commande, Utilisateur, Rapport
from .forms import ProduitForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum


# Vue pour l'inscription des utilisateurs
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Utilisateur.objects.create(user=user, nom=user.username, email=user.email, role='employe')  # Set default role to 'employe'
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

        # Récupérer le produit
        produit = Produit.objects.get(id=produit_id)

        try:
            # Récupérer l'objet de l'utilisateur connecté
            utilisateur = Utilisateur.objects.get(user=request.user)
        except Utilisateur.DoesNotExist:
            return render(request, 'inventaire/erreur_commande.html', {'message': "Utilisateur non trouvé, veuillez vous inscrire"})

        # Vérification des quantités disponibles si c'est une vente
        if type_transaction == 'vente' and quantite > produit.quantite_stock:
            return render(request, 'inventaire/erreur_commande.html', {'message': "Quantité demandée supérieure au stock"})

        # Mettre à jour la quantité du produit en fonction du type de transaction
        if type_transaction == 'vente':
            produit.quantite_stock -= quantite  # Réduire la quantité en stock
        elif type_transaction == 'achat':
            produit.quantite_stock += quantite  # Augmenter la quantité en stock

        produit.save()  # Sauvegarder les changements de stock

        # Créer la commande
        commande = Commande.objects.create(
            produit=produit,
            type=type_transaction,
            quantite=quantite,
            montant_total=produit.prix * quantite,
            statut='en_cours',
            utilisateur=utilisateur
        )

        return redirect('liste_commandes')
    
    produits = Produit.objects.all()
    return render(request, 'inventaire/enregistrer_commande.html', {'produits': produits})



def rapport_ventes(request):
     produits_ventes = Commande.objects.filter(type='vente') \
        .values('produit__nom') \
        .annotate(total_ventes=Sum('quantite')) \
        .order_by('-total_ventes')  # Order by total sales quantity
     #total des commandes
     produits_achats = Commande.objects.filter(type='achat') \
        .values('produit__nom') \
        .annotate(total_achats=Sum('quantite')) \
        .order_by('-total_achats') 
     #niveau de stock
     stocks = Produit.objects.all().values('nom', 'quantite_stock')

     return render(request, 'inventaire/rapport_ventes.html', {
         'produits_ventes': produits_ventes,
         'produits_achats': produits_achats,
         'stocks': stocks,
         
    })


