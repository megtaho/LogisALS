from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Commande, Utilisateur, Rapport
from .forms import ProduitForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
import json


# Inscription
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Utilisateur.objects.create(user=user, nom=user.username, email=user.email, role='employe')
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'inventaire/inscription.html', {'form': form})

# Profil et accueil
def profile(request):
    produits = Produit.objects.all()
    stock_bas = [p for p in produits if p.quantite_stock < p.seuil_min]

    for p in stock_bas:
        messages.error(request, f"⚠️ Stock bas pour « {p.nom} » : {p.quantite_stock} (seuil : {p.seuil_min})")
    return render(request, 'inventaire/profile.html', {
        'nb_stock_bas': len(stock_bas),
    })
def accueil(request):
    return render(request, 'inventaire/accueil.html')

# Produits
def liste_produits(request):
    produits = Produit.objects.all()
    search = request.GET.get('search', '')
    if search:
        produits = produits.filter(nom__icontains=search)
    return render(request, 'inventaire/liste_produits.html', {'produits': produits})

def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'inventaire/ajouter_produit.html', {'form': form})

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

def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'inventaire/supprimer_produit.html', {'produit': produit})

# Commandes
def liste_commandes(request):
    commandes = Commande.objects.all().order_by('-date')  # Inclut ventes et achats
    type_filter = request.GET.get('type', '')  # permet de filtrer par type via l'URL
    if type_filter in ['achat', 'vente']:
        commandes = commandes.filter(type=type_filter)

    statut_filter = request.GET.get('statut', '')
    if statut_filter:
        commandes = commandes.filter(statut=statut_filter)

    return render(request, 'inventaire/liste_commandes.html', {'commandes': commandes})

def enregistrer_commande(request):
    if request.method == 'POST':
        produit_id = request.POST['produit_id']
        type_transaction = request.POST['type_transaction']
        quantite = int(request.POST['quantite'])
        produit = get_object_or_404(Produit, id=produit_id)

        try:
            utilisateur = Utilisateur.objects.get(user=request.user)
        except Utilisateur.DoesNotExist:
            return render(request, 'inventaire/erreur_commande.html', {'message': "Utilisateur non trouvé."})

        if type_transaction == 'vente' and quantite > produit.quantite_stock:
            return render(request, 'inventaire/erreur_commande.html', {'message': "Stock insuffisant."})

        # Créer la commande (le stock est géré dans le modèle Commande)
        statut = request.POST['statut']

        Commande.objects.create(
            produit=produit,
            type=type_transaction,
            quantite=quantite,
            montant_total=produit.prix * quantite,
            statut=statut,
            utilisateur=utilisateur
        )
        return redirect('liste_commandes')

    produits = Produit.objects.all()
    return render(request, 'inventaire/enregistrer_commande.html', {'produits': produits})

# Rapport par produit (quantité uniquement)
def rapport_ventes(request):
    vendeur_filter = request.GET.get('vendeur', '')
    
    commandes = Commande.objects.filter(type='vente')
    
    if vendeur_filter:
        commandes = commandes.filter(produit__vendeur=vendeur_filter)
    produits_ventes = Commande.objects.filter(type='vente') \
    .values('produit__nom', 'produit__vendeur') \
    .annotate(
        total_ventes=Sum('quantite'),
        total_vente_montant=Sum('montant_total')
    ) \
    .order_by('-total_ventes')

    vendeurs = Produit.objects.values_list('vendeur', flat=True).distinct()

    


    produits_achats = Commande.objects.filter(type='achat') \
    .values('produit__nom', 'produit__vendeur') \
    .annotate(
        total_achats=Sum('quantite'),
        total_achat_montant=Sum('montant_total')
    ) \
    .order_by('-total_achats')
    stocks = Produit.objects.all().values('nom', 'quantite_stock')

    return render(request, 'inventaire/rapport_ventes.html', {
        'produits_ventes': produits_ventes,
        'produits_achats': produits_achats,
        'stocks': stocks,
        'vendeurs': vendeurs,
        'vendeur_filter': vendeur_filter,
    })

# ✅ Rapport global (montant total des ventes/achats)
def rapport_global(request):
    periode = request.GET.get('periode', 'mois')
    if periode == 'semaine':
        date_min = datetime.now() - timedelta(days=7)
    elif periode == 'mois':
        date_min = datetime.now() - timedelta(days=30)
    else:
        date_min = datetime.min

    total_ventes = Commande.objects.filter(
        type='vente', date__gte=date_min
    ).aggregate(montant=Sum('montant_total'))['montant'] or 0

    total_achats = Commande.objects.filter(
        type='achat', date__gte=date_min
    ).aggregate(montant=Sum('montant_total'))['montant'] or 0

    return render(request, 'inventaire/rapport_global.html', {
        'total_ventes': total_ventes,
        'total_achats': total_achats,
        'periode': periode
    })

