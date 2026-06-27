# Modèles Django et feuille de route

## 1. Objectif
Ce document décrit la structure des modèles du projet `clinique` et propose une feuille de route pour le développement des fonctionnalités principales.

## 2. Structure des modèles

### accounts.Profile
- Utilise un `OneToOneField` vers `auth.User`
- Définit un rôle (`ADMIN`, `DOCTOR`, `RECEPTIONIST`)
- Stocke le téléphone, la photo et la date de création

### patients.Patient
- Informations personnelles du patient
- Genre, téléphone, email, adresse, groupe sanguin
- Champ `created_at` pour la date d'enregistrement

### doctors.Doctor
- Informations du médecin
- Nom, spécialité, téléphone, email, bureau

### appointments.Appointment
- Relation avec `Patient` et `Doctor`
- Date, heure, raison et statut (`Pending`, `Confirmed`, `Cancelled`, `Completed`)
- `created_at` pour l’historique

### consultations.Consultation
- `OneToOneField` vers `Appointment`
- Diagnostic, traitement, observation
- `consultation_date` horodatée automatiquement

### medicines.Medicine
- Nom, description, fabricant
- Forme galénique, concentration
- Quantité en stock, prix, date de péremption
- Chaines `created_at` et `updated_at`

### prescriptions.Prescription
- Relation `ForeignKey` vers `Consultation`
- Relation `ForeignKey` vers `Medicine`
- Dosage, fréquence, durée

### billing.Invoice
- `OneToOneField` vers `Consultation`
- Montant, statut (`UNPAID`, `PAID`, `PARTIAL`)
- `created_at`

### payements.Payment
- Relation `ForeignKey` vers `Invoice`
- Montant et mode de paiement (`CASH`, `CARD`, `MOBILE`)
- `payment_date`

## 3. Correctifs appliqués
- Correction de l’import incorrect dans `payements/models.py` :
  - avant : `from .models import Invoice`
  - après : `from billing.models import Invoice`
- Suppression de l’entrée invalide `prescription` dans `clinique/settings.py`

## 4. Prochaines étapes (roadmap)

1. Migrer la base de données
   - `python manage.py makemigrations`
   - `python manage.py migrate`

2. Ajouter les modèles au panneau d’administration
   - Enregistrer `Patient`, `Doctor`, `Appointment`, `Consultation`, `Medicine`, `Prescription`, `Invoice`, `Payment`

3. Créer des jeux de données de test
   - Fixtures ou scripts de création de données
   - Vérifier la cohérence des relations entre patients, rendez-vous, consultations, ordonnances et factures

4. Construire les vues / API
   - CRUD pour patients, médecins, médicaments
   - Processus de rendez-vous et de consultation
   - Création d’ordonnances
   - Génération et paiement des factures

5. Gestion du stock de médicaments
   - Mettre à jour `quantity_in_stock` après vente ou prescription
   - Ajouter alertes pour stock faible et péremption

6. Gestion des utilisateurs et des rôles
   - Restreindre l’accès aux médecins et aux réceptionnistes
   - Autoriser uniquement les administrateurs à gérer les factures et les paiements

7. Tests et validation
   - Tests unitaires Django sur les modèles
   - Validation des champs critiques (prix, quantités, dates)

8. Déploiement
   - Configuration des paramètres de production
   - Sécurisation des informations sensibles

## 5. Remarques
- L’application `app` peut rester vide si elle n’a pas de modèles spécifiques.
- Le projet doit garder une architecture claire : chaque app gère un domaine métier distinct.
