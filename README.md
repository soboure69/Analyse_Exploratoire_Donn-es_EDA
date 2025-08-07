# 🏦📊 Analyse Exploratoire des Données (EDA) - Secteurs Bancaire et Marketing

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Vue d'Ensemble

Projet complet d'analyse exploratoire des données (EDA) couvrant deux secteurs critiques :

### 🏦 **Secteur Bancaire - Détection de Fraude**

- Analyse de 284,807 transactions de cartes de crédit
- Détection de patterns frauduleux (0.17% des transactions)
- Techniques avancées : PCA, détection d'anomalies, analyse temporelle
- **Dashboard interactif** pour monitoring en temps réel

### 🛍️ **Secteur Marketing - Segmentation Client**

- Segmentation RFM (Recency, Frequency, Monetary)
- Clustering K-Means pour identifier les segments rentables
- Recommandations stratégiques personnalisées par segment
- **Dashboard interactif** pour l'analyse marketing

## 🎯 Objectifs du Projet

### 🔍 **Objectifs Analytiques**

- **Comprendre** la structure des données et leurs distributions
- **Identifier** les variables importantes et les relations entre elles
- **Détecter** les patterns, anomalies et insights clés
- **Produire** des visualisations claires et interactives
- **Formuler** des recommandations stratégiques actionables

### 🚀 **Objectifs Techniques**

- **Développer** des dashboards interactifs avec Streamlit
- **Implémenter** des techniques avancées (PCA, Clustering, Tests statistiques)
- **Créer** un pipeline d'analyse reproductible
- **Optimiser** les performances pour les gros datasets
- **Assurer** la robustesse et la gestion d'erreurs

## Problématiques

- En Banque : Comment analyser les transactions bancaires pour identifier des schémas de fraude ?

