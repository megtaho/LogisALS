from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.PositiveIntegerField()
    quantite_stock = models.PositiveIntegerField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    seuil_min = models.PositiveIntegerField(default=5)  # seuil critique
    seuil_max = models.PositiveIntegerField(default=100)  # stock idéal  # 
    vendeur = models.CharField(max_length=100, blank=True, null=True)  

    def statut_stock(self):
        if self.quantite_stock <= self.seuil_min:
            return 'bas'
        elif self.quantite_stock >= self.seuil_max:
            return 'haut'
        else:
            return 'normal'

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if self.quantite_stock < 0:
            raise ValueError("La quantité en stock ne peut pas être négative.")
        super().save(*args, **kwargs)


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('employe', 'Employé'),
    ]
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.nom  # Corrigé : self.nom au lieu de self.user.nom


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
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} - {self.produit.nom}'

    def save(self, *args, **kwargs):
        if self.quantite < 0:
            raise ValueError("La quantité de la commande ne peut pas être négative.")

        if self.type == 'vente':
            if self.quantite > self.produit.quantite_stock:
                raise ValueError("La quantité demandée est supérieure au stock disponible.")
            self.produit.quantite_stock -= self.quantite
        elif self.type == 'achat':
            self.produit.quantite_stock += self.quantite

        self.produit.save()
        super().save(*args, **kwargs)


class Rapport(models.Model):
    TYPE_CHOICES = [
        ('vente', 'Vente'),
        ('stock', 'Stock'),
        ('reapprovisionnement', 'Réapprovisionnement'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_generation = models.DateField()
    resume = models.TextField()
    statut = models.CharField(
        max_length=15,
        choices=[
            ('en_attente', 'En Attente'),
            ('termine', 'Terminé')
        ],
        default='en_attente'
    )

    def __str__(self):
        return f'Rapport {self.type} - {self.date_generation}'
