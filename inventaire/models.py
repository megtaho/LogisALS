from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Modèle Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)  # Le nom du produit
    description = models.TextField()        # La description du produit
    prix = models.PositiveIntegerField()  # Le prix du produit
    quantite_stock = models.PositiveIntegerField()  # La quantité en stock

    def __str__(self):
        return self.nom  # Renvoie le nom du produit dans l'admin Django
    
    def save(self, *args, **kwargs):
        if self.quantite_stock < 0:
            raise   ValueError("la quantité en stock ne peut pas être négative")
        super(Produit, self).save(*args, **kwargs)

# Modèle Utilisateur
class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('employe', 'Employé'),
    ]
    nom = models.CharField(max_length=100)  # Le nom de l'utilisateur
    email = models.EmailField()             # L'email de l'utilisateur
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # Le rôle de l'utilisateur (admin ou employé)

    def __str__(self):
        return self.user.nom  # Renvoie le nom de l'utilisateur dans l'admin Django

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
    date = models.DateTimeField(default=timezone.now)  # La date de la commande
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)  # Le montant total de la commande
    quantite = models.PositiveIntegerField()  # La quantité de produits commandés
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)  # Le statut de la commande (en cours, terminée, annulée)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)  # Le produit associé à la commande
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)  # L'utilisateur qui a effectué la commande

    def __str__(self):
        return f'{self.type} - {self.produit.nom}'  # Affiche le type de commande et le nom du produit
    
    def save(self, *args, **kwargs):
        # Empêcher de sauver une commande avec une quantité en stock négative
        if self.quantite < 0:
            raise ValueError("La quantité de la commande ne peut pas être négative.")
        
        # Vérification du type de transaction (achat ou vente)
        if self.type == 'vente':
            # Vérifier que le stock est suffisant pour la vente
            if self.quantite > self.produit.quantite_stock:
                raise ValueError("La quantité demandée est supérieure au stock disponible.")
            
            # Réduire le stock pour la vente
            self.produit.quantite_stock -= self.quantite

        elif self.type == 'achat':
            # Augmenter le stock pour l'achat
            self.produit.quantite_stock += self.quantite
        
        # Sauvegarder les changements du produit
        self.produit.save()

        # Appeler la méthode save() de la commande après avoir modifié le stock
        super().save(*args, **kwargs)


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
    statut = models.CharField(max_length=15, choices=[('en_attente', 'En Attente'), ('termine', 'Terminé')], default='en_attente')  # Statut du rapport

    def __str__(self):
        return f'Rapport {self.type} - {self.date_generation}'  # Affiche le type et la date de génération du rapport