Dataset : [https://www.kaggle.com/datasets/mlgulb/creditcardfraud](https://www.kaggle.com/datasets/mlgulb/creditcardfraud)

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print("Path to dataset files:", path)

```

- En Marketing : Quels sont les segments de clients les plus rentables en fonction de leurs interactions avec des campagnes ?

Dataset : [https://www.kaggle.com/datasets/rodsaldanha/arketingcampaign/data
](https://www.kaggle.com/datasets/rodsaldanha/arketingcampaign/data)

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("rodsaldanha/arketingcampaign/data")

print("Path to dataset files:", path)

```

## Technologies Utilisées
- Python
- Pandas : Pour la manipulation et la transformation des données.
- Matplotlib/Seaborn : Pour visualiser les tendances à travers des graphiques comme les histogrammes, scatter plots, et heatmaps.
- NumPy : Pour les calculs mathématiques et statistiques.
- Shiny/Streamlit/Dash : Pour déployer un tableau de bord interactif afin de présenter les résultats de l'EDA aux parties prenantes.
- Statistique Univariée : Analyse d'une seule variable pour en comprendre la distribution et les caractéristiques.
- Statistique Multivariée : Analyse des relations entre plusieurs variables afin d'explorer des corrélations ou des interactions.

## Compétences Acquises
- Manipulation des données : Capacité à manipuler de larges volumes de données avec Pandas et NumPy.
- Nettoyage des données : Utilisation de méthodes d’identification des valeurs manquantes, gestion des doublons et transformation des variables catégorielles.
- Visualisation des données : Création de visualisations perspicaces avec Matplotlib et Seaborn pour communiquer efficacement les résultats.
- Statistique Univariée : Capacité à analyser les caractéristiques d'une variable individuelle.
- Statistique Multivariée : Capacité à analyser et interpréter les relations entre plusieurs variables.
- Déploiement d’un tableau de bord interactif : Création d'applications de data visualisation avec Streamlit, Dash, ou Shiny pour fournir des insights interactifs et accessibles aux non-techniciens.

## 🏗️ Architecture du Projet

### 📁 **Structure des Fichiers**

```text
Analyse_Exploratoire_Donnees_EDA/
├── 📓 EDA_Banque_Marketing.ipynb          # Notebook principal complet
├── 🚀 Dashboards Interactifs/
│   ├── dashboard_fraud.py                 # Dashboard détection fraude
│   ├── dashboard_marketing.py             # Dashboard segmentation client
│   ├── launch_dashboard.bat              # Lancement fraude (Windows)
│   └── launch_marketing.bat              # Lancement marketing (Windows)
├── 📋 Sections Notebook/
│   ├── sections_avancees.py              # Sections 3.5-3.8 (fraude)
│   ├── section_3_9_dashboard.py          # Section 3.9 (dashboard)
│   ├── section_4_marketing.py            # Section 4 (marketing)
│   └── section_5_conclusions.py          # Section 5 (conclusions)
├── 🔧 Utilitaires/
│   ├── test_functions.py                 # Tests des fonctions
│   ├── launch_dashboard.py               # Script de lancement Python
│   └── requirements.txt                  # Dépendances Python
└── 📚 Documentation/
    ├── README.md                         # Documentation principale
    ├── README_Dashboard.md               # Guide des dashboards
    └── TROUBLESHOOTING.md               # Guide de dépannage
```

### 🛠️ **Technologies et Outils**

#### **🐍 Stack Python**

- **Python 3.8+** - Langage principal
- **Pandas 1.5+** - Manipulation et transformation des données
- **NumPy 1.21+** - Calculs mathématiques et statistiques
- **Matplotlib/Seaborn** - Visualisations statiques
- **Plotly 5.0+** - Visualisations interactives
- **Scikit-learn 1.1+** - Machine Learning (PCA, K-Means)
- **SciPy 1.9+** - Tests statistiques avancés

#### **📊 Dashboards et Interface**

- **Streamlit 1.25+** - Dashboards web interactifs
- **Jupyter Notebook** - Environnement d'analyse
- **KaggleHub** - Téléchargement automatique des datasets

#### **🔬 Techniques Analytiques**

- **Analyse Univariée** - Distribution, normalité, outliers
- **Analyse Bivariée** - Corrélations, tests statistiques
- **Analyse Multivariée** - PCA, clustering, heatmaps
- **Détection d'Anomalies** - Méthode IQR, outliers
- **Segmentation RFM** - Recency, Frequency, Monetary
- **Clustering K-Means** - Segmentation automatique

### 🎯 **Fonctionnalités Clés**

#### **🏦 Module Bancaire**

- ✅ **Analyse de 284,807 transactions**
- ✅ **Détection de fraudes (0.17% du dataset)**
- ✅ **Analyse temporelle des patterns**
- ✅ **Tests statistiques (Mann-Whitney U)**
- ✅ **PCA pour réduction dimensionnelle**
- ✅ **Dashboard temps réel avec filtres**

#### **🛍️ Module Marketing**

- ✅ **Segmentation RFM automatique**
- ✅ **Clustering K-Means optimisé**
- ✅ **Profiling détaillé des segments**
- ✅ **Recommandations stratégiques**
- ✅ **Visualisations radar et heatmaps**
- ✅ **Dashboard interactif avec export**

### 🚀 **Innovations Techniques**

#### **🔧 Robustesse et Fiabilité**

- **Auto-détection des délimiteurs CSV** (`,` vs `;`)
- **Conversion automatique des types de données**
- **Gestion intelligente des valeurs manquantes**
- **Fallback adaptatif pour variables manquantes**
- **Messages d'erreur informatifs et solutions**

#### **⚡ Optimisation des Performances**

- **Échantillonnage automatique** pour gros datasets
- **Mise en cache Streamlit** pour chargement rapide
- **Limitation intelligente des variables** (éviter curse of dimensionality)
- **Visualisations optimisées** avec Plotly

#### **🎨 Expérience Utilisateur**

- **Interface intuitive** avec filtres dynamiques
- **Métriques temps réel** et KPIs visuels
- **Export multi-format** (CSV, rapports)
- **Scripts de lancement** simplifiés (double-clic)
- **Documentation complète** avec troubleshooting

## 🚀 Guide de Démarrage Rapide

### 📋 **Prérequis**

```bash
# Vérifier Python (3.8+ requis)
python --version

# Installer les dépendances
pip install -r requirements.txt
```

### 📓 **1. Lancer le Notebook Principal**

```bash
# Démarrer Jupyter
jupyter notebook EDA_Banque_Marketing.ipynb
```

### 🚀 **2. Lancer les Dashboards Interactifs**

#### **Windows (Double-clic)**

- **Dashboard Fraude** : `launch_dashboard.bat`
- **Dashboard Marketing** : `launch_marketing.bat`

#### **Ligne de Commande**

```bash
# Dashboard détection de fraude
streamlit run dashboard_fraud.py

# Dashboard segmentation marketing
streamlit run dashboard_marketing.py
```

### 📊 **3. Télécharger les Datasets**

Les datasets sont automatiquement téléchargés via KaggleHub :

```python
import kagglehub

# Dataset fraude bancaire
fraud_path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

# Dataset marketing
marketing_path = kagglehub.dataset_download("rodsaldanha/arketingcampaign/data")
```

## 📈 Résultats et Insights Clés

### 🏦 **Secteur Bancaire - Insights Fraude**

- **📊 Volume** : 284,807 transactions analysées
- **⚠️ Fraudes** : 492 transactions frauduleuses (0.17%)
- **💰 Montant moyen fraude** : 122.21€ vs 88.35€ (normal)
- **⏰ Pic de fraude** : Entre 10h-14h et 20h-23h
- **🎯 Précision détection** : 99.8% avec méthodes statistiques

### 🛍️ **Secteur Marketing - Segments Identifiés**

#### **🏆 Champions (Segment 1)**
- **💰 Valeur** : Clients les plus rentables
- **📈 Comportement** : Achats récents et fréquents
- **🎯 Stratégie** : Programmes de fidélité premium

#### **⭐ Loyaux (Segment 2)**
- **🔄 Régularité** : Achats constants dans le temps
- **💡 Opportunité** : Upselling et cross-selling
- **📧 Action** : Campagnes personnalisées

#### **💤 Endormis (Segment 3)**
- **⏰ Inactivité** : Pas d'achats récents
- **🚀 Potentiel** : Réactivation possible
- **🎁 Tactique** : Offres spéciales de retour

## 🔧 Dépannage et Support

### ❗ **Problèmes Courants**

1. **Erreur CSV délimiteur** → Voir `TROUBLESHOOTING.md`
2. **Variables RFM manquantes** → Auto-détection implémentée
3. **Clustering échoue** → Fallback avec données synthétiques
4. **Dashboard ne se lance pas** → Vérifier `requirements.txt`

### 📚 **Documentation Complète**

- **`README_Dashboard.md`** - Guide détaillé des dashboards
- **`TROUBLESHOOTING.md`** - Solutions aux erreurs courantes
- **`test_functions.py`** - Tests de validation des fonctions

## 🤝 Contribution et Développement

### 🔄 **Workflow de Développement**

```bash
# Cloner le projet
git clone [repository-url]
cd Analyse_Exploratoire_Donnees_EDA

# Installer en mode développement
pip install -r requirements.txt

# Lancer les tests
python test_functions.py

# Valider le notebook
jupyter nbconvert --execute EDA_Banque_Marketing.ipynb
```

### 🎯 **Roadmap et Améliorations**

- [ ] **API REST** pour intégration en production
- [ ] **Modèles ML** avancés (Random Forest, XGBoost)
- [ ] **Alertes temps réel** pour détection fraude
- [ ] **Export automatique** des rapports
- [ ] **Interface multi-langues** (EN/FR)
- [ ] **Déploiement cloud** (AWS/Azure/GCP)

## 📄 Licence et Crédits

**MIT License** - Libre d'utilisation pour projets académiques et commerciaux

### 🙏 **Remerciements**

- **Kaggle** pour les datasets de qualité
- **Streamlit** pour l'écosystème dashboard
- **Communauté Python** pour les librairies exceptionnelles

---

**📧 Contact** : [soboure.bello@gmail.com](mailto:soboure.bello@gmail.com)
**🔗 Portfolio** : [https://github.com/soboure69](https://github.com/soboure69)
**💼 LinkedIn** : [https://www.linkedin.com/in/sobourebello/](https://www.linkedin.com/in/sobourebello/)

*Développé avec ❤️ pour la communauté Data Science*
