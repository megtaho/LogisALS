from django.contrib import admin
from .models import Produit, Utilisateur, Commande, Rapport

admin.site.register(Produit)
admin.site.register(Utilisateur)
admin.site.register(Commande)
admin.site.register(Rapport)