# ✅ Rapport par produit (montant € par produit)
def rapport_par_produit(request):
    produits = Produit.objects.all()
    data = []

    for produit in produits:
        total_ventes = Commande.objects.filter(type='vente', produit=produit).aggregate(
            montant=Sum('montant_total'))['montant'] or 0
        total_achats = Commande.objects.filter(type='achat', produit=produit).aggregate(
            montant=Sum('montant_total'))['montant'] or 0

        data.append({
            'nom': produit.nom,
            'achats': total_achats,
            'ventes': total_ventes
        })

    return render(request, 'inventaire/rapport_par_produit.html', {'data': data})
# ✅ Rapport complet : global, par produit, par date, filtré
def rapport_complet(request):
    periode = request.GET.get('periode', 'mois')
    if periode == 'semaine':
        date_min = datetime.now() - timedelta(days=7)
    elif periode == 'mois':
        date_min = datetime.now() - timedelta(days=30)
    else:
        date_min = datetime.min

    commandes_filtrees = Commande.objects.filter(date__gte=date_min)

    # Montants globaux
    total_achats = commandes_filtrees.filter(type='achat').aggregate(total=Sum('montant_total'))['total'] or 0
    total_ventes = commandes_filtrees.filter(type='vente').aggregate(total=Sum('montant_total'))['total'] or 0

    # Montants par produit
    details_par_produit = []
    produits = Produit.objects.all()

    for produit in produits:
        montant_achat = commandes_filtrees.filter(type='achat', produit=produit).aggregate(total=Sum('montant_total'))['total'] or 0
        montant_vente = commandes_filtrees.filter(type='vente', produit=produit).aggregate(total=Sum('montant_total'))['total'] or 0

        if montant_achat > 0 or montant_vente > 0:
            details_par_produit.append({
                'produit': produit.nom,
                'vendeur': produit.vendeur,
                'achat': montant_achat,
                'vente': montant_vente,
            })

    # Liste datée
    achats = commandes_filtrees.filter(type='achat').order_by('-date')
    ventes = commandes_filtrees.filter(type='vente').order_by('-date')
    # Statistiques des statuts (en cours / terminée / annulée)
    statuts = commandes_filtrees.values('statut').annotate(total=Count('id'))
    statut_labels = [dict(Commande.STATUT_CHOICES).get(s['statut'], s['statut']) for s in statuts]
    statut_data = [s['total'] for s in statuts]

    statut_labels_json = json.dumps(statut_labels)
    statut_data_json = json.dumps(statut_data)

    return render(request, 'inventaire/rapport_complet.html', {
        'periode': periode,
        'total_achats': total_achats,
        'total_ventes': total_ventes,
        'details_par_produit': details_par_produit,
        'achats': achats,
        'ventes': ventes,
        'statut_labels': statut_labels_json,
        'statut_data': statut_data_json

    })
def a_propos(request):
    return render(request, 'inventaire/a_propos.html')

def modifier_statut_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in dict(Commande.STATUT_CHOICES):
            commande.statut = nouveau_statut
            commande.save()
            return redirect('liste_commandes')

    return render(request, 'inventaire/modifier_statut_commande.html', {'commande': commande})

@login_required
def gestion_stock(request):
    produits = Produit.objects.all()
    for p in produits:
        if p.quantite_stock < p.seuil_min:
            messages.error(request, f"Stock bas pour « {p.nom} » ({p.quantite_stock} < {p.seuil_min})")
    return render(request, 'inventaire/gestion_stock.html', {
        'produits': produits
    })

@login_required
def evolution_stock(request):
    produits = Produit.objects.all()
    produit_id = request.GET.get('produit')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    historique = []
    if produit_id and date_debut and date_fin:
        p = get_object_or_404(Produit, pk=produit_id)
        commandes = Commande.objects.filter(
            produit=p,
            date__range=[date_debut, date_fin]
        ).order_by('date')
        solde = p.quantite_stock
        for c in commandes:
            historique.append({
                'date': c.date.strftime('%Y-%m-%d'),
                'stock': solde
            })
            solde += c.quantite if c.type == 'achat' else -c.quantite

    context = {
        'produits': produits,
        'historique': json.dumps(historique),
        'selected': produit_id or '',
        'debut': date_debut or '',
        'fin': date_fin or '',
    }
    return render(request, 'inventaire/evolution_stock.html', context)
