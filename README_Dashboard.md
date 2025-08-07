# 🏦 Tableau de Bord Interactif - Détection de Fraudes Bancaires

## 📋 Description

Ce tableau de bord interactif permet d'analyser et de visualiser les données de fraudes bancaires de manière dynamique et intuitive. Il offre une interface web moderne pour explorer les patterns de fraude, analyser les distributions temporelles et détecter les anomalies.

## ✨ Fonctionnalités

### 📊 Vue d'ensemble
- **Métriques clés** : Nombre total de transactions, fraudes détectées, taux de fraude
- **Visualisations** : Graphiques en secteurs, histogrammes, distributions
- **Filtrage dynamique** : Par montant, période temporelle, taille d'échantillon

### ⏰ Analyse Temporelle
- **Patterns horaires** : Distribution des fraudes par heure
- **Tendances** : Évolution du taux de fraude dans le temps
- **Heatmaps** : Visualisation des pics d'activité frauduleuse

### 💰 Analyse des Montants
- **Comparaisons** : Statistiques entre transactions normales et frauduleuses
- **Visualisations** : Box plots, violin plots, distributions
- **Tests statistiques** : Mann-Whitney U pour la significativité

### 🔍 Détection d'Anomalies
- **Outliers** : Détection automatique par méthode IQR
- **Métriques** : Taux d'outliers, concentration de fraudes
- **Visualisations** : Scatter plots, histogrammes avec outliers

### 📥 Export de Données
- **CSV filtré** : Export des données selon les filtres appliqués
- **Rapport d'outliers** : Export des anomalies détectées
- **Rapport statistique** : Résumé complet de l'analyse

## 🚀 Installation et Lancement

### Méthode 1 : Lancement automatique (Windows)
```bash
# Double-cliquez sur le fichier
launch_dashboard.bat
```

### Méthode 2 : Lancement via Python
```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement du dashboard
streamlit run dashboard_fraud.py
```

### Méthode 3 : Script de lancement Python
```bash
python launch_dashboard.py
```

## 📦 Dépendances

Le dashboard nécessite les packages Python suivants :

```
streamlit>=1.25.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.0.0
seaborn>=0.11.0
matplotlib>=3.5.0
scipy>=1.9.0
scikit-learn>=1.1.0
```

## 📁 Structure des Fichiers

```
Analyse_Exploratoire_Donnees_EDA/
├── dashboard_fraud.py          # Application Streamlit principale
├── launch_dashboard.py         # Script de lancement Python
├── launch_dashboard.bat        # Script de lancement Windows
├── requirements.txt            # Dépendances Python
├── README_Dashboard.md         # Documentation du dashboard
└── creditcard.csv             # Dataset (à placer ici)
```

## 🔧 Configuration

### Données
- Placez le fichier `creditcard.csv` dans le répertoire du projet
- Le dashboard détecte automatiquement le fichier de données
- Format attendu : CSV avec colonnes `Class` (cible) et `Amount`, `Time` (optionnelles)

### Paramètres
- **Port** : 8501 (par défaut)
- **Mode** : Interface web locale
- **Performance** : Échantillonnage automatique pour les gros datasets

## 🎯 Utilisation

1. **Lancement** : Utilisez une des méthodes de lancement ci-dessus
2. **Navigation** : Le dashboard s'ouvre automatiquement dans votre navigateur
3. **Filtrage** : Utilisez la barre latérale pour ajuster les filtres
4. **Exploration** : Naviguez entre les onglets pour différentes analyses
5. **Export** : Téléchargez les résultats via les boutons d'export

## 📊 Onglets Disponibles

### 📊 Vue d'ensemble
- Répartition des types de transactions
- Distribution générale des montants
- Métriques de base

### ⏰ Analyse Temporelle
- Patterns de fraude par heure
- Évolution temporelle des taux
- Heatmaps d'activité

### 💰 Analyse des Montants
- Comparaisons statistiques détaillées
- Visualisations de distributions
- Tests de significativité

### 🔍 Détection d'Anomalies
- Identification automatique des outliers
- Analyse de la concentration de fraudes
- Visualisations des anomalies

## ⚡ Performance

- **Échantillonnage** : Limitation automatique pour les gros datasets
- **Mise en cache** : Optimisation du chargement des données
- **Réactivité** : Interface responsive et fluide

## 🛠️ Dépannage

### Problèmes Courants

**Dashboard ne se lance pas :**
- Vérifiez que Python est installé
- Installez les dépendances : `pip install -r requirements.txt`
- Vérifiez que le port 8501 est libre

**Données non trouvées :**
- Placez le fichier `creditcard.csv` dans le répertoire
- Vérifiez les permissions de lecture du fichier

**Performance lente :**
- Réduisez la taille d'échantillon dans la barre latérale
- Appliquez des filtres pour limiter les données

### Messages d'Erreur

- **"Fichier de données non trouvé"** : Placez `creditcard.csv` dans le répertoire
- **"Colonne cible non trouvée"** : Vérifiez que la colonne `Class` existe
- **"Port déjà utilisé"** : Fermez les autres instances ou changez le port

## 🔮 Fonctionnalités Avancées

### Personnalisation
- Modifiez `dashboard_fraud.py` pour adapter les visualisations
- Ajustez les seuils de détection d'anomalies
- Personnalisez les couleurs et le style

### Extension
- Ajoutez de nouveaux onglets d'analyse
- Intégrez des modèles de machine learning
- Connectez à d'autres sources de données

## 📞 Support

Pour toute question ou problème :
1. Consultez cette documentation
2. Vérifiez les logs dans le terminal
3. Assurez-vous que toutes les dépendances sont installées

## 📄 Licence

Ce projet est développé dans le cadre d'une analyse exploratoire des données bancaires pour la détection de fraudes.

---

**🎯 Objectif** : Fournir un outil interactif et intuitif pour l'analyse des fraudes bancaires, permettant une exploration approfondie des données et une détection efficace des patterns suspects.
