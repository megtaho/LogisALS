from django.db import models

# Modèle Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)  # Le nom du produit
    description = models.TextField()        # La description du produit
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Le prix du produit
    quantite_stock = models.PositiveIntegerField()  # La quantité en stock

    def __str__(self):
        return self.nom  # Renvoie le nom du produit dans l'admin Django

# Modèle Utilisateur
class Utilisateur(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('employe', 'Employé'),
    ]
    nom = models.CharField(max_length=100)  # Le nom de l'utilisateur
    email = models.EmailField()             # L'email de l'utilisateur
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # Le rôle de l'utilisateur (admin ou employé)

    def __str__(self):
        return self.nom  # Renvoie le nom de l'utilisateur dans l'admin Django

# Modèle Commande
class Commande(models.Model):
    TYPE_CHOICES = [
        ('achat', 'Achat'),
        ('vente', 'Vente'),
    ]
    STATUT_CHOICES = [
        ('en_cours', 'En Cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # Type de la commande (achat ou vente)
    date = models.DateField()  # La date de la commande
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)  # Le montant total de la commande
    quantite = models.PositiveIntegerField()  # La quantité de produits commandés
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)  # Le statut de la commande (en cours, terminée, annulée)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)  # Le produit associé à la commande
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)  # L'utilisateur qui a effectué la commande

    def __str__(self):
        return f'{self.type} - {self.produit.nom}'  # Affiche le type de commande et le nom du produit

# Modèle Rapport
class Rapport(models.Model):
    TYPE_CHOICES = [
        ('vente', 'Vente'),
        ('stock', 'Stock'),
        ('reapprovisionnement', 'Réapprovisionnement'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # Le type de rapport (vente, stock, réapprovisionnement)
    date_generation = models.DateField()  # La date de génération du rapport
    resume = models.TextField()  # Le résumé du rapport

    def __str__(self):
        return f'Rapport {self.type} - {self.date_generation}'  # Affiche le type et la date de génération du rapport