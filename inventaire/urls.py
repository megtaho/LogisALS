from django.urls import path
from . import views  # Importer les vues depuis le fichier views.py

urlpatterns = [
    # Route pour afficher la liste des produits
    path('produits/', views.liste_produits, name='liste_produits'),  

    # Route pour afficher la liste des commandes
    path('commandes/', views.liste_commandes, name='liste_commandes'),
    path('commande/enregistrer/', views.enregistrer_commande, name='enregistrer_commande'),


    # Route pour afficher les rapports
    path('rapports/', views.rapport_ventes, name='rapport_ventes'),
    path('rapports/complet/', views.rapport_complet, name='rapport_complet'),


    path('produit/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produit/modifier/<int:pk>/', views.modifier_produit, name='modifier_produit'),
    path('produit/supprimer/<int:pk>/', views.supprimer_produit, name='supprimer_produit'),
    

    path('commande/<int:pk>/modifier-statut/', views.modifier_statut_commande, name='modifier_statut_commande'),
    path('stocks/', views.gestion_stock, name='gestion_stock'),

    path('a-propos/', views.a_propos, name='a_propos'),


]
