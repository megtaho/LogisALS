LogisALS – Gestion de Stock et de Commandes

LogisALS est une application web de gestion de stock et de commandes, conçue avec Django 5.2. Elle permet de suivre les produits, d’enregistrer des achats et ventes, de générer des rapports, et de gérer le stock en temps réel. Idéal pour les TPE/PME.

Fonctionnalités

- Ajout, modification, suppression de produits
- Enregistrement des commandes (achats / ventes)
- Suivi de stock avec seuils d’alerte
- Gestion des statuts de commande
- Rapports détaillés : par produit, par vendeur, par période
- Graphiques de ventes et performances

Technologies

- Python 3.12
- Django 5.2
- SQLite (par défaut)
- Bootstrap 5 + Chart.js

Installation rapide

```bash
git clone https://github.com/megtaho/LogisALS.git
cd LogisALS
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Manuel utilisateur

[![Voir la vidéo](https://img.youtube.com/vi/ID_YOUTUBE/maxresdefault.jpg)](https://youtu.be/E5V-TxTaRu0)

👉 Cliquez sur l’image pour regarder le manuel utilisateur.

Structure du projet

```bash
LogisALS/
├── inventaire/           # Application principale
│   ├── models.py         # Modèles (Produit, Commande, Utilisateur)
│   ├── views.py          # Vues logiques
│   ├── forms.py          # Formulaires Django
│   ├── templates/        # HTML frontend (Bootstrap)
│   ├── urls.py           # Routes internes
├── LogisALS/             # Réglages Django
│   ├── settings.py       # Configuration du projet
├── db.sqlite3            # Base de données locale
├── manage.py             # Entrée CLI du projet
```

Sécurité

- Authentification requise pour accéder aux données sensibles
- Protection CSRF pour tous les formulaires
- Rôles utilisateurs gérés via un modèle personnalisé


Contribution

1. Fork le dépôt
2. Crée une branche `feature/...`
3. Soumets une Pull Request

## 📄 Licence

MIT – voir `LICENSE`.

---

Développé avec ❤️ par [megtaho](https://github.com/megtaho)   
