from django.urls import path
from . import views  # Importer les vues depuis le fichier views.py

urlpatterns = [
    # Route pour afficher la liste des produits
    path('produits/', views.liste_produits, name='liste_produits'),  

    # Route pour afficher la liste des commandes
    path('commandes/', views.liste_commandes, name='liste_commandes'),

    # Route pour afficher la liste des rapports
    path('rapports/', views.liste_rapports, name='liste_rapports'),
]
